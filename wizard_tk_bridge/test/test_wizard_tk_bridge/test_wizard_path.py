#! /usr/local/bin/python3
"""Tests for the Tk-specific parts of the wizard bridge's path picking.

Validating a path answer itself is
wizard_ui_bridge.bridge_helpers.path_answer(), already exercised by
wizard_ui_bridge's own test suite; the tests here cover only what this
module adds on top of it: the native picker and the editable path row.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import pytest
from wizard_ui_bridge import PathAskOptions, WizardPathKind
from wizard_tk_bridge.wizard_path import PathRow, pick_path, _start_location
from .gui_test_helpers import gui_root


def test_start_loc_seed() -> None:
    """Test the initial directory and file come from the seed text."""
    assert _start_location('/a/b/c.csv', None) == ('/a/b', 'c.csv')


def test_start_loc_default() -> None:
    """Test the default path seeds the location when no text is given."""
    assert _start_location('', Path('/a/b')) == ('/a', 'b')


def test_start_loc_empty() -> None:
    """Test an empty seed and no default give an empty location."""
    assert _start_location('', None) == ('', '')


PICKERS: list[tuple[WizardPathKind, str]] = [
    (WizardPathKind.EXISTING_FILE, 'askopenfilename'),
    (WizardPathKind.FILE, 'asksaveasfilename'),
    (WizardPathKind.NON_EXISTING_FILE, 'asksaveasfilename'),
    (WizardPathKind.EXISTING_DIR, 'askdirectory'),
    (WizardPathKind.NON_EXISTING_DIR, 'askdirectory'),
    (WizardPathKind.DIR, 'askdirectory')]
"""Each path kind paired with the native dialog its picker opens."""


@pytest.mark.parametrize('kind, dialog', PICKERS)
def test_pick_path(monkeypatch: pytest.MonkeyPatch, kind: WizardPathKind,
                   dialog: str) -> None:
    """Test the picker opens the dialog matching the path kind."""
    target = f'wizard_tk_bridge.wizard_path.filedialog.{dialog}'
    with gui_root() as root:
        monkeypatch.setattr(target, lambda **kw: 'chosen')
        options = PathAskOptions(kind=kind)
        assert pick_path(root, options, '') == 'chosen'
        monkeypatch.setattr(target, lambda **kw: '')
        assert pick_path(root, options, '') is None


def test_path_row_get() -> None:
    """Test a path row returns its pre-filled text."""
    with gui_root() as root:
        row = PathRow(root, PathAskOptions(), '/seed')
        assert row.get() == '/seed'


def test_path_row_set_text() -> None:
    """Test set_text rewrites, clears on empty, and skips an equal value."""
    with gui_root() as root:
        row = PathRow(root, PathAskOptions(), '/seed')
        row.set_text('/seed')
        assert row.get() == '/seed'
        row.set_text('/new')
        assert row.get() == '/new'
        row.set_text('')
        assert row.get() == ''


def test_set_text_disabled() -> None:
    """Test set_text writes into a disabled entry and keeps it disabled."""
    with gui_root() as root:
        row = PathRow(root, PathAskOptions(), '')
        row.set_enabled(False)
        row.set_text('/x')
        assert row.get() == '/x'
        # pylint: disable-next=protected-access
        assert str(row._entry.cget('state')) == 'disabled'


def test_path_row_disable() -> None:
    """Test disabling a path row disables its entry and button."""
    with gui_root() as root:
        row = PathRow(root, PathAskOptions(), '')
        row.set_enabled(False)
        # pylint: disable-next=protected-access
        assert str(row._entry.cget('state')) == 'disabled'
        # pylint: disable-next=protected-access
        assert str(row._button.cget('state')) == 'disabled'
        row.set_enabled(True)
        # pylint: disable-next=protected-access
        assert str(row._entry.cget('state')) == 'normal'


def test_path_row_browse(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test browsing fills the entry and fires the change callback."""
    seen: list[int] = []

    def changed() -> None:
        """Record that the change callback ran."""
        seen.append(1)
    with gui_root() as root:
        monkeypatch.setattr('wizard_tk_bridge.wizard_path.pick_path',
                            lambda *a: '/picked')
        row = PathRow(root, PathAskOptions(), '', changed)
        # pylint: disable-next=protected-access
        row._browse()
        assert row.get() == '/picked'
        assert seen == [1]


def test_path_row_cancel(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test cancelling the picker keeps the existing text unchanged."""
    with gui_root() as root:
        monkeypatch.setattr('wizard_tk_bridge.wizard_path.pick_path',
                            lambda *a: None)
        row = PathRow(root, PathAskOptions(), 'keep')
        # pylint: disable-next=protected-access
        row._browse()
        assert row.get() == 'keep'


def test_browse_no_change(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test browsing without a change callback still fills the entry."""
    with gui_root() as root:
        monkeypatch.setattr('wizard_tk_bridge.wizard_path.pick_path',
                            lambda *a: '/picked')
        row = PathRow(root, PathAskOptions(), '')
        # pylint: disable-next=protected-access
        row._browse()
        assert row.get() == '/picked'


def test_path_row_bind_return() -> None:
    """Test bind_return registers a Return-key binding on the entry."""
    with gui_root() as root:
        row = PathRow(root, PathAskOptions(), '')
        row.bind_return(lambda: None)
        # pylint: disable-next=protected-access
        assert row._entry.bind('<Return>') != ''
