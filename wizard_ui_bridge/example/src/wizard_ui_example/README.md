# wizard-ui-bridge teaching examples

## Introduction

A *wizard* is any code that asks a user a series of questions. A
`WizardUiBridge` is the user-interface-independent object the wizard asks them
through, so one wizard can run on a plain console, on a full-screen Textual
interface, or on any other bridge an application supplies. (The
`tableio-cfg-json` package is one such application; these examples need nothing
from it.)

These examples are meant to be read in order by a fluent Python programmer who
is new to the API. Each one is self-contained: it asks some questions and
prints a summary, so nothing but the bridge itself is in the way. Each is also
fully scriptable — `make_text_ui_bridge()` shows a full-screen Textual form in
a real terminal (with the optional `wizard-ui-bridge[textual]` extra) and falls
back to the plain console bridge when input is redirected, which is what the
tests rely on.

Run any example as a module, optionally forcing a bridge with `--ui`:

```sh
python -m wizard_ui_example.e01_one_question
python -m wizard_ui_example.e02_question_kinds --ui console
```

## The examples, in reading order

- [`e01_one_question.py`](https://github.com/tom-bjorkholm/wizard-ui-bridge/blob/master/wizard_ui_bridge/example/src/wizard_ui_example/e01_one_question.py)
  obtains a bridge and asks a few free-text questions.
- [`e02_question_kinds.py`](https://github.com/tom-bjorkholm/wizard-ui-bridge/blob/master/wizard_ui_bridge/example/src/wizard_ui_example/e02_question_kinds.py)
  uses each one-at-a-time ask method once to gather export settings.
- [`e03_navigation.py`](https://github.com/tom-bjorkholm/wizard-ui-bridge/blob/master/wizard_ui_bridge/example/src/wizard_ui_example/e03_navigation.py)
  lets the user step back, cancel a nested section or abort the wizard.
- [`e04_table_question.py`](https://github.com/tom-bjorkholm/wizard-ui-bridge/blob/master/wizard_ui_bridge/example/src/wizard_ui_example/e04_table_question.py)
  edits a fixed-row table and then a variable-row table.
- [`e05_ask_form.py`](https://github.com/tom-bjorkholm/wizard-ui-bridge/blob/master/wizard_ui_bridge/example/src/wizard_ui_example/e05_ask_form.py)
  asks the same kind of export settings as one whole form.
- [`e06_typed_form.py`](https://github.com/tom-bjorkholm/wizard-ui-bridge/blob/master/wizard_ui_bridge/example/src/wizard_ui_example/e06_typed_form.py)
  adds the typed form fields (numbers, dates, times, durations) and prefills.
- [`e07_custom_bridge.py`](https://github.com/tom-bjorkholm/wizard-ui-bridge/blob/master/wizard_ui_bridge/example/src/wizard_ui_example/e07_custom_bridge.py)
  implements a bridge of your own for an unusual device and runs an earlier
  wizard through it.
- [`e08_matrix_form.py`](https://github.com/tom-bjorkholm/wizard-ui-bridge/blob/master/wizard_ui_bridge/example/src/wizard_ui_example/e08_matrix_form.py)
  asks a fixed timesheet as one matrix form: a grid of label and input cells.
- [`e09_resizable_matrix.py`](https://github.com/tom-bjorkholm/wizard-ui-bridge/blob/master/wizard_ui_bridge/example/src/wizard_ui_example/e09_resizable_matrix.py)
  asks a contractor list as a matrix the user can resize, with live
  validation, a final check and re-asking.

All the examples except `e07` *use* a bridge this package provides; `e07` is
the one that *implements* one. `e08` and `e09` come after it only because the
matrix form was added later; they do not depend on `e07`, so read them after
`e06` if you prefer.

## The same wizards on a graphical bridge

Every wizard here is bridge-independent, so the same modules also run on a
graphical bridge without a line changed. The companion package
`wizard-tk-bridge` is a Tkinter bridge, and its
[teaching examples](https://github.com/tom-bjorkholm/wizard-ui-bridge/blob/master/wizard_tk_bridge/example/src/wizard_tk_example/README.md)
show how to place a wizard in a command-line program, in a pop-up window, or
in an area of a window the application already built. Its `run_e01` to
`run_e06`, `run_e08` and `run_e09` examples import the matching examples from
this folder and run those very modules through Tk, which is the easiest way to
see what these questions look like in a real graphical interface.

## `e01_one_question.py`: obtaining a bridge and asking

The smallest useful program that talks to a user through the bridge.

**Getting a bridge.** `make_text_ui_bridge(out, in_, err, kind)` returns a
ready-to-use text-mode bridge. `UiBridgeType.AUTO` builds the Textual
full-screen bridge when Textual is installed and the streams are a real
terminal, and the plain console bridge otherwise; `textual_installed()` reports
whether the optional extra is available, which is exactly what `AUTO` checks
first. `UiBridgeType.CONSOLE` and `UiBridgeType.TEXTUAL` force one bridge.

**Asking one question.** `ask_text()` asks for one line of free text. Three of
its options appear here:

- `default` — an empty answer returns the default instead of an empty string.
- `nullable` — an empty answer with no default returns `None`, so "left blank"
  is distinguishable from a real value.
- `sensitive` — the bridge must not echo the text (a password field, or
  `getpass` on a real console). No default may be combined with it.

**Showing output and side notes.** `show()` presents a message to the user. On
the console it prints at once, but on a graphical or full-screen textual bridge
`show()` only *buffers* the message for the next question's screen — a message
with no following question is never seen. So the example ends with a short
acknowledgement question, which keeps the greeting on screen until the user has
read it (a GUI such as Tkinter needs the same). `error_file()` returns the
stream for side notes and diagnostics, kept apart from the primary output; on
the console bridge it is standard error. The example writes a note there when
the optional nickname is left blank.

**Cancelling.** Any ask method may raise a `WizardNavigation` request instead of
returning, when the user asks to go back, cancel or abort (`:b`, `:c` or `:q` on
the console; `:?` instead shows the help text of the question, if any, and asks
it again). A single question has nowhere to go back to, so the example treats
any such request as "the user gave up".

```sh
python -m wizard_ui_example.e01_one_question
python -m wizard_ui_example.e01_one_question --ui console
```

## `e02_question_kinds.py`: the kinds of question

This example uses each of the one-at-a-time ask methods exactly once to gather a
small "export settings" configuration:

| Ask method | Question kind | Answer type |
| ---------- | ------------- | ----------- |
| `ask_text` | free text (the report title) | `str` |
| `ask_choice` | pick one of a fixed list (the format) | `str` |
| `ask_path` | a file or directory path (the output file) | `Path` |
| `ask_int` | an integer, optionally bounded/nullable (a row limit) | `int` or `None` |
| `ask_yes_no` | a boolean (write a header row?) | `bool` |
| `ask_multi` | pick several of a fixed list (which columns) | `list[str]` |

**The ask methods validate for you.** Each method already re-asks on input it
can judge on its own: `ask_int` rejects non-integers and out-of-range values,
`ask_choice` and `ask_multi` reject unknown items, and `ask_path` rejects a path
of the wrong kind. The program does not loop for those.

**`re_ask_reason`: application-level checks.** Some rules only the application
knows. Here the output file should end with the extension matching the chosen
format, which `ask_path()` cannot know. So the example checks it and, when it
fails, calls `ask_path()` again with a `re_ask_reason` that explains why.
`re_ask_reason` is the shared argument every ask method takes for exactly this.

**`help_text`: help on request.** Every ask method also takes a keyword-only
`help_text`. The console bridge does not print it up front: the user answers
`:?` to see it, and the same question is then asked again. Here the output-file
question carries a help text that explains the extension rule. The form fields
of `e05_ask_form.py` carry a help text in the same way.

The same export settings appear again in `e05_ask_form.py` as one whole form.
Reading `e02` then `e05` is the intended way to see the difference between asking
questions one at a time and asking them all at once.

```sh
python -m wizard_ui_example.e02_question_kinds
python -m wizard_ui_example.e02_question_kinds --ui console
```

## `e03_navigation.py`: letting the user move around

The wizards above only move forward. A real wizard also lets the user change
their mind. Any ask method may raise a `WizardNavigation` subclass instead of
returning, and the wizard author writes the control flow that reacts to it.
`e03_navigation.py` is a small account-setup wizard (username → email →
account type → password) where choosing the *Organization* account type opens
a **nested level** of organization questions. That nested level is what makes
the difference between the two "go somewhere" requests visible:

| Request | Console token | Meaning |
| ------- | ------------- | ------- |
| `WizardBack` | `:b` | Step to the previous question. At the first question of a level there is no earlier question, so it is left to the enclosing level. |
| `WizardCancelLevel` | `:c` | Leave the whole current level and return to the question that opened it, however deep in the level the user is. Here it leaves the organization section and re-asks the account type. The level's answers are not thrown away: they are kept and offered as defaults if it is re-entered, unless a changed outer answer has made them invalid. |
| `WizardAbort` | `:q` | Abandon the whole wizard. |

**The driver pattern.** `drive_level()` is the small reusable driver written
around the ask methods. It walks a list of step functions, stepping back on
`WizardBack`. The nested organization level runs the *same* driver; being an
inner level it re-raises a `WizardBack` from its first question and any
`WizardCancelLevel`, so the driver that opened it (`ask_account_details()`)
can re-ask the opening question. `WizardAbort` is never caught by a level, so
it propagates out and `run_account_setup()` stops.

**Answers become the new default.** Whenever the user returns to a question —
by stepping back, or by re-entering a level they cancelled out of — the
answer given earlier is offered as its default, so pressing enter keeps it.
The example keeps every answer in a draft object (including a nested
`OrgDraft` for the organization level) and passes the stored value back as
the ask method's `default`. The password is the one exception: a sensitive
question cannot carry a default, so it is entered again on return.

The console tokens (`:b`, `:c`, `:q`) make the whole flow scriptable, which is
how the tests drive back, cancel and abort. The console also accepts `:?`, which
is no navigation request: it shows the help text of the question and asks the
question again.

```sh
python -m wizard_ui_example.e03_navigation
python -m wizard_ui_example.e03_navigation --ui console
```

## `e04_table_question.py`: editing a table

`WizardUiBridge.ask_table()` asks the user to fill in a table. A table
question is described by one `TableColumn` per column (its header and whether
the whole column is read-only) and a grid of `TableCell` objects giving each
starting cell's value and its constraints (an optional finite set of
`choices`, and whether an empty cell is allowed). `ask_table()` returns the
whole table as rows of strings — or `None` for an empty cell — including the
read-only columns. `e04_table_question.py` asks two table questions:

- a **fixed-row** table for renaming a known set of columns: a read-only
  *source column*, a free-text *rename to* column, and a per-row *data type*
  choice cell (showing that each `TableCell` can carry its own choices);
- a **variable-row** guest list, where the user adds rows (`:+` on the
  console, an Add-row button in a graphical bridge) and removes them
  (`:- N` on the console) within a minimum and maximum row count.

**Early feedback vs final verification.** The variable table passes a
`PartialCheck`. It is *intended* as advisory early feedback: a graphical or
Textual bridge shows the message beside the cell as the user types, without
blocking, so the answer is guided rather than forced. A console has nowhere to
show such an unobtrusive inline hint, so the console bridge instead re-asks
the cell until the check passes (an optional-to-heed prompt reads badly on a
console). Because a bridge might handle — or even skip — the check in different
ways, **a wizard must not trust the bridge to enforce it.** After `ask_table()`
returns, `ask_guest_list()` verifies the whole table itself and, when
something is wrong, calls `ask_table()` again with a `re_ask_reason` and the
user's current rows, so nothing is retyped. The final pass also enforces a
rule a per-cell check cannot see — that the guest names are unique.

Editing a table also honors the navigation requests from `e03_navigation.py`;
this example simply treats any request that propagates out of a table as
"cancelled".

```sh
python -m wizard_ui_example.e04_table_question
python -m wizard_ui_example.e04_table_question --ui console
```

## `e05_ask_form.py`: asking a whole form at once

The wizards above ask one question at a time. That is natural on a plain
console, but a graphical or full-screen textual interface can do better: it can
show several related questions together, so the user sees the whole picture and
fills the fields in any order before submitting. `WizardUiBridge.ask_form()` is
the bridge method for that. `e05_ask_form.py` asks one export-settings form with
`ask_form()` and prints a summary; it reads or writes nothing, so it isolates
the `ask_form()` API. In a real terminal the whole form appears on one screen;
on the console the same program asks each field in turn.

### How to use `ask_form()`

Describe the form as a list of `Ask*Field` objects, one per row. The Python type
of each object tells the bridge which input widget to show, so there is one
class per kind of question:

| Field class | Question kind | Typical widget |
| ----------- | ------------- | -------------- |
| `AskTextField` | free text | text input |
| `AskIntField` | integer, optionally bounded/nullable | numeric input |
| `AskPathField` | file or directory path | text input plus a picker |
| `AskYesNoField` | boolean | check box or toggle |
| `AskChoiceField` | pick one of a fixed list | drop-down or radio buttons |
| `AskMultiChoiceField` | pick several of a fixed list | check-box list |

Every field carries a `short_question` (the label) and an optional `help_text`
(a tooltip in a graphical or textual bridge; the console prints it before the
field and shows it again when the user answers `:?`). A path field is configured with
`PathAskOptions`, whose `WizardPathKind` says whether the path must exist and
whether it must be a file or a directory:

```python
AskPathField(short_question='Output file',
             help_text='Where the report will be written.',
             path_options=PathAskOptions(kind=WizardPathKind.NON_EXISTING_FILE))
```

Call `ask_form()` with the main instruction and the fields, and read back one
`Answer*Field` per field, in the same order:

```python
answers = bridge.ask_form(long_question, ask_fields,
                          re_ask_reason=reason,
                          partial_validator=export_validator)
title = answers[0].value        # each Answer*Field.value holds the typed answer
```

The optional `partial_validator` gives early feedback. It receives the current
answers and the index of the field that changed, and returns a
`PartFormValidationResult(is_valid, message, disable_row_idxs)`:

- `disable_row_idxs` lists rows that are irrelevant given the current answers,
  for example the CSV delimiter when the chosen format is not CSV. Disabling a
  row never blocks submitting the form.
- `is_valid` and `message` report a real problem the user must fix. A graphical
  or textual bridge refuses to submit while `is_valid` is `False`, so an
  informational note should leave `is_valid` `True` and only genuine errors
  should set it `False`.

The base `ask_form()` is a permanent console implementation: it simply asks each
field with the ordinary typed ask methods, so a program keeps working when
output is redirected or under tests. A graphical, textual, curses or web bridge
overrides `ask_form()` to show the whole form on one screen; the Textual bridge
in this package already does. Because the console fallback treats validator
messages as advisory, a caller that must reject a bad final value re-calls
`ask_form()` with a `re_ask_reason`, which `e05_ask_form.py` demonstrates.

```sh
python -m wizard_ui_example.e05_ask_form
python -m wizard_ui_example.e05_ask_form --ui console
```

## `e06_typed_form.py`: typed form fields and prefills

On top of the six fields above, `ask_form()` supports five *typed* fields whose
answer is a real Python object, so a graphical or textual bridge can offer a
better editor and no string parsing leaks into the application:

| Field class | Answer type | Accepted text / widget |
| ----------- | ----------- | ---------------------- |
| `AskFloatField` | `float` | a number, optionally bounded |
| `AskDateField` | `date` | `YYYY-MM-DD`; the Textual bridge opens a calendar |
| `AskTimeField` | `time` | `HH:MM` or `HH:MM:SS` |
| `AskDateTimeField` | `datetime` | `YYYY-MM-DD HH:MM:SS`; calendar for the date part |
| `AskDurationField` | `timedelta` | `<days> d HH:MM:SS`, or a number of seconds |

Each typed field takes the same `short_question`, `help_text`, `nullable` and
`default` as the other fields, and the date-like and numeric fields also take
inclusive `min_value` and `max_value` bounds. `e06_typed_form.py` asks a small
event-scheduling form that uses every typed field. On the plain console bridge
each field is still asked as text and parsed, so the same program stays
scriptable even though it shows a calendar in a real terminal.

### Prefilling a field from others

`PartFormValidationResult` has a fourth part, `prefill_values`: a tuple of
`(row_index, value)` pairs the validator asks the bridge to place into other
rows, exactly as if the user had typed them. `e06_typed_form.py` uses it to fill
the "Ends at" date-time from the event date, the start time and the duration
whenever any of those change:

```python
def schedule_validator(answers, changed):
    disable = () if not _is_free(answers) else (_PRICE,)   # hide an irrelevant row
    end = _computed_end(answers)                            # date + time + duration
    prefill = () if end is None else ((_END, end),)         # offer it in "Ends at"
    return PartFormValidationResult(True, '', disable, prefill)
```

The prefilled value is only a starting point the user may edit. A prefill aimed
at the row that just changed is ignored, so writing back never fights the user's
own edit, and emitting a stable value (the same computed end) does not loop. The
value must match the target field's answer type: a `date` for a date field, a
`datetime` for a date-time field, a `float` for a float field, and so on.

### Working with older bridges: `ask_form_w_fake()`

A bridge that overrides `ask_form()` but predates the typed fields reports
through `supports_form_field()` that it cannot show them. A wizard that wants the
typed fields anyway can call `bridge.ask_form_w_fake(...)` instead of
`ask_form()`: each unsupported field is shown as a text field with the format in
its help text, a wrapping validator guides the entry and converts it, and the
answers come back as the requested typed answers. On a bridge that already
supports the typed fields — the console and Textual bridges here both do —
`ask_form_w_fake()` simply calls `ask_form()`.

```sh
python -m wizard_ui_example.e06_typed_form
python -m wizard_ui_example.e06_typed_form --ui console
```

## `e07_custom_bridge.py`: implementing a bridge of your own

Every example so far *used* a bridge; this one *is* a bridge, written from
scratch, so you can see exactly what teaching the wizard a new user interface
takes. To keep the lesson honest it drives an *earlier* wizard through the new
bridge: it imports `ask_export_settings` and `summarize` from
`e02_question_kinds.py` and runs that unchanged code. A bridge works with any
wizard, and a wizard runs on any bridge.

### The device: an uppercase-only teleprinter

Imagine driving a classic uppercase-only teleprinter, such as a Teletype
Model 33. It prints capital letters `A-Z`, the digits `0-9` and a handful of
punctuation marks (`. , : - ( ) [ ] ?`) and nothing else — no lowercase, no
Unicode. Sending any other glyph does not just look wrong, it jams the
machine. The console bridge writes whatever text it is given straight to the
stream, so the first lowercase letter or slash would jam this device. That is
the whole reason for a new bridge: its one distinctive job is to **fold** every
line it prints into the device's glyph set — letters to uppercase, everything
unsupported to a `?`. On this bridge the export summary comes out as
`REPORT TITLE: CITIES REPORT` and a path prints as `?TMP?REPORT.CSV`; on the
built-in bridges the same wizard prints normally.

### Correctness first: the base class does most of the work

A `WizardUiBridge` is designed so a new bridge is **correct from day one and
improved incrementally**. Only a few methods have no default and must be
written; the rest are inherited and already work:

| Must implement (no default) | Inherited (permanent base fallback) |
| --------------------------- | ----------------------------------- |
| `ask_text`, `ask_yes_no`, `ask_choice`, `ask_multi`, `show` | `ask_path` (asks text, validates), `ask_int` (asks text, re-asks in range), `ask_form` (asks each field one at a time), `ask_matrix_form` (asks each cell one at a time, with a resize menu), `ask_table` (asks the table as a matrix form), `error_file` |

So the moment the mandatory methods work, the bridge can already run any of
the earlier wizards — path questions, whole forms and tables included —
because the base class fills the gaps. This example proves it: the export
wizard's path question rides the inherited `ask_path`, and the mandatory
methods stay a few lines each by delegating to the public helpers in
`wizard_ui_bridge.bridge_helpers` (`ask_one`, `ask_many`, `ask_yes_no`),
exactly as the built-in console bridge does.

Tables are covered too. When a table question gives both `min_rows` and
`max_rows`, the wizard is asking for a *variable* number of rows, which the
user can only supply if the bridge lets them add and remove rows — a matter of
correctness, not polish, since a wizard that expects the user to extend a
table (a translation table, say) has no way to receive those rows otherwise.
The inherited `ask_table()` describes the table as a matrix form, which may
grow and shrink by whole rows, and asks it with `ask_matrix_form()`, so this
bridge needs no table code of its own. `WizardUiBridgeConsole`,
`WizardUiBridgeTextual` and the `WizardUiBridgeTk` of the companion package
`wizard-tk-bridge` override `ask_table()` with table editors of their own — a
user experience rung, not a correctness requirement.

### Help on request

Every ask method takes a keyword-only `help_text`. The wizard passes the help
text of a question there, and the base `ask_form` and `ask_matrix_form` pass
the help text of each field or cell. The teleprinter bridge
offers it on request, like the console bridge: the answer `:?` prints the help
text and asks the same question again, so the wizard never sees the request.
Try it on the output-file question, which carries a help text in `e02`. A
bridge written before `help_text` existed still works, but the base class then
leaves the help text out and issues a `DeprecationWarning`.

### User experience second: the "override to improve" move

Those mandatory methods are the **floor for correctness, not the target**. A
real bridge should override every method whose user experience its environment
can improve. To show the move concretely the example overrides exactly one
convenience method, `ask_int`: the inherited `ask_int` asks bare and explains
the allowed range only *after* a rejected value, which reads badly on a
teleprinter where that reason scrolls away. The override states the range up
front (`ROW LIMIT (BLANK ? ALL ROWS) (AT LEAST 1)`) and then delegates the
re-ask loop to `super().ask_int()` — better UX, no logic rewritten.

### The UX ladder: what a real bridge should climb next

The example stops at the floor plus one rung so the code stays readable. A
production bridge should keep climbing. Each rung names the capability it
exploits and a finished bridge that already shows how: `WizardUiBridgeConsole`
and `WizardUiBridgeTextual` are two reference rungs, and the
`WizardUiBridgeTk` of the companion package `wizard-tk-bridge` is a graphical
bridge that has climbed all six:

1. Whole-screen `ask_form()` and `ask_matrix_form()` — show every field or
   cell at once instead of one at a time, and with the inherited
   `ask_table()` a whole table too (Textual and Tk bridges).
2. A native `ask_path()` picker — a file/directory dialog instead of typed
   text (Tk bridge).
3. A calendar for date fields (Textual and Tk bridges).
4. Richer typed-field widgets (spin boxes, sliders) for float/time/duration.
5. `help_text` as a tooltip rather than an extra printed line (Textual and Tk
   bridges).
6. Inline re-ask — a rejected value's reason beside the field, not scrolled
   into the transcript.

The helper modules `wizard_ui_bridge.bridge_helpers` and
`wizard_ui_bridge.form_helpers` exist to make climbing this ladder cheaper:
they interpret raw answers, fill a table one cell at a time, and validate form
prefills exactly as the built-in bridges do.

`--ui` selects the bridge, and the very same wizard runs on all three, so you
can watch the folding appear only on the custom bridge:

```sh
python -m wizard_ui_example.e07_custom_bridge
python -m wizard_ui_example.e07_custom_bridge --ui console
python -m wizard_ui_example.e07_custom_bridge --ui textual
```

## `e08_matrix_form.py`: asking a matrix form

A form asks one value per row. Some questions are naturally a *grid*: hours per
person and weekday, or one row of facts per contractor. `ask_matrix_form()` asks
such a grid on one screen. `e08_matrix_form.py` asks a small team timesheet:
one row per team member and one column per weekday.

```text
         | Mon | Tue | Wed | Thu | Fri
  Alice  |  8  |  8  |  8  |  8  |  8
  Bob    |  8  |  8  |  8  |  8  |  8
  Cleo   |  8  |  8  |  8  |  8  |  8
```

### How to use `ask_matrix_form()`

Everything the bridge needs is one `MatrixRequest`:

- `long_question`: the instruction shown above the grid;
- `ask_cells`: one `Ask*Cell` per cell, as a list of rows;
- `dimensions`: a `MatrixDimensions` of minimum, maximum and default shape;
  `MatrixDimensions.fixed(rows, columns)` gives a shape the user cannot change;
- `console_question`: how a console, which cannot show a grid, asks the cells
  one at a time, and which labels it shows with each cell;
- optionally `partial_validator` and `cell_namer`, shown in `e09`.

The cells are the matrix counterparts of the form fields: `AskTextCell`,
`AskIntCell`, `AskDateCell` and so on, with the same attributes except that a
cell has no `short_question`. An `AskLabelCell` is plain text with no input,
typically a row or column header, but it may be placed anywhere. The header
labels of `e08` ask to be shown in bold with `AskLabelCell('Mon', bold=True)`;
`bold` and `italic` are hints that a bridge which cannot show them ignores.
Every cell also takes an optional `width` hint, in characters.

The answers come back in the shape of the matrix: one list per row, holding the
`Answer*Cell` for each input cell and `None` for each label cell:

```python
answers = bridge.ask_matrix_form(build_request())
for row in answers[1:]:                 # row 0 is the header
    hours = [cell.value for cell in row[1:]]
```

### Which bridges show a matrix

A graphical bridge shows the whole grid at once; run `run_e08_matrix_form.py`
from the
[Tk examples](https://github.com/tom-bjorkholm/wizard-ui-bridge/blob/master/wizard_tk_bridge/example/src/wizard_tk_example/README.md)
to see it. The console bridge cannot show a grid, so it uses the base
implementation of `ask_matrix_form()`, which asks one input cell at a time,
named by its labels as in `Alice / Mon`. The `console_question` of the request
chooses the order (row by row or column by column), which labels name a cell,
and whether the help text of each cell is shown. The Textual bridge uses the
same base implementation until it gets a grid of its own.

```sh
python -m wizard_ui_example.e08_matrix_form
python -m wizard_ui_example.e08_matrix_form --ui console
```

## `e09_resizable_matrix.py`: a resizable, validated matrix

`e09_resizable_matrix.py` builds on `e08` with what a real application usually
needs: a contractor list with one row per contractor and the columns name,
start date, end date and one to three contract files.

**A matrix the user resizes.** When the minimum and maximum of `dimensions`
differ, the user may append or delete the *last* row or column within those
bounds; a graphical bridge offers buttons for that. The normal way to describe
the cells is a grid of the *maximum* size: the matrix first shows the part
within the default shape, and an appended row or column shows the cells already
given at its position. That is how a re-asked matrix keeps the user's values as
defaults in every row. (A smaller grid repeats its last row and last cell, and
`ask_cells` may also be a function from `CellPosition` to `AskCell`.)

**Validation in two layers.** As in `e04` and `e05`, a `partial_validator` gives
live feedback while the matrix is edited and blocks submitting it while a start
date is not before its end date. It gets the current answers and the
`CellPosition` that changed, or `None` when nothing has changed yet or the
shape changed. Its `PartMatrixValidationRes` can also disable irrelevant cells
and prefill others, as in `e06`. The wizard must not trust a bridge to enforce
anything, so after `ask_matrix_form()` returns the whole matrix is checked again
and, on a problem, asked again with a `re_ask_reason`.

**Naming a cell.** A bridge also checks each cell on its own, for instance that
2027-14-32 is not a date, and names the cell in its message. By default the
name comes from the nearest labels, here the header above the cell and the row
number, as in `Row 3 / Start date`. A `cell_namer` names the cell from the
current answers instead:

```python
def contractor_cell_name(answers, position):
    name = answers[position.row][_NAME]          # the contractor's name cell
    who = f'Contractor {position.row - _HEADER_ROWS + 1}'
    if isinstance(name, AnswerTextCell) and name.value:
        who = name.value
    return f'{who}, {_HEADER_TEXTS[position.column].lower()}'
```

so the message reads `Alice, start date: ...`. With
`MatrixConsoleQuestion(..., use_cell_namer=True)` a console also uses the name
in the question of each cell, so `e09` asks `Alice, start date` on the
console. Run `run_e09_resizable_matrix.py` from the Tk examples to see the grid.

**Resizing on a console.** A console cannot show resize buttons, so it offers
menus instead. After the first contractor row it would ask whether to append or
delete a contract file column, so the width is set before the other rows are
asked (`e09` starts with a single contractor, so this menu is folded into the
next one). After the last cell it asks whether to append or delete a
contractor row or a contract file column, or be done. An appended row or column
asks its new cells at once, and an empty answer to a menu goes on.

```sh
python -m wizard_ui_example.e09_resizable_matrix
python -m wizard_ui_example.e09_resizable_matrix --ui console
```
