
sample_example = """
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> s1.plot()
            >>> s1(3.5)
            1
            >>> s1([1, 2, 4.5, 6])
            \[1, 0, -1, 0\]
            >>> s1([1, 2, 4.5, 6], how="left")
            \[0, 1, -1, 0\]
            >>> s1([1, 2, 4.5], aggfunc="mean", window=(-0.5, 0.5))
            \[0.5, 0.5, -1.0\]
            >>> s1([1, 2, 4.5], aggfunc="max", window=(-0.5, 0.5))
            \[1, 1, -1\]
            >>> s1([1, 2, 4.5], aggfunc="max", window=(-0.5, 0.5), lower_how="left")
            \[1, 1, 1\]
            >>> s1([1, 2, 4.5], aggfunc="max", window=(-0.5, 0.5), upper_how="right")
            \[1, 1, 0\]
"""


resample_example = """
        Examples
        --------
            
        .. plot::
            :context: close-figs

            >>> stair_list = [s1, s1.resample([1.5,2.5,4,4.5])]
            >>> fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12,5), sharey=True, sharex=True)
            >>> for ax, title, stair_instance in zip(axes, ("s1", "s1 resampled"), stair_list):
            ...     stair_instance.plot(ax)
            ...     ax.set_title(title)
"""



layer_example = """
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> import staircase as sc
            ... (sc.Stairs()
            ...     .layer(1,3)
            ...     .layer(4,5,-2)
            ...     .plot()
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
            >>> (sc.Stairs(1.5)
            ...     .layer(data["starts"], data["ends"], data["values"])
            ...     .plot()
            ... )
"""

step_changes_example = """
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> s1.plot()
            >>> s1.step_changes()
            {1: 1, 2: -1, 3: 1, 4: -2, 5: 1}
"""

negate_example = """
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> s1.plot()
            >>> (-s1).plot(color='r')
"""

add_example = """
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> stair_list = [s1, s2, s1+s2]
            >>> fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(17,5), sharey=True, sharex=True)
            >>> for ax, title, stair_instance in zip(axes, ("s1", "s2", "s1+s2"), stair_list):
            ...     stair_instance.plot(ax)
            ...     ax.set_title(title)
"""

subtract_example = """
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> stair_list = [s1, s2, s1-s2]
            >>> fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(17,5), sharey=True, sharex=True)
            >>> for ax, title, stair_instance in zip(axes, ("s1", "s2", "s1-s2"), stair_list):
            ...     stair_instance.plot(ax)
            ...     ax.set_title(title)
"""

divide_example = """
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> stair_list = [s1, (s2+2), s1/(s2+2)]
            >>> fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(17,5), sharey=True, sharex=True)
            >>> for ax, title, stair_instance in zip(axes, ("s1", "s2+2", "s1/(s2+2)"), stair_list):
            ...     stair_instance.plot(ax)
            ...     ax.set_title(title)
"""

multiply_example = """
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> stair_list = [s1, s2, s1*s2]
            >>> fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(17,5), sharey=True, sharex=True)
            >>> for ax, title, stair_instance in zip(axes, ("s1", "s2", "s1*s2"), stair_list):
            ...     stair_instance.plot(ax)
            ...     ax.set_title(title)
"""


make_boolean_example = """
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> stair_list = [s2, s2.make_boolean()]
            >>> fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12,5), sharey=True, sharex=True)
            >>> for ax, title, stair_instance in zip(axes, ("s2", "s2.make_boolean()"), stair_list):
            ...     stair_instance.plot(ax)
            ...     ax.set_title(title)
"""

invert_example = """
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> stair_list = [s2, ~s2]
            >>> fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12,5), sharey=True, sharex=True)
            >>> for ax, title, stair_instance in zip(axes, ("s2", "~s2"), stair_list):
            ...     stair_instance.plot(ax)
            ...     ax.set_title(title)
"""


logical_and_example = """
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> stair_list = [s1, s2, s1 & s2]
            >>> fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(17,5), sharey=True, sharex=True)
            >>> for ax, title, stair_instance in zip(axes, ("s1", "s2", "s1 & s2"), stair_list):
            ...     stair_instance.plot(ax)
            ...     ax.set_title(title)
"""

logical_or_example = """
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> stair_list = [s1, s2, s1 | s2]
            >>> fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(17,5), sharey=True, sharex=True)
            >>> for ax, title, stair_instance in zip(axes, ("s1", "s2", "s1 | s2"), stair_list):
            ...     stair_instance.plot(ax)
            ...     ax.set_title(title)
"""


lt_example = """
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> stair_list = [s1, s2, s1 < s2]
            >>> fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(17,5), sharey=True, sharex=True)
            >>> for ax, title, stair_instance in zip(axes, ("s1", "s2", "s1 < s2"), stair_list):
            ...     stair_instance.plot(ax)
            ...     ax.set_title(title)
"""

gt_example = """
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> stair_list = [s1, s2, s1 > s2]
            >>> fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(17,5), sharey=True, sharex=True)
            >>> for ax, title, stair_instance in zip(axes, ("s1", "s2", "s1 > s2"), stair_list):
            ...     stair_instance.plot(ax)
            ...     ax.set_title(title)
"""

le_example = """
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> stair_list = [s1, s2, s1 <= s2]
            >>> fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(17,5), sharey=True, sharex=True)
            >>> for ax, title, stair_instance in zip(axes, ("s1", "s2", "s1 <= s2"), stair_list):
            ...     stair_instance.plot(ax)
            ...     ax.set_title(title)
"""

ge_example = """
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> stair_list = [s1, s2, s1 >= s2]
            >>> fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(17,5), sharey=True, sharex=True)
            >>> for ax, title, stair_instance in zip(axes, ("s1", "s2", "s1 >= s2"), stair_list):
            ...     stair_instance.plot(ax)
            ...     ax.set_title(title)
"""

eq_example = """
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> stair_list = [s1, s2, s1 == s2]
            >>> fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(17,5), sharey=True, sharex=True)
            >>> for ax, title, stair_instance in zip(axes, ("s1", "s2", "s1 == s2"), stair_list):
            ...     stair_instance.plot(ax)
            ...     ax.set_title(title)
"""


ne_example = """
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> stair_list = [s1, s2, s1 != s2]
            >>> fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(17,5), sharey=True, sharex=True)
            >>> for ax, title, stair_instance in zip(axes, ("s1", "s2", "s1 != s2"), stair_list):
            ...     stair_instance.plot(ax)
            ...     ax.set_title(title)
"""

number_of_steps_example = """
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> s1.plot()
            >>> s1.number_of_steps()
            5
"""

identical_example = """
        Examples
        --------
        
        >>> s1.identical(s1)
        True
        >>> s1.identical(s1.copy())
        True
        >>> s1.identical(s1.copy().layer(1,2))
        False
"""

integral_and_mean_example = """
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> s1.plot()
            >>> s1.get_integral_and_mean(3, 4.5)
            (0.5, 0.3333333333333333)
"""

integrate_example = """
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> s1.plot()
            >>> s1.integrate(3, 4.5)
            0.5
"""

mean_example = """
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> s1.plot()
            >>> s1.mean(3, 4.5)
            0.3333333333333333
"""

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

clip_example = """
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12,5))
            >>> s1.plot(axes[0])
            >>> s1.clip(2,4).plot(axes[1])
            >>> s1.clip(2,4).mean()
            0.5
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

var_example = """
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> s1.plot()
            
        .. plot::
            :context: close-figs
            
            >>> s1.var()
            0.6875
            
            >>> s1.var(lower=0, upper=6)
            0.4722222222222224
    
"""

std_example = """
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> s1.plot()
            
        .. plot::
            :context: close-figs
            
            >>> s1.std()
            0.82915619758885
            
            >>> s1.std(lower=0, upper=6)
            0.6871842709362769
    
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

values_in_range_example = """
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> s2.plot()
            >>> s2.values_in_range()
            {-1.0, 0.0, 0.5}
            >>> s2.values_in_range(lower=2)
            {-1.0, 0.0}
            >>> s2.values_in_range(lower=2, lower_how="left")
            {-1.0, 0.0, 0.5}
            >>> s2.values_in_range(upper=2)
            {0.0, 0.5}
            >>> s2.values_in_range(upper=3, upper_how="right")
            {-1.0, 0.0, 0.5}
            
"""