.. _user_guide.distributions:

Distribution of values
=======================


The possible values of a variable, and how often they occur, is known as a distribution.  It describes the likelihood of a particular value being observed.  The distribution of step function values can be analysed in several different ways using :mod:`staircase`.  The first thing to note is though is where most observed data corresponds to a finite sample, that is *n* observations, a step function corresponds to an infinite number of observations.  Consequently, we cannot tally a count of values observed, but we can perform a *value sum* (analogous to :meth:`pandas.Series.value_counts`:

.. ipython:: python
    :suppress:

    import staircase as sc
    import pandas as pd
    import matplotlib.pyplot as plt
    plt.rcParams['figure.autolayout'] = True

.. ipython:: python

    sf = sc.Stairs().layer([0,1,2], [3,6,7]).mask((4,5))
    @savefig distribution_sf_simple.png
    sf.plot()

.. ipython:: python
    
    sf.value_sums()

The result of :meth:`staircase.Stairs.value_sums` is a :meth:`pandas.Series` where the index contains the observed values of the step function, and the values are the combined lengths of the intervals in the step function with that value.  By default, the intervals where the step functions is undefined are omitted however this behaviour can be changed with the *drop_na* parameter:

.. ipython:: python
    
    sf.value_sums(dropna=False)

Consider this example of a step function with datetime domain:

.. ipython:: python

    df = sc.make_test_data(dates=True, positive_only=True, seed=42)
    sf = sc.Stairs(df, "start", "end")
    @savefig distribution_sf.png
    sf.plot();

When the domain of a step function is datetime based then the result will be expressed as :class:`pandas.Timedelta`.

.. ipython:: python

    sf.value_sums()

Conversion from :class:`pandas.Timedelta` to a numerical representation can be done by dividing the result by a unit timedelta.  The following example demonstrates how to convert the values to days and plot the distribution with pandas' bar plot.

.. ipython:: python

    hist_days = sf.value_sums()/pd.Timedelta(1, "day")
    hist_days
    @savefig distribution_sf_bar.png
    hist_days.plot.bar();


Histograms
-----------

To combine the observed values into bins we could group the index values of the Series and sum them, however an alternative exists in the form of :meth:`staircase.Stairs.hist`.  This method has a *bins* parameter, similar to that of :meth:`pandas.Series.hist`.  The bins parameter allows us to define the intervals with which to bin the observed values.  For example, to create bins of width 2.

.. ipython:: python

    sf.hist(bins=range(10, 27, 2))

In addition to defining bins, the method also permits the statistic to be defined for computing the value of each bin, via the *stat* parameter.  The possibilities, inspired by :meth:`seaborn.histplot` include

- ``sum`` the magnitude of observations
- ``frequency`` values of the histogram are divided by the corresponding bin width
- ``density`` normalises values of the histogram so that the area is 1
- ``probability`` normalises values so that the histogram values sum to 1


.. plot::
    :context: close-figs
    :include-source: False

    >>> df = sc.make_test_data(dates=True, positive_only=True, seed=42)
    >>> sf = sc.Stairs(df, "start", "end")
    >>> bins = range(10, 27, 2)
    >>> fig, axes = plt.subplots(ncols=2, nrows=2, figsize=(7,7), sharex=True)
    >>> for stat, ax in zip(("sum", "frequency", "density", "probability"), axes.flatten()):
    >>>     hist = sf.hist(bins=bins, stat=stat)
    >>>     if stat in ("sum", "frequency"):
    >>>         hist = hist/pd.Timedelta(1, "days")
    >>>     hist.plot.bar(ax=ax)
    >>>     ax.set_title(stat)


Histograms bar charts are one way of visualising a distribution, however they do have their drawbacks.  Histograms can suffer from *binning bias* where the shape of the plot, and the story it tells, changes depending on the bin definition.  An arguably better choice for visualising distributions is with the cumulative distribution function.

Cumulative Distribution Functions
----------------------------------

This cumulative distribution function - perhaps better known as the ECDF, where the "E" standing for *Empirical*, signifying that the result is derived from observed data - describes the fraction of the distribution below each unique value in the dataset.  It has several advantages over histogram plots for visualisation.  This style of plot has been implemented in seaborn (:meth:`seaborn.ecdfplot`) but can also be plotted with :mod:`staircase` too.  In fact, the ECDF itself is a step function and its implementation in staircase is a derivation of the :class:`staircase.Stairs` class, and is such inherits many useful methods such as :meth:`staircase.Stairs.plot` and :meth:`staircase.Stairs.sample`.

.. ipython:: python

    sf.ecdf
    @savefig distribution_sf_ecdf.png
    sf.ecdf.plot()
    
.. ipython:: python

    print(f"{sf.ecdf(16) :.0%} of the time sf <= 16")
    print(f"{sf.ecdf(20) :.0%} of the time sf <= 20")
    print(f"{sf.ecdf(20) - sf.ecdf(16):.0%} of the time 16 < sf <= 20")


One of the strongest arguments for ECDFs over histogram plots is when several distributions are compared on the same plot.

.. ipython:: python

    df = sc.make_test_data(dates=False, groups=["A","B","C","D"], seed=60)
    series = df.groupby("group").apply(sc.Stairs, "start", "end", "value")
    fig, axes = plt.subplots(ncols=2, figsize=(7,3))
    for i, stairs in series.items():
        stairs.plot(axes[0], label=i)
    axes[0].set_title("step functions");
    for i, stairs in series.items():
        stairs.ecdf.plot(axes[1], label=i)
    axes[1].legend();
    @savefig distribution_multipl_ecdf.png
    axes[1].set_title("ECDFs");

* mention caching


Percentiles, Fractiles, Quantiles
----------------------------------

quantiles needs docstring


.. ipython:: python
    :suppress:
 
    plt.close("all")