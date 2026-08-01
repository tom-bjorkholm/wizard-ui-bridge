#! /usr/bin/env python3
"""Tests for the raw answer shapes the public bridge helpers accept.

A bridge reports a raw answer as text or as a 0-based index into the
choices it offered, and a yes/no bridge with a real two-state control
may report a bool. The bundled console bridge never reports a bool and
reports an index only from a numbered menu, so these tests drive the
public helpers directly with a scripted reader to cover the shapes a
bridge of one's own may report.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional, Sequence

import pytest

from wizard_ui_bridge import TableCell, TableColumn
from wizard_ui_bridge.bridge_helpers import ask_many, ask_one, \
    ask_yes_no, run_table, CHOICE_ERROR

_COLORS = ('red', 'green', 'blue')
_NEEDED = 'Please enter a value.'


class _Reader:
    """A scripted reader of raw answers recording its re-ask reasons."""

    def __init__(self, answers: Sequence[str | int]) -> None:
        """Store the scripted answers and start with no recorded reason."""
        self.answers = list(answers)
        self.reasons: list[Optional[str]] = []

    def one(self, reason: Optional[str]) -> str | int:
        """Return the next answer to a question reader."""
        self.reasons.append(reason)
        return self.answers.pop(0)

    def cell(self, question: str, reason: Optional[str] = None,
             choices: Optional[Sequence[str]] = None) -> str | int:
        """Return the next answer to a table cell reader."""
        _ = (question, choices)
        return self.one(reason)


def _ignore(message: str) -> None:
    """Ignore a message the table helper shows to the user."""
    _ = message


def _many(reader: _Reader, one_based: bool) -> list[str]:
    """Ask a multi choice over the colours through a scripted reader."""
    return ask_many(reader.one, _COLORS, None, 0, None, None, one_based)


@pytest.mark.parametrize('answer, default', [(True, False), (False, True)])
def test_yes_no_bool(answer: bool, default: bool) -> None:
    """A bridge with a real yes/no control may answer with a bool."""
    reader = _Reader([answer])
    assert ask_yes_no(reader.one, default, None) is answer


@pytest.mark.parametrize('answer, expected', [
    (0, True), (1, False), ('', True)])
def test_yes_no_shapes(answer: str | int, expected: bool) -> None:
    """A yes/no answer may be a menu index, and blank takes the default."""
    reader = _Reader([answer])
    assert ask_yes_no(reader.one, True, None) is expected


def test_yes_no_bad_index() -> None:
    """A yes/no index outside the two choices asks the question again."""
    reader = _Reader([7, 1])
    assert ask_yes_no(reader.one, True, 'first') is False
    assert reader.reasons == ['first', 'Please answer yes or no.']


def test_one_bool() -> None:
    """A bool is no choice index, so a single choice is asked again."""
    reader = _Reader([True, 1])
    assert ask_one(reader.one, _COLORS, None, None) == 'green'
    assert reader.reasons == [None, CHOICE_ERROR]


@pytest.mark.parametrize('answer, expected', [(0, 'red'), (2, 'blue')])
def test_one_index(answer: int, expected: str) -> None:
    """A single choice may be answered with a 0-based choice index."""
    reader = _Reader([answer])
    assert ask_one(reader.one, _COLORS, None, None) == expected


def test_many_bool() -> None:
    """A bool is no choice index, so a multi choice is asked again."""
    reader = _Reader([False, '1'])
    assert _many(reader, True) == ['red']
    assert reader.reasons == [None, CHOICE_ERROR]


@pytest.mark.parametrize('answer, expected', [(0, ['red']), (2, ['blue'])])
def test_many_index(answer: int, expected: list[str]) -> None:
    """A multi choice may be answered with one 0-based choice index."""
    assert _many(_Reader([answer]), False) == expected


def test_many_bad_index() -> None:
    """A multi choice index outside the choices is asked again."""
    reader = _Reader([9, 1])
    assert _many(reader, False) == ['green']
    assert reader.reasons == [None, CHOICE_ERROR]


def test_cell_bool() -> None:
    """A bool is no cell value, so the table cell is asked again."""
    reader = _Reader([True, 'text'])
    cells = [[TableCell(value='a')]]
    table = run_table(reader.cell, _ignore, (TableColumn('A'),), cells, 'Q:',
                      None, None)
    assert table == [['text']]
    assert reader.reasons == [None, _NEEDED]
