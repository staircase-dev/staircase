.. _casestudies.intervals:

======================================
Case study: interval manipulation
======================================

This tutorial illustrates how :mod:`staircase` can be applied to manipulate intervals.  The ideas demonstrated below form the basis for `piso <https://piso.readthedocs.io>`_, a python package providing set operations for :mod:`pandas` interval classes.

Intervals are not explicitly modelled by :mod:`staircase`, unlike :mod:`pandas`, but we can map intervals to step functions (and vice versa) and :mod:`staircase` can certainly handle step functions!  There are several mappings from intervals to step functions which seem reasonable, however the most useful for our purposes will be one where, for a set of intervals, the corresponding step function is `f(x) = 1` if the point `x` belongs to one of the intervals and 0 otherwise.  Note that this is only a one-to-one mapping if the intervals, in each set, are disjoint and non-adjacent.

To start, we'll consider an example working with intervals `[3,6)` and `[5,7)`, and create corresponding step functions (i.e. :class:`staircase.Stairs`) `a` and `b` respectively.

.. ipython:: python

    import pandas as pd
    import staircase as sc

    a = sc.Stairs(start=3, end=6, closed="left")
    b = sc.Stairs(start=5, end=7, closed="left")

The following function will be useful to map back to intervals:

.. ipython:: python

    def stairs_to_intervals(stairs):
        return (
            stairs
            .to_frame()
            .query("value == 1")
            .drop(columns="value")
        ) 

These intervals clearly overlap between 5 and 6, and we can create the union, with the step functions, using a "logical or" operation:

.. ipython:: python

    result = a | b  # result will be a Stairs instance
    stairs_to_intervals(result)

Similarly, the intersection can be calculated with a "logical and":

.. ipython:: python

    result = a & b  # result will be a Stairs instance
    stairs_to_intervals(result)

For set difference, we can literally translate "in a, and not in b" with :class:`staircase.Stairs` like so:

.. ipython:: python

    result = a & ~b  # result will be a Stairs instance
    stairs_to_intervals(result)


The same result for *set difference* can be achieved by using `b` as a mask (which creates undefined values where `b` in non-zero) then filling the undefined values of the step function with 0. It can also be achieved by multiplying instead of using :meth:`staircase.Stairs.logical_and`:

.. ipython:: python

    result = a.mask(b).fillna(0)

or

.. ipython:: python

    result = a * ~b

Let's say we want to create the union of many intervals.  There are two approaches, the first of which is to create a step function for every interval and repeatedly apply the :meth:`staircase.Stairs.logical_or` function:

.. ipython:: python

    from functools import reduce

    intervals = pd.arrays.IntervalArray.from_tuples([(0, 1), (1, 3), (2, 4), (5, 7)])
    result = reduce(sc.Stairs.logical_or, [sc.Stairs(start=i.left, end=i.right) for i in intervals])
    stairs_to_intervals(result)

The second approach is to add the step functions together (and values where the intervals overlap will have values of 2 or more), and then set non-zero values of the step function to 1. This approach is favourable as it allows us to pass in vectors of `start` and `end` values for the intervals into the constructor of a single :class:`staircase.Stairs` object.

.. ipython:: python

    result1 = sc.Stairs(start=intervals.left, end=intervals.right)
    result1.to_frame()
From here we can just use a relational operator to get a boolean valued step function:

.. ipython:: python

    stairs_to_intervals(result1 > 0)


We could have also used `result1 != 0` or `result1.make_boolean()` to convert to the binary valued step function.

Converting this step function back to an interval array can be done by using the start and end columns of the dataframe as arguments to :meth:`pandas.arrays.IntervalArray.from_arrays`.
