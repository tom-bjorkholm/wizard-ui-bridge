#! /usr/local/bin/python3
"""Tests for table questions in the Tk bridge.

The Tk bridge inherits WizardUiBridge.ask_table(), which asks the table
as a matrix form, so a table is shown by the Tk matrix editor. The bridge
tests answer the table the way a user does, through its real buttons. The
editor tests build the matrix request of a table and drive the editor
directly, since a change of an entry is only reported on a key press,
which needs a shown and focused window.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter as tk
from typing import Callable, Optional
import pytest
from wizard_ui_bridge import AnswerCells, CellPosition, TableCell, \
    TableColumn
from wizard_ui_bridge._table_matrix import TableMatrix
from wizard_tk_bridge import WizardUiBridgeTk
from wizard_tk_bridge.wizard_matrix import ADD_ROW, REMOVE_ROW, MatrixEditor
from .gui_test_helpers import click_button, content_of, find_widgets, \
    gui_root, set_entry

_GUEST = (TableColumn('Guest'),)
_RENAME = (TableColumn('Source', read_only=True), TableColumn('Rename to'))
_NEED_NAME = 'Need a name.'


def _ask(columns: tuple[TableColumn, ...], cells: list[list[TableCell]],
         action: Callable[[tk.Frame], None],
         rows: tuple[Optional[int], Optional[int]] = (None, None)
         ) -> list[list[Optional[str]]]:
    """Ask a table through the Tk bridge, answering it with action."""
    with gui_root() as root:
        bridge = WizardUiBridgeTk(root)
        try:
            # pylint: disable-next=protected-access
            root.after(0, lambda: action(content_of(bridge._window_obj())))
            return bridge.ask_table(columns, cells, 'Fill?', min_rows=rows[0],
                                    max_rows=rows[1])
        finally:
            bridge.close()


def test_table_fixed() -> None:
    """A read-only cell keeps its text and an editable cell is filled."""
    def fill(content: tk.Frame) -> None:
        """Replace the editable value and confirm the table."""
        set_entry(find_widgets(content, tk.Entry)[0], 'town')
        click_button(content, 'OK')
    cells = [[TableCell('city'), TableCell('city')]]
    assert _ask(_RENAME, cells, fill) == [['city', 'town']]


def test_table_add_remove() -> None:
    """A variable table grows and shrinks with the matrix row buttons."""
    def grow(content: tk.Frame) -> None:
        """Add two rows, fill one, drop the other, and confirm."""
        click_button(content, ADD_ROW)
        set_entry(find_widgets(content, tk.Entry)[1], 'b')
        click_button(content, ADD_ROW)
        click_button(content, REMOVE_ROW)
        click_button(content, 'OK')
    assert _ask(_GUEST, [[TableCell('a')]], grow, (1, 3)) == [['a'], ['b']]


@pytest.mark.parametrize('rows, row_buttons', [
    ((None, None), False), ((1, None), False), ((None, 3), False),
    ((1, 3), True)])
def test_table_row_buttons(rows: tuple[Optional[int], Optional[int]],
                           row_buttons: bool) -> None:
    """Row buttons are offered only when both row bounds are given."""
    shown: list[set[str]] = []

    def confirm(content: tk.Frame) -> None:
        """Record the button texts and confirm the table."""
        shown.append({str(button.cget('text'))
                      for button in find_widgets(content, tk.Button)})
        click_button(content, 'OK')
    _ask(_GUEST, [[TableCell('a')]], confirm, rows)
    assert (ADD_ROW in shown[0]) is row_buttons
    assert (REMOVE_ROW in shown[0]) is row_buttons


def _named(table: list[list[Optional[str]]],
           position: tuple[int, int]) -> tuple[bool, str]:
    """Accept a cell that is not empty."""
    return (bool(table[position[0]][position[1]]), _NEED_NAME)


def _editor(root: tk.Tk, cells: list[list[TableCell]],
            rows: tuple[Optional[int], Optional[int]] = (None, None)
            ) -> tuple[MatrixEditor, list[AnswerCells]]:
    """Build the matrix editor of a guest table, recording submits."""
    table = TableMatrix(_GUEST, cells, _named, None)
    recorded: list[AnswerCells] = []
    editor = MatrixEditor(tk.Frame(root), table.request('Q', *rows),
                          recorded.append)
    return editor, recorded


def _edit(editor: MatrixEditor, row: int, text: str) -> None:
    """Type text into the guest cell of a matrix row and report it."""
    # pylint: disable-next=protected-access
    widget = editor._cell(CellPosition(row, 0)).widget
    assert isinstance(widget, tk.Entry)
    set_entry(widget, text)
    # pylint: disable-next=protected-access
    editor._changed(CellPosition(row, 0))


def _status(editor: MatrixEditor) -> str:
    """Return the text of the editor's status line."""
    # pylint: disable-next=protected-access
    return str(editor._status.cget('text'))


def test_check_untouched() -> None:
    """A cell the user has not changed does not block the table."""
    with gui_root() as root:
        editor, recorded = _editor(root, [[TableCell('')]])
        editor.submit()
        assert len(recorded) == 1


def test_check_blocks() -> None:
    """A changed cell the check rejects blocks the table until fixed."""
    with gui_root() as root:
        editor, recorded = _editor(root, [[TableCell('Ann')]])
        _edit(editor, 1, '')
        assert _status(editor) == _NEED_NAME
        editor.submit()
        assert not recorded
        _edit(editor, 1, 'Bo')
        assert _status(editor) == ''
        editor.submit()
        assert len(recorded) == 1


def test_check_earlier_cell() -> None:
    """An earlier changed cell still blocks, named in the message."""
    with gui_root() as root:
        editor, recorded = _editor(root, [[TableCell('Ann')],
                                          [TableCell('Bo')]])
        _edit(editor, 1, '')
        _edit(editor, 2, 'Cy')
        assert _status(editor) == f'Row 1 / Guest: {_NEED_NAME}'
        editor.submit()
        assert not recorded


def test_check_new_row() -> None:
    """The empty cell of an appended row does not complain or block."""
    with gui_root() as root:
        editor, recorded = _editor(root, [[TableCell('Ann')],
                                          [TableCell('Bo')]], (1, 3))
        editor.add_row()
        assert _status(editor) == ''
        editor.submit()
        assert len(recorded) == 1


def test_choice_required() -> None:
    """An empty choice cell that is not nullable blocks the table."""
    with gui_root() as root:
        cells = [[TableCell(None, choices=('x', 'y'))]]
        table = TableMatrix(_GUEST, cells, None, None)
        recorded: list[AnswerCells] = []
        editor = MatrixEditor(tk.Frame(root), table.request('Q', None, None),
                              recorded.append)
        editor.submit()
        assert not recorded
        assert _status(editor).startswith('Row 1 / Guest: ')
