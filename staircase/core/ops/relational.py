import numpy as np
from staircase.core.tools import _sanitize_binary_operands
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


def _make_relational_func(comparator, docstring):
    @Appender(docstring, join="\n", indents=1)
    def func(self, other):
        self, other = _sanitize_binary_operands(self, other)
        return _compare(
            (other - self)._cumulative(),
            comparator,
            self.use_dates or other.use_dates,
            self.tz,
        )

    return func


lt = _make_relational_func(float(0).__lt__, docstrings.lt_docstring)
gt = _make_relational_func(float(0).__gt__, docstrings.gt_docstring)
le = _make_relational_func(float(0).__le__, docstrings.le_docstring)
ge = _make_relational_func(float(0).__ge__, docstrings.ge_docstring)
eq = _make_relational_func(float(0).__eq__, docstrings.eq_docstring)
ne = _make_relational_func(float(0).__ne__, docstrings.ne_docstring)


@Appender(docstrings.identical_docstring, join="\n", indents=1)
def identical(self, other):
    self, other = _sanitize_binary_operands(self, other)
    return bool(self == other)
