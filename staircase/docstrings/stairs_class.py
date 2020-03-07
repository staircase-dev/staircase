
sample_example = """
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> s1.plot()
            >>> s1(3.5)
            1
            >>> s1([1, 2, 4.5, 6])
            [1, 0, -1, 0]
            >>> s1([1, 2, 4.5, 6], how='left')
            [0, 1, -1, 0]
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
            >>> for ax, title, stair_instance in zip(axes, ("s1", "s2+2", "S1/(s2+2)"), stair_list):
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
            >>> s2_percentiles = s2.percentile_Stairs()
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
            >>> s2.min(0,3)
            -1.0
            >>> s2.min(1,2.5)
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
            >>> s1.max(2,3)
            1.0
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