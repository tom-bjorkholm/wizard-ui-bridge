#! /usr/bin/env python3
"""Tests for the wizard_tk_bridge teaching examples."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter as tk
from io import StringIO
from typing import Callable, Iterator, Literal, Optional, Sequence, overload
from contextlib import contextmanager
import pytest
from wizard_ui_example import e08_matrix_form
from wizard_tk_example import e01_cli_wizard, e02_new_window, \
    e03_embedded_area
from wizard_tk_example._shared_wizard import ask_pizza_order
from wizard_ui_bridge import WizardAbort, WizardBack, WizardUiBridge
from wizard_tk_bridge import WizardUiBridgeTk

_WATCHDOG_MS = 5000


# pylint: disable-next=abstract-method
class _FakeBridge(WizardUiBridge):
    """A minimal bridge answering from a fixed script, for logic-only tests."""

    def __init__(self, answers: Sequence[object]) -> None:
        """Store the answers to return in order, one per ask call."""
        self._answers = list(answers)
        self.defaults: list[object] = []

    def _next(self) -> object:
        """Return the next scripted answer, or abort when none are left."""
        if not self._answers:
            raise WizardAbort()
        answer = self._answers.pop(0)
        if isinstance(answer, WizardBack):
            raise answer
        return answer

    # pylint: disable-next=too-many-arguments
    def ask_text(self, question: str, re_ask_reason: Optional[str] = None,
                 nullable: bool = False, *, default: Optional[str] = None,
                 sensitive: bool = False,
                 help_text: Optional[str] = None) -> Optional[str]:
        """Return the next scripted text answer."""
        self.defaults.append(default)
        answer = self._next()
        assert answer is None or isinstance(answer, str)
        return answer

    # pylint: disable=too-many-arguments
    @overload
    def ask_choice(self, question: str, *, choices: Sequence[str],
                   default: Optional[str] = None,
                   re_ask_reason: Optional[str] = None,
                   nullable: Literal[False] = False,
                   help_text: Optional[str] = None) -> str: ...

    @overload
    def ask_choice(self, question: str, *, choices: Sequence[str],
                   default: Optional[str] = None,
                   re_ask_reason: Optional[str] = None, nullable: bool,
                   help_text: Optional[str] = None) -> Optional[str]: ...
    # pylint: enable=too-many-arguments

    # pylint: disable-next=too-many-arguments
    def ask_choice(self, question: str, *, choices: Sequence[str],
                   default: Optional[str] = None,
                   re_ask_reason: Optional[str] = None, nullable: bool = False,
                   help_text: Optional[str] = None) -> Optional[str]:
        """Return the next scripted choice answer."""
        self.defaults.append(default)
        answer = self._next()
        assert answer is None or isinstance(answer, str)
        return answer

    def ask_yes_no(self, question: str, default: bool,
                   re_ask_reason: Optional[str] = None, *,
                   help_text: Optional[str] = None) -> bool:
        """Return the next scripted yes/no answer."""
        self.defaults.append(default)
        answer = self._next()
        assert isinstance(answer, bool)
        return answer

    def show(self, message: str) -> None:
        """Discard a shown message; these tests do not check it."""


def test_pizza_order_summary() -> None:
    """Test a full order is summarized with the name, topping and cheese."""
    bridge = _FakeBridge(['Alice', 'Pepperoni', True])
    assert ask_pizza_order(bridge) == \
        'Alice orders a Pepperoni pizza with extra cheese.'


def test_pizza_order_anon() -> None:
    """Test an empty name falls back to 'Anonymous' and no cheese phrase."""
    bridge = _FakeBridge([None, 'Olive', False])
    assert ask_pizza_order(bridge) == 'Anonymous orders a Olive pizza.'


def test_pizza_order_cancel() -> None:
    """Test a navigation request during the wizard returns None."""
    bridge = _FakeBridge([])
    assert ask_pizza_order(bridge) is None


def test_pizza_back_defaults() -> None:
    """Test Back revisits a question and keeps its later answer default."""
    bridge = _FakeBridge(['Alice', 'Pepperoni', WizardBack(), 'Olive', True])
    assert ask_pizza_order(bridge) == \
        'Alice orders a Olive pizza with extra cheese.'
    assert bridge.defaults == [None, None, False, 'Pepperoni', False]


@contextmanager
def _gui_root() -> Iterator[tk.Tk]:
    """Yield a withdrawn Tk root, skipping the test with no display.

    The root stays withdrawn and these tests build no window of their
    own, so nothing of this test package ever reaches the screen. The
    bridge tests need more than this on teardown and have their own
    gui_root in test_wizard_tk_bridge.gui_test_helpers; the two test
    packages are built and analyzed as separate roots, so neither
    imports across that boundary.
    """
    # pylint: disable=duplicate-code
    try:
        root = tk.Tk()
    except tk.TclError:
        pytest.skip('no display available')
    root.withdraw()
    try:
        yield root
    finally:
        root.destroy()
# pylint: enable=duplicate-code


def test_cli_wizard_plumbing(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test run_cli_wizard owns and closes its bridge.

    ask_pizza_order itself is exercised directly by the fake-bridge tests
    above; this test instead checks the standalone lifecycle around it.
    """
    class _Bridge:
        """Record that the standalone example closes its bridge."""

        def __init__(self) -> None:
            """Start with no close call."""
            self.closed = False

        def close(self) -> None:
            """Record the cleanup call."""
            self.closed = True

        def is_closed(self) -> bool:
            """Return whether close() has been called."""
            return self.closed

    bridge = _Bridge()
    monkeypatch.setattr(e01_cli_wizard, 'WizardUiBridgeTk', lambda: bridge)
    monkeypatch.setattr(e01_cli_wizard, 'ask_pizza_order',
                        lambda bridge: 'Bob orders a Mushroom pizza.')
    summary = e01_cli_wizard.run_cli_wizard()
    assert summary == 'Bob orders a Mushroom pizza.'
    assert bridge.is_closed()


def test_new_window_builds() -> None:
    """Test the pop-up example builds its main widgets and wizard button."""
    with _gui_root() as root:
        app = e02_new_window.PizzaCounterApp(root)
        # pylint: disable-next=protected-access
        assert isinstance(app._log, tk.Listbox)


def test_new_window_logs(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test taking an order opens a wizard window and logs its summary."""
    monkeypatch.setattr(e02_new_window, 'run_pizza_order',
                        lambda bridge: 'Cara orders a Olive pizza.')
    with _gui_root() as root:
        app = e02_new_window.PizzaCounterApp(root)
        # pylint: disable-next=protected-access
        app._take_order()
        # pylint: disable-next=protected-access
        assert app._log.get(0) == 'Cara orders a Olive pizza.'


def test_embedded_app_builds() -> None:
    """Test the embedded example builds its two panels and status label."""
    with _gui_root() as root:
        app = e03_embedded_area.SplitWindowApp(root)
        # pylint: disable-next=protected-access
        assert app._status.cget('text') == 'No order yet.'
        # pylint: disable-next=protected-access
        app._click_unrelated()
        # pylint: disable-next=protected-access
        assert '1 time' in str(app._status.cget('text'))


def test_embedded_logs_order(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test taking an order fills the area and updates the status label."""
    monkeypatch.setattr(e03_embedded_area, 'run_pizza_order',
                        lambda bridge: 'Dave orders a Pepperoni pizza.')
    with _gui_root() as root:
        app = e03_embedded_area.SplitWindowApp(root)
        # pylint: disable-next=protected-access
        app._take_order()
        # pylint: disable-next=protected-access
        assert app._status.cget('text') == 'Dave orders a Pepperoni pizza.'
        # pylint: disable-next=protected-access
        assert not app._area.winfo_children()


def _widgets(parent: tk.Misc, kind: type[tk.Widget]) -> list[tk.Widget]:
    """Return every widget of the given kind under parent, in child order."""
    found: list[tk.Widget] = []
    for child in parent.winfo_children():
        if isinstance(child, kind):
            found.append(child)
        found.extend(_widgets(child, kind))
    return found


def _click(parent: tk.Misc, text: str) -> None:
    """Press the button labelled text somewhere under parent."""
    buttons = [button for button in _widgets(parent, tk.Button)
               if str(button.cget('text')) == text]
    assert buttons, f'No button labelled {text} was built.'
    assert isinstance(buttons[0], tk.Button)
    buttons[0].invoke()


def _set_hours(area: tk.Misc, member: int, day: int, text: str) -> None:
    """Type text into the hours cell of one team member and weekday.

    The cells are built row by row, so the entries come in that order.
    """
    entry = _widgets(area, tk.Entry)[member * 5 + day]
    assert isinstance(entry, tk.Entry)
    entry.delete(0, 'end')
    entry.insert(0, text)


def _status(area: tk.Misc) -> list[str]:
    """Return the red, non-empty status and reason texts under area."""
    return [str(label.cget('text')) for label in _widgets(area, tk.Label)
            if str(label.cget('fg')) == 'red' and label.cget('text')]


def _ask_e08(action: Callable[[tk.Misc], None]) -> tuple[Optional[str], str]:
    """Ask the e08 timesheet through the Tk bridge, answered by action.

    The bridge is embedded in a frame of the withdrawn root, so no window
    reaches the screen, and is not modal, since a withdrawn window cannot
    be grabbed. action gets that frame once the matrix is shown. A
    watchdog aborts the matrix if action leaves it unanswered.

    Returns:
        The summary, or None when cancelled, and the example's output.
    """
    with _gui_root() as root:
        area = tk.Frame(root)
        bridge = WizardUiBridgeTk(area=area, modal=False)
        output = StringIO()
        root.after(0, lambda: action(area))
        watchdog = root.after(_WATCHDOG_MS, lambda: _click(area, 'Abort'))
        try:
            answers = e08_matrix_form.ask_timesheet(bridge, output)
        finally:
            root.after_cancel(watchdog)
            bridge.close()
    summary = None if answers is None else e08_matrix_form.summarize(answers)
    return summary, output.getvalue()


def test_e08_tk_defaults() -> None:
    """Test accepting the e08 timesheet as shown gives every default."""
    summary, _ = _ask_e08(lambda area: _click(area, 'OK'))
    assert summary == '\n'.join([
        'Hours worked this week:',
        '  Alice: Mon 8, Tue 8, Wed 8, Thu 8, Fri 8 (total 40)',
        '  Bob: Mon 8, Tue 8, Wed 8, Thu 8, Fri 8 (total 40)',
        '  Cleo: Mon 8, Tue 8, Wed 8, Thu 8, Fri 8 (total 40)'])


def test_e08_tk_hours() -> None:
    """Test hours typed into the e08 matrix end up in the summary."""
    def _answer(area: tk.Misc) -> None:
        """Change Bob's Tuesday and Cleo's Friday, then press OK."""
        _set_hours(area, 1, 1, '6')
        _set_hours(area, 2, 4, '0')
        _click(area, 'OK')
    summary, _ = _ask_e08(_answer)
    assert summary is not None
    assert summary.splitlines()[2:] == [
        '  Bob: Mon 8, Tue 6, Wed 8, Thu 8, Fri 8 (total 38)',
        '  Cleo: Mon 8, Tue 8, Wed 8, Thu 8, Fri 0 (total 32)']


def test_e08_tk_range() -> None:
    """Test an out-of-range e08 cell blocks OK until it is corrected.

    The message names the cell by its team member and weekday labels.
    """
    shown: list[list[str]] = []

    def _answer(area: tk.Misc) -> None:
        """Try 25 hours, record the message, then correct it to 6."""
        _set_hours(area, 1, 1, '25')
        _click(area, 'OK')
        shown.append(_status(area))
        _set_hours(area, 1, 1, '6')
        _click(area, 'OK')
    summary, _ = _ask_e08(_answer)
    assert shown == [['Bob / Tue: Please enter an integer between 0 and 24.']]
    assert summary is not None and 'Tue 6' in summary


def test_e08_tk_cancel() -> None:
    """Test aborting the e08 matrix is reported as a cancelled timesheet."""
    summary, output = _ask_e08(lambda area: _click(area, 'Abort'))
    assert summary is None
    assert output == 'Timesheet cancelled.\n'
