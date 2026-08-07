#! /usr/bin/env python3
"""Examples for the wizard user interface Tk bridge.

The run_e01 through run_e06 examples reuse the corresponding
bridge-independent teaching modules of wizard_ui_example. When these
source-tree examples are run directly, make that sibling example source
directory importable too.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import sys
from pathlib import Path


def _add_ui_example_path() -> None:
    """Make the sibling UI example source available in this source tree."""
    source = Path(__file__).resolve().parents[4] / 'wizard_ui_bridge' / \
        'example' / 'src'
    if source.is_dir() and str(source) not in sys.path:
        sys.path.insert(0, str(source))


_add_ui_example_path()
