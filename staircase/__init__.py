from staircase.core.stairs import Stairs, _add_operations  # isort: skip

_add_operations()

from staircase.constants import inf
from staircase.core.arrays import (
    agg,
    corr,
    cov,
    limit,
    logical_and,
    logical_or,
    max,
    mean,
    median,
    min,
    plot,
    sample,
    sum,
)
from staircase.core.arrays.extension import StairsArray
from staircase.core.slicing import StairsSlicer
from staircase.core.stats.distribution import Dist
from staircase.test_data import make_test_data


def get_version():
    def get_version_post_py38():
        from importlib.metadata import version  # type: ignore

        return version(__name__)

    def get_version_pre_py38():
        from pkg_resources import get_distribution

        return get_distribution(__name__).version

    def default_version():
        return "unknown"

    for func in (get_version_post_py38, get_version_pre_py38, default_version):
        try:
            return func()
        except Exception:
            pass


__version__ = get_version()
