#! /usr/bin/env python3
"""Tests for the cells and validation of the Textual matrix form screen.

The screen is resized in the tests of test_ui_textual_resize.py, and a
table asked through it in those of test_ui_textual_table.py.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

# pylint: disable=protected-access

from datetime import date
from typing import Optional
import pytest
from textual.pilot import Pilot
from textual.widgets import Button, Input, Static
from wizard_ui_bridge import AnswerCells, AskCell, CellPosition, \
    MatrixDimensions, PartMatrixValidationRes, PathAskOptions, \
    PrefillCellValues, AskLabelCell, AskTextCell, AskYesNoCell, \
    AskChoiceCell, AskPathCell, AskDateCell, AnswerIntCell, AnswerTextCell, \
    AnswerYesNoCell, WizardBack
from wizard_ui_bridge._calendar import _CalendarScreen
from wizard_ui_bridge._path import _PickerScreen
from wizard_ui_bridge._textual_matrix import _MatrixApp
from .textual_matrix_support import HOURS, POS, Recorder, \
    focused_id, matrix_request, run_matrix, status, type_in
from .ui_textual_support import _CannedBridge


async def _read(app: _MatrixApp, _pilot: Pilot[AnswerCells]) -> AnswerCells:
    """Return the answers of the mounted screen."""
    return app.answers()


def test_matrix_answers() -> None:
    """The answers have the shape, None for labels, and the defaults."""
    answers = run_matrix(matrix_request(), _read)[1]
    assert [len(row) for row in answers] == [3, 3, 3]
    assert answers[0] == [None, None, None]
    assert answers[1][0] is None
    assert answers[1][1] == AnswerIntCell(HOURS, 8)


def test_matrix_repeats_cells() -> None:
    """A short cell sequence repeats its last row and its last cell."""
    text = AskTextCell(None, default='x')
    cells: list[list[AskCell]] = [[AskLabelCell('Name')], [text]]
    request = matrix_request(cells, MatrixDimensions.fixed(3, 2))
    answers = run_matrix(request, _read)[1]
    assert answers[0] == [None, None]
    assert list(answers[2]) == [AnswerTextCell(text, 'x')] * 2


def test_matrix_generator() -> None:
    """A generator gives each cell, called with its position."""
    def generate(position: CellPosition) -> AskCell:
        """Return a text cell whose default names the position."""
        return AskTextCell(None, default=f'{position.row}{position.column}')
    request = matrix_request(generate, MatrixDimensions.fixed(2, 2))
    answers = run_matrix(request, _read)[1]
    assert [[getattr(answer, 'value') for answer in row]
            for row in answers] == [['00', '01'], ['10', '11']]


def test_matrix_labels() -> None:
    """A label shows its text as it is, in its style and width hint."""
    cells: list[list[AskCell]] = [[
        AskLabelCell('[b]Mon[/b]', bold=True, italic=True, width=4),
        AskLabelCell('Plain')]]

    async def script(app: _MatrixApp,
                     _pilot: Pilot[AnswerCells]) -> list[object]:
        """Read the text, style and width of both labels."""
        found: list[object] = []
        for widget_id in ('#cell_0_0', '#cell_0_1'):
            label = app.query_one(widget_id, Static)
            style = label.styles.text_style
            width = label.styles.inline.width
            found += [str(label.render()), bool(style.bold),
                      bool(style.italic), width is not None]
        return found
    found = run_matrix(matrix_request(cells, MatrixDimensions.fixed(1, 2)),
                       script)[1]
    assert found == ['[b]Mon[/b]', True, True, True,
                     'Plain', False, False, False]


def test_matrix_tooltips() -> None:
    """A cell with help text gets it as tooltip, and one without none."""
    cells: list[list[AskCell]] = [
        [AskLabelCell('Name', help_text='Who.'), AskLabelCell('Plain')],
        [AskTextCell(None), HOURS]]

    async def script(app: _MatrixApp,
                     _pilot: Pilot[AnswerCells]) -> list[object]:
        """Read the tooltip of each cell."""
        return [app.query_one(f'#cell_{row}_{column}').tooltip
                for row, column in ((0, 0), (0, 1), (1, 0), (1, 1))]
    found = run_matrix(matrix_request(cells, MatrixDimensions.fixed(2, 2)),
                       script)[1]
    assert found == ['Who.', None, None, 'Hours worked.']


def test_matrix_submit_ok() -> None:
    """Submitting a valid matrix exits with its answers."""
    async def script(app: _MatrixApp, pilot: Pilot[AnswerCells]) -> None:
        """Change a cell and submit."""
        await type_in(app, pilot, (2, 2), '6')
        await pilot.press('ctrl+s')
    app = run_matrix(matrix_request(), script)[0]
    assert app.return_value is not None
    assert app.return_value[2][2] == AnswerIntCell(HOURS, 6)


def test_matrix_cell_error() -> None:
    """An invalid cell blocks submit, takes the focus and is named.

    Its input is framed in the error colour.
    """
    async def script(app: _MatrixApp,
                     pilot: Pilot[AnswerCells]) -> list[object]:
        """Make a cell invalid, move the focus away and submit."""
        await type_in(app, pilot, (2, 2), '25')
        app.query_one('#cell_1_1').focus()
        await pilot.press('ctrl+s')
        return [status(app), focused_id(app),
                app.query_one('#cell_2_2').has_class('cell_error')]
    app, found = run_matrix(matrix_request(), script)
    assert app.return_value is None
    assert found == ['Bob / Tue: Please enter an integer between 0 and 24.',
                     'cell_2_2', True]


def test_matrix_live_error() -> None:
    """A change of a cell shows that cell's own error until it is fixed."""
    async def script(app: _MatrixApp,
                     pilot: Pilot[AnswerCells]) -> list[object]:
        """Make a cell invalid, then valid again."""
        await type_in(app, pilot, (1, 1), 'x')
        found: list[object] = [
            status(app), app.query_one('#cell_1_1').has_class('cell_error')]
        await type_in(app, pilot, (1, 1), '7')
        return found + [status(app), len(app.query('.cell_error'))]
    found = run_matrix(matrix_request(), script)[1]
    assert found == ['Alice / Mon: Please enter an integer.', True, '', 0]


def test_matrix_cell_namer() -> None:
    """The cell namer of the request names a cell's own error."""
    def namer(answers: AnswerCells, position: CellPosition) -> str:
        """Name the cell by its row and the number of answer rows."""
        return f'Row {position.row} of {len(answers)}'

    async def script(app: _MatrixApp, pilot: Pilot[AnswerCells]) -> str:
        """Make a cell invalid and read the message."""
        await type_in(app, pilot, (2, 2), 'x')
        return status(app)
    request = matrix_request()._replace(cell_namer=namer)
    assert run_matrix(request, script)[1] == \
        'Row 2 of 3: Please enter an integer.'


def test_matrix_first_call() -> None:
    """The validator is called at first show, but its message is hidden.

    The cell it disables starts disabled, and the change events Textual
    posts as it mounts the inputs, which hold values, are not taken as
    changes by the user.
    """
    validator = Recorder(PartMatrixValidationRes(False, 'Empty.',
                                                 (POS(2, 2),)))

    async def script(app: _MatrixApp,
                     _pilot: Pilot[AnswerCells]) -> list[object]:
        """Read the status and which inputs are disabled."""
        return [status(app), app.query_one('#cell_2_2').disabled,
                app.query_one('#cell_2_1').disabled]
    found = run_matrix(matrix_request(validator=validator), script)[1]
    assert found == ['', True, False]
    assert validator.calls == [None]


def test_matrix_no_echo() -> None:
    """Mounting a drop-down or text with a start value is no change."""
    validator = Recorder(PartMatrixValidationRes(False, 'Rejected.'))
    cells: list[list[AskCell]] = [[
        AskChoiceCell(None, ('a', 'b'), default='b'),
        AskTextCell(None, start_value='x'),
        AskYesNoCell(None, default=True)]]
    request = matrix_request(cells, MatrixDimensions.fixed(1, 3), validator)

    async def script(app: _MatrixApp, _pilot: Pilot[AnswerCells]) -> str:
        """Read the status of the fresh screen."""
        return status(app)
    assert run_matrix(request, script)[1] == ''
    assert validator.calls == [None]


def test_matrix_live_check() -> None:
    """A change runs the validator with its position and shows it."""
    validator = Recorder(PartMatrixValidationRes(False, 'Too much.'))

    async def script(app: _MatrixApp,
                     pilot: Pilot[AnswerCells]) -> list[object]:
        """Change a cell and read the answers and the status."""
        await type_in(app, pilot, (1, 2), '9')
        return [app.answers(), status(app)]
    request = matrix_request(validator=validator)
    answers, shown = run_matrix(request, script)[1]
    assert validator.calls == [None, POS(1, 2)]
    assert validator.answers[1] == answers
    assert shown == 'Too much.'


def test_matrix_check_blocks() -> None:
    """The validator's verdict blocks submit and shows its message."""
    validator = Recorder(PartMatrixValidationRes(False, 'No.'))

    async def script(app: _MatrixApp, pilot: Pilot[AnswerCells]) -> str:
        """Submit the fresh matrix and read the status."""
        await pilot.press('ctrl+s')
        return status(app)
    app, shown = run_matrix(matrix_request(validator=validator), script)
    assert app.return_value is None
    assert validator.calls == [None, None]
    assert shown == 'No.'


def test_matrix_disabled_cell() -> None:
    """A disabled cell's own error is skipped live and on submit."""
    validator = Recorder(PartMatrixValidationRes(True, '', (POS(2, 2),)))

    async def script(app: _MatrixApp, pilot: Pilot[AnswerCells]) -> str:
        """Make the disabled cell invalid and submit."""
        await type_in(app, pilot, (2, 2), '25')
        shown = status(app)
        await pilot.press('ctrl+s')
        return shown
    app, shown = run_matrix(matrix_request(validator=validator), script)
    assert shown == ''
    assert app.return_value is not None


def test_matrix_prefills() -> None:
    """Prefills are written at first show and as if typed after a change.

    The validator prefills Alice's Mon with 1 at first show, which is not
    taken as a change by the user. When Mon changes it prefills Tue with
    twice Mon, which runs the validator for Tue as if the user typed it,
    and Mon itself with 0, which is skipped as Mon is the changed cell.
    """
    calls: list[Optional[CellPosition]] = []

    def doubler(answers: AnswerCells,
                changed: Optional[CellPosition]) -> PartMatrixValidationRes:
        """Record the call and prefill as described above."""
        calls.append(changed)
        monday = answers[1][1]
        assert isinstance(monday, AnswerIntCell)
        if changed is None:
            prefills: PrefillCellValues = ((POS(1, 1), 1),)
        elif changed == POS(1, 1) and monday.value is not None:
            prefills = ((POS(1, 1), 0), (POS(1, 2), 2 * monday.value))
        else:
            prefills = ()
        return PartMatrixValidationRes(True, '', prefill_values=prefills)

    async def script(app: _MatrixApp, pilot: Pilot[AnswerCells]) -> list[str]:
        """Read Alice's Mon and Tue at first show and after changing Mon."""
        def row() -> list[str]:
            """Return the texts of Alice's Mon and Tue."""
            return [app.query_one(f'#cell_1_{column}', Input).value
                    for column in (1, 2)]
        first = row()
        await type_in(app, pilot, (1, 1), '3')
        return first + row()
    found = run_matrix(matrix_request(validator=doubler), script)[1]
    assert found == ['1', '8', '3', '6']
    assert calls == [None, POS(1, 1), POS(1, 2)]


def test_matrix_bad_prefill() -> None:
    """A prefill aimed at a label cell is reported as a validator bug."""
    prefills: PrefillCellValues = ((POS(0, 1), 'x'),)
    validator = Recorder(PartMatrixValidationRes(True, '',
                                                 prefill_values=prefills))
    with pytest.raises(TypeError, match='label cell'):
        run_matrix(matrix_request(validator=validator), _read)


def test_matrix_check_box() -> None:
    """Clicking a check box changes its answer and runs the validator."""
    validator = Recorder(PartMatrixValidationRes(True, ''))
    paid = AskYesNoCell(None, default=False)
    cells: list[list[AskCell]] = [[AskLabelCell('Paid?'), paid]]
    request = matrix_request(cells, MatrixDimensions.fixed(1, 2), validator)

    async def script(app: _MatrixApp,
                     pilot: Pilot[AnswerCells]) -> AnswerCells:
        """Click the check box and read the answers."""
        await pilot.click('#cell_0_1')
        await pilot.pause()
        return app.answers()
    answers = run_matrix(request, script)[1]
    assert validator.calls == [None, POS(0, 1)]
    assert answers[0][1] == AnswerYesNoCell(paid, True)


_DIALOG_CELLS: list[list[AskCell]] = [[
    AskPathCell(None, PathAskOptions()), AskDateCell(None, nullable=True)]]


def test_dialog_buttons() -> None:
    """A path and a date cell get a narrow button opening their dialog."""
    async def script(app: _MatrixApp,
                     pilot: Pilot[AnswerCells]) -> list[object]:
        """Read the button labels and open and cancel each dialog."""
        found: list[object] = [
            str(app.query_one(button_id, Button).label)
            for button_id in ('#browse_0_0', '#pick_0_1')]
        for button_id in ('#browse_0_0', '#pick_0_1'):
            await pilot.click(button_id)
            await pilot.pause()
            found.append(type(app.screen))
            await pilot.press('escape')
            await pilot.pause()
        return found
    request = matrix_request(_DIALOG_CELLS, MatrixDimensions.fixed(1, 2))
    assert run_matrix(request, script)[1] == \
        ['…', '…', _PickerScreen, _CalendarScreen]


def test_matrix_date_token() -> None:
    """Typing '?' into a date cell opens the calendar to pick a day."""
    async def script(app: _MatrixApp, pilot: Pilot[AnswerCells]) -> str:
        """Type the token, pick the 20th and read the cell."""
        await type_in(app, pilot, (0, 1), '?')
        await pilot.click('#day_20')
        await pilot.pause()
        return app.query_one('#cell_0_1', Input).value
    request = matrix_request(_DIALOG_CELLS, MatrixDimensions.fixed(1, 2))
    assert run_matrix(request, script)[1] == \
        date.today().replace(day=20).isoformat()


def test_ask_matrix_canned() -> None:
    """ask_matrix_form() returns the answers the screen exited with.

    The screen gets the buffered messages and the re-ask reason.
    """
    bridge = _CannedBridge([[[None]]])
    bridge.show('note')
    answers = bridge.ask_matrix_form(matrix_request(), re_ask_reason='bad')
    assert answers == [[None]]
    app = bridge.launched[0]
    assert isinstance(app, _MatrixApp)
    assert app._messages == ['note', 'bad']


def test_ask_matrix_nav() -> None:
    """ask_matrix_form() re-raises a navigation request of the screen."""
    bridge = _CannedBridge([WizardBack])
    with pytest.raises(WizardBack):
        bridge.ask_matrix_form(matrix_request())


def test_matrix_nav_key() -> None:
    """ctrl+b on the matrix screen records a back request and exits."""
    async def script(_app: _MatrixApp, pilot: Pilot[AnswerCells]) -> None:
        """Press the back key."""
        await pilot.press('ctrl+b')
    app = run_matrix(matrix_request(), script)[0]
    assert app.return_value is None
    assert app.nav is WizardBack
