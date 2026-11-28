#! /usr/local/bin/python3
"""Textual full-screen user interface bridge for the wizard.

This module provides the concrete Textual bridge used when the wizard
talks to a user through a real terminal. Each ask method runs a short
lived Textual application for one question and returns its result, which
keeps the one-question-at-a-time contract of WizardUiBridge while giving
the user a full-screen interface with selectable lists, check boxes,
whole forms and matrix forms. A table question is asked by the inherited
WizardUiBridge.ask_table() through ask_matrix_form().

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
from wizard_ui_bridge.bridge_helpers import check_text_args, \
    multi_count_message, path_answer, text_answer, offered_choices
from wizard_ui_bridge.form_helpers import answer_of, valid_prefills, \
    live_validator_of
from wizard_ui_bridge.matrix_defs import AnswerCells, MatrixRequest
from wizard_ui_bridge._textual_cell import CellInput, build_input
from wizard_ui_bridge._textual_matrix import _MatrixApp
from wizard_ui_bridge._textual_nav import _NavApp
from wizard_ui_bridge._textual_widgets import \
    _header_widgets, _default_index, _preselected, _field_index, \
    _field_message
from wizard_ui_bridge._path import _PathPick, _start_dir, _start_value
from wizard_ui_bridge.arg_types import WizardAbort, PathAskOptions, \
    check_choice_args, check_multi_args
from wizard_ui_bridge.form_defs import AskField, AskFields, \
    ALL_ASK_FIELD_TYPES, AnswerField, AnswerFields, LiveFormValidator, \
    PartialFormValidator

_T = TypeVar('_T')


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
    input for a float, time or duration field. A live validator, when
    given, runs when the form is shown, to disable rows and write
    prefills, and after each change to show advisory feedback as well.
    On submit the validator runs first, then each enabled field is
    validated, so the returned answers are complete and a choice with no
    default is always answered. The first field that fails gets the
    keyboard focus.

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
                 validator: Optional[LiveFormValidator]) -> None:
        """Store the prompt, fields, buffered messages and validator."""
        super().__init__()
        self._question = question
        self._fields = fields
        self._messages = messages
        self._validator = validator
        self._inputs: list[CellInput] = []
        self._disabled: set[int] = set()
        self._last_changed: Optional[int] = None

    def compose(self) -> ComposeResult:
        """Lay out the header, the field grid, submit and footer."""
        yield from _header_widgets(self._messages, self._question)
        with VerticalScroll(id='form_scroll'), Grid(id='form_grid'):
            yield from self._field_widgets()
        yield Button('Submit', id='submit')
        yield Static('', id='form_status')
        yield Footer()

    def _field_widgets(self) -> Iterator[Widget]:
        """Yield a label and an input widget for each field.

        The inputs are built here, since a Textual input can only be
        built while the app is running.
        """
        self._inputs = [build_input(field, 'field', str(index))
                        for index, field in enumerate(self._fields)]
        for index, field in enumerate(self._fields):
            label = Static(field.short_question, id=f'label_{index}')
            label.tooltip = field.help_text
            yield label
            yield self._inputs[index].widget

    def on_mount(self) -> None:
        """Size the grid, validate it, focus the first field, not the scroll.

        The validator is called for the whole form, with None, to disable
        the rows that start irrelevant and write any prefills, but its
        message is not shown yet. Then each input records its answer as
        seen, so the change event Textual posts as it mounts an input, or
        as a prefill is written, is not taken as an edit.
        """
        self.query_one('#form_scroll').can_focus = False
        self.query_one('#form_grid', Grid).styles.grid_size_columns = 2
        self._validate(None, live=True)
        for cell_input in self._inputs:
            cell_input.settle()
        if self._fields:
            self._inputs[0].main.focus()

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
        """Update the changed answer and refresh the shown feedback.

        Typing the '?' token into a date field opens its calendar.
        """
        index = _field_index(widget_id)
        if index is None:
            return
        cell_input = self._inputs[index]
        if cell_input.wants_calendar():
            cell_input.open_dialog()
            return
        if not cell_input.take_change():
            return
        self._last_changed = index
        validator_message = self._validate(index, live=True)
        self._show_live(index, validator_message or '')

    def _validate(self, changed: Optional[int], live: bool) -> Optional[str]:
        """Run the validator and return its message when invalid.

        The disabled rows of its result are applied, and while the user
        edits (live) its prefills too, which are ignored on submit.
        """
        if self._validator is None:
            return None
        result = self._validator(self.answers(), changed)
        self._apply_disabled(result.disable_row_idxs)
        if live:
            for target, value in valid_prefills(self._fields, changed,
                                                result.prefill_values):
                self._inputs[target].write(value)
        return None if result.is_valid else result.message

    def _show_live(self, index: int, validator_message: str) -> None:
        """Report the changed field's own error, else the validator's.

        A field disabled by the validator is skipped, as on submit, so an
        irrelevant field never blocks the user with its own error. This
        gives a path, integer, choice or multi-choice field the same
        immediate feedback while editing that the console bridge gives by
        re-asking, instead of waiting for submit.
        """
        error = None if index in self._disabled \
            else self._inputs[index].error()
        if error is None:
            self._report(None, validator_message)
        else:
            self._report(index, error)

    def _apply_disabled(self, disable_row_idxs: tuple[int, ...]) -> None:
        """Enable or disable each row to match the validator result.

        A prefill aimed at a disabled row is still written, so the value
        shows greyed and takes effect if the row is later enabled.
        """
        self._disabled = set(disable_row_idxs)
        for index, cell_input in enumerate(self._inputs):
            off = index in self._disabled
            cell_input.set_enabled(not off)
            self.query_one(f'#label_{index}').disabled = off

    @on(Button.Pressed, '#submit')
    def _submit_clicked(self, _event: Button.Pressed) -> None:
        """Submit the form when the submit button is pressed."""
        self.action_submit()

    @on(Button.Pressed, '.browse, .pick')
    def _dialog_clicked(self, event: Button.Pressed) -> None:
        """Open the directory picker or calendar of the clicked field."""
        index = _field_index(event.button.id)
        if index is not None:
            self._inputs[index].open_dialog()

    def action_submit(self) -> None:
        """Validate the whole form and exit with its answers when valid.

        The live validator runs first, so the rows it disables are not
        checked. Every enabled field must then pass its own check, and
        the first that does not gets the keyboard focus. Last the
        validator must accept the form.
        """
        problem = self._validate(self._last_changed, live=False)
        failing = self._first_error()
        if failing is not None:
            self._inputs[failing[0]].main.focus()
            self._report(*failing)
        elif problem is not None:
            self._report(None, problem)
        else:
            self.exit(self.answers())

    def answers(self) -> list[AnswerField]:
        """Return the current answer of every field, in field order."""
        return [self._read_field(index) for index in range(len(self._fields))]

    def _first_error(self) -> Optional[tuple[int, str]]:
        """Return the first enabled field's index and error, or None."""
        for index, cell_input in enumerate(self._inputs):
            if index in self._disabled:
                continue
            error = cell_input.error()
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
        return answer_of(self._fields[index], self._inputs[index].value())


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

    The ask methods accept help_text but ignore it; ask_form() and
    ask_matrix_form() show the help text of each field or cell as a
    tooltip instead, and so does the inherited ask_table(), which asks
    a table as a matrix form.
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

    def ask_form(self, long_question: str, ask_fields: AskFields, *,
                 re_ask_reason: Optional[str] = None,
                 partial_validator: Optional[PartialFormValidator] = None,
                 live_validator: Optional[LiveFormValidator] = None) \
            -> AnswerFields:
        """Ask the user to fill a whole form on one screen; see ask_form."""
        validator = live_validator_of(partial_validator, live_validator)
        messages = self._collect(re_ask_reason)
        return self._run(_FormApp(long_question, list(ask_fields), messages,
                                  validator))

    def ask_matrix_form(self, request: MatrixRequest, *,
                        re_ask_reason: Optional[str] = None) -> AnswerCells:
        """Ask the user to fill a whole matrix on one screen; see base.

        The matrix is shown as a grid of labels and inputs, with buttons
        to resize it when its bounds allow, see _MatrixApp.
        """
        messages = self._collect(re_ask_reason)
        return self._run(_MatrixApp(request, messages))

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
