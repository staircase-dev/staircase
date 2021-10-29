.. _intro_tutorials.domains:

What domains and range are possible?
====================================

Let's quickly revise what *domain* and *range* refer to in the language of (mathematical) functions.

The **domain** is the set of all possible inputs for a function.

The **range** is the set of all possible outputs, or values for a function.  


:mod:`staircase` is designed with two domain types in mind: real numbers and time - or in the language of Python computing, floats and datetimes.
However this is not to say that other domains are not possible.  If the domain is totally ordered and is compatible with Python's *bisect* module, and :func:`numpy.searchsorted`, then there is a reasonable chance that it could be used with staircase 2.*.  Support for *timedelta* domains was added in v2.1.

For datetime domains, staircase (v2) has been tested with :class:`numpy.datetime64`, :class:`datetime.datetime`, and :class:`pandas.Timestamp`, including **time-zone aware** variants for the latter two of these.

For timedelta domains, staircase (v2.1)  has been tested with :class:`numpy.timedelta64`, :class:`datetime.timedelta`, and :class:`pandas.Timedelta`.

Prior to v2 the domain of a step function always extended from negative infinity to positive infinity, however the ability to exclude intervals from the domain (where the step function is undefined) was introduced in v2 via masking.

The range of step functions in staircase are the real numbers only.

