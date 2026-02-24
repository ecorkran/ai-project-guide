---
description: Rules for modern Python development with focus on readability and testability
alwaysApply: true
---

### Git Rules

#### Branch Naming
When working on a slice, use a branch named after the slice (without the `.md` extension but with the numeric index prefix).

Before starting implementation work on a slice:
1. verify you are on main or the expected slice branch
2. if the expected slice branch does not exist, create it from `main`: `git checkout -b {branch-name}`
3. If the slice branch already exists, switch to it: `git checkout {branch-name}`
4. Never start slice work from another slice's branch unless explicitly instructed
5. If in doubt, STOP and ask the Project Manager

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
