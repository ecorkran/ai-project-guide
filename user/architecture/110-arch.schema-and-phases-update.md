---
docType: architecture
layer: project
project: ai-project-guide
archIndex: 110
component: schema-and-phases-update
relatedSlices: []
riskLevel: medium
dateCreated: 20260322
dateUpdated: 20260322
---

# Architecture: Schema and Phases Update

## Overview

This initiative addresses two related areas of the ai-project-guide system: **YAML schema standardization** across all document types and prompts, and **phase restructuring** to add an Initiatives phase and refactor the Concept phase.

Both areas share a common motivation: the guide system has grown organically, and its metadata definitions and early-phase workflows have drifted out of alignment. Fixing them together reduces the number of times we touch the same files.

### Scope

- Canonical YAML schema definitions for all document types
- Commit prefix standardization (adding `review:`)
- New `aiModel` common optional field
- Concept phase refactoring
- New Initiatives phase

### Motivation

YAML frontmatter is defined inconsistently across guides, prompts, and file-naming-conventions — some docTypes have schemas in multiple places that disagree, others have no formal schema at all. This causes AI agents to produce inconsistent or incomplete frontmatter. Separately, the project lifecycle would benefit from an explicit Initiatives phase and a tighter Concept phase.

## Design Goals

- **Single source of truth for YAML schemas** — one canonical location per docType, referenced (not duplicated) by prompts and guides
- **Consistent metadata across all document types** — standardized required and optional fields
- **Cleaner early-phase workflow** — Concept phase focused on concept, Initiatives phase bridging concept to architecture
- **Minimal disruption** — changes should be backward-compatible with existing project documents where possible

## Architectural Principles

- **Canonical + reference**: Define schemas in one place (file-naming-conventions.md), reference from prompts. Prompts may include inline YAML examples but must cite the canonical source.
- **Required minimum over optional sprawl**: Promote fields that are effectively always used (status, project) to required. Keep optional fields genuinely optional.
- **Phase clarity**: Each phase should have a single clear purpose. If a phase is doing two things, it should be split.

## Current State

### YAML Schema Issues

- `file-naming-conventions.md` defines minimum required fields (docType, dateCreated, dateUpdated) and lists common optional fields (layer, audience, description, dependsOn, status)
- `project` appears on nearly every docType but is not listed as required or common optional
- `status` is included on most docTypes in practice but listed as optional
- Per-docType schemas are scattered across guide files and prompt templates, with varying levels of completeness:
  - **concept**: richest schema (8 fields), only docType using layer/audience/phase/phaseName/guideRole
  - **architecture**: schema exists only in the prompt, not in a guide
  - **slice-plan**: guide and prompt match (5 fields)
  - **slice-design**: guide and prompt match (8 fields)
  - **tasks**: schema in guide omits docType; has unique fields (lld, projectState)
  - **review**: severely underspecified (only layer + docType in the guide)
  - **analysis**: no formal YAML schema anywhere
- Commit type prefixes are convention-by-example only, defined in `project-guides/rules/git.md` (CLAUDE.md is auto-generated from rules) but not in the process guides

### Phase Structure Issues

- No explicit Initiative Plan phase — the fan-out from "one project" to "many architectures" is informal
- Concept phase's "Solution Approach" section is vague ("high-level description of the approach") and doesn't clearly bridge to architecture
- Process guide occupies the 000 index, creating a collision if concept becomes Phase 0
- Spec guide (`guide.ai-project.002-spec.md`) is legacy — phase 2 is always architecture now, spec is unused
- `fileSpec` field exists in cf tooling but is never used

## Envisioned State

### YAML

- `file-naming-conventions.md` contains a **canonical schema section** with:
  - Universal required fields: `docType`, `project`, `dateCreated`, `dateUpdated`, `status`
  - Common optional fields: `layer`, `audience`, `description`, `dependsOn`, `aiModel`
  - Per-docType schema blocks for: concept, architecture, slice-plan, slice-design, tasks, review, analysis
- Prompts include inline YAML examples for the docType being created, with a reference to the canonical source
- Guides reference the canonical schema rather than defining their own
- `review:` added as a semantic commit type
- `aiModel` available as a common optional field, required for review documents

### Phases

- Process guide becomes unnumbered meta-document: `guide.ai-project.process.md`
- Phase 0: Concept — `guide.ai-project.000-concept.md`, "Solution Approach" sharpened to identify capability areas (named pieces, not yet indexed)
- Phase 1: Initiative Plan — new `guide.ai-project.001-initiative-plan.md`, single living document per project (`user/project-guides/001-initiative-plan.{project}.md`), formalizes initiatives with base indices, sequencing, and cross-initiative dependencies. Index gap is a project-level decision (default 20-based; broad initiatives may use wider gaps).
- Phase 2: Architecture — unchanged in number, but spec guide removed and `fileSpec` dropped
- Phases 3-6: Unchanged
- Deprecated prompts (Summarize Context, Task Breakdown Supplement) removed

## Technical Considerations

- **Migration of existing documents**: Existing project documents with older/inconsistent frontmatter should remain valid. Schema standardization applies to new document creation and future updates, not retroactive enforcement.
- **Prompt self-containedness vs DRY**: Prompts need to be usable without reading external files, but duplicated schemas drift. The compromise is inline examples that cite the canonical source.
- **aiModel field values**: Need to decide on a convention for values (e.g., `claude-opus-4-6`, `claude-sonnet-4-5`, or shorter forms like `opus-4.6`).
- **Commit prefix documentation location**: Commit types are defined in `project-guides/rules/git.md` (source of truth; CLAUDE.md is auto-generated). The question is whether process guides should also list them or just reference the rules file.
- **Process guide rename**: Removing the 000 index from the process guide is a filename change that will break any hardcoded references (dependsOn fields, prompt text, rules files, auto-generated CLAUDE.md). These need to be found and updated.
- **Spec removal**: `guide.ai-project.002-spec.md` and `fileSpec` in cf tooling should be removed. Existing projects that referenced spec can ignore it — no migration needed since it was unused.
- **Index gap flexibility**: Initiative plan indices are a project-level decision rather than a global convention. The guide recommends a default gap of 20 but explicitly supports wider gaps for broad initiatives. This means file-naming-conventions.md needs to describe the convention as a default, not a rule.
- **Deprecated prompt cleanup**: Summarize Context and Task Breakdown Supplement prompts will be removed from prompt.ai-project.system.md during this initiative.

## Anticipated Slices

- **(110) YAML Schema Standardization** — Canonical schema section in file-naming-conventions.md, align all guides and prompts, add `review:` commit type, add `aiModel` field
- **(111) Phase Renumbering and Initiative Plan** — Process guide rename, concept → Phase 0, new Initiative Plan phase, spec removal, prompt updates, deprecated prompt cleanup
- **(112) Cross-Reference Verification** — Integration check

## Related Work

- [file-naming-conventions.md](../../file-naming-conventions.md) — current YAML frontmatter definitions
- [prompt.ai-project.system.md](../../project-guides/prompt.ai-project.system.md) — prompt templates containing inline YAML schemas
- [guide.ai-project.090-code-review.md](../../project-guides/guide.ai-project.090-code-review.md) — underspecified review YAML
- Existing slices 100/105 in the 100-band (completed, unrelated)
