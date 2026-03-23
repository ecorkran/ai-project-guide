---
slice: phase-renumbering-and-initiative-plan
project: ai-project-guide
lld: user/slices/111-slice.phase-renumbering-and-initiative-plan.md
dependencies: []
projectState: Planning artifacts (arch, slice plan, slice design) complete. No implementation started.
dateCreated: 20260322
dateUpdated: 20260322
status: not_started
---

## Context Summary
- Working on phase-renumbering-and-initiative-plan slice (111)
- This slice restructures the project phase numbering, adds an Initiative Plan phase, removes the legacy spec guide, and updates all references
- No prerequisites — this slice proceeds independently
- Delivers: Phase 0 (Concept), Phase 1 (Initiative Plan), cleaned Phase 2 (Architecture), updated prompts and references
- Next planned slice: 110 (YAML Schema Standardization)

---

### Task 1: Rename Process Guide (drop 000 index)
**Objective**: Rename `guide.ai-project.000-process.md` → `guide.ai-project.process.md` and update its frontmatter to reflect meta (non-phase) status.

- [ ] `git mv project-guides/guide.ai-project.000-process.md project-guides/guide.ai-project.process.md`
- [ ] Update frontmatter: change `phase: 0` and `phaseName: meta` to remove phase number. Set `phase: meta` or remove the `phase` field entirely — the process guide is not a phase.
  - Keep `layer: process` and all other frontmatter fields
- [ ] Success criteria:
  - [ ] File exists at `project-guides/guide.ai-project.process.md`
  - [ ] No file at `project-guides/guide.ai-project.000-process.md`
  - [ ] Frontmatter reflects meta status (no numeric phase)

**Commit**: `guides: rename process guide to drop 000 index`

---

### Task 2: Update All References to Process Guide Filename
**Objective**: Replace all occurrences of `guide.ai-project.000-process` with `guide.ai-project.process` across the codebase.

- [ ] Update references in **project-guides/** (highest priority — these are machine-parsed):
  - [ ] `guide.ai-project.001-concept.md` — `dependsOn` field and body text (2 occurrences)
  - [ ] `guide.ai-project.003-slice-planning.md` — `dependsOn` and body (2)
  - [ ] `guide.ai-project.004-slice-design.md` — `dependsOn` and body (2)
  - [ ] `guide.ai-project.005-task-breakdown.md` — `dependsOn` and body (4)
  - [ ] `guide.ai-project.005-variant-task-expansion.md` — body (3)
  - [ ] `guide.ai-project.090-code-review.md` — body (1)
  - [ ] `prompt.ai-project.system.md` — body references (13)
  - [ ] `project-guides/readme.md` (5)
- [ ] Update references in **root-level files**:
  - [ ] `file-naming-conventions.md` (1)
  - [ ] `readme.md` (1)
- [ ] Update references in **scripts/**:
  - [ ] `scripts/bootstrap.sh` (1)
  - [ ] `scripts/template-stubs/prompt.legacy-migration.md` (4)
- [ ] Update references in **rules/**:
  - [ ] `project-guides/rules/general.md` (1)
- [ ] Update references in **active user/ files** (skip completed/historical slices):
  - [ ] `user/architecture/110-slices.schema-and-phases-update.md` (1)
  - [ ] `user/tasks/950-tasks.maintenance.md` — if it references the process guide
- [ ] Run verification: `grep -r "guide.ai-project.000-process" project-guides/ file-naming-conventions.md scripts/ readme.md` — should return zero matches
- [ ] Success criteria:
  - [ ] Zero occurrences of `guide.ai-project.000-process` in project-guides/, file-naming-conventions.md, scripts/, readme.md, and rules/
  - [ ] All `dependsOn` arrays reference the new filename
  - [ ] User/ files with active status are updated; completed files may retain old references

**Commit**: `guides: update all references from 000-process to process`

---

### Task 3: Rename Concept Guide (001 → 000) and Update to Phase 0
**Objective**: Rename `guide.ai-project.001-concept.md` → `guide.ai-project.000-concept.md`, update phase from 1 to 0, and update the Solution Approach section.

- [ ] `git mv project-guides/guide.ai-project.001-concept.md project-guides/guide.ai-project.000-concept.md`
- [ ] Update frontmatter:
  - [ ] `phase: 1` → `phase: 0`
  - [ ] `description:` update to reference "Phase 0"
  - [ ] `dependsOn: [guide.ai-project.process.md]` (use new process guide name from Task 1)
- [ ] Update body text: change any references to "Phase 1" → "Phase 0" and "Phase 2" → keep as "Phase 2" (architecture didn't move)
- [ ] Update the document template's YAML example: `phase: 1` → `phase: 0`
- [ ] Update Solution Approach section in the document template. Add capability area guidance after existing text (see slice design for exact wording):
  ```
  If the project involves multiple capability areas or components,
  name them here. These are not yet initiatives with indices or
  sequencing — just the identified pieces that Phase 1 (Initiative
  Plan) will later formalize.
  ```
- [ ] Update references to `guide.ai-project.001-concept` across the codebase to `guide.ai-project.000-concept`:
  - [ ] `guide.ai-project.002-spec.md` — `dependsOn` (will be removed in Task 6, but update if still present)
  - [ ] `prompt.ai-project.system.md` — any concept guide references
  - [ ] `project-guides/readme.md` — guide listing
  - [ ] Process guide (`guide.ai-project.process.md`) — guide listing section
- [ ] Success criteria:
  - [ ] File exists at `project-guides/guide.ai-project.000-concept.md` with `phase: 0`
  - [ ] Solution Approach section includes capability area guidance
  - [ ] No references to `guide.ai-project.001-concept` in project-guides/

**Commit**: `guides: rename concept guide to 000, update to Phase 0`

---

### Task 4: Update Process Guide Phases Section
**Objective**: Rewrite the Phases Detail section of the process guide to reflect the new phase numbering (0-7) and include the Initiative Plan phase.

- [ ] Update **Phase Approval** section:
  - [ ] Change "Phases 1–3 (strategic decisions)" → "Phases 0–2 (strategic decisions)" or similar to reflect that concept (0), initiative plan (1), and architecture (2) are the strategic phases
  - [ ] Adjust Phase 4-5 and 6-7 ranges if they reference old numbers (they should still be correct)
- [ ] Rewrite **Phases Detail** section:
  - [ ] Renumber current "1. **Phase 1: Concept**" → "0. **Phase 0: Concept**"
  - [ ] Update concept description to mention that Solution Approach should identify capability areas for the initiative plan
  - [ ] Insert new "1. **Phase 1: Initiative Plan**" section after concept:
    - PM and Architect collaborate to decompose the concept into named initiatives
    - Single living document per project at `user/project-guides/001-initiative-plan.{project}.md`
    - Each initiative gets a base index and scope description
    - Index gap is project-level decision (default 20, wider for broad initiatives)
    - Cross-initiative dependencies are declared
    - Outcome: _An ordered list of initiatives with base indices, scope descriptions, and dependency declarations._
  - [ ] Update "2. **Phase 2: Architecture**" — keep number, but:
    - [ ] Remove the "Note on Specifications" paragraph entirely
    - [ ] Remove reference to `guide.ai-project.002-spec`
    - [ ] Update the entry point descriptions to reference the initiative plan as the source of initiative identification
  - [ ] Phases 3-7: no changes needed (verify numbering is still correct)
- [ ] Update **Project Scale and Entry Points** section:
  - [ ] "Phase 1 (Concept)" → "Phase 0 (Concept)"
  - [ ] Add Initiative Plan where appropriate in the flow descriptions
  - [ ] Update "Skip directly to Phase 5" for ad-hoc work — no change needed here
- [ ] Update **Living Document Pattern** → Applies To section:
  - [ ] Remove "Specifications (`002-spec.{project}.md`) — when used"
  - [ ] Add "Initiative plans (`001-initiative-plan.{project}.md`)" if appropriate
- [ ] Update **Project Guide Files** listing:
  - [ ] Rename concept entry from `guide.ai-project.001-concept` to `guide.ai-project.000-concept`
  - [ ] Remove `guide.ai-project.002-spec` entry
  - [ ] Add `guide.ai-project.001-initiative-plan` entry
  - [ ] Rename `guide.ai-project.000-process` reference to `guide.ai-project.process` (should already be done from Task 2, verify)
- [ ] Success criteria:
  - [ ] Process guide phases list starts at Phase 0 and includes Initiative Plan at Phase 1
  - [ ] No references to spec guide in the process guide
  - [ ] Phase Approval reflects new numbering
  - [ ] Project Scale entry points reference Phase 0 for concept
  - [ ] Guide file listing is current and accurate

**Commit**: `guides: rewrite process guide phases for 0-based numbering with initiative plan`

---

### Task 5: Create Initiative Plan Guide
**Objective**: Create `guide.ai-project.001-initiative-plan.md` as the Phase 1 guide.

- [ ] Create file at `project-guides/guide.ai-project.001-initiative-plan.md`
- [ ] Include frontmatter:
  ```yaml
  ---
  layer: process
  phase: 1
  phaseName: initiative-plan
  guideRole: primary
  audience: [human, ai]
  description: Phase 1 playbook for decomposing a project concept into named initiatives with index assignments and dependency declarations.
  dependsOn:
    - guide.ai-project.process.md
    - guide.ai-project.000-concept.md
  dateCreated: 20260322
  dateUpdated: 20260322
  ---
  ```
- [ ] Include the following sections (refer to slice design for document structure and content):
  - [ ] **Summary**: Phase 1 bridges concept to architecture by formalizing initiatives
  - [ ] **Purpose**: The fan-out point — one project decomposes into many initiatives, each producing an architecture document and slice plan
  - [ ] **Inputs and Outputs**: Input is concept document; output is `user/project-guides/001-initiative-plan.{project}.md`
  - [ ] **Multiplicity pattern**: concept 1:1 initiative plan, initiative plan 1:N architectures, architecture 1:1 slice plan, slice plan 1:N slices
  - [ ] **Document Structure**: YAML frontmatter template and markdown structure (use checklist format for initiatives, matching slice plan convention)
  - [ ] **Index Gap Convention**: Project-level decision. Default gap of 20 (100, 120, 140). Broad initiatives may use 100+. Choice recorded in the plan, adjustable via re-indexing.
  - [ ] **Cross-Initiative Dependencies**: How to declare and maintain the dependency graph
  - [ ] **Guidelines**: Keep at initiative level, don't prescribe slice boundaries. Identify capability areas from the concept's Solution Approach. Indices are tentative.
  - [ ] **Output Location**: `user/project-guides/001-initiative-plan.{project}.md`
  - [ ] **Success Criteria**: Initiative plan exists, all concept capability areas are represented, indices assigned, dependencies declared
- [ ] Success criteria:
  - [ ] File exists at `project-guides/guide.ai-project.001-initiative-plan.md`
  - [ ] Valid frontmatter with `phase: 1`
  - [ ] Document structure template includes YAML example with `docType: initiative-plan`
  - [ ] Index gap convention is documented as project-level decision with default of 20
  - [ ] Checklist format for initiative listing matches slice plan convention

**Commit**: `guides: add initiative plan guide for Phase 1`

---

### Task 6: Remove Spec Guide and Clean Up References
**Objective**: Delete `guide.ai-project.002-spec.md` and remove/replace all references to it.

- [ ] `git rm project-guides/guide.ai-project.002-spec.md`
- [ ] Remove or update references across 13 files. For each reference, either remove the line or replace with the architecture prompt reference as appropriate:
  - [ ] `project-guides/guide.ai-project.process.md` — should already be cleaned in Task 4, verify
  - [ ] `project-guides/guide.ai-project.003-slice-planning.md` — check `dependsOn` and body
  - [ ] `project-guides/guide.ai-project.090-code-review.md` — check body
  - [ ] `project-guides/readme.md` — remove spec entry from guide listing
  - [ ] `scripts/rename-private-to-user-in-repo.sh` — check context, update or leave
  - [ ] `scripts/template-stubs/prompt.legacy-migration.md` — update references
  - [ ] Active user/ files (check `user/tasks/` and `user/slices/` for active references)
- [ ] Run verification: `grep -r "guide.ai-project.002-spec" project-guides/ scripts/` — should return zero matches
- [ ] Success criteria:
  - [ ] `guide.ai-project.002-spec.md` does not exist
  - [ ] Zero references to `guide.ai-project.002-spec` in project-guides/ and scripts/
  - [ ] No broken `dependsOn` arrays

**Commit**: `guides: remove legacy spec guide and clean up references`

---

### Task 7: Update Prompts — Concept (Phase 0) and Architecture (Phase 2)
**Objective**: Update existing prompts in `prompt.ai-project.system.md` for the new phase structure.

- [ ] **Context Profiles** section (top of file):
  - [ ] Rename `concept-phase-1` → `concept-phase-0`
  - [ ] Add `initiative-plan-phase-1: [fileConcept]`
  - [ ] Verify `architecture-phase-2` is unchanged
- [ ] **Concept prompt** (currently "##### Concept (Phase 1)"):
  - [ ] Update heading to "##### Concept (Phase 0)"
  - [ ] Update body: "Phase 1" → "Phase 0" where it refers to the concept phase
  - [ ] Update reference from `guide.ai-project.001-concept` → `guide.ai-project.000-concept`
  - [ ] Reference to `guide.ai-project.000-process` should already be `guide.ai-project.process` from Task 2
- [ ] **Architecture prompt** (Phase 2):
  - [ ] Remove any remaining references to spec or `guide.ai-project.002-spec`
  - [ ] Verify process guide reference is updated (should be from Task 2)
- [ ] Success criteria:
  - [ ] Context profiles reflect Phase 0 concept and Phase 1 initiative plan
  - [ ] Concept prompt header and body reference Phase 0
  - [ ] No spec references in architecture prompt
  - [ ] All guide filename references use new names

**Commit**: `guides: update concept and architecture prompts for new phase numbering`

---

### Task 8: Create Initiative Plan Prompt (Phase 1) and Migration Variant
**Objective**: Add a new Phase 1 prompt section and a migration variant to `prompt.ai-project.system.md`.

- [ ] Add new **Initiative Plan (Phase 1)** prompt section after the Concept prompt:
  - [ ] Role: Architect (working with PM)
  - [ ] Input: concept document (`user/project-guides/001-concept.{project}.md`)
  - [ ] Output: `user/project-guides/001-initiative-plan.{project}.md`
  - [ ] Reference `guide.ai-project.001-initiative-plan` for detailed guidance
  - [ ] Include guidance on:
    - Identifying capability areas from the concept's Solution Approach
    - Assigning base indices with appropriate gaps (reference guide for convention)
    - Declaring cross-initiative dependencies
    - Using checklist format for initiative listing
  - [ ] Emphasize this is a collaborative PM + Architect task — ask questions, don't assume
- [ ] Add **Initiative Plan Migration** variant (for existing projects):
  - [ ] Scan `user/architecture/` for existing `nnn-arch.*.md` files
  - [ ] Extract initiative names, index ranges, and dependencies from frontmatter and content
  - [ ] Scan for `nnn-slices.*.md` to determine initiative status
  - [ ] Generate initiative plan in checklist format
  - [ ] Present to PM for review before writing
  - [ ] Tag as migration variant within the Phase 1 section
- [ ] Success criteria:
  - [ ] Phase 1 prompt section exists between Concept (Phase 0) and Architecture (Phase 2)
  - [ ] Migration variant is included and clearly tagged
  - [ ] Both reference `guide.ai-project.001-initiative-plan`

**Commit**: `guides: add initiative plan prompt and migration variant`

---

### Task 9: Remove Deprecated Prompts
**Objective**: Remove deprecated prompt sections from `prompt.ai-project.system.md`.

- [ ] Remove **Summarize Context** prompt section (under Deprecated heading)
- [ ] Remove **Task Breakdown Supplement** prompt section (under Deprecated heading)
- [ ] If the Deprecated section is now empty, remove the section heading as well
- [ ] Success criteria:
  - [ ] No "Summarize Context" prompt in the file
  - [ ] No "Task Breakdown Supplement" prompt in the file
  - [ ] File structure remains clean (no orphaned headings)

**Commit**: `guides: remove deprecated prompts`

---

### Task 10: Update Git Rules
**Objective**: Add `review` commit type to `project-guides/rules/git.md`.

- [ ] Add to the Types list in `project-guides/rules/git.md`:
  ```
  - `review` — Code review, design review, or audit documentation
  ```
  - Place alphabetically or logically near `docs` (both are documentation-adjacent)
- [ ] Check for any phase number references in rules files and update if present
- [ ] Success criteria:
  - [ ] `review` appears in the commit types list in `project-guides/rules/git.md`
  - [ ] No stale phase references in rules/

**Commit**: `guides: add review commit type to git rules`

---

### Task 11: Final Verification Sweep
**Objective**: Run all verification checks from the slice design to confirm completeness.

- [ ] `grep -r "guide.ai-project.000-process" project-guides/ file-naming-conventions.md scripts/` — zero matches
- [ ] `grep -r "guide.ai-project.001-concept" project-guides/` — zero matches (should be 000-concept now)
- [ ] `grep -r "guide.ai-project.002-spec" project-guides/` — zero matches
- [ ] Confirm file existence:
  - [ ] `project-guides/guide.ai-project.process.md` exists
  - [ ] `project-guides/guide.ai-project.000-concept.md` exists with `phase: 0`
  - [ ] `project-guides/guide.ai-project.001-initiative-plan.md` exists with `phase: 1`
  - [ ] `project-guides/guide.ai-project.002-spec.md` does NOT exist
- [ ] Read process guide — phases list 0 through 7 with Initiative Plan at 1
- [ ] Read prompt file — has Phase 0, Phase 1, Phase 2 prompts; no deprecated entries
- [ ] `grep "review" project-guides/rules/git.md` — shows the review commit type
- [ ] Verify all guide `dependsOn` fields reference correct filenames
- [ ] Success criteria:
  - [ ] All verification checks pass
  - [ ] No broken cross-references

**Commit**: `guides: final verification sweep for phase renumbering`
