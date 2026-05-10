import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.table import Table


def load_logs(file_path: str) -> list:
    """
    Loads logs from a file.

    Args:
        file_path (str): The path to the file to load logs from.

    Raises:
        TypeError: If file_path is not a string.
        FileNotFoundError: If the file does not exist.
        FileNotFoundError: If the file is not a file.

    Returns:
        list: A list of logs from the file.
    """

    if not isinstance(file_path, str):
        raise TypeError("file_path is not a str")

    file_as_path = Path(file_path)

    if not file_as_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not file_as_path.is_file():
        raise FileNotFoundError(f"File is not a file: {file_path}")

    with open(file_as_path, "r") as file:
        return file.readlines()


DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TIME_PATTERN = re.compile(r"^\d{1,2}:\d{2}:\d{2}$([AP]M)?")
LOG_LEVELS = ["INFO", "DEBUG", "WARNING", "ERROR"]


def parse_log_line(line: str) -> dict:
    """
    Parses a log line into a dictionary.

    Args:
        line (str): The log line to parse.

    Raises:
        TypeError: If line is not a string.
        ValueError: If line is empty.
        ValueError: If line is not a valid log line.
        ValueError: If line is not a valid date and time.
        ValueError: If line is not a valid level.

    Returns:
        dict: A dictionary containing the parsed log line.
    """
    if not isinstance(line, str):
        raise TypeError("line is not a str")

    line = line.strip()
    if not line:
        raise ValueError("Invalid log line: empty line")

    parts = line.split()
    if len(parts) < 4:
        raise ValueError("Invalid log line: not enough parts")

    try:
        datetime_obj = datetime.strptime(" ".join(parts[0:2]), "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise ValueError("Invalid log line: invalid date and time")

    date = datetime_obj.strftime("%Y-%m-%d")
    time = datetime_obj.strftime("%H:%M:%S")

    level = parts[2]
    if level not in LOG_LEVELS:
        raise ValueError("Invalid log line: invalid level")

    message = " ".join(parts[3:])
    return {
        "date": date,
        "time": time,
        "level": level,
        "message": message,
    }


def filter_logs_by_level(logs: list, level: str) -> list:
    """
    Filters logs by level.

    Args:
        logs (list): The logs to filter.
        level (str): The level to filter by.

    Raises:
        TypeError: If logs is not a list.
        ValueError: If level is not a valid level.

    Returns:
        list: A list of logs filtered by level.
    """
    if not isinstance(logs, list):
        raise TypeError("logs is not a list")

    if level.upper() not in LOG_LEVELS:
        raise ValueError("Invalid log level")

    return list(filter(lambda log: log["level"].upper() == level.upper(), logs))


def count_logs_by_level(logs: list) -> dict:
    """
    Counts the number of logs by level.

    Args:
        logs (list): The logs to count.

    Raises:
        TypeError: If logs is not a list.

    Returns:
        dict: A dictionary containing the number of logs by level.
    """
    if not isinstance(logs, list):
        raise TypeError("logs is not a list")

    extracted_levels = [log["level"] for log in logs]
    counts = dict(Counter(extracted_levels).items())
    counts.update({level: 0 for level in LOG_LEVELS if level not in counts})

    return counts


def display_log_counts(counts: dict) -> None:
    """
    Displays the log counts in a rich table.

    Args:
        counts (dict): The counts to display.

    Returns:
        None: This function does not return anything.
    """
    table = Table(title="Log Counts")

    table.add_column("Level", justify="right", style="cyan", no_wrap=True)
    table.add_column("Count", style="magenta")

    for level, count in counts.items():
        table.add_row(level, f"{count:,}")

    console = Console()
    console.print(table)


def main():
    args = sys.argv[1:]
    if not args:
        raise ValueError("Usage: log_analyzer.py <log_file>")

    print("Parsing logs...\n\n")

    log_file = args[0]
    logs = load_logs(log_file)

    parsed_logs = []
    for log in logs:
        try:
            parsed_logs.append(parse_log_line(log))
        except ValueError as e:
            print(f"Error parsing log line: {e}")
            print(f"Line: {log}")
            continue

    filtered_logs = None
    if len(args) > 1:
        level = args[1]
        filtered_logs = filter_logs_by_level(parsed_logs, level)

    counts = count_logs_by_level(parsed_logs)
    display_log_counts(counts)

    if filtered_logs:
        for log in filtered_logs:
            print(" ".join(log.values()))


if __name__ == "__main__":
    main()
