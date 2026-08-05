#! /usr/bin/env python3
"""Shared runner for the Tk versions of the UI bridge examples."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Callable, Optional, TextIO
from wizard_ui_bridge import AnswerFields, WizardNavigation, WizardUiBridge
from wizard_tk_bridge import WizardUiBridgeTk


def run_tk_example(ask: Callable[[WizardUiBridge], Optional[str]]) \
        -> Optional[str]:
    """Run one bridge-independent wizard in an owned Tk application.

    The result is shown in the wizard before the bridge closes, so a person
    running an example can inspect it without looking at the terminal. The
    final acknowledgement also gives ``show()`` a following question, as a
    real graphical bridge needs to do for a final message to be visible.
    """
    bridge = WizardUiBridgeTk()
    try:
        try:
            result = ask(bridge)
        except WizardNavigation:
            result = None
        bridge.show(result if result is not None else 'Wizard cancelled.')
        try:
            bridge.ask_text('Press Enter to close.', nullable=True)
        except WizardNavigation:
            pass
        return result
    finally:
        bridge.close()


def run_form_example(
        ask: Callable[[WizardUiBridge, TextIO], Optional[AnswerFields]],
        summarize: Callable[[AnswerFields], str]) -> Optional[str]:
    """Run one shared form example through the Tk bridge."""
    def _ask_form(bridge: WizardUiBridge) -> Optional[str]:
        """Ask the form and convert its typed answers to a summary."""
        answers = ask(bridge, bridge.error_file())
        return None if answers is None else summarize(answers)
    return run_tk_example(_ask_form)
