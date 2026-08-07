#! /usr/local/bin/python3
"""A Tk host that asks every wizard prompt in turn, one at a time.

:class:`WizardWindow` lays out one question at a time: a text entry, an
integer entry, a path entry with a native Browse button, a yes/no button
pair, a single- and a multi-selection list, an editable table and a whole
form on one screen, kept below a lasting message area. Every prompt also
offers back, out-one-level and abort buttons, which raise the matching
:class:`WizardNavigation` request so the wizard can step within the
configuration or abandon it.

Return pressed in an input confirms the prompt, exactly as its OK button
does, which that button shows by being the marked default one. The
editable table is the exception: a row added after the buttons were built
would miss the binding, so a table is confirmed by its button alone.

A WizardWindow either owns a new window of its own, built with ``parent``,
or is embedded directly into an existing container the caller built,
given as ``area``. Exactly one of the two is given.
``modal`` decides whether the wizard grabs that window for the session,
which the caller is best placed to decide since only it knows whether the
rest of the window should stay usable meanwhile.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter as tk
from pathlib import Path
from tkinter import ttk
from typing import Callable, Optional, Sequence
from wizard_ui_bridge import AnswerFields, AskFields, PartialCheck, \
    PartialFormValidator, PathAskOptions, TableCell, TableColumn, \
    WizardAbort, WizardBack, WizardCancelLevel, WizardNavigation
from wizard_ui_bridge.bridge_helpers import path_answer
from wizard_tk_bridge.close_binding import bind_close
from wizard_tk_bridge.gui_style import focus_first_input, style_input
from wizard_tk_bridge.wizard_form import FormEditor, int_answer
from wizard_tk_bridge.wizard_path import PathRow
from wizard_tk_bridge.wizard_table import TableEditor

WIZARD_TITLE = 'Configuration wizard'
WINDOW_SIZE = '720x620'
WRAP_LENGTH = 520
MESSAGE_HEIGHT = 8
CHOICE_HEIGHT = 10
_RETURN_INPUTS = (tk.Entry, tk.Listbox, tk.Checkbutton, ttk.Combobox)


def _default_path_text(options: PathAskOptions) -> str:
    """Return the initial path text from the option's default."""
    return '' if options.default is None else str(options.default)


def _bind_submit(widget: tk.Misc, on_ok: Callable[[], None]) -> None:
    """Bind Return to the confirm action on every input inside widget.

    A prompt builds its inputs before its buttons, so binding them all
    from one place gives every prompt the same rule: Return in an input
    does what the default OK button does. Only inputs are bound, which
    both leaves the Browse, Pick and navigation buttons their own keys
    and reaches the entry inside a two-widget input row.
    """
    if isinstance(widget, _RETURN_INPUTS):
        widget.bind('<Return>', lambda _event: on_ok(), add='+')
    for child in widget.winfo_children():
        _bind_submit(child, on_ok)


# pylint: disable-next=too-many-instance-attributes
class WizardWindow:
    """A Tk host, own window or embedded, that asks every wizard prompt."""

    def __init__(self, parent: Optional[tk.Misc] = None,
                 area: Optional[tk.Misc] = None, modal: bool = True) -> None:
        """Build the wizard's own window, or embed it into an existing area.

        Exactly one of parent or area must be given; see the module
        docstring for what each means and how modal applies to it.
        """
        if (parent is None) == (area is None):
            raise ValueError('Give exactly one of parent and area.')
        self._result: object = ''
        self._nav: Optional[type[WizardNavigation]] = None
        self._editor: Optional[TableEditor] = None
        self._form: Optional[FormEditor] = None
        self._modal = modal
        self._closed = False
        if parent is not None:
            self._win: Optional[tk.Toplevel] = self._build_toplevel(parent)
            container: tk.Misc = self._win
            self._grab_target: tk.Misc = self._win
        else:
            assert area is not None
            self._win = None
            container = area
            self._grab_target = area.winfo_toplevel()
        if modal:
            self._grab()
        self._done = tk.IntVar(container, 0)
        self._messages = self._build_messages(container)
        self._content = tk.Frame(container)
        self._content.pack(fill='both', expand=True, padx=12, pady=6)

    def _build_toplevel(self, parent: tk.Misc) -> tk.Toplevel:
        """Create and configure the wizard's own top-level window."""
        win = tk.Toplevel(parent)
        win.title(WIZARD_TITLE)
        win.geometry(WINDOW_SIZE)
        win.resizable(True, True)
        top = parent.winfo_toplevel()
        if isinstance(top, tk.Wm) and top.state() != 'withdrawn':
            win.transient(top)
        else:
            win.deiconify()
            win.lift()
        win.protocol('WM_DELETE_WINDOW', self._cancel)
        bind_close(win, self._cancel)
        return win

    def _build_messages(self, container: tk.Misc) -> tk.Text:
        """Build the read-only area that keeps the wizard messages."""
        text = tk.Text(container, height=MESSAGE_HEIGHT, wrap='word',
                       state='disabled')
        text.pack(fill='x', padx=12, pady=(12, 6))
        return text

    def show(self, message: str) -> None:
        """Append one lasting message to the message area."""
        self._messages.configure(state='normal')
        self._messages.insert('end', message + '\n')
        self._messages.see('end')
        self._messages.configure(state='disabled')

    def close(self) -> None:
        """Release any modal grab and remove the wizard's own widgets."""
        if self._closed:
            return
        self._closed = True
        if self._modal and self._grab_target.winfo_exists():
            try:
                self._grab_target.grab_release()
            except tk.TclError:
                pass
        if self._win is not None:
            if self._win.winfo_exists():
                self._win.destroy()
        else:
            self._messages.destroy()
            self._content.destroy()

    def ask_text(self, question: str, re_ask: Optional[str], nullable: bool,
                 default: Optional[str] = None,
                 sensitive: bool = False) -> Optional[str]:
        """Ask one free-text question and return the entered text.

        A sensitive question masks the typed text; a default value is
        pre-filled and returned when the answer is left empty.
        """
        self._begin(question, re_ask)
        entry = tk.Entry(self._content, width=44)
        if sensitive:
            entry.configure(show='*')
        elif default is not None:
            entry.insert(0, default)
        style_input(entry)
        entry.pack(anchor='w', pady=6)
        self._add_buttons(lambda: self._finish(entry.get()))
        result = self._wait()
        assert isinstance(result, str)
        return self._text_result(result, nullable, default)

    @staticmethod
    def _text_result(result: str, nullable: bool,
                     default: Optional[str]) -> Optional[str]:
        """Return the answer after the default and nullable rules."""
        if result != '':
            return result
        if default is not None:
            return default
        return None if nullable else ''

    # pylint: disable-next=too-many-arguments,too-many-positional-arguments
    def ask_int(self, question: str, re_ask: Optional[str], nullable: bool,
                min_value: Optional[int], max_value: Optional[int],
                default: Optional[int]) -> Optional[int]:
        """Ask one integer question, re-asking until it is in range."""
        reason = re_ask
        while True:
            text = self._run_int(question, reason, default)
            done, value, reason = int_answer(text, nullable, min_value,
                                             max_value, default)
            if done:
                return value

    def _run_int(self, question: str, re_ask: Optional[str],
                 default: Optional[int]) -> str:
        """Show one integer entry and return the entered text."""
        self._begin(question, re_ask)
        entry = tk.Entry(self._content, width=14)
        if default is not None:
            entry.insert(0, str(default))
        style_input(entry)
        entry.pack(anchor='w', pady=6)
        self._add_buttons(lambda: self._finish(entry.get()))
        result = self._wait()
        assert isinstance(result, str)
        return result

    def ask_path(self, question: str, options: PathAskOptions,
                 re_ask: Optional[str]) -> Optional[Path]:
        """Ask one path question with a Browse button, re-asking on error."""
        reason = re_ask
        value: Optional[str] = None
        while True:
            text = self._run_path(question, reason, options, value)
            done, path, reason = path_answer(text, options)
            if done:
                return path
            value = text

    def _run_path(self, question: str, re_ask: Optional[str],
                  options: PathAskOptions, value: Optional[str]) -> str:
        """Show one path entry with a Browse button and return the text."""
        self._begin(question, re_ask)
        initial = value if value is not None else _default_path_text(options)
        row = PathRow(self._content, options, initial)
        row.frame.pack(anchor='w', pady=6)
        self._add_buttons(lambda: self._finish(row.get()))
        result = self._wait()
        assert isinstance(result, str)
        return result

    def ask_form(self, long_question: str, fields: AskFields,
                 re_ask: Optional[str],
                 validator: Optional[PartialFormValidator]) -> AnswerFields:
        """Ask a whole form on one screen and return its answers."""
        self._begin(long_question, re_ask)
        self._form = FormEditor(self._content, fields, validator, self._finish)
        self._add_buttons(self._form.submit)
        result = self._wait()
        assert isinstance(result, list)
        return result

    def ask_yes_no(self, question: str, default: bool,
                   re_ask: Optional[str]) -> bool:
        """Ask one yes/no question with dedicated buttons."""
        self._begin(question, re_ask)
        box = tk.Frame(self._content)
        box.pack(pady=10)
        yes = tk.Button(box, text='Yes', command=lambda: self._finish(True))
        no = tk.Button(box, text='No', command=lambda: self._finish(False))
        yes.bind('<Return>', lambda _event: yes.invoke())
        no.bind('<Return>', lambda _event: no.invoke())
        yes.pack(side='left', padx=6)
        no.pack(side='left', padx=6)
        self._add_nav_buttons(box)
        chosen = yes if default else no
        chosen.configure(default='active')
        chosen.focus_set()
        result = self._wait()
        assert isinstance(result, bool)
        return result

    def ask_choice(self, question: str, choices: Sequence[str],
                   default: Optional[str], re_ask: Optional[str]) -> str:
        """Ask the user to pick exactly one choice and return it."""
        self._begin(question, re_ask)
        listbox = self._choice_list(choices, default, 'browse')
        self._add_buttons(lambda: self._pick_one(listbox, choices))
        result = self._wait()
        assert isinstance(result, str)
        return result

    # pylint: disable-next=too-many-arguments,too-many-positional-arguments
    def ask_multi(self, question: str, choices: Sequence[str],
                  default: Optional[Sequence[str]], min_select: int,
                  max_select: Optional[int], re_ask: Optional[str]
                  ) -> list[str]:
        """Ask the user to pick several choices within the count bounds."""
        reason = re_ask
        while True:
            chosen = self._run_multi(question, reason, choices, default)
            if len(chosen) < min_select:
                reason = f'Please select at least {min_select}.'
            elif max_select is not None and len(chosen) > max_select:
                reason = f'Please select at most {max_select}.'
            else:
                return chosen

    # pylint: disable-next=too-many-arguments,too-many-positional-arguments
    def ask_table(self, columns: Sequence[TableColumn],
                  cells: Sequence[Sequence[TableCell]], question: str,
                  re_ask: Optional[str], partial_check: Optional[PartialCheck],
                  min_rows: Optional[int], max_rows: Optional[int]
                  ) -> list[list[Optional[str]]]:
        """Ask the user to fill the given table rows and return them."""
        self._begin(question, re_ask)
        editor = TableEditor(self._content, columns, cells, partial_check,
                             min_rows, max_rows)
        self._editor = editor
        self._add_table_buttons(editor)
        result = self._wait()
        assert isinstance(result, list)
        return result

    def _run_multi(self, question: str, re_ask: Optional[str],
                   choices: Sequence[str],
                   default: Optional[Sequence[str]]) -> list[str]:
        """Show a multi-selection list once and return the picked values."""
        self._begin(question, re_ask)
        listbox = self._choice_list(choices, default, 'multiple')
        self._add_buttons(lambda: self._pick_many(listbox, choices))
        result = self._wait()
        assert isinstance(result, list)
        return result

    def _choice_list(self, choices: Sequence[str],
                     marked: Optional[str | Sequence[str]],
                     mode: str) -> tk.Listbox:
        """Build a selection list, preselecting the marked choices."""
        listbox = tk.Listbox(self._content, exportselection=False,
                             selectmode=mode,
                             height=min(len(choices), CHOICE_HEIGHT))
        for choice in choices:
            listbox.insert('end', choice)
        style_input(listbox)
        listbox.pack(anchor='w', pady=6)
        preset = self._preset_indexes(choices, marked)
        for index in preset:
            listbox.selection_set(index)
        return listbox

    @staticmethod
    def _preset_indexes(choices: Sequence[str],
                        marked: Optional[str | Sequence[str]]) -> list[int]:
        """Return the indexes to preselect from a default value or list."""
        if marked is None:
            return []
        wanted = {marked} if isinstance(marked, str) else set(marked)
        return [index for index, choice in enumerate(choices)
                if choice in wanted]

    def _pick_one(self, listbox: tk.Listbox, choices: Sequence[str]) -> None:
        """Finish a single-choice question with the selected value."""
        picks = listbox.curselection()  # type: ignore[no-untyped-call]
        if picks:
            self._finish(choices[int(picks[0])])

    def _pick_many(self, listbox: tk.Listbox, choices: Sequence[str]) -> None:
        """Finish a multi-choice question with the selected values."""
        picks = listbox.curselection()  # type: ignore[no-untyped-call]
        self._finish([choices[int(index)] for index in picks])

    def _begin(self, question: str, re_ask: Optional[str]) -> None:
        """Clear the content area and show the question and any reason."""
        self._nav = None
        self._editor = None
        self._form = None
        for child in self._content.winfo_children():
            child.destroy()
        if re_ask is not None:
            self._add_label(re_ask, 'red')
        self._add_label(question, 'black')

    def _add_label(self, text: str, color: str) -> None:
        """Add one wrapped label to the content area."""
        label = tk.Label(self._content, text=text, fg=color,
                         wraplength=WRAP_LENGTH, justify='left')
        label.pack(anchor='w', pady=4)

    def _add_buttons(self, on_ok: Callable[[], None]) -> None:
        """Add the confirm and navigation buttons, and bind Return.

        The confirm button is marked as the default one, which is how a
        platform shows that pressing Return does the same thing.
        """
        _bind_submit(self._content, on_ok)
        box = self._button_box()
        tk.Button(box, text='OK', command=on_ok,
                  default='active').pack(side='left')
        self._add_nav_buttons(box)

    def _button_box(self) -> tk.Frame:
        """Add and return the frame holding a prompt's buttons."""
        box = tk.Frame(self._content)
        box.pack(side='bottom', anchor='w', pady=10)
        return box

    def _add_table_buttons(self, editor: TableEditor) -> None:
        """Add confirm, optional add/remove-row and navigation buttons.

        A table binds no Return key, since a row added later would miss
        the binding, so its confirm button is not marked as the default.
        """
        box = self._button_box()
        tk.Button(box, text='OK',
                  command=lambda: self._finish(editor.values())).pack(
                      side='left')
        if editor.is_variable():
            tk.Button(box, text='Add row',
                      command=editor.add_row).pack(side='left', padx=6)
            tk.Button(box, text='Remove row',
                      command=editor.remove_row).pack(side='left', padx=6)
        self._add_nav_buttons(box)

    def _add_nav_buttons(self, box: tk.Frame) -> None:
        """Add the back, out-one-level and abort navigation buttons."""
        tk.Button(box, text='Back',
                  command=self._back).pack(side='left', padx=6)
        tk.Button(box, text='Out one level',
                  command=self._cancel_level).pack(side='left', padx=6)
        tk.Button(box, text='Abort',
                  command=self._cancel).pack(side='left', padx=6)

    def _wait(self) -> object:
        """Focus the first input, then wait for an answer or navigation."""
        if self._win is not None:
            self._win.lift()
        focus_first_input(self._content)
        self._content.wait_variable(self._done)
        if self._nav is not None:
            raise self._nav()
        return self._result

    def _finish(self, value: object) -> None:
        """Store the answer and release the waiting prompt."""
        self._result = value
        self._done.set(self._done.get() + 1)

    def _back(self) -> None:
        """Request a step back to the previous question."""
        self._navigate(WizardBack)

    def _cancel_level(self) -> None:
        """Request leaving the current level by one step."""
        self._navigate(WizardCancelLevel)

    def _cancel(self) -> None:
        """Request abandoning the whole configuration."""
        self._navigate(WizardAbort)

    def _navigate(self, request: type[WizardNavigation]) -> None:
        """Record a navigation request and release the waiting prompt."""
        self._nav = request
        self._done.set(self._done.get() + 1)

    def _grab(self) -> None:
        """Take the modal grab, retrying until the target is viewable."""
        if self._closed or not self._grab_target.winfo_exists():
            return
        try:
            self._grab_target.grab_set()
        except tk.TclError:
            self._grab_target.after(50, self._grab)
