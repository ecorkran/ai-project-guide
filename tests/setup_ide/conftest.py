"""Fixtures for the setup-ide suite: snapshot comparison and a stub `cf`."""

import difflib
from pathlib import Path
from typing import Callable

import pytest
from harness import stub_dir

SNAPSHOT_DIR = Path(__file__).resolve().parent / "snapshots"

CF_HELP_WITH_VALUE = "Usage: cf config get [--value] <key>\n"
CF_HELP_WITHOUT_VALUE = "Usage: cf config get <key>\n"


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--update-snapshots",
        action="store_true",
        default=False,
        help="Rewrite snapshot files from the current setup-ide output.",
    )


@pytest.fixture
def assert_snapshot(request: pytest.FixtureRequest) -> Callable[[str, str], None]:
    """assert_snapshot(name, text): compare with snapshots/<name>.snap.

    With --update-snapshots the file is written instead. A missing snapshot
    fails otherwise, so a new test can never pass by accident.
    """
    update = request.config.getoption("--update-snapshots")

    def check(name: str, text: str) -> None:
        path = SNAPSHOT_DIR / f"{name}.snap"
        if update:
            SNAPSHOT_DIR.mkdir(exist_ok=True)
            path.write_text(text, encoding="utf-8", newline="")
            return
        if not path.exists():
            pytest.fail(f"missing snapshot {path.name}; run with --update-snapshots")
        expected = path.read_text(encoding="utf-8")
        if text != expected:
            diff = difflib.unified_diff(
                expected.splitlines(),
                text.splitlines(),
                fromfile=f"{path.name} (stored)",
                tofile="actual",
                lineterm="",
            )
            pytest.fail("snapshot differs:\n" + "\n".join(diff))

    return check


@pytest.fixture
def cf_stub() -> Callable[..., None]:
    """cf_stub(guide, *, value="", exit_code=0, has_value_flag=True).

    Writes an executable `cf` into the guide's stub directory (first on PATH).
    `cf config get --help` prints help with or without `--value`. With the flag,
    `cf config get --value <key>` prints `value` and exits `exit_code`. Without
    it, `cf config get <key>` prints the older labeled form with a `Value:` line.
    """

    def install(
        guide: Path,
        *,
        value: str = "",
        exit_code: int = 0,
        has_value_flag: bool = True,
    ) -> None:
        help_text = CF_HELP_WITH_VALUE if has_value_flag else CF_HELP_WITHOUT_VALUE
        script = f"""#!/bin/bash
if [ "$1 $2" != "config get" ]; then exit 64; fi
shift 2
case "$1" in
  --help) printf '%s' '{help_text}'; exit 0 ;;
  --value) printf '%s\\n' '{value}'; exit {exit_code} ;;
  *) printf 'Key:     %s\\nValue:   %s\\nSource:  stub\\n' "$1" '{value}'
     exit {exit_code} ;;
esac
"""
        cf = stub_dir(guide) / "cf"
        cf.write_text(script)
        cf.chmod(0o755)

    return install
