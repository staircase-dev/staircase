import numpy as np
import pandas as pd
from pandas.api.types import is_list_like

from staircase.docstrings import examples
from staircase.util._decorators import Appender


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
    if frame is not None:
        start, end, value = _extract_from_frame(frame, start, end, value)
    if value is None:
        value = 1
    if not any(list(map(is_list_like, (start, end, value)))):
        return _layer_scalar(self, start, end, value)
    value = np.array(value)
    assert not pd.isna(value).any(), "value parameter cannot contain null values"
    if not isinstance(start, pd.Series):
        start = pd.Series(start)
    if not isinstance(end, pd.Series):
        end = pd.Series(end)
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
