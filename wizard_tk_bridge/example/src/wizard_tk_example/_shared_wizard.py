#! /usr/bin/env python3
"""A tiny wizard shared by the wizard_tk_bridge usage examples.

Every example script in this package shows the *same* three questions
run through :class:`~wizard_tk_bridge.WizardUiBridgeTk`, so what differs
between the examples is only how the Tk widgets around the wizard are
put together -- a hidden root for a CLI program, a pop-up window in an
application with other windows, or an area inside a window the
application already built. Keeping the wizard itself trivial lets each
example stay focused on that one difference.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from dataclasses import dataclass
from typing import Callable, Optional
from wizard_ui_bridge import WizardAbort, WizardBack, WizardCancelLevel, \
    WizardUiBridge
from wizard_tk_bridge import WizardUiBridgeTk

TOPPINGS = ('Mushroom', 'Pepperoni', 'Olive')


@dataclass
class _PizzaDraft:
    """Keep pizza answers so revisited questions have useful defaults."""

    name: Optional[str] = None
    topping: Optional[str] = None
    extra_cheese: bool = False


def _ask_name(bridge: WizardUiBridge, draft: _PizzaDraft) -> None:
    """Ask the customer's name, keeping an earlier answer as default."""
    draft.name = bridge.ask_text('Your name?', nullable=True,
                                 default=draft.name)


def _ask_topping(bridge: WizardUiBridge, draft: _PizzaDraft) -> None:
    """Ask for a topping, keeping an earlier answer as default."""
    draft.topping = bridge.ask_choice('Favorite topping?', choices=TOPPINGS,
                                      default=draft.topping)


def _ask_cheese(bridge: WizardUiBridge, draft: _PizzaDraft) -> None:
    """Ask whether to add cheese, keeping an earlier answer as default."""
    draft.extra_cheese = bridge.ask_yes_no('Extra cheese?',
                                           default=draft.extra_cheese)


def _previous(position: int) -> int:
    """Return the previous position, staying at the first question."""
    return max(0, position - 1)


def ask_pizza_order(bridge: WizardUiBridge) -> Optional[str]:
    """Ask a name, a topping and whether to add cheese; return a summary.

    Back moves to the previous question and the draft supplies earlier
    answers as defaults. At the first question Back stays there. Out one
    level has no meaning at this top level, so it re-asks the current
    question with a note; Abort returns None.
    """
    draft = _PizzaDraft()
    steps: tuple[Callable[[WizardUiBridge, _PizzaDraft], None], ...] = (
        _ask_name, _ask_topping, _ask_cheese)
    position = 0
    while position < len(steps):
        try:
            steps[position](bridge, draft)
        except WizardBack:
            if position == 0:
                bridge.show('Already at the first question.')
            position = _previous(position)
        except WizardCancelLevel:
            bridge.show('This is the top level; there is nothing to cancel.')
        except WizardAbort:
            return None
        else:
            position += 1
    who = draft.name or 'Anonymous'
    cheese = ' with extra cheese' if draft.extra_cheese else ''
    assert draft.topping is not None
    return f'{who} orders a {draft.topping} pizza{cheese}.'


def run_pizza_order(bridge: WizardUiBridgeTk) -> Optional[str]:
    """Ask the pizza wizard and make sure the bridge is closed afterward.

    Every example shares this: whichever way the bridge showed its
    widgets -- a hidden root, a pop-up window or an embedded area -- it
    must still be closed once the wizard is done, so its window or its
    area's widgets are cleaned up even if the user aborted.
    """
    try:
        return ask_pizza_order(bridge)
    finally:
        bridge.close()
