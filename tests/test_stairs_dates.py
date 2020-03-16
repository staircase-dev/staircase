import pytest
import itertools
import staircase.stairs as stairs
import pandas as pd

def _expand_interval_definition(start, end=None, value=1):
    return start, end, value

def _compare_iterables(it1, it2):
    it1 = [i for i in it1 if i is not None]
    it2 = [i for i in it2 if i is not None]    
    for e1, e2 in zip(it1, it2):
        if e1 != e2:
            return False
    return True
    
@pytest.fixture
def IS1():
    int_seq1 = stairs.Stairs(0, use_dates=True)
    int_seq1.layer(pd.Timestamp(2020,1,1),pd.Timestamp(2020,1,10),2)
    int_seq1.layer(pd.Timestamp(2020,1,3),pd.Timestamp(2020,1,5),2.5)
    int_seq1.layer(pd.Timestamp(2020,1,6),pd.Timestamp(2020,1,7),-2.5)
    int_seq1.layer(pd.Timestamp(2020,1,7),pd.Timestamp(2020,1,10),-2.5)
    return int_seq1

@pytest.fixture
def IS2():    
    int_seq2 = stairs.Stairs(0, use_dates=True)
    int_seq2.layer(pd.Timestamp(2020,1,1),pd.Timestamp(2020,1,7),-2.5)
    int_seq2.layer(pd.Timestamp(2020,1,8),pd.Timestamp(2020,1,10),5)
    int_seq2.layer(pd.Timestamp(2020,1,2),pd.Timestamp(2020,1,5),4.5)
    int_seq2.layer(pd.Timestamp(2020,1,2,12),pd.Timestamp(2020,1,4),-2.5)
    return int_seq2
    
@pytest.fixture
def IS3(): #boolean    
    int_seq = stairs.Stairs(0, use_dates=True)
    int_seq.layer(pd.Timestamp(2020,1,10),pd.Timestamp(2020,1,30),1)
    int_seq.layer(pd.Timestamp(2020,1,12),pd.Timestamp(2020,1,13),-1)
    int_seq.layer(pd.Timestamp(2020,1,15),pd.Timestamp(2020,1,18),-1)
    int_seq.layer(pd.Timestamp(2020,1,20,12),pd.Timestamp(2020,1,21),-1)
    int_seq.layer(pd.Timestamp(2020,1,23),pd.Timestamp(2020,1,23,12),-1)
    int_seq.layer(pd.Timestamp(2020,1,27),pd.Timestamp(2020,1,29,12),-1)
    return int_seq

@pytest.fixture
def IS4(): #boolean      
    int_seq = stairs.Stairs(0, use_dates=True)
    int_seq.layer(pd.Timestamp(2020,1,9),pd.Timestamp(2020,1,29),1)
    int_seq.layer(pd.Timestamp(2020,1,10,12),pd.Timestamp(2020,1,12),-1)
    int_seq.layer(pd.Timestamp(2020,1,12,12),pd.Timestamp(2020,1,13),-1)
    int_seq.layer(pd.Timestamp(2020,1,20),pd.Timestamp(2020,1,23),-1)
    int_seq.layer(pd.Timestamp(2020,1,26),pd.Timestamp(2020,1,26,12),-1)
    int_seq.layer(pd.Timestamp(2020,1,27),pd.Timestamp(2020,1,28,12),-1)
    return int_seq
    
def test_max_dates_1(IS1):
    assert IS1.max() == 4.5, "Expected maximum to be 4.5"
    
def test_max_dates_2(IS1):
    assert IS1.max(upper=pd.Timestamp(2020,1,2)) == 2, "Expected maximum to be 2"

def test_max_dates_3(IS1):
    assert IS1.max(lower=pd.Timestamp(2020,1,5,12)) == 2, "Expected maximum to be 2"

def test_max_dates_4(IS1):
    assert IS1.max(lower=pd.Timestamp(2020,1,8),upper=pd.Timestamp(2020,1,9)) == -0.5, "Expected maximum to be -0.5"

def test_min_dates_1(IS1):
    assert IS1.min() == -0.5, "Expected minimum to be -0.5"
    
def test_min_dates_2(IS1):
    assert IS1.min(upper=pd.Timestamp(2020,1,4)) == 2, "Expected minimum to be 2"

def test_min_dates_3(IS1):
    assert IS1.min(lower=pd.Timestamp(2020,1,10,12)) == 0, "Expected minimum to be 0"

def test_min_dates_4(IS1):
    assert IS1.min(lower=pd.Timestamp(2020,1,4),upper=pd.Timestamp(2020,1,4,12)) == 4.5, "Expected minimum to be 4.5"

def test_mode_dates_1(IS1):
    assert IS1.mode() == -0.5, "Expected mode to be -0.5"
    
def test_mode_dates_2(IS1):
    assert IS1.mode(upper=pd.Timestamp(2020,1,4)) == 2, "Expected mode to be 2"

def test_mode_dates_3(IS1):
    assert IS1.mode(lower=pd.Timestamp(2019,12,27)) == 0, "Expected mode to be 0"

def test_mode_dates_4(IS1):
    assert IS1.mode(lower=pd.Timestamp(2020,1,4,12),upper=pd.Timestamp(2020,1,6,12)) == 2, "Expected mode to be 2"
    
def test_median_dates_1(IS1):
    assert IS1.median() == 2, "Expected median to be 2"
    
def test_median_dates_2(IS1):
    assert IS1.median(upper=pd.Timestamp(2020,1,17)) == 0, "Expected median to be 0"

def test_median_dates_3(IS1):
    assert IS1.median(lower=pd.Timestamp(2020,1,3)) == -0.5, "Expected median to be -0.5"

def test_median_dates_4(IS1):
    assert IS1.median(lower=pd.Timestamp(2020,1,4,12),upper=pd.Timestamp(2020,1,6,12)) == 2, "Expected median to be 2"

def test_mean_dates_1(IS1):
    assert abs(IS1.mean() -13/9) <= 0.00001, "Expected mean to be 13/9"
    
def test_mean_dates_2(IS1):
    assert IS1.mean(upper=pd.Timestamp(2020,1,6)) == 3, "Expected mean to be 3"

def test_mean_dates_3(IS1):
    assert IS1.mean(lower=pd.Timestamp(2020,1,4)) == 0.75, "Expected mean to be 0.75"

def test_mean_dates_4(IS1):
    assert IS1.mean(lower=pd.Timestamp(2020,1,4),upper=pd.Timestamp(2020,1,8)) == 1.375, "Expected mean to be 1.375"
    