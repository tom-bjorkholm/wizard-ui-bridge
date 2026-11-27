#! /usr/bin/env python3
"""Tests for the base ask_matrix_form() on the console bridge.

The console bridge inherits the base implementation, which asks one
input cell at a time with the typed ask methods, in the order and with
the cell names of the MatrixConsoleQuestion, and offers resize menus
when the shape of the matrix may change.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from datetime import date
from io import StringIO
from pathlib import Path
from typing import Optional, Sequence

import pytest

from wizard_ui_bridge import AnswerCells, AskCell, CellPosition, \
    MatrixConsoleQuestion, MatrixDimension, MatrixDimensions, \
    MatrixRequest, PartialMatrixValidator, PartMatrixValidationRes, \
    PathAskOptions, AskLabelCell, AskTextCell, AskIntCell, AskPathCell, \
    AskYesNoCell, AskChoiceCell, AskMultiChoiceCell, AskDateCell, \
    AnswerIntCell, CellNamer, WizardBack, WizardCancelLevel, WizardAbort, \
    WizardUiBridgeConsole

_POS = CellPosition
_ROWS = MatrixConsoleQuestion(False, True, True)
_COLUMNS = MatrixConsoleQuestion(False, True, True, row_order=False)
_HOURS = AskIntCell('Hours that day.', default=8)
_DAYS = ('Mon', 'Tue', 'Wed')


class _Recorder(WizardUiBridgeConsole):
    """A console bridge with scripted input that records each question."""

    def __init__(self, lines: Sequence[str]) -> None:
        """Answer with lines, one per question."""
        self.out = StringIO()
        super().__init__(self.out, StringIO(''.join(f'{line}\n'
                                                    for line in lines)),
                         StringIO())
        self.questions: list[str] = []
        self.menus: list[list[str]] = []

    def _emit_question(self, question: str, re_ask_reason: Optional[str],
                       lines: Sequence[str], hint: str) -> None:
        """Record the question, and the lines of a menu, then emit them.

        The ' [default]' the console adds to a question is not recorded.
        """
        self.questions.append(question.split(' [')[0])
        if question.startswith('Rows: '):
            self.menus.append(list(lines))
        super()._emit_question(question, re_ask_reason, lines, hint)


def _grid(names: Sequence[str], days: int = 2) -> list[list[AskCell]]:
    """Return a header row of days and one row of hours per name."""
    header: list[AskCell] = [AskLabelCell('')]
    header += [AskLabelCell(day) for day in _DAYS[:days]]
    grid = [header]
    for name in names:
        row: list[AskCell] = [AskLabelCell(name)]
        grid.append(row + [_HOURS] * days)
    return grid


def _dims(low: tuple[int, int], high: tuple[int, int],
          start: tuple[int, int]) -> MatrixDimensions:
    """Return dimensions from (rows, columns) pairs."""
    return MatrixDimensions(MatrixDimension(*low), MatrixDimension(*high),
                            MatrixDimension(*start))


# pylint: disable-next=too-many-arguments
def _ask(lines: Sequence[str], cells: list[list[AskCell]],
         dims: MatrixDimensions, *, console: MatrixConsoleQuestion = _ROWS,
         validator: Optional[PartialMatrixValidator] = None,
         namer: Optional[CellNamer] = None,
         reason: Optional[str] = None) -> tuple[AnswerCells, _Recorder]:
    """Ask a matrix on a recording console; return answers and bridge."""
    bridge = _Recorder(lines)
    request = MatrixRequest('Fill in the hours.', cells, dims, console,
                            validator, namer)
    return bridge.ask_matrix_form(request, re_ask_reason=reason), bridge


def _values(answers: AnswerCells) -> list[list[object]]:
    """Return the answer values, with None for each label cell."""
    return [[None if cell is None else cell.value for cell in row]
            for row in answers]


def _fixed(cells: list[list[AskCell]]) -> MatrixDimensions:
    """Return the fixed dimensions of a full grid."""
    return MatrixDimensions.fixed(len(cells), len(cells[0]))


@pytest.mark.parametrize('console, questions, values', [
    (_ROWS, ['Alice / Mon', 'Alice / Tue', 'Bob / Mon', 'Bob / Tue'],
     [[None, 1, 2], [None, 8, 4]]),
    (_COLUMNS, ['Alice / Mon', 'Bob / Mon', 'Alice / Tue', 'Bob / Tue'],
     [[None, 1, 8], [None, 2, 4]])])
def test_order(console: MatrixConsoleQuestion, questions: list[str],
               values: list[list[object]]) -> None:
    """Input cells are asked in row or column order, labels are skipped."""
    cells = _grid(['Alice', 'Bob'])
    answers, bridge = _ask(['1', '2', '', '4'], cells, _fixed(cells),
                           console=console)
    assert bridge.questions == questions
    assert _values(answers) == [[None] * 3] + values


def test_fixed_values() -> None:
    """Each input cell gets its typed answer, or its default when empty."""
    cells = _grid(['Alice', 'Bob'])
    answers, _ = _ask(['1', '', '3', '0'], cells, _fixed(cells))
    assert _values(answers) == [[None] * 3, [None, 1, 8], [None, 3, 0]]
    cell = answers[1][1]
    assert isinstance(cell, AnswerIntCell)
    assert cell.asking is _HOURS


def test_question_shown() -> None:
    """The long question and any re-ask reason are shown first."""
    cells = _grid(['Alice'], days=1)
    _, bridge = _ask([''], cells, _fixed(cells), reason='Try again.')
    assert bridge.out.getvalue().startswith('Fill in the hours.\n'
                                            'Try again.\n')


def _name_hours(answers: AnswerCells, position: CellPosition) -> str:
    """Name a cell by the hours answered in the cell to its left."""
    left = answers[position.row][position.column - 1]
    return '' if left is None else f'after {left.value}'


@pytest.mark.parametrize('horizontal, vertical, use_namer, question', [
    (True, True, False, 'Alice / Tue'),
    (True, False, False, 'Alice'),
    (False, True, False, 'Tue'),
    (False, False, True, 'after 5'),
    (True, True, True, 'Alice / Tue / after 5'),
    (False, False, False, 'Alice / Tue')])
def test_question_parts(horizontal: bool, vertical: bool, use_namer: bool,
                        question: str) -> None:
    """The question joins the parts switched on, else uses cell_name()."""
    cells = _grid(['Alice'])
    console = MatrixConsoleQuestion(False, horizontal, vertical,
                                    use_cell_namer=use_namer)
    _, bridge = _ask(['5', ''], cells, _fixed(cells), console=console,
                     namer=_name_hours)
    assert bridge.questions[1] == question


def test_empty_namer_name() -> None:
    """An empty name is left out, falling back to cell_name()."""
    cells = _grid(['Alice'], days=1)
    console = MatrixConsoleQuestion(False, False, False, use_cell_namer=True)
    _, bridge = _ask([''], cells, _fixed(cells), console=console,
                     namer=_name_hours)
    assert bridge.questions == ['Alice / Mon']


def test_no_labels() -> None:
    """A cell with no labels is named by its 1-based row and column."""
    cells: list[list[AskCell]] = [[_HOURS]]
    _, bridge = _ask([''], cells, _fixed(cells))
    assert bridge.questions == ['Row 1 / Column 1']


@pytest.mark.parametrize('use_help', [True, False])
def test_help_text(use_help: bool) -> None:
    """The help text is shown before the cell only when use_help_text."""
    cells = _grid(['Alice'], days=1)
    console = MatrixConsoleQuestion(use_help, True, True)
    _, bridge = _ask([''], cells, _fixed(cells), console=console)
    assert ('Hours that day.' in bridge.out.getvalue()) == use_help


def test_generator_spec() -> None:
    """A generator gives the cell of each position."""
    def cell_of(position: CellPosition) -> AskCell:
        """Label the first row and column, and ask hours elsewhere."""
        if position.row == 0 or position.column == 0:
            return AskLabelCell(f'L{position.row}{position.column}')
        return _HOURS
    dims = MatrixDimensions.fixed(2, 3)
    request = MatrixRequest('Q', cell_of, dims, _ROWS)
    bridge = _Recorder(['1', '2'])
    answers = bridge.ask_matrix_form(request)
    assert bridge.questions == ['L10 / L01', 'L10 / L02']
    assert _values(answers) == [[None] * 3, [None, 1, 2]]


def test_cell_kinds(tmp_path: Path) -> None:
    """Every kind of input cell is asked with its typed ask method."""
    cells: list[list[AskCell]] = [[
        AskTextCell(None), AskDateCell(None),
        AskPathCell(None, path_options=PathAskOptions(nullable=True)),
        AskYesNoCell(None, default=False),
        AskChoiceCell(None, choices=['a', 'b']),
        AskChoiceCell(None, choices=['a', 'b'], nullable=True),
        AskMultiChoiceCell(None, choices=['a', 'b'])]]
    lines = ['hi', '2027-01-02', str(tmp_path / 'f.txt'), '1', '2', '0',
             '1,2']
    answers, _ = _ask(lines, cells, _fixed(cells))
    assert _values(answers) == [['hi', date(2027, 1, 2), tmp_path / 'f.txt',
                                 True, 'b', None, ['a', 'b']]]


def test_first_menu() -> None:
    """After the first row the width is set before the next rows.

    The appended column asks its new cell of the first row at once, and
    the menu is offered again until the user goes on. The next row is
    asked with the new width. The rows are fixed, so the end menu only
    offers to delete the last column.
    """
    cells = _grid(['Alice', 'Bob'], days=3)
    lines = ['1', '2', '2', '3', '', '', '', '', '']
    answers, bridge = _ask(lines, cells, _dims((3, 2), (3, 4), (3, 3)))
    menu = 'Rows: 3, columns: 4. What next?'
    assert bridge.questions == [
        'Alice / Mon', 'Alice / Tue', 'Rows: 3, columns: 3. What next?',
        'Alice / Wed', menu, 'Bob / Mon', 'Bob / Tue', 'Bob / Wed', menu]
    assert bridge.menus == [
        ['1: Next row (default)', '2: Append column', '3: Delete last column'],
        ['1: Next row (default)', '2: Delete last column'],
        ['1: Done (default)', '2: Delete last column']]
    assert _values(answers) == [[None] * 4, [None, 1, 2, 3],
                                [None, 8, 8, 8]]


def test_first_menu_columns() -> None:
    """In column order the first menu, after the first column, sets rows.

    The first column holds only labels, so the menu comes after the
    second column. The appended row asks its new input cell in that
    column at once, and its label cell is not asked.
    """
    cells = _grid(['Alice', 'Bob'])
    lines = ['1', '2', '2', '', '3', '4', '']
    answers, bridge = _ask(lines, cells, _dims((2, 3), (3, 3), (2, 3)),
                           console=_COLUMNS)
    assert bridge.questions == [
        'Alice / Mon', 'Rows: 2, columns: 3. What next?', 'Bob / Mon',
        'Rows: 3, columns: 3. What next?', 'Alice / Tue', 'Bob / Tue',
        'Rows: 3, columns: 3. What next?']
    assert bridge.menus[0] == ['1: Next column (default)', '2: Append row']
    assert _values(answers) == [[None] * 3, [None, 1, 3], [None, 2, 4]]


def test_no_first_menu() -> None:
    """With a single input row only the end menu is offered."""
    cells = _grid(['Alice'], days=3)
    _, bridge = _ask(['1', '2', ''], cells, _dims((2, 2), (2, 4), (2, 3)))
    assert bridge.questions == ['Alice / Mon', 'Alice / Tue',
                                'Rows: 2, columns: 3. What next?']


def test_end_rows() -> None:
    """The end menu appends and deletes rows within the bounds.

    An appended row is asked at once. A deleted row that is appended
    again gets fresh cells, so the answers given in it are lost.
    """
    cells = _grid(['Alice', 'Bob', 'Cleo'])
    lines = ['1', '1', '2', '2', '2', '3', '2', '', '', '']
    answers, bridge = _ask(lines, cells, _dims((2, 3), (4, 3), (2, 3)))
    assert bridge.menus == [
        ['1: Done (default)', '2: Append row'],
        ['1: Done (default)', '2: Append row', '3: Delete last row'],
        ['1: Done (default)', '2: Append row'],
        ['1: Done (default)', '2: Append row', '3: Delete last row']]
    assert bridge.questions.count('Bob / Mon') == 2
    assert _values(answers) == [[None] * 3, [None, 1, 1], [None, 8, 8]]


def test_end_columns() -> None:
    """An appended column at the end asks its cell in every row."""
    cells = _grid(['Alice', 'Bob'], days=3)
    lines = ['1', '1', '', '2', '2', '2', '3', '4', '2', '']
    answers, bridge = _ask(lines, cells, _dims((3, 3), (3, 4), (3, 3)))
    assert bridge.questions[-5:] == [
        'Rows: 3, columns: 3. What next?', 'Alice / Wed', 'Bob / Wed',
        'Rows: 3, columns: 4. What next?', 'Rows: 3, columns: 3. What next?']
    assert _values(answers) == [[None] * 3, [None, 1, 1], [None, 2, 2]]


def test_empty_start() -> None:
    """A matrix starting with no rows is filled through the end menu."""
    cells: list[list[AskCell]] = [[_HOURS]]
    dims = _dims((0, 1), (1, 1), (0, 1))
    answers, bridge = _ask(['2', '5', ''], cells, dims)
    assert bridge.questions == ['Rows: 0, columns: 1. What next?',
                                'Row 1 / Column 1',
                                'Rows: 1, columns: 1. What next?']
    assert _values(answers) == [[5]]


def test_back() -> None:
    """Back re-asks the previous cell, then goes on."""
    cells = _grid(['Alice'])
    answers, bridge = _ask(['1', ':b', '5', '2'], cells, _fixed(cells))
    assert bridge.questions == ['Alice / Mon', 'Alice / Tue', 'Alice / Mon',
                                'Alice / Tue']
    assert _values(answers)[1] == [None, 5, 2]


def test_back_from_menu() -> None:
    """Back from a menu re-asks the last cell, then the menu again."""
    cells = _grid(['Alice'])
    answers, bridge = _ask(['1', '2', ':b', '3', ''], cells,
                           _dims((2, 2), (2, 3), (2, 3)))
    assert bridge.questions[2:] == ['Rows: 2, columns: 3. What next?',
                                    'Alice / Tue',
                                    'Rows: 2, columns: 3. What next?']
    assert _values(answers)[1] == [None, 1, 3]


def test_back_first_cell() -> None:
    """Back from the first cell is passed on to the wizard."""
    cells = _grid(['Alice'])
    with pytest.raises(WizardBack):
        _ask([':b'], cells, _fixed(cells))


@pytest.mark.parametrize('token, error', [(':c', WizardCancelLevel),
                                          (':q', WizardAbort)])
def test_navigation(token: str, error: type[Exception]) -> None:
    """Cancel and abort are passed on to the wizard."""
    cells = _grid(['Alice'])
    with pytest.raises(error):
        _ask(['1', token], cells, _fixed(cells))


def _hours_at(answers: AnswerCells, row: int, column: int) -> Optional[int]:
    """Return the hours answered in a cell."""
    cell = answers[row][column]
    assert isinstance(cell, AnswerIntCell)
    return cell.value


def test_validator_calls() -> None:
    """The validator sees the matrix first, each cell and each reshape.

    Its message is shown for each change, but not for the first call.
    """
    calls: list[Optional[CellPosition]] = []

    def check(answers: AnswerCells, changed: Optional[CellPosition]
              ) -> PartMatrixValidationRes:
        """Record the change and report the matrix as not valid."""
        _ = answers
        calls.append(changed)
        return PartMatrixValidationRes(False, 'Not yet.')
    cells = _grid(['Alice', 'Bob'], days=1)
    dims = _dims((2, 2), (3, 2), (2, 2))
    _, bridge = _ask(['1', '2', '2', ''], cells, dims, validator=check)
    assert calls == [None, _POS(1, 1), None, _POS(2, 1)]
    assert bridge.out.getvalue().count('Not yet.') == 3


def test_validator_disables() -> None:
    """A disabled cell is skipped and keeps its default answer."""
    def check(answers: AnswerCells, changed: Optional[CellPosition]
              ) -> PartMatrixValidationRes:
        """Disable Tuesday."""
        _ = (answers, changed)
        return PartMatrixValidationRes(True, '', disable_cells=(_POS(1, 2),))
    cells = _grid(['Alice'])
    answers, bridge = _ask(['1'], cells, _fixed(cells), validator=check)
    assert bridge.questions == ['Alice / Mon']
    assert _values(answers)[1] == [None, 1, 8]


def test_validator_prefills() -> None:
    """A prefill is offered as the default of its cell when asked."""
    def check(answers: AnswerCells, changed: Optional[CellPosition]
              ) -> PartMatrixValidationRes:
        """Prefill Tuesday with Monday's hours plus one."""
        if changed != _POS(1, 1):
            return PartMatrixValidationRes(True, '')
        hours = _hours_at(answers, 1, 1)
        assert hours is not None
        return PartMatrixValidationRes(True, '', prefill_values=(
            (_POS(1, 2), hours + 1),))
    cells = _grid(['Alice'])
    answers, bridge = _ask(['4', ''], cells, _fixed(cells), validator=check)
    assert 'Alice / Tue [5]' in bridge.out.getvalue()
    assert _values(answers)[1] == [None, 4, 5]


def test_back_reenabled() -> None:
    """Going back walks forward again over a cell that was disabled.

    Monday 0 disables Tuesday. Going back from Wednesday to Monday and
    changing it enables Tuesday again, so Tuesday is asked.
    """
    def check(answers: AnswerCells, changed: Optional[CellPosition]
              ) -> PartMatrixValidationRes:
        """Disable Tuesday while Monday is 0."""
        _ = changed
        off = (_POS(1, 2),) if _hours_at(answers, 1, 1) == 0 else ()
        return PartMatrixValidationRes(True, '', disable_cells=off)
    cells = _grid(['Alice'], days=3)
    lines = ['0', ':b', '4', '5', '6']
    answers, bridge = _ask(lines, cells, _fixed(cells), validator=check)
    assert bridge.questions == ['Alice / Mon', 'Alice / Wed', 'Alice / Mon',
                                'Alice / Tue', 'Alice / Wed']
    assert _values(answers)[1] == [None, 4, 5, 6]
