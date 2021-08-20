.. _release_notes.versiontwo:

========================
What's new in version 2?
========================

Version 2 of :mod:`staircase` was released in September 2021.  Whereas version 1 was based upon `Sorted Containers <http://www.grantjenks.com/docs/sortedcontainers/>`_, version 2 is based upon :mod:`pandas` and :mod:`numpy`.  Making this move required a complete rewrite of staircase internals but yielded significant speedups:

.. toctree::
    :maxdepth: 1
 
    Speed comparison v1 versus v2 (floats) <v1_v2_floats>
    Speed comparison v1 versus v2 (dates) <v1_v2_dates>


In addition new functionality was added, namely :ref:`masking <user_guide.masking>` and :ref:`slicing <user_guide.slicing>`.

Mention dates

While much of the API has remained the same there are many backwards incompatible changes.  These will be detailed here soon.  Stay tuned.

We use *v1* to refer to Staircase v1.*


Enhancements
-------------

Optional *layer* arguments in constructor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:meth:`staircase.Stairs.__init__` now includes those parameters found in :meth:`staircase.Stairs.layer`.  This was done to simplify the two-step process of initialising a Stairs instance, and then layering, into one.  


Constructor signature includes *closed* parameter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In v1, users were asked to assume a convention of *left-closed* or *right-closed* half open intervals, comprising their step functions.  This assumption would be used when calling :meth:`staircase.Stairs.sample`.  To better align to the `Zen of Python <https://en.wikipedia.org/wiki/Zen_of_Python>`_, in particular "explicit is better than implicit", users of v2 are required to declare this assumption on construction of a Stairs instance via the *closed* parameter.  The possible values for this parameter are "left" (default) or "right".


:meth:`staircase.Stairs.layer` now accepts a dataframe argument
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In v1, the layer method had three parameters: *start*, *end*, *value*.  These parameters remain in V2, in the same positions, however an optional *frame* parameter, which accepts a :class:`pandas.DataFrame` has been added.  Inspired by conventions found in :mod:`seaborn`, if *frame* is specified then *start*, *end* and *value* arguments may optionally be strings, corresponding to column names in the dataframe.


Masking
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Masking is introduced in v2.  It allows step functions to have intervals where they are undefined.  Areas where a step function is undefined are ignored when calculating statistics, and will be absent from plots.  Masking, and related functionality, is facilitated by the following methods:

- :meth:`staircase.Stairs.mask`
- :meth:`staircase.Stairs.where`
- :meth:`staircase.Stairs.isna`
- :meth:`staircase.Stairs.notna`
- :meth:`staircase.Stairs.fillna`

Please see :ref:`user_guide.masking` in the user guide for more information.


Slicing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Slicing is introduced in v2, and is a similar in concept to groupby operations in pandas.  This functionality allows users to slice a step function into discrete intervals, apply a function, and combine the results.  This can be used to convert from a step function to time series data.  A new class, :class:`staircase.StairsSlicer`, has been introduced to facilitate the functionality, however it is envisioned that users will primarily use :meth:`staircase.Stairs.slice` rather than creating StairsSlicer instances directly.

Please see :ref:`user_guide.slicing` in the user guide for more information.


Extended plotting options
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Several parameters have been added to :meth:`staircase.Stairs.plot` in v2.  These include *style* and *arrows*.  The effect is demonstrated below:

.. ipython:: python
    :suppress:
    
    import staircase as sc
    import pandas as pd

.. ipython:: python

    sf = sc.Stairs().layer([1,4,2], [3,6,5], [1,1,2])
    fig, axes = plt.subplots(ncols=2, figsize=(7,3), sharey=True, tight_layout=True)
    sf.plot(ax=axes[0], arrows=False, style="step");
    axes[0].set_title('arrows=False, style="step"');
    sf.plot(ax=axes[1], arrows=True, style="hlines");
    @savefig version_two_plotting.png
    axes[1].set_title('arrows=True, style="hlines"');

Please see the :ref:`plotting <intro_tutorials.plotting>` intro tutorial for more information.


Reverse operators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Binary operations in staircase have always allowed one operand to be numerical, provided the first operand was a :class:`staircase.Stairs` instance.  Reverse operators have been added in v2 which allow the first operand to be numerical.  These operators include 

- :meth:`staircase.Stairs.radd`  (+)
- :meth:`staircase.Stairs.rdivide`  (/)
- :meth:`staircase.Stairs.rmultiply`  (*)
- :meth:`staircase.Stairs.rsubtract`  (-)
- :meth:`staircase.Stairs.logical_rand`  (*)
- :meth:`staircase.Stairs.logical_ror`  (|)
- :meth:`staircase.Stairs.logical_rxor`  (^)

Like their standard counterparts, these operators are best used with their corresponding symbols for readability, eg::

    sf = sc.Stairs().layer([1,4,2], [3,6,5], [1,1,2])
    sf + 3  # staircase.Stairs.add
    3 + sf  # staircase.Stairs.radd


Support for :class:`numpy.datetime64` and :class:`datetime.datetime`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Datetime domains in v1 were possible via :class:`pandas.Timestamp`.  In v2 this has been extended to include  :class:`numpy.datetime64`, :class:`datetime.datetime`.  Note however that numpy does not support **time-zone aware** variants.  "Under the hood" of :mod:`staircase` datetimes are represented by :class:`pandas.Timestamp`, even if the original data was another datetime class.  This conversion is something that is inherited from :mod:`pandas`.  If you wish to convert from :class:`pandas.Timestamp` to another datetime class then the following methods may be of use

- :meth:`pandas.Timestamp.to_pydatetime`,
- :meth:`pandas.Timestamp.to_datetime64`,
- :meth:`pandas.Timedelta.to_pytimedelta` and
- :meth:`pandas.Timedelta.to_timedelta64`.
  
Please see :ref:`user_guide.dates` in the user guide for more information.


:meth:`staircase.Stairs.hist` now has *stat* parameter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In v2, the *stat* parameter is introduced to define the statistic used for computing the value of each bin in the histogram.  The possibilities, inspired by :meth:`seaborn.histplot` include

- ``sum`` the magnitude of observations
- ``frequency`` values of the histogram are divided by the corresponding bin width
- ``density`` normalises values of the histogram so that the area is 1
- ``probability`` normalises values so that the histogram values sum to 1

Please see :ref:`user_guide.distributions` in the user guide for more information.

Other additions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- :meth:`staircase.Stairs.logical_xor`
- :meth:`staircase.Stairs.mode`
- :meth:`staircase.Stairs.pipe` 
- :meth:`staircase.Stairs.limit`
- :meth:`staircase.Stairs.agg`
- :meth:`staircase.Stairs.quantiles`
- :meth:`staircase.Stairs.value_sums`
- :attr:`staircase.Stairs.step_values`
- :attr:`staircase.Stairs.step_points`


Backwards incompatible API changes
-----------------------------------

Optional dataframe first parameter in constructor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In v1, the first parameter of the constructor was `value` (renamed to `initial_value` in v2).  In v2 the first parameter is now a :class:`pandas.DataFrame`.  This decision was made to facilitate construction of :class:`staircase.Stairs` instances using :meth:`pandas.DataFrame.pipe` or "groupby-apply":

.. ipython:: python

    df = sc.make_test_data(groups=("a", "b", "c"));
    df.head()

    df.query("start > '2021-5'").pipe(sc.Stairs, "start", "end")

    df.groupby("group").apply(sc.Stairs, "start", "end")



:meth:`staircase.Stairs.clip` set values to null, not zero
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In v1 the clip function, given an interval in the domain defined by *lower* and *upper* parameters, would return a copy of the Stairs instance where the value of the step function outside of this interval is zero.  In v2 these values are undefined instead.

Please see :ref:`user_guide.masking` in the user guide for more information.


:meth:`staircase.Stairs.sample` now takes only one parameter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In v1, :meth:`staircase.Stairs.sample` was capable of performing multiple tasks.  In the interests of the `single-responsibility principle <https://en.wikipedia.org/wiki/Single-responsibility_principle>`_ the existing functionality has been delegated to new methods:

- evaluating the step function at given points - responsibility remains :meth:`staircase.Stairs.sample`
- evaluating the step function as it approaches given points, from a given side - responsibility now :meth:`staircase.Stairs.limit`
- performing windowed aggregations around points - responsibility now :meth:`staircase.Stairs.slice`


:attr:`staircase.Stairs.step_changes` is now a property and returns :class:`pandas.Series`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In v1, the return type was a dictionary, and was a consequence of staircase being built upon :class:`sortedcontainers.SortedDict`.  The return type in v2 is a :class:`pandas.Series` and reflects is a consequence of being built upon pandas.  It is now a property, rather than a method.


Other changes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- :meth:`staircase.Stairs.number_of_steps` changed from method to property
- *bin_edges* parameter in :meth:`staircase.Stairs.hist` renamed to *bins*
- :meth:`staircase.Stairs.values_in_range` returns :class:`numpy.ndarray` instead of :class:`set`
- :meth:`staircase.Stairs.sample` returns either :class:`numpy.ndarray` of :class:`pandas.Series` instead of :class:`list`

Deprecations
--------------

`value` parameter in constructor renamed to `initial_value`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In v2, the parameters of :meth:`staircase.Stairs.layer` were added to the Stairs constructor.  This resulted in a name clash, which was resolved by renaming the original *value* parameter in the constructor to *initial_value*.


*use_dates* and *tz* parameters removed from constructor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In v1, datetime domains were facilitated with conversions between :class:`pandas.Timestamp` and the real numbers.  The use of a datetime domain needed to be defined in the constructor, so that the Stairs instance could be instructed to make, or not make, conversions when needed.  In v2, there are no such conversions, and the values in the Stairs internal data structures can remain as :class:`pandas.Timestamp`.


Domain parameters removed from statistical functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In v1, there are several statistic methods which take *lower* and *upper* parameters to restrict a calculation to an interval.  In v2 these parameters have been removed in favour of using the method on a "clipped" step function.  Affected methods include:

- :meth:`staircase.Stairs.describe`
- :meth:`staircase.Stairs.min`
- :meth:`staircase.Stairs.max`
- :meth:`staircase.Stairs.var`
- :meth:`staircase.Stairs.std`
- :meth:`staircase.Stairs.median`
- :meth:`staircase.Stairs.mean`   
- :meth:`staircase.Stairs.percentile`
- :meth:`staircase.Stairs.hist`
  

`staircase.Stairs.integral_and_mean` removed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Integral and mean calculations for functions are related, and the latter relies on the former.  To avoid duplicate calculations v1 provided this method.  In v2 both results are calculated, when either :meth:`staircase.Stairs.integral` or :meth:`staircase.Stairs.mean` is called, and cached on the Stairs instance to avoid duplicate calculation.


`staircase.Stairs.percentile_stairs` removed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In v1, `staircase.Stairs.percentile_stairs` returned an instance of :class:`staircase.Stairs`, and `staircase.Stairs.percentile()` could be used for evaluating percentile values.  In v2,  :attr:`staircase.Stairs.percentile` combines both of these functions.  It is an accessor (think if it like a property) that returns an instance of a `Percentiles` class (a subclass of `Stairs`).  The Percentiles class is callable, providing the ability to evaluate percentile values.


`staircase.Stairs.ecdf_stairs` removed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Similar to the case for `staircase.Stairs.percentile_stairs` above, the existing functionality is now provided by :attr:`staircase.Stairs.ecdf`, an accessor which returns an `ECDF` class (a subclass of `Stairs`).  The ECDF class is callable.


`staircase.Stairs.resample` removed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Resampling is now achieved through slicing.  Please see :ref:`user_guide.slicing` for more information.


Other deprecations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- `staircase.Stairs.integrate` renamed to :meth:`staircase.Stairs.integral`
- :meth:`staircase.Stairs.to_dataframe` renamed to :meth:`staircase.Stairs.to_frame`
- *lower* and *upper* parameters in :meth:`staircase.Stairs.rolling_mean` removed.  Use *where* parameter instead.
- *lower* and *upper* parameters in :meth:`staircase.Stairs.cov` removed.  Use *where* parameter instead.
- *lower* and *upper* parameters in :meth:`staircase.Stairs.corr` removed.  Use *where* parameter instead.