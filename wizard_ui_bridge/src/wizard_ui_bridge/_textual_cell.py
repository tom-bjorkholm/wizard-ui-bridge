#! /usr/local/bin/python3
"""The input of one form field or matrix cell in the Textual bridge.

A form row and a matrix cell show the same kinds of input: a text input
for text, integers and the typed values, a path input with a Browse
button, a check box, a drop-down, a check-box list, and a date or
date-time input with a calendar Pick button. :func:`build_input` builds
the :class:`CellInput` for one Ask*Cell (every Ask*Field is one too),
which reads the current answer value, reports the input's own validation
error, writes a prefill into the input, enables or disables it, and opens
the directory picker or the calendar of a path or date input.

The input gets the id '{prefix}_{key}', such as 'field_3' in a form or
'cell_1_2' in a matrix, and its Browse or Pick button the id
'browse_{key}' or 'pick_{key}' and the class 'browse' or 'pick', so a
screen maps the id of an event's widget back to its field or cell.

The width hint of a cell sizes the text part of its input. Without one,
a compact input, as in a matrix, gets the width of
wizard_ui_bridge.matrix_helpers.compact_width(), and a compact path or
date input gets a narrow '…' button instead of Browse or Pick.

Textual posts a Changed event when an Input or a Select holding a value
is mounted, which reaches the screen after its on_mount, so such an
event is not a change by the user. :meth:`CellInput.settle` records the
answer and error of a mounted input, and :meth:`CellInput.take_change`
tells whether an event really changed them.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from datetime import date
from pathlib import Path
from typing import Optional, Union
from textual.containers import Horizontal
from textual.widget import Widget
from textual.widgets import Button, Checkbox, Input, Select, SelectionList
from textual.widgets.selection_list import Selection
from wizard_ui_bridge.bridge_helpers import INT_ERROR, int_text, \
    multi_count_message, out_of_range, path_answer, range_error, text_answer
from wizard_ui_bridge.form_helpers import answer_of
from wizard_ui_bridge.matrix_helpers import compact_width
from wizard_ui_bridge.matrix_cell_defs import AnswerCell, AskCell, \
    AskTextCell, AskIntCell, AskPathCell, AskYesNoCell, AskChoiceCell, \
    AskMultiChoiceCell, AskDateCell, AskDateTimeCell, PrefillValueType
from wizard_ui_bridge._calendar import _CalendarScreen
from wizard_ui_bridge._parse import NEW_CELL_TYPES, error_from_text, \
    format_new_value, value_from_text
from wizard_ui_bridge._path import _PickerScreen
from wizard_ui_bridge._textual_widgets import _calendar_setup, \
    _combined_text, _preselected

CAL_TOKEN = '?'
_CHOICE_REQUIRED = 'Please choose a value.'
_COMPACT_BUTTON = '…'
# The cells of border and padding each input kind adds around its text, so
# a width hint in characters is the width of the text part, as in Tk.
_GUTTERS: tuple[tuple[type[Widget], int], ...] = (
    (Input, 6), (Select, 8), (SelectionList, 8))


class CellInput:
    """The built input of one field or cell, and how to use it.

    main is the input the user types in or selects from, which carries
    the id of the field or cell, and button the Browse or Pick button of
    a path or date input. widget is the widget to mount: main, or a row
    of main and its button.
    """

    def __init__(self, cell: AskCell, main: Widget,
                 button: Optional[Button] = None) -> None:
        """Store the cell and its widgets, with no answer seen yet."""
        self.cell = cell
        self.main = main
        self.button = button
        self.widget = main if button is None else Horizontal(main, button)
        self._seen: Optional[tuple[Optional[PrefillValueType],
                                   Optional[str]]] = None

    def value(self) -> Optional[PrefillValueType]:
        """Return the current answer value read from the input.

        An empty input gives the default, None when nullable, or an empty
        string for text. Text that is not a valid answer gives None, and
        error() tells why.
        """
        if isinstance(self.main, Input):
            return _text_value(self.cell, self.main.value)
        return _picked_value(self.cell, self.main)

    def answer(self) -> AnswerCell:
        """Return the current answer of the field or cell."""
        return answer_of(self.cell, self.value())

    def error(self) -> Optional[str]:
        """Return the input's own validation error, or None when valid."""
        cell, widget = self.cell, self.main
        if isinstance(widget, Input):
            return _text_error(cell, widget.value)
        if isinstance(widget, Select):
            nullable = isinstance(cell, AskChoiceCell) and cell.nullable
            return _CHOICE_REQUIRED if widget.is_blank() and not nullable \
                else None
        if isinstance(widget, SelectionList):
            assert isinstance(cell, AskMultiChoiceCell)
            return multi_count_message(len(widget.selected), cell.min_select,
                                       cell.max_select)
        return None

    def settle(self) -> None:
        """Record the current answer and error as seen, once mounted."""
        self._seen = (self.value(), self.error())

    def take_change(self) -> bool:
        """Return whether the answer or error changed since last seen.

        The current answer and error are recorded as seen, so an event
        that only repeats them, such as the one Textual posts when the
        input is mounted, is not taken as a change.
        """
        seen = self._seen
        self.settle()
        return self._seen != seen

    def write(self, value: PrefillValueType) -> None:
        """Write a prefill value into the input, even when it is disabled.

        The value has been checked against the cell type, see
        wizard_ui_bridge.form_helpers.prefill_value(). Setting the widget
        value raises the framework's change event, so the screen updates
        as if the user had typed it; an equal value raises none.
        """
        widget = self.main
        if isinstance(widget, Input):
            widget.value = format_new_value(value)
        elif isinstance(widget, Checkbox):
            assert isinstance(value, bool)
            widget.value = value
        elif isinstance(widget, Select):
            assert isinstance(value, str)
            widget.value = value
        else:
            assert isinstance(widget, SelectionList)
            assert isinstance(value, (list, tuple))
            _set_multi(widget, self.cell, value)

    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable the input and any button beside it."""
        self.main.disabled = not enabled
        if self.button is not None:
            self.button.disabled = not enabled

    def wants_calendar(self) -> bool:
        """Return whether a date input holds the calendar pick token.

        Typing the '?' token into a date or date-time input is an
        alternative to pressing the Pick button. The token is left in the
        input until the calendar closes, when it is replaced by the
        picked date or cleared on cancel.
        """
        return isinstance(self.cell, (AskDateCell, AskDateTimeCell)) \
            and self._text() == CAL_TOKEN

    def open_dialog(self) -> None:
        """Open the directory picker or the calendar of the input.

        The picker is seeded with the path typed so far and the calendar
        with the date typed so far.
        """
        cell, text = self.cell, self._text()
        if isinstance(cell, AskPathCell):
            self.main.app.push_screen(_PickerScreen(cell.path_options, text),
                                      self._path_picked)
            return
        seed, minimum, maximum = _calendar_setup(cell, text)
        self.main.app.push_screen(_CalendarScreen(seed, minimum, maximum),
                                  self._date_picked)

    def _text(self) -> str:
        """Return the text of a text input."""
        assert isinstance(self.main, Input)
        return self.main.value

    def _path_picked(self, result: Optional[str]) -> None:
        """Fill the path input with the picked path, if any.

        Setting the input value raises Input.Changed, so the answer and
        the partial validator update as if the user had typed the path.
        """
        if result is not None:
            assert isinstance(self.main, Input)
            self.main.value = result

    def _date_picked(self, result: Optional[date]) -> None:
        """Fill the date input with the picked date, if any.

        A cancelled calendar clears a lingering pick token; a picked date
        replaces the input, keeping any time part of a date-time input.
        Setting the value raises Input.Changed, so the answer refreshes.
        """
        assert isinstance(self.main, Input)
        if result is None:
            if self.main.value == CAL_TOKEN:
                self.main.value = ''
            return
        self.main.value = _combined_text(self.cell, result, self.main.value)


def build_input(cell: AskCell, prefix: str, key: str,
                compact: bool = False) -> CellInput:
    """Build the input of an input cell or field, see the module docstring.

    A label cell has no input and must not be passed. The help text of
    the cell is the tooltip of the input.
    """
    main = _main_widget(cell, f'{prefix}_{key}')
    built = CellInput(cell, main, _button_for(cell, key, compact))
    width = cell.width if cell.width is not None or not compact \
        else compact_width(cell)
    _apply_width(main, width)
    if cell.help_text is not None:
        built.widget.tooltip = cell.help_text
    return built


def _main_widget(cell: AskCell, widget_id: str) -> Widget:
    """Return the input the user types in or selects from for a cell."""
    text = _start_text(cell)
    if text is not None:
        sensitive = isinstance(cell, AskTextCell) and cell.sensitive
        return Input(value=text, password=sensitive, id=widget_id)
    if isinstance(cell, AskYesNoCell):
        return Checkbox(value=cell.start_or_default, id=widget_id)
    if isinstance(cell, AskChoiceCell):
        return _choice_select(cell, widget_id)
    assert isinstance(cell, AskMultiChoiceCell)
    return _multi_selection(cell, widget_id)


def _start_text(cell: AskCell) -> Optional[str]:
    """Return the start text of a cell shown as a text input, else None.

    That is the formatted start value, else the default, else ''.
    """
    if isinstance(cell, NEW_CELL_TYPES):
        start = cell.start_or_default
        return '' if start is None else format_new_value(start)
    if isinstance(cell, AskTextCell):
        return cell.start_or_default or ''
    if isinstance(cell, AskIntCell):
        return _optional_text(cell.start_or_default)
    if isinstance(cell, AskPathCell):
        return _optional_text(cell.path_options.start_or_default)
    return None


def _optional_text(value: Optional[Union[int, Path]]) -> str:
    """Return the input text of an integer or path, or '' for None."""
    return '' if value is None else str(value)


def _choice_select(cell: AskChoiceCell, widget_id: str) -> Select[str]:
    """Return a drop-down for a choice cell, blank when no default.

    It starts with the start value, else the default, else blank.
    """
    options = [(choice, choice) for choice in cell.choices]
    start = cell.start_or_default
    if start is not None:
        return Select(options, value=start, allow_blank=cell.default is None,
                      id=widget_id)
    return Select(options, allow_blank=True, id=widget_id)


def _multi_selection(cell: AskMultiChoiceCell,
                     widget_id: str) -> SelectionList[int]:
    """Return a check-box list for a multi-choice cell."""
    chosen = set(_preselected(cell.choices, cell.start_or_default))
    selections = [Selection(choice, index, index in chosen)
                  for index, choice in enumerate(cell.choices)]
    return SelectionList[int](*selections, id=widget_id)


def _button_for(cell: AskCell, key: str, compact: bool) -> Optional[Button]:
    """Return the Browse or Pick button of a path or date cell, else None."""
    if isinstance(cell, AskPathCell):
        kind, label = 'browse', 'Browse'
    elif isinstance(cell, (AskDateCell, AskDateTimeCell)):
        kind, label = 'pick', 'Pick'
    else:
        return None
    return Button(_COMPACT_BUTTON if compact else label, id=f'{kind}_{key}',
                  classes=kind)


def _apply_width(widget: Widget, width: Optional[int]) -> None:
    """Size an input to a width hint in characters, if one is given.

    The hint is the width of the text part, so the border and padding
    of the input are added. A check box has no text part and keeps its
    size. The minimum width is set too, since an auto-sized grid column,
    as in a matrix, is as wide as its widgets' content and minimum width.
    """
    if width is None:
        return
    for kind, gutter in _GUTTERS:
        if isinstance(widget, kind):
            widget.styles.width = widget.styles.min_width = width + gutter
            return


def _text_value(cell: AskCell, text: str) -> Optional[PrefillValueType]:
    """Return the answer value of a cell shown as a text input."""
    if isinstance(cell, NEW_CELL_TYPES):
        return value_from_text(cell, text)
    if isinstance(cell, AskTextCell):
        return text_answer(text, cell.nullable, cell.default)
    if isinstance(cell, AskIntCell):
        return cell.default if text == '' else int_text(text)
    assert isinstance(cell, AskPathCell)
    return path_answer(text, cell.path_options)[1]


def _picked_value(cell: AskCell, main: Widget) -> Optional[PrefillValueType]:
    """Return the answer value of a check box, drop-down or list."""
    if isinstance(main, Checkbox):
        return bool(main.value)
    if isinstance(main, Select):
        return None if main.is_blank() else str(main.value)
    assert isinstance(main, SelectionList)
    assert isinstance(cell, AskMultiChoiceCell)
    return [cell.choices[index] for index in sorted(main.selected)]


def _text_error(cell: AskCell, text: str) -> Optional[str]:
    """Return the own error of a cell shown as a text input, or None."""
    if isinstance(cell, NEW_CELL_TYPES):
        return error_from_text(cell, text)
    if isinstance(cell, AskIntCell):
        return _int_error(cell, text)
    if isinstance(cell, AskPathCell):
        done, _, reason = path_answer(text, cell.path_options)
        return None if done else reason
    return None


def _int_error(cell: AskIntCell, text: str) -> Optional[str]:
    """Return the integer input's validation error, or None."""
    if text == '':
        return None if cell.nullable or cell.default is not None \
            else INT_ERROR
    value = int_text(text)
    if value is None:
        return INT_ERROR
    if out_of_range(value, cell.min_value, cell.max_value):
        return range_error(cell.min_value, cell.max_value)
    return None


def _set_multi(selection: SelectionList[int], cell: AskCell,
               members: Union[list[str], tuple[str, ...]]) -> None:
    """Select exactly the given members in a check-box list."""
    assert isinstance(cell, AskMultiChoiceCell)
    wanted = {cell.choices.index(member) for member in members}
    current = set(selection.selected)
    for value in wanted - current:
        selection.select(value)
    for value in current - wanted:
        selection.deselect(value)
