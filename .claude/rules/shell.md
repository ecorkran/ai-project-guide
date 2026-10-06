---
description: Shell script standards for bash and sh, including CI/CD and pipeline scripts. Use when writing, modifying, or reviewing .sh/.bash files, extensionless scripts with a bash or sh shebang, or shell in CI workflow run blocks.
paths:
  - "**/*.sh"
  - "**/*.bash"
  - "**/.github/workflows/*.yml"
  - "**/.github/workflows/*.yaml"
  - "**/.gitlab-ci.yml"
---

### Shell Script Rules

#### General
- Use `#!/usr/bin/env bash` and start every script with `set -euo pipefail`.
- All scripts must pass `shellcheck` with no warnings. A `# shellcheck disable=SCxxxx` needs a comment saying why. Run `shellcheck` in the pre-commit hook and in CI so the linter enforces these rules, not the agent.
- If a script exceeds ~50 lines of logic (not counting command invocations), or needs data structures, write it in Python.

#### Quoting and Variables
- Quote all variable expansions: `"$var"`, `"${arr[@]}"`, `"$@"`.
- Declare function variables with `local`.

#### Directories and Temp Files
- Guard every `cd`: `cd "$dir" || exit 1`. `set -e` does not apply inside functions called from `if`, `&&` or `||`.
- Create temp files and directories with `mktemp` and remove them with `trap`:
  `tmp_dir="$(mktemp -d)"; trap 'rm -rf "$tmp_dir"' EXIT`

#### Text Processing
- Never use `sed`, `awk` or `grep` to edit YAML or JSON. Use `yq` or `jq`.
- `sed`/`awk` beyond a single simple substitution: add a comment with sample input → output, or implement it in Python.

#### CI Workflows
- A `run:` block longer than a few lines goes in a script file in the repo, so `shellcheck` checks it and it can be run locally.
- In GitHub Actions, set `shell: bash` (default or per step) to get `-eo pipefail`; the implicit default does not set `pipefail`.
