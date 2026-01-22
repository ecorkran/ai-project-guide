---
docType: inventory
project: ai-project-guide
date: 20250930
purpose: Track all files affected by nn → nnn index migration
status: completed
---

# Index Migration Inventory

## Guide Files to Rename (8 files)
- project-guides/guide.ai-project.00-process.md → guide.ai-project.000-process.md
- project-guides/guide.ai-project.01-concept.md → guide.ai-project.001-concept.md
- project-guides/guide.ai-project.02-spec.md → guide.ai-project.002-spec.md
- project-guides/guide.ai-project.03-slice-planning.md → guide.ai-project.003-slice-planning.md
- project-guides/guide.ai-project.04-slice-design.md → guide.ai-project.004-slice-design.md
- project-guides/guide.ai-project.06-task-expansion.md → guide.ai-project.006-task-expansion.md
- project-guides/guide.ai-project.90-code-review.md → guide.ai-project.090-code-review.md
- project-guides/guide.ai-project.91-legacy-task-migration.md → guide.ai-project.091-legacy-task-migration.md

## Markdown Files in project-guides/ (25 files)
Files that may contain cross-references:
- project-guides/agents/code-review-agent.md
- project-guides/agents/task-checker.md
- project-guides/agents/tester.md
- project-guides/directory-structure.md
- project-guides/file-naming-conventions.md
- project-guides/guide.ai-project.00-process.md
- project-guides/guide.ai-project.01-concept.md
- project-guides/guide.ai-project.02-spec.md
- project-guides/guide.ai-project.03-slice-planning.md
- project-guides/guide.ai-project.04-slice-design.md
- project-guides/guide.ai-project.06-task-expansion.md
- project-guides/guide.ai-project.90-code-review.md
- project-guides/guide.ai-project.91-legacy-task-migration.md
- project-guides/guide.ui-development.ai.md
- project-guides/notes.ai-project.onboarding.md
- project-guides/prompt.ai-project.system.md
- project-guides/prompt.code-review-crawler.md
- project-guides/readme.md
- project-guides/rules/general.md
- project-guides/rules/python.md
- project-guides/rules/react.md
- project-guides/rules/review.md
- project-guides/rules/sql.md
- project-guides/rules/testing.md
- project-guides/rules/typescript.md

## Files in user/project-guides/ (0 files)
Directory does not exist

## Files in user/slices/ (2 files)
- user/slices/100-slice.prompt-optimization-1.md
- user/slices/900-slice.maintenance.md

## Files in user/tasks/ (1 file)
- user/tasks/100-tasks.prompt-optimization-1.md

## Additional Files to Check
Root level files:
- file-naming-conventions.md (in root)

## Cross-Reference Patterns Found

### Pattern: `guide.ai-project.nn-` (guide file references)
Found in 62+ locations across:
- CLAUDE.md (9 references)
- readme.md (5 references)
- CHANGELOG.md (22 references)
- project-guides/*.md files (all 8 guide files, plus supporting files)
- project-guides/rules/*.md files
- project-guides/prompt.ai-project.system.md (extensive - 15+ references)

### Pattern: `nn-concept.`, `nn-spec.`, `nn-hld.`, `nn-slices.`
Found in 35+ locations:
- prompt.ai-project.system.md (primary source)
- guide.ai-project.01-concept.md
- guide.ai-project.02-spec.md
- guide.ai-project.03-slice-planning.md
- guide.ai-project.04-slice-design.md
- guide.ai-project.91-legacy-task-migration.md
- directory-structure.md
- readme.md

**Special case:** `03-hld.{project}.md` → `050-hld.{project}.md` (architecture range, not 003)

### Pattern: `nn-slice.`, `nn-tasks.`, `nn-feature.`
Found in 25+ locations:
- file-naming-conventions.md (both root and project-guides)
- directory-structure.md
- guide.ai-project.06-task-expansion.md (YAML examples)
- Various example references throughout guides

### Pattern: YAML frontmatter `dependsOn:`
Found in 8 guide files with references like:
- `dependsOn: [guide.ai-project.00-process.md]`
- `dependsOn: [guide.ai-project.01-concept.md]`
- `dependsOn: [guide.ai-project.02-spec.md]`
etc.

### Pattern: YAML frontmatter `lld:`
Found in task examples:
- `lld: user/slices/01-slice.user-authentication.md`

## Summary
- Total guide files to rename: 8
- Total markdown files to check for references: 25+ (project-guides) + 2 (slices) + 1 (tasks) + 1 (root) + 5 (various) = 34+
- Private project-guides: None (directory doesn't exist)
- Private slices: 2 files
- Private tasks: 1 file
- **Estimated cross-reference updates needed: 150+ locations**

## Key Files Requiring Extensive Updates
1. **prompt.ai-project.system.md** - 50+ references to update
2. **guide.ai-project.00-process.md** - 10+ references
3. **directory-structure.md** - 15+ references
4. **file-naming-conventions.md** (both copies) - 20+ references
5. **readme.md** (root) - 10+ references
6. **CLAUDE.md** - 10+ references
7. **All 8 guide files** - internal cross-references
