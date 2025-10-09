---
item: project-guide-restructure
project: ai-project-guide
type: feature
lld: user/features/800-feature.project-guide-restructure.md
dependencies: []
projectState: Active development - restructuring layout from git subtree to git submodule
status: in-progress
lastUpdated: 2025-10-05
---

# Tasks: Restructured ai-project-guide Layout

## Context Summary

Converting ai-project-guide from git subtree integration to git submodule structure to:
- Separate framework guides (submodule) from user project documents (parent repo)
- Enable easy updates for both npm and non-npm projects
- Eliminate conflicts between framework updates and user work
- Simplify npm scripts by removing file copying dance

**Target Structure:**
```
project-documents/
├── ai-project-guide/    # Submodule (framework)
└── user/             # User work (parent repo)
```

## Task 1: Update npm Scripts

### 1.1 Update setup-guides Script
- [x] Modify `snippets/npm-scripts.ai-support.json.md` with new submodule-based scripts
- [x] Create `project-documents/user/` subdirectories: architecture, slices, tasks, features, reviews, analysis
- [x] Add git submodule at `project-documents/ai-project-guide`
- [x] Create `.gitkeep` in `project-documents/user/` to ensure directory is tracked
- [x] Test script creates correct structure in fresh project (tested with Python bootstrap)
- **Success:** ✅ Updated snippet shows proper setup-guides script for user projects

### 1.2 Simplify update-guides Script
- [x] Renamed `guides` script to `update-guides` in snippet
- [x] Updated to simple: `git submodule update --remote project-documents/ai-project-guide`
- [x] No need to preserve user/ (it's in parent repo, not submodule)
- [x] Test update works without touching user files (tested locally)
- **Success:** ✅ Script updates guides without affecting `project-documents/user/`

### 1.3 Review sync-guides Script
- [x] Evaluated sync-guides - not present in current snippet
- [x] Not needed with new submodule structure
- [x] Standard git submodule commands handle all sync needs
- **Success:** ✅ No sync-guides needed - obsolete with submodule approach

### 1.4 Create Bootstrap Scripts (Bonus)
- [x] Created `scripts/bootstrap.sh` for universal setup
- [x] Created `scripts/bootstrap.py` for Python-based setup
- [x] Both support one-command curl setup
- [x] Auto-initialize git repo if needed
- [x] Tested in fresh Python projects
- **Success:** ✅ Bootstrap scripts enable zero-dependency setup for any project type

## Task 2: Update Path References in Documentation

### 2.1 Search for Guide Path References
- [x] Run: `grep -r "project-guides/" --include="*.md"` and document findings
- [x] Run: `grep -r "tool-guides/" --include="*.md"` and document findings
- [x] Run: `grep -r "framework-guides/" --include="*.md"` and document findings
- [x] Create list of all files needing path updates (17 files identified)
- **Success:** ✅ Complete inventory of files with guide path references

### 2.2 Update Guide References in Core Files
- [x] Update `readme.md` - change installation instructions and guide references (done in Task 3)
- [x] Update `CLAUDE.md` - update any guide path references
- [x] Update `readme.setup-ide.md` - update manual setup paths with path convention note
- [x] Update `prompt.ai-project.system.md` - all guide references updated, verified Context Init prompts correct
- [x] Update `file-naming-conventions.md` - already correct, uses user/ paths
- [x] Update `directory-structure.md` - updated to show ai-project-guide/ and user/ as siblings, removed research-crumbs
- **Success:** ✅ All core documentation references correct submodule paths

### 2.3 Update Guide References in project-guides/
- [x] Update `guide.ai-project.000-process.md` - updated structure diagram and all guide paths
- [x] Update `guide.ai-project.001-concept.md` - updated output path, fixed filename to 001-
- [x] Update `guide.ai-project.002-spec.md` - updated tool-guides path, fixed filename to 002-
- [x] Update `guide.ai-project.003-slice-planning.md` - already correct, uses user/ paths
- [x] Update `guide.ai-project.004-slice-design.md` - updated tool-guides and framework-guides paths
- [x] Update `guide.ai-project.006-task-expansion.md` - already correct, no guide references
- [x] Update `guide.ai-project.090-code-review.md` - already correct, no guide references
- [x] Update `guide.ai-project.091-legacy-task-migration.md` - already correct, uses user/ paths
- **Success:** ✅ All process guides reference correct paths

### 2.4 Update Monorepo-Specific References
- [x] Review monorepo context initialization prompt
- [x] Update guide references to `ai-project-guide/project-guides/guide.ai-project.000-process`
- [x] Verify `project-artifacts/` pattern remains unchanged (confirmed - user/ maps correctly)
- [ ] Test monorepo development workflow still works (requires monorepo testing)
- **Success:** ✅ Monorepo Context Init prompt updated, project-artifacts mapping preserved

## Task 3: Update readme.md Installation Instructions

### 3.1 Create New Installation Section
- [x] Write "Quick Start" section for new structure
- [x] Document bootstrap script setup for Python/Go/Rust/any project
- [x] Document npm/pnpm setup with updated scripts snippet
- [x] Document manual setup for advanced users
- [x] Add "Updating Guides" section with submodule commands
- [x] Updated IDE setup paths to reflect submodule location
- **Success:** ✅ Clear installation instructions for all project types

### 3.2 Create Migration Guide Section
- [x] Write "Migrating from git subtree" section in Advanced Usage
- [x] Document step-by-step migration:
  1. Backup `project-documents/user/`
  2. Remove subtree: `git rm -r project-documents`
  3. Restore private: `git checkout HEAD~1 -- project-documents/private`
  4. Add submodule: `git submodule add ... project-documents/ai-project-guide`
  5. Commit changes
- [x] Add backup restoration fallback
- [x] Document benefits of submodule over subtree
- **Success:** ✅ Existing users can migrate without losing work

### 3.3 Update Quick Reference
- [x] Updated Quick Start with one-command bootstrap
- [x] Added submodule update command prominently
- [x] Updated IDE setup commands for new paths
- [x] Clarified npm vs non-npm workflows
- **Success:** ✅ Quick reference reflects new structure

## Task 4: Consolidate and Update Setup Scripts

### 4.1 Analyze Existing Template Scripts
- [x] Review current `setup-guides.sh` from template(s) (found in scripts/monorepo-templates/)
- [x] Review current `update-guides.sh` from template(s) (found in scripts/monorepo-templates/)
- [x] Document capabilities and features of existing scripts
- [x] Identify differences between template versions (React template reviewed - no React-specific code)
- [x] Compare with bootstrap scripts already created
- [x] Created GitHub issue #5 for org private guides feature (deferred to future)
- [x] Resolved directory structure mismatch (finalized: analysis, architecture, features, project-guides, reviews, slices, tasks)
- [x] Confirmed git submodule approach is superior to rsync approach
- [x] Confirmed no special monorepo handling needed (same paths work everywhere)
- **Success:** ✅ Complete understanding of current script capabilities and submodule benefits

### 4.2 Evaluate Consolidation Feasibility
- [x] Determine if scripts can be unified and moved to ai-project-guide/scripts/
- [x] Identify any template-specific logic that must remain separate (none - framework-agnostic)
- [x] Assess chicken-and-egg problem: how do fresh templates get the scripts initially?
- [x] Determine script distribution mechanism from monorepo to templates (manual copy stubs)
- [x] Document pros/cons of consolidation vs keeping distributed
- [x] **Decision:** Option B - Minimal stub scripts in templates, full scripts in ai-project-guide
- **Success:** ✅ Clear decision on script consolidation strategy

### 4.3 Update Scripts for New Directory Structure
- [x] Update script paths to use `project-documents/ai-project-guide/` structure (already done in Task 1)
- [x] Update `user/` subdirectory creation (analysis, architecture, features, project-guides, reviews, slices, tasks)
- [x] Verify scripts create `.gitkeep` in user/ directory (confirmed)
- [x] Update any hardcoded paths or assumptions about structure (all paths updated)
- [x] Ensure scripts handle both fresh install and already-installed cases (idempotent checks in place)
- **Success:** ✅ Scripts work correctly with new submodule structure

### 4.4 Update File Naming Patterns
- [x] Review scripts for any filename pattern assumptions (none found - scripts only create directories)
- [x] Update to use `nnn-` index patterns where applicable (N/A - scripts don't create indexed files)
- [x] Ensure consistency with `file-naming-conventions.md` (verified - no conflicts)
- [x] Update any date format patterns (MMDD vs YYYYMMDD) (N/A - scripts don't use dates)
- **Success:** ✅ Scripts use current naming conventions (no file creation, only directories)

### 4.5 Resolve Initial Bootstrap Problem
- [x] Document how templates initially get setup scripts (stub scripts copied to templates)
- [x] Determine if scripts are copied from ai-project-guide/scripts during template creation (yes - manual copy of stubs)
- [x] Design solution for fresh template clones (3-line stub downloads bootstrap.sh from GitHub)
- [x] Update npm scripts in snippet to handle bootstrap case (already updated in Task 1)
- [x] Created template-stubs/ directory with setup-guides.sh and update-guides.sh
- [x] Created README.md documentation for template maintainers
- [ ] Test bootstrap flow: fresh template → pnpm setup-guides → working state (requires template testing)
- **Success:** ✅ Clear, working bootstrap mechanism documented (testing deferred to Task 5)

### 4.6 Implementation and Testing
- [x] Move/create consolidated scripts in ai-project-guide/scripts/ (bootstrap.sh, bootstrap.py, setup-project-guides.py already exist)
- [x] Update `snippets/npm-scripts.ai-support.json.md` with final script calls (done in Task 1)
- [x] Create any necessary wrapper or bootstrap logic (template-stubs created)
- [x] Document script distribution process for monorepo (README.md in template-stubs/)
- [ ] Test scripts in isolation (outside of npm) (deferred to Task 5)
- [ ] Test npm wrapper scripts (deferred to Task 5)
- [ ] **TODO:** Copy template stubs to monorepo templates before completion
- **Success:** ✅ Scripts consolidated and documented (testing deferred to Task 5)

## Task 5: Testing and Validation

### 5.1 Test npm/pnpm Project Setup
- [ ] Create test React/Next.js project
- [ ] Run `pnpm setup-guides`
- [ ] Verify directory structure created correctly
- [ ] Test creating slice in `user/slices/`
- [ ] Test guide updates with `pnpm update-guides`
- [ ] Verify guides update without affecting private files
- **Success:** Full workflow works in npm project

### 5.2 Test Non-npm Project Setup
- [ ] Create test Python project
- [ ] Manually set up structure per readme instructions
- [ ] Test creating project documents in `user/`
- [ ] Test guide updates with `git submodule update --remote`
- [ ] Verify all prompts work correctly
- **Success:** Full workflow works in Python project

### 5.3 Test Monorepo Development
- [ ] Test in monorepo template development environment
- [ ] Verify `project-artifacts/` pattern works unchanged
- [ ] Test guide references resolve correctly
- [ ] Verify no contamination of templates with dev documents
- **Success:** Monorepo development workflow unaffected

### 5.4 Validate All Prompts
- [ ] Test Phase 1: Concept Creation prompt
- [ ] Test Phase 2: Spec Creation prompt
- [ ] Test Phase 3: Slice Planning prompt
- [ ] Test Phase 4: Slice Design prompt
- [ ] Test Phase 5: Task Breakdown prompt
- [ ] Test Phase 7: Task Implementation prompt
- [ ] Test Feature Design prompt
- [ ] Test Analysis prompts (5 variants)
- [ ] Verify all guide references resolve correctly
- **Success:** All prompts work with new structure

## Task 6: Create Migration Documentation

### 6.1 Write Migration Guide Document
- [ ] Create `docs/migration-submodule.md` or similar
- [ ] Document prerequisites (git version, backup steps)
- [ ] Provide step-by-step migration instructions
- [ ] Include verification steps after migration
- [ ] Add troubleshooting section
- **Success:** Comprehensive migration guide available

### 6.2 Create FAQ Document
- [ ] Document "Why switch from subtree to submodule?"
- [ ] Document "How do I update guides?"
- [ ] Document "What if I have merge conflicts?"
- [ ] Document "How does this work for non-npm projects?"
- [ ] Document "What changed with monorepo development?"
- **Success:** Common questions answered

### 6.3 Update CHANGELOG
- [ ] Add entry for version 0.9.0 or 1.0.0
- [ ] Document breaking change: new directory structure
- [ ] List migration steps briefly
- [ ] Link to detailed migration guide
- [ ] Note benefits of new structure
- **Success:** CHANGELOG reflects major version change

## Task 7: Final Validation and Release

### 7.1 Final Review
- [ ] Review all changed files for consistency
- [ ] Verify no broken links in documentation
- [ ] Check all examples use correct paths
- [ ] Ensure backward compatibility notes are clear
- [ ] Review with team/users if applicable
- **Success:** All changes reviewed and validated

### 7.2 Version and Tag
- [ ] Update version to 0.9.0 or 1.0.0 in package.json
- [ ] Create git tag for release
- [ ] Push tag to repository
- [ ] Create GitHub release with migration notes
- **Success:** Release tagged and published

### 7.3 Communication
- [ ] Announce change to users (if applicable)
- [ ] Provide migration support resources
- [ ] Update any external documentation
- [ ] Monitor for migration issues
- **Success:** Users informed and supported through migration

## Notes

- This is a breaking change requiring user migration
- Prioritize backward compatibility where possible
- Test thoroughly in all supported environments
- Provide clear migration path and support
- Consider creating migration helper script if needed
