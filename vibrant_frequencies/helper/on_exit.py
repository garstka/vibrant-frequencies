from contextlib import contextmanager
from typing import Callable


@contextmanager
def on_exit(fun: Callable[[], None]):
    try:
        yield
    finally:
        fun()
