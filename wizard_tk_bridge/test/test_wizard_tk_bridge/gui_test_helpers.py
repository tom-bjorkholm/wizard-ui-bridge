#! /usr/local/bin/python3
"""Shared helpers for wizard_tk_bridge tests."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import time
import tkinter as tk
from contextlib import contextmanager
from typing import Callable, Iterator, Optional, Sequence, TypeVar
import pytest
from wizard_tk_bridge.wizard_window import WizardWindow

SCREEN_CLEAR_TIME = 0.5
EVENT_LOOP_STEP = 0.01
PROMPT_TIMEOUT_MS = 5000
_W = TypeVar('_W', bound=tk.Misc)


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


def content_of(window: WizardWindow) -> tk.Frame:
    """Return the frame a wizard prompt builds its own widgets into."""
    # pylint: disable-next=protected-access
    return window._content


def abort_prompt(window: WizardWindow) -> None:
    """Abandon the waiting prompt, as the window's Abort button does."""
    # pylint: disable-next=protected-access
    window._cancel()


@contextmanager
def prompt_window() -> Iterator[tuple[tk.Tk, WizardWindow]]:
    """Yield a root and a modal wizard window of its own, closed after."""
    with gui_root() as root:
        window = WizardWindow(tk.Frame(root))
        try:
            yield (root, window)
        finally:
            window.close()


def find_widgets(parent: tk.Misc, kind: type[_W]) -> list[_W]:
    """Return every widget of the given kind under parent, in child order."""
    found: list[_W] = []
    for child in parent.winfo_children():
        if isinstance(child, kind):
            found.append(child)
        found.extend(find_widgets(child, kind))
    return found


def click_button(parent: tk.Misc, text: str) -> None:
    """Press the button labelled text somewhere under parent."""
    for button in find_widgets(parent, tk.Button):
        if str(button.cget('text')) == text:
            button.invoke()
            return
    pytest.fail(f'No button labelled {text} was built.')


def set_entry(entry: tk.Entry, text: str) -> None:
    """Replace what an entry holds with the given text."""
    entry.delete(0, 'end')
    entry.insert(0, text)


def first_entry(window: WizardWindow) -> tk.Entry:
    """Return the first entry the shown prompt built."""
    return find_widgets(content_of(window), tk.Entry)[0]


def answer_entry(window: WizardWindow, text: str) -> None:
    """Type text into the prompt's first entry and press its OK button."""
    set_entry(first_entry(window), text)
    click_button(content_of(window), 'OK')


def answer_list(window: WizardWindow, rows: Sequence[int]) -> None:
    """Select exactly the given rows of the prompt's list and press OK."""
    listbox = find_widgets(content_of(window), tk.Listbox)[0]
    listbox.selection_clear(0, 'end')
    for row in rows:
        listbox.selection_set(row)
    click_button(content_of(window), 'OK')


def label_texts(parent: tk.Misc) -> list[str]:
    """Return the texts of the labels under parent, in child order."""
    return [str(label.cget('text'))
            for label in find_widgets(parent, tk.Label)]


# pylint: disable-next=too-few-public-methods
class PromptDriver:
    """Answer the prompts of one wizard window, one action per prompt.

    Every prompt waits in a nested event loop of its own, and Tk runs all
    callbacks that are already due in the same loop, so the actions cannot
    all be scheduled up front: each one is scheduled from within the
    previous one instead. A watchdog abandons a prompt that no action
    answered, so a mistaken test fails instead of waiting for ever.
    """

    def __init__(self, root: tk.Tk, window: WizardWindow,
                 actions: Sequence[Callable[[], None]]) -> None:
        """Schedule the first action and keep the rest for later prompts."""
        self._root = root
        self._window = window
        self._left = list(actions)
        root.after(PROMPT_TIMEOUT_MS, self._give_up)
        self._schedule()

    def _schedule(self) -> None:
        """Let the next action run inside the next prompt's wait loop."""
        if self._left:
            self._root.after(0, self._run_next)

    def _run_next(self) -> None:
        """Run one action, leaving the rest for the prompts after it."""
        self._schedule()
        self._left.pop(0)()

    def _give_up(self) -> None:
        """Abandon a prompt no action answered, ending the nested loop."""
        abort_prompt(self._window)


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
