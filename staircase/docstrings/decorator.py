def add_doc(value):
    def _doc(func):
        func.__doc__ = value
        return func

    return _doc


def append_doc(value):
    def _doc(func):
        func.__doc__ = "\n\n".join([func.__doc__, value])
        return func

    return _doc
