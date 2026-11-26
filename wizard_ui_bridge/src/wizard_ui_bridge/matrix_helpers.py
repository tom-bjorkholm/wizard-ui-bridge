#! /usr/local/bin/python3
"""Helpers shared by the bridges that show a matrix form question.

A bridge builds the cells of a matrix form from the MatrixCellSpec of the
request with cell_at(), applies the prefills of a partial validator with
valid_cell_prefills(), and names a cell in its own message with
message_name(), which uses the CellNamer of the request and falls back
to cell_name(). A bridge asking one cell at a time names it with
row_name() and column_name(). The cells of the current shape are given
to all but cell_at() as a grid of AskCells, one sequence per row.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Iterable, Iterator, Optional, Sequence
from wizard_ui_bridge.form_helpers import prefill_value
from wizard_ui_bridge.matrix_cell_defs import ALL_ASK_CELL_TYPES, AskCell, \
    AskLabelCell, PrefillValueType
from wizard_ui_bridge.matrix_defs import AnswerCells, CellNamer, \
    CellPosition, MatrixCellSpec, PrefillCellValues


def cell_at(spec: MatrixCellSpec, position: CellPosition) -> AskCell:
    """Return the AskCell the specification gives for a position.

    A generator is called with the position. A 2D sequence gives the
    cell at the position, repeating its last row below the sequence and
    the last cell of a row to the right of that row, as described for
    MatrixCellSpec.

    Raises:
        ValueError: The sequence, or the row used, has no cells.
        TypeError: The specification gave no AskCell for the position.
    """
    cell = spec(position) if callable(spec) else _listed_cell(spec, position)
    if not isinstance(cell, ALL_ASK_CELL_TYPES):
        raise TypeError(f'no AskCell for matrix cell {_where(position)}')
    return cell


def _listed_cell(cells: Sequence[Sequence[AskCell]],
                 position: CellPosition) -> AskCell:
    """Return the cell of a 2D sequence, repeating the last row or cell."""
    if not cells:
        raise ValueError('a matrix cell sequence needs at least one row')
    row = cells[min(position.row, len(cells) - 1)]
    if not row:
        raise ValueError('each row of a matrix cell sequence needs a cell')
    return row[min(position.column, len(row) - 1)]


def valid_cell_prefills(cells: Sequence[Sequence[AskCell]],
                        changed: Optional[CellPosition],
                        prefill_values: PrefillCellValues
                        ) -> Iterator[tuple[CellPosition, PrefillValueType]]:
    """Yield the prefill requests a bridge should apply, validated.

    cells is the grid of the current shape and changed the cell that
    just changed, or None after a shape change. Each yielded (position,
    value) pair is ready to place into the input of that cell. The rules
    are those of PartMatrixValidationRes.prefill_values: a prefill aimed
    at the changed cell is skipped; a position outside the matrix raises
    IndexError, and a label cell or a value of the wrong type raises
    TypeError; a choice value not among the cell's choices and any
    prefill of a sensitive cell are dropped.
    """
    for pair, value in prefill_values:
        position = CellPosition(*pair)
        cell = _input_cell(cells, position)
        if position == changed:
            continue
        usable = prefill_value(cell, value, f'cell {_where(position)}')
        if usable is not None:
            yield position, usable


def _input_cell(cells: Sequence[Sequence[AskCell]],
                position: CellPosition) -> AskCell:
    """Return the input cell a prefill is aimed at, raising for a bug."""
    row, column = position
    if not (0 <= row < len(cells) and 0 <= column < len(cells[row])):
        raise IndexError(f'prefill cell {_where(position)} is outside '
                         'the matrix')
    cell = cells[row][column]
    if isinstance(cell, AskLabelCell):
        raise TypeError(f'prefill cell {_where(position)} is a label cell')
    return cell


def _where(position: CellPosition) -> str:
    """Return a 0-based position as text for an exception message."""
    return f'({position.row}, {position.column})'


def row_label(cells: Sequence[Sequence[AskCell]],
              position: CellPosition) -> Optional[str]:
    """Return the nearest label text to the left of a cell, or None.

    Labels whose text is blank, such as an empty corner, are skipped.
    """
    return _nearest_label(reversed(cells[position.row][:position.column]))


def column_label(cells: Sequence[Sequence[AskCell]],
                 position: CellPosition) -> Optional[str]:
    """Return the nearest label text above a cell, or None.

    Labels whose text is blank, such as an empty corner, are skipped.
    """
    above = [row[position.column] for row in cells[:position.row]]
    return _nearest_label(reversed(above))


def _nearest_label(cells: Iterable[AskCell]) -> Optional[str]:
    """Return the text of the first label with non-blank text, or None."""
    for cell in cells:
        if isinstance(cell, AskLabelCell) and cell.text.strip():
            return cell.text
    return None


def cell_name(cells: Sequence[Sequence[AskCell]],
              position: CellPosition) -> str:
    """Return a name of a cell for a message shown to the user.

    The name is the row label and the column label of the cell joined
    with ' / ', such as 'Bob / Tue'. Where a label is missing, the 1-based
    row or column number takes its place, such as 'Row 2 / Start date'.
    """
    return f'{row_name(cells, position)} / {column_name(cells, position)}'


def row_name(cells: Sequence[Sequence[AskCell]],
             position: CellPosition) -> str:
    """Return the row label of a cell, or its 1-based row as 'Row 2'."""
    return row_label(cells, position) or f'Row {position.row + 1}'


def column_name(cells: Sequence[Sequence[AskCell]],
                position: CellPosition) -> str:
    """Return the column label of a cell, or 'Column 3' when it has none."""
    return column_label(cells, position) or f'Column {position.column + 1}'


def message_name(namer: Optional[CellNamer], answers: AnswerCells,
                 cells: Sequence[Sequence[AskCell]],
                 position: CellPosition) -> str:
    """Return the name of a cell for a message the bridge writes itself.

    The CellNamer of the request names the cell when it is given and
    returns a non-empty name; otherwise cell_name() does.
    """
    name = '' if namer is None else namer(answers, position)
    return name or cell_name(cells, position)
