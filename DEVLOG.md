---
docType: devlog
scope: project-wide
description: Internal session log for development work and project context
---

# Development Log

Internal work log for ai-project-guide development. See `CHANGELOG.md` for release notes.

---

## 20260926

**Session**: flutter.md glob over-attachment fix (v0.19.1)

### Completed
- Narrowed `flutter.md`'s `paths:` to `android/**`, `ios/**` only, removing
  the overlap with `dart.md`'s `**/*.dart`, `**/pubspec.yaml`,
  `**/analysis_options.yaml` (#13)
- Updated `flutter.md`'s description to state it supplements `dart.md`
- Fixed the stale scope table entry for `flutter.md` in `readme.setup-ide.md`

### Key decisions (PM-approved)
- Went with the fully deterministic option: platform folders only exist in
  `flutter create` projects, so this has zero false positives on plain Dart.
  Tradeoff accepted: editing a `lib/` widget file alone, without touching
  `android/**`/`ios/**` in the same operation, no longer attaches Flutter
  rules — glob frontmatter can't check `pubspec.yaml` for a `flutter:` key,
  so there's no pattern that's both deterministic and fires on widget-only
  edits
- Did not commit this repo's own `.claude/` install refresh beyond
  `flutter.md` — running `setup-ide claude` also picked up unrelated drift
  in `CLAUDE.md`, `python.md`, `testing.md` that predates this fix and is
  out of scope here

---

## 20260925

**Session**: Install manifest pruning, status value discoverability (v0.19.0)

### Completed
- `setup-ide` writes `.context-forge/<target>.manifest` and prunes stale files
  on the next run (#25)
- Valid status values surfaced at the points where agents write status (#12)
- Split `setup_claude`/`setup_cursor` out of `run_target_setup` so every
  target goes through one manifest begin/finish

### Key decisions (PM-approved)
- Manifest is committed, so clones and worktrees share it
- Delete only when the checksum still matches what we wrote; edited files are
  kept with a warning. `cksum` is used because it is POSIX and identical on
  macOS and Linux
- Exclusions now prune, replacing 0.18.0's skip-only behavior
- Pre-manifest installs: a checksum table of every shipped version of the two
  dropped files (analyze skill, code-review-agent), from git history, rather
  than a warn-only list
- Composites are never in the manifest; they hold user content

### Open
- context-forge#103: cf's worktree propagation still only adds files. It
  needs to copy the manifest and prune worktrees with the same rule

---

**Session**: PR review file naming (v0.18.2)

### Completed
- `file-naming-conventions.md`: PR reviews use `pr-{number}-review.{reviewType}.md`,
  qualified with `.{owner}-{repository}` only in shared review directories

### Key decisions
- Qualify by directory, not always: project `user/reviews/` and squadron's
  per-repo default path already pin the repository, so the long form was noise
- Kept the non-numeric prefix so slice-index globs still can't match a PR review
- Old-form files are left alone rather than migrated

---

**Session**: Copilot skills as Agent Skills, analyze skill removal (v0.18.1)

### Completed
- Copilot target copies skills to `.agents/skills/` instead of emitting
  `.github/prompts/*.prompt.md`; re-runs remove our generated prompt files (#24)
- Removed the obsolete `analyze` skill, the only one the guide shipped
- Filed context-forge#102: cf's copilot worktree propagation needs
  `.agents/skills` added. Either side can land first

### Key decisions
- `.agents/skills/` over `.github/skills/`: both are read by Copilot, but the
  agents target already writes `.agents/skills/`, so one directory covers
  Copilot, Codex and Cursor
- Skill sources were already `<name>/SKILL.md`, so no translation was needed —
  the copilot target now calls the same `copy_skills` as the other targets
- Cleanup keys on the `context-forge:generated` stamp so hand-written prompt
  files survive. The directory is removed only when truly empty (`ls -A`), since
  a `.gitkeep` would otherwise make `rmdir` abort the run under `set -e`

### Known gap (deferred by PM)
- `setup-ide` never removes installed files the guide later drops. Squadron
  carried a v0.11.3 `code-review-agent.md` through to v0.18.0 this way. Fixing
  it needs a record of what was installed; not an issue yet

---

## 20260922

**Session**: Managed-section merge and rule exclusions (v0.18.0)

### Completed
- `setup-ide` merges generated content into `CLAUDE.md`, `AGENTS.md` and
  `.github/copilot-instructions.md` via `<!-- BEGIN:context-forge -->` /
  `<!-- END:context-forge -->` instead of overwriting whole files (#22)
- `rules.exclude` support: comma-separated basename globs, read from
  `CONTEXT_FORGE_RULES_EXCLUDE` then `cf config`, skip-only (#23)
- Filed #24: `.github/prompts/*.prompt.md` is deprecated upstream in favour of
  Agent Skills. No action taken; recorded so it is not rediscovered

### Key decisions
- HTML-comment markers over `[//]: # (...)`. The link-reference form relies on
  renderers discarding unused link reference definitions, which lightweight
  parsers get wrong — it renders as visible text. Next.js already ships the
  same BEGIN/END comment shape for its generated `AGENTS.md`, so this follows
  an existing convention rather than inventing one
- A file with no marker is preserved and the block appended, not overwritten.
  The old behavior destroyed a pre-existing hand-written `CLAUDE.md` on first
  adoption. cf's `.bak` was the only thing standing behind it, and only when
  cf was the entry point — `setup-ide` runs standalone too
- Legacy migration needs no content parsing: generated content always ran from
  the marker to end of file, so that span is known. A duplicate leading H1 is
  dropped only when it is line 1 and exactly matches what the block re-emits —
  absorbing more would risk deleting user content
- Unbalanced markers leave the file untouched and exit non-zero. Guessing at
  the boundary is worse than refusing
- Kept the env-var path alongside `cf config`. cf argued for config-only on the
  grounds that `setup-ide` already shells out to cf; it does not, and never
  has, so config-only would leave direct callers no way to set exclusions
- Always-on rules are unexcludable by construction rather than by
  documentation. Silently dropping `general.md` or `git.md` has no visible
  symptom until something downstream misbehaves

### Notes
- Sequenced behind context-forge#98 (marker recognition) and their
  `rules.exclude` key, both in cf 0.17.0. Held for the merge to main rather
  than the branch commit — the regression window is keyed to what consumers
  actually run
- The AGENTS.md scoped index was being appended after the compile. Left as-is
  it would have landed below `END` and accumulated a duplicate copy on every
  run. Caught by reading the call site, not the function
- Research corrected two widely-repeated claims: Aider does not read
  `AGENTS.md` at all, and Gemini CLI reads it only via opt-in config. Vendor
  docs contradict the aggregator posts
- Root `CLAUDE.md` (generated copy of these rules) not regenerated in this
  release

---

## 20260919

**Session**: Worktree handling and branch protection check in git rules (v0.17.9)

### Completed
- `rules/git.md`: added "Worktrees" subsection and explicit merge steps (#15)
- `rules/git.md`: added "Branch Protection" section — agents were reporting
  "no protection on the default branch" after checking only the classic
  endpoint; reproduced on this repo (classic returns 404, `rules/branches/main`
  returns three active ruleset rules)
- Filed #22 (begin/end managed markers + merge in `setup-ide`) and #23 (rules
  exclude list), counterparts to context-forge #94 and #95

### Key decisions
- Worktree target = the worktree's own branch, set per worktree via
  `git.integration_branch`. Replaced an earlier design (planning on the
  worktree branch, merges run from the target's tree via `git -C`) that needed
  cross-tree operations and a "land planning first" sequence
- No resolution logic in the guide. context-forge confirmed the key is
  personal-scope and stored per checkout directory, so registered worktrees
  already resolve their own value; surfacing the resolved target in built
  context stays with context-forge #70
- Branch protection check went into the always-on git rules rather than a
  customizable per-project rules file — it is a correctness fact for any
  GitHub/GHE repo, not an org preference
- Discussed but deferred: a project-owned rules directory (e.g. a `culture.md`
  compiled alongside `general.md`/`git.md`) and a config key for the git host.
  Nothing filed
- Root `CLAUDE.md` (generated copy of these rules) not regenerated in this
  release

**Session**: Keep guide-development files out of tarball installs (v0.17.10)

### Completed
- Added `.gitattributes` with `export-ignore` for `user/`, `.claude/`,
  `.idea/`, `.obsidian/`, `.understand-anything/`, `DEVLOG.md`, `CLAUDE.md`,
  and `.gitattributes` itself
- Verified with `git archive --worktree-attributes HEAD`: the archive contains
  only guide content, scripts, snippets, `z-attachments/`, and the top-level
  docs. Not yet verified against a real GitHub tag tarball

### Key decisions
- Chose `export-ignore` over moving the guide's own project files to another
  repo or branch: the files stay tracked and carried along here, and no
  tooling is involved
- Scope is the tarball (`manual`) strategy only, which is the one producing PR
  clutter and is expected to become the default. Submodule is acceptable as is
- `.claude/` at the repo root is generated output for this repo; `setup-ide`
  builds a consumer's `.claude/` from `project-guides/`, never from the root
  copy, so excluding it breaks nothing
- Left `z-attachments/` in the archive: guides reference it, and whether they
  link the actual images was not checked

## 20260918

**Session**: Remove self-referential submodule (v0.17.8)

### Completed
- Removed the gitlink at `project-documents/ai-project-guide` (pointing at
  this repo's own URL) and `.gitmodules`, both introduced by `4714fbd`
  ("docs: install ai-project-guide v0.15.6") — the result of running
  `cf guides install` inside a checkout of the guide itself
- Source: another Claude session (context-forge) filed #21 after the v0.17.5
  tarball confirmed both artifacts ship to every consumer install (tarball,
  submodule, clone)
- context-forge is adding a defensive extract filter on its own side in
  parallel; this fix is the upstream side so new installs stop carrying it

### Key decisions
- Tagged v0.17.8, not the v0.17.6 the issue suggested — v0.17.7 had already
  shipped (PR review filename convention) since the issue was filed
- Left `.idea/` and `.obsidian/` alone — flagged in the issue as separate,
  non-blocking hygiene, not part of this fix
- Left the emptied `project-documents/` directory in place untracked (git
  doesn't track empty dirs); no further action needed

## 20260916

**Session**: Pull-request review filename convention (v0.17.7)

### Completed
- Added "Pull-Request Reviews" subsection to `file-naming-conventions.md`'s
  Review Files section: `{host}-{owner}-{repository}-{number}-review.{reviewType}.md`,
  the `targetKind`/`rulesSource` optional frontmatter keys, and the `pr:`
  mapping that replaces `slice:` for PR reviews
- Source: another Claude session (sq-issues) flagged an uncommitted,
  orphaned edit to this same file sitting in the ai-project-guide submodule
  checkout inside the squadron-pr worktree (detached HEAD at e11dcd4, never
  committed anywhere) — the convention it documented was already shipped in
  squadron (`383-slice.pr-keyed-review-persistence`, commits `ae334e8b`,
  `b4129c53`). Rewrote it as a proper commit here instead of leaving it
  hand-edited in a consumer's submodule checkout

### Key decisions
- Placed the new subsection under "## Review Files" as a sibling to
  Slice-Lineage and Operational Reviews, not inside the `#### review`
  frontmatter schema block where the orphaned draft had put it — the schema
  block only gets a pointer to the new subsection plus a one-line summary
  of the new keys
- Ground rule going forward (per Erik, relayed via the peer session): the
  ai-project-guide submodule is only ever edited from this repo, never by
  hand inside a consumer repo's submodule checkout

## 20260915

**Session**: Docker/container tool guide (v0.17.6)

### Completed
- Added `tool-guides/docker/` per issue #20: `00-introduction.md` (vocabulary,
  pitfall quick-reference table), `01-image-and-build.md` (build-time vs
  runtime work, pinning by digest/checksum, generated-vs-hand-maintained
  config), `02-entrypoint-and-process-model.md` (multi-mode dispatch that
  rejects unknown modes, PID 1/exec/tini, loopback-vs-0.0.0.0 binds,
  gitignored env files under `set -e`, graceful stop windows),
  `03-compose-and-orchestration.md` (`depends_on` vs `condition:
  service_healthy`, writing meaningful healthchecks), `04-decision-guide.md`
  (porting an existing systemd unit's resource limits/restart policy/env
  into a container without silently reverting to defaults)

### Key decisions
- Followed the `tool-guides/electron/` numbered-file convention (introduction
  + topic guides + decision guide) exactly, per the issue's suggested shape
- Used `layer: tool-guide` / `docType: introduction|guide` frontmatter
  (electron's schema) rather than the numbered-index project-document
  frontmatter — this is tool-guide content, not initiative/slice work

## 20260914

**Session**: Mechanically enforceable slice-design template (v0.17.5); review-gate guidance (v0.17.4)

### Completed
- Extracted the Phase 4 slice-design template out of guide prose into `project-guides/templates/slice-design.md` with `<!-- required -->` / `<!-- optional: ... -->` heading markers; the template is the single source for both the agent-facing skeleton and the section schema
- Added `scripts/validate-slice-design` (bash 3.2): derives required headings from the template markers, checks level-2 sections plus the level-3 Verification Walkthrough, skips fenced code, prefix-matches headings carrying a `{placeholder}`; verified PASS on the template and on amoeba's `101-slice.store-foundation-and-node-model.md`, FAIL on a copy with two headings removed
- Rewired `guide.ai-project.004-slice-design.md`, the P4 system prompt, the process guide, `file-naming-conventions.md`, and both readmes to the template and validator
- v0.17.4 (earlier, same push): `review: none` in slice-design frontmatter documented as a PM-only review-exempt declaration; agents must not add it, run `cf check --set-review-none`, or copy it from a sibling design; "review required" from `cf next` means stop and report

### Key decisions
- Enforce at level 2 only, plus Verification Walkthrough. The conforming reference design renames or replaces most level-3 headings (custom decision titles, "Storage Schema", "API Contract"), so level-3 enforcement would fail good documents
- Markers live in the template rather than a sidecar manifest: one file to edit, grep-parseable in bash, one regex for Context Forge if it reads them natively
- Implementation Details and Risk Assessment are the only optional level-2 sections; everything else the guide's own review checklist already treats as mandatory
- Validator is a guide script (same pattern as `setup-ide`). Invoking it from `cf` is a context-forge change and was flagged, not assumed

### Open Issues
- Context Forge: `cf check` / `cf validate` do not read design bodies. Options flagged to the cf side: exec `scripts/validate-slice-design` (setup-ide precedent) or parse the template markers natively
- Issue #18 (package distribution) evaluated this session; recommendation is to re-scope to "npm as a fetch source" after context-forge slice 925. Not yet posted to the issue

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
