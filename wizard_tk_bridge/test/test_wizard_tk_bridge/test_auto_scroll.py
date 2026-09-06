#! /usr/local/bin/python3
"""Tests for the auto-hiding scroll command, wheel and touchpad."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter as tk
from tkinter import ttk
import pytest
from wizard_tk_bridge.auto_scroll import NOTCH_DELTA, TOUCHPAD_EVENT, \
    auto_hide, bind_wheel, _own_wheel, _scroll, _touchpad_steps, \
    _wheel_amount, _wheel_area, _wheel_delta
from .gui_test_helpers import find_widgets, gui_root

SCROLL_REGION = (0, 0, 500, 500)
AREA_WIDTH = 100
AREA_HEIGHT = 50
LIST_HEIGHT = 3
LIST_ITEMS = 20
COMBO_WIDTH = 3
UNIT_PIXELS = 10
TOUCH_STEP = 25
TOUCHPAD_ONLY = pytest.mark.skipif(tk.TkVersion < 9.0,
                                   reason='only Tk 9 reports a touchpad')


def wheel_event(delta: int = -NOTCH_DELTA,
                num: int = 0) -> 'tk.Event[tk.Misc]':
    """Return a mouse wheel event as Tk delivers one.

    Tk reports no button number for a wheel event, which tkinter keeps
    as a string that no button number matches; zero stands for it here
    so that the event stays an event of whole numbers.
    """
    event: 'tk.Event[tk.Misc]' = tk.Event()
    event.delta = delta
    event.num = num
    return event


def wheel_over(widget: tk.Misc, delta: int) -> None:
    """Send the widget one wheel event, as Tk delivers one over it."""
    widget.event_generate('<MouseWheel>', delta=delta, x=1, y=1,
                          rootx=widget.winfo_rootx() + 1,
                          rooty=widget.winfo_rooty() + 1)
    widget.update()


def touchpad_over(widget: tk.Misc, sideways: int, downward: int) -> None:
    """Send the widget one touchpad gesture, as Tk delivers one over it.

    Tk packs the two steps of the gesture into the delta of the event,
    the sideways one in its high half and the downward one in its low
    half, which is what a real touchpad event carries.
    """
    widget.event_generate(TOUCHPAD_EVENT,
                          delta=(sideways << 16) | (downward & 0xffff))
    widget.update()


def scroll_area(root: tk.Tk) -> tk.Canvas:
    """Return a wheel-bound area holding content larger than itself.

    A scroll unit is fixed at a number of pixels here, where a canvas
    normally scrolls a tenth of its window, so that the area scrolls by
    a known step also in a window the window system never sized.
    """
    canvas = tk.Canvas(root, width=AREA_WIDTH, height=AREA_HEIGHT)
    canvas.pack()
    inner = tk.Frame(canvas)
    tk.Label(inner, text='content').pack()
    canvas.create_window((0, 0), window=inner, anchor='nw')
    canvas.configure(scrollregion=SCROLL_REGION, xscrollincrement=UNIT_PIXELS,
                     yscrollincrement=UNIT_PIXELS)
    bind_wheel(canvas)
    root.update_idletasks()
    return canvas


def long_list(parent: tk.Misc) -> tk.Listbox:
    """Return a list showing fewer items than it holds."""
    box = tk.Listbox(parent, height=LIST_HEIGHT)
    for index in range(LIST_ITEMS):
        box.insert('end', f'item {index}')
    box.pack()
    parent.update_idletasks()
    return box


@pytest.mark.parametrize('first,last,shown', [
    ('0.0', '1.0', False),
    ('0.0', '0.5', True),
    ('0.3', '1.0', True),
    ('0.25', '0.75', True)])
def test_auto_hide(first: str, last: str, shown: bool) -> None:
    """Test the scrollbar hides only when the whole range is visible."""
    with gui_root() as root:
        scrollbar = ttk.Scrollbar(tk.Frame(root), orient='horizontal')
        scrollbar.grid(row=0, column=0, sticky='ew')
        auto_hide(scrollbar)(first, last)
        assert bool(scrollbar.grid_info()) is shown


def test_reappears() -> None:
    """Test a hidden scrollbar returns to its cell when it can scroll."""
    with gui_root() as root:
        scrollbar = ttk.Scrollbar(tk.Frame(root), orient='horizontal')
        scrollbar.grid(row=1, column=0, sticky='ew')
        command = auto_hide(scrollbar)
        command('0.0', '1.0')
        assert not scrollbar.grid_info()
        command('0.0', '0.5')
        assert scrollbar.grid_info()['row'] == 1


@pytest.mark.parametrize('num,delta,expected', [
    (0, -NOTCH_DELTA, -NOTCH_DELTA), (0, 2 * NOTCH_DELTA, 2 * NOTCH_DELTA),
    (4, 0, NOTCH_DELTA), (5, 0, -NOTCH_DELTA)])
def test_wheel_delta(num: int, delta: int, expected: int) -> None:
    """Test the wheel buttons of X11 stand for one notch of the wheel."""
    assert _wheel_delta(wheel_event(delta, num)) == expected


@pytest.mark.parametrize('delta', [NOTCH_DELTA, -NOTCH_DELTA])
def test_wheel_amount(delta: int) -> None:
    """Test the amount opposes the delta and grows with it."""
    with gui_root() as root:
        amount = _wheel_amount(root, delta)
        assert amount == -_wheel_amount(root, -delta)
        assert (amount < 0.0) is (delta > 0)
        assert abs(_wheel_amount(root, 2 * delta)) > abs(amount)


@pytest.mark.parametrize('axis', ['x', 'y'])
def test_scroll_along_axis(axis: str) -> None:
    """Test one wheel step moves the view along the axis and back."""
    with gui_root() as root:
        canvas = scroll_area(root)
        view = canvas.yview if axis == 'y' else canvas.xview
        start = view()[0]
        _scroll(canvas, axis, -NOTCH_DELTA)
        moved = view()[0]
        assert moved > start
        _scroll(canvas, axis, NOTCH_DELTA)
        assert view()[0] < moved


def test_area_of_content() -> None:
    """Test the area is found from the canvas and from a widget in it."""
    with gui_root() as root:
        canvas = scroll_area(root)
        assert _wheel_area(canvas) is canvas
        assert _wheel_area(find_widgets(canvas, tk.Label)[0]) is canvas


def test_area_outside() -> None:
    """Test a widget outside every bound area is in no area at all."""
    with gui_root() as root:
        scroll_area(root)
        assert _wheel_area(root) is None
        assert _wheel_area(tk.Canvas(root)) is None


def test_bound_once() -> None:
    """Test a second area in the same window adds no second binding."""
    with gui_root() as root:
        scroll_area(root)
        bound = root.bind('<MouseWheel>')
        scroll_area(root)
        assert bound.strip()
        assert root.bind('<MouseWheel>') == bound
        assert '<Shift-MouseWheel>' in root.bind()


def test_own_wheel_list() -> None:
    """Test a list that holds more than it shows owns the wheel."""
    with gui_root() as root:
        assert _own_wheel(long_list(root), 'y') is True


@pytest.mark.visible_window
def test_own_wheel_sideways() -> None:
    """Test a list showing whole item texts leaves the sideways wheel.

    The window is really shown here, as a list that the window system
    never sized has no width for its items to fit in.
    """
    with gui_root() as root:
        root.deiconify()
        box = long_list(root)
        root.update()
        assert _own_wheel(box, 'x') is False


def test_own_wheel_short_list() -> None:
    """Test a list showing all it holds leaves the wheel to the area."""
    with gui_root() as root:
        box = tk.Listbox(root, height=LIST_HEIGHT)
        box.insert('end', 'the only item')
        box.pack()
        root.update_idletasks()
        assert _own_wheel(box, 'y') is False


def test_own_wheel_combobox() -> None:
    """Test a combobox keeps the wheel Tk steps its values with."""
    with gui_root() as root:
        assert _own_wheel(ttk.Combobox(root, values=['a', 'b']), 'y') is True


def test_own_wheel_label() -> None:
    """Test a plain widget leaves the wheel to the area around it."""
    with gui_root() as root:
        assert _own_wheel(tk.Label(root, text='x'), 'y') is False


@pytest.mark.visible_window
def test_wheel_scrolls() -> None:
    """Test a wheel event over the content scrolls the area and back.

    The event goes to the content widget, as Tk delivers it there, so
    the binding on the window is covered together with its handler. The
    window is really shown here, as Tk keeps the widgets inside a canvas
    off the screen, and their events unsent, until the window is on it.
    """
    with gui_root() as root:
        root.deiconify()
        canvas = scroll_area(root)
        root.update()
        label = find_widgets(canvas, tk.Label)[0]
        start = canvas.yview()[0]
        wheel_over(label, -NOTCH_DELTA)
        moved = canvas.yview()[0]
        assert moved > start
        wheel_over(label, NOTCH_DELTA)
        assert canvas.yview()[0] < moved


@pytest.mark.visible_window
def test_wheel_from_outside() -> None:
    """Test the pointer decides when the event reached another widget.

    Tk 8.6 on Windows sends the wheel to the focused widget instead of
    to the one under the pointer, which is why the area under the
    pointer answers an event that reached a widget outside it. The
    window is really shown here, as Tk names the widget at a screen
    position only for a window that is on the screen.
    """
    with gui_root() as root:
        canvas = scroll_area(root)
        outside = tk.Label(root, text='outside the area')
        outside.pack()
        root.deiconify()
        root.update()
        label = find_widgets(canvas, tk.Label)[0]
        start = canvas.yview()[0]
        outside.event_generate('<MouseWheel>', delta=-NOTCH_DELTA, x=1, y=1,
                               rootx=label.winfo_rootx() + 1,
                               rooty=label.winfo_rooty() + 1)
        root.update()
        assert canvas.yview()[0] > start


@pytest.mark.visible_window
def test_wheel_over_combobox() -> None:
    """Test the area holds still under the wheel over a combobox.

    Tk gives a combobox the wheel to step its own values with, and what
    the step comes to differs between Tk versions, so only the area is
    checked here. The window is really shown, for the same reason as in
    test_wheel_scrolls.
    """
    with gui_root() as root:
        root.deiconify()
        canvas = scroll_area(root)
        label = find_widgets(canvas, tk.Label)[0]
        combo = ttk.Combobox(canvas.winfo_children()[0], values=['a', 'b'],
                             width=COMBO_WIDTH)
        combo.pack(before=label)
        root.update()
        start = canvas.yview()[0]
        wheel_over(combo, -NOTCH_DELTA)
        assert canvas.yview()[0] == start


@TOUCHPAD_ONLY
@pytest.mark.parametrize('sideways,downward', [
    (0, -TOUCH_STEP), (0, TOUCH_STEP), (-TOUCH_STEP, 0), (TOUCH_STEP, 0)])
def test_touchpad_steps(sideways: int, downward: int) -> None:
    """Test both steps of a gesture come back out of the packed delta."""
    with gui_root() as root:
        delta = (sideways << 16) | (downward & 0xffff)
        steps = _touchpad_steps(root, delta)
        assert [step > 0 for step in steps] == [sideways > 0, downward > 0]
        assert [step < 0 for step in steps] == [sideways < 0, downward < 0]


@TOUCHPAD_ONLY
@pytest.mark.visible_window
def test_touchpad_scrolls() -> None:
    """Test a gesture over the content scrolls the area and back."""
    with gui_root() as root:
        root.deiconify()
        canvas = scroll_area(root)
        root.update()
        label = find_widgets(canvas, tk.Label)[0]
        start = canvas.yview()[0]
        touchpad_over(label, 0, -TOUCH_STEP)
        moved = canvas.yview()[0]
        assert moved > start
        touchpad_over(label, 0, TOUCH_STEP)
        assert canvas.yview()[0] < moved


@TOUCHPAD_ONLY
@pytest.mark.visible_window
def test_touchpad_both_ways() -> None:
    """Test one sideways-and-down gesture moves the area both ways."""
    with gui_root() as root:
        root.deiconify()
        canvas = scroll_area(root)
        root.update()
        label = find_widgets(canvas, tk.Label)[0]
        start = (canvas.xview()[0], canvas.yview()[0])
        touchpad_over(label, -TOUCH_STEP, -TOUCH_STEP)
        assert canvas.xview()[0] > start[0]
        assert canvas.yview()[0] > start[1]


@TOUCHPAD_ONLY
@pytest.mark.visible_window
def test_touchpad_as_text() -> None:
    """Test the area answers a gesture the way Tk's own text does.

    A text widget brings Tk's own touchpad binding, so moving both under
    the same gesture keeps the area going the way the rest of the window
    goes, whichever way a Tk version and a display turn a gesture into.
    """
    with gui_root() as root:
        root.deiconify()
        canvas = scroll_area(root)
        root.update()
        label = find_widgets(canvas, tk.Label)[0]
        text = tk.Text(root, height=LIST_HEIGHT, wrap='none')
        for line in range(LIST_ITEMS):
            text.insert('end', f'text line {line}\n')
        text.pack()
        root.update()
        text.yview_moveto(0.5)
        before = (text.yview()[0], canvas.yview()[0])
        touchpad_over(text, 0, -TOUCH_STEP)
        touchpad_over(label, 0, -TOUCH_STEP)
        assert (text.yview()[0] > before[0]) is (canvas.yview()[0] > before[1])


@TOUCHPAD_ONLY
@pytest.mark.visible_window
def test_touch_combobox() -> None:
    """Test the area holds still under a gesture over a combobox."""
    with gui_root() as root:
        root.deiconify()
        canvas = scroll_area(root)
        label = find_widgets(canvas, tk.Label)[0]
        combo = ttk.Combobox(canvas.winfo_children()[0], values=['a', 'b'],
                             width=COMBO_WIDTH)
        combo.pack(before=label)
        root.update()
        start = canvas.yview()[0]
        touchpad_over(combo, 0, -TOUCH_STEP)
        assert canvas.yview()[0] == start


@TOUCHPAD_ONLY
def test_touchpad_bound() -> None:
    """Test the window answers the touchpad event Tk 9 reports."""
    with gui_root() as root:
        scroll_area(root)
        assert TOUCHPAD_EVENT in root.bind()
