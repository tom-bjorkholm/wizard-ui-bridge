#! /usr/local/bin/python3
"""A whole wizard form shown on one screen.

A form question asks several related fields at once. :class:`FormEditor`
builds a two-column grid, a label on the left and an input widget on the
right, one row per :class:`AskField`. It reads one :class:`AnswerField`
per row, runs the optional partial validator after every change to show
advisory feedback and disable irrelevant rows, and validates every
enabled field on submit so a submitted form is always complete. The input
of each row is a :class:`~wizard_tk_bridge.wizard_cell.CellInput`, the
same input a matrix form shows in a cell.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter as tk
from dataclasses import dataclass
from functools import partial
from typing import Callable, Optional, Sequence
from wizard_ui_bridge import AskField, AnswerField, PartialFormValidator, \
    PrefillValues, AskTextField, AskIntField, AskPathField, AskYesNoField, \
    AskChoiceField, AskMultiChoiceField, AskFloatField, AskDateField, \
    AskTimeField, AskDateTimeField, AskDurationField
from wizard_ui_bridge.form_helpers import answer_of, valid_prefills
from wizard_tk_bridge.wizard_cell import CellInput, HelpTooltip, \
    build_input, scrolled_editor, tooltip_text

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
                 validator: Optional[PartialFormValidator],
                 on_submit: Callable[[list[AnswerField]], None]) -> None:
        """Build one labelled input row per field, plus a status line."""
        self._validator = validator
        self._on_submit = on_submit
        self._disabled: set[int] = set()
        self._last_changed = 0
        grid, self._status = scrolled_editor(parent, sideways=False)
        self._rows = [self._build_row(grid, index, field)
                      for index, field in enumerate(fields)]
        self._apply_initial()

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
            self._rows[index].cell_input.write(value)

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
        """Return the current answer of one row read from its input."""
        row = self._rows[index]
        return answer_of(row.field, row.cell_input.value())

    def _field_error(self, index: int) -> Optional[str]:
        """Return one field's own error, prefixed with its label."""
        row = self._rows[index]
        return _with_label(row.field, row.cell_input.error())
