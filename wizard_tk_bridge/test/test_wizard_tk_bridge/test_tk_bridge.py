#! /usr/local/bin/python3
"""Tests for the Tkinter WizardUiBridge implementation."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from io import StringIO
from pathlib import Path
import tkinter as tk
import pytest
from wizard_ui_bridge import AskFloatField, AskTextField, PathAskOptions, \
    TableCell, TableColumn, WizardPathKind
from wizard_tk_bridge import WizardUiBridgeTk
from wizard_tk_bridge._no_text_io import NoTextIO
from wizard_tk_bridge.wizard_window import WizardWindow
from .gui_test_helpers import answer_entry, answer_list, gui_root


def test_standalone_owns_root(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test a standalone bridge creates and destroys its hidden root."""
    class _Root:
        """Small root fake for the construction-only lifecycle test."""

        def __init__(self) -> None:
            """Start with no lifecycle calls recorded."""
            self.withdrawn = False
            self.destroyed = False

        def withdraw(self) -> None:
            """Record hiding the root."""
            self.withdrawn = True

        def destroy(self) -> None:
            """Record destroying the root."""
            self.destroyed = True

    root = _Root()
    monkeypatch.setattr('wizard_tk_bridge.tk_bridge.tk.Tk', lambda: root)
    bridge = WizardUiBridgeTk()
    assert root.withdrawn
    bridge.close()
    assert root.destroyed


def test_parent_area_excl() -> None:
    """Test giving both parent and area is rejected."""
    with gui_root() as root:
        with pytest.raises(ValueError):
            WizardUiBridgeTk(root, tk.Frame(root))


def test_sensitive_rejected() -> None:
    """Test a sensitive question with a default is rejected up front.

    This is checked before the wizard window is even built, so it never
    opens a window only to raise once the question is asked.
    """
    with gui_root() as root:
        bridge = WizardUiBridgeTk(root)
        with pytest.raises(ValueError):
            bridge.ask_text('Secret?', default='x', sensitive=True)
        bridge.close()


def test_error_file_discard() -> None:
    """Test error_file() with no log given returns a discarding stream."""
    with gui_root() as root:
        bridge = WizardUiBridgeTk(root)
        stream = bridge.error_file()
        assert isinstance(stream, NoTextIO)
        stream.write('should vanish')
        assert stream.getvalue() == ''
        bridge.close()


def test_error_file_given() -> None:
    """Test error_file() returns the log stream given at construction."""
    with gui_root() as root:
        log = StringIO()
        bridge = WizardUiBridgeTk(root, log=log)
        assert bridge.error_file() is log
        bridge.close()


def test_supports_form_field() -> None:
    """Test supports_form_field delegates to the form editor's coverage."""
    with gui_root() as root:
        bridge = WizardUiBridgeTk(root)
        assert bridge.supports_form_field(AskFloatField('n', None)) is True
        bridge.close()


def test_close_without_asking() -> None:
    """Test closing a bridge that never asked anything does nothing."""
    with gui_root() as root:
        bridge = WizardUiBridgeTk(root)
        bridge.close()


def test_show_builds_lazily() -> None:
    """Test show() builds the wizard window on first use and shows there."""
    with gui_root() as root:
        bridge = WizardUiBridgeTk(root)
        bridge.show('hello')
        # pylint: disable-next=protected-access
        window = bridge._window
        assert window is not None
        # pylint: disable-next=protected-access
        assert 'hello' in window._messages.get('1.0', 'end')
        bridge.close()


def _finish_bridge(bridge: WizardUiBridgeTk, value: object) -> None:
    """Answer the bridge's already-built wizard window with value."""
    # pylint: disable-next=protected-access
    window = bridge._window
    assert window is not None
    # pylint: disable-next=protected-access
    window._finish(value)


def test_ask_text_round_trip() -> None:
    """Test ask_text answers through the wizard window and back."""
    with gui_root() as root:
        bridge = WizardUiBridgeTk(root)
        root.after(0, lambda: _finish_bridge(bridge, ''))
        assert bridge.ask_text('Name?', nullable=True) is None
        bridge.close()


def test_embedded_builds() -> None:
    """Test an embedded bridge builds into the given area, not a window."""
    with gui_root() as root:
        area = tk.Frame(root)
        bridge = WizardUiBridgeTk(area=area, modal=False)
        bridge.show('hi')
        assert area.winfo_children()
        bridge.close()
        assert not area.winfo_children()


def test_ask_int_delegates() -> None:
    """Test ask_int reaches the wizard window and returns its answer."""
    with gui_root() as root:
        bridge = WizardUiBridgeTk(root)
        root.after(0, lambda: _finish_bridge(bridge, '5'))
        assert bridge.ask_int('Age?', default=5) == 5
        bridge.close()


def test_ask_yes_no_delegates() -> None:
    """Test ask_yes_no reaches the wizard window and returns its answer."""
    with gui_root() as root:
        bridge = WizardUiBridgeTk(root)
        root.after(0, lambda: _finish_bridge(bridge, True))
        assert bridge.ask_yes_no('OK?', True) is True
        bridge.close()


def _window_of(bridge: WizardUiBridgeTk) -> WizardWindow:
    """Return the wizard window the bridge built for its session."""
    # pylint: disable-next=protected-access
    window = bridge._window
    assert window is not None
    return window


def test_ask_path_no_options() -> None:
    """Test ask_path without options asks for a plain file path."""
    with gui_root() as root:
        bridge = WizardUiBridgeTk(root)
        root.after(0, lambda: answer_entry(_window_of(bridge), 'new.txt'))
        assert bridge.ask_path('File?') == Path('new.txt')
        bridge.close()


def test_ask_path_options(tmp_path: Path) -> None:
    """Test ask_path passes the given options on to the wizard window."""
    wanted = tmp_path / 'here.txt'
    wanted.write_text('content', encoding='utf-8')
    options = PathAskOptions(kind=WizardPathKind.EXISTING_FILE)
    with gui_root() as root:
        bridge = WizardUiBridgeTk(root)
        root.after(0, lambda: answer_entry(_window_of(bridge), str(wanted)))
        assert bridge.ask_path('File?', options=options) == wanted
        bridge.close()


def test_ask_choice_delegates() -> None:
    """Test ask_choice reaches the wizard window and returns its answer."""
    with gui_root() as root:
        bridge = WizardUiBridgeTk(root)
        root.after(0, lambda: answer_list(_window_of(bridge), [1]))
        assert bridge.ask_choice('Pick?', choices=['a', 'b']) == 'b'
        bridge.close()


def test_ask_multi_delegates() -> None:
    """Test ask_multi reaches the wizard window and returns its answer."""
    with gui_root() as root:
        bridge = WizardUiBridgeTk(root)
        root.after(0, lambda: answer_list(_window_of(bridge), [0, 2]))
        answer = bridge.ask_multi('Pick?', choices=['a', 'b', 'c'],
                                  min_select=2)
        assert answer == ['a', 'c']
        bridge.close()


def test_ask_table_delegates() -> None:
    """Test ask_table reaches the wizard window and returns its rows."""
    columns = [TableColumn('Name')]
    cells = [[TableCell(value='a')]]
    with gui_root() as root:
        bridge = WizardUiBridgeTk(root)
        root.after(0, lambda: answer_entry(_window_of(bridge), 'b'))
        assert bridge.ask_table(columns, cells, 'Fill?') == [['b']]
        bridge.close()


def test_window_is_reused() -> None:
    """Test every question of one session is asked in the same window.

    The bridge builds its wizard window once, so a session does not jump
    around the display as it asks its questions.
    """
    with gui_root() as root:
        bridge = WizardUiBridgeTk(root)
        root.after(0, lambda: answer_entry(_window_of(bridge), 'first'))
        assert bridge.ask_text('One?') == 'first'
        window = _window_of(bridge)
        root.after(0, lambda: answer_entry(_window_of(bridge), 'second'))
        assert bridge.ask_text('Two?') == 'second'
        assert _window_of(bridge) is window
        bridge.close()


def test_ask_form_delegates() -> None:
    """Test ask_form builds the whole-form editor and submits its answer."""
    with gui_root() as root:
        bridge = WizardUiBridgeTk(root)
        field = AskTextField('Name', None, default='Bob')

        def _submit() -> None:
            # pylint: disable-next=protected-access
            window = bridge._window
            assert window is not None
            # pylint: disable-next=protected-access
            assert window._form is not None
            # pylint: disable-next=protected-access
            window._form.submit()
        root.after(0, _submit)
        answers = bridge.ask_form('Fill this in', [field])
        assert answers[0].value == 'Bob'
        bridge.close()
