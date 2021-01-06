import math
import warnings

import numpy as np
from pandas import IntervalIndex, Series

from staircase.util._decorators import Appender
from staircase.core.stats import docstrings
import staircase as sc

warnings.simplefilter("default")


@Appender(docstrings.percentile_stairs_example, join="\n", indents=1)
def percentile_stairs(self, lower=float("-inf"), upper=float("inf")):
    """
    Calculates a percentile function (and returns a corresponding Stairs instance)

    This method can be used for efficiency gains if substituting for multiple calls
    to percentile() with the same lower and upper parameters

    Parameters
    ----------
    lower : int, float or pandas.Timestamp, optional
        lower bound of the interval on which to perform the calculation
    upper : int, float or pandas.Timestamp, optional
        upper bound of the interval on which to perform the calculation

    Returns
    -------
    :class:`Stairs`
        An instance representing a percentile function

    See Also
    --------
    Stairs.percentile
    """
    temp_df = self.clip(lower, upper).to_dataframe()

    assert (
        temp_df.shape[0] >= 3
    ), "Step function composed only of infinite length intervals.  Provide bounds by 'lower' and 'upper' parameters"

    temp_df = (
        temp_df.iloc[1:-1]
        .assign(duration=lambda df: df.end - df.start)
        .groupby("value")
        .sum()
        .assign(duration=lambda df: np.cumsum(df.duration / df.duration.sum()))
        .assign(duration=lambda df: df.duration.shift())
        .fillna(0)
    )
    percentile_step_func = sc.Stairs()
    for start, end, value in zip(
        temp_df.duration.values,
        np.append(temp_df.duration.values[1:], 1),
        temp_df.index,
    ):
        percentile_step_func.layer(start * 100, end * 100, value)
    percentile_step_func[100] = 0
    return percentile_step_func


def percentile_Stairs(self, lower=float("-inf"), upper=float("inf")):
    """Deprecated.  Use Stairs.percentile_stairs."""
    warnings.warn(
        "Stairs.percentile_Stairs will be deprecated in version 2.0.0, use Stairs.percentile_stairs instead",
        PendingDeprecationWarning,
    )
    return percentile_stairs(self, lower, upper)


@Appender(docstrings.ecdf_stairs_example, join="\n", indents=1)
def ecdf_stairs(self, lower=float("-inf"), upper=float("inf")):
    """
    Calculates an `empirical cumulative distribution function <https://en.wikipedia.org/wiki/Empirical_distribution_function>`_
    for the corresponding step function values (and returns the result as a Stairs instance)

    Parameters
    ----------
    lower : int, float or pandas.Timestamp, optional
        lower bound of the step-function domain on which to perform the calculation
    upper : int, float or pandas.Timestamp, optional
        upper bound of the step-function domain to perform the calculation

    Returns
    -------
    :class:`Stairs`
        An instance representing an empirical cumulative distribution function for the step function values

    See Also
    --------
    staircase.hist_from_ecdf
    Stairs.hist
    """

    def _switch_first_key_to_zero(d):
        d[0] = d.get(0, 0) + d.pop(float("-inf"))
        return d

    _ecdf = _switch_first_key_to_zero(
        percentile_stairs(self, lower, upper)._sorted_dict.copy()
    )

    return sc.Stairs().layer(
        np.cumsum(list(_ecdf.values())[:-1]), None, np.diff(list(_ecdf.keys())) / 100
    )


@Appender(docstrings.hist_from_ecdf_example, join="\n", indents=1)
def hist_from_ecdf(ecdf, bin_edges=None, closed="left"):
    """
    Calculates a histogram from a Stairs instance corresponding to an
    `empirical cumulative distribution function <https://en.wikipedia.org/wiki/Empirical_distribution_function>`_.

    Such ecdf stair instances are returned from :meth:`Stairs.ecdf_stairs`.  This function predominantly exists
    to allow users to store the result of a ecdf stairs instance locally, and experiment with bin_edges without
    requiring the recalculation of the ecdf.

    Parameters
    ----------
    ecdf : :class:`Stairs`
        lower bound of the step-function domain on which to perform the calculation
    bin_edges : int, float, optional
        defines the bin edges for the histogram (it is the domain of the ecdf that is being binned).
        If not specified the bin_edges will be assumed to be the integers which cover the domain of the ecdf
    closed: {'left', 'right'}, default 'left'
        determines whether the bins, which are half-open intervals, are left-closed , or right-closed

    Returns
    -------
    :class:`pandas.Series`
        A Series, with a :class:`pandas.IntervalIndex`, representing the values of the histogram

    See Also
    --------
    Stairs.hist
    Stairs.ecdf_stairs
    """
    if bin_edges is None:
        round_func = math.floor if closed == "left" else math.ceil
        bin_edges = range(
            round_func(min(ecdf.step_changes().keys())) - (closed == "right"),
            round_func(max(ecdf.step_changes().keys())) + (closed == "left") + 1,
        )
    return Series(
        data=[
            ecdf(c2, how=closed) - ecdf(c1, how=closed)
            for c1, c2 in zip(bin_edges[:-1], bin_edges[1:])
        ],
        index=IntervalIndex.from_tuples(
            [(c1, c2) for c1, c2 in zip(bin_edges[:-1], bin_edges[1:])], closed=closed
        ),
        dtype="float64",
    )


@Appender(docstrings.hist_example, join="\n", indents=1)
def hist(self, lower=float("-inf"), upper=float("inf"), bin_edges=None, closed="left"):
    """
    Calculates a histogram for the corresponding step function values

    Parameters
    ----------
    lower : int, float or pandas.Timestamp, optional
        lower bound of the step-function domain on which to perform the calculation
    upper : int, float or pandas.Timestamp, optional
        upper bound of the step-function domain to perform the calculation
    bin_edges : array-like of int or float, optional
        defines the bin edges for the histogram (remember it is the step-function range that is being binned).
        If not specified the bin_edges will be assumed to be the integers which cover the step function range
    closed: {'left', 'right'}, default 'left'
        determines whether the bins, which are half-open intervals, are left-closed , or right-closed

    Returns
    -------
    :class:`pandas.Series`
        A Series, with a :class:`pandas.IntervalIndex`, representing the values of the histogram

    See Also
    --------
    staircase.hist_from_ecdf
    Stairs.ecdf_stairs
    """
    _ecdf = ecdf_stairs(self, lower, upper)
    return hist_from_ecdf(_ecdf, bin_edges, closed)
