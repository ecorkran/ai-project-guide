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

Update 20261011: the Python rewrite (121) and its release check (122) are cancelled. setup-ide moves into cf, and the slice 120 suite is the bar for that port. See Direction Change in the architecture doc.

## Foundation Work

None. Slice 120 brings in the first Python and its dev setup.

## Feature Slices

1. [x] **(120) setup-ide Behavior Tests** — Fixture projects and a black-box pytest harness with snapshots that run the current bash `scripts/setup-ide` for each target and flag (`--dry-run`, `--write-lint`, `--root`, `--capabilities`) and record which files are written, their contents, the manifest, the output, and the exit code. Cover overwrite protection (existing manifest, missing manifest with a differing file), pruning, `rules.exclude`, legacy managed-section migration, and lint baseline checks. Adds the repo's first Python dev setup: ruff config, pre-commit hook, `python.md` removed from `rules.exclude`, and `tests/` export-ignored. Dependencies: none. Risk: Medium (the fixtures must describe the real behavior, quirks included, or the rewrite inherits a false baseline). Effort: 3/5

2. [x] **DEPRECATED (20261011)** **(121) setup-ide Python Rewrite** — Status: deprecated. Checked off as resolved, not built. Cancelled 20261011: setup-ide moves into cf (TypeScript), with the slice 120 suite as the bar for cf's port. See Direction Change in the architecture doc. Original scope: Replace the bash body of `scripts/setup-ide` and `scripts/setup-ide-lint.sh` with a standard-library Python package in `scripts/setup_ide/`, minimum Python 3.9. `scripts/setup-ide` becomes a bash wrapper that checks the Python version, keeps the `--dry-run` / `--write-lint` literals for older cf, and execs the package. Must pass every slice 120 test unchanged. Update readme.setup-ide.md for the Python requirement. Dependencies: [120]. Risk: Medium (writes into users' projects; cf depends on the entry point). Effort: 4/5

## Integration Work

3. [x] **DEPRECATED (20261011)** **(122) Release and cf Check** — Status: deprecated. Checked off as resolved, not built. Cancelled 20261011 along with 121. The real-project check of cf's flows moves to the cf slice that ports setup-ide. Original scope: Run cf's setup-ide flows (guide install and update, `--capabilities` detection) against the rewritten script in a real consumer project. Confirm that the release tarball contains `scripts/setup_ide/` and leaves out `tests/` and the dev config. Dependencies: [121]. Effort: 1/5

## Future Work

- **Shipped-version checksum adoption** — When a project has no install manifest, adopt a file only if it matches a version the guide has shipped, using a per-target, per-path checksum table regenerated at release time (`legacy_manifest_entries` is the precedent). Design notes are in the #32 comment. Now belongs to cf, after its port.
