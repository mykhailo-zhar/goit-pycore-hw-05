from src.fibonacci import caching_fibonacci


def print_fibonacci(n: int):
    fibonacci = caching_fibonacci()
    number = fibonacci(n)
    print(f"Fibonacci of {n} is {number}")


def main():
    fibonacci = caching_fibonacci()
    print("Task 1: Fibonacci")
    print_fibonacci(100)
    print_fibonacci(101)


if __name__ == "__main__":
    main()
