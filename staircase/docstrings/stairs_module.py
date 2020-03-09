
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