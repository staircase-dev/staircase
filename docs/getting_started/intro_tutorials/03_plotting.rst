.. _intro_tutorials.plotting:

What does my step function look like?
=====================================

.. ipython:: python
    :suppress:
    
    import staircase as sc
    sf = sc.Stairs().layer([1,4,2], [3,6,5], [1,1,2])

To plot our step function *sf* from the previous tutorial is straightforward:

.. ipython:: python

    @savefig intro_tutes_plot.png
    sf.plot();

Compare this to the result of :meth:`staircase.Stairs.to_frame`.

.. ipython:: python

    sf.to_frame()

We can see that the first, and last, intervals in our step function have infinite length.  Such intervals cannot be plotted, of course, however we can use the *arrows* parameter to indicate they exist.

.. ipython:: python

    @savefig intro_tutes_plot_arrows.png
    sf.plot(arrows=True);

Another stylistic choice is whether to connect adjacent intervals with vertical lines or not.  This can be achieved with the *style* parameter.  :mod:`Matplotlib` provides the backend for plotting and we can make use of the *ax* parameter to pass in a :class:`matplotlib.axes.Axes` argument.

.. ipython:: python

    fig, axes = plt.subplots(ncols=2, figsize=(7,3), sharey=True, sharex=True, tight_layout=True)
    sf.plot(ax=axes[0], arrows=True, style="step");
    @savefig intro_tutes_plot_style.png
    sf.plot(ax=axes[1], arrows=True, style="hlines");


Any additional parameters are passed through through to Matplotlib:

.. ipython:: python

    ax = sf.plot(arrows=True, style="hlines", linewidth=3, color="green", label="sf")
    @savefig intro_tutes_plot_params.png
    ax.legend();