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

##### Optional branch root prefix
A project may configure an **optional** root that is prepended to every work branch name. Read it with `cf config get git.branch_root`. This key is optional and defaults to empty:

- If the value is empty (the default), use the branch name exactly as defined above — no prefix.
- If the value is non-empty (e.g. `myroot`), prefix it with a slash: the branch becomes `{root}/{index}-{type}.{name}` (e.g. `myroot/910-slice.foo`).

The root affects the **git branch name only**. It does not move documents or change where artifacts resolve — the `project-documents/user/...` layout under the branch is unchanged. The configured value is relative and contained (never absolute, never `..`); `cf` rejects invalid values when the key is set.

Before starting work on a slice or planning unit:
1. determine the branch name per the rules above, then read `cf config get git.branch_root` and, if non-empty, prefix it as `{root}/{branch-name}`
2. verify you are on main or the expected branch
3. if the expected branch does not exist, create it from `main`: `git checkout -b {branch-name}`
4. if the branch already exists, switch to it: `git checkout {branch-name}`
5. never start work from another unit's branch unless explicitly instructed
6. if in doubt, STOP and ask the Project Manager

A branch merges to `main` when its unit completes — a planning branch when its planning phase is done, a slice branch when its implementation is done.  Do not hold a branch open across units; a planning branch is not a long-lived home for successive initiatives.  However, do not delete branches unless specifically instructed to do so.

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
