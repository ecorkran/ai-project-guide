---
layer: snippet
docType: template
purpose: reusable-llm-prompts
audience:
  - human
  - ai
ai description: Parameterized prompt library mapped to slice-based project phases.
dependsOn:
  - guide.ai-project.process.md
npmScriptsAiSupport: "!include ../snippets/npm-scripts.ai-support.json"
dateCreated: 20250724
dateUpdated: 20260324
---
## Prompts
This document contains prepared prompts useful in applying the `guide.ai-project.process` and performing additional supplemental tasks.

### Context Profiles
Maps prompt templates to their required context documents.
Variables not listed are excluded from context assembly.
Order: concept → hld → arch → plan → slice → tasks.  Note that not all inputs may be or are required to be present if work can proceed without them.  This table is an interim solution before we split the monolithic prompt file, which should happen soon.
```yaml
context_profiles:
  concept-phase-0:                   []
  initiative-plan-phase-1:           [fileConcept]
  architecture-phase-2:              [fileConcept, fileArch]
  slice-planning-phase-3:            [fileArch, fileSlicePlan]
  slice-design-phase-4:              [fileSlicePlan, fileSlice]
  task-breakdown-phase-5:            [fileSlice, fileTasks]
  implementation-phase-6:            [fileSlice, fileTasks]
  slice-integration-phase-7:         [fileArch, fileSlicePlan, fileSlice, fileTasks]
  context-initialization:            []
  maintenance-task:                  [fileTasks]
  maintenance-routine:               [fileSlice, fileTasks]
  analysis-processing:               [fileSlice, fileTasks]
  analysis-task-creation:            [fileTasks]
  analysis-to-lld:                   [fileSlice]
  analysis-task-implementation:      [fileSlice, fileTasks]
  analyze-codebase:                  []
  custom-instruction:                []
  _default:                          [fileArch, fileSlicePlan, fileSlice, fileTasks]
```

##### Concept (Phase 0)
```markdown
We're starting work on a new project {project}. We will use our curated AI Project Creation methods in `guide.ai-project.process` (can also be referred to as Project Guide or Process Guide) to assist us in designing and performing the work. Your role as described in the Project Guide is Architect.

Our goal is to collaboratively create the concept document. The Project Manager will describe the project — usually conversationally, though they may also provide a starter document in `user/project-guides/001-concept.{project}.md`. Either approach works; follow the PM's lead.

Through conversation, refine the PM's vision into a concept document following the Living Document Pattern and the structure described in `guide.ai-project.000-concept`. The PM's original concept is preserved in the User-Provided Concept section; structured technical analysis goes into the Refined Concept section.

We will use the completed concept as a basis for the initiative plan and subsequent design work — decomposing the project into initiatives, then breaking each into architectural components, slice plans, and tasks.

If the project involves multiple capability areas or components, identify them in the Solution Approach section. These are not yet initiatives with indices — just the named pieces that Phase 1 (Initiative Plan) will later formalize.

When creating the concept, *ask questions* if any information is missing or unclear. The guideline of do not assume or guess applies, but is even more important here at this early concept stage where misunderstandings compound through later phases. Request any needed clarifications from the Project Manager.
```

##### Initiative Plan (Phase 1)
```markdown
We're working on project {project}, Phase 1: Initiative Plan. Use `guide.ai-project.001-initiative-plan` for detailed guidance on this phase.

Your role is Architect, working with the Project Manager to decompose the project concept into named initiatives.

**Input**: Concept document at `user/project-guides/001-concept.{project}.md`. Review the Solution Approach section for identified capability areas.

**Output**: Initiative plan at `user/project-guides/001-initiative-plan.{project}.md`.

Work with the Project Manager to:

1. Identify initiatives from the concept's capability areas. Each initiative represents a cohesive body of work that will produce an architecture document and slice plan.
2. Assign base indices from the 100-799 working range. Discuss index gap with PM:
   - Default gap of 20 (100, 120, 140) works for most projects
   - Broad initiatives may use wider gaps (50, 100, or 200)
   - Record the convention in the plan
3. Declare cross-initiative dependencies — which initiatives need stable interfaces from others before architecture design can begin.
4. List initiatives in checklist format matching slice plan convention:
   `1. [ ] **(nnn) {Initiative Name}** — {scope}. Dependencies: {list}. Status: not_started`

This is a collaborative, strategic task. Ask questions about scope boundaries, sequencing priorities, and dependency assumptions. Do not make unilateral decisions about initiative decomposition.

Small projects with a single capability area may have only one initiative — that's fine. Not every project needs many initiatives.

Include YAML frontmatter per `guide.ai-project.001-initiative-plan`.

Note: This is a planning task, not a coding task.
```

##### Architecture (Phase 2)
*Use this to design a high-level architectural component or initiative that will span multiple slices. This is the most common entry point for work on existing projects.*

```markdown
**Before proceeding with document creation, confirm you have a clear component definition:**
- The component must be explicitly specified by the PM (via `arch` field, Additional Instructions, or conversation)
- A worktree name is NOT a component specification — it only tells you where files go
- If you only have a worktree name and a concept document, STOP and ask the PM what component to design
- If Additional Instructions describe the component, confirm your understanding with the PM before writing

We're designing a new architectural component for project {project}. Architectural components represent major structural elements or new subsystems that will likely result in multiple slices and many tasks. This is distinct from individual slices — it's about the foundational architecture that slices will build upon.

All projects will have at least one architectural component. A small project may have only one, and will directly reference the concept document to create its architectural component. In most projects, the project manager will describe the concept being designed in the architectural component.

{{#if worktreeName}}
**Worktree context (file location only — this does NOT define the component):**
You are working in the `{{worktreeName}}` worktree (index range {{worktreeRange}}).
- Base index for this component's architecture document: {{worktreeIndexStart}}
- Architecture file naming: `{{worktreeIndexStart}}-arch.<component-name>.md`
- Current arch doc: `{{arch}}` (empty means not set — STOP and ask project manager for additional details)

**Component definition check:** If the component is not clearly defined in the `arch` field above or in Additional Instructions below, stop here and confirm the goal with the Project Manager. Do not infer a component from the worktree name, concept document, or other contextual clues.
{{else}}
**Before proceeding, determine the component name and base index:**
1. If the project's `fileArch` is already set, use that component name and index.
2. If Additional Instructions below describe the component, derive the name from that description.
3. Otherwise, **stop and ask the Project Manager** what architectural component they want to create. Do not proceed with placeholder names.

**To determine the base index:**
- Scan `user/architecture/` for existing `nnn-arch.*.md` files to find the highest index in use.
- The next available index is the next multiple of 10 (e.g., if `200-arch.*.md` exists, use `210`).
- Valid range: 100–799 (initiative working range per `file-naming-conventions.md`).
- Do not use 050–099 — that is reserved for project-level architecture (HLD).

This base index will be shared by the slice plan and slice designs derived from this architecture document (e.g., if this document is `120-arch.name.md`, its slice plan will be `120-slices.name.md` and its first slice design will be `121-slice.first-slice.md`).
{{/if}}

Create the design document for the architectural component.

Your role is Architect as described in the Process Guide. Keep this document at the architectural level—do not include task-level breakdown or detailed slice specifications.

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
component: component-name
relatedSlices: []
riskLevel: low|medium|high
dateCreated: YYYYMMDD
dateUpdated: YYYYMMDD
status: not_started
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
Reference to related slices, initiatives, or domain knowledge (if any exist)
Link to existing architectural component, files, slice files, or framework guides
No direct references to individual tasks

3. Guidelines
- Keep it high-level: This document informs slice planning, not implementation. Do not include code, pseudo-code, or detailed API specifications.
- Focus on architecture: Describe structural decisions and principles, not individual user-facing behaviors.
- Avoid implementation detail: Do not prescribe how tasks will be organized or which technologies to use. That emerges during slice design.
- Link to context: Reference existing slices or framework guides where relevant. Do not reference individual tasks.
- Be concrete about principles: Architectural principles should be clear enough to guide slice designers. Avoid vague statements.

**Expected Output**
* Concise architectural component design document in `user/architecture/nnn-arch.component-name.md`
* Create if it doesn't already exist. If file exists, edit existing file as described above.
* Include all required YAML frontmatter
* Preserve any Project Manager-provided context or requirements
* Register the document: `cf set arch <nnn>` (e.g., `cf set arch 120`)

Follow dependency management—identify what foundation work or other architectural components this initiative depends on or affects.

Avoid:
- Vague fluff about future performance testing or involved benchmarking unless specifically relevant
- Speculative risk items; include only if truly relevant
- Time estimates in any form
- Task-level breakdown (that's slice planning's job)
- Code examples unless absolutely essential to convey architectural meaning

Note: This is a design and planning task, not a coding task. Any code samples should be minimal and limited to what is truly needed to convey architectural information.
```

##### Slice Planning (Phase 3)
```markdown
We're working in our guide.ai-project.process, Phase 3: Slice Planning. Use `guide.ai-project.003-slice-planning` to break the work described in the parent document into manageable vertical slices.

**Parent document** 
1. Architecture document (`user/architecture/nnn-arch.{name}.md`) — for architecture-level planning

Your role is Architect as described in the Process Guide. Work with the Project Manager to:

1. Identify the planning context (architecture-level) per the guide
2. Identify foundation work, functional slices, migration/refactoring slices, and integration work as applicable
3. Create the slice plan document in the correct location:
   `user/architecture/nnn-slices.{name}.md` (sharing the parent architecture document's base index, per `file-naming-conventions.md`)
4. When numbering slices, you may use an index starting with 1, but continue the same index throughout the document.  Do not restart the numbering within the plan.
5. When naming slices in the slice plan, avoid use of ampersand or other special characters not commonly accepted in filenames.  - and space are fine.  Include a tentative slice number starting with the sliceplan index.  Example:  1. [ ] **(100) MCP Server Scaffolding** - {remainder of entry}
6. Include YAML frontmatter with `status: not_started` (update to `in_progress` or `complete` as slices progress). 

**Example YAML FrontMatter**:
```yaml
---
docType: slice-plan
parent: user/architecture/140-arch.context-forge-restructure.md
project: context-forge
dateCreated: 20260214
dateUpdated: 20260217
status: not_started
---
```

```markdown
Use enough slices to completely define the scope of the parent document. Consider functional requirements only. Ignore non-functional requirements. Avoid speculative risk projections. Do not include calendar or time-based estimates.

When defining slices, focus on slice independence and clear value delivery (user value, developer value, or architectural enablement). Each slice must leave the system in a working state when complete. If you have all required inputs and sufficient information, proceed with slice planning. If not, request required information from the Project Manager.

Note: This is a design and planning task, not a coding task.
```

##### Slice Design (Phase 4)
```markdown
We're working in our guide.ai-project.process, Phase 4: Slice Design (Low-Level Design). Create a detailed design for slice: {slice} in project {project} by following `guide.ai-project.004-slice-design`.

**Inputs** (two levels — use what applies):

*Strategic context* (provides the big-picture view of where this slice fits):
- Architecture document or HLD — as identified by the Project Manager or referenced in the slice plan's parent document.

*Working input* (defines what this specific slice should accomplish:
1. Slice plan entry from `user/architecture/nnn-slices.{name}.md`
2. Slice description provided directly with this request

If using a slice plan, it must contain an entry for this slice. If the strategic context document is not obvious, ask the Project Manager.

Create the slice design document at `user/slices/nnn-slice.{slice-name}.md`, where `nnn` shares the initiative's base index (for the first slice) or increments sequentially from it (for subsequent slices), per `file-naming-conventions.md`. 

When creating a slice design for a slice plan entry, update its entry to include the materialized `nnn` index.  
Example:
Creating slice 175 for slice plan entry 11:
pre:  11 [ ] **Our Slice Title** {slice plan entry text}
post: 11 [ ] **(175) Our Slice Title** {slice plan entry text}

Your role is Architect.

Include:
- YAML frontmatter as described below.  Ensure that status field is present.
- Detailed technical decisions for this slice
- Data flows and component interactions
- For migration/refactoring slices: migration plan (source/destination, consumer updates, behavior verification)
- UI mockups or API/tool specifications (if applicable)
- Cross-slice dependencies and interfaces
- Success criteria specific enough for task creation
- Verification walkthrough: concrete commands, workflows, and step-by-step confirmation that the user can follow to prove the slice delivers what it claims. This is not a restatement of success criteria — it's the "demo script" showing what the user can actually do.  This is the draft walkthrough that will be refined when Phase 6 (Implementation) is complete.
- Only template sections that are relevant to this slice — omit sections that don't apply

Avoid:
- Time estimates in hours/days/etc. You may use a 1-5 relative effort scale.
- Extensive benchmarking tasks unless actually relevant to this effort.
- Extensive or speculative risk items. Include only if truly relevant.
- Any substantial code writing. This is a planning and process task.
- Filling in template sections with boilerplate just because they exist.

YAML Frontmatter:
```
```yaml
---
docType: slice-design
slice: {slice-name}
project: {project}
parent: {path to the slice plan this slice comes from}
dependencies: [list-if-any]
interfaces: [list-of-slices-that-depend-on-this]
dateCreated: YYYYMMDD
dateUpdated: YYYYMMDD
status: not_started
---
```
```markdown
If framework or platform are specified, guide(s) for the framework(s) should be provided in `ai-project-guide/framework-guides/{framework}/introduction.md`. If tools are specified, guide for each tool should be available at `ai-project-guide/tool-guides/{tool}/introduction.md`.

Stop and request clarification if you need more information to complete the slice design. This is a design and process task — not a coding task! Any code present should be minimal, and should provide essential information.
```

##### Task Breakdown (Phase 5)
```markdown
We're working in our guide.ai-project.process, Phase 5: Slice Task Breakdown. Convert the design for {slice} in project {project} into granular, actionable tasks.  

Your role is Senior AI. Use the following as input:
- The slice design document `user/slices/{slice}.md`.

Create task file at `user/tasks/{sliceindex}-tasks.{slicename}.md` (where `{sliceindex}` matches the parent slice's index, preserving lineage per `file-naming-conventions.md`). 
Use `guide.ai-project.005-task-breakdown` for detailed guidance on this phase.

Include:
1. YAML front matter including slice name, project, LLD reference, dependencies, current project state, and status: not_started
2. Context summary section
3. Granular tasks following Phase 5 guidelines
4. Create separate sub-tasks for each similar component.
5. Organize so that tasks can be completed sequentially.
6. Test-with pattern: place test tasks immediately after their corresponding implementation tasks, not batched at the end. Each feature or component task should be followed by its test task before moving to the next feature.
7. Use checklist format for all task files.

Avoid:
- Time estimates in hours/days/etc.  You may use a 1-5 relative effort scale.
- Extensive benchmarking tasks unless actually relevant to this effort.
- Extensive or speculative risk items.  Include only if truly relevant.

For each {tool} in use, consult knowledge in `ai-project-guide/tool-guides/{tool}/`. Follow all task creation guidelines from the Process Guide.

Each task must be completable by a junior AI with clear success criteria. If insufficient information is available, stop and request clarifying information.  Keep files to about 450 lines or less.  If considerably more space is needed modify files as detailed here.  Do not split a file if it's less than about 100 line overrun.
1. rename current file nnn-tasks.[task section name]-1.md
2. add new file nnn-tasks.[task-section-name]-2.md
3. ...etc...

Notes:
* This is a project planning task, not a coding task.  Code segments should be MINIMAL and kept to only what is necessary to convey information.
* Always use mathematical comparison when evaluating file length vs target size. Always compare vs actual number of lines in the file, not number of list items or checkboxes.
```

##### Implementation (Phase 6)
```markdown
We are working on {slice} in project {project}, phase 6 of `ai-project-guide/project-guides/guide.ai-project.process`. 

Your job is to complete the tasks in the `user/tasks/{sliceindex}-tasks.{slicename}.md` file. Please work through the tasks, following the guidelines in our project guides, and using the relevant provided rules (`rules/`, `CLAUDE.md`, etc).  Your role is "Senior AI". 

Use the following as overview input when needed.  Primary input is the task file referenced above.
- The slice design at `user/slices/{slice}.md`.

Commit at each checkpoint marked in the task file (look for lines starting with `**Commit**:`). Use the commit message provided. If a task has no explicit commit marker, commit at the end of the task before moving to the next.

Work carefully and sequentially through the tasks, ensuring that each task is verified complete before proceeding to the next.  You should write unit tests for code as you work through the task. Ensure that tests pass and task is complete before moving to the next.

If you encounter a failing test, an ambiguous requirement, or a design decision not covered by the slice design, stop and confer with the Project Manager. Do not make more than three attempts at a failing approach before stopping.

Be sure to check off tasks as they are completed.  If a parent slice plan file contains checklist items, check off parent items after all child items are complete. If a `task-checker` tool|agent is available to you, use it.

###### Completion
After completing all tasks, perform the following steps:
1. Run through the Verification Walkthrough section of the slice design as a final confirmation. If any step doesn't work as described, stop and confer with Project Manager before marking the slice complete. Update the Verification Walkthrough with actual commands, expected command output, corrections, and any caveats discovered during implementation.  The goal is for the walkthrough to be aditionally verifiable by an external agent (human or AI, as applicable).

2. Run workflow_check (preferred) or cf check, if either are available to you, and specify the 'fix' parameter to auto-fix any issues.

3. Maintain the YAML frontmatter including:
- status: not_started, in_progress, complete
- dateUpdated: today's date

4. Update CHANGELOG.md in project root
- if file does not exist, create it as described in project-guides/templates/changelog-format.md

###### Notes: 
- Use the task-checker to manage lists if it is available to you.
- Ignore case sensitivity in all file and directory names.
- Use the directory-structure and file-naming-conventions guides.
- If you are missing required information or referenced files, STOP and obtain
  from Project Manager (PM).
- Do not guess, assume, or proceed without required files.
```

##### Slice Integration (Phase 7)
We are completing slice integration (Phase 7) for {slice} in project {project}, as described in `ai-project-guide/project-guides/guide.ai-project.process`.

Your role is Senior AI.

**Integration Steps:**

1. **Merge and verify**
   - Ensure the slice branch is merged into the main development branch (if using branches)
   - Resolve any merge conflicts, preserving slice intent
   - Run full test suite — not just slice tests, but project-wide regressions
   - Verify build succeeds cleanly

2. **Interface verification**
   - Confirm that slice dependencies and interfaces work as expected with the integrated codebase
   - If this slice exposed new interfaces consumed by future slices, verify they are accessible and correctly typed
   - If this slice consumed interfaces from prior slices, confirm integration is clean

3. **Documentation update**
   - Update any project documentation affected by this slice (README, API docs, architecture docs)
   - If the slice introduced new patterns, conventions, or infrastructure, ensure they are documented
   - Skip if no documentation is affected — do not create documentation for its own sake

4. **Close out**
   - Check off the completed slice in the parent slice plan
   - Update the slice design document status to `complete`
   - Update the task file status to `complete`

**Notes:**
- If integration reveals issues that require non-trivial fixes, log them to maintenance (`tasks/950-tasks.maintenance.md`) rather than blocking integration
- This phase does not determine what to work on next — workflow navigation is handled by orchestration
- If you cannot verify integration (e.g., missing test infrastructure), note what was verified and what was not


##### Context Initialization
*Use this prompt when you need to switch models or refresh understanding in a project.*
```markdown
The following provides context on our current work in project {project}.

Refer to `ai-project-guide/project-guides/guide.ai-project.process` for resource structure and locations.

Concentrate on the most granular input available (i.e. tasks if present), and use the higher-level files as reference only if needed.

If you were previously assigned a role, continue in that role. If not, assume role of Senior AI as defined in the Process Guide.

If given an instruction similar to "process and stand by", make sure you understand all instructions, what files or architecture components are involved, and alert Project Manager to any missing, incomplete, or vague information preventing you from accurately carrying out your instructions.  Wait for confirmation from Project Manager before proceeding further.
```

##### Tool Usage
```markdown
You will need to consult specific knowledge for 3rd party tools, libraries, or packages, which should be available to you in the `ai-project-guide/tool-guides/[tool]/` directory for our curated knowledge.  Follow these steps when working with these tools, libraries, or packages.  Use proactively.

1. Consult Overview: Start with the specific `AI Tool Overview [toolname].md` in the `ai-project-guide/tool-guides/[tool]` directory.
2. Locate Docs: Scan the Overview for references to more detailed documentation (like local API files under `/documentation`, reference notes, or official web links).
3. Search Docs: Search within those specific documentation sources first using `grep_search` or `codebase_search`.
4. Additional documentation.  If you have a documentation tool available (ex: context7 MCP) use it for additional information.  Always use it if available and no specific tool guide is provided.
5. Web Search Fallback: If the targeted search doesn't yield results, then search the web.
```


##### Add Slice Overview
*Use to add a slice overview to an existing slice plan.  You should have architecture and slice plan documents associated in order to use this prompt.  If these documents are not present, inform the user or agent that required inputs are missing.*

###### Inputs & Role
* discovery tool: you should have access to a discovery tool, for example a get_status function or skill (/cf:status or similar).  Use this as needed to scan for required inputs and prompt user/agent if any are missing.
* architecture file (arch): associated architecture file
* slice plan file (plan): associated slice plan file
* Your role is Architect as described in the Process Guide.

###### Outputs:
* slice plan updated with overview on the new slice.  
* slice plan dateUpdated set to today's date in YYYYMMDD format.
* slice overview as described here.
* if this slice overview is a result of promoting an existing "Future Work" slice, delete the old future work entry. Knowing that it was previously future work is not a useful data point so we don't keep it.

###### Slice Overview in Slice Plan (required) 
Slices created here will normally go in the Feature Slices section of the slice plan.  Unless specifically instructed, add new slice to end of Feature Slices list

*Note: {tsi} in template below is {tentative-slice-index}.  Use the next available sequential index and tentative slice index.  Do not update index values for additional slices that follow unless asked to do so.*  

*Existing Feature Slices Form*
i. [ ] ** ({tsi}) {Slice Name}** — Brief description. Dependencies: [list]. Risk: Low/Med/High.  Effort: n/5

*Example with New Slice Added*
14. [ ] **(113) {Slice Name}** — Brief description. Dependencies: [list]. Risk: Low/Med/High. Effort: n/5
15. [ ] **(114) {New Slice Name}** — Brief description. Dependencies: [list]. Risk: Low/Med/High. Effort: n/5

## Integration Work
16. [ ] **(115) {Name}** — Brief description. Effort: n/5


##### Add Initiative Overview
*Use to add an initiative entry to an existing initiative plan.  You should have initiative plan document associated in order to use this prompt.  If not present, inform the user or agent that required inputs are missing.*

###### Inputs & Role
* discovery tool: you should have access to a discovery tool, for example a get_status function or skill (/cf:status or similar).  Use this as needed to scan for required inputs and prompt user/agent if any are missing.
* initiative plan file: the projecct's initiative plan file
* Your role is Architect as described in the Process Guide.

###### Outputs:
* initiative plan updated with overview on the new initiative.  
* initiative plan dateUpdated set to today's date in YYYYMMDD format.
* initiative entry as described here.
* if this initiative is a result of promoting an existing "Future Work" initiative, delete the old future work entry. Knowing that it was previously future work is not a useful data point so we don't keep it.

###### Initiative Entry in Initiative Plan (required) 
1. Unless otherwise instructed, add new entry to end of existing list, maintaining existing index gap interval used in ths file.
2. Update or add any relevant cross-initiative dependencies.
3. New initiative should be listed in checklist form, matching the format of existing entries in the file.


##### Session State Summary
*Use at the end of any work session — whether a slice is complete, partially complete, or work was interrupted. Produces a DEVLOG entry that enables project resumption by a human or AI in a new session. This is distinct from Summarize Context (above), which preserves state for in-session compaction.*
```markdown
Write a Session State Summary for project {project}. Append to DEVLOG.md in the project root under today's date heading (## YYYYMMDD). If an entry for today exists, append above it preserving reverse chronological order.

Your role is Senior AI.

**Entry heading:** `### Slice nnn: {Slice Name} — {Complete|In Progress|Design Complete}`

**Include (as applicable):**
- Commits made this session (short hash + one-line)
- What was completed or delivered (build status, test results, documents created)
- What's pending or blocking (open questions, manual verification, deferred items)
- Key decisions or surprises worth noting for future context
- If in progress: state needed to resume (current task, file, important context)
- Issues logged to maintenance (file reference + description)

**Guidelines:**
- Keep concise — this is input for next session's context assembly
- No full code listings, no "next steps" (orchestration handles that)

**Update DEVLOG.md**
- if file does not exist, create it as described in project-guides/templates/devlog-format.md
```

##### Maintenance Task
```markdown
Operate as a Senior AI. Use the issue description provided, and add tasks to the maintenance file to address implementation of the issue.  Use a maintenance task and slice file in the 950-999 range.  Add a concise description in the slist file and add a new task to the task file. Use an existing slice and task file in the maintenance range if present and the item is small enough to represent as a single main task.  Create new files if needed.

Example files:
`slices/950-slices.maintenance.md`
`tasks/950-tasks.maintenance.md`

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

##### Maintenance Routine
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


##### Custom Instruction
*Used as a placeholder by context-builder app*
```markdown
Custom instructions apply.  See Additional Context for instruction prompt.
```

***
### Experimental
*Less than no guarantees here.  Generally promoted to active, or deprecated.*



