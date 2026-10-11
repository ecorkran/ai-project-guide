---
docType: tasks
slice: setup-ide-behavior-tests
project: ai-project-guide
lld: user/slices/120-slice.setup-ide-behavior-tests.md
dependencies: []
projectState: setup-ide is ~1,760 lines of bash with no tests; repo has no Python, no ruff config, no hooks
dateCreated: 20261011
dateUpdated: 20261011
status: not_started
---

## Context Summary
- Working on slice 120, setup-ide-behavior-tests. Design: `project-documents/user/slices/120-slice.setup-ide-behavior-tests.md` (called "the design" below).
- Build a black-box pytest suite that runs `bash <guide>/scripts/setup-ide` against throwaway projects and compares the files written, the manifest and the output with stored snapshots. The snapshots are taken from the current bash version.
- Also add the repo's first Python dev setup: ruff config, pre-commit hook, export-ignore entries.
- **Do not change anything under `scripts/`.** If behavior looks wrong, snapshot it as it is and record it (task 13).
- Dev tools are installed: `python3` (3.13), `pytest`, `ruff` 0.17. setup-ide targets Python 3.9, and the tests do too.
- Work on branch `120-slice.setup-ide-behavior-tests`, forked from `main`. No integration branch is configured.
- Next slice: 121, which rewrites setup-ide in Python and must pass this suite without any snapshot changing.

## Tasks

### Setup

- [ ] **1. Create the slice branch**
  - [ ] Confirm `cf config get git.integration_branch` is empty, so the target is `main`.
  - [ ] `git checkout -b 120-slice.setup-ide-behavior-tests main`
  - [ ] Success: `git branch --show-current` prints `120-slice.setup-ide-behavior-tests`.

- [ ] **2. Add the repo ruff config**
  - [ ] Create `ruff.toml` at the repo root. It contains `extend = "project-guides/lint/python/ruff.toml"` and `target-version = "py39"`.
  - [ ] Success: `ruff check tests` runs. It may find no files yet, but it must not report a config error.

- [ ] **3. Add the pre-commit hook**
  - [ ] Create `.githooks/pre-commit` (bash, executable). It runs `ruff check` and `ruff format --check` on staged `.py` files only, and exits 0 when none are staged.
  - [ ] If `ruff` is not on PATH, it prints `ruff not found; install it (uv tool install ruff)` and exits 1. No silent skip.
  - [ ] Run `git config core.hooksPath .githooks` locally.
  - [ ] Success: staging a `.py` file that has an unused import makes `git commit` fail with ruff's output. Fixing the file lets the commit through. Unstage and delete the probe file afterwards.

- [ ] **4. Add the git attribute, ignore and cf config entries**
  - [ ] `.gitattributes`: add `tests/`, `.githooks/` and `ruff.toml`, each with `export-ignore`.
  - [ ] `.gitignore`: add `__pycache__/`, `.pytest_cache/` and `.ruff_cache/`.
  - [ ] `.context-forge.toml`: remove `python.md` from `rules.exclude` and leave the other entries unchanged.
  - [ ] Success: `git archive HEAD | tar -t | grep -E '^(tests/|\.githooks/|ruff\.toml)'` prints nothing once these files are committed.

- [ ] **5. Install python.md into this repo**
  - [ ] Run `./scripts/setup-ide claude` from the repo root.
  - [ ] Success: `.claude/rules/python.md` exists, and `git diff CLAUDE.md` shows no unexpected changes.

- [ ] **6. Commit the dev setup**
  - [ ] `chore: add ruff config, pre-commit hook and test export-ignore`

### Harness

- [ ] **7. Create the fixture guide** in `tests/setup_ide/fixture_guide/`. See the design, "Component Structure". Keep each file short (frontmatter plus a few lines), so snapshots stay readable.
  - [ ] `rules/always-a.md` and `rules/always-b.md`: `alwaysApply: true`, each with a `description`.
  - [ ] `rules/scoped-a.md`: `paths:` list with two entries, plus a `name:` field.
  - [ ] `rules/scoped-b.md`: `paths:` list with one entry, and no `name:`.
  - [ ] `rules/broken.md`: frontmatter with no `description`.
  - [ ] `agents/agent-a.md`: one agent.
  - [ ] `skills/skill-a/SKILL.md`: a skill folder.
  - [ ] `skills/flat-skill.md`: a flat file, which setup-ide should warn about and skip.
  - [ ] `lint/{python,dart,typescript,csharp}/`: copy the file names `setup-ide-lint.sh` expects from `project-guides/lint/`. Trim the baselines to a few lines, and keep each `required` file's format exactly as the real one.
  - [ ] Success: `find tests/setup_ide/fixture_guide -type f` lists every file above.

- [ ] **8. Write `harness.py`: building the guide and the project**
  - [ ] `make_guide(dest)`: copies the repo's whole `scripts/` folder to `dest/scripts/` and `fixture_guide/` to `dest/project-guides/`, then returns `dest`.
  - [ ] `make_project(tmp_path)`: creates `project/project-documents/`, puts the guide at `project/project-documents/ai-project-guide/` with `make_guide`, and returns both paths.
  - [ ] `write_files(root, {relpath: content})`: a helper for arranging a project state. It accepts `bytes` so tests can set CRLF line endings and a missing final newline.
  - [ ] Success: covered by task 11.

- [ ] **9. Write `harness.py`: running setup-ide and normalizing output**
  - [ ] `run(guide, args, cwd, env_extra=None)`: runs `bash <guide>/scripts/setup-ide *args` and returns exit code, stdout and stderr. The environment is built from scratch, per the design's "State Management": `PATH=<stubdir>:/usr/bin:/bin`, `LC_ALL=C`, `HOME=<tmp>`, with nothing inherited except what is listed. `CONTEXT_FORGE_RULES_EXCLUDE` is only set when `env_extra` provides it.
  - [ ] `normalize(text, root, guide)`: strips ANSI escape codes, replaces `root` with `<ROOT>` and `guide` with `<GUIDE>`, then replaces any remaining path under the system temp directory with `<TMP>`. Real temp paths on macOS have a `/private` prefix, so handle `/private/var/...` and `/var/...` both.
  - [ ] Success: covered by task 11.

- [ ] **10. Write `harness.py` snapshots and `conftest.py`**
  - [ ] `snapshot(project_root, runs)`: builds the text block shown in the design under "Snapshot format". It includes every run (label, exit code, normalized stdout and stderr), then every file under the install paths, sorted, with full contents. Install paths: `CLAUDE.md`, `AGENTS.md`, both `.pre-context-forge` backups, `.claude`, `.cursor`, `.github`, `.agents`, `.context-forge`, and the lint config names from `setup-ide-lint.sh`. Skip anything under `project-documents/`.
  - [ ] File contents are compared exactly. Decode as UTF-8, and render CR characters visibly (for example `\r`) so CRLF differences show up in diffs.
  - [ ] `conftest.py`: adds the `--update-snapshots` option, and an `assert_snapshot(name, text)` fixture that compares with `snapshots/<name>.snap` or writes it. A missing snapshot fails unless `--update-snapshots` is given.
  - [ ] `conftest.py`: a `cf_stub` fixture that writes an executable `cf` into the stub directory. It takes the `--help` text (with or without `--value`), the value to print, and the exit code.
  - [ ] Success: covered by task 11.

- [ ] **11. Test the harness**
  - [ ] `test_harness.py`: `normalize` strips ANSI codes and replaces root, guide and temp paths (both the `/private` and plain forms).
  - [ ] `test_harness.py`: `snapshot` lists files in sorted order, includes project-created files under the install paths, and shows `\r`.
  - [ ] `test_harness.py`: a missing snapshot fails without `--update-snapshots`.
  - [ ] `test_flags.py::test_flags_capabilities`: stdout is exactly `dry-run write-lint root\n` and the exit code is 0. This is an assertion, not a snapshot.
  - [ ] `test_targets.py::test_targets_claude_fresh`: the first snapshot test.
  - [ ] Success: `pytest tests/setup_ide -q` passes. Running `--update-snapshots` twice in a row leaves `git status --short tests/` empty.

- [ ] **12. Commit the harness**
  - [ ] `test: add setup-ide test harness and fixture guide`

### Scenarios

For each test file below, list the scenarios in the design under "Scenario list". Write each test, generate its snapshot with `--update-snapshots`, then **read the snapshot** to confirm it shows the behavior the test name claims. A snapshot that records an error the test didn't intend means the test setup is wrong. Fix the setup, not the snapshot.

- [ ] **13. Create the quirks log**
  - [ ] Create `tests/README.md` with three parts: dev tool install (`uv tool install pytest ruff`, `git config core.hooksPath .githooks`), running the suite and updating snapshots (including the rule that snapshots are never hand-edited), and an empty "Recorded quirks" section.
  - [ ] From here on, any behavior that looks like a bug gets one entry under "Recorded quirks": the test name and one sentence. Add the `project-documents/` walk-up quirk from the design now.
  - [ ] Success: the file exists and has all three parts.

- [ ] **14. Target tests** (`test_targets.py`)
  - [ ] Fresh install for `cursor`, `copilot` and `agents`. `claude` is already done in task 11.
  - [ ] `codex` and `openai` produce the same snapshot files as `agents`, and `CLAUDE` the same as `claude`. Assert by comparing file trees, with no separate snapshots.
  - [ ] Running from `project/src/` installs into the project root.
  - [ ] No target, and an unknown target: exit 1 with usage.
  - [ ] Flat skill warned and skipped, skill folder copied. Check the claude snapshot for both.
  - [ ] `broken.md`: snapshot whatever happens today.
  - [ ] Success: `pytest tests/setup_ide/test_targets.py -q` passes.

- [ ] **15. Flag tests** (`test_flags.py`)
  - [ ] `--dry-run` on a fresh project: `+` lines, and the project tree before and after is identical (assert).
  - [ ] `--dry-run` after an install with nothing changed: "No changes".
  - [ ] `--dry-run` after changing the guide in place (add a scoped rule, edit `scoped-a.md`, delete `scoped-b.md`): one `+`, one `~` and one `-` line.
  - [ ] `--root <dir>` and `--root=<dir>`, with the guide in a different directory from `<dir>`.
  - [ ] `--root` with a missing directory, and `--root` with no value: exit 1.
  - [ ] A flag before the target (`--dry-run claude`) gives the same result as after it.
  - [ ] Success: `pytest tests/setup_ide/test_flags.py -q` passes.

- [ ] **16. Commit targets and flags**
  - [ ] `test: add setup-ide target and flag scenarios`

- [ ] **17. Ownership tests** (`test_ownership.py`). These protect users' files, so read each snapshot carefully.
  - [ ] Running twice gives identical files and manifest.
  - [ ] No manifest, and a differing `.claude/rules/scoped-a.md`: skipped with a warning, and the content is unchanged.
  - [ ] No manifest, and an identical file: adopted, so it is listed in the manifest.
  - [ ] Manifest present, and a differing file it does not list: skipped with a warning.
  - [ ] An installed file edited afterwards: kept with a warning, and the manifest still has its original line.
  - [ ] A rule deleted from the guide between runs: the file is removed, and so is any folder it leaves empty.
  - [ ] A rule deleted from the guide after the installed copy was edited: kept with a warning.
  - [ ] Legacy entry: `.claude/skills/analyze/SKILL.md` whose cksum and size match an entry in `legacy_manifest_entries` is removed. One that doesn't match is kept. For matching content, store the shipped copy as `tests/setup_ide/fixture_data/analyze-SKILL.md`. Recover it with `git show 9a510f0^:project-guides/skills/analyze/SKILL.md` (verified: `cksum` gives `4163870229 9896`).
  - [ ] Success: `pytest tests/setup_ide/test_ownership.py -q` passes.

- [ ] **18. Managed-section tests** (`test_managed_sections.py`). Parametrize over `claude`/`CLAUDE.md` and `agents`/`AGENTS.md`.
  - [ ] File absent.
  - [ ] Present with no markers: `.pre-context-forge` backup created, block appended.
  - [ ] Second run after that: the backup content is still the original.
  - [ ] BEGIN/END present, with CRLF content above and below and no final newline: only the block changes. Assert the bytes outside the block are identical, in addition to the snapshot.
  - [ ] Legacy marker running to EOF with a matching H1 on line 1: migrated, and the H1 is not duplicated.
  - [ ] Legacy marker plus a `[//]: # (context-forge:managed end)` line: content after it is kept (#33).
  - [ ] Two BEGIN lines, and END before BEGIN: error message, and the file is unchanged (assert the bytes).
  - [ ] Success: `pytest tests/setup_ide/test_managed_sections.py -q` passes.

- [ ] **19. Commit ownership and managed sections**
  - [ ] `test: add setup-ide ownership and managed-section scenarios`

- [ ] **20. rules.exclude tests** (`test_rules_exclude.py`). Use the `cf_stub` fixture. Exclude `scoped-b.md` unless a case says otherwise.
  - [ ] Env var set, plus a cf stub that returns a different value: the env var wins.
  - [ ] cf `--help` shows `--value`, value `scoped-b.md`, exit 0: excluded.
  - [ ] cf with `--value`, exit 2: nothing excluded.
  - [ ] cf with `--value`, exit 1: setup-ide exits 1.
  - [ ] cf without `--value` in `--help`, and labeled output with a `Value:   scoped-b.md` line: excluded.
  - [ ] No cf on PATH: nothing excluded.
  - [ ] Pattern `nomatch*.md`: unmatched-pattern warning.
  - [ ] Pattern `always-a.md`: snapshot whatever happens today.
  - [ ] Install with nothing excluded, then run again with `scoped-b.md` excluded: the installed copy is pruned.
  - [ ] Success: `pytest tests/setup_ide/test_rules_exclude.py -q` passes.

- [ ] **21. Target-specific cleanup tests** (add to `test_targets.py`, or a new `test_cleanup.py` if `test_targets.py` would pass ~300 lines)
  - [ ] copilot: a `.github/prompts/x.prompt.md` with the generated marker is removed, and one without the marker is kept.
  - [ ] copilot: every `.github/instructions/*.instructions.md` carries the generated marker (check the snapshot).
  - [ ] cursor: a `.cursor/rules/always-a.mdc` from an earlier run is removed.
  - [ ] cursor: an existing `.cursor/agents/` folder produces its warning and is left in place.
  - [ ] Success: the file's tests pass.

- [ ] **22. Lint tests** (`test_lint.py`)
  - [ ] Python, no config: report only, nothing written.
  - [ ] Python, no config, `--write-lint`: the baseline is written.
  - [ ] Python, `pyproject.toml` with a `[tool.ruff]` that lacks required rules, `--write-lint`: a `ruff.toml` with `extend = "pyproject.toml"` and `extend-select` is added. `pyproject.toml` is unchanged.
  - [ ] Python, complete config: no report.
  - [ ] Dart (`pubspec.yaml`): report, then write with `--write-lint`.
  - [ ] TypeScript (`tsconfig.json`): report, then write with `--write-lint`.
  - [ ] C#, `*.csproj` three levels deep: detected. Four levels deep: not detected.
  - [ ] `python.md` in rules.exclude: Python is not checked. The fixture guide has no `python.md`, so add one to the test's guide copy for this case.
  - [ ] Success: `pytest tests/setup_ide/test_lint.py -q` passes.

- [ ] **23. Commit the remaining scenarios**
  - [ ] `test: add setup-ide rules.exclude, cleanup and lint scenarios`

- [ ] **24. Real-guide smoke test** (`test_real_guide.py`, assertions only)
  - [ ] For each target: copy the real `project-guides/` and `scripts/` into a temp guide, run the target on a fresh project, and check: exit code 0, no `❌` in the output, and the top-level files from the readme's target table exist.
  - [ ] Success: `pytest tests/setup_ide/test_real_guide.py -q` passes.

- [ ] **25. Commit the smoke test**
  - [ ] `test: add setup-ide real-guide smoke test`

### Verification

- [ ] **26. Full suite and determinism**
  - [ ] `pytest tests/setup_ide -q` passes. Record the test count in the design's Verification Walkthrough.
  - [ ] Run `pytest tests/setup_ide -q --update-snapshots` twice. `git status --short tests/` is empty after each run.
  - [ ] `ruff check tests` and `ruff format --check tests` are clean.
  - [ ] `git diff main --stat -- scripts/` is empty.

- [ ] **27. Mutation checks**
  - [ ] In `scripts/setup-ide`, change `MANAGED_BEGIN` to `'<!-- BEGIN:cf -->'`. The suite fails in the managed-section and target tests. Revert with `git checkout scripts/setup-ide`.
  - [ ] In `install_file`, make the no-manifest branch overwrite instead of skipping. The ownership tests fail. Revert.
  - [ ] Success: both mutations caught, and `git status --short scripts/` is empty.

- [ ] **28. Tarball check**
  - [ ] `git archive HEAD | tar -t | grep -E '^(tests/|\.githooks/|ruff\.toml|project-documents/)'` prints nothing.

- [ ] **29. Close out the slice**
  - [ ] Update the design's Verification Walkthrough with the actual commands, test count, and any corrections. Set the design's `status` to `complete` and its `dateUpdated`.
  - [ ] File an issue for each "Recorded quirks" entry, and link the issue numbers in `tests/README.md`.
  - [ ] Add a CHANGELOG `[Unreleased]` entry under `### Added`: setup-ide behavior test suite. This is dev-only, so no user-facing change.
  - [ ] Run `cf check` and fix any findings.
  - [ ] Commit `test: finalize setup-ide behavior tests (slice 120)` on the slice branch.
