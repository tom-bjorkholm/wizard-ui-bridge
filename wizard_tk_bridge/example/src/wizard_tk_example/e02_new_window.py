#! /usr/bin/env python3
"""Run the wizard as a new pop-up window in an app with other windows.

This example is a small Tkinter application: a main window with its own
content (a label and a log of past orders) that also happens to offer a
button opening the pizza wizard. Unlike the CLI example, this
application already has a Tk root and other widgets before the wizard is
ever asked for, so the wizard must show up *over* that application
instead of taking it over.

parent, not area
-----------------
Passing the main window as ``parent`` tells
:class:`~wizard_tk_bridge.WizardUiBridgeTk` to build its *own* new
Toplevel window for the wizard, positioned over ``parent``. modal
defaults to True, so that pop-up grabs the keyboard and pointer for the
whole application while it is open -- the user finishes or cancels the
wizard before going back to the main window. See e03_embedded_area.py
for the alternative: no window of its own, built directly into part of
an existing window instead.

Running it
----------
::

    python -m wizard_tk_example.e02_new_window
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter as tk
from wizard_tk_example._shared_wizard import run_pizza_order
from wizard_tk_bridge import WizardUiBridgeTk


# pylint: disable-next=too-few-public-methods
class PizzaCounterApp:
    """A tiny app window that opens the wizard as a pop-up window."""

    def __init__(self, root: tk.Tk) -> None:
        """Build the main window's own content and its wizard button."""
        self._root = root
        root.title('Pizza counter')
        tk.Label(root, text='Orders taken so far:').pack(padx=12, pady=(12, 4))
        self._log = tk.Listbox(root, width=50)
        self._log.pack(padx=12, pady=4)
        tk.Button(root, text='Take a new order',
                  command=self._take_order).pack(pady=12)

    def _take_order(self) -> None:
        """Open the wizard as a new window and log its summary."""
        bridge = WizardUiBridgeTk(parent=self._root)
        summary = run_pizza_order(bridge)
        if summary is not None:
            self._log.insert('end', summary)


def main() -> int:
    """Run the pizza counter application until its window is closed."""
    root = tk.Tk()
    PizzaCounterApp(root)
    root.mainloop()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
