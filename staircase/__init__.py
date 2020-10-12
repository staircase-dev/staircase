try:
    from ._version import get_versions
    __version__ = get_versions()['version']
    del get_versions
except Exception as e:
    __version__ = ''

from .stairs import Stairs, sample, resample, aggregate, hist_from_ecdf, corr, cov
from .stairs import _mean as mean
from .stairs import _median as median
from .stairs import _min as min
from .stairs import _max as max

from .test_data import make_test_data
