"""
isort:skip_file
"""

from staircase.constants import inf
from staircase.core.stairs import Stairs, _add_operations
from staircase.core.arrays.aggregation import _aggregate as agg
from staircase.core.arrays.aggregation import _max as max
from staircase.core.arrays.aggregation import _mean as mean
from staircase.core.arrays.aggregation import _median as median
from staircase.core.arrays.aggregation import _min as min
from staircase.core.arrays.aggregation import _sum as sum
from staircase.core.arrays.transform import corr, cov, limit, sample
from staircase.core.slicing import StairsSlicer
from staircase.core.stats.distribution import Dist
from staircase.test_data import make_test_data

_add_operations()


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
