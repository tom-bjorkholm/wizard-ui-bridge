#! /usr/bin/env python3
"""Tests for table questions in the Textual bridge.

The Textual bridge inherits WizardUiBridge.ask_table(), which asks the
table as a matrix form, so a table is shown by the Textual matrix screen.
The bridge tests answer the table on that screen the way a user does,
and the screen tests show the matrix request of a table directly, to
read the screen while the partial check rejects a cell.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Awaitable, Callable, Optional
import pytest
from textual.pilot import Pilot
from textual.widgets import Button, Input, Static
from wizard_ui_bridge import AnswerCells, TableCell, TableColumn, WizardBack
from wizard_ui_bridge._table_matrix import TableMatrix
from wizard_ui_bridge._textual_matrix import _MatrixApp, ADD_ROW, \
    REMOVE_ROW
from .textual_matrix_support import ScriptedBridge, run_matrix, status, \
    type_in

_GUEST = (TableColumn('Guest'),)
_RENAME = (TableColumn('Source', read_only=True), TableColumn('Rename to'))
_NEED_NAME = 'Need a name.'


def _ask(columns: tuple[TableColumn, ...], cells: list[list[TableCell]],
         script: Callable[[_MatrixApp, Pilot[AnswerCells]], Awaitable[None]],
         rows: tuple[Optional[int], Optional[int]] = (None, None)
         ) -> list[list[Optional[str]]]:
    """Ask a table through the Textual bridge, answering it with script."""
    bridge = ScriptedBridge(script)
    return bridge.ask_table(columns, cells, 'Fill?', min_rows=rows[0],
                            max_rows=rows[1])


def test_table_fixed() -> None:
    """A read-only cell keeps its text and an editable cell is filled.

    The header row holds the column headers as bold labels, and the
    first editable cell has the focus.
    """
    shown: list[object] = []

    async def fill(app: _MatrixApp, pilot: Pilot[AnswerCells]) -> None:
        """Read the header and focus, replace the value, and submit."""
        header = app.query_one('#cell_0_0', Static)
        shown.extend([str(header.render()), header.styles.text_style.bold,
                      app.focused is app.query_one('#cell_1_1')])
        await pilot.press('end', 'ctrl+u', *'town', 'ctrl+s')
    cells = [[TableCell('city'), TableCell('city')]]
    assert _ask(_RENAME, cells, fill) == [['city', 'town']]
    assert shown == ['Source', True, True]


def test_table_add_remove() -> None:
    """A variable table grows and shrinks with the matrix row buttons."""
    async def grow(app: _MatrixApp, pilot: Pilot[AnswerCells]) -> None:
        """Add two rows, fill one, drop the other, and submit."""
        await pilot.click(f'#{ADD_ROW}')
        await pilot.pause()
        await pilot.press('b')
        # A second click this soon would fall within the button's press
        # animation, which ignores clicks, so the button is pressed.
        app.query_one(f'#{ADD_ROW}', Button).press()
        await pilot.pause()
        await pilot.click(f'#{REMOVE_ROW}')
        await pilot.pause()
        await pilot.press('ctrl+s')
    assert _ask(_GUEST, [[TableCell('a')]], grow, (1, 3)) == [['a'], ['b']]


@pytest.mark.parametrize('rows, row_buttons', [
    ((None, None), False), ((1, None), False), ((None, 3), False),
    ((1, 3), True)])
def test_table_row_buttons(rows: tuple[Optional[int], Optional[int]],
                           row_buttons: bool) -> None:
    """Row buttons are offered only when both row bounds are given."""
    shown: list[int] = []

    async def confirm(app: _MatrixApp, pilot: Pilot[AnswerCells]) -> None:
        """Count the row buttons and submit."""
        shown.append(len(app.query(f'#{ADD_ROW}, #{REMOVE_ROW}')))
        await pilot.press('ctrl+s')
    _ask(_GUEST, [[TableCell('a')]], confirm, rows)
    assert shown == [2 if row_buttons else 0]


@pytest.mark.parametrize('nullable, expected', [(True, None), (False, '')])
def test_table_cleared(nullable: bool, expected: Optional[str]) -> None:
    """A cleared text cell is None when nullable, else an empty string."""
    async def clear(_app: _MatrixApp, pilot: Pilot[AnswerCells]) -> None:
        """Clear the cell and submit."""
        await pilot.press('end', 'ctrl+u', 'ctrl+s')
    cells = [[TableCell('one', nullable=nullable)]]
    assert _ask(_GUEST, cells, clear) == [[expected]]


def test_table_nav() -> None:
    """ctrl+b on a table re-raises a back request from ask_table()."""
    async def back(_app: _MatrixApp, pilot: Pilot[AnswerCells]) -> None:
        """Press the back key."""
        await pilot.press('ctrl+b')
    with pytest.raises(WizardBack):
        _ask(_GUEST, [[TableCell('a')]], back)


def _named(table: list[list[Optional[str]]],
           position: tuple[int, int]) -> tuple[bool, str]:
    """Accept a cell that is not empty."""
    return (bool(table[position[0]][position[1]]), _NEED_NAME)


def _guests(cells: list[list[TableCell]],
            script: Callable[[_MatrixApp, Pilot[AnswerCells]],
                             Awaitable[None]],
            rows: tuple[Optional[int], Optional[int]] = (None, None)
            ) -> _MatrixApp:
    """Show the matrix of a guest table with a name check by script."""
    table = TableMatrix(_GUEST, cells, _named, None)
    return run_matrix(table.request('Q', *rows), script)[0]


async def _submit(_app: _MatrixApp, pilot: Pilot[AnswerCells]) -> None:
    """Submit the table as it is."""
    await pilot.press('ctrl+s')


def test_check_untouched() -> None:
    """A cell the user has not changed does not block the table."""
    app = _guests([[TableCell('')]], _submit)
    assert app.return_value is not None


def test_check_blocks() -> None:
    """A changed cell the check rejects blocks the table until fixed."""
    found: list[object] = []

    async def edit(app: _MatrixApp, pilot: Pilot[AnswerCells]) -> None:
        """Empty the name, submit, fix it and submit again."""
        await type_in(app, pilot, (1, 0), '')
        found.append(status(app))
        await pilot.press('ctrl+s')
        found.append(app.return_value)
        await type_in(app, pilot, (1, 0), 'Bo')
        found.append(status(app))
        await pilot.press('ctrl+s')
    app = _guests([[TableCell('Ann')]], edit)
    assert found == [_NEED_NAME, None, '']
    assert app.return_value is not None


def test_check_earlier_cell() -> None:
    """An earlier changed cell still blocks, named in the message."""
    found: list[str] = []

    async def edit(app: _MatrixApp, pilot: Pilot[AnswerCells]) -> None:
        """Empty the first name, change the second and submit."""
        await type_in(app, pilot, (1, 0), '')
        await type_in(app, pilot, (2, 0), 'Cy')
        found.append(status(app))
        await pilot.press('ctrl+s')
    app = _guests([[TableCell('Ann')], [TableCell('Bo')]], edit)
    assert found == [f'Row 1 / Guest: {_NEED_NAME}']
    assert app.return_value is None


def test_check_new_row() -> None:
    """The empty cell of an appended row does not complain or block."""
    found: list[str] = []

    async def add(app: _MatrixApp, pilot: Pilot[AnswerCells]) -> None:
        """Add a row and submit."""
        await pilot.click(f'#{ADD_ROW}')
        await pilot.pause()
        found.append(status(app))
        await pilot.press('ctrl+s')
    app = _guests([[TableCell('Ann')], [TableCell('Bo')]], add, (1, 3))
    assert found == ['']
    assert app.return_value is not None
    assert len(app.return_value) == 4


def test_choice_required() -> None:
    """An empty choice cell that is not nullable blocks the table."""
    found: list[str] = []

    async def submit(app: _MatrixApp, pilot: Pilot[AnswerCells]) -> None:
        """Submit the fresh table and read the status."""
        await pilot.press('ctrl+s')
        found.append(status(app))
    cells = [[TableCell(None, choices=('x', 'y'))]]
    table = TableMatrix(_GUEST, cells, None, None)
    app = run_matrix(table.request('Q', None, None), submit)[0]
    assert app.return_value is None
    assert found == ['Row 1 / Guest: Please choose a value.']


def test_cell_typed() -> None:
    """Typing into a focused table cell edits that cell."""
    found: list[str] = []

    async def edit(app: _MatrixApp, pilot: Pilot[AnswerCells]) -> None:
        """Type after the start value and read the cell."""
        await pilot.press('end', '!')
        found.append(app.query_one('#cell_1_0', Input).value)
    _guests([[TableCell('Ann')]], edit)
    assert found == ['Ann!']
