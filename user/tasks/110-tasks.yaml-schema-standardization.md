---
docType: tasks
slice: yaml-schema-standardization
project: ai-project-guide
lld: user/slices/110-slice.yaml-schema-standardization.md
dependencies: [111-phase-renumbering-and-initiative-plan]
projectState: Slices 111 and 112 complete (v0.14.1). Guides use new filenames. Schemas are inconsistent across guides and prompts.
dateCreated: 20260324
dateUpdated: 20260324
status: not_started
---

## Context Summary
- Working on yaml-schema-standardization slice (110)
- Creating canonical per-docType YAML schemas in file-naming-conventions.md
- Aligning all guide and prompt YAML examples to canonical source
- Next planned slice: 113 (Cross-Reference Verification)

---

### Task 1: Create Canonical Schema Section in file-naming-conventions.md
**Objective**: Replace the current minimal "YAML Frontmatter Requirement" section with a comprehensive canonical schema reference including per-docType blocks.

- [ ] Replace the current "Minimum required frontmatter" block (lines 16-23) with updated universal required fields:
  ```yaml
  docType: <type>
  project: <project-name>
  dateCreated: YYYYMMDD
  dateUpdated: YYYYMMDD
  status: not_started | in_progress | complete | deprecated
  ```
- [ ] Update the docType enum to include all current types: `[guide|reference|concept|initiative-plan|architecture|slice-plan|slice-design|slice|tasks|analysis|review|notes|template|intro-guide|migration]`
- [ ] Update "Common optional fields" to include `aiModel`:
  - [ ] `layer`: process, project, tool-guide, framework-guide, domain-guide
  - [ ] `audience`: [human, ai] or subset
  - [ ] `description`: Brief purpose description
  - [ ] `dependsOn`: Related documents
  - [ ] `aiModel`: AI model that generated the document (required for reviews)
- [ ] Add a "Valid Status Values" subsection:
  - `not_started` — work has not begun
  - `in_progress` — actively being worked on
  - `complete` — all work finished
  - `deprecated` — no longer relevant
  - Note: `completed` is recognized as an alias for `complete` in existing documents
- [ ] Add per-docType schema blocks after the common fields section. For each docType, show the canonical YAML including universal required fields plus type-specific fields:
  - [ ] **concept**: docType, layer, phase, phaseName, project, audience, description, dependsOn, dateCreated, dateUpdated, status
  - [ ] **initiative-plan**: docType, layer, project, source, dateCreated, dateUpdated, status
  - [ ] **architecture**: docType, layer, project, archIndex, component, relatedSlices, riskLevel, dateCreated, dateUpdated, status
  - [ ] **slice-plan**: docType, parent, project, dateCreated, dateUpdated, status
  - [ ] **slice-design**: docType, slice, project, parent, dependencies, interfaces, dateCreated, dateUpdated, status
  - [ ] **tasks**: docType, slice, project, lld, dependencies, projectState, dateCreated, dateUpdated, status
  - [ ] **review**: docType, layer, project, reviewType, sourceDocument, aiModel, dateCreated, dateUpdated, status
  - [ ] **analysis**: docType, project, topic, dateCreated, dateUpdated, status
- [ ] Success criteria:
  - [ ] Canonical schema section exists with all 8 per-docType blocks
  - [ ] Universal required fields are docType, project, dateCreated, dateUpdated, status
  - [ ] aiModel listed as common optional, noted as required for reviews
  - [ ] Valid status values formalized

**Commit**: `guides: add canonical per-docType YAML schemas to file-naming-conventions`

---

### Task 2: Align Guide YAML Examples to Canonical Schemas
**Objective**: Update each guide's YAML template example to match its canonical schema from file-naming-conventions.md.

- [ ] **guide.ai-project.000-concept.md** — add `docType: concept` and `project: {project}` to the document template YAML block (currently missing both)
- [ ] **guide.ai-project.001-initiative-plan.md** — verify match (should already be correct from slice 111)
- [ ] **guide.ai-project.003-slice-planning.md** — add `project` field if missing from YAML template
- [ ] **guide.ai-project.004-slice-design.md** — verify match (should already be correct)
- [ ] **guide.ai-project.005-task-breakdown.md** — add `docType: tasks` to YAML template (currently missing)
- [ ] **guide.ai-project.090-code-review.md** — expand YAML template from just `layer` + `docType` to full review schema: add `project`, `reviewType`, `sourceDocument`, `aiModel`, `dateCreated`, `dateUpdated`, `status`
- [ ] Add a reference note to each guide near its YAML template: "See `file-naming-conventions.md` for the canonical YAML schema reference."
- [ ] Success criteria:
  - [ ] Each guide's YAML template matches its canonical schema
  - [ ] All guides include a reference to the canonical source
  - [ ] No guide introduces fields absent from its canonical schema

**Commit**: `guides: align guide YAML examples to canonical schemas`

---

### Task 3: Align Prompt YAML Examples to Canonical Schemas
**Objective**: Update inline YAML examples in `prompt.ai-project.system.md` to match canonical schemas.

- [ ] **Architecture prompt** (Phase 2) — verify YAML block matches architecture canonical schema. Current fields: docType, layer, project, archIndex, component, relatedSlices, riskLevel, dateCreated, dateUpdated. Add `status` if missing.
- [ ] **Slice Planning prompt** (Phase 3) — verify match. Fix `status: active` reference in prompt text to use `status: not_started`.
- [ ] **Slice Design prompt** (Phase 4) — verify match (should be correct)
- [ ] **Task Breakdown prompt** (Phase 5) — the prompt doesn't repeat the YAML (it references the guide). Verify the reference is accurate.
- [ ] Success criteria:
  - [ ] All prompt YAML blocks match their canonical schemas
  - [ ] No `status: active` in prompts (use valid values)

**Commit**: `guides: align prompt YAML examples to canonical schemas`

---

### Task 4: Status Value Cleanup
**Objective**: Ensure `status: active` and `status: completed` are not used in guide or prompt files.

- [ ] Search for `status: active` in project-guides/ and file-naming-conventions.md
  - [ ] Replace with appropriate valid value (`in_progress` or `not_started`)
- [ ] Search for `status: completed` in project-guides/ and file-naming-conventions.md
  - [ ] Replace with `complete`
- [ ] Success criteria:
  - [ ] Zero occurrences of `status: active` in guides and prompts
  - [ ] Zero occurrences of `status: completed` in guides and prompts (user/ files may retain historical values)

**Commit**: `guides: standardize status values across guides and prompts`

---

### Task 5: Update Slice Plan Entry and Verification
**Objective**: Link the slice design in the slice plan and run final verification.

- [ ] Update slice plan entry for (110) to include link to slice design
- [ ] Verify canonical schema section in file-naming-conventions.md has all 8 docType blocks
- [ ] For each guide, compare its YAML template to canonical — fields should match
- [ ] For each prompt YAML block, compare to canonical — fields should match
- [ ] `grep -r "status: active" project-guides/` — should return zero
- [ ] `grep -r "status: completed" project-guides/` — should return zero
- [ ] Success criteria:
  - [ ] All checks pass

**Commit**: `docs: verify YAML schema standardization complete`
