#! /usr/bin/env python3
"""Tests that the test process keeps its first Tcl interpreter."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import sys
import tkinter as tk
from typing import Optional
import pytest
from . import conftest
from .gui_test_helpers import gui_root


def test_first_root_survives(first_root: tk.Tk) -> None:
    """Test a root built by a test is never the first interpreter.

    Tk on macOS gives the first Tcl interpreter of a process to AppKit
    once and never updates that pointer, so a destroyed first
    interpreter makes AppKit read freed memory when it next validates
    the application menu. Every root a test builds and destroys must
    therefore be a later interpreter, leaving the first one alive.
    """
    held = first_root.tk.interpaddr()
    with gui_root() as root:
        assert root.tk.interpaddr() != held
    assert first_root.winfo_exists()
    assert first_root.tk.interpaddr() == held


@pytest.mark.parametrize('platform', ['linux', 'win32'])
def test_no_objc_off_macos(monkeypatch: pytest.MonkeyPatch,
                           platform: str) -> None:
    """Test no Objective-C runtime is reached off macOS.

    Turning window restoration off is the one repair of this test
    package that only macOS needs, and only macOS can carry out. This
    pins it to macOS, so that a Linux or Windows run never reaches the
    Objective-C runtime that the repair is written in.
    """
    def refuse() -> Optional[conftest.ObjcRuntime]:
        """Fail the test when the runtime is asked for anyway."""
        pytest.fail(f'Objective-C runtime asked for on {platform}')

    monkeypatch.setattr(sys, 'platform', platform)
    # pylint: disable-next=protected-access
    monkeypatch.setattr(conftest, '_macos_objc_runtime', refuse)
    # pylint: disable-next=protected-access
    conftest._ignore_window_state()
