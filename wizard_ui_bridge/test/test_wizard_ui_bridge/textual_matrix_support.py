#! /usr/bin/env python3
"""Shared helpers for the tests of the Textual matrix form screen.

The screen is driven headlessly by a script, a coroutine that gets the
running screen and its pilot, so a test can change cells, press keys
and read the screen while it runs. A small timesheet matrix and a
validator recording its calls serve most of the tests.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import asyncio
from typing import Awaitable, Callable, Optional, TypeVar
from textual.pilot import Pilot
from textual.widgets import Input, Static
from wizard_ui_bridge import AnswerCells, AskCell, CellPosition, \
    MatrixCellSpec, MatrixConsoleQuestion, MatrixDimension, \
    MatrixDimensions, MatrixRequest, PartMatrixValidationRes, \
    PartialMatrixValidator, AskLabelCell, AskIntCell, WizardUiBridgeTextual
from wizard_ui_bridge._textual_matrix import _MatrixApp
from wizard_ui_bridge._textual_nav import _NavApp

_T = TypeVar('_T')
POS = CellPosition
CONSOLE = MatrixConsoleQuestion(False, True, True)
HOURS = AskIntCell('Hours worked.', default=8, min_value=0, max_value=24)
SHEET: tuple[tuple[AskCell, ...], ...] = (
    (AskLabelCell(''), AskLabelCell('Mon'), AskLabelCell('Tue')),
    (AskLabelCell('Alice'), HOURS, HOURS),
    (AskLabelCell('Bob'), HOURS, HOURS))
FIXED = MatrixDimensions.fixed(3, 3)
RESIZABLE = MatrixDimensions(MatrixDimension(2, 2), MatrixDimension(4, 4),
                             MatrixDimension(3, 3))


# The Tk matrix tests keep the same recording validator. One package's
# tests cannot import another's, so duplicate-code is turned off for it.
# pylint: disable=duplicate-code
# pylint: disable-next=too-few-public-methods
class Recorder:
    """A partial validator recording its calls and giving a set result."""

    def __init__(self, result: PartMatrixValidationRes) -> None:
        """Keep the result to return and start with no calls."""
        self.result = result
        self.calls: list[Optional[CellPosition]] = []
        self.answers: list[AnswerCells] = []

    def __call__(self, answers: AnswerCells,
                 changed: Optional[CellPosition]) -> PartMatrixValidationRes:
        """Record the call and return the set result."""
        self.calls.append(changed)
        self.answers.append(answers)
        return self.result
# pylint: enable=duplicate-code


def matrix_request(cells: MatrixCellSpec = SHEET,
                   dimensions: MatrixDimensions = FIXED,
                   validator: Optional[PartialMatrixValidator] = None
                   ) -> MatrixRequest:
    """Return a matrix request of the given cells, shape and validator."""
    return MatrixRequest('Fill in the hours.', cells, dimensions, CONSOLE,
                         validator)


def run_app(app: _MatrixApp,
            script: Callable[[_MatrixApp, Pilot[AnswerCells]], Awaitable[_T]]
            ) -> _T:
    """Run a matrix screen headlessly through a script, return its result.

    The script starts once the screen is mounted and its mount events
    are handled.
    """
    async def scenario() -> _T:
        async with app.run_test(size=(120, 40)) as pilot:
            await pilot.pause()
            return await script(app, pilot)
    return asyncio.run(scenario())


def run_matrix(request: MatrixRequest,
               script: Callable[[_MatrixApp, Pilot[AnswerCells]],
                                Awaitable[_T]]) -> tuple[_MatrixApp, _T]:
    """Run the matrix screen of a request through a script.

    The screen is returned with the script's result, so a test can read
    the answers the screen exited with.
    """
    app = _MatrixApp(request, [])
    return app, run_app(app, script)


async def type_in(app: _MatrixApp, pilot: Pilot[AnswerCells],
                  position: tuple[int, int], text: str) -> None:
    """Set the text of a text-like cell as if the user had typed it."""
    row, column = position
    app.query_one(f'#cell_{row}_{column}', Input).value = text
    await pilot.pause()


def status(app: _MatrixApp) -> str:
    """Return the text shown in the status line of the matrix screen."""
    return str(app.query_one('#matrix_status', Static).render())


def focused_id(app: _MatrixApp) -> Optional[str]:
    """Return the id of the focused widget, or None when none has focus."""
    return None if app.focused is None else app.focused.id


class ScriptedBridge(WizardUiBridgeTextual):
    """Textual bridge running each matrix screen through a script.

    It stands in for a user at a real terminal, so a test can ask a
    question through the bridge, such as a table through the inherited
    ask_table(), and answer it on the real matrix screen.
    """

    def __init__(self, script: Callable[[_MatrixApp, Pilot[AnswerCells]],
                                        Awaitable[None]]) -> None:
        """Store the script that answers each matrix screen."""
        super().__init__()
        self._script = script

    def _launch(self, app: _NavApp[_T]) -> Optional[_T]:
        """Run a matrix screen through the script, return its result."""
        matrix = app
        assert isinstance(matrix, _MatrixApp)
        run_app(matrix, self._script)
        return app.return_value
