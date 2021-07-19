import numpy as np
import pandas as pd
from pandas.api.types import is_list_like

import staircase as sc
from staircase.constants import inf
from staircase.core.ops.masking import _get_slice_index
from staircase.core.stats import docstrings
from staircase.docstrings import examples
from staircase.util import _get_lims, _replace_none_with_infs
from staircase.util._decorators import Appender


def _get_integral_and_mean_uncached(stairs):
    if stairs._data is None or len(stairs._data) < 2:
        return 0, np.nan  # TODO: is zero right here?  ?

    value_sums = stairs.value_sums(group=False)
    value_sums = value_sums[value_sums.index.notnull()]
    integral = (value_sums * value_sums.index).sum()
    mean = integral / value_sums.sum()
    return integral, mean


# TODO: docstring
# TODO: test
# TODO: what's new
@Appender(docstrings.integral_and_mean_docstring, join="\n", indents=1)
def _get_integral_and_mean(self, where=(-inf, inf)):
    where = _replace_none_with_infs(where)
    if where == (-inf, inf):
        if self._integral_and_mean is None:
            self._integral_and_mean = _get_integral_and_mean_uncached(self)
        return self._integral_and_mean
    return _get_integral_and_mean_uncached(self.clip(*where))


# TODO: docstring
# TODO: test
# TODO: what's new
@Appender(docstrings.integral_docstring, join="\n", indents=1)
def integral(self, where=(-inf, inf)):
    area, _ = _get_integral_and_mean(self, where)
    return area


# TODO: docstring
# TODO: test
# TODO: what's new
@Appender(docstrings.mean_docstring, join="\n", indents=1)
def mean(self, where=(-inf, inf)):
    _, mean = _get_integral_and_mean(self, where)
    return mean


# TODO: docstring
# TODO: test
# TODO: what's new
@Appender(docstrings.median_docstring, join="\n", indents=1)
def median(self, where=(-inf, inf)):
    where = _replace_none_with_infs(where)
    if where == (-inf, inf):
        percentiles = self.dist.percentile
    else:
        percentiles = self.clip(*where).dist.percentile
    return percentiles(50)


def value_sums(self, where=(-inf, inf), dropna=True, group=True):
    if self._data is None:
        return None
    where = _replace_none_with_infs(where)
    if where == (-inf, inf):
        stairs = self
    else:
        stairs = self.clip(*where)

    value_sums = pd.Series(
        np.diff(stairs._data.index.values), index=stairs._get_values().iloc[:-1]
    )
    # .values used to avoid a strange numpy Future Warning
    if group:
        result = value_sums.groupby(value_sums.index.values).sum()
    else:
        return value_sums
    if not dropna:
        isna = value_sums.index.isna()
        if isna.any():
            na_val = value_sums.where(isna).first_valid_index()
            result[na_val] = value_sums[isna].sum()
    return result


# TODO: docstring
# TODO: test
# TODO: what's new
@Appender(docstrings.mode_docstring, join="\n", indents=1)
def mode(self, where=(-inf, inf)):
    return value_sums(self, where).idxmax()


# TODO: docstring
# TODO: test
# TODO: what's new
@Appender(docstrings.var_docstring, join="\n", indents=1)
def var(self, where=(-inf, inf)):
    where = _replace_none_with_infs(where)
    if where == (-inf, inf):
        percentiles = self.dist.percentile
    else:
        percentiles = self.clip(*where).dist.percentile
    percentile_minus_mean = percentiles - mean(self, where)
    values = percentile_minus_mean._get_values()
    squared_values = values * values
    return (
        sc.Stairs.new(
            initial_value=0, data=pd.DataFrame({"value": squared_values}),
        ).agg("integral", (0, 100))
        / 100
    )


# TODO: docstring
# TODO: test
# TODO: what's new
@Appender(docstrings.std_docstring, join="\n", indents=1)
def std(self, where=(-inf, inf)):
    return np.sqrt(var(self, where))


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
    if right_index == -1:
        return np.array([self.initial_value])
    values = self._get_values().iloc[max(0, left_index) : right_index]
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


def agg(self, func, where=(-inf, inf), closed=None):

    where = _replace_none_with_infs(where)
    stairs = self if where == (-inf, inf) else self.clip(*where)

    def apply(_func):
        if isinstance(_func, str):
            name = _func
            _func = _get_stairs_method(_func)
        else:
            name = _func.__name__
        if name in ("min", "max"):
            return name, _func(self, where=where, closed=closed)
        else:
            return name, _func(stairs)

    if is_list_like(func):
        return pd.Series({name: calc for name, calc in map(apply, func)})
    return apply(func)[1]


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
    return mean(self * other, where) - mean(self, where) * mean(other, where)


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
    return self.cov(other, where) / (std(self, where) * std(other, where))


def _get_stairs_method(name):
    return {
        "integral": integral,
        "mean": mean,
        "median": median,
        "mode": mode,
        "max": _max,
        "min": _min,
        "_max": _max,
        "_min": _min,
        "std": std,
        "var": var,
    }[name]
