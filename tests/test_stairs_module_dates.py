import pytest
import pandas as pd
import numpy as np
from sortedcontainers import SortedSet

from staircase import Stairs
from staircase.core.aggregation import _max_pair, _min_pair
from staircase.core.tools import _get_union_of_points
import staircase as sc


def stairs1():
    int_seq1 = Stairs(0)
    int_seq1.layer(pd.Timestamp(2020, 1, 1), pd.Timestamp(2020, 1, 10), 2)
    int_seq1.layer(pd.Timestamp(2020, 1, 3), pd.Timestamp(2020, 1, 5), 2.5)
    int_seq1.layer(pd.Timestamp(2020, 1, 6), pd.Timestamp(2020, 1, 7), -2.5)
    int_seq1.layer(pd.Timestamp(2020, 1, 7), pd.Timestamp(2020, 1, 10), -2.5)
    return int_seq1


def stairs2():
    int_seq2 = Stairs(0)
    int_seq2.layer(pd.Timestamp(2020, 1, 1), pd.Timestamp(2020, 1, 7), -2.5)
    int_seq2.layer(pd.Timestamp(2020, 1, 8), pd.Timestamp(2020, 1, 10), 5)
    int_seq2.layer(pd.Timestamp(2020, 1, 2), pd.Timestamp(2020, 1, 5), 4.5)
    int_seq2.layer(pd.Timestamp(2020, 1, 2, 12), pd.Timestamp(2020, 1, 4), -2.5)
    return int_seq2


def stairs3(tz):
    int_seq1 = Stairs(0)
    int_seq1.layer(
        pd.Timestamp(2020, 1, 1).tz_localize(tz),
        pd.Timestamp(2020, 1, 10).tz_localize(tz),
        2,
    )
    int_seq1.layer(
        pd.Timestamp(2020, 1, 3).tz_localize(tz),
        pd.Timestamp(2020, 1, 5).tz_localize(tz),
        2.5,
    )
    int_seq1.layer(
        pd.Timestamp(2020, 1, 6).tz_localize(tz),
        pd.Timestamp(2020, 1, 7).tz_localize(tz),
        -2.5,
    )
    int_seq1.layer(
        pd.Timestamp(2020, 1, 7).tz_localize(tz),
        pd.Timestamp(2020, 1, 10).tz_localize(tz),
        -2.5,
    )
    return int_seq1


def stairs4(tz):
    int_seq2 = Stairs(0)
    int_seq2.layer(
        pd.Timestamp(2020, 1, 1).tz_localize(tz),
        pd.Timestamp(2020, 1, 7).tz_localize(tz),
        -2.5,
    )
    int_seq2.layer(
        pd.Timestamp(2020, 1, 8).tz_localize(tz),
        pd.Timestamp(2020, 1, 10).tz_localize(tz),
        5,
    )
    int_seq2.layer(
        pd.Timestamp(2020, 1, 2).tz_localize(tz),
        pd.Timestamp(2020, 1, 5).tz_localize(tz),
        4.5,
    )
    int_seq2.layer(
        pd.Timestamp(2020, 1, 2, 12).tz_localize(tz),
        pd.Timestamp(2020, 1, 4).tz_localize(tz),
        -2.5,
    )
    return int_seq2


@pytest.mark.parametrize(
    "IS1, IS2",
    [
        [stairs1(), stairs2()],
        [stairs3(None), stairs4(None)],
        [stairs3("UTC"), stairs4("UTC")],
        [stairs3("Australia/Sydney"), stairs4("Australia/Sydney")],
    ],
)
def test_min_pair(IS1, IS2):
    assert _min_pair(IS1, IS2).step_changes() == {
        pd.Timestamp("2020-01-01").tz_localize(IS1._keys()[0].tz): -2.5,
        pd.Timestamp("2020-01-02").tz_localize(IS1._keys()[0].tz): 4.5,
        pd.Timestamp("2020-01-02 12:00:00").tz_localize(IS1._keys()[0].tz): -2.5,
        pd.Timestamp("2020-01-04").tz_localize(IS1._keys()[0].tz): 2.5,
        pd.Timestamp("2020-01-05").tz_localize(IS1._keys()[0].tz): -4.5,
        pd.Timestamp("2020-01-07").tz_localize(IS1._keys()[0].tz): 2.0,
        pd.Timestamp("2020-01-10").tz_localize(IS1._keys()[0].tz): 0.5,
    }


@pytest.mark.parametrize(
    "IS1, IS2",
    [
        [stairs1(), stairs2()],
        [stairs3(None), stairs4(None)],
        [stairs3("UTC"), stairs4("UTC")],
        [stairs3("Australia/Sydney"), stairs4("Australia/Sydney")],
    ],
)
def test_max_pair(IS1, IS2):
    assert _max_pair(IS1, IS2).step_changes() == {
        pd.Timestamp("2020-01-01").tz_localize(IS1._keys()[0].tz): 2.0,
        pd.Timestamp("2020-01-03").tz_localize(IS1._keys()[0].tz): 2.5,
        pd.Timestamp("2020-01-05").tz_localize(IS1._keys()[0].tz): -2.5,
        pd.Timestamp("2020-01-06").tz_localize(IS1._keys()[0].tz): -2.5,
        pd.Timestamp("2020-01-07").tz_localize(IS1._keys()[0].tz): 0.5,
        pd.Timestamp("2020-01-08").tz_localize(IS1._keys()[0].tz): 5.0,
        pd.Timestamp("2020-01-10").tz_localize(IS1._keys()[0].tz): -5.0,
    }


@pytest.mark.parametrize(
    "IS1, IS2",
    [
        [stairs1(), stairs2()],
        [stairs3(None), stairs4(None)],
        [stairs3("UTC"), stairs4("UTC")],
        [stairs3("Australia/Sydney"), stairs4("Australia/Sydney")],
    ],
)
def test_get_union_of_points_1(IS1, IS2):
    union = list(_get_union_of_points({1: IS1, 2: IS2}))
    assert union == [
        pd.Timestamp("2020-01-01").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-02").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-02 12:00:00").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-03").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-04").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-05").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-06").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-07").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-08").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-10").tz_localize(IS1._keys()[0].tz),
    ]


@pytest.mark.parametrize(
    "IS1, IS2",
    [
        [stairs1(), stairs2()],
        [stairs3(None), stairs4(None)],
        [stairs3("UTC"), stairs4("UTC")],
        [stairs3("Australia/Sydney"), stairs4("Australia/Sydney")],
    ],
)
def test_get_union_of_points_2(IS1, IS2):
    union = list(_get_union_of_points(pd.Series([IS1, IS2])))
    assert union == [
        pd.Timestamp("2020-01-01").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-02").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-02 12:00:00").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-03").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-04").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-05").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-06").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-07").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-08").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-10").tz_localize(IS1._keys()[0].tz),
    ]


@pytest.mark.parametrize(
    "IS1, IS2",
    [
        [stairs1(), stairs2()],
        [stairs3(None), stairs4(None)],
        [stairs3("UTC"), stairs4("UTC")],
        [stairs3("Australia/Sydney"), stairs4("Australia/Sydney")],
    ],
)
def test_get_union_of_points_3(IS1, IS2):
    union = list(_get_union_of_points(np.array([IS1, IS2])))
    assert union == [
        pd.Timestamp("2020-01-01").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-02").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-02 12:00:00").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-03").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-04").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-05").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-06").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-07").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-08").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-10").tz_localize(IS1._keys()[0].tz),
    ]


@pytest.mark.parametrize(
    "IS1, IS2",
    [
        [stairs1(), stairs2()],
        [stairs3(None), stairs4(None)],
        [stairs3("UTC"), stairs4("UTC")],
        [stairs3("Australia/Sydney"), stairs4("Australia/Sydney")],
    ],
)
def test_get_union_of_points_4(IS1, IS2):
    union = list(_get_union_of_points([IS1, IS2]))
    assert union == [
        pd.Timestamp("2020-01-01").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-02").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-02 12:00:00").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-03").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-04").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-05").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-06").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-07").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-08").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-10").tz_localize(IS1._keys()[0].tz),
    ]


@pytest.mark.parametrize(
    "IS1, IS2",
    [
        [stairs1(), stairs2()],
        [stairs3(None), stairs4(None)],
        [stairs3("UTC"), stairs4("UTC")],
        [stairs3("Australia/Sydney"), stairs4("Australia/Sydney")],
    ],
)
def test_get_union_of_points_5(IS1, IS2):
    union = list(_get_union_of_points((IS1, IS2)))
    assert union == [
        pd.Timestamp("2020-01-01").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-02").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-02 12:00:00").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-03").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-04").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-05").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-06").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-07").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-08").tz_localize(IS1._keys()[0].tz),
        pd.Timestamp("2020-01-10").tz_localize(IS1._keys()[0].tz),
    ]


@pytest.mark.parametrize(
    "IS1, IS2",
    [
        [stairs1(), stairs2()],
        [stairs3(None), stairs4(None)],
        [stairs3("UTC"), stairs4("UTC")],
        [stairs3("Australia/Sydney"), stairs4("Australia/Sydney")],
    ],
)
def test_aggregate_1(IS1, IS2):
    assert sc.aggregate({1: IS1, 2: IS2}, np.mean).step_changes() == {
        pd.Timestamp("2020-01-01").tz_localize(IS1._keys()[0].tz): -0.25,
        pd.Timestamp("2020-01-02").tz_localize(IS1._keys()[0].tz): 2.25,
        pd.Timestamp("2020-01-02 12:00:00").tz_localize(IS1._keys()[0].tz): -1.25,
        pd.Timestamp("2020-01-03").tz_localize(IS1._keys()[0].tz): 1.25,
        pd.Timestamp("2020-01-04").tz_localize(IS1._keys()[0].tz): 1.25,
        pd.Timestamp("2020-01-05").tz_localize(IS1._keys()[0].tz): -3.5,
        pd.Timestamp("2020-01-06").tz_localize(IS1._keys()[0].tz): -1.25,
        pd.Timestamp("2020-01-07").tz_localize(IS1._keys()[0].tz): 1.25,
        pd.Timestamp("2020-01-08").tz_localize(IS1._keys()[0].tz): 2.5,
        pd.Timestamp("2020-01-10").tz_localize(IS1._keys()[0].tz): -2.25,
    }


@pytest.mark.parametrize(
    "IS1, IS2",
    [
        [stairs1(), stairs2()],
        [stairs3(None), stairs4(None)],
        [stairs3("UTC"), stairs4("UTC")],
        [stairs3("Australia/Sydney"), stairs4("Australia/Sydney")],
    ],
)
def test_aggregate_2(IS1, IS2):
    assert sc.aggregate(pd.Series([IS1, IS2]), np.mean).step_changes() == {
        pd.Timestamp("2020-01-01").tz_localize(IS1._keys()[0].tz): -0.25,
        pd.Timestamp("2020-01-02").tz_localize(IS1._keys()[0].tz): 2.25,
        pd.Timestamp("2020-01-02 12:00:00").tz_localize(IS1._keys()[0].tz): -1.25,
        pd.Timestamp("2020-01-03").tz_localize(IS1._keys()[0].tz): 1.25,
        pd.Timestamp("2020-01-04").tz_localize(IS1._keys()[0].tz): 1.25,
        pd.Timestamp("2020-01-05").tz_localize(IS1._keys()[0].tz): -3.5,
        pd.Timestamp("2020-01-06").tz_localize(IS1._keys()[0].tz): -1.25,
        pd.Timestamp("2020-01-07").tz_localize(IS1._keys()[0].tz): 1.25,
        pd.Timestamp("2020-01-08").tz_localize(IS1._keys()[0].tz): 2.5,
        pd.Timestamp("2020-01-10").tz_localize(IS1._keys()[0].tz): -2.25,
    }


@pytest.mark.parametrize(
    "IS1, IS2",
    [
        [stairs1(), stairs2()],
        [stairs3(None), stairs4(None)],
        [stairs3("UTC"), stairs4("UTC")],
        [stairs3("Australia/Sydney"), stairs4("Australia/Sydney")],
    ],
)
def test_aggregate_3(IS1, IS2):
    assert sc.aggregate(np.array([IS1, IS2]), np.mean).step_changes() == {
        pd.Timestamp("2020-01-01").tz_localize(IS1._keys()[0].tz): -0.25,
        pd.Timestamp("2020-01-02").tz_localize(IS1._keys()[0].tz): 2.25,
        pd.Timestamp("2020-01-02 12:00:00").tz_localize(IS1._keys()[0].tz): -1.25,
        pd.Timestamp("2020-01-03").tz_localize(IS1._keys()[0].tz): 1.25,
        pd.Timestamp("2020-01-04").tz_localize(IS1._keys()[0].tz): 1.25,
        pd.Timestamp("2020-01-05").tz_localize(IS1._keys()[0].tz): -3.5,
        pd.Timestamp("2020-01-06").tz_localize(IS1._keys()[0].tz): -1.25,
        pd.Timestamp("2020-01-07").tz_localize(IS1._keys()[0].tz): 1.25,
        pd.Timestamp("2020-01-08").tz_localize(IS1._keys()[0].tz): 2.5,
        pd.Timestamp("2020-01-10").tz_localize(IS1._keys()[0].tz): -2.25,
    }


@pytest.mark.parametrize(
    "IS1, IS2",
    [
        [stairs1(), stairs2()],
        [stairs3(None), stairs4(None)],
        [stairs3("UTC"), stairs4("UTC")],
        [stairs3("Australia/Sydney"), stairs4("Australia/Sydney")],
    ],
)
def test_aggregate_4(IS1, IS2):
    assert sc.aggregate([IS1, IS2], np.mean).step_changes() == {
        pd.Timestamp("2020-01-01").tz_localize(IS1._keys()[0].tz): -0.25,
        pd.Timestamp("2020-01-02").tz_localize(IS1._keys()[0].tz): 2.25,
        pd.Timestamp("2020-01-02 12:00:00").tz_localize(IS1._keys()[0].tz): -1.25,
        pd.Timestamp("2020-01-03").tz_localize(IS1._keys()[0].tz): 1.25,
        pd.Timestamp("2020-01-04").tz_localize(IS1._keys()[0].tz): 1.25,
        pd.Timestamp("2020-01-05").tz_localize(IS1._keys()[0].tz): -3.5,
        pd.Timestamp("2020-01-06").tz_localize(IS1._keys()[0].tz): -1.25,
        pd.Timestamp("2020-01-07").tz_localize(IS1._keys()[0].tz): 1.25,
        pd.Timestamp("2020-01-08").tz_localize(IS1._keys()[0].tz): 2.5,
        pd.Timestamp("2020-01-10").tz_localize(IS1._keys()[0].tz): -2.25,
    }


@pytest.mark.parametrize(
    "IS1, IS2",
    [
        [stairs1(), stairs2()],
        [stairs3(None), stairs4(None)],
        [stairs3("UTC"), stairs4("UTC")],
        [stairs3("Australia/Sydney"), stairs4("Australia/Sydney")],
    ],
)
def test_aggregate_5(IS1, IS2):
    assert sc.aggregate((IS1, IS2), np.mean).step_changes() == {
        pd.Timestamp("2020-01-01").tz_localize(IS1._keys()[0].tz): -0.25,
        pd.Timestamp("2020-01-02").tz_localize(IS1._keys()[0].tz): 2.25,
        pd.Timestamp("2020-01-02 12:00:00").tz_localize(IS1._keys()[0].tz): -1.25,
        pd.Timestamp("2020-01-03").tz_localize(IS1._keys()[0].tz): 1.25,
        pd.Timestamp("2020-01-04").tz_localize(IS1._keys()[0].tz): 1.25,
        pd.Timestamp("2020-01-05").tz_localize(IS1._keys()[0].tz): -3.5,
        pd.Timestamp("2020-01-06").tz_localize(IS1._keys()[0].tz): -1.25,
        pd.Timestamp("2020-01-07").tz_localize(IS1._keys()[0].tz): 1.25,
        pd.Timestamp("2020-01-08").tz_localize(IS1._keys()[0].tz): 2.5,
        pd.Timestamp("2020-01-10").tz_localize(IS1._keys()[0].tz): -2.25,
    }


@pytest.mark.parametrize(
    "IS1, IS2",
    [
        [stairs1(), stairs2()],
        [stairs3(None), stairs4(None)],
        [stairs3("UTC"), stairs4("UTC")],
        [stairs3("Australia/Sydney"), stairs4("Australia/Sydney")],
    ],
)
def test_aggregate_6(IS1, IS2):
    assert sc.aggregate(
        {1: IS1, 2: IS2},
        np.mean,
        [
            pd.Timestamp(2020, 1, 3).tz_localize(IS1._keys()[0].tz),
            pd.Timestamp(2020, 1, 5).tz_localize(IS1._keys()[0].tz),
            pd.Timestamp(2020, 1, 7).tz_localize(IS1._keys()[0].tz),
            pd.Timestamp(2020, 1, 9).tz_localize(IS1._keys()[0].tz),
        ],
    ).step_changes() == {
        pd.Timestamp("2020-01-03").tz_localize(IS1._keys()[0].tz): 2.0,
        pd.Timestamp("2020-01-05").tz_localize(IS1._keys()[0].tz): -2.25,
        pd.Timestamp("2020-01-09").tz_localize(IS1._keys()[0].tz): 2.5,
    }


@pytest.mark.parametrize(
    "IS1, IS2",
    [
        [stairs1(), stairs2()],
        [stairs3(None), stairs4(None)],
        [stairs3("UTC"), stairs4("UTC")],
        [stairs3("Australia/Sydney"), stairs4("Australia/Sydney")],
    ],
)
def test_aggregate_7(IS1, IS2):
    assert sc.aggregate(
        pd.Series([IS1, IS2]),
        np.mean,
        [
            pd.Timestamp(2020, 1, 3).tz_localize(IS1._keys()[0].tz),
            pd.Timestamp(2020, 1, 5).tz_localize(IS1._keys()[0].tz),
            pd.Timestamp(2020, 1, 7).tz_localize(IS1._keys()[0].tz),
            pd.Timestamp(2020, 1, 9).tz_localize(IS1._keys()[0].tz),
        ],
    ).step_changes() == {
        pd.Timestamp("2020-01-03").tz_localize(IS1._keys()[0].tz): 2.0,
        pd.Timestamp("2020-01-05").tz_localize(IS1._keys()[0].tz): -2.25,
        pd.Timestamp("2020-01-09").tz_localize(IS1._keys()[0].tz): 2.5,
    }


@pytest.mark.parametrize(
    "IS1, IS2",
    [
        [stairs1(), stairs2()],
        [stairs3(None), stairs4(None)],
        [stairs3("UTC"), stairs4("UTC")],
        [stairs3("Australia/Sydney"), stairs4("Australia/Sydney")],
    ],
)
def test_aggregate_8(IS1, IS2):
    assert sc.aggregate(
        np.array([IS1, IS2]),
        np.mean,
        [
            pd.Timestamp(2020, 1, 3).tz_localize(IS1._keys()[0].tz),
            pd.Timestamp(2020, 1, 5).tz_localize(IS1._keys()[0].tz),
            pd.Timestamp(2020, 1, 7).tz_localize(IS1._keys()[0].tz),
            pd.Timestamp(2020, 1, 9).tz_localize(IS1._keys()[0].tz),
        ],
    ).step_changes() == {
        pd.Timestamp("2020-01-03").tz_localize(IS1._keys()[0].tz): 2.0,
        pd.Timestamp("2020-01-05").tz_localize(IS1._keys()[0].tz): -2.25,
        pd.Timestamp("2020-01-09").tz_localize(IS1._keys()[0].tz): 2.5,
    }


@pytest.mark.parametrize(
    "IS1, IS2",
    [
        [stairs1(), stairs2()],
        [stairs3(None), stairs4(None)],
        [stairs3("UTC"), stairs4("UTC")],
        [stairs3("Australia/Sydney"), stairs4("Australia/Sydney")],
    ],
)
def test_aggregate_9(IS1, IS2):
    assert sc.aggregate(
        [IS1, IS2],
        np.mean,
        [
            pd.Timestamp(2020, 1, 3).tz_localize(IS1._keys()[0].tz),
            pd.Timestamp(2020, 1, 5).tz_localize(IS1._keys()[0].tz),
            pd.Timestamp(2020, 1, 7).tz_localize(IS1._keys()[0].tz),
            pd.Timestamp(2020, 1, 9).tz_localize(IS1._keys()[0].tz),
        ],
    ).step_changes() == {
        pd.Timestamp("2020-01-03").tz_localize(IS1._keys()[0].tz): 2.0,
        pd.Timestamp("2020-01-05").tz_localize(IS1._keys()[0].tz): -2.25,
        pd.Timestamp("2020-01-09").tz_localize(IS1._keys()[0].tz): 2.5,
    }


@pytest.mark.parametrize(
    "IS1, IS2",
    [
        [stairs1(), stairs2()],
        [stairs3(None), stairs4(None)],
        [stairs3("UTC"), stairs4("UTC")],
        [stairs3("Australia/Sydney"), stairs4("Australia/Sydney")],
    ],
)
def test_aggregate_10(IS1, IS2):
    assert sc.aggregate(
        (IS1, IS2),
        np.mean,
        [
            pd.Timestamp(2020, 1, 3).tz_localize(IS1._keys()[0].tz),
            pd.Timestamp(2020, 1, 5).tz_localize(IS1._keys()[0].tz),
            pd.Timestamp(2020, 1, 7).tz_localize(IS1._keys()[0].tz),
            pd.Timestamp(2020, 1, 9).tz_localize(IS1._keys()[0].tz),
        ],
    ).step_changes() == {
        pd.Timestamp("2020-01-03").tz_localize(IS1._keys()[0].tz): 2.0,
        pd.Timestamp("2020-01-05").tz_localize(IS1._keys()[0].tz): -2.25,
        pd.Timestamp("2020-01-09").tz_localize(IS1._keys()[0].tz): 2.5,
    }


def _matrix_close_to_zeros(x):
    return all(map(lambda v: np.isclose(v, 0, atol=0.0001), x.flatten()))


# low, high = pd.Timestamp(2019,12,30), pd.Timestamp(2020,1,8,16)
# total_secs = int((high-low).total_seconds())
# pts = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs, total_secs)]
# np.cov(st1(pts), st2(pts))
# = array([[3.50119325, 0.05618318],
#          [0.05618318, 4.28396767]])


def test_cov_matrix1():
    assert _matrix_close_to_zeros(
        sc.cov(
            [stairs1(), stairs2()],
            pd.Timestamp(2019, 12, 30),
            pd.Timestamp(2020, 1, 8, 16),
        ).values
        - np.array([[3.50119325, 0.05618318], [0.05618318, 4.28396767]])
    )


def test_cov_matrix2():
    assert _matrix_close_to_zeros(
        sc.cov(
            [stairs1(), stairs2()],
            pd.Timestamp(2020, 1, 2),
            pd.Timestamp(2020, 1, 11, 3),
        ).values
        - np.array([[3.97147733, -1.01257284], [-1.01257284, 6.91668318]])
    )


def test_corr_matrix1():
    assert _matrix_close_to_zeros(
        sc.corr(
            [stairs1(), stairs2()],
            pd.Timestamp(2019, 12, 30),
            pd.Timestamp(2020, 1, 8, 16),
        ).values
        - np.array([[1, 0.01450692], [0.01450692, 1]])
    )


def test_corr_matrix2():
    assert _matrix_close_to_zeros(
        sc.corr(
            [stairs1(), stairs2()],
            pd.Timestamp(2020, 1, 2),
            pd.Timestamp(2020, 1, 11, 3),
        ).values
        - np.array([[1, -0.19319741], [-0.19319741, 1]])
    )