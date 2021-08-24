import numpy as np
import pandas as pd

from staircase.core.arrays import docstrings
from staircase.core.stairs import Stairs
from staircase.util._decorators import Appender


# TODO: docstring
# TODO: test
# TODO: what's new
@Appender(docstrings.aggregate_example, join="\n", indents=1)
def _aggregate(collection, func):
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

    See Also
    --------
    staircase.mean, staircase.median, staircase.min, staircase.max
    """
    collection = pd.Series(collection).values
    index = pd.Index(np.unique(np.concatenate([s.step_points for s in collection])))
    return Stairs._new(
        initial_value=func([s.initial_value for s in collection]),
        data=pd.Series(
            func([s.sample(index) for s in collection], axis=0),
            index=index,
            name="value",
        ).to_frame(),
    )._remove_redundant_step_points()


# TODO: docstring
# TODO: test
# TODO: what's new
@Appender(docstrings.mean_docstring, join="\n", indents=1)
def _mean(collection):
    return _aggregate(collection, np.mean)


# TODO: docstring
# TODO: test
# TODO: what's new
@Appender(docstrings.median_docstring, join="\n", indents=1)
def _median(collection):
    return _aggregate(collection, np.median)


# TODO: docstring
# TODO: test
# TODO: what's new
@Appender(docstrings.min_docstring, join="\n", indents=1)
def _min(collection):
    return _aggregate(collection, np.min)


# TODO: docstring
# TODO: test
# TODO: what's new
@Appender(docstrings.max_docstring, join="\n", indents=1)
def _max(collection):
    return _aggregate(collection, np.max)


# TODO: docstring
# TODO: test
# TODO: what's new
def _sum(collection):
    return _aggregate(collection, np.sum)
