.. _getting_started.faq:


Frequently Asked Questions
==========================

.. dropdown:: Can any step function be modelled?
    :container: + shadow
    :title: bg-primary text-white

    Unfortunately no.  The intervals comprising a step function must have non-zero length and either be all left-closed right-open, or right-open left-closed.  Also, there cannot be an infinite number of intervals.


.. dropdown:: What happens if I call :meth:`staircase.Stairs.layer` with default arguments?

    The default arguments for *start*, *end* and *value* in :meth:`staircase.Stairs.layer` are all None, as per the method signature.  However the internals of staircase will treat them as -infinity, infinity and 1 respectively.  The result of this will be increasing the value of a step function by 1 everywhere.  For a discussion around this choice please see...

.. dropdown:: Why can't I calculate the integral of my step function?

    This is an issue which can arise when using a datetime domain.  The result of an integral calculated on such a step function is expressed as a :class:`pandas.Timedelta`.  Unfortunately this class has `limitations <https://pandas.pydata.org/pandas-docs/stable/user_guide/timedeltas.html#timedelta-limitations>`_ which may be exceeded with integral calculations.  A workaround may involve scaling your step function values down before calculating the integral, eg:

    >>> (my_step_function/1000).integral()
       
.. dropdown:: Can I work with :mod:`datetime` data?

    Yes, and :class:`numpy.datetime` too.  However, pandas converts these types to its own :class:`pandas.Timestamp` type, and consequently staircase does too.  If you need to convert a result back to your desired class then you can do so with :meth:`pandas.Timestamp.to_pytimedelta`, :meth:`pandas.Timestamp.to_timedelta64`, :meth:`pandas.Timedelta.to_pytimedelta` and :meth:`pandas.Timedelta.to_timedelta64`.

.. dropdown:: Can I use method chaining?

    Yes, and it is encouraged.  The layer function, arithmetic functions, logical functions, relational functions all return instances of :class:`staircase.Stairs`.  In addition :meth:`staircase.Stairs.pipe` was added in v2 to further facilitate chaining.

.. dropdown:: What is sc.inf?

    blah blah

.. dropdown:: Does my step function plot have infinite intervals?

    blah blah