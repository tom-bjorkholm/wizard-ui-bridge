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

__all__ = ['WizardUiBridgeTk']
