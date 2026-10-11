"""Managed sections: how setup-ide merges its block into CLAUDE.md / AGENTS.md.

Bytes outside the managed block belong to the project and must pass through
untouched. Marker text is repeated here on purpose: the markers are a contract
with files already in users' projects.
"""

import pytest
from harness import make_project, run, snapshot, write_files

BEGIN = "<!-- BEGIN:context-forge -->"
END = "<!-- END:context-forge -->"
LEGACY = "[//]: # (context-forge:managed)"
LEGACY_END = "[//]: # (context-forge:managed end)"

# (target, file, the H1 the generated block starts with)
TARGETS = pytest.mark.parametrize(
    ("target", "filename", "h1"),
    [
        ("claude", "CLAUDE.md", "# Project Guidelines for Claude"),
        ("agents", "AGENTS.md", "# Project Guidelines"),
    ],
    ids=["claude", "agents"],
)


def _name(base, target):
    return f"test_managed_{base}_{target}"


@TARGETS
def test_managed_file_absent(target, filename, h1, tmp_path, assert_snapshot):
    project, guide = make_project(tmp_path)
    result = run(guide, [target], cwd=project)
    text = (project / filename).read_text()
    assert text.startswith(BEGIN + "\n" + h1 + "\n")
    assert_snapshot(_name("absent", target), snapshot(project, [result]))


@TARGETS
def test_managed_no_markers_backed_up(target, filename, h1, tmp_path, assert_snapshot):
    project, guide = make_project(tmp_path)
    original = b"# My Notes\n\nhand-written guidance\n"
    write_files(project, {filename: original})
    result = run(guide, [target], cwd=project)
    backup = project / (filename + ".pre-context-forge")
    assert backup.read_bytes() == original
    assert (project / filename).read_bytes().startswith(original)
    assert_snapshot(_name("no_markers", target), snapshot(project, [result]))


@TARGETS
def test_managed_backup_not_overwritten(
    target, filename, h1, tmp_path, assert_snapshot
):
    project, guide = make_project(tmp_path)
    original = b"# My Notes\n\nhand-written guidance\n"
    write_files(project, {filename: original})
    first = run(guide, [target], cwd=project)
    second = run(guide, [target], cwd=project)
    assert (project / (filename + ".pre-context-forge")).read_bytes() == original
    assert_snapshot(_name("backup_kept", target), snapshot(project, [first, second]))


@TARGETS
def test_managed_block_replaced_outside_bytes_untouched(
    target, filename, h1, tmp_path, assert_snapshot
):
    project, guide = make_project(tmp_path)
    above = b"above one\r\nabove two\r\n"
    below = b"below one\r\nlast line, no final newline"
    old_block = f"{BEGIN}\nstale generated content\n{END}\n".encode()
    write_files(project, {filename: above + old_block + below})
    result = run(guide, [target], cwd=project)
    data = (project / filename).read_bytes()
    assert data.startswith(above + BEGIN.encode() + b"\n" + h1.encode())
    # Recorded quirk: awk adds a final newline the file did not have, although
    # the script promises to pass bytes outside the block through untouched.
    assert data.endswith(END.encode() + b"\n" + below + b"\n")
    assert b"stale generated content" not in data
    assert not (project / (filename + ".pre-context-forge")).exists()
    assert_snapshot(_name("block_replaced", target), snapshot(project, [result]))


@TARGETS
def test_managed_legacy_marker_migrated(
    target, filename, h1, tmp_path, assert_snapshot
):
    project, guide = make_project(tmp_path)
    legacy = f"{h1}\n\nproject intro\n\n{LEGACY}\nold generated content\n"
    write_files(project, {filename: legacy})
    result = run(guide, [target], cwd=project)
    text = (project / filename).read_text()
    assert text.count(h1 + "\n") == 1
    assert "project intro" in text
    assert "old generated content" not in text
    assert LEGACY not in text
    assert_snapshot(_name("legacy", target), snapshot(project, [result]))


@TARGETS
def test_managed_legacy_end_marker_keeps_tail(
    target, filename, h1, tmp_path, assert_snapshot
):
    project, guide = make_project(tmp_path)
    legacy = (
        f"{h1}\n\nproject intro\n\n{LEGACY}\nold generated content\n"
        f"{LEGACY_END}\nproject tail after the end marker\n"
    )
    write_files(project, {filename: legacy})
    result = run(guide, [target], cwd=project)
    text = (project / filename).read_text()
    assert text.endswith(END + "\nproject tail after the end marker\n")
    assert "old generated content" not in text
    assert_snapshot(_name("legacy_end", target), snapshot(project, [result]))


@TARGETS
@pytest.mark.parametrize(
    "broken",
    [
        f"top\n{BEGIN}\none\n{BEGIN}\ntwo\n{END}\n",
        f"top\n{END}\nmiddle\n{BEGIN}\nbottom\n",
    ],
    ids=["two_begin", "end_before_begin"],
)
def test_managed_broken_markers_unchanged(
    target, filename, h1, broken, tmp_path, assert_snapshot, request
):
    project, guide = make_project(tmp_path)
    write_files(project, {filename: broken})
    result = run(guide, [target], cwd=project)
    assert (project / filename).read_text() == broken
    case = request.node.callspec.id
    assert_snapshot(f"test_managed_broken_{case}", snapshot(project, [result]))
