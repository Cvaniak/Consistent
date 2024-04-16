# Test above
def foo(): ...


def bar():  # tricky inline
    a = 10
    pass
    ...


def test():
    pass


# fox above
def fox(): ...


class A:  # class A inline
    # Comment above
    def __init__(self) -> None:
        pass  # Pass inline


# zys above
def zys(): ...
