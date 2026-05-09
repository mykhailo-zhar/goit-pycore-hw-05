from collections.abc import Callable


def caching_fibonacci() -> Callable[[int], int]:
    fibonacci_cache = [0, 1, 1]

    def fibonacci(n: int) -> int:
        nonlocal fibonacci_cache

        if not isinstance(n, int):
            raise TypeError("n must be an integer")

        if n <= 0:
            return 0
        if n < len(fibonacci_cache):
            return fibonacci_cache[n]

        fibonacci_cache.append(fibonacci(n - 1) + fibonacci(n - 2))
        return fibonacci_cache[n]

    return fibonacci
