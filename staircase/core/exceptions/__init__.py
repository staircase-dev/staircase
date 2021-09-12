class DifferentClosedValuesError(ValueError):
    def __init__(self, stairs1, stairs2):
        super().__init__(
            f"`closed` values must be same but were {stairs1._closed} and {stairs2._closed}"
        )
