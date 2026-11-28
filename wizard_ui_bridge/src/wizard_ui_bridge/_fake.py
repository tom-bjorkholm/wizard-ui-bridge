#! /usr/local/bin/python3
"""Fake unsupported typed form fields as text fields.

A wizard may use the float, date, time, date-time or duration form
fields with a bridge that overrides ask_form() but was written before
those field types existed. Such a bridge reports through
supports_form_field() that it cannot show them. This module lets the
wizard still use one form: each unsupported field is shown as a text
field, a wrapping validator parses the text and guides the user to a
convertible value, and the text answers are converted back to the
requested typed answers.

The whole form is shown once by the bridge's own ask_form(), so the user
still sees and edits every field together. The parsing, formatting and
range messages are shared with the console and Textual forms through the
wizard_ui_bridge._parse module, so the faked fields accept exactly the
same text.

The bridge's ask_form() gets the validator as live_validator, or, with a
DeprecationWarning, as partial_validator when it was written before
live_validator existed.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import warnings
from typing import Callable, Optional, Protocol, TypedDict
from wizard_ui_bridge.form_defs import AskField, AskFields, \
    AnswerField, AnswerFields, AnswerTextField, LiveFormValidator, \
    PartialFormValidator, PartFormValidationResult, PrefillValues
from wizard_ui_bridge._help import accepts_keyword
from wizard_ui_bridge.matrix_cell_defs import PrefillValueType
from wizard_ui_bridge._parse import NEW_FIELD_TYPES, \
    fake_field, format_new_value, new_answer, resolve_new


class _FakeableBridge(Protocol):
    """The bridge methods ask_form_faking() relies on."""

    def supports_form_field(self, field: AskField) -> bool:
        """Return whether the bridge can show the field directly."""

    def ask_form(self, long_question: str, ask_fields: AskFields, *,
                 re_ask_reason: Optional[str] = None,
                 partial_validator: Optional[PartialFormValidator] = None,
                 live_validator: Optional[LiveFormValidator] = None
                 ) -> AnswerFields:
        """Show the whole form and return one answer per field."""


class LiveKwargs(TypedDict, total=False):
    """The keyword arguments that carry a validator to ask_form()."""

    live_validator: Optional[LiveFormValidator]
    partial_validator: Optional[PartialFormValidator]


def ask_form_faking(bridge: _FakeableBridge, long_question: str,
                    ask_fields: AskFields, *, re_ask_reason: Optional[str],
                    live_validator: Optional[LiveFormValidator]
                    ) -> AnswerFields:
    """Show a form, faking the fields the bridge cannot show as text.

    Raises RuntimeError when a field is unsupported and cannot be faked.
    """
    fields = list(ask_fields)
    plans = [_plan(bridge, field) for field in fields]
    is_fake = [faked for _, faked in plans]
    if not any(is_fake):
        return bridge.ask_form(long_question, fields,
                               re_ask_reason=re_ask_reason,
                               **live_kwargs(bridge.ask_form, live_validator))
    shown = [field for field, _ in plans]
    validator = _wrap_validator(fields, is_fake, live_validator)
    answers = bridge.ask_form(long_question, shown,
                              re_ask_reason=re_ask_reason,
                              **live_kwargs(bridge.ask_form, validator))
    return [_real_answer(fields[index], is_fake[index], answers[index])
            for index in range(len(fields))]


def live_kwargs(method: Callable[..., object],
                validator: Optional[LiveFormValidator]) -> LiveKwargs:
    """Return validator as keyword arguments for a bridge's ask_form().

    A method that takes neither live_validator nor **kwargs gets the
    validator as partial_validator, which it calls with a row index and
    never None, and a DeprecationWarning names the method.
    """
    if validator is None:
        return {}
    if accepts_keyword(method, 'live_validator'):
        return {'live_validator': validator}
    name = getattr(method, '__qualname__', repr(method))
    warnings.warn(f'{name}() does not accept the keyword-only parameter '
                  'live_validator. This is deprecated; please add it.',
                  DeprecationWarning, stacklevel=3)
    return {'partial_validator': validator}


def _plan(bridge: _FakeableBridge, field: AskField) -> tuple[AskField, bool]:
    """Return the field to show and whether it is a faked text field."""
    if bridge.supports_form_field(field):
        return (field, False)
    if isinstance(field, NEW_FIELD_TYPES):
        faked = fake_field(field)
        if bridge.supports_form_field(faked):
            return (faked, True)
    raise RuntimeError('the bridge cannot show a required form field type')


def _real_answer(field: AskField, is_fake: bool,
                 answer: AnswerField) -> AnswerField:
    """Return the answer of a field, converting a faked text answer."""
    if not is_fake:
        return answer
    assert isinstance(answer, AnswerTextField)
    value, _ = resolve_new(field, answer.value)
    return new_answer(field, value)


def _wrap_validator(fields: list[AskField], is_fake: list[bool],
                    caller: Optional[LiveFormValidator]) -> LiveFormValidator:
    """Return a validator over faked answers wrapping the caller's one.

    It converts the faked text answers back to typed answers for the
    caller, converts the caller's typed prefills to text for the faked
    rows, and blocks submit while any enabled faked field holds text that
    cannot be converted.
    """
    def validator(answers: AnswerFields, changed: Optional[int]
                  ) -> PartFormValidationResult:
        real = [_real_answer(fields[i], is_fake[i], answers[i])
                for i in range(len(fields))]
        base = PartFormValidationResult(True, '') if caller is None \
            else caller(real, changed)
        prefills = _convert_prefills(is_fake, base.prefill_values)
        if not base.is_valid:
            return PartFormValidationResult(False, base.message,
                                            base.disable_row_idxs, prefills)
        guide = _fake_guidance(fields, is_fake, answers,
                               set(base.disable_row_idxs))
        return PartFormValidationResult(
            guide is None, base.message if guide is None else guide,
            base.disable_row_idxs, prefills)
    return validator


def _convert_prefills(is_fake: list[bool],
                      prefills: PrefillValues) -> PrefillValues:
    """Return prefills with faked rows' typed values turned into text."""
    converted: list[tuple[int, PrefillValueType]] = []
    for index, value in prefills:
        if 0 <= index < len(is_fake) and is_fake[index]:
            converted.append((index, format_new_value(value)))
        else:
            converted.append((index, value))
    return tuple(converted)


def _fake_guidance(fields: list[AskField], is_fake: list[bool],
                   answers: AnswerFields, disabled: set[int]) -> Optional[str]:
    """Return the first enabled faked field's parse error, or None."""
    for index, field in enumerate(fields):
        if not is_fake[index] or index in disabled:
            continue
        answer = answers[index]
        assert isinstance(answer, AnswerTextField)
        _, error = resolve_new(field, answer.value)
        if error is not None:
            return error
    return None
