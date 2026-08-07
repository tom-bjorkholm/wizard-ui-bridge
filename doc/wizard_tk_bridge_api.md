# Table of Contents

* [wizard\_tk\_bridge.auto\_scroll](#wizard_tk_bridge.auto_scroll)
  * [auto\_hide](#wizard_tk_bridge.auto_scroll.auto_hide)
* [wizard\_tk\_bridge.\_no\_text\_io](#wizard_tk_bridge._no_text_io)
  * [NoTextIO](#wizard_tk_bridge._no_text_io.NoTextIO)
    * [write](#wizard_tk_bridge._no_text_io.NoTextIO.write)
    * [writelines](#wizard_tk_bridge._no_text_io.NoTextIO.writelines)
    * [flush](#wizard_tk_bridge._no_text_io.NoTextIO.flush)
    * [close](#wizard_tk_bridge._no_text_io.NoTextIO.close)
    * [seek](#wizard_tk_bridge._no_text_io.NoTextIO.seek)
    * [tell](#wizard_tk_bridge._no_text_io.NoTextIO.tell)
    * [truncate](#wizard_tk_bridge._no_text_io.NoTextIO.truncate)
* [wizard\_tk\_bridge.gui\_style](#wizard_tk_bridge.gui_style)
  * [style\_input](#wizard_tk_bridge.gui_style.style_input)
  * [focus\_first\_input](#wizard_tk_bridge.gui_style.focus_first_input)
* [wizard\_tk\_bridge.wizard\_typed](#wizard_tk_bridge.wizard_typed)
  * [parse\_float](#wizard_tk_bridge.wizard_typed.parse_float)
  * [parse\_date](#wizard_tk_bridge.wizard_typed.parse_date)
  * [parse\_time](#wizard_tk_bridge.wizard_typed.parse_time)
  * [parse\_datetime](#wizard_tk_bridge.wizard_typed.parse_datetime)
  * [parse\_duration](#wizard_tk_bridge.wizard_typed.parse_duration)
  * [format\_duration](#wizard_tk_bridge.wizard_typed.format_duration)
  * [format\_value](#wizard_tk_bridge.wizard_typed.format_value)
  * [ordered\_range\_error](#wizard_tk_bridge.wizard_typed.ordered_range_error)
  * [is\_typed](#wizard_tk_bridge.wizard_typed.is_typed)
  * [field\_hint](#wizard_tk_bridge.wizard_typed.field_hint)
  * [default\_text](#wizard_tk_bridge.wizard_typed.default_text)
  * [typed\_value](#wizard_tk_bridge.wizard_typed.typed_value)
  * [typed\_error](#wizard_tk_bridge.wizard_typed.typed_error)
  * [typed\_answer](#wizard_tk_bridge.wizard_typed.typed_answer)
  * [date\_of](#wizard_tk_bridge.wizard_typed.date_of)
  * [calendar\_seed](#wizard_tk_bridge.wizard_typed.calendar_seed)
  * [combined\_text](#wizard_tk_bridge.wizard_typed.combined_text)
* [wizard\_tk\_bridge.wizard\_pick\_row](#wizard_tk_bridge.wizard_pick_row)
  * [TypedInput](#wizard_tk_bridge.wizard_pick_row.TypedInput)
    * [text](#wizard_tk_bridge.wizard_pick_row.TypedInput.text)
    * [set\_text](#wizard_tk_bridge.wizard_pick_row.TypedInput.set_text)
    * [set\_enabled](#wizard_tk_bridge.wizard_pick_row.TypedInput.set_enabled)
  * [HintEntry](#wizard_tk_bridge.wizard_pick_row.HintEntry)
    * [\_\_init\_\_](#wizard_tk_bridge.wizard_pick_row.HintEntry.__init__)
    * [text](#wizard_tk_bridge.wizard_pick_row.HintEntry.text)
    * [set\_text](#wizard_tk_bridge.wizard_pick_row.HintEntry.set_text)
    * [set\_enabled](#wizard_tk_bridge.wizard_pick_row.HintEntry.set_enabled)
  * [PickRow](#wizard_tk_bridge.wizard_pick_row.PickRow)
    * [\_\_init\_\_](#wizard_tk_bridge.wizard_pick_row.PickRow.__init__)
    * [text](#wizard_tk_bridge.wizard_pick_row.PickRow.text)
    * [set\_text](#wizard_tk_bridge.wizard_pick_row.PickRow.set_text)
    * [set\_enabled](#wizard_tk_bridge.wizard_pick_row.PickRow.set_enabled)
* [wizard\_tk\_bridge.wizard\_calendar](#wizard_tk_bridge.wizard_calendar)
  * [month\_weeks](#wizard_tk_bridge.wizard_calendar.month_weeks)
  * [shift\_month](#wizard_tk_bridge.wizard_calendar.shift_month)
  * [day\_out\_of\_range](#wizard_tk_bridge.wizard_calendar.day_out_of_range)
  * [CalendarPicker](#wizard_tk_bridge.wizard_calendar.CalendarPicker)
    * [\_\_init\_\_](#wizard_tk_bridge.wizard_calendar.CalendarPicker.__init__)
* [wizard\_tk\_bridge.close\_binding](#wizard_tk_bridge.close_binding)
  * [bind\_close](#wizard_tk_bridge.close_binding.bind_close)
* [wizard\_tk\_bridge.wizard\_table](#wizard_tk_bridge.wizard_table)
  * [Cell](#wizard_tk_bridge.wizard_table.Cell)
  * [TableEditor](#wizard_tk_bridge.wizard_table.TableEditor)
    * [\_\_init\_\_](#wizard_tk_bridge.wizard_table.TableEditor.__init__)
    * [is\_variable](#wizard_tk_bridge.wizard_table.TableEditor.is_variable)
    * [values](#wizard_tk_bridge.wizard_table.TableEditor.values)
    * [add\_row](#wizard_tk_bridge.wizard_table.TableEditor.add_row)
    * [remove\_row](#wizard_tk_bridge.wizard_table.TableEditor.remove_row)
* [wizard\_tk\_bridge.wizard\_form](#wizard_tk_bridge.wizard_form)
  * [handles\_field](#wizard_tk_bridge.wizard_form.handles_field)
  * [int\_answer](#wizard_tk_bridge.wizard_form.int_answer)
  * [HelpTooltip](#wizard_tk_bridge.wizard_form.HelpTooltip)
    * [\_\_init\_\_](#wizard_tk_bridge.wizard_form.HelpTooltip.__init__)
    * [show](#wizard_tk_bridge.wizard_form.HelpTooltip.show)
    * [hide](#wizard_tk_bridge.wizard_form.HelpTooltip.hide)
  * [FormRow](#wizard_tk_bridge.wizard_form.FormRow)
  * [FormEditor](#wizard_tk_bridge.wizard_form.FormEditor)
    * [\_\_init\_\_](#wizard_tk_bridge.wizard_form.FormEditor.__init__)
    * [answers](#wizard_tk_bridge.wizard_form.FormEditor.answers)
    * [submit](#wizard_tk_bridge.wizard_form.FormEditor.submit)
* [wizard\_tk\_bridge.tk\_bridge](#wizard_tk_bridge.tk_bridge)
  * [WizardUiBridgeTk](#wizard_tk_bridge.tk_bridge.WizardUiBridgeTk)
    * [\_\_init\_\_](#wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.__init__)
    * [ask\_text](#wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.ask_text)
    * [ask\_int](#wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.ask_int)
    * [ask\_path](#wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.ask_path)
    * [ask\_yes\_no](#wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.ask_yes_no)
    * [ask\_choice](#wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.ask_choice)
    * [ask\_multi](#wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.ask_multi)
    * [ask\_table](#wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.ask_table)
    * [ask\_form](#wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.ask_form)
    * [supports\_form\_field](#wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.supports_form_field)
    * [show](#wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.show)
    * [error\_file](#wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.error_file)
    * [close](#wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.close)
* [wizard\_tk\_bridge.wizard\_path](#wizard_tk_bridge.wizard_path)
  * [pick\_path](#wizard_tk_bridge.wizard_path.pick_path)
  * [PathRow](#wizard_tk_bridge.wizard_path.PathRow)
    * [\_\_init\_\_](#wizard_tk_bridge.wizard_path.PathRow.__init__)
    * [get](#wizard_tk_bridge.wizard_path.PathRow.get)
    * [set\_text](#wizard_tk_bridge.wizard_path.PathRow.set_text)
    * [set\_enabled](#wizard_tk_bridge.wizard_path.PathRow.set_enabled)
* [wizard\_tk\_bridge.wizard\_window](#wizard_tk_bridge.wizard_window)
  * [WizardWindow](#wizard_tk_bridge.wizard_window.WizardWindow)
    * [\_\_init\_\_](#wizard_tk_bridge.wizard_window.WizardWindow.__init__)
    * [show](#wizard_tk_bridge.wizard_window.WizardWindow.show)
    * [close](#wizard_tk_bridge.wizard_window.WizardWindow.close)
    * [ask\_text](#wizard_tk_bridge.wizard_window.WizardWindow.ask_text)
    * [ask\_int](#wizard_tk_bridge.wizard_window.WizardWindow.ask_int)
    * [ask\_path](#wizard_tk_bridge.wizard_window.WizardWindow.ask_path)
    * [ask\_form](#wizard_tk_bridge.wizard_window.WizardWindow.ask_form)
    * [ask\_yes\_no](#wizard_tk_bridge.wizard_window.WizardWindow.ask_yes_no)
    * [ask\_choice](#wizard_tk_bridge.wizard_window.WizardWindow.ask_choice)
    * [ask\_multi](#wizard_tk_bridge.wizard_window.WizardWindow.ask_multi)
    * [ask\_table](#wizard_tk_bridge.wizard_window.WizardWindow.ask_table)

<a id="wizard_tk_bridge.auto_scroll"></a>

# wizard\_tk\_bridge.auto\_scroll

A scroll command that shows a scrollbar only while it can scroll.

A table that fits its area needs no scrollbar, and a scrollbar that is
always shown wastes space and hints at hidden content that is not there.
:func:`auto_hide` returns the scroll command for a scrolling widget: the
command hides the scrollbar while the whole range is visible and shows it
again once the widget grows past its area. It works for any widget that
reports its position through an ``xscrollcommand`` or ``yscrollcommand``,
so a wizard table's canvas and any other scrolling widget can share it.

<a id="wizard_tk_bridge.auto_scroll.auto_hide"></a>

#### auto\_hide

```python
def auto_hide(
        scrollbar: ttk.Scrollbar
) -> Callable[[float | str, float | str], None]
```

Return a scroll command that hides the scrollbar when it is full.

The result is used as a widget's ``xscrollcommand`` or
``yscrollcommand``. Tk reports the position as two fractions, which it
passes as strings, so the command accepts either a number or its
string form. The scrollbar must be laid out with the grid manager,
whose ``grid_remove`` remembers its cell across the hide.

<a id="wizard_tk_bridge._no_text_io"></a>

# wizard\_tk\_bridge.\_no\_text\_io

NoTextIO can be used as a TextIO object that does nothing.

<a id="wizard_tk_bridge._no_text_io.NoTextIO"></a>

## NoTextIO Objects

```python
class NoTextIO(io.StringIO)
```

NoTextIO can be used as a TextIO object that does nothing.

When a function expects a TextIO object for output, you can pass in
a NoTextIO object and no output will be produced.
The differrence compared to using StringIO to suppress output is that
the NoTextIO does not store any data, so no matter how much is
written to it, you do not risk running out of memory.

<a id="wizard_tk_bridge._no_text_io.NoTextIO.write"></a>

#### write

```python
@override
def write(s: str) -> int
```

Write a string to the NoTextIO object.

This method does nothing and returns 0.

<a id="wizard_tk_bridge._no_text_io.NoTextIO.writelines"></a>

#### writelines

```python
@override
def writelines(lines: Iterable[str]) -> None
```

Write a list of strings to the NoTextIO object.

This method does nothing and returns None.

<a id="wizard_tk_bridge._no_text_io.NoTextIO.flush"></a>

#### flush

```python
@override
def flush() -> None
```

Flush the NoTextIO object.

This method does nothing and returns None.

<a id="wizard_tk_bridge._no_text_io.NoTextIO.close"></a>

#### close

```python
@override
def close() -> None
```

Close the NoTextIO object.

This method does nothing and returns None.

<a id="wizard_tk_bridge._no_text_io.NoTextIO.seek"></a>

#### seek

```python
@override
def seek(offset: int, whence: int = io.SEEK_SET) -> int
```

Seek to a position in the NoTextIO object.

This method does nothing and returns 0.

<a id="wizard_tk_bridge._no_text_io.NoTextIO.tell"></a>

#### tell

```python
@override
def tell() -> int
```

Get the current position in the NoTextIO object.

This method does nothing and returns 0.

<a id="wizard_tk_bridge._no_text_io.NoTextIO.truncate"></a>

#### truncate

```python
@override
def truncate(size: Optional[int] = None) -> int
```

Truncate the NoTextIO object.

This method does nothing and returns 0.

<a id="wizard_tk_bridge.gui_style"></a>

# wizard\_tk\_bridge.gui\_style

Shared look and focus helpers for the Tkinter input windows.

Editable input widgets blend into the window background on some
platforms, so the user cannot tell an entry, drop-down or list from the
surrounding window. :func:`style_input` gives such a widget a white
field and a thin border so it stands out. :func:`focus_first_input`
puts the keyboard focus on the first editable widget of a window, so the
user can start typing as soon as the window opens.

<a id="wizard_tk_bridge.gui_style.style_input"></a>

#### style\_input

```python
def style_input(widget: tk.Widget) -> None
```

Make one editable input widget stand out from the background.

A classic entry, text box or list gets a white field and a thin
solid border. A drop-down keeps its arrow but gets a white field
through a shared ttk style. Any other widget is left unchanged. The
ttk styling is best-effort: a native theme that ignores field colors
leaves the drop-down as it is.

<a id="wizard_tk_bridge.gui_style.focus_first_input"></a>

#### focus\_first\_input

```python
def focus_first_input(window: tk.Misc) -> None
```

Give the keyboard focus to the first editable input, if any.

<a id="wizard_tk_bridge.wizard_typed"></a>

# wizard\_tk\_bridge.wizard\_typed

Text parsing and formatting for the typed wizard form fields.

The float, date, time, date-time and duration form fields each turn user
text into a typed value and a typed value back into text. This module
holds that conversion for the Tkinter bridge, together with the format
hints and the parse and range error messages, so the graphical form
accepts the same text a user would type on the console.

A duration is written as an optional day count and a clock part,
``<days> d HH:MM:SS``, where the seconds may carry a decimal fraction, or
as a single non-negative number of seconds. Dates, times and date-times
use the ISO 8601 forms accepted by the standard library fromisoformat()
parsers.

<a id="wizard_tk_bridge.wizard_typed.parse_float"></a>

#### parse\_float

```python
def parse_float(text: str) -> Optional[float]
```

Return a finite float from text, or None when not a number.

<a id="wizard_tk_bridge.wizard_typed.parse_date"></a>

#### parse\_date

```python
def parse_date(text: str) -> Optional[date]
```

Return an ISO date from text, or None when not a valid date.

<a id="wizard_tk_bridge.wizard_typed.parse_time"></a>

#### parse\_time

```python
def parse_time(text: str) -> Optional[time]
```

Return an ISO time from text, or None when not a valid time.

<a id="wizard_tk_bridge.wizard_typed.parse_datetime"></a>

#### parse\_datetime

```python
def parse_datetime(text: str) -> Optional[datetime]
```

Return an ISO date-time from text, or None when not valid.

<a id="wizard_tk_bridge.wizard_typed.parse_duration"></a>

#### parse\_duration

```python
def parse_duration(text: str) -> Optional[timedelta]
```

Return a duration from text, or None when it is not valid.

A lone non-negative number is read as a count of seconds; otherwise
the text must be ``<hours>:<minutes>:<seconds>`` with an optional
``<days> d`` prefix, and the seconds may carry a decimal fraction.

<a id="wizard_tk_bridge.wizard_typed.format_duration"></a>

#### format\_duration

```python
def format_duration(value: timedelta) -> str
```

Return a duration as ``<days> d HH:MM:SS`` with any fraction.

<a id="wizard_tk_bridge.wizard_typed.format_value"></a>

#### format\_value

```python
def format_value(value: object) -> str
```

Return the text a typed value would round-trip from.

<a id="wizard_tk_bridge.wizard_typed.ordered_range_error"></a>

#### ordered\_range\_error

```python
def ordered_range_error(minimum: Optional[object],
                        maximum: Optional[object]) -> str
```

Return the message shown when a typed value is out of range.

<a id="wizard_tk_bridge.wizard_typed.is_typed"></a>

#### is\_typed

```python
def is_typed(field: AskField) -> bool
```

Return whether field is one of the five typed form fields.

<a id="wizard_tk_bridge.wizard_typed.field_hint"></a>

#### field\_hint

```python
def field_hint(field: AskField) -> str
```

Return the accepted-format hint shown for a typed field.

<a id="wizard_tk_bridge.wizard_typed.default_text"></a>

#### default\_text

```python
def default_text(field: AskField) -> str
```

Return the starting entry text for a typed field's default.

<a id="wizard_tk_bridge.wizard_typed.typed_value"></a>

#### typed\_value

```python
def typed_value(field: AskField, text: str) -> Optional[object]
```

Return the typed value of a typed field for its widget text.

An empty text yields the field default. A non-empty text is parsed;
unparsable or out-of-range text yields None, and the caller reports
the error separately through typed_error().

<a id="wizard_tk_bridge.wizard_typed.typed_error"></a>

#### typed\_error

```python
def typed_error(field: AskField, text: str) -> Optional[str]
```

Return the parse or range error of a typed field's widget text.

Empty text is accepted when the field is nullable or has a default,
and otherwise reports that a value is required.

<a id="wizard_tk_bridge.wizard_typed.typed_answer"></a>

#### typed\_answer

```python
def typed_answer(field: AskField, value: Optional[object]) -> AnswerField
```

Wrap a typed value in the answer matching a typed field.

<a id="wizard_tk_bridge.wizard_typed.date_of"></a>

#### date\_of

```python
def date_of(value: Optional[object]) -> Optional[date]
```

Return the date part of a date or datetime, or None.

<a id="wizard_tk_bridge.wizard_typed.calendar_seed"></a>

#### calendar\_seed

```python
def calendar_seed(field: AskField,
                  text: str) -> tuple[date, Optional[date], Optional[date]]
```

Return the calendar seed date and its inclusive day bounds.

A date-time field's bounds are its date parts, so the calendar offers
the acceptable days and the field itself validates the exact value.

<a id="wizard_tk_bridge.wizard_typed.combined_text"></a>

#### combined\_text

```python
def combined_text(field: AskField, picked: date, current: str) -> str
```

Return the input text for a picked date, keeping any typed time.

<a id="wizard_tk_bridge.wizard_pick_row"></a>

# wizard\_tk\_bridge.wizard\_pick\_row

Placeholder-aware entries for the typed wizard form fields.

The float, time and duration form fields are shown as a text entry that
displays its accepted-format hint as greyed placeholder text while empty,
so the user learns the format without cluttering the field label. A date
or date-time field adds a Pick button that opens a month calendar, and
typing the ``?`` token into the entry opens the same calendar.

:class:`HintEntry` is the placeholder entry, and :class:`PickRow` bundles
one with the calendar button. Both satisfy :class:`TypedInput`, the small
interface the form editor uses to read, write, and enable a typed row.

<a id="wizard_tk_bridge.wizard_pick_row.TypedInput"></a>

## TypedInput Objects

```python
class TypedInput(Protocol)
```

The read, write and enable interface of a typed form input.

<a id="wizard_tk_bridge.wizard_pick_row.TypedInput.text"></a>

#### text

```python
def text() -> str
```

Return the current text, empty when only a placeholder shows.

<a id="wizard_tk_bridge.wizard_pick_row.TypedInput.set_text"></a>

#### set\_text

```python
def set_text(text: str) -> None
```

Replace the current text, showing the placeholder when empty.

<a id="wizard_tk_bridge.wizard_pick_row.TypedInput.set_enabled"></a>

#### set\_enabled

```python
def set_enabled(enabled: bool) -> None
```

Enable or disable the input for user editing.

<a id="wizard_tk_bridge.wizard_pick_row.HintEntry"></a>

## HintEntry Objects

```python
class HintEntry()
```

A text entry showing a greyed format hint while it is empty.

<a id="wizard_tk_bridge.wizard_pick_row.HintEntry.__init__"></a>

#### \_\_init\_\_

```python
def __init__(parent: tk.Misc, hint: str, initial: str,
             on_change: Callable[[], None]) -> None
```

Build the entry, showing initial text or the greyed hint.

<a id="wizard_tk_bridge.wizard_pick_row.HintEntry.text"></a>

#### text

```python
def text() -> str
```

Return the entered text, empty when only the hint shows.

<a id="wizard_tk_bridge.wizard_pick_row.HintEntry.set_text"></a>

#### set\_text

```python
def set_text(text: str) -> None
```

Replace the text, showing the greyed hint when text is empty.

<a id="wizard_tk_bridge.wizard_pick_row.HintEntry.set_enabled"></a>

#### set\_enabled

```python
def set_enabled(enabled: bool) -> None
```

Enable or disable the entry for user editing.

<a id="wizard_tk_bridge.wizard_pick_row.PickRow"></a>

## PickRow Objects

```python
class PickRow()
```

A hint entry paired with a Pick button that opens a calendar.

<a id="wizard_tk_bridge.wizard_pick_row.PickRow.__init__"></a>

#### \_\_init\_\_

```python
def __init__(parent: tk.Misc, field: AskField, hint: str, initial: str,
             on_change: Callable[[], None]) -> None
```

Build the entry and Pick button inside a new frame.

<a id="wizard_tk_bridge.wizard_pick_row.PickRow.text"></a>

#### text

```python
def text() -> str
```

Return the entered date or date-time text.

<a id="wizard_tk_bridge.wizard_pick_row.PickRow.set_text"></a>

#### set\_text

```python
def set_text(text: str) -> None
```

Replace the entered text, showing the hint when empty.

<a id="wizard_tk_bridge.wizard_pick_row.PickRow.set_enabled"></a>

#### set\_enabled

```python
def set_enabled(enabled: bool) -> None
```

Enable or disable both the entry and the Pick button.

<a id="wizard_tk_bridge.wizard_calendar"></a>

# wizard\_tk\_bridge.wizard\_calendar

A modal month calendar for the Tkinter date and date-time fields.

A date field, and the date part of a date-time field, are shown in the
Tkinter form as a text entry paired with a Pick button. Pressing that
button, or typing the ``?`` token into the entry, opens this calendar.
The user steps between months and years and clicks a day to return it;
Cancel or closing the window returns nothing so the entry keeps its
value. Days outside a field's inclusive bounds are shown disabled, so the
calendar only offers acceptable dates.

The calendar is event driven: a day or Cancel button calls the picked
callback and destroys the window. No nested wait loop is entered, so the
one already running for the wizard host keeps processing events while
the calendar is open.

A modal wizard host holds its own grab, which would otherwise starve this
separate window of pointer and keyboard events. The calendar therefore
takes the grab (and the keyboard focus) while it is open, and hands it
back to the host window when it closes -- but only when that host held a
grab in the first place, so opening a calendar over a non-modal, embedded
wizard never makes it modal.

<a id="wizard_tk_bridge.wizard_calendar.month_weeks"></a>

#### month\_weeks

```python
def month_weeks(year: int, month: int) -> list[list[int]]
```

Return the weeks of a month as day numbers, 0 for padding days.

<a id="wizard_tk_bridge.wizard_calendar.shift_month"></a>

#### shift\_month

```python
def shift_month(year: int, month: int, action: str) -> tuple[int, int]
```

Return the year and month reached by one navigation action.

This mirrors wizard_ui_bridge._calendar, the private module behind
the Textual bridge's own calendar screen; that module is not public
API a sibling package may import, so this one keeps its own copy.

<a id="wizard_tk_bridge.wizard_calendar.day_out_of_range"></a>

#### day\_out\_of\_range

```python
def day_out_of_range(day: date, minimum: Optional[date],
                     maximum: Optional[date]) -> bool
```

Return whether a day lies outside the inclusive date bounds.

<a id="wizard_tk_bridge.wizard_calendar.CalendarPicker"></a>

## CalendarPicker Objects

```python
class CalendarPicker()
```

A month calendar window returning the date the user clicks.

<a id="wizard_tk_bridge.wizard_calendar.CalendarPicker.__init__"></a>

#### \_\_init\_\_

```python
def __init__(parent: tk.Misc, seed: date, minimum: Optional[date],
             maximum: Optional[date], on_pick: Callable[[Optional[date]],
                                                        None]) -> None
```

Build the calendar window on the seed month and show it.

<a id="wizard_tk_bridge.close_binding"></a>

# wizard\_tk\_bridge.close\_binding

Bind the close-window key to a secondary window's close action.

On macOS the Tk toolkit does not close a window when the user presses
Cmd-W, so every secondary window binds that key here. Cmd-W is bound on
every platform, where it is harmless without a Command key, and Ctrl-W is
added on Windows, its customary close-window shortcut. The bound action
defaults to destroying the window but may be the window's own cancel or
abort handler, so the key behaves exactly like the window close button.

<a id="wizard_tk_bridge.close_binding.bind_close"></a>

#### bind\_close

```python
def bind_close(win: tk.Toplevel,
               on_close: Optional[Callable[[], None]] = None) -> None
```

Bind the close-window key to run the window's close action.

**Arguments**:

- `win` - The secondary window to close on the key press.
- `on_close` - The close action, defaulting to destroying the window.
  A window that cancels or aborts on close passes its own
  handler, so the key matches its window close button.

<a id="wizard_tk_bridge.wizard_table"></a>

# wizard\_tk\_bridge.wizard\_table

An editable grid of cells for one wizard table question.

A table question shown by the wizard is rendered as a grid of cells. A
fixed table fills its seed rows only; a variable table, asked with both a
minimum and a maximum row count, offers add-row and remove-row buttons.
Every table shows its grid in a scrolling area: it scrolls horizontally
when its columns are wider than the window, and a variable table also
scrolls vertically within a fixed height so a long table stays usable.
:class:`TableEditor` builds the grid, reads the final cell strings back,
and runs the optional per-cell partial check for early feedback.

<a id="wizard_tk_bridge.wizard_table.Cell"></a>

## Cell Objects

```python
@dataclass(frozen=True)
class Cell()
```

One built table cell: its widget and how its value is read.

A read-only cell keeps the fixed text it shows in its label. An
editable cell keeps the widget the user types in or selects from, and
whether an empty cell is reported as ``None``.

<a id="wizard_tk_bridge.wizard_table.TableEditor"></a>

## TableEditor Objects

```python
class TableEditor()
```

An editable grid of cells for one table question.

A fixed table fills the seed rows only. A variable table, asked with
both a minimum and a maximum row count, adds editable rows up to the
maximum and removes the last row down to the minimum. Every table
scrolls horizontally when its columns overflow the window, and a
variable table also scrolls vertically within a fixed height, so a
long or wide table stays usable while the wizard window is resized.

<a id="wizard_tk_bridge.wizard_table.TableEditor.__init__"></a>

#### \_\_init\_\_

```python
def __init__(parent: tk.Misc,
             columns: Sequence[TableColumn],
             rows: Sequence[Sequence[TableCell]],
             partial_check: Optional[PartialCheck],
             min_rows: Optional[int] = None,
             max_rows: Optional[int] = None) -> None
```

Build the header and one widget per cell of the seed rows.

<a id="wizard_tk_bridge.wizard_table.TableEditor.is_variable"></a>

#### is\_variable

```python
def is_variable() -> bool
```

Return whether the table can add and remove rows.

<a id="wizard_tk_bridge.wizard_table.TableEditor.values"></a>

#### values

```python
def values() -> list[list[Optional[str]]]
```

Return the whole table as rows of final cell strings.

<a id="wizard_tk_bridge.wizard_table.TableEditor.add_row"></a>

#### add\_row

```python
def add_row() -> None
```

Append one editable row, up to the maximum row count.

<a id="wizard_tk_bridge.wizard_table.TableEditor.remove_row"></a>

#### remove\_row

```python
def remove_row() -> None
```

Remove the last row, down to the minimum row count.

<a id="wizard_tk_bridge.wizard_form"></a>

# wizard\_tk\_bridge.wizard\_form

A whole wizard form shown on one screen, and its answer parsing.

A form question asks several related fields at once. :class:`FormEditor`
builds a two-column grid, a label on the left and an input widget on the
right, one row per :class:`AskField`. It reads one :class:`AnswerField`
per row, runs the optional partial validator after every change to show
advisory feedback and disable irrelevant rows, and validates every
enabled field on submit so a submitted form is always complete.

The small scalar-answer helpers (:func:`text_answer`, :func:`int_answer`
and friends) turn the raw text of a text or integer field into its typed
answer. They are shared with the reused wizard window, which asks a
standalone integer question with the same rules.

<a id="wizard_tk_bridge.wizard_form.handles_field"></a>

#### handles\_field

```python
def handles_field(field: AskField) -> bool
```

Return whether the Tk form can show the given field type.

<a id="wizard_tk_bridge.wizard_form.int_answer"></a>

#### int\_answer

```python
def int_answer(
        text: str, nullable: bool, min_value: Optional[int],
        max_value: Optional[int],
        default: Optional[int]) -> tuple[bool, Optional[int], Optional[str]]
```

Return whether an integer answer is final, its value, and a reason.

An empty answer takes the default, is None when nullable, or is
re-asked otherwise. A non-empty answer must parse as an integer that
lies within the inclusive bounds.

<a id="wizard_tk_bridge.wizard_form.HelpTooltip"></a>

## HelpTooltip Objects

```python
class HelpTooltip()
```

A hover bubble showing a field's help text over its widgets.

The bubble is a label placed over the window that holds the bound
widgets, shown when the pointer enters one of them and destroyed
when it leaves, so help appears on hover as it does in the textual
bridge. A window of its own is drawn with the platform's window
shape, which on macOS rounds the corners of a borderless window so
much that a one-line bubble loses its first and last characters. A
placed label is a plain rectangle on every platform, takes neither
focus nor a grab, and cannot outlive the widgets it belongs to.

<a id="wizard_tk_bridge.wizard_form.HelpTooltip.__init__"></a>

#### \_\_init\_\_

```python
def __init__(text: str, anchor: tk.Widget,
             widgets: Sequence[tk.Widget]) -> None
```

Bind hover show and hide on each widget for the help text.

<a id="wizard_tk_bridge.wizard_form.HelpTooltip.show"></a>

#### show

```python
def show() -> None
```

Show the help bubble just below the anchor widget.

<a id="wizard_tk_bridge.wizard_form.HelpTooltip.hide"></a>

#### hide

```python
def hide() -> None
```

Destroy the help bubble when one is shown.

<a id="wizard_tk_bridge.wizard_form.FormRow"></a>

## FormRow Objects

```python
@dataclass(frozen=True)
class FormRow()
```

One built form row: its field, label, input and help tooltip.

<a id="wizard_tk_bridge.wizard_form.FormEditor"></a>

## FormEditor Objects

```python
class FormEditor()
```

A two-column grid that asks a whole wizard form on one screen.

<a id="wizard_tk_bridge.wizard_form.FormEditor.__init__"></a>

#### \_\_init\_\_

```python
def __init__(parent: tk.Misc, fields: Sequence[AskField],
             validator: Optional[PartialFormValidator],
             on_submit: Callable[[list[AnswerField]], None]) -> None
```

Build one labelled input row per field, plus a status line.

<a id="wizard_tk_bridge.wizard_form.FormEditor.answers"></a>

#### answers

```python
def answers() -> list[AnswerField]
```

Return the current answer of every row, in field order.

<a id="wizard_tk_bridge.wizard_form.FormEditor.submit"></a>

#### submit

```python
def submit() -> None
```

Validate every enabled field and submit when all pass.

<a id="wizard_tk_bridge.tk_bridge"></a>

# wizard\_tk\_bridge.tk\_bridge

Graphical Tkinter bridge that drives a synchronous wizard.

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
  window is shown over. This suits an application with other windows.
  A standalone CLI program can omit both ``parent`` and ``area``; the
  bridge then owns the hidden root needed for this window.
- Embedded in an area the application already built: give ``area``, the
  frame or other container the wizard should fill instead of a window of
  its own.
- Either way, ``modal`` decides whether the wizard grabs its window (or
  the window containing ``area``) for the duration of the session, so
  the rest of that window is unusable meanwhile. The application is best
  placed to decide this, since only it knows whether its other content
  should stay usable while the wizard runs.

At most one of ``parent`` and ``area`` may be given. If neither is given,
the bridge creates and owns a hidden root, which is useful for a standalone
CLI program that has no other Tkinter code.

<a id="wizard_tk_bridge.tk_bridge.WizardUiBridgeTk"></a>

## WizardUiBridgeTk Objects

```python
class WizardUiBridgeTk(WizardUiBridge)
```

Bridge that answers wizard prompts through Tkinter widgets.

<a id="wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.__init__"></a>

#### \_\_init\_\_

```python
def __init__(parent: Optional[tk.Misc] = None,
             area: Optional[tk.Misc] = None,
             modal: bool = True,
             log: Optional[TextIO] = None) -> None
```

Store where and how to show the wizard, and the optional log.

**Arguments**:

- `parent` - The widget the wizard's own new window is shown over.
  Leave both parent and area as None for a standalone
  bridge that owns its hidden root.
- `area` - The existing container the wizard fills instead of a
  window of its own. It cannot be given together with
  parent.
- `modal` - Whether the wizard grabs its window (or area's window)
  for the session; see the module docstring.
- `log` - Stream that receives low-level wizard diagnostics.

**Raises**:

- `ValueError` - Both parent and area were given.

<a id="wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.ask_text"></a>

#### ask\_text

```python
def ask_text(question: str,
             re_ask_reason: Optional[str] = None,
             nullable: bool = False,
             *,
             default: Optional[str] = None,
             sensitive: bool = False) -> Optional[str]
```

Ask for free text; see WizardUiBridge.ask_text.

<a id="wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.ask_int"></a>

#### ask\_int

```python
def ask_int(question: str,
            re_ask_reason: Optional[str] = None,
            *,
            nullable: bool = False,
            min_value: Optional[int] = None,
            max_value: Optional[int] = None,
            default: Optional[int] = None) -> Optional[int]
```

Ask for an integer within optional bounds; see ask_int.

<a id="wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.ask_path"></a>

#### ask\_path

```python
def ask_path(question: str,
             re_ask_reason: Optional[str] = None,
             *,
             options: Optional[PathAskOptions] = None) -> Optional[Path]
```

Ask for a path with a native file or directory picker.

<a id="wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.ask_yes_no"></a>

#### ask\_yes\_no

```python
def ask_yes_no(question: str,
               default: bool,
               re_ask_reason: Optional[str] = None) -> bool
```

Ask a yes/no question with dedicated yes and no buttons.

<a id="wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.ask_choice"></a>

#### ask\_choice

```python
def ask_choice(question: str,
               *,
               choices: Sequence[str],
               default: Optional[str] = None,
               re_ask_reason: Optional[str] = None) -> str
```

Ask the user to pick one choice from a single-selection list.

<a id="wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.ask_multi"></a>

#### ask\_multi

```python
def ask_multi(question: str,
              *,
              choices: Sequence[str],
              default: Optional[Sequence[str]] = None,
              min_select: int = 0,
              max_select: Optional[int] = None,
              re_ask_reason: Optional[str] = None) -> list[str]
```

Ask the user to pick several choices from a multi-selection list.

<a id="wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.ask_table"></a>

#### ask\_table

```python
def ask_table(columns: Sequence[TableColumn],
              cells: list[list[TableCell]],
              question: str,
              *,
              re_ask_reason: Optional[str] = None,
              partial_check: Optional[PartialCheck] = None,
              min_rows: Optional[int] = None,
              max_rows: Optional[int] = None) -> list[list[Optional[str]]]
```

Ask the user to fill an editable table of the given rows.

With both ``min_rows`` and ``max_rows`` given the table has a
variable number of rows: add-row and remove-row buttons grow the
table up to ``max_rows`` and shrink it down to ``min_rows``.
Otherwise the rows given in ``cells`` are fixed and only filled.

<a id="wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.ask_form"></a>

#### ask\_form

```python
def ask_form(
        long_question: str,
        ask_fields: AskFields,
        *,
        re_ask_reason: Optional[str] = None,
        partial_validator: Optional[PartialFormValidator] = None
) -> AnswerFields
```

Ask a whole form on one screen; see WizardUiBridge.ask_form.

<a id="wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.supports_form_field"></a>

#### supports\_form\_field

```python
def supports_form_field(field: AskField) -> bool
```

Report that the Tk form shows every current field type.

<a id="wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.show"></a>

#### show

```python
def show(message: str) -> None
```

Show an informational message to the user.

<a id="wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.error_file"></a>

#### error\_file

```python
def error_file() -> TextIO
```

Return the stream used for low-level wizard diagnostics.

<a id="wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.close"></a>

#### close

```python
def close() -> None
```

Close the wizard window, or clear its area, when one was built.

<a id="wizard_tk_bridge.wizard_path"></a>

# wizard\_tk\_bridge.wizard\_path

Native path picking for the wizard bridge.

A path question in the Tkinter wizard shows an editable path entry next
to a Browse button that opens the native open-file, save-file or
directory dialog chosen by the :class:`WizardPathKind`. Validating the
typed or picked path is left to
:func:`wizard_ui_bridge.bridge_helpers.path_answer`, the same check the
console and Textual bridges apply, so a graphical answer is accepted or
rejected the same way. :class:`PathRow` bundles the entry and the Browse
button, and is reused both by the standalone path question and by a path
field inside a form.

<a id="wizard_tk_bridge.wizard_path.pick_path"></a>

#### pick\_path

```python
def pick_path(parent: tk.Misc, options: PathAskOptions,
              initial: str) -> Optional[str]
```

Open the native dialog for the kind, or None when cancelled.

<a id="wizard_tk_bridge.wizard_path.PathRow"></a>

## PathRow Objects

```python
class PathRow()
```

An editable path entry paired with a native Browse button.

<a id="wizard_tk_bridge.wizard_path.PathRow.__init__"></a>

#### \_\_init\_\_

```python
def __init__(parent: tk.Misc,
             options: PathAskOptions,
             initial: str,
             on_change: Optional[Callable[[], None]] = None) -> None
```

Build the entry and Browse button inside a new frame.

<a id="wizard_tk_bridge.wizard_path.PathRow.get"></a>

#### get

```python
def get() -> str
```

Return the current path text.

<a id="wizard_tk_bridge.wizard_path.PathRow.set_text"></a>

#### set\_text

```python
def set_text(text: str) -> None
```

Replace the path text, enabling the entry briefly if disabled.

<a id="wizard_tk_bridge.wizard_path.PathRow.set_enabled"></a>

#### set\_enabled

```python
def set_enabled(enabled: bool) -> None
```

Enable or disable both the entry and the Browse button.

<a id="wizard_tk_bridge.wizard_window"></a>

# wizard\_tk\_bridge.wizard\_window

A Tk host that asks every wizard prompt in turn, one at a time.

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

<a id="wizard_tk_bridge.wizard_window.WizardWindow"></a>

## WizardWindow Objects

```python
class WizardWindow()
```

A Tk host, own window or embedded, that asks every wizard prompt.

<a id="wizard_tk_bridge.wizard_window.WizardWindow.__init__"></a>

#### \_\_init\_\_

```python
def __init__(parent: Optional[tk.Misc] = None,
             area: Optional[tk.Misc] = None,
             modal: bool = True) -> None
```

Build the wizard's own window, or embed it into an existing area.

Exactly one of parent or area must be given; see the module
docstring for what each means and how modal applies to it.

<a id="wizard_tk_bridge.wizard_window.WizardWindow.show"></a>

#### show

```python
def show(message: str) -> None
```

Append one lasting message to the message area.

<a id="wizard_tk_bridge.wizard_window.WizardWindow.close"></a>

#### close

```python
def close() -> None
```

Release any modal grab and remove the wizard's own widgets.

<a id="wizard_tk_bridge.wizard_window.WizardWindow.ask_text"></a>

#### ask\_text

```python
def ask_text(question: str,
             re_ask: Optional[str],
             nullable: bool,
             default: Optional[str] = None,
             sensitive: bool = False) -> Optional[str]
```

Ask one free-text question and return the entered text.

A sensitive question masks the typed text; a default value is
pre-filled and returned when the answer is left empty.

<a id="wizard_tk_bridge.wizard_window.WizardWindow.ask_int"></a>

#### ask\_int

```python
def ask_int(question: str, re_ask: Optional[str], nullable: bool,
            min_value: Optional[int], max_value: Optional[int],
            default: Optional[int]) -> Optional[int]
```

Ask one integer question, re-asking until it is in range.

<a id="wizard_tk_bridge.wizard_window.WizardWindow.ask_path"></a>

#### ask\_path

```python
def ask_path(question: str, options: PathAskOptions,
             re_ask: Optional[str]) -> Optional[Path]
```

Ask one path question with a Browse button, re-asking on error.

<a id="wizard_tk_bridge.wizard_window.WizardWindow.ask_form"></a>

#### ask\_form

```python
def ask_form(long_question: str, fields: AskFields, re_ask: Optional[str],
             validator: Optional[PartialFormValidator]) -> AnswerFields
```

Ask a whole form on one screen and return its answers.

<a id="wizard_tk_bridge.wizard_window.WizardWindow.ask_yes_no"></a>

#### ask\_yes\_no

```python
def ask_yes_no(question: str, default: bool, re_ask: Optional[str]) -> bool
```

Ask one yes/no question with dedicated buttons.

<a id="wizard_tk_bridge.wizard_window.WizardWindow.ask_choice"></a>

#### ask\_choice

```python
def ask_choice(question: str, choices: Sequence[str], default: Optional[str],
               re_ask: Optional[str]) -> str
```

Ask the user to pick exactly one choice and return it.

<a id="wizard_tk_bridge.wizard_window.WizardWindow.ask_multi"></a>

#### ask\_multi

```python
def ask_multi(question: str, choices: Sequence[str],
              default: Optional[Sequence[str]], min_select: int,
              max_select: Optional[int], re_ask: Optional[str]) -> list[str]
```

Ask the user to pick several choices within the count bounds.

<a id="wizard_tk_bridge.wizard_window.WizardWindow.ask_table"></a>

#### ask\_table

```python
def ask_table(columns: Sequence[TableColumn],
              cells: Sequence[Sequence[TableCell]], question: str,
              re_ask: Optional[str], partial_check: Optional[PartialCheck],
              min_rows: Optional[int],
              max_rows: Optional[int]) -> list[list[Optional[str]]]
```

Ask the user to fill the given table rows and return them.

