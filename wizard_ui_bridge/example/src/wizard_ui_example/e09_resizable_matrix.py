#! /usr/bin/env python3
"""Demonstrate a resizable, validated ask_matrix_form() contractor list.

This teaching example builds on e08_matrix_form.py, which shows the basics
of ask_matrix_form() with a fixed timesheet that is asked once. This
example adds what a real application usually needs on top of that: a
matrix the user can resize, several kinds of input cells, live feedback
from a partial validator, and a final check that asks the matrix again
until the answers are acceptable.

The matrix
----------
The matrix is a list of contractors, one contractor per row. The first
row is a header of plain labels; there is no label column::

    Name    | Start date | End date   | Contract 1 | Contract 2 | Contract 3
    Alice   | 2027-01-01 | 2027-06-30 | alice.pdf  | nda.pdf    | (empty)
    Bob     | 2027-02-01 | 2027-12-31 | bob.pdf    | (empty)    | (empty)

The name is an AskTextCell, the dates are AskDateCells (a date picker in a
graphical bridge) and the contract files are AskPathCells (a file picker
in a graphical bridge).

A matrix that grows and shrinks
-------------------------------
The user may append or delete the last row or the last column, within the
minimum and maximum dimensions of the request:

- rows: the header row plus 1 to 4 contractors, and
- columns: name, start date and end date plus 1 to 3 contract files.

An appended column is added to *every* contractor. That is why only the
first contract file is required: contracts 2 and 3 may be left empty, so
one contractor can have three contract files while another has just one.

Validation in two layers
------------------------
The start date must be before the end date for every contractor, and the
contract files must exist. Exactly as in e04 and e05 this is checked in
two layers:

- A partial validator gives live feedback while the matrix is edited: a
  graphical or textual bridge shows its message and refuses to submit
  while a start date is not before its end date.
- The wizard must not trust a bridge to enforce anything, so after
  ask_matrix_form() returns, the whole matrix is verified again. When a
  problem is found the matrix is asked again with a re_ask_reason and with
  the user's own answers as defaults, so no work is lost.

The file existence rule is also given to each path cell
(WizardPathKind.EXISTING_FILE), so a bridge can enforce it as early as it
likes, but the final verification checks it as well.

Nothing is written to disk, so the reader can concentrate on
ask_matrix_form().
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import argparse
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Callable, Optional, Sequence, TextIO

from wizard_ui_bridge import make_text_ui_bridge, UiBridgeType, \
    WizardUiBridge, WizardNavigation, PathAskOptions, WizardPathKind, \
    AskCell, AnswerCell, AnswerCells, CellPosition, MatrixDimension, \
    MatrixDimensions, MatrixConsoleQuestion, MatrixRequest, \
    PartMatrixValidationRes, AskLabelCell, AskTextCell, AskDateCell, \
    AskPathCell, AnswerTextCell, AnswerDateCell, AnswerPathCell

# Each name is the index of one column of the matrix. Columns from
# _FIRST_CONTRACT onwards hold contract files. Row 0 is the header row,
# so contractor number n (counting from 1) is in row n.
_NAME, _START, _END, _FIRST_CONTRACT = range(4)
_HEADER_ROWS = 1

# The limits of the matrix, counted in contractors and contract files.
_MIN_CONTRACTORS, _MAX_CONTRACTORS = 1, 4
_MIN_CONTRACTS, _MAX_CONTRACTS = 1, 3

# The main instruction shown above the whole matrix. A graphical or textual
# bridge lays it out nicely; the console fallback prints it once.
_MATRIX_QUESTION = (
    'Register the contractors, one contractor per row.\n'
    'Add or remove contractor rows (1-4) and contract file columns (1-3) '
    'as needed. Only the first contract file is required.')

# The header row: one label per column. A label cell gives no answer, so
# the header row of the answers holds only None. A label seldom needs help
# text, so AskLabelCell only takes it as an optional keyword argument.
_HEADER: tuple[AskCell, ...] = (
    AskLabelCell('Name'), AskLabelCell('Start date'), AskLabelCell('End date'),
    AskLabelCell('Contract 1'), AskLabelCell('Contract 2'),
    AskLabelCell('Contract 3'))

# The console asks one cell at a time (see e08): here row by row, one
# contractor after the other, naming each cell by the header label above
# it. There is no label to the left of a cell, so no row label is shown.
_CONSOLE_QUESTION = MatrixConsoleQuestion(use_help_text=False,
                                          show_horizontal_label=False,
                                          show_vertical_label=True,
                                          row_order=True)


@dataclass(frozen=True)
class Contractor:
    """One contractor, as read from one row of the matrix.

    The values are Optional where the matrix allows an empty cell, so the
    same class holds both a half-filled row (while the matrix is being
    edited or re-asked) and a verified row.

    Attributes:
        name: The contractor's name.
        start: The first day of the contract, or None when not filled in.
        end: The last day of the contract, or None when not filled in.
        contracts: One entry per contract column currently in the matrix:
                   the path of the contract file, or None for an empty cell.
    """

    name: str
    start: Optional[date]
    end: Optional[date]
    contracts: tuple[Optional[Path], ...]


# An empty contractor, used for the rows the user has not filled in yet.
_EMPTY = Contractor('', None, None, ())


def build_request(previous: Sequence[Contractor] = ()) -> MatrixRequest:
    """Describe the contractor matrix form as a MatrixRequest.

    Args:
        previous: The contractors from an earlier, rejected answer. Their
                  values become the defaults of the cells, and the matrix
                  starts in the shape the user left it in. Empty for the
                  first question.
    """
    return MatrixRequest(long_question=_MATRIX_QUESTION,
                         ask_cells=build_cells(previous),
                         dimensions=_dimensions(previous),
                         console_question=_CONSOLE_QUESTION,
                         partial_validator=contractor_validator)


def build_cells(previous: Sequence[Contractor]) -> list[list[AskCell]]:
    """Return the cells of the matrix in its maximum dimensions.

    The matrix first shows only the part of these cells within the default
    dimensions. A row or column the user appends shows the cells already
    given here at its position, so every cell can have its own default.
    (A MatrixCellSpec may also be a function from CellPosition to AskCell,
    or a smaller grid whose last row and column are repeated, but a full
    grid is the easiest to read.)
    """
    padding = [_EMPTY] * (_MAX_CONTRACTORS - len(previous))
    return [list(_HEADER)] + [_row_cells(contractor)
                              for contractor in list(previous) + padding]


def _row_cells(contractor: Contractor) -> list[AskCell]:
    """Return the cells of one contractor row, with its values as defaults."""
    padding = [None] * (_MAX_CONTRACTS - len(contractor.contracts))
    contracts = list(contractor.contracts) + padding
    cells: list[AskCell] = [
        AskTextCell(help_text='The name of the contractor.',
                    default=contractor.name),
        # A date cell with nullable False (the default) must be filled in.
        AskDateCell(help_text='The first day of the contract.',
                    default=contractor.start),
        AskDateCell(help_text='The last day of the contract.',
                    default=contractor.end)]
    return cells + [_contract_cell(index, path)
                    for index, path in enumerate(contracts)]


def _contract_cell(index: int, path: Optional[Path]) -> AskPathCell:
    """Return the path cell for contract file number index (0-based).

    Every contract file must exist, which WizardPathKind.EXISTING_FILE
    tells the bridge. Only the first contract file is required; the others
    are nullable, so an empty cell is answered with None.
    """
    options = PathAskOptions(kind=WizardPathKind.EXISTING_FILE,
                             nullable=index > 0, default=path)
    return AskPathCell(help_text='A signed contract file that exists.',
                       path_options=options)


def _dimensions(previous: Sequence[Contractor]) -> MatrixDimensions:
    """Return the size limits of the matrix and its starting shape.

    The header row and the name and date columns count like any other row
    or column. The minimum dimensions include them, so the user can never
    delete the header row or the name and date columns.
    """
    contractors = max(_MIN_CONTRACTORS, len(previous))
    contracts = max([_MIN_CONTRACTS] + [len(contractor.contracts)
                                        for contractor in previous])
    return MatrixDimensions(
        min=MatrixDimension(_HEADER_ROWS + _MIN_CONTRACTORS,
                            _FIRST_CONTRACT + _MIN_CONTRACTS),
        max=MatrixDimension(_HEADER_ROWS + _MAX_CONTRACTORS,
                            _FIRST_CONTRACT + _MAX_CONTRACTS),
        default=MatrixDimension(_HEADER_ROWS + contractors,
                                _FIRST_CONTRACT + contracts))


def read_contractors(answers: AnswerCells) -> list[Contractor]:
    """Read one Contractor from each contractor row of the answers.

    The answers have the shape the user left the matrix in: one row per
    matrix row, with an Answer*Cell for each input cell and None for each
    label cell. The header row holds only labels, so it is skipped.
    """
    return [_read_row(row) for row in answers[_HEADER_ROWS:]]


def _read_row(row: Sequence[Optional[AnswerCell]]) -> Contractor:
    """Read one Contractor from one row of the answers.

    Each answer is the Answer*Cell matching the Ask*Cell in its position,
    and its value attribute holds the typed answer.
    """
    name, start, end = row[_NAME], row[_START], row[_END]
    assert isinstance(name, AnswerTextCell)
    assert isinstance(start, AnswerDateCell)
    assert isinstance(end, AnswerDateCell)
    return Contractor('' if name.value is None else name.value, start.value,
                      end.value, tuple(_read_path(cell)
                                       for cell in row[_FIRST_CONTRACT:]))


def _read_path(cell: Optional[AnswerCell]) -> Optional[Path]:
    """Return the path of one contract cell, or None for an empty cell."""
    assert isinstance(cell, AnswerPathCell)
    return cell.value


def _name_problem(contractor: Contractor) -> Optional[str]:
    """Return a problem when the contractor has no name."""
    if contractor.name.strip() == '':
        return 'please enter a name.'
    return None


def _missing_date_problem(contractor: Contractor) -> Optional[str]:
    """Return a problem when a date of the contractor is not filled in."""
    if contractor.start is None or contractor.end is None:
        return 'please enter both the start date and the end date.'
    return None


def _date_order_problem(contractor: Contractor) -> Optional[str]:
    """Return a problem when the start date is not before the end date.

    A date that is not filled in yet is not a problem here; that is
    reported by _missing_date_problem() instead.
    """
    start, end = contractor.start, contractor.end
    if start is not None and end is not None and start >= end:
        return 'the start date must be before the end date.'
    return None


def _contract_problem(contractor: Contractor) -> Optional[str]:
    """Return a problem with the contract files of the contractor."""
    if not contractor.contracts or contractor.contracts[0] is None:
        return 'the first contract file is required.'
    for path in contractor.contracts:
        if path is not None and not path.is_file():
            return f'the contract file {path} does not exist.'
    return None


# The checks a final answer must pass, in the order they are reported.
_FINAL_CHECKS = (_name_problem, _missing_date_problem, _date_order_problem,
                 _contract_problem)


def _first_problem(contractors: Sequence[Contractor],
                   checks: Sequence[Callable[[Contractor], Optional[str]]]
                   ) -> Optional[str]:
    """Return the first problem any check finds, naming the contractor."""
    for number, contractor in enumerate(contractors, start=1):
        for check in checks:
            problem = check(contractor)
            if problem is not None:
                return f'Contractor {number}: {problem}'
    return None


def contractor_validator(answers: AnswerCells, changed: Optional[CellPosition]
                         ) -> PartMatrixValidationRes:
    """Give live feedback while the contractor matrix is edited.

    ask_matrix_form() calls this after every change, passing the current
    answers and the position of the cell that changed, or None when the
    user appended or deleted a row or column. A start date can be made
    wrong by editing either date of the row, and a deleted row can remove
    the only wrong row, so this validator simply checks the whole matrix
    every time and ignores changed.

    Only the date order is checked here. Empty cells are normal while the
    matrix is still being filled, so they are left to the final check.
    is_valid is False while a start date is not before its end date, which
    makes a graphical or textual bridge refuse to submit the matrix.
    """
    _ = changed
    problem = _first_problem(read_contractors(answers), [_date_order_problem])
    if problem is None:
        return PartMatrixValidationRes(True, '')
    return PartMatrixValidationRes(False, problem)


def contractor_problem(contractors: Sequence[Contractor]) -> Optional[str]:
    """Return the first problem with the final contractors, or None."""
    return _first_problem(contractors, _FINAL_CHECKS)


def ask_contractors(bridge: WizardUiBridge,
                    out_file: TextIO) -> Optional[list[Contractor]]:
    """Ask the contractor matrix until the answers pass the final check.

    The partial validator gives early feedback, but a bridge may skip it,
    so the returned matrix is always verified here. When it has a problem
    the matrix is asked again with the problem as re_ask_reason, and the
    request is rebuilt from the user's answers so no work is lost.

    Any ask method may raise a WizardNavigation request (back, cancel or
    abort) instead of returning answers. A single standalone matrix has no
    earlier step to go back to, so all of them are treated here as "the
    user gave up", and the function returns None.
    """
    contractors: list[Contractor] = []
    reason: Optional[str] = None
    while True:
        try:
            answers = bridge.ask_matrix_form(build_request(contractors),
                                             re_ask_reason=reason)
        except WizardNavigation:
            out_file.write('Contractor registration cancelled.\n')
            return None
        contractors = read_contractors(answers)
        reason = contractor_problem(contractors)
        if reason is None:
            return contractors


def summarize(contractors: Sequence[Contractor]) -> str:
    """Return a human-readable summary of the verified contractors."""
    return '\n'.join(['Contractors:'] + [_summary_line(contractor)
                                         for contractor in contractors])


def _summary_line(contractor: Contractor) -> str:
    """Return one indented summary line for a contractor.

    The empty optional contract cells are left out of the summary.
    """
    files = ', '.join(str(path) for path in contractor.contracts
                      if path is not None)
    return (f'  {contractor.name}: {contractor.start} to {contractor.end}, '
            f'contracts: {files}')


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
    """Ask the contractor matrix and print a summary of the answers.

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
    contractors = ask_contractors(bridge, out_file)
    if contractors is None:
        return None
    summary = summarize(contractors)
    out_file.write(summary + '\n')
    return summary


def build_parser() -> argparse.ArgumentParser:
    """Return the argument parser for the matrix-form example."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ui', default='auto',
                        choices=('auto', 'console', 'textual'),
                        help='Which text-mode UI bridge to use.')
    return parser


def main(args: Optional[list[str]] = None) -> int:
    """Parse arguments, ask the contractor matrix and print the summary."""
    ui_name = build_parser().parse_args(args).ui
    bridge = {'auto': UiBridgeType.AUTO, 'console': UiBridgeType.CONSOLE,
              'textual': UiBridgeType.TEXTUAL}[ui_name]
    collect_and_summarize(bridge_type=bridge)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
