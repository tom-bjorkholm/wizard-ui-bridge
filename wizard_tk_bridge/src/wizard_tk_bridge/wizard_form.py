#! /usr/local/bin/python3
"""A whole wizard form shown on one screen.

A form question asks several related fields at once. :class:`FormEditor`
builds a two-column grid, a label on the left and an input widget on the
right, one row per :class:`AskField`. It reads one :class:`AnswerField`
per row, and runs the optional live validator when the form is shown, to
disable irrelevant rows and write prefills, and after every change to
show advisory feedback as well. On submit the validator runs first, then
every enabled field is validated, so a submitted form is always complete,
and the keyboard focus moves to the first field that fails its own
check. The input of each row is a
:class:`~wizard_tk_bridge.wizard_cell.CellInput`, the same input a matrix
form shows in a cell.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter as tk
from dataclasses import dataclass
from functools import partial
from typing import Callable, Optional, Sequence
from wizard_ui_bridge import AskField, AnswerField, LiveFormValidator, \
    AskTextField, AskIntField, AskPathField, AskYesNoField, \
    AskChoiceField, AskMultiChoiceField, AskFloatField, AskDateField, \
    AskTimeField, AskDateTimeField, AskDurationField
from wizard_ui_bridge.form_helpers import answer_of, valid_prefills
from wizard_tk_bridge.wizard_cell import CellInput, HelpTooltip, \
    build_input, scroll_into_view, scrolled_editor, tooltip_text

LABEL_WRAP = 220
_HANDLED = (AskTextField, AskIntField, AskPathField, AskYesNoField,
            AskChoiceField, AskMultiChoiceField, AskFloatField, AskDateField,
            AskTimeField, AskDateTimeField, AskDurationField)


def handles_field(field: AskField) -> bool:
    """Return whether the Tk form can show the given field type."""
    return isinstance(field, _HANDLED)


@dataclass(frozen=True)
class FormRow:
    """One built form row: its field, label, input and help tooltip."""

    field: AskField
    label: tk.Label
    cell_input: CellInput
    tooltip: Optional[HelpTooltip] = None


def _enable_row(row: FormRow, enabled: bool) -> None:
    """Enable or disable one form row, greying its label when disabled."""
    row.cell_input.set_enabled(enabled)
    row.label.configure(fg='black' if enabled else 'grey')


def _row_tooltip(field: AskField, label: tk.Label,
                 widget: tk.Widget) -> Optional[HelpTooltip]:
    """Return a hover tooltip for the field's help and format hint."""
    text = tooltip_text(field)
    if text is None:
        return None
    return HelpTooltip(text, label, (label, widget))


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
                 validator: Optional[LiveFormValidator],
                 on_submit: Callable[[list[AnswerField]], None]) -> None:
        """Build one labelled input row per field, plus a status line.

        The validator is called for the whole form, with None, to disable
        the initially irrelevant rows and write prefills, showing no
        message yet.
        """
        self._validator = validator
        self._on_submit = on_submit
        self._disabled: set[int] = set()
        self._last_changed: Optional[int] = None
        self._grid, self._status = scrolled_editor(parent, sideways=False)
        self._rows = [self._build_row(self._grid, index, field)
                      for index, field in enumerate(fields)]
        self._validate(None, live=True)

    def _build_row(self, grid: tk.Misc, index: int,
                   field: AskField) -> FormRow:
        """Build and place one labelled input row of the grid."""
        label = tk.Label(grid, text=field.short_question, justify='left',
                         wraplength=LABEL_WRAP, anchor='w')
        label.grid(row=index, column=0, sticky='nw', padx=4, pady=3)
        built = build_input(grid, field, partial(self._changed, index))
        built.widget.grid(row=index, column=1, sticky='w', padx=4, pady=3)
        tooltip = _row_tooltip(field, label, built.widget)
        return FormRow(field, label, built, tooltip)

    def answers(self) -> list[AnswerField]:
        """Return the current answer of every row, in field order."""
        return [self._read(index) for index in range(len(self._rows))]

    def submit(self) -> None:
        """Validate the whole form and submit its answers when valid.

        The validator runs first, so the rows it disables are not
        checked. Every enabled field must then pass its own check, and
        the first that does not gets the keyboard focus. Last the
        validator must accept the form.
        """
        problem = self._validate(self._last_changed, live=False)
        invalid = self._first_invalid()
        if invalid is not None:
            self._reveal(invalid)
            self._show(self._field_error(invalid) or '')
        elif problem is not None:
            self._show(problem)
        else:
            self._on_submit(self.answers())

    def _changed(self, index: int) -> None:
        """React to a field change with live feedback and row enabling."""
        self._last_changed = index
        message = self._validate(index, live=True)
        own = None if index in self._disabled else self._field_error(index)
        self._show(own or message or '')

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
            fields = [row.field for row in self._rows]
            for index, value in valid_prefills(fields, changed,
                                               result.prefill_values):
                self._rows[index].cell_input.write(value)
        return None if result.is_valid else result.message

    def _first_invalid(self) -> Optional[int]:
        """Return the first enabled row failing its own check, or None."""
        for index, row in enumerate(self._rows):
            if index not in self._disabled \
                    and row.cell_input.error() is not None:
                return index
        return None

    def _reveal(self, index: int) -> None:
        """Scroll a row into view and give its input the keyboard focus."""
        cell_input = self._rows[index].cell_input
        scroll_into_view(self._grid, cell_input.widget)
        cell_input.main_widget().focus_set()

    def _apply_disabled(self, disable_row_idxs: tuple[int, ...]) -> None:
        """Enable or disable each row to match the validator result."""
        self._disabled = set(disable_row_idxs)
        for index, row in enumerate(self._rows):
            _enable_row(row, index not in self._disabled)

    def _show(self, message: str) -> None:
        """Show a status message below the form."""
        self._status.config(text=message)

    def _read(self, index: int) -> AnswerField:
        """Return the current answer of one row read from its input."""
        row = self._rows[index]
        return answer_of(row.field, row.cell_input.value())

    def _field_error(self, index: int) -> Optional[str]:
        """Return one field's own error, prefixed with its label."""
        row = self._rows[index]
        return _with_label(row.field, row.cell_input.error())
