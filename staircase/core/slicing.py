import numpy as np
import pandas as pd
from pandas.api.types import is_list_like

import staircase as sc
from staircase.core.ops.masking import clip
from staircase.core.stats.statistic import _get_stairs_method
from staircase.docstrings import slicing as docstrings
from staircase.util._decorators import Appender


class StairsSlicer:
    def __init__(self, stairs, interval_index):
        self._stairs = stairs
        self._interval_index = interval_index
        self._slices = None

    def _create_slices(self):
        slices = self._interval_index.map(lambda i: clip(self._stairs, i.left, i.right))
        self._slices = pd.Series(slices, index=self._interval_index)

    def _ensure_slices(self):
        if self._slices is None:
            self._create_slices()
        return self

    @Appender(docstrings.agg_docstring, join="\n", indents=1)
    def agg(self, funcs):
        if isinstance(funcs, str):
            funcs = [funcs]
        self._ensure_slices()
        df = pd.DataFrame(index=self._slices.index)
        for func in funcs:
            df[func] = getattr(self, func)()
        return df

    @Appender(docstrings.apply_docstring, join="\n", indents=1)
    def apply(self, func, *args, **kwargs):
        self._ensure_slices()
        return self._slices.apply(func, args=args, **kwargs)

    @Appender(docstrings._docstrings["max"], join="\n", indents=1)
    def max(self):
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
    def min(self):
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
        zero = (  # hack to get 0 or pd.Timedelta(0)
            self._stairs._data.index[0] - self._stairs._data.index[0]
        )
        return self._slices.apply(sc.Stairs.hist, *args, **kwargs).fillna(zero)

    @Appender(docstrings.resample_docstring, join="\n", indents=1)
    def resample(self, func, points="left"):
        # TODO: assert func in name list
        self._ensure_slices()
        if isinstance(points, str):
            if points == "left":
                index = self._slices.index.left
            elif points == "right":
                index = self._slices.index.right
            elif points == "mid":
                index = self._slices.index.mid
            else:
                pass  # TODO: throw error
        else:
            assert len(points) == len(self._slices.index)
            index = points
        result = getattr(self, func)()
        return sc.Stairs._new(
            initial_value=self._stairs.initial_value,
            data=pd.DataFrame({"value": result.values}, index=index),
        )


def make_slice_method(method_name):

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


def slice(self, cuts, closed="left"):
    """
    Slice the step function into pieces.

    A slice corresponding to an interval *(a,b)* will be equal to *self* everywhere
    in *(a,b)* and undefined elsewhere.

    Parameters
    ----------
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
        end_times = cuts.end_time
        end_times = end_times.ceil(end_times.freq)
        ii = pd.IntervalIndex.from_arrays(cuts.start_time, end_times, closed=closed)
    elif is_list_like(cuts):
        ii = pd.IntervalIndex.from_breaks(cuts, closed=closed)

    return StairsSlicer(self, ii)


def add_methods(cls):
    cls.slice = slice
