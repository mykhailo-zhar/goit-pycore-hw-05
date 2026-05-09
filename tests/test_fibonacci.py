import time
from collections.abc import Callable
from typing import assert_type

import pytest

from src.fibonacci import caching_fibonacci


def _profiler(func: Callable[[int], int], n: int):
    start = time.perf_counter()
    result = func(n)
    end = time.perf_counter()
    return result, end - start


def test_caching_fibonacci_signature():
    assert_type(caching_fibonacci, Callable[[], Callable[[int], int]])


@pytest.mark.parametrize("n", [1.5, "1", None, True, False, [1], {1: 1}, (1, 1)])
def test_unforseentype_throws_error(n):
    with pytest.raises(TypeError):
        caching_fibonacci()(n)


@pytest.mark.parametrize(
    "n, expected",
    [
        (-15, 0),
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 2),
        (4, 3),
        (5, 5),
        (6, 8),
        (7, 13),
        (8, 21),
        (9, 34),
        (10, 55),
    ],
)
def test_caching_fibonacci_returns_correct_value(n, expected):
    assert caching_fibonacci()(n) == expected


def test_caching_fibonacci_does_caching():
    fibonacci = caching_fibonacci()
    _, time = _profiler(fibonacci, 100)
    _, time2 = _profiler(fibonacci, 101)
    assert time2 < time
