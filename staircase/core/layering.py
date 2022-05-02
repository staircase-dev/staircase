import datetime
import warnings

import numpy as np
import pandas as pd
from pandas.api.types import (
    is_datetime64_any_dtype,
    is_list_like,
    is_number,
    is_numeric_dtype,
    is_timedelta64_dtype,
)

from staircase.constants import Inf, NegInf
from staircase.docstrings import examples
from staircase.util._decorators import Appender


def _check_args_dtypes(start, end):
    approved_dtypes_checks = [
        is_datetime64_any_dtype,
        is_timedelta64_dtype,
        is_numeric_dtype,
    ]

    def _check_approved_dtype(vec):
        approved = any(map(lambda func: func(vec), approved_dtypes_checks))
        if not approved:
            warnings.warn(
                f"An argument supplied for 'start' or 'end' has dtype {vec.dtype}.  Only numerical, datetime-like, or timedelta dtypes have been tested.  Using other dtypes is considered experimental."
            )

    _check_approved_dtype(start)
    _check_approved_dtype(end)


def _check_args_types(start, end):
    base_approved_types = [
        pd.Timedelta,
        pd.Timestamp,
        datetime.datetime,
        datetime.timedelta,
        np.datetime64,
        np.timedelta64,
    ]

    def _check_approved_type(arg, approved_types):
        approved = (
            arg is None
            or pd.api.types.is_number(arg)
            or isinstance(arg, approved_types)
        )
        if not approved:
            warnings.warn(
                f"An argument supplied for 'start' or 'end' has type '{type(arg)}'.  Only numerical, datetime-like, or timedelta types have been tested.  Using other types is considered experimental."
            )

    _check_approved_type(start, tuple(base_approved_types + [Inf]))
    _check_approved_type(end, tuple(base_approved_types + [NegInf]))


def _convert_to_series(vec):
    if not isinstance(vec, pd.Series):
        vec = pd.Series(vec)
    else:
        vec = vec.reset_index(drop=True)
    return vec


def _preprocess_layer_args(frame, start, end, value):
    if isinstance(start, NegInf):
        start = None
    if isinstance(end, Inf):
        end = None
    if frame is not None:
        start, end, value = _extract_from_frame(frame, start, end, value)
    if value is None:
        value = 1
    return start, end, value


def _extract_from_frame(frame=None, start=None, end=None, value=None):
    if frame is not None:
        frame = frame.copy()
    if isinstance(start, str):
        start = frame[start]
    if isinstance(end, str):
        end = frame[end]
    if isinstance(value, str):
        value = frame[value]

    return start, end, value


def _layer_scalar(self, start, end, value):
    _check_args_types(start, end)

    if start is not None and end is not None and start == end:
        return self

    if self._data is None:
        deltas = pd.Series(name="delta", dtype="float64")
    else:
        deltas = self._get_deltas()

    if start is None:
        self.initial_value += value
    else:
        if start in deltas.index:
            deltas.loc[start] += value
        else:
            deltas.loc[start] = value
        if deltas.loc[start] == 0:
            deltas.drop(start, inplace=True)

    if end is not None:
        if end in deltas.index:
            deltas.loc[end] -= value
        else:
            deltas.loc[end] = -value
        if deltas.loc[end] == 0:
            deltas.drop(end, inplace=True)
    if len(deltas) > 0:
        self._data = deltas.sort_index().to_frame()
        self._valid_deltas = True
    self._valid_values = False
    return self


@Appender(examples.layer_example, join="\n", indents=1)
def layer(self, start=None, end=None, value=None, frame=None):
    """
    Changes the values of the step function, in place, by 'layering' one or more intervals.

    The values of *start*, *end* and *value* parameters can be one of several types.
    If any of these is a string, then it is expected that *frame* is a :class:`pandas.DataFrame`
    and the string is the name of a column in the dataframe.

    If either *start*, or *end* evaluate to an array-like parameter then all of
    *start*, *end*, and *value* will be broadcast to the same length as the longest of these arrays.

    Parameters
    ----------
    start : scalar, array-like or string, default None
        Start point(s) of the interval(s).
        A value of None is interpreted as negative infinity.
    end : scalar, array-like or string, default None
        End points(s) of the interval(s).
        A value of None is interpreted as positive infinity.
    value : float, array-like or string, default None
        Value(s) of the interval(s).
        A value of None is equivalent to a value of 1.
    frame : :class:`pandas.DataFrame`, optional
        A dataframe containing named columns, whose names may appear as values
        for the other parameters.

    Returns
    -------
    :class:`Stairs`
        The current instance is returned to facilitate method chaining
    """
    if self._data is None and np.isnan(self.initial_value):
        return self
    self._clear_cache()
    start, end, value = _preprocess_layer_args(frame, start, end, value)
    if not any(list(map(is_list_like, (start, end, value)))):
        return _layer_scalar(self, start, end, value)
    value = np.array(value)
    assert not pd.isna(value).any(), "value parameter cannot contain null values"
    start = _convert_to_series(start)
    end = _convert_to_series(end)
    _check_args_dtypes(start, end)  # conversion to Series required before checking
    df = pd.concat([start, end], axis=1, ignore_index=True)
    start_series = pd.Series(value, index=df.iloc[:, 0])
    self.initial_value += start_series[start_series.index.isna()].sum()
    if self._data is None:
        to_concat = [
            start_series,
            pd.Series(-value, index=df.iloc[:, 1]),
        ]
    else:
        to_concat = [
            start_series,
            pd.Series(-value, index=df.iloc[:, 1]),
            self._get_deltas(),
        ]
    deltas = pd.concat(to_concat)

    self._data = deltas.groupby(deltas.index).sum().rename("delta").to_frame()
    self._valid_deltas = True
    self._valid_values = False
    self._remove_redundant_step_points()
    return self


def add_methods(cls):
    cls.layer = layer
