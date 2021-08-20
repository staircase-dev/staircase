import bisect
import inspect
import operator

import numpy as np
import pandas as pd

import staircase as sc
from staircase.constants import inf
from staircase.core.ops import docstrings
from staircase.core.ops.common import _combine_stairs_via_values
from staircase.util import _replace_none_with_infs
from staircase.util._decorators import Appender


def _get_slice_index(self, lower, upper, lower_how, upper_how):
    # returns series
    if self._data is None:
        return -1, -1
    bisect_funcs = {
        "right": bisect.bisect_right,
        "left": bisect.bisect_left,
    }
    index_values = self._data.index.values
    lower_val_for_bisect = pd.Series([lower]).values[0]
    upper_val_for_bisect = pd.Series([upper]).values[0]
    left_index = bisect_funcs[lower_how](index_values, lower_val_for_bisect) - 1
    right_index = bisect_funcs[upper_how](index_values, upper_val_for_bisect)
    return left_index, right_index
    # return self._data["value"].iloc[left_index:right_index]


# TODO: docstring
# TODO: test
# TODO: what's new
@Appender(docstrings.clip_docstring, join="\n", indents=1)
def clip(self, lower=-inf, upper=inf):
    lower, upper = _replace_none_with_infs((lower, upper))
    if not lower < upper:
        raise ValueError("'lower' must be strictly less than 'upper'.")
    if lower == -inf and upper == inf:
        return self
    left_index, right_index = _get_slice_index(
        self, lower, upper, lower_how="right", upper_how="left"
    )

    if right_index == -1:
        sliced_values = pd.Series(dtype="float64")
    else:
        sliced_values = self._get_values().iloc[max(0, left_index) : right_index]
    if upper != inf:
        sliced_values.loc[upper] = np.nan
    if lower != -inf and left_index < 0:
        sliced_values = pd.concat(
            [pd.Series([self.initial_value], index=[lower]), sliced_values]
        )
    elif sliced_values.index[0] < lower:
        index = pd.Series(sliced_values.index)
        index.iloc[0] = lower
        sliced_values.index = index

    data = pd.DataFrame({"value": sliced_values})

    initial_value = self.initial_value if lower == -inf else np.nan

    result = sc.Stairs._new(
        initial_value=initial_value,
        data=data,
    )
    result._remove_redundant_step_points()
    return result


def _maskify(self, inverse=False):
    func = np.array(0).__eq__ if not inverse else np.array(0).__ne__
    op = operator.ne if not inverse else operator.eq

    if self._data is None:
        data = None
    else:
        data = pd.DataFrame(
            {"value": self._get_values().where(func, np.nan).where(np.isnan, 0)}
        )

    return sc.Stairs._new(
        initial_value=np.nan if op(self.initial_value, 0) else 0,
        data=data,
    )


def _mask_stairs(self, other, inverse):
    def is_full_inverse_mask(initial_value):
        return initial_value == 0 or np.isnan(initial_value)

    full_mask_comparator = is_full_inverse_mask if inverse else float(0).__ne__
    if other._data is None:
        if full_mask_comparator(other.initial_value):
            return sc.Stairs(initial_value=np.nan)
        else:
            return self.copy()
    return _combine_stairs_via_values(
        self, _maskify(other, inverse=inverse), pd.Series.add, operator.add
    )


def _make_mask_or_where_func(docstring, which):
    def handle_tuple_mask(self, left, right):
        return _mask_stairs(
            self, sc.Stairs().layer(start=left, end=right), inverse=False
        )

    def handle_tuple_where(self, left, right):
        left = -inf if left is None else left
        right = inf if right is None else right
        return clip(self, lower=left, upper=right)

    handle_tuple_func = {"mask": handle_tuple_mask, "where": handle_tuple_where}[which]
    inverse = which == "where"

    @Appender(docstring, join="\n", indents=1)
    def func(self, other):
        assert isinstance(other, tuple) or isinstance(
            other, sc.Stairs
        )  # TODO: exception
        if isinstance(other, tuple):
            if len(other) != 2:
                raise ValueError(
                    f"'other' tuple has length {len(other)} but requires length 2."
                )
            return handle_tuple_func(self, *other)
        return _mask_stairs(self, other, inverse=inverse)

    return func


mask = _make_mask_or_where_func(docstrings.mask_docstring, "mask")

where = _make_mask_or_where_func(docstrings.where_docstring, "where")


def _make_null_comparison_func(docstring, comp_func):
    @Appender(docstring, join="\n", indents=1)
    def func(self):
        initial_value = 1 if comp_func(self.initial_value) else 0
        if self._data is None:
            data = None
        else:
            data = pd.DataFrame(
                comp_func(self._get_values()) * 1, index=self._data.index
            )

        new_instance = sc.Stairs._new(initial_value=initial_value, data=data)
        new_instance._remove_redundant_step_points()
        return new_instance

    return func


# TODO: test
isna = _make_null_comparison_func(docstrings.isna_docstring, np.isnan)

# TODO: test
notna = _make_null_comparison_func(docstrings.notna_docstring, lambda x: ~np.isnan(x))


# TODO: test
@Appender(docstrings.fillna_docstring, join="\n", indents=1)
def fillna(self, value):

    if not isinstance(value, str) and np.isnan(self.initial_value):
        initial_value = value
    else:
        initial_value = self.initial_value

    if self._data is None:
        data = None
    else:
        values = self._get_values().copy()
        if value in ("pad", "ffill") and np.isnan(values.iloc[0]):
            values.iloc[0] = self.initial_value
        if isinstance(value, str):
            values = values.fillna(method=value)
        else:
            values = values.fillna(value=value)
        if value in ("backfill", "bfill") and np.isnan(self.initial_value):
            initial_value = values.iloc[0]
        data = pd.DataFrame({"value": values})

    new_instance = sc.Stairs._new(initial_value=initial_value, data=data)
    new_instance._remove_redundant_step_points()
    return new_instance
