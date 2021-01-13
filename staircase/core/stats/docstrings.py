_std_var_example = """
Examples
--------

.. plot::
    :context: close-figs

    >>> s1.plot()
    >>> s1.{func}()
    {result1}
    >>> s1.{func}(lower=0, upper=6)
    {result2}
"""

var_example = _std_var_example.format(
    func="var", result1="0.6875", result2="0.4722222222222224",
)

std_example = _std_var_example.format(
    func="std", result1="0.82915619758885", result2="0.6871842709362769",
)

integrate_mean_example = """
Examples
--------

.. plot::
    :context: close-figs

    >>> s1.plot()
    >>> s1.{func}(3, 4.5)
    {result}
"""

integral_and_mean_example = integrate_mean_example.format(
    func="get_integral_and_mean", result="(0.5, 0.3333333333333333)",
)

integrate_example = integrate_mean_example.format(func="integrate", result="0.5",)

mean_example = integrate_mean_example.format(func="mean", result="0.3333333333333333",)

mode_example = """
Examples
--------

.. plot::
    :context: close-figs

    >>> s2.plot()
    >>> s2.mode()
    -1.0
    >>> s2.mode(0,3)
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
    >>> s1.median(2,5)
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
    >>> s1.percentile(40, lower=1.5, upper=3.5)
    0.0
"""

percentile_stairs_example = """
Examples
--------

.. plot::
    :context: close-figs

    >>> fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12,5))
    >>> s2.plot(axes[0])
    >>> axes[0].set_title("s2")
    >>> s2_percentiles = s2.percentile_stairs()
    >>> s2_percentiles.plot(axes[1])
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

    >>> s1.hist(2, 4.5)
    [-1, 0)    0.2
    [0, 1)     0.4
    [1, 2)     0.4
    dtype: float64

    >>> s1.hist(bin_edges=(-1,1,3))
    [-1, 1)    0.5
    [1, 3)     0.5
    dtype: float64

    >>> s1.hist(bin_edges=(-1, 1))
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

    >>> ecdf = s2.ecdf_stairs(1,5)
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

hist_from_ecdf_example = """
Examples
--------

.. plot::
    :context: close-figs

    >>> import staircase as sc
    >>> s1_ecdf_stairs = s1.ecdf_stairs()
    >>> fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(8,5), sharey=False, sharex=False)
    >>> for ax, title, stair_instance in zip(axes, ("s1", "s1 ecdf"), (s1, s1_ecdf_stairs)):
    ...     stair_instance.plot(ax)
    ...     ax.set_title(title)
    >>> plt.show()

    >>> sc.hist_from_ecdf(s1_ecdf_stairs)
    [-1, 0)    0.25
    [0, 1)     0.25
    [1, 2)     0.50
    dtype: float64

    >>> sc.hist_from_ecdf(s1_ecdf_stairs, bin_edges=(-1,1,3))
    [-1, 1)    0.5
    [1, 3)     0.5
    dtype: float64
"""


def _get_example(calculation):

    return {
        "mean": mean_example,
        "integrate": integrate_example,
        "integral_and_mean": integral_and_mean_example,
        "percentile": percentile_stairs_example,
        "median": median_example,
        "mode": mode_example,
        "var": var_example,
        "std": std_example,
    }[calculation]


_calc_map = {
    "integrate": "integral",
    "integral_and_mean": "integral, and the mean",
    "percentile": "x-th percentile",
    "var": "variance",
    "std": "standard deviation",
}

_see_also_map = {
    "mean": "Stairs.rolling_mean, Stairs.get_integral_and_mean, Stairs.median, Stairs.mode",
    "integrate": "Stairs.get_integral_and_mean",
    "integral_and_mean": "Stairs.integrate, Stairs.mean",
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
    return docstring.format(calc=calc, see_also=see_also, example=example,)


mean_docstring = _gen_docstring("mean")
integrate_docstring = _gen_docstring("integrate")
percentile_docstring = _gen_docstring("percentile")
median_docstring = _gen_docstring("median")
mode_docstring = _gen_docstring("mode")
var_docstring = _gen_docstring("var")
std_docstring = _gen_docstring("std")
integral_and_mean_docstring = _gen_docstring("integral_and_mean")
