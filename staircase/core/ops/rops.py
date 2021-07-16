from .arithmetic import add, divide, multiply, subtract
from .logical import logical_and, logical_or, logical_xor


# TODO: docstring
# TODO: test
# TODO: what's new
def radd(self, other):
    return add(other, self)


# TODO: docstring
# TODO: test
# TODO: what's new
def rdivide(self, other):
    return divide(other, self)


# TODO: docstring
# TODO: test
# TODO: what's new
def rmultiply(self, other):
    return multiply(other, self)


# TODO: docstring
# TODO: test
# TODO: what's new
def rsubtract(self, other):
    return subtract(other, self)


# TODO: docstring
# TODO: test
# TODO: what's new
def rlogical_and(self, other):
    return logical_and(other, self)


# TODO: docstring
# TODO: test
# TODO: what's new
def rlogical_or(self, other):
    return logical_or(other, self)


# TODO: docstring
# TODO: test
# TODO: what's new
def rlogical_xor(self, other):
    return logical_xor(other, self)
