import pandas as pd

import staircase.core.arrays.accessor  # registers the accessor with pandas
from staircase.constants import inf
from staircase.core.arrays.extension import StairsArray


def agg(collection, func):
    return StairsArray(collection).agg(func)


def max(collection):
    return StairsArray(collection).max()


def min(collection):
    return StairsArray(collection).min()


def mean(collection):
    return StairsArray(collection).mean()


def median(collection):
    return StairsArray(collection).median()


def sum(collection):
    return StairsArray(collection).sum()


def logical_or(collection):
    return StairsArray(collection).logical_or()


def logical_and(collection):
    return StairsArray(collection).logical_and()


def corr(collection, where=(-inf, inf)):
    return pd.Series(collection, dtype="Stairs").sc.corr(where)


def cov(collection, where=(-inf, inf)):
    return pd.Series(collection, dtype="Stairs").sc.cov(where)


def limit(collection, x, side="right"):
    return pd.Series(collection, dtype="Stairs").sc.limit(x, side)


def sample(collection, x):
    return pd.Series(collection, dtype="Stairs").sc.sample(x)
