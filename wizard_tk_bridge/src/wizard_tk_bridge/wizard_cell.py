#! /usr/local/bin/python3
"""The input of one form field or matrix cell, and the editors' layout.

A form row and a matrix cell show the same kinds of input: an entry for
text and integers, a path entry with a Browse button, a check box, a
drop-down, a multi-selection list, and a placeholder entry, with a
calendar Pick button for dates, for the typed values. :func:`build_input`
builds the :class:`CellInput` for one Ask*Cell (every Ask*Field is one
too), which reads the current answer value, reports the input's own
validation error, writes a prefill into the input, and enables or
disables it. The width hint of a cell sizes the text part of its input;
without one a compact input, as in a matrix, gets the narrower default
of wizard_ui_bridge.matrix_helpers.compact_width(). :class:`HelpTooltip`
shows a help text on hover, :func:`scrolled_editor` builds the scrolling
area and status line shared by the form and matrix editors, and
:func:`scroll_into_view` scrolls that area to show one of its widgets.

Turning the raw text of an integer input into its answer is the same job
in a cell and in a standalone question, so :func:`int_answer` lives here
and is shared with the wizard window. Its text counterpart is
:func:`wizard_ui_bridge.bridge_helpers.text_answer`, which every bridge
shares, so a graphical answer is accepted or rejected exactly as a
console one is.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from tkinter import ttk
from typing import Callable, Optional, Sequence
from wizard_ui_bridge import AskCell, PrefillValueType, AskTextCell, \
    AskIntCell, AskPathCell, AskYesNoCell, AskChoiceCell, \
    AskMultiChoiceCell, AskFloatCell, AskTimeCell, AskDurationCell
from wizard_ui_bridge.bridge_helpers import INT_ERROR as _INT_ERROR, \
    int_text, multi_count_message, out_of_range, path_answer, range_error, \
    text_answer
from wizard_ui_bridge.matrix_helpers import compact_width
from wizard_tk_bridge.auto_scroll import auto_hide, bind_wheel
from wizard_tk_bridge.gui_style import choice_combo, style_input
from wizard_tk_bridge.wizard_path import PathRow
from wizard_tk_bridge.wizard_pick_row import HintEntry, PickRow, TypedInput
from wizard_tk_bridge.wizard_typed import default_text, field_hint, \
    format_value, is_typed, typed_error, typed_value

WRAP_LENGTH = 520
MULTI_HEIGHT = 6
ENTRY_WIDTH = 34
INT_WIDTH = 14
CHOICE_WIDTH = 30
_CHOICE_REQUIRED = 'Please choose a value.'
TOOLTIP_BG = '#ffffe0'
TOOLTIP_WRAP = 320
TOOLTIP_GAP = 2


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


def _inside(start: int, size: int, limit: int) -> int:
    """Return the start coordinate that keeps size within limit."""
    return max(0, min(start, limit - size))


class HelpTooltip:
    """A hover bubble showing a help text over its widgets.

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


def _hint_note(cell: AskCell) -> Optional[str]:
    """Return the format hint sentence for a typed cell, or None."""
    return f'Enter {field_hint(cell)}.' if is_typed(cell) else None


def tooltip_text(cell: AskCell) -> Optional[str]:
    """Return the tooltip text combining help text and format hint."""
    note = _hint_note(cell)
    if cell.help_text is None:
        return note
    return cell.help_text if note is None else f'{cell.help_text}\n{note}'


@dataclass(frozen=True)
class CellInput:
    """The built input of one field or cell, and how to use it.

    widget is the widget to place in a grid. Some inputs keep a handle
    of their own besides it: var holds the value of a yes/no check box,
    path is the path entry with its Browse button, and typed is the
    placeholder entry, with any Pick button, of a typed field or cell.
    """

    cell: AskCell
    widget: tk.Widget
    var: Optional[tk.BooleanVar] = None
    path: Optional[PathRow] = None
    typed: Optional[TypedInput] = None

    def value(self) -> Optional[PrefillValueType]:
        """Return the current answer value read from the input.

        An empty input gives the default, or None when there is no
        default. Text that is not a valid answer also gives None, and
        error() tells why.
        """
        if self.typed is not None:
            return typed_value(self.cell, self.typed.text())
        return _basic_value(self)

    def error(self) -> Optional[str]:
        """Return the input's own validation error, or None when valid."""
        if self.typed is not None:
            return typed_error(self.cell, self.typed.text())
        return _basic_error(self)

    def write(self, value: PrefillValueType) -> None:
        """Write a prefill value into the input, even when it is disabled.

        The value has been checked against the cell type, see
        wizard_ui_bridge.form_helpers.prefill_value().
        """
        cell = self.cell
        if self.typed is not None:
            self.typed.set_text(format_value(value))
        elif isinstance(cell, (AskTextCell, AskIntCell)):
            _set_entry_text(_entry_widget(self), str(value))
        elif isinstance(cell, AskPathCell):
            assert self.path is not None
            self.path.set_text(str(value))
        elif isinstance(cell, AskYesNoCell):
            assert self.var is not None
            self.var.set(bool(value))
        elif isinstance(cell, AskChoiceCell):
            assert isinstance(self.widget, ttk.Combobox)
            _set_combo(self.widget, str(value))
        else:
            assert isinstance(cell, AskMultiChoiceCell)
            assert isinstance(self.widget, tk.Listbox)
            _set_multi(self.widget, cell.choices, value)

    def main_widget(self) -> tk.Widget:
        """Return the widget the user types or clicks in.

        That is the text entry of a path or typed input, beside its
        button, and otherwise the widget itself. It is the widget to give
        the keyboard focus to.
        """
        if self.typed is not None:
            return self.typed.entry
        if self.path is not None:
            return self.path.entry
        return self.widget

    def set_width(self, width: int) -> None:
        """Set the width in characters of the input's text part.

        A check box has no text part, so it keeps its size.
        """
        if self.var is None:
            self.main_widget()['width'] = width

    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable the input, keeping a drop-down read-only."""
        if self.typed is not None:
            self.typed.set_enabled(enabled)
            return
        if self.path is not None:
            self.path.set_enabled(enabled)
            return
        active = 'readonly' if isinstance(self.widget, ttk.Combobox) \
            else 'normal'
        self.widget['state'] = active if enabled else 'disabled'


def _text_input(parent: tk.Misc, cell: AskTextCell,
                change: Callable[[], None]) -> CellInput:
    """Build a text entry, pre-filled unless sensitive.

    It starts with the start value, else the default.
    """
    entry = tk.Entry(parent, width=ENTRY_WIDTH)
    start = cell.start_or_default
    if cell.sensitive:
        entry.configure(show='*')
    elif start is not None:
        entry.insert(0, start)
    style_input(entry)
    entry.bind('<KeyRelease>', lambda _event: change())
    return CellInput(cell, entry)


def _int_input(parent: tk.Misc, cell: AskIntCell,
               change: Callable[[], None]) -> CellInput:
    """Build a numeric text entry pre-filled with its start or default."""
    entry = tk.Entry(parent, width=INT_WIDTH)
    start = cell.start_or_default
    if start is not None:
        entry.insert(0, str(start))
    style_input(entry)
    entry.bind('<KeyRelease>', lambda _event: change())
    return CellInput(cell, entry)


def _path_input(parent: tk.Misc, cell: AskPathCell,
                change: Callable[[], None]) -> CellInput:
    """Build a path entry with a Browse button from the path options.

    It starts with the start value, else the default.
    """
    start = cell.path_options.start_or_default
    initial = '' if start is None else str(start)
    row = PathRow(parent, cell.path_options, initial, change)
    return CellInput(cell, row.frame, path=row)


def _yes_no_input(parent: tk.Misc, cell: AskYesNoCell,
                  change: Callable[[], None]) -> CellInput:
    """Build a check box holding the yes/no start value, else default."""
    var = tk.BooleanVar(parent, cell.start_or_default)
    check = tk.Checkbutton(parent, variable=var, command=change)
    return CellInput(cell, check, var=var)


def _choice_input(parent: tk.Misc, cell: AskChoiceCell,
                  change: Callable[[], None]) -> CellInput:
    """Build a read-only drop-down, preselecting any start or default.

    A nullable choice gets a blank entry, see choice_combo().
    """
    box = choice_combo(parent, cell.choices, cell.nullable, CHOICE_WIDTH)
    start = cell.start_or_default
    if start is not None:
        box.set(start)
    box.bind('<<ComboboxSelected>>', lambda _event: change())
    return CellInput(cell, box)


def _multi_input(parent: tk.Misc, cell: AskMultiChoiceCell,
                 change: Callable[[], None]) -> CellInput:
    """Build a multi-selection list, preselecting the start or default."""
    box = tk.Listbox(parent, selectmode='multiple', exportselection=False,
                     height=min(len(cell.choices), MULTI_HEIGHT))
    for choice in cell.choices:
        box.insert('end', choice)
    _preselect(box, cell.choices, cell.start_or_default)
    style_input(box)
    box.bind('<<ListboxSelect>>', lambda _event: change())
    return CellInput(cell, box)


def _preselect(box: tk.Listbox, choices: Sequence[str],
               start: Optional[Sequence[str]]) -> None:
    """Select the start values in a multi-selection list."""
    if start is None:
        return
    wanted = set(start)
    for index, choice in enumerate(choices):
        if choice in wanted:
            box.selection_set(index)


def _hint_input(parent: tk.Misc, cell: AskCell,
                change: Callable[[], None]) -> CellInput:
    """Build a placeholder entry for a float, time or duration cell."""
    entry = HintEntry(parent, field_hint(cell), default_text(cell), change)
    return CellInput(cell, entry.entry, typed=entry)


def _pick_input(parent: tk.Misc, cell: AskCell,
                change: Callable[[], None]) -> CellInput:
    """Build a date or date-time entry with a calendar Pick button."""
    row = PickRow(parent, cell, field_hint(cell), default_text(cell), change)
    return CellInput(cell, row.frame, typed=row)


def _typed_input(parent: tk.Misc, cell: AskCell,
                 change: Callable[[], None]) -> CellInput:
    """Build the input widget for one of the five typed cells."""
    if isinstance(cell, (AskFloatCell, AskTimeCell, AskDurationCell)):
        return _hint_input(parent, cell, change)
    return _pick_input(parent, cell, change)


def _basic_input(parent: tk.Misc, cell: AskCell,
                 change: Callable[[], None]) -> CellInput:
    """Build the input widget for one of the original cell kinds."""
    if isinstance(cell, AskTextCell):
        return _text_input(parent, cell, change)
    if isinstance(cell, AskIntCell):
        return _int_input(parent, cell, change)
    if isinstance(cell, AskPathCell):
        return _path_input(parent, cell, change)
    if isinstance(cell, AskYesNoCell):
        return _yes_no_input(parent, cell, change)
    if isinstance(cell, AskChoiceCell):
        return _choice_input(parent, cell, change)
    assert isinstance(cell, AskMultiChoiceCell)
    return _multi_input(parent, cell, change)


def build_input(parent: tk.Misc, cell: AskCell, change: Callable[[], None],
                compact: bool = False) -> CellInput:
    """Build the input matching an input cell or field type.

    change is called whenever the user changes the input. A label cell
    has no input and must not be passed. The width hint of the cell sizes
    the text part of the input. Without one, a compact input, as in a
    matrix, gets a narrower default width than a form row.
    """
    if is_typed(cell):
        built = _typed_input(parent, cell, change)
    else:
        built = _basic_input(parent, cell, change)
    width = cell.width if cell.width is not None or not compact \
        else compact_width(cell)
    if width is not None:
        built.set_width(width)
    return built


def _entry_widget(cell_input: CellInput) -> tk.Entry:
    """Return the text entry of a text or integer input."""
    assert isinstance(cell_input.widget, tk.Entry)
    return cell_input.widget


def _int_value(cell_input: CellInput, cell: AskIntCell) -> Optional[int]:
    """Return the integer value of an input, or its default when empty."""
    text = _entry_widget(cell_input).get()
    return cell.default if text == '' else int_text(text)


def _path_value(cell_input: CellInput, cell: AskPathCell) -> Optional[Path]:
    """Return the accepted path of an input, or None when not accepted."""
    assert cell_input.path is not None
    _, path, _ = path_answer(cell_input.path.get(), cell.path_options)
    return path


def _choice_value(cell_input: CellInput) -> Optional[str]:
    """Return the chosen value of an input, or None when none is chosen."""
    assert isinstance(cell_input.widget, ttk.Combobox)
    value = cell_input.widget.get()
    return value if value != '' else None


def _multi_selected(cell_input: CellInput) -> list[int]:
    """Return the selected 0-based indexes of a multi-selection input."""
    assert isinstance(cell_input.widget, tk.Listbox)
    picks = cell_input.widget.curselection()  # type: ignore[no-untyped-call]
    return [int(index) for index in picks]


def _multi_values(cell_input: CellInput,
                  cell: AskMultiChoiceCell) -> list[str]:
    """Return the chosen values of a multi-selection input, in order."""
    return [cell.choices[index] for index in _multi_selected(cell_input)]


def _basic_value(cell_input: CellInput) -> Optional[PrefillValueType]:
    """Return the answer value of an input of an original cell kind."""
    cell = cell_input.cell
    if isinstance(cell, AskTextCell):
        text = _entry_widget(cell_input).get()
        return text_answer(text, cell.nullable, cell.default)
    if isinstance(cell, AskIntCell):
        return _int_value(cell_input, cell)
    if isinstance(cell, AskPathCell):
        return _path_value(cell_input, cell)
    if isinstance(cell, AskYesNoCell):
        assert cell_input.var is not None
        return bool(cell_input.var.get())
    if isinstance(cell, AskChoiceCell):
        return _choice_value(cell_input)
    assert isinstance(cell, AskMultiChoiceCell)
    return _multi_values(cell_input, cell)


def _int_error(cell_input: CellInput, cell: AskIntCell) -> Optional[str]:
    """Return the integer input's own validation error, or None."""
    text = _entry_widget(cell_input).get()
    done, _, reason = int_answer(text, cell.nullable, cell.min_value,
                                 cell.max_value, cell.default)
    return None if done else reason


def _basic_error(cell_input: CellInput) -> Optional[str]:
    """Return the own error of an input of an original cell kind."""
    cell = cell_input.cell
    if isinstance(cell, AskIntCell):
        return _int_error(cell_input, cell)
    if isinstance(cell, AskPathCell):
        assert cell_input.path is not None
        done, _, reason = path_answer(cell_input.path.get(), cell.path_options)
        return None if done else reason
    if isinstance(cell, AskChoiceCell):
        chosen = _choice_value(cell_input) is not None
        return None if chosen or cell.nullable else _CHOICE_REQUIRED
    if isinstance(cell, AskMultiChoiceCell):
        return multi_count_message(len(_multi_selected(cell_input)),
                                   cell.min_select, cell.max_select)
    return None


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


def _scroll_canvas(outer: tk.Frame, sideways: bool) -> tk.Canvas:
    """Grid a canvas with auto-hiding scrollbars into outer's first cells.

    The vertical scrollbar is right of the canvas, and a sideways one
    below it. The wheel and touchpad scroll the canvas from its content.
    """
    canvas = tk.Canvas(outer, highlightthickness=0)
    canvas.grid(row=0, column=0, sticky='nsew')
    vbar = ttk.Scrollbar(outer, orient='vertical', command=canvas.yview)
    canvas.configure(yscrollcommand=auto_hide(vbar))
    vbar.grid(row=0, column=1, sticky='ns')
    if sideways:
        hbar = ttk.Scrollbar(outer, orient='horizontal', command=canvas.xview)
        canvas.configure(xscrollcommand=auto_hide(hbar))
        hbar.grid(row=1, column=0, sticky='ew')
    bind_wheel(canvas)
    return canvas


def scrolled_editor(parent: tk.Misc,
                    sideways: bool) -> tuple[tk.Frame, tk.Label]:
    """Build an editor's scrolling area and the status line below it.

    The inputs of a tall form or matrix would overflow the fixed-size
    wizard window, so they sit in a frame inside a scrolling canvas whose
    scrollbars appear only when they are needed. With sideways the area
    also scrolls horizontally, for a matrix wider than the window. The
    status line stays below the scroll area so it is always shown.

    Returns:
        The frame to grid the inputs into, and the status line label.
    """
    outer = tk.Frame(parent)
    outer.pack(fill='both', expand=True, pady=6)
    outer.rowconfigure(0, weight=1)
    outer.columnconfigure(0, weight=1)
    canvas = _scroll_canvas(outer, sideways)
    grid = tk.Frame(canvas)
    canvas.create_window((0, 0), window=grid, anchor='nw')
    grid.bind('<Configure>', lambda _event: canvas.configure(
        scrollregion=canvas.bbox('all')))
    status = tk.Label(outer, fg='red', wraplength=WRAP_LENGTH, justify='left')
    status.grid(row=2, column=0, columnspan=2, sticky='w', pady=(6, 0))
    return grid, status


def scroll_into_view(grid: tk.Frame, widget: tk.Widget) -> None:
    """Scroll an editor's area as little as needed to show a widget.

    grid is the frame returned by scrolled_editor() and widget one that
    is gridded into it. A widget larger than the area shows its start.
    """
    canvas = grid.master
    assert isinstance(canvas, tk.Canvas)
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox('all'))
    left = view_start(widget.winfo_x(), widget.winfo_reqwidth(),
                      canvas.canvasx(0), canvas.winfo_width())
    top = view_start(widget.winfo_y(), widget.winfo_reqheight(),
                     canvas.canvasy(0), canvas.winfo_height())
    canvas.xview_moveto(left / max(grid.winfo_reqwidth(), 1))
    canvas.yview_moveto(top / max(grid.winfo_reqheight(), 1))


def view_start(item: int, size: int, view: float, shown: int) -> float:
    """Return the new start of a scrolled view along one axis.

    The view starts at view and shows shown pixels. It moves as little
    as possible to show the item, of size pixels from item, or the
    item's start when the item is larger than the view.
    """
    if item < view:
        return item
    if item + size > view + shown:
        return min(item, item + size - shown)
    return view
