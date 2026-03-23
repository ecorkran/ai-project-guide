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
cd project-documents/ai-project-guide
git pull origin main
cd ../..
```

If using npm/pnpm, update the package version instead.

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

**Option B (acceptable for completed/stable projects):** Leave the concept file at 001. The index collision with the initiative plan is cosmetic — both files are in the same directory but serve different purposes. This is acceptable if the project is no longer actively using the concept document.

## Step 3: Create Initiative Plan (Primary Migration Task)

The initiative plan is a new Phase 1 document that formalizes your project's initiative decomposition. If your project already has architecture documents, you already have initiatives — they just aren't documented in a single plan.

### Using the Migration Prompt (Recommended)

The easiest approach is to use the **Initiative Plan Migration** prompt in `prompt.ai-project.system`. This prompt guides an agent to:

1. Scan your `user/architecture/` directory for existing architecture documents
2. Extract initiative names, indices, and dependencies
3. Generate an initiative plan document for your review

To use it, provide the prompt to your agent along with your project name. The agent will create `user/project-guides/001-initiative-plan.{project}.md`.

### Manual Creation

If you prefer to create the initiative plan manually:

1. Create `user/project-guides/001-initiative-plan.{project}.md`
2. Add frontmatter per `guide.ai-project.001-initiative-plan`
3. For each architecture document in `user/architecture/nnn-arch.*.md`, add an initiative entry using the same checklist format as slice plan overviews:

```
1. [ ] **(nnn) {Initiative Name}** — {Brief scope description}. Dependencies: {list or "None"}. Status: {not_started|in_progress|complete}
```

Where `nnn` is the base index from the architecture document's filename.

4. Add a Cross-Initiative Dependencies section declaring any edges between initiatives
5. Document your index gap convention (default: 20)

Refer to `guide.ai-project.001-initiative-plan` for the full document structure and conventions.

### Determining Initiative Status

- Architecture document exists, no slice plan → `not_started`
- Slice plan exists, slices in progress → `in_progress`
- All slices complete → `complete`

## Summary of Actions

- [ ] Update ai-project-guide to v0.14.0
- [ ] Rename concept document from `001-concept` to `000-concept` (if applicable)
- [ ] Update references to renamed guide files in your project's user/ documents
- [ ] Create initiative plan (`001-initiative-plan.{project}.md`) from existing architecture documents
