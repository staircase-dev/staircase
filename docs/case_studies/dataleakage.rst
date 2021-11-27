.. _casestudies.dataleakage:

======================================
Case study: data leakage
======================================

This case study illustrates the use of the staircase package to simplify feature engineering while avoiding *data leakage*.
Data leakage, also known as target leakage, occurs when models are trained and validated using data that would not, and will not, be available at the time of prediction.  In order to avoid data leakage it is important to think about the time at which that data becomes known.

The dataset used in this example is taken from `Kaggle <https://www.kaggle.com/dansbecker/melbourne-housing-snapshot/metadata>`_ and is distributed under a `creative commons license <https://creativecommons.org/licenses/by-nc-sa/4.0/>`_.  If you've ever looked at buying real estate it is likely you have investigated property prices in the same neighbourhood as a guide to estimating price.  It is therefore tempting, when using this dataset for predicting house price, to use average sale price in the neighbourhood as an input feature.  The problem is that when predicting a price for a particular house that is yet to be sold, we will not know the price it sold for (obviously) or the price for any house that sells after it. The data used to train a machine learning model must reflect this. We can still engineer an average house price feature for each house, however in order to avoid data leakage it can only use prices for houses sold prior to that house. This can be a tricky, or inefficient, calculation however :mod:`staircase` can make light work of this.

.. ipython:: python
    :suppress:

    import matplotlib.pyplot as plt
    plt.style.use('seaborn')
    house_data = r"https://raw.githubusercontent.com/staircase-dev/staircase-notebooks/master/data/melb_house_data.csv"

We begin by importing the house price data into a :class:`pandas.DataFrame` instance. Each row corresponds to a house that has been sold.  There are many columns, however for this exercise we are only interested in *Suburb*, *Price*, and *Date*.  The *Date* column does not appear to have a time component (i.e. hour/minute/second) but :mod:`staircase` could have handled this.

.. ipython:: python

    import pandas as pd
    import staircase as sc
    import matplotlib.pyplot as plt
    from matplotlib.dates import MonthLocator, DateFormatter

    data = pd.read_csv(house_data, parse_dates=['Date'], dayfirst=True)
    data

Whenever there is date/time data in a dataset there are immediately step functions which spring to life. For example, in this dataset the following are variables which can be calculated:


    - the number of houses sold, up to a particular point in time
    - the number of houses sold in Abbotsford, up to a particular point in time
    - the number of houses with more than 2 bathrooms sold, up to a particular point in time
    - the total sum of house prices, up to a particular point in time

As these variables change as time moves along, they give rise to step functions.  For example, at the time a house is sold the value of the step function corresponding to "number of houses sold" increases by one, and the value of the step function corresponding to "total sum of house prices" increases by the price of the house. We can take these two step functions and divide them to get another which will describe the average house price over time - this is what we are aiming to calculate.

We can create the step function for number of houses sold by simply passing the *Date* column to the :class:`staircase.Stairs` constructor as the start times of intervals.  There are no end times, as once a house changes state from "unsold" to "sold", it never becomes "unsold" again.

.. ipython:: python

    houses_sold = sc.Stairs(data, start="Date")

We can create the step function for total sum of house prices similarly, however this time we set the *value* argument to be the house price column, so that the step function increases by the house price at each sale date.

.. ipython:: python

    sum_houses_prices = sc.Stairs(data, start="Date", value="Price")

Let's plot these:

.. ipython:: python

    fig, axes = plt.subplots(nrows=2, figsize=(10,5), sharex=True)

    houses_sold.plot(axes[0]);
    axes[0].set_title("Number of houses sold over time");

    sum_houses_prices.plot(axes[1]);
    @savefig case_study_data_leakage_quotients.png
    axes[1].set_title("Sum of houses prices sold over time");

These step functions look to be almost identical, albeit one scaled much higher, however their quotient will tell a different story.  We now divide these step functions to obtain one for average house price over time

.. ipython:: python

    fig, ax = plt.subplots(figsize=(10,3))

    av_house_prices = sum_houses_prices/houses_sold
    av_house_prices.plot(ax);
    @savefig case_study_data_leakage_average.png
    ax.set_title("Average houses price over time");


As can be seen from the plot, as time goes on the average is less variable. It settles down as more and more houses are taken into account when calculating the average. It is also possible to calculate rolling averages too, whether by a fixed number of previous houses, or with a time based rolling window, eg "previous month". This will be discussed later.

So how do we get use this information in our training set? If a house is sold on a particular date then we want to know the average house price up until that point. Given the date in our dataset are at the day level it is sufficient to examine the value of the step function half a day earlier.  For each of our houses, we can calculate this date like so:

.. ipython:: python

    sample_times = data["Date"] - pd.Timedelta(0.5, "day")
    sample_times

So these are the times at which we need to know the value of our `av_house_prices` step function. We can get these values by simply "calling" our step function as if it was a method:

.. ipython:: python

    av_price_samples = av_house_prices(sample_times)
    av_price_samples

At the moment this data is a numpy array, but we can add it to our original dataset.

.. ipython:: python

    data["average_price"] = av_price_samples
    data.head()

To recap, creating the average house price data feature is as simple as

.. ipython:: python

    sample_times = data["Date"] - pd.Timedelta(0.5, "day")
    data["average_price"] = (
        sc.Stairs(data, start="Date", value="Price") /
        sc.Stairs(data, start="Date")
    )(sample_times)


Now, for the houses sold on the earliest date in this dataset there will be no average house price data, and there will be missing values in the `average_price` column for these houses. These values would need to be imputed before proceeding. The `average_price` column can then be used as an input to a machine learning model.

Next we explore some advanced usage with :mod:`staircase`.


**Sampling the step function "immediately to the left"**

We took a shortcut above, by the fact that our dates were at the day-frequency level, and we sampled the step function the day before each sale. What if we wanted the values of the step function up until the exact date? This can be done with the :meth:`staircase.Stairs.limit` method, which takes sample points and a *side* parameter.

.. ipython:: python

    pd.Series(
        av_house_prices.limit(sample_times, side="left")
    )


**A step function per suburb**

We calculate a :class:`pandas.Series` indexed by suburb, whose values are step functions (:class:`staircase.Stairs`). Using this we can calculate average house prices (up to a certain point in time) for each suburb.

.. ipython:: python

    def create_av_price_step_function(df):
        count = sc.Stairs(df, start="Date")
        sum_prices = sc.Stairs(df, start="Date", value="Price")
        return sum_prices/count

    data.groupby("Suburb").apply(create_av_price_step_function)

**Rolling average using time window**

In this example the calculate the average house price, however it only takes into account houses from the past 12 weeks.

.. ipython:: python

    time_window = pd.Timedelta(12, "W")  # 12 weeks
    expiry = data["Date"] + time_window
    count = sc.Stairs(data, start="Date", end=expiry)
    sum_prices = sc.Stairs(data, start="Date", end=expiry, value="Price")
    av_house_prices = sum_prices/count

.. ipython:: python

    fig, ax = plt.subplots(figsize=(10,3))
    av_house_prices.plot(ax);
    @savefig case_study_data_leakage_rolling.png
    ax.set_title("Average houses prices over time (12 week rolling window)");