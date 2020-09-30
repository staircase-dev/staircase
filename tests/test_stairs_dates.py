import pytest
import itertools
import staircase.stairs as stairs
import pandas as pd
import numpy as np

def _expand_interval_definition(start, end=None, value=1):
    return start, end, value

def _compare_iterables(it1, it2):
    it1 = [i for i in it1 if i is not None]
    it2 = [i for i in it2 if i is not None]    
    for e1, e2 in zip(it1, it2):
        if e1 != e2:
            return False
    return True
    
def s1():
    int_seq1 = stairs.Stairs(0, use_dates=True)
    int_seq1.layer(pd.Timestamp(2020,1,1),pd.Timestamp(2020,1,10),2)
    int_seq1.layer(pd.Timestamp(2020,1,3),pd.Timestamp(2020,1,5),2.5)
    int_seq1.layer(pd.Timestamp(2020,1,6),pd.Timestamp(2020,1,7),-2.5)
    int_seq1.layer(pd.Timestamp(2020,1,7),pd.Timestamp(2020,1,10),-2.5)
    return int_seq1

def s2():    
    int_seq2 = stairs.Stairs(0, use_dates=True)
    int_seq2.layer(pd.Timestamp(2020,1,1),pd.Timestamp(2020,1,7),-2.5)
    int_seq2.layer(pd.Timestamp(2020,1,8),pd.Timestamp(2020,1,10),5)
    int_seq2.layer(pd.Timestamp(2020,1,2),pd.Timestamp(2020,1,5),4.5)
    int_seq2.layer(pd.Timestamp(2020,1,2,12),pd.Timestamp(2020,1,4),-2.5)
    return int_seq2
    
def s3(): #boolean    
    int_seq = stairs.Stairs(0, use_dates=True)
    int_seq.layer(pd.Timestamp(2020,1,10),pd.Timestamp(2020,1,30),1)
    int_seq.layer(pd.Timestamp(2020,1,12),pd.Timestamp(2020,1,13),-1)
    int_seq.layer(pd.Timestamp(2020,1,15),pd.Timestamp(2020,1,18),-1)
    int_seq.layer(pd.Timestamp(2020,1,20,12),pd.Timestamp(2020,1,21),-1)
    int_seq.layer(pd.Timestamp(2020,1,23),pd.Timestamp(2020,1,23,12),-1)
    int_seq.layer(pd.Timestamp(2020,1,27),pd.Timestamp(2020,1,29,12),-1)
    return int_seq

def s4(): #boolean      
    int_seq = stairs.Stairs(0, use_dates=True)
    int_seq.layer(pd.Timestamp(2020,1,9),pd.Timestamp(2020,1,29),1)
    int_seq.layer(pd.Timestamp(2020,1,10,12),pd.Timestamp(2020,1,12),-1)
    int_seq.layer(pd.Timestamp(2020,1,12,12),pd.Timestamp(2020,1,13),-1)
    int_seq.layer(pd.Timestamp(2020,1,20),pd.Timestamp(2020,1,23),-1)
    int_seq.layer(pd.Timestamp(2020,1,26),pd.Timestamp(2020,1,26,12),-1)
    int_seq.layer(pd.Timestamp(2020,1,27),pd.Timestamp(2020,1,28,12),-1)
    return int_seq
    
@pytest.fixture
def s1_fix():
    return s1()

@pytest.fixture
def s2_fix():
    return s2()

@pytest.fixture
def s3_fix():
    return s3()

@pytest.fixture
def s4_fix():
    return s4()    
    
def test_max_dates_1(s1_fix):
    assert s1_fix.max() == 4.5, "Expected maximum to be 4.5"
    
def test_max_dates_2(s1_fix):
    assert s1_fix.max(upper=pd.Timestamp(2020,1,2)) == 2, "Expected maximum to be 2"

def test_max_dates_3(s1_fix):
    assert s1_fix.max(lower=pd.Timestamp(2020,1,5,12)) == 2, "Expected maximum to be 2"

def test_max_dates_4(s1_fix):
    assert s1_fix.max(lower=pd.Timestamp(2020,1,8),upper=pd.Timestamp(2020,1,9)) == -0.5, "Expected maximum to be -0.5"

def test_min_dates_1(s1_fix):
    assert s1_fix.min() == -0.5, "Expected minimum to be -0.5"
    
def test_min_dates_2(s1_fix):
    assert s1_fix.min(upper=pd.Timestamp(2020,1,4)) == 2, "Expected minimum to be 2"

def test_min_dates_3(s1_fix):
    assert s1_fix.min(lower=pd.Timestamp(2020,1,10,12)) == 0, "Expected minimum to be 0"

def test_min_dates_4(s1_fix):
    assert s1_fix.min(lower=pd.Timestamp(2020,1,4),upper=pd.Timestamp(2020,1,4,12)) == 4.5, "Expected minimum to be 4.5"

def test_mode_dates_1(s1_fix):
    assert s1_fix.mode() == -0.5, "Expected mode to be -0.5"
    
def test_mode_dates_2(s1_fix):
    assert s1_fix.mode(upper=pd.Timestamp(2020,1,4)) == 2, "Expected mode to be 2"

def test_mode_dates_3(s1_fix):
    assert s1_fix.mode(lower=pd.Timestamp(2019,12,27)) == 0, "Expected mode to be 0"

def test_mode_dates_4(s1_fix):
    assert s1_fix.mode(lower=pd.Timestamp(2020,1,4,12),upper=pd.Timestamp(2020,1,6,12)) == 2, "Expected mode to be 2"
    
def test_median_dates_1(s1_fix):
    assert s1_fix.median() == 2, "Expected median to be 2"
    
def test_median_dates_2(s1_fix):
    assert s1_fix.median(upper=pd.Timestamp(2020,1,17)) == 0, "Expected median to be 0"

def test_median_dates_3(s1_fix):
    assert s1_fix.median(lower=pd.Timestamp(2020,1,3)) == -0.5, "Expected median to be -0.5"

def test_median_dates_4(s1_fix):
    assert s1_fix.median(lower=pd.Timestamp(2020,1,4,12),upper=pd.Timestamp(2020,1,6,12)) == 2, "Expected median to be 2"

def test_mean_dates_1(s1_fix):
    assert abs(s1_fix.mean() -13/9) <= 0.00001, "Expected mean to be 13/9"
    
def test_mean_dates_2(s1_fix):
    assert s1_fix.mean(upper=pd.Timestamp(2020,1,6)) == 3, "Expected mean to be 3"

def test_mean_dates_3(s1_fix):
    assert s1_fix.mean(lower=pd.Timestamp(2020,1,4)) == 0.75, "Expected mean to be 0.75"

def test_mean_dates_4(s1_fix):
    assert s1_fix.mean(lower=pd.Timestamp(2020,1,4),upper=pd.Timestamp(2020,1,8)) == 1.375, "Expected mean to be 1.375"

def test_integrate_dates_1(s1_fix):
    assert s1_fix.integrate() == 312, "Expected integral to be 312"
    
def test_integrate_dates_2(s1_fix):
    assert s1_fix.integrate(upper=pd.Timestamp(2020,1,6)) == 360, "Expected integral to be 360"

def test_integrate_dates_3(s1_fix):
    assert s1_fix.integrate(lower=pd.Timestamp(2020,1,4)) == 108, "Expected integral to be 108"

def test_integrate_dates_4(s1_fix):
    assert s1_fix.integrate(lower=pd.Timestamp(2020,1,4),upper=pd.Timestamp(2020,1,8)) == 132, "Expected integral to be 132"

def test_integral_and_mean_dates_1(s1_fix):
    integral, mean = s1_fix.get_integral_and_mean()
    assert abs(mean -13/9) <= 0.00001, "Expected mean to be 13/9"
    assert integral == 312, "Expected integral to be 312"
    
def test_integral_and_mean_dates_2(s1_fix):
    integral, mean = s1_fix.get_integral_and_mean(upper=pd.Timestamp(2020,1,6))
    assert mean == 3, "Expected mean to be 3"
    assert integral == 360, "Expected integral to be 360"
    
def test_integral_and_mean_3(s1_fix):
    integral, mean = s1_fix.get_integral_and_mean(lower=pd.Timestamp(2020,1,4))
    assert mean == 0.75, "Expected mean to be 0.75"
    assert integral == 108, "Expected integral to be 108"
    
def test_integral_and_mean_dates_4(s1_fix):
    integral, mean = s1_fix.get_integral_and_mean(lower=pd.Timestamp(2020,1,4),upper=pd.Timestamp(2020,1,8))
    assert mean == 1.375, "Expected mean to be 1.375"
    assert integral == 132, "Expected integral to be 132"

def test_percentile_dates_1(s1_fix):
    assert s1_fix.percentile(20) == -0.5, "Expected 20th percentile to be -0.5"
    assert s1_fix.percentile(40) == -0.5, "Expected 40th percentile to be -0.5"
    assert s1_fix.percentile(60) == 2, "Expected 60th percentile to be 2"
    assert s1_fix.percentile(80) == 4.5, "Expected 80th percentile to be 4.5"
    
def test_percentile_dates_2(s1_fix):
    assert s1_fix.percentile(20, upper=pd.Timestamp(2020,1,6)) == 2, "Expected 20th percentile to be 2"
    assert s1_fix.percentile(40, upper=pd.Timestamp(2020,1,6)) == 2, "Expected 40th percentile to be 2"
    assert s1_fix.percentile(60, upper=pd.Timestamp(2020,1,6)) == 3.25, "Expected 60th percentile to be 3.25"
    assert s1_fix.percentile(80, upper=pd.Timestamp(2020,1,6)) == 4.5, "Expected 80th percentile to be 4.5"
        
def test_percentile_dates_3(s1_fix):
    assert s1_fix.percentile(20, lower=pd.Timestamp(2020,1,4)) == -0.5, "Expected 20th percentile to be -0.5"
    assert s1_fix.percentile(40, lower=pd.Timestamp(2020,1,4)) == -0.5, "Expected 40th percentile to be -0.5"
    assert s1_fix.percentile(60, lower=pd.Timestamp(2020,1,4)) == -0.5, "Expected 60th percentile to be -0.5"
    assert s1_fix.percentile(80, lower=pd.Timestamp(2020,1,4)) == 2, "Expected 80th percentile to be 2"
    
def test_percentile_dates_4(s1_fix):
    assert s1_fix.percentile(20, lower=pd.Timestamp(2020,1,4),upper=pd.Timestamp(2020,1,8)) == -0.5, "Expected 20th percentile to be -0.5"
    assert s1_fix.percentile(40, lower=pd.Timestamp(2020,1,4),upper=pd.Timestamp(2020,1,8)) == -0.5, "Expected 40th percentile to be -0.5"
    assert s1_fix.percentile(60, lower=pd.Timestamp(2020,1,4),upper=pd.Timestamp(2020,1,8)) == 2, "Expected 60th percentile to be 2"
    assert s1_fix.percentile(80, lower=pd.Timestamp(2020,1,4),upper=pd.Timestamp(2020,1,8)) == 4.5, "Expected 80th percentile to be 4.5"
    
def test_percentile_stairs_dates_1(s1_fix):
    assert s1_fix.percentile_stairs() == stairs.Stairs().layer(0,400/9, -0.5).layer(400/9, 700/9, 2).layer(700/9, None, 4.5)

def test_percentile_stairs_dates_2(s1_fix):
    assert s1_fix.percentile_stairs(upper=pd.Timestamp(2020,1,6)) == stairs.Stairs().layer(0,60,2).layer(60, None, 4.5)

def test_percentile_stairs_dates_3(s1_fix):
    assert s1_fix.percentile_stairs(lower=pd.Timestamp(2020,1,4)) == stairs.Stairs().layer(0,400/6,-0.5).layer(400/6, 500/6, 2).layer(500/6, None, 4.5)
    
def test_percentile_stairs_dates_4(s1_fix):
    assert s1_fix.percentile_stairs(lower=pd.Timestamp(2020,1,4),upper=pd.Timestamp(2020,1,8)) == stairs.Stairs().layer(0,50,-0.5).layer(50, 75, 2).layer(75, None, 4.5)

def test_plot(s1_fix):
    s1_fix.plot()
    
def test_resample_dates_1(s1_fix):
    assert s1_fix.resample(pd.Timestamp(2020,1,4)).step_changes() == {pd.Timestamp(2020,1,4): 4.5}
    
def test_resample_dates_2(s1_fix):
    assert s1_fix.resample(pd.Timestamp(2020,1,6), how='right').step_changes() == {pd.Timestamp(2020,1,6): -0.5}

def test_resample_dates_3(s1_fix):
    assert s1_fix.resample(pd.Timestamp(2020,1,6), how='left').step_changes() == {pd.Timestamp(2020,1,6): 2}
    
def test_resample_dates_4(s1_fix):
    assert s1_fix.resample([pd.Timestamp(2020,1,4), pd.Timestamp(2020,1,6)]).step_changes() == {pd.Timestamp(2020,1,4): 4.5, pd.Timestamp(2020,1,6): -5.0}

def test_resample_dates_5(s1_fix):
    assert s1_fix.resample([pd.Timestamp(2020,1,4), pd.Timestamp(2020,1,6)], how='right').step_changes() == {pd.Timestamp(2020,1,4): 4.5, pd.Timestamp(2020,1,6): -5.0}
    
def test_resample_dates_6(s1_fix):
    assert s1_fix.resample([pd.Timestamp(2020,1,4), pd.Timestamp(2020,1,6)], how='left').step_changes() == {pd.Timestamp(2020,1,4): 4.5, pd.Timestamp(2020,1,6): -2.5}

def test_sample_dates_1(s1_fix):
    assert s1_fix.sample(pd.Timestamp(2020,1,6)) == -0.5

def test_sample_dates_2(s1_fix):
    assert s1_fix.sample(pd.Timestamp(2020,1,6), how='right') == -0.5

def test_sample_dates_3(s1_fix):
    assert s1_fix.sample(pd.Timestamp(2020,1,6), how='left') == 2
    
def test_sample_dates_4(s1_fix):    
    assert _compare_iterables(s1_fix.sample([pd.Timestamp(2020,1,4), pd.Timestamp(2020,1,6)]), [4.5, -0.5])
    
def test_sample_dates_5(s1_fix):    
    assert _compare_iterables(s1_fix.sample([pd.Timestamp(2020,1,4), pd.Timestamp(2020,1,6)], how='right'), [4.5, -0.5])
   
def test_sample_dates_6(s1_fix):    
    assert _compare_iterables(s1_fix.sample([pd.Timestamp(2020,1,4), pd.Timestamp(2020,1,6)], how='left'), [4.5, 2])

def test_step_changes_dates(s1_fix):
    assert s1_fix.step_changes() == {pd.Timestamp('2020-01-01 00:00:00'): 2,
                             pd.Timestamp('2020-01-03 00:00:00'): 2.5,
                             pd.Timestamp('2020-01-05 00:00:00'): -2.5,
                             pd.Timestamp('2020-01-06 00:00:00'): -2.5,
                             pd.Timestamp('2020-01-10 00:00:00'): 0.5
                        }
                        
def test_dataframe_dates(s1_fix):
    ans = pd.DataFrame({
        "start":[pd.NaT, pd.to_datetime('2020-01-01'), pd.to_datetime('2020-01-03'), pd.to_datetime('2020-01-05'), pd.to_datetime('2020-01-06'), pd.to_datetime('2020-01-10')],
        "end":[pd.to_datetime('2020-01-01'), pd.to_datetime('2020-01-03'), pd.to_datetime('2020-01-05'), pd.to_datetime('2020-01-06'), pd.to_datetime('2020-01-10'), pd.NaT],
        "value":[0,2,4.5,2,-0.5,0]
    })
    assert s1_fix.to_dataframe().equals(ans)
    
def test_add_dates(s1_fix, s2_fix):
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
    assert (s1_fix + s2_fix).step_changes() == ans 
    
def test_subtract_dates(s1_fix, s2_fix):
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
    assert (s1_fix - s2_fix).step_changes() == ans 
 
def test_to_dataframe(s1_fix):
    s1_fix.to_dataframe()
    
@pytest.mark.parametrize("stairs_instance, bounds, cuts",
    itertools.product(
        [s1(),s2(),s3(),s4()],
        [(pd.Timestamp(2020,1,3), pd.Timestamp(2020,1,4)), (pd.Timestamp(2020,1,1), pd.Timestamp(2020,1,4)), (pd.Timestamp(2020,1,2), pd.Timestamp(2020,2,4))],
        [None, (-2, 0, 0.5, 4, 4.5, 7)],
    )
)     
def test_hist_default_bins_left_closed(stairs_instance, bounds, cuts):

    def make_expected_result(interval_index, lower, upper):
        return pd.Series(
            [((stairs_instance >= i.left)*(stairs_instance < i.right)).mean(lower, upper) for i in interval_index],
            index = interval_index,
            dtype='float64',
        )

    hist = stairs_instance.hist(bin_edges=cuts, lower=bounds[0], upper=bounds[1])
    expected = make_expected_result(hist.index, *bounds)
    assert (hist.apply(round,5) == expected.apply(round,5)).all()
    
    
@pytest.mark.parametrize("stairs_instance, bounds, cuts",
    itertools.product(
        [s1(),s2(),s3(),s4()],
        [(pd.Timestamp(2020,1,3), pd.Timestamp(2020,1,4)), (pd.Timestamp(2020,1,1), pd.Timestamp(2020,1,4)), (pd.Timestamp(2020,1,2), pd.Timestamp(2020,2,4))],
        [None, (-2, 0, 0.5, 4, 4.5, 7)],
    )
)
def test_hist_default_bins_right_closed(stairs_instance, bounds, cuts):

    def make_expected_result(interval_index, lower, upper):
        return pd.Series(
            [((stairs_instance > i.left)*(stairs_instance <= i.right)).mean(lower, upper) for i in interval_index],
            index = interval_index,
            dtype='float64',
        )

    hist = stairs_instance.hist(bin_edges=cuts, lower=bounds[0], upper=bounds[1], closed='right')
    expected = make_expected_result(hist.index, *bounds)
    assert (hist.apply(round,5) == expected.apply(round,5)).all()
    
    
@pytest.mark.parametrize("stairs_instance, bounds, closed",
    itertools.product(
        [s1(),s2(),s3(),s4()],
        [(pd.Timestamp(2020,1,3), pd.Timestamp(2020,1,4)), (pd.Timestamp(2020,1,1), pd.Timestamp(2020,1,4)), (pd.Timestamp(2020,1,2), pd.Timestamp(2020,2,4))],
        ['left', 'right'],
    )
)    
def test_hist_default_bins(stairs_instance, bounds, closed):
    #really testing the default binning process here
    hist = stairs_instance.hist(lower=bounds[0], upper=bounds[1], closed=closed)
    assert abs(hist.sum() - 1) < 0.000001
 
 
# low, high = pd.Timestamp(2020,1,1), pd.Timestamp(2020,1,10)
# total_secs = int((high-low).total_seconds())
# pts = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs, total_secs)]
# np.var(st1(pts))
# = 3.8580225122881124

# low, high = pd.Timestamp(2019,12,30), pd.Timestamp(2020,1,8,16)
# total_secs = int((high-low).total_seconds())
# pts = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs, total_secs)]
# np.var(st1(pts))
# = 3.501189060642099

# low, high = pd.Timestamp(2020,1,2), pd.Timestamp(2020,1,11,3)
# total_secs = int((high-low).total_seconds())
# pts = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs, total_secs)]
# np.var(st1(pts))
# = 3.971476824920255

@pytest.mark.parametrize("bounds, expected", [
    ((), 3.8580225122881124),
    ((pd.Timestamp(2019,12,30), pd.Timestamp(2020,1,8,16)), 3.501189060642099),
    ((pd.Timestamp(2020,1,2), pd.Timestamp(2020,1,11,3)), 3.971476824920255),
])
def test_s1_var(bounds, expected):
    assert np.isclose(s1().var(*bounds), expected, atol=0.00001)    
    
# low, high = pd.Timestamp(2020,1,1), pd.Timestamp(2020,1,10)
# total_secs = int((high-low).total_seconds())
# pts = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs, total_secs)]
# np.var(st2(pts))
# = 8.068647476524724

# low, high = pd.Timestamp(2019,12,30), pd.Timestamp(2020,1,8,16)
# total_secs = int((high-low).total_seconds())
# pts = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs, total_secs)]
# np.var(st2(pts))
# = 4.283962544589773

# low, high = pd.Timestamp(2020,1,2), pd.Timestamp(2020,1,11,3)
# total_secs = int((high-low).total_seconds())
# pts = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs, total_secs)]
# np.var(st2(pts))
# = 6.9166823043723

@pytest.mark.parametrize("bounds, expected", [
    ((), 8.068647476524724),
    ((pd.Timestamp(2019,12,30), pd.Timestamp(2020,1,8,16)), 4.283962544589773),
    ((pd.Timestamp(2020,1,2), pd.Timestamp(2020,1,11,3)), 6.9166823043723),
])
def test_s2_var(bounds, expected):
    assert np.isclose(s2().var(*bounds), expected, atol=0.00001)   
    
    
# low, high = pd.Timestamp(2020,1,1), pd.Timestamp(2020,1,10)
# total_secs = int((high-low).total_seconds())
# pts = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs, total_secs)]
# np.std(st1(pts))
# = 1.9641849485952467

# low, high = pd.Timestamp(2019,12,30), pd.Timestamp(2020,1,8,16)
# total_secs = int((high-low).total_seconds())
# pts = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs, total_secs)]
# np.std(st1(pts))
# = 1.871146456224659

# low, high = pd.Timestamp(2020,1,2), pd.Timestamp(2020,1,11,3)
# total_secs = int((high-low).total_seconds())
# pts = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs, total_secs)]
# np.std(st1(pts))
# = 1.9928564486485862

@pytest.mark.parametrize("bounds, expected", [
    ((), 1.9641849485952467),
    ((pd.Timestamp(2019,12,30), pd.Timestamp(2020,1,8,16)), 1.871146456224659),
    ((pd.Timestamp(2020,1,2), pd.Timestamp(2020,1,11,3)), 1.9928564486485862),
])
def test_s1_std(bounds, expected):
    assert np.isclose(s1().std(*bounds), expected, atol=0.00001)   
    
    
# low, high = pd.Timestamp(2020,1,1), pd.Timestamp(2020,1,10)
# total_secs = int((high-low).total_seconds())
# pts = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs, total_secs)]
# np.std(st2(pts))
# = 2.840536476886844

# low, high = pd.Timestamp(2019,12,30), pd.Timestamp(2020,1,8,16)
# total_secs = int((high-low).total_seconds())
# pts = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs, total_secs)]
# np.std(st2(pts))
# = 2.0697735491086395

# low, high = pd.Timestamp(2020,1,2), pd.Timestamp(2020,1,11,3)
# total_secs = int((high-low).total_seconds())
# pts = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs, total_secs)]
# np.std(st2(pts))
# = 2.6299586126728878

@pytest.mark.parametrize("bounds, expected", [
    ((), 2.840536476886844),
    ((pd.Timestamp(2019,12,30), pd.Timestamp(2020,1,8,16)), 2.0697735491086395),
    ((pd.Timestamp(2020,1,2), pd.Timestamp(2020,1,11,3)), 2.6299586126728878),
])
def test_s2_std(bounds, expected):
    assert np.isclose(s2().std(*bounds), expected, atol=0.00001)   