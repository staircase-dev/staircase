_std_var_example = """
Examples
--------

.. plot::
    :context: close-figs

    >>> s1.plot()
    >>> s1.{func}()
    {result1}
    >>> s1.{func}(where=(0, 6))
    {result2}
"""

var_example = _std_var_example.format(
    func="var", result1="0.6875", result2="0.4722222222222224",
)

std_example = _std_var_example.format(
    func="std", result1="0.82915619758885", result2="0.6871842709362769",
)

integral_mean_example = """
Examples
--------

.. plot::
    :context: close-figs

    >>> s1.plot()
    >>> s1.{func}(where=(3, 4.5))
    {result}
"""

integral_and_mean_example = integral_mean_example.format(
    func="get_integral_and_mean", result="(0.5, 0.3333333333333333)",
)

integral_example = integral_mean_example.format(func="integral", result="0.5",)

mean_example = integral_mean_example.format(func="mean", result="0.3333333333333333",)

mode_example = """
Examples
--------

.. plot::
    :context: close-figs

    >>> s2.plot()
    >>> s2.mode()
    -1.0
    >>> s2.mode(where=(0,3))
    0.5
"""


median_example = """
Examples
--------

.. plot::
    :context: close-figs

    >>> s1.plot()
    >>> s1.median()
    0.5
    >>> s1.median(where=(2,5))
    0.0
"""

percentile_example = """
Examples
--------

.. plot::
    :context: close-figs

    >>> s1.plot()
    >>> s1.percentile(70)
    1.0
    >>> s1.percentile(25)
    -0.5
    >>> s1.percentile(40, where=(1.5, 3.5))
    0.0
"""

percentile_stairs_example = """
Examples
--------

.. plot::
    :context: close-figs

    >>> fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12,5))
    >>> s2.plot(ax=axes[0])
    >>> axes[0].set_title("s2")
    >>> s2_percentiles = s2.get_percentiles()
    >>> s2_percentiles.plot(ax=axes[1])
    >>> axes[0].set_title("s2 percentiles")
    >>> s2_percentiles(55)
    0.0
    >>> s2_percentiles(75)
    0.5
"""

hist_example = """
Examples
--------

.. plot::
    :context: close-figs

    >>> s1.plot()

.. plot::
    :context: close-figs

    >>> s1.hist()
    [-1, 0)    0.25
    [0, 1)     0.25
    [1, 2)     0.50
    dtype: float64

    >>> s1.hist(closed='right')
    (-2, -1]    0.25
    (-1, 0]     0.25
    (0, 1]      0.50
    dtype: float64

    >>> s1.hist(where=(2, 4.5))
    [-1, 0)    0.2
    [0, 1)     0.4
    [1, 2)     0.4
    dtype: float64

    >>> s1.hist(x=(-1,1,3))
    [-1, 1)    0.5
    [1, 3)     0.5
    dtype: float64

    >>> s1.hist(x=(-1, 1))
    [-1, 1)    0.5
    dtype: float64
"""

ecdf_stairs_example = """
Examples
--------

.. plot::
    :context: close-figs

    >>> s2.plot()

.. plot::
    :context: close-figs

    >>> ecdf = s2.get_ecdf(1,5)
    >>> ecdf.plot()
    >>> plt.show()


    >>> print(f'{ecdf(0):.2%} of values, for s2 between 1 and 5, are less than or equal to 0')
    75.00% of values, for s2 between 1 and 5, are less than or equal to 0

    >>> print(f'{ecdf(0, how="left"):.2%} of values, for s2 between 1 and 5, are strictly less than 0')
    50.00% of values, for s2 between 1 and 5, are strictly less than 0

    >>> print(f'{ecdf(0.2) - ecdf(-1):.2%} of values, for s2 between 1 and 5, are in (-1, 0.2]')
    25.00% of values, for s2 between 1 and 5, are in (-1, 0.2]

    >>> print(f'{ecdf(0.2, how="left") - ecdf(-1, how="left"):.2%} of values, for s2 between 1 and 5, are in [-1, 0.2)')
    75.00% of values, for s2 between 1 and 5, are in [-1, 0.2)
"""


def _get_example(calculation):

    return {
        "mean": mean_example,
        "integral": integral_example,
        "integral_and_mean": integral_and_mean_example,
        "percentile": percentile_stairs_example,
        "median": median_example,
        "mode": mode_example,
        "var": var_example,
        "std": std_example,
    }[calculation]


_calc_map = {
    "integral": "integral",
    "integral_and_mean": "integral, and the mean",
    "percentile": "x-th percentile",
    "var": "variance",
    "std": "standard deviation",
}

_see_also_map = {
    "mean": "Stairs.rolling_mean, Stairs.get_integral_and_mean, Stairs.median, Stairs.mode",
    "integral": "Stairs.get_integral_and_mean",
    "integral_and_mean": "Stairs.integral, Stairs.mean",
    "percentile": "Stairs.median, Stairs.percentile_stairs",
    "median": "Stairs.mean, Stairs.mode, Stairs.percentile, Stairs.percentile_stairs",
    "mode": "Stairs.mean, Stairs.median",
    "var": "Stairs.std",
    "std": "Stairs.var",
}

_common_docstring = """
Calculates the {{calc}} of the step function.

Parameters
----------
lower : int, float or pandas.Timestamp
    lower bound of the interval on which to perform the calculation
upper : int, float or pandas.Timestamp
    upper bound of the interval on which to perform the calculation
{{extra_params}}
Returns
-------
{return_type}
     The {{calc}} of the step function

See Also
--------
{{see_also}}

{{example}}
"""

_float_return_docstring = _common_docstring.format(return_type="float")
_tuple_return_docstring = _common_docstring.format(return_type="tuple")


def _gen_docstring(calculation):

    calc = _calc_map.get(calculation, calculation)
    see_also = _see_also_map[calculation]
    example = _get_example(calculation)

    if calculation == "integral_and_mean":
        docstring = _tuple_return_docstring
    else:
        docstring = _float_return_docstring

    if calculation in ("mean", "integral", "integral_and_mean"):
        extra_params = "\n".join(
            [
                "datetime : bool, default False",
                "    if True performs calculations using datetime.timedelta instead of pandas.Timedelta",
                "",
            ]
        )
    else:
        extra_params = ""

    return docstring.format(
        calc=calc, extra_params=extra_params, see_also=see_also, example=example,
    )


mean_docstring = _gen_docstring("mean")
integral_docstring = _gen_docstring("integral")
percentile_docstring = _gen_docstring("percentile")
median_docstring = _gen_docstring("median")
mode_docstring = _gen_docstring("mode")
var_docstring = _gen_docstring("var")
std_docstring = _gen_docstring("std")
integral_and_mean_docstring = _gen_docstring("integral_and_mean")


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
"""
