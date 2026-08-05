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

from typing import Optional
from wizard_ui_bridge import WizardNavigation, WizardUiBridge
from wizard_tk_bridge import WizardUiBridgeTk

TOPPINGS = ('Mushroom', 'Pepperoni', 'Olive')


def ask_pizza_order(bridge: WizardUiBridge) -> Optional[str]:
    """Ask a name, a topping and whether to add cheese; return a summary.

    Any WizardNavigation raised by an ask method -- the user asked to go
    back, cancel or abort -- is treated here as "gave up", since a
    three-question wizard has nowhere else to go; this example returns
    None in that case instead of a summary.
    """
    try:
        name = bridge.ask_text('Your name?', nullable=True)
        topping = bridge.ask_choice('Favorite topping?', choices=TOPPINGS)
        extra_cheese = bridge.ask_yes_no('Extra cheese?', default=False)
    except WizardNavigation:
        return None
    who = name or 'Anonymous'
    cheese = ' with extra cheese' if extra_cheese else ''
    return f'{who} orders a {topping} pizza{cheese}.'


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
