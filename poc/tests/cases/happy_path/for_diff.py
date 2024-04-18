# Test above
def foo(): ...


def bar():  # tricky inline
    a = 10
    pass
    ...


# this will be abandoned
def this_will_be_abandoned():
    pass


# fox above
def fox(): ...


class A:  # class A inline
    # Comment above
    def __init__(self) -> None:
        pass  # Pass inline


# zys above
def zys(): ...
