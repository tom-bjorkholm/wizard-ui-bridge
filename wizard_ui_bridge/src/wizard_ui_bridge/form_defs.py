#! /usr/local/bin/python3
"""Definitions of types for wizard UI bridge forms.

Wizard UI bridge forms are used when a number of questions should preferably
be asked on a single form (in a GUI, textual or curses implementation).
For a good user experience the user should see all questions at the same time,
and the user should be able to fill in the answers in any order, and change
them before submitting the form.

In a GUI, curses or textual implementation, the form is typically displayed
in a single window, in something like a grid layout, with 2 columns and
2 - 10 rows. The left column contains the questions, and the right column
contains the input fields. Above the grid there is typically a longer question
or instruction, that explains to the user what the form is about. Below the
grid there are typically buttons for submitting the form, canceling the form,
and possibly for going back to a previous form step in a multi-step wizard.

A variant is the matrix form, described in module matrix_cell_defs. Each
Ask*Field of a form derives from the corresponding Ask*Cell of a matrix
form, adding the short question, and each Answer*Field derives from the
corresponding Answer*Cell.

This file defines the data types used to describe the questions and answers of
a form, and the validation callback function that is used to validate the
answers of a partly filled form.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from dataclasses import dataclass
from typing import Callable, NamedTuple, Optional, Sequence, Union
from wizard_ui_bridge import matrix_cell_defs
from wizard_ui_bridge.matrix_cell_defs import AskTextCell, AskIntCell, \
    AskPathCell, AskYesNoCell, AskChoiceCell, AskMultiChoiceCell, \
    AskFloatCell, AskDateCell, AskTimeCell, AskDateTimeCell, \
    AskDurationCell, AnswerTextCell, AnswerIntCell, AnswerPathCell, \
    AnswerYesNoCell, AnswerChoiceCell, AnswerMultiChoiceCell, \
    AnswerFloatCell, AnswerDateCell, AnswerTimeCell, AnswerDateTimeCell, \
    AnswerDurationCell, PrefillValueType

value_out_of_range = matrix_cell_defs.value_out_of_range
"""Kept for compatibility, see matrix_cell_defs.value_out_of_range."""


@dataclass
class AskFieldCommon:
    """Common attributes of a field in a form.

    Each concrete field is one of the Ask*Field subclasses, so its Python
    type already tells the bridge which kind of input to show. There is no
    separate kind attribute to keep in sync.

    Each Ask*Field derives from its Ask*Cell first and from this class
    last, so the constructor arguments start with short_question and
    help_text. help_text is declared both here and in AskCellCommon, so
    a field type derived only from this class still has it.

    Every field also has the keyword-only width hint of AskCellCommon,
    for instance AskTextField('Name?', None, width=20).

    Attributes:
        short_question: A short question to be displayed to the user.
                        In a GUI implementation this is typically displayed
                        as a label in a left column next to the input field.
        help_text: Optional help text to be displayed to the user. Could be
                   used as tooltip text in a GUI implementation, or as a
                   popup message in response to a help button click
                   or similar user action.
    """

    short_question: str
    help_text: Optional[str]


@dataclass
class AskTextField(AskTextCell, AskFieldCommon):
    """A text field in a form, see AskFieldCommon and AskTextCell."""


@dataclass
class AskIntField(AskIntCell, AskFieldCommon):
    """An integer field in a form, see AskFieldCommon and AskIntCell."""


@dataclass
class AskPathField(AskPathCell, AskFieldCommon):
    """A path field in a form, see AskFieldCommon and AskPathCell."""


@dataclass
class AskYesNoField(AskYesNoCell, AskFieldCommon):
    """A yes/no field in a form, see AskFieldCommon and AskYesNoCell."""


@dataclass
class AskChoiceField(AskChoiceCell, AskFieldCommon):
    """A choice field in a form, see AskFieldCommon and AskChoiceCell."""


@dataclass
class AskMultiChoiceField(AskMultiChoiceCell, AskFieldCommon):
    """A multi-choice field in a form.

    See AskFieldCommon and AskMultiChoiceCell for the attributes.
    """


@dataclass
class AskFloatField(AskFloatCell, AskFieldCommon):
    """A float field in a form, see AskFieldCommon and AskFloatCell."""


@dataclass
class AskDateField(AskDateCell, AskFieldCommon):
    """A date field in a form, see AskFieldCommon and AskDateCell."""


@dataclass
class AskTimeField(AskTimeCell, AskFieldCommon):
    """A time field in a form, see AskFieldCommon and AskTimeCell."""


@dataclass
class AskDateTimeField(AskDateTimeCell, AskFieldCommon):
    """A date-time field in a form.

    See AskFieldCommon and AskDateTimeCell for the attributes.
    """


@dataclass
class AskDurationField(AskDurationCell, AskFieldCommon):
    """A duration field in a form, see AskFieldCommon and AskDurationCell."""


type AskField = Union[AskTextField, AskIntField, AskPathField, AskYesNoField,
                      AskChoiceField, AskMultiChoiceField, AskFloatField,
                      AskDateField, AskTimeField, AskDateTimeField,
                      AskDurationField]
"""An AskField is the question asked in a row in a form in a wizard UI bridge.

   The AskField is one of the Ask*Field dataclasses. It holds the actual
   question text, help text, and other attributes of the question.
"""

type AskFields = Sequence[AskField]
"""AskFields is a sequence of AskField objects, one for each row in a form."""


ALL_ASK_FIELD_TYPES = (AskTextField, AskIntField, AskPathField, AskYesNoField,
                       AskChoiceField, AskMultiChoiceField, AskFloatField,
                       AskDateField, AskTimeField, AskDateTimeField,
                       AskDurationField)
"""Every concrete AskField class, in the order of the AskField union.

A bridge that shows all field types checks membership against this tuple
in supports_form_field(), so a field type added later is reported as
unsupported until this tuple and the bridge are extended together.
"""


@dataclass
class AnswerTextField(AnswerTextCell):
    """An answer to a text field in a form.

    Attributes:
        asking: How the question was asked, including the question text, help
                text, and other attributes of the question.
    """

    asking: AskTextField


@dataclass
class AnswerIntField(AnswerIntCell):
    """An answer to an integer field in a form.

    Attributes:
        asking: How the question was asked, including the question text, help
                text, and other attributes of the question.
    """

    asking: AskIntField


@dataclass
class AnswerPathField(AnswerPathCell):
    """An answer to a path field in a form.

    Attributes:
        asking: How the question was asked, including the question text, help
                text, and other attributes of the question.
    """

    asking: AskPathField


@dataclass
class AnswerYesNoField(AnswerYesNoCell):
    """An answer to a yes/no field in a form.

    Attributes:
        asking: How the question was asked, including the question text, help
                text, and other attributes of the question.
    """

    asking: AskYesNoField


@dataclass
class AnswerChoiceField(AnswerChoiceCell):
    """An answer to a choice field in a form.

    Attributes:
        asking: How the question was asked, including the question text, help
                text, and other attributes of the question.
    """

    asking: AskChoiceField


@dataclass
class AnswerMultiChoiceField(AnswerMultiChoiceCell):
    """An answer to a multi-choice field in a form.

    Attributes:
        asking: How the question was asked, including the question text, help
                text, and other attributes of the question.
    """

    asking: AskMultiChoiceField


@dataclass
class AnswerFloatField(AnswerFloatCell):
    """An answer to a float field in a form.

    Attributes:
        asking: How the question was asked, including the question text, help
                text, and other attributes of the question.
    """

    asking: AskFloatField


@dataclass
class AnswerDateField(AnswerDateCell):
    """An answer to a date field in a form.

    Attributes:
        asking: How the question was asked, including the question text, help
                text, and other attributes of the question.
    """

    asking: AskDateField


@dataclass
class AnswerTimeField(AnswerTimeCell):
    """An answer to a time field in a form.

    Attributes:
        asking: How the question was asked, including the question text, help
                text, and other attributes of the question.
    """

    asking: AskTimeField


@dataclass
class AnswerDateTimeField(AnswerDateTimeCell):
    """An answer to a date-time field in a form.

    Attributes:
        asking: How the question was asked, including the question text, help
                text, and other attributes of the question.
    """

    asking: AskDateTimeField


@dataclass
class AnswerDurationField(AnswerDurationCell):
    """An answer to a duration field in a form.

    Attributes:
        asking: How the question was asked, including the question text, help
                text, and other attributes of the question.
    """

    asking: AskDurationField


type AnswerField = Union[AnswerTextField, AnswerIntField, AnswerPathField,
                         AnswerYesNoField, AnswerChoiceField,
                         AnswerMultiChoiceField, AnswerFloatField,
                         AnswerDateField, AnswerTimeField,
                         AnswerDateTimeField, AnswerDurationField]
"""An AnswerField is the answer to a question in a row in a form.

   The AnswerField is one of the Answer*Field dataclasses. It holds the actual
   answer value, and the AskField that was asked.
   """


type AnswerFields = Sequence[AnswerField]
"""AnswerFields is a sequence of AnswerField objects.

   It holds one AnswerField for each row in a form.
   """


type PrefillValues = tuple[tuple[int, PrefillValueType], ...]
"""Prefill requests returned by a partial form validator.

Each pair is (row_index, value): a request to place value into the input
of the row at row_index, as if the user had typed it. See
PartFormValidationResult.prefill_values for the rules a bridge follows
when it applies these requests.
"""


class PartFormValidationResult(NamedTuple):
    """Result of validating a partly filled form.

    Attributes:
        is_valid: True when the form is valid, False when it is not valid.
        message: A message to be displayed to the user, explaining why the
                 form is not valid. Empty string when the form is valid.
        disable_row_idxs: A tuple of row indexes that should be disabled in the
                          form, because what has been filled in so far makes
                          these rows irrelevant. For example if output format
                          is set to some binary format, then the row(s) that
                          ask for character encoding can be disabled, because
                          they are irrelevant for the chosen output format.
                          Actually disabling these rows is not strictly
                          necessary, but it is a good user experience to do so.
        prefill_values: Values the validator asks the bridge to place into
                        other rows' inputs, as a tuple of (row_index, value)
                        pairs. Each value must match the answer type of the
                        field in that row. A bridge applies each request
                        during live editing as if the user had typed the
                        value; setting a value equal to the one already there
                        is a no-op, so a validator that emits a stable value
                        does not loop. The validator owns idempotency: it
                        should emit a prefill only when it means to fill or
                        overwrite the target. A prefill aimed at the row that
                        just changed is ignored, so writing back never fights
                        the user's current edit. A prefill aimed at a disabled
                        row is still applied, so the value shows in the greyed
                        row and takes effect if the row is later enabled. A
                        row index outside the form, or a value whose type does
                        not match the field, raises an exception, since both
                        are validator bugs. A choice or multi-choice value not
                        among the field's choices, and any prefill of a
                        sensitive field, are ignored. prefill_values is a
                        live-editing convenience only and is ignored when the
                        form is submitted, so an application must still apply
                        the same default on submit.
    """

    is_valid: bool
    message: str
    disable_row_idxs: tuple[int, ...] = ()
    prefill_values: PrefillValues = ()


type PartialFormValidator = Callable[[AnswerFields, int],
                                     PartFormValidationResult]
"""Callback for early per-row feedback while a form is filled.

   The callback receives the current state of the form as AnswerFields,
   and the index of the row most recently filled in.
   It returns a PartFormValidationResult, which indicates whether the form is
   valid, and if not valid, a message to be displayed to the user, a tuple
   of row indexes that should be disabled in the form because they are
   irrelevant given the current state of the form, and any values to prefill
   into other rows. See PartFormValidationResult for the rules of each part.
"""
