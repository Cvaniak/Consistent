# Test above
def foo(): ...


def bar():  # tricky inline
    ...


# fox above
def fox(): ...


class A:  # class A inline
    # Comment above
    def __init__(self) -> None:
        pass  # Pass inline


# zys above
def zys(): ...
