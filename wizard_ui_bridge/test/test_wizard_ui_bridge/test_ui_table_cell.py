#! /usr/bin/env python3
"""Tests for the rules of one editable cell of a fixed-row table.

The console bridge fills a fixed-row table one editable cell at a time
through the shared table helpers, so driving it is the way to test what
a single cell accepts: keeping the value it already holds, the erase
token, a choice given by number or by name, and the values a cell that
must hold one may not be left with.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from io import StringIO
from typing import Optional

import pytest

from wizard_ui_bridge import TableCell, TableColumn, WizardUiBridgeConsole
from wizard_ui_bridge.bridge_helpers import CHOICE_ERROR

_PICK = ('x', 'y', 'z')
_NEEDED = 'Please enter a value.'


def _fill(answers: list[str], cell: TableCell,
          re_ask_reason: Optional[str] = None
          ) -> tuple[list[list[Optional[str]]], str, str]:
    """Fill a one-cell table with scripted answers and return the streams."""
    out_file = StringIO()
    err_file = StringIO()
    lines = ''.join(answer + '\n' for answer in answers)
    bridge = WizardUiBridgeConsole(out_file, StringIO(lines), err_file)
    table = bridge.ask_table((TableColumn('A'),), [[cell]], 'Q:',
                             re_ask_reason=re_ask_reason)
    return table, out_file.getvalue(), err_file.getvalue()


@pytest.mark.parametrize('answer, expected', [
    ('2', 'y'), ('y', 'y'), ('Y', 'y'), ('3', 'z')])
def test_cell_choice(answer: str, expected: str) -> None:
    """A cell with choices takes a menu number or a choice name."""
    table, _, err = _fill([answer], TableCell(value='x', choices=_PICK))
    assert table == [[expected]]
    assert err == ''


@pytest.mark.parametrize('answer', ['w', '0', '9', '-1'])
def test_cell_not_a_choice(answer: str) -> None:
    """A cell with choices refuses a value that is not one of them."""
    table, _, err = _fill([answer, '3'], TableCell(value='x', choices=_PICK))
    assert table == [['z']]
    assert CHOICE_ERROR in err


def test_cell_free_text() -> None:
    """A cell without choices takes the text as it was typed."""
    table, _, err = _fill(['anything'], TableCell(value='x'))
    assert table == [['anything']]
    assert err == ''


@pytest.mark.parametrize('cell, expected', [
    (TableCell(value='x', nullable=True), None),
    (TableCell(value='x', choices=_PICK, nullable=True), None),
    (TableCell(value='x'), '')])
def test_cell_erase(cell: TableCell, expected: Optional[str]) -> None:
    """The erase token empties a cell that may be left empty."""
    table, _, err = _fill([':e'], cell)
    assert table == [[expected]]
    assert err == ''


def test_cell_erase_refused() -> None:
    """A cell that must hold one of its choices refuses the erase token."""
    table, _, err = _fill([':e', '1'], TableCell(value='x', choices=_PICK))
    assert table == [['x']]
    assert _NEEDED in err


@pytest.mark.parametrize('cell, expected', [
    (TableCell(value='x'), 'x'),
    (TableCell(value='x', choices=_PICK), 'x'),
    (TableCell(nullable=True), None),
    (TableCell(), '')])
def test_cell_keep(cell: TableCell, expected: Optional[str]) -> None:
    """Pressing enter keeps whatever value the cell already holds."""
    table, _, err = _fill([''], cell)
    assert table == [[expected]]
    assert err == ''


def test_cell_keep_refused() -> None:
    """An empty cell that must hold one of its choices may not be kept.

    Keeping such a cell would leave it empty, which is what erasing it
    does, so it is refused for the same reason.
    """
    table, _, err = _fill(['', '2'], TableCell(choices=_PICK))
    assert table == [['y']]
    assert _NEEDED in err


def test_cell_prompt() -> None:
    """The cell prompt shows the current value and the editing keys."""
    _, out, _ = _fill([''], TableCell(value='x'))
    assert 'A [x] (enter=keep, :e=erase)' in out


def test_table_reask_reason() -> None:
    """A fixed-row table shows the reason it is asked again."""
    _, out, _ = _fill([''], TableCell(value='x'), 'try again')
    assert 'try again' in out


def test_row_label_in_prompt() -> None:
    """A read-only column labels the editable cell of its row."""
    columns = (TableColumn('Name', read_only=True), TableColumn('Value'))
    cells = [[TableCell(value='size'), TableCell(value='7')]]
    out_file = StringIO()
    bridge = WizardUiBridgeConsole(out_file, StringIO('8\n'), StringIO())
    assert bridge.ask_table(columns, cells, 'Q:') == [['size', '8']]
    assert 'size - Value [7]' in out_file.getvalue()
