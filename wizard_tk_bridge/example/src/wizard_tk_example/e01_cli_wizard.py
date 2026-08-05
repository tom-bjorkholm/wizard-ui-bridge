#! /usr/bin/env python3
"""Run the wizard from a CLI program that has no other Tkinter code.

This is the simplest of the three usage examples: a script that is
otherwise a plain command-line program, with no window of its own, that
still wants to ask its questions through a graphical wizard instead of
the console.

The trick: a hidden root is still a real Tk application
--------------------------------------------------------
Every Tkinter window needs exactly one ``tk.Tk()`` root somewhere in the
process, even if the program never shows it. So a CLI program creates
one, immediately withdraws it (hides it from the screen and the
taskbar/dock), and hands it to :class:`~wizard_tk_bridge.WizardUiBridgeTk`
as ``parent``. The bridge then builds its own pop-up window over that
hidden root -- the *only* window the user ever sees -- runs the wizard in
it, and the CLI program destroys the root once it is done.

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

import tkinter as tk
from typing import Optional
from wizard_tk_example._shared_wizard import run_pizza_order
from wizard_tk_bridge import WizardUiBridgeTk


def run_cli_wizard(root: Optional[tk.Tk] = None) -> Optional[str]:
    """Ask the pizza wizard through a hidden root and return its summary.

    Args:
        root: A Tk root to reuse instead of creating and destroying one,
              so a test can schedule answers on it beforehand. A real
              CLI run leaves this as None.
    """
    owns_root = root is None
    if root is None:
        root = tk.Tk()
        root.withdraw()
    bridge = WizardUiBridgeTk(root)
    try:
        return run_pizza_order(bridge)
    finally:
        if owns_root:
            root.destroy()


def main() -> int:
    """Run the wizard and print its summary, or that it was cancelled."""
    summary = run_cli_wizard()
    print(summary if summary is not None else 'Order cancelled.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
