#! /usr/bin/env python3
"""Run the question-kinds teaching wizard through the Tk bridge."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional
from wizard_ui_example import e02_question_kinds as example
from wizard_tk_example._tk_example import run_tk_example
from wizard_ui_bridge import WizardUiBridge


def _ask(bridge: WizardUiBridge) -> Optional[str]:
    """Ask and summarize the shared question-kinds wizard."""
    settings = example.ask_export_settings(bridge)
    return None if settings is None else example.summarize(settings)


def main() -> int:
    """Run the question-kinds wizard until it is completed or cancelled."""
    run_tk_example(_ask)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
