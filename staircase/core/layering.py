import numpy as np
import pandas as pd
from pandas.api.types import is_list_like

from staircase.docstrings import examples
from staircase.util._decorators import Appender


# TODO: docstring
# TODO: test
# TODO: what's new
def layer_frame(self, frame=None, start=None, end=None, value=None):
    if frame is not None:
        frame = frame.copy()
    if isinstance(start, str):
        start = frame[start]
    if isinstance(end, str):
        end = frame[end]
    if isinstance(value, str):
        value = frame[value]

    return layer(self, start, end, value)


def _layer_scalar(self, start, end, value):
    if start is not None and end is not None and start == end:
        return self

    if self._data is None:
        deltas = pd.Series(name="delta")
    else:
        deltas = self._ensure_deltas()._data["delta"]

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


def _broadcast_arrays(*args):
    def maybe_convert_tz_series_to_list(x):
        try:
            if isinstance(x.dtype, pd.DatetimeTZDtype):
                return x.to_list()
            return x
        except Exception:
            return x

    broadcast_length = max([np.size(x) for x in args])
    return [np.full(broadcast_length, maybe_convert_tz_series_to_list(x)) for x in args]


def layer(self, start=None, end=None, value=None):
    if self._data is None and np.isnan(self.initial_value):
        return self
    if value is None:
        value = 1
    if not any(list(map(is_list_like, (start, end, value)))):
        return _layer_scalar(self, start, end, value)
    start, end, value = _broadcast_arrays(
        start, end, value
    )  # np.broadcast_arrays breaks for timestamps in numpy <1.2
    assert not pd.isna(value).any(), "value parameter cannot contain null values"
    start_series = pd.Series(value, index=start)
    end_series = pd.Series(-value, index=end)
    if self._data is not None:
        to_concat = [
            self._ensure_deltas()._data["delta"],
            start_series,
            end_series,
        ]
    else:
        to_concat = [start_series, end_series]
    self.initial_value += start_series[start_series.index.isna()].sum()
    deltas = pd.concat(to_concat)
    self._data = deltas.groupby(deltas.index).sum().rename("delta").to_frame()
    self._valid_deltas = True
    self._valid_values = False
    self._remove_redundant_step_points()
    return self


def add_methods(cls):
    cls.layer = layer
    cls.layer_frame = layer_frame
