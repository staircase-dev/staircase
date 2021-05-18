number_of_steps_example = """
        Examples
        --------

        .. plot::
            :context: close-figs

            >>> s1.plot()
            >>> s1.number_of_steps()
            5
"""

min_example = """
        Examples
        --------

        .. plot::
            :context: close-figs

            >>> s2.plot()
            >>> s2.min(0, 3)
            0
            >>> s2.min(0, 3, upper_how='right')
            -1
            >>> s2.min(0, 2)
            0.5
            >>> s2.min(0, 2, lower_how='left')
            0.0
"""

max_example = """
        Examples
        --------

        .. plot::
            :context: close-figs

            >>> s1.plot()
            >>> s1.max()
            1.0
            >>> s1.max(4, 5)
            -1
            >>> s1.max(4, 5, lower_how='left')
            1
            >>> s1.max(4, 5, upper_how='right')
            0

"""

shift_example = """
        Examples
        --------

        .. plot::
            :context: close-figs

            >>> stair_list = [s2, s2.shift(1), s2.shift(-1)]
            >>> fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(17,5), sharey=True, sharex=True)
            >>> for ax, title, stair_instance in zip(axes, ("s2", "s2.shift(1)", "s2.shift(-1)"), stair_list):
            ...     stair_instance.plot(ax, label=title)
            ...     ax.set_title(title)

        Note that the definition of shift is designed to be consistent with pandas.Series.shift

        .. plot::
            :context: close-figs

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

            >>> stair_list = [s2, s2.shift(1), s2.diff(1)]
            >>> fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(17,5), sharey=True, sharex=True)
            >>> for ax, title, stair_instance in zip(axes, ("s2", "s2.shift(1)", "s2.diff(1)"), stair_list):
            ...     stair_instance.plot(ax, label=title)
            ...     ax.set_title(title)
            ... s2.plot(axes[1], label="s2", linestyle="--")
            ... axes[1].legend()

        Note that the definition of diff is designed to be consistent with pandas.Series.diff

        .. plot::
            :context: close-figs

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

            >>> s2.plot()

        .. plot::
            :context: close-figs

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

            >>> s2.describe(lower=0, upper=6, percentiles=range(0,101,20))
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

            >>> fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12,5), sharey=True, sharex=True)
            >>> for ax, title, stair_instance in zip(axes, ("s1", "s2"), (s1, s2)):
            ...     stair_instance.plot(ax, label=title)
            ...     ax.set_title(title)

        .. plot::
            :context: close-figs

            >>> s1.cov(s2)
            0.1404958677685951

            >>> s2.cov(s1)
            0.1404958677685951

            >>> s1.cov(s2, lower=0, upper=6)
            0.125

            >>> # autocovariance with lag 1
            >>> s1.cov(s1, lower=1, upper=5, lag=1)
            -0.3333333333333333

            >>> # cross-covariance with lag 1
            >>> s1.cov(s2, lower=1, upper=4.5, lag=1)
            0.15999999999999998

            >>> # cross-covariance with lag 1
            >>> s1.cov(s2, lower=1, upper=4.5, lag=1, clip='post')
            0.163265306122449

"""

corr_example = """
        Examples
        --------

        .. plot::
            :context: close-figs

            >>> fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12,5), sharey=True, sharex=True)
            >>> for ax, title, stair_instance in zip(axes, ("s1", "s2"), (s1, s2)):
            ...     stair_instance.plot(ax, label=title)
            ...     ax.set_title(title)

        .. plot::
            :context: close-figs

            >>> s1.corr(s2)
            0.24687803791136045

            >>> s2.corr(s1)
            0.24687803791136045

            >>> s1.corr(s2, lower=0, upper=6)
            0.27500954910846337

            >>> # autocorrelation with lag 1
            >>> s1.corr(s1, lower=1, upper=5, lag=1)
            -0.8660254037844386

            >>> # cross-correlation with lag 1
            >>> s1.corr(s2, lower=1, upper=5.5, lag=1)
            0.4961389383568339

            >>> # cross-correlation with lag 1
            >>> s1.corr(s2, lower=1, upper=4.5, lag=1, clip='post')
            0.4961389383568339
"""

rolling_mean_example = """
        Examples
        --------

        .. plot::
            :context: close-figs

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

            >>> series_list = [s2.rolling_mean(window=[-0.5, 0.5]), s2.rolling_mean(window=[-0.5, 0.5], lower=0, upper = 5.5)]
            >>> fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12,5), sharey=True, sharex=True)
            >>> for ax, title, series in zip(axes, ("default", "bounds supplied"), series_list):
            ...     s2.plot(ax=ax)
            ...     series.plot(ax=ax, label='rolling mean')
            ...     ax.set_title(title)
            ...     ax.legend()

        .. plot::
            :context: close-figs

            >>> series_list = [s2.rolling_mean(window=[-1, 0], lower=0, upper = 5.5), s2.rolling_mean(window=[0, 1], lower=0, upper = 5.5)]
            >>> fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12,5), sharey=True, sharex=True)
            >>> for ax, title, series in zip(axes, ("trailing window", "leading window"), series_list):
            ...     s2.plot(ax=ax)
            ...     series.plot(ax=ax, label='rolling mean')
            ...     ax.set_title(title)
            ...     ax.legend()
"""
