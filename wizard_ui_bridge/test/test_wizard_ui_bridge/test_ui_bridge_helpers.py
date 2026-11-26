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
    ask_yes_no, run_table, CHOICE_ERROR, check_text_args, offered_choices, \
    NO_CHOICE, new_row_template

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


@pytest.mark.parametrize('answers, expected', [
    ([''], None), (['green'], 'green'), ([2], 'blue'), ([7, ''], None)])
def test_one_nullable(answers: list[str | int],
                      expected: Optional[str]) -> None:
    """A nullable single choice reports an empty answer as None."""
    reader = _Reader(answers)
    assert ask_one(reader.one, _COLORS, None, None, nullable=True) == expected


def test_one_null_default() -> None:
    """A nullable single choice with a default is a programming error."""
    with pytest.raises(ValueError, match='nullable'):
        ask_one(_Reader([]).one, _COLORS, 'red', None, nullable=True)


def test_one_bad_default() -> None:
    """A single-choice default that is not a choice is rejected."""
    reader = _Reader([])
    with pytest.raises(ValueError, match='one of choices'):
        ask_one(reader.one, _COLORS, 'pink', None)
    assert not reader.reasons


def test_many_bad_default() -> None:
    """A multi-choice default that is not a choice is rejected."""
    reader = _Reader([])
    with pytest.raises(ValueError, match='one of choices'):
        ask_many(reader.one, _COLORS, ['pink'], 0, None, None, True)
    assert not reader.reasons


def test_offered_choices() -> None:
    """A nullable list leads with the no-choice entry mapped to None.

    The mapping is by position, so a real choice that happens to carry
    the NO_CHOICE label keeps its own answer.
    """
    assert offered_choices(('a',), False) == [('a', 'a')]
    assert offered_choices(('a', NO_CHOICE), True) == \
        [(NO_CHOICE, None), ('a', 'a'), (NO_CHOICE, NO_CHOICE)]


@pytest.mark.parametrize('default, sensitive, nullable', [
    ('x', True, False), ('x', False, True)])
def test_text_args_bad(default: str, sensitive: bool, nullable: bool) -> None:
    """A text default is rejected with sensitive and with nullable."""
    with pytest.raises(ValueError, match='not allowed'):
        check_text_args(default, sensitive, nullable)


def test_text_args_good() -> None:
    """Nullable or sensitive without a default is accepted."""
    check_text_args(None, True, True)
    check_text_args('x', False)


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


def test_new_row_shared() -> None:
    """A new row keeps the members shared across each template column."""
    columns = (TableColumn('P', read_only=True), TableColumn('V'))
    cells = [[TableCell(value='a', choices=('a', 'b'), nullable=True),
              TableCell(value=None, nullable=True)],
             [TableCell(value='a', choices=('a', 'b'), nullable=True),
              TableCell(value=None, nullable=True)]]
    assert new_row_template(columns, cells) == cells[0]


@pytest.mark.parametrize('first, second, expected', [
    (TableCell(value='a', choices=('a', 'b')),
     TableCell(value='b', choices=('a', 'b')),
     TableCell(value=None, choices=('a', 'b'))),
    (TableCell(value='x'), TableCell(value='y'), TableCell(value='')),
    (TableCell(value='a', choices=('a',), nullable=True),
     TableCell(value='b', choices=('a', 'b')), TableCell(value=''))])
def test_new_row_fallback(first: TableCell, second: TableCell,
                          expected: TableCell) -> None:
    """Differing template members fall back to an empty, plain cell.

    The empty value is None when the column keeps its choices, since an
    empty string is not one of them, and an empty string otherwise.
    """
    columns = (TableColumn('V'),)
    assert new_row_template(columns, [[first], [second]]) == [expected]


def test_new_row_no_rows() -> None:
    """The template of a table with no rows is an empty free-text cell."""
    columns = (TableColumn('V'),)
    assert new_row_template(columns, []) == [TableCell(value='')]
