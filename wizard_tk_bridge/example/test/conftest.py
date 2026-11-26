#! /usr/bin/env python3
"""Pytest configuration for the teaching examples.

The Tk examples run the bridge-independent examples of wizard_ui_example
through the Tk bridge, so the source folder of those examples is put on
the path as well. It does not depend on pytest having collected the
wizard_ui_bridge examples first.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import sys
from pathlib import Path


EXAMPLE_SRC = Path(__file__).resolve().parents[1] / 'src'
UI_EXAMPLE_SRC = (Path(__file__).resolve().parents[3] / 'wizard_ui_bridge'
                  / 'example' / 'src')
for folder in (UI_EXAMPLE_SRC, EXAMPLE_SRC):
    sys.path.insert(0, str(folder))
