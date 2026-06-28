---
description: Python coding standards and conventions. Use when writing, modifying, or reviewing .py files, pyproject.toml, or requirements files.
paths:
 - "**/*.py"
 - "**/pyproject.toml"
 - "**/requirements*.txt"
---

### Python Rules

#### General
* Target Python 3.12+ for production (stability & ecosystem compatibility).
* Note: Python 3.14+ is acceptable for isolated services needing specific features (e.g., free-threading), but verify ML library support first.
* When starting or auditing a Python project, verify the required tooling configuration blocks defined in this guide (ruff, pyright) are present in `pyproject.toml`. If missing, add them before proceeding with substantive work. Mechanical enforcement is what makes these rules real; prose without config is aspirational.

#### Typing & Validation
- Use built-in types: `list`, `dict`, `tuple`, not `List`, `Dict`, `Tuple`
- Use `|` for union types: `str | None` not `Optional[str]` or `Union[str, None]`
- Use `Self` (from `typing`) for return types of fluent methods/factories (3.11+).
- Type hint all function signatures and class attributes
- Use `@dataclass` for internal data transfer objects (DTOs) and configuration.
- Use `Pydantic` for all external boundaries (API inputs/outputs, file parsing, environment variables).
- Import Policy: Keep `from __future__ import annotations` for 3.12/3.13 projects to resolve forward references cleanly. (Remove only once strictly on 3.14+).

#### Code Style & Structure
- Follow PEP 8 with 88-character line length
- Formatter: Use `ruff` for both linting and formatting (replaces Black/Isort/Flake8 due to speed).
- Required ruff configuration: every project MUST have a `[tool.ruff.lint]` block in `pyproject.toml` selecting at minimum `["E", "F", "W", "I", "UP", "BLE", "ASYNC", "B"]`. `BLE` (blind-except) and `ASYNC` (async correctness) mechanically enforce the exception-handling and event-loop-discipline rules elsewhere in this guide. Copy-paste baseline:

    ```toml
    [tool.ruff]
    line-length = 88

    [tool.ruff.lint]
    select = ["E", "F", "W", "I", "UP", "BLE", "ASYNC", "B"]
    ```

- Use descriptive variable names; avoid single letters (except `x`, `i` in short loops/comprehensions).
- Prefer `f-strings` exclusively; avoid `.format()` or `%`.
- Use `pathlib` and its `Path` for all file/path operations, not `os.path.join` or similar
- One class per file for models/services; group related tiny utilities in `utils.py` or specific modules.

#### Functions & Error Handling
- Small, single-purpose functions (max 20 lines preferred)
- Use early returns (`guard clauses`) to flatten nesting.
- Explicit exception handling: catch specific exception types (`ValueError`, `KeyError`), never bare `except:` and never `except Exception: pass`. Every `try/except` must either (a) re-raise after logging at ERROR level via `logger.exception`, (b) handle a specific exception type with an inline comment justifying why swallowing is correct (e.g., `except ConnectionClosed: pass` for normal socket teardown), or (c) be a documented top-level handler at a process boundary. Swallowed exceptions are bugs by default; the `BLE` ruff rule set enforces this mechanically.
- Use `try/except` blocks narrowly around the specific line that might fail.
- Use context managers (`with`) for resource management (files, locks, connections).

#### Modern Python Patterns
- Use `match/case` for structural pattern matching (parsing dictionaries, complex conditions).
- Use `walrus operator (:=)` sparingly—only when it significantly reduces duplication.
- Comprehensions over `map`/`filter` when clear
- Use generator expressions `(x for x in y)` for large sequences to save memory.
- Use `itertools` for efficient looping and `functools.partial`/`reduce` where appropriate.
- Use `Enum` (specifically `StrEnum` in 3.11+) for constants/choices.

#### Testing & Quality
- Write tests alongside implementation
- Use `pytest` exclusively.
- Use `conftest.py` for shared fixtures; keep individual test files clean.
- Parametrize tests (`@pytest.mark.parametrize`) to cover edge cases.
- Mock external I/O boundaries; test internal logic with real data.
- Load-test tier (`tests/load/`): any code on the simulation, network, concurrency, or environment-layer paths requires at least one load test exercising a realistic configuration. Load tests assert on latency, throughput, or resource bounds — not just functional correctness. Unit and integration tests cannot catch event-loop starvation, contention, or budget overruns; load tests can. CI must gate load tests for slices touching these paths.
- Static Analysis: Strict `pyright` (preferred) or `mypy` — zero errors is a merge blocker, not a TODO. Required `[tool.pyright]` configuration:

    ```toml
    [tool.pyright]
    include = ["src", "tests"]
    pythonVersion = "3.12"
    typeCheckingMode = "strict"
    reportMissingImports = true
    reportMissingTypeStubs = false
    ```

    Test code is included in strict checking because bugs in tests can mask bugs in code. Adjust `pythonVersion` to match the project target.
- Docstrings for public APIs (Google or NumPy style)

#### Dependencies & Imports
* Package Manager: Use `uv` for all projects (replaces Poetry/Pipenv for speed and standard compliance).
- Pin direct dependencies in `pyproject.toml`.
- Group imports: Standard Lib -> Third Party -> Local Application.
- Use absolute imports (`from myapp.services import ...`) over relative (`from ..services import ...`).
- No wildcard imports (`from module import *`).

#### Async & Performance
- Use `async`/`await` for I/O-bound operations (DB, API calls).
- Use `asyncio.TaskGroup` (3.11+) for safer concurrent task management.
- Profile before optimizing (use `py-spy` or `cProfile`).
- Use `functools.cache` or `lru_cache` for expensive pure functions.
- Any async def function that calls synchronous code must guarantee that the synchronous code runs in <1ms in the worst case. Anything CPU-bound must use run_in_executor, a dedicated thread, or a subprocess. Violating this blocks ALL I/O on the loop. Reviewers MUST verify this for any code that runs inside await-able functions.

#### Concurrency & Shared State
- Identify every access to shared mutable state. No read-during-mutate races between coroutines or between coroutines and executor threads.
- When state is published across thread or process boundaries, document the publication mechanism (`asyncio.Event`, sequence number, lock-free buffer, queue, etc.). Implicit publication via attribute assignment is not acceptable across boundaries.
- Introducing an executor (`run_in_executor`, `ProcessPoolExecutor`, threads) requires explicit review of every piece of state the executed code touches.

#### Security & Best Practices
- Secrets: Never commit secrets. Use `.env` files (loaded via `pydantic-settings`).
- Input: Validate everything entering the system via Pydantic.
- SQL: Always use parameterized queries (never f-string SQL).
- Randomness: Use `secrets` module for security tokens, `random` only for simulations.
