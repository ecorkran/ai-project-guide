"""Ownership: the manifest decides which files setup-ide may overwrite or delete.

These protect users' files. A regression here clobbers or deletes project files.
"""

import shutil
from pathlib import Path

from harness import install_files, make_project, run, snapshot, write_files

ANALYZE_SKILL = Path(__file__).parent / "fixture_data" / "analyze-SKILL.md"
MANIFEST = ".context-forge/claude.manifest"
SCOPED_A = ".claude/rules/scoped-a.md"
SCOPED_B = ".claude/rules/scoped-b.md"


def _installed(tmp_path):
    """A project with claude installed once: (project, guide, first run)."""
    project, guide = make_project(tmp_path)
    return project, guide, run(guide, ["claude"], cwd=project)


def _guide_rule(guide, name):
    return guide / "project-guides" / "rules" / name


def test_ownership_run_twice_identical(tmp_path, assert_snapshot):
    project, guide, first = _installed(tmp_path)
    after_first = install_files(project)
    second = run(guide, ["claude"], cwd=project)
    assert install_files(project) == after_first
    assert_snapshot("test_ownership_run_twice", snapshot(project, [first, second]))


def test_ownership_no_manifest_differing_file_skipped(tmp_path, assert_snapshot):
    project, guide = make_project(tmp_path)
    write_files(project, {SCOPED_A: "my customized copy\n"})
    result = run(guide, ["claude"], cwd=project)
    assert (project / SCOPED_A).read_text() == "my customized copy\n"
    assert_snapshot("test_ownership_no_manifest_differing", snapshot(project, [result]))


def test_ownership_no_manifest_identical_file_adopted(tmp_path, assert_snapshot):
    project, guide, first = _installed(tmp_path)
    (project / MANIFEST).unlink()
    second = run(guide, ["claude"], cwd=project)
    assert SCOPED_A in (project / MANIFEST).read_text()
    assert_snapshot(
        "test_ownership_no_manifest_identical", snapshot(project, [first, second])
    )


def test_ownership_unlisted_differing_file_skipped(tmp_path, assert_snapshot):
    project, guide, first = _installed(tmp_path)
    # A rule the guide gains after the install, with a same-named project file.
    shutil.copy(_guide_rule(guide, "scoped-a.md"), _guide_rule(guide, "scoped-c.md"))
    write_files(project, {".claude/rules/scoped-c.md": "project's own scoped-c\n"})
    second = run(guide, ["claude"], cwd=project)
    assert (project / ".claude/rules/scoped-c.md").read_text() == (
        "project's own scoped-c\n"
    )
    assert ".claude/rules/scoped-c.md" not in (project / MANIFEST).read_text()
    assert_snapshot(
        "test_ownership_unlisted_differing", snapshot(project, [first, second])
    )


def test_ownership_edited_file_kept(tmp_path, assert_snapshot):
    project, guide, first = _installed(tmp_path)
    manifest_before = (project / MANIFEST).read_bytes()
    write_files(project, {SCOPED_A: "edited after install\n"})
    second = run(guide, ["claude"], cwd=project)
    assert (project / SCOPED_A).read_text() == "edited after install\n"
    # The original manifest line is carried over, so the path stays guide-owned.
    assert (project / MANIFEST).read_bytes() == manifest_before
    assert_snapshot("test_ownership_edited_kept", snapshot(project, [first, second]))


def test_ownership_dropped_rule_removed(tmp_path, assert_snapshot):
    project, guide, first = _installed(tmp_path)
    _guide_rule(guide, "scoped-b.md").unlink()
    second = run(guide, ["claude"], cwd=project)
    assert not (project / SCOPED_B).exists()
    assert_snapshot(
        "test_ownership_dropped_removed", snapshot(project, [first, second])
    )


def test_ownership_dropped_skill_removes_empty_folder(tmp_path, assert_snapshot):
    project, guide, first = _installed(tmp_path)
    shutil.rmtree(guide / "project-guides" / "skills" / "skill-a")
    second = run(guide, ["claude"], cwd=project)
    assert not (project / ".claude/skills/skill-a").exists()
    assert (project / ".claude/skills").is_dir()
    assert_snapshot(
        "test_ownership_dropped_skill_folder", snapshot(project, [first, second])
    )


def test_ownership_dropped_rule_edited_kept(tmp_path, assert_snapshot):
    project, guide, first = _installed(tmp_path)
    write_files(project, {SCOPED_B: "edited before the guide dropped it\n"})
    _guide_rule(guide, "scoped-b.md").unlink()
    second = run(guide, ["claude"], cwd=project)
    assert (project / SCOPED_B).read_text() == "edited before the guide dropped it\n"
    assert_snapshot(
        "test_ownership_dropped_edited_kept", snapshot(project, [first, second])
    )


def test_ownership_legacy_analyze_skill_removed(tmp_path, assert_snapshot):
    project, guide = make_project(tmp_path)
    legacy = ".claude/skills/analyze/SKILL.md"
    write_files(project, {legacy: ANALYZE_SKILL.read_bytes()})
    result = run(guide, ["claude"], cwd=project)
    assert not (project / legacy).exists()
    assert_snapshot("test_ownership_legacy_removed", snapshot(project, [result]))


def test_ownership_legacy_analyze_skill_edited_kept(tmp_path, assert_snapshot):
    project, guide = make_project(tmp_path)
    legacy = ".claude/skills/analyze/SKILL.md"
    write_files(project, {legacy: ANALYZE_SKILL.read_bytes() + b"my addition\n"})
    result = run(guide, ["claude"], cwd=project)
    assert (project / legacy).read_bytes().endswith(b"my addition\n")
    assert_snapshot("test_ownership_legacy_kept", snapshot(project, [result]))
