#! /usr/local/bin/python3
"""Variable-row table editing shared by the wizard UI bridges.

This module holds the console row-menu editor used when the console
bridge is asked for a variable-row table. The descriptor for rows added
at run time is bridge_helpers.new_row_template(), shared by all bridges.

The console editor shows the whole table as a numbered overview each
round and then asks one action prompt last, so the actions and any
re-ask reason stay visible after a long table has scrolled off the
screen. A row number edits that row, ':+' adds a row and ':- N' deletes
row N, while a blank answer accepts the table. Asked for help, the action
prompt explains these actions, followed by the help text of the table.
Editing a row reuses the same per-cell helpers as a fixed table, so choice
cells, the erase token, the help text and per-cell navigation behave
identically.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Callable, Optional, Sequence
from wizard_ui_bridge.arg_types import AskReader, \
    PartialCheck, TableCell, TableColumn, WizardBack
from wizard_ui_bridge.bridge_helpers import cell_checker, \
    fill_cell, int_text, new_row_template
from wizard_ui_bridge._help import help_kwargs

_ADD_ROW = ':+'  # appends a row in the variable-row console table editor
_DEL_ROW = ':-'  # deletes a row in the variable-row console table editor
_BAD_MENU = 'Enter a row number, :+, :- N, or blank to accept.'
_ROW_MENU_PROMPT = ('Enter a row number to edit it, :+ to add a row, '
                    ':- N to delete row N, blank to accept.')


# pylint: disable-next=too-many-instance-attributes,too-few-public-methods
class _VarTable:
    """Mutable state and editing for a variable-row console table.

    A row number edits that row cell by cell, ':+' appends a row and
    edits it, ':- N' deletes row N, and a blank answer accepts the table.
    A row added to the table is fully editable, even in a column that is
    read-only in the template rows, mirroring the Textual bridge.
    """

    # pylint: disable-next=too-many-arguments,too-many-positional-arguments
    def __init__(self, columns: Sequence[TableColumn],
                 cells: list[list[TableCell]],
                 partial_check: Optional[PartialCheck], min_rows: int,
                 max_rows: int, help_text: Optional[str]) -> None:
        """Start from the given rows and remember the bounds and help."""
        self._columns = columns
        self._help = help_text
        self._check = partial_check
        self._min = min_rows
        self._max = max_rows
        self._new = new_row_template(columns, cells)
        self._rows = [list(row) for row in cells]
        self._added = [False] * len(cells)
        self.table: list[list[Optional[str]]] = [
            [cell.value for cell in row] for row in cells]
        self.reason: Optional[str] = None

    def step(self, ask: AskReader, reason: Optional[str]) -> bool:
        """Run one menu round; return True when the table is accepted."""
        self.reason = None
        answer = ask(_ROW_MENU_PROMPT, reason, None,
                     **help_kwargs(ask, self._menu_help()))
        token = (answer if isinstance(answer, str) else str(answer)).strip()
        if token == '':
            return self._accept()
        if token.startswith(_ADD_ROW):
            self._add(ask)
        elif token.startswith(_DEL_ROW):
            self._delete(token[len(_DEL_ROW):])
        else:
            self._edit(ask, token)
        return False

    def _menu_help(self) -> str:
        """Return the explanation of the menu actions and the table help."""
        actions = ('Each row of the table above has a number. Enter a row '
                   'number to edit the cells of that row one at a time, :+ '
                   'to append a new row and edit it, or :- followed by a row '
                   'number, such as :- 2, to delete that row. A blank answer '
                   f'accepts the table, which must keep {self._min} to '
                   f'{self._max} rows.')
        return f'{actions}\n{self._help}' if self._help else actions

    def _accept(self) -> bool:
        """Accept the table when its row count is within the bounds."""
        if len(self._rows) < self._min:
            self.reason = f'Please keep at least {self._min} rows.'
            return False
        if len(self._rows) > self._max:
            self.reason = f'Please keep at most {self._max} rows.'
            return False
        return True

    def _add(self, ask: AskReader) -> None:
        """Append one editable row, up to max_rows, then edit it."""
        if len(self._rows) >= self._max:
            self.reason = f'At most {self._max} rows allowed.'
            return
        self._rows.append(list(self._new))
        self._added.append(True)
        self.table.append([cell.value for cell in self._new])
        self._edit_row(ask, len(self._rows) - 1)

    def _delete(self, arg: str) -> None:
        """Delete the row named by a one-based number, down to min_rows."""
        index = int_text(arg.strip())
        if index is None or not 1 <= index <= len(self._rows):
            self.reason = 'Type :- followed by a row number to delete.'
            return
        if len(self._rows) <= self._min:
            self.reason = f'At least {self._min} rows required.'
            return
        position = index - 1
        self._rows.pop(position)
        self._added.pop(position)
        self.table.pop(position)

    def _edit(self, ask: AskReader, token: str) -> None:
        """Edit the row named by a one-based number."""
        index = int_text(token)
        if index is None or not 1 <= index <= len(self._rows):
            self.reason = _BAD_MENU
            return
        self._edit_row(ask, index - 1)

    def _edit_row(self, ask: AskReader, row: int) -> None:
        """Walk the editable cells of one row, back to the menu on back."""
        cols = [col for col in range(len(self._columns))
                if self._editable(row, col)]
        position = 0
        while position < len(cols):
            try:
                self._fill_one(ask, row, cols[position])
            except WizardBack:
                if position == 0:
                    return
                position -= 1
                continue
            position += 1

    def _fill_one(self, ask: AskReader, row: int, col: int) -> None:
        """Ask one editable cell and store its accepted value."""
        check = cell_checker(self.table, (row, col), self._check)
        self.table[row][col] = fill_cell(ask, self._columns, self._rows[row],
                                         col, self.table[row][col], check,
                                         self._help)

    def _editable(self, row: int, col: int) -> bool:
        """Return whether one cell can be edited in the console table."""
        return self._added[row] or not self._columns[col].read_only


# pylint: disable-next=too-many-arguments,too-many-positional-arguments
def _run_variable_table(ask: AskReader, show: Callable[[str], None],
                        columns: Sequence[TableColumn],
                        cells: list[list[TableCell]], question: str,
                        re_ask_reason: Optional[str],
                        partial_check: Optional[PartialCheck], min_rows: int,
                        max_rows: int,
                        help_text: Optional[str]) -> list[list[Optional[str]]]:
    """Edit a variable-row table through the console row-menu interface."""
    editor = _VarTable(columns, cells, partial_check, min_rows, max_rows,
                       help_text)
    reason = re_ask_reason
    while True:
        show(question)
        for line in _overview_lines(columns, editor.table):
            show(line)
        if editor.step(ask, reason):
            return editor.table
        reason = editor.reason


def _overview_lines(columns: Sequence[TableColumn],
                    table: list[list[Optional[str]]]) -> list[str]:
    """Return the numbered overview lines for a variable-row table."""
    header = ['#'] + [column.header for column in columns]
    rows = [[str(number + 1)] + [_cell_text(value) for value in row]
            for number, row in enumerate(table)]
    widths = _column_widths([header] + rows)
    return [_overview_line(line, widths) for line in [header] + rows]


def _column_widths(lines: list[list[str]]) -> list[int]:
    """Return the widest text in each column across the given lines."""
    return [max(len(line[col]) for line in lines)
            for col in range(len(lines[0]))]


def _overview_line(cells: list[str], widths: list[int]) -> str:
    """Return one space-padded overview line, without trailing spaces."""
    padded = [text.ljust(width) for text, width in zip(cells, widths)]
    return '  '.join(padded).rstrip()


def _cell_text(value: Optional[str]) -> str:
    """Return the overview display text for one cell value."""
    return '' if value is None else value
