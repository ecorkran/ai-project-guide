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
dateCreated: 20260323
dateUpdated: 20260323
---

#### Summary
This guide provides instructions for Phase 1: Initiative Plan. This phase takes the approved concept document and decomposes it into named initiatives — cohesive bodies of work that will each produce an architecture document and slice plan.

The initiative plan is the fan-out point between "one project" and "many architectures." It bridges concept-level thinking (what capability areas exist) with architecture-level work (how each area is designed and sliced).

#### Purpose

The multiplicity pattern in this methodology is:
- **Concept** (1 per project) → **Initiative Plan** (1 per project) → **Architecture** (1 per initiative) → **Slice Plan** (1 per initiative) → **Slice Designs** (1 per slice)

Without the initiative plan, the decomposition from "one project" into "many architecture documents" is informal and undocumented. The initiative plan makes this explicit: which initiatives exist, what order they should be tackled, and how they depend on each other.

#### Inputs and Outputs

**Inputs:**
* `guide.ai-project.process` (process guide)
* `guide.ai-project.001-initiative-plan` (this document)
* Concept document (`user/project-guides/001-concept.{project}.md`) — specifically the Solution Approach section, which should identify capability areas

**Outputs:**
* Initiative plan document: `user/project-guides/001-initiative-plan.{project}.md`

#### Roles

PM and Architect collaborate on this phase. The initiative plan is a strategic document — it determines the scope and sequencing of all subsequent architectural work. The AI should ask questions and surface trade-offs rather than making unilateral decisions about initiative boundaries.

#### Core Principles

##### Initiative Independence
Each initiative should:
- Represent a cohesive capability area or body of work
- Have clear boundaries that enable independent architecture design
- Deliver value that can be reasoned about at the architecture level
- Have manageable scope (typically 3-12 slices per initiative)

##### Index Assignment
- Initiatives claim base indices from the 100-799 working range defined in `file-naming-conventions.md`
- **Index gap is a project-level decision**, not a global convention
- Default gap of 20 (100, 120, 140) works for most projects
- Projects with broad initiatives expected to expand significantly may use wider gaps (50, 100, or even 200)
- The choice is recorded in the initiative plan and can be adjusted via re-indexing
- Indices are tentative — they may be reassigned as initiatives are added or reorganized

##### Dependency Declaration
- Cross-initiative dependencies should be explicit
- Dependencies inform sequencing: which initiatives must produce stable interfaces before others can begin architecture design
- Not all dependencies are blocking — some are informational (e.g., "200 should be aware of 100's data model but can design independently")

#### Document Structure

##### Frontmatter
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

##### Content Template
```markdown
# Initiative Plan: {Project}

## Source
001-concept.{project}.md

## Index Convention
{Describe the index gap chosen for this project and rationale.}
Default: 20-based (100, 120, 140). Adjust based on expected initiative breadth.

## Initiatives

1. [ ] **(100) {Initiative Name}** — {Scope description}. Dependencies: None (foundation). Status: not_started
2. [ ] **(120) {Initiative Name}** — {Scope description}. Dependencies: [100]. Status: not_started
3. [ ] **(140) {Initiative Name}** — {Scope description}. Dependencies: [100, 120]. Status: not_started

## Cross-Initiative Dependencies
- 120 depends on 100: {reason — e.g., "needs stable agent interfaces from behavior engine"}
- 140 depends on 120: {reason}

## Notes
- Indices are tentative and may be reassigned as initiatives are added or reorganized.
- New initiatives discovered during development are added here with the next available base index.
- Check off initiatives as their architecture documents and slice plans are complete.
```

#### Guidelines

- **Keep at initiative level.** Do not prescribe slice boundaries — that's Phase 3's job. An initiative should be described in terms of its capability scope, not its implementation tasks.
- **Derive from the concept.** The concept's Solution Approach section should have identified capability areas. Each capability area typically maps to one initiative. If it doesn't, discuss with the PM.
- **Don't over-decompose.** A small project may have only one or two initiatives. Not every project needs many. If the concept describes a single coherent system with no natural decomposition points, one initiative is fine.
- **Sequence by dependency and risk.** Foundation work comes first. High-risk or highly-depended-upon initiatives should be designed early so downstream initiatives can design against stable interfaces.
- **Flag unknowns.** If you're uncertain whether something is one initiative or two, say so. The PM decides scope boundaries.

#### Migration for Existing Projects

Projects that already have architecture documents but no initiative plan can generate one retroactively:

1. Scan `user/architecture/` for existing `nnn-arch.*.md` files
2. Extract initiative names, index ranges, and dependencies from architecture doc frontmatter and content
3. Scan for `nnn-slices.*.md` to determine initiative status (has slice plan = at least in_progress)
4. Generate `user/project-guides/001-initiative-plan.{project}.md` with initiatives listed in checklist format
5. Present to PM for review before writing

This is agent-assisted — see the v0.14.0 migration guide (`migrations/20260323-migration-v0.14.0.md`) for the full migration prompt.

#### Output Location

Save as `001-initiative-plan.{project}.md` in the `user/project-guides/` directory.

#### Success Criteria
Phase 1 is complete when:
- [ ] Initiative plan document exists with proper frontmatter
- [ ] All capability areas from the concept are represented as initiatives
- [ ] Each initiative has a base index, scope description, and dependency declaration
- [ ] Index gap convention is documented
- [ ] Cross-initiative dependencies are declared
- [ ] Project Manager approves the initiative plan
