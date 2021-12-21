import operator

import pandas as pd
import pytest

import staircase as sc


@pytest.fixture
def dtype():
    """A fixture providing the ExtensionDtype to validate."""
    return sc.core.arrays.extension.StairsDtype()


@pytest.fixture
def data():
    """
    Length-100 array for this type.
    * data[0] and data[1] should both be non missing
    * data[0] and data[1] should not be equal
    """
    return sc.StairsArray([sc.Stairs().layer(0, i + 1) for i in range(100)])


@pytest.fixture
def data_for_twos():
    """Length-100 array in which all the elements are two."""
    raise NotImplementedError


@pytest.fixture
def data_missing():
    """Length-2 array with [NA, Valid]"""
    return sc.StairsArray([None, sc.Stairs()])


@pytest.fixture(params=["data", "data_missing"])
def all_data(request, data, data_missing):
    """Parametrized fixture giving 'data' and 'data_missing'"""
    if request.param == "data":
        return data
    elif request.param == "data_missing":
        return data_missing


@pytest.fixture
def data_repeated(data):
    """
    Generate many datasets.
    Parameters
    ----------
    data : fixture implementing `data`
    Returns
    -------
    Callable[[int], Generator]:
        A callable that takes a `count` argument and
        returns a generator yielding `count` datasets.
    """

    def gen(count):
        for _ in range(count):
            yield data

    return gen


@pytest.fixture
def data_for_sorting():
    """
    Length-3 array with a known sort order.
    This should be three items [B, C, A] with
    A < B < C
    """
    raise NotImplementedError


@pytest.fixture
def data_missing_for_sorting():
    """
    Length-3 array with a known sort order.
    This should be three items [B, NA, A] with
    A < B and NA missing.
    """
    raise NotImplementedError


@pytest.fixture
def na_cmp():
    """
    Binary operator for comparing NA values.
    Should return a function of two arguments that returns
    True if both arguments are (scalar) NA for your type.
    By default, uses ``operator.is_``
    """
    return lambda x, y: x is None and y is None


@pytest.fixture
def na_value():
    """The scalar missing value for this type. Default 'None'"""
    return pd.NA


@pytest.fixture
def data_for_grouping():
    """
    Data for factorization, grouping, and unique tests.
    Expected to be like [B, B, NA, NA, A, A, B, C]
    Where A < B < C and NA is missing
    """
    return sc.StairsArray(
        [
            sc.Stairs().layer(1, 3),
            sc.Stairs().layer(1, 3),
            None,
            None,
            sc.Stairs().layer(2, 4),
            sc.Stairs().layer(2, 4),
            sc.Stairs().layer(1, 3),
            sc.Stairs().layer(1, 4),
        ]
    )


@pytest.fixture(params=[True, False])
def box_in_series(request):
    """Whether to box the data in a Series"""
    return request.param


@pytest.fixture(
    params=[
        lambda x: 1,
        lambda x: [1] * len(x),
        lambda x: pd.Series([1] * len(x)),
        lambda x: x,
    ],
    ids=["scalar", "list", "series", "object"],
)
def groupby_apply_op(request):
    """
    Functions to test groupby.apply().
    """
    return request.param


@pytest.fixture(params=[True, False])
def as_frame(request):
    """
    Boolean fixture to support Series and Series.to_frame() comparison testing.
    """
    return request.param


@pytest.fixture(params=[True, False])
def as_series(request):
    """
    Boolean fixture to support arr and Series(arr) comparison testing.
    """
    return request.param


@pytest.fixture(params=[True, False])
def use_numpy(request):
    """
    Boolean fixture to support comparison testing of ExtensionDtype array
    and numpy array.
    """
    return request.param


@pytest.fixture(params=["ffill", "bfill"])
def fillna_method(request):
    """
    Parametrized fixture giving method parameters 'ffill' and 'bfill' for
    Series.fillna(method=<method>) testing.
    """
    return request.param


@pytest.fixture(params=[True, False])
def as_array(request):
    """
    Boolean fixture to support ExtensionDtype _from_sequence method testing.
    """
    return request.param


@pytest.fixture
def invalid_scalar(data):
    """
    A scalar that *cannot* be held by this ExtensionArray.
    The default should work for most subclasses, but is not guaranteed.
    If the array can hold any item (i.e. object dtype), then use pytest.skip.
    """
    return object.__new__(object)


from pandas.tests.extension import base


class TestConstructors(base.BaseConstructorsTests):
    def test_construct_empty_dataframe(self, dtype):
        pass  # empty DataFrame construction only seems to work on pandas 1.4


# ------------------------


def s1(closed="left"):
    int_seq1 = sc.Stairs(initial_value=0, closed=closed)
    int_seq1.layer(1, 10, 2)
    int_seq1.layer(-4, 5, -1.75)
    int_seq1.layer(3, 5, 2.5)
    int_seq1.layer(6, 7, -2.5)
    int_seq1.layer(7, 10, -2.5)
    return int_seq1


def s2(closed="left"):
    int_seq2 = sc.Stairs(initial_value=0, closed=closed)
    int_seq2.layer(1, 7, -2.5)
    int_seq2.layer(8, 10, 5)
    int_seq2.layer(2, 5, 4.5)
    int_seq2.layer(2.5, 4, -2.5)
    int_seq2.layer(-2, 1, -1.75)
    return int_seq2


def s3(closed="left"):  # boolean
    int_seq = sc.Stairs(initial_value=0, closed=closed)
    int_seq.layer(-10, 10, 1)
    int_seq.layer(-8, -7, -1)
    int_seq.layer(-5, -2, -1)
    int_seq.layer(0.5, 1, -1)
    int_seq.layer(3, 3.5, -1)
    int_seq.layer(7, 9.5, -1)
    return int_seq


def s4(closed="left"):  # boolean
    int_seq = sc.Stairs(initial_value=0, closed=closed)
    int_seq.layer(-11, 9, 1)
    int_seq.layer(-9.5, -8, -1)
    int_seq.layer(-7.5, -7, -1)
    int_seq.layer(0, 3, -1)
    int_seq.layer(6, 6.5, -1)
    int_seq.layer(7, 8.5, -1)
    return int_seq


@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
@pytest.mark.parametrize(
    "operand",
    ["scalar", "Stairs", "array"],
)
@pytest.mark.parametrize(
    "array_type",
    ["StairsArray", "Series"],
)
@pytest.mark.parametrize(
    "func",
    [
        operator.gt,
        operator.ge,
        operator.lt,
        operator.le,
        operator.eq,
        operator.ne,
        operator.add,
        operator.sub,
        operator.mul,
        operator.truediv,
    ],
)
def test_binop(closed, operand, array_type, func):
    arr = sc.StairsArray([s1(closed), s2(closed)])
    other = {
        "scalar": 2.5,
        "Stairs": s3(closed),
        "array": sc.StairsArray([s3(closed), s4(closed)]),
    }[operand]
    if operand == "array":
        expected = sc.StairsArray(
            [func(s1(closed), s3(closed)), func(s2(closed), s4(closed))]
        )
    else:
        expected = sc.StairsArray([func(s1(closed), other), func(s2(closed), other)])
    if array_type == "Series":
        arr = pd.Series(arr)
        if operand == "array":
            other = pd.Series(other)
        expected = pd.Series(expected)
    result = func(arr, other)
    assert type(result) == type(expected)
    if array_type == "Series":
        assert str(result.dtype) == "Stairs"
    assert all([a.identical(b) for a, b in zip(result, expected)])
    assert all([a.closed == closed for a in result])
