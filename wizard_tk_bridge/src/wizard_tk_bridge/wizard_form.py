#! /usr/local/bin/python3
"""A whole wizard form shown on one screen, and its answer parsing.

A form question asks several related fields at once. :class:`FormEditor`
builds a two-column grid, a label on the left and an input widget on the
right, one row per :class:`AskField`. It reads one :class:`AnswerField`
per row, runs the optional partial validator after every change to show
advisory feedback and disable irrelevant rows, and validates every
enabled field on submit so a submitted form is always complete.

Turning the raw text of a field into its typed answer is the same job on
a form row and in a standalone question, so :func:`int_answer` lives
here and is shared with the wizard window. Its text counterpart is
:func:`wizard_ui_bridge.bridge_helpers.text_answer`, which every bridge
shares, so a graphical answer is accepted or rejected exactly as a
console one is.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter as tk
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from tkinter import ttk
from typing import Callable, NamedTuple, Optional, Sequence
from wizard_ui_bridge import AskField, AnswerField, PartialFormValidator, \
    PrefillValues, PrefillValueType, AskTextField, AskIntField, AskPathField, \
    AskYesNoField, AskChoiceField, AskMultiChoiceField, AskFloatField, \
    AskDateField, AskTimeField, AskDateTimeField, AskDurationField, \
    AnswerTextField, AnswerIntField, AnswerPathField, AnswerYesNoField, \
    AnswerChoiceField, AnswerMultiChoiceField
from wizard_ui_bridge.bridge_helpers import INT_ERROR as _INT_ERROR, \
    int_text, multi_count_message, out_of_range, path_answer, range_error, \
    text_answer
from wizard_ui_bridge.form_helpers import valid_prefills
from wizard_tk_bridge.auto_scroll import auto_hide, bind_wheel
from wizard_tk_bridge.gui_style import style_input
from wizard_tk_bridge.wizard_path import PathRow
from wizard_tk_bridge.wizard_pick_row import HintEntry, PickRow, TypedInput
from wizard_tk_bridge.wizard_typed import default_text, field_hint, \
    format_value, is_typed, typed_answer, typed_error, typed_value

WRAP_LENGTH = 520
LABEL_WRAP = 220
MULTI_HEIGHT = 6
ENTRY_WIDTH = 34
INT_WIDTH = 14
CHOICE_WIDTH = 30
_CHOICE_REQUIRED = 'Please choose a value.'
TOOLTIP_BG = '#ffffe0'
TOOLTIP_WRAP = 320
TOOLTIP_GAP = 2
_HANDLED = (AskTextField, AskIntField, AskPathField, AskYesNoField,
            AskChoiceField, AskMultiChoiceField, AskFloatField, AskDateField,
            AskTimeField, AskDateTimeField, AskDurationField)


def handles_field(field: AskField) -> bool:
    """Return whether the Tk form can show the given field type."""
    return isinstance(field, _HANDLED)


# pylint: disable-next=too-many-arguments
def int_answer(text: str, nullable: bool, min_value: Optional[int],
               max_value: Optional[int], default: Optional[int]
               ) -> tuple[bool, Optional[int], Optional[str]]:
    """Return whether an integer answer is final, its value, and a reason.

    An empty answer takes the default, is None when nullable, or is
    re-asked otherwise. A non-empty answer must parse as an integer that
    lies within the inclusive bounds.
    """
    if text == '':
        if default is not None:
            return (True, default, None)
        return (True, None, None) if nullable else (False, None, _INT_ERROR)
    value = int_text(text)
    if value is None:
        return (False, None, _INT_ERROR)
    if out_of_range(value, min_value, max_value):
        return (False, None, range_error(min_value, max_value))
    return (True, value, None)


class _Input(NamedTuple):
    """A built input: the widget to place, plus type-specific handles."""

    widget: tk.Widget
    var: Optional[tk.BooleanVar]
    path: Optional[PathRow]
    typed: Optional[TypedInput] = None


def _inside(start: int, size: int, limit: int) -> int:
    """Return the start coordinate that keeps size within limit."""
    return max(0, min(start, limit - size))


class HelpTooltip:
    """A hover bubble showing a field's help text over its widgets.

    The bubble is a label placed over the window that holds the bound
    widgets, shown when the pointer enters one of them and destroyed
    when it leaves, so help appears on hover as it does in the textual
    bridge. A window of its own is drawn with the platform's window
    shape, which on macOS rounds the corners of a borderless window so
    much that a one-line bubble loses its first and last characters. A
    placed label is a plain rectangle on every platform, takes neither
    focus nor a grab, and cannot outlive the widgets it belongs to.
    """

    def __init__(self, text: str, anchor: tk.Widget,
                 widgets: Sequence[tk.Widget]) -> None:
        """Bind hover show and hide on each widget for the help text."""
        self.text = text
        self._anchor = anchor
        self._tip: Optional[tk.Label] = None
        for widget in widgets:
            widget.bind('<Enter>', lambda _event: self.show(), add='+')
            widget.bind('<Leave>', lambda _event: self.hide(), add='+')
            widget.bind('<Destroy>', lambda _event: self.hide(), add='+')

    def show(self) -> None:
        """Show the help bubble just below the anchor widget."""
        if self._tip is not None:
            return
        host = self._anchor.winfo_toplevel()
        tip = tk.Label(host, text=self.text, background=TOOLTIP_BG,
                       relief='solid', borderwidth=1, justify='left',
                       wraplength=TOOLTIP_WRAP)
        left, top = self._position(host, tip)
        tip.place(x=left, y=top)
        tip.lift()
        self._tip = tip

    def hide(self) -> None:
        """Destroy the help bubble when one is shown."""
        if self._tip is not None and self._tip.winfo_exists():
            self._tip.destroy()
        self._tip = None

    def _position(self, host: tk.Misc, tip: tk.Label) -> tuple[int, int]:
        """Return where in host to place the bubble under the anchor."""
        left = self._anchor.winfo_rootx() - host.winfo_rootx()
        top = (self._anchor.winfo_rooty() - host.winfo_rooty()
               + self._anchor.winfo_height() + TOOLTIP_GAP)
        return (_inside(left, tip.winfo_reqwidth(), host.winfo_width()),
                _inside(top, tip.winfo_reqheight(), host.winfo_height()))


@dataclass(frozen=True)
class FormRow:
    """One built form row: its field, label, input and help tooltip."""

    field: AskField
    label: tk.Label
    widget: tk.Widget
    var: Optional[tk.BooleanVar]
    path: Optional[PathRow]
    typed: Optional[TypedInput] = None
    tooltip: Optional[HelpTooltip] = None


def _text_input(grid: tk.Misc, field: AskTextField,
                change: Callable[[], None]) -> _Input:
    """Build a text entry, masked and without a default when sensitive."""
    entry = tk.Entry(grid, width=ENTRY_WIDTH)
    if field.sensitive:
        entry.configure(show='*')
    elif field.default is not None:
        entry.insert(0, field.default)
    style_input(entry)
    entry.bind('<KeyRelease>', lambda _event: change())
    return _Input(entry, None, None)


def _int_input(grid: tk.Misc, field: AskIntField,
               change: Callable[[], None]) -> _Input:
    """Build a numeric text entry pre-filled with its default."""
    entry = tk.Entry(grid, width=INT_WIDTH)
    if field.default is not None:
        entry.insert(0, str(field.default))
    style_input(entry)
    entry.bind('<KeyRelease>', lambda _event: change())
    return _Input(entry, None, None)


def _path_input(grid: tk.Misc, field: AskPathField,
                change: Callable[[], None]) -> _Input:
    """Build a path entry with a Browse button from the path options."""
    default = field.path_options.default
    initial = '' if default is None else str(default)
    row = PathRow(grid, field.path_options, initial, change)
    return _Input(row.frame, None, row)


def _yes_no_input(grid: tk.Misc, field: AskYesNoField,
                  change: Callable[[], None]) -> _Input:
    """Build a check box holding the yes/no default."""
    var = tk.BooleanVar(grid, field.default)
    check = tk.Checkbutton(grid, variable=var, command=change)
    return _Input(check, var, None)


def _choice_input(grid: tk.Misc, field: AskChoiceField,
                  change: Callable[[], None]) -> _Input:
    """Build a read-only drop-down, preselecting any default choice."""
    box = ttk.Combobox(grid, values=list(field.choices), state='readonly',
                       width=CHOICE_WIDTH)
    if field.default is not None:
        box.set(field.default)
    style_input(box)
    box.bind('<<ComboboxSelected>>', lambda _event: change())
    return _Input(box, None, None)


def _multi_input(grid: tk.Misc, field: AskMultiChoiceField,
                 change: Callable[[], None]) -> _Input:
    """Build a multi-selection list, preselecting the default values."""
    box = tk.Listbox(grid, selectmode='multiple', exportselection=False,
                     height=min(len(field.choices), MULTI_HEIGHT))
    for choice in field.choices:
        box.insert('end', choice)
    _preselect(box, field.choices, field.default)
    style_input(box)
    box.bind('<<ListboxSelect>>', lambda _event: change())
    return _Input(box, None, None)


def _preselect(box: tk.Listbox, choices: Sequence[str],
               default: Optional[Sequence[str]]) -> None:
    """Select the default values in a multi-selection list."""
    if default is None:
        return
    wanted = set(default)
    for index, choice in enumerate(choices):
        if choice in wanted:
            box.selection_set(index)


def _hint_input(grid: tk.Misc, field: AskField,
                change: Callable[[], None]) -> _Input:
    """Build a placeholder entry for a float, time or duration field."""
    entry = HintEntry(grid, field_hint(field), default_text(field), change)
    return _Input(entry.entry, None, None, entry)


def _pick_input(grid: tk.Misc, field: AskField,
                change: Callable[[], None]) -> _Input:
    """Build a date or date-time entry with a calendar Pick button."""
    row = PickRow(grid, field, field_hint(field), default_text(field), change)
    return _Input(row.frame, None, None, row)


def _typed_input(grid: tk.Misc, field: AskField,
                 change: Callable[[], None]) -> _Input:
    """Build the input widget for one of the five typed fields."""
    if isinstance(field, (AskFloatField, AskTimeField, AskDurationField)):
        return _hint_input(grid, field, change)
    return _pick_input(grid, field, change)


def _basic_input(grid: tk.Misc, field: AskField,
                 change: Callable[[], None]) -> _Input:
    """Build the input widget for one of the original field kinds."""
    if isinstance(field, AskTextField):
        return _text_input(grid, field, change)
    if isinstance(field, AskIntField):
        return _int_input(grid, field, change)
    if isinstance(field, AskPathField):
        return _path_input(grid, field, change)
    if isinstance(field, AskYesNoField):
        return _yes_no_input(grid, field, change)
    if isinstance(field, AskChoiceField):
        return _choice_input(grid, field, change)
    assert isinstance(field, AskMultiChoiceField)
    return _multi_input(grid, field, change)


def _make_input(grid: tk.Misc, field: AskField,
                change: Callable[[], None]) -> _Input:
    """Build the input widget matching the field type."""
    if is_typed(field):
        return _typed_input(grid, field, change)
    return _basic_input(grid, field, change)


def _entry_widget(row: FormRow) -> tk.Entry:
    """Return the text entry of a text or integer row."""
    assert isinstance(row.widget, tk.Entry)
    return row.widget


def _int_value(row: FormRow, field: AskIntField) -> Optional[int]:
    """Return the integer value of a row, or its default when empty."""
    text = _entry_widget(row).get()
    return field.default if text == '' else int_text(text)


def _path_value(row: FormRow, field: AskPathField) -> Optional[Path]:
    """Return the accepted path of a row, or None when not accepted."""
    assert row.path is not None
    _, path, _ = path_answer(row.path.get(), field.path_options)
    return path


def _choice_value(row: FormRow) -> Optional[str]:
    """Return the chosen value of a row, or None when none is chosen."""
    assert isinstance(row.widget, ttk.Combobox)
    value = row.widget.get()
    return value if value != '' else None


def _multi_selected(row: FormRow) -> list[int]:
    """Return the selected 0-based indexes of a multi-selection row."""
    assert isinstance(row.widget, tk.Listbox)
    picks = row.widget.curselection()  # type: ignore[no-untyped-call]
    return [int(index) for index in picks]


def _multi_values(row: FormRow, field: AskMultiChoiceField) -> list[str]:
    """Return the chosen values of a multi-selection row, in order."""
    return [field.choices[index] for index in _multi_selected(row)]


def _int_error(row: FormRow, field: AskIntField) -> Optional[str]:
    """Return the integer row's own validation error, or None."""
    text = _entry_widget(row).get()
    done, _, reason = int_answer(text, field.nullable, field.min_value,
                                 field.max_value, field.default)
    return None if done else reason


def _multi_error(row: FormRow, field: AskMultiChoiceField) -> Optional[str]:
    """Return the multi-selection row's count error, or None."""
    return multi_count_message(len(_multi_selected(row)), field.min_select,
                               field.max_select)


def _set_widget_state(row: FormRow, enabled: bool) -> None:
    """Enable or disable a row's input widget, keeping combo read-only."""
    if row.typed is not None:
        row.typed.set_enabled(enabled)
        return
    if row.path is not None:
        row.path.set_enabled(enabled)
        return
    active = 'readonly' if isinstance(row.widget, ttk.Combobox) else 'normal'
    row.widget['state'] = active if enabled else 'disabled'


def _enable_row(row: FormRow, enabled: bool) -> None:
    """Enable or disable one form row, greying its label when disabled."""
    _set_widget_state(row, enabled)
    row.label.configure(fg='black' if enabled else 'grey')


def _hint_note(field: AskField) -> Optional[str]:
    """Return the format hint sentence for a typed field, or None."""
    return f'Enter {field_hint(field)}.' if is_typed(field) else None


def _tooltip_text(field: AskField) -> Optional[str]:
    """Return the tooltip text combining help text and format hint."""
    note = _hint_note(field)
    if field.help_text is None:
        return note
    return field.help_text if note is None else f'{field.help_text}\n{note}'


def _row_tooltip(field: AskField, label: tk.Label,
                 widget: tk.Widget) -> Optional[HelpTooltip]:
    """Return a hover tooltip for the field's help and format hint."""
    text = _tooltip_text(field)
    if text is None:
        return None
    return HelpTooltip(text, label, (label, widget))


def _set_entry_text(entry: tk.Entry, text: str) -> None:
    """Replace a text or integer entry's text, enabling it if disabled."""
    if entry.get() == text:
        return
    state = entry['state']
    entry['state'] = 'normal'
    entry.delete(0, 'end')
    entry.insert(0, text)
    entry['state'] = state


def _set_combo(box: ttk.Combobox, value: str) -> None:
    """Set a drop-down's value, enabling it briefly if disabled."""
    if box.get() == value:
        return
    state = box['state']
    box['state'] = 'normal'
    box.set(value)
    box['state'] = state


def _set_multi(box: tk.Listbox, choices: Sequence[str],
               value: PrefillValueType) -> None:
    """Select the values of a multi-selection list, enabling it briefly."""
    assert isinstance(value, (list, tuple))
    wanted = set(value)
    state = box['state']
    box['state'] = 'normal'
    box.selection_clear(0, 'end')
    for index, choice in enumerate(choices):
        if choice in wanted:
            box.selection_set(index)
    box['state'] = state


def _basic_answer(row: FormRow) -> AnswerField:
    """Return the answer of a row of one of the original field kinds."""
    field = row.field
    if isinstance(field, AskTextField):
        text = _entry_widget(row).get()
        return AnswerTextField(field, text_answer(text, field.nullable,
                                                  field.default))
    if isinstance(field, AskIntField):
        return AnswerIntField(field, _int_value(row, field))
    if isinstance(field, AskPathField):
        return AnswerPathField(field, _path_value(row, field))
    if isinstance(field, AskYesNoField):
        assert row.var is not None
        return AnswerYesNoField(field, bool(row.var.get()))
    if isinstance(field, AskChoiceField):
        return AnswerChoiceField(field, _choice_value(row))
    assert isinstance(field, AskMultiChoiceField)
    return AnswerMultiChoiceField(field, _multi_values(row, field))


def _basic_error(row: FormRow) -> Optional[str]:
    """Return the own error of a row of an original field kind, or None."""
    field = row.field
    if isinstance(field, AskIntField):
        return _int_error(row, field)
    if isinstance(field, AskPathField):
        assert row.path is not None
        done, _, reason = path_answer(row.path.get(), field.path_options)
        return None if done else reason
    if isinstance(field, AskChoiceField):
        return None if _choice_value(row) is not None else _CHOICE_REQUIRED
    if isinstance(field, AskMultiChoiceField):
        return _multi_error(row, field)
    return None


def _row_error(row: FormRow) -> Optional[str]:
    """Return one row's own validation error, without its field label."""
    if is_typed(row.field):
        assert row.typed is not None
        return typed_error(row.field, row.typed.text())
    return _basic_error(row)


def _with_label(field: AskField, error: Optional[str]) -> Optional[str]:
    """Prefix a field's own error with its label, keeping None as None.

    The whole form shares one status line, so naming the field makes clear
    which row a message such as 'Please enter an integer.' refers to.
    """
    if error is None:
        return None
    return f'{field.short_question}: {error}'


class FormEditor:
    """A two-column grid that asks a whole wizard form on one screen."""

    def __init__(self, parent: tk.Misc, fields: Sequence[AskField],
                 validator: Optional[PartialFormValidator],
                 on_submit: Callable[[list[AnswerField]], None]) -> None:
        """Build one labelled input row per field, plus a status line."""
        self._validator = validator
        self._on_submit = on_submit
        self._disabled: set[int] = set()
        self._last_changed = 0
        grid = self._scroll_area(parent)
        self._rows = [self._build_row(grid, index, field)
                      for index, field in enumerate(fields)]
        self._apply_initial()

    def _scroll_area(self, parent: tk.Misc) -> tk.Frame:
        """Build the scrolling field area, returning the frame for the rows.

        A tall form (many rows) would overflow the fixed-size wizard
        window, so the labelled rows sit in a frame inside a vertically
        scrolling canvas whose scrollbar appears only when it is needed.
        The mouse wheel scrolls the area from over the rows as well, which
        Tk gives the scrollbar alone. The status line stays below the
        scroll area so it is always shown.
        """
        outer = tk.Frame(parent)
        outer.pack(fill='both', expand=True, pady=6)
        outer.rowconfigure(0, weight=1)
        outer.columnconfigure(0, weight=1)
        canvas = tk.Canvas(outer, highlightthickness=0)
        vbar = ttk.Scrollbar(outer, orient='vertical', command=canvas.yview)
        canvas.configure(yscrollcommand=auto_hide(vbar))
        canvas.grid(row=0, column=0, sticky='nsew')
        vbar.grid(row=0, column=1, sticky='ns')
        bind_wheel(canvas)
        grid = tk.Frame(canvas)
        canvas.create_window((0, 0), window=grid, anchor='nw')
        grid.bind('<Configure>', lambda _event: canvas.configure(
            scrollregion=canvas.bbox('all')))
        self._status = tk.Label(outer, fg='red', wraplength=WRAP_LENGTH,
                                justify='left')
        self._status.grid(row=1, column=0, columnspan=2, sticky='w',
                          pady=(6, 0))
        return grid

    def _apply_initial(self) -> None:
        """Disable the initially irrelevant rows, showing no message yet."""
        if self._validator is not None:
            result = self._validator(self.answers(), 0)
            self._apply_disabled(result.disable_row_idxs)
            self._apply_prefills(result.prefill_values, 0)

    def _apply_prefills(self, prefills: PrefillValues, changed: int) -> None:
        """Write the validator's valid prefills into their row inputs."""
        fields = [row.field for row in self._rows]
        for index, value in valid_prefills(fields, changed, prefills):
            self._write_value(self._rows[index], value)

    def _write_value(self, row: FormRow, value: PrefillValueType) -> None:
        """Write one prefill value into a row's input by field type."""
        field = row.field
        if row.typed is not None:
            row.typed.set_text(format_value(value))
        elif isinstance(field, (AskTextField, AskIntField)):
            _set_entry_text(_entry_widget(row), str(value))
        elif isinstance(field, AskPathField):
            assert row.path is not None
            row.path.set_text(str(value))
        elif isinstance(field, AskYesNoField):
            assert row.var is not None
            row.var.set(bool(value))
        elif isinstance(field, AskChoiceField):
            assert isinstance(row.widget, ttk.Combobox)
            _set_combo(row.widget, str(value))
        else:
            assert isinstance(field, AskMultiChoiceField)
            assert isinstance(row.widget, tk.Listbox)
            _set_multi(row.widget, field.choices, value)

    def _build_row(self, grid: tk.Misc, index: int,
                   field: AskField) -> FormRow:
        """Build and place one labelled input row of the grid."""
        label = tk.Label(grid, text=field.short_question, justify='left',
                         wraplength=LABEL_WRAP, anchor='w')
        label.grid(row=index, column=0, sticky='nw', padx=4, pady=3)
        built = _make_input(grid, field, partial(self._changed, index))
        built.widget.grid(row=index, column=1, sticky='w', padx=4, pady=3)
        tooltip = _row_tooltip(field, label, built.widget)
        return FormRow(field, label, built.widget, built.var, built.path,
                       built.typed, tooltip)

    def answers(self) -> list[AnswerField]:
        """Return the current answer of every row, in field order."""
        return [self._read(index) for index in range(len(self._rows))]

    def submit(self) -> None:
        """Validate every enabled field and submit when all pass."""
        answers = self.answers()
        error = self._first_error()
        if error is not None:
            self._show(error)
            return
        if self._validator_blocks(answers):
            return
        self._on_submit(answers)

    def _validator_blocks(self, answers: list[AnswerField]) -> bool:
        """Run the whole-form validator and return whether it blocks."""
        if self._validator is None:
            return False
        result = self._validator(answers, self._last_changed)
        self._apply_disabled(result.disable_row_idxs)
        if not result.is_valid:
            self._show(result.message)
        return not result.is_valid

    def _changed(self, index: int) -> None:
        """React to a field change with live feedback and row enabling."""
        self._last_changed = index
        self._show(self._feedback(self.answers(), index))

    def _feedback(self, answers: list[AnswerField], index: int) -> str:
        """Return the live message for the field that just changed."""
        validator_msg = self._run_validator(answers, index)
        if index in self._disabled:
            return validator_msg
        own = self._field_error(index)
        return validator_msg if own is None else own

    def _run_validator(self, answers: list[AnswerField], index: int) -> str:
        """Apply the validator's disabled rows and return its message."""
        if self._validator is None:
            return ''
        result = self._validator(answers, index)
        self._apply_disabled(result.disable_row_idxs)
        self._apply_prefills(result.prefill_values, index)
        return '' if result.is_valid else result.message

    def _first_error(self) -> Optional[str]:
        """Return the first enabled field's own error, or None."""
        for index in range(len(self._rows)):
            if index in self._disabled:
                continue
            error = self._field_error(index)
            if error is not None:
                return error
        return None

    def _apply_disabled(self, disable_row_idxs: tuple[int, ...]) -> None:
        """Enable or disable each row to match the validator result."""
        self._disabled = set(disable_row_idxs)
        for index, row in enumerate(self._rows):
            _enable_row(row, index not in self._disabled)

    def _show(self, message: str) -> None:
        """Show a status message below the form."""
        self._status.config(text=message)

    def _read(self, index: int) -> AnswerField:
        """Return the current answer of one row read from its widget."""
        row = self._rows[index]
        if is_typed(row.field):
            assert row.typed is not None
            value = typed_value(row.field, row.typed.text())
            return typed_answer(row.field, value)
        return _basic_answer(row)

    def _field_error(self, index: int) -> Optional[str]:
        """Return one field's own error, prefixed with its label."""
        row = self._rows[index]
        return _with_label(row.field, _row_error(row))
