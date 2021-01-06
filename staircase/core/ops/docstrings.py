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

negate_example = """
Examples
--------

.. plot::
    :context: close-figs

    >>> s1.plot()
    >>> (-s1).plot(color='r')
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
