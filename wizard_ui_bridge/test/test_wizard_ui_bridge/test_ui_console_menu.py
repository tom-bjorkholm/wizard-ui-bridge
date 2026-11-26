#! /usr/bin/env python3
"""Tests for the console single-choice and multi-choice menus.

These cover how the console bridge turns a menu answer into choices: by
number, by name and by an unambiguous prefix, what an empty answer
selects, the no-choice line 0 of a nullable choice, and the messages
shown when an answer names no choice or picks a number of choices the
question does not allow.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from io import StringIO
from typing import Optional

import pytest

from wizard_ui_bridge import WizardUiBridgeConsole, AskChoiceField, \
    AnswerChoiceField
from wizard_ui_bridge.bridge_helpers import CHOICE_ERROR

_COLORS = ('red', 'green', 'blue')


def _menu(answers: str) -> tuple[WizardUiBridgeConsole, StringIO, StringIO]:
    """Return a console bridge scripted with answers and its streams."""
    out_file = StringIO()
    err_file = StringIO()
    bridge = WizardUiBridgeConsole(out_file, StringIO(answers), err_file)
    return bridge, out_file, err_file


@pytest.mark.parametrize('answer, expected', [
    ('2', 'green'), ('green', 'green'), ('gr', 'green'), ('GREEN', 'green')])
def test_choice_answer(answer: str, expected: str) -> None:
    """One console choice is named by number, by name or by prefix."""
    bridge, _, _ = _menu(answer + '\n')
    assert bridge.ask_choice('Color?', choices=_COLORS) == expected


def test_choice_default() -> None:
    """An empty console choice answer selects the marked default."""
    bridge, out_file, _ = _menu('\n')
    chosen = bridge.ask_choice('Color?', choices=_COLORS, default='blue')
    assert chosen == 'blue'
    assert '3: blue (default)' in out_file.getvalue()


def test_bad_defaults() -> None:
    """A console default that is not a choice is rejected before asking."""
    bridge, out_file, _ = _menu('')
    with pytest.raises(ValueError, match='one of choices'):
        bridge.ask_choice('Color?', choices=_COLORS, default='pink')
    with pytest.raises(ValueError, match='one of choices'):
        bridge.ask_multi('Color?', choices=_COLORS, default=['pink'])
    assert out_file.getvalue() == ''


@pytest.mark.parametrize('answer', ['pink', '0', '4', '-1', ''])
def test_choice_rejected(answer: str) -> None:
    """A console answer naming no choice re-asks with the choice error."""
    bridge, _, err_file = _menu(answer + '\n2\n')
    assert bridge.ask_choice('Color?', choices=_COLORS) == 'green'
    assert CHOICE_ERROR in err_file.getvalue()


def test_choice_first_reason() -> None:
    """An initial re-ask reason is shown before the first console menu."""
    bridge, _, err_file = _menu('1\n')
    bridge.ask_choice('Color?', choices=_COLORS, re_ask_reason='again')
    assert 'again' in err_file.getvalue()


@pytest.mark.parametrize('answer, expected', [
    ('1,3', ['red', 'blue']), ('3,1', ['red', 'blue']),
    ('red,red', ['red']), ('gr, bl', ['green', 'blue']),
    ('2,,3', ['green', 'blue']), ('', [])])
def test_multi_answer(answer: str, expected: list[str]) -> None:
    """A console multi answer maps numbers and names to listed choices.

    The selection is reported in the order the choices were offered, and
    a choice named twice is selected once.
    """
    bridge, _, _ = _menu(answer + '\n')
    assert bridge.ask_multi('Colors?', choices=_COLORS) == expected


def test_multi_default() -> None:
    """An empty console multi answer selects the marked defaults."""
    bridge, out_file, _ = _menu('\n')
    chosen = bridge.ask_multi('Colors?', choices=_COLORS,
                              default=('blue', 'red'))
    assert chosen == ['red', 'blue']
    assert '1: red (default)' in out_file.getvalue()
    assert '3: blue (default)' in out_file.getvalue()


def test_multi_unknown() -> None:
    """A console multi answer naming no choice re-asks with guidance."""
    bridge, _, err_file = _menu('red,pink\n1\n')
    assert bridge.ask_multi('Colors?', choices=_COLORS) == ['red']
    assert CHOICE_ERROR in err_file.getvalue()


@pytest.mark.parametrize('answer, low, high, reason', [
    ('1', 2, None, 'Please select at least 2.'),
    ('1', 2, 2, 'Please select exactly 2.'),
    ('1,2,3', 1, 2, 'Please select between 1 and 2.'),
    ('', 1, None, 'Please select at least 1.')])
def test_multi_count(answer: str, low: int, high: Optional[int],
                     reason: str) -> None:
    """A console multi selection outside the allowed count re-asks."""
    bridge, _, err_file = _menu(answer + '\n1,2\n')
    chosen = bridge.ask_multi('Colors?', choices=_COLORS, min_select=low,
                              max_select=high)
    assert chosen == ['red', 'green']
    assert reason in err_file.getvalue()


@pytest.mark.parametrize('answer, expected', [
    ('0', None), ('', None), ('2', 'green'), ('blue', 'blue')])
def test_null_choice(answer: str, expected: Optional[str]) -> None:
    """A nullable console choice reports 0 or an empty answer as None."""
    bridge, _, _ = _menu(answer + '\n')
    chosen = bridge.ask_choice('Color?', choices=_COLORS, nullable=True)
    assert chosen == expected


def test_null_choice_menu() -> None:
    """A nullable console choice lists the no-choice line 0 first."""
    bridge, out_file, _ = _menu('0\n')
    bridge.ask_choice('Color?', choices=_COLORS, nullable=True)
    assert '0: (none)\n1: red\n' in out_file.getvalue()


def test_null_choice_reask() -> None:
    """A nullable console choice still re-asks an unknown answer."""
    bridge, _, err_file = _menu('4\n0\n')
    assert bridge.ask_choice('Color?', choices=_COLORS, nullable=True) is None
    assert CHOICE_ERROR in err_file.getvalue()


def test_plain_choice_no_none() -> None:
    """A console choice that is not nullable shows no line 0."""
    bridge, out_file, _ = _menu('1\n')
    bridge.ask_choice('Color?', choices=_COLORS)
    assert '0: (none)' not in out_file.getvalue()


def test_null_choice_default() -> None:
    """A nullable console choice with a default is a programming error."""
    bridge, _, _ = _menu('')
    with pytest.raises(ValueError, match='nullable'):
        bridge.ask_choice('Color?', choices=_COLORS, default='red',
                          nullable=True)


def test_text_null_default() -> None:
    """A nullable console text question with a default is rejected."""
    bridge, _, _ = _menu('')
    with pytest.raises(ValueError, match='nullable'):
        bridge.ask_text('Name?', nullable=True, default='x')


@pytest.mark.parametrize('answer, expected', [('\n', None), ('3\n', 'blue')])
def test_null_choice_form(answer: str, expected: Optional[str]) -> None:
    """The console form asks a nullable choice field with line 0."""
    bridge, out_file, _ = _menu(answer)
    field = AskChoiceField('Color', None, choices=_COLORS, nullable=True)
    answers = bridge.ask_form('Fill in', [field])
    assert answers == [AnswerChoiceField(field, expected)]
    assert '0: (none)' in out_file.getvalue()
