from staircase.plotting.matplotlib import plot as plot_matplotlib


class PlotAccessor:
    def __init__(self, stairs):
        self._stairs = stairs

    def _dist(self):
        return self._stairs.dist

    def __call__(self, backend="matplotlib", **kwargs):
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
        if self._stairs._data is None:
            return
        if backend == "matplotlib":
            return plot_matplotlib(self._stairs, **kwargs)
        else:
            raise Exception

    def ecdf(self, backend="matplotlib", **kwargs):
        if backend == "matplotlib":
            return plot_matplotlib(self._dist().get_ecdf(), **kwargs)
        else:
            raise ValueError(f"Plotting backend {backend} not defined for ecdf")


def _get_plot(self):
    if self._plot is None:
        self._plot = PlotAccessor(self)
    return self._plot
