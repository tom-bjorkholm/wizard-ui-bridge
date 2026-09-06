#! /usr/local/bin/python3
"""Scroll commands and wheel and touchpad support for an area.

A table that fits its area needs no scrollbar, and a scrollbar that is
always shown wastes space and hints at hidden content that is not there.
:func:`auto_hide` returns the scroll command for a scrolling widget: the
command hides the scrollbar while the whole range is visible and shows it
again once the widget grows past its area. It works for any widget that
reports its position through an ``xscrollcommand`` or ``yscrollcommand``,
so a wizard table's canvas and any other scrolling widget can share it.

Tk binds the mouse wheel and, from Tk 9 on, the touchpad on each of its
scrolling widgets, but binds neither on a canvas. A scrolling area built
from a canvas therefore answers a scroll only while the pointer is over
its scrollbar. :func:`bind_wheel` gives the area both over its content
as well.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter as tk
from functools import partial
from tkinter import ttk
from typing import Callable, Optional
from weakref import WeakSet

WHEEL_EVENTS = {'<MouseWheel>': 'y', '<Shift-MouseWheel>': 'x'}
X11_WHEEL_EVENTS = {'<Button-4>': 'y', '<Button-5>': 'y',
                    '<Shift-Button-4>': 'x', '<Shift-Button-5>': 'x'}
TOUCHPAD_EVENT = '<TouchpadScroll>'
NOTCH_DELTA = 120
BUTTON_DELTA = {4: NOTCH_DELTA, 5: -NOTCH_DELTA}
UNIT_DELTA = 40.0
STEP_HALF = 0x10000
SIGN_LIMIT = 0x8000
_SCROLL_AREAS: WeakSet[tk.Canvas] = WeakSet()
_WHEEL_WINDOWS: WeakSet[tk.Misc] = WeakSet()


def auto_hide(scrollbar: ttk.Scrollbar
              ) -> Callable[[float | str, float | str], None]:
    """Return a scroll command that hides the scrollbar when it is full.

    The result is used as a widget's ``xscrollcommand`` or
    ``yscrollcommand``. Tk reports the position as two fractions, which it
    passes as strings, so the command accepts either a number or its
    string form. The scrollbar must be laid out with the grid manager,
    whose ``grid_remove`` remembers its cell across the hide.
    """
    def command(first: float | str, last: float | str) -> None:
        """Hide or show the scrollbar, then move its thumb to the view."""
        if float(first) <= 0.0 and float(last) >= 1.0:
            scrollbar.grid_remove()
        else:
            scrollbar.grid()
        scrollbar.set(first, last)
    return command


def bind_wheel(canvas: tk.Canvas) -> None:
    """Let the wheel and the touchpad scroll this canvas from its content.

    The binding sits on the window that holds the canvas, and not on the
    canvas and the widgets inside it, because those widgets are built and
    rebuilt while the user works. The window's handler then finds the
    area from the widget the scroll reached, so a single binding per
    window serves every area in it.

    A touchpad is bound separately from a wheel, as Tk 9 reports the two
    as different events, and only Tk 9 knows the touchpad one at all.
    """
    _SCROLL_AREAS.add(canvas)
    window = canvas.winfo_toplevel()
    if window in _WHEEL_WINDOWS:
        return
    _WHEEL_WINDOWS.add(window)
    for sequence, axis in _wheel_events(window).items():
        window.bind(sequence, partial(_on_wheel, window, axis), add='+')
    if tk.TkVersion >= 9.0:
        window.bind(TOUCHPAD_EVENT, partial(_on_touchpad, window), add='+')


def _wheel_events(window: tk.Misc) -> dict[str, str]:
    """Return the wheel sequences to bind, each with the axis it moves.

    X11 with Tk 8.6 has no wheel event: it presses button 4 and button 5
    instead, and the same buttons with shift held for the sideways
    wheel. Every other windowing system, and Tk 9 on all of them, sends
    a MouseWheel event, and binding those buttons there would answer the
    side buttons of a mouse instead.
    """
    if window.tk.call('tk', 'windowingsystem') == 'x11':
        return {**WHEEL_EVENTS, **X11_WHEEL_EVENTS}
    return WHEEL_EVENTS


def _on_wheel(window: tk.Misc, axis: str, event: 'tk.Event[tk.Misc]') -> None:
    """Scroll the area the wheel belongs to along the event's axis."""
    area = _event_area(window, event, axis)
    if area is not None:
        _scroll(area, axis, _wheel_delta(event))


def _on_touchpad(window: tk.Misc, event: 'tk.Event[tk.Misc]') -> None:
    """Scroll the area a touchpad gesture belongs to, both ways at once.

    A touchpad gesture moves the view whichever way the fingers went, so
    its event carries a sideways and a downward step together and needs
    no shift key for the sideways one. The steps are pixels, which the
    canvas moves by the same way it does under a dragging hand.
    """
    sideways, downward = _touchpad_steps(window, event.delta)
    axis = 'y' if abs(downward) >= abs(sideways) else 'x'
    area = _event_area(window, event, axis)
    if area is not None:
        area.scan_mark(0, 0)
        area.scan_dragto(sideways, downward, gain=1)


def _event_area(window: tk.Misc, event: 'tk.Event[tk.Misc]',
                axis: str) -> Optional[tk.Canvas]:
    """Return the area one scroll event moves along the axis, if any."""
    target = _scroll_widget(window, event)
    if target is None or _own_wheel(target, axis):
        return None
    return _wheel_area(target)


def _scroll_widget(window: tk.Misc,
                   event: 'tk.Event[tk.Misc]') -> Optional[tk.Misc]:
    """Return the widget one scroll event belongs to, if it is in an area.

    Tk sends the event to the widget under the pointer, which is what
    every scrolling widget of its own goes by, so the widget the event
    reached is tried first. Tk 8.6 on Windows instead sends the wheel to
    the focused widget, and looking the pointer position up then catches
    the case where the focus is outside every area.
    """
    widget = event.widget
    if isinstance(widget, tk.Misc) and _wheel_area(widget) is not None:
        return widget
    under_pointer = window.winfo_containing(event.x_root, event.y_root)
    if under_pointer is not None and _wheel_area(under_pointer) is not None:
        return under_pointer
    return None


def _wheel_area(widget: tk.Misc) -> Optional[tk.Canvas]:
    """Return the scrolling area the widget is in, if it is in one."""
    while True:
        if isinstance(widget, tk.Canvas) and widget in _SCROLL_AREAS:
            return widget
        parent = widget.winfo_parent()
        if not parent:
            return None
        widget = widget.nametowidget(parent)


def _own_wheel(widget: tk.Misc, axis: str) -> bool:
    """Return whether the widget answers the mouse wheel itself.

    A combobox steps through its values on the wheel, and a list or a
    text scrolls its own view while it holds more than it shows. The
    wheel then belongs to the widget and not to the area around it, and
    a list that shows all it holds leaves the wheel to the area.
    """
    if isinstance(widget, ttk.Combobox):
        return True
    if not isinstance(widget, (tk.Listbox, tk.Text)):
        return False
    view = widget.yview() if axis == 'y' else widget.xview()
    return float(view[0]) > 0.0 or float(view[1]) < 1.0


def _wheel_delta(event: 'tk.Event[tk.Misc]') -> int:
    """Return the wheel delta, also for X11's wheel button presses.

    X11 with Tk 8.6 has no delta to report: it presses button 4 for one
    notch up and button 5 for one notch down, which the delta of a whole
    notch stands for here. A wheel event carries no button number at
    all, which is why the number is looked up rather than tested.
    """
    return BUTTON_DELTA.get(event.num, event.delta)


def _touchpad_steps(widget: tk.Misc, delta: int) -> tuple[int, int]:
    """Return the sideways and downward pixels of one touchpad event.

    Tk packs both steps of the gesture into the one delta a scroll event
    carries, the sideways step in its high half and the downward one, as
    a signed number, in its low half. The steps are points, which Tk's
    own scrolling widgets turn into pixels for the display in use, and
    ``tk::ScaleNum`` is the very conversion those widgets apply.
    """
    sideways = delta >> 16
    low = delta & (STEP_HALF - 1)
    downward = low if low < SIGN_LIMIT else low - STEP_HALF
    return (int(widget.tk.call('tk::ScaleNum', sideways)),
            int(widget.tk.call('tk::ScaleNum', downward)))


def _scroll(area: tk.Canvas, axis: str, delta: int) -> None:
    """Scroll the area one wheel step along the axis.

    From Tk 9 on the step can be a fraction of a unit, which the finer
    steps of a trackpad give, so the amount goes to Tk as it is instead
    of through the whole-unit ``xview_scroll`` and ``yview_scroll``.
    """
    area.tk.call(str(area), f'{axis}view', 'scroll',
                 _wheel_amount(area, delta), 'units')


def _wheel_amount(widget: tk.Misc, delta: int) -> float:
    """Return the units one wheel event scrolls, as a scrollbar does.

    From Tk 9 on every windowing system reports 120 for one notch of the
    wheel, and Tk's own scrollbars scroll three units for it, taking a
    fraction of a unit for the finer steps of a trackpad. Tk 8.6 scrolls
    one whole unit per notch, and reports that notch as 1 on macOS and
    as 120 on the other windowing systems.
    """
    if tk.TkVersion >= 9.0:
        return -delta / UNIT_DELTA
    aqua = widget.tk.call('tk', 'windowingsystem') == 'aqua'
    return int(-delta / (1 if aqua else NOTCH_DELTA))
