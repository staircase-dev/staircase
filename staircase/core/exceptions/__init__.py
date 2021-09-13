"""
General exceptions
"""


class ClosedMismatchError(ValueError):
    def __init__(self, stairs1, stairs2):
        """
        Create a `ClosedMismatchError` indicating that `stairs1` and
        `stairs2` were supposed to have the same `clased` values but didn't.
        """
        super().__init__(
            f"`closed` values must be same but were {stairs1._closed} and {stairs2._closed}"
        )
