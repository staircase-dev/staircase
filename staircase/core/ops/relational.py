import operator

import numpy as np
import pandas as pd

import staircase as sc
from staircase.core.ops import docstrings
from staircase.core.ops.common import _combine_stairs_via_values
from staircase.util import _sanitize_binary_operands
from staircase.util._decorators import Appender


def _make_relational_func(
    docstring, numpy_relational, series_relational, float_relational
):
    @Appender(docstring, join="\n", indents=1)
    def func(self, other):
        self, other = _sanitize_binary_operands(
            self, other
        )  # converts other to Stairs if not already
        if np.isnan(self.initial_value) or np.isnan(other.initial_value):
            initial_value = np.nan
        else:
            initial_value = (
                float_relational(self.initial_value, other.initial_value) * 1
            )

        if self._data is None and other._data is None:
            return sc.Stairs._new(
                initial_value=initial_value,
                data=None,
            )
        elif self._data is None or other._data is None:
            if other._data is None:  # self._data exists
                values = self._get_values()
                new_values = numpy_relational(values, other.initial_value)
                new_values[values.isna()] = np.nan
                new_index = self._data.index
            else:  # other._data exists
                values = other._get_values()
                new_values = numpy_relational(self.initial_value, values)
                new_values[values.isna()] = np.nan
                new_index = other._data.index

            new_instance = sc.Stairs._new(
                initial_value=initial_value,
                data=pd.DataFrame(
                    {"value": new_values * 1},
                    index=new_index,
                ),
            )
            new_instance._remove_redundant_step_points()
            return new_instance
        else:
            return _combine_stairs_via_values(
                self, other, series_relational, float_relational
            )

    return func


def _is_series_equal(s1, s2):
    if not pd.api.types.is_float_dtype(s1):
        s1 = s1.astype("float64")
    if not pd.api.types.is_float_dtype(s2):
        s2 = s2.astype("float64")
    if pd.api.types.is_numeric_dtype(s1.index) and not pd.api.types.is_float_dtype(
        s1.index
    ):
        s1.index = s1.index.astype("float64")
    if pd.api.types.is_numeric_dtype(s2.index) and not pd.api.types.is_float_dtype(
        s2.index
    ):
        s2.index = s2.index.astype("float64")
    return pd.Series.equals(s1, s2)


def identical(self, other):
    """
    A boolean comparison for Stairs instances.

    Returns True if and only if *self* and *other* represent identical step functions.

    Parameters
    ----------
    other :  int, float, or :class:`Stairs`

    Returns
    -------
    boolean

    Examples
    --------

    >>> s1.identical(s1)
    True

    >>> s1.identical(s1.copy())
    True

    >>> s1.identical(s1.copy().layer(1,2))
    False

    >>> sc.Stairs(initial_value = 3).identical(3)
    True

    >>> sc.Stairs(initial_value = np.nan).identical(np.nan)
    True
    """
    self, other = _sanitize_binary_operands(self, other)
    if (self.initial_value != other.initial_value) and not (
        np.isnan(self.initial_value) and np.isnan(other.initial_value)
    ):
        return False
    elif self._data is None and other._data is None:
        return True
    elif self._data is None or other._data is None:
        return False
    elif self._valid_values and other._valid_values:
        return _is_series_equal(self._data["value"], other._data["value"])
    else:
        return _is_series_equal(self._get_deltas(), other._get_deltas())


lt = _make_relational_func(
    docstrings.lt_docstring,
    np.less,
    pd.Series.lt,
    operator.lt,
)


gt = _make_relational_func(
    docstrings.gt_docstring,
    np.greater,
    pd.Series.gt,
    operator.gt,
)


le = _make_relational_func(
    docstrings.le_docstring,
    np.less_equal,
    pd.Series.le,
    operator.le,
)


ge = _make_relational_func(
    docstrings.ge_docstring,
    np.greater_equal,
    pd.Series.ge,
    operator.ge,
)


eq = _make_relational_func(
    docstrings.eq_docstring,
    np.equal,
    pd.Series.eq,
    operator.eq,
)


ne = _make_relational_func(
    docstrings.ne_docstring,
    np.not_equal,
    pd.Series.ne,
    operator.ne,
)
