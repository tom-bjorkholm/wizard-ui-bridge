#! /usr/bin/env python3
"""Run the wizard from a CLI program that has no other Tkinter code.

This is the simplest of the three usage examples: a script that is
otherwise a plain command-line program, with no window of its own, that
still wants to ask its questions through a graphical wizard instead of
the console.

The bridge owns the Tk application
----------------------------------
Every Tkinter window needs exactly one ``tk.Tk()`` root somewhere in the
process, even if the program never shows it. With no ``parent`` or
``area``, :class:`~wizard_tk_bridge.WizardUiBridgeTk` creates that root,
hides it, and builds the only visible wizard window over it. The bridge
also destroys the root when it closes, so this CLI program contains no
other Tkinter code.

No mainloop() call is needed here: each ask method waits for its answer
with Tk's own ``wait_variable``, which pumps the event loop just long
enough to process the pop-up's events, so the program is not left
running an event loop once the wizard has closed.

Running it
----------
::

    python -m wizard_tk_example.e01_cli_wizard
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional
from wizard_tk_example._shared_wizard import ask_pizza_order
from wizard_tk_bridge import WizardUiBridgeTk


def run_cli_wizard() -> Optional[str]:
    """Ask the pizza wizard through the bridge-owned Tk application."""
    bridge = WizardUiBridgeTk()
    try:
        return ask_pizza_order(bridge)
    finally:
        bridge.close()


def main() -> int:
    """Run the wizard and print its summary, or that it was cancelled."""
    summary = run_cli_wizard()
    print(summary if summary is not None else 'Order cancelled.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
