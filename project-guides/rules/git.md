---
name: git-rules
description: Git workflow conventions including commit message format, branch naming, PR process, and merge strategy. Use when committing, creating branches, or preparing pull requests.
alwaysApply: true
---

### Git Rules

#### Branch Naming
A branch corresponds to one unit of work: slice implementation (Phase 6). Planning work (Phases 0–5: concept, initiative plan, architecture, slice plan, slice design, task breakdown, and reviews of those artifacts) does not get its own branch — it commits directly to the current integration target (see below).

- **Slice work** → `{index}-slice.{name}`, where `{index}` is the slice's index and `{name}` is the document name without the `.md` extension.

##### Integration branch
A project may configure an **optional** integration branch that work forks from and merges into, instead of `main`. Read it with `cf config get git.integration_branch`. This key is optional and defaults to empty:

- **Unset (default):** no change from plain historical behavior. Work branches fork from `main` and merge into `main`, named exactly `{index}-{type}.{name}` — no prefix.
- **Set** (e.g. `dev/erik`):
  - Work branches are named the same as when unset — `{index}-{type}.{name}` (e.g. `910-slice.foo`), with no prefix.
  - Work branches fork **from** `{integration_branch}`, not `main`.
  - Work branches merge **into** `{integration_branch}`, not `main`.
  - **Hard rule: never merge to `main` when `integration_branch` is set.** Syncing `{integration_branch}` from `main`, and eventually merging `{integration_branch}` into `main`, are PM-only actions outside automation scope — never perform either as part of normal slice/planning workflow, only if the Project Manager explicitly instructs it as a standalone action.

The integration branch affects **git topology only** (fork point and merge target) — not the branch name. It does not move documents or change where artifacts resolve — the `project-documents/user/...` layout under the branch is unchanged. The configured value is relative and contained (never absolute, never `..`, no trailing slash, no Windows drive/`\`); `cf` rejects invalid values when the key is set.

##### Worktrees
The target is a property of the config, never of the checkout. The branch you happen to be on is not evidence of the target — always read it (step 1 below), in the primary tree and in every git worktree.

`git.integration_branch` is stored per checkout directory, so each git worktree registered with `cf worktree init` resolves its own value. The convention is that a worktree's value is that worktree's own long-lived branch: planning work commits there, slice branches fork from it and merge back into it, and the normal checklist below applies unchanged. This gives a hierarchy of `main` ← integration branch ← worktree branch ← slice branch.

- **Agents merge exactly one level:** a slice branch into its target. Merging a worktree's branch into a wider integration branch or into `main`, and refreshing it from either, are PM-only actions, same as the hard rule above.
- **Unregistered worktree:** if you are in a git worktree and `cf worktree list` shows no entry for your path, the value `cf` returns belongs to the primary checkout, not to this worktree. STOP and ask the Project Manager.
- **Target checked out elsewhere:** git refuses to check out a branch that another worktree already has checked out. If that happens for the target, STOP and ask the Project Manager. Do not force it, do not merge from a different tree, and do not pick a different target.

Before starting work:
1. read `cf config get git.integration_branch`; call its value (or `main` if empty) the **target**

**If committing planning work (Phases 0–5):**
2. ensure you are on the target. Do not create or switch to a work branch. Commit directly.

**If starting slice implementation (Phase 6):**
2. determine the branch name per the rules above (no prefix, regardless of target)
3. verify you are on the target or the expected slice branch
4. if the expected slice branch does not exist, create it from the target: `git checkout -b {branch-name} {target}`
5. if the branch already exists, switch to it: `git checkout {branch-name}`
6. never start work from another unit's branch unless explicitly instructed
7. if in doubt, STOP and ask the Project Manager

When slice implementation is done, merge the slice branch into the target:
1. re-read the target (step 1 above) — do not infer it from the current branch or from memory
2. `git checkout {target}`, then `git merge {branch-name}`
3. if either command fails, STOP and ask the Project Manager

Do not hold a branch open across units. Do not delete branches unless specifically instructed to do so.

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
