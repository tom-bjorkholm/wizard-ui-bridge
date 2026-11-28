#! /usr/bin/env python3
"""Tests for start values asked on the console and by the base bridge.

The console shows a start value as the answer Enter keeps and offers
':e' to empty the answer. The base ask_form() and ask_matrix_form() ask
a prefilled field or cell with the prefill as its start value, so it
stays nullable, and a field or cell asked again after back starts with
the answer the user gave it. A bridge whose typed ask methods predate
start_value gets the start value as the default, with a warning.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from io import StringIO
from pathlib import Path
from typing import Optional, Sequence

import pytest

from wizard_ui_bridge import AnswerCells, AnswerField, AskCell, AskField, \
    AskFloatField, AskIntCell, AskIntField, AskTextField, \
    CellPosition, MatrixConsoleQuestion, MatrixDimensions, MatrixRequest, \
    PartFormValidationResult, PartMatrixValidationRes, \
    PartialMatrixValidator, PathAskOptions, WizardBack, WizardUiBridge, \
    WizardUiBridgeConsole

_ERASE_HINT = '(:e=erase  :b=back'


def _console(lines: Sequence[str]) -> tuple[WizardUiBridgeConsole, StringIO]:
    """Return a console bridge with scripted input, and its output."""
    out = StringIO()
    answers = StringIO(''.join(f'{line}\n' for line in lines))
    return WizardUiBridgeConsole(out, answers, StringIO()), out


@pytest.mark.parametrize('line, nullable, default, expected', [
    ('', True, None, 'Ada'),
    (':e', True, None, None),
    (':e', False, 'Bo', 'Bo'),
    (':e', False, None, ''),
    ('Cy', True, None, 'Cy')])
def test_text_start(line: str, nullable: bool, default: Optional[str],
                    expected: Optional[str]) -> None:
    """Enter keeps the start value and ':e' gives the empty answer."""
    bridge, out = _console([line])
    assert bridge.ask_text('Name?', nullable=nullable, default=default,
                           start_value='Ada') == expected
    assert 'Name? [Ada]' in out.getvalue()
    assert _ERASE_HINT in out.getvalue()


def test_text_no_start() -> None:
    """Without a start value the console offers no erase token."""
    bridge, out = _console([':e'])
    assert bridge.ask_text('Name?', nullable=True) == ':e'
    assert _ERASE_HINT not in out.getvalue()


@pytest.mark.parametrize('line, expected', [('', 7), (':e', None), ('3', 3)])
def test_int_start(line: str, expected: Optional[int]) -> None:
    """The base ask_int() passes its start value on to ask_text()."""
    bridge, out = _console([line])
    assert bridge.ask_int('Age?', nullable=True, start_value=7) == expected
    assert 'Age? [7]' in out.getvalue()


@pytest.mark.parametrize('line, expected', [
    ('', 'b'), ('0', None), (':e', None), ('3', 'c')])
def test_choice_start(line: str, expected: Optional[str]) -> None:
    """A nullable choice keeps its start; 0 or ':e' choose none."""
    bridge, out = _console([line])
    assert bridge.ask_choice('Pick?', choices=('a', 'b', 'c'), nullable=True,
                             start_value='b') == expected
    assert '2: b (current)' in out.getvalue()


@pytest.mark.parametrize('lines, expected', [
    ([''], ['a', 'c']), ([':e'], []), (['2'], ['b'])])
def test_multi_start(lines: list[str], expected: list[str]) -> None:
    """A multi-choice keeps its start; ':e' selects nothing."""
    bridge, out = _console(lines)
    assert bridge.ask_multi('Pick?', choices=('a', 'b', 'c'), default=['b'],
                            start_value=['a', 'c']) == expected
    assert '1: a (current)' in out.getvalue()
    assert '2: b (default)' not in out.getvalue()


@pytest.mark.parametrize('line, expected', [('', True), (':e', False)])
def test_yes_no_start(line: str, expected: bool) -> None:
    """A yes/no question keeps its start; ':e' gives the default."""
    bridge, out = _console([line])
    assert bridge.ask_yes_no('OK?', False, start_value=True) == expected
    assert '1: yes (current)' in out.getvalue()


def test_path_start(tmp_path: Path) -> None:
    """The base ask_path() starts with the start value of its options."""
    start = tmp_path / 'out.csv'
    bridge, out = _console([''])
    options = PathAskOptions(nullable=True, start_value=start)
    assert bridge.ask_path('File?', options=options) == start
    assert f'File? [{start}]' in out.getvalue()


def test_typed_start() -> None:
    """A typed field shows its formatted start value and keeps it."""
    bridge, _ = _console([''])
    field = AskFloatField('Rate?', None, nullable=True, start_value=2.5)
    assert bridge.ask_form('Q', [field])[0].value == 2.5


# A test double implements only the ask method its tests exercise.
# pylint: disable-next=abstract-method
class _OldBridge(WizardUiBridge):
    """A bridge whose ask_text() was written before start_value existed."""

    def __init__(self) -> None:
        """Start with an empty log of the arguments of ask_text()."""
        self.calls: list[tuple[bool, Optional[str]]] = []

    # The signature deliberately lacks start_value, as in a bridge written
    # before start_value existed, which is what the tests below exercise.
    # pylint: disable-next=too-many-arguments,arguments-differ
    def ask_text(self, question: str,  # type: ignore[override]
                 re_ask_reason: Optional[str] = None, nullable: bool = False,
                 *, default: Optional[str] = None, sensitive: bool = False,
                 help_text: Optional[str] = None) -> Optional[str]:
        """Record nullable and default, and give an empty answer."""
        self.calls.append((nullable, default))
        return default

    def show(self, message: str) -> None:
        """Ignore shown messages."""


def test_old_bridge() -> None:
    """An older bridge gets the start as default, not nullable, warned."""
    bridge = _OldBridge()
    field = AskTextField('Name?', None, nullable=True, start_value='Ada')
    with pytest.warns(DeprecationWarning, match='start_value'):
        answers = bridge.ask_form('Q', [field])
    assert bridge.calls == [(False, 'Ada')]
    assert answers[0].value == 'Ada'


def test_form_back() -> None:
    """A form field asked again after back starts with its answer."""
    bridge, out = _console(['x', ':b', '', 'y'])
    fields: list[AskField] = [AskTextField('A?', None),
                              AskTextField('B?', None)]
    answers = bridge.ask_form('Q', fields)
    assert [answer.value for answer in answers] == ['x', 'y']
    assert 'A? [x]' in out.getvalue()


@pytest.mark.parametrize('first, expected, shown', [
    ('', 3, 2), (':e', None, 1)])
def test_form_back_empty(first: str, expected: Optional[int],
                         shown: int) -> None:
    """A nullable field emptied before starts empty when asked again.

    A kept start value is shown again, an emptied one is not.
    """
    bridge, out = _console([first, ':b', '', 'y'])
    fields: list[AskField] = [
        AskIntField('A?', None, nullable=True, start_value=3),
        AskTextField('B?', None)]
    answers = bridge.ask_form('Q', fields)
    assert [answer.value for answer in answers] == [expected, 'y']
    assert out.getvalue().count('A? [3]') == shown


def _prefill_rule(_answers: Sequence[AnswerField],
                  changed: Optional[int]) -> PartFormValidationResult:
    """Prefill field 1 with 5 once field 0 is answered."""
    return PartFormValidationResult(True, '', (),
                                    ((1, 5),) if changed == 0 else ())


@pytest.mark.parametrize('line, expected', [('', 5), (':e', None)])
def test_form_prefill(line: str, expected: Optional[int]) -> None:
    """A prefilled nullable field stays nullable on the console."""
    bridge, out = _console(['x', line])
    fields: list[AskField] = [AskTextField('A?', None),
                              AskIntField('B?', None, nullable=True)]
    answers = bridge.ask_form('Q', fields, live_validator=_prefill_rule)
    assert answers[1].value == expected
    assert 'B? [5]' in out.getvalue()


def _matrix(cells: list[list[AskCell]],
            validator: Optional[PartialMatrixValidator] = None
            ) -> MatrixRequest:
    """Return a fixed one-row matrix request of cells."""
    return MatrixRequest('Q', cells, MatrixDimensions.fixed(1, len(cells[0])),
                         MatrixConsoleQuestion(False, False, False), validator)


def test_matrix_back() -> None:
    """A matrix cell asked again after back starts with its answer."""
    bridge, out = _console(['5', ':b', '', '7'])
    cells: list[list[AskCell]] = [[AskIntCell(None, default=1),
                                   AskIntCell(None)]]
    answers = bridge.ask_matrix_form(_matrix(cells))
    assert [cell.value for cell in answers[0] if cell] == [5, 7]
    assert '[5]' in out.getvalue()


def _matrix_prefill(_answers: AnswerCells, changed: Optional[CellPosition]
                    ) -> PartMatrixValidationRes:
    """Prefill cell (0, 1) with 5 once cell (0, 0) is answered."""
    prefill = (((CellPosition(0, 1), 5),)
               if changed == CellPosition(0, 0) else ())
    return PartMatrixValidationRes(True, '', prefill_values=prefill)


def test_matrix_prefill() -> None:
    """A prefilled nullable cell can still be emptied to None."""
    bridge, out = _console(['1', ':e'])
    cells: list[list[AskCell]] = [[AskIntCell(None),
                                   AskIntCell(None, nullable=True)]]
    answers = bridge.ask_matrix_form(_matrix(cells, _matrix_prefill))
    assert [cell.value for cell in answers[0] if cell] == [1, None]
    assert '[5]' in out.getvalue()


def test_matrix_back_first() -> None:
    """Back from the first cell still steps out of the matrix."""
    bridge, _ = _console([':b'])
    cells: list[list[AskCell]] = [[AskIntCell(None, start_value=2)]]
    with pytest.raises(WizardBack):
        bridge.ask_matrix_form(_matrix(cells))
