import pytest
import itertools
import staircase.stairs as stairs

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
    
@pytest.fixture
def IS3(): #boolean    
    int_seq = stairs.Stairs(0)
    int_seq.layer(-10,10,1)
    int_seq.layer(-8,-7,-1)
    int_seq.layer(-5,-2,-1)
    int_seq.layer(0.5,1,-1)
    int_seq.layer(3,3.5,-1)
    int_seq.layer(7,9.5,-1)
    return int_seq

@pytest.fixture
def IS4(): #boolean      
    int_seq = stairs.Stairs(0)
    int_seq.layer(-11,9,1)
    int_seq.layer(-9.5,-8,-1)
    int_seq.layer(-7.5,-7,-1)
    int_seq.layer(0,3,-1)
    int_seq.layer(6,6.5,-1)
    int_seq.layer(7,8.5,-1)
    return int_seq
     
def test_init():
    assert stairs.Stairs(0).identical(stairs.Stairs())
    assert stairs.Stairs().identical(stairs.Stairs(0))
    
@pytest.mark.parametrize("init_value", [0, 1.25, -1.25, 2, -2])      
def test_init2(init_value):
    int_seq = stairs.Stairs(init_value)
    assert int_seq.number_of_steps() == 0, "Initialised stairs.Stairs should have exactly one interval"
    
@pytest.mark.parametrize("init_value", [0, 1.25, -1.25, 2, -2])      
def test_init3(init_value):
    int_seq = stairs.Stairs(init_value)
    assert int_seq.step_changes() == {}, "Initialised stairs.Stairs should not have any finite interval endpoints"
    
@pytest.mark.parametrize("init_value", [0, 1.25, -1.25, 2, -2])      
def test_init4(init_value):
    int_seq = stairs.Stairs(init_value)
    assert int_seq(-1) == init_value, "Initialised stairs.Stairs should have initial value everywhere"
    assert int_seq(0) == init_value, "Initialised stairs.Stairs should have initial value everywhere"
    assert int_seq(1) == init_value, "Initialised stairs.Stairs should have initial value everywhere"
    
@pytest.mark.parametrize("init_value, added_interval", itertools.product([0, 1.25, -1.25], [(-2,1),(3,5,2),(1,5,-1),(-5,-3,3), (3,), (2,None,2)])) 
def test_one_finite_interval(init_value, added_interval):
    e = 0.0001
    int_seq = stairs.Stairs(init_value)
    int_seq.layer(*added_interval)
    start, end, value = _expand_interval_definition(*added_interval)
    assert int_seq.number_of_steps() == 2 - (end is None), "One finite interval added to initial infinite interval should result in 3 intervals"
    assert _compare_iterables(int_seq.step_changes(), (start,end)), "Finite endpoints are not what is expected"
    assert int_seq(float('-inf')) == init_value, "Adding finite interval should not change initial value"
    assert int_seq(float('inf')) == init_value+value*(end is None), "Adding finite interval should not change final value"
    assert int_seq(start-e) == init_value
    assert int_seq(start) == init_value + value
    assert int_seq(start+e) == init_value + value
    if end is not None:
        assert int_seq(end-e) == init_value + value
        assert int_seq(end) == init_value
    

@pytest.mark.parametrize("init_value, endpoints, value", itertools.product([0, 1.25, -1.25, 2, -2], [(-2,1,3), (-2,-1,3), (-3,-2,-1), (1,2,3)], [-1,2,3])) 
def test_two_adjacent_finite_interval_same_value(init_value, endpoints, value):
    e = 0.0001
    int_seq = stairs.Stairs(init_value)
    point1, point2, point3 = endpoints
    int_seq.layer(point1,point2,value)
    int_seq.layer(point2,point3,value)
    assert int_seq.number_of_steps() == 2, "Expected result to be 3 intervals"
    assert _compare_iterables(int_seq.step_changes(), (point1, point3)), "Finite endpoints are not what is expected"
    assert int_seq(float('-inf')) == init_value, "Adding finite interval should not change initial value"
    assert int_seq(float('inf')) == init_value, "Adding finite interval should not change final value"
    assert int_seq(point1-e) == init_value
    assert int_seq(point1) == init_value + value
    assert int_seq(point2) == init_value + value
    assert int_seq(point3-e) == init_value + value
    assert int_seq(point3) == init_value

@pytest.mark.parametrize("init_value, endpoints, value, delta", itertools.product([0, 1.25, -1.25, 2, -2], [(-2,1,3), (-2,-1,3), (-3,-2,-1), (1,2,3)], [-1,2,4], [3,-3, 1.5, -1.5])) 
def test_two_adjacent_finite_interval_different_value(init_value, endpoints, value, delta):
    e = 0.0001
    int_seq = stairs.Stairs(init_value)
    point1, point2, point3 = endpoints
    int_seq.layer(point1,point2,value)
    int_seq.layer(point2,point3,value+delta)
    assert int_seq.number_of_steps() == 3, "Expected result to be 4 intervals"
    assert _compare_iterables(int_seq.step_changes(), (point1, point2,point3)), "Finite endpoints are not what is expected"
    assert int_seq(float('-inf')) == init_value, "Adding finite interval should not change initial value"
    assert int_seq(float('inf')) == init_value, "Adding finite interval should not change final value"
    assert int_seq(point1-e) == init_value
    assert int_seq(point1) == init_value + value
    assert int_seq(point2) == init_value + value + delta
    assert int_seq(point3-e) == init_value + value + delta
    assert int_seq(point3) == init_value
    
@pytest.mark.parametrize("init_value, endpoints, value, delta", itertools.product([0, 1.25, -1.25, 2, -2], [(-2,1,2,3), (-3,-2,-1,3), (-4,-3,-2,-1), (0,1,2,3)], [-1,2,4], [3,-3, 1.5, -1.5])) 
def test_two_overlapping_finite_interval(init_value, endpoints, value, delta):
    e = 0.0001
    int_seq = stairs.Stairs(init_value)
    point1, point2, point3, point4 = endpoints
    int_seq.layer(point1,point3,value)
    int_seq.layer(point2,point4,value+delta)
    assert int_seq.number_of_steps() == 4, "Expected result to be 5 intervals"
    assert _compare_iterables(int_seq.step_changes(), (point1, point2,point3,point4)), "Finite endpoints are not what is expected"
    assert int_seq(float('-inf')) == init_value, "Adding finite interval should not change initial value"
    assert int_seq(float('inf')) == init_value, "Adding finite interval should not change final value"
    assert int_seq(point1-e) == init_value
    assert int_seq(point1) == init_value + value
    assert int_seq(point2) == init_value + 2*value + delta
    assert int_seq(point3-e) == init_value + 2*value + delta
    assert int_seq(point3) == init_value + value + delta
    assert int_seq(point4-e) == init_value + value + delta
    assert int_seq(point4) == init_value

@pytest.mark.parametrize("init_value, endpoints, value, delta", itertools.product([0, 1.25, -1.25, 2, -2], [(-2,1,2,3), (-3,-2,-1,3), (-4,-3,-2,-1), (0,1,2,3)], [-1,2,4], [3,-3, 1.5, -1.5])) 
def test_two_finite_interval_one_subinterval(init_value, endpoints, value, delta):
    e = 0.0001
    int_seq = stairs.Stairs(init_value)
    point1, point2, point3, point4 = endpoints
    int_seq.layer(point1,point4,value)
    int_seq.layer(point2,point3,value+delta)
    assert int_seq.number_of_steps() == 4, "Expected result to be 5 intervals"
    assert _compare_iterables(int_seq.step_changes(), (point1, point2,point3,point4)), "Finite endpoints are not what is expected"
    assert int_seq(float('-inf')) == init_value, "Adding finite interval should not change initial value"
    assert int_seq(float('inf')) == init_value, "Adding finite interval should not change final value"
    assert int_seq(point1-e) == init_value
    assert int_seq(point1) == init_value + value
    assert int_seq(point2) == init_value + 2*value + delta
    assert int_seq(point3-e) == init_value + 2*value + delta
    assert int_seq(point3) == init_value + value
    assert int_seq(point4-e) == init_value + value
    assert int_seq(point4) == init_value
    
@pytest.mark.parametrize("init_value", [0, 1.25, -1.25, 2, -2])   
def test_copy_and_equality(init_value):
    int_seq = stairs.Stairs(init_value)
    int_seq_copy = int_seq.copy()
    assert int_seq.identical(int_seq_copy)
    assert int_seq_copy.identical(int_seq)
    
@pytest.mark.parametrize("init_value", [0, 1.25, -1.25, 2, -2])   
def test_deepcopy(init_value):
    int_seq = stairs.Stairs(init_value)
    int_seq_copy = int_seq.copy()
    int_seq_copy.layer(1,2)
    assert not int_seq.identical(int_seq_copy)
    assert not int_seq_copy.identical(int_seq)
    
@pytest.mark.parametrize("init_value", [0, 1.25, -1.25, 2, -2]) 
def test_layer1(init_value):    
    intervals_to_add = [(-2,1),(3,5),(1,5),(-5,-3)]
    int_seq = stairs.Stairs(init_value)
    int_seq2 = stairs.Stairs(init_value)
    for start,end in intervals_to_add:
        int_seq.layer(start,end)
    starts, ends = list(zip(*intervals_to_add))
    int_seq2.layer(starts, ends)
    assert int_seq.identical(int_seq2)
    assert int_seq2.identical(int_seq)
    
@pytest.mark.parametrize("init_value", [0, 1.25, -1.25, 2, -2]) 
def test_layer2(init_value):    
    intervals_to_add = [(-2,1,1),(3,5,2),(1,5,-1),(-5,-3,3)]
    int_seq = stairs.Stairs(init_value)
    int_seq2 = stairs.Stairs(init_value)
    for interval in intervals_to_add:
        int_seq.layer(*interval)
    starts, ends, values = list(zip(*intervals_to_add))
    int_seq2.layer(starts, ends, values)    
    assert int_seq.identical(int_seq2)
    assert int_seq2.identical(int_seq)
    
def test_min(IS1, IS2): 
    int_seq1, int_seq2 = IS1, IS2
    calc = stairs._min_pair(int_seq1, int_seq2)
    expected = stairs.Stairs()
    expected.layer(-4,11,-1.75)
    expected.layer(1,11,-0.75)
    expected.layer(2,11,2.75)
    expected.layer(2.5,11,-0.75)
    expected.layer(4,11,2.5)
    expected.layer(5,11,-4.5)
    expected.layer(7,11,2)
    expected.layer(10,11,0.5)
    assert calc.identical(expected), "Min calculation not what it should be"
    assert expected.identical(calc), "Min calculation not what it should be"

def test_max(IS1, IS2): 
    int_seq1, int_seq2 = IS1, IS2
    calc = stairs._max_pair(int_seq1, int_seq2)
    expected = stairs.Stairs()
    expected = stairs.Stairs(0)
    expected.layer(-2,11,-1.75)
    expected.layer(1,11,2)
    expected.layer(2,11,1.75)
    expected.layer(2.5,11,-1.75)
    expected.layer(3,11,2.5)
    expected.layer(5,11,-0.75)
    expected.layer(6,11,-2.5)
    expected.layer(7,11,0.5)
    expected.layer(8,11,5)
    expected.layer(10,11,-5)
    assert calc.identical(expected), "Max calculation not what it should be"
    assert expected.identical(calc), "Max calculation not what it should be"

def test_make_boolean(IS2):
    int_seq = IS2
    calc = int_seq.make_boolean()
    expected = stairs.Stairs()
    expected.layer(-2,7,1)
    expected.layer(8,10,1)
    assert calc.identical(expected), "Boolean calculation not what it should be"
    assert expected.identical(calc), "Boolean calculation not what it should be"

def test_invert(IS2):
    int_seq = IS2
    calc = ~int_seq
    expected = stairs.Stairs(1)
    expected.layer(-2,7,-1)
    expected.layer(8,10,-1)
    assert calc.identical(expected), "Invert calculation not what it should be"
    assert expected.identical(calc), "Invert calculation not what it should be"

def test_and(IS3, IS4): 
    calc = IS3 & IS4
    expected = stairs.Stairs(0)
    expected.layer(-10,-9.5)
    expected.layer(-7,-5)
    expected.layer(-2,0)
    expected.layer(3.5,6)
    expected.layer(6.5,7)
    assert calc.identical(expected), "AND calculation not what it should be"
    assert expected.identical(calc), "AND calculation not what it should be"

def test_or(IS3, IS4): 
    calc = IS3 | IS4
    expected = stairs.Stairs(0)
    expected.layer(-11,-7.5)
    expected.layer(-7,0.5)
    expected.layer(1,7)
    expected.layer(8.5,9)
    expected.layer(9.5,10)
    assert calc.identical(expected), "OR calculation not what it should be"
    assert expected.identical(calc), "OR calculation not what it should be"


def test_lt(IS1, IS2): 
    calc = IS1 < IS2
    expected = stairs.Stairs(0)
    expected.layer(-4,-2)
    expected.layer(2,2.5)
    expected.layer(7,10)
    assert calc.identical(expected), "LT calculation not what it should be"
    assert expected.identical(calc), "LT calculation not what it should be"

def test_gt(IS1, IS2): 
    calc = IS1 > IS2
    expected = stairs.Stairs(0)
    expected.layer(1,2)
    expected.layer(2.5,7)
    assert calc.identical(expected), "GT calculation not what it should be"
    assert expected.identical(calc), "GT calculation not what it should be"
    
def test_le(IS1, IS2): 
    calc = IS1 <= IS2
    expected = stairs.Stairs(1)
    expected.layer(1,2,-1)
    expected.layer(2.5,7,-1)
    assert calc.identical(expected), "LE calculation not what it should be"
    assert expected.identical(calc), "LE calculation not what it should be"
    
def test_ge(IS1, IS2): 
    calc = IS1 >= IS2
    expected = stairs.Stairs(1)
    expected.layer(-4,-2,-1)
    expected.layer(2,2.5,-1)
    expected.layer(7,10,-1)
    assert calc.identical(expected), "GE calculation not what it should be"
    assert expected.identical(calc), "GE calculation not what it should be"    

def test_eq(IS1, IS2): 
    calc = IS1 == IS2
    expected = stairs.Stairs(1)
    expected.layer(-4,-2,-1)
    expected.layer(1,10,-1)
    assert calc.identical(expected), "EQ calculation not what it should be"
    assert expected.identical(calc), "EQ calculation not what it should be" 

def test_eq(IS1, IS2): 
    calc = IS1 == IS2
    expected = stairs.Stairs(1)
    expected.layer(-4,-2,-1)
    expected.layer(1,10,-1)
    assert calc.identical(expected), "EQ calculation not what it should be"
    assert expected.identical(calc), "EQ calculation not what it should be"     

def test_ne(IS1, IS2): 
    calc = IS1 != IS2
    expected = stairs.Stairs(0)
    expected.layer(-4,-2,1)
    expected.layer(1,10,1)
    assert calc.identical(expected), "NOT EQUAL calculation not what it should be"
    assert expected.identical(calc), "NOT EQUAL calculation not what it should be"     
    
@pytest.mark.parametrize("init_value", [0, 1.25, -1.25, 2, -2])         
def test_base_integrate_0_2(init_value):
    int_seq = stairs.Stairs(init_value)
    assert int_seq.integrate(0,2) == 2*init_value
    
@pytest.mark.parametrize("init_value", [0, 1.25, -1.25, 2, -2])         
def test_base_integrate_neg1_1(init_value):
    int_seq = stairs.Stairs(init_value)
    assert int_seq.integrate(-1,1) == 2*init_value
    
@pytest.mark.parametrize("init_value", [0, 1.25, -1.25, 2, -2])         
def test_base_integrate_neg2_0(init_value):
    int_seq = stairs.Stairs(init_value)
    assert int_seq.integrate(-2,0) == 2*init_value
    
@pytest.mark.parametrize("init_value", [0, 1.25, -1.25, 2, -2])         
def test_base_integrate_point5_1(init_value):
    int_seq = stairs.Stairs(init_value)
    assert int_seq.integrate(0.5,1) == 0.5*init_value

def test_integrate1(IS1, IS2):
    assert IS1.integrate() == -2.75
    assert IS2.integrate() == -0.5
    
def test_integrate2(IS1, IS2):
    assert IS1.integrate(-1,5.5) == 3.5
    assert IS2.integrate(-1,5.5) == -5

def test_mean1(IS1, IS2):
    assert abs(IS1.mean() - -0.19642857) < 0.000001
    assert abs(IS2.mean() - -0.04166666) < 0.000001

def test_mean2(IS1, IS2):
    assert abs(IS1.mean(2,8) - 1.125) < 0.000001
    assert abs(IS2.mean(2,8) - -0.45833333) < 0.000001
    
# @pytest.mark.parametrize("index, init_val", [(1,1.25), (2,-2.5), (3,3.25), (4,-4)])         
# def test_base_subtraction(IS_set, index, init_val):
    # int_seq = IS_set[index]
    # int_seq2 = IS_set[index-1]
    # assert (int_seq - int_seq2).identical(stairs.Stairs(init_val))
    
# @pytest.mark.parametrize("init_value, interval_a_b", itertools.product([0, 1.25, -1.25, 2, -2], [ ((-2,1),(3,5,2)), ((-2,1),(1,5,2)), ((-2,1),(0,5,2)), ((1,2),(3,5,2))]))  
# def test_two_interval_add_commutivity(init_value, interval_a_b):
    # ''' non-overlapping interval adds'''
    # int_seq = stairs.Stairs(init_value)
    # int_seq_copy = int_seq.copy()
    # interval_a, interval_b = interval_a_b
    # int_seq.layer(*interval_a).layer(*interval_b)
    # int_seq_copy.layer(*interval_b).layer(*interval_a)
    # assert int_seq.identical(int_seq_copy)
    # assert int_seq_copy.identical(int_seq)
    
# @pytest.mark.parametrize("init_value, interval_a_b", itertools.product([0, 1.25, -1.25, 2, -2], [ ((-2,1),(3,5,2)), ((-2,1),(1,5,2)), ((-2,1),(0,5,2)), ((1,2),(3,5,2))]))  
# def test_two_interval_integral(init_value, interval_a_b):
    
    # def get_area(interval):
        # height = 1
        # if len(interval) == 3:
            # height = interval[2]
        # return (interval[1] - interval[0])*height
            
    # int_seq = stairs.Stairs(init_value)
    # interval_a, interval_b = interval_a_b
    # interval_a_area = get_area(interval_a)
    # interval_b_area = get_area(interval_b)
    # int_seq.layer(*interval_a).layer(*interval_b)
    # assert int_seq.integrate(-10, 10) == 20*init_value + interval_a_area + interval_b_area
    
    

# @pytest.mark.parametrize("init_value", [0, 1.25, -1.25, 2, -2])     
# def test_two_interval_add_commutivity1(init_value):
    # ''' non-overlapping interval adds'''
    # int_seq = stairs.Stairs(init_value)
    # int_seq_copy = int_seq.copy()
    # int_seq.layer(-2,1).layer(3,5,2)
    # int_seq_copy.layer(3,5,2).layer(-2,1)
    # assert int_seq.identical(int_seq_copy)
    # assert int_seq_copy.identical(int_seq)
    
# @pytest.mark.parametrize("init_value", [0, 1.25, -1.25, 2, -2])  
# def test_two_interval_add_commutivity2(init_value):
    # ''' endpoint = startpoint interval adds'''
    # int_seq = stairs.Stairs(init_value)
    # int_seq_copy = int_seq.copy()
    # int_seq.layer(-2,1).layer(1,5,2)
    # int_seq_copy.layer(1,5,2).layer(-2,1)
    # assert int_seq.identical(int_seq_copy)
    # assert int_seq_copy.identical(int_seq)   
    
# @pytest.mark.parametrize("init_value", [0, 1.25, -1.25, 2, -2])  
# def test_two_interval_add_commutivity3(init_value):
    # ''' overlapping (non subset) interval adds'''
    # int_seq = stairs.Stairs(init_value)
    # int_seq_copy = int_seq.copy()
    # int_seq.layer(-2,1).layer(0,5,2)
    # int_seq_copy.layer(0,5,2).layer(-2,1)
    # assert int_seq.identical(int_seq_copy)
    # assert int_seq_copy.identical(int_seq)
    
# @pytest.mark.parametrize("init_value", [0, 1.25, -1.25, 2, -2])  
# def test_two_interval_add_commutivity4(init_value):
    # ''' overlapping (subset) interval adds'''
    # int_seq = stairs.Stairs(init_value)
    # int_seq_copy = int_seq.copy()
    # int_seq.layer(1,2).layer(0,5,2)
    # int_seq_copy.layer(0,5,2).layer(1,2)
    # assert int_seq.identical(int_seq_copy)
    # assert int_seq_copy.identical(int_seq)
    
# @pytest.mark.parametrize("init_value", [0, 1.25, -1.25, 2, -2])  
# def test_two_interval_add_integrate1(init_value):
    # ''' non-overlapping interval adds'''
    # int_seq = stairs.Stairs(init_value)
    # int_seq.layer(-2,1).layer(3,5,2)
    # assert int_seq.integarate)

    
# @pytest.mark.parametrize("init_value", [0, 1.25, -1.25, 2, -2])  
# def test_two_interval_add_integrate2(init_value):
    # ''' endpoint = startpoint interval adds'''
    # int_seq = stairs.Stairs(init_value)
    # int_seq.layer(-2,1).layer(1,5,2)
    # assert int_seq.identical(int_seq_copy)
    
# @pytest.mark.parametrize("init_value", [0, 1.25, -1.25, 2, -2])  
# def test_two_interval_add_integrate3(init_value):
    # ''' overlapping (non subset) interval adds'''
    # int_seq = stairs.Stairs(init_value)
    # int_seq.layer(-2,1).layer(0,5,2)
    # assert int_seq.identical(int_seq_copy)
    
# @pytest.mark.parametrize("init_value", [0, 1.25, -1.25, 2, -2])  
# def test_two_interval_add_integrate4(init_value):
    # ''' overlapping (subset) interval adds'''
    # int_seq = stairs.Stairs(init_value)
    # int_seq.layer(1,2).layer(0,5,2)
    # assert int_seq.identical(int_seq_copy)