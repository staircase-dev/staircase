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
def layer(self, start=None, end=None, value=None, data=None):
    """
    Changes the values of the step function, in place, by 'layering' intervals.

    #TODO : needs more

    Parameters
    ----------
    start : int, float, array-like or string, optional
        Start time(s) of the interval(s)
    end : int, float, array-like or string, optional
        End time(s) of the interval(s)
    value : int, float, array-like or string, optional
        Value(s) of the interval(s)
    data : :class:`pandas.DataFrame`, optional

    Returns
    -------
    :class:`Stairs`
        The current instance is returned to facilitate method chaining
    """
    if self._data is None and np.isnan(self.initial_value):
        return self
    self._clear_cache()
    if data is not None:
        start, end, value = _extract_from_frame(data, start, end, value)
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
