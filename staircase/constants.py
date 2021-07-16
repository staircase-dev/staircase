class NegInf:
    def __init__(self):
        pass

    def __lt__(self, _):
        return True

    def __gt__(self, other):
        assert type(other) != Inf
        return False

    def __neg__(self):
        return inf

    def __str__(self):
        return "-inf"


class Inf:
    def __init__(self):
        pass

    def __gt__(self, other):
        assert type(other) != Inf
        return True

    def __lt__(self, other):
        assert type(other) != Inf
        return False

    def __neg__(self):
        return neginf

    def __str__(self):
        return "inf"


neginf = NegInf()
inf = Inf()
