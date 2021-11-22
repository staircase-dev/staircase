.. _intro_tutorials.stats:

What statistical properties are available?
==========================================

Anybody who has done a course in basic statistics will be comfortable with most of the single-variable summary statistics that :mod:`staircase` makes available.  However these statistics were likely performed on a finite set of samples, i.e. observations of the variable.  When the variable in question is the value of a step function we do not have a finite set of observations.  This is because a step function is composed of intervals, and every interval contains an infinite number of points.  So a step function gives rise to an infinite set of points?  Yes.  The resulting math to calculate summary statistics may be a little different from their finite-set counterparts but the concepts remain the same.  The following statistics can all be performed on step functions:

* :meth:`staircase.Stairs.min`
* :meth:`staircase.Stairs.max`
* :meth:`staircase.Stairs.median`
* :meth:`staircase.Stairs.mode`
* :meth:`staircase.Stairs.mean`
* :meth:`staircase.Stairs.integral`
* :meth:`staircase.Stairs.var`
* :meth:`staircase.Stairs.std`

The definitions are considered assumed, however examples can be found in the corresponding entries in the :ref:`API reference <user_guide>`.

In staircase v1 these methods featured parameters which indicated the domain over which to perform the calculation.  In v2 these parameters have been removed in favour of :ref:`clipping <user_guide.clipping>`, which is described in the :ref:`user guide section on masking <user_guide.masking>`.

There remains one statistical method which features a domain parameter: :meth:`staircase.Stairs.agg`.  This method accepts a string corresponding to the required statistic, eg "median", a tuple representing the domain interval over which to calculate, and a parameter which indicates whether the interval should be considered closed on both sides, left-closed,
right-closed, or neither.  This *closed* parameter is only relevant when calculating *min* or *max*.  To begin to understand why this might be true, recall that we are dealing with an infinite set of points.  

There are further statistical methods which are beyond the scope of this introduction, namely :meth:`staircase.Stairs.cov` and :meth:`staircase.Stairs.corr` for calculating covariance and correlation respectively.  For analysis which goes beyond summary statistics to evaluating the distribution of the step function values see :ref:`Distribution of values <user_guide.distributions>`.