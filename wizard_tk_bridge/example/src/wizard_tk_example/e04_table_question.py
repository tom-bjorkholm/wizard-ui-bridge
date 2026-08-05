#! /usr/bin/env python3
"""Run the table-question teaching wizard through the Tk bridge."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional
from wizard_ui_example import e04_table_question as example
from wizard_tk_example._tk_example import run_tk_example
from wizard_ui_bridge import WizardUiBridge


def _ask(bridge: WizardUiBridge) -> Optional[str]:
    """Ask and summarize the shared table-question wizard."""
    rules = example.ask_rename_rules(bridge)
    guests = example.ask_guest_list(bridge)
    return example.summarize(rules, guests)


def main() -> int:
    """Run the table-question wizard until it is completed or cancelled."""
    run_tk_example(_ask)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
