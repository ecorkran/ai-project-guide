# Tests

Dev-only tests for the guide's tooling. This folder is export-ignored, so it never ships in release tarballs.

## Dev tools

```bash
uv tool install pytest ruff        # or pipx
git config core.hooksPath .githooks  # pre-commit: ruff check + format on staged .py
```

The tests target Python 3.9, the same as setup-ide.

## setup-ide suite

`tests/setup_ide/` runs `bash <guide>/scripts/setup-ide` as a subprocess against throwaway projects and compares the files written, the manifest, the output and the exit code with stored snapshots. It never imports setup-ide code, so the same suite checks the bash version and the Python rewrite.

```bash
pytest tests/setup_ide -q                      # run
pytest tests/setup_ide -q --update-snapshots   # rewrite snapshots from current output
git diff tests/                                # review what changed and why
```

**Never edit a snapshot by hand.** Snapshots are only written by `--update-snapshots` against the current script. A hand edit can hide a real difference. A change to a snapshot gets its own commit with the reason.

## Recorded quirks

Behavior that looks like a bug but is snapshotted as it is today. Each entry names the test and says what looks wrong. A fix goes into a later commit that updates that snapshot.

- **Default glob has a stray newline** (`test_targets_copilot_fresh`, `test_targets_agents_fresh`). A rule with no `paths:` (the fixture's `broken.md`) gets the default glob `**` printed with a newline in the middle: `applyTo: "**` then `**"` in the copilot instruction file, and the same split in the AGENTS.md "Applies to" line. The default is meant to be a single `**` (scripts/setup-ide, "defaults to \"**\" when paths is absent").
- **Final newline added to a managed file** (`test_managed_block_replaced_*`). When a CLAUDE.md or AGENTS.md already has a BEGIN/END block and its last line has no newline, replacing the block appends one. CRLF endings above and below the block are kept. `write_managed_section` says bytes outside the block pass through untouched, but the awk `print` in the `managed` branch adds the newline.
- **Project root inside the guide** (no test; the harness avoids it). The guide repo now has a `project-documents/` folder, and setup-ide finds the project root by walking up from the working directory to the first `project-documents/`. A submodule install run from inside the guide folder therefore resolves the root to the guide itself. Tarball installs and cf usage are unaffected.
