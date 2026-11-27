#! /usr/local/bin/python3
"""Ask a table question as a matrix form.

The base WizardUiBridge.ask_table() describes the table as a matrix form
with TableMatrix, asks it with ask_matrix_form() and turns the answers
back into table cells. Row 0 of the matrix is a header of bold labels,
and each table row is the matrix row below it, so table row r is matrix
row r + 1. A read-only cell of a starting row is a label, and an editable
cell is a text cell, or a choice cell when it has choices. The last row
of the cell specification is bridge_helpers.new_row_template() with every
column editable, and the matrix repeats it for each row the user appends.

A TableCell separates the value an input starts with from what an empty
cell means, and so does an Ask*Cell: the value of an editable TableCell
is the start_value of its matrix cell, and its nullable is kept. The
matrix cell has no default, so an emptied cell means what an empty
TableCell means.

The partial check of a table is asked about one cell at a time, so the
partial validator of the matrix remembers each cell the user has changed
and checks the changed cell first, then the other changed cells in row
order. The first rejection is the result, its message prefixed with the
cell name when it is about another cell than the changed one. A bridge
that blocks submitting an invalid matrix thus blocks while any changed
cell is rejected, while a cell the user has not touched, such as an
empty cell of a new row, does not complain before the user reaches it.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional, Sequence
from wizard_ui_bridge.arg_types import PartialCheck, TableCell, TableColumn
from wizard_ui_bridge.bridge_helpers import new_row_template
from wizard_ui_bridge.matrix_cell_defs import AnswerCell, \
    AnswerChoiceCell, AnswerTextCell, AskCell, AskChoiceCell, AskLabelCell, \
    AskTextCell
from wizard_ui_bridge.matrix_defs import AnswerCells, CellPosition, \
    MatrixConsoleQuestion, MatrixDimension, MatrixDimensions, \
    MatrixRequest, PartMatrixValidationRes

# A console names each cell with TableMatrix.cell_name() only.
_CONSOLE = MatrixConsoleQuestion(use_help_text=False,
                                 show_horizontal_label=False,
                                 show_vertical_label=False,
                                 use_cell_namer=True)


class TableMatrix:
    """A table question described as the cells of a matrix form."""

    def __init__(self, columns: Sequence[TableColumn],
                 cells: Sequence[Sequence[TableCell]],
                 partial_check: Optional[PartialCheck],
                 help_text: Optional[str]) -> None:
        """Build the matrix cells of the header, starting and new rows.

        Each input cell gets help_text as its help text.

        Raises:
            ValueError: A row of cells does not hold one cell per column.
        """
        if any(len(row) != len(columns) for row in cells):
            raise ValueError('each row of cells needs one TableCell per '
                             'column')
        self._columns = columns
        self._cells = cells
        self._check = partial_check
        self._edited: set[CellPosition] = set()
        header: list[AskCell] = [AskLabelCell(column.header, bold=True)
                                 for column in columns]
        starting = [_starting_row(columns, row, help_text) for row in cells]
        new_row = [_input_cell(cell, help_text)
                   for cell in new_row_template(columns, cells)]
        self.ask_cells: list[list[AskCell]] = [header, *starting, new_row]

    def request(self, question: str, min_rows: Optional[int],
                max_rows: Optional[int]) -> MatrixRequest:
        """Return the matrix request of the table.

        Raises:
            ValueError: A variable number of rows, with both min_rows and
                        max_rows given, does not satisfy 0 <= min_rows <=
                        number of starting rows <= max_rows.
        """
        validator = None if self._check is None else self._validate
        return MatrixRequest(question, self.ask_cells,
                             self._dimensions(min_rows, max_rows), _CONSOLE,
                             validator, self.cell_name)

    def values(self, answers: AnswerCells) -> list[list[Optional[str]]]:
        """Return the table of cell values that matrix answers give."""
        return [[self._value(row, column, answer)
                 for column, answer in enumerate(line)]
                for row, line in enumerate(answers[1:])]

    def cell_name(self, _answers: AnswerCells, position: CellPosition) -> str:
        """Return the name of a cell, such as 'city / Rename to'.

        The texts of the read-only cells of the row, or 'Row 2' when it
        has none, are followed by the header of the column.
        """
        line = self.ask_cells[min(position.row, len(self.ask_cells) - 1)]
        labels = [cell.text for cell in line
                  if isinstance(cell, AskLabelCell) and cell.text.strip()]
        header = self._columns[position.column].header
        return ' / '.join(labels or [f'Row {position.row}']) + f' / {header}'

    def _dimensions(self, min_rows: Optional[int],
                    max_rows: Optional[int]) -> MatrixDimensions:
        """Return the dimensions of the matrix, with its header row.

        The rows are fixed to the starting rows unless both bounds are
        given.
        """
        rows = len(self._cells)
        columns = len(self._columns)
        if min_rows is None or max_rows is None:
            return MatrixDimensions.fixed(rows + 1, columns)
        if not 0 <= min_rows <= rows <= max_rows:
            raise ValueError('a variable-row table needs 0 <= min_rows <= '
                             'number of rows in cells <= max_rows')
        return MatrixDimensions(MatrixDimension(min_rows + 1, columns),
                                MatrixDimension(max_rows + 1, columns),
                                MatrixDimension(rows + 1, columns))

    def _value(self, row: int, column: int,
               answer: Optional[AnswerCell]) -> Optional[str]:
        """Return the value of one table cell from its matrix answer.

        Only a starting row has labels, and a label keeps the value of its
        read-only TableCell.
        """
        if answer is None:
            return self._cells[row][column].value
        assert isinstance(answer, (AnswerTextCell, AnswerChoiceCell))
        return answer.value

    def _validate(self, answers: AnswerCells,
                  changed: Optional[CellPosition]) -> PartMatrixValidationRes:
        """Run the partial check on the cells the user has changed.

        changed is remembered as changed by the user, and a remembered
        cell outside the matrix, in a deleted row, is forgotten. A new row
        later appended there starts unchanged, since a bridge calls the
        validator after each change of shape. It is only used as validator
        when the table has a partial check.
        """
        assert self._check is not None
        if changed is not None:
            self._edited.add(changed)
        self._edited = {cell for cell in self._edited
                        if cell.row < len(answers)}
        table = self.values(answers)
        for position in self._check_order(changed):
            accepted, message = self._check(table, (position.row - 1,
                                                    position.column))
            if not accepted:
                named = self._message(answers, position, changed, message)
                return PartMatrixValidationRes(False, named)
        return PartMatrixValidationRes(True, '')

    def _check_order(self, changed: Optional[CellPosition]
                     ) -> list[CellPosition]:
        """Return the changed cell, then the other edited cells by row."""
        others = sorted(self._edited - {changed})
        return others if changed is None else [changed, *others]

    def _message(self, answers: AnswerCells, position: CellPosition,
                 changed: Optional[CellPosition], message: str) -> str:
        """Return the message, naming its cell unless it is the changed one."""
        if position == changed:
            return message
        return f'{self.cell_name(answers, position)}: {message}'


def _starting_row(columns: Sequence[TableColumn], row: Sequence[TableCell],
                  help_text: Optional[str]) -> list[AskCell]:
    """Return the matrix cells of one starting row of the table."""
    return [AskLabelCell(cell.value or '') if column.read_only
            else _input_cell(cell, help_text)
            for column, cell in zip(columns, row)]


def _input_cell(cell: TableCell, help_text: Optional[str]) -> AskCell:
    """Return the matrix input cell of one editable table cell."""
    if cell.choices is None:
        return AskTextCell(help_text, nullable=cell.nullable,
                           start_value=cell.value)
    return AskChoiceCell(help_text, cell.choices, nullable=cell.nullable,
                         start_value=cell.value)
