.. _user_guide.masking:

Masking
==========================================

Prior to version 2, step functions in staircase had domains which were simply connected, meaning they were defined everywhere.  The step function existed at every point between negative and positive infinity, with no gaps.  This has changed in version 2, with step functions now able to have intervals where they are undefined.  Areas where a step function is undefined are ignored when calculating statistics.  For example, the following two step functions yield the same statistics - from mean, to variance, to percentiles.

.. plot::
    :context: close-figs
    :include-source: False

    >>> fig, axes = plt.subplots(nrows=1, ncols=2,  figsize=(7,3), sharey=True, sharex=True, tight_layout=True, dpi=400)
    >>> sc.Stairs(start=[2,5,6], end=[7,6,8], value=[1,2,-1]).mask((3,5)).plot(ax=axes[0], arrows=True)
    >>> sc.Stairs(start=[2,3,4], end=[5,4,6], value=[1,2,-1]).plot(ax=axes[1], arrows=True)

This feature is where masking finds is primary motivation.  It allows us to perform a calculation over a subset of the step function's domain.  For example, using masking we can:

  * restrict a calculation to a particular interval, such as a year
  * exclude weekends from calculations
  * separate results by day of the week

There are three methods belonging to :class:`staircase.Stairs` which allow us to perform masking: :meth:`staircase.Stairs.clip`, :meth:`staircase.Stairs.mask`, :meth:`staircase.Stairs.where`.

.. _user_guide.clipping:

clip
*****

:meth:`staircase.Stairs.clip` is not new in version 2.  It retains the same method signature but its meaning has changed.  In version 1 the clip function, given an interval in the domain defined by *lower* and *upper* parameters, would return a copy of the Stairs instance where the value of the step function outside of this interval is zero.  In version 2 these values are undefined instead.  That is, the clip method allows us to restrict the domain of a step function to an interval.

.. ipython:: python
    :suppress:

    import staircase as sc
    import matplotlib.pyplot as plt
    plt.rcParams['figure.autolayout'] = True

.. ipython:: python

    sf = sc.Stairs(start=[2,3,4], end=[5,4,6], value=[1,2,-1])
    fig, axes = plt.subplots(ncols=2, figsize=(7,3), sharex=True, sharey=True)
    sf.plot(ax=axes[0], arrows=True);
    axes[0].set_title("sf");
    sf.clip(3,5).plot(ax=axes[1], arrows=True);
    @savefig masking_clip.png
    axes[1].set_title("sf.clip(3,5)");

In version 1, there are several statistic methods which take *lower* and *upper* parameters to restrict a calculation to an interval.  In version 2 these parameters have been removed in favour of using the method on a "clipped" step function, for example

.. ipython:: python

    sf.clip(3,5).mean()
    sf.clip(3,5).std()
    sf.clip(3,5).min()

Note that if there are multiple methods which will be applied to a clipped function, as is the case in the above example, then it is more efficient to assign the clipped Stairs instance:

.. ipython:: python

    sf_clip = sf.clip(3,5)
    sf_clip.mean()
    sf_clip.std()
    sf_clip.min()


On the topic of efficiency, the result achieved by :meth:`staircase.Stairs.clip` can be achieved with both :meth:`staircase.Stairs.mask` and :meth:`staircase.Stairs.where` however these methods are more general and will not be as fast as *clip*.


mask/where
***********

We introduce these methods together as they are two sides of the same coin, much like their counterparts in pandas, :meth:`pandas.Series.mask` and :meth:`pandas.Series.where`.  These methods in pandas allow a user to set values in a Series to ``nan`` by supplying a boolean valued Series as a parameter.  For :meth:`pandas.Series.mask` it is the True values which yield ``nan`` and for :meth:`pandas.Series.where` it is the False values [*]_.  The corresponding methods in staircase operate in much the same way, and utilise the concept of boolean values for step functions, as discussed in the tutorial on :ref:`comparing step functions <intro_tutorials.comparing_logical>`.  For any two Stairs objects *f* and *g*:

* the step function resulting from ``f.mask(g)`` will be undefined wherever *g* is non-zero or undefined
* the step function resulting from ``f.where(g)`` will be undefined wherever *g* is zero or undefined

Let's see some examples:

.. ipython:: python

    masker = sc.Stairs().layer(None,3,2).layer(5,6);
    @savefig masking_masker.png
    masker.plot(arrows=True)

.. ipython:: python

    fig, axes = plt.subplots(ncols=2, figsize=(7,3), sharey=True, sharex=True)
    sf.plot(ax=axes[0], arrows=True);
    axes[0].set_title("sf");
    sf.mask(masker).plot(ax=axes[1], arrows=True);
    @savefig masking_mask.png
    axes[1].set_title("sf.mask(masker)");

.. ipython:: python

    fig, axes = plt.subplots(ncols=2, figsize=(7,3), sharex=True, sharey=True)
    sf.plot(ax=axes[0], arrows=True);
    axes[0].set_title("sf");
    sf.where(masker).plot(ax=axes[1], arrows=True);
    @savefig masking_where.png
    axes[1].set_title("sf.where(masker)");


In particular, the :meth:`staircase.Stairs.where` method, in combination with comparison operators can make for concise and readable calculations.  For example, when calculating the integral for *sf* in the examples above, we arrive at a correct answer of 3.  However the "area under the function" is given by 5.  We can calculate this quantity like so: 

.. ipython:: python

    sf.where(sf > 0).integral() + (-sf).where(sf < 0).integral()

Lastly, when using these two methods a tuple can be used as shorthand notation for simple step functions where ``(a,b)`` is equivalent to ``sc.Stairs(start=a, end=b)``.  Using this convention ``.where((a,b))`` gives an identical result to ``.clip(a,b)``, but as noted above using *clip* will be faster.

fillna
*******

As noted above, there are several methods that can be used for reducing the domain of a step function.  Furthermore intervals not belonging to the domain are propagated through the application of arithmetic operators, logical operators and relational operators.

Currently there is only one method for enlarging the domain of a step function: :meth:`staircase.Stairs.fillna`.  This method is similar to its pandas counterpart :meth:`pandas.Series.fillna`, in that it aims to replace null values, however it differs slightly in the semantics of parameters.

The method :meth:`staircase.Stairs.fillna` takes one parameter, which can be either a real number, or a string corresponding to a method.  These method names are taken from pandas and indicate the following behaviour:

- ``pad / ffill`` propagate last defined value forward
- ``backfill / bfill`` propagate next defined value backward

For example:

.. plot::
    :context: close-figs
    :include-source: False

    >>> sf = sc.Stairs(start=[2,3,4], end=[5,4,6], value=[1,2,-1])
    >>> masker = sc.Stairs().layer(None,3,2).layer(5,6);
    >>> fig, axes = plt.subplots(ncols=2, figsize=(7,3), sharex=True, sharey=True)
    >>> sf.where(masker).plot(ax=axes[0], arrows=True);
    >>> axes[0].set_title("sf.where(masker)");
    >>> sf.where(masker).fillna(0).plot(ax=axes[1], arrows=True);
    >>> axes[1].set_title("sf.where(masker).fillna(0)")

.. plot::
    :context: close-figs
    :include-source: False

    >>> sf = sc.Stairs(start=[2,3,4], end=[5,4,6], value=[1,2,-1])
    >>> masker = sc.Stairs().layer(None,3,2).layer(5,6);
    >>> fig, axes = plt.subplots(ncols=2, figsize=(7,3), sharex=True, sharey=True)
    >>> sf.where(masker).plot(ax=axes[0], arrows=True);
    >>> axes[0].set_title("sf.where(masker)");
    >>> sf.where(masker).fillna("ffill").plot(ax=axes[1], arrows=True);
    >>> axes[1].set_title('sf.where(masker).fillna("ffill")')

.. plot::
    :context: close-figs
    :include-source: False

    >>> masker = sc.Stairs().layer(None,3,2).layer(5,6);
    >>> fig, axes = plt.subplots(ncols=2, figsize=(7,3), sharex=True, sharey=True)
    >>> sf.where(masker).plot(ax=axes[0], arrows=True);
    >>> axes[0].set_title("sf.where(masker)");
    >>> sf.where(masker).fillna("bfill").plot(ax=axes[1], arrows=True);
    >>> axes[1].set_title('sf.where(masker).fillna("bfill")')


isna/notna
*************

Finally, continuing on the theme of counterpart methods in pandas, we have :meth:`staircase.Stairs.isna` and :meth:`staircase.Stairs.notna` which return boolean valued step functions.

.. plot::
    :context: close-figs
    :include-source: False

    >>> masker = sc.Stairs().layer(None,3,2).layer(5,6);
    >>> fig, axes = plt.subplots(ncols=2, figsize=(7,3), sharex=True, sharey=True)
    >>> sf.where(masker).plot(ax=axes[0], arrows=True);
    >>> axes[0].set_title("sf.where(masker)");
    >>> sf.where(masker).isna().plot(ax=axes[1], arrows=True);
    >>> axes[1].set_title('sf.where(masker).isna()')

.. plot::
    :context: close-figs
    :include-source: False

    >>> masker = sc.Stairs().layer(None,3,2).layer(5,6);
    >>> fig, axes = plt.subplots(ncols=2, figsize=(7,3), sharex=True, sharey=True)
    >>> sf.where(masker).plot(ax=axes[0], arrows=True);
    >>> axes[0].set_title("sf.where(masker)");
    >>> sf.where(masker).notna().plot(ax=axes[1], arrows=True);
    >>> axes[1].set_title('sf.where(masker).notna()')

.. ipython:: python
    :suppress:
 
    plt.close("all")

.. rubric:: Footnotes
.. [*] Note that :meth:`pandas.Series.mask` and :meth:`pandas.Series.where` are more general purpose than what is described here.