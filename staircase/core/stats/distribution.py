import math

import numpy as np
import pandas as pd

import staircase as sc
from staircase.constants import inf
from staircase.core.stats import docstrings
from staircase.util import _replace_none_with_infs
from staircase.util._decorators import Appender


class Xtiles(sc.core.stairs.Stairs):

    class_name = None
    scale_factor = None

    def sample(self, x):
        return (self.limit(x, side="left") + self.limit(x, side="right")) / 2

    def __call__(self, *args, **kwargs):
        return self.sample(*args, **kwargs)

    @classmethod
    def from_ecdf(cls, ecdf):
        assert ecdf._data is not None
        return cls.new(
            initial_value=ecdf._data.index[0],
            data=pd.DataFrame(
                {"value": np.append(ecdf._data.index, ecdf._data.index[-1])},
                index=np.append(0, ecdf._get_values().values * cls.scale_factor),
            ),
        )


class Percentiles(Xtiles):

    class_name = "Percentiles"
    scale_factor = 100


class Fractiles(Xtiles):

    class_name = "Fractiles"
    scale_factor = 1

    def to_percentiles(self):

        data = self._get_values().copy()
        data.index = data.index * 100
        return Percentiles.new(initial_value=self.initial_value, data=data.to_frame())


class ECDF(sc.core.stairs.Stairs):

    class_name = "ECDF"

    @staticmethod
    def from_stairs(stairs):
        widths = np.diff(stairs._data.index.values)
        heights = stairs._get_values().values[:-1]
        ecdf_deltas = pd.Series(widths).groupby(heights).sum().rename("delta")
        deltas_sum = ecdf_deltas.sum()
        normalized_deltas = ecdf_deltas / deltas_sum

        ecdf = ECDF.new(
            initial_value=0, data=normalized_deltas.to_frame(), closed="left"
        )
        ecdf._denormalize_factor = deltas_sum
        return ecdf

    def hist(self, x="unit", closed="left", normalize=False):

        step_points = self.step_points
        if isinstance(x, str) and x == "unit":
            round_func = math.floor if closed == "left" else math.ceil
            x = range(
                round_func(min(step_points)) - (closed == "right"),
                round_func(max(step_points)) + (closed == "left") + 1,
            )

        if not isinstance(x, pd.IntervalIndex):
            x = pd.IntervalIndex.from_breaks(x, closed=closed)

        values = self.limit(x.right, side=closed) - self.limit(x.left, side=closed)
        if not normalize:
            values = values * self._denormalize_factor

        return pd.Series(
            data=values,
            index=x,
            # dtype="float64",
        )

    def percentiles(self):
        return Percentiles.from_ecdf(self)

    def fractiles(self):
        return Fractiles.from_ecdf(self)


class Dist:
    def __init__(self, stairs):
        self._ecdf = None
        self._fractiles = None
        self._stairs = stairs
        self._ecdf = ECDF.from_stairs(stairs)

    def get_ecdf(self):
        return self._ecdf

    def hist(self, x="unit", closed="left", normalize=False):
        return self._ecdf.hist(x, closed, normalize)

    def _create_fractiles(self):
        self._fractiles = Fractiles.from_ecdf(self._ecdf)

    def _ensure_fractiles(self):
        if self._fractiles is None:
            self._create_fractiles()
        return self

    def get_fractiles(self):
        return self._ensure_fractiles()._fractiles

    def get_percentiles(self):
        return self.get_fractiles().to_percentiles()

    def ecdf(self, x):
        return self._ecdf(x)

    def fractile(self, x):
        return self.get_fractiles()(x)

    def percentile(self, x):
        return self.fractile(np.divide(x, 100))


# def _get_dist(self, where=(-inf, inf)):
#     if self._data is None:  # assert here instead?
#         return None
#     if where != (-inf, inf):
#         where = _replace_none_with_infs(where)
#         clipped_stairs = self.clip(*where)  # TODO: what if where is a mask
#     else:
#         clipped_stairs = self

#     return _get_dist(clipped_stairs)


def _get_dist(self):
    if self._dist is None:
        self._dist = Dist(self)
    return self._dist


def get_percentiles(self, where=(-inf, inf)):
    where = _replace_none_with_infs(where)
    _dist = _get_dist(self) if where == (-inf, inf) else _get_dist(self.clip(*where))
    return _dist.get_percentiles()


def get_fractiles(self, where=(-inf, inf)):
    where = _replace_none_with_infs(where)
    _dist = _get_dist(self) if where == (-inf, inf) else _get_dist(self.clip(*where))
    return _dist.get_fractiles()


def percentile(self, x, where=(-inf, inf)):
    where = _replace_none_with_infs(where)
    _dist = _get_dist(self) if where == (-inf, inf) else _get_dist(self.clip(*where))
    return _dist.percentile(x)


def fractile(self, x, where=(-inf, inf)):
    where = _replace_none_with_infs(where)
    _dist = _get_dist(self) if where == (-inf, inf) else _get_dist(self.clip(*where))
    return _dist.fractile(x)


def hist(self, where=(-inf, inf), x="unit", closed="left", normalize=False):
    where = _replace_none_with_infs(where)
    _dist = _get_dist(self) if where == (-inf, inf) else _get_dist(self.clip(*where))
    return _dist.hist(x=x, closed=closed, normalize=normalize)


def get_ecdf(self, where=(-inf, inf)):
    where = _replace_none_with_infs(where)
    _dist = _get_dist(self) if where == (-inf, inf) else _get_dist(self.clip(*where))
    return _dist.get_ecdf()


def ecdf(self, x, where=(-inf, inf)):
    where = _replace_none_with_infs(where)
    _dist = _get_dist(self) if where == (-inf, inf) else _get_dist(self.clip(*where))
    return _dist.get_ecdf(x)


# # TODO: docstring
# # TODO: test
# # TODO: what's new
# @Appender(docstrings.percentile_stairs_example, join="\n", indents=1)
# def get_percentiles(self, where=(-inf, inf)):
#     """
#     Calculates a percentile function (and returns a corresponding Stairs instance)

#     This method can be used for efficiency gains if substituting for multiple calls
#     to percentile() with the same lower and upper parameters

#     Parameters
#     ----------
#     lower : int, float or pandas.Timestamp, optional
#         lower bound of the interval on which to perform the calculation
#     upper : int, float or pandas.Timestamp, optional
#         upper bound of the interval on which to perform the calculation

#     Returns
#     -------
#     :class:`Stairs`
#         An instance representing a percentile function

#     See Also
#     --------
#     Stairs.percentile
#     """
#     # TODO: what if self._data is None

#     # ecdf = ecdf_stairs(clipped_stairs)
#     # ecdf._create_values()
#     # return sc.Stairs.new(
#     #     initial_value=ecdf._data.index[0],
#     #     data=pd.DataFrame(
#     #         {"value": np.append(ecdf._data.index, ecdf._data.index[-1])},
#     #         index=np.append(0, ecdf._data["value"].values * 100),
#     #     ),
#     # )
#     return _get_dist(self, where).get_percentiles()


# # TODO: docstring
# # TODO: test
# # TODO: what's new
# @Appender(docstrings.percentile_stairs_example, join="\n", indents=1)
# def get_fractiles(self, where=(-inf, inf)):
#     return _get_dist(self, where).get_fractiles()


# # TODO: docstring
# # TODO: test
# # TODO: what's new
# @Appender(docstrings.ecdf_stairs_example, join="\n", indents=1)
# def get_ecdf(self, where=(-inf, inf)):
#     """
#     Calculates an `empirical cumulative distribution function <https://en.wikipedia.org/wiki/Empirical_distribution_function>`_
#     for the corresponding step function values (and returns the result as a Stairs instance)

#     Parameters
#     ----------
#     lower : int, float or pandas.Timestamp, optional
#         lower bound of the step-function domain on which to perform the calculation
#     upper : int, float or pandas.Timestamp, optional
#         upper bound of the step-function domain to perform the calculation

#     Returns
#     -------
#     :class:`Stairs`
#         An instance representing an empirical cumulative distribution function for the step function values

#     See Also
#     --------
#     staircase.hist_from_ecdf
#     Stairs.hist
#     """
#     return _get_dist(self, where).get_ecdf()


# # TODO: docstring
# # TODO: test
# # TODO: what's new
# @Appender(docstrings.hist_example, join="\n", indents=1)
# def hist(self, where=(-inf, inf), x="unit", closed="left", normalize=False):
#     """
#     Calculates a histogram for the corresponding step function values

#     Parameters
#     ----------
#     lower : int, float or pandas.Timestamp, optional
#         lower bound of the step-function domain on which to perform the calculation
#     upper : int, float or pandas.Timestamp, optional
#         upper bound of the step-function domain to perform the calculation
#     bin_edges : array-like of int or float, optional
#         defines the bin edges for the histogram (remember it is the step-function range that is being binned).
#         If not specified the bin_edges will be assumed to be the integers which cover the step function range
#     closed: {'left', 'right'}, default 'left'
#         determines whether the bins, which are half-open intervals, are left-closed , or right-closed

#     Returns
#     -------
#     :class:`pandas.Series`
#         A Series, with a :class:`pandas.IntervalIndex`, representing the values of the histogram

#     See Also
#     --------
#     staircase.hist_from_ecdf
#     Stairs.ecdf_stairs
#     """
#     return _get_dist(self, where).hist(x, closed, normalize)

# # TODO: docstring
# # TODO: test
# # TODO: what's new
# def percentile(self, x, where=(-inf, inf)):
#     _get_dist(self, where=(-inf, inf)).percentile(x)

# # TODO: docstring
# # TODO: test
# # TODO: what's new
# def fractile(self, x, where=(-inf, inf)):
#     _get_dist(self, where=(-inf, inf)).fractile(x)
