#! /usr/bin/env python3
"""Run the one-question teaching wizard through the Tk bridge."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from wizard_ui_example import e01_one_question as example
from wizard_tk_example._tk_example import run_tk_example


def main() -> int:
    """Run the one-question wizard until it is completed or cancelled."""
    run_tk_example(example.ask_greeting)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
