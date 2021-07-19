import numpy as np
import pandas as pd
from pandas.api.types import is_list_like

import staircase as sc
from staircase.core.ops.masking import clip
from staircase.core.stats.statistic import _get_stairs_method


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

    def agg(self, funcs):
        if isinstance(funcs, str):
            funcs = [funcs]
        self._ensure_slices()
        df = pd.DataFrame(index=self._slices.index)
        for func in funcs:
            df[func] = getattr(self, func)()
        return df

    def apply(self, func, *args, **kwargs):
        self._ensure_slices()
        return self._slices.apply(func, *args, **kwargs)

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

    def hist(self, *args, **kwargs):
        self._ensure_slices()
        return self._slices.apply(sc.Stairs.hist, *args, **kwargs).fillna(0)

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
        return sc.Stairs.new(
            initial_value=self._stairs.initial_value,
            data=pd.DataFrame({"value": result}, index=index),
        )


def make_slice_method(func):
    def method(self):
        self._ensure_slices()
        return self._slices.map(func)

    return method


for method_name in ["_max", "_min", "mean", "median", "integral", "mode"]:
    method = make_slice_method(_get_stairs_method(method_name))
    setattr(StairsSlicer, method_name, method)


def slice(self, x, closed="left"):
    """
    Evaluates the value of the step function at one, or more, points.

    This method can be used to directly sample values of the corresponding step function at the points
    provided, or alternatively calculate aggregations over some window around each point.  The first of these
    is performed when *aggfunc* is None.

    If *aggfunc* is None then the results of this function should be considered as :math:`\\lim_{x \\to z^{-}} f(x)`
    or :math:`\\lim_{x \\to z^{+}} f(x)`, when how = 'left' or how = 'right' respectively. See
    :ref:`A note on interval endpoints<getting_started.interval_endpoints>` for an explanation.

    If *aggfunc* is not None then a window, around each point x (referred to as the focal point), over which to aggregate is required.
    The window is defined by two values paired into an array-like parameter called *window*.
    These two scalars are the distance from the focal point to the left boundary of the window, and the right boundary
    of the window respectively.

    The function can be called using parentheses.  See example below.

    Parameters
    ----------
    x : int, float or vector data
        Values at which to evaluate the function
    how : {'left', 'right'}, default 'right'
        Only relevant if *aggfunc* is None.
        If points where step changes occur do not coincide with x then this parameter
        has no effect.  Where a step changes occurs at a point given by x, this parameter
        determines if the step function is evaluated at the interval to the left, or the right.
    aggfunc: {'mean', 'median', 'mode', 'max', 'min', 'std', None}.  Default None.
        A string corresponding to the aggregating function
    window : array-like of int, float or pandas.Timedelta, optional
        Only relevant if *aggfunc* is not None.  Should be length of 2. Defines distances from focal point to window boundaries.
    lower_how: {'left', 'right'}, default 'right'
        Only relevant if *aggfunc* is not None.  Determines how the left window boundary should be evaluated.
        If 'left' then :math:`\\lim_{x \\to lower_how^{-}} f(x)` is included in the window.
    upper_how: {'left', 'right'}, default 'left'
        Only relevant if *aggfunc* is not None.  Determines how the right window boundary should be evaluated.
        If 'right' then :math:`\\lim_{x \\to upper_how^{+}} f(x)` is included in the window.

    Returns
    -------
    float, or list of floats

    See Also
    --------
    staircase.sample
    """
    if isinstance(x, pd.IntervalIndex):
        ii = x
    elif isinstance(x, pd.PeriodIndex):
        end_times = x.end_time
        end_times = end_times.ceil(end_times.freq)
        ii = pd.IntervalIndex.from_arrays(x.start_time, end_times, closed=closed)
    elif is_list_like(x):
        ii = pd.IntervalIndex.from_breaks(x, closed=closed)

    return StairsSlicer(self, ii)


def add_methods(cls):
    cls.slice = slice
