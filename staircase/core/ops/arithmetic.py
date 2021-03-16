import operator
import numpy as np
from staircase.core.tools import _sanitize_binary_operands
from staircase.util._decorators import Appender
from staircase.core.ops import docstrings
import staircase as sc


@Appender(docstrings.negate_docstring, join="\n", indents=1)
def negate(self):
    new_instance = self.copy()
    for key, delta in new_instance._items():
        new_instance[key] = -delta
    new_instance.cached_cumulative = None
    return new_instance


def _make_add_subtract_func(docstring, op):
    @Appender(docstring, join="\n", indents=1)
    def func(self, other):
        new_instance, other = _sanitize_binary_operands(self, other)
        for key, value in other._items():
            new_instance[key] = op(self._get(key, 0), value)
        new_instance._reduce()
        new_instance.use_dates = self.use_dates or other.use_dates
        new_instance.cached_cumulative = None
        return new_instance

    return func


add = _make_add_subtract_func(docstrings.add_docstring, operator.add)
subtract = _make_add_subtract_func(docstrings.subtract_docstring, operator.sub)


def _make_mul_div_func(docstring, op):

    is_divide = op == np.divide

    @Appender(docstring, join="\n", indents=1)
    def func(self, other):
        self_copy, other_copy = _sanitize_binary_operands(self, other, copy_other=True)
        if is_divide and not bool(other_copy.make_boolean()):
            raise ZeroDivisionError(
                "Divisor Stairs instance must not be zero-valued at any point"
            )

        self_keys = self._keys()
        other_keys = other_copy._keys()
        self_copy._layer_multiple(other_keys, None, [0] * len(other_keys))
        other_copy._layer_multiple(self_keys, None, [0] * len(self_keys))

        multiplied_cumulative_values = op(
            self_copy._cumulative().values(), other_copy._cumulative().values()
        )
        new_instance = sc.Stairs.from_cumulative(
            dict(zip(self_copy._keys(), multiplied_cumulative_values)),
            use_dates=self.use_dates,
            tz=self.tz,
        )
        new_instance._reduce()
        return new_instance

    return func


multiply = _make_mul_div_func(docstrings.multiply_docstring, np.multiply)
divide = _make_mul_div_func(docstrings.divide_docstring, np.divide)
