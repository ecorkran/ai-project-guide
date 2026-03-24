---
slice: phase-renumbering-and-initiative-plan
project: ai-project-guide
lld: user/slices/111-slice.phase-renumbering-and-initiative-plan.md
dependencies: []
projectState: Planning artifacts (arch, slice plan, slice design) complete. No implementation started.
dateCreated: 20260322
dateUpdated: 20260324
status: complete
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

- [x] `git mv project-guides/guide.ai-project.000-process.md project-guides/guide.ai-project.process.md`
- [x] Update frontmatter: change `phase: 0` and `phaseName: meta` to remove phase number. Set `phase: meta` or remove the `phase` field entirely — the process guide is not a phase.
  - Keep `layer: process` and all other frontmatter fields
- [x] Success criteria:
  - [x] File exists at `project-guides/guide.ai-project.process.md`
  - [x] No file at `project-guides/guide.ai-project.000-process.md`
  - [x] Frontmatter reflects meta status (no numeric phase)

**Commit**: `guides: rename process guide to drop 000 index`

---

### Task 2: Update All References to Process Guide Filename
**Objective**: Replace all occurrences of `guide.ai-project.000-process` with `guide.ai-project.process` across the codebase.

- [x] Update references in **project-guides/** (highest priority — these are machine-parsed):
  - [x] `guide.ai-project.001-concept.md` — `dependsOn` field and body text (2 occurrences)
  - [x] `guide.ai-project.003-slice-planning.md` — `dependsOn` and body (2)
  - [x] `guide.ai-project.004-slice-design.md` — `dependsOn` and body (2)
  - [x] `guide.ai-project.005-task-breakdown.md` — `dependsOn` and body (4)
  - [x] `guide.ai-project.005-variant-task-expansion.md` — body (3)
  - [x] `guide.ai-project.090-code-review.md` — body (1)
  - [x] `prompt.ai-project.system.md` — body references (13)
  - [x] `project-guides/readme.md` (5)
- [x] Update references in **root-level files**:
  - [x] `file-naming-conventions.md` (1)
  - [x] `readme.md` (1)
- [x] Update references in **scripts/**:
  - [x] `scripts/bootstrap.sh` (1)
  - [x] `scripts/template-stubs/prompt.legacy-migration.md` (4)
- [x] Update references in **rules/**:
  - [x] `project-guides/rules/general.md` (1)
- [x] Update references in **active user/ files** (skip completed/historical slices):
  - [x] `user/architecture/110-slices.schema-and-phases-update.md` (1)
  - [x] `user/tasks/950-tasks.maintenance.md` — if it references the process guide
- [x] Run verification: `grep -r "guide.ai-project.000-process" project-guides/ file-naming-conventions.md scripts/ readme.md` — should return zero matches
- [x] Success criteria:
  - [x] Zero occurrences of `guide.ai-project.000-process` in project-guides/, file-naming-conventions.md, scripts/, readme.md, and rules/
  - [x] All `dependsOn` arrays reference the new filename
  - [x] User/ files with active status are updated; completed files may retain old references

**Commit**: `guides: update all references from 000-process to process`

---

### Task 3: Rename Concept Guide (001 → 000) and Update to Phase 0
**Objective**: Rename `guide.ai-project.001-concept.md` → `guide.ai-project.000-concept.md`, update phase from 1 to 0, and update the Solution Approach section.

- [x] `git mv project-guides/guide.ai-project.001-concept.md project-guides/guide.ai-project.000-concept.md`
- [x] Update frontmatter:
  - [x] `phase: 1` → `phase: 0`
  - [x] `description:` update to reference "Phase 0"
  - [x] `dependsOn: [guide.ai-project.process.md]` (use new process guide name from Task 1)
- [x] Update body text: change any references to "Phase 1" → "Phase 0" and "Phase 2" → keep as "Phase 2" (architecture didn't move)
- [x] Update the document template's YAML example: `phase: 1` → `phase: 0`
- [x] Update Solution Approach section in the document template. Add capability area guidance after existing text (see slice design for exact wording):
  ```
  If the project involves multiple capability areas or components,
  name them here. These are not yet initiatives with indices or
  sequencing — just the identified pieces that Phase 1 (Initiative
  Plan) will later formalize.
  ```
- [x] Update references to `guide.ai-project.001-concept` across the codebase to `guide.ai-project.000-concept`:
  - [x] `guide.ai-project.002-spec.md` — `dependsOn` (will be removed in Task 6, but update if still present)
  - [x] `prompt.ai-project.system.md` — any concept guide references
  - [x] `project-guides/readme.md` — guide listing
  - [x] Process guide (`guide.ai-project.process.md`) — guide listing section
- [x] Success criteria:
  - [x] File exists at `project-guides/guide.ai-project.000-concept.md` with `phase: 0`
  - [x] Solution Approach section includes capability area guidance
  - [x] No references to `guide.ai-project.001-concept` in project-guides/

**Commit**: `guides: rename concept guide to 000, update to Phase 0`

---

### Task 4: Update Process Guide Phases Section
**Objective**: Rewrite the Phases Detail section of the process guide to reflect the new phase numbering (0-7) and include the Initiative Plan phase.

- [x] Update **Phase Approval** section:
  - [x] Change "Phases 1–3 (strategic decisions)" → "Phases 0–2 (strategic decisions)" or similar to reflect that concept (0), initiative plan (1), and architecture (2) are the strategic phases
  - [x] Adjust Phase 4-5 and 6-7 ranges if they reference old numbers (they should still be correct)
- [x] Rewrite **Phases Detail** section:
  - [x] Renumber current "1. **Phase 1: Concept**" → "0. **Phase 0: Concept**"
  - [x] Update concept description to mention that Solution Approach should identify capability areas for the initiative plan
  - [x] Insert new "1. **Phase 1: Initiative Plan**" section after concept:
    - PM and Architect collaborate to decompose the concept into named initiatives
    - Single living document per project at `user/project-guides/001-initiative-plan.{project}.md`
    - Each initiative gets a base index and scope description
    - Index gap is project-level decision (default 20, wider for broad initiatives)
    - Cross-initiative dependencies are declared
    - Outcome: _An ordered list of initiatives with base indices, scope descriptions, and dependency declarations._
  - [x] Update "2. **Phase 2: Architecture**" — keep number, but:
    - [x] Remove the "Note on Specifications" paragraph entirely
    - [x] Remove reference to `guide.ai-project.002-spec`
    - [x] Update the entry point descriptions to reference the initiative plan as the source of initiative identification
  - [x] Phases 3-7: no changes needed (verify numbering is still correct)
- [x] Update **Project Scale and Entry Points** section:
  - [x] "Phase 1 (Concept)" → "Phase 0 (Concept)"
  - [x] Add Initiative Plan where appropriate in the flow descriptions
  - [x] Update "Skip directly to Phase 5" for ad-hoc work — no change needed here
- [x] Update **Living Document Pattern** → Applies To section:
  - [x] Remove "Specifications (`002-spec.{project}.md`) — when used"
  - [x] Add "Initiative plans (`001-initiative-plan.{project}.md`)" if appropriate
- [x] Update **Project Guide Files** listing:
  - [x] Rename concept entry from `guide.ai-project.001-concept` to `guide.ai-project.000-concept`
  - [x] Remove `guide.ai-project.002-spec` entry
  - [x] Add `guide.ai-project.001-initiative-plan` entry
  - [x] Rename `guide.ai-project.000-process` reference to `guide.ai-project.process` (should already be done from Task 2, verify)
- [x] Success criteria:
  - [x] Process guide phases list starts at Phase 0 and includes Initiative Plan at Phase 1
  - [x] No references to spec guide in the process guide
  - [x] Phase Approval reflects new numbering
  - [x] Project Scale entry points reference Phase 0 for concept
  - [x] Guide file listing is current and accurate

**Commit**: `guides: rewrite process guide phases for 0-based numbering with initiative plan`

---

### Task 5: Create Initiative Plan Guide
**Objective**: Create `guide.ai-project.001-initiative-plan.md` as the Phase 1 guide.

- [x] Create file at `project-guides/guide.ai-project.001-initiative-plan.md`
- [x] Include frontmatter:
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
- [x] Include the following sections (refer to slice design for document structure and content):
  - [x] **Summary**: Phase 1 bridges concept to architecture by formalizing initiatives
  - [x] **Purpose**: The fan-out point — one project decomposes into many initiatives, each producing an architecture document and slice plan
  - [x] **Inputs and Outputs**: Input is concept document; output is `user/project-guides/001-initiative-plan.{project}.md`
  - [x] **Multiplicity pattern**: concept 1:1 initiative plan, initiative plan 1:N architectures, architecture 1:1 slice plan, slice plan 1:N slices
  - [x] **Document Structure**: YAML frontmatter template and markdown structure (use checklist format for initiatives, matching slice plan convention)
  - [x] **Index Gap Convention**: Project-level decision. Default gap of 20 (100, 120, 140). Broad initiatives may use 100+. Choice recorded in the plan, adjustable via re-indexing.
  - [x] **Cross-Initiative Dependencies**: How to declare and maintain the dependency graph
  - [x] **Guidelines**: Keep at initiative level, don't prescribe slice boundaries. Identify capability areas from the concept's Solution Approach. Indices are tentative.
  - [x] **Output Location**: `user/project-guides/001-initiative-plan.{project}.md`
  - [x] **Success Criteria**: Initiative plan exists, all concept capability areas are represented, indices assigned, dependencies declared
- [x] Success criteria:
  - [x] File exists at `project-guides/guide.ai-project.001-initiative-plan.md`
  - [x] Valid frontmatter with `phase: 1`
  - [x] Document structure template includes YAML example with `docType: initiative-plan`
  - [x] Index gap convention is documented as project-level decision with default of 20
  - [x] Checklist format for initiative listing matches slice plan convention

**Commit**: `guides: add initiative plan guide for Phase 1`

---

### Task 6: Remove Spec Guide and Clean Up References
**Objective**: Delete `guide.ai-project.002-spec.md` and remove/replace all references to it.

- [x] `git rm project-guides/guide.ai-project.002-spec.md`
- [x] Remove or update references across 13 files. For each reference, either remove the line or replace with the architecture prompt reference as appropriate:
  - [x] `project-guides/guide.ai-project.process.md` — should already be cleaned in Task 4, verify
  - [x] `project-guides/guide.ai-project.003-slice-planning.md` — check `dependsOn` and body
  - [x] `project-guides/guide.ai-project.090-code-review.md` — check body
  - [x] `project-guides/readme.md` — remove spec entry from guide listing
  - [x] `scripts/rename-private-to-user-in-repo.sh` — check context, update or leave
  - [x] `scripts/template-stubs/prompt.legacy-migration.md` — update references
  - [x] Active user/ files (check `user/tasks/` and `user/slices/` for active references)
- [x] Run verification: `grep -r "guide.ai-project.002-spec" project-guides/ scripts/` — should return zero matches
- [x] Success criteria:
  - [x] `guide.ai-project.002-spec.md` does not exist
  - [x] Zero references to `guide.ai-project.002-spec` in project-guides/ and scripts/
  - [x] No broken `dependsOn` arrays

**Commit**: `guides: remove legacy spec guide and clean up references`

---

### Task 7: Update Prompts — Concept (Phase 0) and Architecture (Phase 2)
**Objective**: Update existing prompts in `prompt.ai-project.system.md` for the new phase structure.

- [x] **Context Profiles** section (top of file):
  - [x] Rename `concept-phase-1` → `concept-phase-0`
  - [x] Add `initiative-plan-phase-1: [fileConcept]`
  - [x] Verify `architecture-phase-2` is unchanged
- [x] **Concept prompt** (currently "##### Concept (Phase 1)"):
  - [x] Update heading to "##### Concept (Phase 0)"
  - [x] Update body: "Phase 1" → "Phase 0" where it refers to the concept phase
  - [x] Update reference from `guide.ai-project.001-concept` → `guide.ai-project.000-concept`
  - [x] Reference to `guide.ai-project.000-process` should already be `guide.ai-project.process` from Task 2
- [x] **Architecture prompt** (Phase 2):
  - [x] Remove any remaining references to spec or `guide.ai-project.002-spec`
  - [x] Verify process guide reference is updated (should be from Task 2)
- [x] Success criteria:
  - [x] Context profiles reflect Phase 0 concept and Phase 1 initiative plan
  - [x] Concept prompt header and body reference Phase 0
  - [x] No spec references in architecture prompt
  - [x] All guide filename references use new names

**Commit**: `guides: update concept and architecture prompts for new phase numbering`

---

### Task 8: Create Initiative Plan Prompt (Phase 1) and Migration Variant
**Objective**: Add a new Phase 1 prompt section and a migration variant to `prompt.ai-project.system.md`.

- [x] Add new **Initiative Plan (Phase 1)** prompt section after the Concept prompt:
  - [x] Role: Architect (working with PM)
  - [x] Input: concept document (`user/project-guides/001-concept.{project}.md`)
  - [x] Output: `user/project-guides/001-initiative-plan.{project}.md`
  - [x] Reference `guide.ai-project.001-initiative-plan` for detailed guidance
  - [x] Include guidance on:
    - Identifying capability areas from the concept's Solution Approach
    - Assigning base indices with appropriate gaps (reference guide for convention)
    - Declaring cross-initiative dependencies
    - Using checklist format for initiative listing
  - [x] Emphasize this is a collaborative PM + Architect task — ask questions, don't assume
- [x] Add **Initiative Plan Migration** variant (for existing projects):
  - [x] Scan `user/architecture/` for existing `nnn-arch.*.md` files
  - [x] Extract initiative names, index ranges, and dependencies from frontmatter and content
  - [x] Scan for `nnn-slices.*.md` to determine initiative status
  - [x] Generate initiative plan in checklist format
  - [x] Present to PM for review before writing
  - [x] Tag as migration variant within the Phase 1 section
- [x] Success criteria:
  - [x] Phase 1 prompt section exists between Concept (Phase 0) and Architecture (Phase 2)
  - [x] Migration variant is included and clearly tagged
  - [x] Both reference `guide.ai-project.001-initiative-plan`

**Commit**: `guides: add initiative plan prompt and migration variant`

---

### Task 9: Remove Deprecated Prompts
**Objective**: Remove deprecated prompt sections from `prompt.ai-project.system.md`.

- [x] Remove **Summarize Context** prompt section (under Deprecated heading)
- [x] Remove **Task Breakdown Supplement** prompt section (under Deprecated heading)
- [x] If the Deprecated section is now empty, remove the section heading as well
- [x] Success criteria:
  - [x] No "Summarize Context" prompt in the file
  - [x] No "Task Breakdown Supplement" prompt in the file
  - [x] File structure remains clean (no orphaned headings)

**Commit**: `guides: remove deprecated prompts`

---

### Task 10: Update Git Rules
**Objective**: Add `review` commit type to `project-guides/rules/git.md`.

- [x] Add to the Types list in `project-guides/rules/git.md`:
  ```
  - `review` — Code review, design review, or audit documentation
  ```
  - Place alphabetically or logically near `docs` (both are documentation-adjacent)
- [x] Check for any phase number references in rules files and update if present
- [x] Success criteria:
  - [x] `review` appears in the commit types list in `project-guides/rules/git.md`
  - [x] No stale phase references in rules/

**Commit**: `guides: add review commit type to git rules`

---

### Task 11: Final Verification Sweep
**Objective**: Run all verification checks from the slice design to confirm completeness.

- [x] `grep -r "guide.ai-project.000-process" project-guides/ file-naming-conventions.md scripts/` — zero matches
- [x] `grep -r "guide.ai-project.001-concept" project-guides/` — zero matches (should be 000-concept now)
- [x] `grep -r "guide.ai-project.002-spec" project-guides/` — zero matches
- [x] Confirm file existence:
  - [x] `project-guides/guide.ai-project.process.md` exists
  - [x] `project-guides/guide.ai-project.000-concept.md` exists with `phase: 0`
  - [x] `project-guides/guide.ai-project.001-initiative-plan.md` exists with `phase: 1`
  - [x] `project-guides/guide.ai-project.002-spec.md` does NOT exist
- [x] Read process guide — phases list 0 through 7 with Initiative Plan at 1
- [x] Read prompt file — has Phase 0, Phase 1, Phase 2 prompts; no deprecated entries
- [x] `grep "review" project-guides/rules/git.md` — shows the review commit type
- [x] Verify all guide `dependsOn` fields reference correct filenames
- [x] Success criteria:
  - [x] All verification checks pass
  - [x] No broken cross-references

**Commit**: `guides: final verification sweep for phase renumbering`
