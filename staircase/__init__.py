try:
    from ._version import get_versions
    __version__ = get_versions()['version']
    del get_versions
except Exception:
    __version__ = ''

from staircase.core.stairs import (
    Stairs, sample, resample,
    aggregate,
    corr, cov
)

from staircase.core.stats import hist_from_ecdf

from staircase.core.stairs import _mean as mean
from staircase.core.stairs import _median as median
from staircase.core.stairs import _min as min
from staircase.core.stairs import _max as max

from .test_data import make_test_data
