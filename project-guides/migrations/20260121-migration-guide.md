---
docType: migration
scope: project-wide
description: Migration instructions for project consistency standards
targetVersion: "0.11.0"
dateCreated: 20260121
dateUpdated: 20260121
---

# Project Consistency Migration Guide

Migration instructions for updating projects to match ai-project-guide consistency standards.

## Overview

This guide helps update existing projects to match the new consistency requirements introduced in the ai-project-guide framework. Apply these changes after updating your ai-project-guide submodule.

## 1. Update ai-project-guide Submodule

```bash
git submodule update --remote project-documents/ai-project-guide
```

## 2. YAML Frontmatter Requirements

All markdown files must have YAML frontmatter. Check all files in:

- `user/architecture/`
- `user/slices/`
- `user/tasks/`
- `user/features/`
- `user/analysis/`
- `user/reviews/`

**Minimum frontmatter:**

```yaml
---
docType: [slice|tasks|analysis|architecture|feature|review]
---
```

## 3. Date Format Standardization

All dates in YAML must use **YYYYMMDD** format (no dashes):

**Before:**
```yaml
lastUpdated: 2025-10-08
date: 2025-09-30
```

**After:**
```yaml
dateCreated: 20250930
dateUpdated: 20251008
```

**Fields to check:** `created`, `lastUpdated`, `date`

## 4. Add Missing Date Fields

Add these fields where missing:

```yaml
dateCreated: YYYYMMDD      # When file was first created (immutable)
dateUpdated: YYYYMMDD  # Most recent modification
```

If you don't know when a file was created, use git history:

```bash
git log --follow --format=%ad --date=format:'%Y%m%d' -- path/to/file | tail -1
```

## 5. Task/Slice File Frontmatter Patterns

**Task files** (`nnn-tasks.*.md`):

```yaml
---
docType: tasks
slice: slice-name
sliceIndex: nnn
project: project-name
lld: user/slices/nnn-slice.slice-name.md
dependencies: []
projectState: brief current state
status: [in_progress|completed]
dateCreated: YYYYMMDD
dateUpdated: YYYYMMDD
---
```

**Slice files** (`nnn-slice.*.md`):

```yaml
---
docType: slice
layer: project
project: project-name
sliceIndex: nnn
sliceName: slice-name
status: [in_progress|completed]
dependencies: []
description: brief description
dateCreated: YYYYMMDD
dateUpdated: YYYYMMDD
---
```

## 6. File Naming - Index Requirement

**All files in `user/tasks/` must be indexed.** Use the 950-999 range for maintenance items:

| Index Range | Purpose |
|-------------|---------|
| 100-749 | Slices and slice-linked features/tasks |
| 750-799 | Standalone features |
| 940-949 | Codebase analysis |
| 950-999 | Maintenance tasks, inventories, reports |

**Example renames:**
- `inventory.index-migration.md` → `952-inventory.index-migration.md`
- `report.index-migration.20250930.md` → `953-report.index-migration.md`

## 7. Quick Validation

**Find files missing frontmatter:**

```bash
find project-documents/user -name "*.md" | while read f; do
  first=$(head -1 "$f")
  if [ "$first" != "---" ]; then echo "$f"; fi
done
```

**Find dates with dashes:**

```bash
grep -rn "lastUpdated:\|date:\|created:" project-documents/user --include="*.md" | grep -E "[0-9]{4}-[0-9]{2}-[0-9]{2}"
```

## 8. Reference Documents

After updating the submodule, these documents contain the authoritative standards:

- [file-naming-conventions.md](../file-naming-conventions.md) - All naming and formatting rules
- [DEVLOG.md](../../DEVLOG.md) - Recent changes and decisions

## Summary of Changes

| What | Old | New |
|------|-----|-----|
| Frontmatter | Optional | Required on all .md files |
| Date format | YYYY-MM-DD | YYYYMMDD |
| Date fields | lastUpdated only | Add created where missing |
| Status field | Inconsistent | Use in_progress, completed, deprecated |
| File indexing | Optional for some files | Required for all user/tasks/ files |
| Standalone features | No dedicated range | 750-799 range |
| Slice range | 100-799 | 100-749 (standalone features carved out) |

---

*Migration guide created 20260121*
