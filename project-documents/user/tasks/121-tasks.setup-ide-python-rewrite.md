---
docType: tasks
slice: setup-ide-python-rewrite
project: ai-project-guide
lld: user/slices/121-slice.setup-ide-python-rewrite.md
dependencies: [120]
projectState: setup-ide is 1,769 lines of bash plus the 220-line setup-ide-lint.sh; slice 120's 76-test black-box suite passes against it
dateCreated: 20261011
dateUpdated: 20261011
status: deprecated
---

> **Deprecated 20261011.** Cancelled before implementation: setup-ide moves into context-forge (TypeScript) instead, with the slice 120 suite as the bar. See Direction Change in `120-arch.guide-tooling.md` and `user/analysis/120-analysis.setup-ide-port-findings.md`.

## Context Summary
- Working on slice 121, setup-ide-python-rewrite. Design: `project-documents/user/slices/121-slice.setup-ide-python-rewrite.md` (called "the design" below). Read its Architecture, Technical Decisions and API Contracts sections before starting.
- Port `scripts/setup-ide` and `scripts/setup-ide-lint.sh` to a standard-library Python package at `scripts/setup_ide/`. `scripts/setup-ide` becomes a bash wrapper. **This is a port, not a redesign.** Output text, exit codes and files written must match the bash exactly.
- **The bar:** all 76 tests in `tests/setup_ide/` pass, and no snapshot changes. Never edit a snapshot, and never run `--update-snapshots` to make a test pass. When a test fails, the Python is wrong.
- **Don't fix while porting.** Odd bash behavior is reproduced, with a one-line comment naming the issue: #38 (managed block adds a final newline), #40 (default glob `**` newline `**`), and the stale "(general, git)" note in `setup_claude`. See also "Recorded quirks" in `tests/README.md`.
- **Bash reference:** the wrapper replaces the bash body early, in task 3. From then on, read the original with `git show v0.20.9:scripts/setup-ide` and `git show v0.20.9:scripts/setup-ide-lint.sh`. Port function by function, with module boundaries as in the design's Component Structure.
- **Python version:** the harness runs with `PATH=<stubs>:/usr/bin:/bin`, so the suite uses `/usr/bin/python3`, which is 3.9.6. Your dev `python3` may be newer. Use no syntax or library features newer than 3.9: no `match`, no `X | Y` unions evaluated at runtime, no `zip(strict=)`. Put `from __future__ import annotations` in every module.
- **Conventions (from the design):**
  - All imports package-qualified (`from setup_ide import manifest`).
  - All file I/O through `textio` (`encoding="utf-8", errors="surrogateescape", newline=""`).
  - Constants defined once in `context.py`.
  - Only `cli.main` catches broadly: `SetupError` → 1, `KeyboardInterrupt` → 130.
  - Modules about 300 lines, functions about 50.
- Run tests: `pytest tests/setup_ide -q`, or a subset with `-k`. Lint: `ruff check scripts/setup_ide tests && ruff format --check scripts/setup_ide tests`. The pre-commit hook runs ruff on staged `.py` files.
- Work on branch `121-slice.setup-ide-python-rewrite`, forked from `main`. No integration branch is configured. Commit after each task that names a commit.

## Tasks

### Setup

- [ ] **1. Create the slice branch**
  - [ ] Confirm `cf config get git.integration_branch` is empty, so the target is `main`.
  - [ ] `git checkout -b 121-slice.setup-ide-python-rewrite main`
  - [ ] Confirm the baseline: `pytest tests/setup_ide -q` → 76 passed (still the bash version).
  - [ ] Success: on the branch, with a green baseline.

### Skeleton

- [ ] **2. Package foundation: `context.py`, `output.py`, `textio.py`, `__main__.py`**
  - [ ] `context.py`:
    - [ ] All constants: the managed markers (`MANAGED_BEGIN`, `MANAGED_END`, `MANAGED_MARKER`, `MANAGED_MARKER_END`, `GENERATED_MARKER`), `PREMANAGED_BACKUP_SUFFIX`, `MANIFEST_DIR_NAME`, `INSTALL_PATHS`, `DRY_RUN_SKIP_PATH`, `CAPABILITIES`, the lint write paths and the color codes. Copy the values exactly from the bash.
    - [ ] `SetupError`.
    - [ ] A `Run` dataclass holding: guide source dirs, `project_root`, `target_root`, `dry_run`, `write_lint`, exclusion state, manifest state, reporter. Fields can be added as later tasks need them.
  - [ ] `output.py`: a `Reporter` whose `status(color, message)` writes `color + message + reset + "\n"`, like `print_status`. It writes to stdout by default, takes a flag for stderr, and can buffer into a list (for dry run). Add a plain `line()` for bash's bare `echo`.
  - [ ] `textio.py`: `read_text`, `write_text`, `read_bytes`, plus a byte-equality helper for `cmp -s`. Use the encoding rule above. Writes create the file with normal permissions.
  - [ ] `__main__.py`: insert the parent of the package folder (`scripts/`) at `sys.path[0]`, then call `cli.main()` and exit with its return value.
  - [ ] Success: `ruff check scripts/setup_ide` is clean.

- [ ] **3. `cli.py` and the wrapper**
  - [ ] Port `main()`'s argument loop exactly:
    - [ ] `--capabilities` prints `CAPABILITIES` and returns 0 immediately.
    - [ ] `--dry-run` and `--write-lint` set the flags.
    - [ ] `--root <dir>` and `--root=<dir>` both work. A missing value or a missing directory gives the same red error on stderr and exit 1.
    - [ ] Every other argument passes through.
  - [ ] Port `show_usage`, `find_project_root` (including the `*/ai-project-guide/scripts` fallback, using the package's own location), `check_directory`, and `run_target_setup`'s lowercasing, aliasing (`openai`/`codex` → `agents`) and validation.
  - [ ] Reconfigure stdout and stderr with `encoding="utf-8", line_buffering=True` at the start of `main`.
  - [ ] Add the dispatch from `run_target_setup`: if `--dry-run`, call the dry run; otherwise call `install_target(target)`. `install_target` picks the target's setup function. Until each one is ported, each branch (the four targets and dry run) raises `SetupError("not ported yet")`. Tasks 11–15 each replace their own branch.
  - [ ] Replace `scripts/setup-ide` with the wrapper from the design's API Contracts section. Keep the comment that names `--dry-run` and `--write-lint`. Keep the file executable.
  - [ ] Success: `bash scripts/setup-ide --capabilities` prints `dry-run write-lint root`.

- [ ] **4. Test the skeleton and the wrapper**
  - [ ] `pytest tests/setup_ide -q -k "capabilities or root_missing_directory or root_without_value or no_target or unknown_target or harness"` → all pass. Fix the Python, never the test.
  - [ ] Write the wrapper tests in a new `tests/setup_ide/test_wrapper.py`. Use plain asserts on the exit code and stderr, not snapshots. Use the harness's `run(..., env_extra=...)` to override `PATH`, and write `python3` stubs into a temp folder.
    - [ ] Python missing: `PATH` is only an empty temp folder → exit 1; stderr contains `python3 not found`; no files written in the project.
    - [ ] Python too old: a stub `python3` that prints `3.8.10` and exits 1 → exit 1; stderr contains `found 3.8.10`.
    - [ ] Python fails to run: a stub that prints nothing and exits 1 → exit 1; stderr contains `did not run`.
    - [ ] Bare filename: run `bash setup-ide --capabilities` with `cwd=<guide>/scripts` → prints `dry-run write-lint root`.
    - [ ] No bytecode: after a `--capabilities` run (which imports the package), there is no `__pycache__` under `<guide>/scripts`.
    - [ ] Literals: the wrapper text contains `--dry-run` and `--write-lint`.
  - [ ] Success: the selected tests and `test_wrapper.py` pass.
  - [ ] Commit: `feat: add setup-ide Python package skeleton and wrapper`

### Building blocks

- [ ] **5. `frontmatter.py`**
  - [ ] Port `validate_frontmatter`, `has_always_apply`, `convert_paths_to_globs`, `strip_name_field`, `get_frontmatter_field` and `get_apply_to`.
  - [ ] Reproduce the awk and grep matching exactly, line by line, including the unanchored `grep -q "description:"` checks.
  - [ ] Keep the default-glob newline from `get_apply_to`, with a `# #40` comment.
  - [ ] These have no black-box test on their own. Tasks 11–14 cover them.
  - [ ] Success: ruff clean. Each function has a docstring line naming the bash function it ports.
  - [ ] Commit: `feat: port setup-ide frontmatter helpers`

- [ ] **6. `exclude.py`**
  - [ ] Port `read_rules_exclude`:
    - [ ] The env var `CONTEXT_FORGE_RULES_EXCLUDE` wins.
    - [ ] Otherwise, if `shutil.which("cf")` finds cf, run it with `cwd=project_root`. If `cf config get --help` mentions `--value`, run the `--value` form: exit 0 = value, 2 = none, anything else = red error on stderr and `SetupError`. Otherwise run the labeled form and parse the `Value:` line; a non-zero exit means none.
    - [ ] An `OSError` while starting cf is treated as a non-zero exit (see the design, "Errors").
    - [ ] No timeout.
  - [ ] Port `rule_is_excluded` (`fnmatch.fnmatchcase` on the basename; trim spaces around each pattern; record matched patterns), `warn_unmatched_exclusions` (stderr) and `always_apply_rule_matches`.
  - [ ] Wire it into `cli.main` in the bash order: read after root resolution, warn after the target run.
  - [ ] Success: `pytest tests/setup_ide -q -k cf_failure_stops_setup` passes. The other exclusion tests need a target and are covered in task 11.
  - [ ] Commit: `feat: port setup-ide rules.exclude handling`

- [ ] **7. `manifest.py`**
  - [ ] `cksum(data: bytes) -> tuple[int, int]`: POSIX CRC-32 (polynomial 0x04C11DB7, not reflected, length bytes folded in, result inverted), with a 256-entry table built once.
  - [ ] Port `legacy_manifest_entries` (copy the checksum lines exactly), `begin_manifest`, `record_installed_file`, `install_file` (same three warning messages), `finish_manifest` and `remove_empty_install_dirs`. The new manifest is held in memory, not in temp files.
  - [ ] Write manifest lines sorted by path in byte order (see the design, "State Management").
  - [ ] Success: checksums match the system `cksum` exactly. For each file, run `cksum < FILE` and compare it with the module's output (run with `PYTHONPATH=scripts`):
    - [ ] `tests/setup_ide/fixture_data/analyze-SKILL.md` must give `4163870229 9896`, the legacy entry.
    - [ ] An empty file.
    - [ ] `scripts/setup_ide/manifest.py` itself.
  - [ ] No separate unit test. The suite never imports setup-ide code, and from task 11 on the manifest snapshots and `test_ownership_legacy_analyze_skill_*` fail on any CRC difference.
  - [ ] Commit: `feat: port setup-ide install manifest and cksum`

- [ ] **8. `managed.py`**
  - [ ] Port `managed_state` (absent, unmanaged, legacy, broken, managed), `backup_premanaged_file` and `write_managed_section`, with all four write branches and the same messages.
  - [ ] Bytes outside the block pass through untouched. The exception is the final-newline add in the `managed` branch, which is reproduced with a `# #38` comment.
  - [ ] Write to `<file>.context-forge.tmp` first, then rename into place.
  - [ ] Covered by `test_managed_sections` in tasks 11 and 12.
  - [ ] Success: ruff clean.
  - [ ] Commit: `feat: port setup-ide managed sections`

- [ ] **9. `lint.py`**
  - [ ] Port all of `setup-ide-lint.sh`: `lint_missing_requirements`, `lint_report`, `lint_write_or_suggest`, `pyproject_ruff_sections`, the four `lint_check_*` functions and `check_lint_configs`.
  - [ ] Read from `project_root` and write to `target_root`.
  - [ ] Excluded languages are skipped through `exclude.rule_is_excluded`.
  - [ ] Covered by `test_lint` in task 11.
  - [ ] Success: ruff clean.
  - [ ] Commit: `feat: port setup-ide lint config check`

### Targets

- [ ] **10. Claude building blocks: `compile.py` and the copiers**
  - [ ] `compile.py`: port `compile_always_on_rules` and `compile_claude_rules`. They use `has_always_apply`, `strip_name_field`, `get_frontmatter_field` and `get_apply_to` (frontmatter), `rule_is_excluded` (exclude), and `write_managed_section` (managed).
  - [ ] `targets.py`: port `copy_files`, `copy_skills` and `copy_claude_modular_rules`. They write through `manifest.install_file`.
  - [ ] Success: ruff clean. Every bash function from `compile_claude_rules` through `copy_claude_modular_rules` (bash lines 545–852 and 921–1018) has a Python counterpart, or is noted as merged into one.
  - [ ] Commit: `feat: port setup-ide rule compilation and copiers`

- [ ] **11. Claude target: `setup_claude` and `install_target`**
  - [ ] Port `setup_claude`, including the stale "(general, git)" note with a comment.
  - [ ] Complete `install_target`: begin manifest → target setup → finish manifest → blank line → lint check. Replace the `claude` placeholder branch.
  - [ ] Test: these pass:
    ```
    pytest tests/setup_ide -q -k "fresh and claude or CLAUDE-claude or subdirectory or managed and claude or ownership or rules_exclude or lint or root_outside_guide or real_guide and claude"
    ```
    If a selected test runs a target other than claude (check its args), note it and confirm it in tasks 12–14.
  - [ ] Commit: `feat: port setup-ide claude target`

- [ ] **12. Agents target**
  - [ ] Port `rules_dir_display_path`, `emit_agents_md` and `setup_agents`. Replace the `agents` placeholder branch.
  - [ ] Test: `pytest tests/setup_ide -q -k "agents and not cursor"` → all pass. This includes the `codex`/`openai` aliases, `test_managed_sections[...agents]` and `real_guide[agents]`.
  - [ ] Commit: `feat: port setup-ide agents target`

- [ ] **13. Copilot target**
  - [ ] Port `emit_copilot_instruction_files`, `remove_generated_prompt_files` and `setup_copilot`. Replace the `copilot` placeholder branch.
  - [ ] If `targets.py` passes ~300 lines, split it by target (for example, `targets_copilot.py`). Don't merge modules.
  - [ ] Test: `pytest tests/setup_ide -q -k "copilot"` → all pass.
  - [ ] Commit: `feat: port setup-ide copilot target`

- [ ] **14. Cursor target**
  - [ ] Port `copy_cursor_rules` and `setup_cursor`, including the superseded-`.mdc` removal and the `.cursor/agents/` warning. Replace the `cursor` placeholder branch.
  - [ ] Test: `pytest tests/setup_ide -q -k "cursor"` → all pass.
  - [ ] Commit: `feat: port setup-ide cursor target`

### Dry run

- [ ] **15. `dryrun.py`**
  - [ ] Port `dry_run_install`:
    - [ ] Copy the existing `INSTALL_PATHS` entries into a `tempfile.TemporaryDirectory` with `shutil.copytree(..., symlinks=True)`, skipping `.claude/worktrees`.
    - [ ] Run `install_target` with a `Run` whose `target_root` is the sandbox and whose reporter buffers.
    - [ ] Print the header, then only the buffered lines that contain `⚠️`, `⊘` or `❌`.
  - [ ] Port `list_install_files` and `report_dry_run_changes`: byte-order sort, `+`/`~`/`-` lines, the count line or "No changes".
  - [ ] Replace the dry-run placeholder branch in `cli` with a call to the dry run. After this, no `not ported yet` is left: `grep -rn "not ported yet" scripts/setup_ide` → no hits.
  - [ ] Test: `pytest tests/setup_ide -q -k "dry_run or before_target"` → all pass.
  - [ ] Commit: `feat: port setup-ide dry run`

### Verification and cleanup

- [ ] **16. Full suite and snapshot check**
  - [ ] `pytest tests/setup_ide -q` → all pass (76 slice 120 tests plus `test_wrapper.py`).
  - [ ] `pytest tests/setup_ide -q --update-snapshots`, then `git status --short tests/` → empty. If anything shows, revert it with `git checkout tests/`, then fix the Python.
  - [ ] Confirm no existing snapshot or test file changed on the branch: `git diff main --stat -- tests/` lists only the new `test_wrapper.py`.
  - [ ] Success: all three hold.

- [ ] **17. Mutation check**
  - [ ] Change `MANAGED_BEGIN` in `context.py`, run the suite, and expect many failures. Revert.
  - [ ] Make `install_file`'s no-manifest branch overwrite instead of skip. Expect `test_ownership_no_manifest_differing_file_skipped` to fail. Revert.
  - [ ] Success: both mutations fail as expected, and `git status` is clean afterwards.

- [ ] **18. Remove `setup-ide-lint.sh`**
  - [ ] `git rm scripts/setup-ide-lint.sh`.
  - [ ] `grep -rn "setup-ide-lint" --include='*.md' --include='*.py' --include='*.sh' . | grep -v project-documents/user` → no hits. Fix any that remain.
  - [ ] Suite still all green.
  - [ ] Commit: `refactor: remove setup-ide-lint.sh, ported to setup_ide/lint.py`

- [ ] **19. Code checks**
  - [ ] `ruff check scripts/setup_ide tests && ruff format --check scripts/setup_ide tests` → clean.
  - [ ] `wc -l scripts/setup_ide/*.py`: no module over 350 lines. Split any that are.
  - [ ] `grep -nE "except( *\(.*)?Exception|except *:" scripts/setup_ide/*.py` → no hits. `cli.main` names `SetupError` and `KeyboardInterrupt`, nothing broader. `grep -n "shell=True" scripts/setup_ide/*.py` → no hits.
  - [ ] Constants defined once: `grep -n "context-forge\|pre-context-forge" scripts/setup_ide/*.py | grep -v context.py` shows no literal marker or suffix strings, only comments.
  - [ ] Each reproduced quirk has its comment: `grep -n "#38\|#40" scripts/setup_ide/*.py` shows at least one hit for each.
  - [ ] Commit any fixes: `refactor: tidy setup_ide modules`

- [ ] **20. Docs**
  - [ ] `readme.setup-ide.md`: add a short "Requirements" note: Python 3.9 or newer as `python3`, the error you get without it, and `xcode-select --install` on macOS.
  - [ ] `CHANGELOG.md` `[Unreleased]`: under `### Changed`, setup-ide now runs as Python 3.9+ (standard library only) behind the same `scripts/setup-ide` entry point, with no change to output or files written. One line noting that manifests written under a non-C locale on Linux may reorder once.
  - [ ] Commit: `docs: note Python 3.9 requirement for setup-ide`

- [ ] **21. Verification walkthrough**
  - [ ] Run steps 1–6 of the design's Verification Walkthrough. Step 5 needs a project installed with the bash version: use `git worktree add /tmp/apg-bash v0.20.9` and run its `scripts/setup-ide claude` in a scratch project. Then run the branch's `setup-ide claude --dry-run` in that project and expect `📋 No changes`. Remove the worktree afterwards.
  - [ ] Update the walkthrough in the design if any command or output differs from what's written.
  - [ ] Set the design's `status: complete` and this file's `status: complete`. Check off slice 121 in `120-slices.guide-tooling.md`.
  - [ ] Commit: `docs: complete slice 121 walkthrough and status`
  - [ ] Do not merge. Merging happens in Phase 7, after code review.
