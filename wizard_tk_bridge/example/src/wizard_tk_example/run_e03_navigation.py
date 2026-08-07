#! /usr/bin/env python3
"""Run the navigation teaching wizard through the Tk bridge."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional
from wizard_ui_example import e03_navigation as example
from wizard_tk_example._tk_example import run_tk_example
from wizard_ui_bridge import WizardUiBridge


def _ask(bridge: WizardUiBridge) -> Optional[str]:
    """Ask and summarize the shared navigation wizard."""
    draft = example.run_account_setup(bridge)
    return None if draft is None else example.summarize(draft)


def main() -> int:
    """Run the navigation wizard until it is completed or cancelled."""
    run_tk_example(_ask)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
