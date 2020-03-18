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

def test_integrate_dates_1(IS1):
    assert IS1.integrate() == 312, "Expected integral to be 312"
    
def test_integrate_dates_2(IS1):
    assert IS1.integrate(upper=pd.Timestamp(2020,1,6)) == 360, "Expected integral to be 360"

def test_integrate_dates_3(IS1):
    assert IS1.integrate(lower=pd.Timestamp(2020,1,4)) == 108, "Expected integral to be 108"

def test_integrate_dates_4(IS1):
    assert IS1.integrate(lower=pd.Timestamp(2020,1,4),upper=pd.Timestamp(2020,1,8)) == 132, "Expected integral to be 132"

def test_integral_and_mean_dates_1(IS1):
    integral, mean = IS1.get_integral_and_mean()
    assert abs(mean -13/9) <= 0.00001, "Expected mean to be 13/9"
    assert integral == 312, "Expected integral to be 312"
    
def test_integral_and_mean_dates_2(IS1):
    integral, mean = IS1.get_integral_and_mean(upper=pd.Timestamp(2020,1,6))
    assert mean == 3, "Expected mean to be 3"
    assert integral == 360, "Expected integral to be 360"
    
def test_integral_and_mean_3(IS1):
    integral, mean = IS1.get_integral_and_mean(lower=pd.Timestamp(2020,1,4))
    assert mean == 0.75, "Expected mean to be 0.75"
    assert integral == 108, "Expected integral to be 108"
    
def test_integral_and_mean_dates_4(IS1):
    integral, mean = IS1.get_integral_and_mean(lower=pd.Timestamp(2020,1,4),upper=pd.Timestamp(2020,1,8))
    assert mean == 1.375, "Expected mean to be 1.375"
    assert integral == 132, "Expected integral to be 132"

def test_percentile_dates_1(IS1):
    assert IS1.percentile(20) == -0.5, "Expected 20th percentile to be -0.5"
    assert IS1.percentile(40) == -0.5, "Expected 40th percentile to be -0.5"
    assert IS1.percentile(60) == 2, "Expected 60th percentile to be 2"
    assert IS1.percentile(80) == 4.5, "Expected 80th percentile to be 4.5"
    
def test_percentile_dates_2(IS1):
    assert IS1.percentile(20, upper=pd.Timestamp(2020,1,6)) == 2, "Expected 20th percentile to be 2"
    assert IS1.percentile(40, upper=pd.Timestamp(2020,1,6)) == 2, "Expected 40th percentile to be 2"
    assert IS1.percentile(60, upper=pd.Timestamp(2020,1,6)) == 3.25, "Expected 60th percentile to be 3.25"
    assert IS1.percentile(80, upper=pd.Timestamp(2020,1,6)) == 4.5, "Expected 80th percentile to be 4.5"
        
def test_percentile_dates_3(IS1):
    assert IS1.percentile(20, lower=pd.Timestamp(2020,1,4)) == -0.5, "Expected 20th percentile to be -0.5"
    assert IS1.percentile(40, lower=pd.Timestamp(2020,1,4)) == -0.5, "Expected 40th percentile to be -0.5"
    assert IS1.percentile(60, lower=pd.Timestamp(2020,1,4)) == -0.5, "Expected 60th percentile to be -0.5"
    assert IS1.percentile(80, lower=pd.Timestamp(2020,1,4)) == 2, "Expected 80th percentile to be 2"
    
def test_percentile_dates_4(IS1):
    assert IS1.percentile(20, lower=pd.Timestamp(2020,1,4),upper=pd.Timestamp(2020,1,8)) == -0.5, "Expected 20th percentile to be -0.5"
    assert IS1.percentile(40, lower=pd.Timestamp(2020,1,4),upper=pd.Timestamp(2020,1,8)) == -0.5, "Expected 40th percentile to be -0.5"
    assert IS1.percentile(60, lower=pd.Timestamp(2020,1,4),upper=pd.Timestamp(2020,1,8)) == 2, "Expected 60th percentile to be 2"
    assert IS1.percentile(80, lower=pd.Timestamp(2020,1,4),upper=pd.Timestamp(2020,1,8)) == 4.5, "Expected 80th percentile to be 4.5"
    
def test_percentile_Stairs_dates_1(IS1):
    assert IS1.percentile_Stairs() == stairs.Stairs().layer(0,400/9, -0.5).layer(400/9, 700/9, 2).layer(700/9, None, 4.5)

def test_percentile_Stairs_dates_2(IS1):
    assert IS1.percentile_Stairs(upper=pd.Timestamp(2020,1,6)) == stairs.Stairs().layer(0,60,2).layer(60, None, 4.5)

def test_percentile_Stairs_dates_3(IS1):
    assert IS1.percentile_Stairs(lower=pd.Timestamp(2020,1,4)) == stairs.Stairs().layer(0,400/6,-0.5).layer(400/6, 500/6, 2).layer(500/6, None, 4.5)
    
def test_percentile_Stairs_dates_4(IS1):
    assert IS1.percentile_Stairs(lower=pd.Timestamp(2020,1,4),upper=pd.Timestamp(2020,1,8)) == stairs.Stairs().layer(0,50,-0.5).layer(50, 75, 2).layer(75, None, 4.5)

def test_plot(IS1):
    IS1.plot()
    
def test_resample_dates_1(IS1):
    assert IS1.resample(pd.Timestamp(2020,1,4)).step_changes() == {pd.Timestamp(2020,1,4): 4.5}
    
def test_resample_dates_2(IS1):
    assert IS1.resample(pd.Timestamp(2020,1,6), how='right').step_changes() == {pd.Timestamp(2020,1,6): -0.5}

def test_resample_dates_3(IS1):
    assert IS1.resample(pd.Timestamp(2020,1,6), how='left').step_changes() == {pd.Timestamp(2020,1,6): 2}
    
def test_resample_dates_4(IS1):
    assert IS1.resample([pd.Timestamp(2020,1,4), pd.Timestamp(2020,1,6)]).step_changes() == {pd.Timestamp(2020,1,4): 4.5, pd.Timestamp(2020,1,6): -5.0}

def test_resample_dates_5(IS1):
    assert IS1.resample([pd.Timestamp(2020,1,4), pd.Timestamp(2020,1,6)], how='right').step_changes() == {pd.Timestamp(2020,1,4): 4.5, pd.Timestamp(2020,1,6): -5.0}
    
def test_resample_dates_6(IS1):
    assert IS1.resample([pd.Timestamp(2020,1,4), pd.Timestamp(2020,1,6)], how='left').step_changes() == {pd.Timestamp(2020,1,4): 4.5, pd.Timestamp(2020,1,6): -2.5}

def test_sample_dates_1(IS1):
    assert IS1.sample(pd.Timestamp(2020,1,6)) == -0.5

def test_sample_dates_2(IS1):
    assert IS1.sample(pd.Timestamp(2020,1,6), how='right') == -0.5

def test_sample_dates_3(IS1):
    assert IS1.sample(pd.Timestamp(2020,1,6), how='left') == 2
    
def test_sample_dates_4(IS1):    
    assert _compare_iterables(IS1.sample([pd.Timestamp(2020,1,4), pd.Timestamp(2020,1,6)]), [4.5, -0.5])
    
def test_sample_dates_5(IS1):    
    assert _compare_iterables(IS1.sample([pd.Timestamp(2020,1,4), pd.Timestamp(2020,1,6)], how='right'), [4.5, -0.5])
   
def test_sample_dates_6(IS1):    
    assert _compare_iterables(IS1.sample([pd.Timestamp(2020,1,4), pd.Timestamp(2020,1,6)], how='left'), [4.5, 2])

def test_step_changes_dates(IS1):
    assert IS1.step_changes() == {pd.Timestamp('2020-01-01 00:00:00'): 2,
                             pd.Timestamp('2020-01-03 00:00:00'): 2.5,
                             pd.Timestamp('2020-01-05 00:00:00'): -2.5,
                             pd.Timestamp('2020-01-06 00:00:00'): -2.5,
                             pd.Timestamp('2020-01-10 00:00:00'): 0.5
                        }
                        
def test_dataframe_dates(IS1):
    ans = pd.DataFrame({
        "start":[pd.NaT, pd.to_datetime('2020-01-01'), pd.to_datetime('2020-01-03'), pd.to_datetime('2020-01-05'), pd.to_datetime('2020-01-06'), pd.to_datetime('2020-01-10')],
        "end":[pd.to_datetime('2020-01-01'), pd.to_datetime('2020-01-03'), pd.to_datetime('2020-01-05'), pd.to_datetime('2020-01-06'), pd.to_datetime('2020-01-10'), pd.NaT],
        "value":[0,2,4.5,2,-0.5,0]
    })
    assert IS1.to_dataframe().equals(ans)
    
def test_add_dates(IS1, IS2):
    ans = {
        pd.Timestamp('2020-01-01 00:00:00'): -0.5,
        pd.Timestamp('2020-01-02 00:00:00'): 4.5,
        pd.Timestamp('2020-01-02 12:00:00'): -2.5,
        pd.Timestamp('2020-01-03 00:00:00'): 2.5,
        pd.Timestamp('2020-01-04 00:00:00'): 2.5,
        pd.Timestamp('2020-01-05 00:00:00'): -7.0,
        pd.Timestamp('2020-01-06 00:00:00'): -2.5,
        pd.Timestamp('2020-01-07 00:00:00'): 2.5,
        pd.Timestamp('2020-01-08 00:00:00'): 5,
        pd.Timestamp('2020-01-10 00:00:00'): -4.5
    }
    assert (IS1 + IS2).step_changes() == ans 
    
def test_subtract_dates(IS1, IS2):
    ans = {
        pd.Timestamp('2020-01-01 00:00:00'): 4.5,
        pd.Timestamp('2020-01-02 00:00:00'): -4.5,
        pd.Timestamp('2020-01-02 12:00:00'): 2.5,
        pd.Timestamp('2020-01-03 00:00:00'): 2.5,
        pd.Timestamp('2020-01-04 00:00:00'): -2.5,
        pd.Timestamp('2020-01-05 00:00:00'): 2.0,
        pd.Timestamp('2020-01-06 00:00:00'): -2.5,
        pd.Timestamp('2020-01-07 00:00:00'): -2.5,
        pd.Timestamp('2020-01-08 00:00:00'): -5,
        pd.Timestamp('2020-01-10 00:00:00'): 5.5
    }
    assert (IS1 - IS2).step_changes() == ans 