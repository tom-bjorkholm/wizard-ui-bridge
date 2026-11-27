#! /usr/bin/env python3
"""Tests for resizing the Textual matrix form screen.

The resize buttons append or delete the last row or column within the
bounds of the request, each disabled at its bound.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional
from textual.containers import Grid, ScrollableContainer
from textual.pilot import Pilot
from textual.widgets import Button, Input, Static
from wizard_ui_bridge import AnswerCells, AskCell, MatrixDimension, \
    MatrixDimensions, PartMatrixValidationRes, AskLabelCell, AskTextCell
from wizard_ui_bridge._textual_matrix import _MatrixApp, ADD_COLUMN, \
    ADD_ROW, REMOVE_COLUMN, REMOVE_ROW
from .textual_matrix_support import RESIZABLE, SHEET, Recorder, \
    focused_id, matrix_request, run_matrix, status, type_in


async def _click(app: _MatrixApp, pilot: Pilot[AnswerCells],
                 *button_ids: str) -> None:
    """Press each button in turn, as the user clicking it does.

    A disabled button ignores the press. Button.press() is used, since a
    Textual button ignores a click within its press animation, which a
    pilot click right after the previous one would fall within.
    """
    for button_id in button_ids:
        button = app.query_one(f'#{button_id}', Button)
        button.focus()
        button.press()
        await pilot.pause()


def _shape(app: _MatrixApp) -> list[int]:
    """Return the number of cells in each row of the answers."""
    return [len(row) for row in app.answers()]


def test_resize_rows() -> None:
    """Rows are appended and deleted at the end within the bounds.

    Each change of the shape calls the validator with None, and a row
    deleted and appended again gets fresh cells, losing what was typed.
    """
    validator = Recorder(PartMatrixValidationRes(True, ''))

    async def script(app: _MatrixApp,
                     pilot: Pilot[AnswerCells]) -> list[object]:
        """Change a cell, delete rows past the minimum, add past the max."""
        await type_in(app, pilot, (2, 1), '1')
        await _click(app, pilot, REMOVE_ROW, REMOVE_ROW)
        shrunk = _shape(app)
        await _click(app, pilot, ADD_ROW, ADD_ROW, ADD_ROW)
        return [shrunk, _shape(app),
                app.query_one('#cell_2_1', Input).value]
    request = matrix_request(SHEET, RESIZABLE, validator)
    found = run_matrix(request, script)[1]
    assert found == [[3, 3], [3, 3, 3, 3], '8']
    assert validator.calls[:2] == [None, (2, 1)]
    assert validator.calls[2:] == [None] * 3


def test_resize_columns() -> None:
    """Columns are appended and deleted at the end within the bounds.

    An appended column repeats the last cell of each row, so it has a
    label in the header row and an input below it.
    """
    async def script(app: _MatrixApp,
                     pilot: Pilot[AnswerCells]) -> list[object]:
        """Add columns past the maximum, then delete past the minimum."""
        await _click(app, pilot, ADD_COLUMN, ADD_COLUMN)
        grown = [_shape(app), type(app.query_one('#cell_0_3')),
                 type(app.query_one('#cell_1_3'))]
        await _click(app, pilot, REMOVE_COLUMN, REMOVE_COLUMN, REMOVE_COLUMN)
        columns = app.query_one('#matrix_grid', Grid).styles.grid_size_columns
        return grown + [_shape(app), columns]
    found = run_matrix(matrix_request(SHEET, RESIZABLE), script)[1]
    assert found == [[4, 4, 4], Static, Input, [2, 2, 2], 2]


def test_resize_order() -> None:
    """Appended columns keep each row's cells in column order."""
    async def script(app: _MatrixApp,
                     pilot: Pilot[AnswerCells]) -> list[Optional[str]]:
        """Add a column and read the ids of the grid, row by row."""
        await _click(app, pilot, ADD_COLUMN)
        return [child.id
                for child in app.query_one('#matrix_grid', Grid).children]
    found = run_matrix(matrix_request(SHEET, RESIZABLE), script)[1]
    assert found == [f'cell_{row}_{column}'
                     for row in range(3) for column in range(4)]


def test_resize_no_rows() -> None:
    """A matrix shown with no rows gets a full row when one is added."""
    dims = MatrixDimensions(MatrixDimension(0, 2), MatrixDimension(2, 2),
                            MatrixDimension(0, 2))

    async def script(app: _MatrixApp,
                     pilot: Pilot[AnswerCells]) -> list[AnswerCells]:
        """Read the answers before and after adding a row."""
        empty = app.answers()
        await _click(app, pilot, ADD_ROW)
        return [empty, app.answers()]
    assert run_matrix(matrix_request(SHEET, dims), script)[1] == \
        [[], [[None, None]]]


def _buttons(app: _MatrixApp) -> dict[Optional[str], bool]:
    """Return whether each resize button is enabled, by its id, in order."""
    return {button.id: not button.disabled
            for button in app.query('#resize Button').results(Button)}


def test_buttons_fixed() -> None:
    """A matrix of fixed shape gets no resize buttons."""
    async def script(app: _MatrixApp,
                     _pilot: Pilot[AnswerCells]) -> dict[Optional[str], bool]:
        """Read the resize buttons."""
        return _buttons(app)
    assert run_matrix(matrix_request(), script)[1] == {}


def test_buttons_rows() -> None:
    """Only row buttons are shown, each disabled at its bound."""
    dims = MatrixDimensions(MatrixDimension(2, 3), MatrixDimension(3, 3),
                            MatrixDimension(3, 3))

    async def script(app: _MatrixApp, pilot: Pilot[AnswerCells]
                     ) -> list[dict[Optional[str], bool]]:
        """Read the buttons before and after deleting a row."""
        before = _buttons(app)
        await _click(app, pilot, REMOVE_ROW)
        return [before, _buttons(app)]
    assert run_matrix(matrix_request(SHEET, dims), script)[1] == [
        {ADD_ROW: False, REMOVE_ROW: True},
        {ADD_ROW: True, REMOVE_ROW: False}]


def test_buttons_all() -> None:
    """A matrix resizable both ways gets all four buttons, in order."""
    async def script(app: _MatrixApp,
                     _pilot: Pilot[AnswerCells]) -> list[Optional[str]]:
        """Read the order of the resize buttons."""
        return list(_buttons(app))
    assert run_matrix(matrix_request(SHEET, RESIZABLE), script)[1] == \
        [ADD_ROW, REMOVE_ROW, ADD_COLUMN, REMOVE_COLUMN]


def test_added_not_change() -> None:
    """The inputs of an appended row are not taken as changes.

    Textual posts a change event when it mounts an input holding a
    value, which must neither run the validator for that cell nor show
    its message.
    """
    validator = Recorder(PartMatrixValidationRes(True, ''))

    async def script(app: _MatrixApp, pilot: Pilot[AnswerCells]) -> str:
        """Add a row and read the status."""
        await _click(app, pilot, ADD_ROW)
        return status(app)
    assert run_matrix(matrix_request(SHEET, RESIZABLE, validator),
                      script)[1] == ''
    assert validator.calls == [None, None]


def test_focus_added() -> None:
    """The first input of an appended row or column gets the focus."""
    async def script(app: _MatrixApp,
                     pilot: Pilot[AnswerCells]) -> list[Optional[str]]:
        """Add a row, then a column, reading the focus after each."""
        await _click(app, pilot, ADD_ROW)
        row = focused_id(app)
        await _click(app, pilot, ADD_COLUMN)
        return [row, focused_id(app)]
    assert run_matrix(matrix_request(SHEET, RESIZABLE), script)[1] == \
        ['cell_3_1', 'cell_1_3']


def _enabled_focus(app: _MatrixApp) -> bool:
    """Return whether an enabled widget has the keyboard focus."""
    return app.focused is not None and not app.focused.disabled


def test_focus_label_row() -> None:
    """An appended row of labels only takes no focus, nor loses it.

    The add button is disabled at the maximum row count, so the focus
    leaves it for another enabled widget.
    """
    cells: list[list[AskCell]] = [
        [AskTextCell(None), AskTextCell(None)],
        [AskLabelCell('A'), AskLabelCell('B')]]
    dims = MatrixDimensions(MatrixDimension(1, 2), MatrixDimension(2, 2),
                            MatrixDimension(1, 2))

    async def script(app: _MatrixApp, pilot: Pilot[AnswerCells]) -> bool:
        """Add the label row and check the focus."""
        await _click(app, pilot, ADD_ROW)
        return _enabled_focus(app)
    assert run_matrix(matrix_request(cells, dims), script)[1]


def test_focus_bound() -> None:
    """A delete button keeps the focus until it is disabled at its bound.

    The focus then passes to another enabled widget.
    """
    async def script(app: _MatrixApp,
                     pilot: Pilot[AnswerCells]) -> list[object]:
        """Delete a row twice, reading the focus after each."""
        await _click(app, pilot, ADD_ROW, REMOVE_ROW)
        kept = focused_id(app)
        await _click(app, pilot, REMOVE_ROW)
        return [kept, app.query_one(f'#{REMOVE_ROW}').disabled,
                _enabled_focus(app)]
    assert run_matrix(matrix_request(SHEET, RESIZABLE), script)[1] == \
        [REMOVE_ROW, True, True]


def test_scroll_added() -> None:
    """An appended column beyond the screen is scrolled into view."""
    wide: list[list[AskCell]] = [[AskTextCell(None, width=40)]]
    dims = MatrixDimensions(MatrixDimension(1, 1), MatrixDimension(1, 4),
                            MatrixDimension(1, 3))

    async def script(app: _MatrixApp, pilot: Pilot[AnswerCells]) -> float:
        """Add a fourth wide column and read the sideways scroll."""
        await _click(app, pilot, ADD_COLUMN)
        await pilot.pause()
        return app.query_one('#matrix_scroll', ScrollableContainer).scroll_x
    assert run_matrix(matrix_request(wide, dims), script)[1] > 0
