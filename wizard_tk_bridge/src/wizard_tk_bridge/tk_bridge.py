#! /usr/local/bin/python3
"""Graphical Tkinter bridge that drives a synchronous wizard.

:class:`WizardUiBridgeTk` is a concrete :class:`WizardUiBridge` that
overrides every typed ask method with a real Tkinter control, including
the GUI-recommended ones: ask_path() opens a native file or directory
picker, and ask_form() shows a whole form on one screen so the user
answers related fields together in any order. All questions of one
wizard session are answered in a single reused
:class:`~wizard_tk_bridge.wizard_window.WizardWindow`, so the session
does not jump around the display.

The bridge supports three ways an application can show the wizard:

- In a new window of its own: give ``parent``, the Tk widget the new
  window is shown over. This suits both an application with other
  windows and a standalone CLI program, which passes a hidden root it
  created for the purpose (``tk.Tk()`` withdrawn right after creation).
- Embedded in an area the application already built: give ``area``, the
  frame or other container the wizard should fill instead of a window of
  its own.
- Either way, ``modal`` decides whether the wizard grabs its window (or
  the window containing ``area``) for the duration of the session, so
  the rest of that window is unusable meanwhile. The application is best
  placed to decide this, since only it knows whether its other content
  should stay usable while the wizard runs.

Exactly one of ``parent`` and ``area`` must be given.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional, Sequence, TextIO
from pathlib import Path
import tkinter as tk
from wizard_ui_bridge import AnswerFields, AskField, AskFields, PartialCheck, \
    PartialFormValidator, PathAskOptions, TableCell, TableColumn, \
    WizardUiBridge
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
                    Exactly one of parent or area must be given.
            area: The existing container the wizard fills instead of a
                  window of its own. Exactly one of parent or area must
                  be given.
            modal: Whether the wizard grabs its window (or area's window)
                   for the session; see the module docstring.
            log: Stream that receives low-level wizard diagnostics.
        Raises:
            ValueError: Neither or both of parent and area were given.
        """
        if (parent is None) == (area is None):
            raise ValueError('Give exactly one of parent or area.')
        self._parent = parent
        self._area = area
        self._modal = modal
        self._log = log
        self._window: Optional[WizardWindow] = None

    def ask_text(self, question: str, re_ask_reason: Optional[str] = None,
                 nullable: bool = False, *, default: Optional[str] = None,
                 sensitive: bool = False) -> Optional[str]:
        """Ask for free text; see WizardUiBridge.ask_text."""
        if sensitive and default is not None:
            raise ValueError('default is not allowed for sensitive input')
        return self._window_obj().ask_text(question, re_ask_reason, nullable,
                                           default, sensitive)

    # pylint: disable-next=too-many-arguments
    def ask_int(self, question: str, re_ask_reason: Optional[str] = None, *,
                nullable: bool = False, min_value: Optional[int] = None,
                max_value: Optional[int] = None,
                default: Optional[int] = None) -> Optional[int]:
        """Ask for an integer within optional bounds; see ask_int."""
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

    def ask_choice(self, question: str, *, choices: Sequence[str],
                   default: Optional[str] = None,
                   re_ask_reason: Optional[str] = None) -> str:
        """Ask the user to pick one choice from a single-selection list."""
        return self._window_obj().ask_choice(question, choices, default,
                                             re_ask_reason)

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

    def supports_form_field(self, field: AskField) -> bool:
        """Report that the Tk form shows every current field type."""
        return handles_field(field)

    def show(self, message: str) -> None:
        """Show an informational message to the user."""
        self._window_obj().show(message)

    def error_file(self) -> TextIO:
        """Return the stream used for low-level wizard diagnostics."""
        return self._log if self._log is not None else NoTextIO()

    def close(self) -> None:
        """Close the wizard window, or clear its area, when one was built."""
        if self._window is not None:
            self._window.close()
            self._window = None

    def _window_obj(self) -> WizardWindow:
        """Return the wizard window, building it on first use."""
        if self._window is None:
            self._window = WizardWindow(self._parent, self._area, self._modal)
        return self._window
