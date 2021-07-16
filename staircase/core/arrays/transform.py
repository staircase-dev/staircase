import numpy as np
import pandas as pd

from staircase.constants import inf
from staircase.core.arrays import docstrings
from staircase.core.stairs import Stairs
from staircase.core.stats.statistic import corr as _corr
from staircase.core.stats.statistic import cov as _cov
from staircase.util._decorators import Appender


# TODO: docstring
# TODO: test
# TODO: what's new
@Appender(docstrings.sample_example, join="\n", indents=1)
def sample(collection, x):
    """
    Takes a dict-like collection of Stairs instances and evaluates their values across a common set of points.

    Technically the results of this function should be considered as :math:`\\lim_{x \\to z^{-}} f(x)`
    or :math:`\\lim_{x \\to z^{+}} f(x)`, when how = 'left' or how = 'right' respectively. See
    :ref:`A note on interval endpoints<getting_started.interval_endpoints>` for an explanation.


    Parameters
    ----------
    collection : dictionary or pandas.Series
        The Stairs instances at which to evaluate
    points : int, float or vector data
        The points at which to sample the Stairs instances

    Returns
    -------
    :class:`pandas.DataFrame`
        A dataframe, in tidy format, with three columns: points, key, value.  The column key contains
        the identifiers used in the dict-like object specified by 'collection'.

    See Also
    --------
    Stairs.sample
    """
    array = pd.Series(collection)
    return array.apply(Stairs.sample, x=x, include_index=True)


# TODO: docstring
# TODO: test
# TODO: what's new
def limit(collection, x, side="right"):
    """
    Takes a dict-like collection of Stairs instances and evaluates their values across a common set of points.

    Technically the results of this function should be considered as :math:`\\lim_{x \\to z^{-}} f(x)`
    or :math:`\\lim_{x \\to z^{+}} f(x)`, when how = 'left' or how = 'right' respectively. See
    :ref:`A note on interval endpoints<getting_started.interval_endpoints>` for an explanation.


    Parameters
    ----------
    collection : dictionary or pandas.Series
        The Stairs instances at which to evaluate
    points : int, float or vector data
        The points at which to sample the Stairs instances
    how : {'left', 'right'}, default 'right'
        if points where step changes occur do not coincide with x then this parameter
        has no effect.  Where a step changes occurs at a point given by x, this parameter
        determines if the step function is evaluated at the interval to the left, or the right.
    expand_key: boolean, default True
        used when collection is a multi-index pandas.Series.  Indicates if index should be expanded from
        tuple to columns in a dataframe.

    Returns
    -------
    :class:`pandas.DataFrame`
        A dataframe, in tidy format, with three columns: points, key, value.  The column key contains
        the identifiers used in the dict-like object specified by 'collection'.

    See Also
    --------
    Stairs.sample
    """
    array = pd.Series(collection)
    return array.apply(Stairs.limit, x=x, side=side, include_index=True)


# TODO: docstring
# TODO: test
# TODO: what's new
def _make_corr_cov_func(docstring, stairs_method, assume_ones_diagonal):
    @Appender(docstring, join="\n", indents=1)
    def func(collection, where=(-inf, inf)):
        series = pd.Series(collection)
        size = series.shape[0]
        vals = np.ones(shape=(size, size))
        for i in range(size):
            for j in range(i + assume_ones_diagonal, size):
                vals[i, j] = stairs_method(series.iloc[i], series.iloc[j], where=where)
                vals[j, i] = vals[i, j]
        return pd.DataFrame(vals, index=series.index, columns=series.index)

    return func


corr = _make_corr_cov_func(docstrings.corr_docstring, _corr, assume_ones_diagonal=True)
cov = _make_corr_cov_func(docstrings.cov_docstring, _cov, assume_ones_diagonal=False)
