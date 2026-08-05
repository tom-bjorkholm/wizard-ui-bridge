#! /usr/local/bin/python3
"""A modal month calendar for the Tkinter date and date-time fields.

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
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import calendar
import tkinter as tk
from datetime import date
from functools import partial
from typing import Callable, Optional
from wizard_ui_bridge.form_defs import value_out_of_range

CALENDAR_TITLE = 'Pick a date'
WEEKDAYS = ('Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su')


def month_weeks(year: int, month: int) -> list[list[int]]:
    """Return the weeks of a month as day numbers, 0 for padding days."""
    return calendar.Calendar().monthdayscalendar(year, month)


def shift_month(year: int, month: int, action: str) -> tuple[int, int]:
    """Return the year and month reached by one navigation action.

    This mirrors wizard_ui_bridge._calendar, the private module behind
    the Textual bridge's own calendar screen; that module is not public
    API a sibling package may import, so this one keeps its own copy.
    """
    # pylint: disable=duplicate-code
    if action == 'prev_year':
        year -= 1
    elif action == 'next_year':
        year += 1
    elif action == 'prev_month':
        year, month = (year, month - 1) if month > 1 else (year - 1, 12)
    else:
        year, month = (year, month + 1) if month < 12 else (year + 1, 1)
    return (min(max(year, date.min.year), date.max.year), month)


def day_out_of_range(day: date, minimum: Optional[date],
                     maximum: Optional[date]) -> bool:
    """Return whether a day lies outside the inclusive date bounds."""
    return value_out_of_range(day, minimum, maximum)
# pylint: enable=duplicate-code


def _held_grab(widget: tk.Misc) -> bool:
    """Return whether widget's own window currently holds the app grab."""
    toplevel = widget.winfo_toplevel()
    return toplevel.grab_current() is not None  # type: ignore[no-untyped-call]


def _restore_grab(widget: Optional[tk.Misc]) -> None:
    """Give the modal grab back to the widget's window, if it survives."""
    if widget is None or not widget.winfo_exists():
        return
    try:
        widget.winfo_toplevel().grab_set()
    except tk.TclError:
        pass


# pylint: disable-next=too-few-public-methods,too-many-instance-attributes
class CalendarPicker:
    """A month calendar window returning the date the user clicks."""

    def __init__(self, parent: tk.Misc, seed: date, minimum: Optional[date],
                 maximum: Optional[date],
                 on_pick: Callable[[Optional[date]], None]) -> None:
        """Build the calendar window on the seed month and show it."""
        self._bounds = (minimum, maximum)
        self._on_pick = on_pick
        self._restore = _held_grab(parent)
        self._year = seed.year
        self._month = seed.month
        self._win = tk.Toplevel(parent)
        self._win.title(CALENDAR_TITLE)
        self._win.transient(parent.winfo_toplevel())
        self._win.protocol('WM_DELETE_WINDOW', self._cancel)
        self._win.bind('<Escape>', lambda _event: self._cancel())
        self._title = tk.Label(self._win)
        self._title.pack(pady=4)
        self._add_nav()
        self._grid = tk.Frame(self._win)
        self._grid.pack(padx=6, pady=6)
        tk.Button(self._win, text='Cancel', command=self._cancel).pack(pady=4)
        self._show_month()
        self._grab()

    def _grab(self) -> None:
        """Take the modal grab and focus, retrying until the window shows.

        Grabbing fails while the new window is not yet viewable, so it is
        retried on the wizard's event loop until it succeeds.
        """
        if not self._win.winfo_exists():
            return
        try:
            self._win.grab_set()
        except tk.TclError:
            self._win.after(50, self._grab)
            return
        self._win.focus_set()

    def _add_nav(self) -> None:
        """Add the previous and next month and year navigation buttons."""
        box = tk.Frame(self._win)
        box.pack()
        for text, action in (('<< year', 'prev_year'), ('< month',
                             'prev_month'), ('month >', 'next_month'),
                             ('year >>', 'next_year')):
            tk.Button(box, text=text,
                      command=partial(self._navigate, action)).pack(
                          side='left', padx=2)

    def _navigate(self, action: str) -> None:
        """Move the shown month by one navigation action and redraw."""
        self._year, self._month = shift_month(self._year, self._month, action)
        self._show_month()

    def _show_month(self) -> None:
        """Show the current month's title and rebuild the day grid."""
        self._title.configure(text=f'{calendar.month_name[self._month]} '
                              f'{self._year}')
        for child in self._grid.winfo_children():
            child.destroy()
        for column, name in enumerate(WEEKDAYS):
            tk.Label(self._grid, text=name).grid(row=0, column=column, padx=1)
        self._place_days()

    def _place_days(self) -> None:
        """Place one day button, or a blank cell, per day of the month."""
        for week, days in enumerate(month_weeks(self._year, self._month), 1):
            for column, day in enumerate(days):
                self._day_widget(day).grid(row=week, column=column, padx=1,
                                           pady=1)

    def _day_widget(self, day: int) -> tk.Widget:
        """Return a blank cell for a padding day, else a day button."""
        if day == 0:
            return tk.Label(self._grid, text='')
        button = tk.Button(self._grid, text=str(day), width=2,
                           command=partial(self._pick, day))
        minimum, maximum = self._bounds
        if day_out_of_range(date(self._year, self._month, day), minimum,
                            maximum):
            button['state'] = 'disabled'
        return button

    def _pick(self, day: int) -> None:
        """Return the clicked day's date and close the calendar."""
        self._finish(date(self._year, self._month, day))

    def _cancel(self) -> None:
        """Close the calendar without returning a date."""
        self._finish(None)

    def _finish(self, chosen: Optional[date]) -> None:
        """Report the outcome, destroy the window and restore the grab."""
        parent = self._win.master
        try:
            self._on_pick(chosen)
        finally:
            self._win.destroy()
            if self._restore:
                _restore_grab(parent)
