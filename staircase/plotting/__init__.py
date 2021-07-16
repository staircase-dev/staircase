from .matplotlib import plot as plot_matplotlib


def plot(self, backend="matplotlib", **kwargs):
    """
    Makes a step plot representing the finite intervals belonging to the Stairs instance.

    Uses matplotlib as a backend.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`, default None
        Allows the axes, on which to plot, to be specified
    **kwargs
        Options to pass to :function: `matplotlib.pyplot.step`

    Returns
    -------
    :class:`matplotlib.axes.Axes`
    """
    # register_matplotlib_converters()
    if self._data is None:
        return
    self._ensure_values()
    if backend == "matplotlib":
        return plot_matplotlib(self, **kwargs)
    else:
        raise Exception


def add_methods(cls):
    cls.plot = plot
