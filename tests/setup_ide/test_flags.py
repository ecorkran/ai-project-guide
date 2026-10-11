"""Flag behavior: --capabilities, --dry-run, --root."""

from harness import make_project, run


def test_flags_capabilities(tmp_path):
    project, guide = make_project(tmp_path)
    result = run(guide, ["--capabilities"], cwd=project)
    # cf parses this exact line to decide which flags it may pass.
    assert result.stdout == "dry-run write-lint root\n"
    assert result.code == 0
