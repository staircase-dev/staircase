.. _user_guide.faq:


Frequently asked questions
==========================

.. dropdown:: Can any step function be modelled?

    Unfortunately no.  The intervals comprising a step function must have non-zero length and either be all left-closed right-open, or right-open left-closed.  Also, there cannot be an infinite number of intervals.


.. dropdown:: What happens if I call :meth:`staircase.Stairs.layer` with default arguments?

    The default arguments for *start*, *end* and *value* in :meth:`staircase.Stairs.layer` are all None, as per the method signature.  However the internals of staircase will treat them as -infinity, infinity and 1 respectively.  The result of this will be increasing the value of a step function by 1 everywhere.  For a discussion around this choice please see  :ref:`user_guide.layering` and then :ref:`user_guide.gotchas`.

.. dropdown:: Why can't I calculate the integral of my step function?

    This is an issue which can arise when using a datetime domain.  The result of an integral calculated on such a step function is expressed as a :class:`pandas.Timedelta`.  Unfortunately this class has `limitations <https://pandas.pydata.org/pandas-docs/stable/user_guide/timedeltas.html#timedelta-limitations>`_ which may be exceeded with integral calculations.  A workaround may involve scaling your step function values down before calculating the integral, eg:

    >>> (my_step_function/1000).integral()
       
.. dropdown:: Can I work with :mod:`datetime` data?

    Yes, and :class:`numpy.datetime` too.  However, pandas converts these types to its own :class:`pandas.Timestamp` type, and consequently staircase does too.  If you need to convert a result back to your desired class then you can do so with 
    
    - :meth:`pandas.Timestamp.to_pydatetime`,
    - :meth:`pandas.Timestamp.to_datetime64`,
    - :meth:`pandas.Timedelta.to_pytimedelta` and
    - :meth:`pandas.Timedelta.to_timedelta64`.

.. dropdown:: Can I use method chaining?

    Yes, and it is encouraged.  The layer function, arithmetic functions, logical functions, relational functions all return instances of :class:`staircase.Stairs`.  In addition :meth:`staircase.Stairs.pipe` was added in v2 to further facilitate chaining.

.. dropdown:: What is `sc.inf`?

    `staircase.inf` is a singleton object of :class:`staircase.Inf`, which is used to represent the concept of infinity within staircase domains (regardless of domain type).  You are welcome to use it and its negative counterpart (`-staircase.inf`) when specifying domain bounds but the use of `None` can be substituted in place.

    For example,

    >>> my_step_function.clip(-sc.inf, 10)
    
    is equivalent to

    >>> my_step_function.clip(None, 10)


.. dropdown:: Does my step function plot have infinite intervals?

    A step function can have at most two infinite intervals, which trail off to negative and positive infinity respectively.  When inspecting the step function with :meth:`staircase.to_frame` it will be obvious if the step function has infinite intervals.  If they exist they will be listed in the first and last rows of the dataframe.  You may also be able to infer an answer to this question from a plot.
    
    .. plot::
        :context: close-figs
        :include-source: False

        >>> sf = sc.Stairs().layer([0,1,2], [3,6,7])
        >>> fig, axes = plt.subplots(ncols=2, figsize=(7,3), sharex=True, sharey=True)
        >>> sf.plot(axes[0])
        >>> sf.clip(None, 7).plot(axes[1])

    In the above example, the step function on the left has two infinite intervals (each having a value of 0).  The step function on the right only has one infinite interval, trailing off to negative infinity.  For all domain values greater than 7 the step function is undefined.  The difference between these two step function can be noticed from the above plot by a keen observer.  If a plot is produced with an argument `style = "hlines"` then it will be impossible to identify infinite intervals in the plot unless `arrows = True`.  See :meth:`staircase.plot` for details on these parameters.


.. dropdown:: Can I use generators as inputs to :meth:`staircase.Stairs.layer`?

    No, however you can use lists, tuples, :class:`pandas.Series`, :class:`numpy.ndarray`