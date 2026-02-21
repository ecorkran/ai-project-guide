---
layer: snippet
docType: template
purpose: reusable-llm-prompts
audience:
  - human
  - ai
ai description: Parameterized prompt library mapped to slice-based project phases.
dependsOn:
  - guide.ai-project.000-process.md
npmScriptsAiSupport: "!include ../snippets/npm-scripts.ai-support.json"
dateCreated: 20250724
dateUpdated: 20260218
---
## Prompts
This document contains prepared prompts useful in applying the `guide.ai-project.000-process` and performing additional supplemental tasks.
##### Project Object Model and Parameters
```python
# input keys
{
  project,
  slice,
  section, 
  subsection,
  framework/language,
  tools,
  apis,
  monorepo,
}
```

##### Project Phase (Phase n)
*Use to directly execute a phase without additional instructions needed. Also usable with traditional (non-slice-based) projects.*

```
Refer to the `guide.ai-project.000-process`, and function as a Senior AI.  Implement the phase requested according to the respective procedures described in the guide.  Remember to follow the rules in `directory-structure` for any files or directories created.
```

##### Concept Creation (Phase 1)
```markdown
We're starting work on a new project {project}.  We will use our curated AI Project Creation methods in `guide.ai-project.000-process` (can also be referred to as Project Guide or Process Guide) to assist us in designing and performing the work.  Your role as described in the Project Guide is Technical Fellow.

The initial concept description will be provided by the project manager, ideally as a starter document in `user/project-guides/001-concept.{project}.md`.  Our goal is to refine this initial user-provided concept into the Refined Concept, which should be placed as instructed into the existing document.  The placeholder document should provide any needed details needed for this procedure.

We will use the refined concept as a basis for creating the spec, which will later be refined into designs, slices, features, and tasks.  Use the Project Guide together with the user-provided concept to create the refined concept tailored to our project.

When creating the refined concept, *ask questions* if any information is missing or unclear.  The guideline of do not assume or guess applies, but is even more important here at this early concept state.  Request any needed clarifications from the Project Manager.  If you do not find or receive the user-provided concept description, obtain from Project Manager before proceeding.
```

##### Spec Creation (Phase 2)
```markdown
We're working in our guide.ai-project.000-process, Phase 2: Spec Creation. Use `guide.ai-project.002-spec` with the approved concept document to create the project specification.

Your role is Technical Fellow as described in the Process Guide. Work with the Project Manager to create `user/project-guides/002-spec.{project}.md`.

Required inputs:
- Approved concept document (001-concept.{project}.md)
- Technical stack and requirements from Project Manager
- Any additional specific requirements

Focus on:
- Tech stack with tool-guides availability check
- Top-level features and major workflows
- Architectural considerations and system boundaries
- Sample data and UI sketches (if applicable)
  
Caution:
- Do not write code into the spec.

Keep the spec concise and focused on coordination between components. If you need more information about requirements or cannot access referenced tools, stop and request from Project Manager.

Note: This is a design and planning task, not a coding task.
```

##### High-Level Design (HLD) Creation (Phase 2.5)
*Use this to create a project-level high-level design that serves as the architectural blueprint for slice planning.*

```markdown
We're creating a High-Level Design (HLD) for project {project}. Use the Phase 2.5 guidelines in `guide.ai-project.000-process` with the project concept and specification documents to create the HLD. The HLD serves as the architectural blueprint that will inform slice planning and guide all subsequent slice designs. It establishes the system's structural foundation without diving into slice-level details.

Create file at `user/architecture/nnn-arch.hld-{project}.md` using the next available index in the 050-099 range as defined in `file-naming-conventions.md`.

Your role is Technical Fellow as described in the Process Guide.

**Required Inputs**
- Approved concept document (`user/project-guides/001-concept.{project}.md`)
- Project specification (`user/project-guides/002-spec.{project}.md`)
- Technical stack and architectural constraints from Project Manager

**Document Structure**

**YAML Frontmatter:**
```
```yaml
---
docType: architecture
layer: project
project: {project}
archIndex: nnn
component: hld-{project}
dateCreated: YYYYMMDD
dateUpdated: YYYYMMDD
status: in_progress
---
```
```markdown
**Content Sections:**
1. Overview
- One-sentence summary of the system's purpose
- High-level description of what the system does and why it matters

2. System Architecture
- Major subsystems and their responsibilities
- How subsystems interact and communicate
- Architectural patterns used (e.g., layered, microservices, monolith)

3. Technology Stack Rationale
- Key technology choices and why they were selected
- How the stack supports the architectural goals
- Dependencies between technologies

4. Data Flow
- Major data flows between subsystems
- Data storage strategy (databases, caching, etc.)
- External integrations and APIs

5. Integration Points & System Boundaries
- Clear boundaries between major components
- How components communicate (APIs, events, etc.)
- Third-party service integrations

6. Infrastructure & Deployment (if applicable)
- Deployment architecture
- Scalability and performance considerations
- Environment strategy (dev, staging, prod)

**Guidelines**
- Focus on structure, not implementation: Describe what systems exist and how they relate, not how they work in detail
- Avoid slice-level thinking: Do not break down into individual features or user workflows (that's Phase 3)
- Avoid code examples: This is architecture, not design. No pseudo-code or implementation details
- Be concrete about decisions: Explain why architectural choices were made, not just what they are
- Consider cross-cutting concerns: Address security, scalability, and deployment without getting into task-level details

**Expected Output**
- Complete HLD document at user/architecture/nnn-arch.hld-{project}.md
- Clear enough that slice designers can use it as a reference without ambiguity
- Detailed enough to prevent conflicting slice designs
- All required YAML frontmatter included

**Avoid**
- Vague statements about future optimization or performance
- Speculative infrastructure requirements
- Time estimates or complexity judgments
- Detailed API specifications (defer to slice designs)
- Individual feature descriptions (that's slice planning)

If you need more information about architectural constraints or technical requirements, stop and request clarification from the Project Manager.
*Note: This is a design and planning task, not a coding task.*
```

##### Slice Planning (Phase 3)
```markdown
We're working in our guide.ai-project.000-process, Phase 3: Slice Planning. Use `guide.ai-project.003-slice-planning` to break the work described in the parent document into manageable vertical slices.

**Parent document** (one of the following — only one will apply):
1. Project specification (`user/project-guides/002-spec.{project}.md`) — for project-level planning
2. Architecture document (`user/architecture/nnn-arch.{name}.md`) — for architecture-level planning

If the parent is a project specification, also reference the concept document and any existing architecture documentation. If the parent is an architecture document, it functions as the HLD — do not create a separate one.

Your role is Technical Fellow as described in the Process Guide. Work with the Project Manager to:

1. Identify the planning context (project-level or architecture-level) per the guide
2. Identify foundation work, feature slices, migration/refactoring slices, and integration work as applicable
3. Create the slice plan document in the correct location:
   - Project-level: `user/project-guides/003-slices.{project}.md`
   - Architecture-level: `user/architecture/nnn-slices.{name}.md` (sharing the parent architecture document's base index, per `file-naming-conventions.md`)

Use enough slices to completely define the scope of the parent document. Consider functional requirements only. Ignore non-functional requirements. Avoid speculative risk projections. Do not include calendar or time-based estimates.

When defining slices, focus on slice independence and clear value delivery (user value, developer value, or architectural enablement). Each slice must leave the system in a working state when complete. If you have all required inputs and sufficient information, proceed with slice planning. If not, request required information from the Project Manager.

Note: This is a design and planning task, not a coding task.
```

```markdown
##### Architectural Component Design (Phase 3.5)
*Use this to design a high-level architectural component or initiative that will span multiple slices*

```markdown
We're designing a new architectural component for project {project}: {component-name}. Architectural components represent major structural changes or new subsystems that will likely result in multiple slices and many tasks. This is distinct from individual slices—it's about the foundational architecture that slices will build upon.

Create a design document for the architectural component.

Create file at `user/architecture/nnn-arch.{component-name}.md`, where nnn is the next available base index at an increment of 10 in the 100-799 initiative working range as defined in `file-naming-conventions.md`. This base index will be shared by the slice plan and slice designs derived from this architecture document (e.g., if this document is `120-arch.{name}.md`, its slice plan will be `120-slices.{name}.md` and its first slice design will be `120-slice.{first-slice}.md`).

Note: Do not use the 050-099 range — that is reserved for project-level architecture (HLD). Initiative-level architecture documents use the working range.

Your role is Technical Fellow as described in the Process Guide. Keep this document at the architectural level—do not include task-level breakdown or detailed slice specifications.

**Document Structure**
The component design should include:

1. YAML Frontmatter
```
```yaml
---
docType: architecture
layer: project
project: {project}
archIndex: nnn
component: {component-name}
dateCreated: YYYYMMDD
dateUpdated: YYYYMMDD
status: in_progress
relatedSlices: []
riskLevel: low|medium|high
---
```
```markdown
2. Content Sections
**Overview**
- High-level description of the architectural component or initiative
- State the core problem it addresses and why it matters to the project
- Scope: Short paragraph on what this component encompasses
- Motivation: Brief explanation of why this architectural change/component is needed

**Design Goals**
- List primary design goals (max: ~5) for this component (outcomes-oriented, not implementation-specific)
- Format as bulleted list of short paragraphs with goal name and brief description

**Architectural Principles**
- Key principles that will guide the design of slices and tasks within this component
- These inform how work should be structured, not what work to do
- Format as bulleted list with principle name and brief description

**Current State**
Brief description of the current architecture or state that necessitates this design work
What constraints or problems does the current system have?

**Envisioned State**
How this component will function at completion
Focus on the role it plays in the larger system, not implementation details
Describe the architecture from a system perspective, not from user perspective

**Technical Considerations**
Key technical challenges, trade-offs, or decisions that will inform slice design
Format as bulleted list with consideration title and explanation
These are constraints/challenges to be addressed, not proposed solutions

**Anticipated Slices (optional)**
At a high level, what slices do we expect this component might decompose into?
This is exploratory—not a commitment or task list
Format as bulleted list with provisional slice concept and brief description
Include only if you have meaningful ideas about slice boundaries

**Related Work**
Reference to related slices, features, initiatives, or domain knowledge (if any exist)
Link to existing slice files, feature files, or framework guides
No direct references to individual tasks

3. Guidelines
- Keep it high-level: This document informs slice planning, not implementation. Do not include code, pseudo-code, or detailed API specifications.
- Focus on architecture: Describe structural decisions and principles, not individual features or user-facing behaviors.
- Avoid implementation detail: Do not prescribe how tasks will be organized or which technologies to use. That emerges during slice design.
- Link to context: Reference existing slices, features, or framework guides where relevant. Do not reference individual tasks.
- Be concrete about principles: Architectural principles should be clear enough to guide slice designers. Avoid vague statements.

**Expected Output**
* Concise architectural component design document in user/architecture/nnn-arch.{component-name}.md
* Create if it doesn't already exist. If file exists, edit existing file as described above.
* Include all required YAML frontmatter
* Preserve any Project Manager-provided context or requirements

Follow dependency management—identify what foundation work or other architectural components this initiative depends on or affects.

Avoid:
- Vague fluff about future performance testing or involved benchmarking unless specifically relevant
- Speculative risk items; include only if truly relevant
- Time estimates in any form
- Task-level breakdown (that's slice planning's job)
- Code examples unless absolutely essential to convey architectural meaning

If you need more information about the component requirements or architectural constraints, stop and request clarification from the Project Manager.

Note: This is a design and planning task, not a coding task. Any code samples should be minimal and limited to what is truly needed to convey architectural information.
```

##### Slice Design (Phase 4)
```markdown
We're working in our guide.ai-project.000-process, Phase 4: Slice Design (Low-Level Design). Create a detailed design for slice: {slice} in project {project} by following `guide.ai-project.004-slice-design`.

**Inputs** (two levels — use what applies):

*Strategic context* (provides the big-picture view of where this slice fits):
- Architecture document, HLD, or project spec — as identified by the Project Manager or referenced in the slice plan's parent document.

*Working input* (defines what this specific slice should accomplish — one of the following):
1. Slice plan entry from `user/project-guides/003-slices.{project}.md` (project-level)
2. Slice plan entry from `user/architecture/nnn-slices.{name}.md` (architecture-level)
3. Slice description provided directly with this request

If using a slice plan, it must contain an entry for this slice. If the strategic context document is not obvious, ask the Project Manager.

Create the slice design document at `user/slices/nnn-slice.{slice-name}.md`, where `nnn` shares the initiative's base index (for the first slice) or increments sequentially from it (for subsequent slices), per `file-naming-conventions.md`. Your role is Technical Fellow.

Include:
- YAML frontmatter as described below
- Detailed technical decisions for this slice
- Data flows and component interactions
- For migration/refactoring slices: migration plan (source/destination, consumer updates, behavior verification)
- UI mockups or API/tool specifications (if applicable)
- Cross-slice dependencies and interfaces
- Success criteria specific enough for task creation
- Only template sections that are relevant to this slice — omit sections that don't apply

Avoid:
- Time estimates in hours/days/etc. You may use a 1-5 relative effort scale.
- Extensive benchmarking tasks unless actually relevant to this effort.
- Extensive or speculative risk items. Include only if truly relevant.
- Any substantial code writing. This is a planning and process task.
- Filling in template sections with boilerplate just because they exist.

YAML Frontmatter:
---
docType: slice-design
slice: {slice-name}
project: {project}
parent: {path to the slice plan this slice comes from}
dependencies: [list-if-any]
interfaces: [list-of-slices-that-depend-on-this]
status: not started
dateCreated: YYYYMMDD
dateUpdated: YYYYMMDD
---

If framework or platform are specified, guide(s) for the framework(s) should be provided in `ai-project-guide/framework-guides/{framework}/introduction.md`. If tools are specified, guide for each tool should be available at `ai-project-guide/tool-guides/{tool}/introduction.md`.

Stop and request clarification if you need more information to complete the slice design. This is a design and process task — not a coding task! Any code present should be minimal, and should provide essential information.
```

##### Task Breakdown (Phase 5)
*This should be usable for Slice or Feature task breakdown.*

```markdown
We're working in our guide.ai-project.000-process, Phase 5: Slice Task Breakdown. Convert the design for {slice | feature} in project {project} into granular, actionable tasks.  Note that this request can be used for *slice* or *feature*, but only one will be applicable to a particular request.  

Your role is Senior AI. Use exactly one of the following as input:
1. The slice design document `user/slices/{slice}.md`.
2. The feature design document `user/features/{feature}.md`.

Create task file at `user/tasks/{sliceindex}-tasks.{slicename}.md` (where `{sliceindex}` matches the parent slice's index, preserving lineage per `file-naming-conventions.md`). 
Use `guide.ai-project.005-task-breakdown` for detailed guidance on this phase.

Include:
1. YAML front matter including slice name, project, LLD reference, dependencies, and current project state
2. Context summary section
3. Granular tasks following Phase 5 guidelines
4. Create separate sub-tasks for each similar component.
5. Organize so that tasks can be completed sequentially.
6. Use checklist format for all task files.

Avoid:
- Time estimates in hours/days/etc.  You may use a 1-5 relative effort scale.
- Extensive benchmarking tasks unless actually relevant to this effort.
- Extensive or speculative risk items.  Include only if truly relevant.

For each {tool} in use, consult knowledge in `ai-project-guide/tool-guides/{tool}/`. Follow all task creation guidelines from the Process Guide.

Each task must be completable by a junior AI with clear success criteria. If insufficient information is available, stop and request clarifying information.  Keep files to about 350 lines or less.  If considerably more space is needed modify files as detailed here.  Do not split a file if it's less than about 100 line overrun.
1. rename current file nnn-tasks.[task section name]-1.md
2. add new file nnn-tasks.[task-section-name]-2.md
3. ...etc...

Notes:
* This is a project planning task, not a coding task.  Code segments should be MINIMAL and kept to only what is necessary to convey information.
* Always use mathematical comparison when evaluating file length vs target size. Always compare vs actual number of lines in the file, not number of list items or checkboxes.
```

##### Task Breakdown - Explicit (Phase 5 - Extra)
*Use this when you have a detailed slice design especially one containing code that may have been iterated on in order to solve complex or subtle design problems.  This should be added to the regular task breakdown prompt.  Until that is properly supported by context-builder, we have duplicated the base task expansion prompt here.

```markdown
We're working in our guide.ai-project.000-process, Phase 5: Slice Task Breakdown. Convert the design for {slice | feature} in project {project} into granular, actionable tasks.  Note that this request can be used for *slice* or *feature*, but only one will be applicable to a particular request.

Your role is Senior AI. Use exactly one of the following as input:
1. The slice design document `user/slices/{slice}.md`.
2. The feature design document `user/features/{feature}.md`.

Create task file at `user/tasks/{sliceindex}-tasks.{slicename}.md` (where `{sliceindex}` matches the parent slice's index, preserving lineage per `file-naming-conventions.md`). 

Include:
1. YAML front matter including slice name, project, LLD reference, dependencies, and current project state
2. Context summary section
3. Granular tasks following Phase 5 guidelines
4. Create separate sub-tasks for each similar component.
5. Organize so that tasks can be completed sequentially.
6. Use checklist format for all task files.

Avoid:
- Time estimates in hours/days/etc.  You may use a 1-5 relative effort scale.
- Extensive benchmarking tasks unless actually relevant to this effort.
- Extensive or speculative risk items.  Include only if truly relevant.

For each {tool} in use, consult knowledge in `ai-project-guide/tool-guides/{tool}/`. Follow all task creation guidelines from the Process Guide.

Each task must be completable by a junior AI with clear success criteria. If insufficient information is available, stop and request clarifying information.  Keep files to about 350 lines or less.  If considerably more space is needed modify files as detailed here.  Do not split a file if it's less than about 100 line overrun.
1. rename current file nnn-tasks.[task section name]-1.md
2. add new file nnn-tasks.[task-section-name]-2.md
3. ...etc...

Notes:
* This is a project planning task, not a coding task.  Code segments should be MINIMAL and kept to only what is necessary to convey information.
* Always use mathematical comparison when evaluating file length vs target size. Always compare vs actual number of lines in the file, not number of list items or checkboxes.

##### Important Additional Information
Note that our slice design is intricate, detailed, and has been refined extensively in order to address complex and/or subtle issues.  The slice design contains code, and we *need* to use this code in our task planning.

As you are planning tasks, proceed *carefully* through the slice design, creating tasks to accomplish the design *exactly* as presented.  Once you complete the task breakdown, review it in light of the slice design to ensure that:
1. You completely addressed the design.  If there are similar items, for example numerous wrapper components, ensure that your tasks explicitly address creation of each one.  
2. You did not miss any details.  This is critical.  Do not "gloss over", simplify, or add workarounds to any coding sections of the design even though they may be difficult.
   
Note also that tasks may reference the relevant design document.  You do not need to replicate large pieces of the design document all over the task list.  Ensure that references are accurate.  Do not assume or guess anywhere in this task.

After creation of task list, you must review the entire list against the slice design to ensure that these requirements are met.
```

##### Slice Task Expansion (Phase 6)
```markdown
We're working in our guide.ai-project.000-process, Phase 6: Task Enhancement and Expansion. Enhance the tasks for slice {slice} in project {project} to improve the chances that our "junior" AI workers can complete assigned tasks on their own.  Only enhance tasks that can truly benefit from it.  Many tasks may already be described with sufficient detail.

Use `guide.ai-project.006-task-expansion` as your detailed guide for this phase. Work on the task file `user/tasks/{sliceindex}-tasks.{slicename}.md`.

Your role is Senior AI. For each task:
- If it would benefit from expansion or subdivision, enhance it.
- If it's already appropriate, output it verbatim.
- Ensure all tasks are accounted for.
  
Additionally:
- Make sure that you do NOT use this expansion as a way to write code in a design and planning phase.  Expanded tasks should not look like writing code for the the tasks.  You may spec out interfaces or use minimal code examples where truly useful.  Evaluate carefully before doing so.

After any expansion, review it against the original unexpanded task and ensure that your expansion is a detailed representation of the original task, not a reinterpretation or change of the original task.

Output results by updating the existing task file. Success: All tasks have been processed and either output as is, or enhanced and divided into further subtasks.

Note: This is a project planning task, not a coding task.
```

##### Task Implementation (Phase 7)
```markdown
We are working on {slice | feature} in project {project}, phase 7 of `ai-project-guide/project-guides/guide.ai-project.000-process`. 

Your job is to complete the tasks in the `user/tasks/{sliceindex}-tasks.{slicename}.md` file. Please work through the tasks, following the guidelines in our project guides, and using the relevant provided rules (`rules/`, `CLAUDE.md`, etc).  Your role is "Senior AI". 

Use exactly one of the following (only one match should exist):
- The slice design at `user/slices/{slice}.md`.
- The feature design at `user/features/{feature}.md`.

Always git commit at least once per task but ideally after every section of items containing a 'Success:' criteria.  For example, if a file contains Task 1.2, Task 1.2.1, commit after each task.  If 1.2.1 contains multiple checklists each with its own 'Success:' criteria, commit after any section containing Success.  STOP and confer with Project Manager after each task, unless directed otherwise 

Work carefully and sequentially through the tasks, ensuring that each task is verified complete before proceeding to the next.  You should write unit tests for code as you work through the task. Ensure that tests pass and task is complete before moving to the next.

If an attempted solution does not work or you find reason to try another approach, do not make more than three attempts without stopping and obtaining confirmation from Project Manager.

Be sure to check off tasks as they are completed.  If a parent file (ex: `003-slices.{project}.md`) contains checklist items, check off parent items after all child items are complete. If a `task-checker` tool|agent is available to you, use it.

Maintain the YAML frontmatter including:
- Status: not-started, in-progress, complete, not-applicable
- Date updated

Notes: 
- Use the task-checker to manage lists if it is available to you.
- Ignore case sensitivity in all file and directory names.
- Use the directory-structure and file-naming-conventions guides.
- If you are missing required information or referenced files, STOP and obtain
  from Project Manager (PM).
- Do not guess, assume, or proceed without required files.
```

##### Context Initialization
*Use this prompt when you need to switch models or refresh understanding in slice-based projects.*
```markdown
The following provides context on our current work in project {project}. 

We are using the slice-based methodology from `ai-project-guide/project-guides/guide.ai-project.000-process`. Current work context:
- Project: {project}
- Slice: {slice}
- Tasks: {task-file}
- Phase: {development-phase}
- if [slice] is provided it can be decomposed into [sliceindex]-slice.[slicename].md

Refer to the Resource Structure in `ai-project-guide/project-guides/guide.ai-project.000-process` for locations of resources. Key project documents:
- Project Documents: `project-documents/user/`. 
- Slice design: user/slices/{slice}.md
- Tasks file: user/tasks/{sliceindex}-tasks.{slicename}.md

Concentrate on the most granular level available (e.g. tasks if present), and use the higher-level files as reference only if needed. 
- Project HLD: user/architecture/050-arch.hld-{project}.md
*Note: legacy HLD location is: user/project-guide/050-hld.{project}.md*

If you were previously assigned a role, continue in that role. If not, assume role of Senior AI as defined in the Process Guide.  

If tasks file is already present, it should be your primary focus.  Slice design may be used to gain overview or as a source for generating tasks.  Once we have the tasks, we primarily work from those.

If given an instruction similar to "process and stand by", make sure you understand all instructions, what files or architecture components are involved, and alert Project Manager to any missing, incomplete, or vague information preventing you from accurately carrying out your instructions.  Wait for confirmation from Project Manager before proceeding further.  
```

##### Context Initialization - Monorepo
*This is the monorepo version of the context initialization prompt.  This creates some duplication but it is sufficient and direct. *
```markdown
The following provides context on our current work in project {project}. 

We are using the slice-based methodology from `ai-project-guide/project-guides/guide.ai-project.000-process`. Current work context:
- Project: {project}
- Slice: {slice}
- Tasks: {task-file}
- Phase: {development-phase}
- if [slice] is provided it can be decomposed into [sliceindex]-slice.[slicename].md

Refer to the Resource Structure in `ai-project-guide/project-guides/guide.ai-project.000-process` for locations of resources. Key project documents and locations:
- Project Documents: `project-artifacts/{project-type}/{project}` where project type == 'template' (only value in use 20251003), for example: `project-artifacts/template/react/`.  This is interpreted as the value of user/ wherever that is encountered.  For example if a prompt references: user/tasks/100-tasks.some-tasks, this would be interpreted as: project-artifacts/template/react/.  Alternately, it can be flattened on level to: project-artifacts/template-react/.  

- Slice design: user/slices/{slice}.md maps to: project-artifacts/{project-type}-{project}/slices/{slice}.md
- Tasks file: user/tasks/{sliceindex}-tasks.{slicename}.md --> synonym: {taskfile}, maps to: project-artifacts/{project-type}-{project}/tasks/{taskfile}.md

Refer to the Resource Structure in `ai-project-guide/project-guides/guide.ai-project.000-process` for locations of resources. Concentrate on the most granular level available (e.g. tasks if present), and use the higher-level files as reference only if needed.  Key project documents:
- High-level design: user/architecture/050-arch.hld-{project}.md
- Current slice design: user/slices/{slice}.md
- Tasks file: user/tasks/{sliceindex}-tasks.{slicename}.md
*Note: legacy HLD location is: user/project-guide/050-hld.{project}.md*

If you were previously assigned a role, continue in that role. If not, assume role of Senior AI as defined in the Process Guide.  

If tasks file is already present, it should be your primary focus.  Slice design may be used to gain overview or as a source for generating tasks.  Once we have the tasks, we primarily work from those.

If given an instruction similar to "process and stand by", make sure you understand all instructions, what files or architecture components are involved, and alert Project Manager to any missing, incomplete, or vague information preventing you from accurately carrying out your instructions.  Wait for confirmation from Project Manager before proceeding further.  
```
##### Tool Usage
```markdown
You will need to consult specific knowledge for 3rd party tools, libraries, or packages, which should be available to you in the `ai-project-guide/tool-guides/[tool]/` directory for our curated knowledge.  Follow these steps when working with these tools, libraries, or packages.  Use proactively.

1. Consult Overview: Start with the specific `AI Tool Overview [toolname].md` in the `ai-project-guide/tool-guides/[tool]` directory.
2. Locate Docs: Scan the Overview for references to more detailed documentation (like local API files under `/documentation`, reference notes, or official web links).
3. Search Docs: Search within those specific documentation sources first using `grep_search` or `codebase_search`.
4. Additional documentation.  If you have a documentation tool available (ex: context7 MCP) use it for additional information.  Always use it if available and no specific tool guide is provided.
5. Web Search Fallback: If the targeted search doesn't yield results, then search the web.
```

##### Feature Design
*Use this to design a feature.  Features are horizontal sections that extend or modify slices.  They are for work that is too large or complex to be described with only a task or few, but that does not represent a vertical slice of functionality.*

```markdown
We're adding a new feature to project {project}, modifying slice {slice}. Features are horizontal sections that extend or modify slices.  They are for work that is too large or complex to be described with only a task or few, but that does not represent a vertical slice of functionality.  Create a design for the feature.  

Create or modify file at features/{sliceindex}-feature.{featurename}.md, where we refer to {sliceindex}-feature.{featurename} as the compound term {feature}. Note that an existing associated slice is required in order to create a feature. The {featurename} value should be provided by Project Manager or clearly contained in existing context.

Any needed high-level design (HLD) can be provided in an ## HLD section in the document.  Place detailed design in an ## LLD section in the document.  Keep it concise and minimal.  Use relevant methodology from `guide.ai-project.000-process` to create the design for the feature.  Your role is Technical Fellow.

The feature description should be provided by the Project Manager. Ideally it will be provided under a ## User-Provided Concept or similar heading in a feature file for you.  DO NOT overwrite any User-Provided (or PM-Provided) concept.  Preserve this information when you edit or re-create the file.

Expected Output:
* Concise feature design document in features/{sliceindex}-feature.{featurename}.md.  Create if it doesn't already exist.  If file exists, edit existing file as described above.

Add YAML FrontMatter to the relevant file if it is not present:
```yaml
---
item: {featurename}
project: {project}
type: feature
github: {url of github issue, if one is related}
dependencies: [list-if-any]
projectState: brief current state
status: not started
dateCreated: YYYYMMDD
dateUpdated: YYYYMMDD
---
```
``` markdown
Follow dependency management - identify what foundation work project elements may depend on or be affected by this change.

Guidelines:
1. Stick to relevant information only.  
2. Follow Phase 4 guidelines substituting 'feature' for 'slice' as needed.

Avoid:
1. Vague fluff about future performance testing or involved benchmarking, unless this is specifically relevant.  
2. Avoid vague or speculative Risk Items.
3. Do not add a time estimate in minutes/hours/days etc.  You may use 1-5 relative effort scale.

If you need more information about the feature requirements, stop and request from Project Manager.  Note that this is a project and process task, NOT a coding task.  Any code samples should be minimal and limited to what is truly needed to provide the information.
```


##### Ad-Hoc Tasks
```markdown
Create tasks for {feature|bugfix|maintenance-work} in project {project}. This is for smaller work items that need task breakdown but don't require full slice design.

Your role is Senior AI. Analyze the work item and create a task file at `user/tasks/nnn-tasks.{item-name}.md` with:

1. YAML front matter:
---
item: {item-name}
project: {project}
type: feature|maintenance|bugfix
dependencies: [list-if-any]
projectState: brief current state
dateCreated: YYYYMMDD
dateUpdated: YYYYMMDD
---

2. Context summary explaining the work
3. Granular tasks following Phase 5 guidelines

Skip LLD creation - go directly from description to implementable tasks. Each task should be completable by a junior AI with clear success criteria.

If the item is too complex for this approach, recommend creating a design file instead. If you need more information about the requirements, stop and request from Project Manager.  Keep tasks focused and atomic.
```

##### Summarize Context
*Use when nearing context limit, e.g. when facing imminent auto-compaction in Claude Code.  Make sure to include inside `[ ]` or Claude will ignore the instructions.  Currently it appears that at best Claude will output the `[ ]` information into the new context.*
```markdown
Perform the following items and add their output to the compacted context:
* Preserve the initial context describing what we are working on.
* Summarize current project state at time of this compaction.
* Include any open todo list items and work in progress.
* add the tag --COMPACTED-- after inserting this information. 
```

##### Session State Summary
*Use at the end of any work session — whether a slice is complete, partially complete, or work was interrupted. Produces a DEVLOG entry that enables project resumption by a human or AI in a new session. This is distinct from Summarize Context (above), which preserves state for in-session compaction.*
```markdown
Write a Session State Summary for project {project}. Append to DEVLOG.md in the project root.  Add entry under today's date heading (## YYYYMMDD). If an entry for today already exists, append above it under a new subsection, preserving the reverse chronological order both overall, and within the entries themselves.

Your role is Senior AI.

**If a slice was completed:**
###### Slice nnn: {Slice Name} — Complete
Include:
- Commits made during this slice (short hash + one-line description, table or list)
- What works: build status, test results, verified functionality
- What's pending: manual verification, known issues, deferred items
- Issues logged to maintenance (file reference + brief description)
- Key implementation decisions or surprises worth noting for future context
- Next: the next slice or work item to pick up

**If work is in progress (mid-slice or mid-task):**
###### Slice nnn: {Slice Name} — In Progress
Include:
- Current task and subtask (reference the task file and specific item)
- What's been completed so far in this session
- Commits made during this session (if any)
- Blockers or open questions for Project Manager
- Key decisions made during the session
- State needed to resume: which task, what file, any important context

**If design or planning work was completed (no implementation):**
###### Slice nnn: {Slice Name} — Design Complete
Include:
- Documents created or updated (file paths)
- Key design decisions and rationale
- Scope summary (what the design covers)
- Notable findings (broken imports, gaps discovered, deferred items)
- Next: what implementation or planning step follows

**Guidelines:**
- Keep it concise — this will be used as input for context assembly on the next session
- Do not include full code listings or verbose explanations
- Focus on: state, decisions, and continuation context
- If tests are relevant, include pass/fail counts and note any failures with brief descriptions
- Reference file paths for any issues logged to maintenance or other task files
- This is a documentation task, not a coding task

**DEVLOG.md format:**
If DEVLOG.md does not exist, create it at project-root directory with the following structure:

# Development Log

A lightweight, append-only record of development activity. Newest entries first.
Format: `## YYYYMMDD` followed by brief notes (1-3 lines per session).
---

## YYYYMMDD
### Slice nnn: {Slice Name} — {Status}
- {concise session notes as described above}
```

##### Maintenance Task
```markdown
Operate as a Senior AI. Use the issue description provided, and add tasks to the maintenance file to address implementation of the issue or feature. Add a new task to your maintenance file, which should be `tasks/950-tasks.maintenance.md` unless there is reason to deviate (there normally isn't). This should be used for an item small enough to represent as a single main task.

Include:
1. A new Task {n}
2. A very brief overview of the task (you may modify if already present).
3. Granular but concise subtasks following Phase 5 guidelines
4. Organize so that subtasks can be completed sequentially.
5. Optimize for early vertical slice testability.
6. Use checklist format for all tasks.

Avoid:
- Time estimates for subtasks.  If work is that complex, this is wrong format.
- Benchmarking tasks unless actually relevant to this effort.
- Risk items.  Include only if truly relevant.  Be skeptical here.

For each {tool} in use, consult knowledge in `ai-project-guide/tool-guides/{tool}/`. Follow all task creation guidelines from the Process Guide.

Each task must be completable by a junior AI with clear success criteria. If insufficient information is available, stop and request clarifying information.

This is a project planning task, not a coding task.
```

##### Perform Routine Maintenance 
```markdown
We are performing routine maintenance by implementing solutions for incomplete tasks in the maintenance task file. Unless otherwise specified, use file `tasks/950-tasks.maintenance.md` and scan for incomplete tasks. If given a particular section heading in the file, consider only that section.

Work through maintenance items one at a time. For each item:
- Determine if task can reasonably be solved without expansion or creating more detailed tasks.  Keep a list of anything requiring this additional detail and present it to the Project Manager after proceeding through all solvable items.
- Implement solutions according to our project guidelines.  Ensure that you create unit tests for each solution, and that the tests pass before proceeding to the next item.  Create tests as you work through each item -- do not wait until the end and try to create them all.
- Run regressions and existing tests to make sure maintenance fixes do not break any existing slices, slice boundaries, dependencies, or interfaces.
- Update tasks and check off as you go.  Use a task-checker agent if one is configured.

Current project: {project}
Active slice work: {slice} (if applicable)
```

##### Analysis Processing
```markdown
We need to process the artifacts from our recent code analysis.

Role: Senior AI, processing analysis results into actionable items
Context: Analysis has been completed on {project} (optionally {subproject}) and findings need to be converted into proper maintenance tasks, code review issues, or GitHub issues as appropriate.

Notes: 
- Be sure to know the current date first.  Do not assume dates based on training 
  data timeframes.

Process:
1. Categorize Findings:
- P0 Critical: Data loss, security vulnerabilities, system failures
- P1 High: Performance issues, major technical debt, broken features
- P2 Medium: Code quality, maintainability, best practices
- P3 Low: Optimizations, nice-to-have improvements

2. Create File and Document by Priority:
- Create markdown file `analysis/nnn-analysis.{project-name}{.subproject?}.md`
  where nnn starts at 940 (analysis range).
- Note that subproject is often not specified. Do not add its term to the name
  if this is the case.
- Divide file into Critical Issues (P0/P1) and Additional Issues(P2/P3)
- Add concise documentation of each issue -- overview, context, conditions.  

3. File Creation Rules:
- Use existing file naming conventions from `file-naming-conventions.md`
- Include YAML front matter for all created files
- Add the correct date (YYYYMMDD) in the file's frontmatter
- Reference source analysis document (if applicable)
- Add line numbers and specific locations where applicable

4. GitHub Integration (if available):
- Create GitHub issues for P0/P1 items
- Label appropriately: `bug`, `critical`, `technical-debt`, `analysis`
- Reference analysis document in issue description
- Include reproduction steps and success criteria
```

##### Analysis Task Creation

*Create tasks based on codebase analysis.  While we don't yet have a generic analysis prompt, we do have the following modified task-creation prompt for use with analysis results.*
```markdown
We're working in our guide.ai-project.000-process, Phase 5: Slice Task Breakdown. Convert the issues from {analysis-file} into granular, actionable tasks if they are not already.  Keep them in priority order (P0/P1/P2/P3). 

If the tasks are already sufficiently granular and in checklist format, you do not need to modify them. Note that each success criteria needs a checkbox.

Your role is Senior AI. Use the specified analysis document `user/analysis/nnn-analysis.{project-name}{.subproject?}.md` as input. Note that subproject is optional (hence the ?). Avoid adding extra `.` characters to filename if subproject is not present.

Create task file at `user/tasks/nnn-analysis{.subproject?}-{date}.md` with:
1. YAML front matter including slice or subproject name, project, YYYYMMDD date, main analysis file reference, dependencies, and current project state
2. Context summary section
3. Granular tasks following Phase 5 guidelines
4. Keep success criteria with their respective task
5. Always use checklist format described in guide.ai-project.000-process under Task Files.

For each {tool} in use, consult knowledge in `ai-project-guide/tool-guides/{tool}/`. Follow all task creation guidelines from the Process Guide.

Each task must be completable by a junior AI with clear success criteria. If insufficient information is available, stop and request clarifying information.

This is a project planning task, not a coding task.
```

##### Analysis to LLD
```markdown
We need to create a Low-Level Design (LLD) for {feature/component} identified during codebase analysis or task planning in project {project}.  It may be an expansion of an initial task section identified during analysis.

Your role is Technical Fellow as described in the Process Guide. This LLD will bridge the gap between high-level understanding and implementable tasks.

Context:
- Analysis document: `user/analysis/nnn-analysis.{project-name}{.subproject or analysis topic?}` (or specify location)
- Related task file: `user/tasks/nnn-analysis{.subproject?}-{date}.md` (if exists)
- Current issue: {brief description of what analysis revealed}

Create LLD document at: `user/features/nnn-lld.{feature-name}.md`

Required YAML front matter:
```yaml
---
layer: project
docType: lld
feature: {featurename}
project: {project}
triggeredBy: analysis|task-breakdown|architecture-review
sourceDocument: {path-to-analysis-or-task-file}
dependencies: [list-any-prerequisites]
affects: [list-components-or-slices-impacted]
complexity: low|medium|high
dateCreated: YYYYMMDD
dateUpdated: YYYYMMDD
---

Guidelines for creating LLD:

Cross-Reference Requirements:

- Update source analysis/task document to reference this LLD
- Add back-reference in this LLD to triggering document
- Note any slice designs or existing features this affects

Focus Areas:

- Keep design concrete and implementation-ready
- Include code examples or pseudocode where helpful
- Reference specific files, classes, or components by name
- Address both immediate needs and future extensibility

If you need more context about the analysis findings or existing system architecture, stop and request from Project Manager.

Note: This creates implementation-ready technical designs, not high-level planning documents.
```

##### Analysis Task Implementation
*Phase 7 Task Implementation customized for analysis files. *
```markdown
We are working on the analysis file {analysis} in project {project}, phase 7 of `ai-project-guide/project-guides/guide.ai-project.000-process`. 

Your role is "Senior AI". Your job is to complete the tasks in the `user/tasks/nnn-analysis-{topic}.md` file. Please work through the tasks, following the guidelines in our project guides, and using the rules in the rules/ directory.

The analysis overview is available at {analysis} for additional context.

STOP and confer with Project Manager after each task, unless directed otherwise by the Project Manager. Do not update any progress files until confirmation from Project Manager.

Work carefully and ensure that each task is verified complete before proceeding to the next. If an attempted solution does not work or you find reason to try another approach, do not make more than three attempts without stopping and obtaining confirmation from Project Manager.

Check off completed tasks in the task file when verified complete. When all tasks for the slice are complete, proceed to Phase 8 (integration) with Project Manager approval.

Notes: 
* Use the task-checker to manage lists if it is available to you
* Ignore case sensitivity in all file and directory names
* If you cannot locate referenced files, STOP and request information from Project Manager
* Do not guess, assume, or proceed without required files.
```

##### Analyze Codebase
*This is mostly specialized to front-end and web apps and should be moved to a specific guide.*
```markdown
Purpose: Perform discovery analysis of existing codebase to:
- Document system architecture and technology stack
- Identify technical debt and improvement opportunities
- Provide foundation for creating slices, features, or maintenance tasks
- Create reference documentation for team members

This is reconnaissance work - not goal-oriented development.

Analyze the following existing codebase and document your findings. We want this to not only assist ourselves in updating and maintaining the codebase, but also to assist humans who may be working on the project.

###### Expected Output
* Document your findings in `user/analysis/nnn-analysis.{topic}.md` where:
  - nnn starts at 940 (analysis range)
  - {topic} describes the analysis focus (e.g., "initial-codebase", "dependency-audit", "architecture-review")
* Write in markdown format, following our rules for markdown output.  

###### General Guidelines
* Document the codebase structure.  Also note presence of any project-documents or similar folders which probably contain information for us.
* Document presence or average of tests, and an estimate of coverage if tests are present.
* Identify technologies and frameworks in use.  
* What package managers are in use?
* Is there a DevOps pipeline indicated?
* Analysis should be concise and relevant - no pontificating.
* Add note in README as follows: Claude: please find code analysis details in {file mentioned above}.

###### Front End
* If this is a JS app, does it use React?  Vue?  Is it NextJS?  Is it typescript, javascript, or both?  Does it use TailWind?  ShadCN?  Something else?

###### NextJS, React
* Perform standard analysis and identify basic environment -- confirm NextJS, identify common packages in use (Tailwind, ShadCN, etc) and any unusual packages or features.  
* If auth is present, attempt to determine its structure and describe its methodology
* Is the project containerized?
* If special scripts (ex: 'docker: {command}') are present, document them in the README.
* Provide a description of the UI style, interactivity, etc
* Document page structure.
* What type of architecture is used to manage SSR vs CSR?
  
###### Tailwind
* Is cn used instead of string operations with parameterized or variable   classNames?
* Prefer Tailwind classes, there should not be custom CSS classes.
* If this is Tailwind 4, are customizations correctly in CSS and no attempt to use tailwind.config.ts/.js.

```

##### Custom Instruction
*Used as a placeholder by context-builder app*
```markdown
Custom instructions apply.  See Additional Context for instruction prompt.
```

***
### Experimental
*Less than no guarantees here.  Generally promoted to active, or deprecated.*

***
### Deprecated 



