import numpy as np
from staircase.core.tools.datetimes import check_binop_timezones
from staircase.util._decorators import Appender
from staircase.core.ops import docstrings
import staircase as sc


def _compare(cumulative, zero_comparator, use_dates=False, tz=None):
    truth = cumulative.copy()
    for key, value in truth.items():
        new_val = int(zero_comparator(float(value)))
        truth[key] = new_val
    deltas = [truth.values()[0]]
    deltas.extend(np.subtract(truth.values()[1:], truth.values()[:-1]))
    new_instance = sc.Stairs(dict(zip(truth.keys(), deltas)), use_dates, tz)
    new_instance._reduce()
    return new_instance


@Appender(docstrings.lt_docstring, join="\n", indents=1)
def lt(self, other):
    if not isinstance(other, sc.Stairs):
        other = sc.Stairs(other, self.use_dates, self.tz)
    else:
        check_binop_timezones(self, other)
    comparator = float(0).__lt__
    return _compare(
        (other - self)._cumulative(),
        comparator,
        self.use_dates or other.use_dates,
        self.tz,
    )


@Appender(docstrings.gt_docstring, join="\n", indents=1)
def gt(self, other):
    if not isinstance(other, sc.Stairs):
        other = sc.Stairs(other, self.use_dates, self.tz)
    else:
        check_binop_timezones(self, other)
    comparator = float(0).__gt__
    return _compare(
        (other - self)._cumulative(),
        comparator,
        self.use_dates or other.use_dates,
        self.tz,
    )


@Appender(docstrings.le_docstring, join="\n", indents=1)
def le(self, other):
    if not isinstance(other, sc.Stairs):
        other = sc.Stairs(other, self.use_dates, self.tz)
    else:
        check_binop_timezones(self, other)
    comparator = float(0).__le__
    return _compare(
        (other - self)._cumulative(),
        comparator,
        self.use_dates or other.use_dates,
        self.tz,
    )


@Appender(docstrings.ge_docstring, join="\n", indents=1)
def ge(self, other):
    if not isinstance(other, sc.Stairs):
        other = sc.Stairs(other, self.use_dates, self.tz)
    else:
        check_binop_timezones(self, other)
    comparator = float(0).__ge__
    return _compare(
        (other - self)._cumulative(),
        comparator,
        self.use_dates or other.use_dates,
        self.tz,
    )


@Appender(docstrings.eq_docstring, join="\n", indents=1)
def eq(self, other):
    if not isinstance(other, sc.Stairs):
        other = sc.Stairs(other, self.use_dates, self.tz)
    else:
        check_binop_timezones(self, other)
    comparator = float(0).__eq__
    return _compare(
        (other - self)._cumulative(),
        comparator,
        self.use_dates or other.use_dates,
        self.tz,
    )


@Appender(docstrings.ne_docstring, join="\n", indents=1)
def ne(self, other):
    if not isinstance(other, sc.Stairs):
        other = sc.Stairs(other, self.use_dates, self.tz)
    else:
        check_binop_timezones(self, other)
    comparator = float(0).__ne__
    return _compare(
        (other - self)._cumulative(),
        comparator,
        self.use_dates or other.use_dates,
        self.tz,
    )


@Appender(docstrings.identical_docstring, join="\n", indents=1)
def identical(self, other):
    check_binop_timezones(self, other)
    return bool(self == other)
