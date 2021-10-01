.. _user_guide.layering:

The layer method
=================

The layer method is unique among all :class:`staircase.Stairs` methods - it is the only mutator method, and is the only method which modifies the step function in place, as opposed to acting on a copy.  It is a very flexible method, taking full advantage of defaults and weak typing afforded by Python.

The layer method was introduced in :ref:intro_tutorials.creating, in which parameters were either all numbers, or all vectors.  Advanced usage allows certain combinations of these, and may allow vectors of different lengths.  Understanding these features is key to ensure they do not result in bugs, or unwanted effects.

For those who are mathematically inclined, a set of axioms pertaining to the layer method can be found at the bottom of the page.  The expected behaviour of any call to :meth:`staircase.Stairs.layer` can be derived from these axioms.  Alternatively, the key ideas are summarised below:

.. raw:: html

    <h4>1) A null value in the <i>start</i> parameter corresponds to -infinity.  A null value in the <i>end</i> parameter corresponds to infinity.</h4>

.. plot::
    :context: close-figs
    :include-source: False

    >>> fig, axes = plt.subplots(nrows=1, ncols=2,  figsize=(7,3), tight_layout=True)
    >>> sc.Stairs().layer(start=2).plot(ax=axes[0], arrows=True)
    >>> axes[0].set_title("sc.Stairs().layer(start=2)")
    >>> sc.Stairs().layer(end=2).plot(ax=axes[1], arrows=True)
    >>> axes[1].set_title("sc.Stairs().layer(end=2)")

.. raw:: html

    <h4>2) A scalar value for <i>start</i> is equivalent to [<i>start</i>].  A scalar value for <i>end</i> is equivalent to [<i>end</i>].</h4>

.. plot::
    :context: close-figs
    :include-source: False

    >>> fig, axes = plt.subplots(nrows=1, ncols=3,  figsize=(8,3), sharey=True, sharex=True, tight_layout=True)
    >>> sc.Stairs().layer(1, 2).plot(ax=axes[0], arrows=True)
    >>> axes[0].set_title("sc.Stairs().layer(1, 2)")
    >>> sc.Stairs().layer([1], 2).plot(ax=axes[1], arrows=True)
    >>> axes[1].set_title("sc.Stairs().layer([1], 2)")
    >>> sc.Stairs().layer(1, [2]).plot(ax=axes[2], arrows=True)
    >>> axes[2].set_title("sc.Stairs().layer(1, [2])")

.. raw:: html

    <h4>3) If <i>start</i> and <i>end</i> are vectors of differing size, then null values are appended to the smallest till they are equal in length.</h4>

And don't forget the meaning of null values according to rule 1!

.. plot::
    :context: close-figs
    :include-source: False

    >>> fig, axes = plt.subplots(nrows=1, ncols=2,  figsize=(7,3), sharey=True, sharex=True, tight_layout=True)
    >>> sc.Stairs().layer([1,2], [3]).plot(ax=axes[0], arrows=True)
    >>> axes[0].set_title("sc.Stairs().layer([1,2], [3])")
    >>> sc.Stairs().layer([1], [2,3]).plot(ax=axes[1], arrows=True)
    >>> axes[1].set_title("sc.Stairs().layer([1], [2,3])")

.. raw:: html

    <h4>4) A scalar value for <i>value</i> is equivalent to a vector, filled with <i>value</i>, whose length is equal to the larger of <i>start</i> and <i>end</i>.</h4>

.. plot::
    :context: close-figs
    :include-source: False

    >>> ax = sc.Stairs().layer([1,2], [3], 2).plot(arrows=True)
    >>> ax.set_title("sc.Stairs().layer([1,2], [3], 2)")

.. raw:: html

    <h4>5) A vector value for <i>value</i> must have the same length as the largest of <i>start</i> and <i>end</i>.</h4>

An error will result otherwise.


Test your knowledge
********************

What do you think the result of `sc.Stairs().layer()` might be?  See discussion and answer in :ref:`user_guide.gotchas`.


Axioms
*******

inf\ :sub:`i`\ = inf (infinity) for all i

* .layer(s, e) = .layer(s, e, None) = .layer(s, e, 1)
* .layer(s, None, v) = .layer(s, inf, v)
* .layer(None, e, v) = .layer(-inf, e, v)
* .layer(s, e, v) is the same as .layer(s, None, v).layer(s, None, -v) provided s, e not None
  
* .layer([s], _, _) = .layer(s, _, _)
* .layer(_, [e], _) = .layer(_, e, _)

* .layer([s\ :sub:`1`\, ..., s\ :sub:`n`\], [e\ :sub:`1`\, ..., e\ :sub:`n`\], v) = .layer([s\ :sub:`1`\, ..., s\ :sub:`n`\], [e\ :sub:`1`\, ..., e\ :sub:`n`\], [v\ :sub:`1`\, ..., v\ :sub:`n`\]) where v\ :sub:`i`\ = v for all i

* .layer([s\ :sub:`1`\, ..., s\ :sub:`n`\], [e\ :sub:`1`\, ..., e\ :sub:`n`\], [v\ :sub:`1`\, ..., v\ :sub:`n`\]) = layer([s\ :sub:`1`\, ..., s\ :sub:`n-1`\], [e\ :sub:`1`\, ..., e\ :sub:`n-1`\], [v\ :sub:`1`\, ..., v\ :sub:`n-1`\]).layer(s\ :sub:`n`\, e\ :sub:`n`\, v\ :sub:`n`\)

* .layer([s\ :sub:`1`\, ..., s\ :sub:`n`\], [e\ :sub:`1`\, ..., e\ :sub:`k`\], _) = .layer([s\ :sub:`1`\, ..., s\ :sub:`n`\], [e\ :sub:`1`\, ..., e\ :sub:`k`\, inf\ :sub:`1`\, ..., inf\ :sub:`n-k`\,], _) if n > k

* .layer([s\ :sub:`1`\, ..., s\ :sub:`n`\], [e\ :sub:`1`\, ..., e\ :sub:`k`\], _) = .layer([s\ :sub:`1`\, ..., s\ :sub:`n`\, -inf\ :sub:`1`\, ..., -inf\ :sub:`k-n`\,], [e\ :sub:`1`\, ..., e\ :sub:`k`\], _) if k > n

  