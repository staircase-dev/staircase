
sample_example = """
    Examples
    --------
        
    .. plot::
        :context: close-figs
        
        >>> import staircase as sc
        >>> stair_list = [s1, s2]
        >>> fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12,5), sharey=True, sharex=True)
        >>> for ax, title, stair_instance in zip(axes, ("s1", "s2"), stair_list):
        ...     stair_instance.plot(ax)
        ...     ax.set_title(title)
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

min_example = """
    Examples
    --------
        
    .. plot::
        :context: close-figs
        
        >>> import staircase as sc
        >>> stair_list = [s1, s2, sc.min([s1,s2])]
        >>> fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(17,5), sharey=True, sharex=True)
        >>> for ax, title, stair_instance in zip(axes, ("s1", "s2", "min(s1,s2)"), stair_list):
        ...     stair_instance.plot(ax)
        ...     ax.set_title(title)
"""

max_example = """
    Examples
    --------
        
    .. plot::
        :context: close-figs
        
        >>> import staircase as sc
        >>> stair_list = [s1, s2, sc.max([s1,s2])]
        >>> fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(17,5), sharey=True, sharex=True)
        >>> for ax, title, stair_instance in zip(axes, ("s1", "s2", "max(s1,s2)"), stair_list):
        ...     stair_instance.plot(ax)
        ...     ax.set_title(title)
"""

mean_example = """
    Examples
    --------
        
    .. plot::
        :context: close-figs
        
        >>> import staircase as sc
        >>> stair_list = [s1, s2, sc.mean([s1,s2])]
        >>> fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(17,5), sharey=True, sharex=True)
        >>> for ax, title, stair_instance in zip(axes, ("s1", "s2", "mean(s1,s2)"), stair_list):
        ...     stair_instance.plot(ax)
        ...     ax.set_title(title)
"""

median_example = """
    Examples
    --------
        
    .. plot::
        :context: close-figs
        
        >>> import staircase as sc
        >>> stair_list = [s1, s2, sc.median([s1,s2])]
        >>> fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(17,5), sharey=True, sharex=True)
        >>> for ax, title, stair_instance in zip(axes, ("s1", "s2", "median(s1,s2)"), stair_list):
        ...     stair_instance.plot(ax)
        ...     ax.set_title(title)
"""

aggregate_example = """
    Examples
    --------
        
    .. plot::
        :context: close-figs
        
        >>> import staircase as sc
        >>> import numpy as np
        >>> stair_list = [s1, s2, sc.aggregate([s1,s2], np.std)]
        >>> fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(17,5), sharey=True, sharex=True)
        >>> for ax, title, stair_instance in zip(axes, ("s1", "s2", "np.std(s1,s2)"), stair_list):
        ...     stair_instance.plot(ax)
        ...     ax.set_title(title)
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

cov_example = """
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

corr_example = """
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