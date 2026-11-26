#! /usr/local/bin/python3
"""Ask a matrix form one cell at a time, as a console does.

The base WizardUiBridge.ask_matrix_form() cannot show a grid, so it asks
each input cell in turn with the typed ask methods of the bridge, as the
MatrixConsoleQuestion of the request directs. The cells are walked line
by line: a line is a row in row order and a column in column order, and
an item is one cell of a line.

The walk is a queue of steps: a cell, a line that turns into its cells
when it is reached (so a line asked after the width changed gets the new
width), and a resize menu. When the matrix may be resized, ask_choice()
offers a menu at two points:

- after the first line with input cells, when the number of items may
  change, so the user can set the width before the other lines are
  asked and then fill each line completely, and
- at the end, to append or delete the last line or item, or be done.

An appended line or item asks its new input cells at once, before the
menu is offered again; cells of lines still waiting in the queue are
asked with those lines. WizardBack steps back to the previously asked
cell that can still be asked, also from a menu, and propagates from the
first cell. The cells passed on the way back are walked again, so a cell
skipped as disabled is asked if it is enabled by then, as in the base
WizardUiBridge.ask_form().

A partial validator gets each answered cell, and the whole matrix after
a shape change; its message is shown when the matrix is not valid, its
disabled cells are skipped, and each prefill becomes the default of its
cell when that cell is asked. The message is advisory only: the wizard
checks the returned answers.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from enum import Enum, auto
from typing import TYPE_CHECKING, NamedTuple, Optional, Union
from wizard_ui_bridge.arg_types import WizardBack
from wizard_ui_bridge.form_helpers import answer_of, initial_answer, \
    prefilled_field
from wizard_ui_bridge.matrix_cell_defs import AnswerCell, AskCell, \
    AskLabelCell, PrefillValueType
from wizard_ui_bridge.matrix_defs import CellPosition, MatrixDimension, \
    MatrixRequest
from wizard_ui_bridge.matrix_helpers import cell_at, cell_name, \
    column_name, row_name, valid_cell_prefills
from wizard_ui_bridge._ask_cell import ask_cell_value
if TYPE_CHECKING:
    from wizard_ui_bridge.bridge import WizardUiBridge


class _Line(NamedTuple):
    """A step asking each input cell of one line, as wide as it is then."""

    line: int


class _Menu(Enum):
    """A resize menu: after the first line with input cells, or at the end."""

    FIRST = auto()
    END = auto()


# The actions of each menu as (lines, items) to add; (0, 0) moves on.
_ACTIONS = {_Menu.FIRST: ((0, 0), (0, 1), (0, -1)),
            _Menu.END: ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1))}


# pylint: disable-next=too-few-public-methods
class ConsoleMatrix:
    """A matrix form asked one cell at a time through a bridge."""

    def __init__(self, bridge: 'WizardUiBridge',
                 request: MatrixRequest) -> None:
        """Build the cells of the default shape with their start answers."""
        self._bridge = bridge
        self._request = request
        self._shape = MatrixDimension(0, 0)
        self._cells: list[list[AskCell]] = []
        self._answers: list[list[Optional[AnswerCell]]] = []
        self._disabled: set[CellPosition] = set()
        self._pending: dict[CellPosition, PrefillValueType] = {}
        self._reshape(request.dimensions.default)

    def run(self) -> list[list[Optional[AnswerCell]]]:
        """Ask the cells and menus and return the answers of the matrix.

        Raises:
            WizardBack: The user stepped back from the first cell.
            WizardCancelLevel: The user cancelled the current level.
            WizardAbort: The user abandoned the whole wizard.
        """
        self._validate(None, quiet=True)
        todo = self._first_steps()
        passed: list[CellPosition] = []
        while todo:
            step = todo.pop(0)
            try:
                self._run_step(step, todo)
            except WizardBack:
                todo[:0] = self._back(passed) + [step]
                continue
            if isinstance(step, CellPosition):
                passed.append(step)
        return self._answers

    def _first_steps(self) -> list[Union[CellPosition, _Line, _Menu]]:
        """Return the lines to ask with the menus that resizing needs."""
        lines, _ = self._span(self._shape)
        steps: list[Union[CellPosition, _Line, _Menu]] = [
            _Line(line) for line in range(lines)]
        first = next((line for line in range(lines)
                      if self._has_input(line)), lines)
        lines_vary, items_vary = self._resizable()
        if first < lines - 1 and items_vary:
            steps.insert(first + 1, _Menu.FIRST)
        if lines_vary or items_vary:
            steps.append(_Menu.END)
        return steps

    def _run_step(self, step: Union[CellPosition, _Line, _Menu],
                  todo: list[Union[CellPosition, _Line, _Menu]]) -> None:
        """Run one step, putting any steps it leads to first in todo.

        A cell that is not an enabled input cell is passed without asking.
        """
        if isinstance(step, _Line):
            lines, items = self._span(self._shape)
            todo[:0] = [self._position(step.line, item)
                        for item in range(items) if step.line < lines]
        elif isinstance(step, _Menu):
            todo[:0] = self._menu(step, todo)
        elif self._askable(step):
            self._ask(step)

    def _back(self, passed: list[CellPosition]) -> list[CellPosition]:
        """Return the passed cells from the last one that can be asked.

        They are removed from passed, to be walked again from that cell.

        Raises:
            WizardBack: No passed cell can be asked, so the wizard steps
                        back instead.
        """
        for index in range(len(passed) - 1, -1, -1):
            if self._askable(passed[index]):
                steps = passed[index:]
                del passed[index:]
                return steps
        raise WizardBack()

    def _ask(self, position: CellPosition) -> None:
        """Ask one input cell, store its answer and run the validator."""
        cell = self._cells[position.row][position.column]
        if self._request.console_question.use_help_text and cell.help_text:
            self._bridge.show(cell.help_text)
        prefill = self._pending.get(position)
        asked = cell if prefill is None else prefilled_field(cell, prefill)
        value = ask_cell_value(self._bridge, self._question(position), asked)
        self._pending.pop(position, None)
        self._answers[position.row][position.column] = answer_of(cell, value)
        self._validate(position)

    def _question(self, position: CellPosition) -> str:
        """Return the name of a cell that its question shows."""
        console = self._request.console_question
        namer = self._request.cell_namer
        parts: list[str] = []
        if console.show_horizontal_label:
            parts.append(row_name(self._cells, position))
        if console.show_vertical_label:
            parts.append(column_name(self._cells, position))
        if console.use_cell_namer and namer is not None:
            parts.append(namer(self._answers, position))
        return ' / '.join(part for part in parts if part) \
            or cell_name(self._cells, position)

    def _menu(self, menu: _Menu, todo: list[Union[CellPosition, _Line, _Menu]]
              ) -> list[Union[CellPosition, _Line, _Menu]]:
        """Ask a resize menu, resize, and return the steps that follow.

        An appended line is asked next, and an appended item in each line
        not still waiting in todo, before the menu is offered again.
        """
        lines, items = self._span(self._shape)
        actions = {self._label(menu, *change): change
                   for change in _ACTIONS[menu] if self._fits(*change)}
        labels = list(actions)
        question = (f'Rows: {self._shape.rows}, columns: '
                    f'{self._shape.columns}. What next?')
        add_lines, add_items = actions[self._bridge.ask_choice(
            question, choices=labels, default=labels[0])]
        if (add_lines, add_items) == (0, 0):
            return []
        self._reshape(self._dimension(lines + add_lines, items + add_items))
        self._validate(None)
        steps: list[Union[CellPosition, _Line, _Menu]] = []
        if add_lines > 0:
            steps.append(_Line(lines))
        if add_items > 0:
            steps += [self._position(line, items) for line in range(lines)
                      if _Line(line) not in todo]
        return steps + [menu]

    def _label(self, menu: _Menu, add_lines: int, add_items: int) -> str:
        """Return the menu text of one resize action."""
        row_order = self._request.console_question.row_order
        line, item = ('row', 'column') if row_order else ('column', 'row')
        if (add_lines, add_items) == (0, 0):
            return 'Done' if menu is _Menu.END else f'Next {line}'
        verb = 'Append' if add_lines + add_items > 0 else 'Delete last'
        return f'{verb} {line if add_lines else item}'

    def _fits(self, add_lines: int, add_items: int) -> bool:
        """Return whether a resize keeps the matrix within its bounds."""
        lines, items = self._span(self._shape)
        low = self._span(self._request.dimensions.min)
        high = self._span(self._request.dimensions.max)
        return low[0] <= lines + add_lines <= high[0] \
            and low[1] <= items + add_items <= high[1]

    def _resizable(self) -> tuple[bool, bool]:
        """Return whether the number of lines, and of items, may change."""
        low = self._span(self._request.dimensions.min)
        high = self._span(self._request.dimensions.max)
        return low[0] != high[0], low[1] != high[1]

    def _has_input(self, line: int) -> bool:
        """Return whether a line of the current shape has an input cell."""
        _, items = self._span(self._shape)
        positions = (self._position(line, item) for item in range(items))
        return any(not isinstance(self._cells[row][column], AskLabelCell)
                   for row, column in positions)

    def _askable(self, position: CellPosition) -> bool:
        """Return whether a cell is an enabled input cell of the shape."""
        row, column = position
        if row >= self._shape.rows or column >= self._shape.columns:
            return False
        is_label = isinstance(self._cells[row][column], AskLabelCell)
        return not is_label and position not in self._disabled

    def _validate(self, changed: Optional[CellPosition],
                  quiet: bool = False) -> None:
        """Run the partial validator, if any, and keep what it returns.

        Its message is shown when the matrix is not valid, unless quiet.
        """
        validator = self._request.partial_validator
        if validator is None:
            return
        result = validator(self._answers, changed)
        if not (quiet or result.is_valid) and result.message:
            self._bridge.show(result.message)
        self._disabled = set(result.disable_cells)
        for position, value in valid_cell_prefills(self._cells, changed,
                                                   result.prefill_values):
            self._pending[position] = value

    def _reshape(self, shape: MatrixDimension) -> None:
        """Change the matrix to shape, deleting or appending at the end.

        A remaining cell keeps its answer. A new cell comes fresh from the
        specification with its start answer, and a prefill waiting for a
        deleted cell is dropped.
        """
        old = self._shape
        self._shape = shape
        grid = [[CellPosition(row, column) for column in range(shape.columns)]
                for row in range(shape.rows)]
        self._cells = [[self._kept_cell(position, old) for position in line]
                       for line in grid]
        self._answers = [[self._kept_answer(position, old)
                          for position in line] for line in grid]
        self._pending = {position: value for position, value
                         in self._pending.items() if _inside(position, shape)}

    def _kept_cell(self, position: CellPosition,
                   old: MatrixDimension) -> AskCell:
        """Return the cell at a position of the old shape, else a new one."""
        if _inside(position, old):
            return self._cells[position.row][position.column]
        return cell_at(self._request.ask_cells, position)

    def _kept_answer(self, position: CellPosition,
                     old: MatrixDimension) -> Optional[AnswerCell]:
        """Return the answer at a position of the old shape, else a new one.

        A new answer is the start answer of the cell in self._cells, which
        must already have the new shape.
        """
        if _inside(position, old):
            return self._answers[position.row][position.column]
        return _start_answer(self._cells[position.row][position.column])

    def _span(self, shape: MatrixDimension) -> tuple[int, int]:
        """Return a shape as (lines, items) in the order cells are asked."""
        if self._request.console_question.row_order:
            return shape.rows, shape.columns
        return shape.columns, shape.rows

    def _dimension(self, lines: int, items: int) -> MatrixDimension:
        """Return the shape of a number of lines and items."""
        if self._request.console_question.row_order:
            return MatrixDimension(lines, items)
        return MatrixDimension(items, lines)

    def _position(self, line: int, item: int) -> CellPosition:
        """Return the position of an item of a line."""
        if self._request.console_question.row_order:
            return CellPosition(line, item)
        return CellPosition(item, line)


def _inside(position: CellPosition, shape: MatrixDimension) -> bool:
    """Return whether a position lies within a shape."""
    return position.row < shape.rows and position.column < shape.columns


def _start_answer(cell: AskCell) -> Optional[AnswerCell]:
    """Return the answer of a cell before it is asked; None for a label."""
    return None if isinstance(cell, AskLabelCell) else initial_answer(cell)
