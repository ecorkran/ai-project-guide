"""Smoke test: every target against the real project-guides/, assertions only.

No snapshot: real rules change often, and this only has to catch a script that
breaks on content the fixture guide does not have.
"""

import pytest
from harness import REPO_ROOT, make_project, run

# Top-level files each target writes, from the target table in README.md.
EXPECTED = {
    "claude": ["CLAUDE.md", ".claude/rules", ".claude/agents"],
    "cursor": ["AGENTS.md", ".cursor/rules"],
    "copilot": ["AGENTS.md", ".github/copilot-instructions.md", ".github/instructions"],
    "agents": ["AGENTS.md"],
}


@pytest.mark.parametrize("target", sorted(EXPECTED))
def test_real_guide_target_installs(target, tmp_path):
    project, guide = make_project(tmp_path, guides=REPO_ROOT / "project-guides")
    result = run(guide, [target], cwd=project)
    assert result.code == 0, result.stdout + result.stderr
    assert "❌" not in result.stdout + result.stderr
    for rel in EXPECTED[target]:
        assert (project / rel).exists(), rel
