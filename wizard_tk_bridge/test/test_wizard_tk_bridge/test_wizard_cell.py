#! /usr/local/bin/python3
"""Tests for the input of one form field or matrix cell, and its helpers."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter as tk
from tkinter import ttk
from datetime import date
from pathlib import Path
from typing import Optional
import pytest
from wizard_ui_bridge import AskCell, PathAskOptions, PrefillValueType, \
    AskLabelCell, AskTextCell, AskIntCell, AskPathCell, AskYesNoCell, \
    AskChoiceCell, AskMultiChoiceCell, AskFloatCell, AskDateCell
from wizard_ui_bridge.bridge_helpers import INT_ERROR as _INT_ERROR, \
    int_text, multi_count_error, out_of_range, range_error, text_answer
from wizard_tk_bridge.wizard_cell import CellInput, HelpTooltip, \
    build_input, int_answer, scrolled_editor, tooltip_text, _inside, \
    _set_combo, _set_entry_text, _set_multi
from .gui_test_helpers import find_widgets, gui_root, set_entry


@pytest.mark.parametrize('text, expected', [
    ('5', 5), ('-3', -3), ('x', None), ('', None), ('1.5', None)])
def test_int_text(text: str, expected: Optional[int]) -> None:
    """Test int_text parses a whole number or reports None."""
    assert int_text(text) == expected


@pytest.mark.parametrize('value, lo, hi, expected', [
    (5, 1, 10, False), (0, 1, 10, True), (11, 1, 10, True),
    (5, None, None, False), (5, None, 4, True), (5, 6, None, True)])
def test_out_of_range(value: int, lo: Optional[int], hi: Optional[int],
                      expected: bool) -> None:
    """Test out_of_range respects each inclusive bound."""
    assert out_of_range(value, lo, hi) is expected


@pytest.mark.parametrize('lo, hi, needle', [
    (None, 5, 'at most 5'), (1, None, 'at least 1'),
    (1, 5, 'between 1 and 5')])
def test_range_error(lo: Optional[int], hi: Optional[int],
                     needle: str) -> None:
    """Test the range error names the bounds that apply."""
    assert needle in range_error(lo, hi)


@pytest.mark.parametrize('lo, hi, needle', [
    (2, None, 'at least 2'), (3, 3, 'exactly 3'), (1, 4, 'between 1 and 4')])
def test_multi_count_error(lo: int, hi: Optional[int], needle: str) -> None:
    """Test the multi-select count error names the allowed range."""
    assert needle in multi_count_error(lo, hi)


@pytest.mark.parametrize('text, nullable, default, expected', [
    ('hi', False, None, 'hi'), ('', True, None, None), ('', False, None, ''),
    ('', False, 'd', 'd'), ('', True, 'd', 'd')])
def test_text_answer(text: str, nullable: bool, default: Optional[str],
                     expected: Optional[str]) -> None:
    """Test the default and nullable rules for a text answer."""
    assert text_answer(text, nullable, default) == expected


@pytest.mark.parametrize('text, nullable, lo, hi, default, expected', [
    ('5', False, 1, 10, None, (True, 5, None)),
    ('', False, None, None, 3, (True, 3, None)),
    ('', True, None, None, None, (True, None, None)),
    ('', False, None, None, None, (False, None, _INT_ERROR)),
    ('x', False, None, None, None, (False, None, _INT_ERROR)),
    ('20', False, 1, 10, None,
     (False, None, 'Please enter an integer between 1 and 10.'))])
# pylint: disable-next=too-many-arguments,too-many-positional-arguments
def test_int_answer(text: str, nullable: bool, lo: Optional[int],
                    hi: Optional[int], default: Optional[int],
                    expected: tuple[bool, Optional[int], Optional[str]]
                    ) -> None:
    """Test int_answer reports its value or a re-ask reason."""
    assert int_answer(text, nullable, lo, hi, default) == expected


def _bubbles(anchor: tk.Widget) -> list[tk.Label]:
    """Return the tooltip labels placed over the anchor's own window."""
    host = anchor.winfo_toplevel()
    return [child for child in host.winfo_children()
            if isinstance(child, tk.Label) and child.place_info()]


def test_tooltip_show_hide() -> None:
    """Test showing then hiding a tooltip creates and removes its bubble."""
    with gui_root() as root:
        anchor = tk.Label(root, text='x')
        tip = HelpTooltip('help me', anchor, (anchor,))
        tip.show()
        assert len(_bubbles(anchor)) == 1
        tip.hide()
        assert not _bubbles(anchor)


def test_tooltip_show_twice() -> None:
    """Test showing an already-shown tooltip keeps a single bubble."""
    with gui_root() as root:
        anchor = tk.Label(root, text='x')
        tip = HelpTooltip('help me', anchor, (anchor,))
        tip.show()
        tip.show()
        assert len(_bubbles(anchor)) == 1
        tip.hide()


def test_tooltip_hide_none() -> None:
    """Test hiding a tooltip that was never shown does nothing."""
    with gui_root() as root:
        anchor = tk.Label(root, text='x')
        tip = HelpTooltip('help me', anchor, (anchor,))
        tip.hide()
        assert not _bubbles(anchor)


def test_tooltip_on_destroy() -> None:
    """Test a shown bubble goes away when its bound widget is destroyed."""
    with gui_root() as root:
        anchor = tk.Label(root, text='x')
        anchor.pack()
        tip = HelpTooltip('help me', anchor, (anchor,))
        tip.show()
        assert len(_bubbles(anchor)) == 1
        holder = tk.Label(root, text='y')
        holder.pack()
        anchor.destroy()
        assert not _bubbles(holder)


@pytest.mark.parametrize('start, size, limit, expected', [
    (10, 50, 200, 10), (180, 50, 200, 150), (-5, 50, 200, 0),
    (10, 300, 200, 0), (150, 50, 200, 150)])
def test_inside(start: int, size: int, limit: int, expected: int) -> None:
    """Test a bubble coordinate is moved back inside the window."""
    assert _inside(start, size, limit) == expected


def test_tooltip_inside() -> None:
    """Test a bubble under the last row still starts inside the window."""
    with gui_root() as root:
        root.geometry('200x80')
        root.update()
        anchor = tk.Label(root, text='a rather wide label text here')
        anchor.pack(side='bottom')
        root.update()
        tip = HelpTooltip('a help text wider than the window', anchor,
                          (anchor,))
        tip.show()
        bubble = _bubbles(anchor)[0]
        assert int(bubble.place_info()['x']) == 0
        assert 0 <= int(bubble.place_info()['y']) <= 80


def test_set_entry_helper() -> None:
    """Test the entry setter writes into a disabled entry and skips no-ops."""
    with gui_root() as root:
        entry = tk.Entry(root)
        _set_entry_text(entry, 'a')
        assert entry.get() == 'a'
        entry.configure(state='disabled')
        _set_entry_text(entry, 'b')
        assert entry.get() == 'b'
        assert str(entry.cget('state')) == 'disabled'
        _set_entry_text(entry, 'b')
        assert entry.get() == 'b'


def test_set_combo_helper() -> None:
    """Test the combo setter sets a value, keeps read-only, skips no-ops."""
    with gui_root() as root:
        box = ttk.Combobox(root, values=['x', 'y'], state='readonly')
        _set_combo(box, 'x')
        assert box.get() == 'x' and str(box.cget('state')) == 'readonly'
        _set_combo(box, 'x')
        assert box.get() == 'x'
        _set_combo(box, 'y')
        assert box.get() == 'y'


def test_set_multi_helper() -> None:
    """Test the multi setter selects the wanted members and clears the rest.

    A stale selection is cleared, then the wanted members are selected and
    the others are left unselected.
    """
    with gui_root() as root:
        box = tk.Listbox(root, selectmode='multiple')
        for choice in ('a', 'b', 'c'):
            box.insert('end', choice)
        box.selection_set(1)
        _set_multi(box, ('a', 'b', 'c'), ['a', 'c'])
        picks = box.curselection()  # type: ignore[no-untyped-call]
        assert [int(index) for index in picks] == [0, 2]


def _input(root: tk.Tk, cell: AskCell) -> tuple[CellInput, list[int]]:
    """Build the input of a cell, counting the change calls it makes."""
    changes: list[int] = []
    built = build_input(tk.Frame(root), cell, lambda: changes.append(1))
    return built, changes


@pytest.mark.parametrize('cell, value', [
    (AskTextCell(None, default='Bob'), 'Bob'),
    (AskTextCell(None, nullable=True), None),
    (AskIntCell(None, default=8), 8),
    (AskYesNoCell(None, default=True), True),
    (AskChoiceCell(None, choices=('a', 'b'), default='b'), 'b'),
    (AskMultiChoiceCell(None, choices=('a', 'b'), default=('a',)), ['a']),
    (AskFloatCell(None, default=1.5), 1.5),
    (AskDateCell(None, default=date(2027, 1, 1)), date(2027, 1, 1))])
def test_cell_default_value(cell: AskCell,
                            value: Optional[PrefillValueType]) -> None:
    """Test a cell input starts from the cell's default and is valid."""
    with gui_root() as root:
        built, _ = _input(root, cell)
        assert built.value() == value
        assert built.error() is None


@pytest.mark.parametrize('cell, value', [
    (AskTextCell(None), 'Ann'), (AskIntCell(None), 7),
    (AskPathCell(None, PathAskOptions()), Path('/x/y')),
    (AskYesNoCell(None, default=False), True),
    (AskChoiceCell(None, choices=('a', 'b')), 'a'),
    (AskMultiChoiceCell(None, choices=('a', 'b', 'c')), ['a', 'c']),
    (AskFloatCell(None), 2.5), (AskDateCell(None), date(2027, 2, 3))])
def test_cell_write_value(cell: AskCell, value: PrefillValueType) -> None:
    """Test a value written into a cell input is read back unchanged."""
    with gui_root() as root:
        built, _ = _input(root, cell)
        built.write(value)
        assert built.value() == value


def test_cell_int_error() -> None:
    """Test an out-of-range integer cell reports the range and no value."""
    with gui_root() as root:
        built, _ = _input(root, AskIntCell(None, min_value=0, max_value=24))
        assert isinstance(built.widget, tk.Entry)
        set_entry(built.widget, '25')
        assert built.value() == 25
        assert built.error() == range_error(0, 24)
        set_entry(built.widget, 'x')
        assert built.value() is None
        assert built.error() == _INT_ERROR


def test_cell_choice_required() -> None:
    """Test a choice cell with no default needs a choice to be valid."""
    with gui_root() as root:
        built, _ = _input(root, AskChoiceCell(None, choices=('a', 'b')))
        assert built.value() is None
        assert built.error() == 'Please choose a value.'


def test_cell_change_call() -> None:
    """Test changing a check box cell calls the change callback.

    A check box is changed through its own command, which, unlike a key
    press, needs no shown and focused window.
    """
    with gui_root() as root:
        built, changes = _input(root, AskYesNoCell(None, default=False))
        find_widgets(root, tk.Checkbutton)[0].invoke()
        assert changes == [1]
        assert built.value() is True


@pytest.mark.parametrize('cell, enabled_state', [
    (AskIntCell(None), 'normal'),
    (AskChoiceCell(None, choices=('a',)), 'readonly')])
def test_cell_set_enabled(cell: AskCell, enabled_state: str) -> None:
    """Test disabling and enabling an input, keeping a drop-down read-only."""
    with gui_root() as root:
        built, _ = _input(root, cell)
        built.set_enabled(False)
        assert str(built.widget.cget('state')) == 'disabled'
        built.set_enabled(True)
        assert str(built.widget.cget('state')) == enabled_state


def test_cell_typed_enabled() -> None:
    """Test disabling a typed cell disables its placeholder entry."""
    with gui_root() as root:
        built, _ = _input(root, AskFloatCell(None))
        built.set_enabled(False)
        entry = find_widgets(built.widget.master, tk.Entry)[0]
        assert str(entry.cget('state')) == 'disabled'


@pytest.mark.parametrize('cell, expected', [
    (AskTextCell('Help.'), 'Help.'), (AskTextCell(None), None),
    (AskFloatCell(None), 'Enter a number.'),
    (AskFloatCell('Help.'), 'Help.\nEnter a number.'),
    (AskLabelCell('Name'), None),
    (AskLabelCell('Name', help_text='Who.'), 'Who.')])
def test_tooltip_text(cell: AskCell, expected: Optional[str]) -> None:
    """Test the tooltip text joins any help text and any format hint."""
    assert tooltip_text(cell) == expected


@pytest.mark.parametrize('sideways, orients', [
    (False, ['vertical']), (True, ['vertical', 'horizontal'])])
def test_scrolled_editor(sideways: bool, orients: list[str]) -> None:
    """Test the editor area scrolls sideways only when asked to."""
    with gui_root() as root:
        parent = tk.Frame(root)
        grid, status = scrolled_editor(parent, sideways)
        scrollbars = find_widgets(parent, ttk.Scrollbar)
        assert [str(scrollbar.cget('orient'))
                for scrollbar in scrollbars] == orients
        assert isinstance(grid, tk.Frame)
        assert str(status.cget('text')) == ''
