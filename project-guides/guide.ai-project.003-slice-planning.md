---
layer: process
phase: 3
phaseName: slice-planning
guideRole: primary
audience: [human, ai]
description: Phase 3 playbook for breaking work into manageable vertical slices. Applies at project level (from spec) or architecture level (from architecture document).
dependsOn:
  - guide.ai-project.000-process.md
  - guide.ai-project.002-spec.md
dateCreated: 20250101
dateUpdated: 20260214
---

#### Summary
This guide provides instructions for Phase 3: Slice Planning. This phase takes a parent document — either a project specification or an architecture document — and breaks it into manageable, independent slices that can be designed and implemented separately. This approach reduces complexity, improves context management, and enables parallelization.

Slice planning applies at two levels:
- **Project-level**: Breaking a new project (from its spec) into initial vertical slices. Parent document is typically a project specification.
- **Architecture-level**: Breaking an architectural component, restructure, or major initiative into slices within an existing project. Parent document is an architecture document.

The process is the same at both levels. What changes is the parent document, the output location, and the types of work involved.

#### Inputs and Outputs

**Inputs:**
* `guide.ai-project.000-process` (process guide)
* `guide.ai-project.003-slice-planning` (this document)
* **Parent document** — one of:
  * Project specification (Phase 2 output) for project-level planning
  * Architecture document (`user/architecture/nnn-arch.{name}.md`) for architecture-level planning
* Project concept document (Phase 1 output), for reference
* Any existing architecture documentation, for reference

**Outputs:**

*Project-level planning:*
* High-level design document (if one does not already exist): `user/architecture/050-arch.hld-{project}.md`
  * Note: HLD creation is handled by a separate Phase 2.5 prompt. If an HLD or architecture document already exists that serves this purpose, do not create another. Confirm with Project Manager.
* Slice planning document: `user/project-guides/003-slices.{project}.md`

*Architecture-level planning:*
* Slice planning document: `user/architecture/nnn-slices.{name}.md` where `nnn` matches the parent architecture document's index
  * Example: If the parent is `055-arch.context-forge-restructure.md`, the slice plan is `055-slices.context-forge-restructure.md`
* No separate HLD — the architecture document serves as the HLD for this work

#### Core Principles

##### Slice Independence
Each slice should:
- Deliver meaningful value on its own (user-facing, developer-facing, or architectural)
- Have minimal dependencies on other slices
- Be completable as a coherent unit of work with clear boundaries
- Leave the system in a working state when complete
- Have clear interfaces with other parts of the system

##### Four Types of Work

**Foundation Work**
- Must be completed before other slices can begin
- Hard to split further (e.g., project setup, monorepo scaffolding, core infrastructure)
- Usually done first, in dependency order
- Examples: project initialization, database schema, authentication system, workspace configuration

**Feature Slices**
- Deliver new user-facing or developer-facing functionality
- Can be implemented as vertical slices (all layers needed for that functionality)
- Should be prioritized by value and technical risk
- Examples: user dashboard, search functionality, MCP tool implementation, CLI commands

**Migration / Refactoring Slices**
- Extract, move, or restructure existing code without changing its external behavior
- Deliver architectural value: improved testability, reduced coupling, unified implementations
- Must leave the application in a working state — no slice should break functionality that a subsequent slice fixes
- Value may be enablement ("this unblocks the MCP server slice") or structural ("core logic is now testable without Electron")
- Examples: extracting services into a shared package, replacing a storage backend, consolidating duplicate implementations, converting a monolith to a monorepo

**Integration Work**
- Happens after feature or migration slices are complete
- Focuses on cross-cutting concerns, polish, and system-wide quality
- Examples: performance optimization, deployment automation, end-to-end testing, documentation

Not all projects will have all four types. A greenfield project may have no migration work. A restructuring effort may have no feature slices initially. Use whichever categories apply.

##### Sizing Slices
- Slices are broken down into tasks (Phase 5) and tasks may be further expanded (Phase 6). The slice itself does not need to be completable in a single session — that is the task's job.
- A well-sized slice is a coherent unit of work that delivers a clear outcome and can be verified independently.
- If a slice feels overwhelming or its success criteria span too many concerns, split it further.
- If a slice is trivial (a single file move, a config change), it may be better as a task within another slice.
- Do not include calendar-based or time-based estimates (days, weeks, hours, Q1, etc.). Use relative effort levels (1-5) if effort indication is needed.

#### Slice Planning Process

##### Step 1: Identify the Planning Context

Determine whether this is project-level or architecture-level planning:

**Project-level**: The parent document is a project specification. You may need to create an HLD first (Phase 2.5) or confirm one exists. The output slice plan goes in `user/project-guides/`.

**Architecture-level**: The parent document is an architecture document (`user/architecture/nnn-arch.{name}.md`). The architecture document functions as the HLD — do not create a separate one. The output slice plan goes in `user/architecture/` with a matching index.

If unclear, confirm with the Project Manager before proceeding.

##### Step 2: Identify Foundation Work
List all work that must be completed before other slices can begin:
- Project or workspace initialization and configuration
- Core infrastructure (database, authentication, shared packages, etc.)
- Shared components, types, or design systems
- Third-party integrations that affect multiple slices

Order foundation work by dependencies.

##### Step 3: Define Slices
For each major area of work in the parent document:

**Slice Criteria:**
- Represents a coherent unit of work with a clear outcome
- Can be verified independently (demonstrated, tested, or inspected)
- Has clear success criteria
- Leaves the system in a working state when complete
- Appropriately scoped (see Sizing Slices above)

**Slice Definition Template:**
```markdown
## Slice: {slice-name}
**Value:** What does this deliver? (user value, developer value, or architectural enablement)
**Success Criteria:** How do we know it's complete?
**Dependencies:** What foundation work or other slices must be done first?
**Interfaces:** What APIs, contracts, or packages does this provide/consume?
**Risk Level:** Low/Medium/High based on technical complexity
**Relative Effort:** 1-5
```

Use as many slices as needed to fully capture the scope of the parent document. Use the examples below for guidance.

##### Step 4: Plan Implementation Order
Order slices by:
1. **Dependencies:** Foundation work first, then slices in dependency order
2. **Testability:** Strive for early vertical slice testability. Core first, then expand.
3. **Risk:** Higher-risk slices earlier to surface problems
4. **Value:** Most valuable slices first within each risk tier
5. **Enablement:** Slices that unblock other slices

##### Step 5: Create Slice Sketches (Optional)
For complex efforts, create brief design sketches for each slice to identify potential conflicts:
- Key technical decisions
- Schema or data model needs
- API or interface contracts
- Shared dependency concerns

This helps catch "Slice A needs X but Slice B needs Y" conflicts early.

#### Examples

##### Example 1: Project-Level (Greenfield)

**Project:** Task Management API

**Foundation Work:**
1. Project setup (Node.js, TypeScript, Express, database)
2. Authentication system (JWT, middleware)
3. Database schema and migrations

**Feature Slices:**
1. **Task CRUD** — Create, read, update, delete tasks. Dependencies: Foundation. Risk: Low. Effort: 2
2. **Task Assignment** — Assign tasks to users, notification on assignment. Dependencies: Task CRUD. Risk: Low. Effort: 2
3. **Project Grouping** — Group tasks into projects, project-level views. Dependencies: Task CRUD. Risk: Medium. Effort: 3
4. **Search and Filtering** — Full-text search, filter by status/assignee/project. Dependencies: Task CRUD. Risk: Medium. Effort: 3

**Integration Work:**
- API documentation generation
- Rate limiting and input validation hardening
- Deployment and CI/CD pipeline

##### Example 2: Architecture-Level (Restructure)

**Architecture:** Monorepo Extraction — extracting core logic from an Electron app into shared packages

**Foundation Work:**
1. Monorepo scaffolding (pnpm workspaces, package structure, build config)

**Migration Slices:**
1. **Core Type Extraction** — Move shared types/interfaces to `packages/core`. Electron imports from core instead of local definitions. Dependencies: Foundation. Risk: Low. Effort: 2
2. **Service Extraction** — Move business logic services to `packages/core`. Remove Electron dependencies from extracted services. Dependencies: Core Type Extraction. Risk: Medium. Effort: 3
3. **Storage Migration** — Replace Electron-specific storage with filesystem-based storage in core. Migrate existing data. Dependencies: Service Extraction. Risk: Medium. Effort: 3

**Feature Slices:**
4. **MCP Server** — MCP protocol wrapper exposing core services as tools. Dependencies: Service Extraction. Risk: Medium. Effort: 3
5. **Electron Client Conversion** — Rewire Electron app to use core (direct import) or MCP server (client). Dependencies: MCP Server. Risk: Medium. Effort: 3

**Integration Work:**
- End-to-end testing (MCP server ↔ Claude Code)
- Desktop app packaging with new structure
- Documentation and README for MCP server consumers

#### Common Pitfalls

**Slices Too Large**
- If a slice has more than 5-6 distinct concerns in its success criteria, it's probably too large
- Split by layer, by component, or by data boundary

**Migration Slices That Break Things**
- Every migration slice must leave the application in a working state
- If extracting code from A to B, the slice includes updating all consumers of A to use B
- "Extract now, fix consumers later" is not a valid slice boundary

**Hidden Dependencies**
- Slices that seem independent but share data models or types
- UI patterns that need to be consistent across slices
- Authentication/authorization that affects multiple slices

**Premature Optimization**
- Don't over-engineer slice boundaries
- Some duplication between slices is acceptable
- Perfect abstractions can wait until integration phase

#### Working with AI

**Technical Fellow Role:**
- Help identify logical slice boundaries
- Spot potential conflicts between slices
- Suggest alternative slice organizations
- Validate that slices are appropriately sized
- Identify migration ordering that maintains system stability

**Common AI Questions:**
- "What would be the implications of combining these two slices?"
- "Are there any technical conflicts between these slice designs?"
- "Is this slice appropriately sized, or should it be split further?"
- "What foundation work is needed before this slice can begin?"
- "Does this migration slice leave the system in a working state?"

#### Output Format

**For project-level planning**, create:

*HLD* (`user/architecture/050-arch.hld-{project}.md`) — only if one does not already exist. Confirm with Project Manager.

*Slice Plan* (`user/project-guides/003-slices.{project}.md`):

**For architecture-level planning**, create:

*Slice Plan* (`user/architecture/nnn-slices.{name}.md`, matching parent document index):

**Slice plan template:**
```markdown
---
docType: slice-plan
parent: {path to parent document}
project: {project-name}
dateCreated: YYYYMMDD
dateUpdated: YYYYMMDD
---

# Slice Plan: {Name}

## Parent Document
{Reference to the spec or architecture document this plan derives from}

## Foundation Work
1. [ ] **{Name}** — Brief description. Effort: n/5

## Migration / Refactoring Slices (if applicable)
1. [ ] **{Slice Name}** — Brief description. Dependencies: [list]. Risk: Low/Med/High. Effort: n/5
2. [ ] **{Slice Name}** — Brief description. Dependencies: [list]. Risk: Low/Med/High. Effort: n/5

## Feature Slices (in implementation order)
1. [ ] **{Slice Name}** — Brief description. Dependencies: [list]. Risk: Low/Med/High. Effort: n/5
2. [ ] **{Slice Name}** — Brief description. Dependencies: [list]. Risk: Low/Med/High. Effort: n/5

## Integration Work
1. [ ] **{Name}** — Brief description. Effort: n/5

## Notes
- Key decisions made during planning
- Alternative approaches considered
- Open questions for later phases
```

Include only the slice categories that apply. A restructuring effort may have no feature slices. A greenfield project may have no migration slices.

#### Success Criteria
Phase 3 is complete when:
- [ ] All work from the parent document is categorized into appropriate slice types
- [ ] Slices are appropriately sized (coherent units with clear boundaries)
- [ ] Dependencies between slices are clearly identified
- [ ] Implementation order is logical and accounts for risk and enablement
- [ ] Each slice has clear success criteria
- [ ] Migration slices (if any) each leave the system in a working state
- [ ] Slice plan document is created in the correct location with proper frontmatter
- [ ] Project Manager approves the slice plan

#### Next Steps
With approved slice plan:
1. For each slice: Phase 4 (Slice Design) → Phase 5 (Task Breakdown) → Phase 6 (Task Enhancement) → Phase 7 (Execution) → Phase 8 (Review)
2. Complete integration work as needed
3. Iterate and add new slices as requirements evolve
