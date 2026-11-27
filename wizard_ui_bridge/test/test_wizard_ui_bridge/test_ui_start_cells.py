#! /usr/bin/env python3
"""Tests for the start value of cells, fields and the raw-answer helpers.

A start value is where an input starts, separate from the default that
an empty answer gives. These tests cover its validation on the cells and
fields, the start_or_default properties, the initial answer, the shared
bridge_helpers functions that read a raw answer with a start value, and
start_args(), which falls back to the default for an older bridge.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from datetime import date
from pathlib import Path
from typing import Callable, Optional, Sequence

import pytest

from wizard_ui_bridge import AskChoiceCell, AskDateCell, AskIntCell, \
    AskMultiChoiceCell, AskPathField, AskTextCell, AskTextField, \
    AskYesNoCell, PathAskOptions, WizardUiBridge
from wizard_ui_bridge.bridge_helpers import ask_many, ask_one, ask_yes_no, \
    check_text_args, text_answer
from wizard_ui_bridge.form_helpers import initial_answer
from wizard_ui_bridge._start import start_args

_ABC = ('a', 'b', 'c')


@pytest.mark.parametrize('make, message', [
    (lambda: AskIntCell(None, min_value=1, max_value=5, start_value=9),
     'start_value is out of the allowed range'),
    (lambda: AskDateCell(None, min_value=date(2026, 1, 1),
                         start_value=date(2025, 1, 1)),
     'start_value is out of the allowed range'),
    (lambda: AskChoiceCell(None, _ABC, start_value='x'),
     'start_value must be one of choices'),
    (lambda: AskMultiChoiceCell(None, _ABC, start_value=['x']),
     'every start_value value must be one of choices'),
    (lambda: AskMultiChoiceCell(None, _ABC, start_value=['a', 'a']),
     'start_value must not name a choice twice'),
    (lambda: AskMultiChoiceCell(None, _ABC, max_select=1,
                                start_value=['a', 'b']),
     'start_value must not name more than max_select'),
    (lambda: AskTextCell(None, sensitive=True, start_value='x'),
     'cannot have a start_value')])
def test_bad_start(make: Callable[[], object], message: str) -> None:
    """A start value breaking the rules of a default is rejected."""
    with pytest.raises(ValueError, match=message):
        make()


@pytest.mark.parametrize('cell', [
    AskTextCell(None, nullable=True, start_value='x'),
    AskIntCell(None, nullable=True, start_value=3),
    AskChoiceCell(None, _ABC, nullable=True, start_value='b'),
    AskPathField('P', None, PathAskOptions(nullable=True,
                                           start_value=Path('f')))])
def test_nullable_start(cell: object) -> None:
    """Unlike a default, a start value may be combined with nullable.

    Building each cell in the parameters above raises no ValueError.
    """
    assert cell is not None


def test_default_with_start() -> None:
    """A start value may differ from the default; it wins at the start."""
    cell = AskIntCell(None, default=1, start_value=2)
    assert (cell.default, cell.start_or_default) == (1, 2)
    assert AskIntCell(None, default=1).start_or_default == 1


@pytest.mark.parametrize('cell, expected', [
    (AskYesNoCell(None, False, start_value=True), True),
    (AskYesNoCell(None, True), True),
    (AskChoiceCell(None, _ABC, default='a', start_value='c'), 'c'),
    (AskMultiChoiceCell(None, _ABC, default=['a'], start_value=[]), []),
    (AskMultiChoiceCell(None, _ABC), None)])
def test_start_or_default(cell: AskYesNoCell | AskChoiceCell
                          | AskMultiChoiceCell, expected: object) -> None:
    """start_or_default is the start value, else the default."""
    assert cell.start_or_default == expected


def test_path_start() -> None:
    """The PathAskOptions hold the start value of a path question."""
    options = PathAskOptions(default=Path('d'), start_value=Path('s'))
    assert options.start_or_default == Path('s')
    assert PathAskOptions(default=Path('d')).start_or_default == Path('d')


def test_field_start() -> None:
    """A form field inherits the keyword-only start value of its cell."""
    field = AskTextField('Name?', None, nullable=True, start_value='Ada')
    assert (field.nullable, field.start_value) == (True, 'Ada')


@pytest.mark.parametrize('cell, value', [
    (AskTextCell(None, nullable=True, start_value='x'), 'x'),
    (AskMultiChoiceCell(None, _ABC, default=['a'], start_value=['b']),
     ['b']),
    (AskPathField('P', None, PathAskOptions(start_value=Path('f'))),
     Path('f'))])
def test_initial_answer(cell: AskTextCell | AskMultiChoiceCell
                        | AskPathField, value: object) -> None:
    """The initial answer of a cell or field is its start value."""
    assert initial_answer(cell).value == value


def test_text_args_start() -> None:
    """check_text_args() rejects a start value for sensitive input."""
    with pytest.raises(ValueError, match='start_value is not allowed'):
        check_text_args(None, True, False, 'x')
    check_text_args(None, False, True, 'x')


@pytest.mark.parametrize('text, nullable, default, expected', [
    ('', False, None, 'S'),
    ('', True, None, 'S'),
    (':e', True, None, None),
    (' :E ', False, 'D', 'D'),
    (':e', False, None, ''),
    ('new', True, None, 'new')])
def test_text_answer(text: str, nullable: bool, default: Optional[str],
                     expected: Optional[str]) -> None:
    """Enter keeps a start value, and ':e' is the empty answer."""
    assert text_answer(text, nullable, default, 'S') == expected


def test_text_no_start() -> None:
    """Without a start value ':e' is ordinary text."""
    assert text_answer(':e', True, None) == ':e'
    assert text_answer('', True, None) is None


def _reader(answers: Sequence[str | int]
            ) -> Callable[[Optional[str]], str | int]:
    """Return a reader that gives the scripted answers in turn."""
    queue = list(answers)

    def read(_reason: Optional[str]) -> str | int:
        return queue.pop(0)
    return read


@pytest.mark.parametrize('answers, nullable, expected', [
    ([''], False, 'b'),
    ([':e'], True, None),
    ([':e', 2], False, 'c'),
    ([0], True, 'a')])
def test_ask_one_start(answers: list[str | int], nullable: bool,
                       expected: Optional[str]) -> None:
    """ask_one() keeps a start value on Enter and empties it on ':e'.

    An emptied answer with no default and not nullable is asked again.
    """
    assert ask_one(_reader(answers), _ABC, None, None, nullable=nullable,
                   start_value='b') == expected


def test_ask_one_numeric() -> None:
    """A start value is kept by name, even when it looks like an index."""
    assert ask_one(_reader(['']), ('1', '0'), None, None,
                   start_value='0') == '0'


@pytest.mark.parametrize('answers, start, min_select, expected', [
    ([''], ['a', 'c'], 0, ['a', 'c']),
    ([''], [], 0, []),
    ([':e'], ['b'], 0, []),
    ([':e', 'c'], ['b'], 1, ['c']),
    (['a'], ['b'], 0, ['a'])])
def test_ask_many_start(answers: list[str | int], start: list[str],
                        min_select: int, expected: list[str]) -> None:
    """ask_many() keeps a start value; ':e' selects nothing, not default."""
    assert ask_many(_reader(answers), _ABC, ['a'], min_select, None, None,
                    one_based=False, start_value=start) == expected


@pytest.mark.parametrize('answers, expected', [
    ([''], True), ([':e'], False), (['no'], False)])
def test_yes_no_start(answers: list[str | int], expected: bool) -> None:
    """ask_yes_no() keeps a start value; ':e' gives the default."""
    assert ask_yes_no(_reader(answers), False, None, True) == expected


def _old_ask(question: str, *, default: Optional[str] = None) -> str:
    """Stand for an ask method written before start_value existed."""
    return default or question


def test_start_args_none() -> None:
    """With no start value, default and nullable pass unchanged."""
    assert start_args(_old_ask, None, 'D', False) == ('D', False, {})


def test_start_args_new() -> None:
    """A method that takes start_value gets it next to default."""
    assert start_args(WizardUiBridge.ask_text, 'S', None, True) == \
        (None, True, {'start_value': 'S'})


def test_start_args_old() -> None:
    """An older method gets the start as default, not nullable, warned."""
    with pytest.warns(DeprecationWarning, match='_old_ask'):
        assert start_args(_old_ask, 'S', None, True) == ('S', False, {})
