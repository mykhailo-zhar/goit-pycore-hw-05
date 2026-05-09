from collections.abc import Callable

from src.fibonacci import caching_fibonacci
from src.sum_profit import generator_numbers, sum_profit


def print_fibonacci(fibonacci: Callable[[int], int], n: int):
    number = fibonacci(n)
    print(f"Fibonacci of {n} is {number}")


def main():
    fibonacci = caching_fibonacci()
    print("Task 1: Fibonacci")
    print_fibonacci(fibonacci, 100)
    print_fibonacci(fibonacci, 101)

    print("Task 2: Sum profits")
    text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}")


if __name__ == "__main__":
    main()
