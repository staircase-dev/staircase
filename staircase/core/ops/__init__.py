from staircase.core.ops.arithmetic import add, subtract, multiply, negate, divide
from staircase.core.ops.relational import eq, ne, lt, gt, le, ge, identical
from staircase.core.ops.logical import invert, logical_and, logical_or, make_boolean


def add_operations(cls):

    cls.negate = negate

    cls.add = add
    cls.subtract = subtract
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
    cls.make_boolean = make_boolean

    cls.__or__ = logical_or
    cls.__and__ = logical_and
    cls.__invert__ = invert

    cls.identical = identical
