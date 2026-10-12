---
docType: analysis
project: ai-project-guide
topic: setup-ide port findings
dateCreated: 20261011
dateUpdated: 20261011
status: complete
---

# setup-ide Port Findings

Exact behaviors of the bash `scripts/setup-ide` (v0.20.9) and `scripts/setup-ide-lint.sh` that a port has to reproduce to pass the slice 120 suite (`tests/setup_ide/`, 76 tests). They were collected by reading the bash for the cancelled Python port (slice 121). They hold for any target language, including cf's TypeScript port.

The suite runs with `LC_ALL=C` on macOS, so the reference behavior is macOS awk (version 20200816), BSD sed and bash 3.2 under the C locale.

## Text handling
- **Lines are awk records.** Split on `\n`. A final line without a newline is still a line, and every awk `print` writes it back with `\n`. CR stays part of the line, so `---\r` is not a frontmatter fence.
- **`print_status` uses `echo -e`.** Backslash escapes in messages (filenames, paths, exclusion patterns) are interpreted. Plain `echo` lines are not.
- **Command substitution** (`$(...)`) strips trailing newlines. Several values pass through it: titles, fields, `applyTo`, cf output.
- **Glob order:** `"$dir"/*.md` is sorted by locale. Under `LC_ALL=C` that is byte order. Dotfiles are skipped.

## Frontmatter helpers
- **`has_always_apply`:** the first `---` line opens frontmatter, and the second returns false. A line matching `^alwaysApply:[ ]*true` inside it returns true. At end of file awk exits 0, so **a file with no closing `---`, or no frontmatter at all, counts as always-on.**
- **`validate_frontmatter`:** unanchored greps over the whole file. `^---` on any line; `description:` anywhere; `paths:`, `globs:` or `alwaysApply:` anywhere.
- **`get_apply_to` (#40):** when the frontmatter closes with no `paths:`, it prints `**` and calls `exit`. awk still runs `END` after `exit`, and END prints `**` again, so the value is `**\n**`. With unclosed frontmatter and paths collected, it prints nothing. Quotes are stripped from each path.
- **`get_frontmatter_field`:** the first match of `^<field>:[ ]*` inside the frontmatter. One leading and one trailing `"` are stripped.
- **`convert_paths_to_globs` (cursor):** `in_frontmatter` toggles on every `---` and nothing tracks that the frontmatter has ended. **A later `---` in the body reopens frontmatter mode**, and `name:` lines and `paths:` lists there are rewritten too. Quotes are kept in globs.
- **`strip_name_field` (claude):** does track the end of the frontmatter, so only `name:` lines in the first frontmatter block are dropped.

## Rule compilation
- **Two body extractors that differ:**
  - claude (`compile_claude_rules`): keeps `---` lines after the frontmatter.
  - always-on (`compile_always_on_rules`, used for AGENTS.md and copilot): drops every `---` line, inside code fences too.
  - Both:
    - print code-fence lines even before the frontmatter
    - skip the first `#{1,6} ` heading after the frontmatter
    - strip one `#` from `#{2,6} ` headings outside code fences
- **Section title:** the first `#{1,6} ` heading after the frontmatter, outside code fences. macOS awk supports `{1,6}` intervals.
- **Fallback title when there is no heading:**
  - claude: `sed 's/\b\w/\U&/g'`. BSD sed has no `\b`, `\w` or `\U`, so this is literally `s/bw/Ubw/g`. The macOS result is: strip `.md`, replace `bw` with `Ubw`, replace `-` with a space, then append ` Rules`. GNU sed would capitalize words instead.
  - always-on: strip `.md`, replace `-` with a space. No ` Rules`.
- The claude content starts with `# Project Guidelines for Claude` and a blank line. AGENTS.md uses `# Project Guidelines`; copilot-instructions.md has no H1. Each rule adds `## <title>`, then its body, then a blank line.

## Managed sections
- **`managed_state`:** compares whole lines (`grep -Fx`). One BEGIN before one END is `managed`. Any other count or order is `broken`. With no BEGIN or END, the old single marker means `legacy`; otherwise `unmanaged`.
- **`managed` branch (#38):** awk rewrites every line, so a file whose last line had no newline gets one. CRLF lines keep their `\r`.
- **`legacy` branch:**
  - The first line is dropped only when it equals the H1 the block will re-emit. A blank second line after it is dropped too.
  - Everything from the marker on is replaced.
  - Content after a hand-added `[//]: # (context-forge:managed end)` is kept. Later marker and end lines in that tail are dropped.
- **`unmanaged` branch:**
  - The original file is copied to `<file>.pre-context-forge`, but only if no backup exists yet.
  - Then comes the original, a forced `\n`, and the block.
- Writes go to `<file>.context-forge.tmp` and are then moved into place with `mv`.

## Install manifest
- **`cksum`** is POSIX CRC-32, not zlib: polynomial 0x04C11DB7, not reflected, the byte length folded in, and the result inverted. Check: `tests/setup_ide/fixture_data/analyze-SKILL.md` gives `4163870229 9896`.
- **`install_file`:**
  - A destination that exists and differs is overwritten only when the old manifest lists the path and its current checksum matches that entry.
  - Listed but edited: kept, and the old entry is carried into the new manifest.
  - Not listed: skipped.
  - No manifest at all: skipped. Identical content is adopted.
  - The entry lookup can return several lines. They are compared as one string, so duplicates never match.
- **`finish_manifest`:**
  - The old manifest text and the hard-coded legacy entries are concatenated as raw text.
  - Paths are `cut -d' ' -f3-`.
  - Stale paths are processed in `sort -u` order.
  - A stale file is removed when any old entry matches its current checksum.
  - The new manifest is written with `sort -k3`. The key includes the leading blank, and equal keys fall back to comparing the whole line. Under a non-C locale on Linux this is locale order, not byte order.
- **`remove_empty_install_dirs`** removes emptied parent directories while the path still has at least two slashes, so `.claude/skills` itself is never removed.

## Control flow under `set -e`
- `exit 1` inside a function ends the whole run, so `warn_unmatched_exclusions` only runs after a successful target.
- Broken markers:
  - claude: the three marker messages, then `❌ Failed to compile CLAUDE.md`, exit 1.
  - agents/copilot: exit 1 straight after the marker messages.
- A missing lint directory makes `check_lint_configs` return 1, and the run exits 1.
- In a dry run only stdout is captured into the log; stderr passes through. A failure inside the dry run exits before the log is printed, so that output is lost.
- Errors that go to stderr: only the two `--root` errors and the cf failure. `Unsupported target` and the usage text go to stdout.

## Paths
- `pwd` is logical, and bash exports `PWD` to child processes. Project root detection, `--root` (`cd "$root" && pwd`) and the guide directory all use logical paths.
- `rules_dir_display_path` strips the `"$TARGET_ROOT/"` prefix from the logical rules dir, so both sides have to be logical or the prefix will not match.

## rules.exclude
- The env var `CONTEXT_FORGE_RULES_EXCLUDE` (non-empty) wins. Its value is used as is.
- **cf, new form:** `cf config get --help` stdout contains `--value`. Then `cf config get --value rules.exclude`, run from the project root, with its stderr passed through.
  - Exit 0: the value. Each line is trimmed of `[[:space:]]`, then trailing newlines are dropped.
  - Exit 2: no exclusions.
  - Anything else: `❌ cf config get --value rules.exclude failed (exit N)` on stderr, exit 1.
- **cf, old form:** `cf config get rules.exclude`, stderr discarded. A non-zero exit means no exclusions. Otherwise the first `Value:` line, trimmed.
- **Matching:**
  - Split on `,`. Trim whitespace around each pattern and skip empty ones.
  - Match the basename with bash `case` glob rules.
  - Record each pattern that matched.
- **Warnings:**
  - A pattern that matched nothing is reported on stderr.
  - A pattern that names an always-on rule (one `has_always_apply` accepts) gets its own message.
  - The active source is named first.
- **Bash bug, not worth porting:** `for pattern in $RULES_EXCLUDE` is unquoted, so each pattern is also glob-expanded against the current directory. `*.md`, run from a project root holding `CLAUDE.md`, becomes the list of that directory's `.md` files, and the exclusion quietly stops working. No test covers it.

## Lint check
- Reads from the project root and writes to the target root, so a dry run still checks the real project.
- **`lint_missing_requirements`:**
  - Requirement lines come from `while IFS= read -r`, so **a final line without a newline is ignored**.
  - Lines that are blank or start with `#` are skipped.
  - Alternatives are split on `|`. Each is a fixed-string match against the config text, and an empty text matches nothing.
  - The reported name is the line text before the first `|`.
- **Python:**
  - Detection: `pyproject.toml`, `setup.py` or `requirements*.txt`.
  - Config precedence: `.ruff.toml`, then `ruff.toml`, then `[tool.ruff*]` sections in `pyproject.toml`. Quotes are normalized `'` → `"`. A ruff config with `extend = "pyproject.toml"` also includes those sections.
  - With `--write-lint`, a weak pyproject gets a `ruff.toml` with `extend = "pyproject.toml"` and `extend-select` listing the missing rules.
- **Dart:** `pubspec.yaml`. `sdk: flutter` switches the label and the include line.
- **TypeScript:** `tsconfig.json` or `tsconfig.base.json`. The first ESLint config found, in a fixed order, is checked.
- **C#:**
  - Detection: `find -maxdepth 3`, pruning `.git`, `node_modules`, `project-documents`, `bin` and `obj`. Depth 3 is detected, depth 4 is not.
  - `.editorconfig`, `Directory.Build.props` and every `.csproj` are checked together. Missing files are written with `--write-lint`.
- A language whose `<lang>.md` rule is excluded is skipped.
