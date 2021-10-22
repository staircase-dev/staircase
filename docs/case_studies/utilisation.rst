.. _casestudies.utilisation:

======================================
Case study: asset utilisation
======================================


This case study illustrates the use of the staircase package for analysing asset utilisation. In this example we have a group of 3 identical assets, X, Y, and Z. These assets are parallel 'machines', such as bays in a carwash, or buses in a fleet etc. Each asset can either be in one of two states - on or off (or alternatively working or not working).

.. ipython:: python
    :suppress:

    import matplotlib.pyplot as plt
    plt.style.use('seaborn')
    asset_data = r"https://raw.githubusercontent.com/staircase-dev/staircase-notebooks/master/data/asset_use.csv"

We begin by importing the asset data into a :class:`pandas.DataFrame` instance. Each row corresponds to a period of time that an asset is being used. The first column identifies the asset, while the second and third columns give the start and end times of the period of use respectively.

.. ipython:: python

    import pandas as pd
    import staircase as sc

    data = pd.read_csv(asset_data, parse_dates=['start', 'end'], dayfirst=True)
    data

For the analysis we would like a :class:`staircase.Stairs` object for each asset. Each Stairs object will represent a step function which has a value of zero, when the asset is not in use, and a value of one when the asset is in use. We can pandas' groupby process (`"split-apply-combine" <https://pandas.pydata.org/docs/user_guide/groupby.html>`_) with the :class:`staircase.Stairs` constructor method to get a :class:`pandas.Series`, indexed by asset name, with :class:`staircase.Stairs` values:

.. ipython:: python

    asset_use = data.groupby("asset").apply(sc.Stairs, start="start", end="end")
    asset_use

Note that since we want to examine 2020 we clip the step function at the year endpoints, making the functions undefined for any time outside of 2020 (see :ref:`user_guide.gotchas` for why this is a good idea).  :meth:`pandas.Series.apply` is used here, rather than looping, for efficiency.

.. ipython:: python

    asset_use = asset_use.apply(sc.Stairs.clip, (pd.Timestamp("2020"), pd.Timestamp("2021")))

We can access an individual :class:`staircase.Stairs` object with the corresponding asset name. For example, to plot the step function corresponding to asset Z, for the first day:

.. ipython:: python

    ax = asset_use['Z'].plot()
    @savefig case_study_asset_z.png
    ax.set_xlim('2020-1-1', '2020-1-2');

Because these assets belong to a group, we are interested in their combined utilisation, i.e. the addition of the three step functions. This can be achieved by simply summing up the :class:`staircase.Stairs` objects, and results in another :class:`staircase.Stairs` object (assigned to `combined_asset_use`):

.. ipython:: python

    combined_asset_use = asset_use['X'] + asset_use['Y'] + asset_use['Z']

Note that we can also achieve the same result by leveraging the :meth:`pandas.Series.sum` method, or preferably :meth:`staircase.sum` (a more efficient method for :class:`staircase.Stairs` objects).

Using the :meth:`staircase.Stairs.integral` method we can see that the three assets together worked for a total of ~13,172 hours in the year 2020.

.. ipython:: python

    combined_asset_use.integral()

    combined_asset_use.integral()/pd.Timedelta("1 hour")

Given there are 3 assets, and 8784 hours in the year 2020, there are a total of 26,352 hours that the assets could have worked - approximately double the hours used. It is not surprising then that calculating the average group utilisation for the year 2020 is approximately 1.5

.. ipython:: python

    combined_asset_use.mean()


Now we will look to discover how often exactly none of the assets were being used. If we compare `combined_asset_use` to 0, then the result is also :class:`staircase.Stairs` instance. This object represents a binary (or boolean) valued step function, which takes value 1 whenever there are 0 assets being used.

.. ipython:: python

    combined_asset_use == 0

The question, of how often none of the assets are being used, can be answered with the :meth:`staircase.Stairs.mean` method:

.. ipython:: python
    
    (combined_asset_use == 0).mean()

So all assets are idle, during 2020, approximately 12.3% of the time. If we wish to further this idea by extending to 1, 2, or 3 assets being used, then the :meth:`staircase.Stairs.hist` method can perform the calculation efficiently.

.. ipython:: python

    combined_utilisation = combined_asset_use.hist(stat="probability")
    combined_utilisation


We can also use the pandas.Series plotting methods to get a quick visual of this utilisation breakdown:

.. ipython:: python

    combined_utilisation.index = combined_utilisation.index.left
    @savefig case_study_asset_bar_plot.png
    combined_utilisation.plot.bar()

We now show how to answer a variety of miscellaneous questions for the purposes of demonstration:

*How often is X working while Y is not?*

.. ipython:: python

    (asset_use["X"] > asset_use["Y"]).mean()

*How many assets were being used at 9:40am on the 5th of September?*

.. ipython:: python

    combined_asset_use(pd.Timestamp(2020, 9, 5, 9, 40))

*Which 2 assets were being used at this time?*

.. ipython:: python

    asset_use.apply(lambda s: s(pd.Timestamp(2020, 9, 5, 9, 40)))


If we’d prefer to work with “idleness”, instead of “in use”, we can create a :class:`staircase.Stairs` object to capture this by simply subtracting the "in use" step function from the number of assets (3):

.. ipython:: python

    combined_assets_idle = 3 - combined_asset_use

The number of assets idle at 9:40am on the 5th of September should be 1 right? Let’s check:

.. ipython:: python

    combined_assets_idle(pd.Timestamp(2020, 9, 5, 9, 40))