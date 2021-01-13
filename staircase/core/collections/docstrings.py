sample_footer = """
    >>> sc.sample({"s1":s1, "s2":s2}, [1, 1.5, 2.5, 4])
       points   key   value
    0     1.0    s1     1.0
    1     1.5    s1     1.0
    2     2.5    s1     0.0
    3     4.0    s1    -1.0
    4     1.0    s2     0.5
    5     1.5    s2     0.5
    6     2.5    s2     0.0
    7     4.0    s2    -1.0
"""

_plot_titles_map = {
    "sample": ["s1", "s2"],
    "min": ["s1", "s2", "sc.min([s1,s2])"],
    "max": ["s1", "s2", "sc.max([s1,s2])"],
    "mean": ["s1", "s2", "sc.mean([s1,s2])"],
    "median": ["s1", "s2", "sc.median([s1,s2])"],
    "aggregate": ["s1", "s2", "sc.aggregate([s1,s2], np.std)"],
}

_example = """
Examples
--------

.. plot::
    :context: close-figs

    >>> stair_list = [{plots}]
    >>> fig, axes = plt.subplots(nrows=1, ncols={ncols}, figsize=(17,5), sharey=True, sharex=True)
    >>> for ax, title, stair_instance in zip(axes, ({plot_titles}), stair_list):
    ...     stair_instance.plot(ax)
    ...     ax.set_title(title)
"""


def _gen_example(operation):
    plot_titles = _plot_titles_map[operation]
    ncols = len(plot_titles)
    plots = ", ".join(plot_titles)
    return _example.format(plots=plots, ncols=ncols, plot_titles=plot_titles)


sample_example = _gen_example("sample") + sample_footer
min_example = _gen_example("min")
max_example = _gen_example("max")
mean_example = _gen_example("mean")
median_example = _gen_example("median")
aggregate_example = _gen_example("aggregate")

_corr_cov_header = """
Examples
--------

.. plot::
    :context: close-figs

    >>> import staircase as sc
    >>> pd.Series([s1, s2, s1+s2])
    0    <staircase.Stairs, id=2452772382088, dates=False>
    1    <staircase.Stairs, id=2452772381320, dates=False>
    2    <staircase.Stairs, id=2452772893512, dates=False>
    dtype: object
"""

cov_example = (
    _corr_cov_header
    + """
    >>> sc.cov(pd.Series([s1, s2, s1+s2], index=['s1', 's2', 's1+s2']))
                  s1         s2      s1+s2
    s1      0.687500   0.140496   0.652893
    s2      0.140496   0.471074   0.611570
    s1+ s2  0.652893   0.611570   1.264463

    >>> sc.cov([s1, s2, s1+s2])
              0          1          2
    0  0.687500   0.140496   0.652893
    1  0.140496   0.471074   0.611570
    2  0.652893   0.611570   1.264463
"""
)

corr_example = (
    _corr_cov_header
    + """
    >>> sc.corr(pd.Series([s1, s2, s1+s2], index=['s1', 's2', 's1+s2']))
                  s1         s2      s1+s2
    s1      1.000000   0.246878   0.700249
    s2      0.246878   1.000000   0.792407
    s1+ s2  0.700249   0.792407   1.000000

    >>> sc.corr([s1, s2, s1+s2])
              0          1          2
    0  1.000000   0.246878   0.700249
    1  0.246878   1.000000   0.792407
    2  0.700249   0.792407   1.000000
"""
)


def _get_example(calculation):

    return {
        "min": min_example,
        "max": max_example,
        "mean": mean_example,
        "median": median_example,
        "corr": corr_example,
        "cov": cov_example,
    }[calculation]


_see_also_map = {
    "min": "staircase.aggregate, staircase.mean, staircase.median, staircase.max",
    "max": "staircase.aggregate, staircase.mean, staircase.median, staircase.min",
    "mean": "staircase.aggregate, staircase.median, staircase.min, staircase.max",
    "median": "staircase.aggregate, staircase.mean, staircase.min, staircase.max",
    "corr": "Stairs.corr, staircase.cov",
    "cov": "Stairs.cov, staircase.corr",
}

_calc_map = {
    "min": "minimum",
    "max": "maximum",
    "corr": "correlation",
    "cov": "covariance",
}


_return_stairs_docstring = """
Takes a collection of Stairs instances and returns the {calc} of the corresponding step functions.

Parameters
----------
collection : tuple, list, numpy array, dict or pandas.Series
    The Stairs instances to aggregate using a {calc} function

Returns
-------
:class:`Stairs`

See Also
--------
{see_also}

{example}
"""

_corr_cov_docstring = """
Calculates the {calc} matrix for a collection of :class:`Stairs` instances

Parameters
----------
collection: :class:`pandas.Series`, dict, or array-like of :class:`Stairs` values
    the stairs instances with which to compute the {calc} matrix
lower : int, float or pandas.Timestamp
    lower bound of the interval on which to perform the calculation
upper : int, float or pandas.Timestamp
    upper bound of the interval on which to perform the calculation

Returns
-------
:class:`pandas.DataFrame`
    The {calc} matrix

See Also
--------
{see_also}

{example}
"""


def _gen_docstring(calculation):

    calc = _calc_map.get(calculation, calculation)
    see_also = _see_also_map[calculation]
    example = _get_example(calculation)

    if calculation in ("cov", "corr"):
        docstring = _corr_cov_docstring
    else:
        docstring = _return_stairs_docstring
    return docstring.format(calc=calc, see_also=see_also, example=example,)


min_docstring = _gen_docstring("min")
max_docstring = _gen_docstring("max")
mean_docstring = _gen_docstring("mean")
median_docstring = _gen_docstring("median")
cov_docstring = _gen_docstring("cov")
corr_docstring = _gen_docstring("corr")
