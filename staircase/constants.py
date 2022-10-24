from __future__ import annotations


class NegInf:
    def __init__(self):
        pass

    def __lt__(self, other) -> bool:
        assert not isinstance(other, NegInf)
        return True

    def __gt__(self, other) -> bool:
        assert not isinstance(other, (Inf, NegInf))
        return False

    def __neg__(self) -> Inf:
        return inf

    def __str__(self) -> str:
        return "-inf"


class Inf:
    def __init__(self):
        pass

    def __gt__(self, other) -> bool:
        assert not isinstance(other, Inf)
        return True

    def __lt__(self, other) -> bool:
        assert not isinstance(other, (Inf, NegInf))
        return False

    def __neg__(self) -> NegInf:
        return neginf

    def __str__(self) -> str:
        return "inf"


neginf = NegInf()
inf = Inf()
