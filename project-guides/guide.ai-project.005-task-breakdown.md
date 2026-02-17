---
layer: process
phase: 5
phaseName: task-breakdown
guideRole: primary
audience: [human, ai]
description: Phase 5 playbook for converting slice or feature designs into granular task lists.
dependsOn:
  - guide.ai-project.000-process.md
  - guide.ai-project.003-slice-planning.md
  - guide.ai-project.004-slice-design.md
dateCreated: 20260217
dateUpdated: 20260217
---

#### Summary
This guide provides instructions for converting approved slice or feature designs into granular, actionable task lists. This is Phase 5 in `guide.ai-project.000-process`. Phase 5 cannot begin until the slice design (Phase 4 output) or feature design is approved by the Project Manager.

The goal is to produce a task list that can be executed in a single context session by a junior AI or human developer. Each task must be self-contained enough to complete without requiring product decisions.

#### Role
Senior AI performs this phase. The Project Manager approves the output before proceeding to Phase 6 (Task Expansion).

#### Inputs
* guide.ai-project.000-process
* guide.ai-project.005-task-breakdown (this document)
* {project} - spec (Phase 2 output)
* {project} - high-level design (Phase 2.5 output)
* {slice} - slice design (Phase 4 output), OR {feature} - feature design
* rules/ - directory containing coding rules and guidelines organized by platform/technology
* tool-guides/{tool}/ - for each tool referenced in the design

If any inputs are missing or insufficient, stop and resolve with the Project Manager before proceeding.

#### Output
A task file saved as `user/tasks/{sliceindex}-tasks.{slicename}.md`, where `{sliceindex}` matches the parent slice's numeric index (preserving lineage per `file-naming-conventions.md`).

#### Task File Format

##### Front Matter and Context
Every task file begins with YAML front matter and a context summary:

```yaml
---
slice: {slice-name}
project: {project-name}
lld: user/slices/nnn-slice.{slice-name}.md
dependencies: [list-of-prerequisite-slices]
projectState: brief description of current state
dateCreated: YYYYMMDD
dateUpdated: YYYYMMDD
---

## Context Summary
- Working on {slice-name} slice
- Current project state and key assumptions
- Dependencies and prerequisites
- What this slice delivers
- Next planned slice
```

##### Checklist Format
Use the checklist format defined in `guide.ai-project.000-process` under Task Files. Key rules:
- L1 items have checkboxes and describe the task objective
- L2 items are indented with checkboxes for important sub-items and all success criteria
- L3 subtasks (if needed) are numbered
- Success criteria remain at L2 level, not separated from their task

##### File Length
Keep task files to approximately 350 lines or fewer. If considerably more space is needed:
1. Rename current file `nnn-tasks.{task-section-name}-1.md`
2. Add new file `nnn-tasks.{task-section-name}-2.md`
3. Continue as needed

Do not split a file for less than ~100 lines of overrun.

#### Task Quality Requirements

Each task must have:
- **Clearly defined scope**: Precise and narrow. One concern per task.
- **Actionable instructions**: Unambiguous enough for a junior AI or human developer to complete without product decisions.
- **Success criteria**: Specific, measurable definition of "done."

Tasks should be organized so they can be completed sequentially.  Create separate sub-tasks for each similar component rather than grouping them.

#### What to Include
- Consult `ai-project-guide/tool-guides/{tool}/` for each tool referenced in the design. If tool knowledge is not present, search the web if possible and alert the Project Manager.
- If the project contains or will contain `package.json`, include a setup task that adds scripts from `snippets/npm-scripts.ai-support.json`.
- Tasks may reference the slice design document rather than duplicating large sections of it.  Ensure references are accurate.

#### What to Avoid
- **Time estimates** in hours/days. Relative effort (1-5 scale) is acceptable.
- **Extensive benchmarking** tasks unless specifically relevant to this slice.
- **Speculative risk items**. Include only if truly relevant.
- **Open-ended human-centric tasks** such as SEO optimization. Only include tasks that can reasonably be completed by an AI.
- **Code in the task file**. This is a planning task, not a coding task. Code segments should be minimal and limited to what is necessary to convey information.

#### Handling Insufficient Information
If insufficient information is available to fully convert a design item into tasks, **stop** and request clarifying information from the Project Manager before continuing. Do not guess or make assumptions.

#### Procedure
1. Review all inputs: slice design, spec, HLD, relevant tool guides, and rules.
2. Confirm any questions or ambiguities with the Project Manager.
3. Break the design into sequential, granular tasks following the format above.
4. Create separate sub-tasks for similar components (don't batch them).
5. Verify each task has clear scope, instructions, and success criteria.
6. Review the complete task list against the slice design to confirm full coverage.
7. Verify file length is within guidelines.

#### Success Criteria
Phase 5 is complete when:
- Task file exists with proper front matter and context summary
- All design elements are accounted for in the task list
- Each task is completable by a junior AI with clear success criteria
- Tasks are sequentially ordered with dependencies respected
- File length is within guidelines
- Project Manager approves the task breakdown

#### Next Steps
With approved task breakdown:
1. Proceed to Phase 6: Task Enhancement and Expansion
2. Use `guide.ai-project.006-task-expansion` for detailed guidance
3. The Phase 6 output becomes the ready-to-execute task list for Phase 7
