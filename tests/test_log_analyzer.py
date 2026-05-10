import sys
from collections.abc import Callable
from pathlib import Path
from typing import assert_type

import pytest

from src.scripts.log_analyzer import (
    count_logs_by_level,
    filter_logs_by_level,
    load_logs,
    main,
    parse_log_line,
)


@pytest.fixture
def sample_logs_path() -> Path:
    return Path(__file__).parent.parent / "data" / "log_analyzer" / "sample-logs"


@pytest.fixture
def failing_logs_path() -> Path:
    return Path(__file__).parent.parent / "data" / "log_analyzer" / "failing-logs"


# region  load_logs


def test_load_logs_signature():
    assert_type(load_logs, Callable[[str], list])


@pytest.mark.parametrize("argument", [123, True, False, [1], {1: 1}, (1, 1)])
def test_load_logs_argument_is_not_a_string(argument):
    with pytest.raises(TypeError, match="not a str"):
        load_logs(argument)


def test_load_logs_file_not_found():
    with pytest.raises(FileNotFoundError, match="File not found"):
        load_logs("no_such_file.log")


def test_load_logs_file_is_not_a_file():
    with pytest.raises(FileNotFoundError, match="not a file"):
        load_logs(".")


def test_load_logs_no_permission_to_read_file(tmp_path: Path):
    file = tmp_path / "sample-logs"
    file.write_text("test", encoding="utf-8")
    file.chmod(0o000)
    with pytest.raises(PermissionError, match="Permission denied"):
        load_logs(file.absolute().as_posix())


def test_load_logs_success(sample_logs_path: Path):
    assert len(load_logs(sample_logs_path.as_posix())) == 10


# endregion load_logs


# region parse_log_line


def test_parse_log_line_signature():
    assert_type(parse_log_line, Callable[[str], dict])


@pytest.mark.parametrize("argument", [123, True, False, [1], {1: 1}, (1, 1)])
def test_parse_log_line_argument_is_not_a_string(argument):
    with pytest.raises(TypeError, match="not a str"):
        parse_log_line(argument)


@pytest.mark.parametrize(
    "line",
    [
        "",
        "   ",
        "2024/01/22 08:30:01 ERROR Date is all slashes",
        "2024-01/22 08:30:01 ERROR Date has last part as slash",
        "2024/01-22 08:30:01 ERROR Time has first part as slash",
        "2024-01-22 08:30:01AM ERROR Time has AM/PM as slash",
        "2024-01-22 08/30/01 ERROR TIME has all parts as slashes",
        "2024-01-22 08:30/01 ERROR Time has last part as slash",
        "2024-01-22 08/30:01 ERROR Time has first part as slash",
        "2024-01-22 08:30:01 OOGEY Has oogey.",
        "2024-01-22 08:30:01 error Has error not capitalized.",
    ],
)
def test_parse_log_line_invalid_lines(line):
    with pytest.raises(ValueError, match="Invalid log line"):
        parse_log_line(line)


@pytest.mark.parametrize(
    "line, expected",
    [
        (
            "2024-01-22 08:30:01 INFO User logged in successfully.",
            {
                "date": "2024-01-22",
                "time": "08:30:01",
                "level": "INFO",
                "message": "User logged in successfully.",
            },
        ),
        (
            "2024-01-22 08:30:01 ERROR Database connection failed.",
            {
                "date": "2024-01-22",
                "time": "08:30:01",
                "level": "ERROR",
                "message": "Database connection failed.",
            },
        ),
        (
            "2024-01-22 08:00:01 WARNING Disk usage above 80%.",
            {
                "date": "2024-01-22",
                "time": "08:00:01",
                "level": "WARNING",
                "message": "Disk usage above 80%.",
            },
        ),
        (
            "2024-01-22 8:00:01 DEBUG Starting data backup process.",
            {
                "date": "2024-01-22",
                "time": "08:00:01",
                "level": "DEBUG",
                "message": "Starting data backup process.",
            },
        ),
    ],
)
def test_parse_log_line_success(line, expected):
    assert parse_log_line(line) == expected


# endregion parse_log_line

# region filter_logs_by_level


def test_filter_logs_by_level_signature():
    assert_type(filter_logs_by_level, Callable[[list, str], list])


@pytest.mark.parametrize("argument", [123, True, False, "INFO", {1: 1}, (1, 1)])
def test_filter_logs_by_level_argument_is_not_a_string(argument):
    with pytest.raises(TypeError, match="not a list"):
        filter_logs_by_level(argument, "INFO")


@pytest.mark.parametrize(
    "argument", ["INFO", "Info", "info", "DEBUG", "WARNING", "ERROR"]
)
def test_filter_logs_by_level_argument_is_valid_level(argument):
    assert filter_logs_by_level([], argument) == []


def test_filter_logs_by_level_invalid_level():
    with pytest.raises(ValueError, match="Invalid log level"):
        filter_logs_by_level([], "INVALID")


SUCCESS_PARSED_LOGS = [
    {
        "date": "2024-01-22",
        "time": "08:30:01",
        "level": "INFO",
        "message": "User logged in successfully.",
    },
    {
        "date": "2024-01-22",
        "time": "08:30:01",
        "level": "DEBUG",
        "message": "Starting data backup process.",
    },
    {
        "date": "2024-01-22",
        "time": "08:30:01",
        "level": "WARNING",
        "message": "Disk usage above 80%.",
    },
    {
        "date": "2024-01-22",
        "time": "08:30:01",
        "level": "INFO",
        "message": "Database connection failed.",
    },
]


def test_filter_logs_by_level_success():
    assert (
        len(
            filter_logs_by_level(
                SUCCESS_PARSED_LOGS,
                "INFO",
            )
        )
        == 2
    )


# endregion filter_logs_by_level


# region count_logs_by_level


def test_count_logs_by_level_signature():
    assert_type(count_logs_by_level, Callable[[list], dict])


@pytest.mark.parametrize("argument", [123, True, False, "INFO", {1: 1}, (1, 1), None])
def test_count_logs_by_level_argument_is_not_a_list(argument):
    with pytest.raises(TypeError, match="not a list"):
        count_logs_by_level(argument)


def test_count_logs_by_level_empty():
    assert count_logs_by_level([]) == {
        "INFO": 0,
        "DEBUG": 0,
        "WARNING": 0,
        "ERROR": 0,
    }


def test_count_logs_by_level_success():
    assert count_logs_by_level(SUCCESS_PARSED_LOGS) == {
        "INFO": 2,
        "DEBUG": 1,
        "WARNING": 1,
        "ERROR": 0,
    }


# endregion count_logs_by_level


# region Integration Tests


def test_main_success_logs(
    monkeypatch: pytest.MonkeyPatch, capsys, sample_logs_path: Path
):
    monkeypatch.setattr(sys, "argv", ["log_analyzer.py", sample_logs_path.as_posix()])
    main()
    out = capsys.readouterr().out

    assert "Parsing logs..." in out
    assert "Log Counts" in out
    assert "INFO" in out
    assert "DEBUG" in out
    assert "WARNING" in out
    assert "ERROR" in out
    assert all(str(log_count) in out for log_count in range(1, 5))


def test_main_success_logs_with_level(
    monkeypatch: pytest.MonkeyPatch, capsys, sample_logs_path: Path
):
    monkeypatch.setattr(
        sys, "argv", ["log_analyzer.py", sample_logs_path.as_posix(), "INFO"]
    )
    main()
    out = capsys.readouterr().out

    assert "Parsing logs..." in out
    assert "Log Counts" in out
    assert "INFO" in out
    assert "DEBUG" in out
    assert "WARNING" in out
    assert "ERROR" in out
    assert all(str(log_count) in out for log_count in range(1, 5))
    with open(sample_logs_path.as_posix(), "r") as file:
        lines = file.readlines()
        for line in lines:
            if "INFO" in line:
                assert line in out
            else:
                assert line not in out


def test_main_failing_logs(
    monkeypatch: pytest.MonkeyPatch, capsys, failing_logs_path: Path
):
    monkeypatch.setattr(sys, "argv", ["log_analyzer.py", failing_logs_path.as_posix()])
    main()
    out = capsys.readouterr().out

    assert "Parsing logs..." in out
    assert "Log Counts" in out
    assert "INFO" in out
    assert "DEBUG" in out
    assert "WARNING" in out
    assert "ERROR" in out
    assert all(str(log_count) in out for log_count in [4, 3, 1, 0])


def test_main_failing_logs_with_level(
    monkeypatch: pytest.MonkeyPatch, capsys, failing_logs_path: Path
):
    monkeypatch.setattr(
        sys, "argv", ["log_analyzer.py", failing_logs_path.as_posix(), "ERROR"]
    )
    main()
    out = capsys.readouterr().out

    assert "Parsing logs..." in out
    assert "Log Counts" in out
    assert "INFO" in out
    assert "DEBUG" in out
    assert "WARNING" in out
    assert "ERROR" in out
    assert all(str(log_count) in out for log_count in [4, 3, 1, 0])

    with open(failing_logs_path.as_posix(), "r") as file:
        lines = file.readlines()
        after_0 = out.rfind("0")
        for line in lines:
            if "ERROR" in line:
                assert line not in out[after_0:]


# endregion Integration Tests
