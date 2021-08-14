base_header = """
Calculates the {name} of each step function slice

Returns
-------
:class:`pandas.Series`
"""

apply_header = """
Applies a method to each step function slice

Parameters
----------
func : callable
    Must be a function which takes a Stairs instance as first parameter
args, kwargs : tuple and dict
    Optional positional and keyword arguments to pass to *func*.

Returns
-------
:class:`pandas.Series`
"""

agg_header = """
Facilitates multiple aggregations applied at once

Parameters
----------
funcs : str, or list of str
    The aggregation functions to apply. Currently supports "min", "max",
    "mean", "median", "mode", "integral".

Returns
-------
:class:`pandas.Dataframe`
"""

hist_header = """
Calculates histogram data for each of the step function slices

Parameters
----------
bins : "unit", sequence or :class:`pandas.IntervalIndex`
    If *bins* is "unit" then the histogram bins will have unit length and cover the range
    of step function values.  If *bins* is a sequence, it defines a monotonically
    increasing array of bin edges.  If *bins* are defined by :class:`pandas.IntervalIndex`
    they should be non-overlapping and monotonic increasing.
closed : {"left", "right"}, default "left"
    Indicates whether the histogram bins are left-closed right-open
    or right-closed left-open. Only relevant when *bins* is not a :class:`pandas.IntervalIndex`
stat : {"sum", "frequency", "density", "probability"}, default "sum"
    The aggregate statistic to compute in each bin.  Inspired by :meth:`seaborn.histplot` stat parameter.
        - ``sum`` the magnitude of observations
        - ``frequency`` values of the histogram are divided by the corresponding bin width
        - ``density`` normalises values of the histogram so that the area is 1
        - ``probability`` normalises values so that the histogram values sum to 1

Returns
-------
:class:`pandas.Dataframe`
    Each row corresponds to a step function slice.  Each column corresponds to a bin.
"""

resample_header = """
Creates a new step function whose values are derived by applying a function to the
step function slices

Parameters
----------
func : {"min", "max", "mean", "median", "mode", "integral"}
    The function applied to the step function slices.
points : {"left", "right", "mid"} or array-like
    Determines what point in the domain of the new step function each slice will
    be mapped to.  If *points* is a string, it indicates a position in reference
    to each interval used to slice the step functions.  If *points* is array-like
    its length must be the same as the number of slices.

Returns
-------
:class:`staircase.Stairs`
"""

example_header = """
Examples
---------

.. plot::
    :context: close-figs

    >>> df = sc.make_test_data(seed=0)
    >>> sf = sc.Stairs(df, "start", "end", "value")
    >>> sf.plot()
"""

mean_example = """
>>> sf.slice(pd.date_range("2021", periods=12, freq="MS")).mean()
[2021-01-01, 2021-02-01)    436.869646
[2021-02-01, 2021-03-01)    374.335764
[2021-03-01, 2021-04-01)    501.771729
[2021-04-01, 2021-05-01)    502.593889
[2021-05-01, 2021-06-01)    396.009341
[2021-06-01, 2021-07-01)    398.588958
[2021-07-01, 2021-08-01)    488.410708
[2021-08-01, 2021-09-01)    475.959341
[2021-09-01, 2021-10-01)    438.847106
[2021-10-01, 2021-11-01)    463.746685
[2021-11-01, 2021-12-01)    474.082616
dtype: float64
"""

integral_example = """
>>> sf.slice(pd.date_range("2021", periods=12, freq="MS")).integral()
[2021-01-01, 2021-02-01)   13542 days 23:01:00
[2021-02-01, 2021-03-01)   10481 days 09:38:00
[2021-03-01, 2021-04-01)   15554 days 22:10:00
[2021-04-01, 2021-05-01)   15077 days 19:36:00
[2021-05-01, 2021-06-01)   12276 days 06:57:00
[2021-06-01, 2021-07-01)   11957 days 16:03:00
[2021-07-01, 2021-08-01)   15140 days 17:34:00
[2021-08-01, 2021-09-01)   14754 days 17:45:00
[2021-09-01, 2021-10-01)   13165 days 09:55:00
[2021-10-01, 2021-11-01)   14376 days 03:32:00
[2021-11-01, 2021-12-01)   14222 days 11:29:00
dtype: timedelta64[ns]
"""

median_example = """
>>> sf.slice(pd.date_range("2021", periods=12, freq="MS")).median()
[2021-01-01, 2021-02-01)    442.0
[2021-02-01, 2021-03-01)    375.0
[2021-03-01, 2021-04-01)    509.0
[2021-04-01, 2021-05-01)    508.0
[2021-05-01, 2021-06-01)    384.0
[2021-06-01, 2021-07-01)    387.0
[2021-07-01, 2021-08-01)    486.0
[2021-08-01, 2021-09-01)    482.0
[2021-09-01, 2021-10-01)    435.0
[2021-10-01, 2021-11-01)    462.0
[2021-11-01, 2021-12-01)    474.0
dtype: float64
"""

mode_example = """
>>> sf.slice(pd.date_range("2021", periods=12, freq="MS")).mode()
[2021-01-01, 2021-02-01)    469.0
[2021-02-01, 2021-03-01)    354.0
[2021-03-01, 2021-04-01)    578.0
[2021-04-01, 2021-05-01)    532.0
[2021-05-01, 2021-06-01)    371.0
[2021-06-01, 2021-07-01)    372.0
[2021-07-01, 2021-08-01)    452.0
[2021-08-01, 2021-09-01)    485.0
[2021-09-01, 2021-10-01)    425.0
[2021-10-01, 2021-11-01)    452.0
[2021-11-01, 2021-12-01)    471.0
dtype: float64
"""

min_example = """
>>> sf.slice(pd.date_range("2021", periods=12, freq="MS")).min()
[2021-01-01, 2021-02-01)    354.0
[2021-02-01, 2021-03-01)    338.0
[2021-03-01, 2021-04-01)    401.0
[2021-04-01, 2021-05-01)    437.0
[2021-05-01, 2021-06-01)    356.0
[2021-06-01, 2021-07-01)    344.0
[2021-07-01, 2021-08-01)    436.0
[2021-08-01, 2021-09-01)    426.0
[2021-09-01, 2021-10-01)    399.0
[2021-10-01, 2021-11-01)    434.0
[2021-11-01, 2021-12-01)    434.0
dtype: float64
"""

max_example = """
>>> sf.slice(pd.date_range("2021", periods=12, freq="MS")).max()
[2021-01-01, 2021-02-01)    492.0
[2021-02-01, 2021-03-01)    418.0
[2021-03-01, 2021-04-01)    587.0
[2021-04-01, 2021-05-01)    564.0
[2021-05-01, 2021-06-01)    463.0
[2021-06-01, 2021-07-01)    480.0
[2021-07-01, 2021-08-01)    543.0
[2021-08-01, 2021-09-01)    502.0
[2021-09-01, 2021-10-01)    486.0
[2021-10-01, 2021-11-01)    505.0
[2021-11-01, 2021-12-01)    509.0
dtype: float64
"""

apply_example = """
>>> def step_count_above_threshold(s, n):
...     return s.number_of_steps > n
...
>>> cuts = pd.date_range("2021", periods=12, freq="MS")
>>> sf.slice(cuts).apply(step_count_above_threshold, 120)
[2021-01-01, 2021-02-01)     True
[2021-02-01, 2021-03-01)    False
[2021-03-01, 2021-04-01)    False
[2021-04-01, 2021-05-01)    False
[2021-05-01, 2021-06-01)     True
[2021-06-01, 2021-07-01)     True
[2021-07-01, 2021-08-01)    False
[2021-08-01, 2021-09-01)     True
[2021-09-01, 2021-10-01)    False
[2021-10-01, 2021-11-01)     True
[2021-11-01, 2021-12-01)     True
dtype: bool
"""

agg_example = """
>>> cuts = pd.date_range("2021", periods=12, freq="MS")
>>> sf.slice(cuts).agg(["min", "max"])
                            min    max
[2021-01-01, 2021-02-01)  354.0  492.0
[2021-02-01, 2021-03-01)  338.0  418.0
[2021-03-01, 2021-04-01)  401.0  587.0
[2021-04-01, 2021-05-01)  437.0  564.0
[2021-05-01, 2021-06-01)  356.0  463.0
[2021-06-01, 2021-07-01)  344.0  480.0
[2021-07-01, 2021-08-01)  436.0  543.0
[2021-08-01, 2021-09-01)  426.0  502.0
[2021-09-01, 2021-10-01)  399.0  486.0
[2021-10-01, 2021-11-01)  434.0  505.0
[2021-11-01, 2021-12-01)  434.0  509.0
"""

hist_example = """
>>> cuts = pd.date_range("2021", periods=12, freq="MS")
>>> sf.slice(cuts).hist(bins=[300, 400, 500, 600], stat="probability")
                          [300.0, 400.0)  [400.0, 500.0)  [500.0, 600.0)
[2021-01-01, 2021-02-01)        0.216756        0.783244        0.000000
[2021-02-01, 2021-03-01)        0.927480        0.072520        0.000000
[2021-03-01, 2021-04-01)        0.000000        0.443907        0.556093
[2021-04-01, 2021-05-01)        0.000000        0.487269        0.512731
[2021-05-01, 2021-06-01)        0.618996        0.381004        0.000000
[2021-06-01, 2021-07-01)        0.592523        0.407477        0.000000
[2021-07-01, 2021-08-01)        0.000000        0.684812        0.315188
[2021-08-01, 2021-09-01)        0.000000        0.985954        0.014046
[2021-09-01, 2021-10-01)        0.029444        0.970556        0.000000
[2021-10-01, 2021-11-01)        0.000000        0.992876        0.007124
[2021-11-01, 2021-12-01)        0.000000        0.875370        0.124630
"""

resample_example = """
.. plot::
    :context: close-figs

    >>> cuts = pd.date_range("2021", periods=12, freq="MS")
    >>> ax = sf.slice(cuts).resample("mean", points="left").plot()
    >>> ax.xaxis.set_major_formatter(DateFormatter('%b-%y'))
    >>> ax.set_title("resampled by mean")
"""


mean_docstring = "\n".join(
    [base_header.format(name="mean"), example_header, mean_example]
)
min_docstring = "\n".join([base_header.format(name="min"), example_header, min_example])
max_docstring = "\n".join([base_header.format(name="max"), example_header, max_example])
median_docstring = "\n".join(
    [base_header.format(name="median"), example_header, median_example]
)
mode_docstring = "\n".join(
    [base_header.format(name="mode"), example_header, mode_example]
)
integral_docstring = "\n".join(
    [base_header.format(name="integral"), example_header, integral_example]
)
apply_docstring = "\n".join([apply_header, example_header, apply_example])
agg_docstring = "\n".join([agg_header, example_header, agg_example])
hist_docstring = "\n".join([hist_header, example_header, hist_example])
resample_docstring = "\n".join([resample_header, example_header, resample_example])

_docstrings = {
    "mean": mean_docstring,
    "min": min_docstring,
    "max": max_docstring,
    "mode": mode_docstring,
    "median": median_docstring,
    "integral": integral_docstring,
}
