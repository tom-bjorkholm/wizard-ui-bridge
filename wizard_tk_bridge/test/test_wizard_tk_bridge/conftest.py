#! /usr/bin/env python3
"""Pytest configuration for wizard_tk_bridge tests.

Every test runs the same way on macOS, Linux and Windows, with one
exception: turning off window restoration is a macOS-only repair and
_ignore_window_state() returns at once on the other systems. Holding
the first Tcl interpreter is done everywhere, so that the tests behave
the same on every system even though only macOS can crash without it.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import ctypes
import ctypes.util
import sys
import tkinter as tk
from typing import Any, Optional
import pytest

SHOWN_WINDOW_MARKERS = ('focus_sensitive', 'visible_window')
NO_RESTORE_KEY = b'ApplePersistenceIgnoreState'
_FIRST_ROOT: list[tk.Tk] = []


class ObjcRuntime:
    """The Objective-C runtime of this process."""

    def __init__(self, library: ctypes.CDLL) -> None:
        """Keep the runtime and declare the two calls used here."""
        self._lib = library
        library.objc_getClass.restype = ctypes.c_void_p
        library.objc_getClass.argtypes = [ctypes.c_char_p]
        library.sel_registerName.restype = ctypes.c_void_p
        library.sel_registerName.argtypes = [ctypes.c_char_p]

    def cls(self, name: bytes) -> Any:
        """Return the class of that name, or nil when it is unknown."""
        return self._lib.objc_getClass(name)

    def send(self, receiver: Any, selector: bytes, *args: Any,
             types: tuple[Any, ...] = ()) -> Any:
        """Send one message and return the reply pointer.

        A message to a nil receiver replies nil, so a class this
        runtime does not know makes the whole chain fall away without
        raising anything.
        """
        signature = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p,
                                     ctypes.c_void_p, *types)
        call = ctypes.cast(self._lib.objc_msgSend, signature)
        return call(receiver, self._lib.sel_registerName(selector), *args)


def _macos_objc_runtime() -> Optional[ObjcRuntime]:
    """Return the macOS Objective-C runtime, or None without one."""
    found = ctypes.util.find_library('objc')
    if found is None:
        return None
    try:
        return ObjcRuntime(ctypes.CDLL(found))
    except (OSError, AttributeError):
        return None


def _ignore_window_state() -> None:
    """Turn window restoration off for this test process on macOS.

    Only macOS restores the windows of an application, so this does
    nothing at all on Linux or Windows and touches no Objective-C
    runtime there.

    macOS remembers that an application died and then asks, in a modal
    alert, whether to reopen the windows it had. Tk raises that alert
    from inside ``tk.Tk()``, where no test can answer it, so one crash
    of the Python application - from this test run or any other - would
    leave every later run hanging in the first root it builds. The
    ``ApplePersistenceIgnoreState`` default turns the alert off and
    sends the saved state to a temporary folder instead. It is put in
    the in-memory registration domain, which lives only as long as this
    process, so nothing on the computer is changed.
    """
    if sys.platform != 'darwin':
        return
    objc = _macos_objc_runtime()
    if objc is None:
        return
    key = objc.send(objc.cls(b'NSString'), b'stringWithUTF8String:',
                    NO_RESTORE_KEY, types=(ctypes.c_char_p,))
    wanted = objc.send(objc.cls(b'NSNumber'), b'numberWithBool:', True,
                       types=(ctypes.c_bool,))
    table = objc.send(objc.cls(b'NSDictionary'),
                      b'dictionaryWithObject:forKey:', wanted, key,
                      types=(ctypes.c_void_p, ctypes.c_void_p))
    store = objc.send(objc.cls(b'NSUserDefaults'), b'standardUserDefaults')
    objc.send(store, b'registerDefaults:', table, types=(ctypes.c_void_p,))


def _hold_first_interpreter() -> None:
    """Build the hidden root that owns this process's first interpreter.

    Tk on macOS hands the first Tcl interpreter of a process to AppKit
    once, and never updates or clears that pointer. A test that destroys
    that interpreter leaves AppKit holding a freed one, and the next
    time macOS validates the application menu - which the accessibility
    service does at moments no test controls - Tk reads through it and
    the process dies of a segmentation fault. One hidden root built
    before any test builds its own, and never destroyed, keeps the
    pointer aimed at a living interpreter for the whole run.

    Only macOS crashes without this, but the root is taken on every
    system, so that a Linux or Windows run exercises what a macOS run
    does. A machine with no display raises TclError here, and then
    every test that needs a display skips as it did before.
    """
    if _FIRST_ROOT:
        return
    _ignore_window_state()
    try:
        root = tk.Tk()
    except tk.TclError:
        return
    root.withdraw()
    _FIRST_ROOT.append(root)


def pytest_configure(config: pytest.Config) -> None:
    """Register custom markers and hold the first Tcl interpreter.

    The interpreter is taken here, and not in a fixture, because every
    test of every Tk test package has to find it already taken; pytest
    runs this hook before it runs any test.
    """
    config.addinivalue_line(
        'markers',
        'focus_sensitive: test requires a focused window and unlocked '
        'display; run manually under controlled conditions')
    config.addinivalue_line(
        'markers',
        'visible_window: test needs its window really shown on the '
        'screen, so its windows are not kept hidden')
    _hold_first_interpreter()


@pytest.fixture(scope='session')
def first_root() -> tk.Tk:
    """Return the root holding this process's first Tcl interpreter."""
    if not _FIRST_ROOT:
        pytest.skip('no display available')
    return _FIRST_ROOT[0]


class HiddenToplevel(tk.Toplevel):
    """A top-level window that never reaches the screen.

    Tk maps a new top-level window as soon as the event loop runs, and
    the window system removes a window again only while that loop keeps
    running, which a test does not do after destroying its root. Windows
    a test shows are therefore left painted on the desktop for the rest
    of the pytest process. Tests that do not check what is on the screen
    build their windows through this class instead, which keeps them
    withdrawn from the start so nothing is ever mapped.
    """

    def __init__(self, master: Optional[tk.Misc] = None) -> None:
        """Build the window as usual but keep it off the screen."""
        super().__init__(master)
        self.withdraw()

    def deiconify(self) -> None:
        """Ignore a request to show the window, keeping it hidden."""


def _needs_shown_window(node: pytest.Item) -> bool:
    """Return whether the test asked for a window on the screen."""
    return any(node.get_closest_marker(name) is not None
               for name in SHOWN_WINDOW_MARKERS)


@pytest.fixture(autouse=True)
def hidden_windows(request: pytest.FixtureRequest,
                   monkeypatch: pytest.MonkeyPatch) -> None:
    """Keep the windows a test builds off the screen.

    A test marked focus_sensitive or visible_window needs a window that
    is really shown and keeps the normal Tkinter behaviour; gui_root()
    takes such windows off the screen again when the test ends.
    """
    if _needs_shown_window(request.node):
        return
    monkeypatch.setattr(tk, 'Toplevel', HiddenToplevel)
