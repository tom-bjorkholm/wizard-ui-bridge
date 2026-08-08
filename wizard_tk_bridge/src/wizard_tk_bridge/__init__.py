#! /usr/bin/env python3
"""Public API for the wizard user interface Tk bridge.

WizardUiBridgeTk is a WizardUiBridge that asks every question through
real Tkinter widgets, in a window of its own or embedded in an area an
application already built. See wizard_tk_bridge.tk_bridge for the three
ways an application can show the wizard.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from wizard_tk_bridge.tk_bridge import WizardUiBridgeTk
from wizard_tk_bridge.auto_scroll import auto_hide
from wizard_tk_bridge.close_binding import CLOSE_ACCELERATOR, bind_close
from wizard_tk_bridge.gui_style import style_input, focus_first_input

__all__ = ['WizardUiBridgeTk',
           'auto_hide',
           'bind_close',
           'CLOSE_ACCELERATOR',
           'focus_first_input',
           'style_input']
