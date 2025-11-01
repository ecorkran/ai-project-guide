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

##### Slice Planning (Phase 3)
```markdown
We're working in our guide.ai-project.000-process, Phase 3: High-Level Design & Slice Planning.  Use `guide.ai-project.003-slice-planning` with the project concept and specification documents to break {project} into manageable vertical slices.

Your role is Technical Fellow as described in the Process Guide. Work with the Project Manager to:

1. Create the high-level design document (architecture/050-arch.hld-{project}.md)
2. Identify foundation work, feature slices, and integration work
3. Create the slice plan document (003-slices.{project}.md)

Use enough slices to completely define the project.  Consider functional requirements only.  Ignore all non-functional requirements.  Avoid speculative risk projections.    When defining slices, focus on slice independence and clear user value. If you have all required inputs and sufficient information, proceed with slice planning. If not, request required information from the Project Manager.

Note: This is a design and planning task, not a coding task.
```

##### Slice Design (Phase 4)
```markdown
We're working in our guide.ai-project.000-process, Phase 4: Slice Design (Low-Level Design). Create a detailed design for slice: {slice} in project {project} by following the instructions here. These instructions may be used for adding a new slice with provided description, or designing {slice} included in the project slice plan.

Use the following inputs:
1. The project high-level design (architecture/050-arch.hld-{project}.md) if applicable.
2. One of the following (only one will be applicable):
	1. Slice description provided with this request.
	2. The project slice plan at `user/project-guides/003-slices.{project}.md`.

Note: if you are using the slice plan, it must contain information on this slice.

Create the slice design document at `user/slices/{slice}.md`.  Your role is Technical Fellow.

Include:
- YAML frontmatter as described below.
- Detailed technical decisions for this slice
- Data flows and component interactions
- UI mockups or detailed specifications (if applicable)
- Cross-slice dependencies and interfaces
- Any conflicts or considerations discovered

Avoid:
- Time estimates in hours/days/etc.  You may use a 1-5 relative effort scale.
- Extensive benchmarking tasks unless actually relevant to this effort.
- Extensive or speculative risk items.  Include only if truly relevant.
- Any substantial code writing.  This is a planning and process task.

YAML Frontmatter Details:
---
item: {slice}
project: {project}
type: slice
github: {url of github issue, if one is related}
dependencies: [list-if-any]
projectState: brief current state
status: not started
lastUpdated: YYYY-MM-DD
---

If framework or platform are specified, guide(s) for the framework(s) should be provided in `ai-project-guide/framework-guides/{framework}/introduction.md`. If tools are specified, guide for each tool should be available at `ai-project-guide/tool-guides/{tool}/introduction.md`.

Stop and request clarification if you need more information to complete the slice design.  This is a design and process task -- not a coding task!  Any code present should be minimal, and should provide essential information.
```

##### Task Breakdown (Phase 5)
*This should be usable for Slice or Feature task breakdown.*

```markdown
We're working in our guide.ai-project.000-process, Phase 5: Slice Task Breakdown. Convert the design for {slice | feature} in project {project} into granular, actionable tasks.  Note that this request can be used for *slice* or *feature*, but only one will be applicable to a particular request.

Your role is Senior AI. Use exactly one of the following as input:
1. The slice design document `user/slices/{slice}.md`.
2. The feature design document `user/features/{feature}.md`.

Create task file at `user/tasks/{sliceindex}-tasks.{slicename}.md`.  

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

Create task file at `user/tasks/{sliceindex}-tasks.{slicename}.md`.  

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
lastUpdated: YYYY-MM-DD
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
lastUpdated: YYYY-MM-DD
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
- Add the correct date (YYYY-MM-DD) in the file's frontmatter
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
lastUpdated: YYYY-MM-DD
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



