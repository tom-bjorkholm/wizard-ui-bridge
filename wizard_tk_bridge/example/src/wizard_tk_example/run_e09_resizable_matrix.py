#! /usr/bin/env python3
"""Run the resizable-matrix teaching wizard through the Tk bridge."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from wizard_ui_example import e09_resizable_matrix as example
from wizard_tk_example._tk_example import run_form_example


def main() -> int:
    """Run the resizable-matrix wizard until it is completed or cancelled."""
    run_form_example(example.ask_contractors, example.summarize)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
