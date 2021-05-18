.. _api.Stairs:

==============
Stairs methods
==============
.. currentmodule:: staircase

Constructor & basic methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autosummary::
   :toctree: api/

   Stairs
   Stairs.copy
   Stairs.plot
   Stairs.sample
   Stairs.layer
   Stairs.step_changes
   Stairs.to_dataframe
   
.. _api.arithmetic_operators:
 
Arithmetic operators
~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: api/

   Stairs.negate
   Stairs.add
   Stairs.subtract
   Stairs.multiply
   Stairs.divide

.. _api.relational_operators:
   
Relational operators
~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: api/

   Stairs.lt
   Stairs.gt
   Stairs.le
   Stairs.ge
   Stairs.eq
   Stairs.ne
   Stairs.identical
   
.. _api.logical_operators:

Logical operators
~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: api/
   
   Stairs.make_boolean
   Stairs.invert
   Stairs.logical_and
   Stairs.logical_or

.. _api.statistical_operators:

Statistical operators
~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: api/
   
   Stairs.cov
   Stairs.corr

.. _api.summary_statistics:

Summary statistics
~~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: api/

   Stairs.number_of_steps
   Stairs.get_integral_and_mean
   Stairs.integrate
   Stairs.describe
   Stairs.min
   Stairs.max
   Stairs.var
   Stairs.std
   Stairs.mean
   Stairs.median
   Stairs.percentile
   Stairs.percentile_stairs
   Stairs.ecdf_stairs
   Stairs.hist
   
   
Miscellaneous functions
~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: api/
   
   Stairs.clip
   Stairs.shift
   Stairs.diff
   Stairs.rolling_mean
   Stairs.resample
   Stairs.clip
   
