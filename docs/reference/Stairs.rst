.. _api.Stairs:

==============
Stairs
==============
.. currentmodule:: staircase

Constructor & basic methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autosummary::
   :toctree: api/

   Stairs.__init__
   Stairs.copy
   Stairs.sample
   Stairs.limit
   Stairs.layer
   Stairs.step_changes
   Stairs.to_frame
   
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
   Stairs.radd
   Stairs.rsubtract
   Stairs.rmultiply
   Stairs.rdivide

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
   Stairs.logical_xor
   Stairs.logical_rand
   Stairs.logical_ror
   Stairs.logical_rxor

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
   Stairs.integral
   Stairs.describe
   Stairs.values_in_range
   Stairs.min
   Stairs.max
   Stairs.var
   Stairs.std
   Stairs.mode
   Stairs.mean
   Stairs.median
   Stairs.value_sums
   Stairs.percentile
   Stairs.fractile
   Stairs.quantile
   Stairs.ecdf
   Stairs.hist
   
Plotting
~~~~~~~~~~~~~~~~~~ 

.. autosummary::
   :toctree: api/
   :template: autosummary/accessor_callable.rst

   Stairs.plot
   
   
Miscellaneous functions
~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: api/
   
   Stairs.clip
   Stairs.mask
   Stairs.where
   Stairs.isna
   Stairs.notna
   Stairs.fillna
   Stairs.shift
   Stairs.diff
   Stairs.rolling_mean
   Stairs.slice
   Stairs.pipe

