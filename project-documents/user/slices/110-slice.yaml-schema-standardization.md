---
docType: slice-design
slice: yaml-schema-standardization
project: ai-project-guide
parent: user/architecture/110-slices.schema-and-phases-update.md
dependencies: [111-phase-renumbering-and-initiative-plan]
interfaces: [113-cross-reference-verification]
dateCreated: 20260324
dateUpdated: 20260324
status: complete
---

# Slice Design: YAML Schema Standardization

## Overview

Create a canonical YAML schema reference in `file-naming-conventions.md` with per-docType schemas, standardize required and optional fields across all document types, align all guide and prompt YAML examples to the canonical source, and add the `aiModel` common optional field.

## Value

YAML frontmatter is defined inconsistently — some docTypes have schemas in multiple places that disagree, others have no formal schema at all, and fields that are effectively always present (like `project` and `status`) are listed as optional. This causes AI agents to produce inconsistent or incomplete frontmatter. A single canonical reference eliminates ambiguity.

## Technical Scope

### Included

- Canonical YAML schema section in `file-naming-conventions.md` with per-docType blocks
- Updated universal required fields: `docType`, `project`, `dateCreated`, `dateUpdated`, `status`
- Formalized valid status values: `not_started`, `in_progress`, `complete`, `deferred`, `deprecated`
- New common optional field: `aiModel`
- Add missing `docType` to concept and tasks template schemas
- Add missing `project` to concept template schema
- Flesh out severely underspecified review schema
- Add analysis schema (currently missing entirely)
- Align all guide YAML examples to reference or match the canonical source
- Align all prompt YAML examples similarly
- Add `initiative-plan` docType to the canonical list

### Excluded

- Retroactive updates to existing user/ documents in other projects
- Changes to cf tooling (separate project)
- Content changes to guides beyond YAML schema alignment

## Architecture

### Canonical Schema Location

Expand the existing "YAML Frontmatter Requirement" section in `file-naming-conventions.md` with per-docType schema blocks. The current section (lines 12-30) defines minimum required and common optional fields — this gets replaced with a more complete reference.

### Universal Required Fields (all docTypes)

```yaml
docType: <type>
project: <project-name>
dateCreated: YYYYMMDD
dateUpdated: YYYYMMDD
status: not_started | in_progress | complete | deferred | deprecated
```

Current state promotes `docType`, `dateCreated`, `dateUpdated` as required. This adds `project` and `status`.

### Common Optional Fields

```yaml
layer: process | project | tool-guide | framework-guide | domain-guide
audience: [human, ai]
description: Brief purpose description
dependsOn: [related-documents]
aiModel: <model-identifier>    # NEW — required for reviews, optional elsewhere
```

### Per-DocType Schemas

Each docType gets a canonical schema block listing its required + type-specific fields. These are the source of truth — guides and prompts reference them.

**concept** — add missing `docType`, `project`; keep concept-specific fields (phase, phaseName, guideRole, audience)

**initiative-plan** — already well-defined from slice 111

**architecture** — currently only in prompt; formalize with `archIndex`, `component`, `relatedSlices`, `riskLevel`

**slice-plan** — add `project` (currently missing from guide schema); keep `parent`

**slice-design** — already well-defined; keep `slice`, `parent`, `dependencies`, `interfaces`

**tasks** — add missing `docType`; keep `slice`, `lld`, `dependencies`, `projectState`

**review** — currently only `layer` + `docType`; expand to include `project`, `reviewType`, `sourceDocument`, `dateCreated`, `dateUpdated`, `status`, `aiModel` (required for reviews)

**analysis** — new schema; include `project`, `topic`, `sourceDocument` (optional), `priority` (optional)

### Guide and Prompt Alignment

Each guide's YAML example should:
1. Match the canonical schema exactly (same fields, same order)
2. Include a note: "See `file-naming-conventions.md` for the canonical YAML schema reference"

Each prompt's inline YAML example should:
1. Match the canonical schema for that docType
2. Not introduce fields absent from the canonical schema

This is alignment, not duplication — guides and prompts keep their inline examples for self-containedness, but they must agree with the canonical source.

### Status Value Standardization

Current state: `status` values vary (`active`, `completed`, `not_started`, `in_progress`, `complete`, `deferred`, `deprecated`). Standardize to:
- `not_started` — work has not begun
- `in_progress` — actively being worked on
- `complete` — all work finished
- `deprecated` — no longer relevant

Note: `completed` (with -ed) should be listed as a recognized alias for `complete` to avoid breaking existing documents, but new documents should use `complete`.

## Success Criteria

### Functional Requirements
- [ ] `file-naming-conventions.md` contains a canonical schema section with per-docType blocks for: concept, initiative-plan, architecture, slice-plan, slice-design, tasks, review, analysis
- [ ] Universal required fields are `docType`, `project`, `dateCreated`, `dateUpdated`, `status`
- [ ] Valid status values are formalized: `not_started`, `in_progress`, `complete`, `deferred`, `deprecated`
- [ ] `aiModel` is listed as a common optional field, required for review docType
- [ ] `initiative-plan` is in the docType list
- [ ] All guide YAML examples match their canonical schema
- [ ] All prompt YAML examples match their canonical schema
- [ ] Concept template includes `docType` and `project`
- [ ] Tasks template includes `docType`
- [ ] Review schema expanded beyond just `layer` + `docType`
- [ ] Analysis schema exists

### Verification Walkthrough
1. Read `file-naming-conventions.md` — canonical schema section exists with all 8 docType blocks
2. For each guide (000-concept, 001-initiative-plan, 003, 004, 005, 090): compare its YAML example to the canonical schema — fields should match
3. For each prompt YAML block: compare to canonical schema — fields should match
4. Grep for `status: active` or `status: completed` in guides/prompts — should be zero (except historical user/ docs)
