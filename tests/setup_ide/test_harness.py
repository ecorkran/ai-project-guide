"""Tests for the harness itself: normalization, snapshot text, snapshot gate."""

import pytest
from harness import RunResult, normalize, snapshot, write_files

MISSING_SNAPSHOT_NAME = "harness-snapshot-that-must-not-exist"


def test_harness_normalize_strips_ansi_and_replaces_paths(tmp_path):
    root = tmp_path / "project"
    guide = root / "project-documents" / "ai-project-guide"
    text = (
        f"\x1b[0;32m✅ ok {guide}/scripts\x1b[0m\n"
        f"root {root}/CLAUDE.md\n"
        "sandbox /private/var/folders/ab/cd/T/tmp.Xy12/claude\n"
        "sandbox /var/folders/ab/cd/T/tmp.Zz34\n"
        "plain /tmp/tmp.Qq56/x\n"
    )
    assert normalize(text, root, guide) == (
        "✅ ok <GUIDE>/scripts\n"
        "root <ROOT>/CLAUDE.md\n"
        "sandbox <TMP>\n"
        "sandbox <TMP>\n"
        "plain <TMP>\n"
    )


def test_harness_normalize_handles_private_prefix_variants(tmp_path):
    root = tmp_path / "project"
    guide = root / "guide"
    # The same directory spelled with and without macOS's /private prefix.
    plain = str(root.resolve()).removeprefix("/private")
    prefixed = "/private" + plain
    assert normalize(f"{plain}/x", root, guide) == "<ROOT>/x"
    assert normalize(f"{prefixed}/x", root, guide) == "<ROOT>/x"


def test_harness_snapshot_lists_sorted_files_with_visible_cr(tmp_path):
    write_files(
        tmp_path,
        {
            ".claude/rules/b.md": "b\n",
            ".claude/rules/a.md": "a\n",
            "CLAUDE.md": b"line one\r\nline two",
            "project-documents/ignored.md": "not listed\n",
            "unrelated.txt": "not listed\n",
        },
    )
    (tmp_path / ".claude" / "empty").mkdir()
    runs = [RunResult(("claude",), 0, "out\n", "", tmp_path / "guide")]

    text = snapshot(tmp_path, runs)

    assert text.startswith("== run 1: setup-ide claude\nexit: 0\n-- stdout\nout\n")
    files = text.split("== files\n")[1]
    assert files == (
        "--- .claude/empty/ (empty directory)\n"
        "--- .claude/rules/a.md\n"
        "a\n"
        "--- .claude/rules/b.md\n"
        "b\n"
        "--- CLAUDE.md\n"
        "line one\\r\n"
        "line two\n"
        "<no final newline>\n"
    )


def test_harness_snapshot_missing_file_fails(request, assert_snapshot):
    if request.config.getoption("--update-snapshots"):
        pytest.skip("would write the snapshot instead of failing")
    with pytest.raises(pytest.fail.Exception, match="missing snapshot"):
        assert_snapshot(MISSING_SNAPSHOT_NAME, "anything\n")
