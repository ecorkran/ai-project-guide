---
docType: migration
scope: project-wide
description: Migration instructions to v0.14.0 — phase renumbering, initiative plan, spec removal
targetVersion: "0.14.0"
dateCreated: 20260323
dateUpdated: 20260323
---

# v0.14.0 Migration Guide

## Overview

This version restructures the project phase numbering and introduces the **Initiative Plan** as a new Phase 1. The process guide is renamed, concept moves to Phase 0, and the legacy spec guide is removed.

## Step 1: Update Guides

Update your ai-project-guide submodule to the latest version. This gives you all the new and renamed guide files automatically.

```bash
cf guides update
```


## Step 2: Structural Changes (Awareness)

### Phase Renumbering

| Before | After |
|--------|-------|
| `guide.ai-project.000-process.md` (Phase 0, meta) | `guide.ai-project.process.md` (meta, no index) |
| `guide.ai-project.001-concept.md` (Phase 1) | `guide.ai-project.000-concept.md` (Phase 0) |
| _(did not exist)_ | `guide.ai-project.001-initiative-plan.md` (Phase 1, new) |
| `guide.ai-project.002-spec.md` (Phase 2 variant) | _(removed — Phase 2 is always architecture)_ |

Phases 2-7 are unchanged in numbering.

### What This Means for Your Project

- **Process guide references**: Any references to `guide.ai-project.000-process` should be updated to `guide.ai-project.process`. These may appear in your task files, slice designs, or custom documentation.
- **Concept guide references**: Any references to `guide.ai-project.001-concept` should be updated to `guide.ai-project.000-concept`.
- **Spec guide references**: Any references to `guide.ai-project.002-spec` can be removed. Phase 2 is always architecture now.

### Concept Document Reindex

Most projects will have a concept document at `user/project-guides/001-concept.{project}.md`. The 001 index is now reserved for the initiative plan. You have two options:

**Option A (recommended for active projects):** Rename to `000-concept.{project}.md` and update any references to it.

```bash
cd user/project-guides
git mv 001-concept.{project}.md 000-concept.{project}.md
```

Then search your `user/` directory for references to the old filename and update them.

## Step 3: Create Initiative Plan (Primary Migration Task)

The initiative plan is a new Phase 1 document that formalizes your project's initiative decomposition. If your project already has architecture documents, you already have initiatives — they just aren't documented in a single plan.

### Migration Prompt

Use the following prompt with your agent to generate the initiative plan from existing architecture documents. The agent will scan your architecture directory, extract initiative information, and produce a plan for your review.

```markdown
We need to create an initiative plan for project {project} by scanning existing architecture documents. Use `guide.ai-project.001-initiative-plan` for the document structure and conventions.

Your role is Architect, working with the Project Manager.

**Process**:
1. Scan `user/architecture/` for existing `nnn-arch.*.md` files
2. For each architecture document, extract:
   - Initiative name (from the `component` field or document title)
   - Base index (from the `archIndex` field or filename prefix)
   - Dependencies (from the document's dependency references)
3. Scan `user/architecture/` for `nnn-slices.*.md` to determine initiative status:
   - Has slice plan = at least in_progress
   - All slices complete = complete
   - No slice plan yet = not_started
4. Generate initiative plan at `user/project-guides/001-initiative-plan.{project}.md`
5. Populate cross-initiative dependencies from architecture document references
6. Present the generated plan to the PM for review before writing

For each initiative, use the same checklist format as slice plan overviews:
1. [ ] **(nnn) {Initiative Name}** — {Brief scope description}. Dependencies: {list or "None"}. Status: {status}

**Important**: This is a migration task — the initiatives already exist as architecture documents. The goal is to create the missing initiative plan that documents them, not to reorganize the existing work. Existing indices should be preserved.

Include YAML frontmatter per `guide.ai-project.001-initiative-plan`.
```

## Summary of Actions

- [ ] Update ai-project-guide to v0.14.0
- [ ] Rename concept document from `001-concept` to `000-concept` (if applicable)
- [ ] Update references to renamed guide files in your project's user/ documents
- [ ] Create initiative plan (`001-initiative-plan.{project}.md`) from existing architecture documents
