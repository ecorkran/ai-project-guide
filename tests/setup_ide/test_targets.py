"""Target behavior: what each setup-ide target installs."""

from harness import make_project, run, snapshot


def test_targets_claude_fresh(tmp_path, assert_snapshot):
    project, guide = make_project(tmp_path)
    result = run(guide, ["claude"], cwd=project)
    assert_snapshot("test_targets_claude_fresh", snapshot(project, [result]))
