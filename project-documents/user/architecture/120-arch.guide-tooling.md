---
docType: architecture
layer: project
project: ai-project-guide
archIndex: 120
component: guide-tooling
relatedSlices: [120, 121]
riskLevel: medium
dateCreated: 20261011
dateUpdated: 20261011
status: in_progress
---

# Architecture: Guide Tooling

## Overview

The guide ships scripts that run inside consumer projects. The largest is `scripts/setup-ide`, about 1,760 lines of bash plus `scripts/setup-ide-lint.sh`, which it sources. It has no automated tests, shellcheck reports 108 findings, and it breaks the guide's own shell rule (`project-guides/rules/shell.md`: past ~50 lines of logic, or once you need data structures, use Python).

This initiative gives those scripts tests and moves setup-ide to Python. Tracked in GitHub issue #32.

### Scope
- Behavior tests for setup-ide that run against fixture projects.
- A Python rewrite of setup-ide and its lint helper.
- The minimal dev setup that the guide's own rules require once the repo contains Python: a ruff config and a pre-commit hook.

Out of scope for now: the other scripts in `scripts/` (bootstrap, migration helpers, template stubs, validate-slice-design). They are short and stable.

## Design Goals
- **No change for users or cf.** Same entry point, targets, flags, output, exit codes, manifest format, overwrite protection, prune rules, and `rules.exclude` handling.
- **No install step.** Python 3 standard library only. No pyproject, no virtualenv, no third-party packages at runtime or in tests.
- **Tests before the rewrite.** Record what the bash version does, then hold the Python version to the same results.
- **Nothing new in tarballs except the runtime code.** Tests, fixtures, and dev config are export-ignored.

## Constraints

### cf contract
- cf runs `bash <guideDir>/scripts/setup-ide ...` at that fixed path. `scripts/setup-ide` stays a bash file: a thin wrapper that checks the Python version and execs the Python code.
- `--capabilities` must exit 0 and print whitespace-separated words. cf checks `dry-run`, `write-lint` and `root`. The output may only gain words.
- cf versions older than the guide's v0.20.1 support find `--dry-run` and `--write-lint` by searching the script text. Those literals stay in the wrapper.
- Moving or removing the wrapper needs a cf change first.

### Python version
- Minimum Python 3.9. That is what the Xcode command line tools install on macOS, so most Mac users already have it.
- The wrapper fails with a clear message if `python3` is missing or older than 3.9. It never falls back to the old bash code.

## Layout
- `scripts/setup-ide`: bash wrapper (ships).
- `scripts/setup_ide/`: Python package, split into modules of about 300 lines each (ships).
- `tests/`: test code and fixture projects, using `unittest` (export-ignored).
- A repo-level ruff config and a pre-commit hook (export-ignored). Remove `python.md` from `rules.exclude` in `.context-forge.toml` so this repo's own Python rules apply to it.

## Risks
- **Silent behavior drift.** setup-ide writes into users' projects, and a mistake there can overwrite their files. The behavior tests from slice 120 are the guard, and slice 121 cannot merge until the Python version passes all of them.
- **Python missing on a fresh machine.** Handled by the wrapper's version check.

## Anticipated Slices
- **(120) setup-ide Behavior Tests**: fixture harness that runs against the current bash version, plus the repo's first ruff config and hook.
- **(121) setup-ide Python Rewrite**: replace the bash body with the Python package behind the wrapper.

## Related Work
- GitHub issue #32 and its design comment (deferred shipped-version checksum adoption, cf contract).
- [readme.setup-ide.md](../../../readme.setup-ide.md): user-facing setup-ide documentation.
- [shell.md](../../../project-guides/rules/shell.md): the rule the bash version breaks.
