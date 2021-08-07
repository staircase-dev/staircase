.. _user_guide.slicing:

Slicing
========

* new in V2
* part pandas.cut, part pandas.groupby
* "A groupby operation involves some combination of splitting the object, applying a function, and combining the results. This can be used to group large amounts of data and compute operations on these groups."
* divides the step function into slices, which we can then operate on
* we get back a StairsSlicer object
* do interval indexes need to be non-overlapping?
* can i have gaps between intervals in my interval indexes

