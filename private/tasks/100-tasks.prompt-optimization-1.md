---
slice: prompt-optimization-1
project: ai-project-guide
lld: private/slices/100-slice.prompt-optimization-1.md
dependencies: []
projectState: COMPLETE - All tasks finished, migration successful
lastUpdated: 2025-09-30
phase: 9
status: complete
---

## Context Summary

This task file implements the migration from a 2-digit (nn) to 3-digit (nnn) file indexing system for the ai-project-guide project. The work involves:

1. Renaming guide files from `guide.ai-project.nn-*` to `guide.ai-project.nnn-*`
2. Updating all references throughout the codebase to use 3-digit indices
3. Establishing new index range schema (050-089 for architecture, 100-799 for active work)
4. Updating documentation to reflect new conventions

**Critical Note:** This is an intricate, interdependent system. Errors can propagate widely. Execute methodically with verification at each step.

**Current State:**
- 8 guide files using 2-digit indices (00, 01, 02, 03, 04, 06, 90, 91)
- System prompts reference nn patterns
- File naming conventions describe 2-digit system
- Numerous cross-references throughout project

**Target State:**
- All guide files use 3-digit indices (000, 001, 002, 003, 004, 006, 090, 091)
- System prompts reference nnn patterns
- Architecture files use 050-089 range (special: 03-hld becomes 050-hld)
- Work items start at 100 (700 slots available)
- All cross-references updated and verified

## Tasks

### Phase 1: Preparation and Inventory

#### Task 1.1: Generate Complete File Inventory
**Objective:** Create comprehensive list of all files that need updating.

**Steps:**
- [x] List all guide files in project-guides/ directory
- [x] List all markdown files in project-guides/ (for reference updates)
- [x] List all files in private/project-guides/ (if exists)
- [x] List all files in private/slices/ (if exists)
- [x] List all files in private/tasks/ (if exists)
- [x] Create inventory document at `private/maintenance/inventory.index-migration.md`

**Success Criteria:**
- Complete inventory exists with counts for each category
- No files missed in the inventory

**Effort:** 1

---

#### Task 1.2: Document Current Cross-References
**Objective:** Map all existing cross-references before changes.

**Steps:**
- [x] Search for pattern `guide\.ai-project\.\d\d-` across all markdown files
- [x] Search for pattern `\d\d-concept\.`, `\d\d-spec\.`, `\d\d-hld\.`, `\d\d-slices\.`
- [x] Search for pattern `\d\d-slice\.`, `\d\d-tasks\.`, `\d\d-feature\.`
- [x] Search for YAML frontmatter patterns: `dependsOn:.*\d\d-`, `lld:.*\d\d-`
- [x] Document all findings in inventory file with file locations

**Success Criteria:**
- Complete map of all cross-references by pattern type
- Each reference includes source file and line number
- Baseline established for verification

**Effort:** 2

---

#### Task 1.3: Create Backup
**Objective:** Safety net for rollback if needed.

**Steps:**
- [x] Verify current directory with `pwd`
- [x] Create git branch for this work: `git checkout -b feature/index-migration-nnn`
- [x] Verify clean working tree: `git status`
- [x] Create commit of current state before changes

**Success Criteria:**
- New branch created
- Clean starting point established
- Can rollback via git if needed

**Effort:** 1

---

### Phase 2: File Naming Convention Updates

#### Task 2.1: Update file-naming-conventions.md (Root)
**Objective:** Update root-level file naming conventions document.

**Steps:**
- [x] Read `/Users/manta/source/repos/manta/ai-project-guide/file-naming-conventions.md`
- [x] Add new "Index Ranges and Semantic Structure" section before "Sequential Numbering Convention"
- [x] Insert range allocation content from slice design (section 3)
- [x] Update "Sequential Numbering Convention" section with 3-digit ranges
- [x] Update all examples: `01-tasks` → `100-tasks`, etc.
- [x] Update numbering rules to reference new ranges

**Success Criteria:**
- New index range schema documented (000-009, 010-049, 050-089, 090-099, 100-799, 800-899, 900-949, 950-999)
- All examples use 3-digit indices
- Clear explanation of range semantics

**Effort:** 2

---

#### Task 2.2: Update file-naming-conventions.md (Project-Guides)
**Objective:** Update project-guides-level file naming conventions document.

**Steps:**
- [x] Read `/Users/manta/source/repos/manta/ai-project-guide/project-guides/file-naming-conventions.md`
- [x] Add new "Index Ranges and Semantic Structure" section
- [x] Update "Sequential Numbering Convention" with 3-digit system
- [x] Update all examples to 3-digit indices
- [x] Ensure consistency with root-level document

**Success Criteria:**
- Both file-naming-conventions.md files consistent
- All examples use 3-digit system
- Range semantics clearly documented

**Effort:** 2

---

### Phase 3: Guide File Renaming

#### Task 3.1: Rename Guide Files with Git
**Objective:** Rename all guide files preserving git history.

**Steps:**
- [x] Verify current directory: `pwd` (should be project root)
- [x] Execute git renames in project-guides/:
  - [x] `git mv project-guides/guide.ai-project.00-process.md project-guides/guide.ai-project.000-process.md`
  - [x] `git mv project-guides/guide.ai-project.01-concept.md project-guides/guide.ai-project.001-concept.md`
  - [x] `git mv project-guides/guide.ai-project.02-spec.md project-guides/guide.ai-project.002-spec.md`
  - [x] `git mv project-guides/guide.ai-project.03-slice-planning.md project-guides/guide.ai-project.003-slice-planning.md`
  - [x] `git mv project-guides/guide.ai-project.04-slice-design.md project-guides/guide.ai-project.004-slice-design.md`
  - [x] `git mv project-guides/guide.ai-project.06-task-expansion.md project-guides/guide.ai-project.006-task-expansion.md`
  - [x] `git mv project-guides/guide.ai-project.90-code-review.md project-guides/guide.ai-project.090-code-review.md`
  - [x] `git mv project-guides/guide.ai-project.91-legacy-task-migration.md project-guides/guide.ai-project.091-legacy-task-migration.md`
- [x] Run `git status` to verify renames detected
- [x] List files to confirm: `ls project-guides/guide.ai-project.*.md`

**Success Criteria:**
- All 8 guide files renamed with git history preserved
- Git shows renames, not deletes + adds
- No old 2-digit guide files remain

**Effort:** 1

---

### Phase 4: System Prompt Updates

#### Task 4.1: Update prompt.ai-project.system.md File References
**Objective:** Update all nn patterns to nnn in system prompts.

**Steps:**
- [x] Read `project-guides/prompt.ai-project.system.md`
- [x] Update guide file references:
  - [x] All `guide.ai-project.00-process` → `guide.ai-project.000-process`
  - [x] All `guide.ai-project.01-concept` → `guide.ai-project.001-concept` (none found)
  - [x] All `guide.ai-project.02-spec` → `guide.ai-project.002-spec`
  - [x] All `guide.ai-project.03-slice-planning` → `guide.ai-project.003-slice-planning`
  - [x] All `guide.ai-project.04-slice-design` → `guide.ai-project.004-slice-design` (none found)
  - [x] All `guide.ai-project.06-task-expansion` → `guide.ai-project.006-task-expansion`
  - [x] All `guide.ai-project.90-code-review` → `guide.ai-project.090-code-review` (none found)
  - [x] All `guide.ai-project.91-legacy-task-migration` → `guide.ai-project.091-legacy-task-migration` (none found)

**Success Criteria:**
- All guide references use 3-digit indices
- No `guide.ai-project.nn-` patterns remain (where nn is 2 digits)

**Effort:** 2

---

#### Task 4.2: Update prompt.ai-project.system.md Project File Patterns
**Objective:** Update project-specific file naming patterns.

**Steps:**
- [x] Update concept file references: `01-concept.{project}` → `001-concept.{project}` (already correct)
- [x] Update spec file references: `02-spec.{project}` → `002-spec.{project}`
- [x] Update HLD file references: `03-hld.{project}` → `050-hld.{project}` (note: architecture range)
- [x] Update slice plan references: `03-slices.{project}` → `003-slices.{project}`
- [x] Update slice file patterns: `nn-slice.{slice}` → `nnn-slice.{slice}`
- [x] Update task file patterns: `nn-tasks.{slice}` → `nnn-tasks.{slice}`
- [x] Update feature file patterns: `nn-feature.{feature}` → `nnn-feature.{feature}` (none found)

**Success Criteria:**
- All project file patterns use 3-digit indices
- HLD correctly references 050 range (not 003)
- No nn-* patterns remain in templates

**Effort:** 2

---

### Phase 5: Cross-Reference Updates in Guide Files

#### Task 5.1: Update guide.ai-project.000-process.md
**Objective:** Update all internal references in the main process guide.

**Steps:**
- [x] Read `project-guides/guide.ai-project.000-process.md`
- [x] Update YAML frontmatter `dependsOn` references (if any)
- [x] Update all guide file references to 3-digit indices
- [x] Update all project file pattern references
- [x] Search for any remaining `\d\d-` patterns and evaluate
- [x] Verify all cross-references point to correct files

**Success Criteria:**
- All references use 3-digit system
- No broken links
- YAML frontmatter updated

**Effort:** 2

---

#### Task 5.2: Update guide.ai-project.001-concept.md
**Objective:** Update all internal references in concept guide.

**Steps:**
- [x] Read `project-guides/guide.ai-project.001-concept.md`
- [x] Update YAML frontmatter: `dependsOn: [guide.ai-project.000-process.md]`
- [x] Update guide references to 000-process
- [x] Update file saving instruction: `01-concept` → `001-concept`
- [x] Search for remaining 2-digit patterns

**Success Criteria:**
- All references use 3-digit indices
- File saving instructions correct

**Effort:** 1

---

#### Task 5.3: Update guide.ai-project.002-spec.md
**Objective:** Update all internal references in spec guide.

**Steps:**
- [x] Read `project-guides/guide.ai-project.002-spec.md`
- [x] Update YAML frontmatter: `dependsOn: [guide.ai-project.001-concept.md]`
- [x] Update guide references
- [x] Update file saving instruction: `02-spec` → `002-spec`
- [x] Search for remaining 2-digit patterns

**Success Criteria:**
- All references use 3-digit indices
- File saving instructions correct

**Effort:** 1

---

#### Task 5.4: Update guide.ai-project.003-slice-planning.md
**Objective:** Update all internal references in slice planning guide.

**Steps:**
- [x] Read `project-guides/guide.ai-project.003-slice-planning.md`
- [x] Update YAML frontmatter `dependsOn` array to use 3-digit guide names
- [x] Update guide references in content
- [x] Update HLD file reference: `03-hld.{project}` → `050-hld.{project}`
- [x] Update slice plan reference: `03-slices.{project}` → `003-slices.{project}`
- [x] Search for remaining 2-digit patterns

**Success Criteria:**
- All references use 3-digit indices
- HLD correctly references 050 range
- Slice plan correctly references 003

**Effort:** 2

---

#### Task 5.5: Update guide.ai-project.004-slice-design.md
**Objective:** Update all internal references in slice design guide.

**Steps:**
- [x] Read `project-guides/guide.ai-project.004-slice-design.md`
- [x] Update YAML frontmatter `dependsOn` array
- [x] Update spec reference: `02-spec.{project}` → `002-spec.{project}`
- [x] Update HLD reference: `03-hld.{project}` → `050-hld.{project}`
- [x] Update slice plan reference: `03-slices.{project}` → `003-slices.{project}`
- [x] Update slice file pattern: `nn-slice` → `nnn-slice`
- [x] Search for remaining 2-digit patterns

**Success Criteria:**
- All references use 3-digit indices
- HLD correctly in 050 range
- Slice patterns use nnn

**Effort:** 2

---

#### Task 5.6: Update guide.ai-project.006-task-expansion.md
**Objective:** Update all internal references in task expansion guide.

**Steps:**
- [x] Read `project-guides/guide.ai-project.006-task-expansion.md`
- [x] Update YAML frontmatter `dependsOn` array
- [x] Update all guide references
- [x] Update example YAML: `lld: private/slices/01-slice.*` → `lld: private/slices/nnn-slice.*`
- [x] Update task file pattern examples
- [x] Search for remaining 2-digit patterns

**Success Criteria:**
- All references use 3-digit indices
- Example YAML uses nnn patterns

**Effort:** 2

---

#### Task 5.7: Update guide.ai-project.090-code-review.md
**Objective:** Update all internal references in code review guide.

**Steps:**
- [x] Read `project-guides/guide.ai-project.090-code-review.md`
- [x] Update YAML frontmatter `dependsOn` array
- [x] Update guide references
- [x] Update any file naming pattern references
- [x] Search for remaining 2-digit patterns

**Success Criteria:**
- All references use 3-digit indices

**Effort:** 1

---

#### Task 5.8: Update guide.ai-project.091-legacy-task-migration.md
**Objective:** Update all internal references in legacy task migration guide.

**Steps:**
- [x] Read `project-guides/guide.ai-project.091-legacy-task-migration.md`
- [x] Update YAML frontmatter (if any)
- [x] Update guide references: 000-process, 003-slice-planning
- [x] Update project file patterns: `01-concept`, `02-spec`, `03-hld`, `03-slices`, `03-tasks`
- [x] Update HLD to 050 range
- [x] Update slice patterns to nnn
- [x] Search for remaining 2-digit patterns

**Success Criteria:**
- All references use 3-digit indices
- HLD in 050 range
- Slice/task patterns use nnn

**Effort:** 2

---

### Phase 6: Cross-Reference Updates in Supporting Files

#### Task 6.1: Update directory-structure.md
**Objective:** Update file tree examples with 3-digit indices.

**Steps:**
- [x] Read `project-guides/directory-structure.md`
- [x] Update guide file listings in tree structure
- [x] Update project file examples: `01-concept`, `02-spec`, `03-hld`, `03-slices`
- [x] Update HLD to 050-hld
- [x] Update slice examples: `01-slice`, `02-slice` → `nnn-slice`
- [x] Update task examples: `01-tasks`, `02-tasks` → `nnn-tasks`
- [x] Update numbering range descriptions

**Success Criteria:**
- File tree shows 3-digit guide files
- Examples use nnn patterns
- HLD in 050 range
- Range descriptions updated

**Effort:** 2

---

#### Task 6.2: Update readme.md in project-guides/
**Objective:** Update guide file table and links.

**Steps:**
- [x] Read `project-guides/readme.md`
- [x] Update table entries for all guide files
- [x] Update markdown links to use 3-digit filenames
- [x] Verify links are functional
- [x] Update any file path references

**Success Criteria:**
- Table shows 3-digit guide names
- All links functional
- No broken references

**Effort:** 1

---

#### Task 6.3: Update notes.ai-project.onboarding.md
**Objective:** Update guide references in onboarding notes.

**Steps:**
- [x] Read `project-guides/notes.ai-project.onboarding.md`
- [x] Update YAML frontmatter `dependsOn`
- [x] Update guide references throughout content
- [x] Search for remaining 2-digit patterns

**Success Criteria:**
- All references use 3-digit indices

**Effort:** 1

---

#### Task 6.4: Update guide.ui-development.ai.md
**Objective:** Update guide references in UI development guide.

**Steps:**
- [x] Read `project-guides/guide.ui-development.ai.md`
- [x] Update YAML frontmatter `dependsOn`
- [x] Update guide references
- [x] Search for remaining 2-digit patterns

**Success Criteria:**
- All references use 3-digit indices

**Effort:** 1

---

#### Task 6.5: Update rules/ Directory Files
**Objective:** Update any guide references in rules files.

**Steps:**
- [x] List all .md files in `project-guides/rules/`
- [x] For each file:
  - [x] Read file
  - [x] Search for guide references
  - [x] Update to 3-digit indices
  - [x] Search for project file patterns
  - [x] Update to nnn patterns

**Success Criteria:**
- All rules files use 3-digit indices
- No broken references

**Effort:** 1

---

#### Task 6.6: Update agents/ Directory Files
**Objective:** Update any guide references in agent description files.

**Steps:**
- [x] List all .md files in `project-guides/agents/` (if exists)
- [x] For each file:
  - [x] Read file
  - [x] Search for guide or file pattern references
  - [x] Update to 3-digit/nnn patterns

**Success Criteria:**
- All agent files use 3-digit indices

**Effort:** 1

---

### Phase 7: Update Private Project Files (If They Exist)

#### Task 7.1: Update private/project-guides/ Files
**Objective:** Update any project-specific guide files.

**Steps:**
- [x] Check if `private/project-guides/` directory exists
- [x] If exists, list all .md files
- [x] For each file:
  - [x] Read file
  - [x] Update YAML frontmatter references
  - [x] Update guide references to 3-digit
  - [x] Update file references to appropriate patterns
  - [x] Search for remaining 2-digit patterns

**Success Criteria:**
- All project guide files updated (if any exist)
- YAML frontmatter correct
- All references use new system

**Effort:** 2

---

#### Task 7.2: Update private/slices/ Files
**Objective:** Update slice design files with new references.

**Steps:**
- [x] Check if `private/slices/` directory exists
- [x] If exists, list all .md files
- [x] For each file:
  - [x] Read file
  - [x] Update YAML frontmatter (particularly `lld` references)
  - [x] Update guide references
  - [x] Update project file references
  - [x] Search for remaining 2-digit patterns

**Success Criteria:**
- All slice files updated (if any exist)
- YAML references correct
- All references use new system

**Effort:** 2

---

#### Task 7.3: Update private/tasks/ Files
**Objective:** Update task files with new references.

**Steps:**
- [x] Check if `private/tasks/` directory exists
- [x] If exists, list all .md files
- [x] For each file:
  - [x] Read file
  - [x] Update YAML frontmatter (`lld` references)
  - [x] Update guide references
  - [x] Update slice/task file references
  - [x] Search for remaining 2-digit patterns

**Success Criteria:**
- All task files updated (if any exist)
- YAML references correct
- All references use new system

**Effort:** 2

---

### Phase 8: Verification

#### Task 8.1: Comprehensive Pattern Search
**Objective:** Verify no 2-digit patterns remain in critical locations.

**Steps:**
- [x] Search for `guide\.ai-project\.\d\d-` pattern across all markdown files
- [x] Search for `\d\d-concept\.`, `\d\d-spec\.`, `\d\d-slices\.` patterns
- [x] Special: Search for `\d\d-hld\.` pattern (should be 050-hld now)
- [x] Search for `\d\d-slice\.`, `\d\d-tasks\.`, `\d\d-feature\.` patterns
- [x] Review each match to determine if it's:
  - [x] A file reference that needs updating
  - [x] A code example that needs updating
  - [x] Content that should remain unchanged
- [x] Document any remaining 2-digit patterns with justification

**Success Criteria:**
- No unexpected 2-digit patterns remain
- All file references use 3-digit/nnn system
- Any remaining 2-digit content is justified

**Effort:** 2

---

#### Task 8.2: Verify File Renaming Complete
**Objective:** Confirm all guide files renamed correctly.

**Steps:**
- [x] List files: `ls project-guides/guide.ai-project.*.md`
- [x] Verify 8 guide files exist with 3-digit indices:
  - [x] guide.ai-project.000-process.md
  - [x] guide.ai-project.001-concept.md
  - [x] guide.ai-project.002-spec.md
  - [x] guide.ai-project.003-slice-planning.md
  - [x] guide.ai-project.004-slice-design.md
  - [x] guide.ai-project.006-task-expansion.md
  - [x] guide.ai-project.090-code-review.md
  - [x] guide.ai-project.091-legacy-task-migration.md
- [x] Verify no 2-digit guide files remain
- [x] Check git status shows renames properly

**Success Criteria:**
- All 8 guide files exist with 3-digit names
- No 2-digit guide files remain
- Git history preserved (shows as renames)

**Effort:** 1

---

#### Task 8.3: Test Prompt Execution
**Objective:** Verify prompts work with new file naming.

**Steps:**
- [x] Review key prompts in `prompt.ai-project.system.md`
- [x] Verify prompt templates reference correct file patterns
- [x] Confirm HLD references use 050 range
- [x] Confirm slice/task patterns use nnn format
- [x] Document any issues found

**Success Criteria:**
- Prompt templates consistent with new naming
- No references to old 2-digit system
- Ready for use in project work

**Effort:** 1

---

#### Task 8.4: Verify Documentation Consistency
**Objective:** Ensure all documentation aligned on new system.

**Steps:**
- [x] Review file-naming-conventions.md (both copies)
- [x] Verify index range schema documented
- [x] Verify examples use 3-digit system
- [x] Review directory-structure.md file tree
- [x] Review readme.md table
- [x] Confirm all consistent with each other

**Success Criteria:**
- Index ranges clearly documented (050-089 for architecture, 100-799 for work)
- All examples use 3-digit indices
- No conflicting information across documents

**Effort:** 1

---

### Phase 9: Finalization

#### Task 9.1: Update Current Slice File
**Objective:** Update this slice file itself to follow new conventions.

**Steps:**
- [x] Read current file: `private/slices/100-slice.prompt-optimization-1.md`
- [x] Verify YAML frontmatter correct
- [x] Update any internal references to guides or files
- [x] Ensure consistency with implemented changes

**Success Criteria:**
- Slice file follows its own recommendations
- All references use 3-digit system

**Effort:** 1

---

#### Task 9.2: Update Current Task File
**Objective:** Update this task file to follow new conventions.

**Steps:**
- [x] Read current file: `private/tasks/100-tasks.prompt-optimization-1.md`
- [x] Verify YAML frontmatter correct
- [x] Ensure lld reference uses correct slice path
- [x] Update any guide references in tasks

**Success Criteria:**
- Task file follows new conventions
- References correct

**Effort:** 1

---

#### Task 9.3: Create Verification Report
**Objective:** Document migration completion and results.

**Steps:**
- [x] Create report at `private/maintenance/report.index-migration.YYYYMMDD.md`
- [x] Document files changed (count and list)
- [x] Document patterns updated (with counts)
- [x] List any exceptions or special cases
- [x] Include verification results
- [x] Note any follow-up items

**Success Criteria:**
- Complete report of migration work
- All changes documented
- Ready for review

**Effort:** 1

---

#### Task 9.4: Git Commit
**Objective:** Create clean commit of all changes.

**Steps:**
- [x] Run `git status` to review all changes
- [x] Run `git diff` to review modifications
- [x] Stage all changes: `git add .`
- [x] Create descriptive commit message including:
  - [x] Summary of index system migration
  - [x] 2-digit to 3-digit guide file updates
  - [x] New architecture range (050-089)
  - [x] New work item range (100-799)
  - [x] Claude Code attribution
- [x] Commit changes
- [x] Verify commit created successfully

**Success Criteria:**
- Clean commit with all migration changes
- Descriptive commit message
- Ready for merge or review

**Effort:** 1

---

## Notes

**Important Reminders:**
- This system is intricate and interdependent - errors propagate
- Verify each phase before proceeding to next
- The HLD special case: 03-hld → 050-hld (architecture range, not 003)
- Use git mv for all file renames to preserve history
- Test comprehensively before finalizing

**Rollback Plan:**
- All work on feature branch
- Can discard branch if issues found
- Clean starting point preserved in main branch

**Estimated Total Effort:** 3/5 (medium complexity, high precision required)
