import re


def validate_name(name: str, no_spaces: bool = False) -> bool:
    """
    Validate the name of a living being.

    Args:
        name (str): The name of a living being.
        no_spaces (bool, optional): Whether to allow spaces in the name. Defaults to False.
    Returns:
        bool: True if the name is valid, False otherwise.
    """
    if no_spaces:
        return re.match(r"^[\w]+$", name) is not None

    # Checks whether the name consists of letters, spaces and digits
    return re.match(r"^[\w\s]+$", name) is not None


def validate_phone(phone: str) -> bool:
    """
    Validate the phone number of a living being.

    Args:
        phone (str): The phone number of a living being.
    """
    return re.match(r"^\d+$", phone) is not None


def validate_positive_integer(integer: str) -> bool:
    """
    Validate a positive integer.

    Args:
        integer (str): A string representing a positive integer.

    Returns:
        bool: True if the string is a positive integer, False otherwise.
    """

    # Checks whether the integer is a positive integer
    return re.match(r"^\d+$", integer) is not None and int(integer) > 0
