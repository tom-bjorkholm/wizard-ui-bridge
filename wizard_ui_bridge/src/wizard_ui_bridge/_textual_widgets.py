#! /usr/local/bin/python3
"""Header, id, message and calendar helpers for the Textual screens.

The Textual screens show a header of messages above each question, and
they map widget ids back to form field indexes and matrix cell positions.
These pure helpers are kept apart from the screen classes so the main
bridge module stays small; they hold no screen state. The input of a
field or cell is built by wizard_ui_bridge._textual_cell.

A form screen shows every field at once but reports validation in one
shared status line, so the message helper here names the field a message
complains about; without that name the user cannot tell which of the
fields on the screen to correct. A matrix screen names a cell with
wizard_ui_bridge.matrix_helpers.message_name() instead.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from datetime import date, datetime, time
from typing import Iterator, Optional, Sequence
from textual.widgets import Static
from wizard_ui_bridge._parse import parse_date, parse_datetime
from wizard_ui_bridge.form_defs import AskField
from wizard_ui_bridge.matrix_cell_defs import AskCell, AskDateCell, \
    AskDateTimeCell
from wizard_ui_bridge.matrix_defs import CellPosition

# The kinds of id that _id_numbers() reads: a field or cell input, and
# the Browse or Pick button beside one.
_INPUT_KINDS = ('field', 'cell', 'browse', 'pick')


def _header_widgets(messages: list[str], question: str) -> Iterator[Static]:
    """Yield one static line per message and one for the question."""
    for line in messages:
        yield Static(line)
    yield Static(question)


def _default_index(choices: Sequence[str],
                   default: Optional[str]) -> Optional[int]:
    """Return the index of default, one of choices, or None for none."""
    return None if default is None else list(choices).index(default)


def _preselected(choices: Sequence[str],
                 default: Optional[Sequence[str]]) -> list[int]:
    """Return the indexes of the default values within choices."""
    if default is None:
        return []
    wanted = set(default)
    return [index for index, choice in enumerate(choices)
            if choice in wanted]


def _id_numbers(widget_id: Optional[str]) -> tuple[int, ...]:
    """Return the numbers in the id of a field or cell input or its button.

    Such an id is its kind followed by one number for a form field, as in
    'field_3', or by a row and a column for a matrix cell, as in
    'pick_1_2'. Any other id, such as 'label_2' or 'path_input', gives no
    numbers.
    """
    if widget_id is None:
        return ()
    kind, *numbers = widget_id.split('_')
    if kind not in _INPUT_KINDS or not all(map(str.isdigit, numbers)):
        return ()
    return tuple(map(int, numbers))


def _field_index(widget_id: Optional[str]) -> Optional[int]:
    """Return the field index encoded in a field input or button id."""
    numbers = _id_numbers(widget_id)
    return numbers[0] if len(numbers) == 1 else None


def _cell_position(widget_id: Optional[str]) -> Optional[CellPosition]:
    """Return the cell position encoded in a cell input or button id."""
    numbers = _id_numbers(widget_id)
    return CellPosition(*numbers) if len(numbers) == 2 else None


def _field_message(field: AskField, message: str) -> str:
    """Return message named for the form field it complains about."""
    return f"Field '{field.short_question}': {message}"


def _date_of(value: Optional[date]) -> Optional[date]:
    """Return the date part of a date or datetime, or None."""
    if isinstance(value, datetime):
        return value.date()
    return value


def _calendar_setup(field: AskCell, text: str
                    ) -> tuple[date, Optional[date], Optional[date]]:
    """Return the calendar seed date and its inclusive day bounds.

    A date-time field's or cell's bounds are its date parts, so the
    calendar offers the acceptable days and the input validates the exact
    date-time.
    """
    if isinstance(field, AskDateCell):
        parsed = parse_date(text)
        minimum, maximum = field.min_value, field.max_value
    else:
        assert isinstance(field, AskDateTimeCell)
        parsed = _date_of(parse_datetime(text))
        minimum = _date_of(field.min_value)
        maximum = _date_of(field.max_value)
    seed = parsed or _date_of(field.default) or date.today()
    return (seed, minimum, maximum)


def _combined_text(field: AskCell, picked: date, current: str) -> str:
    """Return the input text for a picked date, keeping any typed time."""
    if isinstance(field, AskDateCell):
        return picked.isoformat()
    assert isinstance(field, AskDateTimeCell)
    existing = parse_datetime(current)
    clock = existing.time() if existing is not None else time()
    return datetime.combine(picked, clock).isoformat(sep=' ')
