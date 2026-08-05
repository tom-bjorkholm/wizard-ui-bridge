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
    * [\_\_enter\_\_](#wizard_tk_bridge._no_text_io.NoTextIO.__enter__)
    * [\_\_exit\_\_](#wizard_tk_bridge._no_text_io.NoTextIO.__exit__)
* [wizard\_tk\_bridge.gui\_style](#wizard_tk_bridge.gui_style)
  * [style\_input](#wizard_tk_bridge.gui_style.style_input)
  * [\_style\_combobox](#wizard_tk_bridge.gui_style._style_combobox)
  * [focus\_first\_input](#wizard_tk_bridge.gui_style.focus_first_input)
  * [\_first\_input](#wizard_tk_bridge.gui_style._first_input)
  * [\_is\_input](#wizard_tk_bridge.gui_style._is_input)
* [wizard\_tk\_bridge.wizard\_typed](#wizard_tk_bridge.wizard_typed)
  * [parse\_float](#wizard_tk_bridge.wizard_typed.parse_float)
  * [parse\_date](#wizard_tk_bridge.wizard_typed.parse_date)
  * [parse\_time](#wizard_tk_bridge.wizard_typed.parse_time)
  * [parse\_datetime](#wizard_tk_bridge.wizard_typed.parse_datetime)
  * [parse\_duration](#wizard_tk_bridge.wizard_typed.parse_duration)
  * [\_seconds\_delta](#wizard_tk_bridge.wizard_typed._seconds_delta)
  * [\_parts\_delta](#wizard_tk_bridge.wizard_typed._parts_delta)
  * [format\_duration](#wizard_tk_bridge.wizard_typed.format_duration)
  * [format\_value](#wizard_tk_bridge.wizard_typed.format_value)
  * [ordered\_range\_error](#wizard_tk_bridge.wizard_typed.ordered_range_error)
  * [is\_typed](#wizard_tk_bridge.wizard_typed.is_typed)
  * [field\_hint](#wizard_tk_bridge.wizard_typed.field_hint)
  * [\_default\_of](#wizard_tk_bridge.wizard_typed._default_of)
  * [\_resolve](#wizard_tk_bridge.wizard_typed._resolve)
  * [\_checked](#wizard_tk_bridge.wizard_typed._checked)
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
    * [\_show\_hint](#wizard_tk_bridge.wizard_pick_row.HintEntry._show_hint)
    * [\_focus\_in](#wizard_tk_bridge.wizard_pick_row.HintEntry._focus_in)
    * [\_focus\_out](#wizard_tk_bridge.wizard_pick_row.HintEntry._focus_out)
  * [PickRow](#wizard_tk_bridge.wizard_pick_row.PickRow)
    * [\_\_init\_\_](#wizard_tk_bridge.wizard_pick_row.PickRow.__init__)
    * [text](#wizard_tk_bridge.wizard_pick_row.PickRow.text)
    * [set\_text](#wizard_tk_bridge.wizard_pick_row.PickRow.set_text)
    * [set\_enabled](#wizard_tk_bridge.wizard_pick_row.PickRow.set_enabled)
    * [\_changed](#wizard_tk_bridge.wizard_pick_row.PickRow._changed)
    * [\_open\_calendar](#wizard_tk_bridge.wizard_pick_row.PickRow._open_calendar)
    * [\_picked](#wizard_tk_bridge.wizard_pick_row.PickRow._picked)
* [wizard\_tk\_bridge.wizard\_calendar](#wizard_tk_bridge.wizard_calendar)
  * [month\_weeks](#wizard_tk_bridge.wizard_calendar.month_weeks)
  * [shift\_month](#wizard_tk_bridge.wizard_calendar.shift_month)
  * [day\_out\_of\_range](#wizard_tk_bridge.wizard_calendar.day_out_of_range)
  * [\_held\_grab](#wizard_tk_bridge.wizard_calendar._held_grab)
  * [\_restore\_grab](#wizard_tk_bridge.wizard_calendar._restore_grab)
  * [CalendarPicker](#wizard_tk_bridge.wizard_calendar.CalendarPicker)
    * [\_\_init\_\_](#wizard_tk_bridge.wizard_calendar.CalendarPicker.__init__)
    * [\_grab](#wizard_tk_bridge.wizard_calendar.CalendarPicker._grab)
    * [\_add\_nav](#wizard_tk_bridge.wizard_calendar.CalendarPicker._add_nav)
    * [\_navigate](#wizard_tk_bridge.wizard_calendar.CalendarPicker._navigate)
    * [\_show\_month](#wizard_tk_bridge.wizard_calendar.CalendarPicker._show_month)
    * [\_place\_days](#wizard_tk_bridge.wizard_calendar.CalendarPicker._place_days)
    * [\_day\_widget](#wizard_tk_bridge.wizard_calendar.CalendarPicker._day_widget)
    * [\_pick](#wizard_tk_bridge.wizard_calendar.CalendarPicker._pick)
    * [\_cancel](#wizard_tk_bridge.wizard_calendar.CalendarPicker._cancel)
    * [\_finish](#wizard_tk_bridge.wizard_calendar.CalendarPicker._finish)
* [wizard\_tk\_bridge.close\_binding](#wizard_tk_bridge.close_binding)
  * [\_close\_events](#wizard_tk_bridge.close_binding._close_events)
  * [\_perform\_close](#wizard_tk_bridge.close_binding._perform_close)
  * [bind\_close](#wizard_tk_bridge.close_binding.bind_close)
* [wizard\_tk\_bridge.wizard\_table](#wizard_tk_bridge.wizard_table)
  * [\_uniform](#wizard_tk_bridge.wizard_table._uniform)
  * [\_new\_row\_template](#wizard_tk_bridge.wizard_table._new_row_template)
  * [Cell](#wizard_tk_bridge.wizard_table.Cell)
  * [\_cell\_text](#wizard_tk_bridge.wizard_table._cell_text)
  * [TableEditor](#wizard_tk_bridge.wizard_table.TableEditor)
    * [\_\_init\_\_](#wizard_tk_bridge.wizard_table.TableEditor.__init__)
    * [is\_variable](#wizard_tk_bridge.wizard_table.TableEditor.is_variable)
    * [values](#wizard_tk_bridge.wizard_table.TableEditor.values)
    * [add\_row](#wizard_tk_bridge.wizard_table.TableEditor.add_row)
    * [remove\_row](#wizard_tk_bridge.wizard_table.TableEditor.remove_row)
    * [\_build\_scroll](#wizard_tk_bridge.wizard_table.TableEditor._build_scroll)
    * [\_pack\_box](#wizard_tk_bridge.wizard_table.TableEditor._pack_box)
    * [\_add\_vertical](#wizard_tk_bridge.wizard_table.TableEditor._add_vertical)
    * [\_inner\_frame](#wizard_tk_bridge.wizard_table.TableEditor._inner_frame)
    * [\_resize](#wizard_tk_bridge.wizard_table.TableEditor._resize)
    * [\_scroll\_to\_end](#wizard_tk_bridge.wizard_table.TableEditor._scroll_to_end)
    * [\_build\_header](#wizard_tk_bridge.wizard_table.TableEditor._build_header)
    * [\_append\_cells](#wizard_tk_bridge.wizard_table.TableEditor._append_cells)
    * [\_build\_cell](#wizard_tk_bridge.wizard_table.TableEditor._build_cell)
    * [\_editable\_widget](#wizard_tk_bridge.wizard_table.TableEditor._editable_widget)
    * [\_bind\_change](#wizard_tk_bridge.wizard_table.TableEditor._bind_change)
    * [\_feedback](#wizard_tk_bridge.wizard_table.TableEditor._feedback)
    * [\_show](#wizard_tk_bridge.wizard_table.TableEditor._show)
* [wizard\_tk\_bridge.wizard\_form](#wizard_tk_bridge.wizard_form)
  * [handles\_field](#wizard_tk_bridge.wizard_form.handles_field)
  * [int\_answer](#wizard_tk_bridge.wizard_form.int_answer)
  * [\_Input](#wizard_tk_bridge.wizard_form._Input)
  * [HelpTooltip](#wizard_tk_bridge.wizard_form.HelpTooltip)
    * [\_\_init\_\_](#wizard_tk_bridge.wizard_form.HelpTooltip.__init__)
    * [show](#wizard_tk_bridge.wizard_form.HelpTooltip.show)
    * [hide](#wizard_tk_bridge.wizard_form.HelpTooltip.hide)
    * [\_geometry](#wizard_tk_bridge.wizard_form.HelpTooltip._geometry)
  * [FormRow](#wizard_tk_bridge.wizard_form.FormRow)
  * [\_text\_input](#wizard_tk_bridge.wizard_form._text_input)
  * [\_int\_input](#wizard_tk_bridge.wizard_form._int_input)
  * [\_path\_input](#wizard_tk_bridge.wizard_form._path_input)
  * [\_yes\_no\_input](#wizard_tk_bridge.wizard_form._yes_no_input)
  * [\_choice\_input](#wizard_tk_bridge.wizard_form._choice_input)
  * [\_multi\_input](#wizard_tk_bridge.wizard_form._multi_input)
  * [\_preselect](#wizard_tk_bridge.wizard_form._preselect)
  * [\_hint\_input](#wizard_tk_bridge.wizard_form._hint_input)
  * [\_pick\_input](#wizard_tk_bridge.wizard_form._pick_input)
  * [\_typed\_input](#wizard_tk_bridge.wizard_form._typed_input)
  * [\_basic\_input](#wizard_tk_bridge.wizard_form._basic_input)
  * [\_make\_input](#wizard_tk_bridge.wizard_form._make_input)
  * [\_entry\_widget](#wizard_tk_bridge.wizard_form._entry_widget)
  * [\_int\_value](#wizard_tk_bridge.wizard_form._int_value)
  * [\_path\_value](#wizard_tk_bridge.wizard_form._path_value)
  * [\_choice\_value](#wizard_tk_bridge.wizard_form._choice_value)
  * [\_multi\_selected](#wizard_tk_bridge.wizard_form._multi_selected)
  * [\_multi\_values](#wizard_tk_bridge.wizard_form._multi_values)
  * [\_int\_error](#wizard_tk_bridge.wizard_form._int_error)
  * [\_multi\_error](#wizard_tk_bridge.wizard_form._multi_error)
  * [\_set\_widget\_state](#wizard_tk_bridge.wizard_form._set_widget_state)
  * [\_enable\_row](#wizard_tk_bridge.wizard_form._enable_row)
  * [\_hint\_note](#wizard_tk_bridge.wizard_form._hint_note)
  * [\_tooltip\_text](#wizard_tk_bridge.wizard_form._tooltip_text)
  * [\_row\_tooltip](#wizard_tk_bridge.wizard_form._row_tooltip)
  * [\_set\_entry\_text](#wizard_tk_bridge.wizard_form._set_entry_text)
  * [\_set\_combo](#wizard_tk_bridge.wizard_form._set_combo)
  * [\_set\_multi](#wizard_tk_bridge.wizard_form._set_multi)
  * [\_basic\_answer](#wizard_tk_bridge.wizard_form._basic_answer)
  * [\_basic\_error](#wizard_tk_bridge.wizard_form._basic_error)
  * [\_row\_error](#wizard_tk_bridge.wizard_form._row_error)
  * [\_with\_label](#wizard_tk_bridge.wizard_form._with_label)
  * [FormEditor](#wizard_tk_bridge.wizard_form.FormEditor)
    * [\_\_init\_\_](#wizard_tk_bridge.wizard_form.FormEditor.__init__)
    * [\_scroll\_area](#wizard_tk_bridge.wizard_form.FormEditor._scroll_area)
    * [\_apply\_initial](#wizard_tk_bridge.wizard_form.FormEditor._apply_initial)
    * [\_apply\_prefills](#wizard_tk_bridge.wizard_form.FormEditor._apply_prefills)
    * [\_write\_value](#wizard_tk_bridge.wizard_form.FormEditor._write_value)
    * [\_build\_row](#wizard_tk_bridge.wizard_form.FormEditor._build_row)
    * [answers](#wizard_tk_bridge.wizard_form.FormEditor.answers)
    * [submit](#wizard_tk_bridge.wizard_form.FormEditor.submit)
    * [\_validator\_blocks](#wizard_tk_bridge.wizard_form.FormEditor._validator_blocks)
    * [\_changed](#wizard_tk_bridge.wizard_form.FormEditor._changed)
    * [\_feedback](#wizard_tk_bridge.wizard_form.FormEditor._feedback)
    * [\_run\_validator](#wizard_tk_bridge.wizard_form.FormEditor._run_validator)
    * [\_first\_error](#wizard_tk_bridge.wizard_form.FormEditor._first_error)
    * [\_apply\_disabled](#wizard_tk_bridge.wizard_form.FormEditor._apply_disabled)
    * [\_show](#wizard_tk_bridge.wizard_form.FormEditor._show)
    * [\_read](#wizard_tk_bridge.wizard_form.FormEditor._read)
    * [\_field\_error](#wizard_tk_bridge.wizard_form.FormEditor._field_error)
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
    * [\_window\_obj](#wizard_tk_bridge.tk_bridge.WizardUiBridgeTk._window_obj)
* [wizard\_tk\_bridge.wizard\_path](#wizard_tk_bridge.wizard_path)
  * [\_is\_dir\_kind](#wizard_tk_bridge.wizard_path._is_dir_kind)
  * [pick\_path](#wizard_tk_bridge.wizard_path.pick_path)
  * [\_start\_location](#wizard_tk_bridge.wizard_path._start_location)
  * [\_open\_dialog](#wizard_tk_bridge.wizard_path._open_dialog)
  * [PathRow](#wizard_tk_bridge.wizard_path.PathRow)
    * [\_\_init\_\_](#wizard_tk_bridge.wizard_path.PathRow.__init__)
    * [get](#wizard_tk_bridge.wizard_path.PathRow.get)
    * [set\_text](#wizard_tk_bridge.wizard_path.PathRow.set_text)
    * [set\_enabled](#wizard_tk_bridge.wizard_path.PathRow.set_enabled)
    * [bind\_return](#wizard_tk_bridge.wizard_path.PathRow.bind_return)
    * [\_browse](#wizard_tk_bridge.wizard_path.PathRow._browse)
* [wizard\_tk\_bridge.wizard\_window](#wizard_tk_bridge.wizard_window)
  * [\_default\_path\_text](#wizard_tk_bridge.wizard_window._default_path_text)
  * [WizardWindow](#wizard_tk_bridge.wizard_window.WizardWindow)
    * [\_\_init\_\_](#wizard_tk_bridge.wizard_window.WizardWindow.__init__)
    * [\_build\_toplevel](#wizard_tk_bridge.wizard_window.WizardWindow._build_toplevel)
    * [\_build\_messages](#wizard_tk_bridge.wizard_window.WizardWindow._build_messages)
    * [show](#wizard_tk_bridge.wizard_window.WizardWindow.show)
    * [close](#wizard_tk_bridge.wizard_window.WizardWindow.close)
    * [ask\_text](#wizard_tk_bridge.wizard_window.WizardWindow.ask_text)
    * [\_text\_result](#wizard_tk_bridge.wizard_window.WizardWindow._text_result)
    * [ask\_int](#wizard_tk_bridge.wizard_window.WizardWindow.ask_int)
    * [\_run\_int](#wizard_tk_bridge.wizard_window.WizardWindow._run_int)
    * [ask\_path](#wizard_tk_bridge.wizard_window.WizardWindow.ask_path)
    * [\_run\_path](#wizard_tk_bridge.wizard_window.WizardWindow._run_path)
    * [ask\_form](#wizard_tk_bridge.wizard_window.WizardWindow.ask_form)
    * [ask\_yes\_no](#wizard_tk_bridge.wizard_window.WizardWindow.ask_yes_no)
    * [ask\_choice](#wizard_tk_bridge.wizard_window.WizardWindow.ask_choice)
    * [ask\_multi](#wizard_tk_bridge.wizard_window.WizardWindow.ask_multi)
    * [ask\_table](#wizard_tk_bridge.wizard_window.WizardWindow.ask_table)
    * [\_run\_multi](#wizard_tk_bridge.wizard_window.WizardWindow._run_multi)
    * [\_choice\_list](#wizard_tk_bridge.wizard_window.WizardWindow._choice_list)
    * [\_preset\_indexes](#wizard_tk_bridge.wizard_window.WizardWindow._preset_indexes)
    * [\_pick\_one](#wizard_tk_bridge.wizard_window.WizardWindow._pick_one)
    * [\_pick\_many](#wizard_tk_bridge.wizard_window.WizardWindow._pick_many)
    * [\_begin](#wizard_tk_bridge.wizard_window.WizardWindow._begin)
    * [\_add\_label](#wizard_tk_bridge.wizard_window.WizardWindow._add_label)
    * [\_add\_buttons](#wizard_tk_bridge.wizard_window.WizardWindow._add_buttons)
    * [\_add\_table\_buttons](#wizard_tk_bridge.wizard_window.WizardWindow._add_table_buttons)
    * [\_add\_nav\_buttons](#wizard_tk_bridge.wizard_window.WizardWindow._add_nav_buttons)
    * [\_wait](#wizard_tk_bridge.wizard_window.WizardWindow._wait)
    * [\_finish](#wizard_tk_bridge.wizard_window.WizardWindow._finish)
    * [\_back](#wizard_tk_bridge.wizard_window.WizardWindow._back)
    * [\_cancel\_level](#wizard_tk_bridge.wizard_window.WizardWindow._cancel_level)
    * [\_cancel](#wizard_tk_bridge.wizard_window.WizardWindow._cancel)
    * [\_navigate](#wizard_tk_bridge.wizard_window.WizardWindow._navigate)
    * [\_grab](#wizard_tk_bridge.wizard_window.WizardWindow._grab)

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

<a id="wizard_tk_bridge._no_text_io.NoTextIO.__enter__"></a>

#### \_\_enter\_\_

```python
@override
def __enter__() -> 'NoTextIO'
```

Enter the NoTextIO object.

This method does nothing and returns the NoTextIO object.

<a id="wizard_tk_bridge._no_text_io.NoTextIO.__exit__"></a>

#### \_\_exit\_\_

```python
@override
def __exit__(exc_type: Optional[type[BaseException]],
             exc_value: Optional[BaseException],
             traceback: Optional[TracebackType]) -> None
```

Exit the NoTextIO object.

This method does nothing.

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

<a id="wizard_tk_bridge.gui_style._style_combobox"></a>

#### \_style\_combobox

```python
def _style_combobox(widget: ttk.Combobox) -> None
```

Give a drop-down a white field through a shared ttk style.

<a id="wizard_tk_bridge.gui_style.focus_first_input"></a>

#### focus\_first\_input

```python
def focus_first_input(window: tk.Misc) -> None
```

Give the keyboard focus to the first editable input, if any.

<a id="wizard_tk_bridge.gui_style._first_input"></a>

#### \_first\_input

```python
def _first_input(parent: tk.Misc) -> Optional[tk.Misc]
```

Return the first editable input under parent, in child order.

<a id="wizard_tk_bridge.gui_style._is_input"></a>

#### \_is\_input

```python
def _is_input(widget: tk.Misc) -> bool
```

Return whether the widget is an editable input to fill in.

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

<a id="wizard_tk_bridge.wizard_typed._seconds_delta"></a>

#### \_seconds\_delta

```python
def _seconds_delta(seconds: float) -> Optional[timedelta]
```

Return a duration of seconds seconds, or None when unusable.

<a id="wizard_tk_bridge.wizard_typed._parts_delta"></a>

#### \_parts\_delta

```python
def _parts_delta(groups: tuple[Optional[str], ...]) -> Optional[timedelta]
```

Return a duration built from matched day and clock groups.

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

<a id="wizard_tk_bridge.wizard_typed._default_of"></a>

#### \_default\_of

```python
def _default_of(field: AskField) -> Optional[object]
```

Return the default of a typed field.

<a id="wizard_tk_bridge.wizard_typed._resolve"></a>

#### \_resolve

```python
def _resolve(field: AskField,
             text: str) -> tuple[Optional[object], Optional[str]]
```

Return a typed field's parsed value and any parse or range error.

<a id="wizard_tk_bridge.wizard_typed._checked"></a>

#### \_checked

```python
def _checked(
        value: Optional[_Ordered], field: AskField,
        minimum: Optional[_Ordered],
        maximum: Optional[_Ordered]) -> tuple[Optional[object], Optional[str]]
```

Return value and no error, or None and the reason it is unusable.

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

<a id="wizard_tk_bridge.wizard_pick_row.HintEntry._show_hint"></a>

#### \_show\_hint

```python
def _show_hint() -> None
```

Show the greyed placeholder hint in the empty entry.

<a id="wizard_tk_bridge.wizard_pick_row.HintEntry._focus_in"></a>

#### \_focus\_in

```python
def _focus_in() -> None
```

Clear the greyed hint when the entry gains focus.

<a id="wizard_tk_bridge.wizard_pick_row.HintEntry._focus_out"></a>

#### \_focus\_out

```python
def _focus_out() -> None
```

Restore the greyed hint when the entry is left empty.

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

<a id="wizard_tk_bridge.wizard_pick_row.PickRow._changed"></a>

#### \_changed

```python
def _changed() -> None
```

React to typing, opening the calendar on the pick token.

<a id="wizard_tk_bridge.wizard_pick_row.PickRow._open_calendar"></a>

#### \_open\_calendar

```python
def _open_calendar() -> None
```

Open the month calendar seeded from the current value.

<a id="wizard_tk_bridge.wizard_pick_row.PickRow._picked"></a>

#### \_picked

```python
def _picked(picked: Optional[date]) -> None
```

Write a picked date into the entry, keeping any typed time.

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

<a id="wizard_tk_bridge.wizard_calendar._held_grab"></a>

#### \_held\_grab

```python
def _held_grab(widget: tk.Misc) -> bool
```

Return whether widget's own window currently holds the app grab.

<a id="wizard_tk_bridge.wizard_calendar._restore_grab"></a>

#### \_restore\_grab

```python
def _restore_grab(widget: Optional[tk.Misc]) -> None
```

Give the modal grab back to the widget's window, if it survives.

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

<a id="wizard_tk_bridge.wizard_calendar.CalendarPicker._grab"></a>

#### \_grab

```python
def _grab() -> None
```

Take the modal grab and focus, retrying until the window shows.

Grabbing fails while the new window is not yet viewable, so it is
retried on the wizard's event loop until it succeeds.

<a id="wizard_tk_bridge.wizard_calendar.CalendarPicker._add_nav"></a>

#### \_add\_nav

```python
def _add_nav() -> None
```

Add the previous and next month and year navigation buttons.

<a id="wizard_tk_bridge.wizard_calendar.CalendarPicker._navigate"></a>

#### \_navigate

```python
def _navigate(action: str) -> None
```

Move the shown month by one navigation action and redraw.

<a id="wizard_tk_bridge.wizard_calendar.CalendarPicker._show_month"></a>

#### \_show\_month

```python
def _show_month() -> None
```

Show the current month's title and rebuild the day grid.

<a id="wizard_tk_bridge.wizard_calendar.CalendarPicker._place_days"></a>

#### \_place\_days

```python
def _place_days() -> None
```

Place one day button, or a blank cell, per day of the month.

<a id="wizard_tk_bridge.wizard_calendar.CalendarPicker._day_widget"></a>

#### \_day\_widget

```python
def _day_widget(day: int) -> tk.Widget
```

Return a blank cell for a padding day, else a day button.

<a id="wizard_tk_bridge.wizard_calendar.CalendarPicker._pick"></a>

#### \_pick

```python
def _pick(day: int) -> None
```

Return the clicked day's date and close the calendar.

<a id="wizard_tk_bridge.wizard_calendar.CalendarPicker._cancel"></a>

#### \_cancel

```python
def _cancel() -> None
```

Close the calendar without returning a date.

<a id="wizard_tk_bridge.wizard_calendar.CalendarPicker._finish"></a>

#### \_finish

```python
def _finish(chosen: Optional[date]) -> None
```

Report the outcome, destroy the window and restore the grab.

<a id="wizard_tk_bridge.close_binding"></a>

# wizard\_tk\_bridge.close\_binding

Bind the close-window key to a secondary window's close action.

On macOS the Tk toolkit does not close a window when the user presses
Cmd-W, so every secondary window binds that key here. Cmd-W is bound on
every platform, where it is harmless without a Command key, and Ctrl-W is
added on Windows, its customary close-window shortcut. The bound action
defaults to destroying the window but may be the window's own cancel or
abort handler, so the key behaves exactly like the window close button.

<a id="wizard_tk_bridge.close_binding._close_events"></a>

#### \_close\_events

```python
def _close_events() -> list[str]
```

Return the key patterns that close a window on this platform.

<a id="wizard_tk_bridge.close_binding._perform_close"></a>

#### \_perform\_close

```python
def _perform_close(win: tk.Toplevel,
                   on_close: Optional[Callable[[], None]]) -> str
```

Run the window's close action and stop further event handling.

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

<a id="wizard_tk_bridge.wizard_table._uniform"></a>

#### \_uniform

```python
def _uniform(values: list[_V], default: _V) -> _V
```

Return the value shared by every entry, or the default.

<a id="wizard_tk_bridge.wizard_table._new_row_template"></a>

#### \_new\_row\_template

```python
def _new_row_template(columns: Sequence[TableColumn],
                      rows: Sequence[Sequence[TableCell]]) -> list[TableCell]
```

Return the cell descriptors used for rows added at run time.

For each column the new cell keeps the value, choices and nullable
flag shared by every seed cell of that column, and falls back to an
empty string, no choices and not-nullable when they differ. A cell in
an added row is always editable, even in a read-only column.

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

<a id="wizard_tk_bridge.wizard_table._cell_text"></a>

#### \_cell\_text

```python
def _cell_text(cell: Cell) -> Optional[str]
```

Return the final string a cell holds, or None for an empty cell.

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

<a id="wizard_tk_bridge.wizard_table.TableEditor._build_scroll"></a>

#### \_build\_scroll

```python
def _build_scroll(parent: tk.Misc) -> tk.Frame
```

Build a scrolling area and return its inner grid frame.

Every table scrolls horizontally through an auto-hiding scrollbar
so a table wider than the window stays reachable. A variable table
also scrolls vertically within a fixed height, while a fixed table
grows to show all of its rows.

<a id="wizard_tk_bridge.wizard_table.TableEditor._pack_box"></a>

#### \_pack\_box

```python
def _pack_box(box: tk.Frame) -> None
```

Pack the scroll box, expanding a variable table to the window.

<a id="wizard_tk_bridge.wizard_table.TableEditor._add_vertical"></a>

#### \_add\_vertical

```python
def _add_vertical(box: tk.Frame, canvas: tk.Canvas) -> None
```

Give a variable table a fixed height and a vertical scrollbar.

<a id="wizard_tk_bridge.wizard_table.TableEditor._inner_frame"></a>

#### \_inner\_frame

```python
def _inner_frame(canvas: tk.Canvas) -> tk.Frame
```

Create the grid frame inside the canvas and track its size.

<a id="wizard_tk_bridge.wizard_table.TableEditor._resize"></a>

#### \_resize

```python
def _resize(canvas: tk.Canvas, inner: tk.Frame) -> None
```

Track the scroll region and fit a fixed table to its rows.

<a id="wizard_tk_bridge.wizard_table.TableEditor._scroll_to_end"></a>

#### \_scroll\_to\_end

```python
def _scroll_to_end() -> None
```

Bring the newly added last row into the scrolling area.

<a id="wizard_tk_bridge.wizard_table.TableEditor._build_header"></a>

#### \_build\_header

```python
def _build_header() -> None
```

Show one bold heading label per column.

<a id="wizard_tk_bridge.wizard_table.TableEditor._append_cells"></a>

#### \_append\_cells

```python
def _append_cells(row: Sequence[TableCell], added: bool) -> None
```

Build and store one widget per column of one new table row.

<a id="wizard_tk_bridge.wizard_table.TableEditor._build_cell"></a>

#### \_build\_cell

```python
def _build_cell(index: int, col: int, pair: tuple[TableColumn, TableCell],
                added: bool) -> Cell
```

Build one read-only label or one editable cell widget.

<a id="wizard_tk_bridge.wizard_table.TableEditor._editable_widget"></a>

#### \_editable\_widget

```python
def _editable_widget(cell: TableCell) -> tk.Widget
```

Return a drop-down for a cell with choices, else a text entry.

<a id="wizard_tk_bridge.wizard_table.TableEditor._bind_change"></a>

#### \_bind\_change

```python
def _bind_change(widget: tk.Widget, row: int, col: int) -> None
```

Show early per-cell feedback when an edited cell changes.

<a id="wizard_tk_bridge.wizard_table.TableEditor._feedback"></a>

#### \_feedback

```python
def _feedback(row: int, col: int) -> None
```

Run the partial check and show its message for one cell.

<a id="wizard_tk_bridge.wizard_table.TableEditor._show"></a>

#### \_show

```python
def _show(message: str) -> None
```

Show a status message below the grid.

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

<a id="wizard_tk_bridge.wizard_form._Input"></a>

## \_Input Objects

```python
class _Input(NamedTuple)
```

A built input: the widget to place, plus type-specific handles.

<a id="wizard_tk_bridge.wizard_form.HelpTooltip"></a>

## HelpTooltip Objects

```python
class HelpTooltip()
```

A hover bubble showing a field's help text over its widgets.

The bubble is a borderless top-level window shown when the pointer
enters a bound widget and destroyed when it leaves, so help appears
on hover as it does in the textual bridge. It uses neither a
transient window, forced focus nor a grab, which can crash Tk in
automated runs.

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

<a id="wizard_tk_bridge.wizard_form.HelpTooltip._geometry"></a>

#### \_geometry

```python
def _geometry() -> str
```

Return the position string placing the bubble under the anchor.

<a id="wizard_tk_bridge.wizard_form.FormRow"></a>

## FormRow Objects

```python
@dataclass(frozen=True)
class FormRow()
```

One built form row: its field, label, input and help tooltip.

<a id="wizard_tk_bridge.wizard_form._text_input"></a>

#### \_text\_input

```python
def _text_input(grid: tk.Misc, field: AskTextField,
                change: Callable[[], None]) -> _Input
```

Build a text entry, masked and without a default when sensitive.

<a id="wizard_tk_bridge.wizard_form._int_input"></a>

#### \_int\_input

```python
def _int_input(grid: tk.Misc, field: AskIntField,
               change: Callable[[], None]) -> _Input
```

Build a numeric text entry pre-filled with its default.

<a id="wizard_tk_bridge.wizard_form._path_input"></a>

#### \_path\_input

```python
def _path_input(grid: tk.Misc, field: AskPathField,
                change: Callable[[], None]) -> _Input
```

Build a path entry with a Browse button from the path options.

<a id="wizard_tk_bridge.wizard_form._yes_no_input"></a>

#### \_yes\_no\_input

```python
def _yes_no_input(grid: tk.Misc, field: AskYesNoField,
                  change: Callable[[], None]) -> _Input
```

Build a check box holding the yes/no default.

<a id="wizard_tk_bridge.wizard_form._choice_input"></a>

#### \_choice\_input

```python
def _choice_input(grid: tk.Misc, field: AskChoiceField,
                  change: Callable[[], None]) -> _Input
```

Build a read-only drop-down, preselecting any default choice.

<a id="wizard_tk_bridge.wizard_form._multi_input"></a>

#### \_multi\_input

```python
def _multi_input(grid: tk.Misc, field: AskMultiChoiceField,
                 change: Callable[[], None]) -> _Input
```

Build a multi-selection list, preselecting the default values.

<a id="wizard_tk_bridge.wizard_form._preselect"></a>

#### \_preselect

```python
def _preselect(box: tk.Listbox, choices: Sequence[str],
               default: Optional[Sequence[str]]) -> None
```

Select the default values in a multi-selection list.

<a id="wizard_tk_bridge.wizard_form._hint_input"></a>

#### \_hint\_input

```python
def _hint_input(grid: tk.Misc, field: AskField,
                change: Callable[[], None]) -> _Input
```

Build a placeholder entry for a float, time or duration field.

<a id="wizard_tk_bridge.wizard_form._pick_input"></a>

#### \_pick\_input

```python
def _pick_input(grid: tk.Misc, field: AskField,
                change: Callable[[], None]) -> _Input
```

Build a date or date-time entry with a calendar Pick button.

<a id="wizard_tk_bridge.wizard_form._typed_input"></a>

#### \_typed\_input

```python
def _typed_input(grid: tk.Misc, field: AskField,
                 change: Callable[[], None]) -> _Input
```

Build the input widget for one of the five typed fields.

<a id="wizard_tk_bridge.wizard_form._basic_input"></a>

#### \_basic\_input

```python
def _basic_input(grid: tk.Misc, field: AskField,
                 change: Callable[[], None]) -> _Input
```

Build the input widget for one of the original field kinds.

<a id="wizard_tk_bridge.wizard_form._make_input"></a>

#### \_make\_input

```python
def _make_input(grid: tk.Misc, field: AskField,
                change: Callable[[], None]) -> _Input
```

Build the input widget matching the field type.

<a id="wizard_tk_bridge.wizard_form._entry_widget"></a>

#### \_entry\_widget

```python
def _entry_widget(row: FormRow) -> tk.Entry
```

Return the text entry of a text or integer row.

<a id="wizard_tk_bridge.wizard_form._int_value"></a>

#### \_int\_value

```python
def _int_value(row: FormRow, field: AskIntField) -> Optional[int]
```

Return the integer value of a row, or its default when empty.

<a id="wizard_tk_bridge.wizard_form._path_value"></a>

#### \_path\_value

```python
def _path_value(row: FormRow, field: AskPathField) -> Optional[Path]
```

Return the accepted path of a row, or None when not accepted.

<a id="wizard_tk_bridge.wizard_form._choice_value"></a>

#### \_choice\_value

```python
def _choice_value(row: FormRow) -> Optional[str]
```

Return the chosen value of a row, or None when none is chosen.

<a id="wizard_tk_bridge.wizard_form._multi_selected"></a>

#### \_multi\_selected

```python
def _multi_selected(row: FormRow) -> list[int]
```

Return the selected 0-based indexes of a multi-selection row.

<a id="wizard_tk_bridge.wizard_form._multi_values"></a>

#### \_multi\_values

```python
def _multi_values(row: FormRow, field: AskMultiChoiceField) -> list[str]
```

Return the chosen values of a multi-selection row, in order.

<a id="wizard_tk_bridge.wizard_form._int_error"></a>

#### \_int\_error

```python
def _int_error(row: FormRow, field: AskIntField) -> Optional[str]
```

Return the integer row's own validation error, or None.

<a id="wizard_tk_bridge.wizard_form._multi_error"></a>

#### \_multi\_error

```python
def _multi_error(row: FormRow, field: AskMultiChoiceField) -> Optional[str]
```

Return the multi-selection row's count error, or None.

The count check mirrors wizard_ui_bridge._textual_widgets, the
private module behind the Textual bridge's own form fields; that
module is not public API a sibling package may import.

<a id="wizard_tk_bridge.wizard_form._set_widget_state"></a>

#### \_set\_widget\_state

```python
def _set_widget_state(row: FormRow, enabled: bool) -> None
```

Enable or disable a row's input widget, keeping combo read-only.

<a id="wizard_tk_bridge.wizard_form._enable_row"></a>

#### \_enable\_row

```python
def _enable_row(row: FormRow, enabled: bool) -> None
```

Enable or disable one form row, greying its label when disabled.

<a id="wizard_tk_bridge.wizard_form._hint_note"></a>

#### \_hint\_note

```python
def _hint_note(field: AskField) -> Optional[str]
```

Return the format hint sentence for a typed field, or None.

<a id="wizard_tk_bridge.wizard_form._tooltip_text"></a>

#### \_tooltip\_text

```python
def _tooltip_text(field: AskField) -> Optional[str]
```

Return the tooltip text combining help text and format hint.

<a id="wizard_tk_bridge.wizard_form._row_tooltip"></a>

#### \_row\_tooltip

```python
def _row_tooltip(field: AskField, label: tk.Label,
                 widget: tk.Widget) -> Optional[HelpTooltip]
```

Return a hover tooltip for the field's help and format hint.

<a id="wizard_tk_bridge.wizard_form._set_entry_text"></a>

#### \_set\_entry\_text

```python
def _set_entry_text(entry: tk.Entry, text: str) -> None
```

Replace a text or integer entry's text, enabling it if disabled.

<a id="wizard_tk_bridge.wizard_form._set_combo"></a>

#### \_set\_combo

```python
def _set_combo(box: ttk.Combobox, value: str) -> None
```

Set a drop-down's value, enabling it briefly if disabled.

<a id="wizard_tk_bridge.wizard_form._set_multi"></a>

#### \_set\_multi

```python
def _set_multi(box: tk.Listbox, choices: Sequence[str],
               value: PrefillValueType) -> None
```

Select the values of a multi-selection list, enabling it briefly.

<a id="wizard_tk_bridge.wizard_form._basic_answer"></a>

#### \_basic\_answer

```python
def _basic_answer(row: FormRow) -> AnswerField
```

Return the answer of a row of one of the original field kinds.

<a id="wizard_tk_bridge.wizard_form._basic_error"></a>

#### \_basic\_error

```python
def _basic_error(row: FormRow) -> Optional[str]
```

Return the own error of a row of an original field kind, or None.

<a id="wizard_tk_bridge.wizard_form._row_error"></a>

#### \_row\_error

```python
def _row_error(row: FormRow) -> Optional[str]
```

Return one row's own validation error, without its field label.

<a id="wizard_tk_bridge.wizard_form._with_label"></a>

#### \_with\_label

```python
def _with_label(field: AskField, error: Optional[str]) -> Optional[str]
```

Prefix a field's own error with its label, keeping None as None.

The whole form shares one status line, so naming the field makes clear
which row a message such as 'Please enter an integer.' refers to.

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

<a id="wizard_tk_bridge.wizard_form.FormEditor._scroll_area"></a>

#### \_scroll\_area

```python
def _scroll_area(parent: tk.Misc) -> tk.Frame
```

Build the scrolling field area, returning the frame for the rows.

A tall form (many rows) would overflow the fixed-size wizard
window, so the labelled rows sit in a frame inside a vertically
scrolling canvas whose scrollbar appears only when it is needed.
The status line stays below the scroll area so it is always shown.

<a id="wizard_tk_bridge.wizard_form.FormEditor._apply_initial"></a>

#### \_apply\_initial

```python
def _apply_initial() -> None
```

Disable the initially irrelevant rows, showing no message yet.

<a id="wizard_tk_bridge.wizard_form.FormEditor._apply_prefills"></a>

#### \_apply\_prefills

```python
def _apply_prefills(prefills: PrefillValues, changed: int) -> None
```

Write the validator's valid prefills into their row inputs.

<a id="wizard_tk_bridge.wizard_form.FormEditor._write_value"></a>

#### \_write\_value

```python
def _write_value(row: FormRow, value: PrefillValueType) -> None
```

Write one prefill value into a row's input by field type.

<a id="wizard_tk_bridge.wizard_form.FormEditor._build_row"></a>

#### \_build\_row

```python
def _build_row(grid: tk.Misc, index: int, field: AskField) -> FormRow
```

Build and place one labelled input row of the grid.

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

<a id="wizard_tk_bridge.wizard_form.FormEditor._validator_blocks"></a>

#### \_validator\_blocks

```python
def _validator_blocks(answers: list[AnswerField]) -> bool
```

Run the whole-form validator and return whether it blocks.

<a id="wizard_tk_bridge.wizard_form.FormEditor._changed"></a>

#### \_changed

```python
def _changed(index: int) -> None
```

React to a field change with live feedback and row enabling.

<a id="wizard_tk_bridge.wizard_form.FormEditor._feedback"></a>

#### \_feedback

```python
def _feedback(answers: list[AnswerField], index: int) -> str
```

Return the live message for the field that just changed.

<a id="wizard_tk_bridge.wizard_form.FormEditor._run_validator"></a>

#### \_run\_validator

```python
def _run_validator(answers: list[AnswerField], index: int) -> str
```

Apply the validator's disabled rows and return its message.

<a id="wizard_tk_bridge.wizard_form.FormEditor._first_error"></a>

#### \_first\_error

```python
def _first_error() -> Optional[str]
```

Return the first enabled field's own error, or None.

<a id="wizard_tk_bridge.wizard_form.FormEditor._apply_disabled"></a>

#### \_apply\_disabled

```python
def _apply_disabled(disable_row_idxs: tuple[int, ...]) -> None
```

Enable or disable each row to match the validator result.

<a id="wizard_tk_bridge.wizard_form.FormEditor._show"></a>

#### \_show

```python
def _show(message: str) -> None
```

Show a status message below the form.

<a id="wizard_tk_bridge.wizard_form.FormEditor._read"></a>

#### \_read

```python
def _read(index: int) -> AnswerField
```

Return the current answer of one row read from its widget.

<a id="wizard_tk_bridge.wizard_form.FormEditor._field_error"></a>

#### \_field\_error

```python
def _field_error(index: int) -> Optional[str]
```

Return one field's own error, prefixed with its label.

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

<a id="wizard_tk_bridge.tk_bridge.WizardUiBridgeTk._window_obj"></a>

#### \_window\_obj

```python
def _window_obj() -> WizardWindow
```

Return the wizard window, building it on first use.

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

<a id="wizard_tk_bridge.wizard_path._is_dir_kind"></a>

#### \_is\_dir\_kind

```python
def _is_dir_kind(kind: WizardPathKind) -> bool
```

Return whether the kind asks for a directory rather than a file.

<a id="wizard_tk_bridge.wizard_path.pick_path"></a>

#### pick\_path

```python
def pick_path(parent: tk.Misc, options: PathAskOptions,
              initial: str) -> Optional[str]
```

Open the native dialog for the kind, or None when cancelled.

<a id="wizard_tk_bridge.wizard_path._start_location"></a>

#### \_start\_location

```python
def _start_location(initial: str, default: Optional[Path]) -> tuple[str, str]
```

Return the initial directory and file name for a path dialog.

<a id="wizard_tk_bridge.wizard_path._open_dialog"></a>

#### \_open\_dialog

```python
def _open_dialog(parent: tk.Misc, kind: WizardPathKind, initial_dir: str,
                 initial_file: str) -> str
```

Open the open-file, save-file or directory dialog for a kind.

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

<a id="wizard_tk_bridge.wizard_path.PathRow.bind_return"></a>

#### bind\_return

```python
def bind_return(callback: Callable[[], None]) -> None
```

Call callback when Return is pressed while the entry has focus.

<a id="wizard_tk_bridge.wizard_path.PathRow._browse"></a>

#### \_browse

```python
def _browse() -> None
```

Open the native picker and fill the entry with the choice.

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

A WizardWindow either owns a new window of its own, built with ``parent``,
or is embedded directly into an existing container the caller built,
given as ``area``. Exactly one of the two is given.
``modal`` decides whether the wizard grabs that window for the session,
which the caller is best placed to decide since only it knows whether the
rest of the window should stay usable meanwhile.

<a id="wizard_tk_bridge.wizard_window._default_path_text"></a>

#### \_default\_path\_text

```python
def _default_path_text(options: PathAskOptions) -> str
```

Return the initial path text from the option's default.

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

<a id="wizard_tk_bridge.wizard_window.WizardWindow._build_toplevel"></a>

#### \_build\_toplevel

```python
def _build_toplevel(parent: tk.Misc) -> tk.Toplevel
```

Create and configure the wizard's own top-level window.

<a id="wizard_tk_bridge.wizard_window.WizardWindow._build_messages"></a>

#### \_build\_messages

```python
def _build_messages(container: tk.Misc) -> tk.Text
```

Build the read-only area that keeps the wizard messages.

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

<a id="wizard_tk_bridge.wizard_window.WizardWindow._text_result"></a>

#### \_text\_result

```python
@staticmethod
def _text_result(result: str, nullable: bool,
                 default: Optional[str]) -> Optional[str]
```

Return the answer after the default and nullable rules.

<a id="wizard_tk_bridge.wizard_window.WizardWindow.ask_int"></a>

#### ask\_int

```python
def ask_int(question: str, re_ask: Optional[str], nullable: bool,
            min_value: Optional[int], max_value: Optional[int],
            default: Optional[int]) -> Optional[int]
```

Ask one integer question, re-asking until it is in range.

<a id="wizard_tk_bridge.wizard_window.WizardWindow._run_int"></a>

#### \_run\_int

```python
def _run_int(question: str, re_ask: Optional[str],
             default: Optional[int]) -> str
```

Show one integer entry and return the entered text.

<a id="wizard_tk_bridge.wizard_window.WizardWindow.ask_path"></a>

#### ask\_path

```python
def ask_path(question: str, options: PathAskOptions,
             re_ask: Optional[str]) -> Optional[Path]
```

Ask one path question with a Browse button, re-asking on error.

<a id="wizard_tk_bridge.wizard_window.WizardWindow._run_path"></a>

#### \_run\_path

```python
def _run_path(question: str, re_ask: Optional[str], options: PathAskOptions,
              value: Optional[str]) -> str
```

Show one path entry with a Browse button and return the text.

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

<a id="wizard_tk_bridge.wizard_window.WizardWindow._run_multi"></a>

#### \_run\_multi

```python
def _run_multi(question: str, re_ask: Optional[str], choices: Sequence[str],
               default: Optional[Sequence[str]]) -> list[str]
```

Show a multi-selection list once and return the picked values.

<a id="wizard_tk_bridge.wizard_window.WizardWindow._choice_list"></a>

#### \_choice\_list

```python
def _choice_list(choices: Sequence[str], marked: Optional[str | Sequence[str]],
                 mode: str) -> tk.Listbox
```

Build a selection list, preselecting the marked choices.

<a id="wizard_tk_bridge.wizard_window.WizardWindow._preset_indexes"></a>

#### \_preset\_indexes

```python
@staticmethod
def _preset_indexes(choices: Sequence[str],
                    marked: Optional[str | Sequence[str]]) -> list[int]
```

Return the indexes to preselect from a default value or list.

<a id="wizard_tk_bridge.wizard_window.WizardWindow._pick_one"></a>

#### \_pick\_one

```python
def _pick_one(listbox: tk.Listbox, choices: Sequence[str]) -> None
```

Finish a single-choice question with the selected value.

<a id="wizard_tk_bridge.wizard_window.WizardWindow._pick_many"></a>

#### \_pick\_many

```python
def _pick_many(listbox: tk.Listbox, choices: Sequence[str]) -> None
```

Finish a multi-choice question with the selected values.

<a id="wizard_tk_bridge.wizard_window.WizardWindow._begin"></a>

#### \_begin

```python
def _begin(question: str, re_ask: Optional[str]) -> None
```

Clear the content area and show the question and any reason.

<a id="wizard_tk_bridge.wizard_window.WizardWindow._add_label"></a>

#### \_add\_label

```python
def _add_label(text: str, color: str) -> None
```

Add one wrapped label to the content area.

<a id="wizard_tk_bridge.wizard_window.WizardWindow._add_buttons"></a>

#### \_add\_buttons

```python
def _add_buttons(on_ok: Callable[[], None]) -> None
```

Add the confirm and navigation buttons.

<a id="wizard_tk_bridge.wizard_window.WizardWindow._add_table_buttons"></a>

#### \_add\_table\_buttons

```python
def _add_table_buttons(editor: TableEditor) -> None
```

Add confirm, optional add/remove-row and navigation buttons.

<a id="wizard_tk_bridge.wizard_window.WizardWindow._add_nav_buttons"></a>

#### \_add\_nav\_buttons

```python
def _add_nav_buttons(box: tk.Frame) -> None
```

Add the back, out-one-level and abort navigation buttons.

<a id="wizard_tk_bridge.wizard_window.WizardWindow._wait"></a>

#### \_wait

```python
def _wait() -> object
```

Focus the first input, then wait for an answer or navigation.

<a id="wizard_tk_bridge.wizard_window.WizardWindow._finish"></a>

#### \_finish

```python
def _finish(value: object) -> None
```

Store the answer and release the waiting prompt.

<a id="wizard_tk_bridge.wizard_window.WizardWindow._back"></a>

#### \_back

```python
def _back() -> None
```

Request a step back to the previous question.

<a id="wizard_tk_bridge.wizard_window.WizardWindow._cancel_level"></a>

#### \_cancel\_level

```python
def _cancel_level() -> None
```

Request leaving the current level by one step.

<a id="wizard_tk_bridge.wizard_window.WizardWindow._cancel"></a>

#### \_cancel

```python
def _cancel() -> None
```

Request abandoning the whole configuration.

<a id="wizard_tk_bridge.wizard_window.WizardWindow._navigate"></a>

#### \_navigate

```python
def _navigate(request: type[WizardNavigation]) -> None
```

Record a navigation request and release the waiting prompt.

<a id="wizard_tk_bridge.wizard_window.WizardWindow._grab"></a>

#### \_grab

```python
def _grab() -> None
```

Take the modal grab, retrying until the target is viewable.

