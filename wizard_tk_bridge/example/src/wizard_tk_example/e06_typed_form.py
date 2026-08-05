#! /usr/bin/env python3
"""Run the typed-form teaching wizard through the Tk bridge."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from wizard_ui_example import e06_typed_form as example
from wizard_tk_example._tk_example import run_form_example


def main() -> int:
    """Run the typed-form wizard until it is completed or cancelled."""
    run_form_example(example.ask_schedule, example.summarize_answers)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
