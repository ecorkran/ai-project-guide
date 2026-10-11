"""Lint config checks: detection, report-only mode, and --write-lint.

The check runs after every target, so these use `agents`, which prints the least.
Written configs belong to the project: they are not in the manifest.
"""

import pytest
from harness import FIXTURE_GUIDE, make_project, run, snapshot, write_files

PYPROJECT_PLAIN = '[project]\nname = "demo"\n'
PYPROJECT_WITH_RUFF = '[project]\nname = "demo"\n\n[tool.ruff]\nline-length = 100\n'
RUFF_COMPLETE = '[lint]\nselect = ["E", "F", "W", "I", "UP", "BLE", "ASYNC", "B"]\n'
PYTHON_BASELINE = (FIXTURE_GUIDE / "lint/python/ruff.toml").read_text()


def _lint_run(tmp_path, files, *arg_sets, env_extra=None):
    """Arrange a project, run agents once per arg set: (project, guide, runs)."""
    project, guide = make_project(tmp_path)
    write_files(project, files)
    runs = [
        run(guide, ["agents", *args], cwd=project, env_extra=env_extra)
        for args in arg_sets
    ]
    return project, guide, runs


def test_lint_python_no_config_reports_only(tmp_path, assert_snapshot):
    files = {"pyproject.toml": PYPROJECT_PLAIN}
    project, _, runs = _lint_run(tmp_path, files, [])
    assert not (project / "ruff.toml").exists()
    assert "Lint (python)" in runs[0].stdout
    assert_snapshot("test_lint_python_report", snapshot(project, runs))


def test_lint_python_write_lint_writes_baseline(tmp_path, assert_snapshot):
    files = {"pyproject.toml": PYPROJECT_PLAIN}
    project, _, runs = _lint_run(tmp_path, files, ["--write-lint"])
    assert (project / "ruff.toml").read_text() == PYTHON_BASELINE
    assert_snapshot("test_lint_python_write", snapshot(project, runs))


def test_lint_python_weak_pyproject_gets_extending_ruff_toml(tmp_path, assert_snapshot):
    files = {"pyproject.toml": PYPROJECT_WITH_RUFF}
    project, _, runs = _lint_run(tmp_path, files, [], ["--write-lint"])
    ruff_toml = (project / "ruff.toml").read_text()
    assert 'extend = "pyproject.toml"' in ruff_toml
    assert "extend-select" in ruff_toml
    assert (project / "pyproject.toml").read_text() == PYPROJECT_WITH_RUFF
    assert_snapshot("test_lint_python_extend", snapshot(project, runs))


def test_lint_python_complete_config_no_report(tmp_path, assert_snapshot):
    files = {"pyproject.toml": PYPROJECT_PLAIN, "ruff.toml": RUFF_COMPLETE}
    project, _, runs = _lint_run(tmp_path, files, ["--write-lint"])
    assert "missing required rules" not in runs[0].stdout
    assert (project / "ruff.toml").read_text() == RUFF_COMPLETE
    assert_snapshot("test_lint_python_complete", snapshot(project, runs))


@pytest.mark.parametrize(
    ("language", "marker_file", "written"),
    [
        ("dart", "pubspec.yaml", "analysis_options.yaml"),
        ("typescript", "tsconfig.json", "eslint.config.mjs"),
    ],
)
def test_lint_report_then_write(
    language, marker_file, written, tmp_path, assert_snapshot
):
    project, _, runs = _lint_run(tmp_path, {marker_file: "{}\n"}, [], ["--write-lint"])
    assert f"Lint ({language})" in runs[0].stdout
    assert (project / written).exists()
    assert_snapshot(f"test_lint_{language}", snapshot(project, runs))


@pytest.mark.parametrize(
    ("depth", "detected"), [(3, True), (4, False)], ids=["depth3", "depth4"]
)
def test_lint_csharp_project_depth(depth, detected, tmp_path, assert_snapshot):
    levels = "/".join(["sub"] * (depth - 1))
    files = {f"{levels}/App.csproj": "<Project />\n"}
    project, _, runs = _lint_run(tmp_path, files, ["--write-lint"])
    assert ("Lint (csharp)" in runs[0].stdout) is detected
    assert (project / "Directory.Build.props").exists() is detected
    assert_snapshot(f"test_lint_csharp_depth{depth}", snapshot(project, runs))


def test_lint_excluded_language_not_checked(tmp_path, assert_snapshot):
    project, guide = make_project(tmp_path)
    # The fixture guide has no python.md, so add one for the exclusion to name.
    write_files(
        guide / "project-guides" / "rules",
        {
            "python.md": "---\ndescription: Fixture Python rule.\n"
            'paths:\n  - "**/*.py"\n---\n\n### Python\n'
        },
    )
    write_files(project, {"pyproject.toml": PYPROJECT_PLAIN})
    result = run(
        guide,
        ["agents", "--write-lint"],
        cwd=project,
        env_extra={"CONTEXT_FORGE_RULES_EXCLUDE": "python.md"},
    )
    assert "Lint (python)" not in result.stdout
    assert not (project / "ruff.toml").exists()
    assert_snapshot("test_lint_python_excluded", snapshot(project, [result]))
