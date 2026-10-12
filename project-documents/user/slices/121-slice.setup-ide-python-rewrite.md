---
docType: slice-design
slice: setup-ide-python-rewrite
project: ai-project-guide
parent: project-documents/user/architecture/120-slices.guide-tooling.md
dependencies: [120]
interfaces: [122]
dateCreated: 20261011
dateUpdated: 20261011
status: deprecated
---

> **Deprecated 20261011.** Cancelled before implementation: setup-ide moves into context-forge (TypeScript) instead, with the slice 120 suite as the bar. See Direction Change in `120-arch.guide-tooling.md` and `user/analysis/120-analysis.setup-ide-port-findings.md`.

# Slice Design: setup-ide-python-rewrite

## Overview

Replace the bash body of `scripts/setup-ide` (1,769 lines) and `scripts/setup-ide-lint.sh` (220 lines) with a standard-library Python package at `scripts/setup_ide/`. `scripts/setup-ide` stays at the same path as a short bash wrapper: it checks for Python 3.9+, then execs the package. `setup-ide-lint.sh` is deleted.

This is a port, not a redesign. The bar is the slice 120 suite: all 76 tests pass with no snapshot changed. Known quirks (#38, #40, the stale "(general, git)" note) are reproduced exactly and fixed afterwards as separate `fix:` commits.

## Value

- **Maintainability:** setup-ide is the guide's biggest piece of code and writes into users' projects. In bash it carries awk programs, temp files, and global state across ~60 functions, and shellcheck reports 108 findings. It also breaks the guide's own `shell.md` rule. Python with explicit state is much easier to read, change, and test.
- **Unblocks follow-up work:** the quirk fixes (#38, #40) and the shipped-version checksum adoption (Future Work in the slice plan) are much simpler to write in Python.
- **No change for users or cf:** same entry point, flags, output, exit codes, manifest format and file results. The only new requirement is Python 3.9+, which macOS command line tools already provide.

## Technical Scope

Included:
- `scripts/setup-ide` rewritten as a bash wrapper (Python check, exec).
- `scripts/setup_ide/` package: a full port of `setup-ide` and `setup-ide-lint.sh`.
- Deletion of `scripts/setup-ide-lint.sh` (cf never references it; it is only sourced by setup-ide).
- A few new tests for wrapper-only behavior: Python missing, Python too old, a python3 that fails to run (a stub that exits 1, standing in for the macOS stub), a bare-filename run from inside `scripts/`, no bytecode written into the guide, the cf flag literals present in the wrapper.
- `readme.setup-ide.md`: Python 3.9+ requirement and the error you get without it.
- CHANGELOG `[Unreleased]` entry.

Excluded:
- Behavior changes of any kind, including the known quirks. Each one gets its own `fix:` commit after this slice merges.
- Issue #39 (project root inside the guide) and #37 (README lists `.cursor/agents/`). Both are separate fixes.
- Release and cf verification against a real consumer project (slice 122).
- Shipped-version checksum adoption (Future Work).
- Linux CI. The suite is run on macOS as in slice 120.

## Dependencies

### Prerequisites
- Slice 120 (merged): the behavior suite in `tests/setup_ide/`, root `ruff.toml` (target py39), and `.githooks/pre-commit`.
- Python 3.9+ at runtime (`python3` on PATH). Dev only: pytest and ruff.

### Interfaces Required
- **cf → setup-ide contract** (from the architecture doc), unchanged:
  - cf runs `bash <guideDir>/scripts/setup-ide <target> [flags]`.
  - `--capabilities` exits 0 and prints `dry-run write-lint root`.
  - Older cf finds `--dry-run` and `--write-lint` by searching the script text, so both literals stay in the wrapper.
- **setup-ide → cf**: `cf config get --help`, `cf config get --value rules.exclude`, and the older labeled `cf config get rules.exclude`, run from the project root. The same exit-code handling as today (0 = value, 2 = unknown key, other = hard error).

## Architecture

### Component Structure

```
scripts/
  setup-ide              bash wrapper (ships)
  setup_ide/             Python package (ships)
    __main__.py          puts scripts/ on sys.path, calls cli.main()
    cli.py               argument parsing, usage, target aliases, dispatch, exit codes
    context.py           constants and the Run object (paths, flags, reporter)
    output.py            Reporter: colored status lines to stdout/stderr or a buffer
    textio.py            file read/write helpers (one encoding rule, below)
    exclude.py           rules.exclude: read from env or cf, match, warn
    frontmatter.py       has_always_apply, validate, field lookup, paths→globs, strip name
    manifest.py          POSIX cksum, legacy entries, install_file, finish (prune)
    managed.py           managed_state, pre-managed backup, write_managed_section
    compile.py           CLAUDE.md / AGENTS.md / copilot composite content
    targets.py           setup_claude, setup_cursor, setup_agents, setup_copilot, copiers
    dryrun.py            sandbox copy, run, diff report
    lint.py              port of setup-ide-lint.sh
```

Module names map to the bash function groups, so a reviewer can compare a module with the bash it replaces. Each stays around 300 lines. If `targets.py` or `compile.py` runs over, split it by target. Don't merge modules to save files.

### Data Flow

1. The wrapper checks Python, then runs `python3 -I -B <guide>/scripts/setup_ide/__main__.py "$@"`.
2. `cli.main` parses the arguments. `--capabilities` prints and exits. Other arguments are handled as today: flags may appear anywhere, `--root` has two forms, and everything else passes through.
3. It builds a `Run`:
   - guide source dirs come from the package location (`<guide>/project-guides/...`), never from the project
   - project root comes from `--root`, or from walking up to `project-documents/`, using the same fallback order as today
   - target root starts equal to the project root
4. It reads exclusions (env var first, then cf), then prints the root detection lines.
5. It validates and normalizes the target (case-insensitive; `openai`/`codex` → `agents`).
6. Normal run: begin manifest → target setup → finish manifest (prune, write) → lint check.
   Dry run: copy the existing install paths into a temp sandbox (skipping `.claude/worktrees`), run the same install with the target root set to the sandbox and a buffering reporter, then print the filtered warnings and the `+`/`~`/`-` report.
7. It warns about unmatched exclusions on stderr and exits with the run's status.

### State Management

The bash script keeps its state in globals (`TARGET_ROOT`, `NEW_MANIFEST`, `RULES_EXCLUDE_MATCHED`, `DRY_RUN`, ...). The Python version keeps it in one `Run` object, passed explicitly:
- paths: guide sources, project root, target root
- flags: dry run, write lint
- exclusions: patterns, source label, matched set
- manifest: old entries, new entries (in memory; no temp files)
- reporter

A dry run makes a copy of the `Run` with `target_root` pointing at the sandbox and a buffering reporter. The lint check reads from `project_root` and writes to `target_root`, as it does today, so a dry run still checks the real project.

Persistent state keeps its format: `.context-forge/<target>.manifest` has one `<crc> <size> <path>` line per file, sorted by path in byte order. One deliberate difference: bash runs `sort -k3` under the caller's locale, so on Linux with a UTF-8 locale a bash-written manifest can be in locale collation order. Python always writes byte order, so such a manifest may reorder once on the next run. Reading doesn't depend on order, and the suite (which forces `LC_ALL=C`) can't see this.

## Technical Decisions

### Technology Choices
- **Standard library only, Python 3.9.** No pyproject, no install step. The code must not use features newer than 3.9: no `match`, and no `X | Y` type unions or `list[str]` annotations evaluated at runtime (use `from __future__ import annotations`). ruff's `target-version = "py39"` catches most of these. The suite runs under `/usr/bin/python3` (3.9.6 on macOS), so it catches the rest.
- **Manual argument parsing, not argparse.** argparse changes usage text, error messages and exit codes, and it would reject the pass-through arguments the bash loop accepts. The bash loop is about 30 lines and ports one-to-one.
- **POSIX `cksum` implemented in Python.** Manifest lines and the hard-coded legacy entries use `cksum` output. That is CRC-32 with polynomial 0x04C11DB7, not reflected, with the byte length folded in and the result inverted. It is not `zlib.crc32`. Use a 256-entry table built at import time. The manifest snapshots and the legacy-entry prune tests check it.
- **Glob matching for `rules.exclude`:** `fnmatch.fnmatchcase` on the basename, the same as a bash `case` pattern for `*`, `?` and `[...]`.
- **cf lookup:** `shutil.which("cf")` plus `subprocess.run(..., cwd=project_root)`, with the same exit-code handling as today.

### Patterns and Conventions
- **Wrapper runs Python with `-I -B`.**
  - `-I` (isolated mode) ignores `PYTHONPATH`, user site-packages and `PYTHON*` variables, so a user's environment can't change how setup-ide runs. `__main__.py` adds `scripts/` to `sys.path` so `setup_ide` imports as a package. (On 3.9 and 3.10, Python also puts `scripts/setup_ide/` itself on the path; from 3.11 `-I` doesn't.) All imports are package-qualified (`from setup_ide import ...`), so no module is ever loaded under two names.
  - `-B` stops Python writing `__pycache__/` into the guide. In a submodule install that would dirty the submodule's `git status`.
- **One text I/O rule (`textio.py`).** Every read and write of project or guide files uses `encoding="utf-8", errors="surrogateescape", newline=""`. With these settings any byte sequence survives a round trip and CRLF is never translated, matching bash's byte-for-byte handling. Comparisons that bash does with `cmp` compare bytes. Writes go to the destination with normal permissions (bash uses `cat >` so the file gets the umask mode, not mktemp's 600). Managed writes keep the `.context-forge.tmp` file and rename.
- **Output encoding and buffering.** `cli.main` reconfigures stdout and stderr with `encoding="utf-8", line_buffering=True`.
  - UTF-8, because bash writes emoji bytes whatever the locale. Under `LC_ALL=C`, Python 3.9 already switches to UTF-8 mode, but other non-UTF-8 locales would crash on the first emoji.
  - Line buffering, because bash writes each line as it goes. When cf or a user merges the streams (`2>&1`), the order stays the same as today. The suite captures the streams separately, so it can't check this.
- **Colors.** `Reporter.status(color, message)` always emits the same ANSI codes as `print_status`. Snapshots strip ANSI, so this is for parity, not for the tests.
- **Errors.** Every bash `exit 1` inside a function becomes a `SetupError` raised with the message already printed. `cli.main` is the process boundary. It catches `SetupError` (exit 1) and `KeyboardInterrupt` (exit 130 with no traceback, as bash does on Ctrl-C). No other broad handler. Places where bash ignores a failure (`|| true`, `|| return 0`) catch the specific exception, with a comment saying why. Specific paths:
  - **cf subprocess:** if starting cf raises `OSError`, treat it as a non-zero exit. That takes the same branch as bash's exit 126/127: the "failed (exit N)" hard error and exit 1. No timeout, same as bash.
  - **Dry-run sandbox:** created with `tempfile.TemporaryDirectory` in a `with` block, so it is removed on an error or Ctrl-C too.
- **Port quirks faithfully.** Where awk or grep behavior is odd (unanchored `grep -q "description:"` in frontmatter validation, the `**`-newline-`**` default glob, the final-newline add in the managed branch), the Python reproduces it. Each such spot gets a one-line comment naming the issue number (or "matches bash") so the later fix is easy to find.
- **Constants defined once** in `context.py`: the markers, the backup suffix, the manifest dir name, `INSTALL_PATHS`, `DRY_RUN_SKIP_PATH`, `CAPABILITIES`, the lint write paths, and the color codes.

## Implementation Details

### Migration Plan
- **Source → destination:** `scripts/setup-ide` (body) and `scripts/setup-ide-lint.sh` → `scripts/setup_ide/*.py`. `scripts/setup-ide` is rewritten in place as the wrapper. `setup-ide-lint.sh` is deleted.
- **Consumers:**
  - cf calls the same path with the same arguments, so cf needs no change.
  - Release tarballs already include `scripts/`. `scripts/setup_ide/` ships automatically, and `__pycache__` is gitignored. Slice 122 checks the tarball.
  - The test harness copies the guide's whole `scripts/`, so it picks up the package without changes.
- **Data:** none. Existing `.context-forge/*.manifest` files are read as they are, and new ones are written in the identical format.
- **Behavior verification:**
  - `pytest tests/setup_ide -q` → 76 passed.
  - `git status --short tests/` is empty after `--update-snapshots`.
  - The new wrapper tests pass.
  - The slice 120 mutation check is repeated on the Python version: change `MANAGED_BEGIN` and see mass failures; make the no-manifest branch of `install_file` overwrite and see `test_ownership_no_manifest_differing_file_skipped` fail.

### API Contracts

Wrapper (the whole cf-facing surface). Shape only; final wording is set during implementation:

```bash
#!/bin/bash
# AI Project Guide - IDE setup. The implementation is the Python package in
# setup_ide/; this wrapper only checks for Python and runs it.
# Flags: --dry-run --write-lint --root <dir> --capabilities
# (Older cf versions detect --dry-run and --write-lint by finding these
# literals in this file. Keep them.)
command -v python3 >/dev/null 2>&1 || { echo "❌ setup-ide needs Python 3.9 or newer: python3 not found" >&2; exit 1; }
# One python3 call: on macOS without the command line tools, /usr/bin/python3
# is a stub that opens an install prompt and fails; don't trigger it twice.
if ! found=$(python3 -c 'import sys; print(sys.version.split()[0]); sys.exit(sys.version_info < (3, 9))' 2>/dev/null); then
    echo "❌ setup-ide needs Python 3.9 or newer: found ${found:-a python3 that did not run (on macOS: xcode-select --install)}" >&2
    exit 1
fi
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 -I -B "$SCRIPT_DIR/setup_ide/__main__.py" "$@"
```

- The Python check comes first and uses only bash builtins, so the "python3 not found" path works with an empty PATH.
- `SCRIPT_DIR` uses the same `dirname` form as today, which handles a bare `bash setup-ide` run from inside `scripts/`.
- `found` is empty when python3 didn't run at all (the macOS stub, a broken install), and holds the version when it ran but is too old.
- Exit codes: 1 for a missing or old Python. Otherwise the package's codes, which match today's (0 on success, 1 on errors).

## Integration Points

### Provides to Other Slices
- **122 (Release and cf Check):** a wrapper with the same contract, and a package in `scripts/setup_ide/` to confirm in the tarball.
- **Later `fix:` commits:** a Python codebase where #38, #40 and the stale note are each a small, tested change.

### Consumes from Other Slices
- **120:** the suite, harness and snapshots are the definition of "same behavior". If a snapshot difference shows up, the Python is wrong. The only exception is a difference that comes from the test environment, not from setup-ide; that one is fixed in the harness, in its own commit with the reason.

## Success Criteria

### Functional Requirements
- All 76 slice 120 tests pass against the Python version, with no snapshot file changed and no test edited to accommodate it.
- `bash scripts/setup-ide --capabilities` prints `dry-run write-lint root` and exits 0.
- The wrapper text contains the literals `--dry-run` and `--write-lint`.
- With no `python3` on PATH, or a `python3` older than 3.9, setup-ide prints one clear error on stderr, exits 1, and writes nothing.
- A run writes no `__pycache__/` anywhere under the guide.
- Existing manifests written by the bash version are read correctly: an unchanged guide reports "No changes" on dry run, and pruning works.

### Technical Requirements
- Standard library only, and it runs on Python 3.9 (`/usr/bin/python3` on macOS).
- `ruff check` and `ruff format --check` pass on `scripts/setup_ide/` with the repo's `ruff.toml`.
- Modules are about 300 lines, functions about 50.
- Constants are defined once. No broad exception handler except the one in `cli.main`.
- `scripts/setup-ide-lint.sh` is removed. No reference to it is left outside historical project documents.
- `readme.setup-ide.md` states the Python 3.9+ requirement. CHANGELOG `[Unreleased]` has an entry.

### Integration Requirements
- cf's existing setup-ide flows (install, update, `--dry-run`, `--write-lint`, `--root`) work unchanged. 122 confirms this against a real consumer project.

### Verification Walkthrough

Run from the repo root (`/Users/manta/source/repos/manta/ai-project-guide`).

1. Suite, unchanged snapshots:
   ```bash
   pytest tests/setup_ide -q                       # expect: all passed (76 + the new wrapper tests)
   pytest tests/setup_ide -q --update-snapshots
   git status --short tests/                       # expect: empty
   ```
2. Contract checks:
   ```bash
   bash scripts/setup-ide --capabilities            # expect: dry-run write-lint root
   grep -c -- '--dry-run\|--write-lint' scripts/setup-ide   # expect: ≥ 1
   ls scripts/setup-ide-lint.sh                     # expect: No such file
   ```
3. Python requirement, by hand:
   ```bash
   env PATH=/nonexistent /bin/bash scripts/setup-ide claude; echo "exit $?"
   # expect: ❌ setup-ide needs Python 3.9 or newer: python3 not found / exit 1
   ```
4. Real use in a scratch project:
   ```bash
   tmp=$(mktemp -d) && mkdir "$tmp/project-documents" && cd "$tmp"
   bash /Users/manta/source/repos/manta/ai-project-guide/scripts/setup-ide claude
   bash /Users/manta/source/repos/manta/ai-project-guide/scripts/setup-ide claude --dry-run   # expect: 📋 No changes
   cat .context-forge/claude.manifest | head -3     # expect: "<crc> <size> <path>" lines
   find /Users/manta/source/repos/manta/ai-project-guide/scripts -name __pycache__   # expect: nothing
   ```
5. Bash-written manifest compatibility: in a project installed with the v0.20.9 bash script, run the new version with `--dry-run` and expect "No changes". Then delete one rule from a copy of the guide and expect it to be pruned on a real run.
6. Lint and style: `ruff check scripts/setup_ide && ruff format --check scripts/setup_ide` → clean.

## Risk Assessment

### Technical Risks
- **Byte-level drift.** Line endings, a missing final newline, invalid UTF-8 in a user's CLAUDE.md, or sort order can differ between Python and awk/sort/cmp. A mistake here changes or damages users' files.
- **Checksum mismatch.** If `cksum` isn't reproduced exactly, the guide stops recognizing every file it previously installed. Updates are then skipped as "edited", and nothing gets pruned.

### Mitigation Strategies
- The single `textio` rule (surrogateescape, `newline=""`) plus byte comparisons. The suite already has CRLF and no-final-newline cases (`test_managed_block_replaced_*`).
- Manifest snapshots and the legacy-entry prune tests fail on any CRC difference. Port `manifest.py` first and get those tests green before moving on.

## Implementation Notes

### Development Approach
1. Wrapper, `__main__`, `cli`, `context`, `output`: get the flag tests (`test_flags_*` for capabilities, root errors, usage) passing.
2. `textio`, `manifest` (cksum first), `frontmatter`, `exclude`.
3. `managed`, `compile`, `targets`, one target at a time: claude, then agents, copilot, cursor. Run the matching `test_targets_*` and `test_managed_sections` tests after each.
4. `dryrun`, then `lint`.
5. Delete `setup-ide-lint.sh`. Add the wrapper tests. Run the full suite, the snapshot regeneration check, and the mutation check.
6. Readme and CHANGELOG.

When a test fails, `git show v0.20.9:scripts/setup-ide` gives you the bash version to compare against. Commit after each green step, one commit per task.

### Special Considerations
- **Don't fix while porting.** When the Python looks wrong only because it copies a bash oddity, reproduce it, add a comment with the issue number, and move on. The tests can't tell a deliberate fix from an accident, so fixes go into their own `fix:` commits afterwards.
- **Security:** setup-ide runs `cf` and nothing else. All paths are joined under the target root. No shell=True.
