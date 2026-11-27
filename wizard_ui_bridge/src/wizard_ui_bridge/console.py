#! /usr/local/bin/python3
"""Console text user interface bridge for a wizard.

This module provides the concrete console bridge used when the wizard
talks to a user through plain text streams. It recognises reserved
navigation tokens so a console user can step back, cancel the current
level or abandon the whole wizard, and the help token ':?', which shows
the help text of the question and then asks the same question again.

A question with a start value shows it as the answer an empty line
keeps, and also recognises the erase token ':e', which gives what an
empty answer gives without the start value: the default, None when
nullable, an empty string for text, and nothing selected for a
multi-choice. This is what a GUI gives when the user empties the input.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import getpass
from typing import Literal, Optional, Sequence, TextIO, overload
from wizard_ui_bridge.arg_types import PartialCheck, \
    WizardBack, WizardCancelLevel, WizardAbort, TableColumn, TableCell
from wizard_ui_bridge.bridge import WizardUiBridge
from wizard_ui_bridge.form_defs import AskField, \
    ALL_ASK_FIELD_TYPES
from wizard_ui_bridge.bridge_helpers import check_text_args, \
    text_answer, ask_yes_no, ask_one, ask_many, run_table, int_text, \
    question_with_default, NO_CHOICE, ERASE_TOKEN
from wizard_ui_bridge._table import _run_variable_table

_BACK = ':b'
_CANCEL = ':c'
_ABORT = ':q'
_HELP = ':?'
_NAV_HINT = '(:b=back  :c=cancel level  :q=abort  :?=help)'
_ERASE_HINT = ('(:e=erase  :b=back  :c=cancel level  :q=abort  '
               ':?=help)')
_NO_HELP = 'No help is available for this question.'
_NONE_LINE = f'0: {NO_CHOICE}'
_DEFAULT_MARK = ' (default)'
_START_MARK = ' (current)'


class WizardUiBridgeConsole(WizardUiBridge):
    """Bridge between the wizard and the console text user interface."""

    def __init__(self, stdout_file: TextIO, stdin_file: TextIO,
                 stderr_file: TextIO) -> None:
        """Initialize the bridge.

        Args:
            stdout_file: Stream to print messages to.
            stdin_file: Stream to read user answers from.
            stderr_file: Stream to print errors to.
        """
        self.stdout_file = stdout_file
        self.stdin_file = stdin_file
        self.stderr_file = stderr_file

    # pylint: disable-next=too-many-arguments
    def ask_text(self, question: str, re_ask_reason: Optional[str] = None,
                 nullable: bool = False, *, default: Optional[str] = None,
                 sensitive: bool = False, start_value: Optional[str] = None,
                 help_text: Optional[str] = None) -> Optional[str]:
        """Ask for free text on the console; see WizardUiBridge.ask_text.

        The question shows the start value, else the default, in brackets.
        """
        check_text_args(default, sensitive, nullable, start_value)
        shown = default if start_value is None else start_value
        text = self._prompt(question_with_default(question, shown),
                            re_ask_reason, [], help_text, sensitive=sensitive,
                            erasable=start_value is not None)
        return text_answer(text, nullable, default, start_value)

    def supports_form_field(self, field: AskField) -> bool:
        """Show every form field type; see WizardUiBridge.

        The inherited base ask_form() asks each field with the typed ask
        methods, so the console form handles the typed float, date, time,
        date-time and duration fields as well as the original kinds, and
        a nullable choice field through ask_choice(nullable=True).
        """
        return isinstance(field, ALL_ASK_FIELD_TYPES)

    def ask_yes_no(self, question: str, default: bool,
                   re_ask_reason: Optional[str] = None, *,
                   start_value: Optional[bool] = None,
                   help_text: Optional[str] = None) -> bool:
        """Ask a yes/no question on the console; see ask_yes_no.

        The start value, else the default, is marked in the menu.
        """
        start = default if start_value is None else start_value
        menu_lines = _menu_lines(('yes', 'no'), ('yes',) if start else ('no',),
                                 _mark(start_value))

        def reader(reason: Optional[str]) -> str | int:
            return _to_index(self._prompt(question, reason, menu_lines,
                                          help_text,
                                          erasable=start_value is not None))
        return ask_yes_no(reader, default, re_ask_reason, start_value)

    # pylint: disable-next=too-many-arguments
    def ask_table(self, columns: Sequence[TableColumn],
                  cells: list[list[TableCell]], question: str, *,
                  re_ask_reason: Optional[str] = None,
                  partial_check: Optional[PartialCheck] = None,
                  min_rows: Optional[int] = None,
                  max_rows: Optional[int] = None,
                  help_text: Optional[str] = None
                  ) -> list[list[Optional[str]]]:
        """Ask the user to fill a table on the console; see ask_table.

        With both min_rows and max_rows given the table has a variable
        number of rows, edited through a row-menu interface. Otherwise the
        fixed rows in cells are filled one editable cell at a time. A cell
        that partial_check rejects is asked again until it is accepted.
        """
        if min_rows is not None and max_rows is not None:
            return _run_variable_table(self._ask_raw, self.show, columns,
                                       cells, question, re_ask_reason,
                                       partial_check, min_rows, max_rows,
                                       help_text)
        return run_table(self._ask_raw, self.show, columns, cells, question,
                         re_ask_reason, partial_check, help_text)

    def _ask_raw(self, question: str, re_ask_reason: Optional[str] = None,
                 choices: Optional[Sequence[str]] = None, *,
                 help_text: Optional[str] = None) -> str | int:
        """Ask one question and read a navigation-checked raw answer.

        Returns the entered text, or a 0-based index into choices when
        choices are offered, which is the raw-answer shape the table
        helpers expect (see arg_types.AskReader).
        """
        text = self._prompt(question, re_ask_reason, _menu_lines(choices),
                            help_text)
        return text if choices is None else _to_index(text)

    # pylint: disable=too-many-arguments
    @overload
    def ask_choice(self, question: str, *, choices: Sequence[str],
                   default: Optional[str] = None,
                   re_ask_reason: Optional[str] = None,
                   nullable: Literal[False] = False,
                   start_value: Optional[str] = None,
                   help_text: Optional[str] = None) -> str: ...

    @overload
    def ask_choice(self, question: str, *, choices: Sequence[str],
                   default: Optional[str] = None,
                   re_ask_reason: Optional[str] = None, nullable: bool,
                   start_value: Optional[str] = None,
                   help_text: Optional[str] = None) -> Optional[str]: ...
    # pylint: enable=too-many-arguments

    # pylint: disable-next=too-many-arguments
    def ask_choice(self, question: str, *, choices: Sequence[str],
                   default: Optional[str] = None,
                   re_ask_reason: Optional[str] = None, nullable: bool = False,
                   start_value: Optional[str] = None,
                   help_text: Optional[str] = None) -> Optional[str]:
        """Ask one choice on the console; see WizardUiBridge.ask_choice.

        A nullable choice adds the menu line '0: (none)'. Answering 0, or
        giving an empty answer with no start value, then selects no
        choice. The start value, else the default, is marked in the menu.
        """
        start = default if start_value is None else start_value
        lines = _menu_lines(choices, None if start is None else (start,),
                            _mark(start_value))
        if nullable:
            lines.insert(0, _NONE_LINE)

        erasable = start_value is not None

        def reader(reason: Optional[str]) -> str | int:
            return _single_index(self._prompt(question, reason, lines,
                                              help_text, erasable=erasable),
                                 nullable, erasable)
        return ask_one(reader, choices, default, re_ask_reason,
                       nullable=nullable, start_value=start_value)

    # pylint: disable-next=too-many-arguments
    def ask_multi(self, question: str, *, choices: Sequence[str],
                  default: Optional[Sequence[str]] = None, min_select: int = 0,
                  max_select: Optional[int] = None,
                  re_ask_reason: Optional[str] = None,
                  start_value: Optional[Sequence[str]] = None,
                  help_text: Optional[str] = None) -> list[str]:
        """Ask several choices on the console; see WizardUiBridge.ask_multi.

        The start value, else the default, is marked in the menu.
        """
        start = default if start_value is None else start_value
        lines = _menu_lines(choices, start, _mark(start_value))

        def reader(reason: Optional[str]) -> str | int:
            return self._prompt(_multi_question(question), reason, lines,
                                help_text, erasable=start_value is not None)
        return ask_many(reader, choices, default, min_select, max_select,
                        re_ask_reason, one_based=True, start_value=start_value)

    # pylint: disable-next=too-many-arguments
    def _prompt(self, question: str, re_ask_reason: Optional[str],
                lines: Sequence[str], help_text: Optional[str], *,
                sensitive: bool = False, erasable: bool = False) -> str:
        """Ask one question until the answer is not a request for help.

        The help token shows the help text, or a note that there is none,
        and asks the same question again, with the same re-ask reason. A
        navigation token raises its navigation request. An erasable
        question, one with a start value, lists the erase token too.
        """
        hint = _ERASE_HINT if erasable else _NAV_HINT
        while True:
            self._emit_question(question, re_ask_reason, lines, hint)
            text = self._read_sensitive(question) if sensitive \
                else self._read_answer(question)
            if text.strip() != _HELP:
                return text
            self.show(help_text or _NO_HELP)

    def _emit_question(self, question: str, re_ask_reason: Optional[str],
                       lines: Sequence[str], hint: str) -> None:
        """Print one question, any re-ask reason, choices and the prompt."""
        if re_ask_reason is not None:
            print(re_ask_reason, file=self.stderr_file)
        print('', file=self.stdout_file)
        print(question, file=self.stdout_file)
        for line in lines:
            print(line, file=self.stdout_file)
        print(hint, file=self.stdout_file)
        print('> ', end='', file=self.stdout_file)

    def _read_answer(self, question: str) -> str:
        """Read one navigation-checked answer line from the input stream."""
        answer = self.stdin_file.readline()
        if answer == '':
            raise EOFError(f'No answer supplied for {question}.')
        text = answer.rstrip('\n')
        _raise_for_navigation(text)
        return text

    def _read_sensitive(self, question: str) -> str:
        """Read sensitive text, avoiding echo on a real terminal."""
        if not self.stdin_file.isatty():
            return self._read_answer(question)
        text = getpass.getpass('', stream=self.stdout_file)
        _raise_for_navigation(text)
        return text

    def error_file(self) -> TextIO:
        """Return the stream used for validation diagnostics."""
        return self.stderr_file

    def show(self, message: str) -> None:
        """Show a message to the user.

        This method prints the message to the console.
        Args:
            message: The message to show the user.
        """
        print(message, file=self.stdout_file)


def _raise_for_navigation(text: str) -> None:
    """Raise a navigation request when text is a reserved token."""
    token = text.strip().lower()
    if token == _BACK:
        raise WizardBack()
    if token == _CANCEL:
        raise WizardCancelLevel()
    if token == _ABORT:
        raise WizardAbort()


def _to_index(text: str) -> str | int:
    """Map a numeric menu answer to a 0-based index, else keep the text."""
    index = int_text(text)
    return text if index is None else index - 1


def _single_index(text: str, nullable: bool, erasable: bool) -> str | int:
    """Map a single-choice answer, reading 0 as no choice when nullable.

    No choice is the empty answer, or the erase token when the question
    has a start value, since an empty answer then keeps the start value.
    """
    answer = _to_index(text)
    if nullable and answer == -1:
        return ERASE_TOKEN if erasable else ''
    return answer


def _menu_lines(choices: Optional[Sequence[str]],
                marked: Optional[Sequence[str]] = None,
                mark: str = _DEFAULT_MARK) -> list[str]:
    """Return the numbered menu lines, adding mark to any choice in marked."""
    if choices is None:
        return []
    flagged = set() if marked is None else set(marked)
    lines: list[str] = []
    for index, choice in enumerate(choices, start=1):
        suffix = mark if choice in flagged else ''
        lines.append(f'{index}: {choice}{suffix}')
    return lines


def _mark(start_value: object) -> str:
    """Return the menu mark of the start value, else of the default."""
    return _DEFAULT_MARK if start_value is None else _START_MARK


def _multi_question(question: str) -> str:
    """Return the multi-choice question with an entry hint appended."""
    return f'{question}\nEnter comma-separated numbers or names.'
