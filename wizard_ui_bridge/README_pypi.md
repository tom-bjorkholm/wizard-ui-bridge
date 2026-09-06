# wizard-ui-bridge

`wizard-ui-bridge` is the user-interface-independent way for a wizard to
ask a user questions.

A wizard asks a series of questions and turns the answers into something,
often a configuration file. `WizardUiBridge` is the interface it asks
through, so the same wizard runs on a plain console, on a full-screen
[Textual](https://pypi.org/project/textual/) user interface, in a
graphical user interface (Tkinter through the companion package below,
or a toolkit you write a bridge for yourself), or on a scripted bridge
in your tests.

## Tk companion

`wizard-ui-bridge` has a companion
[wizard-tk-bridge](https://pypi.org/project/wizard-tk-bridge/) that
implements the same user-interface-independent way for a wizard to
ask a user questions using a Tkinter GUI.

## Is this package for you?

This package is a good fit when one or more of these apply:

- You have a wizard, or a program that asks a user a series of questions,
  and you do not want the questions to be tied to one user interface.
- You want typed questions, each with validation and re-asking: text,
  integer, path, yes/no, choice and multi-choice asked one at a time, and
  float, date, time, date and time and duration as fields of a form.
- You want to ask a whole form at once where the user interface can show
  one, and fall back to one question at a time where it cannot.
- You want the user to be able to go back a step or cancel, without every
  question having to handle that.
- You want a full-screen text user interface for free when the program
  runs in a terminal, and a plain console fallback when it does not.
- You want your wizard to be testable without a terminal.

This package is probably not the right one when:

- You want a general widget toolkit. Use
  [Textual](https://pypi.org/project/textual/) or a GUI toolkit directly.
- You only need one `input()` call.

## Installation

`wizard-ui-bridge` requires Python 3.12 or newer.

```sh
pip install --upgrade wizard-ui-bridge
```

Textual is optional. Install it with the extra when you want the
full-screen text user interface:

```sh
pip install --upgrade 'wizard-ui-bridge[textual]'
```

Without the extra, everything except the Textual bridge works, and
`make_text_ui_bridge()` returns the console bridge. Importing
`wizard_ui_bridge` never imports Textual; it is imported the first time a
Textual bridge is actually used. Asking for the Textual bridge without
Textual installed raises `ImportError` naming the extra to install.

## Quick start

Ask a small form, on the best user interface the terminal allows:

```python
import sys

from wizard_ui_bridge import AskTextField, AskIntField, AskYesNoField, \
    make_text_ui_bridge

bridge = make_text_ui_bridge(sys.stdout, sys.stdin, sys.stderr)
answers = bridge.ask_form('Describe the export', [
    AskTextField('Report name', 'Shown as the title of the report'),
    AskIntField('Rows', 'How many rows to export', min_value=1),
    AskYesNoField('Headings', 'Write a heading row', True)])
for answer in answers:
    print(f'{answer.asking.short_question}: {answer.value}')
```

The same code runs as a full-screen form when Textual is installed and
the program runs in a terminal, and as one console question at a time
when it does not.

Ask one question at a time instead:

```python
name = bridge.ask_text('Report name', default='report')
rows = bridge.ask_int('Rows', min_value=1)
```

## Main entry points

- `WizardUiBridge`
  The bridge a wizard asks through. Subclass it to connect a wizard to a
  user interface of your own; the base class turns the typed questions and
  whole-form questions into the few methods your subclass implements.

- `make_text_ui_bridge()` and `UiBridgeType`
  Return the Textual bridge when Textual is installed and both streams are
  a terminal, and the console bridge otherwise. `UiBridgeType` forces one
  or the other.

- `WizardUiBridgeConsole`
  Asks one question at a time on plain text streams.

- `WizardUiBridgeTextual`
  Full-screen text user interface, needs the `textual` extra.

- `AskTextField`, `AskIntField`, `AskFloatField`, `AskPathField`,
  `AskYesNoField`, `AskChoiceField`, `AskMultiChoiceField`,
  `AskDateField`, `AskTimeField`, `AskDateTimeField`, `AskDurationField`
  The typed fields a form is built from, each with a matching
  `Answer...Field`.

- `WizardBack`, `WizardAbort`, `WizardCancelLevel`, `WizardNavigation`
  How a user asks to go back a step or to give up, without every question
  having to handle it.

- `TableColumn`, `TableCell` and `ask_table()`
  Ask for a small table of values, with a fixed or variable number of rows.

- `textual_installed()` and `load_textual_bridge()`
  Ask whether the optional Textual bridge can be used, and get the class
  when it can.

### Writing your own bridge

A bridge of your own subclasses `WizardUiBridge` and implements the few
asking methods. The modules `wizard_ui_bridge.bridge_helpers` and
`wizard_ui_bridge.form_helpers` hold the helpers the bundled bridges use
to interpret raw answers and to build form answers, so that a bridge of
your own behaves the same way.

## History

The low-level `WizardUiBridge.ask()` method was **removed** in version
1.2, together with the fallbacks that let a bridge which only overrode
`ask()` keep working by rerouting the typed `ask_*()` calls through it.
Version 1.1 was the last version that supported it. A bridge implements
the typed methods directly: `ask_text()`, `ask_choice()`, `ask_multi()`,
`ask_yes_no()` and `ask_table()`, together with `show()`. A typed method
a bridge does not implement raises `NotImplementedError`. See *Writing
your own bridge* above.

### Relation to tableio-cfg-json

This package used to be part of
[tableio-cfg-json](https://pypi.org/project/tableio-cfg-json/). It was
split out so that a wizard that has nothing to do with TableIO does not
have to install TableIO and everything TableIO depends on.

### Source code repo history

The two git repos
[https://github.com/tom-bjorkholm/wizard-ui-bridge](https://github.com/tom-bjorkholm/wizard-ui-bridge)
and
[https://github.com/tom-bjorkholm/tableio_cfg_json](https://github.com/tom-bjorkholm/tableio_cfg_json)
share a common history. Up until version 1.1 there was only one repo.
Now that repo is split in two, and each repo holds only code for its
package. However, both repos have the common history.

## Documentation

- Teaching examples and walkthroughs: [wizard_ui_bridge/example/src/wizard_ui_example](https://github.com/tom-bjorkholm/wizard-ui-bridge/blob/master/wizard_ui_bridge/example/src/wizard_ui_example)

- Public API notes: [doc/wizard_ui_bridge_api.md](https://github.com/tom-bjorkholm/wizard-ui-bridge/blob/master/doc/wizard_ui_bridge_api.md)

- Protected/internal API notes: [doc/wizard_ui_bridge_protected_api.md](https://github.com/tom-bjorkholm/wizard-ui-bridge/blob/master/doc/wizard_ui_bridge_protected_api.md)

- Source repository: [wizard-ui-bridge](https://github.com/tom-bjorkholm/wizard-ui-bridge/)

## License

MIT

## Test summary

- Test result: 1084 passed, 9 deselected in 43s
- No flake8 warnings.
- No mypy errors found.
- No pylint warnings.
- No python layout warnings.
- Built version(s): 1.3.1
- Build and test using Python 3.14.7
