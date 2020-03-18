import pytest
import pandas as pd
import numpy as np
import staircase.stairs as stairs
from sortedcontainers import SortedSet

@pytest.fixture
def IS1():
    int_seq1 = stairs.Stairs(0)
    int_seq1.layer(1,10,2)
    int_seq1.layer(-4,5,-1.75)
    int_seq1.layer(3,5,2.5)
    int_seq1.layer(6,7,-2.5)
    int_seq1.layer(7,10,-2.5)
    return int_seq1

@pytest.fixture
def IS2():    
    int_seq2 = stairs.Stairs(0)
    int_seq2.layer(1,7,-2.5)
    int_seq2.layer(8,10,5)
    int_seq2.layer(2,5,4.5)
    int_seq2.layer(2.5,4,-2.5)
    int_seq2.layer(-2,1,-1.75)
    return int_seq2

def test_min_pair(IS1, IS2):
    assert stairs._min_pair(IS1,IS2).step_changes() == {-4: -1.75, 1: -0.75, 2: 2.75, 2.5: -0.75, 4: 2.5, 5: -4.5, 7: 2.0, 10: 0.5}
    
def test_max_pair(IS1, IS2):
    assert stairs._max_pair(IS1,IS2).step_changes() == {-2: -1.75, 1: 2.0, 2: 1.75, 2.5: -1.75, 3: 2.5, 5: -0.75, 6: -2.5, 7: 0.5, 8: 5.0, 10: -5.0}
    
def test_get_union_of_points_1(IS1, IS2):
    stairs._get_union_of_points({1:IS2, 2:IS2}) == SortedSet([float('-inf'), -4, -2, 1, 2, 2.5, 3, 4, 5, 6, 7, 8, 10])
    
def test_get_union_of_points_2(IS1, IS2):
    stairs._get_union_of_points(pd.Series([IS1, IS2])) == SortedSet([float('-inf'), -4, -2, 1, 2, 2.5, 3, 4, 5, 6, 7, 8, 10])
    
def test_get_union_of_points_3(IS1, IS2):
    stairs._get_union_of_points(np.array([IS1, IS2])) == SortedSet([float('-inf'), -4, -2, 1, 2, 2.5, 3, 4, 5, 6, 7, 8, 10])

def test_get_union_of_points_4(IS1, IS2):
    stairs._get_union_of_points([IS1, IS2]) == SortedSet([float('-inf'), -4, -2, 1, 2, 2.5, 3, 4, 5, 6, 7, 8, 10])

def test_get_union_of_points_5(IS1, IS2):
    stairs._get_union_of_points((IS1, IS2)) == SortedSet([float('-inf'), -4, -2, 1, 2, 2.5, 3, 4, 5, 6, 7, 8, 10])

def test_using_dates_1(IS1, IS2):
    assert not stairs._using_dates({1:IS1, 2:IS2})
    
def test_using_dates_2(IS1, IS2):
    assert not stairs._using_dates(pd.Series([IS1, IS2]))

def test_using_dates_3(IS1, IS2):
    assert not stairs._using_dates(np.array([IS1, IS2]))

def test_using_dates_4(IS1, IS2):
    assert not stairs._using_dates([IS1, IS2])

def test_using_dates_5(IS1, IS2):
    assert not stairs._using_dates((IS1, IS2))
    
def test_aggregate_1(IS1, IS2):
    assert stairs.aggregate({1:IS1, 2:IS2}, np.mean).step_changes() == {-4.0: -0.875,
                                                                -2.0: -0.875,
                                                                1.0: 0.625,
                                                                2.0: 2.25,
                                                                2.5: -1.25,
                                                                3.0: 1.25,
                                                                4.0: 1.25,
                                                                5.0: -2.625,
                                                                6.0: -1.25,
                                                                7.0: 1.25,
                                                                8.0: 2.5,
                                                                10.0: -2.25}
                                                                     
def test_aggregate_2(IS1, IS2):
    assert stairs.aggregate(pd.Series([IS1, IS2]), np.mean).step_changes() == {-4.0: -0.875,
                                                                                -2.0: -0.875,
                                                                                1.0: 0.625,
                                                                                2.0: 2.25,
                                                                                2.5: -1.25,
                                                                                3.0: 1.25,
                                                                                4.0: 1.25,
                                                                                5.0: -2.625,
                                                                                6.0: -1.25,
                                                                                7.0: 1.25,
                                                                                8.0: 2.5,
                                                                                10.0: -2.25}

def test_aggregate_3(IS1, IS2):
    assert stairs.aggregate(np.array([IS1, IS2]), np.mean).step_changes() == {-4.0: -0.875,
                                                                                -2.0: -0.875,
                                                                                1.0: 0.625,
                                                                                2.0: 2.25,
                                                                                2.5: -1.25,
                                                                                3.0: 1.25,
                                                                                4.0: 1.25,
                                                                                5.0: -2.625,
                                                                                6.0: -1.25,
                                                                                7.0: 1.25,
                                                                                8.0: 2.5,
                                                                                10.0: -2.25}

def test_aggregate_4(IS1, IS2):
    assert stairs.aggregate([IS1, IS2], np.mean).step_changes() == {-4.0: -0.875,
                                                                    -2.0: -0.875,
                                                                    1.0: 0.625,
                                                                    2.0: 2.25,
                                                                    2.5: -1.25,
                                                                    3.0: 1.25,
                                                                    4.0: 1.25,
                                                                    5.0: -2.625,
                                                                    6.0: -1.25,
                                                                    7.0: 1.25,
                                                                    8.0: 2.5,
                                                                    10.0: -2.25}

def test_aggregate_5(IS1, IS2):
    assert stairs.aggregate((IS1, IS2), np.mean).step_changes() == {-4.0: -0.875,
                                                                    -2.0: -0.875,
                                                                    1.0: 0.625,
                                                                    2.0: 2.25,
                                                                    2.5: -1.25,
                                                                    3.0: 1.25,
                                                                    4.0: 1.25,
                                                                    5.0: -2.625,
                                                                    6.0: -1.25,
                                                                    7.0: 1.25,
                                                                    8.0: 2.5,
                                                                    10.0: -2.25}   
                                                                    
def test_aggregate_6(IS1, IS2):
    assert stairs.aggregate({1:IS1, 2:IS2}, np.mean, points=[-2,2,5,8]).step_changes() == {-2.0: -1.75, 2.0: 2.875, 5.0: -1.375, 8.0: 2.5}
                                                                     
def test_aggregate_7(IS1, IS2):
    assert stairs.aggregate(pd.Series([IS1, IS2]), np.mean, points=[-2,2,5,8]).step_changes() == {-2.0: -1.75, 2.0: 2.875, 5.0: -1.375, 8.0: 2.5}

def test_aggregate_8(IS1, IS2):
    assert stairs.aggregate(np.array([IS1, IS2]), np.mean, points=[-2,2,5,8]).step_changes() == {-2.0: -1.75, 2.0: 2.875, 5.0: -1.375, 8.0: 2.5}

def test_aggregate_9(IS1, IS2):
    assert stairs.aggregate([IS1, IS2], np.mean, points=[-2,2,5,8]).step_changes() == {-2.0: -1.75, 2.0: 2.875, 5.0: -1.375, 8.0: 2.5}

def test_aggregate_10(IS1, IS2):
    assert stairs.aggregate((IS1, IS2), np.mean, points=[-2,2,5,8]).step_changes() == {-2.0: -1.75, 2.0: 2.875, 5.0: -1.375, 8.0: 2.5}

def test_sample_1(IS1, IS2):
    sample = stairs.sample(pd.Series([IS1, IS2]))
    points=[float('-inf'), -4.0, -2.0, 1.0, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 10.0, float('-inf'), -4.0, -2.0, 1.0, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 10.0]
    key=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    value=[0.0, -1.75, -1.75, 0.25, 0.25, 0.25, 2.75, 2.75, 2.0, -0.5, -0.5, -0.5, 0.0, 0.0, 0.0, -1.75, -2.5, 2.0, -0.5, -0.5, 2.0, -2.5, -2.5, 0.0, 5.0, 0.0]
    assert sample.eq(pd.DataFrame({"points":points, "key":key, "value":value})).all(axis=None)
    
def test_sample_2(IS1, IS2):
    sample = stairs.sample({0:IS1, 1:IS2})
    points=[float('-inf'), -4.0, -2.0, 1.0, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 10.0, float('-inf'), -4.0, -2.0, 1.0, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 10.0]
    key=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    value=[0.0, -1.75, -1.75, 0.25, 0.25, 0.25, 2.75, 2.75, 2.0, -0.5, -0.5, -0.5, 0.0, 0.0, 0.0, -1.75, -2.5, 2.0, -0.5, -0.5, 2.0, -2.5, -2.5, 0.0, 5.0, 0.0]
    assert sample.eq(pd.DataFrame({"points":points, "key":key, "value":value})).all(axis=None)
    
def test_sample_3(IS1, IS2):
    sample = stairs.sample(pd.Series([IS1, IS2]), how='left')    
    points=[float('-inf'), -4.0, -2.0, 1.0, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 10.0, float('-inf'), -4.0, -2.0, 1.0, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 10.0]
    key=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    value=[0.0, 0.0, -1.75, -1.75, 0.25, 0.25, 0.25, 2.75, 2.75, 2.0, -0.5, -0.5, -0.5, 0.0, 0.0, 0.0, -1.75, -2.5, 2.0, -0.5, -0.5, 2.0, -2.5, -2.5, 0.0, 5.0]
    assert sample.eq(pd.DataFrame({"points":points, "key":key, "value":value})).all(axis=None)
    
def test_sample_4(IS1, IS2):
    sample = stairs.sample({0:IS1, 1:IS2}, how='left')    
    points=[float('-inf'), -4.0, -2.0, 1.0, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 10.0, float('-inf'), -4.0, -2.0, 1.0, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 10.0]
    key=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    value=[0.0, 0.0, -1.75, -1.75, 0.25, 0.25, 0.25, 2.75, 2.75, 2.0, -0.5, -0.5, -0.5, 0.0, 0.0, 0.0, -1.75, -2.5, 2.0, -0.5, -0.5, 2.0, -2.5, -2.5, 0.0, 5.0]
    assert sample.eq(pd.DataFrame({"points":points, "key":key, "value":value})).all(axis=None)