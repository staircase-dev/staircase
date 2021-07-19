from .accessor import _get_plot


def add_methods(cls):
    cls._get_plot = _get_plot
