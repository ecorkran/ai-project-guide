---
docType: guide
scope: project-wide
audience: [human, ai]
description: setup-ide reference — supported targets, what each writes, and how to run it
---

# setup-ide

`setup-ide` compiles the rules in `project-guides/rules/` into whatever format
your AI tool reads. One source of rules, several output formats.

**Path convention:** `ai-project-guide/` below means
`{project-root}/project-documents/ai-project-guide/`.

## Install and run

Requires ai-project-guide present at `project-documents/ai-project-guide`
(normally a git submodule). Run from your project root:

```bash
./project-documents/ai-project-guide/scripts/setup-ide <target>
```

If you use context-forge, `cf setup-ide <target>` wraps this and adds
CLAUDE.md backup handling and worktree propagation.

Output paths are always resolved from the **project root** — the directory
containing `project-documents/` — so running from a subdirectory is safe.

## Supported targets

| Target | Writes | Use for |
|---|---|---|
| `claude` | `CLAUDE.md`, `.claude/rules/`, `.claude/agents/`, `.claude/skills/` | Claude Code |
| `cursor` | `.cursor/rules/*.mdc`, `.cursor/agents/*.mdc` | Cursor |
| `copilot` | `.github/copilot-instructions.md`, `.github/instructions/`, `.agents/skills/`, `AGENTS.md` | VS Code Copilot |
| `agents` | `AGENTS.md`, `.agents/skills/` | Codex and other AGENTS.md readers |

`openai` and `codex` are aliases for `agents`. `AGENTS.md` is a vendor-neutral
format, so the target is named after the format rather than after one vendor.

Any other value exits non-zero with usage. **`windsurf` is no longer
supported** — it was removed from the script but lingered in this document.

## What each target does

**`claude`** — splits rules by `alwaysApply`. Rules with `alwaysApply: true`
(`general`, `git`) are inlined into `CLAUDE.md`; the other eight are copied to
`.claude/rules/` retaining their `paths:` frontmatter. Agents are copied
verbatim. Skills in directory form (`skill-name/SKILL.md`) are copied to
`.claude/skills/`.

**`cursor`** — always-on rules compile to `AGENTS.md`. Scoped rules are copied
to `.cursor/rules/` renamed `.md` → `.mdc`, translating `paths:` to Cursor's
comma-separated `globs:`. Agents are not installed.

**`copilot`** — always-on rules compile to `.github/copilot-instructions.md`.
Scoped rules become `.github/instructions/*.instructions.md` with `paths:`
translated to `applyTo:`. Skills are copied to `.agents/skills/` in Agent
Skills format, which Copilot reads in the IDE, cloud agent, code review and CLI.
Also writes `AGENTS.md`. Earlier versions emitted skills as
`.github/prompts/*.prompt.md`, a format VS Code has deprecated; re-running
removes those generated prompt files and leaves any hand-written ones alone.

**`agents`** — writes `AGENTS.md`, plus skills to `.agents/skills/` when the
guide ships any: no `.github/`, no vendor-specific files. Always-on rules are
inlined. Scoped rules are **not**
inlined — the AGENTS.md format has no path-scoping mechanism, so inlining would
put Python rules in front of a React project. They are instead indexed by path,
for the agent to read on demand.

## Install manifest and cleanup

Each run records the files it wrote in `.context-forge/<target>.manifest`, one
line per file: checksum, size, and path. Commit it along with the installed
files.

On the next run, a file the old manifest lists but the new run no longer writes
is deleted. That covers a rule, agent or skill the guide dropped, and a rule
newly added to `rules.exclude`. A file edited since it was installed is kept,
with a warning. `CLAUDE.md`, `AGENTS.md` and `copilot-instructions.md` are never
listed, because they hold your own content outside the managed block.

Installs from before the manifest existed are cleaned up too. Files the guide
used to ship (the `analyze` skill, `code-review-agent.md`) are deleted when
their content matches a version the guide shipped.

## Rules inventory

`project-guides/rules/` — always-on rules apply everywhere; scoped rules attach
by file pattern.

| Rule | Scope |
|---|---|
| `general.md` | **always on** — core conventions |
| `git.md` | **always on** — commits, branches, integration branch |
| `dart.md` | `**/*.dart`, `**/pubspec.yaml` |
| `electron.md` | `electron/**`, `src/preload/**`, build configs |
| `flutter.md` | `**/*.dart`, `**/pubspec.yaml`, `android/**`, `ios/**` |
| `python.md` | `**/*.py`, `**/pyproject.toml`, `**/requirements*.txt` |
| `react.md` | React/JSX sources |
| `sql.md` | SQL, PostgreSQL, pgvector, TimescaleDB |
| `testing.md` | test sources |
| `typescript.md` | TypeScript sources |

Agents: `task-checker.md`, `tester.md`.

Skills: `analyze/`. A skill must be a **directory containing `SKILL.md`** —
Claude Code will not load a flat `.md` file, so `setup-ide claude` warns and
skips one rather than dropping it silently. The `cursor` target does not install
skills; Cursor has no equivalent concept.

## Frontmatter contract

Source rules use `paths:` as a YAML list. Each target translates it — you do
not hand-write per-vendor frontmatter.

```yaml
---
name: python-rules
description: When to apply this rule.
paths:
  - "**/*.py"
  - "**/pyproject.toml"
alwaysApply: false
---
```

- `description` — when to apply the rule; carried into every target
- `paths` — becomes Cursor `globs:`, Copilot `applyTo:`, retained as-is for Claude
- `alwaysApply` — `true` means inline into the always-on file (`CLAUDE.md`,
  `copilot-instructions.md`, `AGENTS.md`) rather than emit a scoped file
- `name` — stripped from Claude and Cursor output; used as Copilot `name:`

Generated always-on files carry `[//]: # (context-forge:managed)` so tooling can
recognize them as regenerable. Re-running a target overwrites its own outputs.

## Troubleshooting

**Permission denied**
```bash
chmod +x project-documents/ai-project-guide/scripts/setup-ide
```

**Rules not loading** — restart the IDE; rules load at startup. For Cursor,
confirm files are `.mdc` in `.cursor/rules/` with intact frontmatter.

**Wrong output location** — the script walks up for `project-documents/`. If it
reports an unexpected project root, you are outside the intended tree.
