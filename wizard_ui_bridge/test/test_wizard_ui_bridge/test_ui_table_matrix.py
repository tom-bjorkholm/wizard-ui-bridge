#! /usr/bin/env python3
"""Tests for the base ask_table(), which asks through ask_matrix_form().

A capturing bridge records the MatrixRequest the base ask_table() builds
and returns canned answers, so the mapping of a table to a matrix form
and back is checked on its own. The base ask_table() is also run on the
console bridge, which asks the matrix one cell at a time.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from io import StringIO
from typing import Optional, Sequence

import pytest

from wizard_ui_bridge import AnswerCells, AnswerChoiceCell, AnswerTextCell, \
    AskCell, AskChoiceCell, AskLabelCell, AskTextCell, CellPosition, \
    MatrixConsoleQuestion, MatrixDimension, MatrixDimensions, MatrixRequest, \
    PartialCheck, PartMatrixValidationRes, TableCell, TableColumn, \
    WizardBack, WizardUiBridge, WizardUiBridgeConsole

_KINDS = ('text', 'number')
_RENAME = (TableColumn('Source', read_only=True), TableColumn('Rename to'),
           TableColumn('Type'))
_GUEST = (TableColumn('Guest'),)


# A test double implements only the ask method its tests exercise.
# pylint: disable-next=abstract-method
class _Capture(WizardUiBridge):
    """A bridge that records the matrix request and returns answers."""

    def __init__(self, answers: Optional[AnswerCells] = None) -> None:
        """Return answers from ask_matrix_form(), or no rows when None."""
        self.answers: AnswerCells = [] if answers is None else answers
        self.request: Optional[MatrixRequest] = None
        self.reason: Optional[str] = None

    def ask_matrix_form(self, request: MatrixRequest, *,
                        re_ask_reason: Optional[str] = None) -> AnswerCells:
        """Record the request and the reason, and return the answers."""
        self.request = request
        self.reason = re_ask_reason
        return self.answers


def _request(columns: Sequence[TableColumn], cells: list[list[TableCell]], *,
             check: Optional[PartialCheck] = None,
             rows: tuple[Optional[int], Optional[int]] = (None, None)
             ) -> MatrixRequest:
    """Return the matrix request the base ask_table() builds."""
    bridge = _Capture()
    bridge.ask_table(columns, cells, 'Q', partial_check=check,
                     min_rows=rows[0], max_rows=rows[1], help_text='H')
    assert bridge.request is not None
    return bridge.request


def _rename_cells() -> list[list[TableCell]]:
    """Return two rows of a column-rename table."""
    return [[TableCell('city'), TableCell('city'),
             TableCell('text', choices=_KINDS)],
            [TableCell('size'), TableCell(None),
             TableCell(None, choices=_KINDS)]]


def test_header_and_rows() -> None:
    """Row 0 is a bold header, and a read-only cell is a label."""
    request = _request(_RENAME, _rename_cells())
    assert request.long_question == 'Q'
    assert request.ask_cells == [
        [AskLabelCell('Source', bold=True),
         AskLabelCell('Rename to', bold=True),
         AskLabelCell('Type', bold=True)],
        [AskLabelCell('city'), AskTextCell('H', default='city'),
         AskChoiceCell('H', _KINDS, default='text')],
        [AskLabelCell('size'), AskTextCell('H'), AskChoiceCell('H', _KINDS)],
        [AskTextCell('H', default=''), AskTextCell('H', default=''),
         AskChoiceCell('H', _KINDS)]]


@pytest.mark.parametrize('cell, expected', [
    (TableCell(None), AskTextCell('H')),
    (TableCell(None, nullable=True), AskTextCell('H', nullable=True)),
    (TableCell('x'), AskTextCell('H', default='x')),
    (TableCell('x', nullable=True), AskTextCell('H', default='x')),
    (TableCell(None, choices=_KINDS), AskChoiceCell('H', _KINDS)),
    (TableCell(None, choices=_KINDS, nullable=True),
     AskChoiceCell('H', _KINDS, nullable=True)),
    (TableCell('text', choices=_KINDS, nullable=True),
     AskChoiceCell('H', _KINDS, default='text'))])
def test_input_cell(cell: TableCell, expected: AskCell) -> None:
    """An editable cell is asked with its value as default."""
    request = _request(_GUEST, [[cell]])
    assert isinstance(request.ask_cells, list)
    assert request.ask_cells[1] == [expected]


def test_new_row_read_only() -> None:
    """A new row is editable in a read-only column with a shared value."""
    columns = (TableColumn('Kind', read_only=True),)
    request = _request(columns, [[TableCell('a')], [TableCell('a')]])
    assert isinstance(request.ask_cells, list)
    assert request.ask_cells[-1] == [AskTextCell('H', default='a')]


@pytest.mark.parametrize('rows, expected', [
    ((None, None), MatrixDimensions.fixed(3, 3)),
    ((1, None), MatrixDimensions.fixed(3, 3)),
    ((None, 4), MatrixDimensions.fixed(3, 3)),
    ((0, 4), MatrixDimensions(MatrixDimension(1, 3), MatrixDimension(5, 3),
                              MatrixDimension(3, 3))),
    ((2, 2), MatrixDimensions.fixed(3, 3))])
def test_dimensions(rows: tuple[Optional[int], Optional[int]],
                    expected: MatrixDimensions) -> None:
    """The matrix has a header row above the rows of the table."""
    assert _request(_RENAME, _rename_cells(), rows=rows).dimensions \
        == expected


@pytest.mark.parametrize('rows', [(3, 4), (0, 1), (-1, 2), (3, 1)])
def test_bad_row_bounds(rows: tuple[int, int]) -> None:
    """Variable rows must hold the starting rows within their bounds."""
    with pytest.raises(ValueError, match='min_rows'):
        _request(_RENAME, _rename_cells(), rows=rows)


@pytest.mark.parametrize('cells', [[[TableCell('a')]],
                                   [[TableCell('a')] * 4]])
def test_bad_row_length(cells: list[list[TableCell]]) -> None:
    """Each row of cells must hold one cell per column."""
    with pytest.raises(ValueError, match='per column'):
        _request(_RENAME, cells)


def test_empty_table() -> None:
    """A table with no rows is a matrix with only its header row."""
    request = _request(_GUEST, [])
    assert request.dimensions == MatrixDimensions.fixed(1, 1)


def test_console_question() -> None:
    """A console names each cell with the cell namer only."""
    request = _request(_GUEST, [[TableCell('a')]])
    assert request.console_question == MatrixConsoleQuestion(
        False, False, False, use_cell_namer=True)


@pytest.mark.parametrize('position, name', [
    (CellPosition(1, 1), 'city / Rename to'),
    (CellPosition(2, 2), 'size / Type'),
    (CellPosition(3, 1), 'Row 3 / Rename to'),
    (CellPosition(5, 0), 'Row 5 / Source')])
def test_cell_name(position: CellPosition, name: str) -> None:
    """A cell is named by the read-only texts of its row and its header.

    A new row has no read-only texts, so its number names it.
    """
    request = _request(_RENAME, _rename_cells())
    assert request.cell_namer is not None
    assert request.cell_namer([], position) == name


def test_cell_name_right() -> None:
    """Read-only texts right of the cell name it too, blank ones not."""
    columns = (TableColumn('A'), TableColumn('B', read_only=True),
               TableColumn('C', read_only=True),
               TableColumn('D', read_only=True))
    cells = [[TableCell('w'), TableCell('x'), TableCell(' '), TableCell('y')]]
    request = _request(columns, cells)
    assert request.cell_namer is not None
    assert request.cell_namer([], CellPosition(1, 0)) == 'x / y / A'


def test_values_from_answers() -> None:
    """Labels keep their table value, and inputs give their answers."""
    columns = (TableColumn('A', read_only=True), TableColumn('B'),
               TableColumn('C'))
    cells = [[TableCell(None), TableCell('b'),
              TableCell(None, choices=_KINDS)]]
    text = AskTextCell(None)
    choice = AskChoiceCell(None, _KINDS)
    bridge = _Capture([[None, None, None],
                       [None, AnswerTextCell(text, None),
                        AnswerChoiceCell(choice, 'number')],
                       [AnswerTextCell(text, 'new'),
                        AnswerTextCell(text, ''),
                        AnswerChoiceCell(choice, None)]])
    table = bridge.ask_table(columns, cells, 'Q', re_ask_reason='Why')
    assert table == [[None, None, 'number'], ['new', '', None]]
    assert bridge.reason == 'Why'


def test_no_partial_check() -> None:
    """Without a partial check the matrix has no partial validator."""
    assert _request(_GUEST, [[TableCell('a')]]).partial_validator is None


@pytest.mark.parametrize('accepted, message, expected', [
    (True, 'fine', PartMatrixValidationRes(True, '')),
    (False, 'bad', PartMatrixValidationRes(False, 'bad'))])
def test_partial_check(accepted: bool, message: str,
                       expected: PartMatrixValidationRes) -> None:
    """The partial check gets the table and the changed table position."""
    calls: list[tuple[list[list[Optional[str]]], tuple[int, int]]] = []

    def check(table: list[list[Optional[str]]],
              position: tuple[int, int]) -> tuple[bool, str]:
        calls.append((table, position))
        return (accepted, message)
    request = _request(_GUEST, [[TableCell('a')], [TableCell('b')]],
                       check=check)
    validator = request.partial_validator
    assert validator is not None
    answers: AnswerCells = [[None],
                            [AnswerTextCell(AskTextCell(None), 'a')],
                            [AnswerTextCell(AskTextCell(None), 'c')]]
    assert validator(answers, CellPosition(2, 0)) == expected
    assert calls == [([['a'], ['c']], (1, 0))]


def test_check_no_position() -> None:
    """With no changed cell the table counts as valid, unchecked."""
    def check(_table: list[list[Optional[str]]],
              _position: tuple[int, int]) -> tuple[bool, str]:
        raise AssertionError('a partial check needs a changed cell')
    request = _request(_GUEST, [[TableCell('a')]], check=check)
    assert request.partial_validator is not None
    assert request.partial_validator([[None], [None]], None) \
        == PartMatrixValidationRes(True, '')


def _console(lines: Sequence[str]) -> tuple[WizardUiBridgeConsole, StringIO]:
    """Return a console bridge with scripted input, and its output."""
    out = StringIO()
    answers = StringIO(''.join(f'{line}\n' for line in lines))
    return WizardUiBridgeConsole(out, answers, StringIO()), out


def test_console_fixed() -> None:
    """The base ask_table asks a fixed table one cell at a time."""
    bridge, out = _console(['town', '2', '', '1'])
    table = WizardUiBridge.ask_table(bridge, _RENAME, _rename_cells(), 'Q')
    assert table == [['city', 'town', 'number'], ['size', '', 'text']]
    assert 'city / Rename to [city]' in out.getvalue()


def test_console_choice_req() -> None:
    """A choice cell with no value is asked until a choice is made."""
    bridge, _ = _console(['', '', 'x', '', '1'])
    table = WizardUiBridge.ask_table(bridge, _RENAME, _rename_cells(), 'Q')
    assert table == [['city', 'city', 'text'], ['size', 'x', 'text']]


def _named(table: list[list[Optional[str]]],
           position: tuple[int, int]) -> tuple[bool, str]:
    """Accept a cell that is not empty."""
    value = table[position[0]][position[1]]
    return (bool(value), 'Need a name.')


@pytest.mark.parametrize('lines, expected', [
    (['', '', '2', '', ''], [['Ann'], ['Bo'], ['']]),
    (['', '', '3', ''], [['Ann']]),
    (['', '', '3', '2', 'Cy', ''], [['Ann'], ['Cy']])])
def test_console_rows(lines: list[str],
                      expected: list[list[Optional[str]]]) -> None:
    """The user appends and deletes rows within the row bounds."""
    bridge, out = _console(lines)
    cells = [[TableCell('Ann')], [TableCell('Bo')]]
    table = WizardUiBridge.ask_table(bridge, _GUEST, cells, 'Q',
                                     partial_check=_named, min_rows=1,
                                     max_rows=3)
    assert table == expected
    assert ('Need a name.' in out.getvalue()) == ([''] in expected)


def test_console_back() -> None:
    """Back from the first cell steps back out of the table."""
    bridge, _ = _console([':b'])
    with pytest.raises(WizardBack):
        WizardUiBridge.ask_table(bridge, _RENAME, _rename_cells(), 'Q')
