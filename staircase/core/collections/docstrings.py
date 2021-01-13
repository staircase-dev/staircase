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

_plots_map = {
    "addition": "s1, s2, s1+s2",
    "subtraction": "s1, s2, s1-s2",
    "multiplication": "s1, s2, s1*s2",
    "division": "s1, s2, s1/(s2+2)",
    "lt": "s1, s2, s1<s2",
    "le": "s1, s2, s1<=s2",
    "gt": "s1, s2, s1>s2",
    "ge": "s1, s2, s1>=s2",
    "eq": "s1, s2, s1==s2",
    "ne": "s1, s2, s1!=s2",
    "and": "s1, s2, s1&s2",
    "or": "s1, s2, s1|s2",
    "invert": "s2, ~s2",
    "make_boolean": "s2, s2.make_boolean()",
    "negate": "s1, -s1",
}

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

corr_example = (
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

cov_example = (
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
