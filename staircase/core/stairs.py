"""
Staircase
==============

Staircase is a MIT licensed library, written in pure-Python, for
modelling step functions. See :ref:`Getting Started <getting_started>` for more information.
"""

# uses https://pypi.org/project/sortedcontainers/
from sortedcontainers import SortedDict, SortedSet
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import pytz
from staircase.defaults import default
from staircase.docstrings.decorator import add_doc, append_doc
from staircase.docstrings import stairs_class as SC_docs
from staircase.core import ops, poly, stats
from staircase.core.tools.datetimes import (
    origin,
    _convert_date_to_float,
    _convert_float_to_date,
)

register_matplotlib_converters()


class Stairs:
    """
    An instance of a Stairs class is used to represent a :ref:`step function <getting_started.step_function>`.

    The Stairs class encapsulates a `SortedDict <http://www.grantjenks.com/docs/sortedcontainers/sorteddict.html>`_
    which is used to hold the points at which the step function changes, and by how much.

    See the :ref:`Stairs API <api.Stairs>` for details of methods.
    """

    def __init__(self, value=0, use_dates=default, tz=default):
        """
        Initialise a Stairs instance.

        Parameters
        ----------
        value : float, default 0
            The value of the step function at negative infinity.
        use_dates: bool, default False
            Allows the step function to be defined with `Pandas.Timestamp <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timestamp.html>`_.

        Returns
        -------
        :class:`Stairs`
        """
        if use_dates == default:
            use_dates = default.get_default("use_dates")
        if tz == default:
            tz = default.get_default("tz")

        self._sorted_dict = SortedDict()
        if isinstance(value, dict):
            self._sorted_dict = SortedDict(value)
        else:
            self._sorted_dict = SortedDict()
            self._sorted_dict[float("-inf")] = value
        self.use_dates = use_dates
        self.tz = tz
        self.cached_cumulative = None

        # runtime._add_operations(self, use_dates)

        self._get = self._sorted_dict.get
        self._items = self._sorted_dict.items
        self._keys = self._sorted_dict.keys
        self._sorted_dict_values = self._sorted_dict.values
        self._pop = self._sorted_dict.pop
        self._len = self._sorted_dict.__len__
        self._popitem = self._sorted_dict.popitem

    # DO NOT IMPLEMENT __len__ or __iter__, IT WILL CAUSE ISSUES WITH PANDAS SERIES PRETTY PRINTING

    def __getitem__(self, *args, **kwargs):
        """
        f'{dict.__getitem__.__doc__}'
        """
        return self._sorted_dict.__getitem__(*args, **kwargs)

    def __setitem__(self, key, value):
        """
        f'{dict.__setitem__.__doc__}'
        """
        self._sorted_dict.__setitem__(key, value)

    def copy(self, deep=None):
        """
        Returns a deep copy of this Stairs instance

        Parameters
        ----------
        deep : None
            Dummy parameter to keep pandas satisfied.

        Returns
        -------
        :class:`Stairs`
        """
        new_instance = Stairs(use_dates=self.use_dates, tz=self.tz)
        for key, value in self._items():
            new_instance[key] = value
        return new_instance

    @classmethod
    def from_cumulative(cls, cumulative, use_dates=False, tz=None):
        return cls(
            dict(
                zip(
                    cumulative.keys(),
                    np.insert(
                        np.diff(list(cumulative.values())),
                        0,
                        [next(iter(cumulative.values()))],
                    ),
                )
            ),
            use_dates,
            tz,
        )

    def plot(self, ax=None, **kwargs):
        """
        Makes a step plot representing the finite intervals belonging to the Stairs instance.

        Uses matplotlib as a backend.

        Parameters
        ----------
        ax : :class:`matplotlib.axes.Axes`, default None
            Allows the axes, on which to plot, to be specified
        **kwargs
            Options to pass to :function: `matplotlib.pyplot.step`

        Returns
        -------
        :class:`matplotlib.axes.Axes`
        """
        if ax is None:
            _, ax = plt.subplots()

        cumulative = self._cumulative()
        if self.use_dates:
            register_matplotlib_converters()
            x = list(cumulative.keys())
            if len(x) > 1:
                x[0] = (
                    x[1] - 0.00001
                )  # first element would otherwise be -inf which can't be plotted
                ax.step(
                    _convert_float_to_date(x, self.tz),
                    list(cumulative.values()),
                    where="post",
                    **kwargs,
                )
        else:
            ax.step(cumulative.keys(), cumulative.values(), where="post", **kwargs)
        return ax

    def _cumulative(self):
        if self.cached_cumulative is None:
            self.cached_cumulative = SortedDict(
                zip(self._keys(), np.cumsum(self._sorted_dict_values()))
            )
        return self.cached_cumulative

    def _reduce(self):
        to_remove = [key for key, val in self._items()[1:] if val == 0]
        for key in to_remove:
            self._pop(key)
        return self

    def __bool__(self):
        """
        Return True if and only if step function has a value of 1 everywhere.

        Returns
        -------
        boolean
        """
        if self.number_of_steps() >= 2:
            return float((~self).integrate()) < 0.0000001
        return dict(self._sorted_dict) == {float("-inf"): 1}

    @append_doc(SC_docs.describe_example)
    def describe(
        self, lower=float("-inf"), upper=float("inf"), percentiles=(25, 50, 75)
    ):
        """
        Generate descriptive statistics.

        Parameters
        ----------
        lower : int, float or pandas.Timestamp
            lower bound of the interval on which to perform the calculation
        upper : int, float or pandas.Timestamp
            upper bound of the interval on which to perform the calculation
        percentiles: array-like of float, default [25, 50, 70]
            The percentiles to include in output.  Numbers should be in the range 0 to 100.

        Returns
        -------
        :class:`pandas.Series`

        See Also
        --------
        Stairs.mean, Stairs.std, Stairs.min, Stairs.percentile, Stairs.max
        """
        percentilestairs = self.percentile_stairs(lower, upper)
        return pd.Series(
            {
                **{
                    "unique": percentilestairs.clip(0, 100).number_of_steps() - 1,
                    "mean": self.mean(lower, upper),
                    "std": self.std(lower, upper),
                    "min": self.min(lower, upper),
                },
                **{f"{perc}%": percentilestairs(perc) for perc in percentiles},
                **{"max": self.max(lower, upper),},
            }
        )

    @append_doc(SC_docs.cov_example)
    def cov(self, other, lower=float("-inf"), upper=float("inf"), lag=0, clip="pre"):
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
        if lag != 0:
            assert clip in ["pre", "post"]
            if clip == "pre" and upper != float("inf"):
                upper = upper - lag
            other = other.shift(-lag)
        return (self * other).mean(lower, upper) - self.mean(lower, upper) * other.mean(
            lower, upper
        )

    @append_doc(SC_docs.corr_example)
    def corr(self, other, lower=float("-inf"), upper=float("inf"), lag=0, clip="pre"):
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
        if lag != 0:
            assert clip in ["pre", "post"]
            if clip == "pre" and upper != float("inf"):
                upper = upper - lag
            other = other.shift(-lag)
        return self.cov(other, lower, upper) / (
            self.std(lower, upper) * other.std(lower, upper)
        )

    @append_doc(SC_docs.min_example)
    def min(
        self,
        lower=float("-inf"),
        upper=float("inf"),
        lower_how="right",
        upper_how="left",
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
        return min(self.values_in_range(lower, upper, lower_how, upper_how))

    @append_doc(SC_docs.max_example)
    def max(
        self,
        lower=float("-inf"),
        upper=float("inf"),
        lower_how="right",
        upper_how="left",
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
        return max(self.values_in_range(lower, upper, lower_how, upper_how))

    @append_doc(SC_docs.shift_example)
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
        if isinstance(delta, pd.Timedelta):
            assert self.use_dates, "delta is of type pandas.Timedelta, expected float"
            delta = delta.total_seconds() / 3600
        return Stairs(
            dict(
                zip((key + delta for key in self._keys()), self._sorted_dict_values())
            ),
            self.use_dates,
            self.tz,
        )

    @append_doc(SC_docs.diff_example)
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

    @append_doc(SC_docs.rolling_mean_example)
    def rolling_mean(self, window=(0, 0), lower=float("-inf"), upper=float("inf")):
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

        If *lower* or *upper* is specified then only coordinates corresponding to windows contained within
        [lower, upper] are included.

        Parameters
        ----------
        window : array-like of int, float or pandas.Timedelta
            should be length of 2. Defines distances from focal point to window boundaries.
        lower : int, float, pandas.Timestamp, or None, default None
            used to indicate the lower bound of the domain of the calculation
        upper : int, float, pandas.Timestamp, or None, default None
            used to indicate the upper bound of the domain of the calculation

        Returns
        -------
        :class:`pandas.Series`

        See Also
        --------
        Stairs.mean
        """
        assert len(window) == 2, "Window should be a listlike object of length 2."
        left_delta, right_delta = window
        clipped = self.clip(lower, upper)
        if clipped.use_dates:
            left_delta = pd.Timedelta(left_delta, "h")
            right_delta = pd.Timedelta(right_delta, "h")
        change_points = list(
            SortedSet(
                [c - right_delta for c in clipped.step_changes().keys()]
                + [c - left_delta for c in clipped.step_changes().keys()]
            )
        )
        s = pd.Series(
            clipped.sample(change_points, aggfunc="mean", window=window),
            index=change_points,
        )
        if lower != float("-inf"):
            s = s.loc[s.index >= lower - left_delta]
        if upper != float("inf"):
            s = s.loc[s.index <= upper - right_delta]
        return s

    def to_dataframe(self):
        """
        Returns a pandas.DataFrame with columns 'start', 'end' and 'value'

        The rows of the dataframe can be interpreted as the interval definitions
        which make up the step function.

        Returns
        -------
        :class:`pandas.DataFrame`
        """
        starts = self._keys()
        ends = self._keys()[1:]
        if self.use_dates:
            starts = [pd.NaT] + _convert_float_to_date(np.array(starts[1:]), self.tz)
            ends = _convert_float_to_date(np.array(ends), self.tz) + [pd.NaT]
        else:
            ends.append(float("inf"))
        values = self._cumulative().values()
        df = pd.DataFrame(
            {"start": list(starts), "end": list(ends), "value": list(values)}
        )  # bugfix for pandas 1.1
        return df

    @append_doc(SC_docs.number_of_steps_example)
    def number_of_steps(self):
        """
        Calculates the number of step changes

        Returns
        -------
        int

        See Also
        --------
        Stairs.step_changes
        """
        return len(self._keys()) - 1

    def __str__(self):
        """
        Return str(self)
        """
        tzinfo = f", tz={self.tz}" if self.use_dates else ""
        return f"<staircase.Stairs, id={id(self)}, dates={self.use_dates}{tzinfo}>"

    def __repr__(self):
        """
        Return string representation of Stairs
        """
        return str(self)

    def __call__(self, *args, **kwargs):
        return self.sample(*args, **kwargs)


poly.add_methods(Stairs)
ops.add_operations(Stairs)
stats.add_methods(Stairs)
