from staircase.core.stairs import Stairs, sample, resample, aggregate, corr, cov

from staircase.core.stats import hist_from_ecdf

from staircase.core.stairs import _mean as mean
from staircase.core.stairs import _median as median
from staircase.core.stairs import _min as min
from staircase.core.stairs import _max as max

from .test_data import make_test_data


def get_version():
    def get_version_post_py38():
        from importlib.metadata import version

        return version(__name__)

    def get_version_pre_py38():
        from pkg_resources import get_distribution

        return get_distribution(__name__).version

    def default():
        return "unknown"

    for func in (get_version_post_py38, get_version_pre_py38, default):
        try:
            return func()
        except Exception:
            pass


__version__ = get_version()
