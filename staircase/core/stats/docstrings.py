# PROPERTIES -------------------------------------

_stat_docstring = """
The {calc} of the step function.

Returns
-------
float
     The {calc} of the step function

See Also
--------
{see_also}

{example}
"""

_stat_example = """
Examples
--------

.. plot::
    :context: close-figs

    >>> {stairs1}.plot(arrows=True)
    >>> {stairs1}.{func}()
    {result1}

.. plot::
    :context: close-figs

    >>> {stairs2}.plot(arrows=True)
    >>> {stairs2}.{func}()
    {result2}
"""

simple_min_example = _stat_example.format(
    func="min",
    stairs1="s1",
    result1="-1",
    stairs2="s3.clip(2,4)",
    result2="0.0",
)
simple_max_example = _stat_example.format(
    func="max",
    stairs1="s1",
    result1="1",
    stairs2="s3.clip(2,4)",
    result2="1.0",
)
integral_example = _stat_example.format(
    func="integral",
    stairs1="s1",
    result1="1",
    stairs2="s3",
    result2="0.5",
)
mean_example = _stat_example.format(
    func="mean",
    stairs1="s1",
    result1="0.25",
    stairs2="s3",
    result2="0.166666",
)
mode_example = _stat_example.format(
    func="mode", stairs1="s1", result1="1", stairs2="s4", result2="0.5"
)
median_example = _stat_example.format(
    func="median",
    stairs1="s1",
    result1="0.5",
    stairs2="s4",
    result2="0.0",
)
std_example = _stat_example.format(
    func="std",
    stairs1="s1",
    result1="0.829156",
    stairs2="s3",
    result2="0.897527",
)
var_example = _stat_example.format(
    func="var",
    stairs1="s1",
    result1="0.6875",
    stairs2="s3",
    result2="0.805555",
)


def _get_example(calculation):

    return {
        "mean": mean_example,
        "integral": integral_example,
        # "percentile": percentile_prop_example,
        "median": median_example,
        "mode": mode_example,
        "var": var_example,
        "std": std_example,
    }[calculation]


_calc_map = {
    "integral": "integral",
    "percentile": "x-th percentile",
    "var": "variance",
    "std": "standard deviation",
}

_see_also_map = {
    "mean": "Stairs.integral, Stairs.rolling_mean",
    "integral": "Stairs.mean",
    "percentile": "Stairs.median, Stairs.fractile",
    "median": "Stairs.percentile, Stairs.fractile",
    "mode": "Stairs.mean, Stairs.median",
    "var": "Stairs.std",
    "std": "Stairs.var",
}


def _gen_docstring(calculation):

    calc = _calc_map.get(calculation, calculation)
    see_also = _see_also_map[calculation]
    example = _get_example(calculation)

    if property:
        docstring = _stat_docstring

    return docstring.format(
        calc=calc,
        see_also=see_also,
        example=example,
    )


mean_docstring = _gen_docstring("mean")
integral_docstring = _gen_docstring("integral")
median_docstring = _gen_docstring("median")
mode_docstring = _gen_docstring("mode")
var_docstring = _gen_docstring("var")
std_docstring = _gen_docstring("std")


# AGG ------------------------------------------------------------------

agg_docstring = """
Returns the aggregation of the step function defined over a domain.

Parameters
----------
name : {'max', 'min', 'mode', 'median', 'mean', 'integral', 'var', 'std'}
    The name of the function which which to perform the aggregation.
where : tuple or list of length two, optional
    Indicates the domain interval over which to evaluate the step function.
    Default is (-sc.inf, sc.inf) or equivalently (None, None).
closed : {'both', 'left', 'right', 'neither'}, optional
    Note that this parameter will only change the result for 'min' or 'max' aggregations.
    Indicates whether the interval defined by *where* is closed on both sides, left-closed,
    right-closed, or neither.  Default value is taken from the *closed* attribute of the step function.
    The default values will be used if *closed=None* is used.

Returns
-------
float

See Also
--------
Stairs.max, Stairs.min, Stairs.mode, Stairs.median, Stairs.mean, Stairs.integral, Stairs.var, Stairs.std

Examples
--------
.. plot::
    :context: close-figs

    >>> s1.plot(arrows=True)

>>> s1.agg(where=(1,4), name="min")
0

>>> s1.agg(where=(1,4), name="min", closed="both")
-1

>>> s1.agg(where=(1,4), name="integral")
2.0
"""


# VALUE SUMS -----------------------------------------------------

value_sums_docstring = """
Characterises the distribution of step function values with a series of their sums.

The result is a :class:`pandas.Series`, indexed by the values of a the step function.
The values of the series are the lengths of the intervals whose value is equal
to the corresponding index.

This method is analagous to :func:`pandas.Series.value_counts` over a continous domain.

Parameters
----------
dropna : bool, default True
    Indicates whether to include intervals where the step function is undefined
group : bool, default True
    Indicates whether to group the index values together into a unique index.

Returns
-------
:class:`pandas.Series`

Examples
--------
.. plot::
    :context: close-figs

    >>> s1.plot()

>>> s1.value_sums()
-1    1
 0    1
 1    2
dtype: int64

.. plot::
    :context: close-figs

    >>> s3.plot()

    >>> s3.value_sums(dropna=False)
    -1.0    1.0
     0.0    0.5
     1.0    1.5
     NaN    1.0
    dtype: float64
"""


# MIN MAX VALUES -------------------------------------------------

_min_max_values_in_range_docstring = """
Returns the {calc} of the step function defined over a domain.

Parameters
----------
where : tuple or list of length two, optional
    Indicates the domain interval over which to evaluate the step function.
    Default is (-sc.inf, sc.inf) or equivalently (None, None).
closed: {{'both', 'left', 'right', 'neither'}}, optional
    Indicates whether the interval defined by *where* is closed on both sides, left-closed,
    right-closed, or neither.  Default value is taken from the *closed* attribute of the step function.
    The default values will be used if *closed=None* is used.

Returns
-------
{return_val}

See Also
--------
{see_also}

{example}
"""

values_in_range_example = """
Examples
--------
.. plot::
    :context: close-figs

    >>> s1.plot(arrows=True)

>>> s1.values_in_range()
array([-1,  0,  1], dtype=int64)

>>> s1.values_in_range((1,4))
array([0,  1], dtype=int64)

>>> s1.values_in_range((1,4), closed='both')
array([-1,  0,  1], dtype=int64)
"""

min_example = """
Examples
--------
.. plot::
    :context: close-figs

    >>> from staircase.api import min
    >>> s1.plot(arrows=True)

>>> min(s1)
-1

>>> min(s1, (1,4))
0

>>> min(s1, where=(1,4), closed='both')
-1
"""

max_example = """
Examples
--------
.. plot::
    :context: close-figs

    >>> from staircase.stairs import max
    >>> s1.plot(arrows=True)

>>> max(s1)
-1

>>> max(s1, (4,5))
0

>>> max(s1, where=(4,5), closed='both')
0
"""


values_in_range_docstring = _min_max_values_in_range_docstring.format(
    calc="range (i.e. values)",
    return_val=r":class:`numpy.ndarray`\n    A numpy array of unique values",
    see_also="Stairs.min, Stairs.max",
    example=values_in_range_example,
)


min_docstring = _min_max_values_in_range_docstring.format(
    calc="minimum",
    return_val="float",
    see_also="Stairs.min, staircase.stairs.max",
    example=min_example,
)


max_docstring = _min_max_values_in_range_docstring.format(
    calc="minimum",
    return_val="float",
    see_also="Stairs.max, staircase.stairs.min",
    example=max_example,
)


hist_example = """
Examples
--------

.. plot::
    :context: close-figs

    >>> s1.plot(arrows=True)

>>> s1.hist()
[-1, 0)    1.0
[0, 1)     1.0
[1, 2)     2.0
dtype: float64

>>> s1.hist(closed="right")
(-2, -1]    1.0
(-1, 0]     1.0
(0, 1]      2.0
dtype: float64

>>> s1.hist(bins=[-1,1,2])
[-1, 1)    2.0
[1, 2)     2.0
dtype: float64

>>> s1.hist(bins=[-1,1,2], stat="frequency")
[-1, 1)    1.0
[1, 2)     2.0
dtype: float64

>>> s1.hist(bins=[-1,1,2], stat="density")
[-1, 1)    0.333333
[1, 2)     0.333333
dtype: float64

>>> s1.hist(bins=[-1,1,2], stat="probability")
[-1, 1)    0.5
[1, 2)     0.5
dtype: float64
"""

ecdf_example = """
Examples
--------

.. plot::
    :context: close-figs

    >>> s2.plot(arrows=True)

.. plot::
    :context: close-figs

    >>> s2.ecdf
    <staircase.ECDF, id=1872531189136>

    >>> s2.ecdf.plot()
    >>> plt.show()

>>> print(f'{ecdf(0):.2%} of values for s2 are less than or equal to 0')
75.00% of values, for s2 between 1 and 5, are less than or equal to 0

>>> print(f'{ecdf(0, how="left"):.2%} of values for s2 are strictly less than 0')
50.00% of values, for s2 between 1 and 5, are strictly less than 0

>>> print(f'{ecdf(0.2) - ecdf(-1):.2%} of values for s2 are in (-1, 0.2]')
25.00% of values, for s2 between 1 and 5, are in (-1, 0.2]

>>> print(f'{ecdf(0.2, how="left") - ecdf(-1, how="left"):.2%} of values for s2 are in [-1, 0.2)')
75.00% of values, for s2 between 1 and 5, are in [-1, 0.2)
"""

# ecdf_stairs_example = """
# Examples
# --------

# .. plot::
#     :context: close-figs

#     >>> s2.plot()

# .. plot::
#     :context: close-figs

#     >>> s2.ecdf
#     <staircase.ECDF, id=1872531189136>

#     >>> s2.ecdf.plot()
#     >>> plt.show()


#     >>> print(f'{ecdf(0):.2%} of values, for s2 between 1 and 5, are less than or equal to 0')
#     75.00% of values, for s2 between 1 and 5, are less than or equal to 0

#     >>> print(f'{ecdf(0, how="left"):.2%} of values, for s2 between 1 and 5, are strictly less than 0')
#     50.00% of values, for s2 between 1 and 5, are strictly less than 0

#     >>> print(f'{ecdf(0.2) - ecdf(-1):.2%} of values, for s2 between 1 and 5, are in (-1, 0.2]')
#     25.00% of values, for s2 between 1 and 5, are in (-1, 0.2]

#     >>> print(f'{ecdf(0.2, how="left") - ecdf(-1, how="left"):.2%} of values, for s2 between 1 and 5, are in [-1, 0.2)')
#     75.00% of values, for s2 between 1 and 5, are in [-1, 0.2)
# """


# _prop_docstring = """
# The {calc} of the step function values.

# Parameters
# ----------


# Returns
# -------
# float
#      The {calc} of the step function

# See Also
# --------
# {see_also}

# {example}
# """

# percentile_prop_example = prop_example.format(
#     func1="percentile",
#     stairs1="s1",
#     result1="<staircase.Percentiles, id=1872507658000>",
#     stairs2="s2",
#     result2="-1.0",
# )


# func_example = """
# Examples
# --------

# .. plot::
#     :context: close-figs

#     >>> {stairs1}.plot()
#     >>> {stairs1}.{func}(where=(2, 4.5))
#     {result1}

#     >>> {stairs2}.plot()
#     >>> {stairs2}.{func}(where=(None, 4.5))
#     {result2}
# """

# integral_func_example = func_example.format(
#     func="integral", stairs1="s1", result1="1", stairs2="s3", result2="0.5",
# )
# mean_func_example = func_example.format(
#     func="mean", stairs1="s1", result1="0.25", stairs2="s3", result2="0.166666",
# )
# mode_func_example = func_example.format(
#     func="mode", stairs1="s1", result1="1", stairs2="s4", result2="0.5"
# )
# median_func_example = func_example.format(
#     func="median", stairs1="s1", result1="0.5", stairs2="s4", result2="0.0",
# )
# std_func_example = func_example.format(
#     func="std", stairs1="s1", result1="0.829156", stairs2="s3", result2="0.897527",
# )
# var_func_example = func_example.format(
#     func="var", stairs1="s1", result1="0.6875", stairs2="s3", result2="0.805555",
# )
# percentile_func_example = func_example.format(
#     func1="percentile",
#     stairs1="s1",
#     result1="<staircase.Percentiles, id=1872507658000>",
#     stairs2="s2",
#     result2="-1.0",
# )
