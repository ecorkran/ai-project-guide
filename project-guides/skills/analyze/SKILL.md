---
name: analyze
description: Codebase analysis workflow — discover, categorize findings, create tasks, and implement fixes
disable-model-invocation: true
---

# Codebase Analysis Workflow

This skill provides a complete analysis workflow for existing codebases. It is organized into stages that can be used independently or as a sequential pipeline.

**Usage**: Invoke `/analyze` and specify which stage to run, or start from Stage 1 for a full discovery workflow. Provide `{project}` and optionally `{subproject}` as context.

---

## Stage 1: Analyze Codebase

Purpose: Perform discovery analysis of existing codebase to:
- Document system architecture and technology stack
- Identify technical debt and improvement opportunities
- Provide foundation for creating architectural components, slices, or maintenance tasks
- Create reference documentation for team members

This is reconnaissance work - not goal-oriented development.

Analyze the following existing codebase and document your findings. We want this to not only assist ourselves in updating and maintaining the codebase, but also to assist humans who may be working on the project.

### Expected Output
* Document your findings in `user/analysis/nnn-analysis.{topic}.md` where:
  - nnn starts at 940 (analysis range)
  - {topic} describes the analysis focus (e.g., "initial-codebase", "dependency-audit", "architecture-review")
* Write in markdown format, following our rules for markdown output.

### General Guidelines
* Document the codebase structure. Also note presence of any project-documents or similar folders which probably contain information for us.
* Document presence or average of tests, and an estimate of coverage if tests are present.
* Identify technologies and frameworks in use.
* What package managers are in use?
* Is there a DevOps pipeline indicated?
* Analysis should be concise and relevant - no pontificating.
* Add note in README as follows: Claude: please find code analysis details in {file mentioned above}.

### Front End (if applicable)
* If this is a JS app, does it use React? Vue? Is it NextJS? Is it typescript, javascript, or both? Does it use TailWind? ShadCN? Something else?

### NextJS, React (if applicable)
* Perform standard analysis and identify basic environment -- confirm NextJS, identify common packages in use (Tailwind, ShadCN, etc) and any unusual packages or features.
* If auth is present, attempt to determine its structure and describe its methodology
* Is the project containerized?
* If special scripts (ex: 'docker: {command}') are present, document them in the README.
* Provide a description of the UI style, interactivity, etc
* Document page structure.
* What type of architecture is used to manage SSR vs CSR?

### Tailwind (if applicable)
* Is cn used instead of string operations with parameterized or variable classNames?
* Prefer Tailwind classes, there should not be custom CSS classes.
* If this is Tailwind 4, are customizations correctly in CSS and no attempt to use tailwind.config.ts/.js.

---

## Stage 2: Analysis Processing

We need to process the artifacts from our recent code analysis.

Role: Senior AI, processing analysis results into actionable items
Context: Analysis has been completed on {project} (optionally {subproject}) and findings need to be converted into proper maintenance tasks, code review issues, or GitHub issues as appropriate.

Notes:
- Be sure to know the current date first. Do not assume dates based on training data timeframes.

### Process

1. **Categorize Findings:**
   - P0 Critical: Data loss, security vulnerabilities, system failures
   - P1 High: Performance issues, major technical debt, broken features
   - P2 Medium: Code quality, maintainability, best practices
   - P3 Low: Optimizations, nice-to-have improvements

2. **Create File and Document by Priority:**
   - Create markdown file `analysis/nnn-analysis.{project-name}{.subproject?}.md` where nnn starts at 940 (analysis range).
   - Note that subproject is often not specified. Do not add its term to the name if this is the case.
   - Divide file into Critical Issues (P0/P1) and Additional Issues (P2/P3)
   - Add concise documentation of each issue -- overview, context, conditions.

3. **File Creation Rules:**
   - Use existing file naming conventions from `file-naming-conventions.md`
   - Include YAML front matter for all created files
   - Add the correct date (YYYYMMDD) in the file's frontmatter
   - Reference source analysis document (if applicable)
   - Add line numbers and specific locations where applicable

4. **GitHub Integration (if available):**
   - Create GitHub issues for P0/P1 items
   - Label appropriately: `bug`, `critical`, `technical-debt`, `analysis`
   - Reference analysis document in issue description
   - Include reproduction steps and success criteria

---

## Stage 3: Analysis Task Creation

Convert analysis findings into granular, actionable tasks.

We're working in our guide.ai-project.process, Phase 5: Slice Task Breakdown. Convert the issues from {analysis-file} into granular, actionable tasks if they are not already. Keep them in priority order (P0/P1/P2/P3).

If the tasks are already sufficiently granular and in checklist format, you do not need to modify them. Note that each success criteria needs a checkbox.

Your role is Senior AI. Use the specified analysis document `user/analysis/nnn-analysis.{project-name}{.subproject?}.md` as input. Note that subproject is optional (hence the ?). Avoid adding extra `.` characters to filename if subproject is not present.

Create task file at `user/tasks/nnn-analysis{.subproject?}-{date}.md` with:
1. YAML front matter including slice or subproject name, project, YYYYMMDD date, main analysis file reference, dependencies, and current project state
2. Context summary section
3. Granular tasks following Phase 5 guidelines
4. Keep success criteria with their respective task
5. Always use checklist format described in guide.ai-project.process under Task Files.

For each {tool} in use, consult knowledge in `ai-project-guide/tool-guides/{tool}/`. Follow all task creation guidelines from the Process Guide.

Each task must be completable by a junior AI with clear success criteria. If insufficient information is available, stop and request clarifying information.

This is a project planning task, not a coding task.

---

## Stage 4: Analysis to LLD

*This stage is rarely needed. Normally, analysis findings should be addressed using the standard architectural component → slice plan → slices methodology. Use this only when a focused low-level design is needed for a specific analysis finding.*

We need to create a Low-Level Design (LLD) for {component} identified during codebase analysis or task planning in project {project}. It may be an expansion of an initial task section identified during analysis.

Your role is Architect as described in the Process Guide. This LLD will bridge the gap between high-level understanding and implementable tasks.

### Context
- Analysis document: `user/analysis/nnn-analysis.{project-name}{.subproject or analysis topic?}` (or specify location)
- Related task file: `user/tasks/nnn-analysis{.subproject?}-{date}.md` (if exists)
- Current issue: {brief description of what analysis revealed}

### Output
Create LLD document at: `user/slices/nnn-slice.{slice-name}.md`

Required YAML front matter:
```yaml
---
layer: project
docType: slice-design
slice: {slice-name}
project: {project}
triggeredBy: analysis|task-breakdown|architecture-review
sourceDocument: {path-to-analysis-or-task-file}
dependencies: [list-any-prerequisites]
affects: [list-components-or-slices-impacted]
complexity: low|medium|high
dateCreated: YYYYMMDD
dateUpdated: YYYYMMDD
status: not_started
---
```

### Guidelines

**Cross-Reference Requirements:**
- Update source analysis/task document to reference this LLD
- Add back-reference in this LLD to triggering document
- Note any slice designs or existing slices this affects

**Focus Areas:**
- Keep design concrete and implementation-ready
- Include code examples or pseudocode where helpful
- Reference specific files, classes, or components by name
- Address both immediate needs and future extensibility

If you need more context about the analysis findings or existing system architecture, stop and request from Project Manager.

Note: This creates implementation-ready technical designs, not high-level planning documents.

---

## Stage 5: Analysis Task Implementation

Execute tasks created from analysis findings.

We are working on the analysis file {analysis} in project {project}, phase 6 of `ai-project-guide/project-guides/guide.ai-project.process`.

Your role is "Senior AI". Your job is to complete the tasks in the `user/tasks/nnn-analysis-{topic}.md` file. Please work through the tasks, following the guidelines in our project guides, and using the rules in the rules/ directory.

The analysis overview is available at {analysis} for additional context.

STOP and confer with Project Manager after each task, unless directed otherwise by the Project Manager. Do not update any progress files until confirmation from Project Manager.

Work carefully and ensure that each task is verified complete before proceeding to the next. If an attempted solution does not work or you find reason to try another approach, do not make more than three attempts without stopping and obtaining confirmation from Project Manager.

Check off completed tasks in the task file when verified complete. When all tasks are complete, proceed to Phase 7 (integration) with Project Manager approval.

Notes:
* Use the task-checker to manage lists if it is available to you
* Ignore case sensitivity in all file and directory names
* If you cannot locate referenced files, STOP and request information from Project Manager
* Do not guess, assume, or proceed without required files.
