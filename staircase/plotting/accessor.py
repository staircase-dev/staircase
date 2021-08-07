from staircase.plotting import docstrings
from staircase.plotting.matplotlib import plot as plot_matplotlib
from staircase.util._decorators import Appender


class PlotAccessor:
    def __init__(self, stairs):
        self._stairs = stairs

    def _dist(self):
        return self._stairs.dist

    @Appender(docstrings.matplotlib_docstring, join="\n", indents=1)
    def __call__(self, *args, backend="matplotlib", **kwargs):
        # register_matplotlib_converters()
        if self._stairs._data is None:
            return
        if backend == "matplotlib":
            return plot_matplotlib(self._stairs, *args, **kwargs)
        else:
            raise Exception

    def ecdf(self, backend="matplotlib", **kwargs):
        if backend == "matplotlib":
            return plot_matplotlib(self._dist().ecdf, **kwargs)
        else:
            raise ValueError(f"Plotting backend {backend} not defined for ecdf")


def _get_plot(self, **kwargs):
    if self._plot is None:
        self._plot = PlotAccessor(self, **kwargs)
    return self._plot
