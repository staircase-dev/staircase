import numpy as np
import pandas as pd

import staircase as sc
from staircase.constants import inf
from staircase.core.ops.masking import _get_slice_index
from staircase.core.stats import docstrings
from staircase.docstrings import examples
from staircase.util import _get_lims, _replace_none_with_infs
from staircase.util._decorators import Appender


def _get_integral_and_mean(stairs):
    if stairs._data is None or len(stairs._data) < 2:
        return 0, np.nan  # TODO: is zero right here?  ?
    stairs._ensure_values()
    values = stairs._data["value"]

    widths = np.diff(values.index.values)
    heights = values.values[:-1]
    area = np.nansum(np.multiply(widths, heights))
    mean = area / widths.sum(where=~np.isnan(heights))
    return area, mean


# TODO: docstring
# TODO: test
# TODO: what's new
@Appender(docstrings.integral_and_mean_docstring, join="\n", indents=1)
def get_integral_and_mean(self, where=(-inf, inf)):
    where = _replace_none_with_infs(where)
    if where == (-inf, inf):
        if self._integral_and_mean is None:
            self._integral_and_mean = _get_integral_and_mean(self)
        return self._integral_and_mean
    return _get_integral_and_mean(self.clip(*where))


# TODO: docstring
# TODO: test
# TODO: what's new
@Appender(docstrings.integrate_docstring, join="\n", indents=1)
def integrate(self, where=(-inf, inf)):
    area, _ = self.get_integral_and_mean(where)
    return area


# TODO: docstring
# TODO: test
# TODO: what's new
@Appender(docstrings.mean_docstring, join="\n", indents=1)
def mean(self, where=(-inf, inf)):
    _, mean = self.get_integral_and_mean(where)
    return mean


# TODO: docstring
# TODO: test
# TODO: what's new
@Appender(docstrings.median_docstring, join="\n", indents=1)
def median(self, where=(-inf, inf)):
    return self.fractile(0.5, where)


# TODO: docstring
# TODO: test
# TODO: what's new
@Appender(docstrings.mode_docstring, join="\n", indents=1)
def mode(self, where=(-inf, inf)):
    s = self.clip(*where)._ensure_values()
    value_counts = pd.Series(
        np.diff(s._data.index.values), index=s._data["value"].iloc[:-1]
    )
    return (
        value_counts.groupby(value_counts.index.values).sum().idxmax()
    )  # .values used to avoid a strange numpy Future Warning


# TODO: docstring
# TODO: test
# TODO: what's new
@Appender(docstrings.var_docstring, join="\n", indents=1)
def var(self, where=(-inf, inf)):
    percentile_minus_mean = self.get_percentiles(where) - self.mean(where)
    percentile_minus_mean._ensure_values()
    squared_values = (
        percentile_minus_mean._data["value"] * percentile_minus_mean._data["value"]
    )
    return (
        sc.Stairs.new(
            initial_value=0, data=pd.DataFrame({"value": squared_values}),
        ).integrate((0, 100))
        / 100
    )


# TODO: docstring
# TODO: test
# TODO: what's new
@Appender(docstrings.std_docstring, join="\n", indents=1)
def std(self, where=(-inf, inf)):
    return np.sqrt(self.var(where))


# TODO: docstring
# TODO: test
# TODO: what's new
@Appender(docstrings.values_in_range_docstring, join="\n", indents=1)
def values_in_range(self, where=(-inf, inf), closed=None):
    where = _replace_none_with_infs(where)
    assert len(where) == 2, "Parameter 'where' should be list or tuple of length 2."
    if closed is None:
        closed = self._closed
    lower, upper = where
    lower_how, upper_how = _get_lims(self, closed)
    left_index, right_index = _get_slice_index(self, lower, upper, lower_how, upper_how)
    self._ensure_values()
    if right_index == -1:
        return np.array([self.initial_value])
    values = self._data["value"].iloc[max(0, left_index) : right_index]
    if left_index < 0 and not np.isnan(self.initial_value):
        values = np.append([self.initial_value], values)
    unique = np.unique(values)
    return unique[~np.isnan(unique)]


# TODO: docstring
# TODO: test
# TODO: what's new
@Appender(examples.min_example, join="\n", indents=1)
def _min(
    self, where=(-inf, inf), closed=None,
):
    """
    Calculates the minimum value of the step function

    If an interval which to calculate over is specified it is interpreted
    as a closed interval, with *lower_how* and *upper_how* indicating how the step function
    should be evaluated at the at the endpoints of the interval.

    Parameters
    ----------
    lower : int, float or pandas.Timestamp, optional
        lower bound of the interval on which to perform the calculation
    upper : int, float or pandas.Timestamp, optional
        upper bound of the interval on which to perform the calculation
    lower_how: {'left', 'right'}, default 'right'
        Determines how the step function should be evaluated at *lower*.
        If 'left' then :math:`\\lim_{x \\to lower^{-}} f(x)` is included in the calculation.
    upper_how: {'left', 'right'}, default 'left'
        Determines how the step function should be evaluated at *upper*.
        If 'right' then :math:`\\lim_{x \\to upper^{+}} f(x)` is included in the calculation.

    Returns
    -------
    float
        The minimum value of the step function

    See Also
    --------
    Stairs.max, staircase.min
    """
    where = _replace_none_with_infs(where)
    if closed is None:
        closed = self._closed
    return min(self.values_in_range(where, closed))


# TODO: docstring
# TODO: test
# TODO: what's new
@Appender(examples.max_example, join="\n", indents=1)
def _max(
    self, where=(-inf, inf), closed=None,
):
    """
    Calculates the maximum value of the step function

    If an interval which to calculate over is specified it is interpreted
    as a closed interval, with *lower_how* and *upper_how* indicating how the step function
    should be evaluated at the at the endpoints of the interval.

    Parameters
    ----------
    lower : int, float or pandas.Timestamp, optional
        lower bound of the interval on which to perform the calculation
    upper : int, float or pandas.Timestamp, optional
        upper bound of the interval on which to perform the calculation
    lower_how: {'left', 'right'}, default 'right'
        Determines how the step function should be evaluated at *lower*.
        If 'left' then :math:`\\lim_{x \\to lower^{-}} f(x)` is included in the calculation.
    upper_how: {'left', 'right'}, default 'left'
        Determines how the step function should be evaluated at *upper*.
        If 'right' then :math:`\\lim_{x \\to upper^{+}} f(x)` is included in the calculation.

    Returns
    -------
    float
        The maximum value of the step function

    See Also
    --------
    Stairs.min, staircase.max
    """
    where = _replace_none_with_infs(where)
    if closed is None:
        closed = self._closed
    return max(self.values_in_range(where, closed))


# TODO: docstring
# TODO: test
# TODO: what's new
@Appender(examples.cov_example, join="\n", indents=1)
def cov(self, other, where=(-inf, inf), lag=0, clip="pre"):
    """
    Calculates either covariance, autocovariance or cross-covariance.

    The calculation is between two step functions described by *self* and *other*.
    If lag is None or 0 then covariance is calculated, otherwise cross-covariance is calculated.
    Autocovariance is a special case of cross-covariance when *other* is equal to *self*.

    Parameters
    ----------
    other: :class:`Stairs`
        the stairs instance with which to compute the covariance
    lower : int, float or pandas.Timestamp
        lower bound of the domain on which to perform the calculation
    upper : int, float or pandas.Timestamp
        upper bound of the domain on which to perform the calculation
    lag : int, float, pandas.Timedelta
        a pandas.Timedelta is only valid when using dates.
        If using dates and delta is an int or float, then it is interpreted as a number of hours.
    clip : {'pre', 'post'}, default 'pre'
        only relevant when lag is non-zero.  Determines if the domain is applied before or after *other* is translated.
        If 'pre' then the domain over which the calculation is performed is the overlap
        of the original domain and the translated domain.

    Returns
    -------
    float
        The covariance (or cross-covariance) between *self* and *other*

    See Also
    --------
    Stairs.corr, staircase.cov, staircase.corr
    """
    where = list(_replace_none_with_infs(where))
    if lag != 0:
        assert clip in ["pre", "post"]
        if clip == "pre" and where[1] != inf:
            where[1] = where[1] - lag
        other = other.shift(-lag)
    mask = self.isna() | other.isna()
    self = self.mask(mask)
    other = other.mask(mask)
    return (self * other).mean(where) - self.mean(where) * other.mean(where)


# TODO: docstring
# TODO: test
# TODO: what's new
@Appender(examples.corr_example, join="\n", indents=1)
def corr(self, other, where=(-inf, inf), lag=0, clip="pre"):
    """
    Calculates either correlation, autocorrelation or cross-correlation.

    All calculations are based off the `Pearson correlation coefficient <https://en.wikipedia.org/wiki/Pearson_correlation_coefficient>`_.

    The calculation is between two step functions described by *self* and *other*.
    If lag is None or 0 then correlation is calculated, otherwise cross-correlation is calculated.
    Autocorrelation is a special case of cross-correlation when *other* is equal to *self*.

    Parameters
    ----------
    other: :class:`Stairs`
        the stairs instance with which to compute the correlation
    lower : int, float or pandas.Timestamp
        lower bound of the interval on which to perform the calculation
    upper : int, float or pandas.Timestamp
        upper bound of the interval on which to perform the calculation
    lag : int, float, pandas.Timedelta
        a pandas.Timedelta is only valid when using dates.
        If using dates and delta is an int or float, then it is interpreted as a number of hours.
    clip : {'pre', 'post'}, default 'pre'
        only relevant when lag is non-zero.  Determines if the domain is applied before or after *other* is translated.
        If 'pre' then the domain over which the calculation is performed is the overlap
        of the original domain and the translated domain.

    Returns
    -------
    float
        The correlation (or cross-correlation) between *self* and *other*

    See Also
    --------
    Stairs.cov, staircase.corr, staircase.cov
    """
    where = list(_replace_none_with_infs(where))
    if lag != 0:
        assert clip in ["pre", "post"]
        if clip == "pre" and where[1] != inf:
            where[1] = where[1] - lag
        other = other.shift(-lag)
    mask = self.isna() | other.isna()
    self = self.mask(mask)
    other = other.mask(mask)
    return self.cov(other, where) / (self.std(where) * other.std(where))


def _get_stairs_method(name):
    return {
        "integrate": integrate,
        "mean": mean,
        "median": median,
        "mode": mode,
        "max": _max,
        "min": _min,
        "_max": _max,
        "_min": _min,
    }[name]
