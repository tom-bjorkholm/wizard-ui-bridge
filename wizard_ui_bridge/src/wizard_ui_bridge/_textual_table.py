#! /usr/local/bin/python3
"""The editable table screen of the Textual bridge.

The screen shows a table question as a grid of inputs and drop-downs,
with buttons to add and remove rows when the number of rows may vary.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import ClassVar, Iterator, Optional, Sequence
from textual import on
from textual.app import ComposeResult
from textual.binding import BindingType
from textual.containers import Grid, VerticalScroll
from textual.widget import Widget
from textual.widgets import Button, Footer, Input, Select, Static
from wizard_ui_bridge.arg_types import PartialCheck, TableColumn, TableCell
from wizard_ui_bridge.bridge_helpers import new_row_template
from wizard_ui_bridge._textual_nav import _NavApp
from wizard_ui_bridge._textual_widgets import _header_widgets, \
    _make_select, _parse_cell_id, _cell_message


# pylint: disable-next=too-many-instance-attributes
class _TableApp(_NavApp[list[list[Optional[str]]]]):
    """Editable grid returning every cell the user left.

    Read-only columns show fixed text in the template rows. Editable
    cells are a text input, or a drop-down when the cell offers choices.
    An empty editable cell is reported as None when the cell is nullable
    and as an empty string for a free-text cell, while a drop-down is
    blank only when the cell is nullable.

    When min_rows and max_rows are both given the table has a variable
    number of rows: an Add row and a Remove row button grow the table up
    to max_rows and shrink it down to min_rows. Every cell in an added
    row is editable, even in a read-only column, and its descriptor comes
    from new_row_template().

    A rejected cell is framed in the error colour while the shared status
    line names it, so the user sees which cell of the grid to correct.
    """

    BINDINGS: ClassVar[list[BindingType]] = [('ctrl+s', 'submit', 'Submit')]
    CSS = '''
    #grid { height: auto; }
    #grid .cell_error { border: tall $error; }
    '''

    # pylint: disable-next=too-many-arguments,too-many-positional-arguments
    def __init__(self, columns: Sequence[TableColumn],
                 cells: list[list[TableCell]], question: str,
                 messages: list[str], partial_check: Optional[PartialCheck],
                 min_rows: Optional[int] = None,
                 max_rows: Optional[int] = None) -> None:
        """Store the columns, starting rows, prompt, check and bounds."""
        super().__init__()
        self._columns = columns
        self._question = question
        self._messages = messages
        self._partial_check = partial_check
        self._variable = min_rows is not None and max_rows is not None
        self._min_rows = len(cells) if min_rows is None else min_rows
        self._max_rows = len(cells) if max_rows is None else max_rows
        self._new_row = new_row_template(columns, cells)
        self._rows = [list(row) for row in cells]
        self._added = [False] * len(cells)
        self._table: list[list[Optional[str]]] = [
            [cell.value for cell in row] for row in cells]

    def compose(self) -> ComposeResult:
        """Lay out the header, the editable grid, the buttons and footer."""
        yield from _header_widgets(self._messages, self._question)
        with VerticalScroll(id='scroll'), Grid(id='grid'):
            yield from self._grid_cells()
        if self._variable:
            yield Button('Add row', id='add_row')
            yield Button('Remove row', id='remove_row')
        yield Button('Submit', id='submit')
        yield Static('', id='table_status')
        yield Footer()

    def on_mount(self) -> None:
        """Size the grid, keep the scroll unfocused, focus a cell."""
        self.query_one('#scroll').can_focus = False
        grid = self.query_one('#grid', Grid)
        grid.styles.grid_size_columns = len(self._columns)
        self._focus_first_cell()

    def _focus_first_cell(self) -> None:
        """Move focus to the first editable cell of the first row."""
        if not self._rows:
            return
        for col in range(len(self._columns)):
            if not self._is_readonly(0, col):
                self.query_one(f'#cell_0_{col}').focus()
                return

    def _grid_cells(self) -> Iterator[Widget]:
        """Yield the header labels and then the rows, top to bottom."""
        for column in self._columns:
            yield Static(column.header)
        for row in range(len(self._rows)):
            yield from self._row_widgets(row)

    def _row_widgets(self, row: int) -> Iterator[Widget]:
        """Yield the widgets of one data row, left to right."""
        for col in range(len(self._columns)):
            yield self._cell_widget(row, col)

    def _is_readonly(self, row: int, col: int) -> bool:
        """Return whether a cell shows fixed text instead of a widget.

        Cells in added rows are always editable, even in a column that is
        read-only in the template rows.
        """
        return not self._added[row] and self._columns[col].read_only

    def _cell_widget(self, row: int, col: int) -> Widget:
        """Return the widget shown for one cell of the grid."""
        cell = self._rows[row][col]
        widget_id = f'cell_{row}_{col}'
        if self._is_readonly(row, col):
            return Static(cell.value or '', id=widget_id)
        if cell.choices is None:
            return Input(value=cell.value or '', id=widget_id)
        return _make_select(cell, widget_id)

    @on(Input.Changed)
    def _on_input(self, event: Input.Changed) -> None:
        """Re-check the table after a text cell changes."""
        self._recheck(_parse_cell_id(event.input.id))

    @on(Select.Changed)
    def _on_select(self, event: Select.Changed) -> None:
        """Re-check the table after a drop-down cell changes."""
        self._recheck(_parse_cell_id(event.select.id))

    def _recheck(self, position: Optional[tuple[int, int]]) -> None:
        """Update the changed cell and show any partial-check message."""
        if position is None:
            return
        row, col = position
        self._table[row][col] = self._read_cell(row, col)
        if self._partial_check is None:
            return
        accepted, message = self._partial_check(self._table, position)
        self._report(None if accepted else position,
                     '' if accepted else message)

    def action_submit(self) -> None:
        """Exit returning every cell, including the read-only columns."""
        result = [[self._read_cell(row, col)
                   for col in range(len(self._columns))]
                  for row in range(len(self._rows))]
        self.exit(result)

    @on(Button.Pressed, '#submit')
    def _submit_clicked(self, _event: Button.Pressed) -> None:
        """Submit the table when the submit button is pressed."""
        self.action_submit()

    @on(Button.Pressed, '#add_row')
    def _add_clicked(self, _event: Button.Pressed) -> None:
        """Add a row when the add-row button is pressed."""
        self._add_row()

    @on(Button.Pressed, '#remove_row')
    def _remove_clicked(self, _event: Button.Pressed) -> None:
        """Remove the last row when the remove-row button is pressed."""
        self._remove_row()

    def _add_row(self) -> None:
        """Append one editable row, up to max_rows."""
        if len(self._rows) >= self._max_rows:
            self._report(None, f'At most {self._max_rows} rows allowed.')
            return
        row = len(self._rows)
        self._rows.append(list(self._new_row))
        self._added.append(True)
        self._table.append([cell.value for cell in self._new_row])
        self.query_one('#grid', Grid).mount(*self._row_widgets(row))
        self._report(None, '')

    def _remove_row(self) -> None:
        """Remove the last row, down to min_rows."""
        if len(self._rows) <= self._min_rows:
            self._report(None, f'At least {self._min_rows} rows required.')
            return
        row = len(self._rows) - 1
        for col in range(len(self._columns)):
            self.query_one(f'#cell_{row}_{col}').remove()
        self._rows.pop()
        self._added.pop()
        self._table.pop()
        self._report(None, '')

    def _report(self, position: Optional[tuple[int, int]],
                message: str) -> None:
        """Show a message, naming and framing the cell it complains of.

        A message given no cell position, such as one about the number of
        rows, is about the whole table: it is shown unchanged and no cell
        is framed.
        """
        self.query('.cell_error').remove_class('cell_error')
        if position is None:
            self._set_status(message)
            return
        row, col = position
        self.query_one(f'#cell_{row}_{col}').add_class('cell_error')
        self._set_status(_cell_message(self._columns[col].header, row,
                                       message))

    def _set_status(self, message: str) -> None:
        """Show a status message below the table."""
        self.query_one('#table_status', Static).update(message)

    def _read_cell(self, row: int, col: int) -> Optional[str]:
        """Return the current value of one cell for the result table."""
        cell = self._rows[row][col]
        if self._is_readonly(row, col):
            return cell.value
        widget_id = f'#cell_{row}_{col}'
        if cell.choices is not None:
            select = self.query_one(widget_id, Select)
            return None if select.is_blank() else str(select.value)
        text = self.query_one(widget_id, Input).value
        if text == '':
            return None if cell.nullable else ''
        return text
