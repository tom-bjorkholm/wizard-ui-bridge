#! /usr/bin/env python3
"""Tests for the helpers shared by the bridges showing a matrix form.

They cover building the cells from a MatrixCellSpec, applying the
prefills of a partial validator, naming a cell by its labels, and
wrapping a value in the answer of a form field or a matrix cell.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import Optional, cast

import pytest

from wizard_ui_bridge import AskCell, AnswerCell, AnswerCells, AskField, \
    CellNamer, CellPosition, MatrixCellSpec, PathAskOptions, \
    PrefillCellValues, PrefillValueType, \
    AskLabelCell, AskTextCell, AskIntCell, AskPathCell, AskYesNoCell, \
    AskChoiceCell, AskMultiChoiceCell, AskFloatCell, AskDateCell, \
    AskTimeCell, AskDateTimeCell, AskDurationCell, AnswerTextCell, \
    AnswerIntCell, AnswerPathCell, AnswerYesNoCell, AnswerChoiceCell, \
    AnswerMultiChoiceCell, AnswerFloatCell, AnswerDateCell, AnswerTimeCell, \
    AnswerDateTimeCell, AnswerDurationCell, AskTextField, AskFloatField, \
    AskMultiChoiceField, AnswerTextField, AnswerFloatField, \
    AnswerMultiChoiceField
from wizard_ui_bridge.form_helpers import answer_of, initial_answer, \
    prefill_value, prefilled_field
from wizard_ui_bridge.matrix_helpers import cell_at, cell_name, \
    column_label, column_name, message_name, row_label, row_name, \
    valid_cell_prefills

_POS = CellPosition
_CORNER = AskLabelCell('')
_MON = AskLabelCell('Mon')
_TUE = AskLabelCell('Tue')
_ALICE = AskLabelCell('Alice')
_HOURS = AskIntCell(None)
_GRID: list[list[AskCell]] = [[_CORNER, _MON, _TUE],
                              [_ALICE, _HOURS, _HOURS],
                              [AskTextCell(None), _HOURS, _HOURS]]


@pytest.mark.parametrize('position, expected', [
    (_POS(0, 1), _MON), (_POS(1, 0), _ALICE), (_POS(5, 1), _HOURS),
    (_POS(0, 9), _TUE)])
def test_cell_at_listed(position: CellPosition, expected: AskCell) -> None:
    """A listed cell is used, repeating the last row or cell beyond it."""
    assert cell_at(_GRID, position) is expected


def test_cell_at_short_row() -> None:
    """A position right of a short row repeats that row's last cell."""
    cells: list[list[AskCell]] = [[_ALICE], [_MON, _TUE]]
    assert cell_at(cells, _POS(0, 3)) is _ALICE
    assert cell_at(cells, _POS(3, 3)) is _TUE


def test_cell_at_generator() -> None:
    """A generator is called with the position of the cell."""
    seen: list[CellPosition] = []

    def _generate(position: CellPosition) -> AskCell:
        """Record the position and return a label naming it."""
        seen.append(position)
        return AskLabelCell(f'{position.row},{position.column}')
    cell = cell_at(_generate, _POS(2, 3))
    assert isinstance(cell, AskLabelCell) and cell.text == '2,3'
    assert seen == [_POS(2, 3)]


@pytest.mark.parametrize('cells', [[], [[]]])
def test_cell_at_empty(cells: list[list[AskCell]]) -> None:
    """A sequence with no rows, or a row with no cells, is rejected."""
    with pytest.raises(ValueError):
        cell_at(cells, _POS(0, 0))


@pytest.mark.parametrize('spec', [[['not a cell']], lambda _position: 5])
def test_cell_at_not_cell(spec: object) -> None:
    """A specification giving something that is not an AskCell raises."""
    with pytest.raises(TypeError, match=r'\(0, 0\)'):
        cell_at(cast(MatrixCellSpec, spec), _POS(0, 0))


def test_cell_prefill_applied() -> None:
    """A valid prefill is yielded at its position, as a CellPosition."""
    prefills = cast(PrefillCellValues, (((1, 2), 4),))
    result = list(valid_cell_prefills(_GRID, None, prefills))
    assert result == [(_POS(1, 2), 4)]
    assert isinstance(result[0][0], CellPosition)


def test_cell_prefill_changed() -> None:
    """A prefill aimed at the changed cell is skipped."""
    prefills: PrefillCellValues = ((_POS(1, 1), 4), (_POS(1, 2), 5))
    result = list(valid_cell_prefills(_GRID, _POS(1, 1), prefills))
    assert result == [(_POS(1, 2), 5)]


@pytest.mark.parametrize('position', [
    _POS(3, 0), _POS(0, 3), _POS(-1, 1), _POS(1, -1)])
def test_cell_prefill_outside(position: CellPosition) -> None:
    """A prefill aimed outside the matrix raises IndexError."""
    with pytest.raises(IndexError, match='outside the matrix'):
        list(valid_cell_prefills(_GRID, None, ((position, 4),)))


def test_cell_prefill_label() -> None:
    """A prefill aimed at a label cell raises TypeError."""
    with pytest.raises(TypeError, match='label cell'):
        list(valid_cell_prefills(_GRID, None, ((_POS(0, 1), 'x'),)))


def test_cell_prefill_type() -> None:
    """A prefill of the wrong type names the cell in its TypeError."""
    with pytest.raises(TypeError, match=r'cell \(1, 1\) has the wrong'):
        list(valid_cell_prefills(_GRID, None, ((_POS(1, 1), 'x'),)))


@pytest.mark.parametrize('cell, value', [
    (AskChoiceCell(None, choices=('a', 'b')), 'z'),
    (AskTextCell(None, sensitive=True), 'secret')])
def test_cell_prefill_dropped(cell: AskCell, value: str) -> None:
    """An unknown choice and any prefill of a sensitive cell are dropped."""
    prefills: PrefillCellValues = ((_POS(0, 0), value),)
    assert not list(valid_cell_prefills([[cell]], None, prefills))


def test_prefill_value_where() -> None:
    """The TypeError of a prefill names the place it was aimed at."""
    with pytest.raises(TypeError, match='for row 7 has the wrong type'):
        prefill_value(AskIntCell(None), 'x', 'row 7')


@pytest.mark.parametrize('position, left, above', [
    (_POS(1, 1), 'Alice', 'Mon'), (_POS(2, 2), None, 'Tue'),
    (_POS(1, 0), None, None), (_POS(0, 2), 'Mon', None)])
def test_cell_labels(position: CellPosition, left: Optional[str],
                     above: Optional[str]) -> None:
    """The nearest non-blank labels to the left and above are found."""
    assert row_label(_GRID, position) == left
    assert column_label(_GRID, position) == above


@pytest.mark.parametrize('position, name', [
    (_POS(1, 1), 'Alice / Mon'), (_POS(2, 2), 'Row 3 / Tue'),
    (_POS(2, 0), 'Row 3 / Alice'), (_POS(0, 0), 'Row 1 / Column 1')])
def test_cell_name(position: CellPosition, name: str) -> None:
    """A missing label is replaced by the 1-based row or column number."""
    assert cell_name(_GRID, position) == name


@pytest.mark.parametrize('position, row, column', [
    (_POS(1, 1), 'Alice', 'Mon'), (_POS(2, 2), 'Row 3', 'Tue'),
    (_POS(0, 0), 'Row 1', 'Column 1')])
def test_row_column_name(position: CellPosition, row: str,
                         column: str) -> None:
    """Each half of cell_name() is a label, or the 1-based number."""
    assert row_name(_GRID, position) == row
    assert column_name(_GRID, position) == column


def test_cell_name_no_label() -> None:
    """A cell with no label, or only blank ones, is named by position."""
    cells: list[list[AskCell]] = [[_CORNER, _HOURS], [_HOURS, _HOURS]]
    assert cell_name(cells, _POS(1, 1)) == 'Row 2 / Column 2'


def test_message_name_namer() -> None:
    """The namer gets the answers and position, and its name is used."""
    answers: AnswerCells = [[None, AnswerIntCell(_HOURS, 3)]]
    seen: list[tuple[AnswerCells, CellPosition]] = []

    def _namer(given: AnswerCells, position: CellPosition) -> str:
        """Record the call and name the cell by its answer."""
        seen.append((given, position))
        answer = given[position.row][position.column]
        assert isinstance(answer, AnswerIntCell)
        return f'Cell holding {answer.value}'
    name = message_name(_namer, answers, _GRID, _POS(0, 1))
    assert name == 'Cell holding 3'
    assert seen == [(answers, _POS(0, 1))]


@pytest.mark.parametrize('namer', [None, lambda _answers, _position: ''])
def test_message_name_default(namer: Optional[CellNamer]) -> None:
    """With no namer, or an empty name from it, the labels name the cell."""
    assert message_name(namer, [], _GRID, _POS(1, 1)) == 'Alice / Mon'


_PATH_CELL = AskPathCell(None, PathAskOptions())


@pytest.mark.parametrize('ask, value, expected', [
    (AskTextCell(None), 'a', AnswerTextCell(AskTextCell(None), 'a')),
    (AskIntCell(None), 3, AnswerIntCell(AskIntCell(None), 3)),
    (_PATH_CELL, Path('/x'), AnswerPathCell(_PATH_CELL, Path('/x'))),
    (AskYesNoCell(None, default=False), True,
     AnswerYesNoCell(AskYesNoCell(None, default=False), True)),
    (AskChoiceCell(None, choices=('a',)), None,
     AnswerChoiceCell(AskChoiceCell(None, choices=('a',)), None)),
    (AskMultiChoiceCell(None, choices=('a',)), ['a'],
     AnswerMultiChoiceCell(AskMultiChoiceCell(None, choices=('a',)), ['a'])),
    (AskFloatCell(None), 2.5, AnswerFloatCell(AskFloatCell(None), 2.5)),
    (AskDateCell(None), date(2027, 1, 2),
     AnswerDateCell(AskDateCell(None), date(2027, 1, 2))),
    (AskTimeCell(None), time(9), AnswerTimeCell(AskTimeCell(None), time(9))),
    (AskDateTimeCell(None), datetime(2027, 1, 2, 9),
     AnswerDateTimeCell(AskDateTimeCell(None), datetime(2027, 1, 2, 9))),
    (AskDurationCell(None), timedelta(hours=1),
     AnswerDurationCell(AskDurationCell(None), timedelta(hours=1)))])
def test_answer_of_cell(ask: AskCell, value: Optional[PrefillValueType],
                        expected: AnswerCell) -> None:
    """A matrix cell gets the Answer*Cell of its kind holding the value."""
    answer = answer_of(ask, value)
    assert answer == expected
    assert type(answer) is type(expected)


@pytest.mark.parametrize('ask, value, expected', [
    (AskTextField('T', None), 'a', AnswerTextField(AskTextField('T', None),
                                                   'a')),
    (AskMultiChoiceField('M', None, choices=('a',)), [],
     AnswerMultiChoiceField(AskMultiChoiceField('M', None, choices=('a',)),
                            []))])
def test_answer_of_field(ask: AskField, value: PrefillValueType,
                         expected: AnswerCell) -> None:
    """A form field gets the Answer*Field of its kind, not the cell one."""
    answer = answer_of(ask, value)
    assert answer == expected
    assert type(answer) is type(expected)


def test_answer_of_float_int() -> None:
    """An integer value of a float field is turned into a float."""
    field = AskFloatField('F', None)
    answer = answer_of(field, 2)
    assert answer == AnswerFloatField(field, 2.0)
    assert isinstance(answer.value, float)


@pytest.mark.parametrize('cell, value', [
    (AskTextCell(None), 'hi'), (AskIntCell(None), 7),
    (AskPathCell(None, PathAskOptions()), Path('/tmp/x')),
    (AskYesNoCell(None, False), True),
    (AskChoiceCell(None, choices=('x', 'y')), 'y'),
    (AskMultiChoiceCell(None, choices=('a', 'b')), ['a', 'b']),
    (AskFloatCell(None), 4.0), (AskDateCell(None), date(2024, 5, 6)),
    (AskTimeCell(None), time(9, 30)),
    (AskDateTimeCell(None), datetime(2024, 5, 6, 9, 30)),
    (AskDurationCell(None), timedelta(hours=2))])
def test_prefilled_cell(cell: AskCell, value: PrefillValueType) -> None:
    """A prefilled cell stays a cell, and its start answer is the value."""
    assert initial_answer(cell).asking is cell
    result = prefilled_field(cell, value)
    assert type(result) is type(cell)
    assert initial_answer(result).value == value
