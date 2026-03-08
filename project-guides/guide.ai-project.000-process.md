---
layer: process
phase: 0               # 0 = meta-guide that defines all phases
phaseName: meta
guideRole: primary
audience: [human, ai]
description: Master process guide describing roles and the slice-based workflow.
dependsOn: []
dateCreated: 20250101
dateUpdated: 20260302
---

#### Overview
This document describes our AI project planning methodology and structure. Projects are organized into architectural initiatives, each broken into vertical slices that can be designed and implemented independently. This reduces complexity, improves context management, and enables AI agents to reliably execute implementation work when given properly structured context.

#### Roles
- **Project Manager & Tech Lead**: Typically a human. Oversees overall project direction, coordinates tasks, and makes key decisions. May delegate approval authority for specific phases (see Phase Approval below).
- **Architect** (Human or AI): Provides high-level strategy, architecture design, and brainstorming support. Typically a frontier model with extended reasoning capabilities, or a senior human engineer.
- **Researcher** (AI): A deep reasoning or research-specialized model used for investigation, analysis, and complex problem exploration.
- **Senior AI (Agents)**: Specialized AI agents or tools (e.g., Claude Code, Cursor, Cline) capable of advanced tasks — code generation, advanced logic, or system design.
- **Junior AI**: Capable general-purpose models operating under agent direction. These can be strong models in their own right, but in this context they do not make product decisions and are managed by the Senior AI or Project Manager.
- **Code Reviewer** (Human or AI): Reviews code and documents findings in accordance with the AI Code Review Guide.

Note: Multiple roles can be combined in a single contributor (human or AI), and there can also be multiple contributors in a given role. The Project Manager will assign roles.

---
#### Project Phases

##### Phase Approval
Each phase has an approval authority that must sign off before proceeding to the next phase. By default, the Project Manager & Tech Lead approves all phases. However, the Project Manager may delegate approval authority:

- **Phases 1–3** (strategic decisions): Normally require human PM approval.
- **Phases 4–5** (design and planning execution): May be approved by an AI Architect when operating under established patterns and clear architectural direction.
- **Phases 6–7** (execution and integration): May self-validate via tests and CI when automation pipelines are in place.

When working on project phases, ensure you have all required information first. If in doubt, request and obtain the required information from the Project Manager before proceeding. Do not guess or make assumptions.

##### Slices
All work is organized as slices under architectural initiatives. **Slices** are vertical cuts through the project architecture — complete units of work that deliver independent value. They include all layers needed for that functionality: UI, business logic, data storage, testing. A slice can be demonstrated and verified on its own.

Slices are grouped under architectural initiatives, each with its own architecture document and slice plan. There is no rule that an initiative cannot have more than one slice plan, but they usually don't.

##### Phases Detail

1. **Phase 1: Concept**
   - Project Manager provides an initial product concept in plain language.
   - Collaborate with the Architect to refine the vision, identify challenges, and define the core product concept.
   - Include initial tech stack identification and key constraints where known.
   - Outcome: _A short doc describing the problem, target users, overall solution approach, and initial technology direction._

2. **Phase 2: Architecture**
   - Establish the structural foundation that will inform slice planning. This phase scales by project size and entry point:
   
   **Small or new project** (single initiative):
   - Create a project-level High-Level Design (HLD) at `user/architecture/nnn-arch.hld-{project}.md` using the 050-099 range per `file-naming-conventions.md`.
   - The HLD serves as both the architectural blueprint and the basis for slice planning.
   - Include: system architecture overview, major subsystems, technology stack rationale, data flow, integration points, infrastructure/deployment (if applicable).
   - Avoid: implementation specifics, slice-level breakdown, code examples.
   - Proceed directly to Phase 3 (Slice Planning) from the HLD.
   
   **Large or evolving project** (multiple initiatives):
   - Identify architectural components or initiatives from the concept.
   - For each component, create an architecture document at `user/architecture/nnn-arch.{component-name}.md` using the 100-799 initiative working range per `file-naming-conventions.md`.
   - Each component architecture document functions as the HLD for its scope.
   - Each component then gets its own slice plan in Phase 3.
   
   **New initiative on existing project**:
   - Create the component architecture document directly. No project-level concept or HLD needed.
   - Proceed to Phase 3 (Slice Planning) for that component.
   
   The Architect role leads this phase. If we are applying technologies for which we do not have knowledge, indicate this — search in `tool-guides/` for available knowledge. Project Manager gathers missing knowledge and adds to project.
   
   - Outcome: _Architectural blueprint(s) that guide slice planning. One HLD for small projects, or component architecture documents for larger projects._

   **Note on Specifications**: For projects requiring a traditional specification document (e.g., client-facing deliverables or formal requirements), use `guide.ai-project.002-spec` to create `user/project-guides/002-spec.{project}.md` as a sub-step of this phase. This is rarely needed for projects following the architecture-first workflow.

3. **Phase 3: Slice Planning**
   - Break the work described in the parent architecture document into manageable vertical slices.
   - Use `guide.ai-project.003-slice-planning` for detailed guidance.
   - **Parent document** (one of the following):
     - Project-level HLD (`user/architecture/nnn-arch.hld-{project}.md`)
     - Component architecture document (`user/architecture/nnn-arch.{component}.md`)
   - Categorize work into four types:
     - **Foundation work** (must be done first, hard to slice — e.g., project setup, core architecture)
     - **Functional slices** (deliver new functionality — e.g., user auth, dashboard, MCP tools, CLI commands)
     - **Migration / refactoring slices** (extract, move, or restructure existing code — e.g., monorepo extraction, storage migration)
     - **Integration work** (happens after functional or migration slices — e.g., performance optimization, deployment, documentation)
   - Each slice should be as independent as possible and deliver meaningful value (user-facing, developer-facing, or architectural enablement).
   - Strive for early testability. Build core capabilities then expand.
   - Identify dependencies between slices and create implementation order.
   - For complex initiatives, create lightweight "slice sketches" to identify potential conflicts.
   - Output location per `file-naming-conventions.md`:
     - Project-level: `user/project-guides/003-slices.{project}.md`
     - Architecture-level: `user/architecture/nnn-slices.{name}.md` (sharing the parent architecture document's base index)
   - Outcome: _Ordered list of slices with dependencies and rough effort estimates._

**For each slice, execute the following phases:**

4. **Phase 4: Slice Design (Low-Level Design)**
   - Create detailed design for the specific slice.
   - Use `guide.ai-project.004-slice-design` for detailed guidance.
   - Include specific technical decisions, data flows, and component interactions.
   - Identify any cross-slice dependencies or conflicts.
   - Create mockups or detailed specifications for UI components (if applicable).
   - Save as `user/slices/nnn-slice.{slice-name}.md` where `nnn` follows initiative-based indexing per `file-naming-conventions.md`.
   - Outcome: _Detailed design document for implementing this slice._

5. **Phase 5: Slice Task Breakdown**
   - Convert slice design into granular, actionable tasks.
   - Use `guide.ai-project.005-task-breakdown` for detailed guidance.
   - For each {tool} in use described in the design, ensure that you consult knowledge in `ai-project-guide/tool-guides/{tool}/`. If not present, search web if possible and alert Project Manager.
   - Only include tasks that can reasonably be completed by an AI. Do not include open-ended human-centric tasks such as SEO optimization.
   - If insufficient information is available to fully convert an item into tasks, _stop_ and request clarifying information before continuing.
   - Save as `user/tasks/nnn-tasks.{slice-name}.md` where `nnn` matches the parent slice's index per `file-naming-conventions.md`.
   - Include YAML front matter and context header:
     ```yaml
     ---
     slice: {slice-name}
     project: {project-name}
     lld: user/slices/nnn-slice.{slice-name}.md
     dependencies: [list-of-prerequisite-slices]
     projectState: brief description of current state
     dateCreated: YYYYMMDD
     dateUpdated: YYYYMMDD
     status: not_started | in_progress
     ---
     
     ## Context Summary
     - Working on {slice-name} slice
     - Current project state and key assumptions
     - Dependencies and prerequisites
     - What this slice delivers
     - Next planned slice
     ```
   - Each task must have:
     - Clearly defined scope (precise and narrow)
     - Actionable, unambiguous instructions for junior AI or human developer
     - Success criteria clearly defined (what done looks like)
   - Common Task Considerations:
	   - If this project contains package.json, ensure a project setup task is created and add the scripts contained in `snippets/npm-scripts.ai-support.json` to its scripts block. This also applies when creating package.json.
   - **Optional: Task Enhancement and Expansion** — If tasks are unusually complex or the implementing agent has demonstrated difficulty with similar work, enhance or subdivide tasks to improve the chances that junior AI workers can complete them independently. Use `guide.ai-project.006-task-expansion` for detailed guidance. Skip when the task breakdown is already sufficiently detailed, which is the common case.
   - Outcome: _A detailed task list that can be executed in a single context session._

6. **Phase 6: Slice Execution (AI/Human Collaboration)**
   - Tasks are assigned to the Senior AI or human developers. They will delegate tasks to Junior AIs or junior human developers.
   - The Project Manager or Senior AI (in a reviewer capacity) perform:
     - Code reviews
     - Design reviews
     - Ensuring alignment with the slice design and overall project vision

   - Outcome: _Working software increment for the slice, tested and validated._

7. **Phase 7: Slice Integration**
*Note*: this phase is only run when explicitly needed.  It is omitted in most workflows.
   - Integrate completed slice with existing codebase.
   - For single-developer projects, this is typically straightforward.
   - For team projects or future parallelization, this becomes similar to git merge/PR integration.
   - Verify that slice dependencies and interfaces work as expected.
   - Update project documentation and architecture understanding where applicable.
   - Check off the completed slice in the parent slice and/or slice plan
   - Ensure that any relevant completed files (task, slice) have status: complete
   - Outcome: _Integrated functionality ready for the next development cycle._

##### DEVLOG
DEVLOG updates are a standing practice across all phases, not specific to any single phase. At the end of each work session — whether a slice is complete, partially complete, or work was interrupted — write a Session State Summary to `DEVLOG.md` in the project root. Use the Session State Summary prompt in `prompt.ai-project.system` for formatting guidance. DEVLOG entries should record what was accomplished and the current state; they do not determine what to work on next (that is the responsibility of workflow navigation or orchestration).

---

#### Project Scale and Entry Points

Projects use the same phases but differ in scope and entry point:

**Single-initiative project** (new, small-to-medium):
- Phase 1 (Concept) → Phase 2 (Architecture: single HLD) → Phase 3 (Slice Planning) → execute slices

**Multi-initiative project** (new, large):
- Phase 1 (Concept) → Phase 2 (Architecture: identify components, create architecture docs) → Phase 3 (Slice Planning per component) → execute slices

**New initiative on existing project**:
- Phase 2 (Architecture: component doc) → Phase 3 (Slice Planning) → execute slices

**Small maintenance or ad-hoc work**:
- Skip directly to Phase 5 (Task Breakdown) using the Ad-Hoc Tasks prompt in `prompt.ai-project.system`.

---

### Resource Structure
The following structure should be present in every project. Assume files are in markdown format (.md) unless otherwise specified. Tool documentation may also be present as .pdf.

```
{project-root}/
└── project-documents/
    ├── ai-project-guide/  # Git submodule (framework guides)
    │   ├── project-guides/    # process & methodology (start here)
    │   ├── framework-guides/  # app-level platforms (Next.js, Astro …)
    │   ├── tool-guides/       # importable libs (SciChart, Three.js …)
    │   ├── api-guides/        # external data endpoints (USGS, ArcGIS …)
    │   ├── domain-guides/     # cross-cutting subject matter (hydrology …)
    │   ├── snippets/          # copyable code/config examples
    │   └── scripts/           # setup and utility scripts
    └── user/               # Your project-specific work (parent repo)
```

###### private subfolders
```markdown
* user/: information customized to our current project.
* user/analysis/: analysis documents and research findings.
* user/architecture/: architecture documents (project HLD, initiative architecture docs, slice plans).
* user/project-guides/: project-specific guide customizations.
* user/reviews/: code review findings, task lists, and resolutions.
* user/slices/: slice-specific low-level designs (nnn-slice.{slice-name}.md).
* user/tasks/: all task breakdown files (nnn-tasks.{slice-name}.md or legacy files).
```

> Each folder has its own `README.md` or `introduction.md` with deeper context.
> Attachments live in `project-documents/z-attachments/`.

---

### Living Document Pattern

When creating concept, spec, or architecture documents, use the **living document pattern** where human and AI collaborate on a single evolving file rather than creating fragmented documents:

#### Document Structure
```markdown
---
# YAML frontmatter as appropriate
---

# Overview
[One-sentence description of what this document is]

## User-Provided Concept
[Human's initial concept, goals, requirements, design ideas]
[This section is SACRED - AI must preserve it during all edits]

## {AI-Enhanced Sections}
[AI adds structured content: Design, Specification, Technical Details, etc.]
```

#### How It Works
1. **Human creates file**: Add file with numbered prefix (e.g., `001-concept.{project}.md`, `120-arch.{component}.md`)
2. **Human provides concept**: Fill in User-Provided Concept section (can be simple or detailed)
3. **AI enhances**: AI reads user concept and adds structured technical sections
4. **Iterative refinement**: Both human and AI continue to evolve the document
5. **Concept preserved**: AI never overwrites or removes User-Provided Concept section

#### Benefits
- **Single source of truth**: No fragmentation across multiple files
- **User intent preserved**: Human's original vision always accessible
- **Collaborative evolution**: Document grows with the project
- **Clear ownership**: User Concept vs AI Technical sections are distinct

#### Applies To
- Concept documents (`001-concept.{project}.md`)
- Specifications (`002-spec.{project}.md`) — when used
- Architecture documents (`nnn-arch.{component}.md`)
- Slice designs (`nnn-slice.{slice}.md`)

This replaces the older pattern where human creates one file and AI creates a separate elaboration file.

---

###### Project Guide Files
```markdown
These files, shared by all of our projects, are contained in {project-root}/project-documents/ai-project-guide/project-guides/.  Synonyms (syn, aka (for also known as)) are provided as some older documentation may still reference by these names.

* guide.ai-project.000-process (aka: AI Project Guide): this document.  Describes 
  roles and project phases.  Always start here.
* guide.ai-project.001-concept (aka: AI Project Concept Guide): details on creating 
  Project Concept documents.
* guide.ai-project.002-spec (aka: AI Spec Guide): details on creating Project 
  Specification (Spec) documents.  Rarely needed for architecture-first workflows.
* guide.ai-project.003-slice-planning: guidance on breaking architectural components
  into vertical slices.
* guide.ai-project.004-slice-design: detailed guidance on creating low-level designs
  for individual slices.
* guide.ai-project.005-task-breakdown: guidance on converting slice designs
  into granular task lists.  
* guide.ai-project.006-task-expansion (aka: AI Task Expansion Guide): specific
  guidance on task expansion for slice-based development.  Optional, rarely needed.
* guide.ai-project.090-code-review (aka: AI Code Review Guide): specific guidance for 
  performing and responding to code reviews.
* guide.ai-project.091-legacy-task-migration: guidance for migrating legacy projects
  to the slice-based methodology.
* guide.ui-development.ai (aka: AI Development Guide - UI): specific guidance 
  pertaining to UI/UX tasks.
* prompt.ai-project.system (aka: AI Project Prompt Templates): parameterized 
  prompts to assist in creating and completing projects using the AI Project 
  Guide. Usable by humans or AIs.
* prompt.code-review-crawler: prompt for automated code review crawling.
* notes.ai-project.onboarding: onboarding notes primarily for human developers.
* rules/: modular code rules organized by platform/technology.  Copy to 
  IDE-specific directories (.cursor/rules/, etc) as needed.  

Additional Relevant in `project-documents/` Directory:
* directory-structure: defines our `project-documents` directory structure
* file-naming-conventions: describes our file-naming conventions
```

###### Tool Guide Files
```markdown
These files provide knowledge on use of 3rd party tools, both in general and in specific {tool} subdirectories.  All documents for {tool} will be in the `ai-project-guide/tool-guides/{tool}/` subdirectory.  Always start with tool's introduction, which should be located at `ai-project-guide/tool-guides/{tool}/introduction.md`.  If you cannot locate this, confirm usage of the tool and presence of its documentation with the Project Manager before starting work.

* introduction (aka: AI Tool Overview - {tool}): Overall guidance for 
  {tool}.  Always start here.
* setup: Information on installing and configuring {tool}.
* guide.{descriptions}: our specific guides and indices.  If `documentation` 
  subdirectory is present, these guides may be built from review of 
  documentation files.
* {tool}/documentation: documentation by tool authors, from web or download.  
  May be in alternate formats such as PDF.
* {tool}/notes: specific knowledge items and reference notes for {tool}.
  Often used to provide additional detail for complex {tool} tasks.
```

##### Task Files
```markdown
Task files are created in several places as the output of various prompts.  All such files should be created using checklist format.  For any such file, important sub-items and all success criteria should have checkboxes.  Do not include time estimates, though you may include relative effort levels (1-n not 15 min, 2 hours, etc).

The following provides an example of a well-created task file item:

### Task 3.4: Migrate BlogIndexCard
**Owner**: Junior AI
**Dependencies**: Task 3.3
**Objective**: Migrate complex BlogIndexCard that loads and displays multiple posts.

**Migration Steps**:
- [x] **Create ui-core component**:
- File: `packages/ui-core/src/components/cards/BlogIndexCard.tsx`
- Remove getAllContent dependency
- Add ContentProvider for multiple content loading
- Abstract content fetching logic

- [x] **Handle complex content loading**:
- Support for loading multiple posts
- Filtering and limiting functionality
- Sorting by date

- [x] **Framework integration**:
- Next.js adapter with server-side content loading
- Preserve async functionality for server components

**Success Criteria**:
- [x] Multiple post loading works
- [x] Filtering and limiting functional
- [x] Date sorting preserved
- [x] Server component compatibility maintained

**Files to Create**:
- `packages/ui-core/src/components/cards/BlogIndexCard.tsx`
- `packages/ui-adapters/nextjs/src/components/BlogIndexCardWithContent.tsx`
```
