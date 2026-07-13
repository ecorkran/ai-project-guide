---
docType: devlog
scope: project-wide
description: Internal session log for development work and project context
---

# Development Log

Internal work log for ai-project-guide development. See `CHANGELOG.md` for release notes.

---

## 20260713

**Session**: Replace `git.branch_root` with `git.integration_branch` (v0.15.11)

### Completed
- Replaced `git.branch_root` (pure name-prefix) with `git.integration_branch` in `project-guides/rules/git.md` — the new key changes fork/merge topology (work forks from and merges into the integration branch, not `main`) rather than just prefixing the branch name
- Removed the `{index}-planning.{name}` branch type entirely; planning work (Phases 0–5) now commits directly to the current integration target instead of a dedicated planning branch
- Fixed a bullet that leaked the old prefix-naming behavior into the new rule (branch names never carry the `{integration_branch}/` prefix — only fork/merge targets change) across `project-guides/rules/git.md`, root `CLAUDE.md`, and the submodule's own copies of both
- Synced root `CLAUDE.md` and the submodule's `project-documents/ai-project-guide/{git.md,CLAUDE.md}` to eliminate drift between the four copies

### Key decisions
- `integration_branch` is a full replacement for `branch_root`, not additive — only one config key exists going forward
- Agents must never merge to `main` when `integration_branch` is set; syncing the integration branch from `main`, or merging it into `main`, is PM-only and outside automation scope
- Submodule commits: since this repo is both the standalone project and (via its own submodule reference) the vendored copy consumed by other projects, fixes land as a commit in the submodule first, then a pointer-bump commit in the outer repo — kept as separate commits per PM preference
- A submodule checkout left in detached HEAD (from a prior fetch) was reattached to `main` (`git checkout -B main`) before committing, since `origin/main` was already an ancestor of the detached commit — avoids stranding commits unreachable from any branch

---

## 20260309

**Session**: Slice design and implementation prompt improvements

### Completed
- Added Verification Walkthrough section to Phase 4 guide and prompt — bridges gap between success criteria and concrete proof of delivery (v0.13.8)
- Updated Phase 5 prompt with test-with pattern (tests placed after corresponding implementation tasks)
- Updated Phase 6 prompt: commit at explicit checkpoints, three-attempt retry limit with PM escalation

---

## 20260306

**Session**: Prompt cleanup and obsolete reference removal

### Completed
- Removed obsolete `project-artifacts` monorepo pattern references (v0.13.2)
- Simplified Context Initialization prompt: removed redundant bullet lists, hardcoded HLD path, legacy path note; replaced with `{{#if fileArch}}` / `{{#if fileSlicePlan}}` template variables (v0.13.3)

---

## 20260228

**Session**: v0.13.0 — Process streamlining

### Completed
- Unified architecture → slice plan → slice → task as the single pipeline
- Consolidated project-level vs architecture-level planning (was redundant)
- Simplified Phase 1 (Concept) — spec absorbed into architecture phase
- Removed standalone feature concept, task expansion phase, legacy migration guide, onboarding notes
- Updated 005-task-breakdown to remove feature references, deleted 091-legacy-task-migration

### Key decisions
- "Feature Slices" kept as a slice *type* descriptor (different from removed standalone feature document category)
- Migration guide docType enum left as-is (historical)

---

## 20260228

**Session**: Guide standardization

### Completed
- Standardized all status enum values to underscore format (`not_started`, `in_progress`) across guides and system prompt
- Promoted `dateCreated`/`dateUpdated` from optional to required frontmatter
- Removed standalone feature concept (reduced complexity with no practical benefit)

---

## 20260225

**Session**: Modular rules support (#11)

### Completed
- Refactored `setup-ide claude` to support modular rules: `alwaysApply: true` rules embedded in CLAUDE.md, all others copied to `.claude/rules/`
- Added `paths` → `globs` conversion for Cursor in `setup-ide cursor`
- Stripped unsupported `name` field from frontmatter when copying to `.claude/rules/` and `.cursor/rules/`
- Marked `git.md` as `alwaysApply: true`
- Dropped Windsurf support from `setup-ide`
- Moved `review.md` and `ui-development.md` to `project-guides/skills/` (future skill support)

### Key decisions
- Rules files use `paths` (Claude-native format) as source of truth; Cursor conversion happens at copy time
- `name` field kept in source rules files but stripped on copy (not supported by Claude or Cursor)
- Only `general.md` and `git.md` are `alwaysApply: true`

---

## 20260121

**Session**: Codebase analysis and consistency standardization

### Completed
- Full codebase analysis after 2-month hiatus (see `user/analysis/940-analysis.initial-codebase.md`)
- Added YAML frontmatter to all 70+ markdown files (was ~55% coverage)
- Fixed malformed frontmatter in `tool-guides/shadcn/setup.md`
- Renamed `800-feature/tasks` → `105-slice/tasks` (800 range is reserved)
- Deleted empty files: `900-slice.maintenance.md`, `guide.object-creation.complex.md`, `api-guides/usgs/`
- Standardized all YAML dates to YYYYMMDD format
- Added frontmatter requirement and date format to `file-naming-conventions.md`
- Added `created` field to frontmatter schema
- Documented DEVLOG.md purpose and format

### Decisions
- Keep both agent directories (`.claude/agents/` and `project-guides/agents/`) - former is Claude Code specific
- Missing `guide.ai-project.005-xxx` is intentional - Phase 5 covered in `000-process`
- DEVLOG.md for internal session notes; CHANGELOG.md for external releases
- YYYYMMDD date format standardized across all YAML frontmatter

### Deferred
- Update `directory-structure.md` to remove date from title
- Review open GitHub issues (#1, #3, #4, #6)

---

## 20260121 (continued)

**Session**: Migration guides and file indexing standardization

### Completed
- Created `project-guides/migrations/` directory for version-specific migration docs
- Added `20260121-migration-guide.md` - consistency standards (YAML, dates, indexing)
- Moved `MIGRATION.md` → `project-guides/migrations/20251008-migration-private-to-user.md`
- Marked v0.10.0 migration as obsolete
- Root `MIGRATION.md` now serves as index to migrations folder
- Renamed task files to use proper indexing:
  - `inventory.index-migration.md` → `952-inventory.index-migration.md`
  - `report.index-migration.20250930.md` → `953-report.index-migration.md`
- Updated `950-tasks.maintenance.md` references

### Decisions
- Framework guide files (project-guides/*.md) do not require date fields - stable methodology docs
- Migration guides use YYYYMMDD prefix for chronological sorting
- All files in `user/tasks/` must use nnn- index prefix

---

## 20260121-20260215

**Session**: Expanded architecture support, Phase 3/4 updates, tool guides, version 0.11.0

### Completed
- Added Phase 2.5 (HLD Creation) to process guide and prompt library
- Added Phase 3.5 (Architectural Component Design) prompt
- Updated Phase 3 (Slice Planning) for dual-context support (project-level and architecture-level)
- Updated Phase 4 (Slice Design) to reflect current standards
- Standardized all YAML date fields to `dateCreated`/`dateUpdated` across all files
- Added standalone feature index range (750-799)
- Added Electron tool guides (00-05)
- Added MCP tool guide
- Updated project-guides readme with new phases, resources, and author schema
- Full compliance audit — all files verified against naming conventions
- Released v0.11.0

### Decisions
- YAML date fields use camelCase: `dateCreated`, `dateUpdated`
- Standalone features get dedicated 750-799 range (slices narrowed to 100-749)
- Architecture documents can serve as HLD for their scope (no separate project HLD needed)
- Tool guides may use 2-digit indices (will formalize in future update)
- Phase numbering uses decimals (2.5, 3.5) for now — re-indexing deferred

### Open Issues
- Formalize tool guide indexing conventions
- Review open GitHub issues (#1, #3, #4, #6)
- `setup-ide` script needs verification with current structure
