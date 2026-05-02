"""Tests for src.contacts_bot — parse_input, handlers, dispatch, and main loop."""

from __future__ import annotations

import builtins

import pytest

from src.scripts.contacts_bot import (
    add_contact,
    handle_command,
    main,
    parse_input,
    show_all,
    show_phone,
    update_contact,
)

_VALID_PHONE_12 = "123456789012"
_VALID_PHONE_15 = "123456789012345"

INVALID_COMMAND = "Invalid command."
CONTACT_ADDED = "Contact added."
CONTACT_UPDATED = "Contact updated."
NO_SUCH_USER = "No such user"
PLEASE_CHANGE_USER = "Please change the user"
GOOD_BYE = "Good bye!"


@pytest.mark.parametrize(
    "line,expected_cmd,expected_args",
    [
        ("hello", "hello", []),
        ("HELLO", "hello", []),
        ("Hello", "hello", []),
        ("  hello  ", "hello", []),
        (f"add Alice {_VALID_PHONE_12}", "add", ["Alice", _VALID_PHONE_12]),
        (f"aDd Bob {_VALID_PHONE_15}", "add", ["Bob", _VALID_PHONE_15]),
        (f"upDaTe carol {_VALID_PHONE_12}", "update", ["carol", _VALID_PHONE_12]),
        (f"UpDaTe dave {_VALID_PHONE_12}", "update", ["dave", _VALID_PHONE_12]),
        ("Phone Eve", "phone", ["Eve"]),
        ("PhOnE Frank", "phone", ["Frank"]),
        ("all", "all", []),
        ("ALL", "all", []),
        ("exIt", "exit", []),
        ("cLose", "close", []),
    ],
)
def test_parse_input_tokenization(line, expected_cmd, expected_args):
    cmd, args = parse_input(line)
    assert cmd == expected_cmd
    assert args == expected_args


@pytest.mark.parametrize(
    "line,expected_cmd,expected_args",
    [
        ("", "", []),
        ("   \t  ", "", []),
    ],
)
def test_parse_input_empty_and_blank(line, expected_cmd, expected_args):
    cmd, args = parse_input(line)
    assert cmd == expected_cmd
    assert args == expected_args


def test_add_contact_inserts_and_message():
    book: dict[str, str] = {}
    assert add_contact(book, ["Zoe", _VALID_PHONE_12]) == CONTACT_ADDED
    assert book == {"Zoe": _VALID_PHONE_12}


def test_add_contact_duplicate_asks_to_change():
    book = {"Ann": _VALID_PHONE_12}
    assert add_contact(book, ["Ann", _VALID_PHONE_15]) == PLEASE_CHANGE_USER
    assert book == {"Ann": _VALID_PHONE_12}, "Book should not be updated"


@pytest.mark.parametrize(
    "arguments,expected",
    [
        (["bad", "name", _VALID_PHONE_12], INVALID_COMMAND),
        (["bad name", "12345678901"], INVALID_COMMAND),
        (["Good", "+1234567890123456"], INVALID_COMMAND),
    ],
)
def test_add_contact_invalid_name_or_phone(arguments, expected):
    book: dict[str, str] = {}
    assert add_contact(book, arguments) == expected
    assert book == {}


@pytest.mark.parametrize(
    "arguments,expected",
    [
        (["Good", _VALID_PHONE_12], CONTACT_ADDED),
        (["Good", _VALID_PHONE_15], CONTACT_ADDED),
    ],
)
def test_add_valid_name_and_phone(arguments, expected):
    book: dict[str, str] = {}
    assert add_contact(book, arguments) == expected
    assert len(book) == 1


def test_change_contact_updates():
    book = {"Ann": _VALID_PHONE_12}
    assert update_contact(book, ["Ann", _VALID_PHONE_15]) == CONTACT_UPDATED
    assert book["Ann"] == _VALID_PHONE_15


def test_change_contact_no_such_user():
    book: dict[str, str] = {}
    assert update_contact(book, ["Nobody", _VALID_PHONE_12]) == NO_SUCH_USER
    assert book == {}


def test_change_contact_invalid_credentials():
    book = {"Ann": _VALID_PHONE_12}
    assert update_contact(book, ["Ann", "abcdefghijkl"]) == INVALID_COMMAND
    assert book["Ann"] == _VALID_PHONE_12


@pytest.mark.parametrize(
    "arguments,expected",
    [
        (["Ann"], _VALID_PHONE_12),
        (["Bob"], NO_SUCH_USER),
        (["no@pe"], INVALID_COMMAND),
        (["Ann", "123456789012"], INVALID_COMMAND),
    ],
)
def test_show_phone(arguments, expected):
    book = {"Ann": _VALID_PHONE_12}
    assert show_phone(book, arguments) == expected


def test_show_all_empty_and_sorted_lines():
    assert show_all({}) == "There are no users"
    book = {"Zed": _VALID_PHONE_15, "Amy": _VALID_PHONE_12}
    out = show_all(book)
    assert f"Stored users ({len(book)}):" in out
    assert all(f"{name}: {phone}" in out for name, phone in sorted(book.items()))


@pytest.mark.parametrize(
    "command,arguments,expected",
    [
        ("hello", [], "How can I help you?"),
        ("hello", ["extra"], INVALID_COMMAND),
        ("not_a_command", [], INVALID_COMMAND),
    ],
)
def test_handle_command_hello_and_unknown(command, arguments, expected):
    assert handle_command({}, command, arguments) == expected


def test_handle_command_add_and_update_via_dispatch():
    book: dict[str, str] = {}
    assert handle_command(book, "add", ["x", _VALID_PHONE_12]) == CONTACT_ADDED
    assert handle_command(book, "add", ["x", _VALID_PHONE_15]) == PLEASE_CHANGE_USER
    assert handle_command(book, "update", ["x", _VALID_PHONE_15]) == CONTACT_UPDATED
    assert book["x"] == _VALID_PHONE_15


def test_handle_command_wrong_arity():
    assert handle_command({}, "add", ["onlyone"]) == INVALID_COMMAND
    assert handle_command({}, "update", ["x"]) == INVALID_COMMAND
    assert handle_command({}, "phone", []) == INVALID_COMMAND
    assert handle_command({}, "all", ["extra"]) == INVALID_COMMAND


def test_handle_command_empty_line_invalid():
    assert handle_command({}, "", []) == "Invalid command."
    assert handle_command({}, "  ", []) == "Invalid command."


def test_handle_command_phone_no_user():
    assert handle_command({}, "phone", ["Ghost"]) == NO_SUCH_USER


def test_handle_command_update_no_user():
    assert handle_command({}, "update", ["Ghost", _VALID_PHONE_12]) == NO_SUCH_USER


def test_handle_command_exit_close_returns_none():
    book: dict[str, str] = {}
    assert handle_command(book, "exit", []) == GOOD_BYE
    assert handle_command(book, "close", []) == GOOD_BYE
    assert book == {}


def test_main_prints_replies_and_goodbye(monkeypatch, capsys):
    lines = iter(["hello", f"add Pat {_VALID_PHONE_12}", "exit"])

    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    main()
    out = capsys.readouterr().out
    assert "How can I help you?" in out
    assert "Contact added." in out
    assert "Good bye!" in out
