.. _intro_tutorials.stepfunction:

What is a step function?
=========================

A step function, also known as a staircase function, is a piecewise constant function. In layman's terms this means if we were to draw a step function, we would draw a sequence of horizontal lines which don't overlap:

.. include:: stepfunctionplot.txt

In the left plot the step function is composed of left-closed right-open intervals, and in the right plot the step function is composed of left-open right-closed intervals.

To help clarify the characteristics of a step function we show two plots below which do not contain step functions. The chart on the left shows a function which is not piecewise-constant while the chart on the right shows a relation that fails to be a function.

.. include:: notstepfunctionplot.txt

So, can staircase represent any step function?  Not quite.  Currently the following restrictions apply:

- the intervals comprising a step function must have non-zero length and either be all left-closed right-open, or right-open left-closed.
- there cannot be an infinite number of intervals