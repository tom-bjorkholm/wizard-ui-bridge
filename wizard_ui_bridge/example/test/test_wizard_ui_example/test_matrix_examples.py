#! /usr/bin/env python3
"""Tests for the matrix form teaching examples e08 and e09.

The tests that use the scripted _MatrixBridge check the examples' own
logic. The console tests need the console implementation of
ask_matrix_form() and are skipped until it exists. The Tk bridge
implements ask_matrix_form(), and the tests of the wizard_tk_bridge
examples run e08 through it.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from datetime import date
from io import StringIO
from pathlib import Path
from typing import Optional, Sequence

import pytest
from wizard_ui_example import e08_matrix_form, e09_resizable_matrix
from wizard_ui_example.e09_resizable_matrix import Contractor
from wizard_ui_bridge import WizardPathKind, WizardUiBridge, WizardAbort, \
    MatrixRequest, MatrixDimension, MatrixDimensions, AnswerCells, AskCell, \
    AnswerCell, AskLabelCell, AskTextCell, AskIntCell, AskDateCell, \
    AskPathCell, AnswerTextCell, AnswerIntCell, AnswerDateCell, AnswerPathCell
from .console_driver import drive

_JAN = date(2027, 1, 1)
_JUN = date(2027, 6, 30)
_NO_MATRIX = pytest.mark.skip(
    reason='ask_matrix_form() is not implemented by the console bridge yet')


def _default_answers(request: MatrixRequest) -> AnswerCells:
    """Return the answers a bridge gives when every default is accepted.

    The answers have the default shape of the request, with each input
    cell answered by its default and each label cell by None.
    """
    cells = request.ask_cells
    assert isinstance(cells, list)
    shape = request.dimensions.default
    return [[_default_answer(cell) for cell in row[:shape.columns]]
            for row in cells[:shape.rows]]


def _default_answer(cell: AskCell) -> Optional[AnswerCell]:
    """Return the answer to one example cell that accepts its default."""
    if isinstance(cell, AskTextCell):
        return AnswerTextCell(cell, cell.default)
    if isinstance(cell, AskIntCell):
        return AnswerIntCell(cell, cell.default)
    if isinstance(cell, AskDateCell):
        return AnswerDateCell(cell, cell.default)
    if isinstance(cell, AskPathCell):
        return AnswerPathCell(cell, cell.path_options.default)
    assert isinstance(cell, AskLabelCell)
    return None


# pylint: disable-next=abstract-method
class _MatrixBridge(WizardUiBridge):
    """A bridge answering ask_matrix_form() from scripted answers."""

    def __init__(self, script: Sequence[AnswerCells]) -> None:
        """Store the answers to return, one per call."""
        self._script = list(script)
        self.requests: list[MatrixRequest] = []
        self.reasons: list[Optional[str]] = []

    def ask_matrix_form(self, request: MatrixRequest, *,
                        re_ask_reason: Optional[str] = None) -> AnswerCells:
        """Record the call and return the next scripted answers."""
        self.requests.append(request)
        self.reasons.append(re_ask_reason)
        if not self._script:
            raise WizardAbort()
        return self._script.pop(0)


def _texts(cells: Sequence[AskCell]) -> list[str]:
    """Return the texts of label cells."""
    return [cell.text for cell in cells if isinstance(cell, AskLabelCell)]


def _timesheet(hours: Sequence[Sequence[int]]) -> AnswerCells:
    """Return e08 answers holding hours, one row of hours per member."""
    cells = e08_matrix_form.build_request().ask_cells
    assert isinstance(cells, list)
    header: list[Optional[AnswerCell]] = [None] * len(cells[0])
    return [header] + [_member_answers(cells[1][1], row) for row in hours]


def _member_answers(cell: AskCell,
                    hours: Sequence[int]) -> list[Optional[AnswerCell]]:
    """Return the answers of one e08 member row: a label and hours."""
    assert isinstance(cell, AskIntCell)
    answers: list[Optional[AnswerCell]] = [None]
    return answers + [AnswerIntCell(cell, value) for value in hours]


def test_e08_request() -> None:
    """The timesheet is a fixed grid labelled in both directions."""
    request = e08_matrix_form.build_request()
    assert request.dimensions == MatrixDimensions.fixed(4, 6)
    assert request.partial_validator is None
    assert request.console_question.show_horizontal_label
    assert request.console_question.show_vertical_label
    cells = request.ask_cells
    assert isinstance(cells, list)
    assert _texts(cells[0]) == ['', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    assert _texts([row[0] for row in cells]) == ['', 'Alice', 'Bob', 'Cleo']
    hours = [cell for row in cells[1:] for cell in row[1:]]
    assert len(hours) == 15
    for cell in hours:
        assert isinstance(cell, AskIntCell)
        assert (cell.min_value, cell.max_value, cell.default) == (0, 24, 8)
    assert e08_matrix_form.build_parser().parse_args([]).ui == 'auto'


def test_e08_summary() -> None:
    """The summary lists each member's hours per day and the total."""
    answers = _timesheet([[8, 8, 8, 8, 8], [0, 4, 8, 12, 24],
                          [1, 2, 3, 4, 5]])
    assert e08_matrix_form.summarize(answers) == '\n'.join([
        'Hours worked this week:',
        '  Alice: Mon 8, Tue 8, Wed 8, Thu 8, Fri 8 (total 40)',
        '  Bob: Mon 0, Tue 4, Wed 8, Thu 12, Fri 24 (total 48)',
        '  Cleo: Mon 1, Tue 2, Wed 3, Thu 4, Fri 5 (total 15)'])


def test_e08_ask_once() -> None:
    """The timesheet is asked once, without a re-ask reason."""
    answers = _default_answers(e08_matrix_form.build_request())
    bridge = _MatrixBridge([answers])
    out_file = StringIO()
    assert e08_matrix_form.ask_timesheet(bridge, out_file) == answers
    assert bridge.reasons == [None]
    assert out_file.getvalue() == ''


def test_e08_ask_cancel() -> None:
    """A navigation request returns None and reports the cancellation."""
    out_file = StringIO()
    assert e08_matrix_form.ask_timesheet(_MatrixBridge([]), out_file) is None
    assert 'cancelled' in out_file.getvalue()


@_NO_MATRIX
def test_e08_console_defaults() -> None:
    """Accepting every default gives 8 hours a day to every member."""
    summary, _, _ = drive(e08_matrix_form.collect_and_summarize, [''] * 15)
    assert summary is not None
    assert 'Alice: Mon 8, Tue 8, Wed 8, Thu 8, Fri 8 (total 40)' in summary
    assert 'Cleo: Mon 8, Tue 8, Wed 8, Thu 8, Fri 8 (total 40)' in summary


@_NO_MATRIX
def test_e08_console_hours() -> None:
    """Typed hours are asked row by row and reach the summary."""
    lines = ['1', '2', '3', '4', '5'] + [''] * 5 + ['0', '0', '0', '0', '24']
    summary, _, _ = drive(e08_matrix_form.collect_and_summarize, lines)
    assert summary is not None
    assert 'Alice: Mon 1, Tue 2, Wed 3, Thu 4, Fri 5 (total 15)' in summary
    assert 'Cleo: Mon 0, Tue 0, Wed 0, Thu 0, Fri 24 (total 24)' in summary


@_NO_MATRIX
def test_e08_console_range() -> None:
    """An hours value outside 0-24 is re-asked by the cell's bounds."""
    lines = ['25', '9'] + [''] * 14
    summary, _, _ = drive(e08_matrix_form.collect_and_summarize, lines)
    assert summary is not None
    assert 'Alice: Mon 9, Tue 8' in summary


@_NO_MATRIX
def test_e08_console_cancel() -> None:
    """Aborting at the first cell returns no summary."""
    summary, output, _ = drive(e08_matrix_form.collect_and_summarize, [':q'])
    assert summary is None
    assert 'cancelled' in output


def _answers_for(contractors: Sequence[Contractor]) -> AnswerCells:
    """Return the e09 matrix answers a user gives to describe contractors."""
    return _default_answers(e09_resizable_matrix.build_request(contractors))


def _paths(tmp_path: Path,
           kinds: Sequence[Optional[str]]) -> tuple[Optional[Path], ...]:
    """Return contract paths: 'ok' exists, 'missing' does not, None empty."""
    (tmp_path / 'ok.pdf').write_text('signed')
    return tuple(None if kind is None else tmp_path / f'{kind}.pdf'
                 for kind in kinds)


def test_e09_request_shape() -> None:
    """The first request has a header row and one empty contractor."""
    request = e09_resizable_matrix.build_request()
    assert request.dimensions.min == MatrixDimension(2, 4)
    assert request.dimensions.max == MatrixDimension(5, 6)
    assert request.dimensions.default == MatrixDimension(2, 4)
    assert request.partial_validator is \
        e09_resizable_matrix.contractor_validator
    cells = request.ask_cells
    assert isinstance(cells, list)
    assert len(cells) == 5
    assert all(len(row) == 6 for row in cells)
    assert all(isinstance(cell, AskLabelCell) for cell in cells[0])
    assert e09_resizable_matrix.read_contractors(
        _default_answers(request)) == [Contractor('', None, None, (None,))]
    assert e09_resizable_matrix.build_parser().parse_args([]).ui == 'auto'


def test_e09_contract_cells() -> None:
    """Contract files must exist; only the first one is required."""
    cells = e09_resizable_matrix.build_request().ask_cells
    assert isinstance(cells, list)
    for row in cells[1:]:
        contracts = row[3:]
        assert all(isinstance(cell, AskPathCell) for cell in contracts)
        options = [cell.path_options for cell in contracts
                   if isinstance(cell, AskPathCell)]
        assert [option.nullable for option in options] == [False, True, True]
        assert all(option.kind == WizardPathKind.EXISTING_FILE
                   for option in options)


def test_e09_reask_shape(tmp_path: Path) -> None:
    """A re-ask starts in the user's shape with the user's values."""
    contracts = _paths(tmp_path, ['ok', None])
    contractors = [Contractor('Alice', _JAN, _JUN, contracts),
                   Contractor('Bob', None, _JAN, (None, None))]
    request = e09_resizable_matrix.build_request(contractors)
    assert request.dimensions.default == MatrixDimension(3, 5)
    assert e09_resizable_matrix.read_contractors(
        _default_answers(request)) == contractors


@pytest.mark.parametrize('start, end, valid', [
    (_JAN, _JUN, True), (_JUN, _JAN, False), (_JAN, _JAN, False),
    (None, _JAN, True), (_JAN, None, True), (None, None, True)])
def test_e09_validator(start: Optional[date], end: Optional[date],
                       valid: bool) -> None:
    """Live feedback flags only a start date not before its end date."""
    answers = _answers_for([Contractor('Alice', _JAN, _JUN, (None,)),
                            Contractor('', start, end, (None,))])
    result = e09_resizable_matrix.contractor_validator(answers, None)
    assert result.is_valid == valid
    assert result.message == ('' if valid else 'Contractor 2: the start '
                              'date must be before the end date.')
    assert result.disable_cells == ()
    assert result.prefill_values == ()


@pytest.mark.parametrize('name, dates, kinds, problem', [
    ('Alice', (_JAN, _JUN), ['ok'], None),
    ('Alice', (_JAN, _JUN), ['ok', None, 'ok'], None),
    (' ', (_JAN, _JUN), ['ok'], 'please enter a name'),
    ('Alice', (None, _JUN), ['ok'], 'both the start date and the end date'),
    ('Alice', (_JAN, None), ['ok'], 'both the start date and the end date'),
    ('Alice', (_JUN, _JAN), ['ok'], 'start date must be before'),
    ('Alice', (_JAN, _JAN), ['ok'], 'start date must be before'),
    ('Alice', (_JAN, _JUN), [None, 'ok'], 'first contract file is required'),
    ('Alice', (_JAN, _JUN), ['ok', 'missing'], 'missing.pdf does not exist')])
def test_e09_final_check(tmp_path: Path, name: str,
                         dates: tuple[Optional[date], Optional[date]],
                         kinds: list[Optional[str]],
                         problem: Optional[str]) -> None:
    """The final check reports the first problem, naming the contractor."""
    good = Contractor('Bob', _JAN, _JUN, _paths(tmp_path, ['ok']))
    checked = Contractor(name, *dates, _paths(tmp_path, kinds))
    result = e09_resizable_matrix.contractor_problem([good, checked])
    if problem is None:
        assert result is None
    else:
        assert result is not None
        assert result.startswith('Contractor 2: ')
        assert problem in result


def test_e09_ask_reask(tmp_path: Path) -> None:
    """A rejected matrix is re-asked with the reason and the user's values."""
    contracts = _paths(tmp_path, ['ok', None])
    bad = [Contractor('Alice', _JUN, _JAN, contracts)]
    good = [Contractor('Alice', _JAN, _JUN, contracts),
            Contractor('Bob', _JAN, _JUN, contracts)]
    bridge = _MatrixBridge([_answers_for(bad), _answers_for(good)])
    out_file = StringIO()
    assert e09_resizable_matrix.ask_contractors(bridge, out_file) == good
    assert bridge.reasons == [None, 'Contractor 1: the start date must be '
                              'before the end date.']
    second = bridge.requests[1]
    assert second.dimensions.default == MatrixDimension(2, 5)
    assert e09_resizable_matrix.read_contractors(
        _default_answers(second)) == bad
    assert out_file.getvalue() == ''


def test_e09_ask_cancel() -> None:
    """A navigation request returns None and reports the cancellation."""
    out_file = StringIO()
    bridge = _MatrixBridge([])
    assert e09_resizable_matrix.ask_contractors(bridge, out_file) is None
    assert 'cancelled' in out_file.getvalue()


def test_e09_summary(tmp_path: Path) -> None:
    """The summary lists each contractor and leaves out empty contracts."""
    first, _, third = _paths(tmp_path, ['ok', None, 'ok'])
    summary = e09_resizable_matrix.summarize([
        Contractor('Alice', _JAN, _JUN, (first, None, third)),
        Contractor('Bob', _JAN, _JUN, (first, None, None))])
    assert summary == '\n'.join([
        'Contractors:',
        f'  Alice: 2027-01-01 to 2027-06-30, contracts: {first}, {third}',
        f'  Bob: 2027-01-01 to 2027-06-30, contracts: {first}'])


@_NO_MATRIX
def test_e09_console(tmp_path: Path) -> None:
    """One contractor with one contract file is summarized."""
    contract = tmp_path / 'alice.pdf'
    contract.write_text('signed')
    lines = ['Alice', '2027-01-01', '2027-06-30', str(contract)]
    summary, _, _ = drive(e09_resizable_matrix.collect_and_summarize, lines)
    assert summary is not None
    assert f'Alice: 2027-01-01 to 2027-06-30, contracts: {contract}' \
        in summary


@_NO_MATRIX
def test_e09_console_reask(tmp_path: Path) -> None:
    """Swapped dates are reported and the matrix is asked again."""
    contract = tmp_path / 'alice.pdf'
    contract.write_text('signed')
    bad = ['Alice', '2027-06-30', '2027-01-01', str(contract)]
    good = ['', '2027-01-01', '2027-06-30', '']
    collect = e09_resizable_matrix.collect_and_summarize
    summary, output, errors = drive(collect, bad + good)
    assert summary is not None
    assert 'Alice: 2027-01-01 to 2027-06-30' in summary
    assert 'start date must be before' in output + errors


@_NO_MATRIX
def test_e09_console_cancel() -> None:
    """Aborting at the first cell returns no summary."""
    summary, output, _ = drive(e09_resizable_matrix.collect_and_summarize,
                               [':q'])
    assert summary is None
    assert 'cancelled' in output
