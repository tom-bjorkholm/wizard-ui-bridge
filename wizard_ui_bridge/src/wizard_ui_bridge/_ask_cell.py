#! /usr/local/bin/python3
"""Ask one form field or matrix cell with the typed ask methods.

The base WizardUiBridge.ask_form() and ask_matrix_form() both ask one
question at a time. Every Ask*Field derives from its Ask*Cell, so a
single function asks either, given the question to show, through the
public typed ask methods of the bridge, which a derived bridge may
override. The help text of the cell is passed as help_text, so a console
user can ask to see it, and its start value as start_value.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import TYPE_CHECKING, Optional
from wizard_ui_bridge.matrix_cell_defs import AskCell, AskTextCell, \
    AskIntCell, AskPathCell, AskYesNoCell, AskChoiceCell, \
    AskMultiChoiceCell, AskFloatCell, AskDateCell, AskTimeCell, \
    AskDateTimeCell, AskDurationCell, PrefillValueType
from wizard_ui_bridge._help import help_kwargs
from wizard_ui_bridge._start import start_args
from wizard_ui_bridge._parse import ask_typed, parse_float, parse_date, \
    parse_time, parse_datetime, parse_duration, FLOAT_HINT, DATE_HINT, \
    TIME_HINT, DATETIME_HINT, DURATION_HINT
if TYPE_CHECKING:
    from wizard_ui_bridge.bridge import WizardUiBridge

_TYPED_CELLS = (AskFloatCell, AskDateCell, AskTimeCell, AskDateTimeCell,
                AskDurationCell)


def ask_cell_value(bridge: 'WizardUiBridge', question: str,
                   cell: AskCell) -> Optional[PrefillValueType]:
    """Ask the value of an input cell or form field and return it.

    The value has the answer type of the cell (see PrefillValueType), or
    is None for an empty nullable answer. A label cell has no value and
    must not be passed.
    """
    if isinstance(cell, _TYPED_CELLS):
        return _ask_typed_value(bridge, question, cell)
    return _ask_basic_value(bridge, question, cell)


def _ask_typed_value(bridge: 'WizardUiBridge', question: str,
                     cell: AskCell) -> Optional[PrefillValueType]:
    """Ask a float, date, time, date-time or duration through ask_text.

    The shared re-ask loop parses the entered text, checks the inclusive
    bounds and shows the format hint until the value is accepted.
    """
    ask = bridge.ask_text
    if isinstance(cell, AskFloatCell):
        return ask_typed(ask, question, cell, parse_float, FLOAT_HINT)
    if isinstance(cell, AskDateCell):
        return ask_typed(ask, question, cell, parse_date, DATE_HINT)
    if isinstance(cell, AskTimeCell):
        return ask_typed(ask, question, cell, parse_time, TIME_HINT)
    if isinstance(cell, AskDateTimeCell):
        return ask_typed(ask, question, cell, parse_datetime, DATETIME_HINT)
    assert isinstance(cell, AskDurationCell)
    return ask_typed(ask, question, cell, parse_duration, DURATION_HINT)


def _ask_basic_value(bridge: 'WizardUiBridge', question: str,
                     cell: AskCell) -> Optional[PrefillValueType]:
    """Ask one of the original cell kinds with its typed ask method."""
    if isinstance(cell, AskTextCell):
        return _ask_text_value(bridge, question, cell)
    if isinstance(cell, AskIntCell):
        return _ask_int_value(bridge, question, cell)
    if isinstance(cell, AskPathCell):
        return bridge.ask_path(question, options=cell.path_options,
                               **help_kwargs(bridge.ask_path, cell.help_text))
    if isinstance(cell, AskYesNoCell):
        return _ask_yes_no_value(bridge, question, cell)
    if isinstance(cell, AskChoiceCell):
        return _ask_choice_value(bridge, question, cell)
    assert isinstance(cell, AskMultiChoiceCell)
    return _ask_multi_value(bridge, question, cell)


def _ask_text_value(bridge: 'WizardUiBridge', question: str,
                    cell: AskTextCell) -> Optional[str]:
    """Ask a text cell with ask_text, starting with its start value."""
    default, nullable, start = start_args(bridge.ask_text, cell.start_value,
                                          cell.default, cell.nullable)
    return bridge.ask_text(question, nullable=nullable, default=default,
                           sensitive=cell.sensitive, **start,
                           **help_kwargs(bridge.ask_text, cell.help_text))


def _ask_int_value(bridge: 'WizardUiBridge', question: str,
                   cell: AskIntCell) -> Optional[int]:
    """Ask an integer cell with ask_int, starting with its start value."""
    default, nullable, start = start_args(bridge.ask_int, cell.start_value,
                                          cell.default, cell.nullable)
    return bridge.ask_int(question, nullable=nullable,
                          min_value=cell.min_value, max_value=cell.max_value,
                          default=default, **start,
                          **help_kwargs(bridge.ask_int, cell.help_text))


def _ask_yes_no_value(bridge: 'WizardUiBridge', question: str,
                      cell: AskYesNoCell) -> bool:
    """Ask a yes/no cell with ask_yes_no, starting with its start value."""
    default, _, start = start_args(bridge.ask_yes_no, cell.start_value,
                                   cell.default)
    return bridge.ask_yes_no(question, default, **start,
                             **help_kwargs(bridge.ask_yes_no, cell.help_text))


def _ask_choice_value(bridge: 'WizardUiBridge', question: str,
                      cell: AskChoiceCell) -> Optional[str]:
    """Ask a choice, passing nullable only when it is set.

    A bridge whose ask_choice() predates the nullable parameter still
    asks a non-nullable choice this way.
    """
    extra = help_kwargs(bridge.ask_choice, cell.help_text)
    default, nullable, start = start_args(bridge.ask_choice, cell.start_value,
                                          cell.default, cell.nullable)
    if nullable:
        return bridge.ask_choice(question, choices=cell.choices, nullable=True,
                                 **start, **extra)
    return bridge.ask_choice(question, choices=cell.choices, default=default,
                             **start, **extra)


def _ask_multi_value(bridge: 'WizardUiBridge', question: str,
                     cell: AskMultiChoiceCell) -> list[str]:
    """Ask a multi-choice cell with ask_multi, starting with its start."""
    default, _, start = start_args(bridge.ask_multi, cell.start_value,
                                   cell.default)
    return bridge.ask_multi(question, choices=cell.choices, default=default,
                            min_select=cell.min_select,
                            max_select=cell.max_select, **start,
                            **help_kwargs(bridge.ask_multi, cell.help_text))
