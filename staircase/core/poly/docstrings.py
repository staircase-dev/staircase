sample_docstring = """
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

Examples
--------

.. plot::
    :context: close-figs

    >>> s1.plot()
    >>> s1(3.5)
    1
    >>> s1([1, 2, 4.5, 6])
    [1, 0, -1, 0]
    >>> s1([1, 2, 4.5, 6], how="left")
    [0, 1, -1, 0]
    >>> s1([1, 2, 4.5], aggfunc="mean", window=(-0.5, 0.5))
    [0.5, 0.5, -1.0]
    >>> s1([1, 2, 4.5], aggfunc="max", window=(-0.5, 0.5))
    [1, 1, -1]
    >>> s1([1, 2, 4.5], aggfunc="max", window=(-0.5, 0.5), lower_how="left")
    [1, 1, 1]
    >>> s1([1, 2, 4.5], aggfunc="max", window=(-0.5, 0.5), upper_how="right")
    [1, 1, 0]
"""

resample_docstring = """
Evaluates the value of the step function at one, or more, points and
creates a new Stairs instance whose step changes occur at a subset of these
points.  The new instance and self have the same values when evaluated at x.

Parameters
----------
x : int, float or vector data
    Values at which to evaluate the function
how : {'left', 'right'}, default 'right'
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
:class:`Stairs`

See Also
--------
staircase.resample

Examples
--------

.. plot::
    :context: close-figs

    >>> stair_list = [s1, s1.resample([1.5,2.5,4,4.5])]
    >>> fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12,5), sharey=True, sharex=True)
    >>> for ax, title, stair_instance in zip(axes, ("s1", "s1 resampled"), stair_list):
    ...     stair_instance.plot(ax)
    ...     ax.set_title(title)
"""

layer_docstring = """
Changes the value of the step function.


Parameters
----------
start : int, float or vector data, optional
    start time(s) of the interval(s)
end : int, float or vector data, optional
    end time(s) of the interval(s)
value: int, float or vector data, optional
    value(s) of the interval(s)

Returns
-------
:class:`Stairs`
    The current instance is returned to facilitate method chaining

Examples
--------

.. plot::
    :context: close-figs

    >>> import staircase as sc
    ... (sc.Stairs()
    ...     .layer(1,3)
    ...     .layer(4,5,-2)
    ...     .plot()
    ... )

.. plot::
    :context: close-figs

    >>> import pandas as pd
    >>> import staircase as sc
    >>> data = pd.DataFrame({"starts":[1,4,5.5],
    ...                      "ends":[3,5,7],
    ...                      "values":[-1,2,-3]})
    >>> data
       starts  ends  values
    0     1.0     3      -1
    1     4.0     5       2
    2     5.5     7      -3
    >>> (sc.Stairs(1.5)
    ...     .layer(data["starts"], data["ends"], data["values"])
    ...     .plot()
    ... )
"""

step_changes_docstring = """
Returns a dictionary of key, value pairs of indicating where step changes occur in the step function, and the change in value

Returns
-------
dictionary

See Also
--------
Stairs.number_of_steps

Examples
--------

.. plot::
    :context: close-figs

    >>> s1.plot()
    >>> s1.step_changes()
    {1: 1, 2: -1, 3: 1, 4: -2, 5: 1}
"""


values_in_range_docstring = """
Returns the range of the step function as a set of discrete values.

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
set of floats

Examples
--------

.. plot::
    :context: close-figs

    >>> s2.plot()
    >>> s2.values_in_range()
    {-1.0, 0.0, 0.5}
    >>> s2.values_in_range(lower=2)
    {-1.0, 0.0}
    >>> s2.values_in_range(lower=2, lower_how="left")
    {-1.0, 0.0, 0.5}
    >>> s2.values_in_range(upper=2)
    {0.0, 0.5}
    >>> s2.values_in_range(upper=3, upper_how="right")
    {-1.0, 0.0, 0.5}

"""

clip_docstring = """
Returns a copy of *self* which is zero-valued everywhere outside of [lower, upper)

Parameters
----------
lower : int, float or pandas.Timestamp
    lower bound of the interval
upper : int, float or pandas.Timestamp
    upper bound of the interval

Returns
-------
:class:`Stairs`
    Returns a copy of *self* which is zero-valued everywhere outside of [lower, upper)

Examples
--------

.. plot::
    :context: close-figs

    >>> fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12,5))
    >>> s1.plot(axes[0])
    >>> s1.clip(2,4).plot(axes[1])
    >>> s1.clip(2,4).mean()
    0.5

"""
