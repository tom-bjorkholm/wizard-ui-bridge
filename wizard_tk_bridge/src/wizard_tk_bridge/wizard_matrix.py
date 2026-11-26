#! /usr/local/bin/python3
"""A whole matrix form shown on one screen.

A matrix form asks a grid of cells at once. :class:`MatrixEditor` builds
one widget per cell of the current shape: a plain label for an
AskLabelCell, and for every other cell a
:class:`~wizard_tk_bridge.wizard_cell.CellInput`, the same input a form
row shows. It reads the answers of the current shape, runs the optional
partial validator after every change of a cell and of the shape to show
advisory feedback, disable irrelevant cells and apply prefills, and
validates every enabled cell on submit, so a submitted matrix is always
complete. The partial validator is not called when the matrix is first
shown, only once the user changes it, and on submit.

When the minimum and maximum dimensions of a request differ,
:meth:`MatrixEditor.add_resize_buttons` adds buttons that append or
delete the last row or column, each greyed out at its bound. Return in an
input submits the matrix, also in a row or column added later, since each
input is bound when it is built.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter as tk
from dataclasses import dataclass
from functools import partial
from itertools import product
from typing import Callable, Iterator, Optional
from wizard_ui_bridge import AnswerCell, AnswerCells, AskCell, AskLabelCell, \
    CellPosition, MatrixDimension, MatrixRequest, PrefillCellValues
from wizard_ui_bridge.form_helpers import answer_of
from wizard_ui_bridge.matrix_helpers import cell_at, cell_name, \
    valid_cell_prefills
from wizard_tk_bridge.gui_style import bind_submit
from wizard_tk_bridge.wizard_cell import CellInput, HelpTooltip, \
    build_input, scrolled_editor, tooltip_text

ADD_ROW = '+ Row'
REMOVE_ROW = '− Row'
ADD_COLUMN = '+ Column'
REMOVE_COLUMN = '− Column'
LABEL_WRAP = 220


@dataclass(frozen=True)
class MatrixCell:
    """One built matrix cell: its AskCell, widget, input and tooltip.

    A label cell has no input.
    """

    ask: AskCell
    widget: tk.Widget
    cell_input: Optional[CellInput] = None
    tooltip: Optional[HelpTooltip] = None

    def answer(self) -> Optional[AnswerCell]:
        """Return the current answer of the cell, or None for a label."""
        if self.cell_input is None:
            return None
        return answer_of(self.ask, self.cell_input.value())

    def error(self) -> Optional[str]:
        """Return the cell's own validation error, or None when valid."""
        return None if self.cell_input is None else self.cell_input.error()


def _cell_tooltip(ask: AskCell, widget: tk.Widget) -> Optional[HelpTooltip]:
    """Return a hover tooltip for the cell's help and format hint."""
    text = tooltip_text(ask)
    return None if text is None else HelpTooltip(text, widget, (widget,))


# pylint: disable-next=too-many-instance-attributes
class MatrixEditor:
    """A grid of label and input cells that asks a whole matrix form."""

    def __init__(self, parent: tk.Misc, request: MatrixRequest,
                 on_submit: Callable[[AnswerCells], None]) -> None:
        """Build the cells of the default shape, plus a status line."""
        self._request = request
        self._on_submit = on_submit
        self._disabled: frozenset[CellPosition] = frozenset()
        self._last_changed: Optional[CellPosition] = None
        self._resizers: dict[str, tk.Button] = {}
        self._grid, self._status = scrolled_editor(parent, sideways=True)
        default = request.dimensions.default
        self._shape = MatrixDimension(0, default.columns)
        self._cells: list[list[MatrixCell]] = []
        for _ in range(default.rows):
            self._append_row()

    @property
    def shape(self) -> MatrixDimension:
        """Return the current number of rows and columns."""
        return self._shape

    def answers(self) -> list[list[Optional[AnswerCell]]]:
        """Return the current answers, one list per row of the shape."""
        return [[cell.answer() for cell in row] for row in self._cells]

    def submit(self) -> None:
        """Validate the whole matrix and submit its answers when valid.

        The partial validator runs first, so the cells it disables are not
        checked. Every enabled cell must then pass its own check, and the
        validator must accept the matrix.
        """
        problem = self._validate(self._last_changed, live=False)
        message = self._first_error() or problem
        if message is not None:
            self._show(message)
            return
        self._on_submit(self.answers())

    def add_resize_buttons(self, box: tk.Frame) -> None:
        """Add the buttons that append or delete the last row or column.

        Only a dimension whose minimum and maximum differ gets buttons.
        """
        bounds = self._request.dimensions
        actions: list[tuple[str, Callable[[], None]]] = []
        if bounds.min.rows != bounds.max.rows:
            actions += [(ADD_ROW, self.add_row), (REMOVE_ROW, self.remove_row)]
        if bounds.min.columns != bounds.max.columns:
            actions += [(ADD_COLUMN, self.add_column),
                        (REMOVE_COLUMN, self.remove_column)]
        for text, command in actions:
            button = tk.Button(box, text=text, command=command)
            button.pack(side='left', padx=6)
            self._resizers[text] = button
        self._update_resizers()

    def add_row(self) -> None:
        """Append a row of fresh cells, up to the maximum row count."""
        if self._allowed()[ADD_ROW]:
            self._append_row()
            self._reshaped()

    def remove_row(self) -> None:
        """Delete the last row, down to the minimum row count."""
        if self._allowed()[REMOVE_ROW]:
            for cell in self._cells.pop():
                cell.widget.destroy()
            self._shape = MatrixDimension(self._shape.rows - 1,
                                          self._shape.columns)
            self._reshaped()

    def add_column(self) -> None:
        """Append a column of fresh cells, up to the maximum column count."""
        if self._allowed()[ADD_COLUMN]:
            column = self._shape.columns
            for row, cells in enumerate(self._cells):
                cells.append(self._build_cell(CellPosition(row, column)))
            self._shape = MatrixDimension(self._shape.rows, column + 1)
            self._reshaped()

    def remove_column(self) -> None:
        """Delete the last column, down to the minimum column count."""
        if self._allowed()[REMOVE_COLUMN]:
            for cells in self._cells:
                cells.pop().widget.destroy()
            self._shape = MatrixDimension(self._shape.rows,
                                          self._shape.columns - 1)
            self._reshaped()

    def _allowed(self) -> dict[str, bool]:
        """Return for each resize action whether the bounds allow it."""
        low = self._request.dimensions.min
        high = self._request.dimensions.max
        now = self._shape
        return {ADD_ROW: now.rows < high.rows, REMOVE_ROW: now.rows > low.rows,
                ADD_COLUMN: now.columns < high.columns,
                REMOVE_COLUMN: now.columns > low.columns}

    def _update_resizers(self) -> None:
        """Grey out each resize button whose action the bounds forbid."""
        allowed = self._allowed()
        for text, button in self._resizers.items():
            button['state'] = 'normal' if allowed[text] else 'disabled'

    def _append_row(self) -> None:
        """Build the cells of a new last row of the current columns."""
        row = self._shape.rows
        self._cells.append([self._build_cell(CellPosition(row, column))
                            for column in range(self._shape.columns)])
        self._shape = MatrixDimension(row + 1, self._shape.columns)

    def _reshaped(self) -> None:
        """Update the resize buttons and re-validate the whole matrix."""
        self._update_resizers()
        self._last_changed = None
        self._show(self._validate(None, live=True) or '')

    def _build_cell(self, position: CellPosition) -> MatrixCell:
        """Build and place the label or input of one cell."""
        ask = cell_at(self._request.ask_cells, position)
        widget, cell_input = self._new_widget(ask, position)
        widget.grid(row=position.row, column=position.column, sticky='w',
                    padx=4, pady=2)
        return MatrixCell(ask, widget, cell_input, _cell_tooltip(ask, widget))

    def _new_widget(self, ask: AskCell, position: CellPosition
                    ) -> tuple[tk.Widget, Optional[CellInput]]:
        """Return a new label, or a new input bound to Return and change."""
        if isinstance(ask, AskLabelCell):
            label = tk.Label(self._grid, text=ask.text, justify='left',
                             wraplength=LABEL_WRAP)
            return label, None
        built = build_input(self._grid, ask, partial(self._changed, position))
        bind_submit(built.widget, self.submit)
        return built.widget, built

    def _positions(self) -> Iterator[CellPosition]:
        """Yield every position of the current shape, row by row."""
        for row, column in product(range(self._shape.rows),
                                   range(self._shape.columns)):
            yield CellPosition(row, column)

    def _asks(self) -> list[list[AskCell]]:
        """Return the AskCells of the current shape, one list per row."""
        return [[cell.ask for cell in row] for row in self._cells]

    def _changed(self, position: CellPosition) -> None:
        """React to a cell change with live feedback and cell enabling."""
        self._last_changed = position
        message = self._validate(position, live=True)
        own = None if position in self._disabled \
            else self._cell_error(position)
        self._show(own or message or '')

    def _validate(self, changed: Optional[CellPosition],
                  live: bool) -> Optional[str]:
        """Run the partial validator and return its message when invalid.

        The disabled cells of its result are applied, and while the user
        edits (live) its prefills too, which are ignored on submit.
        """
        validator = self._request.partial_validator
        if validator is None:
            return None
        result = validator(self.answers(), changed)
        self._apply_disabled(result.disable_cells)
        if live:
            self._apply_prefills(result.prefill_values, changed)
        return None if result.is_valid else result.message

    def _apply_disabled(self, positions: tuple[CellPosition, ...]) -> None:
        """Enable or disable each input to match the validator result."""
        self._disabled = frozenset(positions)
        for position in self._positions():
            cell_input = self._cell(position).cell_input
            if cell_input is not None:
                cell_input.set_enabled(position not in self._disabled)

    def _apply_prefills(self, prefills: PrefillCellValues,
                        changed: Optional[CellPosition]) -> None:
        """Write the validator's valid prefills into their cell inputs."""
        for position, value in valid_cell_prefills(self._asks(), changed,
                                                   prefills):
            cell_input = self._cell(position).cell_input
            assert cell_input is not None
            cell_input.write(value)

    def _first_error(self) -> Optional[str]:
        """Return the first enabled cell's own error, or None."""
        for position in self._positions():
            if position not in self._disabled:
                error = self._cell_error(position)
                if error is not None:
                    return error
        return None

    def _cell_error(self, position: CellPosition) -> Optional[str]:
        """Return one cell's own error, prefixed with the cell's name.

        The whole matrix shares one status line, so naming the cell by
        its labels makes clear which cell a message refers to.
        """
        error = self._cell(position).error()
        if error is None:
            return None
        return f'{cell_name(self._asks(), position)}: {error}'

    def _cell(self, position: CellPosition) -> MatrixCell:
        """Return the built cell at a position of the current shape."""
        return self._cells[position.row][position.column]

    def _show(self, message: str) -> None:
        """Show a status message below the matrix."""
        self._status.config(text=message)
