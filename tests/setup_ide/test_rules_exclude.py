"""rules.exclude: where the exclusion list comes from, and what it removes.

setup-ide asks, in order: the CONTEXT_FORGE_RULES_EXCLUDE env var, then `cf`
(new form with --value, or the older labeled `Value:` form). `cf` is always a
stub script from the cf_stub fixture, never the real one.
"""

import pytest
from harness import make_project, run, snapshot

SCOPED_A = ".claude/rules/scoped-a.md"
SCOPED_B = ".claude/rules/scoped-b.md"
ENV = "CONTEXT_FORGE_RULES_EXCLUDE"


def test_rules_exclude_env_wins_over_cf(tmp_path, cf_stub, assert_snapshot):
    project, guide = make_project(tmp_path)
    cf_stub(guide, value="scoped-a.md")
    result = run(guide, ["claude"], cwd=project, env_extra={ENV: "scoped-b.md"})
    assert (project / SCOPED_A).exists()
    assert not (project / SCOPED_B).exists()
    assert_snapshot("test_rules_exclude_env_wins", snapshot(project, [result]))


def test_rules_exclude_cf_value_flag(tmp_path, cf_stub, assert_snapshot):
    project, guide = make_project(tmp_path)
    cf_stub(guide, value="scoped-b.md")
    result = run(guide, ["claude"], cwd=project)
    assert (project / SCOPED_A).exists()
    assert not (project / SCOPED_B).exists()
    assert_snapshot("test_rules_exclude_cf_value", snapshot(project, [result]))


def test_rules_exclude_cf_unknown_key_excludes_nothing(
    tmp_path, cf_stub, assert_snapshot
):
    project, guide = make_project(tmp_path)
    cf_stub(guide, value="scoped-b.md", exit_code=2)
    result = run(guide, ["claude"], cwd=project)
    assert result.code == 0
    assert (project / SCOPED_B).exists()
    assert_snapshot("test_rules_exclude_cf_exit2", snapshot(project, [result]))


def test_rules_exclude_cf_failure_stops_setup(tmp_path, cf_stub, assert_snapshot):
    project, guide = make_project(tmp_path)
    cf_stub(guide, value="scoped-b.md", exit_code=1)
    result = run(guide, ["claude"], cwd=project)
    assert result.code == 1
    assert_snapshot("test_rules_exclude_cf_exit1", snapshot(project, [result]))


def test_rules_exclude_old_cf_labeled_value(tmp_path, cf_stub, assert_snapshot):
    project, guide = make_project(tmp_path)
    cf_stub(guide, value="scoped-b.md", has_value_flag=False)
    result = run(guide, ["claude"], cwd=project)
    assert (project / SCOPED_A).exists()
    assert not (project / SCOPED_B).exists()
    assert_snapshot("test_rules_exclude_old_cf", snapshot(project, [result]))


def test_rules_exclude_no_cf_on_path(tmp_path, assert_snapshot):
    project, guide = make_project(tmp_path)
    result = run(guide, ["claude"], cwd=project)
    assert (project / SCOPED_B).exists()
    assert_snapshot("test_rules_exclude_no_cf", snapshot(project, [result]))


@pytest.mark.parametrize(
    ("case", "pattern"),
    [("unmatched", "nomatch*.md"), ("always_on", "always-a.md")],
)
def test_rules_exclude_pattern_warnings(case, pattern, tmp_path, assert_snapshot):
    project, guide = make_project(tmp_path)
    result = run(guide, ["claude"], cwd=project, env_extra={ENV: pattern})
    assert_snapshot(f"test_rules_exclude_{case}", snapshot(project, [result]))


def test_rules_exclude_prunes_installed_rule(tmp_path, cf_stub, assert_snapshot):
    project, guide = make_project(tmp_path)
    first = run(guide, ["claude"], cwd=project)
    assert (project / SCOPED_B).exists()
    cf_stub(guide, value="scoped-b.md")
    second = run(guide, ["claude"], cwd=project)
    assert not (project / SCOPED_B).exists()
    assert_snapshot("test_rules_exclude_prunes", snapshot(project, [first, second]))
