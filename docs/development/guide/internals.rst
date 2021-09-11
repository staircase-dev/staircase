.. _development.internals:


The internals of staircase
======================================

A step function can be represented in a number of ways.  There are two formats which staircase uses internally and it may switch between them, or use both at once.  Both of these formats share a couple of common components.  The first of these is a property `Stairs.initial_value` which indicates the value of the step function at "negative infinity".  It's value is either numerical of `numpy.nan`.  The second shared component is a pandas index of sorted, unique, values which indicate where the step function changes value.  Each :class:`staircase.Stairs` instance has a "private" attribute `._data` which is either a :class:`pandas.DataFrame` or is `None`.  If `._data` is None then the step function does not change value at any point.  If `.data` is not None, then it is indexed by the domain values where the step function changes.

This dataframe will contain at least one column, named "delta" or "value" and may contain both of these.  The *delta* describe the difference in step function value at each of the points in the index, while *value* describe the value of the step function as it approaches each point in the index from the right.

To help convey the idea we define a function called *internals* which prints the value of `Stairs.initial_value` and `Stairs._data`, and use it conjunction with plotting some simple examples.

.. ipython:: python
    
    import staircase as sc
    import pandas as pd
    import matplotlib.pyplot as plt

    def internals(stairs):
        stairs._get_values()
        stairs._get_deltas()
        print()
        print(f"initial_value = {stairs.initial_value}")
        print()
        print(stairs._data)
        _, ax= plt.subplots()
        ax.set_xlim(-1,2)
        ax.set_ylim(-1,2)
        stairs.plot(ax, arrows="True")

.. ipython:: python

    @savefig internals_1.png
    internals(sc.Stairs(initial_value = -0.5, start=0, end=1, value=1.5))

.. ipython:: python

    @savefig internals_2.png
    internals(sc.Stairs(start=0.5))

.. ipython:: python

    @savefig internals_3.png
    internals(sc.Stairs(end=0.5))

.. ipython:: python

    @savefig internals_4.png
    internals(sc.Stairs(initial_value=1).clip(0,1))

.. ipython:: python

    @savefig internals_5.png
    internals(sc.Stairs(initial_value=1).clip(None,1))

.. ipython:: python

    @savefig internals_6.png
    internals(sc.Stairs(initial_value=1).mask((0,1)))

.. ipython:: python

    @savefig internals_7.png
    internals(sc.Stairs(initial_value=-0.5, start=-0.5, end=1.5).mask((0,1)))


The :class:`pandas.Series` which correspond to the *delta* and *value* columns are best obtained with the private methods `Stairs._get_deltas` and `Stairs._get_values`, which will create the objects if they don't exist.

The :class:`staircase.Stairs` class is defined in staircase/core/stairs.py but many of its methods are defined elsewhere in the package, and then added to class dynamically.  This is purely done to organise and separate the code into related functionality.