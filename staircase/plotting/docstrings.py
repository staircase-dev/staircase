matplotlib_docstring = """
Plots the step function.

Parameters
----------
ax : :class:`matplotlib.axes.Axes`, optional
    Pre-existing axes to plot onto.
style : {"step", "hlines"}, default "step"
    Indicates whether the plot is based on :meth:`matplotlib.axes.Axes.step`
    or :meth:`matplotlib.axes.Axes.hlines`
arrows : bool, default False
    Whether or not to plot arrows where there exist intervals of infinite length
arrow_kwargs : dict or None, default None
    Additional keyword parameters passed to :meth:`matplotlib.axes.Axes.arrow`

Returns
-------
:class:`matplotlib.axes.Axes`

Examples
--------

.. plot::
    :context: close-figs

    >>> s1.plot()


.. plot::
    :context: close-figs

    >>> s1.plot(arrows=True)


.. plot::
    :context: close-figs

    >>> s1.plot(style="hlines", arrows=True)

"""
