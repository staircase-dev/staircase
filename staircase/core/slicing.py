from __future__ import annotations

from typing import Callable

import numpy as np
import pandas as pd
from pandas.api.types import is_list_like
from typing_extensions import Literal

import staircase as sc
from staircase.core.ops.masking import clip
from staircase.core.stats.statistic import _get_stairs_method
from staircase.docstrings import slicing as docstrings
from staircase.util._decorators import Appender


class StairsSlicer:
    def __init__(self, stairs: sc.Stairs, interval_index):
        self._stairs = stairs
        self._interval_index = interval_index
        self._slices: pd.Series | None = None

    def _create_slices(self) -> None:
        slices = self._interval_index.map(lambda i: clip(self._stairs, i.left, i.right))
        self._slices = pd.Series(slices, index=self._interval_index)

    def _ensure_slices(self) -> StairsSlicer:
        if self._slices is None:
            self._create_slices()
        return self

    @Appender(docstrings.agg_docstring, join="\n", indents=1)
    def agg(self, funcs) -> pd.DataFrame:
        if isinstance(funcs, str):
            funcs = [funcs]
        self._ensure_slices()
        df = pd.DataFrame(index=self._slices.index)
        for func in funcs:
            df[func] = getattr(self, func)()
        return df

    @Appender(docstrings.apply_docstring, join="\n", indents=1)
    def apply(self, func: Callable, *args, **kwargs) -> pd.Series:
        self._ensure_slices()
        return self._slices.apply(func, args=args, **kwargs)

    @Appender(docstrings._docstrings["max"], join="\n", indents=1)
    def max(self) -> float:
        result = self._max()
        if self._stairs._closed == "left" and self._interval_index.closed in (
            "right",
            "both",
        ):
            result = np.maximum(result, self._stairs(self._interval_index.right))
        elif self._stairs._closed == "right" and self._interval_index.closed in (
            "left",
            "both",
        ):
            result = np.maximum(result, self._stairs(self._interval_index.left))
        return result

    @Appender(docstrings._docstrings["min"], join="\n", indents=1)
    def min(self) -> float:
        result = self._min()
        if self._stairs._closed == "left" and self._interval_index.closed in (
            "right",
            "both",
        ):
            result = np.minimum(result, self._stairs(self._interval_index.right))
        elif self._stairs._closed == "right" and self._interval_index.closed in (
            "left",
            "both",
        ):
            result = np.minimum(result, self._stairs(self._interval_index.left))
        return result

    @Appender(docstrings.hist_docstring, join="\n", indents=1)
    def hist(self, *args, **kwargs):
        self._ensure_slices()
        zero = (
            self._stairs._data.index[0] - self._stairs._data.index[0]
        )  # hack to get 0 or pd.Timedelta(0)
        return self._slices.apply(sc.Stairs.hist, *args, **kwargs).fillna(zero)

    @Appender(docstrings.resample_docstring, join="\n", indents=1)
    def resample(self, func: str):
        if not self._interval_index.is_non_overlapping_monotonic:
            raise ValueError(
                "Slices must be monotonic increasing (ascending order) and not overlapping"
            )
        self._ensure_slices()
        new_values = getattr(self, func)()
        left_bound = self._slices.index.left.min()
        right_bound = self._slices.index.right.max()
        stairs_na = self._stairs.isna().mask((left_bound, right_bound)).fillna(0)
        return (
            self._stairs.mask((left_bound, right_bound))
            .fillna(0)
            .mask(stairs_na)
            .layer(new_values.index.left, new_values.index.right, new_values.values)
        )


def make_slice_method(method_name: str) -> Callable:

    func = _get_stairs_method(method_name)
    docstring = docstrings._docstrings.get(method_name, "")

    @Appender(docstring, join="\n", indents=1)
    def method(self):
        self._ensure_slices()
        return self._slices.map(func)

    return method


for method_name in ["_max", "_min", "mean", "median", "integral", "mode"]:
    method = make_slice_method(method_name)
    setattr(StairsSlicer, method_name, method)


def slice(
    self: sc.Stairs, cuts, closed: Literal["left", "right", "both", "neither"] = "left"
) -> StairsSlicer:
    """
    Slice the step function into pieces.

    A slice corresponding to an interval *(a,b)* will be equal to *self* everywhere
    in *(a,b)* and undefined elsewhere.

    Parameters
    ----------
    self : Stairs : class
    cuts : sequence, :class:`pandas.IntervalIndex`, :class:`pandas.PeriodIndex`.
        Used to slice the step function.  If *cuts* is a sequence then it should comprised
        of monotonically increasing values from the step function domain.
    closed : {'left', 'right', 'both', 'neither'}
        Only relevant if *cuts* is not a :class:`pandas.IntervalIndex`, and indicates
        if the intervals derived from *cuts* should closed on the left-side, right-side, both or neither.

    Returns
    -------
    :class:`StairsSlicer`

    Examples
    --------

    .. plot::
        :context: close-figs

        >>> s3.plot(arrows=True)

    >>> s3.slice(np.linspace(1,5,9))
    <staircase.core.slicing.StairsSlicer at 0x20053f07400>

    >>> s3.slice(np.linspace(1,5,9)).mean()
    [1.0, 1.5)    1.0
    [1.5, 2.0)    1.0
    [2.0, 2.5)    0.0
    [2.5, 3.0)    NaN
    [3.0, 3.5)    NaN
    [3.5, 4.0)    1.0
    [4.0, 4.5)   -1.0
    [4.5, 5.0)   -1.0
    dtype: float64

    >>> s3.slice(np.linspace(0,6,4)).agg(["min", "max"])
                min  max
    [0.0, 2.0)  0.0  1.0
    [2.0, 4.0)  0.0  1.0
    [4.0, 6.0) -1.0  0.0

    >>> s3.slice(np.linspace(0,6,4)).hist(bins=[-1, -0.5, 0, 0.5, 1, 1.5])
                [-1.0, -0.5)  [-0.5, 0.0)  [0.0, 0.5)  [0.5, 1.0)  [1.0, 1.5)
    [0.0, 2.0)           0.0          0.0         1.0         0.0         1.0
    [2.0, 4.0)           0.0          0.0         0.5         0.0         0.5
    [4.0, 6.0)           1.0          0.0         1.0         0.0         0.0
    """
    if isinstance(cuts, pd.IntervalIndex):
        ii = cuts
    elif isinstance(cuts, pd.PeriodIndex):
        end_times = cuts.end_time + pd.Timedelta(
            "1ns"
        )  # PeriodIndex leaves a 1ns gap between intervals
        ii = pd.IntervalIndex.from_arrays(cuts.start_time, end_times, closed=closed)
    elif is_list_like(cuts):
        ii = pd.IntervalIndex.from_breaks(cuts, closed=closed)

    return StairsSlicer(self, ii)


def add_methods(cls):
    cls.slice = slice
