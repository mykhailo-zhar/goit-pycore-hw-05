# goit-pycore-hw-05

GoIT **Python Core** homework: closures and generators, log parsing, a small contacts CLI, and tests.

## Tasks and results

**Task 1 — Fibonacci with cache**  
Factory [`caching_fibonacci()`](src/fibonacci.py) returns a function that computes the **n**th Fibonacci number and **reuses a growing cache**. Demos run from [`main.py`](main.py) for indices 100 and 101.

**Task 2 — Sum profits from text**  
[`generator_numbers`](src/sum_profit.py) yields numeric tokens from prose as `Decimal`; [`sum_profit`](src/sum_profit.py) sums them via a caller-supplied extractor. Demo text and call live in [`main.py`](main.py).

**Log analyzer (CLI)**  
[`src/scripts/log_analyzer.py`](src/scripts/log_analyzer.py): loads a log file, parses lines into structured dicts, **counts entries by level**, prints a **`rich` table**, and optionally filters and prints lines for a given level. Usage: `python src/scripts/log_analyzer.py <log_file> [LEVEL]`.

**Contacts assistant (CLI)**  
Interactive-style bot in [`src/scripts/contacts_bot.py`](src/scripts/contacts_bot.py): `parse_input()`, `hello`, `add`, **`update`** (change phone), `phone`, `all`, `exit` / `close`, and a **`main()`** read–eval loop; the in-memory book is `dict` (name → phone). Name and phone rules use [`src/validations.py`](src/validations.py).

## Tests and docs

- **Tests**: `pytest` under [`tests/`](tests/) (Fibonacci, sum profits, log analyzer, contacts bot).
- **API docs**: Sphinx—generate stubs with `mise run gd` (or `sphinx-apidoc`), build HTML with `mise run bd`; output in `docs/build/`.

## Quick commands

```bash
uv sync
pytest
python main.py
```

To try the CLIs:

```bash
python src/scripts/contacts_bot.py
python src/scripts/log_analyzer.py data/log_analyzer/sample-logs
```
