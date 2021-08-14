sample_footer = """
>>> stairs = [s2, s3]
>>> sc.sample(stairs, [2,3,4])
     2    3    4
0  0.0 -1.0 -1.0
1  0.0  NaN -1.0

>>> stairs = {"s2":s2, "s3":s3}
>>> sc.sample(stairs, [2,3,4])
      2    3    4
s1  0.0 -1.0 -1.0
s2  0.0  NaN -1.0

>>> index=pd.MultiIndex.from_tuples([("a", "s2"), ("b", "s3")])
>>> stairs = pd.Series([s2,s3], index=index)
>>> sc.sample(stairs, [2,3,4])
        2    3    4
a s1  0.0 -1.0 -1.0
b s2  0.0  NaN -1.0
"""

limit_footer = """
>>> stairs = [s2, s3]
>>> sc.limit(stairs, [2,3,4], side="left"))
     2    3    4
0  0.5  0.0 -1.0
1  1.0  NaN  1.0

>>> stairs = [s2, s3]
>>> sc.limit(stairs, [2,3,4], side="right"))
     2    3    4
0  0.0 -1.0 -1.0
1  0.0  NaN -1.0

>>> stairs = {"s2":s2, "s3":s3}
>>> sc.limit(stairs, [2,3,4], side="left"))
      2    3    4
s1  0.5  0.0 -1.0
s2  1.0  NaN  1.0

>>> index=pd.MultiIndex.from_tuples([("a", "s2"), ("b", "s3")])
>>> stairs = pd.Series([s2,s3], index=index)
>>> sc.limit(stairs, [2,3,4], side="left"))
        2    3    4
a s1  0.5  0.0 -1.0
b s2  1.0  NaN  1.0
"""


_plot_titles_map = {
    "sample": ["s2", "s3"],
    "limit": ["s2", "s3"],
    "sum": ["s1", "s2", "sc.sum([s1,s2])"],
    "min": ["s1", "s2", "sc.min([s1,s2])"],
    "max": ["s1", "s2", "sc.max([s1,s2])"],
    "mean": ["s1", "s2", "sc.mean([s1,s2])"],
    "median": ["s1", "s2", "sc.median([s1,s2])"],
    "aggregate": ["s1", "s2", "sc.agg([s1,s2], np.std)"],
}

_example = """
.. plot::
    :context: close-figs
    :include-source: False

    {setup}
    >>> stair_list = [{plots}]
    >>> fig, axes = plt.subplots(nrows=1, ncols={ncols},  figsize=({width},3), sharey=True, sharex=True, tight_layout=True, dpi=400)
    >>> for ax, title, stair_instance in zip(axes, {plot_titles}, stair_list):
    ...     stair_instance.plot(ax=ax, arrows=True)
    ...     ax.set_title(title)
"""


def _gen_example(plot_titles, setup=""):
    # plot_titles is a list of strings
    ncols = len(plot_titles)
    plots = ", ".join(plot_titles)
    return _example.format(
        plots=plots,
        ncols=ncols,
        plot_titles=plot_titles,
        setup=setup,
        width=ncols + 5,
    )


_example_section = """
Examples
--------
{example}
"""

sample_example = (
    _example_section.format(example=_gen_example(_plot_titles_map["sample"]))
    + sample_footer
)

limit_example = (
    _example_section.format(example=_gen_example(_plot_titles_map["limit"]))
    + limit_footer
)

min_example = _example_section.format(example=_gen_example(_plot_titles_map["min"]))
max_example = _example_section.format(example=_gen_example(_plot_titles_map["max"]))
mean_example = _example_section.format(example=_gen_example(_plot_titles_map["mean"]))
median_example = _example_section.format(
    example=_gen_example(_plot_titles_map["median"])
)
aggregate_example = _example_section.format(
    example=_gen_example(_plot_titles_map["aggregate"])
)

_corr_cov_header = """
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

Examples
--------
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

Examples
--------
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
    return docstring.format(
        calc=calc,
        see_also=see_also,
        example=example,
    )


min_docstring = _gen_docstring("min")
max_docstring = _gen_docstring("max")
mean_docstring = _gen_docstring("mean")
median_docstring = _gen_docstring("median")
cov_docstring = _gen_docstring("cov")
corr_docstring = _gen_docstring("corr")
