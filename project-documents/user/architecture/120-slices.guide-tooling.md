---
docType: slice-plan
parent: user/architecture/120-arch.guide-tooling.md
project: ai-project-guide
dateCreated: 20261011
dateUpdated: 20261011
status: not_started
---

# Slice Plan: Guide Tooling

## Parent

[120-arch.guide-tooling.md](120-arch.guide-tooling.md)

## Overview

Put setup-ide under test, then rewrite it in Python behind the existing bash entry point. Tests come first so the rewrite has something to be checked against.

## Foundation Work

None. Slice 120 brings in the first Python and its dev setup.

## Feature Slices

1. [ ] **(120) setup-ide Behavior Tests** — Fixture projects and a black-box pytest harness with snapshots that run the current bash `scripts/setup-ide` for each target and flag (`--dry-run`, `--write-lint`, `--root`, `--capabilities`) and record which files are written, their contents, the manifest, the output, and the exit code. Cover overwrite protection (existing manifest, missing manifest with a differing file), pruning, `rules.exclude`, legacy managed-section migration, and lint baseline checks. Adds the repo's first Python dev setup: ruff config, pre-commit hook, `python.md` removed from `rules.exclude`, and `tests/` export-ignored. Dependencies: none. Risk: Medium (the fixtures must describe the real behavior, quirks included, or the rewrite inherits a false baseline). Effort: 3/5

2. [ ] **(121) setup-ide Python Rewrite** — Replace the bash body of `scripts/setup-ide` and `scripts/setup-ide-lint.sh` with a standard-library Python package in `scripts/setup_ide/`, minimum Python 3.9. `scripts/setup-ide` becomes a bash wrapper that checks the Python version, keeps the `--dry-run` / `--write-lint` literals for older cf, and execs the package. Must pass every slice 120 test unchanged. Update readme.setup-ide.md for the Python requirement. Dependencies: [120]. Risk: Medium (writes into users' projects; cf depends on the entry point). Effort: 4/5

## Integration Work

3. [ ] **(122) Release and cf Check** — Run cf's setup-ide flows (guide install and update, `--capabilities` detection) against the rewritten script in a real consumer project. Confirm that the release tarball contains `scripts/setup_ide/` and leaves out `tests/` and the dev config. Dependencies: [121]. Effort: 1/5

## Future Work

- **Shipped-version checksum adoption** — When a project has no install manifest, adopt a file only if it matches a version the guide has shipped, using a per-target, per-path checksum table regenerated at release time (`legacy_manifest_entries` is the precedent). Design notes are in the #32 comment. Much easier to build once the code is in Python.
