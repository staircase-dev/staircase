import numpy as np
from staircase.core.tools.datetimes import check_binop_timezones
from staircase.util._decorators import Appender
from staircase.core.ops import docstrings
import staircase as sc


def _sanitize_binary_operands(self, other, copy_other=False):
    if not isinstance(other, sc.Stairs):
        other = sc.Stairs(other, self.use_dates, self.tz)
    else:
        check_binop_timezones(self, other)
        if copy_other:
            other = other.copy()
    return self.copy(), other


@Appender(docstrings.negate_docstring, join="\n", indents=1)
def negate(self):
    new_instance = self.copy()
    for key, delta in new_instance._items():
        new_instance[key] = -delta
    new_instance.cached_cumulative = None
    return new_instance


@Appender(docstrings.add_docstring, join="\n", indents=1)
def add(self, other):
    new_instance, other = _sanitize_binary_operands(self, other)
    for key, value in other._items():
        new_instance[key] = self._get(key, 0) + value
    new_instance._reduce()
    new_instance.use_dates = self.use_dates or other.use_dates
    new_instance.cached_cumulative = None
    return new_instance


@Appender(docstrings.subtract_docstring, join="\n", indents=1)
def subtract(self, other):
    if not isinstance(other, sc.Stairs):
        other = sc.Stairs(other, self.use_dates, self.tz)
    else:
        check_binop_timezones(self, other)
    other = -other
    return self + other


def _mul_or_div(self, other, op):
    a = self.copy()
    b = other.copy()
    a_keys = a._keys()
    b_keys = b._keys()
    a._layer_multiple(b_keys, None, [0] * len(b_keys))
    b._layer_multiple(a_keys, None, [0] * len(a_keys))

    multiplied_cumulative_values = op(
        a._cumulative().values(), b._cumulative().values()
    )
    new_instance = sc.Stairs.from_cumulative(
        dict(zip(a._keys(), multiplied_cumulative_values)),
        use_dates=self.use_dates,
        tz=self.tz,
    )
    new_instance._reduce()
    return new_instance


@Appender(docstrings.divide_docstring, join="\n", indents=1)
def divide(self, other):
    if not isinstance(other, sc.Stairs):
        other = sc.Stairs(other, self.use_dates, self.tz)
    else:
        check_binop_timezones(self, other)
    if not bool(other.make_boolean()):
        raise ZeroDivisionError(
            "Divisor Stairs instance must not be zero-valued at any point"
        )

    return _mul_or_div(self, other, np.divide)


@Appender(docstrings.multiply_docstring, join="\n", indents=1)
def multiply(self, other):
    if not isinstance(other, sc.Stairs):
        other = sc.Stairs(other, self.use_dates, self.tz)
    else:
        check_binop_timezones(self, other)
    return _mul_or_div(self, other, np.multiply)
