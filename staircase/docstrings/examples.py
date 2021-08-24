sample_example = """
Examples
--------

.. plot::
    :context: close-figs

    >>> s3.plot(arrows=True)

>>> s3(1.5)
1

>>> s3(3)
nan

>>> s3([1, 3, 4])
array([ 1., nan, -1.])
"""

limit_example = """
Examples
--------

.. plot::
    :context: close-figs

    >>> s3.plot(arrows=True)

>>> s3.limit(2, side="left")
1.0

>>> s3.limit(2, side="right")
0.0

>>> s3.limit([2, 2.5, 3.5], side="right")
array([ 0., nan,  1.])
"""


layer_example = """
Examples
--------

.. plot::
    :context: close-figs

    >>> import staircase as sc
    ... (
    ...     sc.Stairs()
    ...     .layer(1,3)
    ...     .layer(4,5,-2)
    ...     .plot(arrows=True)
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

    >>> (
    ...     sc.Stairs(initial_value=1.5)
    ...     .layer(data["starts"], data["ends"], data["values"])
    ...     .plot(arrows=True)
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
    1     4.0     5        2
    2     5.5     7     -3

    >>> (
    ...     sc.Stairs(initial_value=1.5)
    ...     .layer("starts", "ends", "values", frame=data)
    ...     .plot(arrows=True)
    ... )
"""

number_of_steps_example = """
Examples
--------

.. plot::
    :context: close-figs

    >>> s1.plot(arrows=True)
    >>> s1.number_of_steps
    5

.. plot::
    :context: close-figs

    >>> s3.plot(arrows=True)
    >>> s3.number_of_steps
    6
"""


shift_example = """
Examples
--------

.. plot::
    :context: close-figs
    :include-source: False

    >>> stair_list = [s2, s2.shift(1), s2.shift(-1)]
    >>> fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(8,3), sharey=True, sharex=True, tight_layout=True, dpi=400)
    >>> for ax, title, stair_instance in zip(axes, ("s2", "s2.shift(1)", "s2.shift(-1)"), stair_list):
    ...     stair_instance.plot(ax=ax, label=title, arrows=True)
    ...     ax.set_title(title)

Note that the definition of shift is designed to be consistent with :meth:`pandas.Series.shift`

>>> pd.Series(s2(range(7)))
0    0.5
1    0.5
2    0.0
3   -1.0
4   -1.0
5   -1.0
6    0.0
dtype: float64

>>> pd.Series(s2(range(7))).shift(1)
0    NaN
1    0.5
2    0.5
3    0.0
4   -1.0
5   -1.0
6   -1.0
dtype: float64

>>> pd.Series(s2.shift(1)(range(7)))
0    0.0
1    0.5
2    0.5
3    0.0
4   -1.0
5   -1.0
6   -1.0
dtype: float64
"""

diff_example = """
Examples
--------

.. plot::
    :context: close-figs
    :include-source: False

    >>> stair_list = [s2, s2.shift(1), s2.diff(1)]
    >>> fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(8,3), sharey=True, sharex=True, tight_layout=True, dpi=400)
    >>> for ax, title, stair_instance in zip(axes, ("s2", "s2.shift(1)", "s2.diff(1)"), stair_list):
    ...     stair_instance.plot(ax=ax, label=title, arrows=True)
    ...     ax.set_title(title)
    ... s2.plot(ax=axes[1], label="s2", linestyle="--", arrows=True)
    ... axes[1].legend()

Note that the definition of diff is designed to be consistent with :meth:`pandas.Series.diff`

>>> pd.Series(s2(range(7)))
0    0.5
1    0.5
2    0.0
3   -1.0
4   -1.0
5   -1.0
6    0.0
dtype: float64

>>> pd.Series(s2(range(7))).diff(1)
0    NaN
1    0.0
2   -0.5
3   -1.0
4    0.0
5    0.0
6    1.0
dtype: float64

>>> pd.Series(s2.diff(1)(range(7)))
0    0.5
1    0.0
2   -0.5
3   -1.0
4    0.0
5    0.0
6    1.0
dtype: float64
"""

describe_example = """
Examples
--------

.. plot::
    :context: close-figs

    >>> s2.plot(arrows=True)

>>> s2.describe()
unique    3.000000
mean     -0.272727
std       0.686349
min      -1.000000
25%      -1.000000
50%       0.000000
75%       0.500000
max       0.500000
dtype: float64

>>> s2.describe(where=(0,6), percentiles=np.linspace(0,100,6))
unique    3.000000
mean     -0.250000
std       0.661438
min      -1.000000
0%       -1.000000
20%      -1.000000
40%      -1.000000
60%       0.000000
80%       0.500000
100%      0.500000
max       0.500000
dtype: float64
"""

cov_example = """
Examples
--------

.. plot::
    :context: close-figs
    :include-source: False

    >>> fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(7,3), sharey=True, sharex=True, tight_layout=True, dpi=400)
    >>> for ax, title, stair_instance in zip(axes, ("s1", "s2"), (s1, s2)):
    ...     stair_instance.plot(ax=ax, label=title, arrows=True)
    ...     ax.set_title(title)

>>> s1.cov(s2)
0.1404958677685951

>>> s2.cov(s1)
0.1404958677685951

>>> s1.cov(s2, where=(0, 6))
0.125

>>> # autocovariance with lag 1
>>> s1.cov(s1, where=(1, 5), lag=1)
-0.3333333333333333

>>> # cross-covariance with lag 1
>>> s1.cov(s2, where=(1, 4.5), lag=1)
0.15999999999999998

>>> # cross-covariance with lag 1
>>> s1.cov(s2, where=(1, 4.5), lag=1, clip='post')
0.163265306122449
"""

corr_example = """
Examples
--------

.. plot::
    :context: close-figs
    :include-source: False

    >>> fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(7,3), sharey=True, sharex=True, tight_layout=True, dpi=400)
    >>> for ax, title, stair_instance in zip(axes, ("s1", "s2"), (s1, s2)):
    ...     stair_instance.plot(ax=ax, label=title, arrows=True)
    ...     ax.set_title(title)

>>> s1.corr(s2)
0.24687803791136045

>>> s2.corr(s1)
0.24687803791136045

>>> s1.corr(s2, where=(0, 6))
0.27500954910846337

>>> # autocorrelation with lag 1
>>> s1.corr(s1, where=(1, 5), lag=1)
-0.8660254037844386

>>> # cross-correlation with lag 1
>>> s1.corr(s2, where=(1, 5.5), lag=1)
0.4961389383568339

>>> # cross-correlation with lag 1
>>> s1.corr(s2, where=(1, 4.5), lag=1, clip='post')
0.4961389383568339
"""

rolling_mean_example = """
Examples
--------

>>> s2.rolling_mean(window=[-0.5, 0.5])
-0.5    0.0
 0.5    0.5
 1.5    0.5
 2.5    0.0
 3.5   -1.0
 5.0   -1.0
 6.0    0.0
dtype: float64

.. plot::
    :context: close-figs

    >>> series_list = [s2.rolling_mean(window=[-0.5, 0.5]), s2.rolling_mean(window=[-0.5, 0.5], where=(0, 5.5))]
    >>> fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(7,3), sharey=True, sharex=True, tight_layout=True, dpi=400)
    >>> for ax, title, series in zip(axes, ("default", "'where' specified"), series_list):
    ...     s2.plot(ax=ax)
    ...     series.plot(ax=ax, label='rolling mean')
    ...     ax.set_title(title)
    ...     ax.legend()

.. plot::
    :context: close-figs

    >>> series_list = [s2.rolling_mean(window=[-1, 0], where=(0, 5.5)), s2.rolling_mean(window=[0, 1], where=(0, 5.5))]
    >>> fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(8,3), sharey=True, sharex=True, tight_layout=True, dpi=400)
    >>> for ax, title, series in zip(axes, ("trailing window", "leading window"), series_list):
    ...     s2.plot(ax=ax)
    ...     series.plot(ax=ax, label='rolling mean')
    ...     ax.set_title(title)
    ...     ax.legend()
"""
