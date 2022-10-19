.. _casestudies.queues:

======================================
Case study: queue analysis
======================================


This case study illustrates the use of the staircase package for queue analysis. In this example  vessels (i.e. ships) arrive offshore and await their turn to enter a harbour where they will be loaded with cargo. We will examine the queue, which is composed of all vessels which is offshore but yet to enter the harbour, for the year 2020.

.. ipython:: python
    :suppress:

    vessel_data = r"https://raw.githubusercontent.com/staircase-dev/staircase-notebooks/master/data/vessel_queue.csv"


We begin by importing the queue data into a :class:`pandas.DataFrame` where each row corresponds to a vessel. The first column gives the time at which the vessel arrives offshore (enters the queue), and the second column gives the time at which the vessel enters the harbour (leaves the queue). A `NaT` value in either of these columns indicates the vessel entered the queue prior to 2020, or left the queue after 2020, however this approach does not require these values to be NaT. The third column gives the weight, in tonnes, of cargo destined for the vessel. Note, for this approach we require every vessel, that was in the queue at some point in 2020, to appear in the dataframe.

.. ipython:: python

    import pandas as pd
    import staircase as sc
    import matplotlib.pyplot as plt

    data = pd.read_csv(vessel_data, parse_dates=["enter", "leave"], dayfirst=True)
    data

.. ipython:: python
    :suppress:

    plt.style.use('seaborn-v0_8')

A step function, which quantifies the size of the queue, can be created with vector data corresponding to start and end times for the state being modelled.  In this case, where the state is "in the queue", the required data is the columns “enter” and “leave”.  Note that since we want to examine 2020 we clip the step function at the year endpoints, making the functions undefined for any time outside of 2020 (see :ref:`user_guide.gotchas` for why this is a good idea).

.. ipython:: python

    queue = sc.Stairs(frame=data, start="enter", end="leave")
    queue = queue.clip(pd.Timestamp("2020"), pd.Timestamp("2021"))
    @savefig case_study_queue.png
    queue.plot();

From the chart it would appear the size of the queue at the beginning of 2020 is around 10 vessels.  This can be confirmed by *calling* the step function with this time as an argument - a deliberate choice to emulate the notation for evaluating a function at a particular point:

.. ipython:: python

    queue(pd.Timestamp("2020-01-01"))

Assuming that no vessels arrive precisely at midnight on the 1st of Jan, we can expect the number of vessels in the queue at this time to be equal to the number of NaT values in the “enter” column:

.. ipython:: python

    data["enter"].isna().sum()

There are a number of ways we can characterise the distribution of the queue size values.  The :meth:`staircase.Stairs.hist` method creates histogram data as a :class:`pandas.Series`, indexed by a :class:`pandas.IntervalIndex`. If the `bins` parameter is not supplied then the method will use unit bins which cover the range of the step function values:

.. ipython:: python

    queue_hist = queue.hist(stat="probability")
    queue_hist

Given the queue length is integer variable the :class:`pandas.IntervalIndex` can be replaced to produce a simpler plot:

.. ipython:: python

    queue_hist.index = queue_hist.index.left
    ax = queue_hist.plot.bar()
    ax.set_xlabel("queue size", fontsize="12")
    @savefig case_study_queue_hist_bar.png
    ax.set_ylabel("probability", fontsize="12")


Another useful queue metric in the context of this case study is “queue tonnes”.  This metric is calculated as the sum of the cargo tonnes destined for vessels in the queue. Since the queue is a step function, queue tonnes must also be a step function.  The creation of a queue tonnes step function is similar to that used for the queue, but requires the vector of cargo tonnes to be used in construction.  The `value` parameter, which defaults to a vector of ones, indicates how much the step function should increase or decrease whenever the corresponding vessels enter or leave the queue:

.. ipython:: python

    queue_tonnes = sc.Stairs(frame=data, start="enter", end="leave", value="tonnes")
    queue_tonnes = queue_tonnes.clip(pd.Timestamp("2020"), pd.Timestamp("2021"))
    @savefig case_study_queue_tonnes.png
    queue_tonnes.plot();

Before diving deeper into distributions we tackle a variety of miscellaneous questions for the purposes of demonstration.

*What was the maximum queue tonnes in 2020?*

.. ipython:: python

    queue_tonnes.max()

*What was the average queue tonnes in 2020?*

.. ipython:: python

    queue_tonnes.mean()

*What fraction of the year was the queue_tonnes larger than 1.5 million tonnes?*

.. ipython:: python

    (queue_tonnes > 1.5e6).mean()

*What was the median queue tonnes for March?*

.. ipython:: python

    queue_tonnes.clip(pd.Timestamp("2020-3"), pd.Timestamp("2020-4")).median()

*What is the 80th percentile for queue tonnes?*

.. ipython:: python

    queue_tonnes.percentile(80)

What is the 40th, 65th, 77th and 90th percentiles for queue tonnes?

.. ipython:: python

    queue_tonnes.percentile([40,65,77,90])

Aside from being able to evaluate any number of percentiles, we can plot the "percentile function":

.. ipython:: python

    queue_tonnes.percentile.plot()


The percentile function is essentially the inverse of an `empirical cumulative distribution function <https://en.wikipedia.org/wiki/Empirical_distribution_function>`_.  We can generate an ecdf for the step function values too:

.. ipython:: python

    @savefig case_study_queue_ecdf.png
    queue_tonnes.ecdf.plot()


Earlier we found that the queue tonnes were strictly above 1.5Mt about 9.87% of the time. The ecdf can tell us what fraction of the time the queue tonnes was less than or equal to 1.5Mt. (We’d expect these results to add to 1).

.. ipython:: python

    queue_tonnes.ecdf(1.5e6)

We can also then discover the fraction of time that 1Mt < queue tonnes <= 1.5Mt like so:

.. ipython:: python

    queue_tonnes.ecdf(1.5e6) - queue_tonnes.ecdf(1e6)


This piece of data is tantamount to a single bin in histogram data. Earlier we used the :class:`staircase.Stairs.hist` function on the queue length, with default bin sizes. Since the range of the queue tonnes values is much larger it will be useful to specify the bins (defined by the edges) to generate a histogram for the queue tonnes.

.. ipython:: python

    queue_tonnes_hist = queue_tonnes.hist(bins = range(0, 2100000, 100000), stat="probability")
    queue_tonnes_hist

As we did earlier for the queue length histogram, we can quickly create a chart with pandas Series plotting functions.

.. ipython:: python

    ax = queue_tonnes_hist.plot.bar()
    ax.set_xlabel("queue size in tonnes", fontsize="12")
    ax.set_ylabel("probability", fontsize="12")
    @savefig case_study_queue_tonnes_hist_bar.png
    plt.tight_layout()

Although there is plenty of analysis achieveable through step functions, it may be desirable to aggregate the data to a traditional time series - a daily mean for example.  This can be achieved with SLICING

.. ipython:: python

    day_range = pd.date_range("2020", freq="D", periods=366)
    queue_tonnes.slice(day_range).mean()



