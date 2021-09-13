.. _release_notes.changelog:


=========
Changelog
=========

UNRELEASED
- bugfix for incorrect closed parameter not being produced by operations with right-closed step functions (#GH95)
- bugfix for slicing with non-fixed frequency period index (#GH108)
- bugfix for Stairs binary operations with np.nan reporting incorrect number of step changes (#GH109)
- throw `ClosedMismatchError` on binary operations with different `closed` values (#GH96) (@amagee)
- added test for :meth:`staircase.Stairs.logical_xor` with two Stairs arguments


v2.0.0 2021-08-25

- see :ref:`What's new in Version 2 <release_notes.versiontwo>`


v1.6.6 2021-07-06

- workaround for groupby bug in pandas 1.3.0 (GH42395)


v1.6.5 2021-06-14

- bugfix for :meth:`staircase.Stairs.mode`


v1.6.4 2021-03-16

- bugfix for broken functionality for multiplication, or division, of staircase.Stairs with a number


v1.6.3 2021-02-26

- bugfix for missing *lower_how* and *upper_how* parameters in :meth:`staircase.Stairs.resample`
- renamed Stairs._values to avoid error when performing Series.groupby.sum in pandas>=1.2
 

v1.6.2 2020-01-13

- efficiency improvement for :meth:`staircase.Stairs.multiply`


v1.6.1 2020-12-30

- bugfix for :meth:`staircase.Stairs.plot` when using datetimes and step function has no step changes


v1.6.0 2020-11-10

- support for `timezones` added
- bugfix for :func:`staircase.sample` when *points* == None (-inf is no longer included)
- bugfix for :func:`staircase.aggregate` where Stairs objects have non-zero value at -inf


v1.5.2 2020-10-20

- bugfix for :meth:`staircase.Stairs.layer` when None appears in vector parameters start and end


v1.5.1 2020-10-15

- removed dependency on 'private' methods in sortedcontainers
- increased upper limit for version dependency on sortedcontainers


v1.5.0 2020-10-12

- fixed typo in diff docstring
- extended :meth:`staircase.Stairs.values_in_range` to allow specification of how endpoints of domain should be evaluated
- extended :meth:`staircase.Stairs.min` to allow specification of how endpoints of domain should be evaluated
- extended :meth:`staircase.Stairs.max` to allow specification of how endpoints of domain should be evaluated
- extended :meth:`staircase.Stairs.sample` to allow specification of how endpoints of domain should be evaluated
- extended :meth:`staircase.Stairs.resample` to allow specification of how endpoints of domain should be evaluated
- added :meth:`staircase.Stairs.rolling_mean`
- added example usage of rolling_mean to Queue Analysis tutorial


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
