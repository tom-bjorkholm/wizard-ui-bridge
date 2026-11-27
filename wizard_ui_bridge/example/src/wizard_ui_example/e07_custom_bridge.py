#! /usr/bin/env python3
"""Implement a WizardUiBridge of your own for an unusual device.

This is the advanced capstone of the wizard-ui-bridge examples. The earlier
examples *used* a bridge that this package already provides; this one *is* a
bridge, written from scratch, so you can see exactly what it takes to teach
the wizard a new user interface.

The device: an uppercase-only teleprinter
-----------------------------------------
Imagine driving a classic uppercase-only teleprinter, such as a Teletype
Model 33. It can print capital letters A-Z, the digits 0-9 and a handful of
punctuation marks (``. , : - ( ) [ ] ?``) and nothing else: no lowercase, no
Unicode, no box drawing. Sending any other glyph does not merely look wrong,
it jams the machine.

The console bridge writes whatever text it is given straight to the stream,
so it cannot safely drive this device: the very first lowercase letter or
slash would jam it. So we need a bridge whose one distinctive job is to
*fold* every line it prints into the device's glyph set. That single
responsibility is the whole reason this bridge exists, and it is pure
standard library, so the example stays small.

Correctness first: the base class does most of the work
-------------------------------------------------------
A WizardUiBridge is designed so a new bridge is *correct from day one and
improved incrementally*. Only a handful of methods have no default and must
be implemented: the mandatory ask methods ``ask_text``, ``ask_yes_no``,
``ask_choice``, ``ask_multi`` and ``ask_table``, plus ``show``. Everything
else has a permanent base implementation this bridge simply inherits:

- ``ask_path`` asks for text through ``ask_text`` and validates the path,
- ``ask_int`` asks for text and re-asks until the value is a number in range,
- ``ask_form`` asks the form's fields one at a time with the typed ask
  methods above.

So the moment the mandatory methods work, this bridge can already run any of
the earlier wizards unchanged, path questions and whole forms included.

Help on request
---------------
Every ask method takes a keyword-only ``help_text``. The wizard, or the base
``ask_form`` for a form field, passes the help text of the question there,
and a bridge decides how to offer it. A text bridge like this one offers it
on request: the answer ``:?`` prints the help text and asks the same question
again. A graphical bridge would rather show it as a tooltip. A bridge written
before ``help_text`` existed still works, but the base class then leaves the
help text out and issues a DeprecationWarning, so do accept the parameter. This
example proves it by importing the export-settings wizard from
``e02_question_kinds`` and running that unchanged code through the new
bridge. A bridge works with *any* wizard; a wizard runs on *any* bridge.

One correctness gap is deliberately left open, not hidden: a table question
with both min_rows and max_rows asks for a *variable* number of rows, which
the user can only supply if the bridge lets them add and remove rows. That is
correctness, not polish -- a wizard that expects the user to extend a table
(a translation table, say) cannot receive those rows otherwise. Implementing
the add/remove interface is left out here only for brevity, so ask_table()
raises NotImplementedError for a variable-row request rather than silently
returning just the starting rows; WizardUiBridgeConsole,
WizardUiBridgeTextual and the WizardUiBridgeTk of the companion package
wizard-tk-bridge show three ways to implement it.

User experience second: the "override to improve" move
------------------------------------------------------
The mandatory methods above are the *floor for correctness, not the target*.
A production bridge should override every method whose user experience its
environment can improve. To show the move concretely, this bridge overrides
exactly one convenience method, ``ask_int``: the base ``ask_int`` asks bare
and explains the allowed range only *after* a rejected value, which reads
badly on a teleprinter where that reason scrolls away. The override states
the range up front and then delegates the actual re-ask loop to
``super().ask_int`` -- better UX, no logic rewritten.

The UX ladder: what a real bridge should climb next
---------------------------------------------------
This bridge deliberately stops at the floor plus one rung, so the code stays
readable. A real bridge should keep climbing. Each rung below names the
capability it exploits and a finished bridge that already shows how. The
console and Textual bridges in this package are two reference rungs, and
the WizardUiBridgeTk of the companion package wizard-tk-bridge is a
graphical bridge that has climbed all six:

1. Whole-screen ``ask_form`` -- show every field at once instead of one at a
   time. See ``WizardUiBridgeTextual.ask_form``.
2. A native ``ask_path`` picker -- a file/directory dialog instead of typed
   text. The text bridges validate typed text; a GUI toolkit supplies a
   real dialog, as the Tk bridge does.
3. A calendar for date fields -- see the date widgets in the Textual bridge,
   and the month calendar of the Tk bridge.
4. Richer typed-field widgets (spin boxes, sliders) for the float, time and
   duration fields.
5. ``help_text`` as a tooltip rather than an extra printed line, as in the
   Textual and Tk bridges.
6. Inline re-ask -- show a rejected value's reason beside the field instead
   of scrolling it into the transcript.

The helper modules ``wizard_ui_bridge.bridge_helpers`` and
``wizard_ui_bridge.form_helpers`` exist to make climbing this ladder cheaper:
they interpret raw answers, run the table loop and validate form prefills
exactly as the built-in bridges do. This example already uses the
``bridge_helpers`` functions so the mandatory methods stay a few lines each.

Running it
----------
``--ui`` selects the bridge, and the very same wizard runs on all three, so
you can watch the folding appear only on the custom (teleprinter) bridge::

    python -m wizard_ui_example.e07_custom_bridge
    python -m wizard_ui_example.e07_custom_bridge --ui console
    python -m wizard_ui_example.e07_custom_bridge --ui textual
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import argparse
import sys
from typing import Literal, Optional, Sequence, TextIO, overload

from wizard_ui_example.e02_question_kinds import ask_export_settings, summarize
from wizard_ui_bridge import make_text_ui_bridge, UiBridgeType, \
    WizardUiBridge, WizardNavigation, WizardBack, WizardCancelLevel, \
    WizardAbort, TableColumn, TableCell, PartialCheck
from wizard_ui_bridge.bridge_helpers import check_text_args, text_answer, \
    question_with_default, ask_yes_no, ask_one, ask_many, run_table, int_text

# The glyphs the teleprinter can print. Every other character, including any
# lowercase letter or slash, would jam the device, so the bridge folds all
# output into this set before printing it.
_ALLOWED = frozenset('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,:-()[]?\n')
_REPLACEMENT = '?'
_NAV_HINT = '(:b back  :c cancel  :q abort  :? help)'
# One reserved navigation token per WizardNavigation subclass. Answering with
# a token asks to move within the wizard instead of answering the question.
_NAV_TOKENS = {':b': WizardBack, ':c': WizardCancelLevel, ':q': WizardAbort}
# The help token is not a navigation move: the bridge answers it itself, by
# printing the help text and asking the same question again, so the wizard
# never sees it.
_HELP_TOKEN = ':?'
_NO_HELP = 'No help is available for this question.'


def _fold(text: str) -> str:
    """Return text reduced to the glyphs the teleprinter can print.

    Letters are folded to uppercase and any character outside the device's
    glyph set becomes a single replacement mark, so a lowercase name or a
    path separator prints as a safe stand-in instead of jamming the device.
    """
    return ''.join(ch if ch in _ALLOWED else _REPLACEMENT
                   for ch in text.upper())


def _range_hint(min_value: Optional[int], max_value: Optional[int]) -> str:
    """Return a short phrase naming the accepted integer range, or ''."""
    if min_value is not None and max_value is not None:
        return f'{min_value} to {max_value}'
    if min_value is not None:
        return f'at least {min_value}'
    if max_value is not None:
        return f'at most {max_value}'
    return ''


def _int_prompt(question: str, min_value: Optional[int],
                max_value: Optional[int]) -> str:
    """Return the integer question with the accepted range appended."""
    hint = _range_hint(min_value, max_value)
    return question if not hint else f'{question} ({hint})'


class TeleprinterBridge(WizardUiBridge):
    """A minimal WizardUiBridge for an uppercase-only teleprinter.

    The class implements only the mandatory ask methods and show(), routes
    side notes through error_file(), and overrides ask_int() to show its
    range up front. Every other method -- ask_path(), ask_form() and the
    rest -- is inherited from WizardUiBridge, so this bridge is a complete,
    correct bridge despite its small size. See the module docstring for the
    device it targets and the UX ladder a real bridge should climb.
    """

    def __init__(self, stdout_file: TextIO, stdin_file: TextIO,
                 stderr_file: TextIO) -> None:
        """Store the teleprinter output, input and diagnostic streams."""
        self.stdout_file = stdout_file
        self.stdin_file = stdin_file
        self.stderr_file = stderr_file

    def show(self, message: str) -> None:
        """Print a message to the teleprinter, folded into its glyph set."""
        self._emit(message)

    def error_file(self) -> TextIO:
        """Return the diagnostic stream, kept apart from the device."""
        return self.stderr_file

    def _emit(self, line: str) -> None:
        """Fold one line and print it to the teleprinter."""
        print(_fold(line), file=self.stdout_file)

    def _read(self) -> str:
        """Read one answer line, raising the requested navigation move.

        The typed answer is returned unfolded: folding protects the device
        the bridge prints to, not the text the user typed back to the wizard.
        """
        line = self.stdin_file.readline()
        if line == '':
            raise EOFError('No answer supplied.')
        text = line.rstrip('\n')
        navigation = _NAV_TOKENS.get(text.strip().lower())
        if navigation is not None:
            raise navigation()
        return text

    def _ask(self, question: str, re_ask_reason: Optional[str] = None,
             choices: Optional[Sequence[str]] = None, *,
             help_text: Optional[str] = None) -> str | int:
        """Print one question and read a navigation-checked raw answer.

        Choices are printed as a numbered menu, because digits are glyphs the
        teleprinter can show and type back cleanly. A numeric answer is
        returned as its 0-based menu index and any other answer as its text,
        which is the raw-answer shape the bridge_helpers functions expect.
        This method is also the AskReader that run_table() calls, which is
        why it takes help_text as a keyword-only parameter.
        """
        while True:
            self._print_question(question, re_ask_reason, choices)
            text = self._read()
            if text.strip() != _HELP_TOKEN:
                break
            # A request for help is not an answer: print the help text and
            # loop to ask the very same question again.
            self._emit(help_text or _NO_HELP)
        if choices is None:
            return text
        number = int_text(text)
        return text if number is None else number

    def _print_question(self, question: str, re_ask_reason: Optional[str],
                        choices: Optional[Sequence[str]]) -> None:
        """Print the re-ask reason, the question, its menu and the hint."""
        if re_ask_reason is not None:
            self._emit(re_ask_reason)
        self._emit(question)
        for index, choice in enumerate(choices or ()):
            self._emit(f'{index}) {choice}')
        self._emit(_NAV_HINT)

    # pylint: disable-next=too-many-arguments
    def ask_text(self, question: str, re_ask_reason: Optional[str] = None,
                 nullable: bool = False, *, default: Optional[str] = None,
                 sensitive: bool = False,
                 help_text: Optional[str] = None) -> Optional[str]:
        """Ask for free text; see WizardUiBridge.ask_text.

        The teleprinter cannot hide what it prints, so a sensitive answer is
        read like any other. A real bridge would suppress the echo instead;
        that is one more rung on the UX ladder.
        """
        # check_text_args() raises ValueError for a default combined with
        # sensitive or with nullable, the same programming errors every
        # bundled bridge rejects.
        check_text_args(default, sensitive, nullable)
        answer = self._ask(question_with_default(question, default),
                           re_ask_reason, help_text=help_text)
        assert isinstance(answer, str)  # no choices, so the answer is text
        return text_answer(answer, nullable, default)

    def ask_yes_no(self, question: str, default: bool,
                   re_ask_reason: Optional[str] = None, *,
                   help_text: Optional[str] = None) -> bool:
        """Ask a yes/no question; see WizardUiBridge.ask_yes_no."""
        def reader(reason: Optional[str]) -> str | int:
            return self._ask(question, reason, ('yes', 'no'),
                             help_text=help_text)
        return ask_yes_no(reader, default, re_ask_reason)

    # The base class declares ask_choice() with two overloads, so a caller
    # that leaves nullable out gets a plain str back while a caller passing
    # nullable gets Optional[str]. An override must repeat both overloads,
    # otherwise mypy reports it as incompatible with the base class.
    # pylint: disable=too-many-arguments
    @overload
    def ask_choice(self, question: str, *, choices: Sequence[str],
                   default: Optional[str] = None,
                   re_ask_reason: Optional[str] = None,
                   nullable: Literal[False] = False,
                   help_text: Optional[str] = None) -> str: ...

    @overload
    def ask_choice(self, question: str, *, choices: Sequence[str],
                   default: Optional[str] = None,
                   re_ask_reason: Optional[str] = None, nullable: bool,
                   help_text: Optional[str] = None) -> Optional[str]: ...
    # pylint: enable=too-many-arguments

    # pylint: disable-next=too-many-arguments
    def ask_choice(self, question: str, *, choices: Sequence[str],
                   default: Optional[str] = None,
                   re_ask_reason: Optional[str] = None, nullable: bool = False,
                   help_text: Optional[str] = None) -> Optional[str]:
        """Ask for one choice; see WizardUiBridge.ask_choice.

        A nullable choice may be left empty, which reports no choice (None).
        The teleprinter says so in the question. A richer bridge would show
        an explicit '(none)' entry instead; that is one more rung on the UX
        ladder (see bridge_helpers.offered_choices).
        """
        prompt = f'{question} (empty answer for none)' if nullable \
            else question

        def reader(reason: Optional[str]) -> str | int:
            return self._ask(prompt, reason, choices, help_text=help_text)
        # ask_one() re-asks until the answer is valid. With nullable=True it
        # returns None for an empty answer, and it raises ValueError when
        # nullable is combined with a default.
        return ask_one(reader, choices, default, re_ask_reason,
                       nullable=nullable)

    # pylint: disable-next=too-many-arguments
    def ask_multi(self, question: str, *, choices: Sequence[str],
                  default: Optional[Sequence[str]] = None, min_select: int = 0,
                  max_select: Optional[int] = None,
                  re_ask_reason: Optional[str] = None,
                  help_text: Optional[str] = None) -> list[str]:
        """Ask for several choices; see WizardUiBridge.ask_multi."""
        def reader(reason: Optional[str]) -> str | int:
            return self._ask(f'{question} (numbers separated by commas)',
                             reason, choices, help_text=help_text)
        return ask_many(reader, choices, default, min_select, max_select,
                        re_ask_reason, one_based=False)

    # pylint: disable-next=too-many-arguments
    def ask_table(self, columns: Sequence[TableColumn],
                  cells: list[list[TableCell]], question: str, *,
                  re_ask_reason: Optional[str] = None,
                  partial_check: Optional[PartialCheck] = None,
                  min_rows: Optional[int] = None,
                  max_rows: Optional[int] = None,
                  help_text: Optional[str] = None
                  ) -> list[list[Optional[str]]]:
        """Fill a fixed-row table; see WizardUiBridge.ask_table.

        run_table asks each editable cell one at a time through the same
        reader as the other questions, passing it the help text of the
        table.

        Both min_rows and max_rows being given means the wizard wants a
        *variable* number of rows, so the user must be able to add and
        remove rows. That is a matter of correctness, not polish: a wizard
        that expects the user to extend a table (a translation table, say)
        cannot receive those rows unless the bridge offers the add/remove
        interface. Implementing it is left out here only for brevity, so
        this bridge refuses a variable-row request with NotImplementedError
        rather than silently return just the starting rows. See the
        variable-row table in WizardUiBridgeConsole and WizardUiBridgeTextual
        for two worked implementations.
        """
        if min_rows is not None and max_rows is not None:
            raise NotImplementedError(
                'TeleprinterBridge supports only fixed-row tables; '
                'add/remove-row editing is left out for brevity.')
        return run_table(self._ask, self.show, columns, cells, question,
                         re_ask_reason, partial_check, help_text)

    # pylint: disable-next=too-many-arguments
    def ask_int(self, question: str, re_ask_reason: Optional[str] = None, *,
                nullable: bool = False, min_value: Optional[int] = None,
                max_value: Optional[int] = None, default: Optional[int] = None,
                help_text: Optional[str] = None) -> Optional[int]:
        """Ask for an integer, naming the accepted range up front.

        This is the one convenience method the bridge overrides to improve on
        the inherited implementation. The base ask_int() explains the range
        only after a rejected value; on a teleprinter that reason scrolls
        away, so this override puts the range in the question and then
        delegates the re-ask loop to super().ask_int() unchanged.
        """
        return super().ask_int(_int_prompt(question, min_value, max_value),
                               re_ask_reason, nullable=nullable,
                               min_value=min_value, max_value=max_value,
                               default=default, help_text=help_text)


def _present(bridge: WizardUiBridge, summary: str) -> None:
    """Show the summary and keep it on screen until acknowledged.

    show() prints at once on the teleprinter and console, but only buffers
    the message for the next screen on the Textual bridge, so one trailing
    question keeps the summary visible on every bridge, exactly as e01 does.
    """
    bridge.show(summary)
    try:
        bridge.ask_text('Press Enter to finish.', nullable=True)
    except WizardNavigation:
        pass  # the user closed the wizard; the summary was already shown


def _make_bridge(ui: str, out_file: TextIO, in_file: TextIO,
                 err_file: TextIO) -> WizardUiBridge:
    """Build the teleprinter bridge, or a built-in bridge for contrast."""
    if ui == 'custom':
        return TeleprinterBridge(out_file, in_file, err_file)
    forced = UiBridgeType.CONSOLE if ui == 'console' else UiBridgeType.TEXTUAL
    return make_text_ui_bridge(out_file, in_file, err_file, forced)


# The stream defaults, the --ui switch and main() below are the same plumbing
# in every example, so each example stays a complete program a reader can run
# and study on its own. Repeating this ceremony is a deliberate teaching
# choice, so duplicate-code is turned off from here to the end of the file.
# pylint: disable=duplicate-code
def collect_and_summarize(stdin_file: Optional[TextIO] = None,
                          stdout_file: Optional[TextIO] = None,
                          stderr_file: Optional[TextIO] = None,
                          ui: str = 'custom') -> Optional[str]:
    """Run the e02 export wizard through the chosen bridge and summarize.

    Args:
        stdin_file: Optional input stream for tests or scripted use.
        stdout_file: Optional output stream for tests or scripted use.
        stderr_file: Optional diagnostic stream for side notes.
        ui: Which bridge to build: 'custom' for the teleprinter bridge, or
            'console'/'textual' for a built-in bridge, to show that the same
            wizard runs on all three.

    Returns:
        The unfolded summary text, or None when the user cancelled. On the
        teleprinter the same summary is shown folded into the device's
        glyphs, which is the visible payoff of the custom bridge.
    """
    in_file = sys.stdin if stdin_file is None else stdin_file
    out_file = sys.stdout if stdout_file is None else stdout_file
    err_file = sys.stderr if stderr_file is None else stderr_file
    bridge = _make_bridge(ui, out_file, in_file, err_file)
    settings = ask_export_settings(bridge)
    if settings is None:
        bridge.show('Export configuration cancelled.')
        return None
    summary = summarize(settings)
    _present(bridge, summary)
    return summary


def build_parser() -> argparse.ArgumentParser:
    """Return the argument parser for the custom-bridge example."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ui', choices=('custom', 'console', 'textual'),
                        default='custom', help='UI bridge to use.')
    return parser


def main(args: Optional[list[str]] = None) -> int:
    """Parse arguments, run the wizard through the bridge and summarize."""
    parsed = build_parser().parse_args(args)
    collect_and_summarize(ui=parsed.ui)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
