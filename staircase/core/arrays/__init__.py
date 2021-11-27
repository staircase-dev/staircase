import pandas as pd

# registers the accessor with pandas
import staircase.core.arrays.accessor  # noqa
from staircase.constants import inf
from staircase.core.arrays import docstrings
from staircase.core.arrays.extension import StairsArray
from staircase.util._decorators import Appender


@Appender(docstrings.make_docstring("toplevel", "agg"), join="\n", indents=1)
def agg(collection, func):
    return StairsArray(collection).agg(func)


@Appender(docstrings.make_docstring("toplevel", "max"), join="\n", indents=1)
def max(collection):  # noqa
    return StairsArray(collection).max()


@Appender(docstrings.make_docstring("toplevel", "min"), join="\n", indents=1)
def min(collection):  # noqa
    return StairsArray(collection).min()


@Appender(docstrings.make_docstring("toplevel", "mean"), join="\n", indents=1)
def mean(collection):
    return StairsArray(collection).mean()


@Appender(docstrings.make_docstring("toplevel", "median"), join="\n", indents=1)
def median(collection):
    return StairsArray(collection).median()


@Appender(docstrings.make_docstring("toplevel", "sum"), join="\n", indents=1)
def sum(collection):  # noqa
    return StairsArray(collection).sum()


@Appender(docstrings.make_docstring("toplevel", "logical_or"), join="\n", indents=1)
def logical_or(collection):
    return StairsArray(collection).logical_or()


@Appender(docstrings.make_docstring("toplevel", "logical_and"), join="\n", indents=1)
def logical_and(collection):
    return StairsArray(collection).logical_and()


@Appender(docstrings.make_docstring("toplevel", "corr"), join="\n", indents=1)
def corr(collection, where=(-inf, inf)):
    return pd.Series(collection, dtype="Stairs").sc.corr(where)


@Appender(docstrings.make_docstring("toplevel", "cov"), join="\n", indents=1)
def cov(collection, where=(-inf, inf)):
    return pd.Series(collection, dtype="Stairs").sc.cov(where)


@Appender(docstrings.make_docstring("toplevel", "limit"), join="\n", indents=1)
def limit(collection, x, side="right"):
    return pd.Series(collection, dtype="Stairs").sc.limit(x, side)


@Appender(docstrings.make_docstring("toplevel", "sample"), join="\n", indents=1)
def sample(collection, x):
    return pd.Series(collection, dtype="Stairs").sc.sample(x)


@Appender(docstrings.make_docstring("toplevel", "plot"), join="\n", indents=1)
def plot(collection, ax=None, **kwargs):
    return pd.Series(collection, dtype="Stairs").sc.plot(ax, **kwargs)
