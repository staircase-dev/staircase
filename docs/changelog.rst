=========
Changelog
=========

v1.0.0

- Updated documentation to include :ref:`A note on interval endpoints<getting_started.interval_endpoints>`
- parameter *start* in :meth:`staircase.Stairs.layer` made optional to make method symmetric with respect to time
- removed *staircase.Stairs.evaluate* method (superseded by :meth:`staircase.Stairs.sample`)