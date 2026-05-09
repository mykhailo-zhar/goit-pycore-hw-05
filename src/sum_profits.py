import re
from collections.abc import Callable, Generator
from decimal import Decimal


def generator_numbers(text: str) -> Generator[Decimal, None, None]:
    """
    A generator that yields the numbers in the text

    Args:
        text (str): The text to extract the numbers from

    Raises:
        TypeError: text must be a string

    Yields:
        Generator[Decimal, None, None]: The numbers in the text
    """

    if not isinstance(text, str):
        raise TypeError("text must be a string")

    regex = re.compile(r"(^| )(\d*)(\.\d+)?($| )")
    for number in re.finditer(regex, text):
        yield Decimal(number.group().strip())


def sum_profits(text: str, func: Callable[[str], Decimal]) -> Decimal:
    """
    A function that sums the numbers in the text

    Args:
        text (str): The text to extract the numbers from
        func (Callable[[str], Decimal]): A function that extracts the numbers from the text

    Raises:
        TypeError: text must be a string
        TypeError: func must be a callable

    Returns:
        Decimal: The sum of the numbers in the text
    """

    if not isinstance(text, str):
        raise TypeError("text must be a string")

    if not callable(func):
        raise TypeError("func must be a callable")

    return sum(func(text))
