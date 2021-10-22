.. _userguide.overview:

Package overview
=================================

The staircase package is used to model step functions. Step functions can be used to represent continuous time series - think changes in state over time, queue size over time, utilisation over time, success rates over time - you get the idea.

The package is built upon :mod:`numpy` and :mod:`pandas`, with a deliberate, stylistic alignment to the latter introduced in :ref:`version 2 <release_notes.versiontwo>`.

The staircase package makes converting raw, temporal data into time series easy and readable. Furthermore there is a rich variety of :ref:`arithmetic operations <api.arithmetic_operators>`, :ref:`relational operations <api.relational_operators>`, :ref:`logical operations <api.logical_operators>`, :ref:`statistical operations <api.statistical_operators>`, to enable analysis, in addition to functions for :ref:`univariate analysis <api.summary_statistics>`, :ref:`aggregations <api.array_funcs>` and compatibility with datetimes.


Versioning
-----------

`SemVer <http://semver.org/>`_ is used by :mod:`staircase` for versioning releases.  For versions available, see the `tags on this repository <https://github.com/staircase-dev/staircase/tags>`_.  It is highly recommended to use version 2, for both performance and additional features.


License
--------

This project is licensed under the MIT License::

    Copyright © 2020-2021 <Riley Clement>

    Permission is hereby granted, free of charge, to any person obtaining a copy of this
    software and associated documentation files (the “Software”), to deal in the Software
    without restriction, including without limitation the rights to use, copy, modify, 
    merge, publish, distribute, sublicense, and/or sell copies of the Software, and to 
    permit persons to whom the Software is furnished to do so, subject to the following 
    conditions:

    The above copyright notice and this permission notice shall be included in all copies 
    or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
    INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
    PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
    FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
    OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
    DEALINGS IN THE SOFTWARE.


Acknowledgement
----------------

The seeds of :mod:`staircase` began developing at the Hunter Valley Coal Chain Coordinator, where it finds strong application in analysing simulated data.

We also recognise that two classes have been borrowed, with minor adjustments, from the :mod:`pandas` source code:

    - :class:`pandas.util._decorators.Appender`
    - :class:`pandas.core.accessor.CachedAccessor`