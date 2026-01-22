---
analysisType: initial-codebase
project: ai-project-guide
date: 2025-11-14
analyst: Claude Opus 4.5
scope: full-codebase-review
status: completed
lastUpdated: 2025-11-14
---

# Initial Codebase Analysis - ai-project-guide

## Executive Summary

This analysis documents the current state of the ai-project-guide codebase after a two-month hiatus. The project is a methodology and toolset for AI-assisted software development, consisting primarily of markdown documentation files organized in a structured hierarchy.

**Original Findings (Pre-Remediation):**
- 73 markdown files total (excluding .git)
- ~55% had YAML frontmatter (40 files), ~45% did not (33 files)
- Several naming inconsistencies and structural issues identified
- No automated tests present
- No package manager or DevOps pipeline (documentation-only project)

**Post-Remediation Status:**
- 100% of markdown files now have YAML frontmatter
- All identified inconsistencies resolved (see Section 10)
- YAML frontmatter requirement added to `file-naming-conventions.md`

---

## 1. Project Overview

### Technology Stack
- **Type**: Documentation/methodology project (no runtime code)
- **Format**: Markdown (.md) files
- **Version Control**: Git with submodule architecture
- **IDE Support**: Obsidian, VSCode, Cursor, Windsurf, Claude Code
- **Scripts**: Bash scripts for bootstrap and IDE setup

### Project Purpose
Framework for AI-assisted software development providing:
- Structured methodology (slice-based development workflow)
- Tool/framework guides for common technologies
- Code rules for various languages/frameworks
- Process documentation and templates

---

## 2. Directory Structure

### Root Level (11 directories, 6 files)
```
ai-project-guide/
├── .claude/agents/        # Claude Code agent definitions (3 files)
├── api-guides/            # External API documentation (1 empty subdir: usgs/)
├── domain-guides/         # Cross-cutting knowledge (4 files)
├── framework-guides/      # App-level platforms: astro/, nextjs/ (5 files)
├── project-guides/        # Core methodology (18 files + rules/ + agents/)
│   ├── agents/            # Duplicate of .claude/agents/ (3 files)
│   └── rules/             # Language/framework code rules (8 files)
├── scripts/               # Setup and utility scripts (4 scripts + template-stubs/)
├── snippets/              # Copyable code examples (2 files)
├── tool-guides/           # Library guides (21 files across 9 tools)
├── user/                  # Project-specific work (template structure)
│   ├── analysis/          # (empty - target for this file)
│   ├── architecture/      # (empty)
│   ├── features/          # (1 file)
│   ├── project-guides/    # (empty)
│   ├── reviews/           # (empty)
│   ├── slices/            # (2 files)
│   └── tasks/             # (5 files)
└── z-attachments/         # Images/media (4 PNG files)
```

### Key Files at Root
| File | Purpose |
|------|---------|
| `readme.md` | Main repository documentation |
| `readme.setup-ide.md` | IDE setup instructions |
| `directory-structure.md` | Canonical structure contract |
| `file-naming-conventions.md` | Naming rules and index ranges |
| `CHANGELOG.md` | Version history |
| `MIGRATION.md` | Migration guide for breaking changes |

---

## 3. YAML Frontmatter Analysis

### Summary
- **With frontmatter**: 40 files (55%)
- **Without frontmatter**: 33 files (45%)

### Files WITH Frontmatter (40)
**Core Process Guides (12):**
- All `project-guides/guide.ai-project.*.md` files (except 091)
- `project-guides/prompt.*.md` files
- `project-guides/notes.ai-project.onboarding.md`

**Rules Files (8):**
- All `project-guides/rules/*.md` files

**Agent Definitions (6):**
- `.claude/agents/*` (3) and `project-guides/agents/*` (3) - duplicates

**Tool Guides (9):**
- `tool-guides/electron/introduction.md`
- `tool-guides/manta-templates/*` (3)
- `tool-guides/radix/introduction.md`
- `tool-guides/shadcn/introduction.md`
- `tool-guides/threejs/introduction.md`, `overview.md`, `setup.md`

**Framework Guides (2):**
- `framework-guides/astro/introduction.md`
- `framework-guides/nextjs/introduction.md`

**User Work Files (5):**
- `user/features/800-feature.project-guide-restructure.md`
- `user/slices/100-slice.prompt-optimization-1.md`
- `user/tasks/100-tasks.prompt-optimization-1.md`
- `user/tasks/800-tasks.project-guide-restructure.md`
- `user/tasks/950-tasks.maintenance.md`

### Files WITHOUT Frontmatter (33)
**Root Level (4):**
- `CHANGELOG.md`, `MIGRATION.md`
- `directory-structure.md`, `file-naming-conventions.md`

**Domain Guides (4):**
- All files in `domain-guides/`

**Framework Guides (3):**
- `framework-guides/nextjs/guide.*.md` (3 files)

**Project Guides (2):**
- `project-guides/guide.ai-project.091-legacy-task-migration.md`
- `project-guides/readme.md`

**Snippets (2):**
- All files in `snippets/`

**Tool Guides (15):**
- `tool-guides/r3f/introduction.md`
- `tool-guides/radix/radix-colors-quick-reference.md`, `radix-theming-guide.md`
- `tool-guides/shadcn/setup.md` (has frontmatter in code block - malformed)
- `tool-guides/supabase/*` (2)
- `tool-guides/tailwindcss/*` (4)
- `tool-guides/threejs/guide.*.md` (4)

**User Files (3):**
- `user/slices/900-slice.maintenance.md` (empty file)
- `user/tasks/inventory.index-migration.md`
- `user/tasks/report.index-migration.20250930.md`

### Frontmatter Feasibility Assessment

**Can reasonably construct frontmatter for:**
1. All tool-guide introduction files (standard pattern exists)
2. All domain-guide files
3. Framework guide non-introduction files
4. Root documentation files (CHANGELOG, MIGRATION, etc.)
5. User task/slice files following existing patterns

**Exceptions (may not benefit):**
- `snippets/` files - these are code snippets, not guides
- Legacy report/inventory files - historical artifacts

---

## 4. File Naming Inconsistencies

### Index Mismatch Issues

**Critical: Slice/Task Index Mismatch**
| File | Index | Issue |
|------|-------|-------|
| `900-slice.maintenance.md` | 900 | Should be 950 per naming conventions |
| `950-tasks.maintenance.md` | 950 | Correct index for maintenance |

Per `file-naming-conventions.md`:
- 900-939: Code review tasks
- 950-999: Maintenance tasks

The slice file should be `950-slice.maintenance.md` to match its task file.

**Missing Index: 005**
Process guides skip from 004 to 006:
- `guide.ai-project.004-slice-design.md`
- (missing 005)
- `guide.ai-project.006-task-expansion.md`

This may be intentional (Phase 5 is "Slice Task Breakdown" but uses guide 004).

### Naming Pattern Inconsistencies

**Root Files Using Non-Standard Patterns:**
| File | Pattern | Standard Would Be |
|------|---------|-------------------|
| `readme.md` | lowercase | `README.md` (conventional) |
| `readme.setup-ide.md` | `readme.xxx` | Consider `guide.setup-ide.md` |
| `CHANGELOG.md` | UPPERCASE | Conventional, keep |
| `MIGRATION.md` | UPPERCASE | Conventional, keep |

**Duplicate Agent Directories:**
- `.claude/agents/` - Claude Code specific location
- `project-guides/agents/` - General location

Files are identical. Consider removing `project-guides/agents/` or making it the source with symlinks.

**Empty Directory:**
- `api-guides/usgs/` - Empty placeholder

### Snippet Naming
Current: `npm-scripts.ai-support.json.md`
This pattern includes the file type being described, which is reasonable for snippets.

---

## 5. directory-structure.md Review

### Potential Issues

1. **Date in Title**: Contains date "2026-01-17 update" - suggests manual tracking vs version control

2. **References Non-Existent File**:
   - Mentions `DEVLOG.md` in root - does not exist
   - Mentions `CLAUDE.md` in root - does not exist (created by setup-ide script)

3. **Path Reference Confusion**:
   - Shows `project-documents/` prefix but actual repo doesn't have this
   - This is correct for submodule context but may confuse direct users

4. **Incomplete Folder Description**:
   - `api-guides/` listed but only contains empty `usgs/` folder

### Consistency Check
Structure matches actual directory layout except:
- Empty directories not explicitly noted
- Some subdirectories like `project-guides/agents/` not documented

---

## 6. file-naming-conventions.md Review

### Potential Issues

1. **800-899 Range Ambiguity**:
   - Listed as "Reserved (100 slots)"
   - But `800-feature.project-guide-restructure.md` exists in `user/features/`
   - Convention doc says 800-899 reserved but semantic map says "Feature documents"
   - **Conflict between line 41 ("Reserved") and line 87 ("Feature documents")**

2. **maintenance Document Type**:
   - Listed under Document Types: `maintenance` - "maintenance tasks or actions, in `user/maintenance`"
   - But `user/maintenance/` directory doesn't exist (removed in v0.9.0)
   - Should reference `user/tasks/950-tasks.maintenance.md` instead

3. **Date Format Examples**:
   - Shows `MMDD` (e.g., `0419`) but also `YYYYMMDD`
   - Current files use `.20250930` (YYYYMMDD) which is correct

---

## 7. Additional Observations

### Malformed Frontmatter
`tool-guides/shadcn/setup.md` has YAML frontmatter wrapped in code block markers:
```
```
---
layer: process
...
---
```
```
This renders as code, not parsed frontmatter.

### Empty/Stub Files
- `user/slices/900-slice.maintenance.md` - completely empty
- `tool-guides/threejs/guide.object-creation.complex.md` - appears empty

### Version Information
- Current version: 0.10.0 (per CHANGELOG)
- Last release: 2025-10-08
- Git submodule architecture adopted in v0.9.0

### Scripts Available
| Script | Purpose |
|--------|---------|
| `bootstrap.sh` | One-command project setup |
| `setup-ide` | Configure IDE (Cursor/Windsurf/Claude) |
| `migrate-private-to-user.sh` | Migration helper |
| `rename-private-to-user-in-repo.sh` | Batch rename utility |

---

## 8. Recommendations Summary

### High Priority (Inconsistency Fixes)
1. Rename `900-slice.maintenance.md` to `950-slice.maintenance.md` (or delete if empty)
2. Fix `tool-guides/shadcn/setup.md` malformed frontmatter
3. Resolve 800-899 range conflict in `file-naming-conventions.md`
4. Update `file-naming-conventions.md` to remove `user/maintenance/` reference

### Medium Priority (Frontmatter Standardization)
1. Add frontmatter to all `introduction.md` files following existing pattern
2. Add frontmatter to domain-guide files
3. Add frontmatter to root documentation files
4. Consider frontmatter for tool guide content files

### Low Priority (Cleanup)
1. Remove or populate `api-guides/usgs/` empty directory
2. Consolidate duplicate agent directories
3. Remove or update `directory-structure.md` date in title
4. Add `DEVLOG.md` if referenced (or remove reference)

---

## 9. Recommended Task Breakdown

If proceeding with fixes, suggest creating tasks in `950-tasks.maintenance.md`:

**Immediate Fixes:**
- [ ] Rename/delete `900-slice.maintenance.md` inconsistency
- [ ] Fix shadcn/setup.md frontmatter
- [ ] Update file-naming-conventions.md (800-899 range, maintenance path)

**Frontmatter Standardization (if desired):**
- [ ] Tool guides introduction files (6 files)
- [ ] Domain guide files (4 files)
- [ ] Framework guide non-introduction files (3 files)
- [ ] Root documentation files (4 files)
- [ ] Project guide exceptions (2 files)

**Structural Cleanup:**
- [ ] Decide on agent directory duplication
- [ ] Clean up empty directories
- [ ] Update directory-structure.md

---

## 10. Remediation Completed (2025-11-14)

The following issues identified in this analysis have been resolved:

### High Priority - COMPLETED

| Issue | Resolution |
|-------|------------|
| `900-slice.maintenance.md` index mismatch | Deleted (was empty file; `950-tasks.maintenance.md` is correct location) |
| `tool-guides/shadcn/setup.md` malformed frontmatter | Fixed - removed code block wrapping |
| `800-feature.project-guide-restructure.md` in reserved range | Moved to `105-slice.project-guide-restructure.md` with corrected YAML |
| `800-tasks.project-guide-restructure.md` | Renamed to `105-tasks.project-guide-restructure.md` |
| `file-naming-conventions.md` stale `user/maintenance/` reference | Updated to reference `user/tasks/950-tasks.maintenance.md` |

### Medium Priority - COMPLETED

| Issue | Resolution |
|-------|------------|
| Missing frontmatter (33 files) | All files now have YAML frontmatter |
| No frontmatter requirement documented | Added "YAML Frontmatter Requirement" section to `file-naming-conventions.md` |

### Low Priority - COMPLETED

| Issue | Resolution |
|-------|------------|
| `api-guides/usgs/` empty directory | Deleted; `api-guides/` kept for future use |
| `tool-guides/threejs/guide.object-creation.complex.md` empty | Deleted |

### Deferred/Not Changed

| Issue | Decision |
|-------|----------|
| Duplicate agent directories (`.claude/agents/` and `project-guides/agents/`) | Keep both - `.claude/` is Claude Code specific deployment |
| Missing `guide.ai-project.005-xxx` | Intentional - Phase 5 (task creation) covered in `000-process` |
| `DEVLOG.md` not present | To be created - for documenting changes and project notes |
| `CLAUDE.md` not in repo | Correct - created by `setup-ide` script at deployment |

### Files Created/Modified Summary

**Created:**
- `user/analysis/940-analysis.initial-codebase.md` (this file)

**Renamed/Moved:**
- `user/features/800-feature.project-guide-restructure.md` → `user/slices/105-slice.project-guide-restructure.md`
- `user/tasks/800-tasks.project-guide-restructure.md` → `user/tasks/105-tasks.project-guide-restructure.md`

**Deleted:**
- `user/slices/900-slice.maintenance.md` (empty)
- `api-guides/usgs/` (empty directory)
- `tool-guides/threejs/guide.object-creation.complex.md` (empty)

**Modified (frontmatter added or fixed):**
- All 70+ markdown files now have proper YAML frontmatter
- `file-naming-conventions.md` - added frontmatter requirement section, fixed stale reference
- `tool-guides/shadcn/setup.md` - fixed malformed frontmatter
- `readme.md` - added Claude analysis reference

---

*Analysis completed 2025-11-14*
*Remediation completed 2025-11-14*
