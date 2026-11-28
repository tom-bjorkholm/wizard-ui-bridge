#! /usr/local/bin/python3
"""Tests for the whole-matrix-form editor."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter as tk
import tkinter.font as tkfont
from typing import Optional
import pytest
from wizard_ui_bridge import AnswerCells, AskCell, CellPosition, \
    MatrixCellSpec, MatrixConsoleQuestion, MatrixDimension, \
    MatrixDimensions, MatrixRequest, PartMatrixValidationRes, \
    PrefillCellValues, \
    PartialMatrixValidator, AskLabelCell, AskIntCell, AskTextCell, \
    AskYesNoCell, AnswerIntCell, AnswerTextCell, AnswerYesNoCell
from wizard_tk_bridge.wizard_matrix import ADD_COLUMN, ADD_ROW, \
    LABEL_WRAP, REMOVE_COLUMN, REMOVE_ROW, MatrixEditor
from .gui_test_helpers import find_widgets, gui_root, \
    record_focus, set_entry

_POS = CellPosition
_CONSOLE = MatrixConsoleQuestion(False, True, True)
_HOURS = AskIntCell('Hours worked.', default=8, min_value=0, max_value=24)
_SHEET: tuple[tuple[AskCell, ...], ...] = (
    (AskLabelCell(''), AskLabelCell('Mon'), AskLabelCell('Tue')),
    (AskLabelCell('Alice'), _HOURS, _HOURS),
    (AskLabelCell('Bob'), _HOURS, _HOURS))
_FIXED = MatrixDimensions.fixed(3, 3)
_RESIZABLE = MatrixDimensions(MatrixDimension(2, 2), MatrixDimension(4, 4),
                              MatrixDimension(3, 3))


# pylint: disable-next=too-few-public-methods
class _Validator:
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


def _request(cells: MatrixCellSpec = _SHEET,
             dimensions: MatrixDimensions = _FIXED,
             validator: Optional[PartialMatrixValidator] = None
             ) -> MatrixRequest:
    """Return a matrix request of the given cells, shape and validator."""
    return MatrixRequest('Fill in the hours.', cells, dimensions, _CONSOLE,
                         validator)


def _build(root: tk.Tk, request: MatrixRequest
           ) -> tuple[MatrixEditor, list[AnswerCells]]:
    """Build a matrix editor recording every submitted answer set."""
    recorded: list[AnswerCells] = []
    editor = MatrixEditor(tk.Frame(root), request, recorded.append)
    return editor, recorded


def _widget(editor: MatrixEditor, row: int, column: int) -> tk.Widget:
    """Return the widget built for one cell of the editor."""
    # pylint: disable-next=protected-access
    return editor._cell(_POS(row, column)).widget


def _entry(editor: MatrixEditor, row: int, column: int) -> tk.Entry:
    """Return the entry of one text or integer cell of the editor."""
    widget = _widget(editor, row, column)
    assert isinstance(widget, tk.Entry)
    return widget


def _status(editor: MatrixEditor) -> str:
    """Return the text of the editor's status line."""
    # pylint: disable-next=protected-access
    return str(editor._status.cget('text'))


def _change(editor: MatrixEditor, row: int, column: int) -> None:
    """React as the editor does when the user changes one cell."""
    # pylint: disable-next=protected-access
    editor._changed(_POS(row, column))


def _focus_on(editor: MatrixEditor, widget: Optional[tk.Widget],
              monkeypatch: pytest.MonkeyPatch) -> None:
    """Make the editor see widget, or nothing, as the focused widget."""
    path = '' if widget is None else str(widget)
    monkeypatch.setattr(editor, '_focus_path', lambda: path)


def test_matrix_answers() -> None:
    """Test the answers have the shape, None for labels, and defaults."""
    with gui_root() as root:
        editor, _ = _build(root, _request())
        answers = editor.answers()
        assert [len(row) for row in answers] == [3, 3, 3]
        assert answers[0] == [None, None, None]
        assert answers[1][0] is None
        assert answers[1][1] == AnswerIntCell(_HOURS, 8)


def test_matrix_label_widget() -> None:
    """Test a label cell is shown as a plain label with its text."""
    with gui_root() as root:
        editor, _ = _build(root, _request())
        label = _widget(editor, 2, 0)
        assert isinstance(label, tk.Label)
        assert str(label.cget('text')) == 'Bob'


def test_matrix_repeats_cells() -> None:
    """Test a short cell sequence repeats its last row and last cell."""
    with gui_root() as root:
        text = AskTextCell(None, default='x')
        cells: list[list[AskCell]] = [[AskLabelCell('Name')], [text]]
        dims = MatrixDimensions.fixed(3, 2)
        answers = _build(root, _request(cells, dims))[0].answers()
        assert answers[0] == [None, None]
        assert list(answers[2]) == [AnswerTextCell(text, 'x')] * 2


def test_matrix_generator() -> None:
    """Test a generator gives each cell, called with its position."""
    def _generate(position: CellPosition) -> AskCell:
        """Return a text cell whose default names the position."""
        return AskTextCell(None, default=f'{position.row}{position.column}')
    with gui_root() as root:
        editor, _ = _build(root, _request(_generate,
                                          MatrixDimensions.fixed(2, 2)))
        values = [[getattr(answer, 'value') for answer in row]
                  for row in editor.answers()]
        assert values == [['00', '01'], ['10', '11']]


def test_matrix_submit_ok() -> None:
    """Test submitting a valid matrix hands its answers on."""
    with gui_root() as root:
        editor, recorded = _build(root, _request())
        set_entry(_entry(editor, 2, 2), '6')
        editor.submit()
        assert len(recorded) == 1
        assert recorded[0][2][2] == AnswerIntCell(_HOURS, 6)


def test_matrix_cell_error() -> None:
    """Test an invalid cell blocks submit and is named by its labels."""
    with gui_root() as root:
        editor, recorded = _build(root, _request())
        set_entry(_entry(editor, 2, 2), '25')
        editor.submit()
        assert not recorded
        assert _status(editor) == \
            'Bob / Tue: Please enter an integer between 0 and 24.'


def test_matrix_live_error() -> None:
    """Test a change of a cell shows that cell's own error at once."""
    with gui_root() as root:
        editor, _ = _build(root, _request())
        set_entry(_entry(editor, 1, 1), 'x')
        _change(editor, 1, 1)
        assert _status(editor) == 'Alice / Mon: Please enter an integer.'


def test_matrix_change_wired() -> None:
    """Test changing an input reports the position of its cell.

    A check box is changed through its own command, which, unlike a key
    press, needs no shown and focused window.
    """
    with gui_root() as root:
        validator = _Validator(PartMatrixValidationRes(True, ''))
        paid = AskYesNoCell(None, default=False)
        cells: list[list[AskCell]] = [[AskLabelCell('Paid?'), paid]]
        editor, _ = _build(root, _request(cells, MatrixDimensions.fixed(1, 2),
                                          validator))
        check = _widget(editor, 0, 1)
        assert isinstance(check, tk.Checkbutton)
        check.invoke()
        assert validator.calls == [None, _POS(0, 1)]
        assert editor.answers()[0][1] == AnswerYesNoCell(paid, True)


def test_matrix_first_call() -> None:
    """Test the validator is called at first show, but its message hidden.

    The cells it disables start disabled, while a fresh matrix does not
    open with a complaint.
    """
    with gui_root() as root:
        result = PartMatrixValidationRes(False, 'Empty.', (_POS(2, 2),))
        validator = _Validator(result)
        editor, _ = _build(root, _request(validator=validator))
        assert validator.calls == [None]
        assert _status(editor) == ''
        assert str(_entry(editor, 2, 2).cget('state')) == 'disabled'
        assert str(_entry(editor, 2, 1).cget('state')) == 'normal'


def test_matrix_live_check() -> None:
    """Test a change runs the validator with its position and shows it."""
    with gui_root() as root:
        validator = _Validator(PartMatrixValidationRes(False, 'Too much.'))
        editor, _ = _build(root, _request(validator=validator))
        _change(editor, 1, 2)
        assert validator.calls == [None, _POS(1, 2)]
        assert validator.answers[1] == editor.answers()
        assert _status(editor) == 'Too much.'


def test_matrix_check_blocks() -> None:
    """Test the validator's verdict blocks submit and shows its message."""
    with gui_root() as root:
        validator = _Validator(PartMatrixValidationRes(False, 'No.'))
        editor, recorded = _build(root, _request(validator=validator))
        editor.submit()
        assert not recorded
        assert validator.calls == [None, None]
        assert _status(editor) == 'No.'


def test_matrix_disabled_cell() -> None:
    """Test a disabled cell is greyed out and its own error is skipped.

    The validator runs first on submit, so the cell it disables is not
    checked and the matrix is submitted although that cell is invalid.
    """
    with gui_root() as root:
        validator = _Validator(PartMatrixValidationRes(True, '',
                                                       (_POS(2, 2),)))
        editor, recorded = _build(root, _request(validator=validator))
        set_entry(_entry(editor, 2, 2), '25')
        editor.submit()
        assert str(_entry(editor, 2, 2).cget('state')) == 'disabled'
        assert len(recorded) == 1


def test_matrix_prefills() -> None:
    """Test prefills are written at first show and after a change.

    A prefill aimed at the changed cell is skipped.
    """
    with gui_root() as root:
        result = PartMatrixValidationRes(
            True, '', prefill_values=((_POS(1, 1), 1), (_POS(1, 2), 2)))
        editor, _ = _build(root, _request(validator=_Validator(result)))
        assert [_entry(editor, 1, 1).get(), _entry(editor, 1, 2).get()] == \
            ['1', '2']
        set_entry(_entry(editor, 1, 1), '5')
        set_entry(_entry(editor, 1, 2), '7')
        _change(editor, 1, 1)
        assert _entry(editor, 1, 1).get() == '5'
        assert _entry(editor, 1, 2).get() == '2'


def test_matrix_bad_prefill() -> None:
    """Test a prefill aimed at a label cell is reported as a bug.

    The validator runs when the matrix is first shown, so the bug shows
    at once.
    """
    with gui_root() as root:
        prefills: PrefillCellValues = ((_POS(0, 1), 'x'),)
        result = PartMatrixValidationRes(True, '', prefill_values=prefills)
        with pytest.raises(TypeError, match='label cell'):
            _build(root, _request(validator=_Validator(result)))


def test_matrix_resize_rows() -> None:
    """Test rows are appended and deleted at the end within the bounds.

    Each change of the shape calls the validator with None, and a row
    deleted and appended again gets fresh cells, losing what was typed.
    """
    with gui_root() as root:
        validator = _Validator(PartMatrixValidationRes(True, ''))
        editor, _ = _build(root, _request(_SHEET, _RESIZABLE, validator))
        set_entry(_entry(editor, 2, 1), '1')
        editor.remove_row()
        editor.remove_row()
        assert editor.shape == MatrixDimension(2, 3)
        editor.add_row()
        editor.add_row()
        editor.add_row()
        assert editor.shape == MatrixDimension(4, 3)
        assert _entry(editor, 2, 1).get() == '8'
        assert validator.calls == [None] * 4
        assert len(editor.answers()) == 4


def test_matrix_resize_cols() -> None:
    """Test columns are appended and deleted at the end within bounds."""
    with gui_root() as root:
        editor, _ = _build(root, _request(_SHEET, _RESIZABLE))
        editor.add_column()
        editor.add_column()
        assert editor.shape == MatrixDimension(3, 4)
        assert isinstance(_widget(editor, 0, 3), tk.Label)
        assert isinstance(_widget(editor, 1, 3), tk.Entry)
        editor.remove_column()
        editor.remove_column()
        editor.remove_column()
        assert editor.shape == MatrixDimension(3, 2)
        assert [len(row) for row in editor.answers()] == [2, 2, 2]


def test_matrix_no_rows() -> None:
    """Test a matrix shown with no rows gets full rows when one is added."""
    with gui_root() as root:
        dims = MatrixDimensions(MatrixDimension(0, 2), MatrixDimension(2, 2),
                                MatrixDimension(0, 2))
        editor, _ = _build(root, _request(_SHEET, dims))
        assert editor.answers() == []
        editor.add_row()
        assert editor.shape == MatrixDimension(1, 2)
        assert editor.answers() == [[None, None]]


def _button_states(root: tk.Misc) -> dict[str, str]:
    """Return the state of every button under root, by its text."""
    return {str(button.cget('text')): str(button.cget('state'))
            for button in find_widgets(root, tk.Button)}


def test_resize_buttons_fixed() -> None:
    """Test a matrix of fixed shape gets no resize buttons."""
    with gui_root() as root:
        editor, _ = _build(root, _request())
        box = tk.Frame(root)
        editor.add_resize_buttons(box)
        assert not find_widgets(box, tk.Button)


def test_resize_buttons_rows() -> None:
    """Test only row buttons are added, each greyed out at its bound."""
    with gui_root() as root:
        dims = MatrixDimensions(MatrixDimension(2, 3), MatrixDimension(3, 3),
                                MatrixDimension(3, 3))
        editor, _ = _build(root, _request(_SHEET, dims))
        box = tk.Frame(root)
        editor.add_resize_buttons(box)
        assert _button_states(box) == {ADD_ROW: 'disabled',
                                       REMOVE_ROW: 'normal'}
        editor.remove_row()
        assert _button_states(box) == {ADD_ROW: 'normal',
                                       REMOVE_ROW: 'disabled'}


def test_resize_buttons_all() -> None:
    """Test a matrix resizable both ways gets all four buttons in order."""
    with gui_root() as root:
        editor, _ = _build(root, _request(_SHEET, _RESIZABLE))
        box = tk.Frame(root)
        editor.add_resize_buttons(box)
        assert list(_button_states(box)) == [ADD_ROW, REMOVE_ROW, ADD_COLUMN,
                                             REMOVE_COLUMN]


def test_matrix_added_return() -> None:
    """Test Return also submits from an input in an appended row."""
    with gui_root() as root:
        editor, _ = _build(root, _request(_SHEET, _RESIZABLE))
        editor.add_row()
        assert _entry(editor, 3, 1).bind('<Return>') != ''


def test_matrix_tooltips() -> None:
    """Test a cell with help text gets a tooltip, and one without none."""
    with gui_root() as root:
        cells: list[list[AskCell]] = [
            [AskLabelCell('Name', help_text='Who.'), AskLabelCell('Plain')],
            [AskTextCell(None), _HOURS]]
        dims = MatrixDimensions.fixed(2, 2)
        editor, _ = _build(root, _request(cells, dims))
        # pylint: disable=protected-access
        tooltips = [editor._cell(_POS(*pair)).tooltip
                    for pair in ((0, 0), (0, 1), (1, 0), (1, 1))]
        # pylint: enable=protected-access
        assert [tip.text if tip is not None else None
                for tip in tooltips] == ['Who.', None, None, 'Hours worked.']


def test_matrix_cell_namer() -> None:
    """Test the cell namer of the request names a cell's own error."""
    def _namer(answers: AnswerCells, position: CellPosition) -> str:
        """Name the cell by its row and the number of its answer rows."""
        return f'Row {position.row} of {len(answers)}'
    with gui_root() as root:
        request = _request()._replace(cell_namer=_namer)
        editor, _ = _build(root, request)
        set_entry(_entry(editor, 2, 2), 'x')
        _change(editor, 2, 2)
        assert _status(editor) == 'Row 2 of 3: Please enter an integer.'


def test_matrix_invalid_focus(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test submit moves the focus to the first invalid enabled cell."""
    focused = record_focus(monkeypatch)
    with gui_root() as root:
        validator = _Validator(PartMatrixValidationRes(True, '',
                                                       (_POS(1, 2),)))
        editor, recorded = _build(root, _request(validator=validator))
        set_entry(_entry(editor, 1, 2), '25')
        set_entry(_entry(editor, 2, 2), '25')
        editor.submit()
        assert not recorded
        assert focused == [_entry(editor, 2, 2)]


@pytest.mark.parametrize('disabled, column', [((), 1), ((_POS(3, 1),), 2)])
def test_matrix_focus_new_row(monkeypatch: pytest.MonkeyPatch,
                              disabled: tuple[CellPosition, ...],
                              column: int) -> None:
    """Test an appended row's first enabled input gets the focus."""
    focused = record_focus(monkeypatch)
    with gui_root() as root:
        validator = _Validator(PartMatrixValidationRes(True, '', disabled))
        editor, _ = _build(root, _request(_SHEET, _RESIZABLE, validator))
        editor.add_row()
        assert focused == [_entry(editor, 3, column)]


def test_matrix_focus_new_col(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test an appended column's first input, below its label, is focused."""
    focused = record_focus(monkeypatch)
    with gui_root() as root:
        editor, _ = _build(root, _request(_SHEET, _RESIZABLE))
        editor.add_column()
        assert focused == [_entry(editor, 1, 3)]


def test_label_row_no_focus(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test an appended row of only labels gives no input the focus."""
    focused = record_focus(monkeypatch)
    with gui_root() as root:
        cells: list[list[AskCell]] = [[AskLabelCell('Name')]]
        dims = MatrixDimensions(MatrixDimension(1, 1), MatrixDimension(2, 1),
                                MatrixDimension(1, 1))
        editor, _ = _build(root, _request(cells, dims))
        editor.add_row()
        assert editor.shape == MatrixDimension(2, 1)
        assert not focused


def test_matrix_scroll_added() -> None:
    """Test an appended row below the visible area is scrolled into view."""
    with gui_root() as root:
        frame = tk.Frame(root)
        frame.pack()
        editor = MatrixEditor(frame, _request(_SHEET, _RESIZABLE),
                              lambda _answers: None)
        canvas = _widget(editor, 0, 0).master.master
        assert isinstance(canvas, tk.Canvas)
        canvas.configure(height=40)
        editor.add_row()
        assert canvas.yview()[0] > 0


@pytest.mark.parametrize('focus_row, expected', [(3, True), (1, False),
                                                 (None, False)])
def test_remove_row_refocus(monkeypatch: pytest.MonkeyPatch,
                            focus_row: Optional[int], expected: bool) -> None:
    """Test deleting the focused row moves the focus to the new last row.

    The focus is left alone when it was in a row that is kept, or not in
    the matrix at all.
    """
    focused = record_focus(monkeypatch)
    with gui_root() as root:
        editor, _ = _build(root, _request(_SHEET, _RESIZABLE))
        editor.add_row()
        focused.clear()
        was = None if focus_row is None else _entry(editor, focus_row, 1)
        _focus_on(editor, was, monkeypatch)
        editor.remove_row()
        assert focused == ([_entry(editor, 2, 1)] if expected else [])


def test_remove_col_refocus(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test deleting the focused column focuses the new last column."""
    focused = record_focus(monkeypatch)
    with gui_root() as root:
        editor, _ = _build(root, _request(_SHEET, _RESIZABLE))
        _focus_on(editor, _entry(editor, 2, 2), monkeypatch)
        editor.remove_column()
        assert focused == [_entry(editor, 1, 1)]


@pytest.mark.parametrize('bold, italic, weight, slant', [
    (True, False, 'bold', 'roman'), (False, True, 'normal', 'italic'),
    (True, True, 'bold', 'italic')])
def test_matrix_label_style(bold: bool, italic: bool, weight: str,
                            slant: str) -> None:
    """Test a label cell asking for bold or italics gets that font."""
    with gui_root() as root:
        cells: list[list[AskCell]] = [
            [AskLabelCell('Day', bold=bold, italic=italic)]]
        editor, _ = _build(root, _request(cells, MatrixDimensions.fixed(1, 1)))
        actual = tkfont.Font(root, _widget(editor, 0, 0).cget('font')).actual()
        assert (actual['weight'], actual['slant']) == (weight, slant)


def test_matrix_label_width() -> None:
    """Test a label wraps at its width hint, in average digit widths."""
    with gui_root() as root:
        cells: list[list[AskCell]] = [
            [AskLabelCell('Plain'), AskLabelCell('Narrow', width=10)]]
        editor, _ = _build(root, _request(cells, MatrixDimensions.fixed(1, 2)))
        plain, narrow = _widget(editor, 0, 0), _widget(editor, 0, 1)
        digit = tkfont.Font(root, narrow.cget('font')).measure('0')
        assert int(plain.cget('wraplength')) == LABEL_WRAP
        assert int(narrow.cget('wraplength')) == 10 * digit


def test_matrix_input_widths() -> None:
    """Test inputs are compact by default, and a width hint wins."""
    with gui_root() as root:
        cells: list[list[AskCell]] = [
            [_HOURS, AskIntCell(None, width=3), AskTextCell(None)]]
        editor, _ = _build(root, _request(cells, MatrixDimensions.fixed(1, 3)))
        assert [int(_entry(editor, 0, column).cget('width'))
                for column in range(3)] == [8, 3, 20]
