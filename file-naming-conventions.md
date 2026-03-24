---
docType: reference
scope: project-wide
audience: [human, ai]
description: Standard naming conventions for project files and directories
---

# File Naming Conventions

This document outlines standard naming conventions for project files and directories to ensure consistency and clarity across the project.

## YAML Frontmatter Requirement

**All markdown files in this project must include YAML frontmatter.** This enables consistent metadata, automated processing, and better AI comprehension.

### Universal Required Fields

All document types must include these fields:

```yaml
---
docType: <type>
project: <project-name>
dateCreated: YYYYMMDD
dateUpdated: YYYYMMDD
status: not_started | in_progress | complete | deferred | deprecated
---
```

Valid `docType` values: `guide`, `reference`, `concept`, `initiative-plan`, `architecture`, `slice-plan`, `slice-design`, `slice`, `tasks`, `analysis`, `review`, `notes`, `template`, `intro-guide`, `migration`

### Common Optional Fields

- `layer`: process, project, tool-guide, framework-guide, domain-guide
- `audience`: [human, ai] or subset
- `description`: Brief purpose description
- `dependsOn`: Related documents
- `aiModel`: AI model that generated the document (required for `review` docType)

### Valid Status Values

- `not_started` — work has not begun
- `in_progress` — actively being worked on
- `complete` — all work finished
- `deferred` — postponed, may be revisited
- `deprecated` — no longer relevant

Note: `completed` is recognized as an alias for `complete` in existing documents, but new documents should use `complete`.

### Date Format in YAML

All dates in YAML frontmatter must use **YYYYMMDD** format (no dashes):
```yaml
dateCreated: 20260121
dateUpdated: 20260121
```

This format:
- Matches filename date conventions
- Sorts correctly as strings
- Is unambiguous across locales

### Per-DocType Schemas

The following are the canonical schemas for each document type. Guides and prompts may include inline YAML examples for self-containedness, but they must agree with these definitions.

#### concept
```yaml
---
docType: concept
layer: project
phase: 0
phaseName: concept
project: {project}
audience: [human, ai]
description: Concept for {project}
dependsOn: []
dateCreated: YYYYMMDD
dateUpdated: YYYYMMDD
status: not_started
---
```

#### initiative-plan
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

#### architecture
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

#### slice-plan
```yaml
---
docType: slice-plan
parent: {path to parent architecture document}
project: {project}
dateCreated: YYYYMMDD
dateUpdated: YYYYMMDD
status: not_started
---
```

#### slice-design
```yaml
---
docType: slice-design
slice: {slice-name}
project: {project}
parent: {path to slice plan}
dependencies: [list-of-prerequisite-slices]
interfaces: [list-of-slices-that-depend-on-this]
dateCreated: YYYYMMDD
dateUpdated: YYYYMMDD
status: not_started
---
```

#### tasks
```yaml
---
docType: tasks
slice: {slice-name}
project: {project}
lld: user/slices/nnn-slice.{slice-name}.md
dependencies: [list-of-prerequisite-slices]
projectState: brief description of current state
dateCreated: YYYYMMDD
dateUpdated: YYYYMMDD
status: not_started
---
```

#### review
```yaml
---
docType: review
layer: project
project: {project}
reviewType: tasks|code|arch
sourceDocument: {path to reviewed document}
aiModel: {model-identifier}
dateCreated: YYYYMMDD
dateUpdated: YYYYMMDD
status: not_started
---
```

#### analysis
```yaml
---
docType: analysis
project: {project}
topic: {analysis-focus}
dateCreated: YYYYMMDD
dateUpdated: YYYYMMDD
status: not_started
---
```

## Directory Structure
- Use kebab-case (hyphenated lowercase) for directory names
  - Example: `project-guides`, `private`

- Maintain a logical hierarchy with clear parent-child relationships
  - Example: `project-documents/code-reviews/`

## Index Ranges and Semantic Structure

The project uses 3-digit indices (000-999). Indices serve two purposes: **lineage tracing** (related documents share a base index) and **broad categorization** (reserved ranges for system, operational, and standalone work).

The filename prefix (`arch.`, `slice.`, `tasks.`, `slices.`) identifies document type. The index identifies document family.

### Reserved Ranges

- **000-009**: Core AI-project process guides
  - Example: `guide.ai-project.process.md`, `guide.ai-project.000-concept.md`
  - Matching project files: `user/project-guides/001-concept.{project}.md`

- **010-049**: Reserved for future process extensions
  - Available for new methodology guides
  - Maintain consistent `guide.ai-project.nnn-{name}.md` pattern

- **050-099**: Project-level architecture and governance
  - Project HLD, project-wide specs, specialized utility guides
  - These documents describe the project as a whole, not a specific initiative
  - Documents here may generate architecture-level initiatives in the working range
  - Example: `050-arch.hld-{project}.md`
  - Example: `guide.ai-project.090-code-review.md` (090-099: specialized guides)

- **800-899**: Reserved for future use

- **900-999**: Operational work (not tied to an initiative)
  - **900-939**: Ad-hoc reviews, audits, quality gates → `user/reviews/`
  - **940-949**: Codebase analysis, research, investigation → `user/analysis/`
  - **950-999**: Maintenance, tech debt, bug tracking → `user/tasks/`
  - Example: `900-review.auth-module.md` (standalone audit, no parent slice)
  - Example: `940-analysis.dependency-audit.md`
  - Example: `950-tasks.maintenance.md`

### Working Range (100-799): Initiative-Based Indexing

The range 100-799 is a shared index space for all initiative work. An **initiative** is a cohesive body of work — typically originating from an architecture document — that produces slice plans, slice designs, and tasks.

#### How It Works

1. **Claim a base index** for the initiative at increments of 10 (100, 110, 120, ..., 790).
2. **The base index** is shared by the architecture doc, slice plan, and first slice:
   - `100-arch.context-forge-restructure.md`
   - `100-slices.context-forge-restructure.md`
   - `100-slice.restructure-scaffolding.md`
   - `100-tasks.restructure-scaffolding.md`
3. **Subsequent slices** increment from the base:
   - `101-slice.core-types-extraction.md`, `101-tasks.core-types-extraction.md`
   - `102-slice.core-services-extraction.md`, `102-tasks.core-services-extraction.md`
   - ...up to `109-slice.{name}.md`

#### Overflow

Most initiatives fit within 10 indices. If an initiative needs more (e.g., 12 slices), it spills into the next band. Simply skip that band when claiming the next initiative's base index:
- Initiative A: 100-111 (12 slices)
- Initiative B: 120+ (next available increment of 10)

#### Numbering Rules

- **Initiatives**: Claim indices at increments of 10 (100, 110, 120, ...)
- **Within an initiative**: Increment sequentially from the base index
- **Index reuse**: The same index appears across file types to indicate lineage (e.g., `101-slice.*.md` and `101-tasks.*.md` are the same work)
- **No collisions**: Check existing indices before claiming a new initiative base

#### Example: Context Forge Restructure

```
100-arch.context-forge-restructure.md        # Architecture document
100-slices.context-forge-restructure.md      # Slice plan
100-slice.restructure-scaffolding.md         # Slice 1 design
100-tasks.restructure-scaffolding.md         # Slice 1 tasks
101-slice.core-types-extraction.md           # Slice 2 design
101-tasks.core-types-extraction.md           # Slice 2 tasks
102-slice.core-services-extraction.md        # Slice 3
103-slice.core-orchestration-extraction.md   # Slice 4
104-slice.storage-migration.md               # Slice 5
105-slice.mcp-server-project-tools.md        # Slice 6
106-slice.mcp-server-context-tools.md        # Slice 7
107-slice.mcp-server-state-update-tools.md   # Slice 8
108-slice.electron-client-conversion.md      # Slice 9
109-slice.core-test-suite.md                 # Slice 10
110-slice.mcp-integration-testing.md         # Slice 11 (overflows into next band)
111-slice.documentation-and-packaging.md     # Slice 12
```

Next initiative would claim 120 as its base index.

#### Example: Multiple Initiatives

```
Project-level:
  050-arch.hld-trading-app.md                # Project HLD

Initiative A (100-band):
  100-arch.data-pipeline.md
  100-slices.data-pipeline.md
  100-slice.ingestion-service.md
  101-slice.transform-engine.md
  102-slice.output-adapters.md

Initiative B (110-band):
  110-arch.user-dashboard.md
  110-slices.user-dashboard.md
  110-slice.dashboard-layout.md
  111-slice.chart-widgets.md
  112-slice.filter-controls.md

Operational:
  900-review.ingestion-service.md
  950-tasks.maintenance.md
```

## Document Naming

### General Convention

Use periods (`.`) as primary separators and hyphens (`-`) for secondary grouping:
```
[document-type].[subject].[additional-info].md
```

Examples:
- `review.chartcanvas.0419.md`
- `tasks.code-review.chartcanvas.0419.md`
- `guide.development.react.md`

### Document Types

Common document type prefixes:
- `introduction` - Overview of platform, tech, or project area
- `tasks` - Task lists for implementation
- `review` - Code or design review documents
- `guide` - Technical or process guidance
- `spec` - Technical specifications
- `notes` - Meeting notes or research findings
- `template` - Prompt or other templates, organized with project-guides.
- `maintenance` - maintenance tasks, centralized in `user/tasks/950-tasks.maintenance.md`.

### Date Format

When including dates in filenames:
- Use `MMDD` format for short-term documents (e.g., `0419` for April 19)
- Use `YYYYMMDD` format for archival purposes (e.g., `20250419`)

## Task Files

Task files share the index of their parent slice:

```
nnn-tasks.{section}.md
```

Where:
- `nnn` matches the parent slice index (lineage link)
- `{section}` is the section name in lowercase with special characters removed and spaces replaced with hyphens

Examples:
- `100-tasks.restructure-scaffolding.md` (tasks for `100-slice.restructure-scaffolding.md`)
- `101-tasks.core-types-extraction.md` (tasks for `101-slice.core-types-extraction.md`)
- `950-tasks.maintenance.md` (operational — maintenance range)

### Legacy Task File Patterns
Previously used patterns (now deprecated):
- `tasks.[category].[component/feature].[additional-info].md`
- `{section}-tasks-phase-4.md`
- `nn-tasks-{section}.md` (2-digit index, replaced by nnn-tasks pattern)
- `tasks.code-review.{filename}.{date}.md` (still used for code review tasks)

## Slice Files

Slice design files share the initiative's base index (first slice) or increment from it:

```
nnn-slice.{slice-name}.md
```

Where:
- `nnn` is the initiative base index or an increment from it
- `{slice-name}` is the slice name in lowercase with spaces replaced by hyphens

Examples:
- `100-slice.restructure-scaffolding.md` (first slice, shares initiative base)
- `101-slice.core-types-extraction.md` (second slice, increments)
- `102-slice.core-services-extraction.md` (third slice)

## Slice Plan Files

Slice plans share the index of their parent architecture document:

```
nnn-slices.{initiative-name}.md
```

Where:
- `nnn` matches the parent architecture document's index
- `{initiative-name}` matches the initiative name

Example:
- `100-slices.context-forge-restructure.md` (plan for `100-arch.context-forge-restructure.md`)

## Review Files

Reviews come in two forms: **slice-lineage reviews** that are part of a slice's lifecycle, and **operational reviews** that stand alone.

### Slice-Lineage Reviews

Reviews produced during slice execution (e.g., task review after phase 5, code review after phase 6) share the index of their parent slice. This follows the same lineage principle as task files — the index identifies the family.

nnn-review.{template}.{slice-name}.md

Where:
- `nnn` matches the parent slice index (lineage link)
- `{template}` is the review template name (`tasks`, `code`, `arch`)
- `{slice-name}` matches the parent slice name

Directory: `user/reviews/`

Examples:
- `179-review.tasks.cli-foundation.md` (task review for `179-tasks.cli-foundation.md`)
- `179-review.code.cli-foundation.md` (code review for `179-slice.cli-foundation.md`)
- `105-review.arch.review-workflow-templates.md` (arch review for `105-slice.review-workflow-templates.md`)

When a pipeline re-runs a review (e.g., after fixing CONCERNS findings), the file is overwritten in place. Git history preserves prior runs.

### Operational Reviews

Standalone reviews not tied to a slice use the 900-939 range:
9nn-review.{subject}.md

Directory: `user/reviews/`

Examples:
- `900-review.auth-module.md` (ad-hoc audit of the auth module)
- `901-review.dependency-security.md` (one-off security review)


## File Size Limits and Splitting

To maintain manageable file sizes and improve readability:

### Size Guidelines
- **Non-architecture files**: Target ~350 lines when possible
- **Architecture files**: Allowed to grow larger as needed
- **Trigger for splitting**: When a file exceeds limits by >33% (~465 lines for non-architecture files)

### File Splitting Procedure
When a file considerably overruns the size limit (>33% over):

1. **First split**: Rename existing file from `{filename}.md` to `{filename}-1.md`
2. **Create continuation**: Add new file `{filename}-2.md` for additional content
3. **Subsequent splits**: Continue with `-3.md`, `-4.md`, etc. as needed

### Examples
- `103-tasks.auth.md` → exceeds 465 lines
- Rename to: `103-tasks.auth-1.md`
- Create: `103-tasks.auth-2.md`
- If needed: `103-tasks.auth-3.md`

### Rationale
- Keeps files navigable and focused
- Prevents overwhelming AI context windows
- Maintains clear organization within the index system
- Each continuation file still links to parent via index number

## Architectural Index Semantic Map

The index structure provides a machine-readable project architecture. This enables automated project analysis, cross-project pattern detection, and meta-agent coordination.

### Semantic Ranges and Directory Mapping

**000-009: Foundation** → `user/project-guides/`
- Project genesis documents (concept, spec, project-level slice plan)
- Defines project vision and scope
- Example: `001-concept.trading.md`, `002-spec.trading.md`

**050-099: Project-Level Architecture & Guides** → `user/architecture/`
- Project HLD, project-wide architectural decisions
- Specialized utility guides (090-099)
- Example: `050-arch.hld-trading.md`

**100-799: Initiative Working Space** → `user/architecture/`, `user/slices/`, `user/tasks/`, `user/reviews/`
- Architecture documents, slice plans, slice designs, tasks, and slice-lineage reviews
- Organized by initiative family (shared base index), not by document type
- Initiatives claim base indices at increments of 10 or 20
- Example family: `100-arch.data-pipeline.md`, `100-slices.data-pipeline.md`, `100-slice.ingestion.md`, `100-tasks.ingestion.md`, `100-review.tasks.ingestion.md`

**800-899: Reserved**
- Available for future semantic categorization
- Not currently in use

**900-939: Quality Assurance** → `user/reviews/`
- Ad-hoc reviews, audits, quality gates (not tied to a slice lifecycle)
- Slice-lineage reviews live at their parent slice's index in the 100-799 range
- Example: `900-review.auth-module.md`

**940-949: Investigation** → `user/analysis/`
- Codebase analysis, research, problem investigation
- Example: `940-analysis.async-boundaries.md`

**950-999: Maintenance** → `user/tasks/`
- Tech debt, bug tracking, operational tasks
- Centralized in: `950-tasks.maintenance.md`

### Usage for Meta-Project Analysis

This structure enables automated project snapshots:
```json
{
  "project": "trading",
  "foundation": ["001-concept.trading.md", "002-spec.trading.md"],
  "projectArchitecture": ["050-arch.hld-trading.md"],
  "initiatives": {
    "100": {
      "arch": "100-arch.data-pipeline.md",
      "slicePlan": "100-slices.data-pipeline.md",
      "slices": ["100-slice.ingestion.md", "101-slice.transform.md"],
      "tasks": ["100-tasks.ingestion.md", "101-tasks.transform.md"],
      "reviews": ["100-review.tasks.ingestion.md", "100-review.code.ingestion.md"]
    },
    "110": {
      "arch": "110-arch.user-dashboard.md",
      "slices": ["110-slice.layout.md", "111-slice.widgets.md"]
    }
  },
  "quality": ["900-review.ingestion-service.md"],
  "investigation": ["940-analysis.async-sync.md"],
  "maintenance": ["950-tasks.maintenance.md"]
}
```