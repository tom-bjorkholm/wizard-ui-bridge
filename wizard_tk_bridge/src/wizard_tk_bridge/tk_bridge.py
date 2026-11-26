#! /usr/local/bin/python3
"""Graphical Tkinter bridge that drives a synchronous wizard.

:class:`WizardUiBridgeTk` is a concrete :class:`WizardUiBridge` that
overrides every typed ask method with a real Tkinter control, including
the GUI-recommended ones: ask_path() opens a native file or directory
picker, ask_form() shows a whole form on one screen so the user
answers related fields together in any order, and ask_matrix_form()
shows a whole grid of cells on one screen the same way. All questions of one
wizard session are answered in a single reused
:class:`~wizard_tk_bridge.wizard_window.WizardWindow`, so the session
does not jump around the display.

The bridge supports three ways an application can show the wizard:

- In a new window of its own: give ``parent``, the Tk widget the new
  window is shown over. This suits an application with other windows.
- Embedded in an area the application already built: give ``area``, the
  frame or other container the wizard should fill instead of a window of
  its own.
- In a window of its own over a hidden root the bridge itself owns: give
  neither ``parent`` nor ``area``. This suits a standalone CLI program
  that has no other Tkinter code.

At most one of ``parent`` and ``area`` may be given.

Whichever of the three is used, ``modal`` decides whether the wizard
grabs its window (or the window containing ``area``) for the duration of
the session, so the rest of that window is unusable meanwhile. The
application is best placed to decide this, since only it knows whether
its other content should stay usable while the wizard runs.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Literal, Optional, Sequence, TextIO, overload
from pathlib import Path
import tkinter as tk
from wizard_ui_bridge import AnswerCells, AnswerFields, AskField, AskFields, \
    MatrixRequest, PartialCheck, PartialFormValidator, PathAskOptions, \
    TableCell, TableColumn, WizardUiBridge
from wizard_ui_bridge.arg_types import check_nullable
from wizard_ui_bridge.bridge_helpers import check_text_args
from wizard_tk_bridge._no_text_io import NoTextIO
from wizard_tk_bridge.wizard_form import handles_field
from wizard_tk_bridge.wizard_window import WizardWindow


class WizardUiBridgeTk(WizardUiBridge):
    """Bridge that answers wizard prompts through Tkinter widgets."""

    def __init__(self, parent: Optional[tk.Misc] = None,
                 area: Optional[tk.Misc] = None, modal: bool = True,
                 log: Optional[TextIO] = None) -> None:
        """Store where and how to show the wizard, and the optional log.

        Args:
            parent: The widget the wizard's own new window is shown over.
                    Leave both parent and area as None for a standalone
                    bridge that owns its hidden root.
            area: The existing container the wizard fills instead of a
                  window of its own. It cannot be given together with
                  parent.
            modal: Whether the wizard grabs its window (or area's window)
                   for the session; see the module docstring.
            log: Stream that receives low-level wizard diagnostics.
        Raises:
            ValueError: Both parent and area were given.
        """
        if parent is not None and area is not None:
            raise ValueError('Give at most one of parent and area.')
        self._root: Optional[tk.Tk] = None
        if parent is None and area is None:
            self._root = tk.Tk()
            self._root.withdraw()
            parent = self._root
        self._parent = parent
        self._area = area
        self._modal = modal
        self._log = log
        self._window: Optional[WizardWindow] = None

    def ask_text(self, question: str, re_ask_reason: Optional[str] = None,
                 nullable: bool = False, *, default: Optional[str] = None,
                 sensitive: bool = False) -> Optional[str]:
        """Ask for free text; see WizardUiBridge.ask_text."""
        check_text_args(default, sensitive, nullable)
        return self._window_obj().ask_text(question, re_ask_reason, nullable,
                                           default, sensitive)

    # pylint: disable-next=too-many-arguments
    def ask_int(self, question: str, re_ask_reason: Optional[str] = None, *,
                nullable: bool = False, min_value: Optional[int] = None,
                max_value: Optional[int] = None,
                default: Optional[int] = None) -> Optional[int]:
        """Ask for an integer within optional bounds; see ask_int."""
        check_nullable(nullable, default is not None)
        return self._window_obj().ask_int(question, re_ask_reason, nullable,
                                          min_value, max_value, default)

    def ask_path(self, question: str, re_ask_reason: Optional[str] = None, *,
                 options: Optional[PathAskOptions] = None) -> Optional[Path]:
        """Ask for a path with a native file or directory picker."""
        path_options = PathAskOptions() if options is None else options
        return self._window_obj().ask_path(question, path_options,
                                           re_ask_reason)

    def ask_yes_no(self, question: str, default: bool,
                   re_ask_reason: Optional[str] = None) -> bool:
        """Ask a yes/no question with dedicated yes and no buttons."""
        return self._window_obj().ask_yes_no(question, default, re_ask_reason)

    @overload
    def ask_choice(self, question: str, *, choices: Sequence[str],
                   default: Optional[str] = None,
                   re_ask_reason: Optional[str] = None,
                   nullable: Literal[False] = False) -> str: ...

    @overload
    def ask_choice(self, question: str, *, choices: Sequence[str],
                   default: Optional[str] = None,
                   re_ask_reason: Optional[str] = None,
                   nullable: bool) -> Optional[str]: ...

    # pylint: disable-next=too-many-arguments
    def ask_choice(self, question: str, *, choices: Sequence[str],
                   default: Optional[str] = None,
                   re_ask_reason: Optional[str] = None,
                   nullable: bool = False) -> Optional[str]:
        """Ask the user to pick one choice from a single-selection list.

        A nullable choice is offered with a leading '(none)' entry.
        """
        check_nullable(nullable, default is not None)
        return self._window_obj().ask_choice(question, choices, default,
                                             re_ask_reason, nullable)

    # pylint: disable-next=too-many-arguments
    def ask_multi(self, question: str, *, choices: Sequence[str],
                  default: Optional[Sequence[str]] = None, min_select: int = 0,
                  max_select: Optional[int] = None,
                  re_ask_reason: Optional[str] = None) -> list[str]:
        """Ask the user to pick several choices from a multi-selection list."""
        return self._window_obj().ask_multi(question, choices, default,
                                            min_select, max_select,
                                            re_ask_reason)

    # pylint: disable-next=too-many-arguments
    def ask_table(self, columns: Sequence[TableColumn],
                  cells: list[list[TableCell]], question: str, *,
                  re_ask_reason: Optional[str] = None,
                  partial_check: Optional[PartialCheck] = None,
                  min_rows: Optional[int] = None,
                  max_rows: Optional[int] = None) -> list[list[Optional[str]]]:
        """Ask the user to fill an editable table of the given rows.

        With both ``min_rows`` and ``max_rows`` given the table has a
        variable number of rows: add-row and remove-row buttons grow the
        table up to ``max_rows`` and shrink it down to ``min_rows``.
        Otherwise the rows given in ``cells`` are fixed and only filled.
        """
        return self._window_obj().ask_table(columns, cells, question,
                                            re_ask_reason, partial_check,
                                            min_rows, max_rows)

    def ask_form(self, long_question: str, ask_fields: AskFields, *,
                 re_ask_reason: Optional[str] = None,
                 partial_validator: Optional[PartialFormValidator] = None) \
            -> AnswerFields:
        """Ask a whole form on one screen; see WizardUiBridge.ask_form."""
        return self._window_obj().ask_form(long_question, ask_fields,
                                           re_ask_reason, partial_validator)

    def ask_matrix_form(self, request: MatrixRequest, *,
                        re_ask_reason: Optional[str] = None) -> AnswerCells:
        """Ask a whole matrix form on one screen; see ask_matrix_form.

        Each AskLabelCell is shown as plain text and every other cell as
        the input a form field of its type gets, with its help text and
        any format hint as a hover tooltip. When the minimum and maximum
        dimensions differ, buttons in the button row append or delete the
        last row or column within the bounds. The partial validator is
        called after each change of a cell, with its position, and after
        each change of the shape, with None, but not when the matrix is
        first shown. Its disabled cells are greyed out, its prefills are
        written into the inputs, and its message is shown below the
        matrix. OK first runs the partial validator, then needs every
        enabled cell to hold a valid answer, and finally needs the
        validator to accept the matrix.
        """
        return self._window_obj().ask_matrix_form(request, re_ask_reason)

    def supports_form_field(self, field: AskField) -> bool:
        """Report that the Tk form shows every current field type.

        This includes a nullable choice field, whose drop-down has a
        blank entry that empties it.
        """
        return handles_field(field)

    def show(self, message: str) -> None:
        """Show an informational message to the user."""
        self._window_obj().show(message)

    def error_file(self) -> TextIO:
        """Return the stream used for low-level wizard diagnostics."""
        return self._log if self._log is not None else NoTextIO()

    def close(self) -> None:
        """Close the wizard window, or clear its area, when one was built."""
        try:
            if self._window is not None:
                self._window.close()
                self._window = None
        finally:
            if self._root is not None:
                self._root.destroy()
                self._root = None

    def _window_obj(self) -> WizardWindow:
        """Return the wizard window, building it on first use."""
        if self._window is None:
            self._window = WizardWindow(self._parent, self._area, self._modal)
        return self._window
