#! /usr/local/bin/python3
"""Shared look and focus helpers for the Tkinter input windows.

Editable input widgets blend into the window background on some
platforms, so the user cannot tell an entry, drop-down or list from the
surrounding window. :func:`style_input` gives such a widget a white
field and a thin border so it stands out. :func:`choice_combo` builds a
styled read-only drop-down that a nullable choice can empty again.
:func:`focus_first_input` puts the keyboard focus on the first editable
widget of a window, so the user can start typing as soon as the window
opens. :func:`bind_submit` lets Return in an input confirm the prompt.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional, Sequence

INPUT_BG = 'white'
INPUT_STYLE = 'Input.TCombobox'
_RETURN_INPUTS = (tk.Entry, tk.Listbox, tk.Checkbutton, ttk.Combobox)


def style_input(widget: tk.Widget) -> None:
    """Make one editable input widget stand out from the background.

    A classic entry, text box or list gets a white field and a thin
    solid border. A drop-down keeps its arrow but gets a white field
    through a shared ttk style. Any other widget is left unchanged. The
    ttk styling is best-effort: a native theme that ignores field colors
    leaves the drop-down as it is.
    """
    if isinstance(widget, ttk.Widget):
        if isinstance(widget, ttk.Combobox):
            _style_combobox(widget)
        return
    if isinstance(widget, (tk.Entry, tk.Text, tk.Listbox)):
        widget.configure(background=INPUT_BG, relief='solid', borderwidth=1)


def choice_combo(parent: tk.Misc, choices: Sequence[str], nullable: bool,
                 width: int) -> ttk.Combobox:
    """Return a styled read-only drop-down offering choices.

    A read-only drop-down cannot be emptied by typing once a value is
    picked, so a nullable drop-down leads its list with a blank entry
    that empties it again. The drop-down starts empty.
    """
    values = ['', *choices] if nullable else list(choices)
    box = ttk.Combobox(parent, values=values, state='readonly', width=width)
    style_input(box)
    return box


def _style_combobox(widget: ttk.Combobox) -> None:
    """Give a drop-down a white field through a shared ttk style."""
    style = ttk.Style(widget)
    style.configure(INPUT_STYLE, fieldbackground=INPUT_BG)
    style.map(INPUT_STYLE, fieldbackground=[('readonly', INPUT_BG)])
    widget.configure(style=INPUT_STYLE)


def focus_first_input(window: tk.Misc) -> None:
    """Give the keyboard focus to the first editable input, if any."""
    target = _first_input(window)
    if target is not None:
        target.focus_set()


def _first_input(parent: tk.Misc) -> Optional[tk.Misc]:
    """Return the first editable input under parent, in child order."""
    for child in parent.winfo_children():
        if _is_input(child):
            return child
        found = _first_input(child)
        if found is not None:
            return found
    return None


def _is_input(widget: tk.Misc) -> bool:
    """Return whether the widget is an editable input to fill in."""
    if not isinstance(widget, (tk.Entry, tk.Listbox, tk.Text)):
        return False
    return str(widget.cget('state')) != 'disabled'


def bind_submit(widget: tk.Misc, on_ok: Callable[[], None]) -> None:
    """Bind Return to the confirm action on every input inside widget.

    A prompt builds its inputs before its buttons, so binding them all
    from one place gives every prompt the same rule: Return in an input
    does what the default OK button does. Only inputs are bound, which
    both leaves the Browse, Pick and navigation buttons their own keys
    and reaches the entry inside a two-widget input row. An editor that
    adds inputs later binds each of them itself when it builds it.
    """
    if isinstance(widget, _RETURN_INPUTS):
        widget.bind('<Return>', lambda _event: on_ok(), add='+')
    for child in widget.winfo_children():
        bind_submit(child, on_ok)
