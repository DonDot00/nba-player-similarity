"""Reusable decorators for the pipeline. (Phase 1: you write these.)

- rate_limited: space out calls so we don't hammer NBA.com
- cache_to_sqlite: skip the API call if the result is already stored
- timed: report how long a function took
"""

from collections.abc import Callable
from typing import Any


def rate_limited(min_interval: float) -> Callable:
    """Decorator factory: ensure at least `min_interval` seconds pass between calls.

    Usage: @rate_limited(2.0)
    Hint: remember when the last call finished; sleep for the remainder if needed.
    """
    # TODO: return a decorator that returns a wrapper (use functools.wraps)
    raise NotImplementedError


def cache_to_sqlite(table: str) -> Callable:
    """Decorator factory: store a function's DataFrame result in SQLite, keyed by its arguments.

    If the data for these arguments is already stored, return it without calling the function.
    """
    # TODO
    raise NotImplementedError


def timed(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator: print (or log) how long `func` took to run."""
    # TODO
    raise NotImplementedError
