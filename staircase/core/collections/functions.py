import pandas as pd
import numpy as np
from staircase.core.tools.datetimes import (
    _convert_date_to_float,
    _convert_float_to_date,
    _using_dates,
)
from staircase.core.tools import _get_union_of_points
from staircase.util._decorators import Appender
from staircase.core.collections import docstrings
from staircase.core.stairs import Stairs
from staircase.core.poly.methods import _sample_raw


@Appender(docstrings.sample_example, join="\n", indents=1)
def sample(collection, points=None, how="right", expand_key=True):
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
    use_dates, tz = _using_dates(collection)
    # assert len(set([type(x) for x in collection.values()])) == 1, "collection must contain values of same type"
    if points is None:
        points = _get_union_of_points(collection)
        points.discard(float("-inf"))
        if use_dates:
            points = _convert_float_to_date(
                list(points), tz
            )  # bugfix - pandas>=1.1 breaks with points as type SortedSet
    else:
        if not hasattr(points, "__iter__"):
            points = [points]
    points = list(points)  # bugfix - pandas>=1.1 breaks with points as type SortedSet
    result = pd.DataFrame(
        {
            "points": points,
            **{
                key: stairs.sample(points, how=how)
                for key, stairs in collection.items()
            },
        }
    ).melt(id_vars="points", var_name="key")
    if (
        isinstance(collection, pd.Series)
        and expand_key
        and len(collection.index.names) > 1
    ):
        try:
            result = result.join(
                pd.DataFrame(result.key.tolist(), columns=collection.index.names)
            ).drop(columns="key")
        except Exception:
            pass
    return result


@Appender(docstrings.aggregate_example, join="\n", indents=1)
def aggregate(collection, func, points=None):
    """
    Takes a collection of Stairs instances and returns a single instance representing the aggregation.

    Parameters
    ----------
    collection: tuple, list, numpy array, dict or pandas.Series
        The Stairs instances to aggregate
    func: a function taking a 1 dimensional vector of floats, and returning a single float
        The function to apply, eg numpy.max
    points: vector of floats or dates
        Points at which to evaluate.  Defaults to union of all step changes.  Equivalent to applying Stairs.resample().

    Returns
    ----------
    :class:`Stairs`

    Notes
    -----
    The points at which to aggregate will include -infinity whether explicitly included or not.

    See Also
    --------
    staircase.mean, staircase.median, staircase.min, staircase.max
    """
    if isinstance(collection, dict) or isinstance(collection, pd.Series):
        Stairs_dict = collection
    else:
        Stairs_dict = dict(enumerate(collection))
    use_dates, tz = _using_dates(collection)
    df = sample(Stairs_dict, points, expand_key=False)
    aggregation = df.pivot_table(
        index="points", columns="key", values="value"
    ).aggregate(func, axis=1)
    if use_dates:
        aggregation.index = _convert_date_to_float(aggregation.index, tz=tz)
    aggregation[float("-inf")] = func(
        [_sample_raw(val, float("-inf")) for key, val in Stairs_dict.items()]
    )
    step_changes = aggregation.sort_index().diff().fillna(0)
    step_changes[float("-inf")] = aggregation[float("-inf")]
    # groupby.sum is necessary on next line as step_changes series may not have unique index elements
    return Stairs(
        dict(step_changes.groupby(level=0).sum()), use_dates=use_dates, tz=tz
    )._reduce()


@Appender(docstrings.mean_docstring, join="\n", indents=1)
def _mean(collection):
    return aggregate(collection, np.mean)


@Appender(docstrings.median_docstring, join="\n", indents=1)
def _median(collection):
    return aggregate(collection, np.median)


@Appender(docstrings.min_docstring, join="\n", indents=1)
def _min(collection):
    return aggregate(collection, np.min)


@Appender(docstrings.max_docstring, join="\n", indents=1)
def _max(collection):
    return aggregate(collection, np.max)


def resample(container, x, how="right"):
    """
    Applies the Stairs.resample function to a 1D container, eg tuple, list, numpy array, pandas series, dictionary

    Returns
    -------
    type(container)

    See Also
    --------
    Stairs.resample
    """
    if isinstance(container, dict):
        return {key: s.resample(x, how) for key, s in container}
    if isinstance(container, pd.Series):
        return pd.Series(
            [s.resample(x, how) for s in container.values], index=container.index
        )
    if isinstance(container, np.ndarray):
        return np.array([s.resample(x, how) for s in container])
    return type(container)([s.resample(x, how) for s in container])


def _make_corr_cov_func(docstring, stairs_method, assume_ones_diagonal):
    @Appender(docstring, join="\n", indents=1)
    def func(collection, lower=float("-inf"), upper=float("inf")):
        series = pd.Series(collection)
        size = series.shape[0]
        vals = np.ones(shape=(size, size))
        for i in range(size):
            for j in range(i + assume_ones_diagonal, size):
                vals[i, j] = stairs_method(series.iloc[i], series.iloc[j], lower, upper)
                vals[j, i] = vals[i, j]
        return pd.DataFrame(vals, index=series.index, columns=series.index)

    return func


corr = _make_corr_cov_func(
    docstrings.corr_docstring, Stairs.corr, assume_ones_diagonal=True
)
cov = _make_corr_cov_func(
    docstrings.cov_docstring, Stairs.cov, assume_ones_diagonal=False
)
