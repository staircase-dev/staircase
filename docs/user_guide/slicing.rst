.. _user_guide.slicing:

Slicing
========

Slicing is a new feature introduces in v2.  It has some similarities to :func:`pandas.cut`, which is used to bin data into discrete intervals, and :meth:`pandas.Series.groupby`, which involves splitting the data, applying a function and combining the results.

The method :meth:`staircase.Stairs.slice` is designed to slice a step function into discrete intervals, apply a function, and combine the results.  In most cases the result will be a :class:`pandas.Series` but there are slice functions which return something different.  The ``slice`` method has a parameter *cut* which can be a sequence, :class:`pandas.IntervalIndex`, or :class:`pandas.PeriodIndex` - the latter is only applicable for datetime domains.  The *cut* parameter is almost identical to the *bin* parameter in :func:`pandas.cut`.  It is used to provide the interval bounds which are used to slice the step function.  

Examples:

.. ipython:: python

    import staircase as sc
    import pandas as pd

    df = sc.make_test_data(seed=42)
    sf = sc.Stairs(df, "start", "end")
    @savefig slicing1.png
    sf.plot()

.. ipython:: python   

    sf_sliced = sf.slice(pd.period_range("2021", "2022"))
    sf_sliced.mean()
    sf_sliced.median()

In the above example *sf_sliced* is a :class:`staircase.StairSlicer` object.  This object exposes many intuitive methods which can be performed on the "slices".  If several methods are to be performed then it may be wise to assign the StairSlicer object to a variable.  This is not necessary though, as demonstrated in the below example, and the :meth:`staircase.StairSlicer.agg` method can be used to perform multiple statistical operations in one method call.

.. ipython:: python

    df = sc.make_test_data(dates=False, seed=42)
    sf = sc.Stairs(df, "start", "end")
    @savefig slicing2.png
    sf.plot()

.. ipython:: python

    ii = pd.IntervalIndex.from_breaks(range(0, 101, 5))
    sf.slice(ii).agg(["min", "max"])


A major point of difference in the comparison between :meth:`staircase.Stairs.slice` and :meth:`pandas.Series.groupby`, is that the intervals used to slice a step function may overlap, nor they need to cover the domain.  This is demonstrated in the following trivial examples:

.. ipython:: python

    ii = pd.IntervalIndex.from_arrays([0]*5, [100]*5)
    sf.slice(ii).mode()

.. ipython:: python

    ii = pd.IntervalIndex.from_tuples([(0,10),  (40,50)])
    sf.slice(ii).integral()

There are several methods, beyond simple summary stats, that :class:`staircase.StairSlicer` provides.  This includes :meth:`staircase.StairSlicer.apply` which functions similarly to :meth:`pandas.Series.apply` and allows any function, which takes a Stairs object as its first argument to be applied to the slices:

.. ipython:: python

    def count_steps(s):
        return s.number_of_steps

    ii = pd.IntervalIndex.from_breaks(range(0, 101, 5))
    sf.slice(ii).apply(count_steps)

The concept of resampling a step function was introduced in `staircase` v1.  In v2 resampling is achieved by slicing, applying a function which returns a number, then producing a new step function from those values.  The points at which the resampled step function changes value are chosen relative to the intervals used to slice the step function.  They may either be the left-endpoings, right-endpoints or midpoints, and the *points* parameter in :meth:`staircase.StairSlicer.resample` affects this behaviour.

.. ipython:: python
    :suppress:

    import matplotlib.pyplot as plt

.. ipython:: python

    fig, axes = plt.subplots(ncols=2, figsize=(7,3), sharex=True, sharey=True)
    sf.plot(axes[0]);
    axes[0].set_title("sf");
    ii = pd.IntervalIndex.from_breaks(range(0, 101, 10))
    sf.slice(ii).resample("mean", points="mid").plot(axes[1]);
    @savefig slicing_resample.png
    axes[1].set_title("sf - resampled");
