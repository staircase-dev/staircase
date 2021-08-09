.. _intro_tutorials.combining:

How do I combine step functions?
=================================

.. ipython:: python
    :suppress:
    
    import staircase as sc
    sf = sc.Stairs().layer([1,4,2], [3,6,5], [1,1,2])

Step functions can be added, subtracted, divided and multiplied together.  The :class:`staircase.Stairs` class provides these binary operator methods [*]_:

* :meth:`staircase.Stairs.add`
* :meth:`staircase.Stairs.subtract`
* :meth:`staircase.Stairs.divide`
* :meth:`staircase.Stairs.multiply`

To promote readability, these methods are ideally invoked using their operator symbols.  Note that we can use them in conjunction with floats and a number, *x*, is equivalent to ``sc.Stairs(initial_value=x)`` when used as an operand.  Instead of walking through each of these methods, let's roll the example into one:

.. ipython:: python

    fig, axes = plt.subplots(ncols=2, figsize=(7,3), tight_layout=True)
    sf.plot(ax=axes[0], arrows=True);
    @savefig intro_tutes_combining.png
    ((sf*sf + 2)/(4 - sf)).plot(ax=axes[1], arrows=True);

.. rubric:: Footnotes
.. [*] and their "reverse" operator counterparts