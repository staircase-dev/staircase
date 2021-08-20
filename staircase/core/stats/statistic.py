import warnings

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


def _cache_integral_and_mean(self):
    if self._data is None or len(self._data) < 2:
        self._integral_and_mean = 0, np.nan  # TODO: is zero right here?  ?
    else:
        value_sums = self.value_sums(group=False)
        value_sums = value_sums[value_sums.index.notnull()]
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                integral = (value_sums * value_sums.index).sum()
                mean = integral / value_sums.sum()
                self._integral_and_mean = (integral, mean)
        except ValueError as exc:
            integral = None
            mean = ((value_sums / value_sums.sum()) * value_sums.index).sum()
            self._integral_and_mean = (integral, mean)
            raise exc


@Appender(docstrings.integral_docstring, join="\n", indents=1)
def integral(self):
    if self._integral_and_mean is None:
        try:
            _cache_integral_and_mean(self)
        except ValueError:
            raise ValueError(
                "Integral calculation results in overflow error.  Consider scaling down step function values to accommodate."
            )
    return self._integral_and_mean[0]


@Appender(docstrings.mean_docstring, join="\n", indents=1)
def mean(self):
    if self._integral_and_mean is None:
        try:
            _cache_integral_and_mean(self)
        except ValueError:
            pass
    return self._integral_and_mean[1]


@Appender(docstrings.median_docstring, join="\n", indents=1)
def median(self):
    return self.dist.percentile(50)


@Appender(docstrings.value_sums_docstring, join="\n", indents=1)
def value_sums(self, dropna=True, group=True):

    if self._data is None:
        return None

    value_sums = pd.Series(
        np.diff(self._data.index.values), index=self._get_values().iloc[:-1]
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


@Appender(docstrings.mode_docstring, join="\n", indents=1)
def mode(self):
    return value_sums(self).idxmax()


@Appender(docstrings.var_docstring, join="\n", indents=1)
def var(self):
    percentile_minus_mean = self.dist.percentile - mean(self)
    values = percentile_minus_mean._get_values()
    squared_values = values * values
    return (
        sc.Stairs._new(
            initial_value=0,
            data=pd.DataFrame({"value": squared_values}),
        ).agg("integral", (0, 100))
        / 100
    )


@Appender(docstrings.std_docstring, join="\n", indents=1)
def std(self):
    return np.sqrt(var(self))


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


def _min(
    self,
    where=(-inf, inf),
    closed=None,
):
    where = _replace_none_with_infs(where)
    if closed is None:
        closed = self._closed
    return min(self.values_in_range(where, closed))


def _max(
    self,
    where=(-inf, inf),
    closed=None,
):
    where = _replace_none_with_infs(where)
    if closed is None:
        closed = self._closed
    return max(self.values_in_range(where, closed))


@Appender(docstrings.agg_docstring, join="\n", indents=1)
def agg(self, name, where=(-inf, inf), closed=None):

    where = _replace_none_with_infs(where)
    stairs = self if where == (-inf, inf) else self.clip(*where)

    def apply(func):
        if isinstance(func, str):
            name = func
            func = _get_stairs_method(name)
        else:
            name = func.__name__
        if name in ("min", "max"):
            return name, func(self, where=where, closed=closed)
        else:
            return name, func(stairs)

    if is_list_like(name):
        return pd.Series({func: calc for func, calc in map(apply, name)})
    return apply(name)[1]


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
    where : tuple or list of length two, optional
    Indicates the domain interval over which to perform the calculation.
        Default is (-sc.inf, sc.inf) or equivalently (None, None).
    lag : int, float, pandas.Timedelta
        A pandas.Timedelta is only valid when domain is date-like.
    clip : {'pre', 'post'}, default 'pre'
        Only relevant when lag is non-zero.  Determines if the domain is applied before or
        after *other* is translated.  If 'pre' then the domain over which the calculation
        is performed is the overlap of the original domain and the translated domain.

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
    return (self * other).clip(*where).mean() - self.clip(*where).mean() * other.clip(
        *where
    ).mean()


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
    where : tuple or list of length two, optional
    Indicates the domain interval over which to perform the calculation.
        Default is (-sc.inf, sc.inf) or equivalently (None, None).
    lag : int, float, pandas.Timedelta
        A pandas.Timedelta is only valid when domain is date-like.
    clip : {'pre', 'post'}, default 'pre'
        Only relevant when lag is non-zero.  Determines if the domain is applied before or
        after *other* is translated.  If 'pre' then the domain over which the calculation
        is performed is the overlap of the original domain and the translated domain.

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
    return self.cov(other, where) / (self.clip(*where).std() * other.clip(*where).std())


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
