import pandas as pd
import pytest

import staircase as sc


def test_typing():
    from staircase._typing import (
        IO,
        TYPE_CHECKING,
        Any,
        AnyStr,
        Callable,
        Collection,
        Dict,
        Hashable,
        List,
        Mapping,
        Optional,
        Sequence,
        Tuple,
        TypeVar,
        Union,
        type_t,
    )


@pytest.mark.parametrize(
    "dates",
    [True, False],
)
@pytest.mark.parametrize(
    "positive_only",
    [True, False],
)
@pytest.mark.parametrize(
    "groups",
    [(), ("a", "b")],
)
@pytest.mark.parametrize(
    "seed",
    [None, 42],
)
def test_make_test_data(dates, positive_only, groups, seed):
    sc.make_test_data(
        dates=dates, positive_only=positive_only, groups=groups, seed=seed
    )


def test_accessor_non_Stairs_dtype():
    with pytest.raises(AttributeError):
        pd.Series([1]).sc


def test_accessor_inspection():
    # GH158
    dir(pd.Series([1]))
