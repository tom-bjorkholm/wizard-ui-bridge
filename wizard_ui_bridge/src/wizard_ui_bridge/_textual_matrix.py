#! /usr/local/bin/python3
"""The matrix form screen of the Textual bridge.

A matrix form asks a grid of cells at once. :class:`_MatrixApp` shows one
widget per cell of the current shape in a grid that scrolls both ways: a
label for an AskLabelCell, in bold or italics when the cell asks for it,
and for every other cell a compact input built by
wizard_ui_bridge._textual_cell, the same input a form row shows but
narrower by default and with a narrow '…' button for a path or date.

The optional partial validator runs when the matrix is first shown and
after every change of a cell and of the shape, to disable irrelevant
cells, apply prefills and show advisory feedback. Its message is first
shown once the user changes the matrix or submits it, so a fresh matrix
does not open with a complaint. On submit every enabled cell is
validated, so a submitted matrix is always complete, and the keyboard
focus moves to the first cell that fails its own check. Such a cell is
framed in the error colour and named in the shared status line by the
CellNamer of the request, or else by its labels.

When the minimum and maximum dimensions of the request differ, buttons
append or delete the last row or column, each disabled at its bound. The
first enabled input of an appended row or column gets the keyboard focus
and is scrolled into view. A delete button keeps the focus, as a pressed
Textual button takes it, so the user can delete again, until it is
disabled at its bound and the focus passes to the first enabled input.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from dataclasses import dataclass
from functools import partial
from itertools import product
from typing import ClassVar, Iterable, Iterator, Optional, Sequence
from textual import on
from textual.app import ComposeResult
from textual.binding import BindingType
from textual.containers import Grid, Horizontal, ScrollableContainer
from textual.widget import Widget
from textual.widgets import Button, Checkbox, Footer, Input, Select, \
    SelectionList, Static
from wizard_ui_bridge.matrix_cell_defs import AnswerCell, AskCell, \
    AskLabelCell
from wizard_ui_bridge.matrix_defs import AnswerCells, CellPosition, \
    MatrixDimension, MatrixRequest, PrefillCellValues
from wizard_ui_bridge.matrix_helpers import cell_at, message_name, \
    valid_cell_prefills
from wizard_ui_bridge._textual_cell import CellInput, build_input
from wizard_ui_bridge._textual_nav import _NavApp
from wizard_ui_bridge._textual_widgets import _cell_position, \
    _header_widgets

ADD_ROW = 'add_row'
REMOVE_ROW = 'remove_row'
ADD_COLUMN = 'add_column'
REMOVE_COLUMN = 'remove_column'
_ROW_BUTTONS = ((ADD_ROW, '+ Row'), (REMOVE_ROW, '− Row'))
_COLUMN_BUTTONS = ((ADD_COLUMN, '+ Column'), (REMOVE_COLUMN, '− Column'))


@dataclass(frozen=True)
class _MatrixCell:
    """One built matrix cell: its AskCell, widget and input.

    A label cell has no input.
    """

    ask: AskCell
    widget: Widget
    cell_input: Optional[CellInput] = None

    def answer(self) -> Optional[AnswerCell]:
        """Return the current answer of the cell, or None for a label."""
        return None if self.cell_input is None else self.cell_input.answer()

    def error(self) -> Optional[str]:
        """Return the cell's own validation error, or None when valid."""
        return None if self.cell_input is None else self.cell_input.error()


def _build_cell(ask: AskCell, position: CellPosition) -> _MatrixCell:
    """Return the label or compact input of one cell, not yet mounted.

    Both get the id 'cell_{row}_{column}'.
    """
    key = f'{position.row}_{position.column}'
    if isinstance(ask, AskLabelCell):
        return _MatrixCell(ask, _label(ask, f'cell_{key}'))
    built = build_input(ask, 'cell', key, compact=True)
    return _MatrixCell(ask, built.widget, built)


def _label(ask: AskLabelCell, widget_id: str) -> Static:
    """Return the label of a label cell, wrapped at its width hint.

    The text is shown as it is, not as Textual markup.
    """
    label = Static(ask.text, markup=False, id=widget_id,
                   classes='matrix_label')
    styles = [name for name, wanted in (('bold', ask.bold),
                                        ('italic', ask.italic)) if wanted]
    if styles:
        label.styles.text_style = ' '.join(styles)
    if ask.width is not None:
        label.styles.width = ask.width
    label.tooltip = ask.help_text
    return label


class _MatrixApp(_NavApp[AnswerCells]):
    """A grid of label and input cells that asks a whole matrix form."""

    BINDINGS: ClassVar[list[BindingType]] = [('ctrl+s', 'submit', 'Submit')]
    CSS = '''
    #matrix_grid { grid-columns: auto; grid-gutter: 0 1; width: auto;
                   height: auto; }
    #matrix_grid .matrix_label { max-width: 30; padding-top: 1; }
    #matrix_grid .cell_error { border: tall $error; }
    #matrix_grid Horizontal { width: auto; height: auto; }
    #matrix_grid Button { min-width: 5; }
    #matrix_grid SelectionList { max-height: 10; }
    #resize { height: auto; }
    '''

    def __init__(self, request: MatrixRequest, messages: list[str]) -> None:
        """Store the request; the cells are built when composed."""
        super().__init__()
        self._request = request
        self._messages = messages
        self._disabled: frozenset[CellPosition] = frozenset()
        self._last_changed: Optional[CellPosition] = None
        self._shape = request.dimensions.default
        self._cells: list[list[_MatrixCell]] = []

    def answers(self) -> list[list[Optional[AnswerCell]]]:
        """Return the current answers, one list per row of the shape."""
        return [[cell.answer() for cell in row] for row in self._cells]

    def compose(self) -> ComposeResult:
        """Lay out the header, the grid, the buttons, status and footer.

        The cells of the default shape are built here, since a Textual
        input can only be built while the app is running.
        """
        question = self._request.long_question
        yield from _header_widgets(self._messages, question)
        self._cells = [[self._new_cell(CellPosition(row, column))
                        for column in range(self._shape.columns)]
                       for row in range(self._shape.rows)]
        with ScrollableContainer(id='matrix_scroll'), Grid(id='matrix_grid'):
            for row in self._cells:
                yield from (cell.widget for cell in row)
        buttons = self._resize_buttons()
        if buttons:
            yield Horizontal(*buttons, id='resize')
        yield Button('Submit', id='submit')
        yield Static('', id='matrix_status')
        yield Footer()

    def _resize_buttons(self) -> list[Button]:
        """Return the resize buttons of each dimension that may change."""
        bounds = self._request.dimensions
        pairs: list[tuple[str, str]] = []
        if bounds.min.rows != bounds.max.rows:
            pairs += _ROW_BUTTONS
        if bounds.min.columns != bounds.max.columns:
            pairs += _COLUMN_BUTTONS
        return [Button(text, id=button_id) for button_id, text in pairs]

    def on_mount(self) -> None:
        """Size the grid, validate it, and focus the first enabled input.

        The validator's message is not shown yet. The inputs record their
        answers as seen, also after its prefills, so neither the change
        event Textual posts as it mounts an input nor a first prefill is
        taken as an edit by the user.
        """
        self.query_one('#matrix_scroll').can_focus = False
        self._set_grid_columns()
        self._validate(None, live=True)
        self._settle(self._positions())
        self._update_resizers()
        self._focus_first(list(self._positions()))

    @on(Input.Changed)
    def _input_changed(self, event: Input.Changed) -> None:
        """React to a change of a text-like cell."""
        self._changed(event.input.id)

    @on(Select.Changed)
    def _select_changed(self, event: Select.Changed) -> None:
        """React to a change of a choice cell."""
        self._changed(event.select.id)

    @on(Checkbox.Changed)
    def _checkbox_changed(self, event: Checkbox.Changed) -> None:
        """React to a change of a yes/no cell."""
        self._changed(event.checkbox.id)

    @on(SelectionList.SelectedChanged)
    def _multi_changed(self, event: SelectionList.SelectedChanged[int]
                       ) -> None:
        """React to a change of a multi-choice cell."""
        self._changed(event.control.id)

    @on(Button.Pressed, '.browse, .pick')
    def _dialog_clicked(self, event: Button.Pressed) -> None:
        """Open the directory picker or calendar of the clicked cell."""
        cell_input = self._input_of(event.button.id)
        if cell_input is not None:
            cell_input.open_dialog()

    @on(Button.Pressed, '#submit')
    def _submit_clicked(self, _event: Button.Pressed) -> None:
        """Submit the matrix when the submit button is pressed."""
        self.action_submit()

    def action_submit(self) -> None:
        """Validate the whole matrix and exit with its answers when valid.

        The partial validator runs first, so the cells it disables are not
        checked. Every enabled cell must then pass its own check, and the
        first that does not gets the keyboard focus. Last the validator
        must accept the matrix.
        """
        problem = self._validate(self._last_changed, live=False)
        invalid = self._first_invalid()
        if invalid is not None:
            self._reveal(invalid)
            self._report(invalid, self._cell_error(invalid) or '')
        elif problem is not None:
            self._report(None, problem)
        else:
            self.exit(self.answers())

    @on(Button.Pressed, f'#{ADD_ROW}')
    async def _add_row(self, _event: Button.Pressed) -> None:
        """Append a row of fresh cells, up to the maximum row count."""
        if not self._allowed()[ADD_ROW]:
            return
        line = [CellPosition(self._shape.rows, column)
                for column in range(self._shape.columns)]
        cells = [self._new_cell(position) for position in line]
        self._cells.append(cells)
        self._shape = MatrixDimension(self._shape.rows + 1,
                                      self._shape.columns)
        await self._grid().mount_all(cell.widget for cell in cells)
        self._added(line)

    @on(Button.Pressed, f'#{ADD_COLUMN}')
    async def _add_column(self, _event: Button.Pressed) -> None:
        """Append a column of fresh cells, up to the maximum column count.

        Each new cell is mounted after the last cell of its row, since
        the grid places its children row by row.
        """
        if not self._allowed()[ADD_COLUMN]:
            return
        line = [CellPosition(row, self._shape.columns)
                for row in range(self._shape.rows)]
        self._shape = MatrixDimension(self._shape.rows,
                                      self._shape.columns + 1)
        for position, cells in zip(line, self._cells):
            cell = self._new_cell(position)
            await self._grid().mount(cell.widget, after=cells[-1].widget
                                     if cells else None)
            cells.append(cell)
        self._set_grid_columns()
        self._added(line)

    @on(Button.Pressed, f'#{REMOVE_ROW}')
    async def _remove_row(self, _event: Button.Pressed) -> None:
        """Delete the last row, down to the minimum row count."""
        if not self._allowed()[REMOVE_ROW]:
            return
        self._shape = MatrixDimension(self._shape.rows - 1,
                                      self._shape.columns)
        await self._remove(self._cells.pop())
        self._reshaped()

    @on(Button.Pressed, f'#{REMOVE_COLUMN}')
    async def _remove_column(self, _event: Button.Pressed) -> None:
        """Delete the last column, down to the minimum column count."""
        if not self._allowed()[REMOVE_COLUMN]:
            return
        self._shape = MatrixDimension(self._shape.rows,
                                      self._shape.columns - 1)
        await self._remove([cells.pop() for cells in self._cells])
        self._set_grid_columns()
        self._reshaped()

    def _new_cell(self, position: CellPosition) -> _MatrixCell:
        """Return the cell the request gives for a position, not mounted."""
        return _build_cell(cell_at(self._request.ask_cells, position),
                           position)

    def _grid(self) -> Grid:
        """Return the grid holding the cell widgets."""
        return self.query_one('#matrix_grid', Grid)

    def _set_grid_columns(self) -> None:
        """Lay the grid out in as many columns as the current shape.

        A shape with no columns has no cells, so one grid column is kept.
        """
        self._grid().styles.grid_size_columns = max(self._shape.columns, 1)

    async def _remove(self, cells: Sequence[_MatrixCell]) -> None:
        """Remove the widgets of deleted cells from the grid.

        The removal is awaited, so a cell appended later may reuse an id.
        """
        await self._grid().remove_children([cell.widget for cell in cells])

    def _added(self, line: Sequence[CellPosition]) -> None:
        """Settle an appended row or column, re-validate and focus it."""
        self._settle(line)
        self._reshaped()
        self._focus_first(line)

    def _reshaped(self) -> None:
        """Update the resize buttons and re-validate the whole matrix.

        The focus stays on the resize button the user just pressed, unless
        an appended row or column takes it. A button disabled at its
        bound cannot keep the focus, so it passes to the first enabled
        input, as when the matrix is first shown.
        """
        self._update_resizers()
        self._last_changed = None
        self._report(None, self._validate(None, live=True) or '')
        if self.focused is None or self.focused.disabled:
            self._focus_first(list(self._positions()))

    def _allowed(self) -> dict[str, bool]:
        """Return for each resize action whether the bounds allow it."""
        low = self._request.dimensions.min
        high = self._request.dimensions.max
        now = self._shape
        return {ADD_ROW: now.rows < high.rows, REMOVE_ROW: now.rows > low.rows,
                ADD_COLUMN: now.columns < high.columns,
                REMOVE_COLUMN: now.columns > low.columns}

    def _update_resizers(self) -> None:
        """Disable each resize button whose action the bounds forbid."""
        for button_id, allowed in self._allowed().items():
            for button in self.query(f'#{button_id}'):
                button.disabled = not allowed

    def _settle(self, positions: Iterable[CellPosition]) -> None:
        """Record the answers of mounted input cells as seen."""
        for position in positions:
            cell_input = self._cell(position).cell_input
            if cell_input is not None:
                cell_input.settle()

    def _changed(self, widget_id: Optional[str]) -> None:
        """React to a cell change with live feedback and cell enabling.

        Typing the '?' token into a date cell opens its calendar.
        """
        position = _cell_position(widget_id)
        cell_input = self._input_of(widget_id)
        if position is None or cell_input is None:
            return
        if cell_input.wants_calendar():
            cell_input.open_dialog()
            return
        if not cell_input.take_change():
            return
        self._last_changed = position
        message = self._validate(position, live=True)
        own = None if position in self._disabled \
            else self._cell_error(position)
        if own is None:
            self._report(None, message or '')
        else:
            self._report(position, own)

    def _input_of(self, widget_id: Optional[str]) -> Optional[CellInput]:
        """Return the input a widget id belongs to, None if it is gone.

        An event of a cell in a row or column just deleted has a position
        outside the current shape.
        """
        position = _cell_position(widget_id)
        if position is None or position.row >= self._shape.rows \
                or position.column >= self._shape.columns:
            return None
        return self._cell(position).cell_input

    def _validate(self, changed: Optional[CellPosition],
                  live: bool) -> Optional[str]:
        """Run the partial validator and return its message when invalid.

        The disabled cells of its result are applied, and while the user
        edits (live) its prefills too, which are ignored on submit.
        """
        validator = self._request.partial_validator
        if validator is None:
            return None
        result = validator(self.answers(), changed)
        self._apply_disabled(result.disable_cells)
        if live:
            self._apply_prefills(result.prefill_values, changed)
        return None if result.is_valid else result.message

    def _apply_disabled(self, positions: tuple[CellPosition, ...]) -> None:
        """Enable or disable each input to match the validator result."""
        self._disabled = frozenset(CellPosition(*pair) for pair in positions)
        for position in self._positions():
            cell_input = self._cell(position).cell_input
            if cell_input is not None:
                cell_input.set_enabled(position not in self._disabled)

    def _apply_prefills(self, prefills: PrefillCellValues,
                        changed: Optional[CellPosition]) -> None:
        """Write the validator's valid prefills into their cell inputs."""
        for position, value in valid_cell_prefills(self._asks(), changed,
                                                   prefills):
            cell_input = self._cell(position).cell_input
            assert cell_input is not None
            cell_input.write(value)

    def _first_invalid(self) -> Optional[CellPosition]:
        """Return the first enabled cell failing its own check, or None."""
        for position in self._positions():
            if position not in self._disabled \
                    and self._cell(position).error() is not None:
                return position
        return None

    def _cell_error(self, position: CellPosition) -> Optional[str]:
        """Return one cell's own error, prefixed with the cell's name.

        The whole matrix shares one status line, so naming the cell, by
        the CellNamer of the request or by its labels, makes clear which
        cell a message refers to.
        """
        error = self._cell(position).error()
        if error is None:
            return None
        name = message_name(self._request.cell_namer, self.answers(),
                            self._asks(), position)
        return f'{name}: {error}'

    def _report(self, position: Optional[CellPosition], message: str) -> None:
        """Show a message, framing the input of the cell it complains of.

        A message given no position, such as one from the partial
        validator, is about the whole matrix, so no cell is framed.
        """
        self.query('.cell_error').remove_class('cell_error')
        if position is not None:
            cell_input = self._cell(position).cell_input
            assert cell_input is not None
            cell_input.main.add_class('cell_error')
        self.query_one('#matrix_status', Static).update(message)

    def _focus_first(self, positions: Sequence[CellPosition]) -> None:
        """Reveal the first enabled input, else the first of the cells."""
        inputs = [position for position in positions
                  if self._focusable(position)]
        target = next(iter(inputs or positions), None)
        if target is not None:
            self._reveal(target)

    def _focusable(self, position: CellPosition) -> bool:
        """Return whether a cell is an enabled input."""
        return position not in self._disabled \
            and self._cell(position).cell_input is not None

    def _reveal(self, position: CellPosition) -> None:
        """Scroll a cell into view, focusing it when it is focusable.

        The scroll waits for the next refresh, so a cell just appended
        has been laid out and has a place to scroll to.
        """
        cell = self._cell(position)
        if cell.cell_input is not None and self._focusable(position):
            cell.cell_input.main.focus(scroll_visible=False)
        self.call_after_refresh(partial(cell.widget.scroll_visible,
                                        animate=False))

    def _positions(self) -> Iterator[CellPosition]:
        """Yield every position of the current shape, row by row."""
        for row, column in product(range(self._shape.rows),
                                   range(self._shape.columns)):
            yield CellPosition(row, column)

    def _asks(self) -> list[list[AskCell]]:
        """Return the AskCells of the current shape, one list per row."""
        return [[cell.ask for cell in row] for row in self._cells]

    def _cell(self, position: CellPosition) -> _MatrixCell:
        """Return the built cell at a position of the current shape."""
        return self._cells[position.row][position.column]
