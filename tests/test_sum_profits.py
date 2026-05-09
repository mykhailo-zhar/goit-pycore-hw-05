from collections.abc import Callable, Generator
from decimal import Decimal
from typing import assert_type

import pytest

from src.sum_profit import generator_numbers, sum_profit


def test_generator_numbers_signature():
    """
    Test the signature of the generator_numbers function
    """
    assert_type(generator_numbers, Callable[[str], Generator[Decimal, None, None]])


@pytest.mark.parametrize("text", [1, 1.5, True, False, [1], {1: 1}, (1, 1)])
def test_generator_numbers_throws_error(text):
    """
    Test that the generator_numbers function raises a TypeError if the input is not a string

    Args:
        text (str): The text to extract the numbers from
    """
    with pytest.raises(TypeError):
        list(generator_numbers(text))


@pytest.mark.parametrize("func", [1, 1.5, True, False, [1], {1: 1}, (1, 1)])
def test_sum_profits_func_throws_error(func):
    """
    Test that the sum_profits function raises a TypeError if the input is not a callable

    Args:
        func (Callable[[str], Decimal]): A function that extracts the numbers from the text
    """
    with pytest.raises(TypeError):
        sum_profit("Company A: $100, Company B: $200, Company C: $300", func)


@pytest.mark.parametrize("text", [1, 1.5, True, False, [1], {1: 1}, (1, 1)])
def test_sum_profits_text_throws_error(text):
    """
    Test that the sum_profits function raises a TypeError if the input is not a string

    Args:
        text (str): The text to extract the numbers from
    """
    with pytest.raises(TypeError):
        sum_profit(text, generator_numbers)


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Company A: $100, Company B: $200, Company C: $300", []),
        (
            "Company A: $ 100 , Company B: $ 200 , Company C: $ 300",
            [Decimal("100"), Decimal("200"), Decimal("300")],
        ),
        ("300.0 bucks is not 300,00 dollars", [Decimal("300.0")]),
        (
            "100.04 lol 1.04 , .03 not so funny 1.35",
            [Decimal("100.04"), Decimal("1.04"), Decimal("0.03"), Decimal("1.35")],
        ),
    ],
)
def test_generator_numbers_returns_correct_value(text, expected):
    """
    Test that the generator_numbers function returns the correct value for the given input

    Args:
        text (str): The text to extract the numbers from
        expected (list[Decimal]): The expected result
    """
    assert list(generator_numbers(text)) == expected


def test_sum_profit_signature():
    """
    Test the signature of the sum_profits function
    """
    assert_type(sum_profit, Callable[[str, Callable[[str], Decimal]], Decimal])


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Company A: $100, Company B: $200, Company C: $300", Decimal("0")),
        ("Company A: $100 , Company B: $200 , Company C: $ 300", Decimal("300")),
        ("300.0 bucks is not 300,00 dollars", Decimal("300.0")),
        ("100.04 lol .03 not so funny 1.35", Decimal("101.42")),
    ],
)
def test_sum_profit_returns_correct_value(text, expected):
    """
    Test that the sum_profits function returns the correct value for the given input

    Args:
        text (str): The text to extract the numbers from
        expected (Decimal): The expected result
    """
    assert sum_profit(text, generator_numbers) == expected
