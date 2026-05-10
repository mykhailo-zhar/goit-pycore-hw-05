import sys
from pathlib import Path

if __name__ == "__main__":
    sys.path.append(str(Path(__file__).parent.parent.parent.absolute()))


from src.validations import validate_name, validate_phone

INVALID_COMMAND = "Invalid command."


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, TypeError, IndexError) as e:
            return str(e)

    return wrapper


def parse_input(line: str) -> tuple[str, list[str]]:
    """
    Parse the input.

    Args:
        line (str): The line to parse.

    Returns:
        tuple[str, list[str]]: A tuple containing the command and the arguments.
    """
    if line.strip() == "":
        return "", []
    arguments = line.split()
    return arguments[0].lower(), arguments[1:]


@input_error
def hello(arguments: list[str] = []) -> str:
    """
    Print the hello message.

    Args:
        arguments (list[str]): The arguments to the hello command.

    Returns:
        str: The hello message.
    """
    if arguments:
        return INVALID_COMMAND

    return "How can I help you?"


@input_error
def add_contact(book: dict[str, str], arguments: list[str]) -> str:
    """
    Add a new contact.

    Args:
        book (dict[str, str]): The book of contacts.
        arguments (list[str]): The arguments to add the contact.

    Returns:
        str: The response to the command.
    """
    if len(arguments) != 2:
        return INVALID_COMMAND
    name, phone = arguments
    if not validate_name(name, no_spaces=True):
        return INVALID_COMMAND
    if not validate_phone(phone):
        return INVALID_COMMAND
    if name in book:
        return "Please change the user"
    book.update({name: phone})
    return "Contact added."


@input_error
def update_contact(book: dict[str, str], arguments: list[str]) -> str:
    """
    Update a contact.

    Args:
        book (dict[str, str]): The book of contacts.
        arguments (list[str]): The arguments to update the contact.

    Returns:
        str: The response to the command.
    """
    if len(arguments) != 2:
        return INVALID_COMMAND
    name, phone = arguments
    if not validate_name(name, no_spaces=True):
        return INVALID_COMMAND
    if not validate_phone(phone):
        return INVALID_COMMAND
    if name not in book:
        return "No such user"
    book.update({name: phone})
    return "Contact updated."


@input_error
def show_phone(book: dict[str, str], arguments: list[str]) -> str:
    """
    Show the phone number of a contact.

    Args:
        book (dict[str, str]): The book of contacts.
        arguments (list[str]): The arguments to show the phone number of the contact.

    Returns:
        str: The response to the command.
    """
    if len(arguments) != 1:
        return INVALID_COMMAND
    name = arguments[0]
    if not validate_name(name, no_spaces=True):
        return INVALID_COMMAND

    return book.get(name, "No such user")


@input_error
def show_all(book: dict[str, str], arguments: list[str] = []) -> str:
    """
    Show all contacts.

    Args:
        book (dict[str, str]): The book of contacts.
        arguments (list[str]): The arguments to show all contacts.

    Returns:
        str: The response to the command.
    """
    if arguments:
        return INVALID_COMMAND
    if not book:
        return "There are no users"

    return f"Stored users ({len(book)}):\n{'\n'.join(f'{name}: {phone}' for name, phone in sorted(book.items()))}"


@input_error
def exit(arguments: list[str] = []) -> str:
    """
    Exit the program.

    Args:
        arguments (list[str], optional): The arguments to the exit command. Defaults to [].

    Returns:
        str: The goodbye message.
    """
    if arguments:
        return INVALID_COMMAND
    return "Good bye!"


def handle_command(book: dict[str, str], command: str, arguments: list[str]) -> str:
    """
    Handle the command.

    Args:
        command (str): The command to handle.
        arguments (list[str]): The arguments to the command.
        book (dict[str, str]): The book of contacts.

    Returns:
        str: The response to the command.
    """

    match command:
        case "hello":
            return hello(arguments)
        case "add":
            return add_contact(book, arguments)
        case "update":
            return update_contact(book, arguments)
        case "phone":
            return show_phone(book, arguments)
        case "all":
            return show_all(book, arguments)
        case "exit":
            return exit(arguments)
        case "close":
            return exit(arguments)
        case _:
            return INVALID_COMMAND


def main() -> None:
    """
    Main function.
    """
    book: dict[str, str] = {}
    while True:
        line = input()
        command, arguments = parse_input(line)
        response = handle_command(book, command, arguments)
        print(response)
        if command in ["exit", "close"]:
            break


if __name__ == "__main__":
    main()
