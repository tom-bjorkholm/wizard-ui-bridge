# Table of Contents

* [wizard\_tk\_bridge.auto\_scroll](#wizard_tk_bridge.auto_scroll)
  * [auto\_hide](#wizard_tk_bridge.auto_scroll.auto_hide)
  * [bind\_wheel](#wizard_tk_bridge.auto_scroll.bind_wheel)
* [wizard\_tk\_bridge.\_no\_text\_io](#wizard_tk_bridge._no_text_io)
  * [NoTextIO](#wizard_tk_bridge._no_text_io.NoTextIO)
    * [write](#wizard_tk_bridge._no_text_io.NoTextIO.write)
    * [writelines](#wizard_tk_bridge._no_text_io.NoTextIO.writelines)
    * [flush](#wizard_tk_bridge._no_text_io.NoTextIO.flush)
    * [close](#wizard_tk_bridge._no_text_io.NoTextIO.close)
    * [seek](#wizard_tk_bridge._no_text_io.NoTextIO.seek)
    * [tell](#wizard_tk_bridge._no_text_io.NoTextIO.tell)
    * [truncate](#wizard_tk_bridge._no_text_io.NoTextIO.truncate)
* [wizard\_tk\_bridge.wizard\_cell](#wizard_tk_bridge.wizard_cell)
  * [int\_answer](#wizard_tk_bridge.wizard_cell.int_answer)
  * [HelpTooltip](#wizard_tk_bridge.wizard_cell.HelpTooltip)
    * [\_\_init\_\_](#wizard_tk_bridge.wizard_cell.HelpTooltip.__init__)
    * [show](#wizard_tk_bridge.wizard_cell.HelpTooltip.show)
    * [hide](#wizard_tk_bridge.wizard_cell.HelpTooltip.hide)
  * [tooltip\_text](#wizard_tk_bridge.wizard_cell.tooltip_text)
  * [CellInput](#wizard_tk_bridge.wizard_cell.CellInput)
    * [value](#wizard_tk_bridge.wizard_cell.CellInput.value)
    * [error](#wizard_tk_bridge.wizard_cell.CellInput.error)
    * [write](#wizard_tk_bridge.wizard_cell.CellInput.write)
    * [main\_widget](#wizard_tk_bridge.wizard_cell.CellInput.main_widget)
    * [set\_width](#wizard_tk_bridge.wizard_cell.CellInput.set_width)
    * [set\_enabled](#wizard_tk_bridge.wizard_cell.CellInput.set_enabled)
  * [build\_input](#wizard_tk_bridge.wizard_cell.build_input)
  * [scrolled\_editor](#wizard_tk_bridge.wizard_cell.scrolled_editor)
  * [scroll\_into\_view](#wizard_tk_bridge.wizard_cell.scroll_into_view)
  * [view\_start](#wizard_tk_bridge.wizard_cell.view_start)
* [wizard\_tk\_bridge.gui\_style](#wizard_tk_bridge.gui_style)
  * [style\_input](#wizard_tk_bridge.gui_style.style_input)
  * [choice\_combo](#wizard_tk_bridge.gui_style.choice_combo)
  * [focus\_first\_input](#wizard_tk_bridge.gui_style.focus_first_input)
  * [bind\_submit](#wizard_tk_bridge.gui_style.bind_submit)
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
  * [date\_of](#wizard_tk_bridge.wizard_typed.date_of)
  * [calendar\_seed](#wizard_tk_bridge.wizard_typed.calendar_seed)
  * [combined\_text](#wizard_tk_bridge.wizard_typed.combined_text)
* [wizard\_tk\_bridge.wizard\_pick\_row](#wizard_tk_bridge.wizard_pick_row)
  * [TypedInput](#wizard_tk_bridge.wizard_pick_row.TypedInput)
    * [entry](#wizard_tk_bridge.wizard_pick_row.TypedInput.entry)
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
    * [entry](#wizard_tk_bridge.wizard_pick_row.PickRow.entry)
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
    * [ask\_matrix\_form](#wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.ask_matrix_form)
    * [supports\_form\_field](#wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.supports_form_field)
    * [show](#wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.show)
    * [error\_file](#wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.error_file)
    * [close](#wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.close)
* [wizard\_tk\_bridge.wizard\_path](#wizard_tk_bridge.wizard_path)
  * [pick\_path](#wizard_tk_bridge.wizard_path.pick_path)
  * [PathRow](#wizard_tk_bridge.wizard_path.PathRow)
    * [\_\_init\_\_](#wizard_tk_bridge.wizard_path.PathRow.__init__)
    * [entry](#wizard_tk_bridge.wizard_path.PathRow.entry)
    * [get](#wizard_tk_bridge.wizard_path.PathRow.get)
    * [set\_text](#wizard_tk_bridge.wizard_path.PathRow.set_text)
    * [set\_enabled](#wizard_tk_bridge.wizard_path.PathRow.set_enabled)
* [wizard\_tk\_bridge.wizard\_matrix](#wizard_tk_bridge.wizard_matrix)
  * [MatrixCell](#wizard_tk_bridge.wizard_matrix.MatrixCell)
    * [answer](#wizard_tk_bridge.wizard_matrix.MatrixCell.answer)
    * [error](#wizard_tk_bridge.wizard_matrix.MatrixCell.error)
  * [MatrixEditor](#wizard_tk_bridge.wizard_matrix.MatrixEditor)
    * [\_\_init\_\_](#wizard_tk_bridge.wizard_matrix.MatrixEditor.__init__)
    * [shape](#wizard_tk_bridge.wizard_matrix.MatrixEditor.shape)
    * [answers](#wizard_tk_bridge.wizard_matrix.MatrixEditor.answers)
    * [submit](#wizard_tk_bridge.wizard_matrix.MatrixEditor.submit)
    * [add\_resize\_buttons](#wizard_tk_bridge.wizard_matrix.MatrixEditor.add_resize_buttons)
    * [add\_row](#wizard_tk_bridge.wizard_matrix.MatrixEditor.add_row)
    * [remove\_row](#wizard_tk_bridge.wizard_matrix.MatrixEditor.remove_row)
    * [add\_column](#wizard_tk_bridge.wizard_matrix.MatrixEditor.add_column)
    * [remove\_column](#wizard_tk_bridge.wizard_matrix.MatrixEditor.remove_column)
* [wizard\_tk\_bridge.wizard\_window](#wizard_tk_bridge.wizard_window)
  * [WizardWindow](#wizard_tk_bridge.wizard_window.WizardWindow)
    * [\_\_init\_\_](#wizard_tk_bridge.wizard_window.WizardWindow.__init__)
    * [show](#wizard_tk_bridge.wizard_window.WizardWindow.show)
    * [close](#wizard_tk_bridge.wizard_window.WizardWindow.close)
    * [ask\_text](#wizard_tk_bridge.wizard_window.WizardWindow.ask_text)
    * [ask\_int](#wizard_tk_bridge.wizard_window.WizardWindow.ask_int)
    * [ask\_path](#wizard_tk_bridge.wizard_window.WizardWindow.ask_path)
    * [ask\_form](#wizard_tk_bridge.wizard_window.WizardWindow.ask_form)
    * [ask\_matrix\_form](#wizard_tk_bridge.wizard_window.WizardWindow.ask_matrix_form)
    * [ask\_yes\_no](#wizard_tk_bridge.wizard_window.WizardWindow.ask_yes_no)
    * [ask\_choice](#wizard_tk_bridge.wizard_window.WizardWindow.ask_choice)
    * [ask\_multi](#wizard_tk_bridge.wizard_window.WizardWindow.ask_multi)
    * [ask\_table](#wizard_tk_bridge.wizard_window.WizardWindow.ask_table)

<a id="wizard_tk_bridge.auto_scroll"></a>

# wizard\_tk\_bridge.auto\_scroll

Scroll commands and wheel and touchpad support for an area.

A table that fits its area needs no scrollbar, and a scrollbar that is
always shown wastes space and hints at hidden content that is not there.
:func:`auto_hide` returns the scroll command for a scrolling widget: the
command hides the scrollbar while the whole range is visible and shows it
again once the widget grows past its area. It works for any widget that
reports its position through an ``xscrollcommand`` or ``yscrollcommand``,
so a wizard table's canvas and any other scrolling widget can share it.

Tk binds the mouse wheel and, from Tk 9 on, the touchpad on each of its
scrolling widgets, but binds neither on a canvas. A scrolling area built
from a canvas therefore answers a scroll only while the pointer is over
its scrollbar. :func:`bind_wheel` gives the area both over its content
as well.

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

<a id="wizard_tk_bridge.auto_scroll.bind_wheel"></a>

#### bind\_wheel

```python
def bind_wheel(canvas: tk.Canvas) -> None
```

Let the wheel and the touchpad scroll this canvas from its content.

The binding sits on the window that holds the canvas, and not on the
canvas and the widgets inside it, because those widgets are built and
rebuilt while the user works. The window's handler then finds the
area from the widget the scroll reached, so a single binding per
window serves every area in it.

A touchpad is bound separately from a wheel, as Tk 9 reports the two
as different events, and only Tk 9 knows the touchpad one at all.

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
The difference compared to using StringIO to suppress output is that
the NoTextIO does not store any data, so no matter how much is
written to it, you do not risk running out of memory.

<a id="wizard_tk_bridge._no_text_io.NoTextIO.write"></a>

#### write

```python
@override
def write(s: str) -> int
```

Write a string to the NoTextIO object.

This method does nothing and returns length of the string.

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

<a id="wizard_tk_bridge.wizard_cell"></a>

# wizard\_tk\_bridge.wizard\_cell

The input of one form field or matrix cell, and the editors' layout.

A form row and a matrix cell show the same kinds of input: an entry for
text and integers, a path entry with a Browse button, a check box, a
drop-down, a multi-selection list, and a placeholder entry, with a
calendar Pick button for dates, for the typed values. :func:`build_input`
builds the :class:`CellInput` for one Ask*Cell (every Ask*Field is one
too), which reads the current answer value, reports the input's own
validation error, writes a prefill into the input, and enables or
disables it. The width hint of a cell sizes the text part of its input;
without one a compact input, as in a matrix, gets a narrower default
than a form row. :class:`HelpTooltip` shows a help text on hover,
:func:`scrolled_editor` builds the scrolling area and status line shared
by the form and matrix editors, and :func:`scroll_into_view` scrolls that
area to show one of its widgets.

Turning the raw text of an integer input into its answer is the same job
in a cell and in a standalone question, so :func:`int_answer` lives here
and is shared with the wizard window. Its text counterpart is
:func:`wizard_ui_bridge.bridge_helpers.text_answer`, which every bridge
shares, so a graphical answer is accepted or rejected exactly as a
console one is.

<a id="wizard_tk_bridge.wizard_cell.int_answer"></a>

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

<a id="wizard_tk_bridge.wizard_cell.HelpTooltip"></a>

## HelpTooltip Objects

```python
class HelpTooltip()
```

A hover bubble showing a help text over its widgets.

The bubble is a label placed over the window that holds the bound
widgets, shown when the pointer enters one of them and destroyed
when it leaves, so help appears on hover as it does in the textual
bridge. A window of its own is drawn with the platform's window
shape, which on macOS rounds the corners of a borderless window so
much that a one-line bubble loses its first and last characters. A
placed label is a plain rectangle on every platform, takes neither
focus nor a grab, and cannot outlive the widgets it belongs to.

<a id="wizard_tk_bridge.wizard_cell.HelpTooltip.__init__"></a>

#### \_\_init\_\_

```python
def __init__(text: str, anchor: tk.Widget,
             widgets: Sequence[tk.Widget]) -> None
```

Bind hover show and hide on each widget for the help text.

<a id="wizard_tk_bridge.wizard_cell.HelpTooltip.show"></a>

#### show

```python
def show() -> None
```

Show the help bubble just below the anchor widget.

<a id="wizard_tk_bridge.wizard_cell.HelpTooltip.hide"></a>

#### hide

```python
def hide() -> None
```

Destroy the help bubble when one is shown.

<a id="wizard_tk_bridge.wizard_cell.tooltip_text"></a>

#### tooltip\_text

```python
def tooltip_text(cell: AskCell) -> Optional[str]
```

Return the tooltip text combining help text and format hint.

<a id="wizard_tk_bridge.wizard_cell.CellInput"></a>

## CellInput Objects

```python
@dataclass(frozen=True)
class CellInput()
```

The built input of one field or cell, and how to use it.

widget is the widget to place in a grid. Some inputs keep a handle
of their own besides it: var holds the value of a yes/no check box,
path is the path entry with its Browse button, and typed is the
placeholder entry, with any Pick button, of a typed field or cell.

<a id="wizard_tk_bridge.wizard_cell.CellInput.value"></a>

#### value

```python
def value() -> Optional[PrefillValueType]
```

Return the current answer value read from the input.

An empty input gives the default, or None when there is no
default. Text that is not a valid answer also gives None, and
error() tells why.

<a id="wizard_tk_bridge.wizard_cell.CellInput.error"></a>

#### error

```python
def error() -> Optional[str]
```

Return the input's own validation error, or None when valid.

<a id="wizard_tk_bridge.wizard_cell.CellInput.write"></a>

#### write

```python
def write(value: PrefillValueType) -> None
```

Write a prefill value into the input, even when it is disabled.

The value has been checked against the cell type, see
wizard_ui_bridge.form_helpers.prefill_value().

<a id="wizard_tk_bridge.wizard_cell.CellInput.main_widget"></a>

#### main\_widget

```python
def main_widget() -> tk.Widget
```

Return the widget the user types or clicks in.

That is the text entry of a path or typed input, beside its
button, and otherwise the widget itself. It is the widget to give
the keyboard focus to.

<a id="wizard_tk_bridge.wizard_cell.CellInput.set_width"></a>

#### set\_width

```python
def set_width(width: int) -> None
```

Set the width in characters of the input's text part.

A check box has no text part, so it keeps its size.

<a id="wizard_tk_bridge.wizard_cell.CellInput.set_enabled"></a>

#### set\_enabled

```python
def set_enabled(enabled: bool) -> None
```

Enable or disable the input, keeping a drop-down read-only.

<a id="wizard_tk_bridge.wizard_cell.build_input"></a>

#### build\_input

```python
def build_input(parent: tk.Misc,
                cell: AskCell,
                change: Callable[[], None],
                compact: bool = False) -> CellInput
```

Build the input matching an input cell or field type.

change is called whenever the user changes the input. A label cell
has no input and must not be passed. The width hint of the cell sizes
the text part of the input. Without one, a compact input, as in a
matrix, gets a narrower default width than a form row.

<a id="wizard_tk_bridge.wizard_cell.scrolled_editor"></a>

#### scrolled\_editor

```python
def scrolled_editor(parent: tk.Misc,
                    sideways: bool) -> tuple[tk.Frame, tk.Label]
```

Build an editor's scrolling area and the status line below it.

The inputs of a tall form or matrix would overflow the fixed-size
wizard window, so they sit in a frame inside a scrolling canvas whose
scrollbars appear only when they are needed. With sideways the area
also scrolls horizontally, for a matrix wider than the window. The
status line stays below the scroll area so it is always shown.

**Returns**:

  The frame to grid the inputs into, and the status line label.

<a id="wizard_tk_bridge.wizard_cell.scroll_into_view"></a>

#### scroll\_into\_view

```python
def scroll_into_view(grid: tk.Frame, widget: tk.Widget) -> None
```

Scroll an editor's area as little as needed to show a widget.

grid is the frame returned by scrolled_editor() and widget one that
is gridded into it. A widget larger than the area shows its start.

<a id="wizard_tk_bridge.wizard_cell.view_start"></a>

#### view\_start

```python
def view_start(item: int, size: int, view: float, shown: int) -> float
```

Return the new start of a scrolled view along one axis.

The view starts at view and shows shown pixels. It moves as little
as possible to show the item, of size pixels from item, or the
item's start when the item is larger than the view.

<a id="wizard_tk_bridge.gui_style"></a>

# wizard\_tk\_bridge.gui\_style

Shared look and focus helpers for the Tkinter input windows.

Editable input widgets blend into the window background on some
platforms, so the user cannot tell an entry, drop-down or list from the
surrounding window. :func:`style_input` gives such a widget a white
field and a thin border so it stands out. :func:`choice_combo` builds a
styled read-only drop-down that a nullable choice can empty again.
:func:`focus_first_input` puts the keyboard focus on the first editable
widget of a window, so the user can start typing as soon as the window
opens. :func:`bind_submit` lets Return in an input confirm the prompt.

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

<a id="wizard_tk_bridge.gui_style.choice_combo"></a>

#### choice\_combo

```python
def choice_combo(parent: tk.Misc, choices: Sequence[str], nullable: bool,
                 width: int) -> ttk.Combobox
```

Return a styled read-only drop-down offering choices.

A read-only drop-down cannot be emptied by typing once a value is
picked, so a nullable drop-down leads its list with a blank entry
that empties it again. The drop-down starts empty.

<a id="wizard_tk_bridge.gui_style.focus_first_input"></a>

#### focus\_first\_input

```python
def focus_first_input(window: tk.Misc) -> None
```

Give the keyboard focus to the first editable input, if any.

<a id="wizard_tk_bridge.gui_style.bind_submit"></a>

#### bind\_submit

```python
def bind_submit(widget: tk.Misc, on_ok: Callable[[], None]) -> None
```

Bind Return to the confirm action on every input inside widget.

A prompt builds its inputs before its buttons, so binding them all
from one place gives every prompt the same rule: Return in an input
does what the default OK button does. Only inputs are bound, which
both leaves the Browse, Pick and navigation buttons their own keys
and reaches the entry inside a two-widget input row. An editor that
adds inputs later binds each of them itself when it builds it.

<a id="wizard_tk_bridge.wizard_typed"></a>

# wizard\_tk\_bridge.wizard\_typed

Text parsing and formatting for the typed form fields and cells.

The float, date, time, date-time and duration form fields and matrix
cells each turn user text into a typed value and a typed value back into
text. This module holds that conversion for the Tkinter bridge, together
with the format hints and the parse and range error messages, so the
graphical form and matrix form accept the same text a user would type on
the console. Every Ask*Field derives from its Ask*Cell, so each function
taking a cell takes a field too.

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
def is_typed(field: AskCell) -> bool
```

Return whether field is one of the five typed fields or cells.

<a id="wizard_tk_bridge.wizard_typed.field_hint"></a>

#### field\_hint

```python
def field_hint(field: AskCell) -> str
```

Return the accepted-format hint shown for a typed field or cell.

<a id="wizard_tk_bridge.wizard_typed.default_text"></a>

#### default\_text

```python
def default_text(field: AskCell) -> str
```

Return the starting entry text: the start value, else the default.

<a id="wizard_tk_bridge.wizard_typed.typed_value"></a>

#### typed\_value

```python
def typed_value(field: AskCell, text: str) -> Optional[PrefillValueType]
```

Return the typed value of a typed field for its widget text.

An empty text yields the field default. A non-empty text is parsed;
unparsable or out-of-range text yields None, and the caller reports
the error separately through typed_error().

<a id="wizard_tk_bridge.wizard_typed.typed_error"></a>

#### typed\_error

```python
def typed_error(field: AskCell, text: str) -> Optional[str]
```

Return the parse or range error of a typed field's widget text.

Empty text is accepted when the field is nullable or has a default,
and otherwise reports that a value is required.

<a id="wizard_tk_bridge.wizard_typed.date_of"></a>

#### date\_of

```python
def date_of(value: Optional[object]) -> Optional[date]
```

Return the date part of a date or datetime, or None.

<a id="wizard_tk_bridge.wizard_typed.calendar_seed"></a>

#### calendar\_seed

```python
def calendar_seed(field: AskCell,
                  text: str) -> tuple[date, Optional[date], Optional[date]]
```

Return the calendar seed date and its inclusive day bounds.

A date-time field's bounds are its date parts, so the calendar offers
the acceptable days and the field itself validates the exact value.

<a id="wizard_tk_bridge.wizard_typed.combined_text"></a>

#### combined\_text

```python
def combined_text(field: AskCell, picked: date, current: str) -> str
```

Return the input text for a picked date, keeping any typed time.

<a id="wizard_tk_bridge.wizard_pick_row"></a>

# wizard\_tk\_bridge.wizard\_pick\_row

Placeholder-aware entries for the typed form fields and matrix cells.

The float, time and duration fields and cells are shown as a text entry
that displays its accepted-format hint as greyed placeholder text while
empty, so the user learns the format without cluttering the field label.
A date or date-time field or cell adds a Pick button that opens a month
calendar, and typing the ``?`` token into the entry opens the same
calendar.

:class:`HintEntry` is the placeholder entry, and :class:`PickRow` bundles
one with the calendar button. Both satisfy :class:`TypedInput`, the small
interface a cell input uses to read, write, enable and size a typed
input.

<a id="wizard_tk_bridge.wizard_pick_row.TypedInput"></a>

## TypedInput Objects

```python
class TypedInput(Protocol)
```

The read, write, enable and entry interface of a typed form input.

<a id="wizard_tk_bridge.wizard_pick_row.TypedInput.entry"></a>

#### entry

```python
@property
def entry() -> tk.Entry
```

Return the text entry, for instance to set its width.

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
def __init__(parent: tk.Misc, field: AskCell, hint: str, initial: str,
             on_change: Callable[[], None]) -> None
```

Build the entry and Pick button inside a new frame.

<a id="wizard_tk_bridge.wizard_pick_row.PickRow.entry"></a>

#### entry

```python
@property
def entry() -> tk.Entry
```

Return the text entry beside the Pick button.

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

A whole wizard form shown on one screen.

A form question asks several related fields at once. :class:`FormEditor`
builds a two-column grid, a label on the left and an input widget on the
right, one row per :class:`AskField`. It reads one :class:`AnswerField`
per row, runs the optional partial validator after every change to show
advisory feedback and disable irrelevant rows, and validates every
enabled field on submit so a submitted form is always complete. The input
of each row is a :class:`~wizard_tk_bridge.wizard_cell.CellInput`, the
same input a matrix form shows in a cell.

<a id="wizard_tk_bridge.wizard_form.handles_field"></a>

#### handles\_field

```python
def handles_field(field: AskField) -> bool
```

Return whether the Tk form can show the given field type.

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
picker, ask_form() shows a whole form on one screen so the user
answers related fields together in any order, and ask_matrix_form()
shows a whole grid of cells on one screen the same way. All questions of one
wizard session are answered in a single reused
:class:`~wizard_tk_bridge.wizard_window.WizardWindow`, so the session
does not jump around the display.

The bridge supports three ways an application can show the wizard:

- In a new window of its own: give ``parent``, the Tk widget the new
  window is shown over. This suits an application with other windows.
- Embedded in an area the application already built: give ``area``, the
  frame or other container the wizard should fill instead of a window of
  its own.
- In a window of its own over a hidden root the bridge itself owns: give
  neither ``parent`` nor ``area``. This suits a standalone CLI program
  that has no other Tkinter code.

At most one of ``parent`` and ``area`` may be given.

Whichever of the three is used, ``modal`` decides whether the wizard
grabs its window (or the window containing ``area``) for the duration of
the session, so the rest of that window is unusable meanwhile. The
application is best placed to decide this, since only it knows whether
its other content should stay usable while the wizard runs.

<a id="wizard_tk_bridge.tk_bridge.WizardUiBridgeTk"></a>

## WizardUiBridgeTk Objects

```python
class WizardUiBridgeTk(WizardUiBridge)
```

Bridge that answers wizard prompts through Tkinter widgets.

The ask methods accept help_text but ignore it; ask_form() and
ask_matrix_form() show the help text of each field or cell as a
tooltip instead.

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
             sensitive: bool = False,
             start_value: Optional[str] = None,
             help_text: Optional[str] = None) -> Optional[str]
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
            default: Optional[int] = None,
            start_value: Optional[int] = None,
            help_text: Optional[str] = None) -> Optional[int]
```

Ask for an integer within optional bounds; see ask_int.

<a id="wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.ask_path"></a>

#### ask\_path

```python
def ask_path(question: str,
             re_ask_reason: Optional[str] = None,
             *,
             options: Optional[PathAskOptions] = None,
             help_text: Optional[str] = None) -> Optional[Path]
```

Ask for a path with a native file or directory picker.

<a id="wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.ask_yes_no"></a>

#### ask\_yes\_no

```python
def ask_yes_no(question: str,
               default: bool,
               re_ask_reason: Optional[str] = None,
               *,
               start_value: Optional[bool] = None,
               help_text: Optional[str] = None) -> bool
```

Ask a yes/no question with dedicated yes and no buttons.

The button of the start value, else the default, has the focus.

<a id="wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.ask_choice"></a>

#### ask\_choice

```python
def ask_choice(question: str,
               *,
               choices: Sequence[str],
               default: Optional[str] = None,
               re_ask_reason: Optional[str] = None,
               nullable: bool = False,
               start_value: Optional[str] = None,
               help_text: Optional[str] = None) -> Optional[str]
```

Ask the user to pick one choice from a single-selection list.

A nullable choice is offered with a leading '(none)' entry. The
start value, else the default, is preselected.

<a id="wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.ask_multi"></a>

#### ask\_multi

```python
def ask_multi(question: str,
              *,
              choices: Sequence[str],
              default: Optional[Sequence[str]] = None,
              min_select: int = 0,
              max_select: Optional[int] = None,
              re_ask_reason: Optional[str] = None,
              start_value: Optional[Sequence[str]] = None,
              help_text: Optional[str] = None) -> list[str]
```

Ask the user to pick several choices from a multi-selection list.

The start value, else the default, is preselected.

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
              max_rows: Optional[int] = None,
              help_text: Optional[str] = None) -> list[list[Optional[str]]]
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

<a id="wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.ask_matrix_form"></a>

#### ask\_matrix\_form

```python
def ask_matrix_form(request: MatrixRequest,
                    *,
                    re_ask_reason: Optional[str] = None) -> AnswerCells
```

Ask a whole matrix form on one screen; see ask_matrix_form.

Each AskLabelCell is shown as plain text, in bold or italics when
it asks for it, and every other cell as the input a form field of
its type gets, narrower unless the cell gives a width hint, with
its help text and any format hint as a hover tooltip. When the
minimum and maximum dimensions differ, buttons in the button row
append or delete the last row or column within the bounds; an
appended row or column is scrolled into view and its first input
gets the keyboard focus. The partial validator is called when the
matrix is first shown, with None, after each change of a cell,
with its position, and after each change of the shape, with None.
Its disabled cells are greyed out and its prefills are written
into the inputs. Its message is shown below the matrix, except
for the call when the matrix is first shown. OK first runs the
partial validator, then needs every enabled cell to hold a valid
answer, moving the keyboard focus to the first cell that does not
and naming it by the cell_namer of the request or its labels, and
finally needs the validator to accept the matrix.

<a id="wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.supports_form_field"></a>

#### supports\_form\_field

```python
def supports_form_field(field: AskField) -> bool
```

Report that the Tk form shows every current field type.

This includes a nullable choice field, whose drop-down has a
blank entry that empties it.

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

<a id="wizard_tk_bridge.wizard_path.PathRow.entry"></a>

#### entry

```python
@property
def entry() -> tk.Entry
```

Return the path entry beside the Browse button.

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

<a id="wizard_tk_bridge.wizard_matrix"></a>

# wizard\_tk\_bridge.wizard\_matrix

A whole matrix form shown on one screen.

A matrix form asks a grid of cells at once. :class:`MatrixEditor` builds
one widget per cell of the current shape: a plain label for an
AskLabelCell, in bold or italics when the cell asks for it, and for
every other cell a compact :class:`~wizard_tk_bridge.wizard_cell.CellInput`,
the same input a form row shows but narrower by default. It reads the
answers of the current shape and runs the optional partial validator
when the matrix is first shown and after every change of a cell and of
the shape, to disable irrelevant cells, apply prefills and show advisory
feedback. Its message is first shown once the user changes the matrix or
submits it, so a fresh matrix does not open with a complaint. On submit
every enabled cell is validated, so a submitted matrix is always
complete, and the keyboard focus moves to the first cell that fails its
own check. Such a cell is named in the message by the CellNamer of the
request, or else by its labels.

When the minimum and maximum dimensions of a request differ,
:meth:`MatrixEditor.add_resize_buttons` adds buttons that append or
delete the last row or column, each greyed out at its bound. An appended
row or column is scrolled into view and its first enabled input gets the
keyboard focus, as does the new last row or column when the focus was in
a deleted one. Return in an input submits the matrix, also in a row or
column added later, since each input is bound when it is built.

<a id="wizard_tk_bridge.wizard_matrix.MatrixCell"></a>

## MatrixCell Objects

```python
@dataclass(frozen=True)
class MatrixCell()
```

One built matrix cell: its AskCell, widget, input and tooltip.

A label cell has no input.

<a id="wizard_tk_bridge.wizard_matrix.MatrixCell.answer"></a>

#### answer

```python
def answer() -> Optional[AnswerCell]
```

Return the current answer of the cell, or None for a label.

<a id="wizard_tk_bridge.wizard_matrix.MatrixCell.error"></a>

#### error

```python
def error() -> Optional[str]
```

Return the cell's own validation error, or None when valid.

<a id="wizard_tk_bridge.wizard_matrix.MatrixEditor"></a>

## MatrixEditor Objects

```python
class MatrixEditor()
```

A grid of label and input cells that asks a whole matrix form.

<a id="wizard_tk_bridge.wizard_matrix.MatrixEditor.__init__"></a>

#### \_\_init\_\_

```python
def __init__(parent: tk.Misc, request: MatrixRequest,
             on_submit: Callable[[AnswerCells], None]) -> None
```

Build the cells of the default shape, plus a status line.

<a id="wizard_tk_bridge.wizard_matrix.MatrixEditor.shape"></a>

#### shape

```python
@property
def shape() -> MatrixDimension
```

Return the current number of rows and columns.

<a id="wizard_tk_bridge.wizard_matrix.MatrixEditor.answers"></a>

#### answers

```python
def answers() -> list[list[Optional[AnswerCell]]]
```

Return the current answers, one list per row of the shape.

<a id="wizard_tk_bridge.wizard_matrix.MatrixEditor.submit"></a>

#### submit

```python
def submit() -> None
```

Validate the whole matrix and submit its answers when valid.

The partial validator runs first, so the cells it disables are not
checked. Every enabled cell must then pass its own check, and the
first that does not gets the keyboard focus. Last the validator
must accept the matrix.

<a id="wizard_tk_bridge.wizard_matrix.MatrixEditor.add_resize_buttons"></a>

#### add\_resize\_buttons

```python
def add_resize_buttons(box: tk.Frame) -> None
```

Add the buttons that append or delete the last row or column.

Only a dimension whose minimum and maximum differ gets buttons.

<a id="wizard_tk_bridge.wizard_matrix.MatrixEditor.add_row"></a>

#### add\_row

```python
def add_row() -> None
```

Append a row of fresh cells, up to the maximum row count.

<a id="wizard_tk_bridge.wizard_matrix.MatrixEditor.remove_row"></a>

#### remove\_row

```python
def remove_row() -> None
```

Delete the last row, down to the minimum row count.

<a id="wizard_tk_bridge.wizard_matrix.MatrixEditor.add_column"></a>

#### add\_column

```python
def add_column() -> None
```

Append a column of fresh cells, up to the maximum column count.

<a id="wizard_tk_bridge.wizard_matrix.MatrixEditor.remove_column"></a>

#### remove\_column

```python
def remove_column() -> None
```

Delete the last column, down to the minimum column count.

<a id="wizard_tk_bridge.wizard_window"></a>

# wizard\_tk\_bridge.wizard\_window

A Tk host that asks every wizard prompt in turn, one at a time.

:class:`WizardWindow` lays out one question at a time: a text entry, an
integer entry, a path entry with a native Browse button, a yes/no button
pair, a single- and a multi-selection list, an editable table, a whole
form and a whole matrix form on one screen, kept below a lasting message
area. Every prompt also
offers back, out-one-level and abort buttons, which raise the matching
:class:`WizardNavigation` request so the wizard can step within its
questions or be abandoned.

Return pressed in an input confirms the prompt, exactly as its OK button
does, which that button shows by being the marked default one. The
editable table is the exception: a row added after the buttons were built
would miss the binding, so a table is confirmed by its button alone. A
matrix form binds Return in each input as it builds it, so a row or
column it adds later confirms the matrix too.

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
             sensitive: bool = False,
             start: Optional[str] = None) -> Optional[str]
```

Ask one free-text question and return the entered text.

A sensitive question masks the typed text. The entry is pre-filled
with start, else default, and a default is returned when the
answer is left empty.

<a id="wizard_tk_bridge.wizard_window.WizardWindow.ask_int"></a>

#### ask\_int

```python
def ask_int(question: str,
            re_ask: Optional[str],
            nullable: bool,
            min_value: Optional[int],
            max_value: Optional[int],
            default: Optional[int],
            start: Optional[int] = None) -> Optional[int]
```

Ask one integer question, re-asking until it is in range.

The entry is pre-filled with start, else default.

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

<a id="wizard_tk_bridge.wizard_window.WizardWindow.ask_matrix_form"></a>

#### ask\_matrix\_form

```python
def ask_matrix_form(request: MatrixRequest,
                    re_ask: Optional[str]) -> AnswerCells
```

Ask a whole matrix form on one screen and return its answers.

The matrix editor binds Return in each input itself, also in a
row or column added later, so the content is not bound here.

<a id="wizard_tk_bridge.wizard_window.WizardWindow.ask_yes_no"></a>

#### ask\_yes\_no

```python
def ask_yes_no(question: str, start: bool, re_ask: Optional[str]) -> bool
```

Ask one yes/no question with dedicated buttons.

The button of start has the focus when the question starts.

<a id="wizard_tk_bridge.wizard_window.WizardWindow.ask_choice"></a>

#### ask\_choice

```python
def ask_choice(question: str,
               choices: Sequence[str],
               start: Optional[str],
               re_ask: Optional[str],
               nullable: bool = False) -> Optional[str]
```

Ask the user to pick exactly one choice and return it.

The choice start is preselected. A nullable choice is offered with
a leading '(none)' entry that selects no choice, reported as None,
and is preselected when start is None.

<a id="wizard_tk_bridge.wizard_window.WizardWindow.ask_multi"></a>

#### ask\_multi

```python
def ask_multi(question: str, choices: Sequence[str],
              start: Optional[Sequence[str]], min_select: int,
              max_select: Optional[int], re_ask: Optional[str]) -> list[str]
```

Ask the user to pick several choices within the count bounds.

The choices in start are preselected.

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

