#! /usr/local/bin/python3
"""The base screen of the Textual bridge, which turns keys into navigation.

Every screen of the Textual bridge derives from _NavApp, so the keys
that ask to go back or cancel the current level work the same way on
every screen.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import ClassVar, Optional, TypeVar
from textual.app import App
from textual.binding import BindingType
from wizard_ui_bridge.arg_types import WizardNavigation, WizardBack, \
    WizardCancelLevel

_T = TypeVar('_T')


class _NavApp(App[_T]):
    """Base screen translating navigation keys into wizard requests.

    A subclass lays out one question. ctrl+b records a request to go
    back and ctrl+o a request to cancel the current level; the mnemonic
    for ctrl+o is "out one level". Both exit the screen with no value so
    the bridge can raise the matching request. The built-in ctrl+q quit
    also exits with no value, which the bridge treats as an abort. These
    keys avoid the editing shortcuts that the text input widget binds,
    so they work on every screen.
    """

    BINDINGS: ClassVar[list[BindingType]] = [
        ('ctrl+b', 'nav_back', 'Back'),
        ('ctrl+o', 'nav_cancel', 'Out one level')]

    def __init__(self) -> None:
        """Initialize with no pending navigation request."""
        super().__init__()
        self.nav: Optional[type[WizardNavigation]] = None

    def action_nav_back(self) -> None:
        """Record a request to return to the previous question.

        The name avoids App.action_back, the built-in screen-history
        action, so this records a wizard back request instead.
        """
        self.nav = WizardBack
        self.exit()

    def action_nav_cancel(self) -> None:
        """Record a request to cancel the current level."""
        self.nav = WizardCancelLevel
        self.exit()
