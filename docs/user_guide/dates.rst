.. _user_guide.dates:

Working with dates
===================

:mod:`staircase` is designed with two domain types in mind: real numbers and time - or in the language of Python computing, floats and datetimes.  Even when the domain is real numbers it is quite likely that, semantically, those numbers represent a time value.

In version 1 of :mod:`staircase` a user wanting to use datetimes needed to declare this when creating a :class:`staircase.Stairs` instance.  This is not required in v2:

.. ipython:: python
    :suppress:

    import matplotlib as mpl
    mpl.rcParams['figure.figsize'] = 9,3

.. ipython:: python
    
    import pandas as pd
    import staircase as sc
    sf = sc.Stairs().layer(pd.Timestamp("2021"), pd.Timestamp("2022"), 3)
    @savefig dates_simple.png
    sf.plot(arrows=True)

|

For datetime domains *v2* has been tested with :class:`numpy.datetime64`, :class:`datetime.datetime`, and :class:`pandas.Timestamp`.  This includes **time-zone aware** variants for the latter two of these.  If you're working with datetime domains then arguments to methods with domain-based parameters need to be datetime too.  These methods include:

* :meth:`staircase.Stairs.layer`
* :meth:`staircase.Stairs.sample`
* :meth:`staircase.Stairs.limit`
* :meth:`staircase.Stairs.clip`
* :meth:`staircase.Stairs.mask`
* :meth:`staircase.Stairs.where`
* :meth:`staircase.Stairs.slice`

String representations of timestamps can also be used as arguments for :meth:`staircase.Stairs.clip`, :meth:`staircase.Stairs.mask` and :meth:`staircase.Stairs.where`.

Note that when using datetime domains an integral calculation will be a timedelta:

.. ipython:: python
    
    sf.integral()


Unfortunately the :class:`pandas.Timedelta` class has `limitations <https://pandas.pydata.org/pandas-docs/stable/user_guide/timedeltas.html#timedelta-limitations>`_ which may be exceeded with integral calculations (resulting in an overflow error).  A workaround may involve scaling your step function values down, by dividing by a constant, before calculating the integral.  This begs the question of whether this situation can be avoided by using :class:`numpy.datetime64` or :class:`datetime.datetime`.  "Under the hood" of :mod:`staircase` datetimes are represented by :class:`pandas.Timestamp`, even if the original data was another datetime class.  This conversion is something that is inherited from :mod:`pandas` and the overflow error remains.  If you wish to convert from :class:`pandas.Timestamp` to another datetime class then the following methods may be of use:

* :meth:`pandas.Timestamp.to_datetime64`
* :meth:`pandas.Timestamp.to_pydatetime`

Timezones
**********

Datetime data can be timezone-naíve or timezone-aware.  For many datetime applications of staircase it may suffice to ignore the concept of timezones and work with timezone-naíve data - an attractive option as working with timezones, and converting between them, can be tricky. However many countries observe `Daylight Savings Time <https://en.wikipedia.org/wiki/Daylight_saving_time>`_ which results in one day of the year having 23 hours, and another having 25 hours:

.. ipython:: python
    
    import pytz
    timezone = pytz.timezone('Australia/Sydney')
    sc.Stairs().layer(
        pd.Timestamp("2021-4-4", tz=timezone),
        pd.Timestamp("2021-4-5", tz=timezone),
    ).integral()
    sc.Stairs().layer(
        pd.Timestamp("2021-10-3", tz=timezone),
        pd.Timestamp("2021-10-4", tz=timezone),
    ).integral()


If you are computing some daily metric and do not take this into account then the calculations on those days will be incorrect, however the consequences, and indeed the calculated result, maybe small enough to ignore. However, for some applications the use of timezone-aware timestamps may be critical.

Given the sheer number of packages available for Python it may be of no surprise that there are several for dealing with timezones.  There is one which is clearly the de facto standard: :mod:`pytz`, however staircase supports any timezone package that pandas supports.

.. ipython:: python
    :suppress:
 
    plt.close("all")