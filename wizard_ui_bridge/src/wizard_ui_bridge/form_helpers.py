#! /usr/local/bin/python3
"""Helpers shared by the WizardUiBridge form and matrix form questions.

Every Ask*Field of a form derives from the Ask*Cell of a matrix form, so
the helpers that only need what a field and a cell have in common take a
cell, and serve both questions.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Sequence
from dataclasses import replace
from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import Iterator, NoReturn, Optional, TypeVar, overload
from wizard_ui_bridge.matrix_cell_defs import PrefillValueType, AskCell, \
    AnswerCell, AskLabelCell, AskTextCell, AskIntCell, AskPathCell, \
    AskYesNoCell, AskChoiceCell, AskMultiChoiceCell, AskFloatCell, \
    AskDateCell, AskTimeCell, AskDateTimeCell, AskDurationCell, \
    AnswerTextCell, AnswerIntCell, AnswerPathCell, AnswerYesNoCell, \
    AnswerChoiceCell, AnswerMultiChoiceCell, AnswerFloatCell, \
    AnswerDateCell, AnswerTimeCell, AnswerDateTimeCell, AnswerDurationCell
from wizard_ui_bridge.form_defs import AskField, \
    AnswerField, AskTextField, AskIntField, AskPathField, AskYesNoField, \
    AskChoiceField, AskMultiChoiceField, AskFloatField, AskDateField, \
    AskTimeField, AskDateTimeField, AskDurationField, AnswerTextField, \
    AnswerIntField, AnswerPathField, AnswerYesNoField, AnswerChoiceField, \
    AnswerMultiChoiceField, AnswerFloatField, AnswerDateField, \
    AnswerTimeField, AnswerDateTimeField, AnswerDurationField, \
    PrefillValues
_ORDERED_CELLS = (AskIntCell, AskFloatCell, AskDateCell, AskTimeCell,
                  AskDateTimeCell, AskDurationCell)
_T = TypeVar('_T')


def nullable_choice(field: AskField) -> bool:
    """Return whether field is a nullable choice field.

    The base WizardUiBridge.supports_form_field() rejects such a field,
    since a bridge written before ask_choice() took nullable cannot ask
    one. Each bridge in this package supports it.
    """
    return isinstance(field, AskChoiceField) and field.nullable


@overload
def initial_answer(field: AskField) -> AnswerField: ...


@overload
def initial_answer(field: AskCell) -> AnswerCell: ...


def initial_answer(field: AskCell) -> AnswerCell:
    """Return the starting answer for a field or input cell.

    The value is the field's start value, else its default, or the empty
    or not-yet-answered state when the field has neither. A choice field
    with neither starts as None, which tells a partial validator the
    choice is not answered yet; a bridge must not leave that None in a
    submitted form.
    A form field gets its Answer*Field and a matrix cell its Answer*Cell.
    A label cell has no answer and must not be passed.
    """
    return answer_of(field, _starting_value(field))


def _starting_value(cell: AskCell) -> Optional[PrefillValueType]:
    """Return the value an input cell or field starts with.

    A multi-choice with neither a start value nor a default starts with
    nothing selected.
    """
    if isinstance(cell, AskPathCell):
        return cell.path_options.start_or_default
    if isinstance(cell, AskMultiChoiceCell):
        start = cell.start_or_default
        return [] if start is None else list(start)
    assert not isinstance(cell, AskLabelCell)
    return cell.start_or_default


@overload
def answer_of(ask: AskField,
              value: Optional[PrefillValueType]) -> AnswerField: ...


@overload
def answer_of(ask: AskCell,
              value: Optional[PrefillValueType]) -> AnswerCell: ...


def answer_of(ask: AskCell, value: Optional[PrefillValueType]) -> AnswerCell:
    """Return the answer holding value for a form field or an input cell.

    A form field gets its Answer*Field and a matrix cell its Answer*Cell,
    so a bridge reads a field and a cell the same way. value must have
    the answer type of ask (see PrefillValueType), where an integer is
    accepted for a float, a list of str is needed for a multi-choice, a
    bool for a yes/no, and None is accepted wherever the answer value is
    Optional. A label cell has no answer and must not be passed.
    """
    return _text_like_answer(ask, value) or _choice_answer(ask, value) \
        or _number_answer(ask, value) or _temporal_answer(ask, value)


def _optional(value: Optional[PrefillValueType],
              kind: type[_T]) -> Optional[_T]:
    """Return value, which must be None or an instance of kind."""
    assert value is None or isinstance(value, kind)
    return value


def _float_value(value: Optional[PrefillValueType]) -> Optional[float]:
    """Return value as a float, accepting an integer as float defaults do."""
    if value is None:
        return None
    assert isinstance(value, (int, float))
    return float(value)


def _text_like_answer(ask: AskCell, value: Optional[PrefillValueType]
                      ) -> Optional[AnswerCell]:
    """Return the answer of a text, integer or path ask, else None."""
    if isinstance(ask, AskTextCell):
        text = _optional(value, str)
        return AnswerTextField(ask, text) if isinstance(ask, AskTextField) \
            else AnswerTextCell(ask, text)
    if isinstance(ask, AskIntCell):
        number = _optional(value, int)
        return AnswerIntField(ask, number) if isinstance(ask, AskIntField) \
            else AnswerIntCell(ask, number)
    if isinstance(ask, AskPathCell):
        path = _optional(value, Path)
        return AnswerPathField(ask, path) if isinstance(ask, AskPathField) \
            else AnswerPathCell(ask, path)
    return None


def _choice_answer(ask: AskCell, value: Optional[PrefillValueType]
                   ) -> Optional[AnswerCell]:
    """Return the answer of a yes/no, choice or multi-choice, else None."""
    if isinstance(ask, AskYesNoCell):
        assert isinstance(value, bool)
        return AnswerYesNoField(ask, value) \
            if isinstance(ask, AskYesNoField) else AnswerYesNoCell(ask, value)
    if isinstance(ask, AskChoiceCell):
        chosen = _optional(value, str)
        return AnswerChoiceField(ask, chosen) \
            if isinstance(ask, AskChoiceField) \
            else AnswerChoiceCell(ask, chosen)
    if isinstance(ask, AskMultiChoiceCell):
        assert isinstance(value, list)
        return AnswerMultiChoiceField(ask, value) \
            if isinstance(ask, AskMultiChoiceField) \
            else AnswerMultiChoiceCell(ask, value)
    return None


def _number_answer(ask: AskCell, value: Optional[PrefillValueType]
                   ) -> Optional[AnswerCell]:
    """Return the answer of a float, date or time ask, else None."""
    if isinstance(ask, AskFloatCell):
        number = _float_value(value)
        return AnswerFloatField(ask, number) \
            if isinstance(ask, AskFloatField) else AnswerFloatCell(ask, number)
    if isinstance(ask, AskDateCell):
        day = _optional(value, date)
        return AnswerDateField(ask, day) if isinstance(ask, AskDateField) \
            else AnswerDateCell(ask, day)
    if isinstance(ask, AskTimeCell):
        clock = _optional(value, time)
        return AnswerTimeField(ask, clock) if isinstance(ask, AskTimeField) \
            else AnswerTimeCell(ask, clock)
    return None


def _temporal_answer(ask: AskCell,
                     value: Optional[PrefillValueType]) -> AnswerCell:
    """Return the answer of a date-time or duration ask."""
    if isinstance(ask, AskDateTimeCell):
        moment = _optional(value, datetime)
        return AnswerDateTimeField(ask, moment) \
            if isinstance(ask, AskDateTimeField) \
            else AnswerDateTimeCell(ask, moment)
    assert isinstance(ask, AskDurationCell)
    span = _optional(value, timedelta)
    return AnswerDurationField(ask, span) \
        if isinstance(ask, AskDurationField) else AnswerDurationCell(ask, span)


def valid_prefills(fields: Sequence[AskField], changed: int,
                   prefill_values: PrefillValues
                   ) -> Iterator[tuple[int, PrefillValueType]]:
    """Yield the prefill requests a bridge should apply, validated.

    Each yielded (index, value) pair is ready to place into the row's
    input. A prefill aimed at the changed row is skipped, so writing back
    never fights the user's current edit. A row index outside the form
    raises IndexError and a value whose Python type does not match the
    field raises TypeError, since both are validator bugs. A choice value
    not among the field's choices, any prefill of a sensitive text field,
    and a multi-choice value with no valid member, are dropped instead, so
    a portable validator stays safe. A multi-choice value keeps only its
    members that are valid choices.
    """
    for index, value in prefill_values:
        _check_row(fields, index)
        if index == changed:
            continue
        usable = prefill_value(fields[index], value, f'row {index}')
        if usable is not None:
            yield index, usable


def _check_row(fields: Sequence[AskField], index: int) -> None:
    """Raise when a prefill row index lies outside the form."""
    if not 0 <= index < len(fields):
        raise IndexError(f'prefill row index {index} is out of range')


def prefill_value(cell: AskCell, value: PrefillValueType,
                  where: str) -> Optional[PrefillValueType]:
    """Return the value to apply for a prefill, or None to drop it.

    cell is the input field or cell the prefill is aimed at, and where
    names its place, such as 'row 2', in the error message. The rules are
    those of valid_prefills(). Raises TypeError when value's Python type
    does not match cell.
    """
    if isinstance(cell, _ORDERED_CELLS):
        return _ordered_prefill(cell, value, where)
    if isinstance(cell, AskTextCell):
        _need(value, where, str)
        return None if cell.sensitive else value
    if isinstance(cell, AskPathCell):
        _need(value, where, Path)
        return value
    if isinstance(cell, AskYesNoCell):
        if not isinstance(value, bool):
            _bad_type(where)
        return value
    if isinstance(cell, AskChoiceCell):
        _need(value, where, str)
        return value if value in cell.choices else None
    assert isinstance(cell, AskMultiChoiceCell)
    return _multi_prefill(cell, value, where)


def _ordered_prefill(cell: AskCell, value: PrefillValueType,
                     where: str) -> PrefillValueType:
    """Return an ordered cell's prefill, or raise TypeError for it.

    An integer or float cell takes a number, and a date cell takes a
    date that is not a datetime, so a datetime is never mistaken for a
    plain date. Each temporal cell takes exactly its own type.
    """
    if isinstance(cell, AskIntCell):
        if isinstance(value, bool) or not isinstance(value, int):
            _bad_type(where)
        return value
    if isinstance(cell, AskFloatCell):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            _bad_type(where)
        return value
    if isinstance(cell, AskDateCell):
        if not isinstance(value, date) or isinstance(value, datetime):
            _bad_type(where)
        return value
    if isinstance(cell, AskTimeCell):
        if not isinstance(value, time):
            _bad_type(where)
        return value
    if isinstance(cell, AskDateTimeCell):
        if not isinstance(value, datetime):
            _bad_type(where)
        return value
    assert isinstance(cell, AskDurationCell)
    if not isinstance(value, timedelta):
        _bad_type(where)
    return value


def _multi_prefill(cell: AskMultiChoiceCell, value: PrefillValueType,
                   where: str) -> Optional[list[str]]:
    """Return the valid members of a multi-choice prefill, or None."""
    if isinstance(value, str) or not isinstance(value, Sequence):
        _bad_type(where)
    if not all(isinstance(member, str) for member in value):
        _bad_type(where)
    members = [member for member in value if member in cell.choices]
    return members if members else None


def _need(value: PrefillValueType, where: str, wanted: type) -> None:
    """Raise TypeError when value is not an instance of wanted."""
    if not isinstance(value, wanted):
        _bad_type(where)


def _bad_type(where: str) -> NoReturn:
    """Raise a TypeError for a prefill value of the wrong type."""
    raise TypeError(f'prefill value for {where} has the wrong type')


@overload
def prefilled_field(field: AskField,
                    prefill: Optional[PrefillValueType]) -> AskField: ...


@overload
def prefilled_field(field: AskCell,
                    prefill: Optional[PrefillValueType]) -> AskCell: ...


def prefilled_field(field: AskCell,
                    prefill: Optional[PrefillValueType]) -> AskCell:
    """Return a form field or input cell that starts with prefill.

    The console bridge asks a field or cell with a prefill, or with the
    answer the user gave before stepping back to it, as its start_value.
    Unlike a default, a start value keeps nullable, so the user can still
    empty the answer. A prefill of None starts the field with its
    default, which is empty for a nullable field. A prefill that cannot
    serve as a valid start value, such as an integer or date outside the
    field's bounds or a multi-choice selection of more than max_select
    choices, is ignored so the field keeps its own start. The prefill
    has already been checked against the field type by valid_prefills()
    or matrix_helpers.valid_cell_prefills(), or is an earlier answer. A
    label cell must not be passed.
    """
    try:
        result = _start_a(field, prefill)
        return result if result is not None else _start_b(field, prefill)
    except ValueError:
        return field


def _start_a(field: AskCell,
             value: Optional[PrefillValueType]) -> Optional[AskCell]:
    """Return field starting with value, for the first field group."""
    if isinstance(field, AskPathCell):
        options = replace(field.path_options,
                          start_value=_optional(value, Path))
        return replace(field, path_options=options)
    if isinstance(field, AskIntCell):
        return replace(field, start_value=_optional(value, int))
    if isinstance(field, AskFloatCell):
        return replace(field, start_value=_float_value(value))
    if isinstance(field, AskDateCell):
        return replace(field, start_value=_optional(value, date))
    if isinstance(field, AskTimeCell):
        return replace(field, start_value=_optional(value, time))
    return None


def _start_b(field: AskCell, value: Optional[PrefillValueType]) -> AskCell:
    """Return field starting with value, for the second field group."""
    if isinstance(field, AskDateTimeCell):
        return replace(field, start_value=_optional(value, datetime))
    if isinstance(field, AskDurationCell):
        return replace(field, start_value=_optional(value, timedelta))
    if isinstance(field, AskYesNoCell):
        return replace(field, start_value=_optional(value, bool))
    if isinstance(field, (AskChoiceCell, AskTextCell)):
        return replace(field, start_value=_optional(value, str))
    assert isinstance(field, AskMultiChoiceCell)
    return replace(field, start_value=_optional(value, list))
