#! /usr/local/bin/python3
"""Textual full-screen user interface bridge for the wizard.

This module provides the concrete Textual bridge used when the wizard
talks to a user through a real terminal. Each ask method runs a short
lived Textual application for one question and returns its result, which
keeps the one-question-at-a-time contract of WizardUiBridge while giving
the user a full-screen interface with selectable lists, check boxes and
editable tables.

Navigation keys exit a screen with no value and record which
WizardNavigation request to raise, so the bridge re-raises it after the
screen closes. Messages passed to show() and diagnostics written to
error_file() are buffered and rendered in the header of the next
screen, so nothing is written straight to the terminal where it would
corrupt the Textual display.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from __future__ import annotations
from datetime import date
from functools import partial
from io import StringIO
from pathlib import Path
from typing import ClassVar, Iterator, Literal, Optional, Sequence, \
    TypeVar, overload
from textual import on
from textual.app import ComposeResult
from textual.binding import BindingType
from textual.containers import Grid, VerticalScroll
from textual.widget import Widget
from textual.widgets import Button, Checkbox, Footer, Input, \
    OptionList, Select, SelectionList, Static
from textual.widgets.selection_list import Selection
from wizard_ui_bridge.bridge import WizardUiBridge
from wizard_ui_bridge.bridge_helpers import check_text_args, INT_ERROR, \
    int_text, multi_count_message, out_of_range, path_answer, range_error, \
    text_answer, offered_choices
from wizard_ui_bridge.form_helpers import initial_answer
from wizard_ui_bridge._form_prefill import apply_prefills
from wizard_ui_bridge._parse import NEW_FIELD_TYPES, \
    value_from_text, error_from_text, new_answer
from wizard_ui_bridge._calendar import _CalendarScreen
from wizard_ui_bridge._textual_nav import _NavApp
from wizard_ui_bridge._textual_table import _TableApp
from wizard_ui_bridge._textual_widgets import \
    _header_widgets, _default_index, _preselected, _make_field_widget, \
    _field_index, _browse_index, _pick_index, _multi_error, \
    _calendar_setup, _combined_text, _field_message, _apply_width
from wizard_ui_bridge._path import _PathPick, \
    _PickerScreen, _start_dir, _start_value
from wizard_ui_bridge.arg_types import PartialCheck, WizardAbort, \
    PathAskOptions, TableColumn, TableCell, check_choice_args, \
    check_multi_args
from wizard_ui_bridge.form_defs import AskField, AskFields, \
    ALL_ASK_FIELD_TYPES, AnswerField, AnswerFields, PartialFormValidator, \
    AskTextField, AskIntField, AskPathField, AskYesNoField, AskChoiceField, \
    AskMultiChoiceField, AskDateField, AskDateTimeField, AnswerTextField, \
    AnswerIntField, AnswerPathField, AnswerYesNoField, AnswerChoiceField, \
    AnswerMultiChoiceField

_CAL_TOKEN = '?'

_T = TypeVar('_T')
_CHOICE_REQUIRED = 'Please choose a value.'


class _TextApp(_NavApp[str]):
    """Free-text screen returning the string the user typed."""

    def __init__(self, question: str, messages: list[str], value: str = '',
                 password: bool = False) -> None:
        """Store the prompt, buffered messages and input settings."""
        super().__init__()
        self._question = question
        self._messages = messages
        self._value = value
        self._password = password

    def compose(self) -> ComposeResult:
        """Lay out the header, the input field and the footer."""
        yield from _header_widgets(self._messages, self._question)
        yield Input(value=self._value, password=self._password)
        yield Footer()

    @on(Input.Submitted)
    def _entered(self, event: Input.Submitted) -> None:
        """Exit returning the entered text, empty when nothing typed."""
        self.exit(event.value)


class _PathApp(_PathPick, _NavApp[str]):
    """Path screen with a filesystem tree and editable path input."""

    BINDINGS: ClassVar[list[BindingType]] = [('ctrl+s', 'submit', 'Submit')]

    def __init__(self, question: str, messages: list[str],
                 options: PathAskOptions, value: Optional[str]) -> None:
        """Store prompt, path options and initial input state."""
        super().__init__()
        self._question = question
        self._messages = messages
        self._kind = options.kind
        self._start = _start_dir(options.start_or_default)
        self._value = _start_value(value, options.start_or_default)

    def compose(self) -> ComposeResult:
        """Lay out the header, directory tree, path input and footer."""
        yield from _header_widgets(self._messages, self._question)
        yield from self.pick_widgets(self._start, self._value)
        yield Button('Submit', id='submit')
        yield Footer()

    @on(Button.Pressed, '#submit')
    def _submit_clicked(self, _event: Button.Pressed) -> None:
        """Submit the current input when the button is pressed."""
        self.action_submit()

    def _confirm(self, value: str) -> None:
        """Exit returning the confirmed path input."""
        self.exit(value)


class _ChoiceApp(_NavApp[int]):
    """Single-choice screen returning the chosen 0-based index."""

    def __init__(self, question: str, choices: list[str],
                 default_index: Optional[int], messages: list[str]) -> None:
        """Store the prompt, choices and the index to highlight."""
        super().__init__()
        self._question = question
        self._choices = choices
        self._default_index = default_index
        self._messages = messages

    def compose(self) -> ComposeResult:
        """Lay out the header, the option list and the footer."""
        yield from _header_widgets(self._messages, self._question)
        yield OptionList(*self._choices)
        yield Footer()

    def on_mount(self) -> None:
        """Highlight the default option when one is given."""
        if self._default_index is not None:
            self.query_one(OptionList).highlighted = self._default_index

    @on(OptionList.OptionSelected)
    def _picked(self, event: OptionList.OptionSelected) -> None:
        """Exit returning the index of the selected option."""
        self.exit(event.option_index)


class _MultiApp(_NavApp[list[int]]):
    """Multi-choice screen returning the chosen 0-based indexes."""

    BINDINGS: ClassVar[list[BindingType]] = [('ctrl+s', 'submit', 'Submit')]
    _list: SelectionList[int]

    # pylint: disable-next=too-many-arguments,too-many-positional-arguments
    def __init__(self, question: str, choices: list[str],
                 preselected: list[int], min_select: int,
                 max_select: Optional[int], messages: list[str]) -> None:
        """Store the prompt, choices, preselection and count limits."""
        super().__init__()
        self._question = question
        self._choices = choices
        self._preselected = set(preselected)
        self._min_select = min_select
        self._max_select = max_select
        self._messages = messages

    def compose(self) -> ComposeResult:
        """Lay out the header, the check-box list, submit and footer."""
        yield from _header_widgets(self._messages, self._question)
        self._list = SelectionList[int](*self._selections())
        yield self._list
        yield Button('Submit', id='submit')
        yield Static('', id='multi_error')
        yield Footer()

    def _selections(self) -> list[Selection[int]]:
        """Return one selection per choice, preselected as requested."""
        return [Selection(choice, index, index in self._preselected)
                for index, choice in enumerate(self._choices)]

    @on(Button.Pressed)
    def _clicked(self, _event: Button.Pressed) -> None:
        """Treat a click on the submit button like the submit action."""
        self.action_submit()

    def action_submit(self) -> None:
        """Exit with the selection, or show why the count is wrong."""
        chosen = list(self._list.selected)
        message = multi_count_message(len(chosen), self._min_select,
                                      self._max_select)
        if message is None:
            self.exit(chosen)
            return
        self.query_one('#multi_error', Static).update(message)


# pylint: disable-next=too-many-instance-attributes
class _FormApp(_NavApp[list[AnswerField]]):
    """One screen showing every form field in a two-column grid.

    The left column of each row is a label with the field's short
    question and the right column an input widget chosen by the field
    type: a text input, an integer input, a path input with a Browse
    button, a check box, a drop-down, a check-box list, a text input with
    a calendar Pick button for a date or date-time field, and a plain text
    input for a float, time or duration field. A partial validator, when
    given, runs after each change to show advisory feedback and to enable
    or disable rows. On submit each enabled field is validated, so the
    returned answers are complete and a choice with no default is always
    answered.

    A rejected field is named in the shared status line and its label is
    shown in the error colour, so the user sees which of the fields on
    the screen the message is about.
    """

    BINDINGS: ClassVar[list[BindingType]] = [('ctrl+s', 'submit', 'Submit')]
    CSS = '''
    #form_grid { height: auto; }
    #form_grid .field_error { color: $error; text-style: bold; }
    #form_grid Horizontal { height: auto; width: 1fr; }
    #form_grid Horizontal Input { width: 1fr; }
    #form_grid Horizontal Button { width: auto; margin-left: 1; }
    /* A definite max-height lets the auto-height grid size this row;
       the inherited 100% is parent-relative and collapses it to a
       sliver. A longer list scrolls inside these rows. */
    #form_grid SelectionList { max-height: 10; }
    '''

    def __init__(self, question: str, fields: list[AskField],
                 messages: list[str],
                 validator: Optional[PartialFormValidator]) -> None:
        """Store the prompt, fields, buffered messages and validator."""
        super().__init__()
        self._question = question
        self._fields = fields
        self._messages = messages
        self._validator = validator
        self._answers = [initial_answer(field) for field in fields]
        self._disabled: set[int] = set()
        self._last_changed = 0
        self._form_ready = False

    def compose(self) -> ComposeResult:
        """Lay out the header, the field grid, submit and footer."""
        yield from _header_widgets(self._messages, self._question)
        with VerticalScroll(id='form_scroll'), Grid(id='form_grid'):
            yield from self._field_widgets()
        yield Button('Submit', id='submit')
        yield Static('', id='form_status')
        yield Footer()

    def _field_widgets(self) -> Iterator[Widget]:
        """Yield a label and an input widget for each field."""
        for index, field in enumerate(self._fields):
            label = Static(field.short_question, id=f'label_{index}')
            widget = _make_field_widget(field, index)
            if field.help_text is not None:
                label.tooltip = field.help_text
                widget.tooltip = field.help_text
            yield label
            yield widget

    def on_mount(self) -> None:
        """Size the grid and inputs, focus the first field, not the scroll.

        An input with a width hint keeps that width; the others fill
        their grid column.
        """
        self.query_one('#form_scroll').can_focus = False
        self.query_one('#form_grid', Grid).styles.grid_size_columns = 2
        for index, field in enumerate(self._fields):
            _apply_width(self.query_one(f'#field_{index}'), field.width)
        if self._fields:
            self.query_one('#field_0').focus()
        self._form_ready = True

    @on(Input.Changed)
    def _input_changed(self, event: Input.Changed) -> None:
        """React to a text, integer or path field change."""
        self._changed(event.input.id)

    @on(Select.Changed)
    def _select_changed(self, event: Select.Changed) -> None:
        """React to a choice drop-down change."""
        self._changed(event.select.id)

    @on(Checkbox.Changed)
    def _checkbox_changed(self, event: Checkbox.Changed) -> None:
        """React to a yes/no check-box change."""
        self._changed(event.checkbox.id)

    @on(SelectionList.SelectedChanged)
    def _multi_changed(self, event: SelectionList.SelectedChanged[int]
                       ) -> None:
        """React to a multi-choice selection change."""
        self._changed(event.control.id)

    def _changed(self, widget_id: Optional[str]) -> None:
        """Update the changed answer and refresh the shown feedback."""
        if not self._form_ready:
            return
        index = _field_index(widget_id)
        if index is None:
            return
        if self._maybe_open_calendar(index):
            return
        self._last_changed = index
        self._answers[index] = self._read_field(index)
        validator_message = self._apply_validator(index)
        self._show_live(index, validator_message)

    def _maybe_open_calendar(self, index: int) -> bool:
        """Open the calendar when a date field holds the pick token.

        Typing the '?' token into a date or date-time input is an
        alternative to pressing the Pick button. The token is left in the
        input until the calendar closes, when it is replaced by the picked
        date or cleared on cancel.
        """
        field = self._fields[index]
        if not isinstance(field, (AskDateField, AskDateTimeField)):
            return False
        if self.query_one(f'#field_{index}', Input).value != _CAL_TOKEN:
            return False
        self._open_calendar(index)
        return True

    def _apply_validator(self, index: int) -> str:
        """Apply the validator's disabled rows and prefills, return message."""
        if self._validator is None:
            return ''
        result = self._validator(self._answers, index)
        self._apply_disabled(result.disable_row_idxs)
        apply_prefills(self, self._fields, index, result.prefill_values)
        return '' if result.is_valid else result.message

    def _show_live(self, index: int, validator_message: str) -> None:
        """Report the changed field's own error, else the validator's.

        A field disabled by the validator is skipped, as on submit, so an
        irrelevant field never blocks the user with its own error. This
        gives a path, integer, choice or multi-choice field the same
        immediate feedback while editing that the console bridge gives by
        re-asking, instead of waiting for submit.
        """
        error = None if index in self._disabled \
            else self._field_error(index, self._fields[index])
        if error is None:
            self._report(None, validator_message)
        else:
            self._report(index, error)

    def _apply_disabled(self, disable_row_idxs: tuple[int, ...]) -> None:
        """Enable or disable each row to match the validator result."""
        self._disabled = set(disable_row_idxs)
        for index in range(len(self._fields)):
            off = index in self._disabled
            self.query_one(f'#field_{index}').disabled = off
            self.query_one(f'#label_{index}').disabled = off
            for button in self.query(f'#browse_{index}'):
                button.disabled = off
            for button in self.query(f'#pick_{index}'):
                button.disabled = off

    @on(Button.Pressed, '#submit')
    def _submit_clicked(self, _event: Button.Pressed) -> None:
        """Submit the form when the submit button is pressed."""
        self.action_submit()

    @on(Button.Pressed, '.browse')
    def _browse_clicked(self, event: Button.Pressed) -> None:
        """Open the directory picker for the clicked path field."""
        index = _browse_index(event.button.id)
        if index is not None:
            self._open_picker(index)

    @on(Button.Pressed, '.pick')
    def _pick_clicked(self, event: Button.Pressed) -> None:
        """Open the calendar for the clicked date field."""
        index = _pick_index(event.button.id)
        if index is not None:
            self._open_calendar(index)

    def _open_picker(self, index: int) -> None:
        """Push the picker seeded with the field's current text."""
        field = self._fields[index]
        assert isinstance(field, AskPathField)
        text = self.query_one(f'#field_{index}', Input).value
        self.push_screen(_PickerScreen(field.path_options, text),
                         partial(self._path_picked, index))

    def _open_calendar(self, index: int) -> None:
        """Push the calendar seeded from the date field's current text."""
        field = self._fields[index]
        assert isinstance(field, (AskDateField, AskDateTimeField))
        text = self.query_one(f'#field_{index}', Input).value
        seed, minimum, maximum = _calendar_setup(field, text)
        self.push_screen(_CalendarScreen(seed, minimum, maximum),
                         partial(self._date_picked, index))

    def _path_picked(self, index: int, result: Optional[str]) -> None:
        """Fill the path input with the picked path, if any.

        Setting the input value raises Input.Changed, so the answer and
        the partial validator update as if the user had typed the path.
        """
        if result is not None:
            self.query_one(f'#field_{index}', Input).value = result

    def _date_picked(self, index: int, result: Optional[date]) -> None:
        """Fill the date input with the picked date, if any.

        A cancelled calendar clears a lingering pick token; a picked date
        replaces the input, keeping any time part of a date-time field.
        Setting the value raises Input.Changed, so the answer refreshes.
        """
        field = self._fields[index]
        assert isinstance(field, (AskDateField, AskDateTimeField))
        widget = self.query_one(f'#field_{index}', Input)
        if result is None:
            if widget.value == _CAL_TOKEN:
                widget.value = ''
            return
        widget.value = _combined_text(field, result, widget.value)

    def action_submit(self) -> None:
        """Validate every enabled field and exit with the answers."""
        for index in range(len(self._fields)):
            self._answers[index] = self._read_field(index)
        failing = self._first_error()
        if failing is not None:
            self._report(*failing)
            return
        if not self._validator_accepts():
            return
        self.exit(list(self._answers))

    def _validator_accepts(self) -> bool:
        """Return whether the partial validator accepts the whole form."""
        if self._validator is None:
            return True
        result = self._validator(self._answers, self._last_changed)
        self._apply_disabled(result.disable_row_idxs)
        if not result.is_valid:
            self._report(None, result.message)
        return result.is_valid

    def _first_error(self) -> Optional[tuple[int, str]]:
        """Return the first enabled field's index and error, or None."""
        for index, field in enumerate(self._fields):
            if index in self._disabled:
                continue
            error = self._field_error(index, field)
            if error is not None:
                return (index, error)
        return None

    def _report(self, index: Optional[int], message: str) -> None:
        """Show a message, naming and marking the field it complains of.

        A message given no field index, such as one from the partial
        validator, is about the whole form: it is shown unchanged and no
        field label is marked.
        """
        self.query('.field_error').remove_class('field_error')
        if index is None:
            self._set_status(message)
            return
        self.query_one(f'#label_{index}').add_class('field_error')
        self._set_status(_field_message(self._fields[index], message))

    def _set_status(self, message: str) -> None:
        """Show a status message below the form."""
        self.query_one('#form_status', Static).update(message)

    def _read_field(self, index: int) -> AnswerField:
        """Return the current answer of one field read from its widget."""
        field = self._fields[index]
        answer = self._read_new_field(index, field)
        return answer if answer is not None \
            else self._read_basic_field(index, field)

    def _read_new_field(self, index: int,
                        field: AskField) -> Optional[AnswerField]:
        """Return a typed field's answer from its text input, else None."""
        if not isinstance(field, NEW_FIELD_TYPES):
            return None
        text = self.query_one(f'#field_{index}', Input).value
        return new_answer(field, value_from_text(field, text))

    def _read_basic_field(self, index: int, field: AskField) -> AnswerField:
        """Return one original field kind's answer read from its widget."""
        widget_id = f'#field_{index}'
        if isinstance(field, AskTextField):
            text = self.query_one(widget_id, Input).value
            answer = text_answer(text, field.nullable, field.default)
            return AnswerTextField(field, answer)
        if isinstance(field, AskIntField):
            return AnswerIntField(field, self._int_value(widget_id, field))
        if isinstance(field, AskPathField):
            text = self.query_one(widget_id, Input).value
            _, path, _ = path_answer(text, field.path_options)
            return AnswerPathField(field, path)
        if isinstance(field, AskYesNoField):
            checked = self.query_one(widget_id, Checkbox).value
            return AnswerYesNoField(field, bool(checked))
        if isinstance(field, AskChoiceField):
            select = self.query_one(widget_id, Select)
            value = None if select.is_blank() else str(select.value)
            return AnswerChoiceField(field, value)
        assert isinstance(field, AskMultiChoiceField)
        selection = self.query_one(widget_id, SelectionList)
        chosen = sorted(selection.selected)
        values = [field.choices[i] for i in chosen]
        return AnswerMultiChoiceField(field, values)

    def _int_value(self, widget_id: str, field: AskIntField) -> Optional[int]:
        """Return the integer value of a field, or None when unparsed."""
        text = self.query_one(widget_id, Input).value
        if text == '':
            return field.default
        return int_text(text)

    def _field_error(self, index: int, field: AskField) -> Optional[str]:
        """Return one field's own validation error, or None when valid."""
        widget_id = f'#field_{index}'
        if isinstance(field, NEW_FIELD_TYPES):
            text = self.query_one(widget_id, Input).value
            return error_from_text(field, text)
        if isinstance(field, AskIntField):
            return self._int_error(widget_id, field)
        if isinstance(field, AskPathField):
            text = self.query_one(widget_id, Input).value
            done, _, reason = path_answer(text, field.path_options)
            return None if done else reason
        if isinstance(field, AskChoiceField):
            blank = self.query_one(widget_id, Select).is_blank()
            return _CHOICE_REQUIRED if blank and not field.nullable else None
        if isinstance(field, AskMultiChoiceField):
            count = len(self.query_one(widget_id, SelectionList).selected)
            return _multi_error(count, field)
        return None

    def _int_error(self, widget_id: str, field: AskIntField) -> Optional[str]:
        """Return the integer field's validation error, or None."""
        text = self.query_one(widget_id, Input).value
        if text == '':
            if field.nullable or field.default is not None:
                return None
            return INT_ERROR
        value = int_text(text)
        if value is None:
            return INT_ERROR
        if out_of_range(value, field.min_value, field.max_value):
            return range_error(field.min_value, field.max_value)
        return None


class WizardUiBridgeTextual(WizardUiBridge):
    """Bridge between the wizard and a Textual terminal interface.

    Each ask method runs a short-lived Textual application for one
    question and returns its result. Validation diagnostics written to
    error_file() and messages passed to show() are buffered and rendered
    in the header of the next question's screen, so nothing reaches the
    terminal directly where it would corrupt the Textual display.

    This bridge draws on the controlling terminal itself, so it takes no
    streams. Use make_text_ui_bridge() to obtain this bridge when a
    terminal is available and a console bridge otherwise.

    The ask methods accept help_text but ignore it; ask_form() shows the
    help text of each field as a tooltip instead.
    """

    def __init__(self) -> None:
        """Start with an empty diagnostics buffer and message list."""
        self._error_buffer = StringIO()
        self._pending: list[str] = []

    # pylint: disable-next=too-many-arguments
    def ask_text(self, question: str, re_ask_reason: Optional[str] = None,
                 nullable: bool = False, *, default: Optional[str] = None,
                 sensitive: bool = False, start_value: Optional[str] = None,
                 help_text: Optional[str] = None) -> Optional[str]:
        """Ask for free text; see WizardUiBridge.ask_text.

        The input starts with the start value, else the default.
        """
        check_text_args(default, sensitive, nullable, start_value)
        messages = self._collect(re_ask_reason)
        start = default if start_value is None else start_value
        value = '' if start is None else start
        text = self._run(_TextApp(question, messages, value, sensitive))
        return text_answer(text, nullable, default)

    def ask_path(self, question: str, re_ask_reason: Optional[str] = None, *,
                 options: Optional[PathAskOptions] = None,
                 help_text: Optional[str] = None) -> Optional[Path]:
        """Ask for a path with a directory tree and editable path input."""
        path_options = PathAskOptions() if options is None else options
        reason = re_ask_reason
        value: Optional[str] = None
        while True:
            messages = self._collect(reason)
            text = self._run(_PathApp(question, messages, path_options, value))
            done, path, reason = path_answer(text, path_options)
            if done:
                return path
            value = text

    def ask_yes_no(self, question: str, default: bool,
                   re_ask_reason: Optional[str] = None, *,
                   start_value: Optional[bool] = None,
                   help_text: Optional[str] = None) -> bool:
        """Ask a yes/no question; see WizardUiBridge.ask_yes_no.

        The start value, else the default, is highlighted.
        """
        messages = self._collect(re_ask_reason)
        start = default if start_value is None else start_value
        chosen = self._run(_ChoiceApp(question, ['yes', 'no'],
                                      0 if start else 1, messages))
        return chosen == 0

    # pylint: disable=too-many-arguments
    @overload
    def ask_choice(self, question: str, *, choices: Sequence[str],
                   default: Optional[str] = None,
                   re_ask_reason: Optional[str] = None,
                   nullable: Literal[False] = False,
                   start_value: Optional[str] = None,
                   help_text: Optional[str] = None) -> str: ...

    @overload
    def ask_choice(self, question: str, *, choices: Sequence[str],
                   default: Optional[str] = None,
                   re_ask_reason: Optional[str] = None, nullable: bool,
                   start_value: Optional[str] = None,
                   help_text: Optional[str] = None) -> Optional[str]: ...
    # pylint: enable=too-many-arguments

    # pylint: disable-next=too-many-arguments
    def ask_choice(self, question: str, *, choices: Sequence[str],
                   default: Optional[str] = None,
                   re_ask_reason: Optional[str] = None, nullable: bool = False,
                   start_value: Optional[str] = None,
                   help_text: Optional[str] = None) -> Optional[str]:
        """Ask the user to pick one choice; see ask_choice.

        A nullable choice is offered with a leading '(none)' option that
        selects no choice. The start value is highlighted, else '(none)'
        when nullable, else the default.
        """
        check_choice_args(choices, default, nullable, start_value)
        messages = self._collect(re_ask_reason)
        offered = offered_choices(choices, nullable)
        start = _choice_start(choices, default, nullable, start_value)
        index = self._run(_ChoiceApp(question, [lbl for lbl, _ in offered],
                                     start, messages))
        return offered[index][1]

    # pylint: disable-next=too-many-arguments
    def ask_multi(self, question: str, *, choices: Sequence[str],
                  default: Optional[Sequence[str]] = None, min_select: int = 0,
                  max_select: Optional[int] = None,
                  re_ask_reason: Optional[str] = None,
                  start_value: Optional[Sequence[str]] = None,
                  help_text: Optional[str] = None) -> list[str]:
        """Ask the user to pick several choices; see ask_multi.

        The start value, else the default, is preselected.
        """
        check_multi_args(choices, default, min_select, max_select, start_value)
        messages = self._collect(re_ask_reason)
        start = default if start_value is None else start_value
        chosen = self._run(_MultiApp(question, list(choices),
                                     _preselected(choices, start), min_select,
                                     max_select, messages))
        return [choices[index] for index in sorted(chosen)]

    # pylint: disable-next=too-many-arguments
    def ask_table(self, columns: Sequence[TableColumn],
                  cells: list[list[TableCell]], question: str, *,
                  re_ask_reason: Optional[str] = None,
                  partial_check: Optional[PartialCheck] = None,
                  min_rows: Optional[int] = None,
                  max_rows: Optional[int] = None,
                  help_text: Optional[str] = None
                  ) -> list[list[Optional[str]]]:
        """Ask the user to fill a table; see WizardUiBridge.ask_table."""
        messages = self._collect(re_ask_reason)
        return self._run(_TableApp(columns, cells, question, messages,
                                   partial_check, min_rows, max_rows))

    def ask_form(self, long_question: str, ask_fields: AskFields, *,
                 re_ask_reason: Optional[str] = None,
                 partial_validator: Optional[PartialFormValidator] = None) \
            -> AnswerFields:
        """Ask the user to fill a whole form on one screen; see ask_form."""
        messages = self._collect(re_ask_reason)
        return self._run(_FormApp(long_question, list(ask_fields), messages,
                                  partial_validator))

    def supports_form_field(self, field: AskField) -> bool:
        """Show every form field type; see WizardUiBridge.

        The Textual form has a widget for each field type, including a
        text input for float, time and duration fields and a text input
        with a calendar Pick button for date and date-time fields. A
        nullable choice field has a drop-down that can be left blank.
        """
        return isinstance(field, ALL_ASK_FIELD_TYPES)

    def _run(self, app: _NavApp[_T]) -> _T:
        """Run one screen and translate its outcome.

        A recorded navigation request is re-raised. A screen that ends
        with no value, such as the built-in quit, is treated as an
        abort.
        """
        result = self._launch(app)
        if app.nav is not None:
            raise app.nav()
        if result is None:
            raise WizardAbort()
        return result

    def _launch(self, app: _NavApp[_T]) -> Optional[_T]:
        """Run the app and return its result.

        This is the only place that drives the terminal, so tests
        override it to exercise the bridge without a real terminal.
        """
        return app.run()  # pragma: no cover

    def _collect(self, re_ask_reason: Optional[str]) -> list[str]:
        """Drain buffered messages and append any re-ask reason."""
        lines = self._drain_messages()
        if re_ask_reason is not None:
            lines.append(re_ask_reason)
        return lines

    def _drain_messages(self) -> list[str]:
        """Return and clear buffered show() and diagnostic lines."""
        text = self._error_buffer.getvalue()
        self._error_buffer.seek(0)
        self._error_buffer.truncate(0)
        diagnostics = [line for line in text.splitlines() if line]
        lines = self._pending + diagnostics
        self._pending = []
        return lines

    def error_file(self) -> StringIO:
        """Return the in-memory stream shown on the next screen."""
        return self._error_buffer

    def show(self, message: str) -> None:
        """Buffer a message for the next question's screen.

        A message shown when no further question follows is not
        displayed, because only a Textual screen renders it.
        """
        self._pending.append(message)


def _choice_start(choices: Sequence[str], default: Optional[str],
                  nullable: bool, start_value: Optional[str]) -> Optional[int]:
    """Return the index of the offered choice to highlight, or None.

    That is the start value, else '(none)' when nullable, else the
    default. A nullable choice offers '(none)' first, so the start value
    is one further down.
    """
    if start_value is not None:
        return list(choices).index(start_value) + (1 if nullable else 0)
    return 0 if nullable else _default_index(choices, default)
