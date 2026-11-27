#! /usr/bin/env python3
"""Tests for start values in the Textual bridge.

Each single-question screen starts with the start value, else the
default, and a form shows each field's start value, else its default,
in its widget. Emptying a pre-filled widget gives what an empty answer
gives, so a nullable field still reports None.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

# pylint: disable=protected-access

from datetime import date
from pathlib import Path

import pytest

from wizard_ui_bridge import AskChoiceField, AskDateField, AskField, \
    AskIntField, AskMultiChoiceField, AskPathField, AskTextField, \
    AskYesNoField, PathAskOptions
from wizard_ui_bridge.textual_bridge import _ChoiceApp, _FormApp, \
    _MultiApp, _PathApp, _TextApp
from .ui_textual_support import drive, submit_typed, _CannedBridge, \
    _submitted


def test_text_start() -> None:
    """ask_text() pre-fills the start value; an emptied answer is None."""
    bridge = _CannedBridge([''])
    assert bridge.ask_text('q', nullable=True, start_value='Ada') is None
    app = bridge.launched[0]
    assert isinstance(app, _TextApp)
    assert app._value == 'Ada'


def test_path_start(tmp_path: Path) -> None:
    """ask_path() starts its input with the start value of its options."""
    start = tmp_path / 'out.csv'
    bridge = _CannedBridge([str(start)])
    options = PathAskOptions(nullable=True, start_value=start)
    assert bridge.ask_path('q', options=options) == start
    app = bridge.launched[0]
    assert isinstance(app, _PathApp)
    assert app._value == str(start)


@pytest.mark.parametrize('start, index', [(True, 0), (False, 1)])
def test_yes_no_start(start: bool, index: int) -> None:
    """ask_yes_no() highlights the start value, not the default."""
    bridge = _CannedBridge([0])
    bridge.ask_yes_no('q', default=not start, start_value=start)
    app = bridge.launched[0]
    assert isinstance(app, _ChoiceApp)
    assert app._default_index == index


@pytest.mark.parametrize('nullable, index', [(False, 2), (True, 3)])
def test_choice_start(nullable: bool, index: int) -> None:
    """ask_choice() highlights the start value, below '(none)' if any."""
    bridge = _CannedBridge([0])
    bridge.ask_choice('q', choices=['a', 'b', 'c'], nullable=nullable,
                      start_value='c')
    app = bridge.launched[0]
    assert isinstance(app, _ChoiceApp)
    assert app._default_index == index


def test_choice_named_none() -> None:
    """A start value named like '(none)' is found by its position."""
    bridge = _CannedBridge([0])
    bridge.ask_choice('q', choices=['a', '(none)'], nullable=True,
                      start_value='(none)')
    app = bridge.launched[0]
    assert isinstance(app, _ChoiceApp)
    assert app._default_index == 2


def test_multi_start() -> None:
    """ask_multi() preselects the start value instead of the default."""
    bridge = _CannedBridge([[2]])
    assert bridge.ask_multi('q', choices=['a', 'b', 'c'], default=['a'],
                            start_value=['b', 'c']) == ['c']
    app = bridge.launched[0]
    assert isinstance(app, _MultiApp)
    assert app._preselected == {1, 2}


def _start_form(tmp_path: Path) -> list[AskField]:
    """Return one field of each kind with a start value apart from default."""
    return [
        AskTextField('Name', None, nullable=True, start_value='Ada'),
        AskIntField('Age', None, default=30, start_value=40),
        AskPathField('File', None,
                     PathAskOptions(start_value=tmp_path / 'out.csv')),
        AskYesNoField('Sub?', None, False, start_value=True),
        AskChoiceField('Color', None, choices=('red', 'green'), nullable=True,
                       start_value='green'),
        AskMultiChoiceField('Tags', None, choices=('a', 'b'), default=('a',),
                            start_value=('b',)),
        AskDateField('Day', None, start_value=date(2027, 2, 3))]


def test_form_start(tmp_path: Path) -> None:
    """A form submitted unchanged returns each field's start value."""
    driven = drive(_FormApp('H', _start_form(tmp_path), [], None), ['#submit'])
    assert [answer.value for answer in _submitted(driven)] == \
        ['Ada', 40, tmp_path / 'out.csv', True, 'green', ['b'],
         date(2027, 2, 3)]


@pytest.mark.parametrize('field, expected', [
    (AskTextField('Name', None, nullable=True, start_value='Ada'), None),
    (AskIntField('Age', None, default=30, start_value=40), 30)])
def test_form_start_emptied(field: AskField, expected: object) -> None:
    """An emptied start value gives what an empty field gives."""
    assert _submitted(submit_typed([field], ''))[0].value == expected
