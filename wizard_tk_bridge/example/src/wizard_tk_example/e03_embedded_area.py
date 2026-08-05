#! /usr/bin/env python3
"""Run the wizard embedded in an area of an existing window.

This example's application window is split in two: a left panel that is
the application's own content (unrelated buttons and a status label) and
a right panel that is nothing but an empty frame until a wizard is
running in it. Unlike e02_new_window.py, the wizard here never gets a
pop-up window of its own -- it is built directly into that right frame.

area, not parent -- and modal is the application's call
--------------------------------------------------------
Passing the frame as ``area`` (instead of the window as ``parent``) tells
:class:`~wizard_tk_bridge.WizardUiBridgeTk` to fill that frame in place
rather than opening a window. modal defaults to True, same as
e02_new_window.py, but this example passes modal=False on purpose: the
left panel's own button keeps working *while the wizard runs* in the
right panel, which is the whole point of embedding instead of popping up
a separate window. Passing modal=True here instead would still avoid a
separate window, but would grab the *whole* application window, making
the left panel unusable until the wizard finished -- close() releases
that grab and clears the area either way.

Running it
----------
::

    python -m wizard_tk_example.e03_embedded_area
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter as tk
from wizard_tk_example._shared_wizard import run_pizza_order
from wizard_tk_bridge import WizardUiBridgeTk


# pylint: disable-next=too-few-public-methods
class SplitWindowApp:
    """A window with its own left panel and a right area for the wizard."""

    def __init__(self, root: tk.Tk) -> None:
        """Build the two panels and the button that starts the wizard."""
        root.title('Pizza counter with an embedded wizard')
        left = tk.Frame(root, borderwidth=1, relief='groove')
        left.pack(side='left', fill='y', padx=8, pady=8)
        self._status = tk.Label(left, text='No order yet.', wraplength=160)
        self._status.pack(padx=8, pady=8)
        self._clicks = 0
        tk.Button(left, text='Unrelated button',
                  command=self._click_unrelated).pack(padx=8, pady=8)
        self._area = tk.Frame(root, borderwidth=1, relief='sunken')
        self._area.pack(side='left', fill='both', expand=True, padx=8, pady=8)
        tk.Button(root, text='Take a new order',
                  command=self._take_order).pack(side='bottom', pady=8)

    def _click_unrelated(self) -> None:
        """Prove the left panel keeps responding while the wizard runs."""
        self._clicks += 1
        self._status.configure(text=f'Unrelated button clicked '
                               f'{self._clicks} time(s).')

    def _take_order(self) -> None:
        """Run the wizard inside the right area, non-modally."""
        bridge = WizardUiBridgeTk(area=self._area, modal=False)
        summary = run_pizza_order(bridge)
        if summary is not None:
            self._status.configure(text=summary)


def main() -> int:
    """Run the split-window application until its window is closed."""
    root = tk.Tk()
    SplitWindowApp(root)
    root.mainloop()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
