# wizard-tk-bridge teaching examples

## Introduction

A *wizard* is any code that asks a user a series of questions. A
`WizardUiBridge` is the user-interface-independent object the wizard asks them
through, so one wizard can run on a plain console, on a full-screen Textual
interface, or on any other bridge an application supplies.

`WizardUiBridgeTk` is that bridge built out of real Tkinter widgets. A wizard
written against `wizard-ui-bridge` runs on it unchanged: the wizard code never
mentions Tk, and the bridge never knows which wizard it is serving.

That leaves exactly one new question for you to answer, and it is the subject
of these examples: **where in your Tkinter application does the wizard
appear?** A command-line program has no window at all, an application with its
own windows wants a pop-up over them, and an application with a panel set aside
for the wizard wants it built into that panel. The three teaching examples are
one each of those.

## Read the wizard-ui-bridge examples first

This README covers only what Tk adds. The bridge API itself — the ask methods,
the navigation requests, tables, forms and typed form fields — is taught by the
[wizard-ui-bridge teaching examples](https://github.com/tom-bjorkholm/wizard-ui-bridge/blob/master/wizard_ui_bridge/example/src/wizard_ui_example/README.md),
which are the intended reading before this folder. Everything they teach holds
here, because they are teaching the wizard's side of the same interface.

## The examples in this folder

There are two groups, and only the first group is a lesson about Tk.

### Teaching examples: putting the wizard in your application

Read these in order. All three ask the *same* three trivial pizza questions, so
the only thing that differs between them is how the Tk widgets around the
wizard are put together.

- [`e01_cli_wizard.py`](https://github.com/tom-bjorkholm/wizard-ui-bridge/blob/master/wizard_tk_bridge/example/src/wizard_tk_example/e01_cli_wizard.py)
  a command-line program with no Tkinter code of its own; the bridge owns the
  whole Tk application.
- [`e02_new_window.py`](https://github.com/tom-bjorkholm/wizard-ui-bridge/blob/master/wizard_tk_bridge/example/src/wizard_tk_example/e02_new_window.py)
  an application that already has a window; the wizard pops up in a new window
  over it.
- [`e03_embedded_area.py`](https://github.com/tom-bjorkholm/wizard-ui-bridge/blob/master/wizard_tk_bridge/example/src/wizard_tk_example/e03_embedded_area.py)
  an application with a panel set aside for the wizard; the wizard is built
  into that panel, with no window of its own.

### Runner examples: the same wizards, shown in Tk

These teach nothing new about the Tk bridge. Each one imports a wizard from
`wizard_ui_example` — the *same* module the console and Textual examples run —
and hands it a `WizardUiBridgeTk`. The `run_` prefix says so: the lesson is in
the file they run, not in the file itself.

- [`run_e01_one_question.py`](https://github.com/tom-bjorkholm/wizard-ui-bridge/blob/master/wizard_tk_bridge/example/src/wizard_tk_example/run_e01_one_question.py)
  runs [`e01_one_question.py`](https://github.com/tom-bjorkholm/wizard-ui-bridge/blob/master/wizard_ui_bridge/example/src/wizard_ui_example/e01_one_question.py):
  free text, an optional answer and a sensitive answer.
- [`run_e02_question_kinds.py`](https://github.com/tom-bjorkholm/wizard-ui-bridge/blob/master/wizard_tk_bridge/example/src/wizard_tk_example/run_e02_question_kinds.py)
  runs [`e02_question_kinds.py`](https://github.com/tom-bjorkholm/wizard-ui-bridge/blob/master/wizard_ui_bridge/example/src/wizard_ui_example/e02_question_kinds.py):
  every one-at-a-time ask method once.
- [`run_e03_navigation.py`](https://github.com/tom-bjorkholm/wizard-ui-bridge/blob/master/wizard_tk_bridge/example/src/wizard_tk_example/run_e03_navigation.py)
  runs [`e03_navigation.py`](https://github.com/tom-bjorkholm/wizard-ui-bridge/blob/master/wizard_ui_bridge/example/src/wizard_ui_example/e03_navigation.py):
  back, out one level and abort, with a nested level.
- [`run_e04_table_question.py`](https://github.com/tom-bjorkholm/wizard-ui-bridge/blob/master/wizard_tk_bridge/example/src/wizard_tk_example/run_e04_table_question.py)
  runs [`e04_table_question.py`](https://github.com/tom-bjorkholm/wizard-ui-bridge/blob/master/wizard_ui_bridge/example/src/wizard_ui_example/e04_table_question.py):
  a fixed-row table and a variable-row table.
- [`run_e05_ask_form.py`](https://github.com/tom-bjorkholm/wizard-ui-bridge/blob/master/wizard_tk_bridge/example/src/wizard_tk_example/run_e05_ask_form.py)
  runs [`e05_ask_form.py`](https://github.com/tom-bjorkholm/wizard-ui-bridge/blob/master/wizard_ui_bridge/example/src/wizard_ui_example/e05_ask_form.py):
  a whole form on one screen.
- [`run_e06_typed_form.py`](https://github.com/tom-bjorkholm/wizard-ui-bridge/blob/master/wizard_tk_bridge/example/src/wizard_tk_example/run_e06_typed_form.py)
  runs [`e06_typed_form.py`](https://github.com/tom-bjorkholm/wizard-ui-bridge/blob/master/wizard_ui_bridge/example/src/wizard_ui_example/e06_typed_form.py):
  the typed form fields (numbers, dates, times, durations) and prefills.

They exist for two reasons. The first is the point made above: the same wizard
really does run on another bridge, and here is the proof, running the very same
module. The second is practical — running one is the fastest way to *see* what
a question kind looks like in Tk before you write any code of your own.

[`e07_custom_bridge.py`](https://github.com/tom-bjorkholm/wizard-ui-bridge/blob/master/wizard_ui_bridge/example/src/wizard_ui_example/e07_custom_bridge.py)
has no runner here. It is the example that *implements* a bridge of its own, so
running its wizard through a different bridge would defeat its purpose. Read it
anyway: `WizardUiBridgeTk` is the same exercise carried through to a finished
bridge, and that example explains what a bridge must implement and what it may
inherit.

### Supporting files

- [`_shared_wizard.py`](https://github.com/tom-bjorkholm/wizard-ui-bridge/blob/master/wizard_tk_bridge/example/src/wizard_tk_example/_shared_wizard.py)
  the trivial three-question pizza wizard the three teaching examples share,
  so what differs between them is only the Tk plumbing.
- [`_tk_example.py`](https://github.com/tom-bjorkholm/wizard-ui-bridge/blob/master/wizard_tk_bridge/example/src/wizard_tk_example/_tk_example.py)
  the shared runner the `run_*` examples use: it builds a bridge, runs one
  wizard, shows the result and closes the bridge.
- [`__init__.py`](https://github.com/tom-bjorkholm/wizard-ui-bridge/blob/master/wizard_tk_bridge/example/src/wizard_tk_example/__init__.py)
  puts the sibling `wizard_ui_example` source directory on `sys.path` when
  these examples are run from a source checkout, which is what lets the `run_*`
  examples import the wizards they run.

## Running an example

The examples are not an installed package, so run them from this directory's
parent, which puts it on `sys.path`:

```sh
cd wizard_tk_bridge/example/src
python -m wizard_tk_example.e01_cli_wizard
python -m wizard_tk_example.run_e04_table_question
```

Every example opens a real window, so a working display is needed; there is no
`--ui` switch here, since a Tk bridge is the only bridge these examples use.

## `e01_cli_wizard.py`: the bridge owns the Tk application

The starting point: a program that is otherwise a plain command-line tool, with
no window of its own, that still wants to ask through a graphical wizard.

```python
bridge = WizardUiBridgeTk()          # no parent, no area
try:
    return ask_pizza_order(bridge)
finally:
    bridge.close()
```

**The hidden root.** Every Tkinter window needs exactly one `tk.Tk()` root
somewhere in the process, even when the program never shows it. With neither
`parent` nor `area`, the bridge creates that root, withdraws it, and builds the
only visible window over it. `close()` destroys the root again, so this program
contains no Tkinter code at all.

**No `mainloop()`.** Each ask method waits for its answer with Tk's own
`wait_variable`, which pumps the event loop just long enough to process the
wizard's events and returns as soon as the user answers. So the ask methods
behave like ordinary blocking calls — the wizard is written as straight-line
code — and the program is not left running an event loop after the wizard
closes.

## `e02_new_window.py`: a pop-up window over an application

Here the example *is* a small Tkinter application: a main window with a label,
a list of past orders, and a button that opens the wizard. There is already a
root and other widgets before the wizard is asked for, so the wizard has to
appear *over* the application rather than take it over.

```python
bridge = WizardUiBridgeTk(parent=self._root)
```

**`parent` means "a new window of your own, over this widget".** The bridge
builds a `Toplevel`, makes it transient for the parent's window so the window
manager keeps it above, and destroys it on `close()`.

**`modal` defaults to `True`,** so the pop-up grabs pointer and keyboard for
the whole application while it is open: the user finishes or cancels the wizard
before returning to the main window. That is usually right for a pop-up, and it
is the application's call rather than the wizard's, because only the
application knows whether its other content should stay usable.

The wizard runs inside a button callback, so its per-question `wait_variable`
nests inside the application's own `mainloop()`. Nothing special is needed for
that; it is the ordinary Tk way to run a modal dialog.

## `e03_embedded_area.py`: an area inside a window you built

This example's window is split in two: a left panel with the application's own
content, and a right frame that stays empty until a wizard runs in it. The
wizard never gets a window of its own — it is built directly into that frame.

```python
bridge = WizardUiBridgeTk(area=self._area, modal=False)
```

**`area` means "fill this container, do not open a window".** `close()` clears
the widgets the wizard put there and leaves the frame itself for the next time.

**`modal=False` is the point of embedding.** The default `True` would still
avoid a separate window, but it grabs the whole window containing the area,
which would make the left panel unusable while the wizard runs — and being able
to keep using the rest of the window is the reason to embed instead of popping
up. The example's left panel carries an unrelated button that keeps counting
clicks while the wizard runs, to make that visible.

## Choosing between the three

| Your application | Arguments | The bridge builds | Owns the root |
| ---------------- | --------- | ----------------- | ------------- |
| A CLI program with no Tkinter code (`e01`) | neither | a withdrawn root and its own window | yes |
| Has its own windows (`e02`) | `parent=widget` | a new `Toplevel` over `parent` | no |
| Has a place for the wizard (`e03`) | `area=container` | widgets inside `container` | no |

`parent` and `area` are mutually exclusive; giving both raises `ValueError`.
The visible part — the wizard's own window, or its widgets inside the area — is
built lazily on the first question, so a bridge that is never asked anything
puts nothing on the screen. (In the CLI case the hidden root is made at once,
but a withdrawn root is not shown either.)

## `close()` is not optional

Whichever of the three shapes is used, the bridge holds resources the
application must get back:

```python
bridge = WizardUiBridgeTk(parent=root)
try:
    ...                      # ask questions
finally:
    bridge.close()           # even when the user aborted
```

`close()` releases the modal grab, destroys the wizard's own window or clears
its area, and destroys the root when the bridge owns one. Reaching it through
`finally` matters more than usual here, because a wizard's normal ways of
ending are the `WizardNavigation` exceptions — an abort leaves through a
`raise`, not a `return`. Every example does this: `e01_cli_wizard.py` in its own
`run_cli_wizard()`, the two application examples through `run_pizza_order()` in
`_shared_wizard.py`, and the runners through `run_tk_example()` in
`_tk_example.py`. `close()` is idempotent, so calling it twice is harmless.

## What the user sees

One `WizardUiBridgeTk` shows every question of a session in the *same* reused
window or area, so a session does not jump around the display.

**Navigation.** Every question carries **Back**, **Out one level** and
**Abort** buttons, which raise `WizardBack`, `WizardCancelLevel` and
`WizardAbort` — the same three requests the console bridge spells `:b`, `:c`
and `:q`. Closing the wizard's window, or pressing Cmd-W (Ctrl-W on Windows),
is an abort. `run_e03_navigation.py` is the one to run to see them at work.

**Messages.** `show()` appends to a message area kept above the current
question, so earlier messages stay readable as the wizard moves on. They
disappear with the window when the bridge closes, which is why **a final
message needs a question after it** to be seen at all — exactly as on the
Textual bridge. `_tk_example.py` ends every runner with a short *Press Enter to
close* question for that reason.

**Diagnostics.** A GUI has no console to write side notes to, so `error_file()`
returns a stream that discards what is written to it. Pass
`WizardUiBridgeTk(log=stream)` to send those notes somewhere real, such as an
open log file.

**Widgets per question kind.** The Tk bridge overrides every ask method, the
inheritable ones included — above all `ask_path()` and `ask_form()`, where a
graphical interface beats the base class fallback outright:

| Ask method | What the user gets |
| ---------- | ------------------ |
| `ask_text` | a text entry, masked when `sensitive` |
| `ask_int` | a numeric entry, re-asked until the value parses and fits its bounds |
| `ask_path` | an entry with a **Browse** button opening the native file or directory picker |
| `ask_yes_no` | a **Yes** and a **No** button |
| `ask_choice` / `ask_multi` | a single- / multi-selection list |
| `ask_table` | an editable grid, with **Add row** and **Remove row** when the question allows a variable number of rows |
| `ask_form` | every field of the form on one screen, answered in any order |

In a form, `help_text` becomes a hover tooltip rather than an extra printed
line, the float, time and duration fields show their accepted format as greyed
placeholder text, and a date or date-time field adds a **Pick** button opening
a month calendar. `run_e06_typed_form.py` shows all of that at once.

Because `ask_form()` is overridden, `supports_form_field()` reports that all
current field types are shown, and `ask_form_w_fake()` therefore just calls
`ask_form()`. Compare with the plain console bridge, where the same form is
asked one field at a time — the wizard code is identical either way.

## Tests

The examples are covered by
[`test_examples.py`](https://github.com/tom-bjorkholm/wizard-ui-bridge/blob/master/wizard_tk_bridge/example/test/test_wizard_tk_example/test_examples.py).
The pizza wizard's logic is tested through a scripted fake bridge, and the two
application examples are tested by building their widgets on a withdrawn root,
so no test window ever reaches the screen. Tests that need a real focused
window live with the bridge's own tests and are run by hand with
`./run_focus_sensitive_tests.py`.
