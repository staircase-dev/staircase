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
    stairs._get_union_of_points({1:IS1, 2:IS2}) == SortedSet([float('-inf'), -4, -2, 1, 2, 2.5, 3, 4, 5, 6, 7, 8, 10])
    
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
    
def test_mean_1(IS1, IS2):
    assert stairs._mean({1:IS1, 2:IS2}).step_changes() == {-4.0: -0.875,
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
                                                                     
def test_mean_2(IS1, IS2):
    assert stairs._mean(pd.Series([IS1, IS2])).step_changes() == {-4.0: -0.875,
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

def test_mean_3(IS1, IS2):
    assert stairs._mean(np.array([IS1, IS2])).step_changes() == {-4.0: -0.875,
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

def test_mean_4(IS1, IS2):
    assert stairs._mean([IS1, IS2]).step_changes() == {-4.0: -0.875,
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

def test_mean_5(IS1, IS2):
    assert stairs._mean((IS1, IS2)).step_changes() == {-4.0: -0.875,
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
                                                                    
def test_median_1(IS1, IS2):
    assert stairs._median({1:IS1, 2:IS2, 3:IS1+IS2}).step_changes() == {
        -4.0: -1.75,
        1.0: -0.5,
        2.0: 4.25,
        2.5: -2.25,
        3.0: 2.5,
        4.0: 0.5,
        5.0: -3.25,
        6.0: -2.0,
        7.0: 2.0,
        8.0: 5.0,
        10.0: -4.5,
    }                                                                 
                                                                   
def test_max_1(IS1, IS2):
    assert stairs._max({1:IS1, 2:IS2}).step_changes() == {
        -2.0: -1.75,
         1.0: 2.0,
         2.0: 1.75,
         2.5: -1.75,
         3.0: 2.5,
         5.0: -0.75,
         6.0: -2.5,
         7.0: 0.5,
         8.0: 5.0,
         10.0: -5.0,
    }   
    
def test_min_1(IS1, IS2):
    assert stairs._min({1:IS1, 2:IS2}).step_changes() == {
        -4.0: -1.75,
         1.0: -0.75,
         2.0: 2.75,
         2.5: -0.75,
         4.0: 2.5,
         5.0: -4.5,
         7.0: 2.0,
         10.0: 0.5,
    }   

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
    
def test_sample_5(IS1, IS2):
    sample = stairs.sample(pd.Series([IS1, IS2]), 3)
    points = [3, 3]
    key = [0, 1]
    value = [2.75, -0.5]
    assert sample.eq(pd.DataFrame({"points":points, "key":key, "value":value})).all(axis=None)
    
def test_sample_6(IS1, IS2):
    sample = stairs.sample({0:IS1, 1:IS2}, 3)
    points = [3, 3]
    key = [0, 1]
    value = [2.75, -0.5]
    assert sample.eq(pd.DataFrame({"points":points, "key":key, "value":value})).all(axis=None)
    
def test_sample_7(IS1, IS2):
    sample = stairs.sample(pd.Series([IS1, IS2]), 3, how='left')    
    points = [3, 3]
    key = [0, 1]
    value = [0.25, -0.5]
    assert sample.eq(pd.DataFrame({"points":points, "key":key, "value":value})).all(axis=None)
    
def test_sample_8(IS1, IS2):
    sample = stairs.sample({0:IS1, 1:IS2}, 3, how='left')    
    points = [3, 3]
    key = [0, 1]
    value = [0.25, -0.5]
    assert sample.eq(pd.DataFrame({"points":points, "key":key, "value":value})).all(axis=None)
    
def test_sample_9(IS1, IS2):
    sample = stairs.sample(pd.Series([IS1, IS2]), [3, 6, 8])
    points = [3, 6, 8, 3, 6, 8]
    key = [0, 0, 0, 1, 1, 1]
    value = [2.75, -0.5, -0.5, -0.5, -2.5, 5.0]
    assert sample.eq(pd.DataFrame({"points":points, "key":key, "value":value})).all(axis=None)
    
def test_sample_10(IS1, IS2):
    sample = stairs.sample({0:IS1, 1:IS2}, [3, 6, 8])
    points = [3, 6, 8, 3, 6, 8]
    key = [0, 0, 0, 1, 1, 1]
    value = [2.75, -0.5, -0.5, -0.5, -2.5, 5.0]
    assert sample.eq(pd.DataFrame({"points":points, "key":key, "value":value})).all(axis=None)
    
def test_sample_11(IS1, IS2):
    sample = stairs.sample(pd.Series([IS1, IS2]), [3, 6, 8], how='left')    
    points = [3, 6, 8, 3, 6, 8]
    key = [0, 0, 0, 1, 1, 1]
    value = [0.25, 2.0, -0.5, -0.5, -2.5, 0.0]
    assert sample.eq(pd.DataFrame({"points":points, "key":key, "value":value})).all(axis=None)
    
def test_sample_12(IS1, IS2):
    sample = stairs.sample({0:IS1, 1:IS2}, [3, 6, 8], how='left')    
    points = [3, 6, 8, 3, 6, 8]
    key = [0, 0, 0, 1, 1, 1]
    value = [0.25, 2.0, -0.5, -0.5, -2.5, 0.0]
    assert sample.eq(pd.DataFrame({"points":points, "key":key, "value":value})).all(axis=None)
    
 
def _matrix_close_to_zeros(x):
    return all(map(lambda v: np.isclose(v, 0, atol = 0.00001), x.flatten()))
    
# np.cov(st1(np.linspace(-4,10,10000000)), st2(np.linspace(-4,10,10000000))) = array([[2.50159449, 0.28762709], [0.28762709, 6.02104508]])
def test_cov_matrix1(IS1, IS2):
    assert _matrix_close_to_zeros(stairs.cov([IS1, IS2], -4, 10).values - np.array([[2.50159449, 0.28762709], [0.28762709, 6.02104508]]))
    
# np.cov(st1(np.linspace(0,12,10000000)), st2(np.linspace(0,12,10000000))) = array([[ 1.81727486, -0.25520783],[-0.25520783,  6.45312616]])
def test_cov_matrix2(IS1, IS2):    
    assert _matrix_close_to_zeros(stairs.cov([IS1, IS2], 0, 12).values - np.array([[ 1.81727486, -0.25520783],[-0.25520783,  6.45312616]]))
    
# np.corrcoef(st1(np.linspace(-4,10,10000000)), st2(np.linspace(-4,10,10000000))) = array([[1, 0.07411146], [0.07411146, 1]])
def test_corr_matrix1(IS1, IS2):
    assert _matrix_close_to_zeros(stairs.corr([IS1, IS2], -4, 10).values - np.array([[1, 0.07411146], [0.07411146, 1]]))
  
# np.corrcoef(st1(np.linspace(0,12,10000000)), st2(np.linspace(0,12,10000000))) = array([[1, -0.07452442], [-0.07452442,  1]])
def test_corr_matrix2(IS1, IS2):    
    assert _matrix_close_to_zeros(stairs.corr([IS1, IS2],0, 12).values - np.array([[1, -0.07452442], [-0.07452442,  1]]))    
    

def test_convert_date_to_float():
    assert stairs._convert_date_to_float(None) is None
    
    
def test_convert_float_to_date():
    assert stairs._convert_float_to_date(1) == stairs.origin + pd.Timedelta(1, 'h')
    
    
def test_get_union_of_points_exception():
    with pytest.raises(TypeError):
        assert stairs._get_union_of_points(None)
        
def test_using_dates_exception():
    with pytest.raises(TypeError):
        assert stairs._using_dates(None)
        
def test_sample_series_expand_key(IS1, IS2):
    s = pd.Series(
        [IS1, IS2],
        index = pd.MultiIndex.from_product([("A",), ("X","Y")], names=['first', 'second'])
    )
    df = stairs.sample(s, [-4,-2,1,3], expand_key=True)
    df = df.sort_values(list(df.columns)).reset_index(drop=True)
    assert df.to_dict() == {
        'points': {0: -4, 1: -4, 2: -2, 3: -2, 4: 1, 5: 1, 6: 3, 7: 3},
        'value': {0: -1.75, 1: 0.0, 2: -1.75, 3: -1.75, 4: -2.5, 5: 0.25, 6: -0.5, 7: 2.75},
        'first': {0: 'A', 1: 'A', 2: 'A', 3: 'A', 4: 'A', 5: 'A', 6: 'A', 7: 'A'},
        'second': {0: 'X', 1: 'Y', 2: 'X', 3: 'Y', 4: 'Y', 5: 'X', 6: 'Y', 7: 'X'}
    }
    
# def test_sample_series_(IS1, IS2):
    # s = pd.Series(
        # [IS1, IS2],
        # index = pd.MultiIndex.from_product([("A",), ("X","Y")], names=['first', 'second'])
    # )
    # df = stairs.sample(s, [-4,-2,1,3], expand_key=False)
    # df = df.sort_values(list(df.columns)).reset_index(drop=True)
    # assert df.to_dict() == {'points': {0: -4, 1: -4, 2: -2, 3: -2, 4: 1, 5: 1, 6: 3, 7: 3},
        # 'key': {0: ('A', 'X'), 1: ('A', 'Y'), 2: ('A', 'X'), 3: ('A', 'Y'), 4: ('A', 'X'), 5: ('A', 'Y'), 6: ('A', 'X'), 7: ('A', 'Y')},
        # 'value': {0: -1.75, 1: 0.0, 2: -1.75, 3: -1.75, 4: 0.25, 5: -2.5, 6: 2.75,7: -0.5}
        # }