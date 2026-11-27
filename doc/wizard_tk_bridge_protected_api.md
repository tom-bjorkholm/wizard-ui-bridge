# Table of Contents

* [wizard\_tk\_bridge.auto\_scroll](#wizard_tk_bridge.auto_scroll)
  * [auto\_hide](#wizard_tk_bridge.auto_scroll.auto_hide)
  * [bind\_wheel](#wizard_tk_bridge.auto_scroll.bind_wheel)
  * [\_wheel\_events](#wizard_tk_bridge.auto_scroll._wheel_events)
  * [\_on\_wheel](#wizard_tk_bridge.auto_scroll._on_wheel)
  * [\_on\_touchpad](#wizard_tk_bridge.auto_scroll._on_touchpad)
  * [\_event\_area](#wizard_tk_bridge.auto_scroll._event_area)
  * [\_scroll\_widget](#wizard_tk_bridge.auto_scroll._scroll_widget)
  * [\_wheel\_area](#wizard_tk_bridge.auto_scroll._wheel_area)
  * [\_own\_wheel](#wizard_tk_bridge.auto_scroll._own_wheel)
  * [\_wheel\_delta](#wizard_tk_bridge.auto_scroll._wheel_delta)
  * [\_touchpad\_steps](#wizard_tk_bridge.auto_scroll._touchpad_steps)
  * [\_scroll](#wizard_tk_bridge.auto_scroll._scroll)
  * [\_wheel\_amount](#wizard_tk_bridge.auto_scroll._wheel_amount)
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
* [wizard\_tk\_bridge.wizard\_cell](#wizard_tk_bridge.wizard_cell)
  * [int\_answer](#wizard_tk_bridge.wizard_cell.int_answer)
  * [\_inside](#wizard_tk_bridge.wizard_cell._inside)
  * [HelpTooltip](#wizard_tk_bridge.wizard_cell.HelpTooltip)
    * [\_\_init\_\_](#wizard_tk_bridge.wizard_cell.HelpTooltip.__init__)
    * [show](#wizard_tk_bridge.wizard_cell.HelpTooltip.show)
    * [hide](#wizard_tk_bridge.wizard_cell.HelpTooltip.hide)
    * [\_position](#wizard_tk_bridge.wizard_cell.HelpTooltip._position)
  * [\_hint\_note](#wizard_tk_bridge.wizard_cell._hint_note)
  * [tooltip\_text](#wizard_tk_bridge.wizard_cell.tooltip_text)
  * [CellInput](#wizard_tk_bridge.wizard_cell.CellInput)
    * [value](#wizard_tk_bridge.wizard_cell.CellInput.value)
    * [error](#wizard_tk_bridge.wizard_cell.CellInput.error)
    * [write](#wizard_tk_bridge.wizard_cell.CellInput.write)
    * [main\_widget](#wizard_tk_bridge.wizard_cell.CellInput.main_widget)
    * [set\_width](#wizard_tk_bridge.wizard_cell.CellInput.set_width)
    * [set\_enabled](#wizard_tk_bridge.wizard_cell.CellInput.set_enabled)
  * [\_text\_input](#wizard_tk_bridge.wizard_cell._text_input)
  * [\_int\_input](#wizard_tk_bridge.wizard_cell._int_input)
  * [\_path\_input](#wizard_tk_bridge.wizard_cell._path_input)
  * [\_yes\_no\_input](#wizard_tk_bridge.wizard_cell._yes_no_input)
  * [\_choice\_input](#wizard_tk_bridge.wizard_cell._choice_input)
  * [\_multi\_input](#wizard_tk_bridge.wizard_cell._multi_input)
  * [\_preselect](#wizard_tk_bridge.wizard_cell._preselect)
  * [\_hint\_input](#wizard_tk_bridge.wizard_cell._hint_input)
  * [\_pick\_input](#wizard_tk_bridge.wizard_cell._pick_input)
  * [\_typed\_input](#wizard_tk_bridge.wizard_cell._typed_input)
  * [\_basic\_input](#wizard_tk_bridge.wizard_cell._basic_input)
  * [build\_input](#wizard_tk_bridge.wizard_cell.build_input)
  * [\_compact\_width](#wizard_tk_bridge.wizard_cell._compact_width)
  * [\_entry\_widget](#wizard_tk_bridge.wizard_cell._entry_widget)
  * [\_int\_value](#wizard_tk_bridge.wizard_cell._int_value)
  * [\_path\_value](#wizard_tk_bridge.wizard_cell._path_value)
  * [\_choice\_value](#wizard_tk_bridge.wizard_cell._choice_value)
  * [\_multi\_selected](#wizard_tk_bridge.wizard_cell._multi_selected)
  * [\_multi\_values](#wizard_tk_bridge.wizard_cell._multi_values)
  * [\_basic\_value](#wizard_tk_bridge.wizard_cell._basic_value)
  * [\_int\_error](#wizard_tk_bridge.wizard_cell._int_error)
  * [\_basic\_error](#wizard_tk_bridge.wizard_cell._basic_error)
  * [\_set\_entry\_text](#wizard_tk_bridge.wizard_cell._set_entry_text)
  * [\_set\_combo](#wizard_tk_bridge.wizard_cell._set_combo)
  * [\_set\_multi](#wizard_tk_bridge.wizard_cell._set_multi)
  * [\_scroll\_canvas](#wizard_tk_bridge.wizard_cell._scroll_canvas)
  * [scrolled\_editor](#wizard_tk_bridge.wizard_cell.scrolled_editor)
  * [scroll\_into\_view](#wizard_tk_bridge.wizard_cell.scroll_into_view)
  * [view\_start](#wizard_tk_bridge.wizard_cell.view_start)
* [wizard\_tk\_bridge.gui\_style](#wizard_tk_bridge.gui_style)
  * [style\_input](#wizard_tk_bridge.gui_style.style_input)
  * [choice\_combo](#wizard_tk_bridge.gui_style.choice_combo)
  * [\_style\_combobox](#wizard_tk_bridge.gui_style._style_combobox)
  * [focus\_first\_input](#wizard_tk_bridge.gui_style.focus_first_input)
  * [\_first\_input](#wizard_tk_bridge.gui_style._first_input)
  * [\_is\_input](#wizard_tk_bridge.gui_style._is_input)
  * [bind\_submit](#wizard_tk_bridge.gui_style.bind_submit)
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
    * [\_show\_hint](#wizard_tk_bridge.wizard_pick_row.HintEntry._show_hint)
    * [\_focus\_in](#wizard_tk_bridge.wizard_pick_row.HintEntry._focus_in)
    * [\_focus\_out](#wizard_tk_bridge.wizard_pick_row.HintEntry._focus_out)
  * [PickRow](#wizard_tk_bridge.wizard_pick_row.PickRow)
    * [\_\_init\_\_](#wizard_tk_bridge.wizard_pick_row.PickRow.__init__)
    * [entry](#wizard_tk_bridge.wizard_pick_row.PickRow.entry)
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
* [wizard\_tk\_bridge.wizard\_form](#wizard_tk_bridge.wizard_form)
  * [handles\_field](#wizard_tk_bridge.wizard_form.handles_field)
  * [FormRow](#wizard_tk_bridge.wizard_form.FormRow)
  * [\_enable\_row](#wizard_tk_bridge.wizard_form._enable_row)
  * [\_row\_tooltip](#wizard_tk_bridge.wizard_form._row_tooltip)
  * [\_with\_label](#wizard_tk_bridge.wizard_form._with_label)
  * [FormEditor](#wizard_tk_bridge.wizard_form.FormEditor)
    * [\_\_init\_\_](#wizard_tk_bridge.wizard_form.FormEditor.__init__)
    * [\_apply\_initial](#wizard_tk_bridge.wizard_form.FormEditor._apply_initial)
    * [\_apply\_prefills](#wizard_tk_bridge.wizard_form.FormEditor._apply_prefills)
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
    * [ask\_form](#wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.ask_form)
    * [ask\_matrix\_form](#wizard_tk_bridge.tk_bridge.WizardUiBridgeTk.ask_matrix_form)
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
    * [entry](#wizard_tk_bridge.wizard_path.PathRow.entry)
    * [get](#wizard_tk_bridge.wizard_path.PathRow.get)
    * [set\_text](#wizard_tk_bridge.wizard_path.PathRow.set_text)
    * [set\_enabled](#wizard_tk_bridge.wizard_path.PathRow.set_enabled)
    * [\_browse](#wizard_tk_bridge.wizard_path.PathRow._browse)
* [wizard\_tk\_bridge.wizard\_matrix](#wizard_tk_bridge.wizard_matrix)
  * [MatrixCell](#wizard_tk_bridge.wizard_matrix.MatrixCell)
    * [answer](#wizard_tk_bridge.wizard_matrix.MatrixCell.answer)
    * [error](#wizard_tk_bridge.wizard_matrix.MatrixCell.error)
  * [\_cell\_tooltip](#wizard_tk_bridge.wizard_matrix._cell_tooltip)
  * [\_label](#wizard_tk_bridge.wizard_matrix._label)
  * [\_label\_font](#wizard_tk_bridge.wizard_matrix._label_font)
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
    * [\_allowed](#wizard_tk_bridge.wizard_matrix.MatrixEditor._allowed)
    * [\_update\_resizers](#wizard_tk_bridge.wizard_matrix.MatrixEditor._update_resizers)
    * [\_append\_row](#wizard_tk_bridge.wizard_matrix.MatrixEditor._append_row)
    * [\_reshaped](#wizard_tk_bridge.wizard_matrix.MatrixEditor._reshaped)
    * [\_destroy](#wizard_tk_bridge.wizard_matrix.MatrixEditor._destroy)
    * [\_focus\_path](#wizard_tk_bridge.wizard_matrix.MatrixEditor._focus_path)
    * [\_focus\_first](#wizard_tk_bridge.wizard_matrix.MatrixEditor._focus_first)
    * [\_focusable](#wizard_tk_bridge.wizard_matrix.MatrixEditor._focusable)
    * [\_reveal](#wizard_tk_bridge.wizard_matrix.MatrixEditor._reveal)
    * [\_build\_cell](#wizard_tk_bridge.wizard_matrix.MatrixEditor._build_cell)
    * [\_new\_widget](#wizard_tk_bridge.wizard_matrix.MatrixEditor._new_widget)
    * [\_positions](#wizard_tk_bridge.wizard_matrix.MatrixEditor._positions)
    * [\_row\_line](#wizard_tk_bridge.wizard_matrix.MatrixEditor._row_line)
    * [\_column\_line](#wizard_tk_bridge.wizard_matrix.MatrixEditor._column_line)
    * [\_asks](#wizard_tk_bridge.wizard_matrix.MatrixEditor._asks)
    * [\_changed](#wizard_tk_bridge.wizard_matrix.MatrixEditor._changed)
    * [\_validate](#wizard_tk_bridge.wizard_matrix.MatrixEditor._validate)
    * [\_apply\_disabled](#wizard_tk_bridge.wizard_matrix.MatrixEditor._apply_disabled)
    * [\_apply\_prefills](#wizard_tk_bridge.wizard_matrix.MatrixEditor._apply_prefills)
    * [\_first\_invalid](#wizard_tk_bridge.wizard_matrix.MatrixEditor._first_invalid)
    * [\_cell\_error](#wizard_tk_bridge.wizard_matrix.MatrixEditor._cell_error)
    * [\_cell](#wizard_tk_bridge.wizard_matrix.MatrixEditor._cell)
    * [\_show](#wizard_tk_bridge.wizard_matrix.MatrixEditor._show)
* [wizard\_tk\_bridge.wizard\_window](#wizard_tk_bridge.wizard_window)
  * [\_default\_path\_text](#wizard_tk_bridge.wizard_window._default_path_text)
  * [WizardWindow](#wizard_tk_bridge.wizard_window.WizardWindow)
    * [\_\_init\_\_](#wizard_tk_bridge.wizard_window.WizardWindow.__init__)
    * [\_build\_toplevel](#wizard_tk_bridge.wizard_window.WizardWindow._build_toplevel)
    * [\_build\_messages](#wizard_tk_bridge.wizard_window.WizardWindow._build_messages)
    * [show](#wizard_tk_bridge.wizard_window.WizardWindow.show)
    * [close](#wizard_tk_bridge.wizard_window.WizardWindow.close)
    * [ask\_text](#wizard_tk_bridge.wizard_window.WizardWindow.ask_text)
    * [ask\_int](#wizard_tk_bridge.wizard_window.WizardWindow.ask_int)
    * [\_run\_int](#wizard_tk_bridge.wizard_window.WizardWindow._run_int)
    * [ask\_path](#wizard_tk_bridge.wizard_window.WizardWindow.ask_path)
    * [\_run\_path](#wizard_tk_bridge.wizard_window.WizardWindow._run_path)
    * [ask\_form](#wizard_tk_bridge.wizard_window.WizardWindow.ask_form)
    * [ask\_matrix\_form](#wizard_tk_bridge.wizard_window.WizardWindow.ask_matrix_form)
    * [ask\_yes\_no](#wizard_tk_bridge.wizard_window.WizardWindow.ask_yes_no)
    * [ask\_choice](#wizard_tk_bridge.wizard_window.WizardWindow.ask_choice)
    * [ask\_multi](#wizard_tk_bridge.wizard_window.WizardWindow.ask_multi)
    * [\_run\_multi](#wizard_tk_bridge.wizard_window.WizardWindow._run_multi)
    * [\_choice\_list](#wizard_tk_bridge.wizard_window.WizardWindow._choice_list)
    * [\_preset\_indexes](#wizard_tk_bridge.wizard_window.WizardWindow._preset_indexes)
    * [\_pick\_one](#wizard_tk_bridge.wizard_window.WizardWindow._pick_one)
    * [\_pick\_many](#wizard_tk_bridge.wizard_window.WizardWindow._pick_many)
    * [\_begin](#wizard_tk_bridge.wizard_window.WizardWindow._begin)
    * [\_add\_label](#wizard_tk_bridge.wizard_window.WizardWindow._add_label)
    * [\_add\_buttons](#wizard_tk_bridge.wizard_window.WizardWindow._add_buttons)
    * [\_ok\_box](#wizard_tk_bridge.wizard_window.WizardWindow._ok_box)
    * [\_button\_box](#wizard_tk_bridge.wizard_window.WizardWindow._button_box)
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

<a id="wizard_tk_bridge.auto_scroll._wheel_events"></a>

#### \_wheel\_events

```python
def _wheel_events(window: tk.Misc) -> dict[str, str]
```

Return the wheel sequences to bind, each with the axis it moves.

X11 with Tk 8.6 has no wheel event: it presses button 4 and button 5
instead, and the same buttons with shift held for the sideways
wheel. Every other windowing system, and Tk 9 on all of them, sends
a MouseWheel event, and binding those buttons there would answer the
side buttons of a mouse instead.

<a id="wizard_tk_bridge.auto_scroll._on_wheel"></a>

#### \_on\_wheel

```python
def _on_wheel(window: tk.Misc, axis: str, event: 'tk.Event[tk.Misc]') -> None
```

Scroll the area the wheel belongs to along the event's axis.

<a id="wizard_tk_bridge.auto_scroll._on_touchpad"></a>

#### \_on\_touchpad

```python
def _on_touchpad(window: tk.Misc, event: 'tk.Event[tk.Misc]') -> None
```

Scroll the area a touchpad gesture belongs to, both ways at once.

A touchpad gesture moves the view whichever way the fingers went, so
its event carries a sideways and a downward step together and needs
no shift key for the sideways one. The steps are pixels, which the
canvas moves by the same way it does under a dragging hand.

<a id="wizard_tk_bridge.auto_scroll._event_area"></a>

#### \_event\_area

```python
def _event_area(window: tk.Misc, event: 'tk.Event[tk.Misc]',
                axis: str) -> Optional[tk.Canvas]
```

Return the area one scroll event moves along the axis, if any.

<a id="wizard_tk_bridge.auto_scroll._scroll_widget"></a>

#### \_scroll\_widget

```python
def _scroll_widget(window: tk.Misc,
                   event: 'tk.Event[tk.Misc]') -> Optional[tk.Misc]
```

Return the widget one scroll event belongs to, if it is in an area.

Tk sends the event to the widget under the pointer, which is what
every scrolling widget of its own goes by, so the widget the event
reached is tried first. Tk 8.6 on Windows instead sends the wheel to
the focused widget, and looking the pointer position up then catches
the case where the focus is outside every area.

<a id="wizard_tk_bridge.auto_scroll._wheel_area"></a>

#### \_wheel\_area

```python
def _wheel_area(widget: tk.Misc) -> Optional[tk.Canvas]
```

Return the scrolling area the widget is in, if it is in one.

<a id="wizard_tk_bridge.auto_scroll._own_wheel"></a>

#### \_own\_wheel

```python
def _own_wheel(widget: tk.Misc, axis: str) -> bool
```

Return whether the widget answers the mouse wheel itself.

A combobox steps through its values on the wheel, and a list or a
text scrolls its own view while it holds more than it shows. The
wheel then belongs to the widget and not to the area around it, and
a list that shows all it holds leaves the wheel to the area.

<a id="wizard_tk_bridge.auto_scroll._wheel_delta"></a>

#### \_wheel\_delta

```python
def _wheel_delta(event: 'tk.Event[tk.Misc]') -> int
```

Return the wheel delta, also for X11's wheel button presses.

X11 with Tk 8.6 has no delta to report: it presses button 4 for one
notch up and button 5 for one notch down, which the delta of a whole
notch stands for here. A wheel event carries no button number at
all, which is why the number is looked up rather than tested.

<a id="wizard_tk_bridge.auto_scroll._touchpad_steps"></a>

#### \_touchpad\_steps

```python
def _touchpad_steps(widget: tk.Misc, delta: int) -> tuple[int, int]
```

Return the sideways and downward pixels of one touchpad event.

Tk packs both steps of the gesture into the one delta a scroll event
carries, the sideways step in its high half and the downward one, as
a signed number, in its low half. The steps are points, which Tk's
own scrolling widgets turn into pixels for the display in use, and
``tk::ScaleNum`` is the very conversion those widgets apply.

<a id="wizard_tk_bridge.auto_scroll._scroll"></a>

#### \_scroll

```python
def _scroll(area: tk.Canvas, axis: str, delta: int) -> None
```

Scroll the area one wheel step along the axis.

From Tk 9 on the step can be a fraction of a unit, which the finer
steps of a trackpad give, so the amount goes to Tk as it is instead
of through the whole-unit ``xview_scroll`` and ``yview_scroll``.

<a id="wizard_tk_bridge.auto_scroll._wheel_amount"></a>

#### \_wheel\_amount

```python
def _wheel_amount(widget: tk.Misc, delta: int) -> float
```

Return the units one wheel event scrolls, as a scrollbar does.

From Tk 9 on every windowing system reports 120 for one notch of the
wheel, and Tk's own scrollbars scroll three units for it, taking a
fraction of a unit for the finer steps of a trackpad. Tk 8.6 scrolls
one whole unit per notch, and reports that notch as 1 on macOS and
as 120 on the other windowing systems.

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

<a id="wizard_tk_bridge.wizard_cell._inside"></a>

#### \_inside

```python
def _inside(start: int, size: int, limit: int) -> int
```

Return the start coordinate that keeps size within limit.

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

<a id="wizard_tk_bridge.wizard_cell.HelpTooltip._position"></a>

#### \_position

```python
def _position(host: tk.Misc, tip: tk.Label) -> tuple[int, int]
```

Return where in host to place the bubble under the anchor.

<a id="wizard_tk_bridge.wizard_cell._hint_note"></a>

#### \_hint\_note

```python
def _hint_note(cell: AskCell) -> Optional[str]
```

Return the format hint sentence for a typed cell, or None.

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

<a id="wizard_tk_bridge.wizard_cell._text_input"></a>

#### \_text\_input

```python
def _text_input(parent: tk.Misc, cell: AskTextCell,
                change: Callable[[], None]) -> CellInput
```

Build a text entry, pre-filled unless sensitive.

It starts with the start value, else the default.

<a id="wizard_tk_bridge.wizard_cell._int_input"></a>

#### \_int\_input

```python
def _int_input(parent: tk.Misc, cell: AskIntCell,
               change: Callable[[], None]) -> CellInput
```

Build a numeric text entry pre-filled with its start or default.

<a id="wizard_tk_bridge.wizard_cell._path_input"></a>

#### \_path\_input

```python
def _path_input(parent: tk.Misc, cell: AskPathCell,
                change: Callable[[], None]) -> CellInput
```

Build a path entry with a Browse button from the path options.

It starts with the start value, else the default.

<a id="wizard_tk_bridge.wizard_cell._yes_no_input"></a>

#### \_yes\_no\_input

```python
def _yes_no_input(parent: tk.Misc, cell: AskYesNoCell,
                  change: Callable[[], None]) -> CellInput
```

Build a check box holding the yes/no start value, else default.

<a id="wizard_tk_bridge.wizard_cell._choice_input"></a>

#### \_choice\_input

```python
def _choice_input(parent: tk.Misc, cell: AskChoiceCell,
                  change: Callable[[], None]) -> CellInput
```

Build a read-only drop-down, preselecting any start or default.

A nullable choice gets a blank entry, see choice_combo().

<a id="wizard_tk_bridge.wizard_cell._multi_input"></a>

#### \_multi\_input

```python
def _multi_input(parent: tk.Misc, cell: AskMultiChoiceCell,
                 change: Callable[[], None]) -> CellInput
```

Build a multi-selection list, preselecting the start or default.

<a id="wizard_tk_bridge.wizard_cell._preselect"></a>

#### \_preselect

```python
def _preselect(box: tk.Listbox, choices: Sequence[str],
               start: Optional[Sequence[str]]) -> None
```

Select the start values in a multi-selection list.

<a id="wizard_tk_bridge.wizard_cell._hint_input"></a>

#### \_hint\_input

```python
def _hint_input(parent: tk.Misc, cell: AskCell,
                change: Callable[[], None]) -> CellInput
```

Build a placeholder entry for a float, time or duration cell.

<a id="wizard_tk_bridge.wizard_cell._pick_input"></a>

#### \_pick\_input

```python
def _pick_input(parent: tk.Misc, cell: AskCell,
                change: Callable[[], None]) -> CellInput
```

Build a date or date-time entry with a calendar Pick button.

<a id="wizard_tk_bridge.wizard_cell._typed_input"></a>

#### \_typed\_input

```python
def _typed_input(parent: tk.Misc, cell: AskCell,
                 change: Callable[[], None]) -> CellInput
```

Build the input widget for one of the five typed cells.

<a id="wizard_tk_bridge.wizard_cell._basic_input"></a>

#### \_basic\_input

```python
def _basic_input(parent: tk.Misc, cell: AskCell,
                 change: Callable[[], None]) -> CellInput
```

Build the input widget for one of the original cell kinds.

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

<a id="wizard_tk_bridge.wizard_cell._compact_width"></a>

#### \_compact\_width

```python
def _compact_width(cell: AskCell) -> Optional[int]
```

Return the default width of a compact input, None for a check box.

A typed input fits a typical value rather than its format hint, which
the tooltip shows as well, and a choice input fits its longest choice.

<a id="wizard_tk_bridge.wizard_cell._entry_widget"></a>

#### \_entry\_widget

```python
def _entry_widget(cell_input: CellInput) -> tk.Entry
```

Return the text entry of a text or integer input.

<a id="wizard_tk_bridge.wizard_cell._int_value"></a>

#### \_int\_value

```python
def _int_value(cell_input: CellInput, cell: AskIntCell) -> Optional[int]
```

Return the integer value of an input, or its default when empty.

<a id="wizard_tk_bridge.wizard_cell._path_value"></a>

#### \_path\_value

```python
def _path_value(cell_input: CellInput, cell: AskPathCell) -> Optional[Path]
```

Return the accepted path of an input, or None when not accepted.

<a id="wizard_tk_bridge.wizard_cell._choice_value"></a>

#### \_choice\_value

```python
def _choice_value(cell_input: CellInput) -> Optional[str]
```

Return the chosen value of an input, or None when none is chosen.

<a id="wizard_tk_bridge.wizard_cell._multi_selected"></a>

#### \_multi\_selected

```python
def _multi_selected(cell_input: CellInput) -> list[int]
```

Return the selected 0-based indexes of a multi-selection input.

<a id="wizard_tk_bridge.wizard_cell._multi_values"></a>

#### \_multi\_values

```python
def _multi_values(cell_input: CellInput,
                  cell: AskMultiChoiceCell) -> list[str]
```

Return the chosen values of a multi-selection input, in order.

<a id="wizard_tk_bridge.wizard_cell._basic_value"></a>

#### \_basic\_value

```python
def _basic_value(cell_input: CellInput) -> Optional[PrefillValueType]
```

Return the answer value of an input of an original cell kind.

<a id="wizard_tk_bridge.wizard_cell._int_error"></a>

#### \_int\_error

```python
def _int_error(cell_input: CellInput, cell: AskIntCell) -> Optional[str]
```

Return the integer input's own validation error, or None.

<a id="wizard_tk_bridge.wizard_cell._basic_error"></a>

#### \_basic\_error

```python
def _basic_error(cell_input: CellInput) -> Optional[str]
```

Return the own error of an input of an original cell kind.

<a id="wizard_tk_bridge.wizard_cell._set_entry_text"></a>

#### \_set\_entry\_text

```python
def _set_entry_text(entry: tk.Entry, text: str) -> None
```

Replace a text or integer entry's text, enabling it if disabled.

<a id="wizard_tk_bridge.wizard_cell._set_combo"></a>

#### \_set\_combo

```python
def _set_combo(box: ttk.Combobox, value: str) -> None
```

Set a drop-down's value, enabling it briefly if disabled.

<a id="wizard_tk_bridge.wizard_cell._set_multi"></a>

#### \_set\_multi

```python
def _set_multi(box: tk.Listbox, choices: Sequence[str],
               value: PrefillValueType) -> None
```

Select the values of a multi-selection list, enabling it briefly.

<a id="wizard_tk_bridge.wizard_cell._scroll_canvas"></a>

#### \_scroll\_canvas

```python
def _scroll_canvas(outer: tk.Frame, sideways: bool) -> tk.Canvas
```

Grid a canvas with auto-hiding scrollbars into outer's first cells.

The vertical scrollbar is right of the canvas, and a sideways one
below it. The wheel and touchpad scroll the canvas from its content.

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
def is_typed(field: AskCell) -> bool
```

Return whether field is one of the five typed fields or cells.

<a id="wizard_tk_bridge.wizard_typed.field_hint"></a>

#### field\_hint

```python
def field_hint(field: AskCell) -> str
```

Return the accepted-format hint shown for a typed field or cell.

<a id="wizard_tk_bridge.wizard_typed._default_of"></a>

#### \_default\_of

```python
def _default_of(field: AskCell) -> Optional[PrefillValueType]
```

Return the default of a typed field or cell.

<a id="wizard_tk_bridge.wizard_typed._resolve"></a>

#### \_resolve

```python
def _resolve(field: AskCell,
             text: str) -> tuple[Optional[PrefillValueType], Optional[str]]
```

Return a typed field's parsed value and any parse or range error.

<a id="wizard_tk_bridge.wizard_typed._checked"></a>

#### \_checked

```python
def _checked(
    value: Optional[_Ordered], field: AskCell, minimum: Optional[_Ordered],
    maximum: Optional[_Ordered]
) -> tuple[Optional[PrefillValueType], Optional[str]]
```

Return value and no error, or None and the reason it is unusable.

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

<a id="wizard_tk_bridge.wizard_form._enable_row"></a>

#### \_enable\_row

```python
def _enable_row(row: FormRow, enabled: bool) -> None
```

Enable or disable one form row, greying its label when disabled.

<a id="wizard_tk_bridge.wizard_form._row_tooltip"></a>

#### \_row\_tooltip

```python
def _row_tooltip(field: AskField, label: tk.Label,
                 widget: tk.Widget) -> Optional[HelpTooltip]
```

Return a hover tooltip for the field's help and format hint.

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

Return the current answer of one row read from its input.

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
picker, ask_form() shows a whole form on one screen so the user
answers related fields together in any order, and ask_matrix_form()
shows a whole grid of cells on one screen the same way. A table question
is asked by the inherited WizardUiBridge.ask_table() through
ask_matrix_form(), so it is a grid too. All questions of one
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
tooltip instead, and so does the inherited ask_table().

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

<a id="wizard_tk_bridge.wizard_path.PathRow._browse"></a>

#### \_browse

```python
def _browse() -> None
```

Open the native picker and fill the entry with the choice.

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

<a id="wizard_tk_bridge.wizard_matrix._cell_tooltip"></a>

#### \_cell\_tooltip

```python
def _cell_tooltip(ask: AskCell, widget: tk.Widget) -> Optional[HelpTooltip]
```

Return a hover tooltip for the cell's help and format hint.

<a id="wizard_tk_bridge.wizard_matrix._label"></a>

#### \_label

```python
def _label(parent: tk.Misc, ask: AskLabelCell) -> tk.Label
```

Return the label of a label cell, wrapped at its width hint.

<a id="wizard_tk_bridge.wizard_matrix._label_font"></a>

#### \_label\_font

```python
def _label_font(parent: tk.Misc, ask: AskLabelCell) -> tuple[str, int, str]
```

Return the default font in the bold and italic style of a label.

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

<a id="wizard_tk_bridge.wizard_matrix.MatrixEditor._allowed"></a>

#### \_allowed

```python
def _allowed() -> dict[str, bool]
```

Return for each resize action whether the bounds allow it.

<a id="wizard_tk_bridge.wizard_matrix.MatrixEditor._update_resizers"></a>

#### \_update\_resizers

```python
def _update_resizers() -> None
```

Grey out each resize button whose action the bounds forbid.

<a id="wizard_tk_bridge.wizard_matrix.MatrixEditor._append_row"></a>

#### \_append\_row

```python
def _append_row() -> None
```

Build the cells of a new last row of the current columns.

<a id="wizard_tk_bridge.wizard_matrix.MatrixEditor._reshaped"></a>

#### \_reshaped

```python
def _reshaped(edge: Sequence[CellPosition], focus: bool) -> None
```

Update the resize buttons and re-validate the whole matrix.

edge is the new last row or column, which gets the keyboard focus
when focus is True.

<a id="wizard_tk_bridge.wizard_matrix.MatrixEditor._destroy"></a>

#### \_destroy

```python
def _destroy(cells: Sequence[MatrixCell]) -> bool
```

Destroy deleted cells, telling whether one of them had focus.

<a id="wizard_tk_bridge.wizard_matrix.MatrixEditor._focus_path"></a>

#### \_focus\_path

```python
def _focus_path() -> str
```

Return the path name of the widget last focused in the window.

The window keeps it also while another application is active.

<a id="wizard_tk_bridge.wizard_matrix.MatrixEditor._focus_first"></a>

#### \_focus\_first

```python
def _focus_first(positions: Sequence[CellPosition]) -> None
```

Reveal the first enabled input, else the first of the cells.

<a id="wizard_tk_bridge.wizard_matrix.MatrixEditor._focusable"></a>

#### \_focusable

```python
def _focusable(position: CellPosition) -> bool
```

Return whether a cell is an enabled input.

<a id="wizard_tk_bridge.wizard_matrix.MatrixEditor._reveal"></a>

#### \_reveal

```python
def _reveal(position: CellPosition) -> None
```

Scroll a cell into view, focusing it when it is focusable.

<a id="wizard_tk_bridge.wizard_matrix.MatrixEditor._build_cell"></a>

#### \_build\_cell

```python
def _build_cell(position: CellPosition) -> MatrixCell
```

Build and place the label or input of one cell.

<a id="wizard_tk_bridge.wizard_matrix.MatrixEditor._new_widget"></a>

#### \_new\_widget

```python
def _new_widget(
        ask: AskCell,
        position: CellPosition) -> tuple[tk.Widget, Optional[CellInput]]
```

Return a new label, or a new input bound to Return and change.

<a id="wizard_tk_bridge.wizard_matrix.MatrixEditor._positions"></a>

#### \_positions

```python
def _positions() -> Iterator[CellPosition]
```

Yield every position of the current shape, row by row.

<a id="wizard_tk_bridge.wizard_matrix.MatrixEditor._row_line"></a>

#### \_row\_line

```python
def _row_line(row: int) -> list[CellPosition]
```

Return the positions of one row of the current shape.

<a id="wizard_tk_bridge.wizard_matrix.MatrixEditor._column_line"></a>

#### \_column\_line

```python
def _column_line(column: int) -> list[CellPosition]
```

Return the positions of one column, top to bottom.

<a id="wizard_tk_bridge.wizard_matrix.MatrixEditor._asks"></a>

#### \_asks

```python
def _asks() -> list[list[AskCell]]
```

Return the AskCells of the current shape, one list per row.

<a id="wizard_tk_bridge.wizard_matrix.MatrixEditor._changed"></a>

#### \_changed

```python
def _changed(position: CellPosition) -> None
```

React to a cell change with live feedback and cell enabling.

<a id="wizard_tk_bridge.wizard_matrix.MatrixEditor._validate"></a>

#### \_validate

```python
def _validate(changed: Optional[CellPosition], live: bool) -> Optional[str]
```

Run the partial validator and return its message when invalid.

The disabled cells of its result are applied, and while the user
edits (live) its prefills too, which are ignored on submit.

<a id="wizard_tk_bridge.wizard_matrix.MatrixEditor._apply_disabled"></a>

#### \_apply\_disabled

```python
def _apply_disabled(positions: tuple[CellPosition, ...]) -> None
```

Enable or disable each input to match the validator result.

<a id="wizard_tk_bridge.wizard_matrix.MatrixEditor._apply_prefills"></a>

#### \_apply\_prefills

```python
def _apply_prefills(prefills: PrefillCellValues,
                    changed: Optional[CellPosition]) -> None
```

Write the validator's valid prefills into their cell inputs.

<a id="wizard_tk_bridge.wizard_matrix.MatrixEditor._first_invalid"></a>

#### \_first\_invalid

```python
def _first_invalid() -> Optional[CellPosition]
```

Return the first enabled cell failing its own check, or None.

<a id="wizard_tk_bridge.wizard_matrix.MatrixEditor._cell_error"></a>

#### \_cell\_error

```python
def _cell_error(position: CellPosition) -> Optional[str]
```

Return one cell's own error, prefixed with the cell's name.

The whole matrix shares one status line, so naming the cell, by
the CellNamer of the request or by its labels, makes clear which
cell a message refers to.

<a id="wizard_tk_bridge.wizard_matrix.MatrixEditor._cell"></a>

#### \_cell

```python
def _cell(position: CellPosition) -> MatrixCell
```

Return the built cell at a position of the current shape.

<a id="wizard_tk_bridge.wizard_matrix.MatrixEditor._show"></a>

#### \_show

```python
def _show(message: str) -> None
```

Show a status message below the matrix.

<a id="wizard_tk_bridge.wizard_window"></a>

# wizard\_tk\_bridge.wizard\_window

A Tk host that asks every wizard prompt in turn, one at a time.

:class:`WizardWindow` lays out one question at a time: a text entry, an
integer entry, a path entry with a native Browse button, a yes/no button
pair, a single- and a multi-selection list, a whole form and a whole
matrix form on one screen, kept below a lasting message area. Every prompt also
offers back, out-one-level and abort buttons, which raise the matching
:class:`WizardNavigation` request so the wizard can step within its
questions or be abandoned.

Return pressed in an input confirms the prompt, exactly as its OK button
does, which that button shows by being the marked default one. A matrix
form binds Return in each input as it builds it, so a row or column it
adds later confirms the matrix too. A table question is asked by the
inherited WizardUiBridge.ask_table() as a matrix form.

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

Return the initial path text: the start value, else the default.

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

<a id="wizard_tk_bridge.wizard_window.WizardWindow._run_int"></a>

#### \_run\_int

```python
def _run_int(question: str, re_ask: Optional[str], seed: Optional[int]) -> str
```

Show one integer entry pre-filled with seed; return its text.

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

<a id="wizard_tk_bridge.wizard_window.WizardWindow._run_multi"></a>

#### \_run\_multi

```python
def _run_multi(question: str, re_ask: Optional[str], choices: Sequence[str],
               start: Optional[Sequence[str]]) -> list[str]
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
def _pick_one(listbox: tk.Listbox, choices: Sequence[Optional[str]]) -> None
```

Finish a single-choice question with the selected row's answer.

choices holds the answer of each list row, in row order.

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

Add the confirm and navigation buttons, and bind Return.

The confirm button is marked as the default one, which is how a
platform shows that pressing Return does the same thing.

<a id="wizard_tk_bridge.wizard_window.WizardWindow._ok_box"></a>

#### \_ok\_box

```python
def _ok_box(on_ok: Callable[[], None]) -> tk.Frame
```

Add the button frame holding the default OK button; return it.

<a id="wizard_tk_bridge.wizard_window.WizardWindow._button_box"></a>

#### \_button\_box

```python
def _button_box() -> tk.Frame
```

Add and return the frame holding a prompt's buttons.

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

Request abandoning the whole wizard.

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

