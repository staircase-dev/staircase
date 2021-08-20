from staircase.core.ops import docstrings
from staircase.util._decorators import Appender

from .arithmetic import add, divide, multiply, subtract
from .logical import logical_and, logical_or, logical_xor


@Appender(docstrings.radd_docstring, join="\n", indents=1)
def radd(self, other):
    return add(other, self)


@Appender(docstrings.rdivide_docstring, join="\n", indents=1)
def rdivide(self, other):
    return divide(other, self)


@Appender(docstrings.rmultiply_docstring, join="\n", indents=1)
def rmultiply(self, other):
    return multiply(other, self)


@Appender(docstrings.rsubtract_docstring, join="\n", indents=1)
def rsubtract(self, other):
    return subtract(other, self)


@Appender(docstrings.logical_rand_docstring, join="\n", indents=1)
def logical_rand(self, other):
    return logical_and(other, self)


@Appender(docstrings.logical_ror_docstring, join="\n", indents=1)
def logical_ror(self, other):
    return logical_or(other, self)


@Appender(docstrings.logical_rxor_docstring, join="\n", indents=1)
def logical_rxor(self, other):
    return logical_xor(other, self)
