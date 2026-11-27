#! /usr/local/bin/python3
"""Pass a help text only to the ask methods and readers that accept it.

The typed ask methods, ask_table() and the AskReader of the table helpers
gained a keyword-only help_text parameter after bridges outside this
package were written. The code of this package calls them through
help_kwargs(), which leaves the help text out, with a DeprecationWarning,
for a method or reader that does not accept it yet, so an older bridge
keeps working until it is updated.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import inspect
import warnings
from typing import Callable, Optional, TypedDict


class HelpKwargs(TypedDict, total=False):
    """The keyword arguments that carry a help text to an ask method."""

    help_text: Optional[str]


def help_kwargs(method: Callable[..., object],
                help_text: Optional[str]) -> HelpKwargs:
    """Return help_text as keyword arguments for method, if it takes them.

    A method that takes neither a help_text parameter nor **kwargs gets
    no keyword arguments, and a DeprecationWarning names the method.
    """
    if _accepts_help(method):
        return {'help_text': help_text}
    name = getattr(method, '__qualname__', repr(method))
    warnings.warn(f'{name}() does not accept the keyword-only parameter '
                  'help_text. This is deprecated; please add it.',
                  DeprecationWarning, stacklevel=3)
    return {}


def _accepts_help(method: Callable[..., object]) -> bool:
    """Return whether method takes help_text, by name or as **kwargs."""
    parameters = inspect.signature(method).parameters
    return 'help_text' in parameters or any(
        parameter.kind is inspect.Parameter.VAR_KEYWORD
        for parameter in parameters.values())
