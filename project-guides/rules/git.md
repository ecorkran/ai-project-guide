---
name: git-rules
description: Git workflow conventions including commit message format, branch naming, PR process, and merge strategy. Use when committing, creating branches, or preparing pull requests.
alwaysApply: true
---

### Git Rules

#### Branch Naming
A branch corresponds to one unit of work, named by its index family and type:`{index}-{type}.{name}` (the document name without the `.md` extension, with the numeric index prefix). Two types of work get branches:

- **Slice work** (Phase 6 implementation) → `{index}-slice.{name}`, where `{index}` is the slice's index.
- **Planning work** (Phases 0–5: concept, initiative plan, architecture, slice plan, slice design, task breakdown, and reviews of those artifacts) → `{index}-planning.{name}`, where `{index}` is:
  - index 000 for project setup (concept / initiative plan), or
  - the initiative base index for an initiative's architecture, slice plan, slice designs, and task breakdowns.

`planning` is a branch type only — it has no corresponding document type. It names the branch that carries an index family's planning artifacts before implementation begins. Implementation moves to the slice branch; reviews stay with whatever they review (arch/slice/task reviews on the planning branch, code review on the slice branch).

Before starting work on a slice or planning unit:
1. verify you are on main or the expected branch
2. if the expected branch does not exist, create it from `main`: `git checkout -b {branch-name}`
3. if the branch already exists, switch to it: `git checkout {branch-name}`
4. never start work from another unit's branch unless explicitly instructed
5. if in doubt, STOP and ask the Project Manager

A branch merges to `main` when its unit completes — a planning branch when its planning phase is done, a slice branch when its implementation is done.  Do not hold a branch open across units; a planning branch is not a long-lived home for successive initiatives.

#### Commit Messages
Use semantic commit prefixes. The goal is a readable `git log --oneline`.

Format: `{type}: {short imperative summary}`

Types:
- `feat` — New functionality or capability
- `fix` — Bug fix
- `refactor` — Code restructuring without behavior change
- `test` — Adding or updating tests
- `style` — Formatting, whitespace, linting (no logic change)
- `guides` - Update or addition to project guides (system/project level)
- `docs` — Update or addition to user/ guides or documentation (slices, readme, etc)
- `review` — Code review, design review, or audit documentation
- `package` - Updates related to packaging, npm, package.json, PyPi, etc
- `chore` — Build config, dependencies, tooling, CI

Actions (optional, use if applicable):
- `update`: primarily update/edit to existing information
- `add`: primarily addition of new code or information
- `extract`: primarily used in refactoring
- `reduce`: if primary work involves reduction or streamlining

#### Guidelines:
- Summary is imperative mood ("add X" not "added X" or "adds X")
- Keep to ~72 characters
- No period at end
- Scope is optional but useful in monorepos: `feat(core): add template variable resolution`

#### Examples:
feat: add context_build MCP tool
fix: update to handle missing template directory gracefully
refactor(core): extract service instantiation into shared helper
docs: add MCP server installation instructions to README
test: add unit tests for prompt_list tool handler
chore: update @modelcontextprotocol/server to v2.1
