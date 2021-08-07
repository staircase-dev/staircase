from staircase.core.ops.arithmetic import add, divide, multiply, negate, subtract
from staircase.core.ops.logical import (
    invert,
    logical_and,
    logical_or,
    logical_xor,
    make_boolean,
)
from staircase.core.ops.masking import clip, fillna, isna, mask, notna, where
from staircase.core.ops.relational import eq, ge, gt, identical, le, lt, ne
from staircase.core.ops.rops import (
    logical_rand,
    logical_ror,
    logical_rxor,
    radd,
    rdivide,
    rmultiply,
    rsubtract,
)


def add_operations(cls):

    cls.negate = negate

    cls.add = add
    cls.subtract = subtract
    cls.clip = clip
    cls.mask = mask
    cls.where = where
    cls.isna = isna
    cls.notna = notna
    cls.fillna = fillna
    cls.multiply = multiply
    cls.divide = divide
    cls.eq = eq
    cls.ne = ne
    cls.lt = lt
    cls.gt = gt
    cls.le = le
    cls.ge = ge

    cls.__neg__ = negate
    cls.__add__ = add
    cls.__sub__ = subtract
    cls.__mul__ = multiply
    cls.__truediv__ = divide
    cls.__eq__ = eq
    cls.__ne__ = ne
    cls.__lt__ = lt
    cls.__gt__ = gt
    cls.__le__ = le
    cls.__ge__ = ge

    cls.invert = invert
    cls.logical_and = logical_and
    cls.logical_or = logical_or
    cls.logical_xor = logical_xor
    cls.make_boolean = make_boolean

    cls.__or__ = logical_or
    cls.__xor__ = logical_xor
    cls.__and__ = logical_and
    cls.__invert__ = invert

    cls.identical = identical

    cls.radd = radd
    cls.rdivide = rdivide
    cls.rmultiply = rmultiply
    cls.rsubtract = rsubtract
    cls.logical_rand = logical_rand
    cls.logical_ror = logical_ror
    cls.logical_rxor = logical_rxor

    cls.__radd__ = radd
    # cls.__rdiv__ = rdivide
    cls.__rtruediv__ = rdivide
    cls.__rmul__ = rmultiply
    cls.__rsub__ = rsubtract
    cls.__rand__ = logical_rand
    cls.__ror__ = logical_ror
    cls.__rxor__ = logical_rxor
