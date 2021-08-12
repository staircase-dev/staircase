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

While much of the API has remained the same there are many backwards incompatible changes.  These will be detailed here soon.  Stay tuned.