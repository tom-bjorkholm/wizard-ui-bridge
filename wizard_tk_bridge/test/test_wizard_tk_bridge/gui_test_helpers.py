#! /usr/local/bin/python3
"""Shared helpers for wizard_tk_bridge tests."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import time
import tkinter as tk
from contextlib import contextmanager
from typing import Callable, Iterator, Optional
import pytest

SCREEN_CLEAR_TIME = 0.5
EVENT_LOOP_STEP = 0.01


def root_or_skip() -> tk.Tk:
    """Return a withdrawn Tk root, or skip when no display is available."""
    try:
        root = tk.Tk()
    except tk.TclError:
        pytest.skip('no display available')
    root.withdraw()
    return root


def _shown_windows(root: tk.Tk) -> list[tk.Wm]:
    """Return the windows of this Tk application that are on the screen.

    ``wm stackorder`` lists exactly the top-level windows Tk has mapped,
    which are the ones that still have to leave the screen.
    """
    windows: list[tk.Wm] = []
    for name in root.tk.splitlist(root.tk.call('wm', 'stackorder', '.')):
        window = root.nametowidget(str(name))
        assert isinstance(window, tk.Wm)
        windows.append(window)
    return windows


def _run_event_loop(root: tk.Tk, seconds: float) -> None:
    """Run the root's event loop for the given time."""
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        root.update()
        time.sleep(EVENT_LOOP_STEP)


def _clear_screen(root: tk.Tk) -> None:
    """Take the windows a test showed off the screen.

    Tk leaves the actual removal to the window system, which finishes it
    only while the event loop keeps running. Destroying the root does not
    run that loop, so without this the windows stay painted on the desktop
    for the rest of the pytest process. Tests that keep every window
    hidden have nothing to remove and pay nothing here.
    """
    windows = _shown_windows(root)
    if not windows:
        return
    for window in windows:
        window.withdraw()
    _run_event_loop(root, SCREEN_CLEAR_TIME)


@contextmanager
def gui_root() -> Iterator[tk.Tk]:
    """Yield a withdrawn Tk root and destroy it afterwards.

    This factors out the create-try-finally-destroy boilerplate the widget
    tests share; the test body runs inside the ``with`` block. The test is
    skipped when no display is available.
    """
    root = root_or_skip()
    try:
        yield root
    finally:
        _clear_screen(root)
        root.destroy()


def press_close(win: tk.Toplevel) -> None:
    """Send a Cmd-W key press to a window so its close binding fires.

    The window is realized with ``update`` first, and the event is
    delivered synchronously with ``when='now'`` so the bound handler runs
    before this call returns. This delivers to a normal top-level window;
    a transient window would need forced focus, which is avoided here as
    it can crash Tk during automated runs, so transient windows verify
    the binding through :class:`CloseSpy` instead.
    """
    win.update()
    win.event_generate('<Command-w>', when='now')


# pylint: disable-next=too-few-public-methods
class CloseSpy:
    """Record the windows and actions passed to a patched ``bind_close``.

    A transient window cannot receive a synthetic key press without forced
    focus, so its test replaces ``bind_close`` with this spy and checks
    that the window wires the intended close action.
    """

    def __init__(self) -> None:
        """Start with no recorded close bindings."""
        self.calls: list[tuple[tk.Misc, Optional[Callable[[], None]]]] = []

    def __call__(self, win: tk.Misc,
                 on_close: Optional[Callable[[], None]] = None) -> None:
        """Record one ``bind_close`` call and its close action."""
        self.calls.append((win, on_close))
