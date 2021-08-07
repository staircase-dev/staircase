Stairs_docstring = """
Objects of class Stairs are used to represent a :ref:`step function <intro_tutorials.stepfunction>`.

See the :ref:`Stairs API <api.Stairs>` for details of attributes and methods.

The constructor provides the ability to combine a call to :meth:`Stairs.layer` which is useful for
creating Stairs objects via the split-apply-combine pattern facilitated by :meth:`pandas.DataFrame.groubpy`

Parameters
----------
frame : :class:`pandas.DataFrame`, optional
    A long-form collection of vectors that can be assigned to named variables
start : float, array-like of floats, str, default None
    Start point(s) of the interval(s).
    A value of None is interpreted as negative infinity.
end : float, array-like of floats, [description], by default Nonestr, default None
    End points(s) of the interval(s).
    A value of None is interpreted as positive infinity.
value : float, array-like of floats, str, default None
    Value(s) of the interval(s).
    A value of None is equivalent to a value of 1.
initial_value : float, default 0
    The value of the step function at negative infinity.
closed : {"left", "right"}
    Indicates whether the half-open intervals comprising the step function should be interpreted
    as left-closed or right-closed.

Returns
-------
:class:`Stairs`

See Also
--------
Stairs.layer

Examples
--------

.. plot::
    :context: close-figs

    >>> sc.Stairs(start=1, end=2)
    <staircase.Stairs, id=2375047689840>

    >>> sc.Stairs(start=1, end=2).to_frame()
    0  -inf    1      0
    1     1    2      1
    2     2  inf      0

    >>> sc.Stairs(start=1, end=2).plot()


.. plot::
    :context: close-figs

    >>> sc.Stairs(start=[0,1], end=[2,3]).to_frame()
    0  -inf    0      0
    1     0    1      1
    2     1    2      2
    3     2    3      1
    4     3  inf      0

    >>> sc.Stairs(start=[0,1], end=[2,3]).plot()


.. plot::
    :context: close-figs

    >>> data = pd.DataFrame(
    ...     {
    ...         "start":[0,1],
    ...         "end":[2,3],
    ...         "value":[3,4],
    ...     }
    ... )

    >>> sc.Stairs(frame=data, start="start", end="end", value="value").to_frame()
    0  -inf    0      0
    1     0    1      3
    2     1    2      7
    3     2    3      4
    4     3  inf      0

    >>> sc.Stairs(frame=data, start="start", end="end", value="value").plot()
    """
