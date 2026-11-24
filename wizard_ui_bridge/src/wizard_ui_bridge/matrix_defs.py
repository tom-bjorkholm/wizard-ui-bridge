#! /usr/local/bin/python3
"""Definitions of the request and validator types of a matrix form.

A matrix form asks a single context setting question on the top of the
screen, followed by a matrix of cells, and has a feed-back area for
messages from a partial validator. The cell types are defined in module
matrix_cell_defs.

The number of rows and columns may vary at run time between the minimum
and maximum dimensions of the request. Rows and columns with only labels
still count like any other row or column. Rows and columns are only
appended after the last row or column, and only the last row or column
is deleted, so the position of a remaining cell never changes.

Labels can be used to provide context at any position in the matrix.
There is no requirement for any position to have a label;
labels are optional and can be placed wherever needed.

Sometimes the client chooses a design with leading label rows
or columns that provide context for the rest of the matrix.
A minimum dimension larger than the number of leading label
rows or columns keeps those labels from being deleted.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from dataclasses import dataclass
from typing import Callable, NamedTuple, Optional, Self, Sequence, \
    Union
from wizard_ui_bridge.matrix_cell_defs import AskCell, AnswerCell, \
    PrefillValueType

type AnswerCells = Sequence[Sequence[Optional[AnswerCell]]]
"""The answers to a matrix form.

   A 2D sequence representing the answers in a matrix form, in the current
   shape of the matrix. Each inner sequence corresponds to a row in the
   matrix, and each element within the inner sequence corresponds to a cell
   in that row: an AnswerCell for an input cell, and None for a label cell.
"""


class CellPosition(NamedTuple):
    """The position of a cell in a matrix form, both indexes 0-based.

    Attributes:
        row: The row index of the cell.
        column: The column index of the cell.
    """

    row: int
    column: int


@dataclass(frozen=True)
class MatrixDimension:
    """The number of rows and columns of a matrix form.

    Label rows and label columns count like any other row or column.

    Attributes:
        rows: The number of rows in the matrix.
        columns: The number of columns in the matrix.
    """

    rows: int
    columns: int

    def __post_init__(self) -> None:
        """Check that neither size is negative."""
        if self.rows < 0 or self.columns < 0:
            raise ValueError('matrix dimensions must not be negative')


@dataclass(frozen=True)
class MatrixDimensions:
    """The minimum, maximum and default dimensions of a matrix form.

    When min and max are equal the matrix has a fixed shape, which
    MatrixDimensions.fixed(rows, columns) builds directly. Otherwise the
    user may append or delete the last row or column within the bounds.
    An appended row or column normally shows cells the MatrixCellSpec
    already gives for its position; see MatrixCellSpec for when a cell
    is repeated instead.

    Attributes:
        min: The minimum dimensions of the matrix.
        max: The maximum dimensions of the matrix.
        default: The default dimensions of the matrix.
                 What is first shown before the user resizes the matrix.
    """

    min: MatrixDimension
    max: MatrixDimension
    default: MatrixDimension

    def __post_init__(self) -> None:
        """Check that min <= default <= max for both rows and columns."""
        for low, high in ((self.min, self.default), (self.default, self.max)):
            if low.rows > high.rows or low.columns > high.columns:
                raise ValueError('matrix dimensions need min <= default <= '
                                 'max for both rows and columns')

    @classmethod
    def fixed(cls, rows: int, columns: int) -> Self:
        """Return the dimensions of a matrix the user cannot resize.

        The minimum, maximum and default dimensions are all rows x columns.
        """
        shape = MatrixDimension(rows, columns)
        return cls(shape, shape, shape)


type PrefillCellValues = tuple[tuple[CellPosition, PrefillValueType], ...]
"""Prefill requests returned by a partial matrix validator.

Each pair is (position, value): a request to place value into the input
of the cell at the given position, as if the user had typed it. See
PartMatrixValidationRes.prefill_values for the rules a bridge follows
when it applies these requests.
"""


class PartMatrixValidationRes(NamedTuple):
    """Result of validating a partly filled matrix form.

    Attributes:
        is_valid: True when the form is valid, False when it is not valid.
        message: A message to be displayed to the user, explaining why the
                 form is not valid. Empty string when the form is valid.
        disable_cells: A tuple of positions that should be disabled in the
                       matrix, because what has been filled in so far makes
                       these cells irrelevant. For example if output format
                       is set to some binary format, then the cell(s) that
                       ask for character encoding can be disabled, because
                       they are irrelevant for the chosen output format.
                       Each result replaces the disabled cells of the
                       previous one. Actually disabling these cells is not
                       strictly necessary, but it is a good user experience
                       to do so.
        prefill_values: Values the validator asks the bridge to place into
                        other cells' inputs, as a tuple of
                        (cell_position, value) pairs. Each value must match
                        the answer type of the cell in that position. A bridge
                        applies each request during live editing as if the
                        user had typed the value; setting a value equal to
                        the one already there is a no-op, so a validator
                        that emits a stable value does not loop. The validator
                        owns idempotency: it should emit a prefill only when
                        it means to fill or overwrite the target. A prefill
                        aimed at the cell that just changed is ignored, so
                        writing back never fights the user's current edit.
                        A prefill aimed at a disabled cell is still applied,
                        so the value shows in the greyed cell and takes effect
                        if the cell is later enabled. A cell position outside
                        the matrix, a label cell, or a value whose type does
                        not match the cell, raises an exception, since all
                        are validator bugs. A choice or multi-choice value not
                        among the cell's choices, and any prefill of a
                        sensitive cell, are ignored. prefill_values is a
                        live-editing convenience only and is ignored when the
                        form is submitted, so an application must still apply
                        the same default on submit.
    """

    is_valid: bool
    message: str
    disable_cells: tuple[CellPosition, ...] = ()
    prefill_values: PrefillCellValues = ()


type PartialMatrixValidator = Callable[[AnswerCells, Optional[CellPosition]],
                                       PartMatrixValidationRes]
"""Callback for early per-cell feedback while a matrix form is filled.

   The callback receives the current state of the matrix form as AnswerCells,
   and the CellPosition of the cell most recently filled in, or None when
   the shape of the matrix changed because the user appended or deleted
   the last row or column. After a shape change the validator should
   re-evaluate the whole matrix from the answers.
   It returns a PartMatrixValidationRes, which indicates whether the matrix
   form is valid, and if not valid, a message to be displayed to the user,
   a tuple of CellPosition objects that should be disabled in the matrix
   form because they are irrelevant given the current state of the matrix
   form, and any values to prefill into other cells.
   See PartMatrixValidationRes for the rules of each part.
"""


type AskCellGenerator = Callable[[CellPosition], AskCell]
"""Callback for generating the AskCell at a CellPosition.

   The bridge may call it more than once for the same position, so it
   must return an equivalent cell each time.
"""


type MatrixCellSpec = Union[Sequence[Sequence[AskCell]], AskCellGenerator]
"""Specification for the cells in a matrix form.

   Can be either a 2D sequence of AskCell objects, representing the fixed
   layout of the matrix, or an AskCellGenerator, which generates an AskCell
   given a CellPosition.

   The normal use of a 2D sequence is to give it the maximum dimensions
   of the matrix. The matrix first shows only the part of it within the
   default dimensions, and each row or column the user appends shows the
   cells already given at its position in the sequence. Each cell can
   then have its own defaults and label texts, for instance existing
   data in the first rows and empty cells in the rows after them.

   A 2D sequence may also be smaller than the maximum dimensions, but it
   must have at least one row, and each row at least one cell. Only
   for a position beyond the sequence is a cell repeated: a row below
   the last row of the sequence repeats its last row, and a column right
   of the last cell of a row repeats that last cell. This is a
   convenience for a matrix whose appended rows or columns are all alike.
   The repeated cells keep their defaults and label texts, so a header
   label is repeated as well.

   A deleted last row or column that is appended again gets fresh cells
   from the specification, so the values the user entered in it are lost.
"""


class MatrixConsoleQuestion(NamedTuple):
    """How to ask for cells in a matrix form in a console.

    The matrix form is not well-suited for console input, so this class
    provides guidance on how to ask for cells in a console environment.

    Attributes:
        use_help_text: Whether to display the help text for each cell
            when asking for input in the console without requiring
            the user to explicitly request help. If this is True,
            the help text should be displayed immediately before
            expecting input for that cell. If this is False, the help text
            should only be displayed in response to an explicit request
            from the user.
        show_horizontal_label: If this is True, the label closest to
            the left of the cell asked for in the same row is displayed
            for each cell asked for in the console.
            If this is False, the horizontal label should not be displayed.
        show_vertical_label: If this is True, the label closest above
            the cell asked for in the same column is displayed for each
            cell asked for in the console.
            If this is False, the vertical label should not be displayed.
        row_order: If this is True, the cells should be asked for in
            row-major order, meaning that all cells in a row are asked for
            before moving on to the next row. If False, column-major order
            should be used, meaning that all cells in a column are asked for
            before moving on to the next column.
    """

    use_help_text: bool
    show_horizontal_label: bool
    show_vertical_label: bool
    row_order: bool = True


class MatrixRequest(NamedTuple):
    """Request for a matrix form.

    Attributes:
        long_question: The main question or instruction to display above the
            matrix form. It may be a long string that the UI bridge is
            responsible for wrapping and displaying nicely.
        ask_cells: The specification for the cells in the matrix form.
        dimensions: The minimum, maximum and default dimensions of the matrix.
        console_question: How a console bridge asks for the cells.
        partial_validator: Optional callback for early per-cell feedback.
    """

    long_question: str
    ask_cells: MatrixCellSpec
    dimensions: MatrixDimensions
    console_question: MatrixConsoleQuestion
    partial_validator: Optional[PartialMatrixValidator] = None
