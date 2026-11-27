#! /usr/bin/env python3
"""Tests for the console help token ':?' and the help_text parameter.

The console bridge answers ':?' itself: it shows the help text of the
question, or a note that there is none, and asks the same question again.
The base class passes the help text of a form field, a matrix cell and a
resize menu through the keyword-only help_text parameter, and leaves it
out, with a DeprecationWarning, for a method or reader without it.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import warnings
from io import StringIO
from pathlib import Path
from typing import Callable, Optional, Sequence, cast

import pytest

from wizard_ui_bridge import AskField, AskFloatField, AskIntCell, \
    AskTextField, MatrixConsoleQuestion, MatrixDimension, MatrixDimensions, \
    MatrixRequest, TableCell, TableColumn, WizardBack, WizardUiBridgeConsole
from wizard_ui_bridge.arg_types import AskReader
from wizard_ui_bridge.bridge_helpers import run_table
from wizard_ui_bridge._help import help_kwargs

_HELP = 'Some helpful words.'
_NO_HELP = 'No help is available for this question.'
_HINT = '(:b=back  :c=cancel level  :q=abort  :?=help)'


def _console(lines: Sequence[str]
             ) -> tuple[WizardUiBridgeConsole, StringIO, StringIO]:
    """Return a console bridge answering with lines, and its out and err."""
    out, err = StringIO(), StringIO()
    stdin = StringIO(''.join(f'{line}\n' for line in lines))
    return WizardUiBridgeConsole(out, stdin, err), out, err


_ASKS: list[tuple[Callable[[WizardUiBridgeConsole], object], str, object]] = [
    (lambda b: b.ask_text('Q', help_text=_HELP), 'x', 'x'),
    (lambda b: b.ask_text('Q', sensitive=True, help_text=_HELP), 'pw', 'pw'),
    (lambda b: b.ask_int('Q', help_text=_HELP), '7', 7),
    (lambda b: b.ask_path('Q', help_text=_HELP), 'x.txt', Path('x.txt')),
    (lambda b: b.ask_yes_no('Q', True, help_text=_HELP), 'no', False),
    (lambda b: b.ask_choice('Q', choices=('a', 'b'), help_text=_HELP), '2',
     'b'),
    (lambda b: b.ask_multi('Q', choices=('a', 'b'), help_text=_HELP), '1',
     ['a'])]


@pytest.mark.parametrize('ask, answer, expected', _ASKS)
def test_help_reasks(ask: Callable[[WizardUiBridgeConsole], object],
                     answer: str, expected: object) -> None:
    """':?' shows the help text and asks the same question again."""
    bridge, out, _ = _console([':?', answer])
    assert ask(bridge) == expected
    assert out.getvalue().count(_HELP) == 1
    assert out.getvalue().count(_HINT) == 2


@pytest.mark.parametrize('help_text', [None, ''])
def test_no_help(help_text: Optional[str]) -> None:
    """Without a help text ':?' says that there is no help."""
    bridge, out, _ = _console([':?', 'x'])
    assert bridge.ask_text('Q', help_text=help_text) == 'x'
    assert _NO_HELP in out.getvalue()


def test_help_token_spaces() -> None:
    """The help token may be surrounded by spaces."""
    bridge, out, _ = _console(['  :?  ', 'x'])
    assert bridge.ask_text('Q', help_text=_HELP) == 'x'
    assert _HELP in out.getvalue()


def test_help_keeps_reason() -> None:
    """The re-ask reason is shown again with the repeated question."""
    bridge, _, err = _console([':?', 'x'])
    assert bridge.ask_text('Q', 'Bad.', help_text=_HELP) == 'x'
    assert err.getvalue() == 'Bad.\nBad.\n'


def test_help_then_back() -> None:
    """After help a navigation token still raises its request."""
    bridge, _, _ = _console([':?', ':b'])
    with pytest.raises(WizardBack):
        bridge.ask_text('Q', help_text=_HELP)


def test_form_help() -> None:
    """A form field shows its help first and again on request."""
    fields: list[AskField] = [AskTextField('Name', 'Name help.'),
                              AskFloatField('Rate', 'Rate help.')]
    bridge, out, _ = _console([':?', 'Bob', ':?', '1.5'])
    answers = bridge.ask_form('Long.', fields)
    assert [answer.value for answer in answers] == ['Bob', 1.5]
    assert out.getvalue().count('Name help.') == 2
    assert out.getvalue().count('Rate help.') == 2


def _matrix(use_help: bool, dims: MatrixDimensions) -> MatrixRequest:
    """Return a one-column request of cells with a help text."""
    console = MatrixConsoleQuestion(use_help, True, True)
    return MatrixRequest('Long.', [[AskIntCell('Cell help.', default=8)]],
                         dims, console)


@pytest.mark.parametrize('use_help, shown', [(False, 1), (True, 2)])
def test_matrix_help(use_help: bool, shown: int) -> None:
    """A matrix cell shows its help on request, and first if use_help."""
    bridge, out, _ = _console([':?', '3'])
    answers = bridge.ask_matrix_form(_matrix(use_help,
                                             MatrixDimensions.fixed(1, 1)))
    cell = answers[0][0]
    assert cell is not None and cell.value == 3
    assert out.getvalue().count('Cell help.') == shown


def test_matrix_menu_help() -> None:
    """The resize menu explains its actions on request."""
    dims = MatrixDimensions(MatrixDimension(1, 1), MatrixDimension(2, 1),
                            MatrixDimension(1, 1))
    bridge, out, _ = _console(['3', ':?', ''])
    bridge.ask_matrix_form(_matrix(False, dims))
    assert 'Done accepts the matrix as it is.' in out.getvalue()
    assert 'Append adds a row or column' in out.getvalue()


def test_var_table_help() -> None:
    """The row menu explains its actions, then shows the table help."""
    bridge, out, _ = _console([':?', ''])
    table = bridge.ask_table((TableColumn('A'),), [[TableCell(value='a')]],
                             'Q:', min_rows=0, max_rows=3,
                             help_text='Table help.')
    assert table == [['a']]
    assert 'keep 0 to 3 rows.\nTable help.' in out.getvalue()


@pytest.mark.parametrize('min_rows, max_rows, lines', [
    (None, None, [':?', 'v']), (0, 3, ['1', ':?', 'v', ''])])
def test_table_cell_help(min_rows: Optional[int], max_rows: Optional[int],
                         lines: list[str]) -> None:
    """A cell of a fixed or variable-row table shows the table help."""
    bridge, out, _ = _console(lines)
    table = bridge.ask_table((TableColumn('A'),), [[TableCell(value='a')]],
                             'Q:', min_rows=min_rows, max_rows=max_rows,
                             help_text='Table help.')
    assert table == [['v']]
    assert out.getvalue().count('Table help.') == 1


def _named(*, help_text: Optional[str] = None) -> None:
    """Stand for an ask method that takes help_text by name."""
    _ = help_text


def _any_keyword(**kwargs: Optional[str]) -> None:
    """Stand for an ask method that takes any keyword argument."""
    _ = kwargs


def _old(question: str) -> None:
    """Stand for an ask method written before help_text existed."""
    _ = question


@pytest.mark.parametrize('method', [_named, _any_keyword])
def test_kwargs_accepted(method: Callable[..., None]) -> None:
    """A method that takes help_text gets it, without any warning."""
    with warnings.catch_warnings():
        warnings.simplefilter('error')
        assert help_kwargs(method, _HELP) == {'help_text': _HELP}


def test_kwargs_old_warns() -> None:
    """A method without help_text gets nothing, and a warning names it."""
    with pytest.warns(DeprecationWarning, match='_old'):
        assert not help_kwargs(_old, _HELP)


def _ignore(message: str) -> None:
    """Ignore a message the table helper shows to the user."""
    _ = message


class _OldBridge(WizardUiBridgeConsole):
    """A console bridge whose ask_text() predates help_text."""

    # pylint: disable-next=arguments-differ,too-many-arguments
    def ask_text(self, question: str,  # type: ignore[override]
                 re_ask_reason: Optional[str] = None, nullable: bool = False,
                 *, default: Optional[str] = None,
                 sensitive: bool = False) -> Optional[str]:
        """Ask for text, without any help."""
        return super().ask_text(question, re_ask_reason, nullable,
                                default=default, sensitive=sensitive)


def test_old_bridge_works() -> None:
    """The base ask_int() still works on a bridge without help_text."""
    bridge = _OldBridge(StringIO(), StringIO('7\n'), StringIO())
    with pytest.warns(DeprecationWarning, match='_OldBridge.ask_text'):
        assert bridge.ask_int('Q', help_text=_HELP) == 7


def test_old_reader_works() -> None:
    """run_table() still works with a reader without help_text."""
    def reader(question: str, reason: Optional[str],
               choices: Optional[Sequence[str]]) -> str | int:
        _ = (question, reason, choices)
        return 'v'
    with pytest.warns(DeprecationWarning):
        table = run_table(cast(AskReader, reader), _ignore,
                          (TableColumn('A'),), [[TableCell(value='a')]], 'Q:',
                          None, None, _HELP)
    assert table == [['v']]
