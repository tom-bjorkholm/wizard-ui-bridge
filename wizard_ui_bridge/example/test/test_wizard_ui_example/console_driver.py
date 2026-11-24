#! /usr/bin/env python3
"""Run a teaching example on the console bridge with scripted input."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from io import StringIO
from typing import Callable, Optional
from wizard_ui_bridge import UiBridgeType


def drive(collect: Callable[..., Optional[str]],
          lines: list[str]) -> tuple[Optional[str], str, str]:
    """Run one example's collect function on the console with scripted lines.

    Args:
        collect: The example's collect_* function; all of them accept the
                 same stream and bridge_type keyword arguments.
        lines: One scripted answer per line, in the order the console
               fallback asks the questions.
    Returns:
        The value the collect function returned, the stdout text and the
        stderr text.
    """
    out_file = StringIO()
    err_file = StringIO()
    result = collect(stdin_file=StringIO('\n'.join(lines) + '\n'),
                     stdout_file=out_file, stderr_file=err_file,
                     bridge_type=UiBridgeType.CONSOLE)
    return result, out_file.getvalue(), err_file.getvalue()
