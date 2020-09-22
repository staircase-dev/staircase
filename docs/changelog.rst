=========
Changelog
=========

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