---
docType: architecture
layer: project
project: ai-project-guide
archIndex: 120
component: guide-tooling
relatedSlices: [120, 121, 122]
riskLevel: medium
dateCreated: 20261011
dateUpdated: 20261013
status: complete
---

# Architecture: Guide Tooling

## Overview

The guide ships scripts that run inside consumer projects. The largest is `scripts/setup-ide`, about 1,760 lines of bash plus `scripts/setup-ide-lint.sh`, which it sources. It has no automated tests, shellcheck reports 108 findings, and it breaks the guide's own shell rule (`project-guides/rules/shell.md`: past ~50 lines of logic, or once you need data structures, use Python).

This initiative gives those scripts tests and moves setup-ide to Python. Tracked in GitHub issue #32.

## Outcome (20261013)

Done. cf 0.19.6 ships the native installer (cf slice 215) and `cf validate design` (cf slice 214), and the suite lives in cf at `packages/cli/tests/ideInstall/`. The guide removed `scripts/`, `tests/`, `ruff.toml` and `.githooks/` and is now docs only. Minimum cf version: 0.19.6.

## Direction Change: the Installer Moves to cf (20261011)

The Python rewrite (slice 121) is cancelled. setup-ide moves into context-forge (cf, TypeScript) instead. The sections below this one describe the original Python plan and are kept as a record.

Why:
- The guide is no longer supported without cf. Guide releases already follow what cf and sq need, so tying installer changes to a cf release costs nothing.
- setup-ide calls back into cf (`cf config get rules.exclude`) to read cf's own config. That is a dependency in both directions. Inside cf it becomes a plain function call.
- The whole cf contract below (`--capabilities`, the `--dry-run`/`--write-lint` literals kept for older cf, "moving the wrapper needs a cf change first") becomes internal code once cf owns the installer.
- It keeps a Python 3.9 runtime requirement out of a documentation repo.

What it means here:
- **The guide becomes docs only.** cf ports setup-ide natively in TypeScript and stops calling the guide's script. No setup-ide wrapper is left in the guide.
- **The slice 120 suite moves into cf as the spec.** `tests/setup_ide/` (76 black-box tests and their snapshots) moves to cf. Only the harness's `run()` changes, to call cf's command instead of `bash <guide>/scripts/setup-ide`. The snapshots stay as they are and define the expected behavior.
- **The bash `scripts/setup-ide` stays in the guide unchanged** until a cf release no longer calls it. Older cf versions still run it at that path. It is removed in a later guide release.
- **The cf stub tests need a redesign on the cf side.** The harness puts a stub `cf` first on `PATH` to answer `cf config get` for the `rules.exclude` tests (`test_rules_exclude.py`). Once cf is the installer, it reads that config itself, so those tests have to supply the config another way. That is cf's decision.
- **Exact behaviors to reproduce:** [120-analysis.setup-ide-port-findings.md](../analysis/120-analysis.setup-ide-port-findings.md) lists the bash behaviors a port has to match, including several that are easy to miss.
- **#38 and #40** (managed block adds a final newline; default glob `**` newline `**`) are no longer "fix after the Python port". They are decisions for cf's port: reproduce them first and fix them afterwards with a snapshot update, or fix them in the port and update those snapshots in a separate, labeled commit.
- **Slice 122** (release and cf check) is cancelled as written. Its job, running cf's flows in a real consumer project, moves to the cf slice.
- **Later cleanup:**
  - Once the suite has moved to cf, remove `tests/setup_ide/` from this repo. Remove the Python dev setup (`ruff.toml`, `.githooks/`) too if nothing else needs it. Both stay while `tests/setup_ide/` is here, because the suite is Python.
  - Once a cf release no longer calls `scripts/setup-ide`, a later guide release removes it and `scripts/setup-ide-lint.sh`. No wrapper is left behind.  - The other scripts (validate-slice-design, bootstrap, migration helpers, template stubs) stay where they are.

### Scope
- Behavior tests for setup-ide that run against fixture projects.
- A Python rewrite of setup-ide and its lint helper.
- The minimal dev setup that the guide's own rules require once the repo contains Python: a ruff config and a pre-commit hook.

Out of scope for now: the other scripts in `scripts/` (bootstrap, migration helpers, template stubs, validate-slice-design). They are short and stable.

## Design Goals
- **No change for users or cf.** Same entry point, targets, flags, output, exit codes, manifest format, overwrite protection, prune rules, and `rules.exclude` handling.
- **No install step.** setup-ide uses the Python 3 standard library only: no pyproject, no virtualenv, no third-party packages. Tests use pytest and ruff (per `python.md`), which are dev tools only and never needed to run setup-ide.
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
- `tests/`: black-box pytest suite with snapshots (export-ignored).
- A repo-level ruff config and a pre-commit hook (export-ignored). Remove `python.md` from `rules.exclude` in `.context-forge.toml` so this repo's own Python rules apply to it.

## Risks
- **Silent behavior drift.** setup-ide writes into users' projects, and a mistake there can overwrite their files. The behavior tests from slice 120 are the guard, and slice 121 cannot merge until the Python version passes all of them.
- **Python missing on a fresh machine.** Handled by the wrapper's version check.

## Anticipated Slices
- **(120) setup-ide Behavior Tests**: fixture harness that runs against the current bash version, plus the repo's first ruff config and hook.
- **(121) setup-ide Python Rewrite**: cancelled; the installer moves to cf (see Direction Change).
- **(122) Release and cf Check**: cancelled as written; the real-project check moves to the cf slice.

## Related Work
- GitHub issue #32 and its design comment (deferred shipped-version checksum adoption, cf contract).
- [readme.setup-ide.md](../../../readme.setup-ide.md): user-facing setup-ide documentation.
- [shell.md](../../../project-guides/rules/shell.md): the rule the bash version breaks.
