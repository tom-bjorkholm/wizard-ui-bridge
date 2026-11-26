#! /usr/bin/env python3
"""Demonstrate the basics of ask_matrix_form() with a weekly timesheet.

This teaching example builds on e05_ask_form.py. Where ask_form() asks a
single column of questions, ask_matrix_form() asks a whole grid of them.
Here the grid is a weekly timesheet: one row per team member, one column
per weekday, and in each cell the hours that member worked that day::

             | Mon | Tue | Wed | Thu | Fri
    Alice    |  8  |  8  |  8  |  8  |  8
    Bob      |  8  |  8  |  8  |  8  |  8
    Cleo     |  8  |  8  |  8  |  8  |  8

The example is deliberately as small as possible: the matrix has a fixed
shape, it is asked once, and the answers are printed. e09_resizable_matrix
shows a matrix the user can resize, validation, and asking again.

Describing the matrix
---------------------
A MatrixRequest holds everything the bridge needs:

- long_question: the instruction shown above the grid,
- ask_cells: one Ask*Cell object per cell, as a list of rows,
- dimensions: how many rows and columns the matrix has, and
- console_question: how a console, which cannot show a grid, asks the
  cells one at a time.

Each cell is an Ask*Cell, and its Python type tells the bridge what to
show. The weekday names and the team member names are AskLabelCells:
plain text with no input. The weekday names ask to be shown in bold, so
the header row stands out where the bridge can show bold text. The hours
are AskIntCells. Their min_value and max_value make the bridge accept
only 0 to 24 hours, so no validation code is needed in this example.

Reading the answers
-------------------
ask_matrix_form() returns the answers in the same shape as the matrix:
one list per row, holding an AnswerIntCell for each hours cell and None
for each label cell.

On the plain console bridge each cell is asked in turn, so the very same
program runs under tests and with redirected input.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import argparse
import sys
from typing import Optional, TextIO

from wizard_ui_bridge import make_text_ui_bridge, UiBridgeType, \
    WizardUiBridge, WizardNavigation, AskCell, AnswerCell, AnswerCells, \
    MatrixDimensions, MatrixConsoleQuestion, MatrixRequest, AskLabelCell, \
    AskIntCell, AnswerIntCell

_DAYS = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri')
_TEAM = ('Alice', 'Bob', 'Cleo')

# The main instruction shown above the whole matrix. A graphical or textual
# bridge lays it out nicely; the console fallback prints it once.
_MATRIX_QUESTION = 'Fill in the hours each team member worked this week.'

# Every hours cell is asked the same way, so one AskIntCell object can be
# used in all of them. It starts at a normal working day of 8 hours.
_HOURS = AskIntCell(help_text='Hours worked that day (0-24).', default=8,
                    min_value=0, max_value=24)

# A console asks one cell at a time. This tells the console bridge to ask
# row by row (all days of Alice, then of Bob, ...), and to name each cell
# by the label to its left (the team member) and the label above it (the
# weekday), so the user knows which cell is asked. The help text is only
# shown when the user asks for it.
_CONSOLE_QUESTION = MatrixConsoleQuestion(use_help_text=False,
                                          show_horizontal_label=True,
                                          show_vertical_label=True,
                                          row_order=True)


def build_request() -> MatrixRequest:
    """Describe the timesheet as a MatrixRequest.

    The first row is the header: an empty corner label, then one label per
    weekday. Every other row starts with the team member's name as a label,
    followed by one hours cell per weekday. The label row and the label
    column count like any other row and column, so the matrix has
    1 + 3 rows and 1 + 5 columns. MatrixDimensions.fixed() gives a matrix
    of exactly that size, which the user cannot resize.
    """
    header: list[AskCell] = [AskLabelCell('')]
    # bold is only a hint: a bridge that cannot show bold text ignores it.
    header += [AskLabelCell(day, bold=True) for day in _DAYS]
    rows = [header] + [_member_row(member) for member in _TEAM]
    dimensions = MatrixDimensions.fixed(len(rows), len(header))
    return MatrixRequest(long_question=_MATRIX_QUESTION, ask_cells=rows,
                         dimensions=dimensions,
                         console_question=_CONSOLE_QUESTION)


def _member_row(member: str) -> list[AskCell]:
    """Return the row of one team member: a name label and hours cells."""
    row: list[AskCell] = [AskLabelCell(member)]
    return row + [_HOURS] * len(_DAYS)


def ask_timesheet(bridge: WizardUiBridge,
                  out_file: TextIO) -> Optional[AnswerCells]:
    """Ask the timesheet once and return the answers.

    Any ask method may raise a WizardNavigation request (back, cancel or
    abort) instead of returning answers. A single standalone matrix has no
    earlier step to go back to, so all of them are treated here as "the
    user gave up", and the function returns None.
    """
    try:
        return bridge.ask_matrix_form(build_request())
    except WizardNavigation:
        out_file.write('Timesheet cancelled.\n')
        return None


def summarize(answers: AnswerCells) -> str:
    """Return the hours of each team member as human-readable text.

    The answers have one row per matrix row. Row 0 is the header row, and
    in every other row cell 0 is the name label, so the hours of the team
    members are in answers[1:] and, within each row, in row[1:].
    """
    lines = ['Hours worked this week:']
    for member, row in zip(_TEAM, answers[1:], strict=True):
        hours = [_hours(cell) for cell in row[1:]]
        days = ', '.join(f'{day} {value}'
                         for day, value in zip(_DAYS, hours, strict=True))
        lines.append(f'  {member}: {days} (total {sum(hours)})')
    return '\n'.join(lines)


def _hours(cell: Optional[AnswerCell]) -> int:
    """Return the hours of one answered hours cell.

    The answer to an AskIntCell is an AnswerIntCell. Its value is only None
    for a nullable cell left empty; the hours cells are not nullable, so a
    bridge always gives them a number.
    """
    assert isinstance(cell, AnswerIntCell)
    assert cell.value is not None
    return cell.value


# The stream defaults, the --ui switch and main() below are the same plumbing
# in every example, so each example stays a complete program a reader can run
# and study on its own. Repeating this ceremony is a deliberate teaching
# choice, so duplicate-code is turned off from here to the end of the file.
# pylint: disable=duplicate-code
def collect_and_summarize(stdin_file: Optional[TextIO] = None,
                          stdout_file: Optional[TextIO] = None,
                          stderr_file: Optional[TextIO] = None,
                          bridge_type: UiBridgeType = UiBridgeType.AUTO
                          ) -> Optional[str]:
    """Ask the timesheet and print a summary of the answers.

    Args:
        stdin_file: Optional input stream for tests or scripted use.
        stdout_file: Optional output stream for tests or scripted use.
        stderr_file: Optional diagnostic stream for validation messages.
        bridge_type: Which text-mode bridge to build. AUTO selects the
                     Textual bridge in a real terminal and the console
                     bridge otherwise, which is what tests rely on.

    Returns:
        The printed summary text, or None when the user cancelled.
    """
    out_file = sys.stdout if stdout_file is None else stdout_file
    bridge = make_text_ui_bridge(
        out_file, sys.stdin if stdin_file is None else stdin_file,
        sys.stderr if stderr_file is None else stderr_file, bridge_type)
    answers = ask_timesheet(bridge, out_file)
    if answers is None:
        return None
    summary = summarize(answers)
    out_file.write(summary + '\n')
    return summary


def build_parser() -> argparse.ArgumentParser:
    """Return the argument parser for the timesheet example."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ui', default='auto',
                        choices=('auto', 'console', 'textual'),
                        help='Which text-mode UI bridge to use.')
    return parser


def main(args: Optional[list[str]] = None) -> int:
    """Parse arguments, ask the timesheet and print the summary."""
    ui_name = build_parser().parse_args(args).ui
    bridge = {'auto': UiBridgeType.AUTO, 'console': UiBridgeType.CONSOLE,
              'textual': UiBridgeType.TEXTUAL}[ui_name]
    collect_and_summarize(bridge_type=bridge)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
