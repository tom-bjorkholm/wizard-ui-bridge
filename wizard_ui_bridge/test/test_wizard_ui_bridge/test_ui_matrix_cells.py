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
from typing import Callable, Optional, TypeAliasType, get_args

import pytest

from wizard_ui_bridge.arg_types import PathAskOptions
from wizard_ui_bridge.form_defs import ALL_ASK_FIELD_TYPES, AnswerField, \
    AskFieldCommon, AskChoiceField, AskMultiChoiceField
from wizard_ui_bridge.matrix_cell_defs import ALL_ASK_CELL_TYPES, AskCell, \
    AnswerCell, AskRangeCell, AskIntCell, AskFloatCell, AskDateCell, \
    AskTimeCell, AskDateTimeCell, AskDurationCell, AskTextCell, \
    AskLabelCell, AskCellCommon, AskChoiceCell, AskMultiChoiceCell, \
    _OrderedValue


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


_ABC = ('a', 'b', 'c')
_BAD_MULTI = [(None, -1, None, 'min_select'), (None, 2, 1, 'min_select'),
              (None, 0, 4, 'number of choices'),
              (None, 4, None, 'number of choices'),
              (['a', 'x'], 0, None, 'one of choices'),
              (['a', 'a'], 0, None, 'twice'), (['a', 'b'], 0, 1, 'max_select')]
_GOOD_MULTI = [(None, 0, None), (['a'], 2, None), (list(_ABC), 0, None),
               (None, 3, 3), ([], 0, 0)]


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


@pytest.mark.parametrize('make', [AskChoiceCell, partial(AskChoiceField, 'Q')])
def test_choice_bad_default(make: Callable[..., AskChoiceCell]) -> None:
    """A choice default that is not one of the choices is rejected."""
    with pytest.raises(ValueError, match='one of choices'):
        make(None, _ABC, default='x')
    assert make(None, _ABC, default='b').default == 'b'


@pytest.mark.parametrize('make', [AskMultiChoiceCell,
                                  partial(AskMultiChoiceField, 'Q')])
@pytest.mark.parametrize('default, low, high, message', _BAD_MULTI)
def test_multi_bad_args(make: Callable[..., AskMultiChoiceCell],
                        default: Optional[list[str]], low: int,
                        high: Optional[int], message: str) -> None:
    """Unsatisfiable bounds or a default breaking them are rejected."""
    with pytest.raises(ValueError, match=message):
        make(None, _ABC, default=default, min_select=low, max_select=high)


@pytest.mark.parametrize('default, low, high', _GOOD_MULTI)
def test_multi_good_args(default: Optional[list[str]], low: int,
                         high: Optional[int]) -> None:
    """A default may name fewer choices than min_select, never more.

    The bounds may also reach the number of choices, and a default of no
    choices is accepted.
    """
    AskMultiChoiceCell(None, _ABC, default=default, min_select=low,
                       max_select=high)


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


_WIDTH_CELLS: list[Callable[..., AskCellCommon]] = [
    partial(AskLabelCell, 'Name'), partial(AskTextCell, None),
    partial(AskIntCell, None), partial(AskChoiceCell, None, ('a',)),
    partial(AskChoiceField, 'Q', None, ('a',)), partial(AskDateCell, None)]


@pytest.mark.parametrize('make', _WIDTH_CELLS)
def test_width_hint(make: Callable[..., AskCellCommon]) -> None:
    """Every cell and field takes a keyword-only width, None by default."""
    assert make().width is None
    assert make(width=7).width == 7


@pytest.mark.parametrize('make', _WIDTH_CELLS)
@pytest.mark.parametrize('width', [0, -3])
def test_width_too_small(make: Callable[..., AskCellCommon],
                         width: int) -> None:
    """A width hint below one character is a programming error."""
    with pytest.raises(ValueError, match='width'):
        make(width=width)


def test_width_kw_only() -> None:
    """The width hint cannot be given positionally."""
    help_field = next(cell_field for cell_field in fields(AskCellCommon)
                      if cell_field.name == 'width')
    assert help_field.kw_only


def test_label_style() -> None:
    """A label is plain by default, and bold and italic are keywords."""
    plain = AskLabelCell('Name')
    assert (plain.bold, plain.italic) == (False, False)
    styled = AskLabelCell('Name', bold=True, italic=True)
    assert (styled.bold, styled.italic) == (True, True)
    with pytest.raises(TypeError):
        AskLabelCell('Name', None, True)  # type: ignore[call-arg]
