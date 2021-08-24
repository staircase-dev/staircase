import operator

import numpy as np
import pandas as pd

import staircase as sc
from staircase.core.ops import docstrings
from staircase.core.ops.common import _combine_stairs_via_values
from staircase.util import _sanitize_binary_operands
from staircase.util._decorators import Appender


def _make_boolean_func(docstring, series_comp, float_comp):
    @Appender(docstring, join="\n", indents=1)
    def func(self):
        if np.isnan(self.initial_value):
            initial_value = np.nan
        else:
            initial_value = float_comp(self.initial_value, 0) * 1

        if self._data is None:
            return sc.Stairs(initial_value=initial_value)
        values = series_comp(self._get_values(), 0) * 1
        values.loc[np.isnan(self._get_values().values)] = np.nan
        result = sc.Stairs._new(
            initial_value=initial_value,
            data=pd.DataFrame(
                {"value": values},
            ),
        )
        result._remove_redundant_step_points()
        return result

    return func


make_boolean = _make_boolean_func(
    docstrings.make_boolean_docstring, pd.Series.ne, operator.ne
)


invert = _make_boolean_func(docstrings.invert_docstring, pd.Series.eq, operator.eq)


def _make_logical_func(docstring, array_op, float_op):
    def _op_with_scalar_and(self, other):
        if np.isnan(other):
            return sc.Stairs._new(np.nan, None)
        elif other == 0:
            return sc.Stairs._new(0, None)
        else:
            return self.make_boolean()

    def _op_with_scalar_or(self, other):
        if np.isnan(other):
            return sc.Stairs._new(np.nan, None)
        elif other == 0:
            return self.make_boolean()
        else:
            return sc.Stairs._new(1, None)

    def _op_with_scalar_xor(self, other):
        if np.isnan(other):
            return sc.Stairs._new(np.nan, None)
        elif other == 0:
            return self.make_boolean()
        else:
            return self.invert()

    _op_with_scalar_func = {
        np.logical_and: _op_with_scalar_and,
        np.logical_or: _op_with_scalar_or,
        np.logical_xor: _op_with_scalar_xor,
    }[array_op]

    @Appender(docstring, join="\n", indents=1)
    def func(self, other):
        self, other = _sanitize_binary_operands(self, other)
        if other._data is None:
            return _op_with_scalar_func(self, other.initial_value)
        elif self._data is None:
            return _op_with_scalar_func(other, self.initial_value)
        else:
            return _combine_stairs_via_values(self, other, array_op, float_op)

    return func


def scalar_and(x, y):
    if np.isnan(x) or np.isnan(y):
        return np.nan
    if x == 0 or y == 0:
        return 0
    else:
        return 1


def scalar_or(x, y):
    if np.isnan(x) or np.isnan(y):
        return np.nan
    if x == 0 and y == 0:
        return 0
    else:
        return 1


def scalar_xor(x, y):
    if np.isnan(x) or np.isnan(y):
        return np.nan
    if x != 0 and y == 0:
        return 1
    elif x == 0 and y != 0:
        return 1
    else:
        return 0


logical_and = _make_logical_func(
    docstrings.logical_and_docstring, np.logical_and, scalar_and
)

logical_or = _make_logical_func(
    docstrings.logical_or_docstring, np.logical_or, scalar_or
)

logical_xor = _make_logical_func(
    docstrings.logical_xor_docstring, np.logical_xor, scalar_xor
)
