---
docType: tasks
slice: yaml-schema-standardization
project: ai-project-guide
lld: user/slices/110-slice.yaml-schema-standardization.md
dependencies: [111-phase-renumbering-and-initiative-plan]
projectState: Slices 111 and 112 complete (v0.14.1). Guides use new filenames. Schemas are inconsistent across guides and prompts.
dateCreated: 20260324
dateUpdated: 20260324
status: complete
---

## Context Summary
- Working on yaml-schema-standardization slice (110)
- Creating canonical per-docType YAML schemas in file-naming-conventions.md
- Aligning all guide and prompt YAML examples to canonical source
- Next planned slice: 113 (Cross-Reference Verification)

---

### Task 1: Create Canonical Schema Section in file-naming-conventions.md
**Objective**: Replace the current minimal "YAML Frontmatter Requirement" section with a comprehensive canonical schema reference including per-docType blocks.

- [x] Replace the current "Minimum required frontmatter" block (lines 16-23) with updated universal required fields:
  ```yaml
  docType: <type>
  project: <project-name>
  dateCreated: YYYYMMDD
  dateUpdated: YYYYMMDD
  status: not_started | in_progress | complete | deferred | deprecated
  ```
- [x] Update the docType enum to include all current types: `[guide|reference|concept|initiative-plan|architecture|slice-plan|slice-design|slice|tasks|analysis|review|notes|template|intro-guide|migration]`
- [x] Update "Common optional fields" to include `aiModel`:
  - [x] `layer`: process, project, tool-guide, framework-guide, domain-guide
  - [x] `audience`: [human, ai] or subset
  - [x] `description`: Brief purpose description
  - [x] `dependsOn`: Related documents
  - [x] `aiModel`: AI model that generated the document (required for reviews)
- [x] Add a "Valid Status Values" subsection:
  - `not_started` — work has not begun
  - `in_progress` — actively being worked on
  - `complete` — all work finished
  - `deferred` — postponed, may be revisited
  - `deprecated` — no longer relevant
  - Note: `completed` is recognized as an alias for `complete` in existing documents
- [x] Add per-docType schema blocks after the common fields section. For each docType, show the canonical YAML including universal required fields plus type-specific fields:
  - [x] **concept**: docType, layer, phase, phaseName, project, audience, description, dependsOn, dateCreated, dateUpdated, status
  - [x] **initiative-plan**: docType, layer, project, source, dateCreated, dateUpdated, status
  - [x] **architecture**: docType, layer, project, archIndex, component, relatedSlices, riskLevel, dateCreated, dateUpdated, status
  - [x] **slice-plan**: docType, parent, project, dateCreated, dateUpdated, status
  - [x] **slice-design**: docType, slice, project, parent, dependencies, interfaces, dateCreated, dateUpdated, status
  - [x] **tasks**: docType, slice, project, lld, dependencies, projectState, dateCreated, dateUpdated, status
  - [x] **review**: docType, layer, project, reviewType, sourceDocument, aiModel, dateCreated, dateUpdated, status
  - [x] **analysis**: docType, project, topic, dateCreated, dateUpdated, status
- [x] Success criteria:
  - [x] Canonical schema section exists with all 8 per-docType blocks
  - [x] Universal required fields are docType, project, dateCreated, dateUpdated, status
  - [x] aiModel listed as common optional, noted as required for reviews
  - [x] Valid status values formalized

**Commit**: `guides: add canonical per-docType YAML schemas to file-naming-conventions`

---

### Task 2: Clean Up file-naming-conventions.md Sections
**Objective**: Update Document Naming, Document Types, Legacy Task Patterns, and File Size sections to reflect current conventions.

- [x] **Document Naming examples** — replace the current examples with realistic indexed examples:
  - Replace `review.chartcanvas.0419.md`, `tasks.code-review.chartcanvas.0419.md`, `guide.development.react.md`
  - Use examples like: `120-arch.data-pipeline.md`, `120-slices.data-pipeline.md`, `121-slice.ingestion-service.md`, `121-tasks.ingestion-service.md`, `121-review.tasks.ingestion-service.md`
- [x] **Document Types** — update the common prefixes list:
  - [x] Remove `spec` (legacy, no longer used)
  - [x] Add or verify: `arch`, `slice`, `slices` (slice plan), `analysis`, `initiative-plan`
  - [x] Update examples to use realistic initiative/arch/plan/slice/tasks/review patterns
- [x] **Remove Legacy Task File Patterns** — delete the entire "Legacy Task File Patterns" subsection (lines 212-217). These patterns are long obsolete.
- [x] **File Size Limits** — update target from ~350 to ~450 lines:
  - [x] "Non-architecture files": Target ~450 lines
  - [x] Splitting trigger: >33% over (~600 lines for non-architecture files)
  - [x] Update the example to use ~600 instead of ~465
- [x] Success criteria:
  - [x] Document Naming examples use realistic indexed filenames
  - [x] No `spec` in Document Types
  - [x] No Legacy Task File Patterns section
  - [x] File size target is ~450

**Commit**: `guides: clean up file-naming-conventions document naming and size limits`

---

### Task 3: Align Guide YAML Examples to Canonical Schemas
**Objective**: Update each guide's YAML template example to match its canonical schema from file-naming-conventions.md.

- [x] **guide.ai-project.000-concept.md** — add `docType: concept` and `project: {project}` to the document template YAML block (currently missing both)
- [x] **guide.ai-project.001-initiative-plan.md** — verify match (should already be correct from slice 111)
- [x] **guide.ai-project.003-slice-planning.md** — add `project` field if missing from YAML template
- [x] **guide.ai-project.004-slice-design.md** — verify match (should already be correct)
- [x] **guide.ai-project.005-task-breakdown.md** — add `docType: tasks` to YAML template (currently missing)
- [x] **guide.ai-project.090-code-review.md** — expand YAML template from just `layer` + `docType` to full review schema: add `project`, `reviewType`, `sourceDocument`, `aiModel`, `dateCreated`, `dateUpdated`, `status`
- [x] Add a reference note to each guide near its YAML template: "See `file-naming-conventions.md` for the canonical YAML schema reference."
- [x] Success criteria:
  - [x] Each guide's YAML template matches its canonical schema
  - [x] All guides include a reference to the canonical source
  - [x] No guide introduces fields absent from its canonical schema

**Commit**: `guides: align guide YAML examples to canonical schemas`

---

### Task 4: Align Prompt YAML Examples to Canonical Schemas
**Objective**: Update inline YAML examples in `prompt.ai-project.system.md` to match canonical schemas.

- [x] **Architecture prompt** (Phase 2) — verify YAML block matches architecture canonical schema. Current fields: docType, layer, project, archIndex, component, relatedSlices, riskLevel, dateCreated, dateUpdated. Add `status` if missing.
- [x] **Slice Planning prompt** (Phase 3) — verify match. Fix `status: active` reference in prompt text to use `status: not_started`.
- [x] **Slice Design prompt** (Phase 4) — verify match (should be correct)
- [x] **Task Breakdown prompt** (Phase 5) — the prompt doesn't repeat the YAML (it references the guide). Verify the reference is accurate.
- [x] Success criteria:
  - [x] All prompt YAML blocks match their canonical schemas
  - [x] No `status: active` in prompts (use valid values)

**Commit**: `guides: align prompt YAML examples to canonical schemas`

---

### Task 5: Status Value Cleanup
**Objective**: Ensure `status: active` and `status: completed` are not used in guide or prompt files.

- [x] Search for `status: active` in project-guides/ and file-naming-conventions.md
  - [x] Replace with appropriate valid value (`in_progress` or `not_started`)
- [x] Search for `status: completed` in project-guides/ and file-naming-conventions.md
  - [x] Replace with `complete`
- [x] Success criteria:
  - [x] Zero occurrences of `status: active` in guides and prompts
  - [x] Zero occurrences of `status: completed` in guides and prompts (user/ files may retain historical values)

**Commit**: `guides: standardize status values across guides and prompts`

---

### Task 6: Update Slice Plan Entry and Verification
**Objective**: Link the slice design in the slice plan and run final verification.

- [x] Update slice plan entry for (110) to include link to slice design
- [x] Verify canonical schema section in file-naming-conventions.md has all 8 docType blocks
- [x] For each guide, compare its YAML template to canonical — fields should match
- [x] For each prompt YAML block, compare to canonical — fields should match
- [x] `grep -r "status: active" project-guides/` — should return zero
- [x] `grep -r "status: completed" project-guides/` — should return zero
- [x] Success criteria:
  - [x] All checks pass

**Commit**: `docs: verify YAML schema standardization complete`
