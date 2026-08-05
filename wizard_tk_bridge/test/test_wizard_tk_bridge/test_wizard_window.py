#! /usr/local/bin/python3
"""Tests for the Tk host that asks every wizard prompt in turn."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter as tk
import pytest
from wizard_tk_bridge import wizard_window
from wizard_tk_bridge.wizard_window import WizardWindow
from .gui_test_helpers import CloseSpy, gui_root


def test_choice_list_shown() -> None:
    """Test the choice list is packed and holds every choice.

    This guards against a regression where the single-selection list was
    built but never added to the window, so it stayed invisible.
    """
    with gui_root() as root:
        window = WizardWindow(tk.Frame(root))
        # pylint: disable-next=protected-access
        listbox = window._choice_list(['a', 'b', 'c'], None, 'browse')
        assert listbox.size() == 3
        assert listbox.winfo_manager() == 'pack'
        window.close()


def test_window_resizable() -> None:
    """Test the wizard window can be enlarged for large table questions."""
    with gui_root() as root:
        window = WizardWindow(tk.Frame(root))
        # pylint: disable-next=protected-access
        assert window._win is not None and window._win.resizable() == (1, 1)
        window.close()


def test_buttons_at_bottom() -> None:
    """Test the wizard button row is anchored to the content bottom."""
    with gui_root() as root:
        window = WizardWindow(tk.Frame(root))
        # pylint: disable-next=protected-access
        window._add_buttons(lambda: None)
        # pylint: disable-next=protected-access
        button_bar = window._content.winfo_children()[-1]
        assert isinstance(button_bar, tk.Frame)
        assert button_bar.pack_info()['side'] == 'bottom'
        window.close()


def test_pick_one() -> None:
    """Test picking a single choice finishes with its value."""
    with gui_root() as root:
        window = WizardWindow(tk.Frame(root))
        # pylint: disable-next=protected-access
        listbox = tk.Listbox(window._content)
        listbox.insert('end', 'a')
        listbox.insert('end', 'b')
        listbox.selection_set(1)
        # pylint: disable-next=protected-access
        window._pick_one(listbox, ['a', 'b'])
        # pylint: disable-next=protected-access
        assert window._result == 'b'
        window.close()


def test_pick_many() -> None:
    """Test picking several choices finishes with the values in order."""
    with gui_root() as root:
        window = WizardWindow(tk.Frame(root))
        # pylint: disable-next=protected-access
        listbox = tk.Listbox(window._content, selectmode='multiple')
        for choice in ('a', 'b', 'c'):
            listbox.insert('end', choice)
        listbox.selection_set(0)
        listbox.selection_set(2)
        # pylint: disable-next=protected-access
        window._pick_many(listbox, ['a', 'b', 'c'])
        # pylint: disable-next=protected-access
        assert window._result == ['a', 'c']
        window.close()


def test_pick_one_none() -> None:
    """Test confirming a single choice with no selection picks nothing."""
    with gui_root() as root:
        window = WizardWindow(tk.Frame(root))
        # pylint: disable-next=protected-access
        listbox = tk.Listbox(window._content)
        listbox.insert('end', 'a')
        # pylint: disable-next=protected-access
        window._pick_one(listbox, ['a'])
        # pylint: disable-next=protected-access
        assert window._result == ''
        window.close()


def test_choice_preselect() -> None:
    """Test a default choice is preselected in the single-choice list.

    A string default marks one row, while a sequence default marks each
    of its rows, so the list opens with the configured values selected.
    """
    with gui_root() as root:
        window = WizardWindow(tk.Frame(root))
        # pylint: disable-next=protected-access
        listbox = window._choice_list(['a', 'b', 'c'], 'b', 'browse')
        selected = listbox.curselection()  # type: ignore[no-untyped-call]
        assert list(selected) == [1]
        # pylint: disable-next=protected-access
        assert WizardWindow._preset_indexes(['a', 'b', 'c'],
                                            ['a', 'c']) == [0, 2]
        window.close()


def test_text_sensitive() -> None:
    """Test a sensitive question masks the entry text."""
    with gui_root() as root:
        window = WizardWindow(tk.Frame(root))
        # pylint: disable-next=protected-access
        root.after(0, lambda: window._finish('secret'))
        result = window.ask_text('PW?', None, False, sensitive=True)
        assert result == 'secret'
        # pylint: disable-next=protected-access
        entries = [w for w in window._content.winfo_children()
                   if isinstance(w, tk.Entry)]
        assert entries and entries[0].cget('show') == '*'
        window.close()


def test_text_default() -> None:
    """Test an empty answer falls back to the pre-filled default."""
    with gui_root() as root:
        window = WizardWindow(tk.Frame(root))
        # pylint: disable-next=protected-access
        root.after(0, lambda: window._finish(''))
        assert window.ask_text('Name?', None, False, default='D') == 'D'
        window.close()


def test_binds_cancel(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the wizard window binds Cmd-W to its cancel action."""
    spy = CloseSpy()
    monkeypatch.setattr(wizard_window, 'bind_close', spy)
    with gui_root() as root:
        window = WizardWindow(tk.Frame(root))
        # pylint: disable-next=protected-access
        assert spy.calls == [(window._win, window._cancel)]
        window.close()


def test_text_binds_return() -> None:
    """Test the text entry itself, not the window, binds Return to submit.

    Binding on the entry rather than the window means the key only
    submits while that entry has the keyboard focus, instead of stealing
    Return from a differently focused button.
    """
    with gui_root() as root:
        window = WizardWindow(tk.Frame(root))
        # pylint: disable-next=protected-access
        root.after(0, lambda: window._finish('typed'))
        result = window.ask_text('Name?', None, False)
        assert result == 'typed'
        # pylint: disable-next=protected-access
        entries = [w for w in window._content.winfo_children()
                   if isinstance(w, tk.Entry)]
        assert entries and entries[0].bind('<Return>') != ''
        window.close()


def test_parent_area_excl() -> None:
    """Test giving neither or both of parent and area is rejected."""
    with pytest.raises(ValueError):
        WizardWindow()
    with gui_root() as root:
        with pytest.raises(ValueError):
            WizardWindow(root, tk.Frame(root))


def test_area_no_toplevel() -> None:
    """Test an embedded wizard builds its widgets into the given area.

    No Toplevel of its own is created, and closing removes the message
    area and the content frame but leaves the caller's area intact.
    """
    with gui_root() as root:
        area = tk.Frame(root)
        before = set(root.winfo_children())
        window = WizardWindow(area=area, modal=False)
        # pylint: disable-next=protected-access
        assert window._win is None
        assert set(root.winfo_children()) == before
        assert area.winfo_children()
        window.close()
        assert not area.winfo_children()
        assert area.winfo_exists()


def test_area_modal_off() -> None:
    """Test an embedded, non-modal wizard never grabs the area's window."""
    with gui_root() as root:
        root.deiconify()
        area = tk.Frame(root)
        area.pack()
        window = WizardWindow(area=area, modal=False)
        root.update()
        assert root.grab_current() is None  # type: ignore[no-untyped-call]
        window.close()


def test_area_modal_on_grabs() -> None:
    """Test an embedded, modal wizard grabs the area's own top-level."""
    with gui_root() as root:
        root.deiconify()
        area = tk.Frame(root)
        area.pack()
        window = WizardWindow(area=area, modal=True)
        root.update()
        assert root.grab_current() is root  # type: ignore[no-untyped-call]
        window.close()
        root.update()
        assert root.grab_current() is None


def test_parent_modal_off() -> None:
    """Test a non-modal own window never grabs its parent."""
    with gui_root() as root:
        root.deiconify()
        window = WizardWindow(tk.Frame(root), modal=False)
        root.update()
        assert root.grab_current() is None  # type: ignore[no-untyped-call]
        window.close()
