#! /usr/local/bin/python3
"""Tests for answering each kind of prompt of the Tk wizard window.

Every test here answers the prompt the way a user does: it fills in the
widgets the prompt built and presses its real buttons, so the commands
behind OK, Add row and the navigation buttons are exercised too.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter as tk
from pathlib import Path
from typing import Callable, Optional
import pytest
from wizard_ui_bridge import PathAskOptions, TableCell, TableColumn, \
    WizardAbort, WizardBack, WizardCancelLevel, WizardNavigation, \
    WizardPathKind
from wizard_ui_bridge.bridge_helpers import INT_ERROR
from wizard_tk_bridge.wizard_window import WizardWindow
from .gui_test_helpers import PromptDriver, answer_entry, answer_list, \
    click_button, content_of, find_widgets, first_entry, gui_root, \
    label_texts, prompt_window, set_entry


def _seen_answer(window: WizardWindow, seen: list[str], text: str) -> None:
    """Record what the entry already held, then answer with text."""
    seen.append(first_entry(window).get())
    answer_entry(window, text)


def _buttons_of(window: WizardWindow) -> dict[str, tk.Button]:
    """Return the prompt's buttons by their label text."""
    return {str(button.cget('text')): button
            for button in find_widgets(content_of(window), tk.Button)}


def _own_window(window: WizardWindow) -> tk.Toplevel:
    """Return the top-level window the wizard built for itself."""
    # pylint: disable-next=protected-access
    win = window._win
    assert win is not None
    return win


def _grab_method(window: WizardWindow) -> Callable[[], None]:
    """Return the wizard's grab method, which a retry is to reuse."""
    # pylint: disable-next=protected-access
    return window._grab


@pytest.mark.parametrize('typed, nullable, default, expected', [
    ('Ada', False, None, 'Ada'), ('Ada', True, 'Bob', 'Ada'),
    ('', False, None, ''), ('', True, None, None), ('', False, 'Bob', 'Bob'),
    ('', True, 'Bob', 'Bob')])
def test_text_rules(typed: str, nullable: bool, default: Optional[str],
                    expected: Optional[str]) -> None:
    """Test an answered text question follows the default and null rules.

    An emptied entry falls back to the default, is None when the question
    is nullable, and is the empty string when it is neither.
    """
    with prompt_window() as (root, window):
        PromptDriver(root, window, [lambda: answer_entry(window, typed)])
        answer = window.ask_text('Name?', None, nullable, default)
        assert answer == expected


def test_re_ask_shows_reason() -> None:
    """Test a re-asked question shows its reason in red above itself."""
    with prompt_window() as (root, window):
        PromptDriver(root, window, [lambda: answer_entry(window, 'Ada')])
        assert window.ask_text('Name?', 'Too short.', False) == 'Ada'
        content = content_of(window)
        assert label_texts(content) == ['Too short.', 'Name?']
        assert str(find_widgets(content, tk.Label)[0].cget('fg')) == 'red'


def test_second_prompt_clears() -> None:
    """Test the next question replaces the previous question's widgets."""
    with prompt_window() as (root, window):
        PromptDriver(root, window, [lambda: answer_entry(window, 'one'),
                                    lambda: answer_entry(window, 'two')])
        assert window.ask_text('First?', None, False) == 'one'
        assert window.ask_text('Second?', None, False) == 'two'
        content = content_of(window)
        assert label_texts(content) == ['Second?']
        assert len(find_widgets(content, tk.Entry)) == 1


@pytest.mark.parametrize('typed, nullable, default, expected', [
    ('7', False, None, 7), ('-4', False, None, -4), ('', True, None, None),
    ('', False, 3, 3), ('9', False, 3, 9)])
def test_int_rules(typed: str, nullable: bool, default: Optional[int],
                   expected: Optional[int]) -> None:
    """Test an answered integer question follows the same answer rules."""
    with prompt_window() as (root, window):
        PromptDriver(root, window, [lambda: answer_entry(window, typed)])
        answer = window.ask_int('Age?', None, nullable, None, None, default)
        assert answer == expected


def test_int_re_ask_empty() -> None:
    """Test a question with no default re-asks from an empty entry."""
    with prompt_window() as (root, window):
        seen: list[str] = []
        PromptDriver(root, window, [
            lambda: _seen_answer(window, seen, 'seven'),
            lambda: _seen_answer(window, seen, '7')])
        assert window.ask_int('Age?', None, False, None, None, None) == 7
        assert seen == ['', '']
        assert label_texts(content_of(window)) == [INT_ERROR, 'Age?']


def test_int_re_ask_default() -> None:
    """Test an out-of-range answer is re-asked from the default again."""
    with prompt_window() as (root, window):
        seen: list[str] = []
        PromptDriver(root, window, [lambda: _seen_answer(window, seen, '20'),
                                    lambda: _seen_answer(window, seen, '5')])
        assert window.ask_int('Count?', None, False, 1, 10, 3) == 5
        assert seen == ['3', '3']
        assert label_texts(content_of(window)) == [
            'Please enter an integer between 1 and 10.', 'Count?']


def test_path_answered() -> None:
    """Test a path question with no default starts empty and returns."""
    with prompt_window() as (root, window):
        seen: list[str] = []
        PromptDriver(root, window,
                     [lambda: _seen_answer(window, seen, 'new/file.txt')])
        assert window.ask_path('File?', PathAskOptions(), None) == \
            Path('new/file.txt')
        assert seen == ['']


@pytest.mark.parametrize('typed', ['given/name.txt', ''])
def test_path_default(typed: str) -> None:
    """Test a path question pre-fills its default and falls back to it."""
    with prompt_window() as (root, window):
        options = PathAskOptions(default=Path('given/name.txt'))
        seen: list[str] = []
        PromptDriver(root, window, [lambda: _seen_answer(window, seen, typed)])
        assert window.ask_path('File?', options, None) == options.default
        assert seen == ['given/name.txt']


def test_path_re_ask_keeps(tmp_path: Path) -> None:
    """Test a rejected path is re-asked with the typed text kept."""
    wanted = tmp_path / 'here.txt'
    wanted.write_text('content', encoding='utf-8')
    with prompt_window() as (root, window):
        options = PathAskOptions(kind=WizardPathKind.EXISTING_FILE)
        seen: list[str] = []
        PromptDriver(root, window, [
            lambda: _seen_answer(window, seen, 'no/such/file.txt'),
            lambda: _seen_answer(window, seen, str(wanted))])
        assert window.ask_path('File?', options, None) == wanted
        assert seen == ['', 'no/such/file.txt']
        assert label_texts(content_of(window)) == ['Path does not exist.',
                                                   'File?']


@pytest.mark.parametrize('default, row, expected', [
    (None, 1, 'b'), ('a', 2, 'c')])
def test_choice_selected(default: Optional[str], row: int,
                         expected: str) -> None:
    """Test the row selected when OK is pressed is the returned choice."""
    with prompt_window() as (root, window):
        PromptDriver(root, window, [lambda: answer_list(window, [row])])
        choices = ['a', 'b', 'c']
        assert window.ask_choice('Pick?', choices, default, None) == expected


def test_choice_keeps_default() -> None:
    """Test confirming without touching the list returns the default."""
    with prompt_window() as (root, window):
        PromptDriver(root, window,
                     [lambda: click_button(content_of(window), 'OK')])
        assert window.ask_choice('Pick?', ['a', 'b', 'c'], 'c', None) == 'c'


@pytest.mark.parametrize('rows, expected', [
    ((2, 0), ['a', 'c']), ((), []), ((0, 1, 2), ['a', 'b', 'c'])])
def test_multi_selected(rows: tuple[int, ...], expected: list[str]) -> None:
    """Test the picked choices come back in the order they are listed."""
    with prompt_window() as (root, window):
        PromptDriver(root, window, [lambda: answer_list(window, rows)])
        answer = window.ask_multi('Pick?', ['a', 'b', 'c'], None, 0, None,
                                  None)
        assert answer == expected


@pytest.mark.parametrize('min_select, max_select, first, second, expected,'
                         ' reason', [
                             (2, None, (0,), (0, 1), ['a', 'b'],
                              'Please select at least 2.'),
                             (0, 1, (0, 1), (2,), ['c'],
                              'Please select between 0 and 1.'),
                             (2, 2, (0,), (1, 2), ['b', 'c'],
                              'Please select exactly 2.')])
# pylint: disable-next=too-many-arguments,too-many-positional-arguments
def test_multi_count_re_ask(min_select: int, max_select: Optional[int],
                            first: tuple[int, ...], second: tuple[int, ...],
                            expected: list[str], reason: str) -> None:
    """Test a wrong number of picks is re-asked with the shared message."""
    with prompt_window() as (root, window):
        PromptDriver(root, window, [lambda: answer_list(window, first),
                                    lambda: answer_list(window, second)])
        answer = window.ask_multi('Pick?', ['a', 'b', 'c'], None, min_select,
                                  max_select, None)
        assert answer == expected
        assert label_texts(content_of(window)) == [reason, 'Pick?']


def test_multi_preselects() -> None:
    """Test a default selection is offered and returned untouched."""
    with prompt_window() as (root, window):
        PromptDriver(root, window,
                     [lambda: click_button(content_of(window), 'OK')])
        answer = window.ask_multi('Pick?', ['a', 'b', 'c'], ['a', 'c'], 1,
                                  None, None)
        assert answer == ['a', 'c']


def test_table_filled() -> None:
    """Test a fixed table returns the strings its cells hold."""
    columns = [TableColumn('Name', read_only=True), TableColumn('Value')]
    cells = [[TableCell(value='a'), TableCell(value='1')]]
    with prompt_window() as (root, window):
        PromptDriver(root, window, [lambda: answer_entry(window, '2')])
        rows = window.ask_table(columns, cells, 'Fill?', None, None, None,
                                None)
        assert rows == [['a', '2']]


def _grow_table(window: WizardWindow) -> None:
    """Add two rows, fill and drop one again, then confirm the table."""
    content = content_of(window)
    click_button(content, 'Add row')
    set_entry(find_widgets(content, tk.Entry)[1], 'b')
    click_button(content, 'Add row')
    click_button(content, 'Remove row')
    click_button(content, 'OK')


def test_table_add_and_remove() -> None:
    """Test a variable table grows and shrinks with its own buttons."""
    columns = [TableColumn('Name')]
    cells = [[TableCell(value='a')]]
    with prompt_window() as (root, window):
        PromptDriver(root, window, [lambda: _grow_table(window)])
        rows = window.ask_table(columns, cells, 'Fill?', None, None, 1, 3)
        assert rows == [['a'], ['b']]


@pytest.mark.parametrize('min_rows, max_rows, row_buttons', [
    (None, None, False), (1, None, False), (None, 3, False), (1, 3, True)])
def test_table_row_buttons(min_rows: Optional[int], max_rows: Optional[int],
                           row_buttons: bool) -> None:
    """Test row buttons are offered for a variable table only.

    A table has a variable number of rows only when both a minimum and a
    maximum row count are given; either bound alone leaves it fixed.
    """
    columns = [TableColumn('Name')]
    cells = [[TableCell(value='a')]]
    with prompt_window() as (root, window):
        PromptDriver(root, window,
                     [lambda: click_button(content_of(window), 'OK')])
        window.ask_table(columns, cells, 'Fill?', None, None, min_rows,
                         max_rows)
        buttons = _buttons_of(window)
        assert ('Add row' in buttons) is row_buttons
        assert ('Remove row' in buttons) is row_buttons


@pytest.mark.parametrize('pressed, expected', [('Yes', True), ('No', False)])
def test_yes_no_pressed(pressed: str, expected: bool) -> None:
    """Test each yes/no button answers with the value it stands for."""
    with prompt_window() as (root, window):
        PromptDriver(root, window,
                     [lambda: click_button(content_of(window), pressed)])
        assert window.ask_yes_no('Sure?', True, None) is expected


@pytest.mark.parametrize('default, marked, plain', [
    (True, 'Yes', 'No'), (False, 'No', 'Yes')])
def test_yes_no_default(default: bool, marked: str, plain: str) -> None:
    """Test the default answer's button is the marked default one."""
    with prompt_window() as (root, window):
        PromptDriver(root, window,
                     [lambda: click_button(content_of(window), marked)])
        assert window.ask_yes_no('Sure?', default, None) is default
        buttons = _buttons_of(window)
        assert str(buttons[marked].cget('default')) == 'active'
        assert str(buttons[plain].cget('default')) != 'active'


@pytest.mark.parametrize('label, request_type', [
    ('Back', WizardBack), ('Out one level', WizardCancelLevel),
    ('Abort', WizardAbort)])
def test_nav_raises(label: str, request_type: type[WizardNavigation]) -> None:
    """Test each navigation button raises its own navigation request."""
    with prompt_window() as (root, window):
        PromptDriver(root, window,
                     [lambda: click_button(content_of(window), label)])
        with pytest.raises(request_type):
            window.ask_text('Name?', None, False)


def test_nav_then_answer() -> None:
    """Test a question asked after a navigation request works as usual."""
    with prompt_window() as (root, window):
        PromptDriver(root, window, [
            lambda: click_button(content_of(window), 'Back'),
            lambda: answer_entry(window, 'Ada')])
        with pytest.raises(WizardBack):
            window.ask_text('Name?', None, False)
        assert window.ask_text('Name?', None, False) == 'Ada'


def test_embedded_prompt() -> None:
    """Test an embedded wizard answers a question without a window."""
    with gui_root() as root:
        area = tk.Frame(root)
        window = WizardWindow(area=area, modal=False)
        PromptDriver(root, window, [lambda: answer_entry(window, 'Ada')])
        assert window.ask_text('Name?', None, False) == 'Ada'
        window.close()


def test_close_twice() -> None:
    """Test closing an already closed wizard window does nothing more."""
    with gui_root() as root:
        window = WizardWindow(tk.Frame(root))
        win = _own_window(window)
        window.close()
        window.close()
        assert not win.winfo_exists()


def test_close_window_gone() -> None:
    """Test closing tolerates a window that was destroyed elsewhere."""
    with gui_root() as root:
        window = WizardWindow(tk.Frame(root))
        _own_window(window).destroy()
        window.close()


def test_close_grab_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test closing swallows a Tcl error from releasing the grab."""
    with gui_root() as root:
        window = WizardWindow(tk.Frame(root))
        win = _own_window(window)

        def _boom() -> None:
            """Fail the release as Tk does when the grab is already gone."""
            raise tk.TclError('grab release failed')
        monkeypatch.setattr(win, 'grab_release', _boom)
        window.close()
        assert not win.winfo_exists()


def test_grab_after_close() -> None:
    """Test a retried grab is dropped once the wizard was closed."""
    with gui_root() as root:
        window = WizardWindow(tk.Frame(root))
        window.close()
        _grab_method(window)()


def test_grab_window_gone() -> None:
    """Test a retried grab is dropped once its window is destroyed."""
    with gui_root() as root:
        window = WizardWindow(tk.Frame(root))
        _own_window(window).destroy()
        _grab_method(window)()
        window.close()


def test_grab_retry(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test a not-yet-viewable window reschedules the grab on the loop.

    Tk refuses the grab while the new window is not viewable yet, so the
    wizard retries it on the event loop instead of failing the prompt.
    """
    with gui_root() as root:
        window = WizardWindow(tk.Frame(root))
        scheduled: list[tuple[int, object]] = []

        def _boom() -> None:
            """Refuse the grab as Tk does for a not-yet-viewable window."""
            raise tk.TclError('grab failed: window not viewable')

        def _after(delay: int, callback: object) -> str:
            """Record a rescheduled retry instead of running it."""
            scheduled.append((delay, callback))
            return ''
        win = _own_window(window)
        monkeypatch.setattr(win, 'grab_set', _boom)
        monkeypatch.setattr(win, 'after', _after)
        _grab_method(window)()
        assert scheduled == [(50, _grab_method(window))]
        window.close()
