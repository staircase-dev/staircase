import pandas as pd
import numpy as np
from sortedcontainers import SortedDict
from staircase.util._decorators import Appender
from staircase.core.poly import docstrings
from staircase.core.stats.docstrings import integral_and_mean_docstring
import staircase as sc
from staircase.core.tools import (
    _from_cumulative,
    _get_stairs_method,
    _verify_window,
)
from staircase.core.tools.datetimes import (
    _convert_date_to_float,
    _convert_float_to_date,
    _maybe_convert_from_timedeltas,
    _maybe_convert_from_timestamps,
)


def _sample_raw(self, x, how="right"):
    """
    Evaluates the value of the step function at one, or more, points.

    Technically the results of this function should be considered as :math:`\\lim_{x \\to z^{-}} f(x)`
    or :math:`\\lim_{x \\to z^{+}} f(x)`, when how = 'left' or how = 'right' respectively. See
    :ref:`A note on interval endpoints<getting_started.interval_endpoints>` for an explanation.

    Parameters
    ----------
    x : int, float or vector data
        values at which to evaluate the function
    how : {'left', 'right'}, default 'right'
        if points where step changes occur do not coincide with x then this parameter
        has no effect.  Where a step changes occurs at a point given by x, this parameter
        determines if the step function is evaluated at the interval to the left, or the right.

    Returns
    -------
    float, or list of floats

    See Also
    --------
    staircase.sample
    """
    assert how in ("right", "left")
    if hasattr(x, "__iter__"):
        new_instance = _layer_multiple(self.copy(), x, None, [0] * len(x))
        cumulative = new_instance._cumulative()
        if how == "right":
            return [cumulative[_x] for _x in x]
        else:
            shifted_cumulative = SortedDict(
                zip(cumulative.keys()[1:], cumulative.values()[:-1])
            )
            if float("-inf") in x:
                vals = [self[float("-inf")]]
            else:
                vals = []
            vals.extend([val for key, val in shifted_cumulative.items() if key in x])
            return vals
    elif x == float("-inf"):
        return self._sorted_dict_values()[0]
    else:
        cumulative = self._cumulative()
        if how == "right":
            preceding_boundary_index = cumulative.bisect_right(x) - 1
        else:
            preceding_boundary_index = cumulative.bisect_left(x) - 1
        return cumulative.values()[preceding_boundary_index]


def _sample_agg(self, x, window, aggfunc, lower_how="right", upper_how="left"):
    """
    Evaluates the aggregation of the step function over a window around one, or more, points.

    The window around each point is defined by two values paired into an array-like parameter called *window*.
    These two scalars are the distance from the point to the left boundary of the window, and the right boundary
    of the window respectively.


    Parameters
    ----------
    x : int, float or vector data
        values at which to evaluate the function
    aggfunc: {'mean', 'median', 'mode', 'max', 'min', 'std'}
        A string corresponding to the aggregating function
    window : array-like of int, float, optional
        Should be length of 2. Defines distances from focal point to window boundaries.
    lower_how: {'left', 'right'}, default 'right'
        Determines how the left window boundary should be evaluated.
        If 'left' then :math:`\\lim_{x \\to lower_how^{-}} f(x)` is included in the window.
    upper_how: {'left', 'right'}, default 'left'
        Determines how the right window boundary should be evaluated.
        If 'right' then :math:`\\lim_{x \\to upper_how^{+}} f(x)` is included in the window.

    Returns
    -------
    float, or list of floats

    See Also
    --------
    staircase.sample
    """
    assert len(window) == 2, "Window should be a array-like object of length 2."
    if isinstance(aggfunc, str):
        aggfunc = _get_stairs_method(aggfunc)
    left_delta, right_delta = window
    _verify_window(left_delta, right_delta, 0)
    kwargs = (
        {"lower_how": lower_how, "upper_how": upper_how}
        if aggfunc in [sc.Stairs.min, sc.Stairs.max]
        else {}
    )
    if not hasattr(x, "__iter__"):
        return aggfunc(self, lower=x + left_delta, upper=x + right_delta, **kwargs)
    return [
        aggfunc(self, lower=point + left_delta, upper=point + right_delta, **kwargs)
        for point in x
    ]


@Appender(docstrings.sample_docstring, join="\n", indents=1)
def _sample(
    self,
    x,
    how="right",
    aggfunc=None,
    window=(0, 0),
    lower_how="right",
    upper_how="left",
):
    # not using dates
    if aggfunc is None:
        return _sample_raw(self, x, how)
    else:
        return _sample_agg(self, x, window, aggfunc, lower_how, upper_how)


@Appender(docstrings.sample_docstring, join="\n", indents=1)
def sample(
    self,
    x,
    how="right",
    aggfunc=None,
    window=(0, 0),
    lower_how="right",
    upper_how="left",
):
    if self.use_dates:
        x = _convert_date_to_float(x, self.tz)
        window = _maybe_convert_from_timedeltas(window)
    return _sample(self, x, how, aggfunc, window, lower_how, upper_how)


@Appender(docstrings.resample_docstring, join="\n", indents=1)
def _resample(
    self,
    x,
    how="right",
    aggfunc=None,
    window=(0, 0),
    lower_how="right",
    upper_how="left",
):
    if aggfunc is not None:
        assert len(window) == 2, "Window should be a array-like object of length 2."
    if not hasattr(x, "__iter__"):
        x = [
            x,
        ]
    new_cumulative = SortedDict({float("-inf"): _sample(self, float("-inf"))})
    new_cumulative.update(
        {
            point: _sample(self, point, how, aggfunc, window, lower_how, upper_how)
            for point in x
        }
    )
    return _from_cumulative(new_cumulative, self.use_dates, self.tz)


@Appender(docstrings.resample_docstring, join="\n", indents=1)
def resample(
    self,
    x,
    how="right",
    aggfunc=None,
    window=(0, 0),
    lower_how="right",
    upper_how="left",
):
    if self.use_dates:
        x = _convert_date_to_float(x, self.tz)
        window = _maybe_convert_from_timedeltas(window)
    return _resample(self, x, how, aggfunc, window, lower_how, upper_how)


@Appender(docstrings.layer_docstring, join="\n", indents=1)
def _layer(self, start=None, end=None, value=None):
    if hasattr(start, "__iter__") or hasattr(end, "__iter__"):
        layer_func = _layer_multiple
    else:
        layer_func = _layer_single
    return layer_func(self, start, end, value)


@Appender(docstrings.layer_docstring, join="\n", indents=1)
def layer(self, start=None, end=None, value=None):
    if self.use_dates:
        start, end = _maybe_convert_from_timestamps((start, end), self.tz)
    return _layer(self, start, end, value)


def _layer_single(self, start=None, end=None, value=None):
    """
    Implementation of the layer function for when start parameter is single-valued
    """
    if pd.isna(start):
        start = float("-inf")
    if pd.isna(value):
        value = 1
    self[start] = self._get(start, 0) + value
    if start != float("-inf") and self[start] == 0:
        self._pop(start)

    if not pd.isna(end):
        self[end] = self._get(end, 0) - value
        if self[end] == 0 or end == float("inf"):
            self._pop(end)

    self.cached_cumulative = None
    return self


def _layer_multiple(self, starts=None, ends=None, values=None):
    """
    Implementation of the layer function for when start parameter is vector data
    """
    for vector in (starts, ends):
        if vector is not None and values is not None:
            assert len(vector) == len(values)

    if starts is None:
        starts = [float("-inf")] * len(ends)
    if ends is None:
        ends = []
    if values is None:
        values = [1] * max(len(starts), len(ends))

    for start, value in zip(starts, values):
        if pd.isna(start):
            start = float("-inf")
        self[start] = self._get(start, 0) + value
    for end, value in zip(ends, values):
        if not pd.isna(end):
            self[end] = self._get(end, 0) - value
    self.cached_cumulative = None
    return self


@Appender(docstrings.step_changes_docstring, join="\n", indents=1)
def step_changes(self):
    if self.use_dates:
        return dict(
            zip(
                _convert_float_to_date(self._keys()[1:], self.tz),
                self._sorted_dict_values()[1:],
            )
        )
    return dict(self._items()[1:])


@Appender(docstrings.values_in_range_docstring, join="\n", indents=1)
def values_in_range(
    self, lower=float("-inf"), upper=float("inf"), lower_how="right", upper_how="left",
):
    if self.use_dates:
        lower, upper = _maybe_convert_from_timestamps((lower, upper), self.tz)
    return _values_in_range(self, lower, upper, lower_how, upper_how)


@Appender(docstrings.values_in_range_docstring, join="\n", indents=1)
def _values_in_range(
    self, lower=float("-inf"), upper=float("inf"), lower_how="right", upper_how="left",
):
    interior_points = [key for key in self._keys() if lower < key < upper]
    endpoint_vals = _sample_raw(self, [lower], how="right") + _sample_raw(
        self, [upper], how="left"
    )
    if lower_how == "left":
        endpoint_vals += _sample_raw(self, [lower], how="left")
    if upper_how == "right":
        endpoint_vals += _sample_raw(self, [upper], how="right")
    return set(_sample_raw(self, interior_points) + endpoint_vals)


@Appender(docstrings.clip_docstring, join="\n", indents=1)
def _clip(self, lower=float("-inf"), upper=float("inf")):
    assert (
        lower is not None and upper is not None
    ), "clip function should not be called with no parameters."
    assert (
        lower < upper
    ), "Value of parameter 'lower' must be less than the value of parameter 'upper'"
    cumulative = self._cumulative()
    left_boundary_index = cumulative.bisect_right(lower) - 1
    right_boundary_index = cumulative.bisect_right(upper) - 1
    value_at_left = cumulative.values()[left_boundary_index]
    value_at_right = cumulative.values()[right_boundary_index]
    s = dict(self._items()[left_boundary_index + 1 : right_boundary_index + 1])
    s[float("-inf")] = 0
    if lower != float("-inf"):
        s[float("-inf")] = 0
        s[lower] = value_at_left
    else:
        s[float("-inf")] = self[float("-inf")]
    if upper != float("inf"):
        s[upper] = s.get(upper, 0) - value_at_right
    return sc.Stairs(s, self.use_dates, self.tz)


@Appender(docstrings.clip_docstring, join="\n", indents=1)
def clip(self, lower=float("-inf"), upper=float("inf")):
    if self.use_dates:
        lower, upper = _maybe_convert_from_timestamps((lower, upper), self.tz)
    return _clip(self, lower, upper)


@Appender(integral_and_mean_docstring, join="\n", indents=1)
def _get_integral_and_mean(self, lower=float("-inf"), upper=float("inf")):
    new_instance = self.clip(lower, upper)
    if new_instance.number_of_steps() < 2:
        return 0, np.nan
    if lower != float("-inf"):
        new_instance[lower] = new_instance._get(lower, 0)
    if upper != float("inf"):
        new_instance[upper] = new_instance._get(upper, 0)
    cumulative = new_instance._cumulative()
    widths = np.subtract(cumulative.keys()[2:], cumulative.keys()[1:-1])
    heights = cumulative.values()[1:-1]
    area = np.multiply(widths, heights).sum()
    mean = area / (cumulative.keys()[-1] - cumulative.keys()[1])
    return area, mean


@Appender(integral_and_mean_docstring, join="\n", indents=1)
def get_integral_and_mean(self, lower=float("-inf"), upper=float("inf")):
    if self.use_dates:
        lower, upper = _maybe_convert_from_timestamps((lower, upper), self.tz)
    return _get_integral_and_mean(self, lower, upper)
