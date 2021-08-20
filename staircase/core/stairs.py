"""
staircase
==============

staircase is a MIT licensed library, written in pure-Python, for
modelling step functions. See :ref:`Getting Started <getting_started>` for more information.
"""


import numpy as np
import pandas as pd

from staircase import docstrings, plotting
from staircase.constants import inf
from staircase.core import stats
from staircase.core.accessor import CachedAccessor
from staircase.plotting import docstrings as plot_docstrings
from staircase.plotting.accessor import PlotAccessor
from staircase.util import _replace_none_with_infs
from staircase.util._decorators import Appender


def _make_deltas_from_vals(init_val, vals):
    if not np.isnan(vals).any():
        result = pd.Series(np.diff((np.append([init_val], vals.values))))
    else:
        temp = pd.Series(np.append([init_val], vals.values))
        result = pd.Series.add(
            temp[pd.notnull(temp)].diff(), temp[pd.isnull(temp)], fill_value=0
        )[1:]
    if np.isnan(init_val):
        result.iloc[0] = vals.iloc[0]
    result.index = vals.index
    return result


def _make_vals_from_deltas(init_val, deltas):
    base = 0 if np.isnan(init_val) else init_val
    return deltas.cumsum() + base


class Stairs:

    class_name = "Stairs"

    @Appender(docstrings.Stairs_docstring, join="\n", indents=2)
    def __init__(
        self,
        frame=None,
        start=None,
        end=None,
        value=None,
        initial_value=0,
        closed="left",
    ):
        assert frame is None or isinstance(frame, pd.DataFrame)
        self._data = None
        self._valid_deltas = False
        self._valid_values = False
        self._masked = False
        self._closed = closed
        self.initial_value = initial_value
        self._clear_cache()

        if any([x is not None for x in (start, end, value)]):
            self.layer(start, end, value, frame)

    def _clear_cache(self):
        self.dist._reset()
        self._integral_and_mean = None

    @classmethod
    def _new(cls, initial_value, data, closed="left"):
        new_instance = cls(closed=closed)
        new_instance.initial_value = initial_value
        new_instance._data = data
        new_instance._valid_deltas = False if data is None else "delta" in data.columns
        new_instance._valid_values = False if data is None else "value" in data.columns
        return new_instance

    def _has_na(self):
        return np.isnan(self._data.values).any() or np.isnan(self.initial_value)

    def _create_values(self):
        assert self._valid_deltas
        self._data.loc[:, "value"] = _make_vals_from_deltas(
            self.initial_value, self._data["delta"]
        )
        self._valid_values = True
        return self

    def _create_deltas(self):
        assert self._valid_values
        self._data.loc[:, "delta"] = _make_deltas_from_vals(
            self.initial_value, self._data["value"]
        )
        self._valid_deltas = True
        return self

    def _get_deltas(self):
        if self._data is None:
            return pd.Series(dtype="float64")
        if not self._valid_deltas:
            self._create_deltas()
        return self._data["delta"]

    def _get_values(self):
        if self._data is None:
            return pd.Series(dtype="float64")
        if not self._valid_values:
            self._create_values()
        return self._data["value"]

    @property
    def closed(self):
        return self._closed

    @property
    @Appender(stats.docstrings.ecdf_example, join="\n", indents=2)
    def ecdf(self):
        """
        Calculates an `empirical cumulative distribution function <https://en.wikipedia.org/wiki/Empirical_distribution_function>`_
        for the corresponding step function values.

        Returns
        -------
        :class:`ECDF`

        See Also
        --------
        Stairs.hist
        Stairs.percentile
        Stairs.fractile
        """
        return self.dist.ecdf

    @property
    def fractile(self):
        return self.dist.fractile

    @property
    def percentile(self):
        return self.dist.percentile

    @Appender(stats.docstrings.hist_example, join="\n", indents=2)
    def hist(self, bins="unit", closed="left", stat="sum"):
        """
        Calculates histogram data for the corresponding step function values

        Parameters
        ----------
        bins : "unit", sequence or :class:`pandas.IntervalIndex`
            If *bins* is "unit" then the histogram bins will have unit length and cover the range
            of step function values.  If *bins* is a sequence, it defines a monotonically
            increasing array of bin edges.  If *bins* are defined by :class:`pandas.IntervalIndex`
            they should be non-overlapping and monotonic increasing.
        closed : {"left", "right"}, default "left"
            Indicates whether the histogram bins are left-closed right-open
            or right-closed left-open. Only relevant when *bins* is not a :class:`pandas.IntervalIndex`
        stat : {"sum", "frequency", "density", "probability"}, default "sum"
            The aggregate statistic to compute in each bin.  Inspired by :meth:`seaborn.histplot` stat parameter.
                - ``sum`` the magnitude of observations
                - ``frequency`` values of the histogram are divided by the corresponding bin width
                - ``density`` normalises values of the histogram so that the area is 1
                - ``probability`` normalises values so that the histogram values sum to 1

        Returns
        -------
        :class:`pandas.DataFrame`
        """
        return self.dist.hist(bins=bins, closed=closed, stat=stat)

    def quantiles(self, q):
        """
        Returns an array of q-quantiles.

        Quantiles are cut points which divide a distribution into continuous intervals with equal probabilities.
        The 2-quantile is more commonly known as the median.
        The 4-quantiles are more commonly known as quartiles.
        The 100-quantiles are more commonly known as percentiles.

        Parameters
        ----------
        q : int

        Returns
        -------
        :class:`numpy.ndarray` of floats

        See Also
        --------
        Stairs.percentile, Stairs.fractile

        Examples
        --------

        .. plot::
            :context: close-figs

            >>> sf = sc.Stairs().layer([0,1,2,3,4], [6,7,8,9,10])
            >>> fig, axes = plt.subplots(ncols=2, figsize=(7,3), sharex=True)
            >>> sf.plot(axes[0])
            >>> axes[0].set_title("sf")
            >>> sf.ecdf.plot(axes[1])
            >>> axes[1].set_title("sf")

        >>> sf.quantiles(4)
        array([2., 3., 4.])
        """
        return self.dist.quantiles(q)

    @Appender(stats.docstrings.simple_max_example, join="\n", indents=2)
    def max(self):
        """
        The maximum of the step function.

        Returns
        -------
        float
            The maximum of the step function

        See Also
        --------
        Stairs.min, Stairs.values_in_range
        """
        return stats.max(self)

    @Appender(stats.docstrings.simple_min_example, join="\n", indents=2)
    def min(self):
        """
        The minimum of the step function.

        Returns
        -------
        float
            The minimum of the step function

        See Also
        --------
        Stairs.max, Stairs.values_in_range
        """
        return stats.min(self)

    plot = CachedAccessor("plot", PlotAccessor)

    @property
    def step_changes(self):  # TODO: alias as deltas?
        """
        A pandas Series of key, value pairs of indicating where step changes occur in the step function, and the change in value

        Returns
        -------
        :class:`pandas.Series`

        See Also
        --------
        Stairs.step_points
        Stairs.step_values
        Stairs.number_of_steps

        Examples
        --------

        .. plot::
            :context: close-figs

            >>> s1.plot()
            >>> s1.step_changes
            1    1
            2   -1
            3    1
            4   -2
            5    1
            dtype: int64
        """
        return self._get_deltas().copy()

    @property
    def step_values(self):
        """
        A pandas Series of key, value pairs of indicating where step changes occur in the step function, and
        the limit of the step function when it approaches these points from the right.

        Returns
        -------
        :class:`pandas.Series`

        See Also
        --------
        Stairs.step_points
        Stairs.step_changes
        Stairs.number_of_steps

        Examples
        --------

        .. plot::
            :context: close-figs

            >>> s1.plot()
            >>> s1.step_values
            1    1
            2    0
            3    1
            4   -1
            5    0
            dtype: int64
        """
        return self._get_values().copy()

    # TODO: test
    @property
    def step_points(self):
        """
        A numpy arrauy of domain values indicating where step changes occur in the step function.

        Returns
        -------
        :class:`numpy.ndarray`

        See Also
        --------
        Stairs.step_values
        Stairs.step_changes
        Stairs.number_of_steps

        Examples
        --------

        .. plot::
            :context: close-figs

            >>> s1.plot()
            >>> s1.step_values
            array([1, 2, 3, 4, 5], dtype=int64)
        """
        if self._data is None:
            return np.array([])
        return self._data.index.values

    @Appender(docstrings.examples.number_of_steps_example, join="\n", indents=2)
    @property
    def number_of_steps(self):
        """
        Calculates the number of step changes

        Returns
        -------
        int

        See Also
        --------
        Stairs.step_changes
        Stairs.step_values
        Stairs.step_points
        """
        return len(self.step_points)

    def _remove_redundant_step_points(self):

        # preferred over values method
        def remove_via_deltas():
            remove_index = (
                self._data["delta"].isna() & self._data["delta"].isna().shift()
            ) | (self._data["delta"] == 0)
            self._data = self._data.loc[~remove_index]

        # do we just make deltas and then run above method?
        def remove_via_values():
            remove_index = (
                self._data["value"].isna() & self._data["value"].isna().shift()
            ) | (self._data["value"] == self._data["value"].shift())
            if (self._data["value"].iloc[0] == self.initial_value) or (
                pd.isnull(self._data.loc[:, "value"].iloc[0])
                and pd.isnull(self.initial_value)
            ):
                remove_index.iloc[0] = True
            self._data = self._data.loc[~remove_index]

        if self._data is not None:
            if self._valid_deltas:
                remove_via_deltas()
            elif self._valid_values:
                remove_via_values()
            else:
                assert False, "no deltas or values valid!"
            if len(self._data) == 0:
                self._data = None

        return self

    def copy(self):
        """
        Returns a deep copy of this Stairs instance

        Returns
        -------
        :class:`Stairs`
        """
        new_instance = Stairs._new(
            initial_value=self.initial_value,
            data=self._data.copy() if self._data is not None else None,
        )
        return new_instance

    def __bool__(self):
        """
        Return True if and only if step function has a value of 1 everywhere.

        Returns
        -------
        boolean
        """
        if self.initial_value == 1 and self.number_of_steps == 0:
            return True
        return False

    @Appender(docstrings.examples.describe_example, join="\n", indents=2)
    def describe(self, where=(-inf, inf), percentiles=(25, 50, 75)):
        """
        Generate descriptive statistics for the step function values over a specified domain.

        Parameters
        ----------
        where : tuple or list of length two, optional
            Indicates the domain interval over which to evaluate the step function.
            Default is (-sc.inf, sc.inf) or equivalently (None, None).
        percentiles: array-like of float, default [25, 50, 70]
            The percentiles to include in output.  Numbers should be in the range 0 to 100.

        Returns
        -------
        :class:`pandas.Series`

        See Also
        --------
        Stairs.mean, Stairs.std, Stairs.min, Stairs.percentile, Stairs.max
        """
        where = _replace_none_with_infs(where)
        stairs = self if where == (-inf, inf) else self.clip(*where)

        return pd.Series(
            {
                **{
                    "unique": stairs.percentile.clip(0, 100).number_of_steps - 1,
                    "mean": stairs.mean,
                    "std": stairs.std,
                    "min": stairs.min,
                },
                **{f"{perc}%": stairs.percentile(perc) for perc in percentiles},
                **{"max": stairs.max},
            }
        )

    @Appender(docstrings.examples.shift_example, join="\n", indents=2)
    def shift(self, delta):
        """
        Returns a stairs instance corresponding to a horizontal translation by delta

        If delta is positive the corresponding step function is moved right.
        If delta is negative the corresponding step function is moved left.

        Parameters
        ----------
        delta : int, float or pandas.Timedelta
            the amount by which to translate.  A pandas.Timedelta is only valid when using dates.
            If using dates and delta is an int or float, then it is interpreted as a number of hours.

        Returns
        -------
        :class:`Stairs`

        See Also
        --------
        Stairs.diff
        """
        if self._data is None:
            return Stairs(initial_value=self.initial_value)
        return Stairs._new(
            initial_value=self.initial_value,
            data=self._data.set_index(self._data.index + delta),
        )

    @Appender(docstrings.examples.diff_example, join="\n", indents=2)
    def diff(self, delta):
        """
        Returns a stairs instance corresponding to the difference between the step function corresponding to *self*
        and the same step-function translated by delta.

        Parameters
        ----------
        delta : int, float or pandas.Timedelta
            the amount by which to translate.  A pandas.Timestamp is only valid when using dates.
            If using dates and delta is an int or float, then it is interpreted as a number of hours.

        Returns
        -------
        :class:`Stairs`

        See Also
        --------
        Stairs.shift
        """
        return self - self.shift(delta)

    @Appender(docstrings.examples.rolling_mean_example, join="\n", indents=2)
    def rolling_mean(self, window=(0, 0), where=(-inf, inf)):
        """
        Returns coordinates defining rolling mean

        The rolling mean of a step function is a continous piece-wise linear function, hence it can
        be described by a sequence of x,y coordinates which mark where function changes gradient.  These
        x,y coordinates are returned as a :class:`pandas.Series` which could then be used with
        :meth:`matplotlib.axes.Axes.plot`, or equivalent, to visualise.

        A rolling mean requires a window around a point x (referred to as the focal point) to be defined.
        In this implementation the window is defined by two values paired into an array-like parameter called *window*.
        These two numbers are the distance from the focal point to the left boundary of the window, and the right boundary
        of the window respectively.  This allows for trailing windows, leading windows and everything between
        (including a centred window).

        Parameters
        ----------
        window : array-like of int, float or pandas.Timedelta
            should be length of 2. Defines distances from focal point to window boundaries.
        where : tuple or list of length two, optional
            Indicates the domain interval over which to evaluate the step function.
            Default is (-sc.inf, sc.inf) or equivalently (None, None).

        Returns
        -------
        :class:`pandas.Series`

        See Also
        --------
        Stairs.mean
        """
        where = _replace_none_with_infs(where)
        assert len(window) == 2, "Window should be a listlike object of length 2."
        left_delta, right_delta = window
        lower, upper = where
        clipped = self.clip(lower, upper)
        step_points = clipped._data.index  # TODO: what if data is none
        sample_points = pd.Index.union(
            step_points - left_delta,
            step_points - right_delta,
        )
        ii = pd.IntervalIndex.from_arrays(
            sample_points + left_delta, sample_points + right_delta
        )
        s = pd.Series(
            clipped.slice(ii).mean().values,
            index=sample_points,
        )
        if lower != -inf:
            s = s.loc[s.index >= lower - left_delta]
        if upper != inf:
            s = s.loc[s.index <= upper - right_delta]
        return s

    def to_frame(self):
        """
        Returns a pandas.DataFrame with columns 'start', 'end' and 'value'

        The rows of the dataframe can be interpreted as the interval definitions
        which make up the step function.

        Returns
        -------
        :class:`pandas.DataFrame`

        Examples
        --------

        .. plot::
            :context: close-figs

            >>> s1.plot()

        >>> s1.to_frame()
        0  -inf    1      0
        1     1    2      1
        2     2    3      0
        3     3    4      1
        4     4    5     -1
        5     5  inf      0
        """
        if self._data is None:
            starts = [-inf]
            ends = [inf]
            values = [self.initial_value]
        else:
            if not self._valid_values:
                self._create_values()
            step_points = self._data.index
            starts = [-inf] + step_points.to_list()
            ends = step_points.to_list() + [inf]
            values = np.append(self.initial_value, self._data["value"].values)
        return pd.DataFrame({"start": starts, "end": ends, "value": values})

    def pipe(self, func, *args, **kwargs):
        """
        Applies func and returns the result.

        Primarily intended to facilitate method chaining.

        Parameters
        ----------
        func : callable
            Function to apply to *self*.
        args : , optional
            Positional arguments passed into *func*.
        kwargs : mapping, optional
            A dictionary of keyword arguments passed into *func*.

        Returns
        -------
        object
            return type of *func*
        """
        return func(self, *args, **kwargs)

    def __str__(self):
        """
        Return str(self)
        """
        return f"<staircase.{self.class_name}, id={id(self)}>"

    def __repr__(self):
        """
        Return string representation of Stairs
        """
        return str(self)

    def __call__(self, *args, **kwargs):
        return self.sample(*args, **kwargs)


def _add_operations():
    from staircase.core import layering, ops, sampling, slicing, stats

    ops.add_operations(Stairs)
    stats.add_methods(Stairs)
    plotting.add_methods(Stairs)
    sampling.add_methods(Stairs)
    layering.add_methods(Stairs)
    slicing.add_methods(Stairs)
