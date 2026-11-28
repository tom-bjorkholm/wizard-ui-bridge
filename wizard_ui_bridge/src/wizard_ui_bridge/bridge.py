#! /usr/local/bin/python3
"""User interface bridge for a wizard asking a user questions.

This module defines the abstract bridge between the wizard and a user
interface, the navigation requests a bridge raises to steer wizard flow,
and the column and cell descriptors used by table questions. Concrete
console and graphical bridges derive from WizardUiBridge.

An application that drives the wizard is responsible for implementing
the typed ask methods of its bridge, together with show(). A concrete
bridge implements ask_text(), ask_choice(), ask_multi() and ask_yes_no();
ask_path() has a permanent base implementation that a bridge may override
for a native file or directory picker.

A GUI, textual, curses or web application should override ask_form() and
ask_matrix_form() to show the whole form or matrix at once, so the user sees
every question together and answers them in any order. The base
implementations are permanent and suitable for a console text interface.
The permanent base ask_table() asks the table through ask_matrix_form(),
so a bridge gets a table question shown the way it shows a matrix form.

A GUI, textual, curses or web application should also override ask_path() to
provide a native file or directory picker. The base implementation asks for
text and validates the path.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import sys
from pathlib import Path
from typing import Literal, Optional, Sequence, TextIO, Union, overload
from wizard_ui_bridge.arg_types import PartialCheck, \
    PathAskOptions, TableColumn, TableCell, WizardBack, check_nullable
from wizard_ui_bridge.bridge_helpers import int_text, \
    out_of_range, range_error, path_answer, INT_ERROR
from wizard_ui_bridge.form_helpers import answer_of, initial_answer, \
    valid_prefills, prefilled_field, nullable_choice, live_validator_of
from wizard_ui_bridge._ask_cell import ask_cell_value
from wizard_ui_bridge._help import help_kwargs
from wizard_ui_bridge._start import start_args
from wizard_ui_bridge._fake import ask_form_faking
from wizard_ui_bridge._matrix_console import ConsoleMatrix
from wizard_ui_bridge._table_matrix import TableMatrix
from wizard_ui_bridge.form_defs import AskField, AskFields, \
    AnswerField, AnswerFields, LiveFormValidator, PartialFormValidator, \
    AskTextField, AskIntField, AskPathField, AskYesNoField, AskChoiceField, \
    AskMultiChoiceField
from wizard_ui_bridge.matrix_cell_defs import PrefillValueType, \
    check_bounds
from wizard_ui_bridge.matrix_defs import MatrixRequest, AnswerCells


class WizardUiBridge:
    """Bridge between the wizard and the user interface.

    This is an abstract base class for a bridge between the wizard and
    the user interface. Provide concrete classes of this bridge to allow
    the wizard to use a console text user interface or a graphical user
    interface.

    A concrete bridge implements ask_text(), ask_choice(), ask_multi(),
    ask_yes_no() and show(). It may override ask_path() for a native file
    or directory picker; otherwise the base implementation asks for text
    and validates the path. It may override ask_form() and
    ask_matrix_form() to show the whole form or matrix at once, so the
    user sees every question together and answers them in any order.
    Overriding ask_form(), ask_matrix_form() and ask_path() is strongly
    recommended for a GUI, textual, curses or web application. The base
    ask_table() asks through ask_matrix_form(), so a bridge only overrides
    ask_table() for a table widget of its own.

    Any ask method may raise a WizardNavigation subclass to request back,
    cancel-level or abort instead of returning an answer.

    Every typed ask method and ask_table() take a keyword-only help_text,
    which a console bridge shows when the user asks for help. A GUI
    bridge that overrides ask_form() and ask_matrix_form() may ignore it.
    The base class calls an ask method of a derived bridge that lacks the
    help_text parameter without it, and issues a DeprecationWarning, so
    an older bridge keeps working until it is updated.

    The typed ask methods also take a keyword-only start_value, the value
    the question starts with, separate from the default that an empty
    answer gives (see Start value in wizard_ui_bridge.matrix_cell_defs).
    A path question takes it in its PathAskOptions. The base class calls
    a typed ask method of a derived bridge that lacks start_value with
    the start value as the default instead, not nullable, and issues a
    DeprecationWarning; the user then cannot empty the answer.

    ask_form() and ask_form_w_fake() take the validator of the form as
    live_validator. The older partial_validator is deprecated and will
    be removed in version 2.0. A bridge that overrides ask_form() should
    accept both, and turn them into one validator with
    wizard_ui_bridge.form_helpers.live_validator_of(). ask_form_w_fake()
    passes a live validator as partial_validator to an ask_form() override
    that lacks live_validator, and issues a DeprecationWarning.
    """

    # pylint: disable-next=too-many-arguments
    def ask_text(self, question: str, re_ask_reason: Optional[str] = None,
                 nullable: bool = False, *, default: Optional[str] = None,
                 sensitive: bool = False, start_value: Optional[str] = None,
                 help_text: Optional[str] = None) -> Optional[str]:
        """Ask a free-text question and return the entered text.

        The application is responsible for implementing this method with
        a real text-entry control. The base class has no implementation.

        Args:
            question: The question to ask the user.
            re_ask_reason: The reason for re-asking the question, for
                           instance that the user's answer was invalid.
            nullable: When True an empty answer is reported as None.
                      When False an empty answer with no default is the
                      empty string.
            default: The value returned by an empty answer, or None for
                     no default. Not allowed together with nullable.
            sensitive: True when the bridge must avoid echoing the
                       entered text, such as for passwords. Neither a
                       default nor a start_value is allowed for a
                       sensitive question.
            start_value: The text the question starts with, or None to
                         start with the default. The user may keep it,
                         change it or empty it, and an emptied answer
                         gives what an empty answer gives, so it may be
                         combined with nullable. A console bridge shows
                         it as the answer Enter keeps and offers ':e' to
                         empty it.
            help_text: A help text for the question, or None for no help.
                       A console bridge shows it when the user asks for
                       help. A GUI bridge that overrides ask_form() and
                       ask_matrix_form() may ignore it.

        Returns:
            The entered or kept text, default for an empty answer with a
            default, or None for an empty answer when nullable.
        Raises:
            ValueError: default is given together with sensitive or
                        nullable, or start_value together with sensitive.
            NotImplementedError: The bridge does not implement ask_text().
            WizardBack: The user asked to return to the previous question.
            WizardCancelLevel: The user cancelled the current level.
            WizardAbort: The user abandoned the whole wizard.
        """
        raise NotImplementedError('ask_text() not implemented')

    # pylint: disable-next=too-many-arguments
    def ask_int(self, question: str, re_ask_reason: Optional[str] = None, *,
                nullable: bool = False, min_value: Optional[int] = None,
                max_value: Optional[int] = None, default: Optional[int] = None,
                start_value: Optional[int] = None,
                help_text: Optional[str] = None) -> Optional[int]:
        """Ask for an integer, optionally within inclusive bounds.

        The base implementation uses ask_text() and re-asks until the
        answer is empty when allowed or parses as an integer in range. A
        derived bridge may override it with a direct numeric control.

        Args:
            question: The question to ask the user.
            re_ask_reason: The reason for re-asking the question, for
                           instance that the user's answer was invalid.
            nullable: When True an empty answer is reported as None.
                      When False an empty answer with no default will be
                      re-asked until a valid answer is entered.
            min_value: The minimum allowed value, or None for no lower bound.
                       The min value is inclusive.
            max_value: The maximum allowed value, or None for no upper bound.
                       The max value is inclusive.
            default: The value returned by an empty answer, or None for
                     no default. Not allowed together with nullable.
            start_value: The value the question starts with, or None to
                         start with the default, as for ask_text(). It
                         must lie within the bounds.
            help_text: A help text for the question, or None for no help.
                       A console bridge shows it when the user asks for
                       help. A GUI bridge that overrides ask_form() and
                       ask_matrix_form() may ignore it.

        Returns:
            The entered or kept integer, default for an empty answer with
            a default, or None for an empty answer when nullable.
        Raises:
            ValueError: min_value exceeds max_value, default or
                        start_value is outside the bounds, or default is
                        given together with nullable.
            WizardBack: The user asked to return to the previous question.
            WizardCancelLevel: The user cancelled the current level.
            WizardAbort: The user abandoned the whole wizard.
        """
        check_bounds(min_value, max_value, default, start_value)
        check_nullable(nullable, default is not None)
        reason = re_ask_reason
        args = start_args(self.ask_text, _text_of(start_value),
                          _text_of(default), nullable)
        extra = help_kwargs(self.ask_text, help_text)
        while True:
            text = self.ask_text(question, reason, args.nullable,
                                 default=args.default, **args.kwargs, **extra)
            if text is None:
                return None
            value = int_text(text)
            if value is None:
                reason = INT_ERROR
            elif out_of_range(value, min_value, max_value):
                reason = range_error(min_value, max_value)
            else:
                return value

    def ask_path(self, question: str, re_ask_reason: Optional[str] = None, *,
                 options: Optional[PathAskOptions] = None,
                 help_text: Optional[str] = None) -> Optional[Path]:
        """Ask a question for a path and return the accepted path.

        A derived bridge may override this method to provide a native file
        or directory picker. The base implementation is permanent and
        asks for text through ask_text(), then validates the answer.

        Args:
            question: The question to ask the user.
            re_ask_reason: The reason for re-asking the question.
            options: Path options, including the default and start_value.
                     None only rejects existing directories.
            help_text: A help text for the question, or None for no help.
                       A console bridge shows it when the user asks for
                       help. A GUI bridge that overrides ask_form() and
                       ask_matrix_form() may ignore it.

        Returns:
            The accepted path, a default path, or None when nullable.
            PathAskOptions does not allow both a default and nullable.
        Raises:
            WizardBack: The user asked to return to the previous question.
            WizardCancelLevel: The user cancelled the current level.
            WizardAbort: The user abandoned the whole wizard.
        """
        path_options = PathAskOptions() if options is None else options
        reason = re_ask_reason
        args = start_args(self.ask_text, _text_of(path_options.start_value),
                          _text_of(path_options.default),
                          path_options.nullable)
        extra = help_kwargs(self.ask_text, help_text)
        while True:
            text = self.ask_text(question, reason, args.nullable,
                                 default=args.default, **args.kwargs, **extra)
            done, path, reason = path_answer(text, path_options)
            if done:
                return path

    def ask_yes_no(self, question: str, default: bool,
                   re_ask_reason: Optional[str] = None, *,
                   start_value: Optional[bool] = None,
                   help_text: Optional[str] = None) -> bool:
        """Ask a yes/no question and return the chosen boolean.

        Yes/no questions are asked through this method, and the
        application is responsible for implementing it with a real yes/no
        interface, such as a pair of yes and no buttons in a graphical
        bridge or a y/n prompt in a console bridge. The base class has no
        implementation.

        Args:
            question: The yes/no question to ask.
            default: The value to use when the user makes no explicit
                     choice.
            re_ask_reason: The reason for re-asking the question, for
                           instance that the user's answer was invalid.
            start_value: The value the question starts with, or None to
                         start with the default. A console bridge shows
                         it as the answer Enter keeps and offers ':e' for
                         the default.
            help_text: A help text for the question, or None for no help.
                       A console bridge shows it when the user asks for
                       help. A GUI bridge that overrides ask_form() and
                       ask_matrix_form() may ignore it.

        Returns:
            The user's choice as a boolean.
        Raises:
            NotImplementedError: The bridge does not implement ask_yes_no().
            WizardBack: The user asked to return to the previous question.
            WizardCancelLevel: The user cancelled the current level.
            WizardAbort: The user abandoned the whole wizard.
        """
        raise NotImplementedError('ask_yes_no() not implemented')

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
        """Ask the user to pick exactly one of choices and return it.

        The return value is one of choices, or None for no choice when
        nullable. An empty answer selects default, so default must name
        one of choices; when default is None an empty answer counts as no
        choice, which is None when nullable and is re-asked otherwise.
        The overloads type the result as str when nullable is left out
        or False, so existing callers need no None check.

        The application is responsible for implementing this method with
        a real single-choice control, such as a drop-down or a set of
        radio buttons in a graphical bridge, that offers an explicit
        empty entry when nullable. A derived bridge repeats the two
        overloads on its override. The base class has no implementation.

        Args:
            question: The question to ask the user.
            choices: The choices to offer, in display order.
            default: The choice selected by an empty answer, or None to
                     require an explicit choice. Not allowed together
                     with nullable.
            re_ask_reason: The reason for re-asking, shown before the
                           first question when not None.
            nullable: When True the user may select no choice, which is
                      reported as None.
            start_value: The choice the question starts with, or None to
                         start with the default. It must be one of
                         choices. An emptied answer gives what an empty
                         answer gives, so it may be combined with
                         nullable. A console bridge shows it as the
                         answer Enter keeps and offers ':e' to empty it.
            help_text: A help text for the question, or None for no help.
                       A console bridge shows it when the user asks for
                       help. A GUI bridge that overrides ask_form() and
                       ask_matrix_form() may ignore it.

        Returns:
            The chosen value, one of choices, or None for no choice when
            nullable.
        Raises:
            ValueError: default or start_value is not one of choices,
                        or default is given together with nullable. A
                        bridge checks this with
                        arg_types.check_choice_args().
            NotImplementedError: The bridge does not implement ask_choice().
            WizardBack: The user asked to return to the previous question.
            WizardCancelLevel: The user cancelled the current level.
            WizardAbort: The user abandoned the whole wizard.
        """
        raise NotImplementedError('ask_choice() not implemented')

    # pylint: disable-next=too-many-arguments
    def ask_multi(self, question: str, *, choices: Sequence[str],
                  default: Optional[Sequence[str]] = None, min_select: int = 0,
                  max_select: Optional[int] = None,
                  re_ask_reason: Optional[str] = None,
                  start_value: Optional[Sequence[str]] = None,
                  help_text: Optional[str] = None) -> list[str]:
        """Ask the user to pick several of choices and return them.

        The result holds the chosen values in the order of choices, with
        a count between min_select and max_select; max_select None means
        no upper bound, and 0 <= min_select <= max_select <= len(choices).
        An empty answer selects default, or selects nothing when default
        is None. A default names distinct choices, at most max_select of
        them, but may name fewer than min_select so that the user makes
        the rest of the selection deliberately.

        The application is responsible for implementing this method with
        a real multi-selection control, such as a list of check boxes or
        a multi-select list in a graphical bridge. The base class has no
        implementation.

        Args:
            question: The question to ask the user.
            choices: The choices to offer, in display order.
            default: The values pre-selected by an empty answer, or None.
            min_select: The smallest acceptable number of choices.
            max_select: The largest acceptable number of choices, or None
                        for no upper bound.
            re_ask_reason: The reason for re-asking, shown before the
                           first question when not None.
            start_value: The values selected when the question starts,
                         or None to start with the default. It follows
                         the rules of a default. Emptying the selection
                         selects nothing, not the default. A console
                         bridge shows it as the answer Enter keeps and
                         offers ':e' to select nothing.
            help_text: A help text for the question, or None for no help.
                       A console bridge shows it when the user asks for
                       help. A GUI bridge that overrides ask_form() and
                       ask_matrix_form() may ignore it.

        Returns:
            The chosen values, each one of choices, in choices order.
        Raises:
            ValueError: The bounds cannot be satisfied, or default or
                        start_value names a value that is not a choice,
                        names a choice twice or names more than
                        max_select choices. A
                        bridge checks this with
                        arg_types.check_multi_args().
            NotImplementedError: The bridge does not implement ask_multi().
            WizardBack: The user asked to return to the previous question.
            WizardCancelLevel: The user cancelled the current level.
            WizardAbort: The user abandoned the whole wizard.
        """
        raise NotImplementedError('ask_multi() not implemented')

    # pylint: disable-next=too-many-arguments
    def ask_table(self, columns: Sequence[TableColumn],
                  cells: list[list[TableCell]], question: str, *,
                  re_ask_reason: Optional[str] = None,
                  partial_check: Optional[PartialCheck] = None,
                  min_rows: Optional[int] = None,
                  max_rows: Optional[int] = None,
                  help_text: Optional[str] = None
                  ) -> list[list[Optional[str]]]:
        """Ask the user to fill in a table and return its cells.

        The bridge shows a table whose columns are described by columns
        and whose rows start from cells. Each row in cells holds one
        TableCell per column. Read-only columns show the fixed text in
        each cell, such as a column of parameter names, while editable
        columns show pre-filled or empty values the user may change.

        The base implementation is permanent. It asks the table as a
        matrix form with ask_matrix_form(), so a bridge that shows a
        matrix form shows a table the same way. Row 0 of the matrix is a
        header row of bold labels with the column headers, and each table
        row is the matrix row below it. A read-only cell is a label, and
        an editable cell is a text cell, or a choice cell when it has
        choices, with help_text as its help text, its value as its
        start_value and the nullable of its TableCell. Each row the user
        adds is built from the cells shared by every starting row, as
        bridge_helpers.new_row_template() does, with every column
        editable. A console names each cell by the
        read-only texts of its row and its column header. A bridge may
        override this method to show its own table widget, and the
        helpers in wizard_ui_bridge.bridge_helpers fill a table one cell
        at a time for a bridge that asks one question at a time.

        How an empty editable cell is reported follows its TableCell: a
        nullable cell reports None, a free-text cell reports an empty
        string, and a cell with choices treats empty as not yet a valid
        value. A pre-filled cell starts with its value, and the user may
        keep it, change it or empty it.

        When partial_check is given, the bridge calls it after the user
        changes a cell, passing the whole table as it currently stands
        and the (row, column) position of the changed cell, both 0-based.
        The callback returns (accepted, message); the bridge uses message
        to give early feedback. The callback must tolerate empty or partly
        filled cells. A bridge should, where its user interface makes it
        reasonable, refuse to accept the table while the check rejects a
        cell the user has changed, but the caller must not rely on that:
        a bridge may only show the message, so the wizard must validate
        the final table. In the base implementation the partial validator
        of ask_matrix_form() checks the changed cell first, then the other
        cells the user has changed, and gives the message of the first
        cell rejected, prefixed with its cell name when it is not the
        changed cell. A cell the user has not changed is not checked. So
        a bridge whose ask_matrix_form() refuses an invalid matrix refuses
        the table too, while the base console ask_matrix_form() only shows
        the message.

        Args:
            columns: Description of each column, in left-to-right order.
            cells: Starting rows, each a list of one TableCell per column.
            question: The question or instruction shown above the table.
            re_ask_reason: The reason for re-asking, for instance that a
                           value failed validation.
            partial_check: Optional callback for early per-cell feedback.
                           It receives the current table and the changed
                           (row, column) position and returns an accepted
                           flag and a message.
            min_rows: Minimum number of rows the user must leave in the
                      table, or None when rows are fixed to the rows in
                      cells. A variable number of rows requires both
                      min_rows and max_rows to be non-None, and
                      0 <= min_rows <= len(cells) <= max_rows.
            max_rows: Maximum number of rows the user may add the table
                      to, or None when rows are fixed to the rows in
                      cells. A variable number of rows requires both
                      min_rows and max_rows to be non-None.
            help_text: A help text for the question, or None for no help.
                       A console bridge shows it when the user asks for
                       help. A GUI bridge that overrides ask_form() and
                       ask_matrix_form() may ignore it.

        Returns:
            The complete table as rows of cells, including the read-only
            columns, with one cell per column in each row. Each cell is
            the final string the user left, or None for an empty cell.
        Raises:
            ValueError: A row of cells does not hold one cell per column,
                        or a variable number of rows breaks
                        0 <= min_rows <= len(cells) <= max_rows.
            WizardBack: The user asked to return to the previous question.
            WizardCancelLevel: The user cancelled the current level.
            WizardAbort: The user abandoned the whole wizard.
        """
        table = TableMatrix(columns, cells, partial_check, help_text)
        request = table.request(question, min_rows, max_rows)
        answers = self.ask_matrix_form(request, re_ask_reason=re_ask_reason)
        return table.values(answers)

    def ask_form(self, long_question: str, ask_fields: AskFields, *,
                 re_ask_reason: Optional[str] = None,
                 partial_validator: Optional[PartialFormValidator] = None,
                 live_validator: Optional[LiveFormValidator] = None) \
            -> AnswerFields:
        """Ask the user to fill in a form and return the answers.

        The bridge shows a form whose fields are described by ask_fields.
        The base implementation is permanent and suitable for a console
        text interface: it shows long_question, then asks each field in
        turn with the typed ask methods ask_text(), ask_int(),
        ask_yes_no(), ask_path(), ask_choice() and ask_multi(), and
        returns one AnswerField per field in the same order. A field's
        help text is shown before the field is asked, and is also passed
        as help_text, so a console user can ask to see it again.

        Any serious application or library using GUI, textual, curses or
        web interfaces should override this method to show the whole form
        at once, so the user sees every question together and answers them
        in any order. In such an implementation ask_form is typically a
        dialog or form window with long_question and re_ask_reason shown
        above a grid with two columns: the left column a label with the
        field's short question, and the right column an input widget.

        See wizard_ui_bridge.form_defs for the AskFields, and the
        description of how each field type is typically implemented in a GUI
        or textual interface.

        When live_validator is given, the base implementation calls it
        first for the whole form, with None, without showing its message,
        and then after each field is answered, passing the current answers
        and the index of the field just answered. It shows the returned
        message and skips asking the fields listed in disable_row_idxs,
        filling them with their start value, default or not-yet-answered
        value instead. Each prefill is offered as the start value of its
        field when that field is asked. WizardBack steps to the previous asked
        field, which starts with the answer the user gave it; from the
        first field it propagates so the wizard steps to the previous
        question.

        The verdict of live_validator is advisory to the caller. A bridge
        that overrides this method should call it with None when the form
        is first shown, to find the rows that start disabled and any
        prefills, but show its message only once the user has changed the
        form or tried to submit it. It should, where its user interface
        makes it reasonable, refuse to accept the form while the verdict
        is not valid, but the caller must not rely on that: the base
        implementation only shows the message, so the wizard must validate
        the final answers.

        Args:
            long_question: The main question or instruction to the user,
                           typically shown above the form. It may be long
                           string that the UI bridge is responsible for
                           wrapping and displaying nicely.
            ask_fields: Description of each field in the form.
            re_ask_reason: The reason for re-asking, for instance how a
                           value failed validation.
            partial_validator: Deprecated, use live_validator. It will be
                               removed in version 2.0. It is called as
                               live_validator, but with 0 in place of None.
            live_validator: Optional callback for live feedback on the
                            partly filled form. It receives the current
                            answers and the changed field index, or None
                            when no field has changed yet, and returns a
                            PartFormValidationResult.

        Returns:
            One AnswerField per AskField, in the order of ask_fields.
        Raises:
            WizardBack: The user asked to return to the previous question.
            WizardCancelLevel: The user cancelled the current level.
            WizardAbort: The user abandoned the whole wizard.
            TypeError: Both partial_validator and live_validator are given.
        """
        validator = live_validator_of(partial_validator, live_validator)
        self._show_question(long_question, re_ask_reason)
        answers = [initial_answer(field) for field in ask_fields]
        self._fill_form(ask_fields, answers, validator)
        return answers

    def supports_form_field(self, field: AskField) -> bool:
        """Return True when the bridge can show the given form field.

        A bridge that overrides ask_form() may not yet support all
        the AskField types. This method returns True when the bridge can
        show the given field, and False when it cannot. The base implementation
        returns True only for the field types that oldest form bridges support,
        so a bridge that overrides ask_form() should override this method as
        well. The base implementation returns False for a nullable choice
        field, since a bridge written before ask_choice() took nullable
        cannot ask one; a bridge whose ask_choice() supports nullable
        overrides this method to accept it.

        Args:
            field: The form field to check.
        Returns:
            True if the bridge can show the field, False otherwise.
        """
        return isinstance(field, (AskTextField, AskIntField, AskPathField,
                                  AskYesNoField, AskChoiceField,
                                  AskMultiChoiceField)) \
            and not nullable_choice(field)

    def ask_form_w_fake(self, long_question: str, ask_fields: AskFields, *,
                        re_ask_reason: Optional[str] = None,
                        partial_validator: Optional[PartialFormValidator]
                        = None,
                        live_validator: Optional[LiveFormValidator] = None
                        ) -> AnswerFields:
        """Ask the user to fill in a form faking unsupported field types.

        This is a temporary migration aid for a wizard that uses field types
        the bridge does not yet support. It replaces each unsupported field
        with a supported field that asks the question and inserts a partial
        form validator that guides the answer to something that can be
        converted to the unsupported field type. ask_form() is then called
        with the modified fields and validator, and the answers are converted
        back to the original field types before returning.

        Args:
            long_question: The main question or instruction to the user,
                           typically shown above the form. It may be long
                           string that the UI bridge is responsible for
                           wrapping and displaying nicely.
            ask_fields: Description of each field in the form.
            re_ask_reason: The reason for re-asking, for instance how a
                           value failed validation.
            partial_validator: Deprecated, use live_validator. It will be
                               removed in version 2.0. It is called as
                               live_validator, but with 0 in place of None.
            live_validator: Optional callback for live feedback on the
                            partly filled form. It receives the current
                            answers and the changed field index, or None
                            when no field has changed yet, and returns a
                            PartFormValidationResult.

        Returns:
            One AnswerField per AskField, in the order of ask_fields.
        Raises:
            WizardBack: The user asked to return to the previous question.
            WizardCancelLevel: The user cancelled the current level.
            WizardAbort: The user abandoned the whole wizard.
            RuntimeError: The bridge cannot show any field type that would
                          allow the requested field types to be faked, so
                          the form cannot be shown at all.
            TypeError: Both partial_validator and live_validator are given.
        """
        validator = live_validator_of(partial_validator, live_validator)
        return ask_form_faking(self, long_question, ask_fields,
                               re_ask_reason=re_ask_reason,
                               live_validator=validator)

    def ask_matrix_form(self, request: MatrixRequest, *,
                        re_ask_reason: Optional[str] = None) -> AnswerCells:
        """Ask the user to fill in values in the cells of a matrix form.

        The bridge shows a matrix shaped form whose cells are described
        by request.ask_cells, in the shape request.dimensions.default.
        When the minimum and maximum dimensions differ, the user may
        append or delete the last row or column within those bounds.

        The base implementation is permanent and suitable for a console
        text interface. It shows request.long_question and re_ask_reason,
        then asks each enabled input cell in turn with the typed ask
        methods, in the order and with the cell names that
        request.console_question gives. When the matrix may be resized,
        ask_choice() offers to append or delete the last row or column:
        at the end of the matrix, where an empty answer is done, and when
        the number of cells in a line may change, also after the first
        row (or column, in column order) with input cells, so the user
        can set the width before the other rows are asked. An appended
        row or column asks its new cells at once. Each cell is asked with
        its help text as help_text, and the resize menu with a help text
        that explains its actions; the help text of a cell is also shown
        before the cell is asked when request.console_question has
        use_help_text set. WizardBack steps back to the previously asked
        cell, and from the first cell propagates so the wizard steps to
        the previous question.

        In the base implementation the partial validator is called first
        for the whole matrix, then after each cell is answered and after
        each change of shape. Its message is shown when the matrix is not
        valid, its disabled cells are skipped and keep their answers, and
        each prefill is offered as the start value of its cell when that
        cell is asked. A cell asked again after WizardBack starts with the
        answer the user gave it. The message is advisory only: the matrix
        is returned even when it is not valid, so the wizard must check
        the answers.

        Any serious application or library using GUI, textual, curses or
        web interfaces should override this method to show the whole matrix
        form at once, so the user sees all the cells together and answers them
        in any order. In such an implementation ask_matrix_form is typically a
        window with request.long_question and re_ask_reason shown above a
        grid of rows x columns cells, where each cell shows the AskCell at
        its position. The window also has a feed-back area for messages
        from request.partial_validator, and for the bridge's own messages
        about a single cell, which name the cell with request.cell_namer
        or its labels (see wizard_ui_bridge.matrix_helpers). The partial
        validator is called when the matrix is first shown, to find the
        cells that start disabled, but its message is only shown once
        the user has changed the matrix or tried to submit it. Such an
        implementation should, where its user interface makes it
        reasonable, refuse to submit the matrix while the partial
        validator finds it not valid. The caller must not rely on that,
        since the base implementation returns an invalid matrix too.

        See wizard_ui_bridge.matrix_cell_defs for the cell types and
        wizard_ui_bridge.matrix_defs for the request and its validator.

        Args:
            request: The MatrixRequest object containing all the details for
                the matrix form.
            re_ask_reason: The reason for re-asking, for instance how a
                           value failed validation.

        Returns:
            The answers in the final shape of the matrix, one row per
            matrix row: an AnswerCell for each input cell, and None for
            each label cell (AskLabelCell).

        Raises:
            WizardBack: The user asked to return to the previous question.
            WizardCancelLevel: The user cancelled the current level.
            WizardAbort: The user abandoned the whole wizard.
        """
        self._show_question(request.long_question, re_ask_reason)
        return ConsoleMatrix(self, request).run()

    def _show_question(self, long_question: str,
                       re_ask_reason: Optional[str]) -> None:
        """Show the question of a form, and the reason when re-asked."""
        self.show(long_question)
        if re_ask_reason is not None:
            self.show(re_ask_reason)

    def _fill_form(self, ask_fields: AskFields, answers: list[AnswerField],
                   validator: Optional[LiveFormValidator]) -> None:
        """Ask each enabled field in turn, stepping back on WizardBack.

        starts holds the latest answer or prefill of each field, which
        the field starts with when it is asked (again). The validator
        is first called for the whole form, with None.
        """
        starts: dict[int, Optional[PrefillValueType]] = {}
        disabled = self._form_feedback(ask_fields, answers, None, validator,
                                       starts)
        position = 0
        while position < len(ask_fields):
            if position in disabled:
                position += 1
                continue
            try:
                answers[position] = self._ask_field(ask_fields[position],
                                                    position, starts)
            except WizardBack:
                position = self._prev_field(position, disabled)
                continue
            starts[position] = answers[position].value
            disabled = self._form_feedback(ask_fields, answers, position,
                                           validator, starts)
            position += 1

    @staticmethod
    def _prev_field(position: int, disabled: set[int]) -> int:
        """Return the previous enabled field index, or re-raise WizardBack."""
        prev = position - 1
        while prev >= 0 and prev in disabled:
            prev -= 1
        if prev < 0:
            raise WizardBack()
        return prev

    # pylint: disable-next=too-many-arguments
    def _form_feedback(self, ask_fields: AskFields, answers: list[AnswerField],
                       position: Optional[int],
                       validator: Optional[LiveFormValidator],
                       starts: dict[int, Optional[PrefillValueType]]
                       ) -> set[int]:
        """Run the validator, show its message, store prefills, return rows.

        Prefills for other rows are validated and kept in starts, so a
        row is offered the value as its start value when it is asked.
        The message is not shown for the first call, with position None,
        when no field has been answered yet.
        """
        if validator is None:
            return set()
        result = validator(answers, position)
        if position is not None and not result.is_valid and result.message:
            self.show(result.message)
        for index, value in valid_prefills(ask_fields, position,
                                           result.prefill_values):
            starts[index] = value
        return set(result.disable_row_idxs)

    def _ask_field(self, field: AskField, position: int,
                   starts: dict[int, Optional[PrefillValueType]]
                   ) -> AnswerField:
        """Ask one form field with the matching typed ask method.

        A field with an entry in starts starts with that value, so the
        user can keep, edit or empty it. The answer refers to field.
        """
        asked = prefilled_field(field, starts[position]) \
            if position in starts else field
        if field.help_text is not None:
            self.show(field.help_text)
        return answer_of(field, ask_cell_value(self, field.short_question,
                                               asked))

    def error_file(self) -> TextIO:
        """Return the stream used for validation diagnostics."""
        return sys.stderr

    def show(self, message: str) -> None:
        """Show a message to the user.

        If implementing a graphical user interface, this method should
        display the message in a dialog or a message box. If implementing
        a console text user interface, this method should print the
        message to the console.

        Args:
            message: The message to show the user.
        """
        raise NotImplementedError('show() not implemented')


def _text_of(value: Optional[Union[int, Path]]) -> Optional[str]:
    """Return value as the text a user types for it, or None for None."""
    return None if value is None else str(value)
