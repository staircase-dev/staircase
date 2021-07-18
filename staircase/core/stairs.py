"""
Staircase
==============

Staircase is a MIT licensed library, written in pure-Python, for
modelling step functions. See :ref:`Getting Started <getting_started>` for more information.
"""


import numpy as np
import pandas as pd
from pandas.plotting import register_matplotlib_converters

from staircase import plotting
from staircase.constants import inf

# from staircase.docstrings import stairs_class as examples
from staircase.docstrings import examples
from staircase.util import _replace_none_with_infs

# from staircase.docstrings.decorator import @Appender
from staircase.util._decorators import Appender

register_matplotlib_converters()


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
    """
    An instance of a Stairs class is used to represent a :ref:`step function <getting_started.step_function>`.

    The Stairs class encapsulates a `SortedDict <http://www.grantjenks.com/docs/sortedcontainers/sorteddict.html>`_
    which is used to hold the points at which the step function changes, and by how much.

    See the :ref:`Stairs API <api.Stairs>` for details of methods.
    """

    class_name = "Stairs"

    # TODO: docstring
    # TODO: test
    # TODO: what's new
    def __init__(
        self,
        frame=None,
        start=None,
        end=None,
        value=None,
        initial_value=0,
        closed="left",
    ):
        """
        Initialise a Stairs instance.

        Parameters
        ----------
        init_value : float, default 0
            The value of the step function at negative infinity.

        Returns
        -------
        :class:`Stairs`
        """
        assert frame is None or isinstance(frame, pd.DataFrame)
        self._data = None
        self._valid_deltas = False
        self._valid_values = False
        self._masked = False
        self._closed = closed
        self.initial_value = initial_value
        self._dist = None
        self._integral_and_mean = None

        if any([x is not None for x in (start, end, value)]):
            # value = 1 if value is None else value
            self.layer_frame(frame, start, end, value)

    # DO NOT IMPLEMENT __len__ or __iter__, IT WILL CAUSE ISSUES WITH PANDAS SERIES PRETTY PRINTING

    @classmethod
    def new(cls, initial_value, data, closed="left"):
        new_instance = cls(closed=closed)
        new_instance.initial_value = initial_value
        new_instance._data = data
        new_instance._valid_deltas = False if data is None else "delta" in data.columns
        new_instance._valid_values = False if data is None else "value" in data.columns
        return new_instance

    # TODO: docstring
    # TODO: test
    # TODO: what's new
    def is_masked(self):
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

    # def _ensure_values(self):
    #     if not self._valid_values:
    #         self._create_values()
    #     return self

    # def _ensure_deltas(self):
    #     if not self._valid_deltas:
    #         self._create_deltas()
    #     return self

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

    # TODO: docstring
    # TODO: test
    # TODO: what's new
    def step_changes(self):  # TODO: alias as deltas?
        """
        Returns a pandas Series of key, value pairs of indicating where step changes occur in the step function, and the change in value

        Returns
        -------
        :class:`pandas.Series`

        See Also
        --------
        Stairs.number_of_steps

        Examples
        --------

        .. plot::
            :context: close-figs

            >>> s1.plot()
            >>> s1.step_changes()
            1    1
            2   -1
            3    1
            4   -2
            5    1
            dtype: int64
        """
        return self._get_deltas().copy()

    # TODO: docstring
    # TODO: test
    # TODO: what's new
    def step_values(self):  # TODO: new in v2.0, needs docstring
        return self._get_values().copy()

    # TODO: docstring
    # TODO: test
    # TODO: what's new
    def step_points(self):
        if self._data is None:
            return np.array([])
        return self._data.index.values

    # TODO: docstring
    # TODO: test
    # TODO: what's new
    @Appender(examples.number_of_steps_example, join="\n", indents=2)
    def number_of_steps(self):
        """
        Calculates the number of step changes

        Returns
        -------
        int

        See Also
        --------
        Stairs.step_changes
        Stairs.step_points
        """
        return len(self.step_points())

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

    # TODO: docstring
    # TODO: test
    # TODO: what's new
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
        new_instance = Stairs.new(
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
        if self.initial_value == 1 and self.number_of_steps() == 0:
            return True
        return False

    # TODO: docstring
    # TODO: test
    # TODO: what's new
    @Appender(examples.describe_example, join="\n", indents=2)
    def describe(self, where=(-inf, inf), percentiles=(25, 50, 75)):
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
        where = _replace_none_with_infs(where)
        percentilestairs = self.get_percentiles(where)
        return pd.Series(
            {
                **{
                    "unique": percentilestairs.clip(0, 100).number_of_steps() - 1,
                    "mean": self.mean(where),
                    "std": self.std(where),
                    "min": self.min(where),
                },
                **{f"{perc}%": percentilestairs(perc) for perc in percentiles},
                **{"max": self.max(where),},
            }
        )

    # TODO: docstring
    # TODO: test
    # TODO: what's new
    @Appender(examples.shift_example, join="\n", indents=2)
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
        return Stairs.new(
            initial_value=self.initial_value,
            data=self._data.set_index(self._data.index + delta),
        )

    # TODO: docstring
    # TODO: test
    # TODO: what's new
    @Appender(examples.diff_example, join="\n", indents=2)
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

    # TODO: docstring
    # TODO: test
    # TODO: what's new
    @Appender(examples.rolling_mean_example, join="\n", indents=2)
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
        where = _replace_none_with_infs(where)
        assert len(window) == 2, "Window should be a listlike object of length 2."
        left_delta, right_delta = window
        lower, upper = where
        clipped = self.clip(lower, upper)
        step_points = clipped._data.index  # TODO: what if data is none
        sample_points = pd.Index.union(
            step_points - left_delta, step_points - right_delta,
        )
        ii = pd.IntervalIndex.from_arrays(
            sample_points + left_delta, sample_points + right_delta
        )
        s = pd.Series(clipped.slice(ii).mean().values, index=sample_points,)
        if lower != -inf:
            s = s.loc[s.index >= lower - left_delta]
        if upper != inf:
            s = s.loc[s.index <= upper - right_delta]
        return s

    # TODO: docstring
    # TODO: test
    # TODO: what's new
    # this name changed in v2.0
    def to_frame(self):
        """
        Returns a pandas.DataFrame with columns 'start', 'end' and 'value'

        The rows of the dataframe can be interpreted as the interval definitions
        which make up the step function.

        Returns
        -------
        :class:`pandas.DataFrame`
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
