=========
Changelog
=========

v1.4.0 2020-10-05

- extended :meth:`staircase.Stairs.corr` to facilitate cross-correlation and autocorrelation
- extended :meth:`staircase.Stairs.cov` to facilitate cross-covariance and autocovariance


v1.3.0 2020-10-01

- added :meth:`staircase.Stairs.describe`
- added :meth:`staircase.Stairs.var` (variance)
- added :meth:`staircase.Stairs.std` (standard deviation)
- added :meth:`staircase.Stairs.corr` (correlation)
- added :meth:`staircase.Stairs.cov` (covariance)
- added :func:`staircase.cov` (pairwise covariance matrix)
- added :func:`staircase.corr` (pairwise correlation matrix)


v1.2.0 2020-09-23

- added :meth:`staircase.Stairs.hist`
- added :meth:`staircase.Stairs.ecdf_stairs`
- added :func:`staircase.hist_from_ecdf`
- added :func:`staircase.make_test_data`
- :meth:`staircase.Stairs.percentile_Stairs` pending deprecation in favour of :meth:`staircase.Stairs.percentile_stairs`


v1.1.1 2020-09-22

- bugfix for :meth:`staircase.Stairs.sample` when parameter x = float("-inf")


v1.1.0 2020-09-15

- added :meth:`staircase.Stairs.shift`
- added :meth:`staircase.Stairs.diff`


v1.0.3 2020-09-08

- *deep* parameter added to :meth:`staircase.Stairs.copy` method for pandas compatability


v1.0.[1|2] 2020-09-02

- bugfix with Pandas 1.1.x where SortedSet cannot be used as basis for Series or DataFrame


v1.0.0 2020-09-01

- updated documentation to include :ref:`A note on interval endpoints<getting_started.interval_endpoints>`
- parameter *start* in :meth:`staircase.Stairs.layer` made optional to make method symmetric with respect to time
- removed *staircase.Stairs.evaluate* method (superseded by :meth:`staircase.Stairs.sample`)