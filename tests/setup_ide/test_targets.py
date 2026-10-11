"""Target behavior: what each setup-ide target installs."""

import pytest
from harness import install_files, make_project, run, snapshot


@pytest.mark.parametrize("target", ["claude", "cursor", "copilot", "agents"])
def test_targets_fresh(target, tmp_path, assert_snapshot):
    project, guide = make_project(tmp_path)
    result = run(guide, [target], cwd=project)
    assert_snapshot(f"test_targets_{target}_fresh", snapshot(project, [result]))


def _installed(workdir, target):
    project, guide = make_project(workdir)
    result = run(guide, [target], cwd=project)
    assert result.code == 0
    return install_files(project)


@pytest.mark.parametrize(
    ("alias", "reference"),
    [("codex", "agents"), ("openai", "agents"), ("CLAUDE", "claude")],
)
def test_targets_alias_matches_reference(alias, reference, tmp_path):
    # Fixed directory names: CLAUDE and claude collide on case-insensitive disks.
    assert _installed(tmp_path / "alias", alias) == _installed(
        tmp_path / "reference", reference
    )


def test_targets_run_from_subdirectory(tmp_path, assert_snapshot):
    project, guide = make_project(tmp_path)
    subdir = project / "src"
    subdir.mkdir()
    result = run(guide, ["claude"], cwd=subdir)
    assert not (subdir / ".claude").exists()
    assert_snapshot("test_targets_subdirectory", snapshot(project, [result]))


def test_targets_no_target(tmp_path, assert_snapshot):
    project, guide = make_project(tmp_path)
    result = run(guide, [], cwd=project)
    assert result.code == 1
    assert_snapshot("test_targets_no_target", snapshot(project, [result]))


def test_targets_unknown_target(tmp_path, assert_snapshot):
    project, guide = make_project(tmp_path)
    result = run(guide, ["vim"], cwd=project)
    assert result.code == 1
    assert_snapshot("test_targets_unknown_target", snapshot(project, [result]))
