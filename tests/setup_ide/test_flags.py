"""Flag behavior: --capabilities, --dry-run, --root, flag order."""

import pytest
from harness import make_guide, make_project, run, snapshot, tree, write_files


def _project_tree(project):
    """Everything in the project except the guide folder."""
    return {
        rel: content
        for rel, content in tree(project).items()
        if not rel.startswith("project-documents/")
    }


def test_flags_capabilities(tmp_path):
    project, guide = make_project(tmp_path)
    result = run(guide, ["--capabilities"], cwd=project)
    # cf parses this exact line to decide which flags it may pass.
    assert result.stdout == "dry-run write-lint root\n"
    assert result.code == 0


def test_flags_dry_run_fresh(tmp_path, assert_snapshot):
    project, guide = make_project(tmp_path)
    before = _project_tree(project)
    result = run(guide, ["claude", "--dry-run"], cwd=project)
    assert _project_tree(project) == before
    assert_snapshot("test_flags_dry_run_fresh", snapshot(project, [result]))


def test_flags_dry_run_no_changes(tmp_path, assert_snapshot):
    project, guide = make_project(tmp_path)
    install = run(guide, ["claude"], cwd=project)
    before = _project_tree(project)
    result = run(guide, ["claude", "--dry-run"], cwd=project)
    assert _project_tree(project) == before
    assert_snapshot(
        "test_flags_dry_run_no_changes", snapshot(project, [install, result])
    )


def test_flags_dry_run_guide_changed(tmp_path, assert_snapshot):
    project, guide = make_project(tmp_path)
    install = run(guide, ["claude"], cwd=project)
    rules = guide / "project-guides" / "rules"
    write_files(
        rules,
        {
            "scoped-c.md": "---\ndescription: New scoped rule C.\n"
            'paths:\n  - "**/*.cc"\n---\n\n### Scoped C\n',
            "scoped-a.md": "---\ndescription: Edited scoped rule A.\n"
            'paths:\n  - "**/*.aa"\n---\n\n### Scoped A edited\n',
        },
    )
    (rules / "scoped-b.md").unlink()
    before = _project_tree(project)
    result = run(guide, ["claude", "--dry-run"], cwd=project)
    assert _project_tree(project) == before
    assert_snapshot(
        "test_flags_dry_run_guide_changed", snapshot(project, [install, result])
    )


@pytest.mark.parametrize("form", ["separate", "equals"])
def test_flags_root_outside_guide(form, tmp_path, assert_snapshot):
    guide = make_guide(tmp_path / "guide")
    target = tmp_path / "target"
    target.mkdir()
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    root_args = ["--root", str(target)] if form == "separate" else [f"--root={target}"]
    result = run(guide, ["claude", *root_args], cwd=elsewhere)
    assert not (elsewhere / ".claude").exists()
    assert_snapshot(f"test_flags_root_{form}", snapshot(target, [result]))


def test_flags_root_missing_directory(tmp_path, assert_snapshot):
    project, guide = make_project(tmp_path)
    missing = tmp_path / "does-not-exist"
    result = run(guide, ["claude", "--root", str(missing)], cwd=project)
    assert result.code == 1
    assert_snapshot("test_flags_root_missing_dir", snapshot(project, [result]))


def test_flags_root_without_value(tmp_path, assert_snapshot):
    project, guide = make_project(tmp_path)
    result = run(guide, ["claude", "--root"], cwd=project)
    assert result.code == 1
    assert_snapshot("test_flags_root_no_value", snapshot(project, [result]))


@pytest.mark.parametrize("flag", ["--dry-run", "--write-lint"])
def test_flags_before_target_same_as_after(flag, tmp_path):
    texts = []
    for name, args in (("before", [flag, "claude"]), ("after", ["claude", flag])):
        project, guide = make_project(tmp_path / name)
        texts.append(snapshot(project, [run(guide, args, cwd=project)]))
    # Snapshots differ only in the run label, which lists the args in order.
    before, after = (text.split("\n", 1)[1] for text in texts)
    assert before == after
