# wizard-tk-bridge

[wizard-ui-bridge](https://pypi.org/project/wizard-ui-bridge/) is
the user-interface-independent way for a wizard to ask a user questions.

`wizard-tk-bridge` is the Tk (Tkinter) implementation of this
user-interface-independent way for a wizard to ask a user questions.
A wizard written for `wizard-ui-bridge` works out of the box if
passed a `wizard-tk-bridge` as bridge.

## Is this package for you?

This package is a good fit when one or more of these apply:

- You have a wizard written for `wizard-ui-bridge` and want to run it in
  a graphical user interface, without changing a line of the wizard.
- Your application is a Tkinter application, and its questions belong in
  real widgets rather than in a terminal.
- You want what a console cannot offer: a native file and directory
  picker, a month calendar for dates, help texts as hover tooltips, an
  editable table with add-row and remove-row buttons, and a whole form
  on one screen that the user fills in any order.
- Your program is otherwise a plain command-line tool, and you want to
  ask through a window without writing any Tkinter code of your own.
- You want to decide where the wizard appears: in a window of its own
  over your application, or inside a panel your application built.

This package is probably not the right one when:

- Your program runs in a terminal, or on a machine with no display. Use
  the console or Textual bridge of
  [wizard-ui-bridge](https://pypi.org/project/wizard-ui-bridge/).
- Your application uses another graphical toolkit, such as Qt, wxPython
  or GTK. Write a bridge for that toolkit instead, by subclassing
  `WizardUiBridge`.
- You want a general widget toolkit. Use Tkinter directly.

## Installation

`wizard-tk-bridge` requires Python 3.12 or newer, and the standard
library module `tkinter`.

```sh
pip install --upgrade wizard-tk-bridge
```

This installs
[wizard-ui-bridge](https://pypi.org/project/wizard-ui-bridge/) as well,
since a Tk bridge is a `WizardUiBridge`.

`tkinter` belongs to the standard library, but it is not a pure Python
module, and several Linux distributions leave it out of their base
Python package. A standard library module is not something `pip` can
install, so add it with the system package manager instead:

```sh
sudo apt install python3-tk       # Debian, Ubuntu
sudo dnf install python3-tkinter  # Fedora, RHEL
```

The usual CPython installers for Windows and macOS already include it.

## Quick start

Ask a few questions from a program that has no window of its own:

```python
from wizard_tk_bridge import WizardUiBridgeTk

bridge = WizardUiBridgeTk()
try:
    name = bridge.ask_text('Your name?', nullable=True)
    topping = bridge.ask_choice('Favorite topping?',
                                choices=('Mushroom', 'Pepperoni', 'Olive'))
    cheese = bridge.ask_yes_no('Extra cheese?', default=False)
finally:
    bridge.close()
print(f'{name or "Anonymous"} orders {topping}, extra cheese: {cheese}')
```

Every ask method blocks until the user answers, so the wizard stays
straight-line code. No `mainloop()` call is needed: the ask methods pump
the Tk event loop themselves and return as soon as the answer is in, and
the program is not left running an event loop once the wizard closes.
All questions of one session are asked in the same reused window, so the
session does not jump around the display.

Every question also carries **Back**, **Out one level** and **Abort**
buttons, which raise `WizardBack`, `WizardCancelLevel` and `WizardAbort`
instead of returning an answer. Closing the wizard's own window, or
pressing Cmd-W (Ctrl-W on Windows) in it, is an abort as well. The short
example above catches none of them and simply lets them propagate.

## Where the wizard appears

That is the one question the Tk bridge adds to the wizard-ui-bridge API,
and the constructor answers it:

| Your application | Arguments | What the bridge builds |
| ---------------- | --------- | ---------------------- |
| A command-line program with no Tkinter code | neither | a hidden root, and the wizard's own window over it |
| Has windows of its own | `parent=widget` | a new window over the widget's window |
| Has a container set aside for the wizard | `area=container` | the wizard's widgets inside that container |

`parent` and `area` are mutually exclusive; giving both raises
`ValueError`. The visible part is built on the first question, so a
bridge that is never asked anything puts nothing on the screen.

`modal` (default `True`) decides whether the wizard grabs its window —
or the window containing `area` — for the whole session, leaving the
rest of that window unusable meanwhile. Only the application knows
whether its other content should stay usable, which is why it decides.
An embedded wizard normally passes `modal=False`, since keeping the rest
of the window usable is the reason to embed rather than pop up.

`close()` is not optional. It releases the modal grab, destroys the
wizard's own window or clears its area, and destroys the hidden root
when the bridge owns one. Call it from a `finally`, because a wizard's
normal way of ending is often a `WizardNavigation` exception rather than
a `return`. Calling it twice is harmless.

## What the user gets

`WizardUiBridgeTk` overrides every ask method, the inheritable ones
included — above all `ask_path()` and `ask_form()`, where a graphical
interface beats the base class fallback outright:

| Ask method | What the user gets |
| ---------- | ------------------ |
| `ask_text` | a text entry, masked when `sensitive` |
| `ask_int` | a numeric entry, re-asked until the value parses and fits its bounds |
| `ask_path` | an entry with a **Browse** button opening the native file or directory picker |
| `ask_yes_no` | a **Yes** and a **No** button |
| `ask_choice` / `ask_multi` | a single- / multi-selection list |
| `ask_table` | an editable grid, with **Add row** and **Remove row** when the question allows a variable number of rows |
| `ask_form` | every field of the form on one screen, answered in any order |

In a form, a field's `help_text` becomes a hover tooltip rather than an
extra printed line, the float, time and duration fields show their
accepted format as greyed placeholder text, and a date or date-time
field adds a **Pick** button opening a month calendar.

`show()` appends to a message area kept above the current question, so
earlier messages stay readable as the wizard moves on. They disappear
with the window, so a final message needs a question after it to be seen
at all — exactly as on the Textual bridge.

A graphical interface has no console to write side notes to, so
`error_file()` returns a stream that discards what is written to it.
Pass `WizardUiBridgeTk(log=stream)` to send those diagnostics somewhere
real, such as an open log file.

## Relation to wizard-ui-bridge

`wizard-tk-bridge` and `wizard-ui-bridge` are built from the same
repository and released together, so a version of this package requires
the matching version of `wizard-ui-bridge`, or newer.

This Tk bridge started out inside one application that used
`wizard-ui-bridge`. It was moved into a package of its own so that it
can be developed alongside `wizard-ui-bridge` and used by any other
application.

## Documentation

- Teaching examples and walkthroughs: [wizard_tk_bridge/example/src/wizard_tk_example/README.md](https://github.com/tom-bjorkholm/wizard-ui-bridge/blob/master/wizard_tk_bridge/example/src/wizard_tk_example/README.md)

- Public API notes: [doc/wizard_tk_bridge_api.md](https://github.com/tom-bjorkholm/wizard-ui-bridge/blob/master/doc/wizard_tk_bridge_api.md)

- Protected/internal API notes: [doc/wizard_tk_bridge_protected_api.md](https://github.com/tom-bjorkholm/wizard-ui-bridge/blob/master/doc/wizard_tk_bridge_protected_api.md)

- Source repository: [wizard-ui-bridge](https://github.com/tom-bjorkholm/wizard-ui-bridge/)

## License

MIT

## Test summary

- Test result: 1051 passed, 9 deselected in 37s
- No flake8 warnings.
- No mypy errors found.
- No pylint warnings.
- No python layout warnings.
- Built version(s): 1.3.1
- Build and test using Python 3.14.6
