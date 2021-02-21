from sortedcontainers import SortedDict
import numpy as np
from staircase.core.tools import _sanitize_binary_operands
from staircase.util._decorators import Appender
from staircase.core.ops import docstrings
import staircase as sc


def _compare(init_val_diff, cumulative, zero_comparator):
    truth = cumulative.copy()
    for key, value in truth.items():
        new_val = int(zero_comparator(float(value)))
        truth[key] = new_val
    init_val = int(zero_comparator(float(init_val_diff)))
    new_instance = sc.Stairs(init_val)
    if len(truth) > 0:
        deltas = [truth.values()[0] - init_val]
        deltas.extend(np.diff(truth.values()))
        new_instance._replace_sorted_dict(SortedDict(zip(truth.keys(), deltas)))
        new_instance._reduce()
    else:
        new_instance._replace_sorted_dict(SortedDict())
    return new_instance


def _make_relational_func(comparator, docstring):
    @Appender(docstring, join="\n", indents=1)
    def func(self, other):
        self, other = _sanitize_binary_operands(self, other)
        diff = other - self
        return _compare(diff.get_init_value(), diff._cumulative(), comparator,)

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
