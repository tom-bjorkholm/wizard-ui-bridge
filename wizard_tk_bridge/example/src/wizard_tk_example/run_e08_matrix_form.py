#! /usr/bin/env python3
"""Run the timesheet matrix-form teaching wizard through the Tk bridge."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from wizard_ui_example import e08_matrix_form as example
from wizard_tk_example._tk_example import run_form_example


def main() -> int:
    """Run the timesheet wizard until it is completed or cancelled."""
    run_form_example(example.ask_timesheet, example.summarize)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
