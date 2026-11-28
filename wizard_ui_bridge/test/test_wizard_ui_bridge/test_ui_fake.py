#! /usr/bin/env python3
"""Tests for ask_form_w_fake faking unsupported typed fields as text.

A bridge that overrides ask_form() but reports the typed fields as
unsupported gets them faked as text fields. These tests check the field
substitution, the answer conversion back to the typed answers, the
wrapping of the caller's validator, the fallback for a bridge whose
ask_form() predates live_validator, and the RuntimeError when nothing can
be shown.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import warnings
from datetime import date
from typing import Optional, Sequence

import pytest

from wizard_ui_bridge import AskField, AskFields, AskFloatField, \
    AskDateField, AskTextField, AskChoiceField, AnswerField, AnswerFields, \
    AnswerFloatField, AnswerDateField, AnswerTextField, \
    PartFormValidationResult, LiveFormValidator, PartialFormValidator, \
    PrefillValues, WizardUiBridge
from wizard_ui_bridge.form_helpers import initial_answer, live_validator_of


def _shown_answer(field: AskField, text: Optional[str]) -> AnswerField:
    """Return a scripted answer for one field the bridge was shown."""
    if isinstance(field, AskTextField):
        return AnswerTextField(field, text)
    return initial_answer(field)


# A test double implements only the ask methods its tests exercise.
# pylint: disable-next=abstract-method
class _FakeBridge(WizardUiBridge):
    """A form bridge that supports only the original field kinds.

    It records the fields and validator ask_form() was given and returns
    a scripted text answer for each shown field, so a test can inspect the
    faked form and drive the wrapped validator directly.
    """

    def __init__(self, texts: dict[int, str],
                 support_all: bool = False) -> None:
        """Store the scripted per-index texts and the support policy."""
        self._texts = texts
        self._support_all = support_all
        self.seen: list[AskField] = []
        self.validator: Optional[LiveFormValidator] = None

    def supports_form_field(self, field: AskField) -> bool:
        """Support all fields, or only the original kinds by policy."""
        if self._support_all:
            return True
        return WizardUiBridge.supports_form_field(self, field)

    def show(self, message: str) -> None:
        """Ignore shown messages in the test bridge."""
        _ = message

    def ask_form(self, long_question: str, ask_fields: AskFields, *,
                 re_ask_reason: Optional[str] = None,
                 partial_validator: Optional[PartialFormValidator] = None,
                 live_validator: Optional[LiveFormValidator] = None
                 ) -> AnswerFields:
        """Record the shown fields and validator; return scripted answers."""
        _ = (long_question, re_ask_reason)
        self.validator = live_validator_of(partial_validator, live_validator)
        return self._answers(ask_fields)

    def _answers(self, ask_fields: AskFields) -> AnswerFields:
        """Record the shown fields and return their scripted answers."""
        self.seen = list(ask_fields)
        return [_shown_answer(field, self._texts.get(index))
                for index, field in enumerate(self.seen)]


# pylint: disable-next=abstract-method
class _OldBridge(_FakeBridge):
    """A form bridge whose ask_form() predates live_validator.

    It records the partial validator it was given, which it would only
    call with a row index, never with None.
    """

    def __init__(self, texts: dict[int, str]) -> None:
        """Store the scripted texts and no partial validator yet."""
        super().__init__(texts)
        self.old_validator: Optional[PartialFormValidator] = None

    # This deliberately has the signature of a bridge written before
    # live_validator existed.
    # pylint: disable-next=arguments-differ
    def ask_form(self, long_question: str,  # type: ignore[override]
                 ask_fields: AskFields, *, re_ask_reason: Optional[str] = None,
                 partial_validator: Optional[PartialFormValidator] = None
                 ) -> AnswerFields:
        """Record the shown fields and validator; return scripted answers."""
        _ = (long_question, re_ask_reason)
        self.old_validator = partial_validator
        return self._answers(ask_fields)


# pylint: disable-next=abstract-method
class _NoSupportBridge(_FakeBridge):
    """A form bridge that cannot show any field type."""

    def supports_form_field(self, field: AskField) -> bool:
        """Report every field type as unsupported."""
        _ = field
        return False


def test_fake_converts() -> None:
    """Faked text answers convert back to the typed answers."""
    fields: list[AskField] = [AskFloatField('R', None),
                              AskDateField('D', None)]
    bridge = _FakeBridge({0: '3.5', 1: '2024-05-06'})
    answers = bridge.ask_form_w_fake('Q', fields)
    assert [type(a).__name__ for a in answers] == \
        ['AnswerFloatField', 'AnswerDateField']
    assert [a.value for a in answers] == [3.5, date(2024, 5, 6)]


def test_fake_shows_text() -> None:
    """Each unsupported field is shown to the bridge as a text field."""
    fields: list[AskField] = [AskDateField('D', 'the day')]
    bridge = _FakeBridge({0: '2024-05-06'})
    bridge.ask_form_w_fake('Q', fields)
    shown = bridge.seen[0]
    assert isinstance(shown, AskTextField)
    assert shown.help_text is not None and 'YYYY-MM-DD' in shown.help_text


def test_fake_mixed() -> None:
    """A supported field is kept while an unsupported one is faked."""
    fields: list[AskField] = [AskTextField('Name', None),
                              AskDateField('D', None)]
    bridge = _FakeBridge({0: 'Tom', 1: '2024-05-06'})
    answers = bridge.ask_form_w_fake('Q', fields)
    assert bridge.seen[0] is fields[0]
    assert isinstance(bridge.seen[1], AskTextField)
    assert answers[0].value == 'Tom'
    assert answers[1].value == date(2024, 5, 6)


def test_fake_no_faking() -> None:
    """A bridge that supports all fields is called without faking."""
    fields: list[AskField] = [
        AskDateField('D', None, default=date(2024, 1, 1))]
    bridge = _FakeBridge({}, support_all=True)
    answers = bridge.ask_form_w_fake('Q', fields)
    assert bridge.seen[0] is fields[0]
    assert isinstance(answers[0], AnswerDateField)
    assert answers[0].value == date(2024, 1, 1)


def test_fake_runtime_error() -> None:
    """A bridge that can show nothing raises RuntimeError."""
    bridge = _NoSupportBridge({})
    with pytest.raises(RuntimeError, match='cannot show'):
        bridge.ask_form_w_fake('Q', [AskDateField('D', None)])


def _drive(bridge: _FakeBridge, fields: list[AskField],
           validator: LiveFormValidator) -> LiveFormValidator:
    """Run ask_form_w_fake and return the wrapped validator it installed."""
    bridge.ask_form_w_fake('Q', fields, live_validator=validator)
    assert bridge.validator is not None
    return bridge.validator


def test_fake_validator_typed() -> None:
    """The wrapped validator passes typed answers to the caller."""
    fields: list[AskField] = [AskFloatField('R', None)]
    seen: list[Sequence[AnswerField]] = []

    def caller(answers: AnswerFields,
               changed: Optional[int]) -> PartFormValidationResult:
        _ = changed
        seen.append(list(answers))
        return PartFormValidationResult(True, '')
    bridge = _FakeBridge({0: '3.5'})
    wrapped = _drive(bridge, fields, caller)
    faked = AnswerTextField(_text_field(bridge, 0), '3.5')
    wrapped([faked], 0)
    assert isinstance(seen[0][0], AnswerFloatField)
    assert seen[0][0].value == 3.5


def test_fake_guidance() -> None:
    """The wrapped validator blocks while a faked value cannot convert."""
    fields: list[AskField] = [AskFloatField('R', None)]

    def caller(answers: AnswerFields,
               changed: Optional[int]) -> PartFormValidationResult:
        _ = (answers, changed)
        return PartFormValidationResult(True, '')
    bridge = _FakeBridge({0: 'x'})
    wrapped = _drive(bridge, fields, caller)
    result = wrapped([AnswerTextField(_text_field(bridge, 0), 'x')], 0)
    assert result.is_valid is False
    assert 'a number' in result.message


def test_fake_prefill_convert() -> None:
    """A caller prefill for a faked row is converted to text."""
    name = AskTextField('A', None)
    fields: list[AskField] = [name, AskDateField('D', None)]

    def caller(answers: AnswerFields,
               changed: Optional[int]) -> PartFormValidationResult:
        _ = (answers, changed)
        prefill: PrefillValues = ((1, date(2024, 5, 6)),)
        return PartFormValidationResult(True, '', (), prefill)
    bridge = _FakeBridge({0: 'Tom', 1: '2024-05-06'})
    wrapped = _drive(bridge, fields, caller)
    answers = [AnswerTextField(name, 'Tom'),
               AnswerTextField(_text_field(bridge, 1), '2024-05-06')]
    result = wrapped(answers, 0)
    assert result.prefill_values == ((1, '2024-05-06'),)


def test_fake_unsupported() -> None:
    """An unsupported non-typed field cannot be faked and errors."""
    bridge = _NoSupportBridge({})
    with pytest.raises(RuntimeError, match='cannot show'):
        bridge.ask_form_w_fake('Q', [AskTextField('T', None)])


def test_fake_nullable_choice() -> None:
    """The base bridge rejects a nullable choice, which cannot be faked."""
    bridge = _FakeBridge({})
    field = AskChoiceField('C', None, choices=('a',), nullable=True)
    with pytest.raises(RuntimeError, match='cannot show'):
        bridge.ask_form_w_fake('Q', [field])


def test_fake_caller_invalid() -> None:
    """The wrapped validator returns the caller's failure and prefills."""
    fields: list[AskField] = [AskDateField('D', None)]

    def caller(answers: AnswerFields,
               changed: Optional[int]) -> PartFormValidationResult:
        _ = (answers, changed)
        prefill: PrefillValues = ((0, date(2024, 1, 1)),)
        return PartFormValidationResult(False, 'nope', (), prefill)
    bridge = _FakeBridge({0: '2024-05-06'})
    wrapped = _drive(bridge, fields, caller)
    faked = AnswerTextField(_text_field(bridge, 0), '2024-05-06')
    result = wrapped([faked], 0)
    assert result.is_valid is False
    assert result.message == 'nope'
    assert result.prefill_values == ((0, '2024-01-01'),)


def test_fake_prefill_kept() -> None:
    """A prefill for a non-faked or out-of-range row passes unchanged."""
    name = AskTextField('A', None)
    fields: list[AskField] = [name, AskDateField('D', None)]

    def caller(answers: AnswerFields,
               changed: Optional[int]) -> PartFormValidationResult:
        _ = (answers, changed)
        prefill: PrefillValues = ((0, 'kept'), (5, 'far'))
        return PartFormValidationResult(True, '', (), prefill)
    bridge = _FakeBridge({0: 'Tom', 1: '2024-05-06'})
    wrapped = _drive(bridge, fields, caller)
    answers = [AnswerTextField(name, 'Tom'),
               AnswerTextField(_text_field(bridge, 1), '2024-05-06')]
    result = wrapped(answers, 0)
    assert result.prefill_values == ((0, 'kept'), (5, 'far'))


def _text_field(bridge: _FakeBridge, index: int) -> AskTextField:
    """Return the faked text field the bridge was shown at index."""
    field = bridge.seen[index]
    assert isinstance(field, AskTextField)
    return field


def test_fake_old_bridge() -> None:
    """A bridge without live_validator gets it as partial_validator."""
    fields: list[AskField] = [AskDateField('D', None)]

    def caller(answers: AnswerFields,
               changed: Optional[int]) -> PartFormValidationResult:
        _ = (answers, changed)
        return PartFormValidationResult(True, '')
    bridge = _OldBridge({0: '2024-05-06'})
    with pytest.warns(DeprecationWarning, match='_OldBridge.ask_form'):
        answers = bridge.ask_form_w_fake('Q', fields, live_validator=caller)
    assert bridge.old_validator is not None
    assert answers[0].value == date(2024, 5, 6)


def test_old_no_validator() -> None:
    """A bridge without live_validator gets no warning with no validator.

    Nothing is faked, so no wrapping validator is installed either.
    """
    bridge = _OldBridge({0: 'Tom'})
    with warnings.catch_warnings():
        warnings.simplefilter('error')
        answers = bridge.ask_form_w_fake('Q', [AskTextField('T', None)])
    assert bridge.old_validator is None
    assert answers[0].value == 'Tom'


def test_fake_passes_none() -> None:
    """The wrapped validator passes None on to the caller's validator."""
    calls: list[Optional[int]] = []

    def caller(answers: AnswerFields,
               changed: Optional[int]) -> PartFormValidationResult:
        _ = answers
        calls.append(changed)
        return PartFormValidationResult(True, '')
    bridge = _FakeBridge({0: '3.5'})
    wrapped = _drive(bridge, [AskFloatField('R', None)], caller)
    wrapped([AnswerTextField(_text_field(bridge, 0), '3.5')], None)
    assert calls == [None]


def test_fake_deprecated() -> None:
    """A deprecated partial_validator warns once, at ask_form_w_fake()."""
    calls: list[int] = []

    def old(answers: AnswerFields, index: int) -> PartFormValidationResult:
        _ = answers
        calls.append(index)
        return PartFormValidationResult(True, '')
    bridge = _FakeBridge({0: '3.5'})
    with pytest.warns(DeprecationWarning) as record:
        bridge.ask_form_w_fake('Q', [AskFloatField('R', None)],
                               partial_validator=old)
    assert len(record) == 1
    assert bridge.validator is not None
    bridge.validator([AnswerTextField(_text_field(bridge, 0), '3.5')], None)
    assert calls == [0]
