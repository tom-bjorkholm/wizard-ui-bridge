#! /usr/bin/env python3
"""Tests for the matrix cell definitions and their relation to form fields.

Every Ask*Field must be its Ask*Cell plus a leading short question, and
every Answer*Field must be its Answer*Cell, so code written for cells
also handles form fields, while old form field constructors keep their
argument order.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from dataclasses import MISSING, fields
from datetime import date, datetime, time, timedelta
from functools import partial
from pathlib import Path
from typing import Callable, TypeAliasType, get_args

import pytest

from wizard_ui_bridge.arg_types import PathAskOptions
from wizard_ui_bridge.form_defs import ALL_ASK_FIELD_TYPES, AnswerField, \
    AskFieldCommon, AskChoiceField
from wizard_ui_bridge.matrix_cell_defs import ALL_ASK_CELL_TYPES, AskCell, \
    AnswerCell, AskRangeCell, AskIntCell, AskFloatCell, AskDateCell, \
    AskTimeCell, AskDateTimeCell, AskDurationCell, AskTextCell, \
    AskLabelCell, AskCellCommon, AskChoiceCell, _OrderedValue


def _members(alias: TypeAliasType) -> tuple[type, ...]:
    """Return the member types of a type alias for a Union."""
    return get_args(alias.__value__)


_FIELD_CELLS = list(zip(ALL_ASK_FIELD_TYPES, ALL_ASK_CELL_TYPES[1:]))
_ANSWER_CELLS = list(zip(_members(AnswerField), _members(AnswerCell)))
_LOW_HIGH = [(AskIntCell, 1, 2), (AskFloatCell, 1.0, 2.0),
             (AskDateCell, date(2026, 1, 1), date(2026, 1, 2)),
             (AskTimeCell, time(1), time(2)),
             (AskDateTimeCell, datetime(2026, 1, 1), datetime(2026, 1, 2)),
             (AskDurationCell, timedelta(1), timedelta(2))]
_NULL_DEFAULTS: list[Callable[[], AskCellCommon | PathAskOptions]] = [
    *[partial(cell_type, None, nullable=True, default=low)
      for cell_type, low, _ in _LOW_HIGH],
    partial(AskTextCell, None, nullable=True, default='x'),
    partial(AskChoiceCell, None, ('a',), default='a', nullable=True),
    partial(AskChoiceField, 'Q', None, ('a',), default='a', nullable=True),
    partial(PathAskOptions, nullable=True, default=Path('x'))]


def _names(cls: type) -> list[str]:
    """Return the dataclass field names of cls, in constructor order."""
    return [field.name for field in fields(cls)]


def test_cell_tuple_union() -> None:
    """ALL_ASK_CELL_TYPES lists the AskCell union, label cell first."""
    assert ALL_ASK_CELL_TYPES == _members(AskCell)
    assert ALL_ASK_CELL_TYPES[0] is AskLabelCell


@pytest.mark.parametrize('field_type, cell_type', _FIELD_CELLS)
def test_field_is_cell(field_type: type, cell_type: type) -> None:
    """Each Ask*Field is its Ask*Cell and an AskFieldCommon."""
    assert field_type.__name__ == cell_type.__name__[:-4] + 'Field'
    assert issubclass(field_type, cell_type)
    assert issubclass(field_type, AskFieldCommon)


@pytest.mark.parametrize('field_type, cell_type', _FIELD_CELLS)
def test_field_arg_order(field_type: type, cell_type: type) -> None:
    """A field takes short_question first, then the cell arguments."""
    assert _names(field_type) == ['short_question'] + _names(cell_type)
    assert _names(cell_type)[0] == 'help_text'


@pytest.mark.parametrize('answer_type, cell_type', _ANSWER_CELLS)
def test_answer_is_cell(answer_type: type, cell_type: type) -> None:
    """Each Answer*Field is its Answer*Cell with the same arguments."""
    assert answer_type.__name__ == cell_type.__name__[:-4] + 'Field'
    assert issubclass(answer_type, cell_type)
    assert _names(answer_type) == _names(cell_type) == ['asking', 'value']


@pytest.mark.parametrize('cell_type, low, high', _LOW_HIGH)
def test_range_bad_bounds(cell_type: type[AskRangeCell[_OrderedValue]],
                          low: _OrderedValue, high: _OrderedValue) -> None:
    """A range cell with min greater than max is rejected."""
    with pytest.raises(ValueError, match='min_value'):
        cell_type(None, min_value=high, max_value=low)


@pytest.mark.parametrize('cell_type, low, high', _LOW_HIGH)
def test_range_bad_default(cell_type: type[AskRangeCell[_OrderedValue]],
                           low: _OrderedValue, high: _OrderedValue) -> None:
    """A range cell default outside the bounds is rejected."""
    with pytest.raises(ValueError, match='range'):
        cell_type(None, default=low, min_value=high)
    with pytest.raises(ValueError, match='range'):
        cell_type(None, default=high, max_value=low)


@pytest.mark.parametrize('cell_type, low, high', _LOW_HIGH)
def test_range_good(cell_type: type[AskRangeCell[_OrderedValue]],
                    low: _OrderedValue, high: _OrderedValue) -> None:
    """A range cell default within the inclusive bounds is accepted."""
    cell = cell_type('tip', default=high, min_value=low, max_value=high)
    assert cell.help_text == 'tip'
    assert cell.default == high


def test_text_secret_default() -> None:
    """A sensitive text cell cannot carry a default."""
    with pytest.raises(ValueError, match='default'):
        AskTextCell(None, default='x', sensitive=True)


@pytest.mark.parametrize('make', _NULL_DEFAULTS)
def test_null_default(make: Callable[[], AskCellCommon | PathAskOptions]
                      ) -> None:
    """Nullable together with a default is a programming error.

    None means nothing is filled in or selected, which contradicts a
    default, so every cell type with both attributes rejects the pair.
    """
    with pytest.raises(ValueError, match='nullable'):
        make()


def test_choice_nullable() -> None:
    """A choice cell is not nullable by default; nullable is its last arg."""
    assert AskChoiceCell(None, ('a', 'b')).nullable is False
    assert _names(AskChoiceCell)[-1] == 'nullable'


def test_label_cell() -> None:
    """A label cell holds the displayed text and keyword-only help text."""
    label = AskLabelCell('Name', help_text='tip')
    assert isinstance(label, AskCellCommon)
    assert (label.help_text, label.text) == ('tip', 'Name')
    assert AskLabelCell('Name').help_text is None


def test_label_help_kw_only() -> None:
    """Help text of a label cannot be given positionally."""
    with pytest.raises(TypeError):
        AskLabelCell('Name', 'tip')  # type: ignore[call-arg]


@pytest.mark.parametrize('cell_type', [
    cell_type for cell_type in ALL_ASK_CELL_TYPES
    if cell_type is not AskLabelCell])
def test_input_help_required(cell_type: type) -> None:
    """Only a label defaults help_text; an input cell still requires it."""
    help_field = next(cell_field for cell_field in fields(cell_type)
                      if cell_field.name == 'help_text')
    assert help_field.default is MISSING
    assert not help_field.kw_only
