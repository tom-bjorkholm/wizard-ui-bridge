#! /usr/bin/env python3
"""Tests for the wizard_tk_bridge teaching examples."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter as tk
from typing import Iterator, Optional, Sequence
from contextlib import contextmanager
import pytest
from wizard_tk_example import e01_cli_wizard, e02_new_window, \
    e03_embedded_area
from wizard_tk_example._shared_wizard import ask_pizza_order
from wizard_ui_bridge import WizardAbort, WizardBack, WizardUiBridge


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

    def ask_text(self, question: str, re_ask_reason: Optional[str] = None,
                 nullable: bool = False, *, default: Optional[str] = None,
                 sensitive: bool = False) -> Optional[str]:
        """Return the next scripted text answer."""
        self.defaults.append(default)
        answer = self._next()
        assert answer is None or isinstance(answer, str)
        return answer

    def ask_choice(self, question: str, *, choices: Sequence[str],
                   default: Optional[str] = None,
                   re_ask_reason: Optional[str] = None) -> str:
        """Return the next scripted choice answer."""
        self.defaults.append(default)
        answer = self._next()
        assert isinstance(answer, str)
        return answer

    def ask_yes_no(self, question: str, default: bool,
                   re_ask_reason: Optional[str] = None) -> bool:
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

    This mirrors test_wizard_tk_bridge.gui_test_helpers.gui_root; the two
    test packages are built and analyzed as separate roots, so this one
    keeps its own copy instead of importing across that boundary.
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
        root.deiconify()
        app = e02_new_window.PizzaCounterApp(root)
        # pylint: disable-next=protected-access
        assert isinstance(app._log, tk.Listbox)


def test_new_window_logs(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test taking an order opens a wizard window and logs its summary."""
    monkeypatch.setattr(e02_new_window, 'run_pizza_order',
                        lambda bridge: 'Cara orders a Olive pizza.')
    with _gui_root() as root:
        root.deiconify()
        app = e02_new_window.PizzaCounterApp(root)
        # pylint: disable-next=protected-access
        app._take_order()
        # pylint: disable-next=protected-access
        assert app._log.get(0) == 'Cara orders a Olive pizza.'


def test_embedded_app_builds() -> None:
    """Test the embedded example builds its two panels and status label."""
    with _gui_root() as root:
        root.deiconify()
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
        root.deiconify()
        app = e03_embedded_area.SplitWindowApp(root)
        # pylint: disable-next=protected-access
        app._take_order()
        # pylint: disable-next=protected-access
        assert app._status.cget('text') == 'Dave orders a Pepperoni pizza.'
        # pylint: disable-next=protected-access
        assert not app._area.winfo_children()
