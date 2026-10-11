---
docType: slice-design
slice: phase-renumbering-and-initiative-plan
project: ai-project-guide
parent: user/architecture/110-slices.schema-and-phases-update.md
dependencies: []
interfaces: [112-cross-reference-verification]
dateCreated: 20260322
dateUpdated: 20260324
status: complete
---

# Slice Design: Phase Renumbering and Initiative Plan

## Overview

Restructure the project phase numbering to make Concept phase 0, add a new Initiative Plan as phase 1, remove the legacy spec phase, rename the process guide to drop its numeric index, and update all prompts, guides, and references accordingly. This also includes removing deprecated prompts.

## Value

The current phase structure has a gap between concept (a single project-level document) and architecture (which can be many per project). There is no formal artifact that decomposes a project into named initiatives, assigns index ranges, or declares cross-initiative dependencies. This slice:

- Adds the missing fan-out point between "one project" and "many architectures"
- Makes the process guide's meta nature explicit (unnumbered)
- Removes dead weight (unused spec guide, deprecated prompts)
- Aligns phase numbering with actual workflow semantics

## Technical Scope

### Included

- Process guide filename rename (drop 000 index)
- Concept guide filename rename and phase field update (Phase 1 → Phase 0)
- New initiative plan guide creation (Phase 1)
- New initiative plan docType and YAML schema (registered in file-naming-conventions.md per slice 110)
- Migration prompt for existing projects to generate an initiative plan from existing architecture documents
- Spec guide removal and `fileSpec` cleanup
- Process guide phases section rewrite
- Prompt updates: Phase 0 (concept), Phase 1 (initiative plan, new), Phase 2 (architecture)
- Deprecated prompt removal: Summarize Context, Task Breakdown Supplement
- Git rules update (`project-guides/rules/git.md`)
- All cross-file reference updates for renamed files

### Excluded

- YAML schema definitions (slice 110)
- cf tooling code changes (separate maintenance — log to 950-tasks if needed)
- Changes to phases 3-6 guides or prompts (unchanged)
- Retroactive updates to existing user/ documents in other projects

## Dependencies

### Prerequisites

- None. This slice can proceed independently of slice 110. New/updated guides should use correct YAML frontmatter; slice 110 will later formalize the canonical schema reference.

### Interfaces Required

- Slice 110 will register the `initiative-plan` docType schema in file-naming-conventions.md. This slice defines the schema inline; slice 110 canonicalizes it.

## Architecture

### File Renames

| Current | New | Reason |
|---------|-----|--------|
| `guide.ai-project.000-process.md` | `guide.ai-project.process.md` | Meta-guide, not a phase — should not occupy a phase index |
| `guide.ai-project.001-concept.md` | `guide.ai-project.000-concept.md` | Concept becomes Phase 0 |

### New Files

| File | Purpose |
|------|---------|
| `guide.ai-project.001-initiative-plan.md` | Phase 1 guide |

### Removed Files

| File | Reason |
|------|--------|
| `guide.ai-project.002-spec.md` | Legacy, unused — Phase 2 is architecture only |

### Phase Structure (Before → After)

**Before:**
```
Phase 0: (meta — process guide at 000)
Phase 1: Concept (guide at 001)
Phase 2: Architecture / Spec (guides at 002, prompt)
Phase 3-7: unchanged
```

**After:**
```
Meta:    Process guide (no phase number, no numeric index)
Phase 0: Concept (guide at 000)
Phase 1: Initiative Plan (guide at 001) — NEW
Phase 2: Architecture (guide at 002 index available, prompt only — no dedicated guide)
Phase 3-6: unchanged
Phase 7: unchanged (integration, run when needed)
```

### Initiative Plan Document Structure

Single living document per project at `user/project-guides/001-initiative-plan.{project}.md`.

```yaml
---
docType: initiative-plan
layer: project
project: {project}
source: user/project-guides/001-concept.{project}.md
dateCreated: YYYYMMDD
dateUpdated: YYYYMMDD
status: not_started
---
```

```markdown
# Initiative Plan: {Project}

## Source
001-concept.{project}.md

## Initiatives

1. [ ] **(nnn) {Initiative Name}** — {Scope description}. Dependencies: {list or "None (foundation)"}. Status: not_started
2. [ ] **(nnn) {Initiative Name}** — {Scope description}. Dependencies: [{nnn}]. Status: not_started

## Cross-Initiative Dependencies
- {nnn} depends on {nnn}: {reason}
- ...

## Notes
- Indices are tentative and may be reassigned as initiatives are added or reorganized.
- New initiatives discovered during development are added here with the next available base index.
- Check off initiatives as their architecture documents and slice plans are complete.
```

### Migration for Existing Projects

Existing projects updating their ai-project-guide will get the new guide files automatically (submodule/subtree update). The non-trivial step is creating an initiative plan from their existing architecture documents.

**Migration prompt** (add to `prompt.ai-project.system.md` alongside the Phase 1 prompt):

The migration prompt should:
1. Scan `user/architecture/` for existing `nnn-arch.*.md` files
2. Extract initiative names, index ranges, and dependencies from architecture doc frontmatter and content
3. Scan `user/architecture/` for `nnn-slices.*.md` to determine initiative status (has slice plan = at least in_progress)
4. Generate `user/project-guides/001-initiative-plan.{project}.md` with initiatives listed in checklist format
5. Populate cross-initiative dependencies from architecture document references
6. Present the generated plan to the PM for review before writing

This is an agent-assisted task — the PM and agent collaborate since the initiative plan is a strategic document. The prompt should be usable from the Phase 1 prompt section (tagged as a migration variant) or as a standalone supplemental prompt.

**Index gap convention**: Project-level decision, not global. Default gap of 20 (100, 120, 140) works for most projects. Projects with broad initiatives expected to expand significantly may use gaps of 100 or more. The choice is recorded in the initiative plan and can be adjusted via re-indexing.

### Concept Guide Changes

Update `Solution Approach` section guidance to nudge toward identifying **capability areas** — named pieces that the initiative plan will later formalize and sequence. The concept says "this project needs X, Y, and Z." The initiative plan says "X is 100-band, Y is 120-band, here's why that ordering."

Current text:
```
### Solution Approach
High-level description of the approach. Where does it run?
What makes it distinct? Are we building the whole thing or a
specific component/layer?
```

Updated text:
```
### Solution Approach
High-level description of the approach. Where does it run?
What makes it distinct? Are we building the whole thing or a
specific component/layer?

If the project involves multiple capability areas or components,
name them here. These are not yet initiatives with indices or
sequencing — just the identified pieces that Phase 1 (Initiative
Plan) will later formalize. Example: "This project needs a
behavior engine, a world server, an environment layer, and
clients."
```

### Process Guide Phase Numbering Update

The `Phases Detail` section in the process guide must be rewritten:

1. Renumber Phase 1 → Phase 0, remove "Phase 1:" prefix, add "Phase 0:"
2. Insert new Phase 1: Initiative Plan section
3. Update Phase 2 description — remove spec reference, remove the "Note on Specifications" paragraph
4. Update Phase Approval section — Phase 0-1 replace "Phases 1-3" strategic range reference
5. Update any internal cross-references to phase numbers

### Prompt Updates

**Concept prompt (Phase 0):**
- Update phase reference from "Phase 1" to "Phase 0"
- Reference `guide.ai-project.000-concept` (new filename)
- No structural changes to the prompt itself

**Initiative Plan prompt (Phase 1, new):**
- Create new prompt section in `prompt.ai-project.system.md`
- Role: Architect (working with PM)
- Inputs: concept document, existing architecture/ directory scan
- Output: `user/project-guides/001-initiative-plan.{project}.md`
- Guidance on index gap selection, cross-initiative dependency declaration
- Context profile entry: `initiative-plan-phase-1: [fileConcept]`

**Architecture prompt (Phase 2):**
- Remove any remaining spec references
- Update reference from `guide.ai-project.000-process` to `guide.ai-project.process`

**Deprecated prompts to remove:**
- Summarize Context (under Deprecated section)
- Task Breakdown Supplement (under Deprecated section)

### Reference Updates

63 occurrences of `guide.ai-project.000-process` across 24 files need updating to `guide.ai-project.process`. Key files:

- `file-naming-conventions.md` (1)
- `project-guides/readme.md` (5)
- `project-guides/prompt.ai-project.system.md` (13)
- All phase guide files (001-concept, 003, 004, 005, 005-variant, 090)
- `project-guides/rules/general.md` (1)
- `scripts/bootstrap.sh` (1)
- `scripts/template-stubs/prompt.legacy-migration.md` (4)
- Various user/ task and slice files (historical — update where practical)

13 files reference `guide.ai-project.002-spec` — these need the reference removed or replaced with the architecture guide/prompt reference.

### Git Rules Update

Add `review` commit type to `project-guides/rules/git.md`:
```
- `review` — Code review, design review, or audit documentation
```

Update any phase number references in rules if present.

## Success Criteria

### Functional Requirements
- [ ] Process guide renamed to `guide.ai-project.process.md` with no numeric index
- [ ] Concept guide renamed to `guide.ai-project.000-concept.md` with `phase: 0`
- [ ] Solution Approach section updated to mention capability area identification
- [ ] New `guide.ai-project.001-initiative-plan.md` exists with complete Phase 1 guidance
- [ ] Initiative plan document structure and YAML schema are defined
- [ ] Spec guide (`guide.ai-project.002-spec.md`) removed
- [ ] Process guide phases section reflects new numbering (0-7)
- [ ] Phase Approval section updated for new numbering
- [ ] All prompts updated (Phase 0, Phase 1 new, Phase 2 cleaned)
- [ ] Deprecated prompts removed (Summarize Context, Task Breakdown Supplement)
- [ ] Context profiles in prompt file updated for new phase names
- [ ] `review` commit type added to `project-guides/rules/git.md`
- [ ] All 63+ references to `guide.ai-project.000-process` updated
- [ ] All 13 references to `guide.ai-project.002-spec` removed or replaced
- [ ] Migration prompt exists for existing projects to generate initiative plans from architecture documents

### Technical Requirements
- [ ] No broken cross-references between guides
- [ ] All guide files have valid YAML frontmatter per canonical schemas (slice 110)
- [ ] `dependsOn` fields in all guides reference correct filenames post-rename

### Verification Walkthrough
1. `grep -r "guide.ai-project.000-process" project-guides/ file-naming-conventions.md scripts/` — should return zero matches
2. `grep -r "guide.ai-project.002-spec" project-guides/` — should return zero matches (user/ files may retain historical references)
3. Confirm `guide.ai-project.process.md` exists and has `phase: 0` removed / set to meta
4. Confirm `guide.ai-project.000-concept.md` exists with `phase: 0`
5. Confirm `guide.ai-project.001-initiative-plan.md` exists with `phase: 1`
6. Confirm `guide.ai-project.002-spec.md` does not exist
7. Read process guide — phases should list 0 through 7 with Initiative Plan at 1
8. Read prompt file — should have Phase 0 (concept), Phase 1 (initiative plan), Phase 2 (architecture) prompts; no deprecated section entries for Summarize Context or Task Breakdown Supplement
9. `grep "review" project-guides/rules/git.md` — should show the review commit type

## Implementation Notes

### Development Approach
Suggested order:
1. File renames (process guide, concept guide) — mechanical, high ripple
2. Reference updates for renames — sweep all files
3. Process guide content updates (phase numbering, remove spec note)
4. Concept guide content update (Solution Approach)
5. New initiative plan guide creation
6. Spec guide removal and reference cleanup
7. Prompt updates (concept, new initiative plan, architecture, deprecated removal)
8. Migration prompt for existing projects
9. Git rules update
10. Final reference sweep and verification

### Special Considerations
- The process guide rename has the widest blast radius (63 occurrences across 24 files). Do this first so subsequent edits work against the new filename.
- User/ files (tasks, slices) contain historical references. Update active/in-progress files; completed files can retain old references since they're historical artifacts.
- The `dependsOn` arrays in guide frontmatter are the most critical references to update — these are machine-parseable and used by tooling.
