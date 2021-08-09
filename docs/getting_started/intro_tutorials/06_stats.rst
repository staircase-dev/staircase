.. _intro_tutorials.stats:

What statistical properties are available?
==========================================

standard ones

* :meth:`staircase.Stairs.min`
* :meth:`staircase.Stairs.max`
* :meth:`staircase.Stairs.median`
* :meth:`staircase.Stairs.mode`
* :meth:`staircase.Stairs.mean`
* :meth:`staircase.Stairs.integral`
* :meth:`staircase.Stairs.var`
* :meth:`staircase.Stairs.std`

* clipping

* min/max

* agg
  
* functions which ignore infinite intervals


.. ipython:: python

    import staircase as sc
    
    sf = sc.Stairs()
    sf.to_frame()
    
Blah blah

.. ipython:: python

    sf.layer(1)
    sf.to_frame()