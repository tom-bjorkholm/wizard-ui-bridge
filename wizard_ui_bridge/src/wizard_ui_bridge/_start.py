#! /usr/local/bin/python3
"""Pass a start value only to the ask methods that accept it.

The typed ask methods gained a keyword-only start_value parameter after
bridges outside this package were written. The code of this package
calls them through start_args(). For a method that does not accept
start_value yet, the start value is passed as the default instead, and
the question is not nullable. A DeprecationWarning names the method.
The question then still starts with the value, but an emptied answer
gives the start value and never None, as before start_value existed.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import warnings
from typing import Callable, Generic, NamedTuple, Optional, TypedDict, \
    TypeVar, Union
from wizard_ui_bridge._help import accepts_keyword

_V = TypeVar('_V')
_D = TypeVar('_D')


class StartKwargs(TypedDict, Generic[_V], total=False):
    """The keyword arguments that carry a start value to an ask method."""

    start_value: _V


class StartArgs(NamedTuple, Generic[_V, _D]):
    """The default, nullable and start keyword arguments for a method."""

    default: Union[_V, _D]
    nullable: bool
    kwargs: StartKwargs[_V]


def start_args(method: Callable[..., object], start_value: Optional[_V],
               default: _D, nullable: bool = False) -> StartArgs[_V, _D]:
    """Return how to pass default, nullable and start_value to method.

    With no start value, default and nullable are passed unchanged. A
    method that takes start_value, by name or as **kwargs, also gets
    the start value. Any other method gets the start value as its
    default and nullable False, and a DeprecationWarning names it.
    """
    if start_value is None:
        return StartArgs(default, nullable, {})
    if accepts_keyword(method, 'start_value'):
        return StartArgs(default, nullable, {'start_value': start_value})
    name = getattr(method, '__qualname__', repr(method))
    warnings.warn(f'{name}() does not accept the keyword-only parameter '
                  'start_value. This is deprecated; please add it. The '
                  'start value is passed as the default instead.',
                  DeprecationWarning, stacklevel=3)
    return StartArgs(start_value, False, {})
