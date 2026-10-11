---
docType: slice-design
slice: setup-ide-behavior-tests
project: ai-project-guide
parent: project-documents/user/architecture/120-slices.guide-tooling.md
dependencies: []
interfaces: [121, 122]
dateCreated: 20261011
dateUpdated: 20261011
status: not_started
review: none
---

# Slice Design: setup-ide-behavior-tests

## Overview

A black-box test suite for `scripts/setup-ide`. It runs the script the way cf does (`bash <guide>/scripts/setup-ide ...`) against throwaway projects, then compares the files written, the manifest, the output and the exit code with stored snapshots. Snapshots are taken from the current bash version. Slice 121 replaces the bash with Python and must pass this suite without changing a snapshot.

The slice also adds the repo's first Python dev setup: a ruff config, a pre-commit hook, and the export-ignore entries that keep all of it out of release tarballs.

## Value

- **For slice 121:** a fixed definition of "same behavior". Without it, the rewrite can only be checked by reading 1,760 lines of bash side by side with the Python.
- **For any setup-ide change, starting now:** setup-ide writes into users' projects, and it has no tests today. A regression in overwrite protection or pruning deletes or clobbers project files. The suite catches that before release.
- **For reviewers:** the snapshots show what setup-ide does for each case in a readable form, which is easier to check than the bash.

## Technical Scope

Included:
- `tests/setup_ide/`: pytest suite, helpers, a fixture guide, and snapshot files.
- Scenarios covering every target, flag, manifest and ownership path, rules.exclude source, managed-section state, and lint check listed under Implementation Details.
- A smoke test that runs each target against the real `project-guides/` with no snapshot.
- Repo dev setup: `ruff.toml` at the repo root, `.githooks/pre-commit`, `.gitattributes` and `.gitignore` entries, and `python.md` removed from `rules.exclude` in `.context-forge.toml`.

Excluded:
- Any change to `scripts/setup-ide` or `scripts/setup-ide-lint.sh`. Behavior that looks wrong gets recorded, not fixed (see Special Considerations).
- shellcheck fixes. The bash is replaced in 121, so it is not worth cleaning up.
- CI. There is none in this repo; the hook and a manual run cover it for now.
- The other scripts in `scripts/`.

## Dependencies

### Prerequisites
- Dev tools on the developer's machine: `python3` (3.9 or newer), `pytest`, `ruff`. None are needed to run setup-ide.
- The tools setup-ide already uses: `bash`, `awk`, `sed`, `cksum`, `tar`, `cmp`, `comm`, `find`, `mktemp`.

### Interfaces Required
- The setup-ide command line: targets, `--dry-run`, `--write-lint`, `--root`, `--capabilities`.
- The cf calls setup-ide makes for rules.exclude: `cf config get --help`, `cf config get --value rules.exclude`, and the older `cf config get rules.exclude` with its `Value:` line. Tests replace `cf` with a stub script.

## Architecture

### Component Structure

```
tests/
  README.md                  how to install dev tools, run tests, update snapshots
  setup_ide/
    conftest.py              fixtures and the --update-snapshots option
    harness.py               build guide and project, run setup-ide, take snapshot
    fixture_guide/           small stand-in for project-guides/
      rules/  agents/  skills/  lint/
    snapshots/               one .snap file per snapshot test
    test_targets.py
    test_flags.py
    test_ownership.py        manifest, overwrite protection, pruning, legacy entries
    test_rules_exclude.py
    test_managed_sections.py
    test_lint.py
    test_real_guide.py       smoke test against the real project-guides/
```

**Fixture guide.** Each test builds a temporary guide: a copy of the repo's whole `scripts/` directory, plus `fixture_guide/` as its `project-guides/`. setup-ide reads rules from `SCRIPT_DIR/../project-guides`, so it uses the fixture rules, and the snapshots don't change whenever a real rule is edited. Copying all of `scripts/` means the Python package added in 121 is picked up with no harness change.

The fixture guide has:
- `rules/`: two always-on rules (the stand-ins for `general.md` and `git.md`), two scoped rules with `paths:` lists (one carries a `name:` field), and one rule with broken frontmatter.
- `agents/`: one agent.
- `skills/`: one skill folder with a `SKILL.md`, and one flat `.md` file (setup-ide must warn about it and skip it).
- `lint/`: minimal baselines and `required` files for each language.

**Fixture projects** are built in code, inside each test, under pytest's `tmp_path`. None are stored as file trees in the repo. A stored tree would put `CLAUDE.md` and `.claude/` folders inside this repo, and Claude Code would load them as if they were real config.

The layout matches a real install: `<tmp>/project/project-documents/ai-project-guide/` holds the guide, and setup-ide runs with the project as its working directory. `--root` tests put the guide in a different directory from the project.

### Data Flow

1. The test builds the guide and the project, then optionally changes either one: drops a rule, edits an installed file, writes a manifest from an earlier run.
2. `harness.run(project, args, cwd=..., env=...)` runs `bash <guide>/scripts/setup-ide <args>` and returns the exit code, stdout and stderr.
3. `harness.snapshot(project, result)` returns one text block: the exit code, stdout and stderr after normalization, then every file under the install paths in sorted order, each with its full contents.
4. The test compares that block with `snapshots/<test>.snap`. Run with `--update-snapshots` to rewrite the file instead.

Most scenarios are two runs (install, then change something, then run again), and the snapshot covers both runs.

### State Management

Each test works only in its own `tmp_path`. Nothing is written into this repo except snapshot files, and only with `--update-snapshots`.

The environment for each run is fixed:
- `PATH` is the stub directory plus `/usr/bin:/bin`, so neither a real `cf` nor Homebrew tools are found.
- `CONTEXT_FORGE_RULES_EXCLUDE` is removed unless the test sets it.
- `LC_ALL=C`.
- `HOME` points into `tmp_path`.

## Technical Decisions

### Technology Choices
- **pytest.** `rules/python.md` says to use pytest only. It is a dev tool, like ruff, and setup-ide never needs it to run.
- **Black-box tests.** Tests only run the script as a separate process and never import its code. That's what lets the same suite check both the bash and the Python versions.
- **Hand-rolled snapshots.** About 30 lines in `harness.py`, plus a pytest option. The format is plain text that diffs well. syrupy and similar plugins would add a dependency to save very little code.
- **A stub `cf`.** A short shell script, written into the stub directory by a fixture. It is set up to answer `--help` with or without `--value` and to return a chosen value, exit 2, or exit 1.

### Patterns and Conventions

**Snapshot format.** One `.snap` file per test:

```
== run 1: setup-ide claude
exit: 0
-- stdout
<normalized lines>
-- stderr
<normalized lines>
== files
--- .claude/rules/scoped-a.md
<contents>
--- .context-forge/claude.manifest
<contents>
```

**Normalization.** Applied to stdout and stderr only, never to file contents:
- ANSI color codes are stripped.
- The project root becomes `<ROOT>`, the guide directory becomes `<GUIDE>`, and anything else under the system temp directory (dry-run sandboxes, `mktemp` files) becomes `<TMP>`.

File contents are compared byte for byte. That includes the manifest: cf reads it with its own cksum code, so its format is a contract.

**Install paths.** The snapshot covers the same paths setup-ide's dry run compares: `CLAUDE.md`, `AGENTS.md`, their `.pre-context-forge` backups, `.claude`, `.cursor`, `.github`, `.agents`, `.context-forge`, and the lint config files. Files the project created itself are listed too, so a test that should leave a file alone also shows that it did.

**Test names.** `test_<area>_<case>`, for example `test_ownership_edited_file_kept`. The snapshot file has the same name as the test.

## Implementation Details

### Scenario list

Every item below is a test with a snapshot unless marked (assert).

**Targets** (`test_targets.py`)
- Fresh install for each of `claude`, `cursor`, `copilot`, `agents`.
- `codex`, `openai` and `CLAUDE` (upper case) give the same files as `agents` and `claude`. (assert: equal to the reference run)
- Running from a subdirectory of the project writes to the project root.
- No target, or an unknown target: usage text, exit 1.
- A flat skill file gets a warning and is skipped. A skill folder is copied.
- A rule with broken frontmatter: whatever setup-ide does today, recorded as is.

**Flags** (`test_flags.py`)
- `--capabilities` prints `dry-run write-lint root` and exits 0. (assert: the exact line; cf depends on it)
- `--dry-run` on a fresh project lists `+` lines, and the project is unchanged afterwards. (assert: the file tree before and after is identical)
- `--dry-run` after an install, with nothing changed: "No changes".
- `--dry-run` when the guide changed (one rule added, one edited, one dropped): `+`, `~` and `-` lines.
- `--root <dir>` with the guide outside `<dir>`. `--root=<dir>` form too.
- `--root` with a missing directory, and `--root` with no value: error, exit 1.
- Flags placed before the target as well as after it.

**Ownership** (`test_ownership.py`)
- Running twice gives the same files and manifest.
- No manifest, and a file that differs from the guide's version: skipped with a warning, file kept (#34).
- No manifest, and a file identical to the guide's version: adopted into the manifest.
- A manifest exists and a differing file is not listed in it: skipped with a warning.
- A file installed earlier and edited since: kept with a warning, and its old manifest line is carried over.
- A rule dropped from the guide: removed, and folders it leaves empty are removed too.
- A rule dropped from the guide that was edited after install: kept with a warning.
- Legacy entries: a `.claude/skills/analyze/SKILL.md` matching a shipped checksum is removed. One that doesn't match is kept.

**rules.exclude** (`test_rules_exclude.py`)
- Set by the `CONTEXT_FORGE_RULES_EXCLUDE` env var, which wins over cf.
- cf with `--value`: the rule is excluded.
- cf with `--value`, exit 2 (unknown key): no exclusions.
- cf with `--value`, exit 1: setup-ide exits 1.
- Older cf without `--value`: the `Value:` line is parsed.
- No cf on PATH: no exclusions.
- A pattern that matches nothing: warning.
- A pattern that matches an always-on rule: whatever setup-ide does today.
- A rule installed earlier and now excluded: pruned.

**Managed sections** (`test_managed_sections.py`), for `CLAUDE.md` (claude) and `AGENTS.md` (agents):
- File absent.
- File present with no markers: backed up, block appended.
- Running again after that: the backup is not overwritten.
- BEGIN/END block present: only the block is replaced. Content above and below it is byte-identical, including CRLF line endings and a missing final newline.
- Legacy marker that runs to the end of the file: migrated, and a duplicated H1 is dropped.
- Legacy marker plus a hand-added end marker: content after the end marker is kept (#33).
- Broken markers (two BEGIN lines, or END before BEGIN): error, file unchanged.

**Target-specific cleanup**
- copilot: generated `.github/prompts/*.prompt.md` files are removed, and hand-written ones are kept. The instruction files carry the generated marker.
- cursor: an `.mdc` for a rule that is now always-on is removed. An existing `.cursor/agents/` folder triggers its warning.

**Lint** (`test_lint.py`)
- Python: no config gives a report. `--write-lint` writes the baseline. A `[tool.ruff]` section missing required rules plus `--write-lint` adds a `ruff.toml` with `extend`. A complete config gives no report.
- Dart, TypeScript and C# (with `*.csproj` three levels deep, and four levels deep): report, and write with `--write-lint`.
- A language whose rule file is in rules.exclude is not checked.

**Real guide** (`test_real_guide.py`, assert only)
- Each target against the real `project-guides/` exits 0, prints no `❌` line, and writes its expected top-level files.

## Integration Points

### Provides to Other Slices
- **121:** the pass/fail gate. 121 is done when `pytest tests/setup_ide` passes with no snapshot changed. If 121 has to change behavior on purpose, that change gets its own commit, which updates the affected snapshots and says why.
- **122:** the real-guide smoke test, and a running harness to use against a real consumer project.
- **Any later setup-ide change,** such as the shipped-version checksum adoption in Future Work: snapshots show exactly which behavior changed.

### Consumes from Other Slices
Nothing. This slice only reads the current `scripts/` folder.

## Success Criteria

### Functional Requirements
- Every scenario under Implementation Details exists and passes against the current bash setup-ide.
- `pytest tests/setup_ide --update-snapshots` run twice in a row leaves no diff, so the snapshots are deterministic.
- Breaking setup-ide on purpose makes the suite fail. Two checks: change `MANAGED_BEGIN`, and make `install_file` overwrite without checking the manifest. Both changes are reverted afterwards.
- No real `cf` and no user environment variable can reach a test run.

### Technical Requirements
- `ruff check tests` and `ruff format --check tests` are clean under the repo `ruff.toml`.
- Test files stay around 300 lines each; helper functions around 50.
- `git archive HEAD` contains nothing from `tests/`, `.githooks/` or `ruff.toml`.
- No file under `scripts/` changes.

### Integration Requirements
- The pre-commit hook rejects a commit that adds a staged `.py` file failing ruff, and lets it through once the file is fixed. If ruff is not installed, the hook fails with a message saying so.
- `setup-ide claude`, run in this repo with `python.md` no longer excluded, installs `.claude/rules/python.md` here.

### Verification Walkthrough

1. Install the dev tools once, if they are missing:
   ```bash
   uv tool install pytest && uv tool install ruff   # or pipx
   git config core.hooksPath .githooks
   ```
2. Run the suite from the repo root:
   ```bash
   pytest tests/setup_ide -q
   ```
   Expected: every test passes, about 60 of them.
3. Check that the snapshots are stable:
   ```bash
   pytest tests/setup_ide -q --update-snapshots && git status --short tests/
   ```
   Expected: no output from `git status`.
4. Check that the suite catches a regression. Change `MANAGED_BEGIN` in `scripts/setup-ide` to `'<!-- BEGIN:cf -->'`, run step 2, and see the managed-section and target tests fail with snapshot diffs. Then:
   ```bash
   git checkout scripts/setup-ide
   ```
5. Check that nothing dev-only ships:
   ```bash
   git archive HEAD | tar -t | grep -E '^(tests/|\.githooks/|ruff\.toml)'
   ```
   Expected: no output.
6. Check the hook. Stage a `.py` file that ruff rejects, such as one with an unused import, and run `git commit`. Expected: the commit is rejected with ruff's output.

## Risk Assessment

### Technical Risks
- **The snapshots record a bug as correct behavior.** A characterization suite records what the script does today, bugs included.
- **Platform differences.** Snapshots are taken on macOS (bash 3.2, BSD tools). Linux (bash 5, GNU tools) could differ in output or in the order of dry-run lines. With no CI, Linux is untested.

### Mitigation Strategies
- While writing tests, anything that looks like a bug is listed in `tests/README.md` under "Recorded quirks", with the test name, and filed as an issue. The snapshot keeps the current behavior. A fix goes into a later commit that updates that snapshot.
- Fixed `LC_ALL=C` and path normalization take away the most likely sources of difference. Linux is checked by hand in slice 122.

## Implementation Notes

### Development Approach
1. Dev setup first: `ruff.toml` (`extend` the baseline at `project-guides/lint/python/ruff.toml`, `target-version = "py39"`), `.githooks/pre-commit`, the `.gitattributes` and `.gitignore` entries, and the `.context-forge.toml` change.
2. `harness.py` and `conftest.py`: build guide, build project, run, normalize, snapshot, the update option, and the stub `cf`. Prove them with the `--capabilities` test and one fresh claude install.
3. The fixture guide.
4. Test files in this order: targets, flags, ownership, managed sections, rules.exclude, lint, real guide. Ownership and managed sections protect user data, so they come early.
5. The determinism check (step 3 of the walkthrough) and the mutation check (step 4).
6. `tests/README.md`.

### Special Considerations
- **Never edit a snapshot by hand.** Snapshots are only written by `--update-snapshots` against the current script. A hand edit could hide a real difference.
- **Hidden temp paths.** Dry run builds its sandbox with `mktemp`, and some lint messages print absolute paths. Normalization has to catch every temp path, or runs will differ from one another. The determinism check catches any it misses.
- **The new `project-documents/` folder in this repo.** setup-ide finds the project root by walking up from the current directory to the first `project-documents/` folder. Now that this repo has one, a submodule install run from inside its guide folder stops at the guide itself, not the project. Tarball installs are not affected, because the folder is export-ignored. The harness runs from the project root or `--root`, which matches how cf and the README run it, so the tests don't depend on this. Recorded as a quirk.
- **Python version.** setup-ide targets Python 3.9 (see the architecture doc), which is older than the 3.12+ in `python.md`. The exception is deliberate: setup-ide runs on users' machines, and 3.9 is what macOS command line tools ship. The tests follow the same `target-version` so that the repo has one ruff config.
