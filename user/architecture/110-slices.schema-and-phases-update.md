---
docType: slice-plan
parent: user/architecture/110-arch.schema-and-phases-update.md
project: ai-project-guide
dateCreated: 20260322
dateUpdated: 20260324
status: not_started
---

# Slice Plan: Schema and Phases Update

## Parent

[110-arch.schema-and-phases-update.md](110-arch.schema-and-phases-update.md)

## Overview

This initiative standardizes YAML frontmatter schemas across all document types, aligns prompts and guides to a single canonical source, restructures the early project phases (Concept → Phase 0, new Initiative Plan → Phase 1), removes the legacy spec phase, and cleans up deprecated prompts.

Four feature slices plus integration verification.

## Foundation Work

None — this initiative modifies existing guide and reference documents. No new infrastructure is required.

## Feature Slices

1. [x] **(111) Phase Renumbering and Initiative Plan** — [111-slice.phase-renumbering-and-initiative-plan.md](../slices/111-slice.phase-renumbering-and-initiative-plan.md). Restructure the phase numbering and add the Initiative Plan phase. Scope:
   - **Process guide rename**: `guide.ai-project.000-process.md` → `guide.ai-project.process.md` (meta, no phase number — it describes the methodology, not a step within it)
   - **Concept → Phase 0**: Rename guide to `guide.ai-project.000-concept.md`, update phase field. Sharpen "Solution Approach" section to identify capability areas (named pieces that the initiative plan will later formalize and sequence). No other concept guide changes.
   - **Initiative Plan → Phase 1**: Create `guide.ai-project.001-initiative-plan.md`. Single living document per project at `user/project-guides/001-initiative-plan.{project}.md`. Bridges concept to architecture by formalizing initiatives with base indices, sequencing, and cross-initiative dependencies. Index gap is a project-level decision (default gap of 20; broad initiatives may use 100+; recorded in the plan, adjustable via re-indexing).
   - **Architecture remains Phase 2**: No phase number change. Remove `fileSpec` — spec is a legacy concept no longer used. Evaluate whether Phase 2 needs a dedicated guide or if the prompt is sufficient.
   - **Phases 3-6 unchanged**: No renumbering.
   - **Prompt updates**: Update Phase 0 (concept) and Phase 2 (architecture) prompts. Create Phase 1 (initiative plan) prompt. Remove deprecated prompts (Summarize Context, Task Breakdown Supplement).
   - **Migration**: Prompt for existing projects to generate initiative plans from existing architecture documents.
   - **Git rules**: Update commit type list and any phase references in `project-guides/rules/git.md` (CLAUDE.md is generated from this by a setup script).

   Dependencies: none. Risk: Medium (touches process guide, multiple guide files, prompts, rules, and cf tooling). Effort: 4/5

2. [ ] **(112) Analysis Skill Extraction** — [112-slice.analysis-skill-extraction.md](../slices/112-slice.analysis-skill-extraction.md). Extract the five analysis prompts from `prompt.ai-project.system.md` into a single combined `/analyze` skill at `project-guides/skills/analyze/SKILL.md`. Update `setup-ide` to copy skills to `.claude/skills/` during IDE setup. Retain analysis context profiles in the prompt file (lightweight, needed by cf). Dependencies: [111]. Risk: Low. Effort: 2/5

3. [ ] **(110) YAML Schema Standardization** — Create canonical per-docType schema definitions in file-naming-conventions.md (including new `initiative-plan` docType from slice 111), align all guide and prompt YAML examples to reference the canonical source, add `aiModel` common optional field, promote `project` and `status` to universal required fields, formalize valid status values. Dependencies: [111] (phase renumbering should land first to avoid editing renamed files twice). Risk: Medium (wide surface area across many files). Effort: 3/5

## Integration Work

4. [ ] **(113) Cross-Reference Verification** — Verify all guides, prompts, and file-naming-conventions are internally consistent after slices 110-113. Run cf check. Confirm existing project documents remain valid under updated schemas. Verify phase numbering is consistent across all references. Dependencies: [110, 111, 113]. Effort: 1/5
