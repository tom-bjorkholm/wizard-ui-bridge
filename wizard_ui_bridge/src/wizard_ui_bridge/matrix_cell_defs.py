#! /usr/local/bin/python3
"""Definitions of cell types for wizard UI bridge matrix forms.

A matrix form asks a single context setting question on the top of the
screen, followed by a matrix of cells. Each cell typically represents a
single input field for a validated input. However, a cell may also be a
label that is only text displayed with no input. Typically the label cells
are used to name the rows and columns of the matrix, but they are not
limited to the edges; they can appear anywhere in the grid to provide
context or labels for the input cells. The matrix form also has a
feed-back area, typically below the grid, where validation messages or
other contextual information can be displayed to the user.

One example of a matrix form is a list of contractors, one contractor
per row in the matrix, with a column containing the name,
another column the start date as date picker, yet another column the
end date as date picker, the last column the file name of the contract
as file picker.

An Ask*Cell is like the corresponding Ask*Field of a form, except that
no question is asked per cell. Each Ask*Field derives from its Ask*Cell,
so code written for a cell also handles the corresponding form field.
Likewise each Answer*Field derives from its Answer*Cell.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from dataclasses import dataclass
from typing import Any, Generic, Optional, Protocol, Sequence, TypeVar, Union
from pathlib import Path
from datetime import datetime, date, time, timedelta
from wizard_ui_bridge.arg_types import PathAskOptions


class _OrderedValue(Protocol):
    """A value comparable to values of its own type with < and >.

    Int, float, date, time, datetime and timedelta all satisfy this, so a
    single helper can range-check every ordered cell. The other operand
    is Any because each concrete type only compares with itself, which is
    exactly how the standard library types are annotated.
    """

    def __lt__(self, other: Any) -> bool:
        """Return whether this value sorts before other."""

    def __gt__(self, other: Any) -> bool:
        """Return whether this value sorts after other."""


_OrderedT = TypeVar('_OrderedT', bound=_OrderedValue)


def value_out_of_range(value: _OrderedT, minimum: Optional[_OrderedT],
                       maximum: Optional[_OrderedT]) -> bool:
    """Return whether value lies outside the inclusive bounds."""
    below = minimum is not None and value < minimum
    above = maximum is not None and value > maximum
    return below or above


def _check_bounds(minimum: Optional[_OrderedValue],
                  maximum: Optional[_OrderedValue],
                  default: Optional[_OrderedValue]) -> None:
    """Raise ValueError when ordered bounds or the default disagree."""
    if minimum is not None and maximum is not None and minimum > maximum:
        raise ValueError('min_value must not exceed max_value')
    if default is not None and value_out_of_range(default, minimum, maximum):
        raise ValueError('default is out of the allowed range')


@dataclass
class AskCellCommon:
    """Common attributes of a cell in a matrix form.

    Each concrete cell is one of the Ask*Cell subclasses, so its Python
    type already tells the bridge which kind of input to show.

    Attributes:
        help_text: Optional help text to be displayed to the user. Could be
                   used as tooltip text in a GUI implementation, or as a
                   popup message in response to a help button click
                   or similar user action.
    """

    help_text: Optional[str]


@dataclass
class AskLabelCell(AskCellCommon):
    """A label cell in a matrix form, only text with no input.

    A label cell typically names a row or a column of the matrix, but it
    can be placed anywhere in the grid. It gives no answer, so its
    position in the answers of a matrix form holds None.

    Attributes:
        text: The text displayed in the cell.
    """

    text: str


@dataclass
class AskTextCell(AskCellCommon):
    """A text cell in a matrix form.

    Attributes:
        nullable: When True an empty answer with no default is reported
                  as None. When False an empty answer with no default is
                  the empty string.
        default: The value returned when user fills in nothing, or None for
                 no default. In a GUI implementation this is typically shown
                 as the starting value in the input field, and the user can
                 change it.
        sensitive: True when the bridge must avoid echoing the entered text,
                   such as for passwords. A default is not allowed for a
                   sensitive question.
    """

    nullable: bool = False
    default: Optional[str] = None
    sensitive: bool = False

    def __post_init__(self) -> None:
        """Check that the text cell arguments are valid."""
        if self.sensitive and self.default is not None:
            raise ValueError('Sensitive text field cannot have a default')


@dataclass
class AskRangeCell(AskCellCommon, Generic[_OrderedT]):
    """A cell in a matrix form for an ordered value with optional bounds.

    This is the common base of the integer, float, date, time, date-time
    and duration cells, so a bridge can handle their shared attributes
    once.

    Attributes:
        nullable: When True an empty answer with no default is reported
                  as None. When False an empty answer with no default will
                  be re-asked until the user fills in a valid value.
        default: The value returned when user fills in nothing, or None for
                 no default. In a GUI implementation this is typically shown
                 as the starting value in the input field, and the user can
                 change it.
        min_value: The minimum allowed value, or None for no minimum.
                   The min value is inclusive.
        max_value: The maximum allowed value, or None for no maximum.
                   The max value is inclusive.
    """

    nullable: bool = False
    default: Optional[_OrderedT] = None
    min_value: Optional[_OrderedT] = None
    max_value: Optional[_OrderedT] = None

    def __post_init__(self) -> None:
        """Check that the bounds and the default agree."""
        _check_bounds(self.min_value, self.max_value, self.default)


@dataclass
class AskIntCell(AskRangeCell[int]):
    """An integer cell in a matrix form."""


@dataclass
class AskPathCell(AskCellCommon):
    """A path cell in a matrix form.

    In a GUI implementation this is typically displayed as a text input field
    with a button next to it that opens a file/directory chooser dialog.

    Attributes:
        path_options: Options for how the path question is asked, including
                      whether the path must exist, whether it must be a file
                      or a directory.
    """

    path_options: PathAskOptions


@dataclass
class AskYesNoCell(AskCellCommon):
    """A yes/no cell in a matrix form.

    In a GUI implementation this is typically displayed as a checkbox or a
    toggle button.

    Attributes:
        default: The boolean value used when the user makes no explicit
                 choice. In a GUI implementation this is typically shown as
                 the starting value in the checkbox or toggle, and the user
                 can change it.
    """

    default: bool


@dataclass
class AskChoiceCell(AskCellCommon):
    """A choice cell in a matrix form.

    In a GUI implementation this is typically displayed as a dropdown list
    or a set of radio buttons.

    Attributes:
        choices: The allowed choices for the answer.
        default: The value returned when user fills in nothing, or None for
                 no default. In a GUI implementation this is typically shown
                 as the starting value in the input field, and the user can
                 change it.
    """

    choices: Sequence[str]
    default: Optional[str] = None


@dataclass
class AskMultiChoiceCell(AskCellCommon):
    """A multi-choice cell in a matrix form.

    In a GUI implementation this is typically displayed as a list of checkboxes
    or a list of items with multiple selection enabled.

    Attributes:
        choices: The allowed choices for the answer.
        default: The values returned when user fills in nothing, or None for
                 no default. In a GUI implementation this is typically shown
                 as the starting value in the input field, and the user can
                 change it.
        min_select: The minimum number of choices that must be selected.
        max_select: The maximum number of choices that can be selected,
                    or None for no maximum.
    """

    choices: Sequence[str]
    default: Optional[Sequence[str]] = None
    min_select: int = 0
    max_select: Optional[int] = None


@dataclass
class AskFloatCell(AskRangeCell[float]):
    """A float cell in a matrix form."""


@dataclass
class AskDateCell(AskRangeCell[date]):
    """A date cell in a matrix form.

    In a GUI implementation this is typically displayed as a text input field
    with a button next to it that opens a date chooser dialog.
    """


@dataclass
class AskTimeCell(AskRangeCell[time]):
    """A time cell in a matrix form."""


@dataclass
class AskDateTimeCell(AskRangeCell[datetime]):
    """A date-time cell in a matrix form.

    In a GUI implementation this is typically displayed as a text input field
    with a button next to it that opens a date-time chooser dialog for the
    date part.
    """


@dataclass
class AskDurationCell(AskRangeCell[timedelta]):
    """A duration cell in a matrix form."""


type AskCell = Union[AskLabelCell, AskTextCell, AskIntCell, AskPathCell,
                     AskYesNoCell, AskChoiceCell, AskMultiChoiceCell,
                     AskFloatCell, AskDateCell, AskTimeCell, AskDateTimeCell,
                     AskDurationCell]
"""An AskCell is one cell in the matrix of a matrix form.

   The AskCell is one of the Ask*Cell dataclasses. It holds the help text
   and other attributes of the cell. Every Ask*Field of a form is also an
   instance of the corresponding Ask*Cell.
"""


ALL_ASK_CELL_TYPES = (AskLabelCell, AskTextCell, AskIntCell, AskPathCell,
                      AskYesNoCell, AskChoiceCell, AskMultiChoiceCell,
                      AskFloatCell, AskDateCell, AskTimeCell, AskDateTimeCell,
                      AskDurationCell)
"""Every concrete AskCell class, in the order of the AskCell union.

A bridge that shows all cell types checks membership against this tuple,
so a cell type added later is reported as unsupported until this tuple
and the bridge are extended together. Since every Ask*Field derives from
its Ask*Cell, an isinstance check against this tuple also accepts fields.
"""


@dataclass
class AnswerTextCell:
    """An answer to a text cell in a matrix form.

    Attributes:
        asking: How the cell was asked, including the help text and other
                attributes of the cell.
        value: The value of the answer, or None when the user did not fill in
               anything and the cell is nullable.
    """

    asking: AskTextCell
    value: Optional[str]


@dataclass
class AnswerIntCell:
    """An answer to an integer cell in a matrix form.

    Attributes:
        asking: How the cell was asked, including the help text and other
                attributes of the cell.
        value: The value of the answer, or None when the user did not fill in
               anything and the cell is nullable.
    """

    asking: AskIntCell
    value: Optional[int]


@dataclass
class AnswerPathCell:
    """An answer to a path cell in a matrix form.

    Attributes:
        asking: How the cell was asked, including the help text and other
                attributes of the cell.
        value: The value of the answer, or None when the user did not fill in
               anything and the cell is nullable.
    """

    asking: AskPathCell
    value: Optional[Path]


@dataclass
class AnswerYesNoCell:
    """An answer to a yes/no cell in a matrix form.

    Attributes:
        asking: How the cell was asked, including the help text and other
                attributes of the cell.
        value: The value of the answer.
    """

    asking: AskYesNoCell
    value: bool


@dataclass
class AnswerChoiceCell:
    """An answer to a choice cell in a matrix form.

    Attributes:
        asking: How the cell was asked, including the help text and other
                attributes of the cell.
        value: The chosen value, one of the choices. It is None only to
               tell a partial validator that a choice with no default has
               not been answered yet. A bridge never returns None as a final
               choice answer: it makes sure a choice with no default is
               answered before the form is submitted for final validation,
               unless the choice is disabled by a partial validator because
               it is irrelevant given the current state of the form.
    """

    asking: AskChoiceCell
    value: Optional[str]


@dataclass
class AnswerMultiChoiceCell:
    """An answer to a multi-choice cell in a matrix form.

    Attributes:
        asking: How the cell was asked, including the help text and other
                attributes of the cell.
        value: The values of the answer.
    """

    asking: AskMultiChoiceCell
    value: Sequence[str]


@dataclass
class AnswerFloatCell:
    """An answer to a float cell in a matrix form.

    Attributes:
        asking: How the cell was asked, including the help text and other
                attributes of the cell.
        value: The value of the answer, or None when the user did not fill in
               anything and the cell is nullable.
    """

    asking: AskFloatCell
    value: Optional[float]


@dataclass
class AnswerDateCell:
    """An answer to a date cell in a matrix form.

    Attributes:
        asking: How the cell was asked, including the help text and other
                attributes of the cell.
        value: The value of the answer, or None when the user did not fill in
               anything and the cell is nullable.
    """

    asking: AskDateCell
    value: Optional[date]


@dataclass
class AnswerTimeCell:
    """An answer to a time cell in a matrix form.

    Attributes:
        asking: How the cell was asked, including the help text and other
                attributes of the cell.
        value: The value of the answer, or None when the user did not fill in
               anything and the cell is nullable.
    """

    asking: AskTimeCell
    value: Optional[time]


@dataclass
class AnswerDateTimeCell:
    """An answer to a date-time cell in a matrix form.

    Attributes:
        asking: How the cell was asked, including the help text and other
                attributes of the cell.
        value: The value of the answer, or None when the user did not fill in
               anything and the cell is nullable.
    """

    asking: AskDateTimeCell
    value: Optional[datetime]


@dataclass
class AnswerDurationCell:
    """An answer to a duration cell in a matrix form.

    Attributes:
        asking: How the cell was asked, including the help text and other
                attributes of the cell.
        value: The value of the answer, or None when the user did not fill in
               anything and the cell is nullable.
    """

    asking: AskDurationCell
    value: Optional[timedelta]


type AnswerCell = Union[AnswerTextCell, AnswerIntCell, AnswerPathCell,
                        AnswerYesNoCell, AnswerChoiceCell,
                        AnswerMultiChoiceCell, AnswerFloatCell,
                        AnswerDateCell, AnswerTimeCell, AnswerDateTimeCell,
                        AnswerDurationCell]
"""An AnswerCell is the answer to one input cell in a matrix form.

   The AnswerCell is one of the Answer*Cell dataclasses. It holds the actual
   answer value, and the AskCell that was asked. A label cell gives no
   answer, so there is no AnswerCell for it. Every Answer*Field of a form is
   also an instance of the corresponding Answer*Cell.
"""
