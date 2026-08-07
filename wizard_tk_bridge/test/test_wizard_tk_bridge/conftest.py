#! /usr/bin/env python3
"""Pytest configuration for wizard_tk_bridge tests."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter as tk
from typing import Optional
import pytest

SHOWN_WINDOW_MARKERS = ('focus_sensitive', 'visible_window')


def pytest_configure(config: pytest.Config) -> None:
    """Register custom pytest markers for wizard_tk_bridge tests."""
    config.addinivalue_line(
        'markers',
        'focus_sensitive: test requires a focused window and unlocked '
        'display; run manually under controlled conditions')
    config.addinivalue_line(
        'markers',
        'visible_window: test needs its window really shown on the '
        'screen, so its windows are not kept hidden')


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
