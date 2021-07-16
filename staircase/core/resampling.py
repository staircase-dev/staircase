import pandas as pd

import staircase as sc
from staircase.docstrings import examples
from staircase.util._decorators import Appender


# TODO: docstring
# TODO: test
# TODO: what's new
# capable of single or vector
# @Appender(examples.sample_example, join="\n", indents=1)
def resample(self, x):
    """
    Evaluates the value of the step function at one, or more, points and
    creates a new Stairs instance whose step changes occur at a subset of these
    points.  The new instance and self have the same values when evaluated at x.

    Parameters
    ----------
    x : int, float or vector data
        Values at which to evaluate the function
    side : {'left', 'right'}, default 'right'
        If points where step changes occur do not coincide with x then this parameter
        has no effect.  Where a step change occurs at a point given by x, this parameter
        determines if the step function is evaluated at the interval to the left, or the right.

    Returns
    -------
    float, or numpy array of floats

    See Also
    --------
    Stairs.cut
    staircase.sample
    """
    return sc.Stairs.new(
        initial_value=self.initial_value,
        data=pd.DataFrame({"value": self.sample(x, include_index=True)}),
    )._remove_redundant_step_points()


# TODO: docstring
# TODO: test
# TODO: what's new
# @Appender(examples.limit_example, join="\n", indents=1)
def from_limits(self, x, side):
    """
    Evaluates the value of the step function at one, or more, points.

    The results of this function should be considered as :math:`\\lim_{x \\to z^{-}} f(x)`
    or :math:`\\lim_{x \\to z^{+}} f(x)`, when side = 'left' or how = 'right' respectively. See
    :ref:`A note on interval endpoints<getting_started.interval_endpoints>` for an explanation.

    The function can be called using parentheses.  See example below.

    Parameters
    ----------
    x : int, float or vector data
        Values at which to evaluate the function
    side : {'left', 'right'}, default 'right'
        If points where step changes occur do not coincide with x then this parameter
        has no effect.  Where a step change occurs at a point given by x, this parameter
        determines if the step function is evaluated at the interval to the left, or the right.

    Returns
    -------
    float, or numpy array of floats

    See Also
    --------
    Stairs.cut
    staircase.sample
    """
    return sc.Stairs.new(
        initial_value=self.initial_value,
        data=pd.DataFrame({"value": self.limit(x, side=side, include_index=True)}),
    )._remove_redundant_step_points()


# TODO: docstring
# TODO: test
# TODO: what's new
# @Appender(examples.cut_example, join="\n", indents=1)
def from_cuts(self, x, aggfunc, closed="left", map_to="mid"):
    """
    Evaluates the value of the step function at one, or more, points.

    This method can be used to directly sample values of the corresponding step function at the points
    provided, or alternatively calculate aggregations over some window around each point.  The first of these
    is performed when *aggfunc* is None.

    If *aggfunc* is None then the results of this function should be considered as :math:`\\lim_{x \\to z^{-}} f(x)`
    or :math:`\\lim_{x \\to z^{+}} f(x)`, when how = 'left' or how = 'right' respectively. See
    :ref:`A note on interval endpoints<getting_started.interval_endpoints>` for an explanation.

    If *aggfunc* is not None then a window, around each point x (referred to as the focal point), over which to aggregate is required.
    The window is defined by two values paired into an array-like parameter called *window*.
    These two scalars are the distance from the focal point to the left boundary of the window, and the right boundary
    of the window respectively.

    The function can be called using parentheses.  See example below.

    Parameters
    ----------
    x : int, float or vector data
        Values at which to evaluate the function
    how : {'left', 'right'}, default 'right'
        Only relevant if *aggfunc* is None.
        If points where step changes occur do not coincide with x then this parameter
        has no effect.  Where a step changes occurs at a point given by x, this parameter
        determines if the step function is evaluated at the interval to the left, or the right.
    aggfunc: {'mean', 'median', 'mode', 'max', 'min', 'std', None}.  Default None.
        A string corresponding to the aggregating function
    window : array-like of int, float or pandas.Timedelta, optional
        Only relevant if *aggfunc* is not None.  Should be length of 2. Defines distances from focal point to window boundaries.
    lower_how: {'left', 'right'}, default 'right'
        Only relevant if *aggfunc* is not None.  Determines how the left window boundary should be evaluated.
        If 'left' then :math:`\\lim_{x \\to lower_how^{-}} f(x)` is included in the window.
    upper_how: {'left', 'right'}, default 'left'
        Only relevant if *aggfunc* is not None.  Determines how the right window boundary should be evaluated.
        If 'right' then :math:`\\lim_{x \\to upper_how^{+}} f(x)` is included in the window.

    Returns
    -------
    float, or list of floats

    See Also
    --------
    staircase.sample
    """
    values = self.cut(x, aggfunc=aggfunc, closed=closed)
    if map_to == "left":
        values.index = values.index.left
    elif map_to == "right":
        values.index = values.index.right
    else:
        values.index = values.index.mid
    return sc.Stairs.new(
        initial_value=self.initial_value,
        data=pd.DataFrame({"value": values}),
    )._remove_redundant_step_points()


# TODO: docstring
# TODO: test
# TODO: what's new
def from_aggs(self, x, window, aggfunc, closed="left"):
    """
    Evaluates the value of the step function at one, or more, points.

    This method can be used to directly sample values of the corresponding step function at the points
    provided, or alternatively calculate aggregations over some window around each point.  The first of these
    is performed when *aggfunc* is None.

    If *aggfunc* is None then the results of this function should be considered as :math:`\\lim_{x \\to z^{-}} f(x)`
    or :math:`\\lim_{x \\to z^{+}} f(x)`, when how = 'left' or how = 'right' respectively. See
    :ref:`A note on interval endpoints<getting_started.interval_endpoints>` for an explanation.

    If *aggfunc* is not None then a window, around each point x (referred to as the focal point), over which to aggregate is required.
    The window is defined by two values paired into an array-like parameter called *window*.
    These two scalars are the distance from the focal point to the left boundary of the window, and the right boundary
    of the window respectively.

    The function can be called using parentheses.  See example below.

    Parameters
    ----------
    x : int, float or vector data
        Values at which to evaluate the function
    how : {'left', 'right'}, default 'right'
        Only relevant if *aggfunc* is None.
        If points where step changes occur do not coincide with x then this parameter
        has no effect.  Where a step changes occurs at a point given by x, this parameter
        determines if the step function is evaluated at the interval to the left, or the right.
    aggfunc: {'mean', 'median', 'mode', 'max', 'min', 'std', None}.  Default None.
        A string corresponding to the aggregating function
    window : array-like of int, float or pandas.Timedelta, optional
        Only relevant if *aggfunc* is not None.  Should be length of 2. Defines distances from focal point to window boundaries.
    lower_how: {'left', 'right'}, default 'right'
        Only relevant if *aggfunc* is not None.  Determines how the left window boundary should be evaluated.
        If 'left' then :math:`\\lim_{x \\to lower_how^{-}} f(x)` is included in the window.
    upper_how: {'left', 'right'}, default 'left'
        Only relevant if *aggfunc* is not None.  Determines how the right window boundary should be evaluated.
        If 'right' then :math:`\\lim_{x \\to upper_how^{+}} f(x)` is included in the window.

    Returns
    -------
    float, or list of floats

    See Also
    --------
    staircase.sample
    """
    values = self.agg(x, window=window, aggfunc=aggfunc, closed=closed)
    return sc.Stairs.new(
        initial_value=self.initial_value,
        data=pd.DataFrame({"value": values}),
    )._remove_redundant_step_points()


def add_methods(cls):
    cls.resample = resample
    cls.from_cuts = from_cuts
    cls.from_limits = from_limits
    cls.from_aggs = from_aggs
