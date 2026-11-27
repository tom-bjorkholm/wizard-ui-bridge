# Table of Contents

* [wizard\_ui\_bridge](#wizard_ui_bridge)
  * [\_\_getattr\_\_](#wizard_ui_bridge.__getattr__)
* [wizard\_ui\_bridge.\_path](#wizard_ui_bridge._path)
  * [\_start\_dir](#wizard_ui_bridge._path._start_dir)
  * [\_start\_value](#wizard_ui_bridge._path._start_value)
  * [\_new\_child\_prefix](#wizard_ui_bridge._path._new_child_prefix)
  * [\_selection\_text](#wizard_ui_bridge._path._selection_text)
  * [\_seed\_path](#wizard_ui_bridge._path._seed_path)
  * [\_PathPick](#wizard_ui_bridge._path._PathPick)
    * [pick\_widgets](#wizard_ui_bridge._path._PathPick.pick_widgets)
    * [\_file\_selected](#wizard_ui_bridge._path._PathPick._file_selected)
    * [\_dir\_selected](#wizard_ui_bridge._path._PathPick._dir_selected)
    * [\_input\_entered](#wizard_ui_bridge._path._PathPick._input_entered)
    * [action\_submit](#wizard_ui_bridge._path._PathPick.action_submit)
    * [\_fill\_input](#wizard_ui_bridge._path._PathPick._fill_input)
    * [\_confirm](#wizard_ui_bridge._path._PathPick._confirm)
  * [\_PickerScreen](#wizard_ui_bridge._path._PickerScreen)
    * [\_\_init\_\_](#wizard_ui_bridge._path._PickerScreen.__init__)
    * [compose](#wizard_ui_bridge._path._PickerScreen.compose)
    * [\_submit\_clicked](#wizard_ui_bridge._path._PickerScreen._submit_clicked)
    * [\_cancel\_clicked](#wizard_ui_bridge._path._PickerScreen._cancel_clicked)
    * [action\_cancel](#wizard_ui_bridge._path._PickerScreen.action_cancel)
    * [\_confirm](#wizard_ui_bridge._path._PickerScreen._confirm)
* [wizard\_ui\_bridge.\_ask\_cell](#wizard_ui_bridge._ask_cell)
  * [ask\_cell\_value](#wizard_ui_bridge._ask_cell.ask_cell_value)
  * [\_ask\_typed\_value](#wizard_ui_bridge._ask_cell._ask_typed_value)
  * [\_ask\_basic\_value](#wizard_ui_bridge._ask_cell._ask_basic_value)
  * [\_ask\_choice\_value](#wizard_ui_bridge._ask_cell._ask_choice_value)
* [wizard\_ui\_bridge.form\_defs](#wizard_ui_bridge.form_defs)
  * [value\_out\_of\_range](#wizard_ui_bridge.form_defs.value_out_of_range)
  * [AskFieldCommon](#wizard_ui_bridge.form_defs.AskFieldCommon)
  * [AskTextField](#wizard_ui_bridge.form_defs.AskTextField)
  * [AskIntField](#wizard_ui_bridge.form_defs.AskIntField)
  * [AskPathField](#wizard_ui_bridge.form_defs.AskPathField)
  * [AskYesNoField](#wizard_ui_bridge.form_defs.AskYesNoField)
  * [AskChoiceField](#wizard_ui_bridge.form_defs.AskChoiceField)
  * [AskMultiChoiceField](#wizard_ui_bridge.form_defs.AskMultiChoiceField)
  * [AskFloatField](#wizard_ui_bridge.form_defs.AskFloatField)
  * [AskDateField](#wizard_ui_bridge.form_defs.AskDateField)
  * [AskTimeField](#wizard_ui_bridge.form_defs.AskTimeField)
  * [AskDateTimeField](#wizard_ui_bridge.form_defs.AskDateTimeField)
  * [AskDurationField](#wizard_ui_bridge.form_defs.AskDurationField)
  * [ALL\_ASK\_FIELD\_TYPES](#wizard_ui_bridge.form_defs.ALL_ASK_FIELD_TYPES)
  * [AnswerTextField](#wizard_ui_bridge.form_defs.AnswerTextField)
  * [AnswerIntField](#wizard_ui_bridge.form_defs.AnswerIntField)
  * [AnswerPathField](#wizard_ui_bridge.form_defs.AnswerPathField)
  * [AnswerYesNoField](#wizard_ui_bridge.form_defs.AnswerYesNoField)
  * [AnswerChoiceField](#wizard_ui_bridge.form_defs.AnswerChoiceField)
  * [AnswerMultiChoiceField](#wizard_ui_bridge.form_defs.AnswerMultiChoiceField)
  * [AnswerFloatField](#wizard_ui_bridge.form_defs.AnswerFloatField)
  * [AnswerDateField](#wizard_ui_bridge.form_defs.AnswerDateField)
  * [AnswerTimeField](#wizard_ui_bridge.form_defs.AnswerTimeField)
  * [AnswerDateTimeField](#wizard_ui_bridge.form_defs.AnswerDateTimeField)
  * [AnswerDurationField](#wizard_ui_bridge.form_defs.AnswerDurationField)
  * [PartFormValidationResult](#wizard_ui_bridge.form_defs.PartFormValidationResult)
* [wizard\_ui\_bridge.console](#wizard_ui_bridge.console)
  * [WizardUiBridgeConsole](#wizard_ui_bridge.console.WizardUiBridgeConsole)
    * [\_\_init\_\_](#wizard_ui_bridge.console.WizardUiBridgeConsole.__init__)
    * [ask\_text](#wizard_ui_bridge.console.WizardUiBridgeConsole.ask_text)
    * [supports\_form\_field](#wizard_ui_bridge.console.WizardUiBridgeConsole.supports_form_field)
    * [ask\_yes\_no](#wizard_ui_bridge.console.WizardUiBridgeConsole.ask_yes_no)
    * [ask\_table](#wizard_ui_bridge.console.WizardUiBridgeConsole.ask_table)
    * [\_ask\_raw](#wizard_ui_bridge.console.WizardUiBridgeConsole._ask_raw)
    * [ask\_choice](#wizard_ui_bridge.console.WizardUiBridgeConsole.ask_choice)
    * [ask\_multi](#wizard_ui_bridge.console.WizardUiBridgeConsole.ask_multi)
    * [\_prompt](#wizard_ui_bridge.console.WizardUiBridgeConsole._prompt)
    * [\_emit\_question](#wizard_ui_bridge.console.WizardUiBridgeConsole._emit_question)
    * [\_read\_answer](#wizard_ui_bridge.console.WizardUiBridgeConsole._read_answer)
    * [\_read\_sensitive](#wizard_ui_bridge.console.WizardUiBridgeConsole._read_sensitive)
    * [error\_file](#wizard_ui_bridge.console.WizardUiBridgeConsole.error_file)
    * [show](#wizard_ui_bridge.console.WizardUiBridgeConsole.show)
  * [\_raise\_for\_navigation](#wizard_ui_bridge.console._raise_for_navigation)
  * [\_to\_index](#wizard_ui_bridge.console._to_index)
  * [\_single\_index](#wizard_ui_bridge.console._single_index)
  * [\_menu\_lines](#wizard_ui_bridge.console._menu_lines)
  * [\_multi\_question](#wizard_ui_bridge.console._multi_question)
* [wizard\_ui\_bridge.matrix\_helpers](#wizard_ui_bridge.matrix_helpers)
  * [cell\_at](#wizard_ui_bridge.matrix_helpers.cell_at)
  * [\_listed\_cell](#wizard_ui_bridge.matrix_helpers._listed_cell)
  * [valid\_cell\_prefills](#wizard_ui_bridge.matrix_helpers.valid_cell_prefills)
  * [\_input\_cell](#wizard_ui_bridge.matrix_helpers._input_cell)
  * [\_where](#wizard_ui_bridge.matrix_helpers._where)
  * [row\_label](#wizard_ui_bridge.matrix_helpers.row_label)
  * [column\_label](#wizard_ui_bridge.matrix_helpers.column_label)
  * [\_nearest\_label](#wizard_ui_bridge.matrix_helpers._nearest_label)
  * [cell\_name](#wizard_ui_bridge.matrix_helpers.cell_name)
  * [row\_name](#wizard_ui_bridge.matrix_helpers.row_name)
  * [column\_name](#wizard_ui_bridge.matrix_helpers.column_name)
  * [message\_name](#wizard_ui_bridge.matrix_helpers.message_name)
* [wizard\_ui\_bridge.\_help](#wizard_ui_bridge._help)
  * [HelpKwargs](#wizard_ui_bridge._help.HelpKwargs)
  * [help\_kwargs](#wizard_ui_bridge._help.help_kwargs)
  * [\_accepts\_help](#wizard_ui_bridge._help._accepts_help)
* [wizard\_ui\_bridge.matrix\_cell\_defs](#wizard_ui_bridge.matrix_cell_defs)
  * [\_OrderedValue](#wizard_ui_bridge.matrix_cell_defs._OrderedValue)
    * [\_\_lt\_\_](#wizard_ui_bridge.matrix_cell_defs._OrderedValue.__lt__)
    * [\_\_gt\_\_](#wizard_ui_bridge.matrix_cell_defs._OrderedValue.__gt__)
  * [value\_out\_of\_range](#wizard_ui_bridge.matrix_cell_defs.value_out_of_range)
  * [check\_bounds](#wizard_ui_bridge.matrix_cell_defs.check_bounds)
  * [AskCellCommon](#wizard_ui_bridge.matrix_cell_defs.AskCellCommon)
    * [\_\_post\_init\_\_](#wizard_ui_bridge.matrix_cell_defs.AskCellCommon.__post_init__)
  * [AskLabelCell](#wizard_ui_bridge.matrix_cell_defs.AskLabelCell)
  * [AskTextCell](#wizard_ui_bridge.matrix_cell_defs.AskTextCell)
    * [\_\_post\_init\_\_](#wizard_ui_bridge.matrix_cell_defs.AskTextCell.__post_init__)
  * [AskRangeCell](#wizard_ui_bridge.matrix_cell_defs.AskRangeCell)
    * [\_\_post\_init\_\_](#wizard_ui_bridge.matrix_cell_defs.AskRangeCell.__post_init__)
  * [AskIntCell](#wizard_ui_bridge.matrix_cell_defs.AskIntCell)
  * [AskPathCell](#wizard_ui_bridge.matrix_cell_defs.AskPathCell)
  * [AskYesNoCell](#wizard_ui_bridge.matrix_cell_defs.AskYesNoCell)
  * [AskChoiceCell](#wizard_ui_bridge.matrix_cell_defs.AskChoiceCell)
    * [\_\_post\_init\_\_](#wizard_ui_bridge.matrix_cell_defs.AskChoiceCell.__post_init__)
  * [AskMultiChoiceCell](#wizard_ui_bridge.matrix_cell_defs.AskMultiChoiceCell)
    * [\_\_post\_init\_\_](#wizard_ui_bridge.matrix_cell_defs.AskMultiChoiceCell.__post_init__)
  * [AskFloatCell](#wizard_ui_bridge.matrix_cell_defs.AskFloatCell)
  * [AskDateCell](#wizard_ui_bridge.matrix_cell_defs.AskDateCell)
  * [AskTimeCell](#wizard_ui_bridge.matrix_cell_defs.AskTimeCell)
  * [AskDateTimeCell](#wizard_ui_bridge.matrix_cell_defs.AskDateTimeCell)
  * [AskDurationCell](#wizard_ui_bridge.matrix_cell_defs.AskDurationCell)
  * [ALL\_ASK\_CELL\_TYPES](#wizard_ui_bridge.matrix_cell_defs.ALL_ASK_CELL_TYPES)
  * [AnswerTextCell](#wizard_ui_bridge.matrix_cell_defs.AnswerTextCell)
  * [AnswerIntCell](#wizard_ui_bridge.matrix_cell_defs.AnswerIntCell)
  * [AnswerPathCell](#wizard_ui_bridge.matrix_cell_defs.AnswerPathCell)
  * [AnswerYesNoCell](#wizard_ui_bridge.matrix_cell_defs.AnswerYesNoCell)
  * [AnswerChoiceCell](#wizard_ui_bridge.matrix_cell_defs.AnswerChoiceCell)
  * [AnswerMultiChoiceCell](#wizard_ui_bridge.matrix_cell_defs.AnswerMultiChoiceCell)
  * [AnswerFloatCell](#wizard_ui_bridge.matrix_cell_defs.AnswerFloatCell)
  * [AnswerDateCell](#wizard_ui_bridge.matrix_cell_defs.AnswerDateCell)
  * [AnswerTimeCell](#wizard_ui_bridge.matrix_cell_defs.AnswerTimeCell)
  * [AnswerDateTimeCell](#wizard_ui_bridge.matrix_cell_defs.AnswerDateTimeCell)
  * [AnswerDurationCell](#wizard_ui_bridge.matrix_cell_defs.AnswerDurationCell)
* [wizard\_ui\_bridge.\_textual\_table](#wizard_ui_bridge._textual_table)
  * [\_TableApp](#wizard_ui_bridge._textual_table._TableApp)
    * [\_\_init\_\_](#wizard_ui_bridge._textual_table._TableApp.__init__)
    * [compose](#wizard_ui_bridge._textual_table._TableApp.compose)
    * [on\_mount](#wizard_ui_bridge._textual_table._TableApp.on_mount)
    * [\_focus\_first\_cell](#wizard_ui_bridge._textual_table._TableApp._focus_first_cell)
    * [\_grid\_cells](#wizard_ui_bridge._textual_table._TableApp._grid_cells)
    * [\_row\_widgets](#wizard_ui_bridge._textual_table._TableApp._row_widgets)
    * [\_is\_readonly](#wizard_ui_bridge._textual_table._TableApp._is_readonly)
    * [\_cell\_widget](#wizard_ui_bridge._textual_table._TableApp._cell_widget)
    * [\_on\_input](#wizard_ui_bridge._textual_table._TableApp._on_input)
    * [\_on\_select](#wizard_ui_bridge._textual_table._TableApp._on_select)
    * [\_recheck](#wizard_ui_bridge._textual_table._TableApp._recheck)
    * [action\_submit](#wizard_ui_bridge._textual_table._TableApp.action_submit)
    * [\_submit\_clicked](#wizard_ui_bridge._textual_table._TableApp._submit_clicked)
    * [\_add\_clicked](#wizard_ui_bridge._textual_table._TableApp._add_clicked)
    * [\_remove\_clicked](#wizard_ui_bridge._textual_table._TableApp._remove_clicked)
    * [\_add\_row](#wizard_ui_bridge._textual_table._TableApp._add_row)
    * [\_remove\_row](#wizard_ui_bridge._textual_table._TableApp._remove_row)
    * [\_report](#wizard_ui_bridge._textual_table._TableApp._report)
    * [\_set\_status](#wizard_ui_bridge._textual_table._TableApp._set_status)
    * [\_read\_cell](#wizard_ui_bridge._textual_table._TableApp._read_cell)
* [wizard\_ui\_bridge.arg\_types](#wizard_ui_bridge.arg_types)
  * [AskReader](#wizard_ui_bridge.arg_types.AskReader)
    * [\_\_call\_\_](#wizard_ui_bridge.arg_types.AskReader.__call__)
  * [WizardNavigation](#wizard_ui_bridge.arg_types.WizardNavigation)
  * [WizardBack](#wizard_ui_bridge.arg_types.WizardBack)
  * [WizardCancelLevel](#wizard_ui_bridge.arg_types.WizardCancelLevel)
  * [WizardAbort](#wizard_ui_bridge.arg_types.WizardAbort)
  * [WizardPathKind](#wizard_ui_bridge.arg_types.WizardPathKind)
  * [check\_nullable](#wizard_ui_bridge.arg_types.check_nullable)
  * [check\_choice\_args](#wizard_ui_bridge.arg_types.check_choice_args)
  * [check\_multi\_args](#wizard_ui_bridge.arg_types.check_multi_args)
  * [PathAskOptions](#wizard_ui_bridge.arg_types.PathAskOptions)
    * [\_\_post\_init\_\_](#wizard_ui_bridge.arg_types.PathAskOptions.__post_init__)
  * [TableColumn](#wizard_ui_bridge.arg_types.TableColumn)
  * [TableCell](#wizard_ui_bridge.arg_types.TableCell)
    * [\_\_post\_init\_\_](#wizard_ui_bridge.arg_types.TableCell.__post_init__)
* [wizard\_ui\_bridge.matrix\_defs](#wizard_ui_bridge.matrix_defs)
  * [CellPosition](#wizard_ui_bridge.matrix_defs.CellPosition)
  * [MatrixDimension](#wizard_ui_bridge.matrix_defs.MatrixDimension)
    * [\_\_post\_init\_\_](#wizard_ui_bridge.matrix_defs.MatrixDimension.__post_init__)
  * [MatrixDimensions](#wizard_ui_bridge.matrix_defs.MatrixDimensions)
    * [\_\_post\_init\_\_](#wizard_ui_bridge.matrix_defs.MatrixDimensions.__post_init__)
    * [fixed](#wizard_ui_bridge.matrix_defs.MatrixDimensions.fixed)
  * [PartMatrixValidationRes](#wizard_ui_bridge.matrix_defs.PartMatrixValidationRes)
  * [MatrixConsoleQuestion](#wizard_ui_bridge.matrix_defs.MatrixConsoleQuestion)
  * [MatrixRequest](#wizard_ui_bridge.matrix_defs.MatrixRequest)
* [wizard\_ui\_bridge.form\_helpers](#wizard_ui_bridge.form_helpers)
  * [nullable\_choice](#wizard_ui_bridge.form_helpers.nullable_choice)
  * [initial\_answer](#wizard_ui_bridge.form_helpers.initial_answer)
  * [\_default\_value](#wizard_ui_bridge.form_helpers._default_value)
  * [answer\_of](#wizard_ui_bridge.form_helpers.answer_of)
  * [\_optional](#wizard_ui_bridge.form_helpers._optional)
  * [\_float\_value](#wizard_ui_bridge.form_helpers._float_value)
  * [\_text\_like\_answer](#wizard_ui_bridge.form_helpers._text_like_answer)
  * [\_choice\_answer](#wizard_ui_bridge.form_helpers._choice_answer)
  * [\_number\_answer](#wizard_ui_bridge.form_helpers._number_answer)
  * [\_temporal\_answer](#wizard_ui_bridge.form_helpers._temporal_answer)
  * [valid\_prefills](#wizard_ui_bridge.form_helpers.valid_prefills)
  * [\_check\_row](#wizard_ui_bridge.form_helpers._check_row)
  * [prefill\_value](#wizard_ui_bridge.form_helpers.prefill_value)
  * [\_ordered\_prefill](#wizard_ui_bridge.form_helpers._ordered_prefill)
  * [\_multi\_prefill](#wizard_ui_bridge.form_helpers._multi_prefill)
  * [\_need](#wizard_ui_bridge.form_helpers._need)
  * [\_bad\_type](#wizard_ui_bridge.form_helpers._bad_type)
  * [prefilled\_field](#wizard_ui_bridge.form_helpers.prefilled_field)
  * [\_default\_a](#wizard_ui_bridge.form_helpers._default_a)
  * [\_default\_b](#wizard_ui_bridge.form_helpers._default_b)
* [wizard\_ui\_bridge.bridge](#wizard_ui_bridge.bridge)
  * [WizardUiBridge](#wizard_ui_bridge.bridge.WizardUiBridge)
    * [ask\_text](#wizard_ui_bridge.bridge.WizardUiBridge.ask_text)
    * [ask\_int](#wizard_ui_bridge.bridge.WizardUiBridge.ask_int)
    * [ask\_path](#wizard_ui_bridge.bridge.WizardUiBridge.ask_path)
    * [ask\_yes\_no](#wizard_ui_bridge.bridge.WizardUiBridge.ask_yes_no)
    * [ask\_choice](#wizard_ui_bridge.bridge.WizardUiBridge.ask_choice)
    * [ask\_multi](#wizard_ui_bridge.bridge.WizardUiBridge.ask_multi)
    * [ask\_table](#wizard_ui_bridge.bridge.WizardUiBridge.ask_table)
    * [ask\_form](#wizard_ui_bridge.bridge.WizardUiBridge.ask_form)
    * [supports\_form\_field](#wizard_ui_bridge.bridge.WizardUiBridge.supports_form_field)
    * [ask\_form\_w\_fake](#wizard_ui_bridge.bridge.WizardUiBridge.ask_form_w_fake)
    * [ask\_matrix\_form](#wizard_ui_bridge.bridge.WizardUiBridge.ask_matrix_form)
    * [\_show\_question](#wizard_ui_bridge.bridge.WizardUiBridge._show_question)
    * [\_fill\_form](#wizard_ui_bridge.bridge.WizardUiBridge._fill_form)
    * [\_prev\_field](#wizard_ui_bridge.bridge.WizardUiBridge._prev_field)
    * [\_form\_feedback](#wizard_ui_bridge.bridge.WizardUiBridge._form_feedback)
    * [\_ask\_field](#wizard_ui_bridge.bridge.WizardUiBridge._ask_field)
    * [error\_file](#wizard_ui_bridge.bridge.WizardUiBridge.error_file)
    * [show](#wizard_ui_bridge.bridge.WizardUiBridge.show)
* [wizard\_ui\_bridge.factory](#wizard_ui_bridge.factory)
  * [textual\_installed](#wizard_ui_bridge.factory.textual_installed)
  * [load\_textual\_bridge](#wizard_ui_bridge.factory.load_textual_bridge)
  * [UiBridgeType](#wizard_ui_bridge.factory.UiBridgeType)
  * [make\_text\_ui\_bridge](#wizard_ui_bridge.factory.make_text_ui_bridge)
  * [\_is\_tty](#wizard_ui_bridge.factory._is_tty)
* [wizard\_ui\_bridge.\_parse](#wizard_ui_bridge._parse)
  * [NEW\_FIELD\_TYPES](#wizard_ui_bridge._parse.NEW_FIELD_TYPES)
  * [parse\_float](#wizard_ui_bridge._parse.parse_float)
  * [parse\_date](#wizard_ui_bridge._parse.parse_date)
  * [parse\_time](#wizard_ui_bridge._parse.parse_time)
  * [parse\_datetime](#wizard_ui_bridge._parse.parse_datetime)
  * [parse\_duration](#wizard_ui_bridge._parse.parse_duration)
  * [\_timedelta\_seconds](#wizard_ui_bridge._parse._timedelta_seconds)
  * [\_timedelta\_parts](#wizard_ui_bridge._parse._timedelta_parts)
  * [format\_duration](#wizard_ui_bridge._parse.format_duration)
  * [format\_new\_value](#wizard_ui_bridge._parse.format_new_value)
  * [ordered\_range\_error](#wizard_ui_bridge._parse.ordered_range_error)
  * [\_AskText](#wizard_ui_bridge._parse._AskText)
    * [\_\_call\_\_](#wizard_ui_bridge._parse._AskText.__call__)
  * [\_TypedCell](#wizard_ui_bridge._parse._TypedCell)
  * [ask\_typed](#wizard_ui_bridge._parse.ask_typed)
  * [\_resolve](#wizard_ui_bridge._parse._resolve)
  * [resolve\_new](#wizard_ui_bridge._parse.resolve_new)
  * [new\_answer](#wizard_ui_bridge._parse.new_answer)
  * [field\_hint](#wizard_ui_bridge._parse.field_hint)
  * [\_new\_bounds](#wizard_ui_bridge._parse._new_bounds)
  * [value\_from\_text](#wizard_ui_bridge._parse.value_from_text)
  * [error\_from\_text](#wizard_ui_bridge._parse.error_from_text)
  * [fake\_field](#wizard_ui_bridge._parse.fake_field)
* [wizard\_ui\_bridge.\_table](#wizard_ui_bridge._table)
  * [\_ADD\_ROW](#wizard_ui_bridge._table._ADD_ROW)
  * [\_DEL\_ROW](#wizard_ui_bridge._table._DEL_ROW)
  * [\_VarTable](#wizard_ui_bridge._table._VarTable)
    * [\_\_init\_\_](#wizard_ui_bridge._table._VarTable.__init__)
    * [step](#wizard_ui_bridge._table._VarTable.step)
    * [\_menu\_help](#wizard_ui_bridge._table._VarTable._menu_help)
    * [\_accept](#wizard_ui_bridge._table._VarTable._accept)
    * [\_add](#wizard_ui_bridge._table._VarTable._add)
    * [\_delete](#wizard_ui_bridge._table._VarTable._delete)
    * [\_edit](#wizard_ui_bridge._table._VarTable._edit)
    * [\_edit\_row](#wizard_ui_bridge._table._VarTable._edit_row)
    * [\_fill\_one](#wizard_ui_bridge._table._VarTable._fill_one)
    * [\_editable](#wizard_ui_bridge._table._VarTable._editable)
  * [\_run\_variable\_table](#wizard_ui_bridge._table._run_variable_table)
  * [\_overview\_lines](#wizard_ui_bridge._table._overview_lines)
  * [\_column\_widths](#wizard_ui_bridge._table._column_widths)
  * [\_overview\_line](#wizard_ui_bridge._table._overview_line)
  * [\_cell\_text](#wizard_ui_bridge._table._cell_text)
* [wizard\_ui\_bridge.\_form\_prefill](#wizard_ui_bridge._form_prefill)
  * [apply\_prefills](#wizard_ui_bridge._form_prefill.apply_prefills)
  * [\_set\_field](#wizard_ui_bridge._form_prefill._set_field)
  * [\_set\_multi](#wizard_ui_bridge._form_prefill._set_multi)
* [wizard\_ui\_bridge.\_calendar](#wizard_ui_bridge._calendar)
  * [\_shift](#wizard_ui_bridge._calendar._shift)
  * [\_CalendarScreen](#wizard_ui_bridge._calendar._CalendarScreen)
    * [\_\_init\_\_](#wizard_ui_bridge._calendar._CalendarScreen.__init__)
    * [compose](#wizard_ui_bridge._calendar._CalendarScreen.compose)
    * [on\_mount](#wizard_ui_bridge._calendar._CalendarScreen.on_mount)
    * [\_show\_month](#wizard_ui_bridge._calendar._CalendarScreen._show_month)
    * [\_grid\_widgets](#wizard_ui_bridge._calendar._CalendarScreen._grid_widgets)
    * [\_day\_widget](#wizard_ui_bridge._calendar._CalendarScreen._day_widget)
    * [\_day\_disabled](#wizard_ui_bridge._calendar._CalendarScreen._day_disabled)
    * [\_pressed](#wizard_ui_bridge._calendar._CalendarScreen._pressed)
    * [action\_cancel](#wizard_ui_bridge._calendar._CalendarScreen.action_cancel)
    * [action\_step\_day](#wizard_ui_bridge._calendar._CalendarScreen.action_step_day)
    * [\_focus\_start\_day](#wizard_ui_bridge._calendar._CalendarScreen._focus_start_day)
    * [\_focused\_day](#wizard_ui_bridge._calendar._CalendarScreen._focused_day)
    * [\_focus\_day](#wizard_ui_bridge._calendar._CalendarScreen._focus_day)
    * [\_nearest\_enabled](#wizard_ui_bridge._calendar._CalendarScreen._nearest_enabled)
* [wizard\_ui\_bridge.\_textual\_nav](#wizard_ui_bridge._textual_nav)
  * [\_NavApp](#wizard_ui_bridge._textual_nav._NavApp)
    * [\_\_init\_\_](#wizard_ui_bridge._textual_nav._NavApp.__init__)
    * [action\_nav\_back](#wizard_ui_bridge._textual_nav._NavApp.action_nav_back)
    * [action\_nav\_cancel](#wizard_ui_bridge._textual_nav._NavApp.action_nav_cancel)
* [wizard\_ui\_bridge.\_matrix\_console](#wizard_ui_bridge._matrix_console)
  * [\_Line](#wizard_ui_bridge._matrix_console._Line)
  * [\_Menu](#wizard_ui_bridge._matrix_console._Menu)
  * [ConsoleMatrix](#wizard_ui_bridge._matrix_console.ConsoleMatrix)
    * [\_\_init\_\_](#wizard_ui_bridge._matrix_console.ConsoleMatrix.__init__)
    * [run](#wizard_ui_bridge._matrix_console.ConsoleMatrix.run)
    * [\_first\_steps](#wizard_ui_bridge._matrix_console.ConsoleMatrix._first_steps)
    * [\_run\_step](#wizard_ui_bridge._matrix_console.ConsoleMatrix._run_step)
    * [\_back](#wizard_ui_bridge._matrix_console.ConsoleMatrix._back)
    * [\_ask](#wizard_ui_bridge._matrix_console.ConsoleMatrix._ask)
    * [\_question](#wizard_ui_bridge._matrix_console.ConsoleMatrix._question)
    * [\_menu](#wizard_ui_bridge._matrix_console.ConsoleMatrix._menu)
    * [\_label](#wizard_ui_bridge._matrix_console.ConsoleMatrix._label)
    * [\_menu\_help](#wizard_ui_bridge._matrix_console.ConsoleMatrix._menu_help)
    * [\_words](#wizard_ui_bridge._matrix_console.ConsoleMatrix._words)
    * [\_fits](#wizard_ui_bridge._matrix_console.ConsoleMatrix._fits)
    * [\_resizable](#wizard_ui_bridge._matrix_console.ConsoleMatrix._resizable)
    * [\_has\_input](#wizard_ui_bridge._matrix_console.ConsoleMatrix._has_input)
    * [\_askable](#wizard_ui_bridge._matrix_console.ConsoleMatrix._askable)
    * [\_validate](#wizard_ui_bridge._matrix_console.ConsoleMatrix._validate)
    * [\_reshape](#wizard_ui_bridge._matrix_console.ConsoleMatrix._reshape)
    * [\_kept\_cell](#wizard_ui_bridge._matrix_console.ConsoleMatrix._kept_cell)
    * [\_kept\_answer](#wizard_ui_bridge._matrix_console.ConsoleMatrix._kept_answer)
    * [\_span](#wizard_ui_bridge._matrix_console.ConsoleMatrix._span)
    * [\_dimension](#wizard_ui_bridge._matrix_console.ConsoleMatrix._dimension)
    * [\_position](#wizard_ui_bridge._matrix_console.ConsoleMatrix._position)
  * [\_inside](#wizard_ui_bridge._matrix_console._inside)
  * [\_start\_answer](#wizard_ui_bridge._matrix_console._start_answer)
* [wizard\_ui\_bridge.\_fake](#wizard_ui_bridge._fake)
  * [\_FakeableBridge](#wizard_ui_bridge._fake._FakeableBridge)
    * [supports\_form\_field](#wizard_ui_bridge._fake._FakeableBridge.supports_form_field)
    * [ask\_form](#wizard_ui_bridge._fake._FakeableBridge.ask_form)
  * [ask\_form\_faking](#wizard_ui_bridge._fake.ask_form_faking)
  * [\_plan](#wizard_ui_bridge._fake._plan)
  * [\_real\_answer](#wizard_ui_bridge._fake._real_answer)
  * [\_wrap\_validator](#wizard_ui_bridge._fake._wrap_validator)
  * [\_convert\_prefills](#wizard_ui_bridge._fake._convert_prefills)
  * [\_fake\_guidance](#wizard_ui_bridge._fake._fake_guidance)
* [wizard\_ui\_bridge.\_table\_matrix](#wizard_ui_bridge._table_matrix)
  * [TableMatrix](#wizard_ui_bridge._table_matrix.TableMatrix)
    * [\_\_init\_\_](#wizard_ui_bridge._table_matrix.TableMatrix.__init__)
    * [request](#wizard_ui_bridge._table_matrix.TableMatrix.request)
    * [values](#wizard_ui_bridge._table_matrix.TableMatrix.values)
    * [cell\_name](#wizard_ui_bridge._table_matrix.TableMatrix.cell_name)
    * [\_dimensions](#wizard_ui_bridge._table_matrix.TableMatrix._dimensions)
    * [\_value](#wizard_ui_bridge._table_matrix.TableMatrix._value)
    * [\_validate](#wizard_ui_bridge._table_matrix.TableMatrix._validate)
  * [\_starting\_row](#wizard_ui_bridge._table_matrix._starting_row)
  * [\_input\_cell](#wizard_ui_bridge._table_matrix._input_cell)
* [wizard\_ui\_bridge.\_textual\_widgets](#wizard_ui_bridge._textual_widgets)
  * [\_header\_widgets](#wizard_ui_bridge._textual_widgets._header_widgets)
  * [\_default\_index](#wizard_ui_bridge._textual_widgets._default_index)
  * [\_preselected](#wizard_ui_bridge._textual_widgets._preselected)
  * [\_parse\_cell\_id](#wizard_ui_bridge._textual_widgets._parse_cell_id)
  * [\_make\_select](#wizard_ui_bridge._textual_widgets._make_select)
  * [\_choice\_select](#wizard_ui_bridge._textual_widgets._choice_select)
  * [\_multi\_selection](#wizard_ui_bridge._textual_widgets._multi_selection)
  * [\_path\_field\_row](#wizard_ui_bridge._textual_widgets._path_field_row)
  * [\_pick\_field\_row](#wizard_ui_bridge._textual_widgets._pick_field_row)
  * [\_make\_field\_widget](#wizard_ui_bridge._textual_widgets._make_field_widget)
  * [\_new\_field\_widget](#wizard_ui_bridge._textual_widgets._new_field_widget)
  * [\_basic\_field\_widget](#wizard_ui_bridge._textual_widgets._basic_field_widget)
  * [\_apply\_width](#wizard_ui_bridge._textual_widgets._apply_width)
  * [\_id\_index](#wizard_ui_bridge._textual_widgets._id_index)
  * [\_field\_index](#wizard_ui_bridge._textual_widgets._field_index)
  * [\_browse\_index](#wizard_ui_bridge._textual_widgets._browse_index)
  * [\_pick\_index](#wizard_ui_bridge._textual_widgets._pick_index)
  * [\_multi\_error](#wizard_ui_bridge._textual_widgets._multi_error)
  * [\_field\_message](#wizard_ui_bridge._textual_widgets._field_message)
  * [\_cell\_message](#wizard_ui_bridge._textual_widgets._cell_message)
  * [\_date\_of](#wizard_ui_bridge._textual_widgets._date_of)
  * [\_calendar\_setup](#wizard_ui_bridge._textual_widgets._calendar_setup)
  * [\_combined\_text](#wizard_ui_bridge._textual_widgets._combined_text)
* [wizard\_ui\_bridge.bridge\_helpers](#wizard_ui_bridge.bridge_helpers)
  * [\_ERASE\_TOKEN](#wizard_ui_bridge.bridge_helpers._ERASE_TOKEN)
  * [NO\_CHOICE](#wizard_ui_bridge.bridge_helpers.NO_CHOICE)
  * [check\_text\_args](#wizard_ui_bridge.bridge_helpers.check_text_args)
  * [question\_with\_default](#wizard_ui_bridge.bridge_helpers.question_with_default)
  * [text\_answer](#wizard_ui_bridge.bridge_helpers.text_answer)
  * [path\_answer](#wizard_ui_bridge.bridge_helpers.path_answer)
  * [\_path\_error](#wizard_ui_bridge.bridge_helpers._path_error)
  * [\_path\_exists](#wizard_ui_bridge.bridge_helpers._path_exists)
  * [\_path\_must\_exist](#wizard_ui_bridge.bridge_helpers._path_must_exist)
  * [\_path\_must\_not\_exist](#wizard_ui_bridge.bridge_helpers._path_must_not_exist)
  * [\_path\_must\_be\_file](#wizard_ui_bridge.bridge_helpers._path_must_be_file)
  * [\_path\_must\_be\_dir](#wizard_ui_bridge.bridge_helpers._path_must_be_dir)
  * [\_interpret\_yes\_no](#wizard_ui_bridge.bridge_helpers._interpret_yes_no)
  * [\_yes\_no\_from\_index](#wizard_ui_bridge.bridge_helpers._yes_no_from_index)
  * [\_yes\_no\_from\_text](#wizard_ui_bridge.bridge_helpers._yes_no_from_text)
  * [ask\_yes\_no](#wizard_ui_bridge.bridge_helpers.ask_yes_no)
  * [run\_table](#wizard_ui_bridge.bridge_helpers.run_table)
  * [\_fill\_table](#wizard_ui_bridge.bridge_helpers._fill_table)
  * [fill\_cell](#wizard_ui_bridge.bridge_helpers.fill_cell)
  * [\_cell\_prompt](#wizard_ui_bridge.bridge_helpers._cell_prompt)
  * [cell\_checker](#wizard_ui_bridge.bridge_helpers.cell_checker)
  * [\_cell\_value](#wizard_ui_bridge.bridge_helpers._cell_value)
  * [\_kept\_value](#wizard_ui_bridge.bridge_helpers._kept_value)
  * [\_erased\_value](#wizard_ui_bridge.bridge_helpers._erased_value)
  * [\_indexed\_value](#wizard_ui_bridge.bridge_helpers._indexed_value)
  * [\_named\_value](#wizard_ui_bridge.bridge_helpers._named_value)
  * [\_choice\_result](#wizard_ui_bridge.bridge_helpers._choice_result)
  * [int\_text](#wizard_ui_bridge.bridge_helpers.int_text)
  * [out\_of\_range](#wizard_ui_bridge.bridge_helpers.out_of_range)
  * [range\_error](#wizard_ui_bridge.bridge_helpers.range_error)
  * [ask\_one](#wizard_ui_bridge.bridge_helpers.ask_one)
  * [offered\_choices](#wizard_ui_bridge.bridge_helpers.offered_choices)
  * [ask\_many](#wizard_ui_bridge.bridge_helpers.ask_many)
  * [\_resolve\_choice](#wizard_ui_bridge.bridge_helpers._resolve_choice)
  * [\_resolve\_multi](#wizard_ui_bridge.bridge_helpers._resolve_multi)
  * [\_multi\_labels](#wizard_ui_bridge.bridge_helpers._multi_labels)
  * [\_tokens\_to\_labels](#wizard_ui_bridge.bridge_helpers._tokens_to_labels)
  * [match\_token](#wizard_ui_bridge.bridge_helpers.match_token)
  * [\_best\_match](#wizard_ui_bridge.bridge_helpers._best_match)
  * [\_choice\_at\_index](#wizard_ui_bridge.bridge_helpers._choice_at_index)
  * [multi\_count\_error](#wizard_ui_bridge.bridge_helpers.multi_count_error)
  * [multi\_count\_message](#wizard_ui_bridge.bridge_helpers.multi_count_message)
  * [\_uniform](#wizard_ui_bridge.bridge_helpers._uniform)
  * [new\_row\_template](#wizard_ui_bridge.bridge_helpers.new_row_template)
* [wizard\_ui\_bridge.textual\_bridge](#wizard_ui_bridge.textual_bridge)
  * [\_TextApp](#wizard_ui_bridge.textual_bridge._TextApp)
    * [\_\_init\_\_](#wizard_ui_bridge.textual_bridge._TextApp.__init__)
    * [compose](#wizard_ui_bridge.textual_bridge._TextApp.compose)
    * [\_entered](#wizard_ui_bridge.textual_bridge._TextApp._entered)
  * [\_PathApp](#wizard_ui_bridge.textual_bridge._PathApp)
    * [\_\_init\_\_](#wizard_ui_bridge.textual_bridge._PathApp.__init__)
    * [compose](#wizard_ui_bridge.textual_bridge._PathApp.compose)
    * [\_submit\_clicked](#wizard_ui_bridge.textual_bridge._PathApp._submit_clicked)
    * [\_confirm](#wizard_ui_bridge.textual_bridge._PathApp._confirm)
  * [\_ChoiceApp](#wizard_ui_bridge.textual_bridge._ChoiceApp)
    * [\_\_init\_\_](#wizard_ui_bridge.textual_bridge._ChoiceApp.__init__)
    * [compose](#wizard_ui_bridge.textual_bridge._ChoiceApp.compose)
    * [on\_mount](#wizard_ui_bridge.textual_bridge._ChoiceApp.on_mount)
    * [\_picked](#wizard_ui_bridge.textual_bridge._ChoiceApp._picked)
  * [\_MultiApp](#wizard_ui_bridge.textual_bridge._MultiApp)
    * [\_\_init\_\_](#wizard_ui_bridge.textual_bridge._MultiApp.__init__)
    * [compose](#wizard_ui_bridge.textual_bridge._MultiApp.compose)
    * [\_selections](#wizard_ui_bridge.textual_bridge._MultiApp._selections)
    * [\_clicked](#wizard_ui_bridge.textual_bridge._MultiApp._clicked)
    * [action\_submit](#wizard_ui_bridge.textual_bridge._MultiApp.action_submit)
  * [\_FormApp](#wizard_ui_bridge.textual_bridge._FormApp)
    * [\_\_init\_\_](#wizard_ui_bridge.textual_bridge._FormApp.__init__)
    * [compose](#wizard_ui_bridge.textual_bridge._FormApp.compose)
    * [\_field\_widgets](#wizard_ui_bridge.textual_bridge._FormApp._field_widgets)
    * [on\_mount](#wizard_ui_bridge.textual_bridge._FormApp.on_mount)
    * [\_input\_changed](#wizard_ui_bridge.textual_bridge._FormApp._input_changed)
    * [\_select\_changed](#wizard_ui_bridge.textual_bridge._FormApp._select_changed)
    * [\_checkbox\_changed](#wizard_ui_bridge.textual_bridge._FormApp._checkbox_changed)
    * [\_multi\_changed](#wizard_ui_bridge.textual_bridge._FormApp._multi_changed)
    * [\_changed](#wizard_ui_bridge.textual_bridge._FormApp._changed)
    * [\_maybe\_open\_calendar](#wizard_ui_bridge.textual_bridge._FormApp._maybe_open_calendar)
    * [\_apply\_validator](#wizard_ui_bridge.textual_bridge._FormApp._apply_validator)
    * [\_show\_live](#wizard_ui_bridge.textual_bridge._FormApp._show_live)
    * [\_apply\_disabled](#wizard_ui_bridge.textual_bridge._FormApp._apply_disabled)
    * [\_submit\_clicked](#wizard_ui_bridge.textual_bridge._FormApp._submit_clicked)
    * [\_browse\_clicked](#wizard_ui_bridge.textual_bridge._FormApp._browse_clicked)
    * [\_pick\_clicked](#wizard_ui_bridge.textual_bridge._FormApp._pick_clicked)
    * [\_open\_picker](#wizard_ui_bridge.textual_bridge._FormApp._open_picker)
    * [\_open\_calendar](#wizard_ui_bridge.textual_bridge._FormApp._open_calendar)
    * [\_path\_picked](#wizard_ui_bridge.textual_bridge._FormApp._path_picked)
    * [\_date\_picked](#wizard_ui_bridge.textual_bridge._FormApp._date_picked)
    * [action\_submit](#wizard_ui_bridge.textual_bridge._FormApp.action_submit)
    * [\_validator\_accepts](#wizard_ui_bridge.textual_bridge._FormApp._validator_accepts)
    * [\_first\_error](#wizard_ui_bridge.textual_bridge._FormApp._first_error)
    * [\_report](#wizard_ui_bridge.textual_bridge._FormApp._report)
    * [\_set\_status](#wizard_ui_bridge.textual_bridge._FormApp._set_status)
    * [\_read\_field](#wizard_ui_bridge.textual_bridge._FormApp._read_field)
    * [\_read\_new\_field](#wizard_ui_bridge.textual_bridge._FormApp._read_new_field)
    * [\_read\_basic\_field](#wizard_ui_bridge.textual_bridge._FormApp._read_basic_field)
    * [\_int\_value](#wizard_ui_bridge.textual_bridge._FormApp._int_value)
    * [\_field\_error](#wizard_ui_bridge.textual_bridge._FormApp._field_error)
    * [\_int\_error](#wizard_ui_bridge.textual_bridge._FormApp._int_error)
  * [WizardUiBridgeTextual](#wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual)
    * [\_\_init\_\_](#wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.__init__)
    * [ask\_text](#wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.ask_text)
    * [ask\_path](#wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.ask_path)
    * [ask\_yes\_no](#wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.ask_yes_no)
    * [ask\_choice](#wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.ask_choice)
    * [ask\_multi](#wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.ask_multi)
    * [ask\_table](#wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.ask_table)
    * [ask\_form](#wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.ask_form)
    * [supports\_form\_field](#wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.supports_form_field)
    * [\_run](#wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual._run)
    * [\_launch](#wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual._launch)
    * [\_collect](#wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual._collect)
    * [\_drain\_messages](#wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual._drain_messages)
    * [error\_file](#wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.error_file)
    * [show](#wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.show)

<a id="wizard_ui_bridge"></a>

# wizard\_ui\_bridge

Public API for the wizard user interface bridge.

A wizard asks a user a series of questions. WizardUiBridge is the
user-interface-independent way to ask them, so that one wizard can run
on a plain console, on a full-screen Textual user interface, or on any
other bridge an application implements.

The Textual bridge needs the optional textual package, installed with
the extra `wizard-ui-bridge[textual]`. Textual is imported only when
the Textual bridge is actually used, so importing this package, or
asking for WizardUiBridgeConsole, never imports Textual. Asking for
WizardUiBridgeTextual without textual installed raises ImportError
naming the extra to install.

Helpers for implementing a bridge of your own are in the modules
wizard_ui_bridge.bridge_helpers and wizard_ui_bridge.form_helpers.

<a id="wizard_ui_bridge.__getattr__"></a>

#### \_\_getattr\_\_

```python
def __getattr__(name: str) -> object
```

Return the Textual bridge class, imported on first use.

Textual is an optional dependency, so the Textual bridge is not
imported when this package is imported. Asking for it without
textual installed raises ImportError naming the extra to install.

<a id="wizard_ui_bridge._path"></a>

# wizard\_ui\_bridge.\_path

Reusable path-input machinery for the Textual wizard bridge.

The directory tree, the editable path input and the logic that fills
the input from a tree selection are shared between the standalone path
question and the directory picker opened from a form path field. This
module holds that shared machinery: the path helpers, the _PathPick
mixin that any host screen uses, and the _PickerScreen modal that a form
opens for one path field.

<a id="wizard_ui_bridge._path._start_dir"></a>

#### \_start\_dir

```python
def _start_dir(default: Optional[Path]) -> Path
```

Return the directory tree root for a path question.

<a id="wizard_ui_bridge._path._start_value"></a>

#### \_start\_value

```python
def _start_value(value: Optional[str], default: Optional[Path]) -> str
```

Return the initial path input text.

<a id="wizard_ui_bridge._path._new_child_prefix"></a>

#### \_new\_child\_prefix

```python
def _new_child_prefix(path: Path) -> str
```

Return path text ready for appending a child name.

<a id="wizard_ui_bridge._path._selection_text"></a>

#### \_selection\_text

```python
def _selection_text(path: Path, is_dir: bool, kind: WizardPathKind) -> str
```

Return the input text to use for a selected path.

<a id="wizard_ui_bridge._path._seed_path"></a>

#### \_seed\_path

```python
def _seed_path(value: str, default: Optional[Path]) -> Optional[Path]
```

Return the path whose folder roots the picker's tree.

<a id="wizard_ui_bridge._path._PathPick"></a>

## \_PathPick Objects

```python
class _PathPick(MessagePump)
```

Fill a path input from a directory-tree selection.

A host lays out the tree and input with pick_widgets(), keeps the
wanted WizardPathKind in _kind, and implements _confirm() to consume
the confirmed path text. Selecting in the tree fills the input;
Return in the input or the submit action confirms the current text.
It derives from MessagePump so that its @on handlers register when it
is mixed into a host screen or app.

<a id="wizard_ui_bridge._path._PathPick.pick_widgets"></a>

#### pick\_widgets

```python
def pick_widgets(start: Path, value: str) -> Iterator[Widget]
```

Yield the directory tree and the editable path input.

<a id="wizard_ui_bridge._path._PathPick._file_selected"></a>

#### \_file\_selected

```python
@on(DirectoryTree.FileSelected)
def _file_selected(event: DirectoryTree.FileSelected) -> None
```

Use the selected file as the editable input value.

<a id="wizard_ui_bridge._path._PathPick._dir_selected"></a>

#### \_dir\_selected

```python
@on(DirectoryTree.DirectorySelected)
def _dir_selected(event: DirectoryTree.DirectorySelected) -> None
```

Use the selected directory as value or editable prefix.

<a id="wizard_ui_bridge._path._PathPick._input_entered"></a>

#### \_input\_entered

```python
@on(Input.Submitted, f'#{_PATH_INPUT_ID}')
def _input_entered(event: Input.Submitted) -> None
```

Confirm the entered path when Return is pressed.

<a id="wizard_ui_bridge._path._PathPick.action_submit"></a>

#### action\_submit

```python
def action_submit() -> None
```

Confirm the current editable path input.

<a id="wizard_ui_bridge._path._PathPick._fill_input"></a>

#### \_fill\_input

```python
def _fill_input(path: Path, is_dir: bool) -> None
```

Set the input from a tree selection and move focus there.

<a id="wizard_ui_bridge._path._PathPick._confirm"></a>

#### \_confirm

```python
def _confirm(value: str) -> None
```

Consume the confirmed path text; overridden by the host.

<a id="wizard_ui_bridge._path._PickerScreen"></a>

## \_PickerScreen Objects

```python
class _PickerScreen(_PathPick, ModalScreen[Optional[str]])
```

Modal directory picker that fills a form path field.

It shows a directory tree and an editable path input, like the
standalone path question. Selecting in the tree fills the input;
Submit or Return returns the text to the form, while Cancel or
Escape returns nothing so the field keeps its current value.

<a id="wizard_ui_bridge._path._PickerScreen.__init__"></a>

#### \_\_init\_\_

```python
def __init__(options: PathAskOptions, value: str) -> None
```

Store the path kind and the tree root and initial input.

<a id="wizard_ui_bridge._path._PickerScreen.compose"></a>

#### compose

```python
def compose() -> ComposeResult
```

Lay out the tree, the path input and the buttons.

<a id="wizard_ui_bridge._path._PickerScreen._submit_clicked"></a>

#### \_submit\_clicked

```python
@on(Button.Pressed, '#submit')
def _submit_clicked(_event: Button.Pressed) -> None
```

Submit the picked path when the submit button is pressed.

<a id="wizard_ui_bridge._path._PickerScreen._cancel_clicked"></a>

#### \_cancel\_clicked

```python
@on(Button.Pressed, '#cancel')
def _cancel_clicked(_event: Button.Pressed) -> None
```

Close without changing the field when cancel is pressed.

<a id="wizard_ui_bridge._path._PickerScreen.action_cancel"></a>

#### action\_cancel

```python
def action_cancel() -> None
```

Close the picker without returning a path.

<a id="wizard_ui_bridge._path._PickerScreen._confirm"></a>

#### \_confirm

```python
def _confirm(value: str) -> None
```

Return the confirmed path text to the form.

<a id="wizard_ui_bridge._ask_cell"></a>

# wizard\_ui\_bridge.\_ask\_cell

Ask one form field or matrix cell with the typed ask methods.

The base WizardUiBridge.ask_form() and ask_matrix_form() both ask one
question at a time. Every Ask*Field derives from its Ask*Cell, so a
single function asks either, given the question to show, through the
public typed ask methods of the bridge, which a derived bridge may
override. The help text of the cell is passed as help_text, so a console
user can ask to see it.

<a id="wizard_ui_bridge._ask_cell.ask_cell_value"></a>

#### ask\_cell\_value

```python
def ask_cell_value(bridge: 'WizardUiBridge', question: str,
                   cell: AskCell) -> Optional[PrefillValueType]
```

Ask the value of an input cell or form field and return it.

The value has the answer type of the cell (see PrefillValueType), or
is None for an empty nullable answer. A label cell has no value and
must not be passed.

<a id="wizard_ui_bridge._ask_cell._ask_typed_value"></a>

#### \_ask\_typed\_value

```python
def _ask_typed_value(bridge: 'WizardUiBridge', question: str,
                     cell: AskCell) -> Optional[PrefillValueType]
```

Ask a float, date, time, date-time or duration through ask_text.

The shared re-ask loop parses the entered text, checks the inclusive
bounds and shows the format hint until the value is accepted.

<a id="wizard_ui_bridge._ask_cell._ask_basic_value"></a>

#### \_ask\_basic\_value

```python
def _ask_basic_value(bridge: 'WizardUiBridge', question: str,
                     cell: AskCell) -> Optional[PrefillValueType]
```

Ask one of the original cell kinds with its typed ask method.

<a id="wizard_ui_bridge._ask_cell._ask_choice_value"></a>

#### \_ask\_choice\_value

```python
def _ask_choice_value(bridge: 'WizardUiBridge', question: str,
                      cell: AskChoiceCell) -> Optional[str]
```

Ask a choice, passing nullable only when it is set.

A bridge whose ask_choice() predates the nullable parameter still
asks a non-nullable choice this way.

<a id="wizard_ui_bridge.form_defs"></a>

# wizard\_ui\_bridge.form\_defs

Definitions of types for wizard UI bridge forms.

Wizard UI bridge forms are used when a number of questions should preferably
be asked on a single form (in a GUI, textual or curses implementation).
For a good user experience the user should see all questions at the same time,
and the user should be able to fill in the answers in any order, and change
them before submitting the form.

In a GUI, curses or textual implementation, the form is typically displayed
in a single window, in something like a grid layout, with 2 columns and
2 - 10 rows. The left column contains the questions, and the right column
contains the input fields. Above the grid there is typically a longer question
or instruction, that explains to the user what the form is about. Below the
grid there are typically buttons for submitting the form, canceling the form,
and possibly for going back to a previous form step in a multi-step wizard.

A variant is the matrix form, described in module matrix_cell_defs. Each
Ask*Field of a form derives from the corresponding Ask*Cell of a matrix
form, adding the short question, and each Answer*Field derives from the
corresponding Answer*Cell.

This file defines the data types used to describe the questions and answers of
a form, and the validation callback function that is used to validate the
answers of a partly filled form.

<a id="wizard_ui_bridge.form_defs.value_out_of_range"></a>

#### value\_out\_of\_range

Kept for compatibility, see matrix_cell_defs.value_out_of_range.

<a id="wizard_ui_bridge.form_defs.AskFieldCommon"></a>

## AskFieldCommon Objects

```python
@dataclass
class AskFieldCommon()
```

Common attributes of a field in a form.

Each concrete field is one of the Ask*Field subclasses, so its Python
type already tells the bridge which kind of input to show. There is no
separate kind attribute to keep in sync.

Each Ask*Field derives from its Ask*Cell first and from this class
last, so the constructor arguments start with short_question and
help_text. help_text is declared both here and in AskCellCommon, so
a field type derived only from this class still has it.

Every field also has the keyword-only width hint of AskCellCommon,
for instance AskTextField('Name?', None, width=20).

**Attributes**:

- `short_question` - A short question to be displayed to the user.
  In a GUI implementation this is typically displayed
  as a label in a left column next to the input field.
- `help_text` - Optional help text to be displayed to the user. Could be
  used as tooltip text in a GUI implementation, or as a
  popup message in response to a help button click
  or similar user action.

<a id="wizard_ui_bridge.form_defs.AskTextField"></a>

## AskTextField Objects

```python
@dataclass
class AskTextField(AskTextCell, AskFieldCommon)
```

A text field in a form, see AskFieldCommon and AskTextCell.

<a id="wizard_ui_bridge.form_defs.AskIntField"></a>

## AskIntField Objects

```python
@dataclass
class AskIntField(AskIntCell, AskFieldCommon)
```

An integer field in a form, see AskFieldCommon and AskIntCell.

<a id="wizard_ui_bridge.form_defs.AskPathField"></a>

## AskPathField Objects

```python
@dataclass
class AskPathField(AskPathCell, AskFieldCommon)
```

A path field in a form, see AskFieldCommon and AskPathCell.

<a id="wizard_ui_bridge.form_defs.AskYesNoField"></a>

## AskYesNoField Objects

```python
@dataclass
class AskYesNoField(AskYesNoCell, AskFieldCommon)
```

A yes/no field in a form, see AskFieldCommon and AskYesNoCell.

<a id="wizard_ui_bridge.form_defs.AskChoiceField"></a>

## AskChoiceField Objects

```python
@dataclass
class AskChoiceField(AskChoiceCell, AskFieldCommon)
```

A choice field in a form, see AskFieldCommon and AskChoiceCell.

<a id="wizard_ui_bridge.form_defs.AskMultiChoiceField"></a>

## AskMultiChoiceField Objects

```python
@dataclass
class AskMultiChoiceField(AskMultiChoiceCell, AskFieldCommon)
```

A multi-choice field in a form.

See AskFieldCommon and AskMultiChoiceCell for the attributes.

<a id="wizard_ui_bridge.form_defs.AskFloatField"></a>

## AskFloatField Objects

```python
@dataclass
class AskFloatField(AskFloatCell, AskFieldCommon)
```

A float field in a form, see AskFieldCommon and AskFloatCell.

<a id="wizard_ui_bridge.form_defs.AskDateField"></a>

## AskDateField Objects

```python
@dataclass
class AskDateField(AskDateCell, AskFieldCommon)
```

A date field in a form, see AskFieldCommon and AskDateCell.

<a id="wizard_ui_bridge.form_defs.AskTimeField"></a>

## AskTimeField Objects

```python
@dataclass
class AskTimeField(AskTimeCell, AskFieldCommon)
```

A time field in a form, see AskFieldCommon and AskTimeCell.

<a id="wizard_ui_bridge.form_defs.AskDateTimeField"></a>

## AskDateTimeField Objects

```python
@dataclass
class AskDateTimeField(AskDateTimeCell, AskFieldCommon)
```

A date-time field in a form.

See AskFieldCommon and AskDateTimeCell for the attributes.

<a id="wizard_ui_bridge.form_defs.AskDurationField"></a>

## AskDurationField Objects

```python
@dataclass
class AskDurationField(AskDurationCell, AskFieldCommon)
```

A duration field in a form, see AskFieldCommon and AskDurationCell.

<a id="wizard_ui_bridge.form_defs.ALL_ASK_FIELD_TYPES"></a>

#### ALL\_ASK\_FIELD\_TYPES

Every concrete AskField class, in the order of the AskField union.

A bridge that shows all field types checks membership against this tuple
in supports_form_field(), so a field type added later is reported as
unsupported until this tuple and the bridge are extended together.

<a id="wizard_ui_bridge.form_defs.AnswerTextField"></a>

## AnswerTextField Objects

```python
@dataclass
class AnswerTextField(AnswerTextCell)
```

An answer to a text field in a form.

**Attributes**:

- `asking` - How the question was asked, including the question text, help
  text, and other attributes of the question.

<a id="wizard_ui_bridge.form_defs.AnswerIntField"></a>

## AnswerIntField Objects

```python
@dataclass
class AnswerIntField(AnswerIntCell)
```

An answer to an integer field in a form.

**Attributes**:

- `asking` - How the question was asked, including the question text, help
  text, and other attributes of the question.

<a id="wizard_ui_bridge.form_defs.AnswerPathField"></a>

## AnswerPathField Objects

```python
@dataclass
class AnswerPathField(AnswerPathCell)
```

An answer to a path field in a form.

**Attributes**:

- `asking` - How the question was asked, including the question text, help
  text, and other attributes of the question.

<a id="wizard_ui_bridge.form_defs.AnswerYesNoField"></a>

## AnswerYesNoField Objects

```python
@dataclass
class AnswerYesNoField(AnswerYesNoCell)
```

An answer to a yes/no field in a form.

**Attributes**:

- `asking` - How the question was asked, including the question text, help
  text, and other attributes of the question.

<a id="wizard_ui_bridge.form_defs.AnswerChoiceField"></a>

## AnswerChoiceField Objects

```python
@dataclass
class AnswerChoiceField(AnswerChoiceCell)
```

An answer to a choice field in a form.

**Attributes**:

- `asking` - How the question was asked, including the question text, help
  text, and other attributes of the question.

<a id="wizard_ui_bridge.form_defs.AnswerMultiChoiceField"></a>

## AnswerMultiChoiceField Objects

```python
@dataclass
class AnswerMultiChoiceField(AnswerMultiChoiceCell)
```

An answer to a multi-choice field in a form.

**Attributes**:

- `asking` - How the question was asked, including the question text, help
  text, and other attributes of the question.

<a id="wizard_ui_bridge.form_defs.AnswerFloatField"></a>

## AnswerFloatField Objects

```python
@dataclass
class AnswerFloatField(AnswerFloatCell)
```

An answer to a float field in a form.

**Attributes**:

- `asking` - How the question was asked, including the question text, help
  text, and other attributes of the question.

<a id="wizard_ui_bridge.form_defs.AnswerDateField"></a>

## AnswerDateField Objects

```python
@dataclass
class AnswerDateField(AnswerDateCell)
```

An answer to a date field in a form.

**Attributes**:

- `asking` - How the question was asked, including the question text, help
  text, and other attributes of the question.

<a id="wizard_ui_bridge.form_defs.AnswerTimeField"></a>

## AnswerTimeField Objects

```python
@dataclass
class AnswerTimeField(AnswerTimeCell)
```

An answer to a time field in a form.

**Attributes**:

- `asking` - How the question was asked, including the question text, help
  text, and other attributes of the question.

<a id="wizard_ui_bridge.form_defs.AnswerDateTimeField"></a>

## AnswerDateTimeField Objects

```python
@dataclass
class AnswerDateTimeField(AnswerDateTimeCell)
```

An answer to a date-time field in a form.

**Attributes**:

- `asking` - How the question was asked, including the question text, help
  text, and other attributes of the question.

<a id="wizard_ui_bridge.form_defs.AnswerDurationField"></a>

## AnswerDurationField Objects

```python
@dataclass
class AnswerDurationField(AnswerDurationCell)
```

An answer to a duration field in a form.

**Attributes**:

- `asking` - How the question was asked, including the question text, help
  text, and other attributes of the question.

<a id="wizard_ui_bridge.form_defs.PartFormValidationResult"></a>

## PartFormValidationResult Objects

```python
class PartFormValidationResult(NamedTuple)
```

Result of validating a partly filled form.

**Attributes**:

- `is_valid` - True when the form is valid, False when it is not valid.
- `message` - A message to be displayed to the user, explaining why the
  form is not valid. Empty string when the form is valid.
- `disable_row_idxs` - A tuple of row indexes that should be disabled in the
  form, because what has been filled in so far makes
  these rows irrelevant. For example if output format
  is set to some binary format, then the row(s) that
  ask for character encoding can be disabled, because
  they are irrelevant for the chosen output format.
  Actually disabling these rows is not strictly
  necessary, but it is a good user experience to do so.
- `prefill_values` - Values the validator asks the bridge to place into
  other rows' inputs, as a tuple of (row_index, value)
  pairs. Each value must match the answer type of the
  field in that row. A bridge applies each request
  during live editing as if the user had typed the
  value; setting a value equal to the one already there
  is a no-op, so a validator that emits a stable value
  does not loop. The validator owns idempotency: it
  should emit a prefill only when it means to fill or
  overwrite the target. A prefill aimed at the row that
  just changed is ignored, so writing back never fights
  the user's current edit. A prefill aimed at a disabled
  row is still applied, so the value shows in the greyed
  row and takes effect if the row is later enabled. A
  row index outside the form, or a value whose type does
  not match the field, raises an exception, since both
  are validator bugs. A choice or multi-choice value not
  among the field's choices, and any prefill of a
  sensitive field, are ignored. prefill_values is a
  live-editing convenience only and is ignored when the
  form is submitted, so an application must still apply
  the same default on submit.

<a id="wizard_ui_bridge.console"></a>

# wizard\_ui\_bridge.console

Console text user interface bridge for a wizard.

This module provides the concrete console bridge used when the wizard
talks to a user through plain text streams. It recognises reserved
navigation tokens so a console user can step back, cancel the current
level or abandon the whole wizard, and the help token ':?', which shows
the help text of the question and then asks the same question again.

<a id="wizard_ui_bridge.console.WizardUiBridgeConsole"></a>

## WizardUiBridgeConsole Objects

```python
class WizardUiBridgeConsole(WizardUiBridge)
```

Bridge between the wizard and the console text user interface.

<a id="wizard_ui_bridge.console.WizardUiBridgeConsole.__init__"></a>

#### \_\_init\_\_

```python
def __init__(stdout_file: TextIO, stdin_file: TextIO,
             stderr_file: TextIO) -> None
```

Initialize the bridge.

**Arguments**:

- `stdout_file` - Stream to print messages to.
- `stdin_file` - Stream to read user answers from.
- `stderr_file` - Stream to print errors to.

<a id="wizard_ui_bridge.console.WizardUiBridgeConsole.ask_text"></a>

#### ask\_text

```python
def ask_text(question: str,
             re_ask_reason: Optional[str] = None,
             nullable: bool = False,
             *,
             default: Optional[str] = None,
             sensitive: bool = False,
             help_text: Optional[str] = None) -> Optional[str]
```

Ask for free text on the console; see WizardUiBridge.ask_text.

<a id="wizard_ui_bridge.console.WizardUiBridgeConsole.supports_form_field"></a>

#### supports\_form\_field

```python
def supports_form_field(field: AskField) -> bool
```

Show every form field type; see WizardUiBridge.

The inherited base ask_form() asks each field with the typed ask
methods, so the console form handles the typed float, date, time,
date-time and duration fields as well as the original kinds, and
a nullable choice field through ask_choice(nullable=True).

<a id="wizard_ui_bridge.console.WizardUiBridgeConsole.ask_yes_no"></a>

#### ask\_yes\_no

```python
def ask_yes_no(question: str,
               default: bool,
               re_ask_reason: Optional[str] = None,
               *,
               help_text: Optional[str] = None) -> bool
```

Ask a yes/no question on the console; see ask_yes_no.

<a id="wizard_ui_bridge.console.WizardUiBridgeConsole.ask_table"></a>

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

Ask the user to fill a table on the console; see ask_table.

With both min_rows and max_rows given the table has a variable
number of rows, edited through a row-menu interface. Otherwise the
fixed rows in cells are filled one editable cell at a time.

<a id="wizard_ui_bridge.console.WizardUiBridgeConsole._ask_raw"></a>

#### \_ask\_raw

```python
def _ask_raw(question: str,
             re_ask_reason: Optional[str] = None,
             choices: Optional[Sequence[str]] = None,
             *,
             help_text: Optional[str] = None) -> str | int
```

Ask one question and read a navigation-checked raw answer.

Returns the entered text, or a 0-based index into choices when
choices are offered, which is the raw-answer shape the table
helpers expect (see arg_types.AskReader).

<a id="wizard_ui_bridge.console.WizardUiBridgeConsole.ask_choice"></a>

#### ask\_choice

```python
def ask_choice(question: str,
               *,
               choices: Sequence[str],
               default: Optional[str] = None,
               re_ask_reason: Optional[str] = None,
               nullable: bool = False,
               help_text: Optional[str] = None) -> Optional[str]
```

Ask one choice on the console; see WizardUiBridge.ask_choice.

A nullable choice adds the menu line '0: (none)'. Answering 0, or
giving an empty answer, then selects no choice.

<a id="wizard_ui_bridge.console.WizardUiBridgeConsole.ask_multi"></a>

#### ask\_multi

```python
def ask_multi(question: str,
              *,
              choices: Sequence[str],
              default: Optional[Sequence[str]] = None,
              min_select: int = 0,
              max_select: Optional[int] = None,
              re_ask_reason: Optional[str] = None,
              help_text: Optional[str] = None) -> list[str]
```

Ask several choices on the console; see WizardUiBridge.ask_multi.

<a id="wizard_ui_bridge.console.WizardUiBridgeConsole._prompt"></a>

#### \_prompt

```python
def _prompt(question: str,
            re_ask_reason: Optional[str],
            lines: Sequence[str],
            help_text: Optional[str],
            *,
            sensitive: bool = False) -> str
```

Ask one question until the answer is not a request for help.

The help token shows the help text, or a note that there is none,
and asks the same question again, with the same re-ask reason. A
navigation token raises its navigation request.

<a id="wizard_ui_bridge.console.WizardUiBridgeConsole._emit_question"></a>

#### \_emit\_question

```python
def _emit_question(question: str, re_ask_reason: Optional[str],
                   lines: Sequence[str]) -> None
```

Print one question, any re-ask reason, choices and the prompt.

<a id="wizard_ui_bridge.console.WizardUiBridgeConsole._read_answer"></a>

#### \_read\_answer

```python
def _read_answer(question: str) -> str
```

Read one navigation-checked answer line from the input stream.

<a id="wizard_ui_bridge.console.WizardUiBridgeConsole._read_sensitive"></a>

#### \_read\_sensitive

```python
def _read_sensitive(question: str) -> str
```

Read sensitive text, avoiding echo on a real terminal.

<a id="wizard_ui_bridge.console.WizardUiBridgeConsole.error_file"></a>

#### error\_file

```python
def error_file() -> TextIO
```

Return the stream used for validation diagnostics.

<a id="wizard_ui_bridge.console.WizardUiBridgeConsole.show"></a>

#### show

```python
def show(message: str) -> None
```

Show a message to the user.

This method prints the message to the console.

**Arguments**:

- `message` - The message to show the user.

<a id="wizard_ui_bridge.console._raise_for_navigation"></a>

#### \_raise\_for\_navigation

```python
def _raise_for_navigation(text: str) -> None
```

Raise a navigation request when text is a reserved token.

<a id="wizard_ui_bridge.console._to_index"></a>

#### \_to\_index

```python
def _to_index(text: str) -> str | int
```

Map a numeric menu answer to a 0-based index, else keep the text.

<a id="wizard_ui_bridge.console._single_index"></a>

#### \_single\_index

```python
def _single_index(text: str, nullable: bool) -> str | int
```

Map a single-choice answer, reading 0 as no choice when nullable.

<a id="wizard_ui_bridge.console._menu_lines"></a>

#### \_menu\_lines

```python
def _menu_lines(choices: Optional[Sequence[str]],
                marked: Optional[Sequence[str]] = None) -> list[str]
```

Return the numbered menu lines, marking any choice in marked.

<a id="wizard_ui_bridge.console._multi_question"></a>

#### \_multi\_question

```python
def _multi_question(question: str) -> str
```

Return the multi-choice question with an entry hint appended.

<a id="wizard_ui_bridge.matrix_helpers"></a>

# wizard\_ui\_bridge.matrix\_helpers

Helpers shared by the bridges that show a matrix form question.

A bridge builds the cells of a matrix form from the MatrixCellSpec of the
request with cell_at(), applies the prefills of a partial validator with
valid_cell_prefills(), and names a cell in its own message with
message_name(), which uses the CellNamer of the request and falls back
to cell_name(). A bridge asking one cell at a time names it with
row_name() and column_name(). The cells of the current shape are given
to all but cell_at() as a grid of AskCells, one sequence per row.

<a id="wizard_ui_bridge.matrix_helpers.cell_at"></a>

#### cell\_at

```python
def cell_at(spec: MatrixCellSpec, position: CellPosition) -> AskCell
```

Return the AskCell the specification gives for a position.

A generator is called with the position. A 2D sequence gives the
cell at the position, repeating its last row below the sequence and
the last cell of a row to the right of that row, as described for
MatrixCellSpec.

**Raises**:

- `ValueError` - The sequence, or the row used, has no cells.
- `TypeError` - The specification gave no AskCell for the position.

<a id="wizard_ui_bridge.matrix_helpers._listed_cell"></a>

#### \_listed\_cell

```python
def _listed_cell(cells: Sequence[Sequence[AskCell]],
                 position: CellPosition) -> AskCell
```

Return the cell of a 2D sequence, repeating the last row or cell.

<a id="wizard_ui_bridge.matrix_helpers.valid_cell_prefills"></a>

#### valid\_cell\_prefills

```python
def valid_cell_prefills(
    cells: Sequence[Sequence[AskCell]], changed: Optional[CellPosition],
    prefill_values: PrefillCellValues
) -> Iterator[tuple[CellPosition, PrefillValueType]]
```

Yield the prefill requests a bridge should apply, validated.

cells is the grid of the current shape and changed the cell that
just changed, or None after a shape change. Each yielded (position,
value) pair is ready to place into the input of that cell. The rules
are those of PartMatrixValidationRes.prefill_values: a prefill aimed
at the changed cell is skipped; a position outside the matrix raises
IndexError, and a label cell or a value of the wrong type raises
TypeError; a choice value not among the cell's choices and any
prefill of a sensitive cell are dropped.

<a id="wizard_ui_bridge.matrix_helpers._input_cell"></a>

#### \_input\_cell

```python
def _input_cell(cells: Sequence[Sequence[AskCell]],
                position: CellPosition) -> AskCell
```

Return the input cell a prefill is aimed at, raising for a bug.

<a id="wizard_ui_bridge.matrix_helpers._where"></a>

#### \_where

```python
def _where(position: CellPosition) -> str
```

Return a 0-based position as text for an exception message.

<a id="wizard_ui_bridge.matrix_helpers.row_label"></a>

#### row\_label

```python
def row_label(cells: Sequence[Sequence[AskCell]],
              position: CellPosition) -> Optional[str]
```

Return the nearest label text to the left of a cell, or None.

Labels whose text is blank, such as an empty corner, are skipped.

<a id="wizard_ui_bridge.matrix_helpers.column_label"></a>

#### column\_label

```python
def column_label(cells: Sequence[Sequence[AskCell]],
                 position: CellPosition) -> Optional[str]
```

Return the nearest label text above a cell, or None.

Labels whose text is blank, such as an empty corner, are skipped.

<a id="wizard_ui_bridge.matrix_helpers._nearest_label"></a>

#### \_nearest\_label

```python
def _nearest_label(cells: Iterable[AskCell]) -> Optional[str]
```

Return the text of the first label with non-blank text, or None.

<a id="wizard_ui_bridge.matrix_helpers.cell_name"></a>

#### cell\_name

```python
def cell_name(cells: Sequence[Sequence[AskCell]],
              position: CellPosition) -> str
```

Return a name of a cell for a message shown to the user.

The name is the row label and the column label of the cell joined
with ' / ', such as 'Bob / Tue'. Where a label is missing, the 1-based
row or column number takes its place, such as 'Row 2 / Start date'.

<a id="wizard_ui_bridge.matrix_helpers.row_name"></a>

#### row\_name

```python
def row_name(cells: Sequence[Sequence[AskCell]],
             position: CellPosition) -> str
```

Return the row label of a cell, or its 1-based row as 'Row 2'.

<a id="wizard_ui_bridge.matrix_helpers.column_name"></a>

#### column\_name

```python
def column_name(cells: Sequence[Sequence[AskCell]],
                position: CellPosition) -> str
```

Return the column label of a cell, or 'Column 3' when it has none.

<a id="wizard_ui_bridge.matrix_helpers.message_name"></a>

#### message\_name

```python
def message_name(namer: Optional[CellNamer], answers: AnswerCells,
                 cells: Sequence[Sequence[AskCell]],
                 position: CellPosition) -> str
```

Return the name of a cell for a message the bridge writes itself.

The CellNamer of the request names the cell when it is given and
returns a non-empty name; otherwise cell_name() does.

<a id="wizard_ui_bridge._help"></a>

# wizard\_ui\_bridge.\_help

Pass a help text only to the ask methods and readers that accept it.

The typed ask methods, ask_table() and the AskReader of the table helpers
gained a keyword-only help_text parameter after bridges outside this
package were written. The code of this package calls them through
help_kwargs(), which leaves the help text out, with a DeprecationWarning,
for a method or reader that does not accept it yet, so an older bridge
keeps working until it is updated.

<a id="wizard_ui_bridge._help.HelpKwargs"></a>

## HelpKwargs Objects

```python
class HelpKwargs(TypedDict)
```

The keyword arguments that carry a help text to an ask method.

<a id="wizard_ui_bridge._help.help_kwargs"></a>

#### help\_kwargs

```python
def help_kwargs(method: Callable[..., object],
                help_text: Optional[str]) -> HelpKwargs
```

Return help_text as keyword arguments for method, if it takes them.

A method that takes neither a help_text parameter nor **kwargs gets
no keyword arguments, and a DeprecationWarning names the method.

<a id="wizard_ui_bridge._help._accepts_help"></a>

#### \_accepts\_help

```python
def _accepts_help(method: Callable[..., object]) -> bool
```

Return whether method takes help_text, by name or as **kwargs.

<a id="wizard_ui_bridge.matrix_cell_defs"></a>

# wizard\_ui\_bridge.matrix\_cell\_defs

Definitions of cell types for wizard UI bridge matrix forms.

A matrix form asks a single context setting question on the top of the
screen, followed by a matrix of cells. Each cell typically represents a
single input field for a validated input. However, a cell may also be a
label that is only text displayed with no input. Typically the label cells
are used to name the rows and columns of the matrix, but they are not
limited to the edges; they can appear anywhere in the grid to provide
context or labels for the input cells. The matrix form also has a
feed-back area, typically below the grid, where validation messages or
other contextual information can be displayed to the user.

One example of a matrix form is a list of contractors, one contractor
per row in the matrix, with a column containing the name,
another column the start date as date picker, yet another column the
end date as date picker, the last column the file name of the contract
as file picker.

An Ask*Cell is like the corresponding Ask*Field of a form, except that
no question is asked per cell. Each Ask*Field derives from its Ask*Cell,
so code written for a cell also handles the corresponding form field.
Likewise each Answer*Field derives from its Answer*Cell.

The request, dimensions and validator of a matrix form are defined in
module matrix_defs.

<a id="wizard_ui_bridge.matrix_cell_defs._OrderedValue"></a>

## \_OrderedValue Objects

```python
class _OrderedValue(Protocol)
```

A value comparable to values of its own type with < and >.

Int, float, date, time, datetime and timedelta all satisfy this, so a
single helper can range-check every ordered cell. The other operand
is Any because each concrete type only compares with itself, which is
exactly how the standard library types are annotated.

<a id="wizard_ui_bridge.matrix_cell_defs._OrderedValue.__lt__"></a>

#### \_\_lt\_\_

```python
def __lt__(other: Any) -> bool
```

Return whether this value sorts before other.

<a id="wizard_ui_bridge.matrix_cell_defs._OrderedValue.__gt__"></a>

#### \_\_gt\_\_

```python
def __gt__(other: Any) -> bool
```

Return whether this value sorts after other.

<a id="wizard_ui_bridge.matrix_cell_defs.value_out_of_range"></a>

#### value\_out\_of\_range

```python
def value_out_of_range(value: _OrderedT, minimum: Optional[_OrderedT],
                       maximum: Optional[_OrderedT]) -> bool
```

Return whether value lies outside the inclusive bounds.

<a id="wizard_ui_bridge.matrix_cell_defs.check_bounds"></a>

#### check\_bounds

```python
def check_bounds(minimum: Optional[_OrderedValue],
                 maximum: Optional[_OrderedValue],
                 default: Optional[_OrderedValue]) -> None
```

Raise ValueError when ordered bounds or the default disagree.

<a id="wizard_ui_bridge.matrix_cell_defs.AskCellCommon"></a>

## AskCellCommon Objects

```python
@dataclass
class AskCellCommon()
```

Common attributes of a cell in a matrix form.

Each concrete cell is one of the Ask*Cell subclasses, so its Python
type already tells the bridge which kind of input to show.

**Attributes**:

- `help_text` - Optional help text to be displayed to the user. Could be
  used as tooltip text in a GUI implementation, or as a
  popup message in response to a help button click
  or similar user action.
- `width` - Optional hint for the width of the cell's input, in
  characters, or None to let the bridge choose. It is only a
  hint, and the shown width is approximate, depending on the
  fonts and widgets of the UI; a UI may also ignore it, as a
  console does. It sizes the text part of an input, not a
  button beside it such as Browse or Pick, and the list of a
  multi-choice cell. On a label cell it is the width at which
  the text wraps. A yes/no check box has no text part, so it
  ignores the hint. It is keyword-only, and must be at least
  1, or ValueError is raised.

<a id="wizard_ui_bridge.matrix_cell_defs.AskCellCommon.__post_init__"></a>

#### \_\_post\_init\_\_

```python
def __post_init__() -> None
```

Check that a width hint is at least one character.

<a id="wizard_ui_bridge.matrix_cell_defs.AskLabelCell"></a>

## AskLabelCell Objects

```python
@dataclass
class AskLabelCell(AskCellCommon)
```

A label cell in a matrix form, only text with no input.

A label cell typically names a row or a column of the matrix, but it
can be placed anywhere in the grid. It gives no answer, so its
position in the answers of a matrix form holds None.

Help text is seldom needed on a label, so unlike the input cells a
label cell defaults help_text to None. It is keyword-only, so the
text comes first: AskLabelCell('Name') or
AskLabelCell('Name', help_text='...').

**Attributes**:

- `text` - The text displayed in the cell.
- `help_text` - Optional help text, as for any cell; None by default.
- `bold` - A hint to show the text in bold, for instance to make a
  header stand out. A UI that cannot show bold text ignores
  it, so the look is not guaranteed. Keyword-only.
- `italic` - A hint to show the text in italics, ignored like bold by
  a UI that cannot show it. Keyword-only.

<a id="wizard_ui_bridge.matrix_cell_defs.AskTextCell"></a>

## AskTextCell Objects

```python
@dataclass
class AskTextCell(AskCellCommon)
```

A text cell in a matrix form.

**Attributes**:

- `nullable` - When True an empty answer is reported as None. When
  False an empty answer with no default is the empty
  string. Not allowed together with a default, which
  raises ValueError.
- `default` - The value returned when user fills in nothing, or None for
  no default. In a GUI implementation this is typically shown
  as the starting value in the input field, and the user can
  change it.
- `sensitive` - True when the bridge must avoid echoing the entered text,
  such as for passwords. A default is not allowed for a
  sensitive question.

<a id="wizard_ui_bridge.matrix_cell_defs.AskTextCell.__post_init__"></a>

#### \_\_post\_init\_\_

```python
def __post_init__() -> None
```

Check that the text cell arguments are valid.

<a id="wizard_ui_bridge.matrix_cell_defs.AskRangeCell"></a>

## AskRangeCell Objects

```python
@dataclass
class AskRangeCell(AskCellCommon, Generic[_OrderedT])
```

A cell in a matrix form for an ordered value with optional bounds.

This is the common base of the integer, float, date, time, date-time
and duration cells, so a bridge can handle their shared attributes
once.

**Attributes**:

- `nullable` - When True an empty answer is reported as None. When
  False an empty answer with no default will be re-asked
  until the user fills in a valid value. Not allowed
  together with a default, which raises ValueError.
- `default` - The value returned when user fills in nothing, or None for
  no default. In a GUI implementation this is typically shown
  as the starting value in the input field, and the user can
  change it.
- `min_value` - The minimum allowed value, or None for no minimum.
  The min value is inclusive.
- `max_value` - The maximum allowed value, or None for no maximum.
  The max value is inclusive.

<a id="wizard_ui_bridge.matrix_cell_defs.AskRangeCell.__post_init__"></a>

#### \_\_post\_init\_\_

```python
def __post_init__() -> None
```

Check that the bounds, the default and nullable agree.

<a id="wizard_ui_bridge.matrix_cell_defs.AskIntCell"></a>

## AskIntCell Objects

```python
@dataclass
class AskIntCell(AskRangeCell[int])
```

An integer cell in a matrix form.

<a id="wizard_ui_bridge.matrix_cell_defs.AskPathCell"></a>

## AskPathCell Objects

```python
@dataclass
class AskPathCell(AskCellCommon)
```

A path cell in a matrix form.

In a GUI implementation this is typically displayed as a text input field
with a button next to it that opens a file/directory chooser dialog.

**Attributes**:

- `path_options` - Options for how the path question is asked, including
  whether the path must exist, whether it must be a file
  or a directory.

<a id="wizard_ui_bridge.matrix_cell_defs.AskYesNoCell"></a>

## AskYesNoCell Objects

```python
@dataclass
class AskYesNoCell(AskCellCommon)
```

A yes/no cell in a matrix form.

In a GUI implementation this is typically displayed as a checkbox or a
toggle button.

**Attributes**:

- `default` - The boolean value used when the user makes no explicit
  choice. In a GUI implementation this is typically shown as
  the starting value in the checkbox or toggle, and the user
  can change it.

<a id="wizard_ui_bridge.matrix_cell_defs.AskChoiceCell"></a>

## AskChoiceCell Objects

```python
@dataclass
class AskChoiceCell(AskCellCommon)
```

A choice cell in a matrix form.

In a GUI implementation this is typically displayed as a dropdown list
or a set of radio buttons.

**Attributes**:

- `choices` - The allowed choices for the answer.
- `default` - The value returned when user fills in nothing, or None for
  no default. In a GUI implementation this is typically shown
  as the starting value in the input field, and the user can
  change it. It must be one of choices, or ValueError is
  raised.
- `nullable` - When True the user may leave the choice empty, which is
  reported as None. When False an empty choice with no
  default is not a valid final answer. Not allowed
  together with a default, which raises ValueError.

<a id="wizard_ui_bridge.matrix_cell_defs.AskChoiceCell.__post_init__"></a>

#### \_\_post\_init\_\_

```python
def __post_init__() -> None
```

Check that a default is a choice and not combined with nullable.

<a id="wizard_ui_bridge.matrix_cell_defs.AskMultiChoiceCell"></a>

## AskMultiChoiceCell Objects

```python
@dataclass
class AskMultiChoiceCell(AskCellCommon)
```

A multi-choice cell in a matrix form.

In a GUI implementation this is typically displayed as a list of checkboxes
or a list of items with multiple selection enabled.

**Attributes**:

- `choices` - The allowed choices for the answer.
- `default` - The values returned when user fills in nothing, or None for
  no default. In a GUI implementation this is typically shown
  as the starting value in the input field, and the user can
  change it. It must name distinct choices, at most
  max_select of them, but may name fewer than min_select.
- `min_select` - The minimum number of choices that must be selected.
- `max_select` - The maximum number of choices that can be selected,
  or None for no maximum. The bounds must satisfy
  0 <= min_select <= max_select <= len(choices).
  
  A default or bounds breaking these rules raise ValueError.

<a id="wizard_ui_bridge.matrix_cell_defs.AskMultiChoiceCell.__post_init__"></a>

#### \_\_post\_init\_\_

```python
def __post_init__() -> None
```

Check that the bounds and the default fit the choices.

<a id="wizard_ui_bridge.matrix_cell_defs.AskFloatCell"></a>

## AskFloatCell Objects

```python
@dataclass
class AskFloatCell(AskRangeCell[float])
```

A float cell in a matrix form.

<a id="wizard_ui_bridge.matrix_cell_defs.AskDateCell"></a>

## AskDateCell Objects

```python
@dataclass
class AskDateCell(AskRangeCell[date])
```

A date cell in a matrix form.

In a GUI implementation this is typically displayed as a text input field
with a button next to it that opens a date chooser dialog.

<a id="wizard_ui_bridge.matrix_cell_defs.AskTimeCell"></a>

## AskTimeCell Objects

```python
@dataclass
class AskTimeCell(AskRangeCell[time])
```

A time cell in a matrix form.

<a id="wizard_ui_bridge.matrix_cell_defs.AskDateTimeCell"></a>

## AskDateTimeCell Objects

```python
@dataclass
class AskDateTimeCell(AskRangeCell[datetime])
```

A date-time cell in a matrix form.

In a GUI implementation this is typically displayed as a text input field
with a button next to it that opens a date-time chooser dialog for the
date part.

<a id="wizard_ui_bridge.matrix_cell_defs.AskDurationCell"></a>

## AskDurationCell Objects

```python
@dataclass
class AskDurationCell(AskRangeCell[timedelta])
```

A duration cell in a matrix form.

<a id="wizard_ui_bridge.matrix_cell_defs.ALL_ASK_CELL_TYPES"></a>

#### ALL\_ASK\_CELL\_TYPES

Every concrete AskCell class, in the order of the AskCell union.

A bridge that shows all cell types checks membership against this tuple,
so a cell type added later is reported as unsupported until this tuple
and the bridge are extended together. Since every Ask*Field derives from
its Ask*Cell, an isinstance check against this tuple also accepts fields.

<a id="wizard_ui_bridge.matrix_cell_defs.AnswerTextCell"></a>

## AnswerTextCell Objects

```python
@dataclass
class AnswerTextCell()
```

An answer to a text cell in a matrix form.

**Attributes**:

- `asking` - How the cell was asked, including the help text and other
  attributes of the cell.
- `value` - The value of the answer, or None when the user did not fill in
  anything and the cell is nullable.

<a id="wizard_ui_bridge.matrix_cell_defs.AnswerIntCell"></a>

## AnswerIntCell Objects

```python
@dataclass
class AnswerIntCell()
```

An answer to an integer cell in a matrix form.

**Attributes**:

- `asking` - How the cell was asked, including the help text and other
  attributes of the cell.
- `value` - The value of the answer, or None when the user did not fill in
  anything and the cell is nullable.

<a id="wizard_ui_bridge.matrix_cell_defs.AnswerPathCell"></a>

## AnswerPathCell Objects

```python
@dataclass
class AnswerPathCell()
```

An answer to a path cell in a matrix form.

**Attributes**:

- `asking` - How the cell was asked, including the help text and other
  attributes of the cell.
- `value` - The value of the answer, or None when the user did not fill in
  anything and the cell is nullable.

<a id="wizard_ui_bridge.matrix_cell_defs.AnswerYesNoCell"></a>

## AnswerYesNoCell Objects

```python
@dataclass
class AnswerYesNoCell()
```

An answer to a yes/no cell in a matrix form.

**Attributes**:

- `asking` - How the cell was asked, including the help text and other
  attributes of the cell.
- `value` - The value of the answer.

<a id="wizard_ui_bridge.matrix_cell_defs.AnswerChoiceCell"></a>

## AnswerChoiceCell Objects

```python
@dataclass
class AnswerChoiceCell()
```

An answer to a choice cell in a matrix form.

**Attributes**:

- `asking` - How the cell was asked, including the help text and other
  attributes of the cell.
- `value` - The chosen value, one of the choices, or None. A final
  answer is None only when the choice is nullable and left
  empty, or when the choice is disabled by a partial validator
  because it is irrelevant given the current state of the form.
  Otherwise None only tells a partial validator that a choice
  with no default has not been answered yet: a bridge makes
  sure such a choice is answered before the form is submitted
  for final validation.

<a id="wizard_ui_bridge.matrix_cell_defs.AnswerMultiChoiceCell"></a>

## AnswerMultiChoiceCell Objects

```python
@dataclass
class AnswerMultiChoiceCell()
```

An answer to a multi-choice cell in a matrix form.

**Attributes**:

- `asking` - How the cell was asked, including the help text and other
  attributes of the cell.
- `value` - The values of the answer.

<a id="wizard_ui_bridge.matrix_cell_defs.AnswerFloatCell"></a>

## AnswerFloatCell Objects

```python
@dataclass
class AnswerFloatCell()
```

An answer to a float cell in a matrix form.

**Attributes**:

- `asking` - How the cell was asked, including the help text and other
  attributes of the cell.
- `value` - The value of the answer, or None when the user did not fill in
  anything and the cell is nullable.

<a id="wizard_ui_bridge.matrix_cell_defs.AnswerDateCell"></a>

## AnswerDateCell Objects

```python
@dataclass
class AnswerDateCell()
```

An answer to a date cell in a matrix form.

**Attributes**:

- `asking` - How the cell was asked, including the help text and other
  attributes of the cell.
- `value` - The value of the answer, or None when the user did not fill in
  anything and the cell is nullable.

<a id="wizard_ui_bridge.matrix_cell_defs.AnswerTimeCell"></a>

## AnswerTimeCell Objects

```python
@dataclass
class AnswerTimeCell()
```

An answer to a time cell in a matrix form.

**Attributes**:

- `asking` - How the cell was asked, including the help text and other
  attributes of the cell.
- `value` - The value of the answer, or None when the user did not fill in
  anything and the cell is nullable.

<a id="wizard_ui_bridge.matrix_cell_defs.AnswerDateTimeCell"></a>

## AnswerDateTimeCell Objects

```python
@dataclass
class AnswerDateTimeCell()
```

An answer to a date-time cell in a matrix form.

**Attributes**:

- `asking` - How the cell was asked, including the help text and other
  attributes of the cell.
- `value` - The value of the answer, or None when the user did not fill in
  anything and the cell is nullable.

<a id="wizard_ui_bridge.matrix_cell_defs.AnswerDurationCell"></a>

## AnswerDurationCell Objects

```python
@dataclass
class AnswerDurationCell()
```

An answer to a duration cell in a matrix form.

**Attributes**:

- `asking` - How the cell was asked, including the help text and other
  attributes of the cell.
- `value` - The value of the answer, or None when the user did not fill in
  anything and the cell is nullable.

<a id="wizard_ui_bridge._textual_table"></a>

# wizard\_ui\_bridge.\_textual\_table

The editable table screen of the Textual bridge.

The screen shows a table question as a grid of inputs and drop-downs,
with buttons to add and remove rows when the number of rows may vary.

<a id="wizard_ui_bridge._textual_table._TableApp"></a>

## \_TableApp Objects

```python
class _TableApp(_NavApp[list[list[Optional[str]]]])
```

Editable grid returning every cell the user left.

Read-only columns show fixed text in the template rows. Editable
cells are a text input, or a drop-down when the cell offers choices.
An empty editable cell is reported as None when the cell is nullable
and as an empty string for a free-text cell, while a drop-down is
blank only when the cell is nullable.

When min_rows and max_rows are both given the table has a variable
number of rows: an Add row and a Remove row button grow the table up
to max_rows and shrink it down to min_rows. Every cell in an added
row is editable, even in a read-only column, and its descriptor comes
from new_row_template().

A rejected cell is framed in the error colour while the shared status
line names it, so the user sees which cell of the grid to correct.

<a id="wizard_ui_bridge._textual_table._TableApp.__init__"></a>

#### \_\_init\_\_

```python
def __init__(columns: Sequence[TableColumn],
             cells: list[list[TableCell]],
             question: str,
             messages: list[str],
             partial_check: Optional[PartialCheck],
             min_rows: Optional[int] = None,
             max_rows: Optional[int] = None) -> None
```

Store the columns, starting rows, prompt, check and bounds.

<a id="wizard_ui_bridge._textual_table._TableApp.compose"></a>

#### compose

```python
def compose() -> ComposeResult
```

Lay out the header, the editable grid, the buttons and footer.

<a id="wizard_ui_bridge._textual_table._TableApp.on_mount"></a>

#### on\_mount

```python
def on_mount() -> None
```

Size the grid, keep the scroll unfocused, focus a cell.

<a id="wizard_ui_bridge._textual_table._TableApp._focus_first_cell"></a>

#### \_focus\_first\_cell

```python
def _focus_first_cell() -> None
```

Move focus to the first editable cell of the first row.

<a id="wizard_ui_bridge._textual_table._TableApp._grid_cells"></a>

#### \_grid\_cells

```python
def _grid_cells() -> Iterator[Widget]
```

Yield the header labels and then the rows, top to bottom.

<a id="wizard_ui_bridge._textual_table._TableApp._row_widgets"></a>

#### \_row\_widgets

```python
def _row_widgets(row: int) -> Iterator[Widget]
```

Yield the widgets of one data row, left to right.

<a id="wizard_ui_bridge._textual_table._TableApp._is_readonly"></a>

#### \_is\_readonly

```python
def _is_readonly(row: int, col: int) -> bool
```

Return whether a cell shows fixed text instead of a widget.

Cells in added rows are always editable, even in a column that is
read-only in the template rows.

<a id="wizard_ui_bridge._textual_table._TableApp._cell_widget"></a>

#### \_cell\_widget

```python
def _cell_widget(row: int, col: int) -> Widget
```

Return the widget shown for one cell of the grid.

<a id="wizard_ui_bridge._textual_table._TableApp._on_input"></a>

#### \_on\_input

```python
@on(Input.Changed)
def _on_input(event: Input.Changed) -> None
```

Re-check the table after a text cell changes.

<a id="wizard_ui_bridge._textual_table._TableApp._on_select"></a>

#### \_on\_select

```python
@on(Select.Changed)
def _on_select(event: Select.Changed) -> None
```

Re-check the table after a drop-down cell changes.

<a id="wizard_ui_bridge._textual_table._TableApp._recheck"></a>

#### \_recheck

```python
def _recheck(position: Optional[tuple[int, int]]) -> None
```

Update the changed cell and show any partial-check message.

<a id="wizard_ui_bridge._textual_table._TableApp.action_submit"></a>

#### action\_submit

```python
def action_submit() -> None
```

Exit returning every cell, including the read-only columns.

<a id="wizard_ui_bridge._textual_table._TableApp._submit_clicked"></a>

#### \_submit\_clicked

```python
@on(Button.Pressed, '#submit')
def _submit_clicked(_event: Button.Pressed) -> None
```

Submit the table when the submit button is pressed.

<a id="wizard_ui_bridge._textual_table._TableApp._add_clicked"></a>

#### \_add\_clicked

```python
@on(Button.Pressed, '#add_row')
def _add_clicked(_event: Button.Pressed) -> None
```

Add a row when the add-row button is pressed.

<a id="wizard_ui_bridge._textual_table._TableApp._remove_clicked"></a>

#### \_remove\_clicked

```python
@on(Button.Pressed, '#remove_row')
def _remove_clicked(_event: Button.Pressed) -> None
```

Remove the last row when the remove-row button is pressed.

<a id="wizard_ui_bridge._textual_table._TableApp._add_row"></a>

#### \_add\_row

```python
def _add_row() -> None
```

Append one editable row, up to max_rows.

<a id="wizard_ui_bridge._textual_table._TableApp._remove_row"></a>

#### \_remove\_row

```python
def _remove_row() -> None
```

Remove the last row, down to min_rows.

<a id="wizard_ui_bridge._textual_table._TableApp._report"></a>

#### \_report

```python
def _report(position: Optional[tuple[int, int]], message: str) -> None
```

Show a message, naming and framing the cell it complains of.

A message given no cell position, such as one about the number of
rows, is about the whole table: it is shown unchanged and no cell
is framed.

<a id="wizard_ui_bridge._textual_table._TableApp._set_status"></a>

#### \_set\_status

```python
def _set_status(message: str) -> None
```

Show a status message below the table.

<a id="wizard_ui_bridge._textual_table._TableApp._read_cell"></a>

#### \_read\_cell

```python
def _read_cell(row: int, col: int) -> Optional[str]
```

Return the current value of one cell for the result table.

<a id="wizard_ui_bridge.arg_types"></a>

# wizard\_ui\_bridge.arg\_types

Types used as arguments to the WizardUiBridge class.

<a id="wizard_ui_bridge.arg_types.AskReader"></a>

## AskReader Objects

```python
class AskReader(Protocol)
```

A reader of one raw user answer, used by the table helpers.

It takes a prompt, an optional re-ask reason, optional choices and a
keyword-only help text, and returns the raw user answer as text or a
0-based choice index. The shared table helpers take one, so every
bridge that fills a table one cell at a time supplies its own reader
and shares the table code. A reader without the help_text parameter
still works but is deprecated: the table helpers then leave the help
text out and issue a DeprecationWarning.

<a id="wizard_ui_bridge.arg_types.AskReader.__call__"></a>

#### \_\_call\_\_

```python
def __call__(question: str,
             re_ask_reason: Optional[str],
             choices: Optional[Sequence[str]],
             *,
             help_text: Optional[str] = None) -> str | int
```

Ask one question and return the raw answer.

**Arguments**:

- `question` - The prompt to show.
- `re_ask_reason` - The reason for re-asking, or None.
- `choices` - The choices to offer as a menu, or None for text.
- `help_text` - The help text to show when the user asks for help,
  or None when there is no help.

<a id="wizard_ui_bridge.arg_types.WizardNavigation"></a>

## WizardNavigation Objects

```python
class WizardNavigation(Exception)
```

Base class for wizard navigation requests raised by a bridge.

A user interface raises a subclass of this exception from an ask
method when the user wants to move within the wizard instead of
answering the current question. The wizard keeps these distinct from
validation errors, so its retry loops never catch them and they
reach the navigation driver unchanged.

<a id="wizard_ui_bridge.arg_types.WizardBack"></a>

## WizardBack Objects

```python
class WizardBack(WizardNavigation)
```

Request to return to the previous wizard question.

A bridge raises this when the user chooses "back". The wizard
restores the data collected before the previous question and asks
that question again. Raised at the first question of one wizard call
it has no earlier question within that call, so the wizard lets it
propagate out to the application. The application can then step back
in its own outer navigation, for instance to the previous section.

<a id="wizard_ui_bridge.arg_types.WizardCancelLevel"></a>

## WizardCancelLevel Objects

```python
class WizardCancelLevel(WizardNavigation)
```

Request to leave the current level and change what opened it.

A bridge raises this when the user asks to step out of the current
level of questions, such as a table of detail values or a group of
questions that exist only because of an earlier choice.
Unlike WizardBack, which moves to the previous question at the same
level, this asks to return to the question one level out whose answer
opened the current level, so the user can change that answer. The
answers collected at the current level are not recorded as answers,
but a well crafted wizard keeps them in memory as drafts so that
they can be offered as defaults if the user returns to the level and
provided that answers to other questions have not invalidated them.

Each level's driver catches this from the level it opened and re-asks
the opening question. When the current level has no enclosing level,
the outermost driver cannot step out; following this contract it
re-asks the current question and tells the user there is no outer
level. Nesting may be arbitrarily deep: each driver either handles the
request for the level it opened or lets it propagate further out.

<a id="wizard_ui_bridge.arg_types.WizardAbort"></a>

## WizardAbort Objects

```python
class WizardAbort(WizardNavigation)
```

Request to abandon the whole wizard.

A bridge raises this when the user gives up entirely. The wizard does
not catch it; it propagates out of the wizard call so the application
can stop the questioning session.

<a id="wizard_ui_bridge.arg_types.WizardPathKind"></a>

## WizardPathKind Objects

```python
class WizardPathKind(Enum)
```

Expected path type and existence for a path question.

<a id="wizard_ui_bridge.arg_types.check_nullable"></a>

#### check\_nullable

```python
def check_nullable(nullable: bool, has_default: bool) -> None
```

Raise ValueError when nullable is combined with a default.

A None answer means that nothing is filled in or selected, while a
default fills in a value for an empty answer, so asking for both is
a contradiction and a programming error in the calling code.

**Arguments**:

- `nullable` - Whether an empty answer is reported as None.
- `has_default` - Whether a default value is given.

**Raises**:

- `ValueError` - Both nullable and has_default are True.

<a id="wizard_ui_bridge.arg_types.check_choice_args"></a>

#### check\_choice\_args

```python
def check_choice_args(choices: Sequence[str], default: Optional[str],
                      nullable: bool) -> None
```

Raise ValueError when single-choice arguments contradict each other.

**Arguments**:

- `choices` - The choices offered.
- `default` - The choice selected by an empty answer, or None.
- `nullable` - Whether no choice is allowed, reported as None.

**Raises**:

- `ValueError` - default is not one of choices, or default is given
  together with nullable.

<a id="wizard_ui_bridge.arg_types.check_multi_args"></a>

#### check\_multi\_args

```python
def check_multi_args(choices: Sequence[str], default: Optional[Sequence[str]],
                     min_select: int, max_select: Optional[int]) -> None
```

Raise ValueError when multi-choice arguments contradict each other.

The selection bounds must be satisfiable, so 0 <= min_select <=
max_select <= len(choices), where a max_select of None stands for
len(choices). A default must name distinct choices, at most
max_select of them. It may name fewer than min_select, leaving the
rest of the selection for the user to make deliberately.

**Arguments**:

- `choices` - The choices offered.
- `default` - The choices pre-selected by an empty answer, or None.
- `min_select` - The smallest acceptable number of choices.
- `max_select` - The largest acceptable number of choices, or None.

**Raises**:

- `ValueError` - The bounds cannot be satisfied, or default names a
  value that is not a choice, names a choice twice or
  names more than max_select choices.

<a id="wizard_ui_bridge.arg_types.PathAskOptions"></a>

## PathAskOptions Objects

```python
@dataclass(frozen=True)
class PathAskOptions()
```

Options for a path question.

**Attributes**:

- `kind` - The expected path type and existence.
- `nullable` - When True an empty answer is reported as None. Not
  allowed together with a default.
- `default` - The path returned by an empty answer, or None for no
  default.

<a id="wizard_ui_bridge.arg_types.PathAskOptions.__post_init__"></a>

#### \_\_post\_init\_\_

```python
def __post_init__() -> None
```

Check that nullable is not combined with a default.

<a id="wizard_ui_bridge.arg_types.TableColumn"></a>

## TableColumn Objects

```python
@dataclass(frozen=True)
class TableColumn()
```

Header and editability for one whole column of a table question.

A table question describes its columns once. Read-only columns show
fixed text the user cannot edit, such as a column of parameter names.
Per-cell values and value constraints are described by TableCell.

**Attributes**:

- `header` - Column heading shown to the user.
- `read_only` - True when the whole column shows fixed text the user
  cannot edit.

<a id="wizard_ui_bridge.arg_types.TableCell"></a>

## TableCell Objects

```python
@dataclass(frozen=True)
class TableCell()
```

Initial content and value constraints for one table cell.

A table question holds one TableCell per column in each row, so each
row of an editable column can offer its own finite value set. This
suits a table whose rows are different parameters that each accept
different values, such as one settings row per named option.

**Attributes**:

- `value` - The initial text shown in the cell. For a read-only column
  this is the fixed text. For an editable column it is the
  pre-filled value, or None for an empty cell.
- `choices` - The finite set of values this cell accepts, or None for
  free text. A graphical bridge can render choices as a
  drop-down.
- `nullable` - True when the user may leave the cell empty, which the
  table reports as None. False when an empty cell is not
  interpreted as None: with choices None an empty cell is
  an empty string the validation may or may not accept,
  and with choices given an empty editable cell is not yet
  a valid final value.

**Raises**:

- `ValueError` - choices is given and value is neither None nor one
  of choices.

<a id="wizard_ui_bridge.arg_types.TableCell.__post_init__"></a>

#### \_\_post\_init\_\_

```python
def __post_init__() -> None
```

Check that a given value is one of the choices.

<a id="wizard_ui_bridge.matrix_defs"></a>

# wizard\_ui\_bridge.matrix\_defs

Definitions of the request and validator types of a matrix form.

A matrix form asks a single context setting question on the top of the
screen, followed by a matrix of cells, and has a feed-back area for
messages from a partial validator. The cell types are defined in module
matrix_cell_defs.

The number of rows and columns may vary at run time between the minimum
and maximum dimensions of the request. Rows and columns with only labels
still count like any other row or column. Rows and columns are only
appended after the last row or column, and only the last row or column
is deleted, so the position of a remaining cell never changes.

Labels can be used to provide context at any position in the matrix.
There is no requirement for any position to have a label;
labels are optional and can be placed wherever needed.

Sometimes the client chooses a design with leading label rows
or columns that provide context for the rest of the matrix.
A minimum dimension larger than the number of leading label
rows or columns keeps those labels from being deleted.

<a id="wizard_ui_bridge.matrix_defs.CellPosition"></a>

## CellPosition Objects

```python
class CellPosition(NamedTuple)
```

The position of a cell in a matrix form, both indexes 0-based.

**Attributes**:

- `row` - The row index of the cell.
- `column` - The column index of the cell.

<a id="wizard_ui_bridge.matrix_defs.MatrixDimension"></a>

## MatrixDimension Objects

```python
@dataclass(frozen=True)
class MatrixDimension()
```

The number of rows and columns of a matrix form.

Label rows and label columns count like any other row or column.

**Attributes**:

- `rows` - The number of rows in the matrix.
- `columns` - The number of columns in the matrix.

<a id="wizard_ui_bridge.matrix_defs.MatrixDimension.__post_init__"></a>

#### \_\_post\_init\_\_

```python
def __post_init__() -> None
```

Check that neither size is negative.

<a id="wizard_ui_bridge.matrix_defs.MatrixDimensions"></a>

## MatrixDimensions Objects

```python
@dataclass(frozen=True)
class MatrixDimensions()
```

The minimum, maximum and default dimensions of a matrix form.

When min and max are equal the matrix has a fixed shape, which
MatrixDimensions.fixed(rows, columns) builds directly. Otherwise the
user may append or delete the last row or column within the bounds.
An appended row or column normally shows cells the MatrixCellSpec
already gives for its position; see MatrixCellSpec for when a cell
is repeated instead.

**Attributes**:

- `min` - The minimum dimensions of the matrix.
- `max` - The maximum dimensions of the matrix.
- `default` - The default dimensions of the matrix.
  What is first shown before the user resizes the matrix.

<a id="wizard_ui_bridge.matrix_defs.MatrixDimensions.__post_init__"></a>

#### \_\_post\_init\_\_

```python
def __post_init__() -> None
```

Check that min <= default <= max for both rows and columns.

<a id="wizard_ui_bridge.matrix_defs.MatrixDimensions.fixed"></a>

#### fixed

```python
@classmethod
def fixed(cls, rows: int, columns: int) -> Self
```

Return the dimensions of a matrix the user cannot resize.

The minimum, maximum and default dimensions are all rows x columns.

<a id="wizard_ui_bridge.matrix_defs.PartMatrixValidationRes"></a>

## PartMatrixValidationRes Objects

```python
class PartMatrixValidationRes(NamedTuple)
```

Result of validating a partly filled matrix form.

**Attributes**:

- `is_valid` - True when the form is valid, False when it is not valid.
- `message` - A message to be displayed to the user, explaining why the
  form is not valid. Empty string when the form is valid.
- `disable_cells` - A tuple of positions that should be disabled in the
  matrix, because what has been filled in so far makes
  these cells irrelevant. For example if output format
  is set to some binary format, then the cell(s) that
  ask for character encoding can be disabled, because
  they are irrelevant for the chosen output format.
  Each result replaces the disabled cells of the
  previous one. Actually disabling these cells is not
  strictly necessary, but it is a good user experience
  to do so.
- `prefill_values` - Values the validator asks the bridge to place into
  other cells' inputs, as a tuple of
  (cell_position, value) pairs. Each value must match
  the answer type of the cell in that position. A bridge
  applies each request during live editing as if the
  user had typed the value; setting a value equal to
  the one already there is a no-op, so a validator
  that emits a stable value does not loop. The validator
  owns idempotency: it should emit a prefill only when
  it means to fill or overwrite the target. A prefill
  aimed at the cell that just changed is ignored, so
  writing back never fights the user's current edit.
  A prefill aimed at a disabled cell is still applied,
  so the value shows in the greyed cell and takes effect
  if the cell is later enabled. A cell position outside
  the matrix, a label cell, or a value whose type does
  not match the cell, raises an exception, since all
  are validator bugs. A choice or multi-choice value not
  among the cell's choices, and any prefill of a
  sensitive cell, are ignored. prefill_values is a
  live-editing convenience only and is ignored when the
  form is submitted, so an application must still apply
  the same default on submit.

<a id="wizard_ui_bridge.matrix_defs.MatrixConsoleQuestion"></a>

## MatrixConsoleQuestion Objects

```python
class MatrixConsoleQuestion(NamedTuple)
```

How to ask for cells in a matrix form in a console.

The matrix form is not well-suited for console input, so this class
provides guidance on how to ask for cells in a console environment,
where the cells are asked one at a time. The question of each cell
names it by the parts that are switched on below, in the order row
label, column label and CellNamer name, joined with ' / ', such as
'Alice / Mon'. When no part is switched on, or all of them are
empty, the cell is named as by matrix_helpers.cell_name().

**Attributes**:

- `use_help_text` - Whether to display the help text for each cell
  when asking for input in the console without requiring
  the user to explicitly request help. If this is True,
  the help text should be displayed immediately before
  expecting input for that cell. If this is False, the help text
  should only be displayed in response to an explicit request
  from the user, which is the answer ':?' on the console.
- `show_horizontal_label` - If this is True, the label closest to
  the left of the cell asked for in the same row is displayed
  for each cell asked for in the console, or the 1-based row
  number, as in 'Row 2', when the row has no such label.
  If this is False, the horizontal label should not be displayed.
- `show_vertical_label` - If this is True, the label closest above
  the cell asked for in the same column is displayed for each
  cell asked for in the console, or the 1-based column number,
  as in 'Column 3', when the column has no such label.
  If this is False, the vertical label should not be displayed.
- `row_order` - If this is True, the cells should be asked for in
  row-major order, meaning that all cells in a row are asked for
  before moving on to the next row. If False, column-major order
  should be used, meaning that all cells in a column are asked for
  before moving on to the next column.
- `use_cell_namer` - If this is True and the request has a cell_namer,
  the name it gives is displayed for each cell asked for in the
  console, after any labels. An empty name is left out. If this
  is False, the cell_namer is only used in the messages the
  bridge writes itself.

<a id="wizard_ui_bridge.matrix_defs.MatrixRequest"></a>

## MatrixRequest Objects

```python
class MatrixRequest(NamedTuple)
```

Request for a matrix form.

**Attributes**:

- `long_question` - The main question or instruction to display above the
  matrix form. It may be a long string that the UI bridge is
  responsible for wrapping and displaying nicely.
- `ask_cells` - The specification for the cells in the matrix form.
- `dimensions` - The minimum, maximum and default dimensions of the matrix.
- `console_question` - How a console bridge asks for the cells.
- `partial_validator` - Optional callback for early per-cell feedback.
- `cell_namer` - Optional callback naming a cell in the messages the
  bridge writes itself, see CellNamer.

<a id="wizard_ui_bridge.form_helpers"></a>

# wizard\_ui\_bridge.form\_helpers

Helpers shared by the WizardUiBridge form and matrix form questions.

Every Ask*Field of a form derives from the Ask*Cell of a matrix form, so
the helpers that only need what a field and a cell have in common take a
cell, and serve both questions.

<a id="wizard_ui_bridge.form_helpers.nullable_choice"></a>

#### nullable\_choice

```python
def nullable_choice(field: AskField) -> bool
```

Return whether field is a nullable choice field.

The base WizardUiBridge.supports_form_field() rejects such a field,
since a bridge written before ask_choice() took nullable cannot ask
one. Each bridge in this package supports it.

<a id="wizard_ui_bridge.form_helpers.initial_answer"></a>

#### initial\_answer

```python
def initial_answer(field: AskCell) -> AnswerCell
```

Return the starting answer for a field or input cell.

The value is the field's default, or the empty or not-yet-answered
state when the field has no default. A choice field with no default
starts as None, which tells a partial validator the choice is not
answered yet; a bridge must not leave that None in a submitted form.
A form field gets its Answer*Field and a matrix cell its Answer*Cell.
A label cell has no answer and must not be passed.

<a id="wizard_ui_bridge.form_helpers._default_value"></a>

#### \_default\_value

```python
def _default_value(cell: AskCell) -> Optional[PrefillValueType]
```

Return the default answer value of an input cell or field.

A multi-choice with no default starts with nothing selected.

<a id="wizard_ui_bridge.form_helpers.answer_of"></a>

#### answer\_of

```python
def answer_of(ask: AskCell, value: Optional[PrefillValueType]) -> AnswerCell
```

Return the answer holding value for a form field or an input cell.

A form field gets its Answer*Field and a matrix cell its Answer*Cell,
so a bridge reads a field and a cell the same way. value must have
the answer type of ask (see PrefillValueType), where an integer is
accepted for a float, a list of str is needed for a multi-choice, a
bool for a yes/no, and None is accepted wherever the answer value is
Optional. A label cell has no answer and must not be passed.

<a id="wizard_ui_bridge.form_helpers._optional"></a>

#### \_optional

```python
def _optional(value: Optional[PrefillValueType],
              kind: type[_T]) -> Optional[_T]
```

Return value, which must be None or an instance of kind.

<a id="wizard_ui_bridge.form_helpers._float_value"></a>

#### \_float\_value

```python
def _float_value(value: Optional[PrefillValueType]) -> Optional[float]
```

Return value as a float, accepting an integer as float defaults do.

<a id="wizard_ui_bridge.form_helpers._text_like_answer"></a>

#### \_text\_like\_answer

```python
def _text_like_answer(
        ask: AskCell,
        value: Optional[PrefillValueType]) -> Optional[AnswerCell]
```

Return the answer of a text, integer or path ask, else None.

<a id="wizard_ui_bridge.form_helpers._choice_answer"></a>

#### \_choice\_answer

```python
def _choice_answer(ask: AskCell,
                   value: Optional[PrefillValueType]) -> Optional[AnswerCell]
```

Return the answer of a yes/no, choice or multi-choice, else None.

<a id="wizard_ui_bridge.form_helpers._number_answer"></a>

#### \_number\_answer

```python
def _number_answer(ask: AskCell,
                   value: Optional[PrefillValueType]) -> Optional[AnswerCell]
```

Return the answer of a float, date or time ask, else None.

<a id="wizard_ui_bridge.form_helpers._temporal_answer"></a>

#### \_temporal\_answer

```python
def _temporal_answer(ask: AskCell,
                     value: Optional[PrefillValueType]) -> AnswerCell
```

Return the answer of a date-time or duration ask.

<a id="wizard_ui_bridge.form_helpers.valid_prefills"></a>

#### valid\_prefills

```python
def valid_prefills(
        fields: Sequence[AskField], changed: int, prefill_values: PrefillValues
) -> Iterator[tuple[int, PrefillValueType]]
```

Yield the prefill requests a bridge should apply, validated.

Each yielded (index, value) pair is ready to place into the row's
input. A prefill aimed at the changed row is skipped, so writing back
never fights the user's current edit. A row index outside the form
raises IndexError and a value whose Python type does not match the
field raises TypeError, since both are validator bugs. A choice value
not among the field's choices, any prefill of a sensitive text field,
and a multi-choice value with no valid member, are dropped instead, so
a portable validator stays safe. A multi-choice value keeps only its
members that are valid choices.

<a id="wizard_ui_bridge.form_helpers._check_row"></a>

#### \_check\_row

```python
def _check_row(fields: Sequence[AskField], index: int) -> None
```

Raise when a prefill row index lies outside the form.

<a id="wizard_ui_bridge.form_helpers.prefill_value"></a>

#### prefill\_value

```python
def prefill_value(cell: AskCell, value: PrefillValueType,
                  where: str) -> Optional[PrefillValueType]
```

Return the value to apply for a prefill, or None to drop it.

cell is the input field or cell the prefill is aimed at, and where
names its place, such as 'row 2', in the error message. The rules are
those of valid_prefills(). Raises TypeError when value's Python type
does not match cell.

<a id="wizard_ui_bridge.form_helpers._ordered_prefill"></a>

#### \_ordered\_prefill

```python
def _ordered_prefill(cell: AskCell, value: PrefillValueType,
                     where: str) -> PrefillValueType
```

Return an ordered cell's prefill, or raise TypeError for it.

An integer or float cell takes a number, and a date cell takes a
date that is not a datetime, so a datetime is never mistaken for a
plain date. Each temporal cell takes exactly its own type.

<a id="wizard_ui_bridge.form_helpers._multi_prefill"></a>

#### \_multi\_prefill

```python
def _multi_prefill(cell: AskMultiChoiceCell, value: PrefillValueType,
                   where: str) -> Optional[list[str]]
```

Return the valid members of a multi-choice prefill, or None.

<a id="wizard_ui_bridge.form_helpers._need"></a>

#### \_need

```python
def _need(value: PrefillValueType, where: str, wanted: type) -> None
```

Raise TypeError when value is not an instance of wanted.

<a id="wizard_ui_bridge.form_helpers._bad_type"></a>

#### \_bad\_type

```python
def _bad_type(where: str) -> NoReturn
```

Raise a TypeError for a prefill value of the wrong type.

<a id="wizard_ui_bridge.form_helpers.prefilled_field"></a>

#### prefilled\_field

```python
def prefilled_field(field: AskCell, prefill: PrefillValueType) -> AskCell
```

Return a form field or input cell with prefill as its default.

The console bridge offers a prefill as the default of the field or
cell when it is asked. A field may not be both nullable and have a
default, so the returned field is not nullable: as for any default,
an empty answer takes the prefill. A prefill that cannot serve as a
valid default, such as an integer or date outside the field's bounds
or a multi-choice selection of more than max_select choices, is
ignored so the field keeps its own default. The prefill has already
been checked against the field type by valid_prefills() or
matrix_helpers.valid_cell_prefills(). A label cell must not be passed.

<a id="wizard_ui_bridge.form_helpers._default_a"></a>

#### \_default\_a

```python
def _default_a(field: AskCell, prefill: PrefillValueType) -> Optional[AskCell]
```

Return field with prefill as default for the first field group.

<a id="wizard_ui_bridge.form_helpers._default_b"></a>

#### \_default\_b

```python
def _default_b(field: AskCell, prefill: PrefillValueType) -> AskCell
```

Return field with prefill as default for the second field group.

<a id="wizard_ui_bridge.bridge"></a>

# wizard\_ui\_bridge.bridge

User interface bridge for a wizard asking a user questions.

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

<a id="wizard_ui_bridge.bridge.WizardUiBridge"></a>

## WizardUiBridge Objects

```python
class WizardUiBridge()
```

Bridge between the wizard and the user interface.

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

<a id="wizard_ui_bridge.bridge.WizardUiBridge.ask_text"></a>

#### ask\_text

```python
def ask_text(question: str,
             re_ask_reason: Optional[str] = None,
             nullable: bool = False,
             *,
             default: Optional[str] = None,
             sensitive: bool = False,
             help_text: Optional[str] = None) -> Optional[str]
```

Ask a free-text question and return the entered text.

The application is responsible for implementing this method with
a real text-entry control. The base class has no implementation.

**Arguments**:

- `question` - The question to ask the user.
- `re_ask_reason` - The reason for re-asking the question, for
  instance that the user's answer was invalid.
- `nullable` - When True an empty answer is reported as None.
  When False an empty answer with no default is the
  empty string.
- `default` - The value returned by an empty answer, or None for
  no default. Not allowed together with nullable.
- `sensitive` - True when the bridge must avoid echoing the
  entered text, such as for passwords. A default is
  not allowed for a sensitive question.
- `help_text` - A help text for the question, or None for no help.
  A console bridge shows it when the user asks for
  help. A GUI bridge that overrides ask_form() and
  ask_matrix_form() may ignore it.
  

**Returns**:

  The entered text, default for an empty answer with a default,
  or None for an empty answer when nullable.

**Raises**:

- `ValueError` - default is given together with sensitive or
  nullable.
- `NotImplementedError` - The bridge does not implement ask_text().
- `WizardBack` - The user asked to return to the previous question.
- `WizardCancelLevel` - The user cancelled the current level.
- `WizardAbort` - The user abandoned the whole wizard.

<a id="wizard_ui_bridge.bridge.WizardUiBridge.ask_int"></a>

#### ask\_int

```python
def ask_int(question: str,
            re_ask_reason: Optional[str] = None,
            *,
            nullable: bool = False,
            min_value: Optional[int] = None,
            max_value: Optional[int] = None,
            default: Optional[int] = None,
            help_text: Optional[str] = None) -> Optional[int]
```

Ask for an integer, optionally within inclusive bounds.

The base implementation uses ask_text() and re-asks until the
answer is empty when allowed or parses as an integer in range. A
derived bridge may override it with a direct numeric control.

**Arguments**:

- `question` - The question to ask the user.
- `re_ask_reason` - The reason for re-asking the question, for
  instance that the user's answer was invalid.
- `nullable` - When True an empty answer is reported as None.
  When False an empty answer with no default will be
  re-asked until a valid answer is entered.
- `min_value` - The minimum allowed value, or None for no lower bound.
  The min value is inclusive.
- `max_value` - The maximum allowed value, or None for no upper bound.
  The max value is inclusive.
- `default` - The value returned by an empty answer, or None for
  no default. Not allowed together with nullable.
- `help_text` - A help text for the question, or None for no help.
  A console bridge shows it when the user asks for
  help. A GUI bridge that overrides ask_form() and
  ask_matrix_form() may ignore it.
  

**Returns**:

  The entered integer, default for an empty answer with a
  default, or None for an empty answer when nullable.

**Raises**:

- `ValueError` - min_value exceeds max_value, default is outside
  the bounds, or default is given together with
  nullable.
- `WizardBack` - The user asked to return to the previous question.
- `WizardCancelLevel` - The user cancelled the current level.
- `WizardAbort` - The user abandoned the whole wizard.

<a id="wizard_ui_bridge.bridge.WizardUiBridge.ask_path"></a>

#### ask\_path

```python
def ask_path(question: str,
             re_ask_reason: Optional[str] = None,
             *,
             options: Optional[PathAskOptions] = None,
             help_text: Optional[str] = None) -> Optional[Path]
```

Ask a question for a path and return the accepted path.

A derived bridge may override this method to provide a native file
or directory picker. The base implementation is permanent and
asks for text through ask_text(), then validates the answer.

**Arguments**:

- `question` - The question to ask the user.
- `re_ask_reason` - The reason for re-asking the question.
- `options` - Path options. None only rejects existing directories.
- `help_text` - A help text for the question, or None for no help.
  A console bridge shows it when the user asks for
  help. A GUI bridge that overrides ask_form() and
  ask_matrix_form() may ignore it.
  

**Returns**:

  The accepted path, a default path, or None when nullable.
  PathAskOptions does not allow both a default and nullable.

**Raises**:

- `WizardBack` - The user asked to return to the previous question.
- `WizardCancelLevel` - The user cancelled the current level.
- `WizardAbort` - The user abandoned the whole wizard.

<a id="wizard_ui_bridge.bridge.WizardUiBridge.ask_yes_no"></a>

#### ask\_yes\_no

```python
def ask_yes_no(question: str,
               default: bool,
               re_ask_reason: Optional[str] = None,
               *,
               help_text: Optional[str] = None) -> bool
```

Ask a yes/no question and return the chosen boolean.

Yes/no questions are asked through this method, and the
application is responsible for implementing it with a real yes/no
interface, such as a pair of yes and no buttons in a graphical
bridge or a y/n prompt in a console bridge. The base class has no
implementation.

**Arguments**:

- `question` - The yes/no question to ask.
- `default` - The value to use when the user makes no explicit
  choice.
- `re_ask_reason` - The reason for re-asking the question, for
  instance that the user's answer was invalid.
- `help_text` - A help text for the question, or None for no help.
  A console bridge shows it when the user asks for
  help. A GUI bridge that overrides ask_form() and
  ask_matrix_form() may ignore it.
  

**Returns**:

  The user's choice as a boolean.

**Raises**:

- `NotImplementedError` - The bridge does not implement ask_yes_no().
- `WizardBack` - The user asked to return to the previous question.
- `WizardCancelLevel` - The user cancelled the current level.
- `WizardAbort` - The user abandoned the whole wizard.

<a id="wizard_ui_bridge.bridge.WizardUiBridge.ask_choice"></a>

#### ask\_choice

```python
def ask_choice(question: str,
               *,
               choices: Sequence[str],
               default: Optional[str] = None,
               re_ask_reason: Optional[str] = None,
               nullable: bool = False,
               help_text: Optional[str] = None) -> Optional[str]
```

Ask the user to pick exactly one of choices and return it.

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

**Arguments**:

- `question` - The question to ask the user.
- `choices` - The choices to offer, in display order.
- `default` - The choice selected by an empty answer, or None to
  require an explicit choice. Not allowed together
  with nullable.
- `re_ask_reason` - The reason for re-asking, shown before the
  first question when not None.
- `nullable` - When True the user may select no choice, which is
  reported as None.
- `help_text` - A help text for the question, or None for no help.
  A console bridge shows it when the user asks for
  help. A GUI bridge that overrides ask_form() and
  ask_matrix_form() may ignore it.
  

**Returns**:

  The chosen value, one of choices, or None for no choice when
  nullable.

**Raises**:

- `ValueError` - default is not one of choices, or is given
  together with nullable. A bridge checks this with
  arg_types.check_choice_args().
- `NotImplementedError` - The bridge does not implement ask_choice().
- `WizardBack` - The user asked to return to the previous question.
- `WizardCancelLevel` - The user cancelled the current level.
- `WizardAbort` - The user abandoned the whole wizard.

<a id="wizard_ui_bridge.bridge.WizardUiBridge.ask_multi"></a>

#### ask\_multi

```python
def ask_multi(question: str,
              *,
              choices: Sequence[str],
              default: Optional[Sequence[str]] = None,
              min_select: int = 0,
              max_select: Optional[int] = None,
              re_ask_reason: Optional[str] = None,
              help_text: Optional[str] = None) -> list[str]
```

Ask the user to pick several of choices and return them.

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

**Arguments**:

- `question` - The question to ask the user.
- `choices` - The choices to offer, in display order.
- `default` - The values pre-selected by an empty answer, or None.
- `min_select` - The smallest acceptable number of choices.
- `max_select` - The largest acceptable number of choices, or None
  for no upper bound.
- `re_ask_reason` - The reason for re-asking, shown before the
  first question when not None.
- `help_text` - A help text for the question, or None for no help.
  A console bridge shows it when the user asks for
  help. A GUI bridge that overrides ask_form() and
  ask_matrix_form() may ignore it.
  

**Returns**:

  The chosen values, each one of choices, in choices order.

**Raises**:

- `ValueError` - The bounds cannot be satisfied, or default names
  a value that is not a choice, names a choice
  twice or names more than max_select choices. A
  bridge checks this with
  arg_types.check_multi_args().
- `NotImplementedError` - The bridge does not implement ask_multi().
- `WizardBack` - The user asked to return to the previous question.
- `WizardCancelLevel` - The user cancelled the current level.
- `WizardAbort` - The user abandoned the whole wizard.

<a id="wizard_ui_bridge.bridge.WizardUiBridge.ask_table"></a>

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

Ask the user to fill in a table and return its cells.

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
choices, with help_text as its help text and its value as its
default. Each row the user adds is built from the cells shared by
every starting row, as bridge_helpers.new_row_template() does,
with every column editable. A console names each cell by the
read-only texts of its row and its column header. A bridge may
override this method to show its own table widget, and the
helpers in wizard_ui_bridge.bridge_helpers fill a table one cell
at a time for a bridge that asks one question at a time.

How an empty editable cell is reported follows its TableCell: a
nullable cell reports None, a free-text cell reports an empty
string, and a cell with choices treats empty as not yet a valid
value. In the base implementation a pre-filled value is the
default of a matrix cell, which an empty answer returns, so a
pre-filled cell cannot be emptied there, and is never None even
when nullable.

When partial_check is given, the bridge calls it after the user
changes a cell, passing the whole table as it currently stands
and the (row, column) position of the changed cell, both 0-based.
The callback returns (accepted, message); the bridge uses message
to give early feedback. The callback must tolerate empty or partly
filled cells, and it gives advisory feedback only: the wizard
still validates the final table. In the base implementation a
message is shown when the cell is not accepted, as the partial
validator of ask_matrix_form() shows it.

**Arguments**:

- `columns` - Description of each column, in left-to-right order.
- `cells` - Starting rows, each a list of one TableCell per column.
- `question` - The question or instruction shown above the table.
- `re_ask_reason` - The reason for re-asking, for instance that a
  value failed validation.
- `partial_check` - Optional callback for early per-cell feedback.
  It receives the current table and the changed
  (row, column) position and returns an accepted
  flag and a message.
- `min_rows` - Minimum number of rows the user must leave in the
  table, or None when rows are fixed to the rows in
  cells. A variable number of rows requires both
  min_rows and max_rows to be non-None, and
  0 <= min_rows <= len(cells) <= max_rows.
- `max_rows` - Maximum number of rows the user may add the table
  to, or None when rows are fixed to the rows in
  cells. A variable number of rows requires both
  min_rows and max_rows to be non-None.
- `help_text` - A help text for the question, or None for no help.
  A console bridge shows it when the user asks for
  help. A GUI bridge that overrides ask_form() and
  ask_matrix_form() may ignore it.
  

**Returns**:

  The complete table as rows of cells, including the read-only
  columns, with one cell per column in each row. Each cell is
  the final string the user left, or None for an empty cell.

**Raises**:

- `ValueError` - A row of cells does not hold one cell per column,
  or a variable number of rows breaks
  0 <= min_rows <= len(cells) <= max_rows.
- `WizardBack` - The user asked to return to the previous question.
- `WizardCancelLevel` - The user cancelled the current level.
- `WizardAbort` - The user abandoned the whole wizard.

<a id="wizard_ui_bridge.bridge.WizardUiBridge.ask_form"></a>

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

Ask the user to fill in a form and return the answers.

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

When partial_validator is given, the base implementation calls it
after each field is answered, passing the current answers and the
index of the field just answered. It shows the returned message and
skips asking the fields listed in disable_row_idxs, filling them
with their default or not-yet-answered value instead. WizardBack
steps to the previous asked field; from the first field it
propagates so the wizard steps to the previous question.

**Arguments**:

- `long_question` - The main question or instruction to the user,
  typically shown above the form. It may be long
  string that the UI bridge is responsible for
  wrapping and displaying nicely.
- `ask_fields` - Description of each field in the form.
- `re_ask_reason` - The reason for re-asking, for instance how a
  value failed validation.
- `partial_validator` - Optional callback for early per-field
  feedback. It receives the current answers
  and the changed field index, and returns a
  PartFormValidationResult.
  

**Returns**:

  One AnswerField per AskField, in the order of ask_fields.

**Raises**:

- `WizardBack` - The user asked to return to the previous question.
- `WizardCancelLevel` - The user cancelled the current level.
- `WizardAbort` - The user abandoned the whole wizard.

<a id="wizard_ui_bridge.bridge.WizardUiBridge.supports_form_field"></a>

#### supports\_form\_field

```python
def supports_form_field(field: AskField) -> bool
```

Return True when the bridge can show the given form field.

A bridge that overrides ask_form() may not yet support all
the AskField types. This method returns True when the bridge can
show the given field, and False when it cannot. The base implementation
returns True only for the field types that oldest form bridges support,
so a bridge that overrides ask_form() should override this method as
well. The base implementation returns False for a nullable choice
field, since a bridge written before ask_choice() took nullable
cannot ask one; a bridge whose ask_choice() supports nullable
overrides this method to accept it.

**Arguments**:

- `field` - The form field to check.

**Returns**:

  True if the bridge can show the field, False otherwise.

<a id="wizard_ui_bridge.bridge.WizardUiBridge.ask_form_w_fake"></a>

#### ask\_form\_w\_fake

```python
def ask_form_w_fake(
        long_question: str,
        ask_fields: AskFields,
        *,
        re_ask_reason: Optional[str] = None,
        partial_validator: Optional[PartialFormValidator] = None
) -> AnswerFields
```

Ask the user to fill in a form faking unsupported field types.

This is a temporary migration aid for a wizard that uses field types
the bridge does not yet support. It replaces each unsupported field
with a supported field that asks the question and inserts a partial
form validator that guides the answer to something that can be
converted to the unsupported field type. ask_form() is then called
with the modified fields and validator, and the answers are converted
back to the original field types before returning.

**Arguments**:

- `long_question` - The main question or instruction to the user,
  typically shown above the form. It may be long
  string that the UI bridge is responsible for
  wrapping and displaying nicely.
- `ask_fields` - Description of each field in the form.
- `re_ask_reason` - The reason for re-asking, for instance how a
  value failed validation.
- `partial_validator` - Optional callback for early per-field
  feedback. It receives the current answers
  and the changed field index, and returns a
  PartFormValidationResult.
  

**Returns**:

  One AnswerField per AskField, in the order of ask_fields.

**Raises**:

- `WizardBack` - The user asked to return to the previous question.
- `WizardCancelLevel` - The user cancelled the current level.
- `WizardAbort` - The user abandoned the whole wizard.
- `RuntimeError` - The bridge cannot show any field type that would
  allow the requested field types to be faked, so
  the form cannot be shown at all.

<a id="wizard_ui_bridge.bridge.WizardUiBridge.ask_matrix_form"></a>

#### ask\_matrix\_form

```python
def ask_matrix_form(request: MatrixRequest,
                    *,
                    re_ask_reason: Optional[str] = None) -> AnswerCells
```

Ask the user to fill in values in the cells of a matrix form.

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
each prefill is offered as the default of its cell when that cell
is asked. The message is advisory only: the matrix is returned
even when it is not valid, so the wizard must check the answers.

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
the user has changed the matrix or tried to submit it.

See wizard_ui_bridge.matrix_cell_defs for the cell types and
wizard_ui_bridge.matrix_defs for the request and its validator.

**Arguments**:

- `request` - The MatrixRequest object containing all the details for
  the matrix form.
- `re_ask_reason` - The reason for re-asking, for instance how a
  value failed validation.
  

**Returns**:

  The answers in the final shape of the matrix, one row per
  matrix row: an AnswerCell for each input cell, and None for
  each label cell (AskLabelCell).
  

**Raises**:

- `WizardBack` - The user asked to return to the previous question.
- `WizardCancelLevel` - The user cancelled the current level.
- `WizardAbort` - The user abandoned the whole wizard.

<a id="wizard_ui_bridge.bridge.WizardUiBridge._show_question"></a>

#### \_show\_question

```python
def _show_question(long_question: str, re_ask_reason: Optional[str]) -> None
```

Show the question of a form, and the reason when re-asked.

<a id="wizard_ui_bridge.bridge.WizardUiBridge._fill_form"></a>

#### \_fill\_form

```python
def _fill_form(ask_fields: AskFields, answers: list[AnswerField],
               validator: Optional[PartialFormValidator]) -> None
```

Ask each enabled field in turn, stepping back on WizardBack.

A prefill returned by the validator for a not-yet-asked row is kept
in pending and offered as that row's default when it is asked.

<a id="wizard_ui_bridge.bridge.WizardUiBridge._prev_field"></a>

#### \_prev\_field

```python
@staticmethod
def _prev_field(position: int, disabled: set[int]) -> int
```

Return the previous enabled field index, or re-raise WizardBack.

<a id="wizard_ui_bridge.bridge.WizardUiBridge._form_feedback"></a>

#### \_form\_feedback

```python
def _form_feedback(ask_fields: AskFields, answers: list[AnswerField],
                   position: int, validator: Optional[PartialFormValidator],
                   pending: dict[int, PrefillValueType]) -> set[int]
```

Run the validator, show its message, store prefills, return rows.

Prefills for other rows are validated and kept in pending, so a
later row is offered the value as its default when it is asked.

<a id="wizard_ui_bridge.bridge.WizardUiBridge._ask_field"></a>

#### \_ask\_field

```python
def _ask_field(field: AskField,
               prefill: Optional[PrefillValueType] = None) -> AnswerField
```

Ask one form field with the matching typed ask method.

When prefill is given it replaces the field's default, so the value
is offered as the starting answer the user can accept or edit.

<a id="wizard_ui_bridge.bridge.WizardUiBridge.error_file"></a>

#### error\_file

```python
def error_file() -> TextIO
```

Return the stream used for validation diagnostics.

<a id="wizard_ui_bridge.bridge.WizardUiBridge.show"></a>

#### show

```python
def show(message: str) -> None
```

Show a message to the user.

If implementing a graphical user interface, this method should
display the message in a dialog or a message box. If implementing
a console text user interface, this method should print the
message to the console.

**Arguments**:

- `message` - The message to show the user.

<a id="wizard_ui_bridge.factory"></a>

# wizard\_ui\_bridge.factory

Factory selecting a text-mode user interface bridge.

The wizard talks to the user through a WizardUiBridge. This factory
returns a Textual full-screen bridge when Textual is installed and the
streams are a real terminal, and falls back to the console bridge
otherwise, such as when output is redirected, when running under tests,
or where Textual is not available. The fallback keeps the library
importable and usable even if Textual has been uninstalled.

Textual is an optional dependency, installed with the extra
`wizard-ui-bridge[textual]`. The Textual bridge is therefore imported
only when it is about to be used, and asking for it without Textual
installed raises ImportError instead of degrading silently.

This factory chooses between text-mode bridges only. An application with
a graphical user interface constructs a graphical bridge itself instead:
WizardUiBridgeTk from the companion package wizard-tk-bridge for Tkinter,
or a bridge of its own for another toolkit.

<a id="wizard_ui_bridge.factory.textual_installed"></a>

#### textual\_installed

```python
def textual_installed() -> bool
```

Return whether the optional textual package is installed.

<a id="wizard_ui_bridge.factory.load_textual_bridge"></a>

#### load\_textual\_bridge

```python
def load_textual_bridge() -> type[WizardUiBridge]
```

Return the Textual bridge class, importing it on demand.

Textual is only imported here, so that a program that never asks
for the Textual bridge never pays for importing Textual. The
availability check keeps the missing-package case a clear
ImportError, while any other import error in the Textual bridge
itself is still reported as the error it is.

**Raises**:

- `ImportError` - If the optional textual package is not installed.

<a id="wizard_ui_bridge.factory.UiBridgeType"></a>

## UiBridgeType Objects

```python
class UiBridgeType(Enum)
```

Type of wizard user interface bridge.

AUTO: Auto-select the best bridge based on the environment.
      This will use Textual if it is installed and the streams
      are a terminal, else a console bridge.
TEXTUAL: Use the Textual bridge, even if it might fail.
CONSOLE: Use the console bridge, even if Textual could be used.

<a id="wizard_ui_bridge.factory.make_text_ui_bridge"></a>

#### make\_text\_ui\_bridge

```python
def make_text_ui_bridge(
        stdout_file: TextIO,
        stdin_file: TextIO,
        stderr_file: TextIO,
        bridge_type: UiBridgeType = UiBridgeType.AUTO) -> WizardUiBridge
```

Return a Textual bridge for a terminal, else a console bridge.

**Arguments**:

- `stdout_file` - Stream the console bridge prints to, also checked
  for being a terminal.
- `stdin_file` - Stream the console bridge reads from, also checked
  for being a terminal.
- `stderr_file` - Stream the console bridge prints errors to.
- `bridge_type` - Type of bridge to use. Defaults to AUTO.
  If AUTO, select the best bridge based on the environment.
  If TEXTUAL, use the Textual bridge that might fail.
  If CONSOLE, use the console bridge.
  

**Raises**:

- `ImportError` - If TEXTUAL is asked for but textual is not installed.
  

**Returns**:

  A Textual bridge when Textual is installed and both streams are
  a terminal, otherwise a console bridge.

<a id="wizard_ui_bridge.factory._is_tty"></a>

#### \_is\_tty

```python
def _is_tty(stream: TextIO) -> bool
```

Return whether a stream reports that it is a terminal.

<a id="wizard_ui_bridge._parse"></a>

# wizard\_ui\_bridge.\_parse

Text parsing and formatting for the typed form fields.

The float, date, time, date-time and duration form fields all need to
turn user text into a typed value and a typed value back into text. This
module holds that shared conversion, together with the human-readable
hints and error messages, so the console form, the Textual form and the
ask_form_w_fake() fallback all agree on the accepted text.

A duration is written as an optional day count and a clock part,
``<days> d <hours>:<minutes>:<seconds>``, where the seconds may carry a
decimal fraction, or as a single non-negative number of seconds. Dates,
times and date-times use the ISO 8601 forms accepted by the standard
library fromisoformat() parsers.

<a id="wizard_ui_bridge._parse.NEW_FIELD_TYPES"></a>

#### NEW\_FIELD\_TYPES

The typed form field classes added on top of the original six.

<a id="wizard_ui_bridge._parse.parse_float"></a>

#### parse\_float

```python
def parse_float(text: str) -> Optional[float]
```

Return a finite float from text, or None when not a number.

<a id="wizard_ui_bridge._parse.parse_date"></a>

#### parse\_date

```python
def parse_date(text: str) -> Optional[date]
```

Return an ISO date from text, or None when not a valid date.

<a id="wizard_ui_bridge._parse.parse_time"></a>

#### parse\_time

```python
def parse_time(text: str) -> Optional[time]
```

Return an ISO time from text, or None when not a valid time.

<a id="wizard_ui_bridge._parse.parse_datetime"></a>

#### parse\_datetime

```python
def parse_datetime(text: str) -> Optional[datetime]
```

Return an ISO date-time from text, or None when not valid.

<a id="wizard_ui_bridge._parse.parse_duration"></a>

#### parse\_duration

```python
def parse_duration(text: str) -> Optional[timedelta]
```

Return a duration from text, or None when it is not valid.

A lone non-negative number is read as a count of seconds; otherwise
the text must be ``<hours>:<minutes>:<seconds>`` with an optional
``<days> d`` prefix, and the seconds may carry a decimal fraction.

<a id="wizard_ui_bridge._parse._timedelta_seconds"></a>

#### \_timedelta\_seconds

```python
def _timedelta_seconds(seconds: float) -> Optional[timedelta]
```

Return a duration of seconds seconds, or None when unusable.

<a id="wizard_ui_bridge._parse._timedelta_parts"></a>

#### \_timedelta\_parts

```python
def _timedelta_parts(groups: tuple[Optional[str], ...]) -> Optional[timedelta]
```

Return a duration built from matched day and clock groups.

<a id="wizard_ui_bridge._parse.format_duration"></a>

#### format\_duration

```python
def format_duration(value: timedelta) -> str
```

Return a duration as ``<days> d HH:MM:SS`` with any fraction.

<a id="wizard_ui_bridge._parse.format_new_value"></a>

#### format\_new\_value

```python
def format_new_value(value: object) -> str
```

Return the text a typed value would round-trip from.

<a id="wizard_ui_bridge._parse.ordered_range_error"></a>

#### ordered\_range\_error

```python
def ordered_range_error(minimum: Optional[object],
                        maximum: Optional[object]) -> str
```

Return the message shown when a typed value is out of range.

<a id="wizard_ui_bridge._parse._AskText"></a>

## \_AskText Objects

```python
class _AskText(Protocol)
```

The bridge ask_text() signature the typed re-ask loop calls.

<a id="wizard_ui_bridge._parse._AskText.__call__"></a>

#### \_\_call\_\_

```python
def __call__(question: str,
             re_ask_reason: Optional[str] = ...,
             nullable: bool = ...,
             *,
             default: Optional[str] = ...,
             help_text: Optional[str] = ...) -> Optional[str]
```

Ask for free text and return it, or None for an empty answer.

<a id="wizard_ui_bridge._parse._TypedCell"></a>

## \_TypedCell Objects

```python
class _TypedCell(Protocol[_OrderedT])
```

The attributes shared by the ordered typed cells and fields.

<a id="wizard_ui_bridge._parse.ask_typed"></a>

#### ask\_typed

```python
def ask_typed(ask_text: _AskText, question: str, field: _TypedCell[_OrderedT],
              parse: Callable[[str], Optional[_OrderedT]],
              hint: str) -> Optional[_OrderedT]
```

Re-ask a typed field or cell through ask_text until it is usable.

The hint is shown after the question and repeated in the parse-error
message, so a console user learns the accepted text format. An empty
answer yields the field default, or None when the field is nullable.
The help text of the field is passed to ask_text as help_text.

<a id="wizard_ui_bridge._parse._resolve"></a>

#### \_resolve

```python
def _resolve(value: Optional[_OrderedT], minimum: Optional[_OrderedT],
             maximum: Optional[_OrderedT],
             hint: str) -> tuple[Optional[_OrderedT], Optional[str]]
```

Return a parsed value and no error, or None and the reason why.

<a id="wizard_ui_bridge._parse.resolve_new"></a>

#### resolve\_new

```python
def resolve_new(field: AskField,
                text: Optional[str]) -> tuple[Optional[object], Optional[str]]
```

Return the typed value for a typed field's text, and any error.

A None text is an empty nullable answer, which is valid and has no
value. Otherwise the text is parsed and range-checked for the field's
type; the error is the reason to re-ask when the value is not usable.

<a id="wizard_ui_bridge._parse.new_answer"></a>

#### new\_answer

```python
def new_answer(field: AskField, value: Optional[object]) -> AnswerField
```

Wrap a typed value in the answer matching a typed field.

<a id="wizard_ui_bridge._parse.field_hint"></a>

#### field\_hint

```python
def field_hint(field: AskField) -> str
```

Return the format hint shown for a typed field.

<a id="wizard_ui_bridge._parse._new_bounds"></a>

#### \_new\_bounds

```python
def _new_bounds(field: AskField) -> tuple[bool, Optional[object]]
```

Return the (nullable, default) pair of a typed field.

<a id="wizard_ui_bridge._parse.value_from_text"></a>

#### value\_from\_text

```python
def value_from_text(field: AskField, text: str) -> Optional[object]
```

Return the typed value of a typed field for widget text.

An empty text yields the field default, matching how the console form
treats an empty answer. A non-empty text is parsed; unparsable or
out-of-range text yields None, and the caller reports the error.

<a id="wizard_ui_bridge._parse.error_from_text"></a>

#### error\_from\_text

```python
def error_from_text(field: AskField, text: str) -> Optional[str]
```

Return the parse or range error of a typed field's widget text.

Empty text is accepted when the field is nullable or has a default,
and otherwise reports that a value is required.

<a id="wizard_ui_bridge._parse.fake_field"></a>

#### fake\_field

```python
def fake_field(field: AskField) -> AskTextField
```

Return the text field used to fake an unsupported typed field.

<a id="wizard_ui_bridge._table"></a>

# wizard\_ui\_bridge.\_table

Variable-row table editing shared by the wizard UI bridges.

This module holds the console row-menu editor used when the console
bridge is asked for a variable-row table. The descriptor for rows added
at run time is bridge_helpers.new_row_template(), shared by all bridges.

The console editor shows the whole table as a numbered overview each
round and then asks one action prompt last, so the actions and any
re-ask reason stay visible after a long table has scrolled off the
screen. A row number edits that row, ':+' adds a row and ':- N' deletes
row N, while a blank answer accepts the table. Asked for help, the action
prompt explains these actions, followed by the help text of the table.
Editing a row reuses the same per-cell helpers as a fixed table, so choice
cells, the erase token, the help text and per-cell navigation behave
identically.

<a id="wizard_ui_bridge._table._ADD_ROW"></a>

#### \_ADD\_ROW

appends a row in the variable-row console table editor

<a id="wizard_ui_bridge._table._DEL_ROW"></a>

#### \_DEL\_ROW

deletes a row in the variable-row console table editor

<a id="wizard_ui_bridge._table._VarTable"></a>

## \_VarTable Objects

```python
class _VarTable()
```

Mutable state and editing for a variable-row console table.

A row number edits that row cell by cell, ':+' appends a row and
edits it, ':- N' deletes row N, and a blank answer accepts the table.
A row added to the table is fully editable, even in a column that is
read-only in the template rows, mirroring the Textual bridge.

<a id="wizard_ui_bridge._table._VarTable.__init__"></a>

#### \_\_init\_\_

```python
def __init__(columns: Sequence[TableColumn], cells: list[list[TableCell]],
             partial_check: Optional[PartialCheck], min_rows: int,
             max_rows: int, help_text: Optional[str]) -> None
```

Start from the given rows and remember the bounds and help.

<a id="wizard_ui_bridge._table._VarTable.step"></a>

#### step

```python
def step(ask: AskReader, reason: Optional[str]) -> bool
```

Run one menu round; return True when the table is accepted.

<a id="wizard_ui_bridge._table._VarTable._menu_help"></a>

#### \_menu\_help

```python
def _menu_help() -> str
```

Return the explanation of the menu actions and the table help.

<a id="wizard_ui_bridge._table._VarTable._accept"></a>

#### \_accept

```python
def _accept() -> bool
```

Accept the table when its row count is within the bounds.

<a id="wizard_ui_bridge._table._VarTable._add"></a>

#### \_add

```python
def _add(ask: AskReader) -> None
```

Append one editable row, up to max_rows, then edit it.

<a id="wizard_ui_bridge._table._VarTable._delete"></a>

#### \_delete

```python
def _delete(arg: str) -> None
```

Delete the row named by a one-based number, down to min_rows.

<a id="wizard_ui_bridge._table._VarTable._edit"></a>

#### \_edit

```python
def _edit(ask: AskReader, token: str) -> None
```

Edit the row named by a one-based number.

<a id="wizard_ui_bridge._table._VarTable._edit_row"></a>

#### \_edit\_row

```python
def _edit_row(ask: AskReader, row: int) -> None
```

Walk the editable cells of one row, back to the menu on back.

<a id="wizard_ui_bridge._table._VarTable._fill_one"></a>

#### \_fill\_one

```python
def _fill_one(ask: AskReader, row: int, col: int) -> None
```

Ask one editable cell and store its accepted value.

<a id="wizard_ui_bridge._table._VarTable._editable"></a>

#### \_editable

```python
def _editable(row: int, col: int) -> bool
```

Return whether one cell can be edited in the console table.

<a id="wizard_ui_bridge._table._run_variable_table"></a>

#### \_run\_variable\_table

```python
def _run_variable_table(ask: AskReader, show: Callable[[str], None],
                        columns: Sequence[TableColumn],
                        cells: list[list[TableCell]], question: str,
                        re_ask_reason: Optional[str],
                        partial_check: Optional[PartialCheck], min_rows: int,
                        max_rows: int,
                        help_text: Optional[str]) -> list[list[Optional[str]]]
```

Edit a variable-row table through the console row-menu interface.

<a id="wizard_ui_bridge._table._overview_lines"></a>

#### \_overview\_lines

```python
def _overview_lines(columns: Sequence[TableColumn],
                    table: list[list[Optional[str]]]) -> list[str]
```

Return the numbered overview lines for a variable-row table.

<a id="wizard_ui_bridge._table._column_widths"></a>

#### \_column\_widths

```python
def _column_widths(lines: list[list[str]]) -> list[int]
```

Return the widest text in each column across the given lines.

<a id="wizard_ui_bridge._table._overview_line"></a>

#### \_overview\_line

```python
def _overview_line(cells: list[str], widths: list[int]) -> str
```

Return one space-padded overview line, without trailing spaces.

<a id="wizard_ui_bridge._table._cell_text"></a>

#### \_cell\_text

```python
def _cell_text(value: Optional[str]) -> str
```

Return the overview display text for one cell value.

<a id="wizard_ui_bridge._form_prefill"></a>

# wizard\_ui\_bridge.\_form\_prefill

Apply a partial validator's prefills to a Textual form's widgets.

The Textual form bridge asks the partial validator after every change and
then places the prefill values it returns into the matching field widgets,
exactly as if the user had typed them. This module holds that write-back,
kept apart from the large Textual bridge module.

<a id="wizard_ui_bridge._form_prefill.apply_prefills"></a>

#### apply\_prefills

```python
def apply_prefills(form: DOMNode, fields: Sequence[AskField], changed: int,
                   prefill_values: PrefillValues) -> None
```

Write each valid prefill into its row's widget in form.

A disabled row is written too, so the value shows greyed and takes
effect if the row is later enabled. Writing a value equal to the one
already there is a no-op, so a stable validator does not loop.

<a id="wizard_ui_bridge._form_prefill._set_field"></a>

#### \_set\_field

```python
def _set_field(form: DOMNode, field: AskField, index: int,
               value: PrefillValueType) -> None
```

Write a prefill value into one field's widget, by field type.

Setting the widget value raises the framework's change event, so the
answer, the disabled set and any own-field error refresh as if the
user had typed it, exactly like the directory picker write-back.

<a id="wizard_ui_bridge._form_prefill._set_multi"></a>

#### \_set\_multi

```python
def _set_multi(form: DOMNode, index: int, field: AskMultiChoiceField,
               members: Sequence[str]) -> None
```

Select exactly the given members in a multi-choice widget.

<a id="wizard_ui_bridge._calendar"></a>

# wizard\_ui\_bridge.\_calendar

A modal month calendar for the Textual date and date-time fields.

A date field, and the date part of a date-time field, are shown in the
Textual form as a text input paired with a Pick button. Pressing that
button, or typing the '?' token into the input, opens this modal
calendar. The user steps between months and years, moves between the
days of the shown month with the arrow keys, and clicks a day to return
it; Escape or the Cancel button returns nothing so the input is left
unchanged. Days outside a field's inclusive bounds are shown disabled,
so the calendar only offers acceptable dates.

<a id="wizard_ui_bridge._calendar._shift"></a>

#### \_shift

```python
def _shift(year: int, month: int, action: str) -> tuple[int, int]
```

Return the year and month reached by one navigation action.

<a id="wizard_ui_bridge._calendar._CalendarScreen"></a>

## \_CalendarScreen Objects

```python
class _CalendarScreen(ModalScreen[Optional[date]])
```

Modal month calendar returning the date the user clicks.

The screen opens on a seed month and offers day buttons for that
month, greying the days outside the inclusive minimum and maximum.
Month and year buttons move the view, a day button returns its date,
and Escape or Cancel returns None so the field keeps its value. The
seed day is focused on opening and the arrow keys move the focus
between the enabled days of the shown month, so a day can be picked
without the mouse.

<a id="wizard_ui_bridge._calendar._CalendarScreen.__init__"></a>

#### \_\_init\_\_

```python
def __init__(seed: date, minimum: Optional[date],
             maximum: Optional[date]) -> None
```

Store the seed month, its day and the inclusive day bounds.

<a id="wizard_ui_bridge._calendar._CalendarScreen.compose"></a>

#### compose

```python
def compose() -> ComposeResult
```

Lay out the title, the navigation, the day grid and footer.

<a id="wizard_ui_bridge._calendar._CalendarScreen.on_mount"></a>

#### on\_mount

```python
async def on_mount() -> None
```

Fill the day grid and focus the seed month's starting day.

<a id="wizard_ui_bridge._calendar._CalendarScreen._show_month"></a>

#### \_show\_month

```python
async def _show_month() -> None
```

Show the current month's title and rebuild the day grid.

The old day widgets are removed before the new ones are mounted,
so navigating to another month never leaves two cells sharing a
day id.

<a id="wizard_ui_bridge._calendar._CalendarScreen._grid_widgets"></a>

#### \_grid\_widgets

```python
def _grid_widgets() -> Iterator[Widget]
```

Yield the weekday headers and then one widget per day cell.

<a id="wizard_ui_bridge._calendar._CalendarScreen._day_widget"></a>

#### \_day\_widget

```python
def _day_widget(day: int) -> Widget
```

Return a blank cell for a padding day, else a day button.

<a id="wizard_ui_bridge._calendar._CalendarScreen._day_disabled"></a>

#### \_day\_disabled

```python
def _day_disabled(day: int) -> bool
```

Return whether a day of the shown month is out of bounds.

<a id="wizard_ui_bridge._calendar._CalendarScreen._pressed"></a>

#### \_pressed

```python
@on(Button.Pressed)
async def _pressed(event: Button.Pressed) -> None
```

Route a button press to navigation, a day, or cancel.

<a id="wizard_ui_bridge._calendar._CalendarScreen.action_cancel"></a>

#### action\_cancel

```python
def action_cancel() -> None
```

Close the calendar without returning a date.

<a id="wizard_ui_bridge._calendar._CalendarScreen.action_step_day"></a>

#### action\_step\_day

```python
def action_step_day(delta: int) -> None
```

Move focus by delta days within the shown month, if possible.

The arrow keys step one day left or right and one week up or
down. A step off the month, or onto a disabled day, is ignored,
so the focus stays on a selectable day of the shown month.

<a id="wizard_ui_bridge._calendar._CalendarScreen._focus_start_day"></a>

#### \_focus\_start\_day

```python
def _focus_start_day() -> None
```

Focus the seed day, or the nearest enabled day of the month.

<a id="wizard_ui_bridge._calendar._CalendarScreen._focused_day"></a>

#### \_focused\_day

```python
def _focused_day() -> Optional[int]
```

Return the day number of the focused day button, or None.

<a id="wizard_ui_bridge._calendar._CalendarScreen._focus_day"></a>

#### \_focus\_day

```python
def _focus_day(day: int) -> None
```

Focus a day's button when it is in the month and enabled.

<a id="wizard_ui_bridge._calendar._CalendarScreen._nearest_enabled"></a>

#### \_nearest\_enabled

```python
def _nearest_enabled(target: int) -> Optional[int]
```

Return the enabled day nearest target, or None when none are.

<a id="wizard_ui_bridge._textual_nav"></a>

# wizard\_ui\_bridge.\_textual\_nav

The base screen of the Textual bridge, which turns keys into navigation.

Every screen of the Textual bridge derives from _NavApp, so the keys
that ask to go back or cancel the current level work the same way on
every screen.

<a id="wizard_ui_bridge._textual_nav._NavApp"></a>

## \_NavApp Objects

```python
class _NavApp(App[_T])
```

Base screen translating navigation keys into wizard requests.

A subclass lays out one question. ctrl+b records a request to go
back and ctrl+o a request to cancel the current level; the mnemonic
for ctrl+o is "out one level". Both exit the screen with no value so
the bridge can raise the matching request. The built-in ctrl+q quit
also exits with no value, which the bridge treats as an abort. These
keys avoid the editing shortcuts that the text input widget binds,
so they work on every screen.

<a id="wizard_ui_bridge._textual_nav._NavApp.__init__"></a>

#### \_\_init\_\_

```python
def __init__() -> None
```

Initialize with no pending navigation request.

<a id="wizard_ui_bridge._textual_nav._NavApp.action_nav_back"></a>

#### action\_nav\_back

```python
def action_nav_back() -> None
```

Record a request to return to the previous question.

The name avoids App.action_back, the built-in screen-history
action, so this records a wizard back request instead.

<a id="wizard_ui_bridge._textual_nav._NavApp.action_nav_cancel"></a>

#### action\_nav\_cancel

```python
def action_nav_cancel() -> None
```

Record a request to cancel the current level.

<a id="wizard_ui_bridge._matrix_console"></a>

# wizard\_ui\_bridge.\_matrix\_console

Ask a matrix form one cell at a time, as a console does.

The base WizardUiBridge.ask_matrix_form() cannot show a grid, so it asks
each input cell in turn with the typed ask methods of the bridge, as the
MatrixConsoleQuestion of the request directs. The cells are walked line
by line: a line is a row in row order and a column in column order, and
an item is one cell of a line.

The walk is a queue of steps: a cell, a line that turns into its cells
when it is reached (so a line asked after the width changed gets the new
width), and a resize menu. When the matrix may be resized, ask_choice()
offers a menu at two points:

- after the first line with input cells, when the number of items may
  change, so the user can set the width before the other lines are
  asked and then fill each line completely, and
- at the end, to append or delete the last line or item, or be done.

An appended line or item asks its new input cells at once, before the
menu is offered again; cells of lines still waiting in the queue are
asked with those lines. Asked for help, a menu explains its actions.
WizardBack steps back to the previously asked
cell that can still be asked, also from a menu, and propagates from the
first cell. The cells passed on the way back are walked again, so a cell
skipped as disabled is asked if it is enabled by then, as in the base
WizardUiBridge.ask_form().

A partial validator gets each answered cell, and the whole matrix after
a shape change; its message is shown when the matrix is not valid, its
disabled cells are skipped, and each prefill becomes the default of its
cell when that cell is asked. The message is advisory only: the wizard
checks the returned answers.

<a id="wizard_ui_bridge._matrix_console._Line"></a>

## \_Line Objects

```python
class _Line(NamedTuple)
```

A step asking each input cell of one line, as wide as it is then.

<a id="wizard_ui_bridge._matrix_console._Menu"></a>

## \_Menu Objects

```python
class _Menu(Enum)
```

A resize menu: after the first line with input cells, or at the end.

<a id="wizard_ui_bridge._matrix_console.ConsoleMatrix"></a>

## ConsoleMatrix Objects

```python
class ConsoleMatrix()
```

A matrix form asked one cell at a time through a bridge.

<a id="wizard_ui_bridge._matrix_console.ConsoleMatrix.__init__"></a>

#### \_\_init\_\_

```python
def __init__(bridge: 'WizardUiBridge', request: MatrixRequest) -> None
```

Build the cells of the default shape with their start answers.

<a id="wizard_ui_bridge._matrix_console.ConsoleMatrix.run"></a>

#### run

```python
def run() -> list[list[Optional[AnswerCell]]]
```

Ask the cells and menus and return the answers of the matrix.

**Raises**:

- `WizardBack` - The user stepped back from the first cell.
- `WizardCancelLevel` - The user cancelled the current level.
- `WizardAbort` - The user abandoned the whole wizard.

<a id="wizard_ui_bridge._matrix_console.ConsoleMatrix._first_steps"></a>

#### \_first\_steps

```python
def _first_steps() -> list[Union[CellPosition, _Line, _Menu]]
```

Return the lines to ask with the menus that resizing needs.

<a id="wizard_ui_bridge._matrix_console.ConsoleMatrix._run_step"></a>

#### \_run\_step

```python
def _run_step(step: Union[CellPosition, _Line, _Menu],
              todo: list[Union[CellPosition, _Line, _Menu]]) -> None
```

Run one step, putting any steps it leads to first in todo.

A cell that is not an enabled input cell is passed without asking.

<a id="wizard_ui_bridge._matrix_console.ConsoleMatrix._back"></a>

#### \_back

```python
def _back(passed: list[CellPosition]) -> list[CellPosition]
```

Return the passed cells from the last one that can be asked.

They are removed from passed, to be walked again from that cell.

**Raises**:

- `WizardBack` - No passed cell can be asked, so the wizard steps
  back instead.

<a id="wizard_ui_bridge._matrix_console.ConsoleMatrix._ask"></a>

#### \_ask

```python
def _ask(position: CellPosition) -> None
```

Ask one input cell, store its answer and run the validator.

<a id="wizard_ui_bridge._matrix_console.ConsoleMatrix._question"></a>

#### \_question

```python
def _question(position: CellPosition) -> str
```

Return the name of a cell that its question shows.

<a id="wizard_ui_bridge._matrix_console.ConsoleMatrix._menu"></a>

#### \_menu

```python
def _menu(
    menu: _Menu, todo: list[Union[CellPosition, _Line, _Menu]]
) -> list[Union[CellPosition, _Line, _Menu]]
```

Ask a resize menu, resize, and return the steps that follow.

An appended line is asked next, and an appended item in each line
not still waiting in todo, before the menu is offered again.

<a id="wizard_ui_bridge._matrix_console.ConsoleMatrix._label"></a>

#### \_label

```python
def _label(menu: _Menu, add_lines: int, add_items: int) -> str
```

Return the menu text of one resize action.

<a id="wizard_ui_bridge._matrix_console.ConsoleMatrix._menu_help"></a>

#### \_menu\_help

```python
def _menu_help(menu: _Menu) -> str
```

Return the help text that explains the actions of a menu.

<a id="wizard_ui_bridge._matrix_console.ConsoleMatrix._words"></a>

#### \_words

```python
def _words() -> tuple[str, str]
```

Return the words for a line and an item, such as row, column.

<a id="wizard_ui_bridge._matrix_console.ConsoleMatrix._fits"></a>

#### \_fits

```python
def _fits(add_lines: int, add_items: int) -> bool
```

Return whether a resize keeps the matrix within its bounds.

<a id="wizard_ui_bridge._matrix_console.ConsoleMatrix._resizable"></a>

#### \_resizable

```python
def _resizable() -> tuple[bool, bool]
```

Return whether the number of lines, and of items, may change.

<a id="wizard_ui_bridge._matrix_console.ConsoleMatrix._has_input"></a>

#### \_has\_input

```python
def _has_input(line: int) -> bool
```

Return whether a line of the current shape has an input cell.

<a id="wizard_ui_bridge._matrix_console.ConsoleMatrix._askable"></a>

#### \_askable

```python
def _askable(position: CellPosition) -> bool
```

Return whether a cell is an enabled input cell of the shape.

<a id="wizard_ui_bridge._matrix_console.ConsoleMatrix._validate"></a>

#### \_validate

```python
def _validate(changed: Optional[CellPosition], quiet: bool = False) -> None
```

Run the partial validator, if any, and keep what it returns.

Its message is shown when the matrix is not valid, unless quiet.

<a id="wizard_ui_bridge._matrix_console.ConsoleMatrix._reshape"></a>

#### \_reshape

```python
def _reshape(shape: MatrixDimension) -> None
```

Change the matrix to shape, deleting or appending at the end.

A remaining cell keeps its answer. A new cell comes fresh from the
specification with its start answer, and a prefill waiting for a
deleted cell is dropped.

<a id="wizard_ui_bridge._matrix_console.ConsoleMatrix._kept_cell"></a>

#### \_kept\_cell

```python
def _kept_cell(position: CellPosition, old: MatrixDimension) -> AskCell
```

Return the cell at a position of the old shape, else a new one.

<a id="wizard_ui_bridge._matrix_console.ConsoleMatrix._kept_answer"></a>

#### \_kept\_answer

```python
def _kept_answer(position: CellPosition,
                 old: MatrixDimension) -> Optional[AnswerCell]
```

Return the answer at a position of the old shape, else a new one.

A new answer is the start answer of the cell in self._cells, which
must already have the new shape.

<a id="wizard_ui_bridge._matrix_console.ConsoleMatrix._span"></a>

#### \_span

```python
def _span(shape: MatrixDimension) -> tuple[int, int]
```

Return a shape as (lines, items) in the order cells are asked.

<a id="wizard_ui_bridge._matrix_console.ConsoleMatrix._dimension"></a>

#### \_dimension

```python
def _dimension(lines: int, items: int) -> MatrixDimension
```

Return the shape of a number of lines and items.

<a id="wizard_ui_bridge._matrix_console.ConsoleMatrix._position"></a>

#### \_position

```python
def _position(line: int, item: int) -> CellPosition
```

Return the position of an item of a line.

<a id="wizard_ui_bridge._matrix_console._inside"></a>

#### \_inside

```python
def _inside(position: CellPosition, shape: MatrixDimension) -> bool
```

Return whether a position lies within a shape.

<a id="wizard_ui_bridge._matrix_console._start_answer"></a>

#### \_start\_answer

```python
def _start_answer(cell: AskCell) -> Optional[AnswerCell]
```

Return the answer of a cell before it is asked; None for a label.

<a id="wizard_ui_bridge._fake"></a>

# wizard\_ui\_bridge.\_fake

Fake unsupported typed form fields as text fields.

A wizard may use the float, date, time, date-time or duration form
fields with a bridge that overrides ask_form() but was written before
those field types existed. Such a bridge reports through
supports_form_field() that it cannot show them. This module lets the
wizard still use one form: each unsupported field is shown as a text
field, a wrapping validator parses the text and guides the user to a
convertible value, and the text answers are converted back to the
requested typed answers.

The whole form is shown once by the bridge's own ask_form(), so the user
still sees and edits every field together. The parsing, formatting and
range messages are shared with the console and Textual forms through the
wizard_ui_bridge._parse module, so the faked fields accept exactly the
same text.

<a id="wizard_ui_bridge._fake._FakeableBridge"></a>

## \_FakeableBridge Objects

```python
class _FakeableBridge(Protocol)
```

The bridge methods ask_form_faking() relies on.

<a id="wizard_ui_bridge._fake._FakeableBridge.supports_form_field"></a>

#### supports\_form\_field

```python
def supports_form_field(field: AskField) -> bool
```

Return whether the bridge can show the field directly.

<a id="wizard_ui_bridge._fake._FakeableBridge.ask_form"></a>

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

Show the whole form and return one answer per field.

<a id="wizard_ui_bridge._fake.ask_form_faking"></a>

#### ask\_form\_faking

```python
def ask_form_faking(
        bridge: _FakeableBridge, long_question: str, ask_fields: AskFields, *,
        re_ask_reason: Optional[str],
        partial_validator: Optional[PartialFormValidator]) -> AnswerFields
```

Show a form, faking the fields the bridge cannot show as text.

Raises RuntimeError when a field is unsupported and cannot be faked.

<a id="wizard_ui_bridge._fake._plan"></a>

#### \_plan

```python
def _plan(bridge: _FakeableBridge, field: AskField) -> tuple[AskField, bool]
```

Return the field to show and whether it is a faked text field.

<a id="wizard_ui_bridge._fake._real_answer"></a>

#### \_real\_answer

```python
def _real_answer(field: AskField, is_fake: bool,
                 answer: AnswerField) -> AnswerField
```

Return the answer of a field, converting a faked text answer.

<a id="wizard_ui_bridge._fake._wrap_validator"></a>

#### \_wrap\_validator

```python
def _wrap_validator(
        fields: list[AskField], is_fake: list[bool],
        caller: Optional[PartialFormValidator]) -> PartialFormValidator
```

Return a validator over faked answers wrapping the caller's one.

It converts the faked text answers back to typed answers for the
caller, converts the caller's typed prefills to text for the faked
rows, and blocks submit while any enabled faked field holds text that
cannot be converted.

<a id="wizard_ui_bridge._fake._convert_prefills"></a>

#### \_convert\_prefills

```python
def _convert_prefills(is_fake: list[bool],
                      prefills: PrefillValues) -> PrefillValues
```

Return prefills with faked rows' typed values turned into text.

<a id="wizard_ui_bridge._fake._fake_guidance"></a>

#### \_fake\_guidance

```python
def _fake_guidance(fields: list[AskField], is_fake: list[bool],
                   answers: AnswerFields, disabled: set[int]) -> Optional[str]
```

Return the first enabled faked field's parse error, or None.

<a id="wizard_ui_bridge._table_matrix"></a>

# wizard\_ui\_bridge.\_table\_matrix

Ask a table question as a matrix form.

The base WizardUiBridge.ask_table() describes the table as a matrix form
with TableMatrix, asks it with ask_matrix_form() and turns the answers
back into table cells. Row 0 of the matrix is a header of bold labels,
and each table row is the matrix row below it, so table row r is matrix
row r + 1. A read-only cell of a starting row is a label, and an editable
cell is a text cell, or a choice cell when it has choices. The last row
of the cell specification is bridge_helpers.new_row_template() with every
column editable, and the matrix repeats it for each row the user appends.

A TableCell separates the value an input starts with from what an empty
cell means, while an Ask*Cell uses its default for both. So a pre-filled
value is the default of its cell, and a nullable TableCell with a value
is asked as a cell that is not nullable.

<a id="wizard_ui_bridge._table_matrix.TableMatrix"></a>

## TableMatrix Objects

```python
class TableMatrix()
```

A table question described as the cells of a matrix form.

<a id="wizard_ui_bridge._table_matrix.TableMatrix.__init__"></a>

#### \_\_init\_\_

```python
def __init__(columns: Sequence[TableColumn],
             cells: Sequence[Sequence[TableCell]],
             partial_check: Optional[PartialCheck],
             help_text: Optional[str]) -> None
```

Build the matrix cells of the header, starting and new rows.

Each input cell gets help_text as its help text.

**Raises**:

- `ValueError` - A row of cells does not hold one cell per column.

<a id="wizard_ui_bridge._table_matrix.TableMatrix.request"></a>

#### request

```python
def request(question: str, min_rows: Optional[int],
            max_rows: Optional[int]) -> MatrixRequest
```

Return the matrix request of the table.

**Raises**:

- `ValueError` - A variable number of rows, with both min_rows and
  max_rows given, does not satisfy 0 <= min_rows <=
  number of starting rows <= max_rows.

<a id="wizard_ui_bridge._table_matrix.TableMatrix.values"></a>

#### values

```python
def values(answers: AnswerCells) -> list[list[Optional[str]]]
```

Return the table of cell values that matrix answers give.

<a id="wizard_ui_bridge._table_matrix.TableMatrix.cell_name"></a>

#### cell\_name

```python
def cell_name(_answers: AnswerCells, position: CellPosition) -> str
```

Return the name of a cell, such as 'city / Rename to'.

The texts of the read-only cells of the row, or 'Row 2' when it
has none, are followed by the header of the column.

<a id="wizard_ui_bridge._table_matrix.TableMatrix._dimensions"></a>

#### \_dimensions

```python
def _dimensions(min_rows: Optional[int],
                max_rows: Optional[int]) -> MatrixDimensions
```

Return the dimensions of the matrix, with its header row.

The rows are fixed to the starting rows unless both bounds are
given.

<a id="wizard_ui_bridge._table_matrix.TableMatrix._value"></a>

#### \_value

```python
def _value(row: int, column: int,
           answer: Optional[AnswerCell]) -> Optional[str]
```

Return the value of one table cell from its matrix answer.

Only a starting row has labels, and a label keeps the value of its
read-only TableCell.

<a id="wizard_ui_bridge._table_matrix.TableMatrix._validate"></a>

#### \_validate

```python
def _validate(answers: AnswerCells,
              changed: Optional[CellPosition]) -> PartMatrixValidationRes
```

Run the partial check of the table on the changed cell.

A partial check needs the changed cell, so a matrix with no
changed cell yet, or with a changed shape, counts as valid. It is
only used as validator when the table has a partial check.

<a id="wizard_ui_bridge._table_matrix._starting_row"></a>

#### \_starting\_row

```python
def _starting_row(columns: Sequence[TableColumn], row: Sequence[TableCell],
                  help_text: Optional[str]) -> list[AskCell]
```

Return the matrix cells of one starting row of the table.

<a id="wizard_ui_bridge._table_matrix._input_cell"></a>

#### \_input\_cell

```python
def _input_cell(cell: TableCell, help_text: Optional[str]) -> AskCell
```

Return the matrix input cell of one editable table cell.

A pre-filled value becomes the default, which an Ask*Cell does not
allow together with nullable, so the value wins over nullable.

<a id="wizard_ui_bridge._textual_widgets"></a>

# wizard\_ui\_bridge.\_textual\_widgets

Widget builders, id helpers and message helpers for Textual.

The Textual bridge builds one input widget per form field and per menu,
and it maps widget ids back to field indexes and table positions. These
pure builders and id helpers are kept apart from the screen classes so
the main bridge module stays small; they hold no screen state and only
turn field descriptions into widgets and widget ids into indexes.

A form and a table screen show every field at once but report validation
in one shared status line, so the message helpers here name the field or
the cell a message complains about; without that name the user cannot
tell which of the fields on the screen to correct.

The width hint of a field sizes its input with _apply_width(), once the
input is mounted.

<a id="wizard_ui_bridge._textual_widgets._header_widgets"></a>

#### \_header\_widgets

```python
def _header_widgets(messages: list[str], question: str) -> Iterator[Static]
```

Yield one static line per message and one for the question.

<a id="wizard_ui_bridge._textual_widgets._default_index"></a>

#### \_default\_index

```python
def _default_index(choices: Sequence[str],
                   default: Optional[str]) -> Optional[int]
```

Return the index of default, one of choices, or None for none.

<a id="wizard_ui_bridge._textual_widgets._preselected"></a>

#### \_preselected

```python
def _preselected(choices: Sequence[str],
                 default: Optional[Sequence[str]]) -> list[int]
```

Return the indexes of the default values within choices.

<a id="wizard_ui_bridge._textual_widgets._parse_cell_id"></a>

#### \_parse\_cell\_id

```python
def _parse_cell_id(widget_id: Optional[str]) -> Optional[tuple[int, int]]
```

Return the (row, column) encoded in an editable cell id.

<a id="wizard_ui_bridge._textual_widgets._make_select"></a>

#### \_make\_select

```python
def _make_select(cell: TableCell, widget_id: str) -> Select[str]
```

Return a drop-down for one cell, blank only when nullable.

<a id="wizard_ui_bridge._textual_widgets._choice_select"></a>

#### \_choice\_select

```python
def _choice_select(field: AskChoiceField, widget_id: str) -> Select[str]
```

Return a drop-down for a choice field, blank when no default.

<a id="wizard_ui_bridge._textual_widgets._multi_selection"></a>

#### \_multi\_selection

```python
def _multi_selection(field: AskMultiChoiceField,
                     widget_id: str) -> SelectionList[int]
```

Return a check-box list for a multi-choice field.

<a id="wizard_ui_bridge._textual_widgets._path_field_row"></a>

#### \_path\_field\_row

```python
def _path_field_row(value: str, index: int) -> Horizontal
```

Return a path input paired with a Browse button.

The input keeps the plain field id so the form reads and validates
it like any other field, while the button carries a browse class so
the form can open the directory picker for this row.

<a id="wizard_ui_bridge._textual_widgets._pick_field_row"></a>

#### \_pick\_field\_row

```python
def _pick_field_row(value: str, index: int) -> Horizontal
```

Return a text input paired with a calendar Pick button.

The input keeps the plain field id so the form reads and validates it
like any other text field, while the button carries a pick class so
the form can open the calendar for this row.

<a id="wizard_ui_bridge._textual_widgets._make_field_widget"></a>

#### \_make\_field\_widget

```python
def _make_field_widget(field: AskField, index: int) -> Widget
```

Return the input widget shown for one form field.

<a id="wizard_ui_bridge._textual_widgets._new_field_widget"></a>

#### \_new\_field\_widget

```python
def _new_field_widget(field: AskField, index: int) -> Optional[Widget]
```

Return the widget for a typed field, or None for the basic kinds.

A date or date-time field shows a text input with a Pick button that
opens the calendar; a float, time or duration field shows a plain
text input parsed on change. Each starts from its formatted default.

<a id="wizard_ui_bridge._textual_widgets._basic_field_widget"></a>

#### \_basic\_field\_widget

```python
def _basic_field_widget(field: AskField, index: int) -> Widget
```

Return the input widget for one of the original field kinds.

<a id="wizard_ui_bridge._textual_widgets._apply_width"></a>

#### \_apply\_width

```python
def _apply_width(widget: Widget, width: Optional[int]) -> None
```

Size a field input to a width hint in characters, if one is given.

The hint is the width of the text part, so the border and padding
of the input are added. A check box has no text part and keeps its
size.

<a id="wizard_ui_bridge._textual_widgets._id_index"></a>

#### \_id\_index

```python
def _id_index(widget_id: Optional[str], prefix: str) -> Optional[int]
```

Return the integer index following prefix in a widget id.

<a id="wizard_ui_bridge._textual_widgets._field_index"></a>

#### \_field\_index

```python
def _field_index(widget_id: Optional[str]) -> Optional[int]
```

Return the field index encoded in a field widget id.

<a id="wizard_ui_bridge._textual_widgets._browse_index"></a>

#### \_browse\_index

```python
def _browse_index(widget_id: Optional[str]) -> Optional[int]
```

Return the field index encoded in a browse button id.

<a id="wizard_ui_bridge._textual_widgets._pick_index"></a>

#### \_pick\_index

```python
def _pick_index(widget_id: Optional[str]) -> Optional[int]
```

Return the field index encoded in a calendar Pick button id.

<a id="wizard_ui_bridge._textual_widgets._multi_error"></a>

#### \_multi\_error

```python
def _multi_error(count: int, field: AskMultiChoiceField) -> Optional[str]
```

Return the multi-choice count error, or None when acceptable.

<a id="wizard_ui_bridge._textual_widgets._field_message"></a>

#### \_field\_message

```python
def _field_message(field: AskField, message: str) -> str
```

Return message named for the form field it complains about.

<a id="wizard_ui_bridge._textual_widgets._cell_message"></a>

#### \_cell\_message

```python
def _cell_message(header: str, row: int, message: str) -> str
```

Return message named for the table cell it complains about.

The 0-based row index is shown as a 1-based row number, so it counts
the rows the way the user sees them on the screen.

<a id="wizard_ui_bridge._textual_widgets._date_of"></a>

#### \_date\_of

```python
def _date_of(value: Optional[date]) -> Optional[date]
```

Return the date part of a date or datetime, or None.

<a id="wizard_ui_bridge._textual_widgets._calendar_setup"></a>

#### \_calendar\_setup

```python
def _calendar_setup(field: AskField,
                    text: str) -> tuple[date, Optional[date], Optional[date]]
```

Return the calendar seed date and its inclusive day bounds.

A date-time field's bounds are its date parts, so the calendar offers
the acceptable days and the field validates the exact date-time.

<a id="wizard_ui_bridge._textual_widgets._combined_text"></a>

#### \_combined\_text

```python
def _combined_text(field: AskField, picked: date, current: str) -> str
```

Return the input text for a picked date, keeping any typed time.

<a id="wizard_ui_bridge.bridge_helpers"></a>

# wizard\_ui\_bridge.bridge\_helpers

Helpers for implementing a WizardUiBridge.

The names without a leading underscore are the public helpers a bridge
implementation can use to interpret raw user answers the same way the
bundled bridges do, and the messages those bridges show when an answer
is not accepted.

<a id="wizard_ui_bridge.bridge_helpers._ERASE_TOKEN"></a>

#### \_ERASE\_TOKEN

empties an editable cell in a one-cell-at-a-time table

<a id="wizard_ui_bridge.bridge_helpers.NO_CHOICE"></a>

#### NO\_CHOICE

the entry that selects no choice when nullable

<a id="wizard_ui_bridge.bridge_helpers.check_text_args"></a>

#### check\_text\_args

```python
def check_text_args(default: Optional[str],
                    sensitive: bool,
                    nullable: bool = False) -> None
```

Raise ValueError when text-question arguments are inconsistent.

A default is allowed neither for sensitive input nor together with
nullable, see arg_types.check_nullable.

<a id="wizard_ui_bridge.bridge_helpers.question_with_default"></a>

#### question\_with\_default

```python
def question_with_default(question: str, default: Optional[str]) -> str
```

Return question with a bracketed default when one is given.

<a id="wizard_ui_bridge.bridge_helpers.text_answer"></a>

#### text\_answer

```python
def text_answer(text: str, nullable: bool,
                default: Optional[str]) -> Optional[str]
```

Return the public text answer for raw text from a bridge.

<a id="wizard_ui_bridge.bridge_helpers.path_answer"></a>

#### path\_answer

```python
def path_answer(
        text: Optional[str],
        options: PathAskOptions) -> tuple[bool, Optional[Path], Optional[str]]
```

Return whether a path answer is final, its value, and retry reason.

<a id="wizard_ui_bridge.bridge_helpers._path_error"></a>

#### \_path\_error

```python
def _path_error(path: Path, kind: WizardPathKind) -> Optional[str]
```

Return the validation error for path, or None when accepted.

<a id="wizard_ui_bridge.bridge_helpers._path_exists"></a>

#### \_path\_exists

```python
def _path_exists(path: Path) -> tuple[bool, Optional[str]]
```

Return whether path exists, or an error for an unusable path.

<a id="wizard_ui_bridge.bridge_helpers._path_must_exist"></a>

#### \_path\_must\_exist

```python
def _path_must_exist(kind: WizardPathKind) -> bool
```

Return whether kind requires an existing path.

<a id="wizard_ui_bridge.bridge_helpers._path_must_not_exist"></a>

#### \_path\_must\_not\_exist

```python
def _path_must_not_exist(kind: WizardPathKind) -> bool
```

Return whether kind requires a path that does not exist.

<a id="wizard_ui_bridge.bridge_helpers._path_must_be_file"></a>

#### \_path\_must\_be\_file

```python
def _path_must_be_file(kind: WizardPathKind) -> bool
```

Return whether kind rejects existing directories.

<a id="wizard_ui_bridge.bridge_helpers._path_must_be_dir"></a>

#### \_path\_must\_be\_dir

```python
def _path_must_be_dir(kind: WizardPathKind) -> bool
```

Return whether kind rejects existing files.

<a id="wizard_ui_bridge.bridge_helpers._interpret_yes_no"></a>

#### \_interpret\_yes\_no

```python
def _interpret_yes_no(answer: str | int, default: bool) -> Optional[bool]
```

Map a bridge answer to a yes/no boolean, or None to re-ask.

<a id="wizard_ui_bridge.bridge_helpers._yes_no_from_index"></a>

#### \_yes\_no\_from\_index

```python
def _yes_no_from_index(index: int) -> Optional[bool]
```

Map a 0-based ('yes', 'no') index to a boolean, or None.

<a id="wizard_ui_bridge.bridge_helpers._yes_no_from_text"></a>

#### \_yes\_no\_from\_text

```python
def _yes_no_from_text(text: str) -> Optional[bool]
```

Map yes/no free text to a boolean, or None when unrecognised.

<a id="wizard_ui_bridge.bridge_helpers.ask_yes_no"></a>

#### ask\_yes\_no

```python
def ask_yes_no(reader: Callable[[Optional[str]], str | int], default: bool,
               re_ask_reason: Optional[str]) -> bool
```

Re-ask through reader until a yes/no answer is understood.

<a id="wizard_ui_bridge.bridge_helpers.run_table"></a>

#### run\_table

```python
def run_table(ask: AskReader,
              show: Callable[[str], None],
              columns: Sequence[TableColumn],
              cells: list[list[TableCell]],
              question: str,
              re_ask_reason: Optional[str],
              partial_check: Optional[PartialCheck],
              help_text: Optional[str] = None) -> list[list[Optional[str]]]
```

Show one table question and fill its editable cells via ask.

The read-only cells stay fixed and only the editable cells are asked,
one at a time, through the ask reader, which gets help_text to show
when the user asks for help. This is the shared core of a fixed-row
table in any bridge that asks one question at a time.

<a id="wizard_ui_bridge.bridge_helpers._fill_table"></a>

#### \_fill\_table

```python
def _fill_table(ask: AskReader, columns: Sequence[TableColumn],
                cells: list[list[TableCell]], table: list[list[Optional[str]]],
                partial_check: Optional[PartialCheck],
                help_text: Optional[str]) -> None
```

Fill the editable cells, stepping back one cell on WizardBack.

WizardBack from the first editable cell has no earlier cell to
return to, so it propagates and the wizard steps to the previous
question. Cells already filled stay in the table while the user
moves between cells.

<a id="wizard_ui_bridge.bridge_helpers.fill_cell"></a>

#### fill\_cell

```python
def fill_cell(ask: AskReader,
              columns: Sequence[TableColumn],
              row: list[TableCell],
              col: int,
              current: Optional[str],
              check: Callable[[Optional[str]], Optional[str]],
              help_text: Optional[str] = None) -> Optional[str]
```

Ask one editable cell until its value is accepted.

**Arguments**:

- `ask` - The ask reader used to read the cell value.
- `columns` - The table columns, used to build the prompt.
- `row` - The cells of the row being filled.
- `col` - The index of the cell being filled.
- `current` - The cell's current value, kept when the user presses
  enter and shown in the prompt.
- `check` - Records a candidate in the table and returns an error
  message, or None when the candidate is accepted.
- `help_text` - The help text the ask reader shows when the user asks
  for help, or None when there is no help.
  

**Returns**:

  The accepted cell value, or None for an empty nullable cell.

**Raises**:

- `WizardBack` - The user asked to return to the previous cell.
- `WizardCancelLevel` - The user cancelled the current level.
- `WizardAbort` - The user abandoned the whole wizard.

<a id="wizard_ui_bridge.bridge_helpers._cell_prompt"></a>

#### \_cell\_prompt

```python
def _cell_prompt(columns: Sequence[TableColumn], row: list[TableCell],
                 col_index: int, current: Optional[str]) -> str
```

Return the console prompt for one editable cell.

<a id="wizard_ui_bridge.bridge_helpers.cell_checker"></a>

#### cell\_checker

```python
def cell_checker(
    table: list[list[Optional[str]]], position: tuple[int, int],
    partial_check: Optional[PartialCheck]
) -> Callable[[Optional[str]], Optional[str]]
```

Return a per-cell check that records a candidate and validates it.

<a id="wizard_ui_bridge.bridge_helpers._cell_value"></a>

#### \_cell\_value

```python
def _cell_value(answer: str | int, cell: TableCell,
                current: Optional[str]) -> tuple[Optional[str], Optional[str]]
```

Map a bridge answer to a rejection reason and a cell value.

The reason is None when the value can be used, and otherwise the
message to show the user before asking the cell again. A bool answer
is not a menu index and has no place in a table cell, so it is
rejected rather than read as the index bool inherits from int.

<a id="wizard_ui_bridge.bridge_helpers._kept_value"></a>

#### \_kept\_value

```python
def _kept_value(cell: TableCell,
                current: Optional[str]) -> tuple[Optional[str], Optional[str]]
```

Map keeping the current value to a reason and a cell value.

Keeping a cell that is already empty leaves it empty, which is the
same outcome as erasing it, so a cell that may not be left empty is
not emptied just because the user kept it.

<a id="wizard_ui_bridge.bridge_helpers._erased_value"></a>

#### \_erased\_value

```python
def _erased_value(cell: TableCell) -> tuple[Optional[str], Optional[str]]
```

Map an erase request to a reason and a cell value.

<a id="wizard_ui_bridge.bridge_helpers._indexed_value"></a>

#### \_indexed\_value

```python
def _indexed_value(index: int,
                   cell: TableCell) -> tuple[Optional[str], Optional[str]]
```

Map a 0-based choice index to a reason and a cell value.

<a id="wizard_ui_bridge.bridge_helpers._named_value"></a>

#### \_named\_value

```python
def _named_value(text: str,
                 cell: TableCell) -> tuple[Optional[str], Optional[str]]
```

Map answer text to a reason and a cell value.

A cell that offers choices accepts only those values, so its text is
matched against them by name the same way a single-choice question
matches a typed name.

<a id="wizard_ui_bridge.bridge_helpers._choice_result"></a>

#### \_choice\_result

```python
def _choice_result(
        match: Optional[str]) -> tuple[Optional[str], Optional[str]]
```

Return the cell result for a matched choice, or a rejection.

<a id="wizard_ui_bridge.bridge_helpers.int_text"></a>

#### int\_text

```python
def int_text(text: str) -> Optional[int]
```

Return an integer from text, or None when text is not an integer.

<a id="wizard_ui_bridge.bridge_helpers.out_of_range"></a>

#### out\_of\_range

```python
def out_of_range(value: int, min_value: Optional[int],
                 max_value: Optional[int]) -> bool
```

Return whether value lies outside the inclusive bounds.

<a id="wizard_ui_bridge.bridge_helpers.range_error"></a>

#### range\_error

```python
def range_error(min_value: Optional[int], max_value: Optional[int]) -> str
```

Return the message shown when an integer is out of range.

<a id="wizard_ui_bridge.bridge_helpers.ask_one"></a>

#### ask\_one

```python
def ask_one(reader: Callable[[Optional[str]], str | int],
            choices: Sequence[str],
            default: Optional[str],
            re_ask_reason: Optional[str],
            *,
            nullable: bool = False) -> Optional[str]
```

Re-ask through reader until one valid choice is selected.

When nullable an empty answer selects no choice, which is reported
as None. Otherwise an empty answer selects default, or is re-asked
when default is None.

**Raises**:

- `ValueError` - default is not one of choices, or is combined with
  nullable.

<a id="wizard_ui_bridge.bridge_helpers.offered_choices"></a>

#### offered\_choices

```python
def offered_choices(choices: Sequence[str],
                    nullable: bool) -> list[tuple[str, Optional[str]]]
```

Return the (label, answer) entries a single-choice list offers.

The entries are in display order. A nullable choice is led by the
entry (NO_CHOICE, None) that selects no choice, so a list control
offers it like any other entry and maps a picked row to its answer
by position, even if one of choices is itself named NO_CHOICE.

<a id="wizard_ui_bridge.bridge_helpers.ask_many"></a>

#### ask\_many

```python
def ask_many(reader: Callable[[Optional[str]], str | int],
             choices: Sequence[str], default: Optional[Sequence[str]],
             min_select: int, max_select: Optional[int],
             re_ask_reason: Optional[str], one_based: bool) -> list[str]
```

Re-ask through reader until a valid set of choices is selected.

**Raises**:

- `ValueError` - The arguments break a rule of check_multi_args().

<a id="wizard_ui_bridge.bridge_helpers._resolve_choice"></a>

#### \_resolve\_choice

```python
def _resolve_choice(answer: str | int, choices: Sequence[str],
                    default: Optional[str]) -> Optional[str]
```

Map a single-choice answer to a choice, or None to re-ask.

<a id="wizard_ui_bridge.bridge_helpers._resolve_multi"></a>

#### \_resolve\_multi

```python
def _resolve_multi(answer: str | int, choices: Sequence[str],
                   default: Optional[Sequence[str]], min_select: int,
                   max_select: Optional[int],
                   one_based: bool) -> tuple[Optional[list[str]], str]
```

Map a multi-choice answer to choices and an error to re-ask.

<a id="wizard_ui_bridge.bridge_helpers._multi_labels"></a>

#### \_multi\_labels

```python
def _multi_labels(answer: str | int, choices: Sequence[str],
                  default: Optional[Sequence[str]],
                  one_based: bool) -> Optional[list[str]]
```

Map a multi-choice answer to chosen labels, or None to re-ask.

<a id="wizard_ui_bridge.bridge_helpers._tokens_to_labels"></a>

#### \_tokens\_to\_labels

```python
def _tokens_to_labels(text: str, choices: Sequence[str],
                      one_based: bool) -> Optional[list[str]]
```

Map a comma-separated answer to labels, or None to re-ask.

<a id="wizard_ui_bridge.bridge_helpers.match_token"></a>

#### match\_token

```python
def match_token(token: str, choices: Sequence[str],
                one_based: bool) -> Optional[str]
```

Map one menu index or name to a choice, or None when no match.

<a id="wizard_ui_bridge.bridge_helpers._best_match"></a>

#### \_best\_match

```python
def _best_match(token: str, choices: Sequence[str]) -> Optional[str]
```

Return the unique best name match for token, or None.

<a id="wizard_ui_bridge.bridge_helpers._choice_at_index"></a>

#### \_choice\_at\_index

```python
def _choice_at_index(index: int, choices: Sequence[str]) -> Optional[str]
```

Return the choice at a 0-based index, or None when out of range.

<a id="wizard_ui_bridge.bridge_helpers.multi_count_error"></a>

#### multi\_count\_error

```python
def multi_count_error(min_select: int, max_select: Optional[int]) -> str
```

Return the message shown when the selected count is not allowed.

<a id="wizard_ui_bridge.bridge_helpers.multi_count_message"></a>

#### multi\_count\_message

```python
def multi_count_message(count: int, min_select: int,
                        max_select: Optional[int]) -> Optional[str]
```

Return why count is not an allowed selection size, or None.

Every bridge accepts the same selection counts and explains a
rejected count with the same message, so each of them asks here
instead of repeating the bounds check and the wording.

<a id="wizard_ui_bridge.bridge_helpers._uniform"></a>

#### \_uniform

```python
def _uniform(values: list[_V], default: _V) -> _V
```

Return the value shared by every entry, or the default.

<a id="wizard_ui_bridge.bridge_helpers.new_row_template"></a>

#### new\_row\_template

```python
def new_row_template(columns: Sequence[TableColumn],
                     cells: Sequence[Sequence[TableCell]]) -> list[TableCell]
```

Return the cell descriptors used for rows added to a table.

For each column, the new cell keeps the value, choices and nullable
flag shared by every template cell in that column. Where they differ
it falls back to no choices, not nullable and an empty value. The
empty value is an empty string for free text, but None, an empty
cell, when the column keeps its choices, as an empty string is not
one of them. A shared value is valid for shared choices, since every
template cell has been checked to hold one of its own choices.

<a id="wizard_ui_bridge.textual_bridge"></a>

# wizard\_ui\_bridge.textual\_bridge

Textual full-screen user interface bridge for the wizard.

This module provides the concrete Textual bridge used when the wizard
talks to a user through a real terminal. Each ask method runs a short
lived Textual application for one question and returns its result, which
keeps the one-question-at-a-time contract of WizardUiBridge while giving
the user a full-screen interface with selectable lists, check boxes and
editable tables.

Navigation keys exit a screen with no value and record which
WizardNavigation request to raise, so the bridge re-raises it after the
screen closes. Messages passed to show() and diagnostics written to
error_file() are buffered and rendered in the header of the next
screen, so nothing is written straight to the terminal where it would
corrupt the Textual display.

<a id="wizard_ui_bridge.textual_bridge._TextApp"></a>

## \_TextApp Objects

```python
class _TextApp(_NavApp[str])
```

Free-text screen returning the string the user typed.

<a id="wizard_ui_bridge.textual_bridge._TextApp.__init__"></a>

#### \_\_init\_\_

```python
def __init__(question: str,
             messages: list[str],
             value: str = '',
             password: bool = False) -> None
```

Store the prompt, buffered messages and input settings.

<a id="wizard_ui_bridge.textual_bridge._TextApp.compose"></a>

#### compose

```python
def compose() -> ComposeResult
```

Lay out the header, the input field and the footer.

<a id="wizard_ui_bridge.textual_bridge._TextApp._entered"></a>

#### \_entered

```python
@on(Input.Submitted)
def _entered(event: Input.Submitted) -> None
```

Exit returning the entered text, empty when nothing typed.

<a id="wizard_ui_bridge.textual_bridge._PathApp"></a>

## \_PathApp Objects

```python
class _PathApp(_PathPick, _NavApp[str])
```

Path screen with a filesystem tree and editable path input.

<a id="wizard_ui_bridge.textual_bridge._PathApp.__init__"></a>

#### \_\_init\_\_

```python
def __init__(question: str, messages: list[str], options: PathAskOptions,
             value: Optional[str]) -> None
```

Store prompt, path options and initial input state.

<a id="wizard_ui_bridge.textual_bridge._PathApp.compose"></a>

#### compose

```python
def compose() -> ComposeResult
```

Lay out the header, directory tree, path input and footer.

<a id="wizard_ui_bridge.textual_bridge._PathApp._submit_clicked"></a>

#### \_submit\_clicked

```python
@on(Button.Pressed, '#submit')
def _submit_clicked(_event: Button.Pressed) -> None
```

Submit the current input when the button is pressed.

<a id="wizard_ui_bridge.textual_bridge._PathApp._confirm"></a>

#### \_confirm

```python
def _confirm(value: str) -> None
```

Exit returning the confirmed path input.

<a id="wizard_ui_bridge.textual_bridge._ChoiceApp"></a>

## \_ChoiceApp Objects

```python
class _ChoiceApp(_NavApp[int])
```

Single-choice screen returning the chosen 0-based index.

<a id="wizard_ui_bridge.textual_bridge._ChoiceApp.__init__"></a>

#### \_\_init\_\_

```python
def __init__(question: str, choices: list[str], default_index: Optional[int],
             messages: list[str]) -> None
```

Store the prompt, choices and the index to highlight.

<a id="wizard_ui_bridge.textual_bridge._ChoiceApp.compose"></a>

#### compose

```python
def compose() -> ComposeResult
```

Lay out the header, the option list and the footer.

<a id="wizard_ui_bridge.textual_bridge._ChoiceApp.on_mount"></a>

#### on\_mount

```python
def on_mount() -> None
```

Highlight the default option when one is given.

<a id="wizard_ui_bridge.textual_bridge._ChoiceApp._picked"></a>

#### \_picked

```python
@on(OptionList.OptionSelected)
def _picked(event: OptionList.OptionSelected) -> None
```

Exit returning the index of the selected option.

<a id="wizard_ui_bridge.textual_bridge._MultiApp"></a>

## \_MultiApp Objects

```python
class _MultiApp(_NavApp[list[int]])
```

Multi-choice screen returning the chosen 0-based indexes.

<a id="wizard_ui_bridge.textual_bridge._MultiApp.__init__"></a>

#### \_\_init\_\_

```python
def __init__(question: str, choices: list[str], preselected: list[int],
             min_select: int, max_select: Optional[int],
             messages: list[str]) -> None
```

Store the prompt, choices, preselection and count limits.

<a id="wizard_ui_bridge.textual_bridge._MultiApp.compose"></a>

#### compose

```python
def compose() -> ComposeResult
```

Lay out the header, the check-box list, submit and footer.

<a id="wizard_ui_bridge.textual_bridge._MultiApp._selections"></a>

#### \_selections

```python
def _selections() -> list[Selection[int]]
```

Return one selection per choice, preselected as requested.

<a id="wizard_ui_bridge.textual_bridge._MultiApp._clicked"></a>

#### \_clicked

```python
@on(Button.Pressed)
def _clicked(_event: Button.Pressed) -> None
```

Treat a click on the submit button like the submit action.

<a id="wizard_ui_bridge.textual_bridge._MultiApp.action_submit"></a>

#### action\_submit

```python
def action_submit() -> None
```

Exit with the selection, or show why the count is wrong.

<a id="wizard_ui_bridge.textual_bridge._FormApp"></a>

## \_FormApp Objects

```python
class _FormApp(_NavApp[list[AnswerField]])
```

One screen showing every form field in a two-column grid.

The left column of each row is a label with the field's short
question and the right column an input widget chosen by the field
type: a text input, an integer input, a path input with a Browse
button, a check box, a drop-down, a check-box list, a text input with
a calendar Pick button for a date or date-time field, and a plain text
input for a float, time or duration field. A partial validator, when
given, runs after each change to show advisory feedback and to enable
or disable rows. On submit each enabled field is validated, so the
returned answers are complete and a choice with no default is always
answered.

A rejected field is named in the shared status line and its label is
shown in the error colour, so the user sees which of the fields on
the screen the message is about.

<a id="wizard_ui_bridge.textual_bridge._FormApp.__init__"></a>

#### \_\_init\_\_

```python
def __init__(question: str, fields: list[AskField], messages: list[str],
             validator: Optional[PartialFormValidator]) -> None
```

Store the prompt, fields, buffered messages and validator.

<a id="wizard_ui_bridge.textual_bridge._FormApp.compose"></a>

#### compose

```python
def compose() -> ComposeResult
```

Lay out the header, the field grid, submit and footer.

<a id="wizard_ui_bridge.textual_bridge._FormApp._field_widgets"></a>

#### \_field\_widgets

```python
def _field_widgets() -> Iterator[Widget]
```

Yield a label and an input widget for each field.

<a id="wizard_ui_bridge.textual_bridge._FormApp.on_mount"></a>

#### on\_mount

```python
def on_mount() -> None
```

Size the grid and inputs, focus the first field, not the scroll.

An input with a width hint keeps that width; the others fill
their grid column.

<a id="wizard_ui_bridge.textual_bridge._FormApp._input_changed"></a>

#### \_input\_changed

```python
@on(Input.Changed)
def _input_changed(event: Input.Changed) -> None
```

React to a text, integer or path field change.

<a id="wizard_ui_bridge.textual_bridge._FormApp._select_changed"></a>

#### \_select\_changed

```python
@on(Select.Changed)
def _select_changed(event: Select.Changed) -> None
```

React to a choice drop-down change.

<a id="wizard_ui_bridge.textual_bridge._FormApp._checkbox_changed"></a>

#### \_checkbox\_changed

```python
@on(Checkbox.Changed)
def _checkbox_changed(event: Checkbox.Changed) -> None
```

React to a yes/no check-box change.

<a id="wizard_ui_bridge.textual_bridge._FormApp._multi_changed"></a>

#### \_multi\_changed

```python
@on(SelectionList.SelectedChanged)
def _multi_changed(event: SelectionList.SelectedChanged[int]) -> None
```

React to a multi-choice selection change.

<a id="wizard_ui_bridge.textual_bridge._FormApp._changed"></a>

#### \_changed

```python
def _changed(widget_id: Optional[str]) -> None
```

Update the changed answer and refresh the shown feedback.

<a id="wizard_ui_bridge.textual_bridge._FormApp._maybe_open_calendar"></a>

#### \_maybe\_open\_calendar

```python
def _maybe_open_calendar(index: int) -> bool
```

Open the calendar when a date field holds the pick token.

Typing the '?' token into a date or date-time input is an
alternative to pressing the Pick button. The token is left in the
input until the calendar closes, when it is replaced by the picked
date or cleared on cancel.

<a id="wizard_ui_bridge.textual_bridge._FormApp._apply_validator"></a>

#### \_apply\_validator

```python
def _apply_validator(index: int) -> str
```

Apply the validator's disabled rows and prefills, return message.

<a id="wizard_ui_bridge.textual_bridge._FormApp._show_live"></a>

#### \_show\_live

```python
def _show_live(index: int, validator_message: str) -> None
```

Report the changed field's own error, else the validator's.

A field disabled by the validator is skipped, as on submit, so an
irrelevant field never blocks the user with its own error. This
gives a path, integer, choice or multi-choice field the same
immediate feedback while editing that the console bridge gives by
re-asking, instead of waiting for submit.

<a id="wizard_ui_bridge.textual_bridge._FormApp._apply_disabled"></a>

#### \_apply\_disabled

```python
def _apply_disabled(disable_row_idxs: tuple[int, ...]) -> None
```

Enable or disable each row to match the validator result.

<a id="wizard_ui_bridge.textual_bridge._FormApp._submit_clicked"></a>

#### \_submit\_clicked

```python
@on(Button.Pressed, '#submit')
def _submit_clicked(_event: Button.Pressed) -> None
```

Submit the form when the submit button is pressed.

<a id="wizard_ui_bridge.textual_bridge._FormApp._browse_clicked"></a>

#### \_browse\_clicked

```python
@on(Button.Pressed, '.browse')
def _browse_clicked(event: Button.Pressed) -> None
```

Open the directory picker for the clicked path field.

<a id="wizard_ui_bridge.textual_bridge._FormApp._pick_clicked"></a>

#### \_pick\_clicked

```python
@on(Button.Pressed, '.pick')
def _pick_clicked(event: Button.Pressed) -> None
```

Open the calendar for the clicked date field.

<a id="wizard_ui_bridge.textual_bridge._FormApp._open_picker"></a>

#### \_open\_picker

```python
def _open_picker(index: int) -> None
```

Push the picker seeded with the field's current text.

<a id="wizard_ui_bridge.textual_bridge._FormApp._open_calendar"></a>

#### \_open\_calendar

```python
def _open_calendar(index: int) -> None
```

Push the calendar seeded from the date field's current text.

<a id="wizard_ui_bridge.textual_bridge._FormApp._path_picked"></a>

#### \_path\_picked

```python
def _path_picked(index: int, result: Optional[str]) -> None
```

Fill the path input with the picked path, if any.

Setting the input value raises Input.Changed, so the answer and
the partial validator update as if the user had typed the path.

<a id="wizard_ui_bridge.textual_bridge._FormApp._date_picked"></a>

#### \_date\_picked

```python
def _date_picked(index: int, result: Optional[date]) -> None
```

Fill the date input with the picked date, if any.

A cancelled calendar clears a lingering pick token; a picked date
replaces the input, keeping any time part of a date-time field.
Setting the value raises Input.Changed, so the answer refreshes.

<a id="wizard_ui_bridge.textual_bridge._FormApp.action_submit"></a>

#### action\_submit

```python
def action_submit() -> None
```

Validate every enabled field and exit with the answers.

<a id="wizard_ui_bridge.textual_bridge._FormApp._validator_accepts"></a>

#### \_validator\_accepts

```python
def _validator_accepts() -> bool
```

Return whether the partial validator accepts the whole form.

<a id="wizard_ui_bridge.textual_bridge._FormApp._first_error"></a>

#### \_first\_error

```python
def _first_error() -> Optional[tuple[int, str]]
```

Return the first enabled field's index and error, or None.

<a id="wizard_ui_bridge.textual_bridge._FormApp._report"></a>

#### \_report

```python
def _report(index: Optional[int], message: str) -> None
```

Show a message, naming and marking the field it complains of.

A message given no field index, such as one from the partial
validator, is about the whole form: it is shown unchanged and no
field label is marked.

<a id="wizard_ui_bridge.textual_bridge._FormApp._set_status"></a>

#### \_set\_status

```python
def _set_status(message: str) -> None
```

Show a status message below the form.

<a id="wizard_ui_bridge.textual_bridge._FormApp._read_field"></a>

#### \_read\_field

```python
def _read_field(index: int) -> AnswerField
```

Return the current answer of one field read from its widget.

<a id="wizard_ui_bridge.textual_bridge._FormApp._read_new_field"></a>

#### \_read\_new\_field

```python
def _read_new_field(index: int, field: AskField) -> Optional[AnswerField]
```

Return a typed field's answer from its text input, else None.

<a id="wizard_ui_bridge.textual_bridge._FormApp._read_basic_field"></a>

#### \_read\_basic\_field

```python
def _read_basic_field(index: int, field: AskField) -> AnswerField
```

Return one original field kind's answer read from its widget.

<a id="wizard_ui_bridge.textual_bridge._FormApp._int_value"></a>

#### \_int\_value

```python
def _int_value(widget_id: str, field: AskIntField) -> Optional[int]
```

Return the integer value of a field, or None when unparsed.

<a id="wizard_ui_bridge.textual_bridge._FormApp._field_error"></a>

#### \_field\_error

```python
def _field_error(index: int, field: AskField) -> Optional[str]
```

Return one field's own validation error, or None when valid.

<a id="wizard_ui_bridge.textual_bridge._FormApp._int_error"></a>

#### \_int\_error

```python
def _int_error(widget_id: str, field: AskIntField) -> Optional[str]
```

Return the integer field's validation error, or None.

<a id="wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual"></a>

## WizardUiBridgeTextual Objects

```python
class WizardUiBridgeTextual(WizardUiBridge)
```

Bridge between the wizard and a Textual terminal interface.

Each ask method runs a short-lived Textual application for one
question and returns its result. Validation diagnostics written to
error_file() and messages passed to show() are buffered and rendered
in the header of the next question's screen, so nothing reaches the
terminal directly where it would corrupt the Textual display.

This bridge draws on the controlling terminal itself, so it takes no
streams. Use make_text_ui_bridge() to obtain this bridge when a
terminal is available and a console bridge otherwise.

The ask methods accept help_text but ignore it; ask_form() shows the
help text of each field as a tooltip instead.

<a id="wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.__init__"></a>

#### \_\_init\_\_

```python
def __init__() -> None
```

Start with an empty diagnostics buffer and message list.

<a id="wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.ask_text"></a>

#### ask\_text

```python
def ask_text(question: str,
             re_ask_reason: Optional[str] = None,
             nullable: bool = False,
             *,
             default: Optional[str] = None,
             sensitive: bool = False,
             help_text: Optional[str] = None) -> Optional[str]
```

Ask for free text; see WizardUiBridge.ask_text.

<a id="wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.ask_path"></a>

#### ask\_path

```python
def ask_path(question: str,
             re_ask_reason: Optional[str] = None,
             *,
             options: Optional[PathAskOptions] = None,
             help_text: Optional[str] = None) -> Optional[Path]
```

Ask for a path with a directory tree and editable path input.

<a id="wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.ask_yes_no"></a>

#### ask\_yes\_no

```python
def ask_yes_no(question: str,
               default: bool,
               re_ask_reason: Optional[str] = None,
               *,
               help_text: Optional[str] = None) -> bool
```

Ask a yes/no question; see WizardUiBridge.ask_yes_no.

<a id="wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.ask_choice"></a>

#### ask\_choice

```python
def ask_choice(question: str,
               *,
               choices: Sequence[str],
               default: Optional[str] = None,
               re_ask_reason: Optional[str] = None,
               nullable: bool = False,
               help_text: Optional[str] = None) -> Optional[str]
```

Ask the user to pick one choice; see ask_choice.

A nullable choice is offered with a leading, highlighted
'(none)' option that selects no choice.

<a id="wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.ask_multi"></a>

#### ask\_multi

```python
def ask_multi(question: str,
              *,
              choices: Sequence[str],
              default: Optional[Sequence[str]] = None,
              min_select: int = 0,
              max_select: Optional[int] = None,
              re_ask_reason: Optional[str] = None,
              help_text: Optional[str] = None) -> list[str]
```

Ask the user to pick several choices; see ask_multi.

<a id="wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.ask_table"></a>

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

Ask the user to fill a table; see WizardUiBridge.ask_table.

<a id="wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.ask_form"></a>

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

Ask the user to fill a whole form on one screen; see ask_form.

<a id="wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.supports_form_field"></a>

#### supports\_form\_field

```python
def supports_form_field(field: AskField) -> bool
```

Show every form field type; see WizardUiBridge.

The Textual form has a widget for each field type, including a
text input for float, time and duration fields and a text input
with a calendar Pick button for date and date-time fields. A
nullable choice field has a drop-down that can be left blank.

<a id="wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual._run"></a>

#### \_run

```python
def _run(app: _NavApp[_T]) -> _T
```

Run one screen and translate its outcome.

A recorded navigation request is re-raised. A screen that ends
with no value, such as the built-in quit, is treated as an
abort.

<a id="wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual._launch"></a>

#### \_launch

```python
def _launch(app: _NavApp[_T]) -> Optional[_T]
```

Run the app and return its result.

This is the only place that drives the terminal, so tests
override it to exercise the bridge without a real terminal.

<a id="wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual._collect"></a>

#### \_collect

```python
def _collect(re_ask_reason: Optional[str]) -> list[str]
```

Drain buffered messages and append any re-ask reason.

<a id="wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual._drain_messages"></a>

#### \_drain\_messages

```python
def _drain_messages() -> list[str]
```

Return and clear buffered show() and diagnostic lines.

<a id="wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.error_file"></a>

#### error\_file

```python
def error_file() -> StringIO
```

Return the in-memory stream shown on the next screen.

<a id="wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.show"></a>

#### show

```python
def show(message: str) -> None
```

Buffer a message for the next question's screen.

A message shown when no further question follows is not
displayed, because only a Textual screen renders it.

