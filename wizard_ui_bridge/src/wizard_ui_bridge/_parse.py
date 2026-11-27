#! /usr/local/bin/python3
"""Text parsing and formatting for the typed form fields and cells.

The float, date, time, date-time and duration form fields and matrix
cells all need to turn user text into a typed value and a typed value
back into text. This module holds that shared conversion, together with
the human-readable hints and error messages, so the console form, the
Textual form and matrix form and the ask_form_w_fake() fallback all agree
on the accepted text. Every Ask*Field derives from its Ask*Cell, so each
function taking a cell takes a field too.

A duration is written as an optional day count and a clock part,
``<days> d <hours>:<minutes>:<seconds>``, where the seconds may carry a
decimal fraction, or as a single non-negative number of seconds. Dates,
times and date-times use the ISO 8601 forms accepted by the standard
library fromisoformat() parsers.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import math
import re
from datetime import date, datetime, time, timedelta
from typing import Callable, Optional, Protocol, TypeVar
from wizard_ui_bridge.matrix_cell_defs import value_out_of_range, \
    _OrderedValue, PrefillValueType, AskCell, AskFloatCell, AskDateCell, \
    AskTimeCell, AskDateTimeCell, AskDurationCell
from wizard_ui_bridge.form_defs import AskField, AnswerField, AskTextField, \
    AskFloatField, AskDateField, AskTimeField, AskDateTimeField, \
    AskDurationField, AnswerFloatField, AnswerDateField, AnswerTimeField, \
    AnswerDateTimeField, AnswerDurationField
from wizard_ui_bridge._help import help_kwargs
from wizard_ui_bridge._start import start_args

FLOAT_HINT = 'a number'
DATE_HINT = 'a date as YYYY-MM-DD'
TIME_HINT = 'a time as HH:MM or HH:MM:SS'
DATETIME_HINT = 'a date and time as YYYY-MM-DD HH:MM:SS'
DURATION_HINT = "a duration as '<days> d HH:MM:SS' or a number of seconds"

NEW_FIELD_TYPES = (AskFloatField, AskDateField, AskTimeField,
                   AskDateTimeField, AskDurationField)
"""The typed form field classes added on top of the original six."""

NEW_CELL_TYPES = (AskFloatCell, AskDateCell, AskTimeCell, AskDateTimeCell,
                  AskDurationCell)
"""The typed cell classes, each the base of one of NEW_FIELD_TYPES."""

_OrderedT = TypeVar('_OrderedT', bound=_OrderedValue)
_DURATION_RE = re.compile(r'^(?:(\d+)\s*d\s+)?(\d+):(\d+):(\d+(?:\.\d+)?)$')


def parse_float(text: str) -> Optional[float]:
    """Return a finite float from text, or None when not a number."""
    try:
        value = float(text.strip())
    except ValueError:
        return None
    return value if math.isfinite(value) else None


def parse_date(text: str) -> Optional[date]:
    """Return an ISO date from text, or None when not a valid date."""
    try:
        return date.fromisoformat(text.strip())
    except ValueError:
        return None


def parse_time(text: str) -> Optional[time]:
    """Return an ISO time from text, or None when not a valid time."""
    try:
        return time.fromisoformat(text.strip())
    except ValueError:
        return None


def parse_datetime(text: str) -> Optional[datetime]:
    """Return an ISO date-time from text, or None when not valid."""
    try:
        return datetime.fromisoformat(text.strip())
    except ValueError:
        return None


def parse_duration(text: str) -> Optional[timedelta]:
    """Return a duration from text, or None when it is not valid.

    A lone non-negative number is read as a count of seconds; otherwise
    the text must be ``<hours>:<minutes>:<seconds>`` with an optional
    ``<days> d`` prefix, and the seconds may carry a decimal fraction.
    """
    stripped = text.strip()
    seconds = parse_float(stripped)
    if seconds is not None:
        return _timedelta_seconds(seconds)
    match = _DURATION_RE.match(stripped)
    return None if match is None else _timedelta_parts(match.groups())


def _timedelta_seconds(seconds: float) -> Optional[timedelta]:
    """Return a duration of seconds seconds, or None when unusable."""
    if seconds < 0:
        return None
    try:
        return timedelta(seconds=seconds)
    except OverflowError:
        return None


def _timedelta_parts(groups: tuple[Optional[str], ...]) -> Optional[timedelta]:
    """Return a duration built from matched day and clock groups."""
    days, hours, minutes, seconds = groups
    assert hours is not None and minutes is not None and seconds is not None
    try:
        return timedelta(days=int(days or 0), hours=int(hours),
                         minutes=int(minutes), seconds=float(seconds))
    except OverflowError:
        return None


def format_duration(value: timedelta) -> str:
    """Return a duration as ``<days> d HH:MM:SS`` with any fraction."""
    hours, rest = divmod(value.seconds, 3600)
    minutes, seconds = divmod(rest, 60)
    text = f'{value.days} d {hours:02d}:{minutes:02d}:{seconds:02d}'
    if value.microseconds:
        return f'{text}.{value.microseconds:06d}'.rstrip('0')
    return text


def format_new_value(value: object) -> str:
    """Return the text a typed value would round-trip from."""
    if isinstance(value, timedelta):
        return format_duration(value)
    return str(value)


def ordered_range_error(minimum: Optional[object],
                        maximum: Optional[object]) -> str:
    """Return the message shown when a typed value is out of range."""
    low = None if minimum is None else format_new_value(minimum)
    high = None if maximum is None else format_new_value(maximum)
    if low is None:
        return f'Please enter a value at most {high}.'
    if high is None:
        return f'Please enter a value at least {low}.'
    return f'Please enter a value between {low} and {high}.'


# pylint: disable-next=too-few-public-methods
class _AskText(Protocol):
    """The bridge ask_text() signature the typed re-ask loop calls."""

    # pylint: disable-next=too-many-arguments
    def __call__(self, question: str, re_ask_reason: Optional[str] = ...,
                 nullable: bool = ..., *, default: Optional[str] = ...,
                 start_value: Optional[str] = ...,
                 help_text: Optional[str] = ...) -> Optional[str]:
        """Ask for free text and return it, or None for an empty answer."""


# pylint: disable-next=too-few-public-methods
class _TypedCell(Protocol[_OrderedT]):
    """The attributes shared by the ordered typed cells and fields."""

    help_text: Optional[str]
    nullable: bool
    default: Optional[_OrderedT]
    min_value: Optional[_OrderedT]
    max_value: Optional[_OrderedT]
    start_value: Optional[_OrderedT]


def ask_typed(ask_text: _AskText, question: str, field: _TypedCell[_OrderedT],
              parse: Callable[[str], Optional[_OrderedT]],
              hint: str) -> Optional[_OrderedT]:
    """Re-ask a typed field or cell through ask_text until it is usable.

    The hint is shown after the question and repeated in the parse-error
    message, so a console user learns the accepted text format. An empty
    answer yields the field default, or None when the field is nullable.
    The help text of the field is passed to ask_text as help_text, and
    its start value, formatted as text, as start_value.
    """
    question = f'{question} ({hint})'
    start, default = _formatted(field.start_value), _formatted(field.default)
    args = start_args(ask_text, start, default, field.nullable)
    reason: Optional[str] = None
    extra = help_kwargs(ask_text, field.help_text)
    while True:
        text = ask_text(question, reason, args.nullable, default=args.default,
                        **args.kwargs, **extra)
        if text is None:
            return None
        value = parse(text)
        if value is None:
            reason = f'Please enter {hint}.'
        elif value_out_of_range(value, field.min_value, field.max_value):
            reason = ordered_range_error(field.min_value, field.max_value)
        else:
            return value


def _resolve(value: Optional[_OrderedT], minimum: Optional[_OrderedT],
             maximum: Optional[_OrderedT],
             hint: str) -> tuple[Optional[_OrderedT], Optional[str]]:
    """Return a parsed value and no error, or None and the reason why."""
    if value is None:
        return (None, f'Please enter {hint}.')
    if value_out_of_range(value, minimum, maximum):
        return (None, ordered_range_error(minimum, maximum))
    return (value, None)


def resolve_new(field: AskCell, text: Optional[str]
                ) -> tuple[Optional[PrefillValueType], Optional[str]]:
    """Return the typed value for a typed field's or cell's text, and error.

    A None text is an empty nullable answer, which is valid and has no
    value. Otherwise the text is parsed and range-checked for the field's
    type; the error is the reason to re-ask when the value is not usable.
    """
    if text is None:
        return (None, None)
    if isinstance(field, AskFloatCell):
        return _resolve(parse_float(text), field.min_value, field.max_value,
                        FLOAT_HINT)
    if isinstance(field, AskDateCell):
        return _resolve(parse_date(text), field.min_value, field.max_value,
                        DATE_HINT)
    if isinstance(field, AskTimeCell):
        return _resolve(parse_time(text), field.min_value, field.max_value,
                        TIME_HINT)
    if isinstance(field, AskDateTimeCell):
        return _resolve(parse_datetime(text), field.min_value, field.max_value,
                        DATETIME_HINT)
    assert isinstance(field, AskDurationCell)
    return _resolve(parse_duration(text), field.min_value, field.max_value,
                    DURATION_HINT)


def new_answer(field: AskField, value: Optional[object]) -> AnswerField:
    """Wrap a typed value in the answer matching a typed field."""
    if isinstance(field, AskFloatField):
        assert value is None or isinstance(value, float)
        return AnswerFloatField(field, value)
    if isinstance(field, AskDateField):
        assert value is None or isinstance(value, date)
        return AnswerDateField(field, value)
    if isinstance(field, AskTimeField):
        assert value is None or isinstance(value, time)
        return AnswerTimeField(field, value)
    if isinstance(field, AskDateTimeField):
        assert value is None or isinstance(value, datetime)
        return AnswerDateTimeField(field, value)
    assert isinstance(field, AskDurationField)
    assert value is None or isinstance(value, timedelta)
    return AnswerDurationField(field, value)


def field_hint(field: AskCell) -> str:
    """Return the format hint shown for a typed field or cell."""
    if isinstance(field, AskFloatCell):
        return FLOAT_HINT
    if isinstance(field, AskDateCell):
        return DATE_HINT
    if isinstance(field, AskTimeCell):
        return TIME_HINT
    if isinstance(field, AskDateTimeCell):
        return DATETIME_HINT
    assert isinstance(field, AskDurationCell)
    return DURATION_HINT


def _new_bounds(field: AskCell) -> tuple[bool, Optional[PrefillValueType]]:
    """Return the (nullable, default) pair of a typed field or cell."""
    assert isinstance(field, NEW_CELL_TYPES)
    return (field.nullable, field.default)


def value_from_text(field: AskCell, text: str) -> Optional[PrefillValueType]:
    """Return the typed value of a typed field or cell for widget text.

    An empty text yields the field default, matching how the console form
    treats an empty answer. A non-empty text is parsed; unparsable or
    out-of-range text yields None, and the caller reports the error.
    """
    if text != '':
        return resolve_new(field, text)[0]
    return _new_bounds(field)[1]


def error_from_text(field: AskCell, text: str) -> Optional[str]:
    """Return the parse or range error of a typed field's or cell's text.

    Empty text is accepted when the field is nullable or has a default,
    and otherwise reports that a value is required.
    """
    if text != '':
        return resolve_new(field, text)[1]
    nullable, default = _new_bounds(field)
    if nullable or default is not None:
        return None
    return f'Please enter {field_hint(field)}.'


def fake_field(field: AskField) -> AskTextField:
    """Return the text field used to fake an unsupported typed field."""
    assert isinstance(field, NEW_FIELD_TYPES)
    hint = field_hint(field)
    note = f'Enter {hint}.'
    help_text = (note if field.help_text is None
                 else f'{field.help_text}\n{note}')
    return AskTextField(short_question=field.short_question,
                        help_text=help_text, nullable=field.nullable,
                        default=_formatted(field.default),
                        start_value=_formatted(field.start_value))


def _formatted(value: Optional[_OrderedValue]) -> Optional[str]:
    """Return value as the text a user types for it, or None for None."""
    return None if value is None else format_new_value(value)
