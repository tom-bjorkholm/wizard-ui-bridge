#! /usr/local/bin/python3
"""Tests for the whole-form editor."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter as tk
from tkinter import ttk
from datetime import date
from pathlib import Path
from typing import Optional, Sequence
import pytest
from wizard_ui_bridge import AnswerFields, AnswerField, AskField, \
    PartFormValidationResult, LiveFormValidator, PathAskOptions, \
    PrefillValues, WizardPathKind, AskTextField, AskIntField, AskPathField, \
    AskYesNoField, AskChoiceField, AskMultiChoiceField, AskFloatField, \
    AskDateField, AskDurationField, AnswerTextField, AnswerIntField, \
    AnswerPathField, AnswerYesNoField, AnswerChoiceField, \
    AnswerMultiChoiceField, AnswerFloatField, AnswerDateField
from wizard_tk_bridge.auto_scroll import _wheel_area
from wizard_tk_bridge.wizard_form import FormEditor, handles_field
from .gui_test_helpers import gui_root, record_focus


def _build(root: tk.Tk, fields: Sequence[AskField],
           validator: Optional[LiveFormValidator] = None
           ) -> tuple[FormEditor, list[list[AnswerField]]]:
    """Build a form editor recording every submitted answer set."""
    recorded: list[list[AnswerField]] = []
    editor = FormEditor(tk.Frame(root), fields, validator, recorded.append)
    return editor, recorded


def test_form_text_default() -> None:
    """Test a text field starts from its default answer."""
    with gui_root() as root:
        field = AskTextField('Name', None, default='Bob')
        editor, _ = _build(root, [field])
        assert editor.answers() == [AnswerTextField(field, 'Bob')]


def test_form_sensitive_masks() -> None:
    """Test a sensitive text field masks its entry text."""
    with gui_root() as root:
        field = AskTextField('PW', None, sensitive=True)
        editor, _ = _build(root, [field])
        # pylint: disable-next=protected-access
        widget = editor._rows[0].cell_input.widget
        assert isinstance(widget, tk.Entry) and widget.cget('show') == '*'


def test_form_int_default() -> None:
    """Test an integer field starts from its default answer."""
    with gui_root() as root:
        field = AskIntField('Age', None, default=7)
        editor, _ = _build(root, [field])
        assert editor.answers() == [AnswerIntField(field, 7)]


def test_form_yes_no_default() -> None:
    """Test a yes/no field starts from its default answer."""
    with gui_root() as root:
        field = AskYesNoField('OK?', None, default=True)
        editor, _ = _build(root, [field])
        assert editor.answers() == [AnswerYesNoField(field, True)]


def test_form_multi_default() -> None:
    """Test a multi-select field starts with its defaults selected."""
    with gui_root() as root:
        field = AskMultiChoiceField('Cols', None, choices=('a', 'b', 'c'),
                                    default=('a', 'c'))
        editor, _ = _build(root, [field])
        answer = editor.answers()[0]
        assert isinstance(answer, AnswerMultiChoiceField)
        assert answer.value == ['a', 'c']


def test_form_submit_ok() -> None:
    """Test submitting a valid form passes the answers on."""
    with gui_root() as root:
        field = AskChoiceField('Pick', None, choices=('a', 'b'), default='a')
        editor, recorded = _build(root, [field])
        editor.submit()
        assert recorded == [[AnswerChoiceField(field, 'a')]]


def test_form_choice_required() -> None:
    """Test a choice with no default blocks submit until answered."""
    with gui_root() as root:
        field = AskChoiceField('Pick', None, choices=('a', 'b'))
        editor, recorded = _build(root, [field])
        assert editor.answers() == [AnswerChoiceField(field, None)]
        editor.submit()
        assert not recorded
        # pylint: disable-next=protected-access
        assert editor._status.cget('text') != ''


def test_form_null_choice() -> None:
    """Test a blank nullable choice submits None, its list led by blank."""
    with gui_root() as root:
        field = AskChoiceField('Pick', None, choices=('a', 'b'), nullable=True)
        editor, recorded = _build(root, [field])
        # pylint: disable-next=protected-access
        widget = editor._rows[0].cell_input.widget
        assert isinstance(widget, ttk.Combobox)
        assert list(widget.cget('values')) == ['', 'a', 'b']
        editor.submit()
        assert recorded == [[AnswerChoiceField(field, None)]]


def test_form_null_reblank() -> None:
    """Test picking the blank entry empties a chosen nullable choice."""
    with gui_root() as root:
        field = AskChoiceField('Pick', None, choices=('a', 'b'), nullable=True)
        editor, _ = _build(root, [field])
        # pylint: disable-next=protected-access
        widget = editor._rows[0].cell_input.widget
        assert isinstance(widget, ttk.Combobox)
        widget.set('a')
        assert editor.answers() == [AnswerChoiceField(field, 'a')]
        widget.set('')
        assert editor.answers() == [AnswerChoiceField(field, None)]


def test_form_int_oor_blocks() -> None:
    """Test an out-of-range integer blocks submit and is reported."""
    with gui_root() as root:
        field = AskIntField('Age', None, min_value=1, max_value=5)
        editor, recorded = _build(root, [field])
        # pylint: disable-next=protected-access
        entry = editor._rows[0].cell_input.widget
        assert isinstance(entry, tk.Entry)
        entry.insert(0, '9')
        editor.submit()
        assert not recorded
        # pylint: disable-next=protected-access
        assert 'between 1 and 5' in editor._status.cget('text')


def test_field_error_labelled() -> None:
    """Test a field's own error is prefixed with its label."""
    with gui_root() as root:
        field = AskIntField('Age', None, min_value=1, max_value=5)
        editor, _ = _build(root, [field])
        # pylint: disable-next=protected-access
        entry = editor._rows[0].cell_input.widget
        assert isinstance(entry, tk.Entry)
        entry.insert(0, '9')
        # pylint: disable-next=protected-access
        message = editor._field_error(0)
        assert message is not None and message.startswith('Age: ')


def test_form_multi_min() -> None:
    """Test selecting fewer than the minimum blocks submit."""
    with gui_root() as root:
        field = AskMultiChoiceField('Cols', None, choices=('a', 'b'),
                                    min_select=1)
        editor, recorded = _build(root, [field])
        editor.submit()
        assert not recorded


def test_form_path_value(tmp_path: Path) -> None:
    """Test a path field reports and submits its accepted default path."""
    with gui_root() as root:
        target = tmp_path / 'f.txt'
        target.write_text('x')
        options = PathAskOptions(kind=WizardPathKind.EXISTING_FILE,
                                 default=target)
        field = AskPathField('File', None, options)
        editor, recorded = _build(root, [field])
        assert editor.answers() == [AnswerPathField(field, target)]
        editor.submit()
        assert recorded == [[AnswerPathField(field, target)]]


def test_form_path_required() -> None:
    """Test an empty required path blocks submit."""
    with gui_root() as root:
        field = AskPathField('File', None,
                             PathAskOptions(kind=WizardPathKind.FILE))
        editor, recorded = _build(root, [field])
        editor.submit()
        assert not recorded
        # pylint: disable-next=protected-access
        assert editor._status.cget('text') != ''


def _invalid(_answers: AnswerFields,
             _index: Optional[int]) -> PartFormValidationResult:
    """Return a validator result that always rejects the form."""
    return PartFormValidationResult(False, 'nope')


def test_form_valid_blocks() -> None:
    """Test a rejecting validator blocks submit and shows its message."""
    with gui_root() as root:
        field = AskTextField('Name', None, default='x')
        editor, recorded = _build(root, [field], _invalid)
        editor.submit()
        assert not recorded
        # pylint: disable-next=protected-access
        assert editor._status.cget('text') == 'nope'


def _disable_second(_answers: AnswerFields,
                    _index: Optional[int]) -> PartFormValidationResult:
    """Return a validator result that disables the second row."""
    return PartFormValidationResult(True, '', (1,))


def test_form_valid_disable() -> None:
    """Test a disabled row is skipped so its own error never blocks."""
    with gui_root() as root:
        first = AskChoiceField('Fmt', None, choices=('a', 'b'), default='a')
        second = AskChoiceField('Delim', None, choices=(',', ';'))
        editor, recorded = _build(root, [first, second], _disable_second)
        # pylint: disable-next=protected-access
        assert 1 in editor._disabled
        editor.submit()
        assert len(recorded) == 1
        answers = recorded[0]
        assert answers[1] == AnswerChoiceField(second, None)


def test_form_live_error() -> None:
    """Test a field change shows the changed field's own error live."""
    with gui_root() as root:
        field = AskIntField('Age', None, min_value=1, max_value=5)
        editor, _ = _build(root, [field])
        # pylint: disable-next=protected-access
        entry = editor._rows[0].cell_input.widget
        assert isinstance(entry, tk.Entry)
        entry.insert(0, '9')
        # pylint: disable-next=protected-access
        editor._changed(0)
        # pylint: disable-next=protected-access
        assert 'between 1 and 5' in editor._status.cget('text')


def test_form_disable_state() -> None:
    """Test applying and clearing disabled rows toggles widget state."""
    with gui_root() as root:
        field = AskTextField('Name', None)
        editor, _ = _build(root, [field])
        # pylint: disable-next=protected-access
        editor._apply_disabled((0,))
        # pylint: disable-next=protected-access
        row = editor._rows[0]
        assert str(row.cell_input.widget.cget('state')) == 'disabled'
        # pylint: disable-next=protected-access
        editor._apply_disabled(())
        assert str(row.cell_input.widget.cget('state')) == 'normal'


def test_form_tooltip_help() -> None:
    """Test a field with help text gets a tooltip carrying that text."""
    with gui_root() as root:
        field = AskTextField('Name', 'Type your name')
        editor, _ = _build(root, [field])
        # pylint: disable-next=protected-access
        row = editor._rows[0]
        assert row.tooltip is not None
        assert row.tooltip.text == 'Type your name'


def test_form_no_tooltip() -> None:
    """Test a field without help text gets no tooltip."""
    with gui_root() as root:
        field = AskTextField('Name', None)
        editor, _ = _build(root, [field])
        # pylint: disable-next=protected-access
        assert editor._rows[0].tooltip is None


def test_multi_error_bounds() -> None:
    """Test a multi-select row reports too few and too many, accepts in range.

    With no pick the count is below the minimum, two picks exceed the
    maximum, and a single pick meets the exactly-one requirement.
    """
    with gui_root() as root:
        field = AskMultiChoiceField('Cols', None, choices=('a', 'b', 'c'),
                                    min_select=1, max_select=1)
        editor, _ = _build(root, [field])
        # pylint: disable-next=protected-access
        assert editor._field_error(0) is not None
        # pylint: disable-next=protected-access
        listbox = editor._rows[0].cell_input.widget
        assert isinstance(listbox, tk.Listbox)
        listbox.selection_set(0, 1)
        # pylint: disable-next=protected-access
        assert editor._field_error(0) is not None
        listbox.selection_clear(0, 'end')
        listbox.selection_set(0)
        # pylint: disable-next=protected-access
        assert editor._field_error(0) is None


def test_form_disable_path() -> None:
    """Test disabling a path row disables it through the path helper."""
    with gui_root() as root:
        field = AskPathField('File', None,
                             PathAskOptions(kind=WizardPathKind.FILE))
        editor, _ = _build(root, [field])
        # pylint: disable-next=protected-access
        editor._apply_disabled((0,))
        # pylint: disable-next=protected-access
        row = editor._rows[0]
        assert row.cell_input.path is not None
        # pylint: disable-next=protected-access
        assert str(row.cell_input.path._entry.cget('state')) == 'disabled'


def test_form_live_validator() -> None:
    """Test a live change runs the whole-form validator and shows it."""
    with gui_root() as root:
        field = AskChoiceField('Fmt', None, choices=('a', 'b'), default='a')
        editor, _ = _build(root, [field], _invalid)
        # pylint: disable-next=protected-access
        editor._changed(0)
        # pylint: disable-next=protected-access
        assert editor._status.cget('text') == 'nope'


def test_disabled_row_change() -> None:
    """Test a change on a disabled row hides that row's own error.

    The validator disables the second row, so a change there shows the
    validator's message (empty) instead of the row's own required error.
    """
    with gui_root() as root:
        first = AskChoiceField('Fmt', None, choices=('a', 'b'), default='a')
        second = AskChoiceField('Delim', None, choices=(',', ';'))
        editor, _ = _build(root, [first, second], _disable_second)
        # pylint: disable-next=protected-access
        assert 1 in editor._disabled
        # pylint: disable-next=protected-access
        editor._changed(1)
        # pylint: disable-next=protected-access
        assert editor._status.cget('text') == ''


def test_handles_field() -> None:
    """Test the form reports it can show the typed field kinds."""
    assert handles_field(AskFloatField('n', None)) is True
    assert handles_field(AskDateField('d', None)) is True
    nullable = AskChoiceField('c', None, choices=('a',), nullable=True)
    assert handles_field(nullable) is True


def test_form_float_default() -> None:
    """Test a float field starts from its default answer."""
    with gui_root() as root:
        field = AskFloatField('Amount', None, default=1.5)
        editor, _ = _build(root, [field])
        assert editor.answers() == [AnswerFloatField(field, 1.5)]


def test_form_float_required() -> None:
    """Test a required float with no default blocks submit."""
    with gui_root() as root:
        field = AskFloatField('Amount', None)
        editor, recorded = _build(root, [field])
        editor.submit()
        assert not recorded
        # pylint: disable-next=protected-access
        assert editor._status.cget('text') != ''


def test_form_date_read() -> None:
    """Test a date field reads the ISO text typed into its entry."""
    with gui_root() as root:
        field = AskDateField('When', None)
        editor, _ = _build(root, [field])
        # pylint: disable-next=protected-access
        row = editor._rows[0]
        assert row.cell_input.typed is not None
        row.cell_input.typed.set_text('2026-07-24')
        answer = editor.answers()[0]
        assert isinstance(answer, AnswerDateField)
        assert answer.value == date(2026, 7, 24)


def test_form_disable_typed() -> None:
    """Test disabling a typed row disables its entry widget."""
    with gui_root() as root:
        field = AskDurationField('Length', None)
        editor, _ = _build(root, [field])
        # pylint: disable-next=protected-access
        editor._apply_disabled((0,))
        # pylint: disable-next=protected-access
        widget = editor._rows[0].cell_input.widget
        assert str(widget.cget('state')) == 'disabled'


def _prefill_date(_answers: AnswerFields,
                  _index: Optional[int]) -> PartFormValidationResult:
    """Return a validator result prefilling the second row with a date."""
    return PartFormValidationResult(True, '', (), ((1, date(2026, 8, 1)),))


def test_form_prefill_applied() -> None:
    """Test a validator prefill is written into its target row's input."""
    with gui_root() as root:
        first = AskTextField('Name', None, default='x')
        second = AskDateField('When', None, nullable=True)
        editor, _ = _build(root, [first, second], _prefill_date)
        # pylint: disable-next=protected-access
        row = editor._rows[1]
        assert row.cell_input.typed is not None
        assert row.cell_input.typed.text() == '2026-08-01'


def _basic_fields() -> list[AskField]:
    """Return one field of each non-typed kind, in a fixed order."""
    return [
        AskTextField('Name', None),
        AskIntField('Age', None),
        AskPathField('File', None, PathAskOptions()),
        AskYesNoField('OK?', None, default=False),
        AskChoiceField('Pick', None, choices=('a', 'b')),
        AskMultiChoiceField('Cols', None, choices=('a', 'b', 'c'))]


def test_write_value_kinds() -> None:
    """Test a prefill writes the right value into every non-typed kind.

    A value of each basic field type flows through CellInput.write() and its
    setters, and is then read back through the row's own answer.
    """
    prefills: PrefillValues = ((0, 'Bob'), (1, 42), (2, Path('/x/y')),
                               (3, True), (4, 'b'), (5, ['a', 'c']))

    def rule(_answers: AnswerFields,
             _index: Optional[int]) -> PartFormValidationResult:
        return PartFormValidationResult(True, '', (), prefills)
    with gui_root() as root:
        editor, _ = _build(root, _basic_fields(), rule)
        answers = editor.answers()
        assert isinstance(answers[0], AnswerTextField)
        assert answers[0].value == 'Bob'
        assert isinstance(answers[1], AnswerIntField)
        assert answers[1].value == 42
        assert isinstance(answers[2], AnswerPathField)
        assert answers[2].value == Path('/x/y')
        assert isinstance(answers[3], AnswerYesNoField)
        assert answers[3].value is True
        assert isinstance(answers[4], AnswerChoiceField)
        assert answers[4].value == 'b'
        assert isinstance(answers[5], AnswerMultiChoiceField)
        assert answers[5].value == ['a', 'c']


def test_form_wheel_area() -> None:
    """Test a field of the form sits in the wheel-scrolling area."""
    with gui_root() as root:
        editor, _ = _build(root, [AskTextField('Name', None, default='Bob')])
        # pylint: disable-next=protected-access
        assert _wheel_area(editor._rows[0].cell_input.widget) is not None


# pylint: disable-next=too-few-public-methods
class _Validator:
    """A live validator recording its calls and giving a set result."""

    def __init__(self, result: PartFormValidationResult) -> None:
        """Keep the result to return and start with no calls."""
        self.result = result
        self.calls: list[Optional[int]] = []

    def __call__(self, _answers: AnswerFields,
                 changed: Optional[int]) -> PartFormValidationResult:
        """Record the call and return the set result."""
        self.calls.append(changed)
        return self.result


def test_form_open_none() -> None:
    """Test the validator gets None at open and on an unchanged submit.

    Its message is not shown when the form opens, only on submit.
    """
    rule = _Validator(PartFormValidationResult(False, 'nope'))
    with gui_root() as root:
        editor, recorded = _build(root, [AskTextField('A', None)], rule)
        # pylint: disable-next=protected-access
        assert editor._status.cget('text') == ''
        editor.submit()
        # pylint: disable-next=protected-access
        assert editor._status.cget('text') == 'nope'
    assert rule.calls == [None, None]
    assert not recorded


def test_form_open_prefill() -> None:
    """Test a prefill aimed at row 0 is applied when the form opens."""
    rule = _Validator(PartFormValidationResult(True, '', (), ((0, 'pre'),)))
    with gui_root() as root:
        field = AskTextField('A', None)
        editor, _ = _build(root, [field], rule)
        assert editor.answers() == [AnswerTextField(field, 'pre')]


def test_form_submit_disable() -> None:
    """Test a row the validator disables on submit is not checked."""
    rule = _Validator(PartFormValidationResult(True, ''))
    with gui_root() as root:
        first = AskTextField('A', None, default='x')
        second = AskChoiceField('Delim', None, choices=(',', ';'))
        editor, recorded = _build(root, [first, second], rule)
        # pylint: disable-next=protected-access
        assert not editor._disabled
        rule.result = PartFormValidationResult(True, '', (1,))
        editor.submit()
    assert len(recorded) == 1


@pytest.mark.parametrize('validator', [None, _invalid])
def test_form_invalid_focus(monkeypatch: pytest.MonkeyPatch,
                            validator: Optional[LiveFormValidator]) -> None:
    """Test submit focuses the first invalid row, before the validator."""
    focused = record_focus(monkeypatch)
    with gui_root() as root:
        fields: list[AskField] = [
            AskTextField('A', None, default='x'),
            AskIntField('Age', None, min_value=1, max_value=5),
            AskIntField('Size', None, min_value=1, max_value=5)]
        editor, recorded = _build(root, fields, validator)
        # pylint: disable-next=protected-access
        rows = editor._rows
        for row in rows[1:]:
            entry = row.cell_input.widget
            assert isinstance(entry, tk.Entry)
            entry.insert(0, '9')
        editor.submit()
        assert focused == [rows[1].cell_input.main_widget()]
        # pylint: disable-next=protected-access
        assert 'Age' in editor._status.cget('text')
    assert not recorded
