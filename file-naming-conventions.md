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

Minimum required frontmatter:
```yaml
---
docType: [guide|reference|slice|tasks|analysis|notes|template|intro-guide]
---
```

Common optional fields:
- `layer`: process, project, tool-guide, framework-guide, domain-guide
- `audience`: [human, ai] or subset
- `description`: Brief purpose description
- `dependsOn`: Related documents
- `dateCreated`: Date file was created (YYYYMMDD format, immutable)
- `dateUpdated`: Date of last modification (YYYYMMDD format)
- `status`: in_progress, completed, deprecated

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

## Directory Structure
- Use kebab-case (hyphenated lowercase) for directory names
  - Example: `project-guides`, `private`

- Maintain a logical hierarchy with clear parent-child relationships
  - Example: `project-documents/code-reviews/`

## Index Ranges and Semantic Structure

The project uses 3-digit indices (000-999) with semantic range allocation:

### Range Allocation
- **000-009**: Core AI-project process guides
  - Example: `guide.ai-project.000-process.md`, `guide.ai-project.001-concept.md`
  - Matching project files: `user/project-guides/001-concept.{project}.md`

- **010-049**: Reserved for future process extensions
  - Available for new methodology guides
  - Maintain consistent guide.ai-project.nnn-{name}.md pattern

- **050-089**: Architecture and system design (40 slots)
  - High-level designs (HLD)
  - System architecture documents
  - Technology selection and rationale
  - Example: `user/architecture/050-arch.hld-{project}.md`

- **090-099**: Specialized utility guides
  - Example: `guide.ai-project.090-code-review.md`
  - Example: `guide.ai-project.091-legacy-task-migration.md`

- **100-799**: Active work items (700 slots)
  - Slice design documents
  - Task files
  - User-created or user-initiated work
  - Primary working range for project execution
  - Example: `user/slices/100-slice.{name}.md`

- **800-899**: Reserved (100 slots)

- **900-939**: Code review tasks (40 slots)
  - Code review task files
  - Review analysis documents
  - Code review follow-up work
  - Example: `user/reviews/review.{component}.{date}.md`

- **940-949**: Codebase analysis tasks (10 slots)
  - Analysis performed when applying methodology to existing projects
  - Investigative/diagnostic work on existing codebases
  - Example: `940-analysis.dependency-audit.md`

- **950-999**: Maintenance tasks (50 slots)
  - Maintenance task lists
  - Operational procedures
  - Bug tracking and tech debt
  - Example: `950-tasks.maintenance.md`

### Number Ranges
- **000-009**: Core process guides
- **010-049**: Extended process documentation
- **050-089**: Architecture documents
- **090-099**: Specialized guides (code review, legacy migration, etc.)
- **100-799**: Regular sequential content (slices, tasks, features, user work)
- **800-899**: Reserved
- **900-939**: Code review files
- **940-949**: Codebase analysis files
- **950-999**: Maintenance files

### Numbering Rules
- **Sequential within category**: Find the highest existing number in the same range category and increment by 1
- **Range boundaries**: Respect range semantics when numbering new files
- **Start appropriately**: Begin at the first number of the appropriate range (e.g., 100 for first slice)

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
Task files should follow this convention:

```
nnn-tasks.{section}.md
```

Where:
- `nnn` is a 3-digit sequential index following the range allocation above (typically 100-799 for active work)
- `{section}` is the section name in lowercase with special characters removed and spaces replaced with hyphens

Examples:
- `100-tasks.user-authentication.md`
- `200-tasks.backend-api.md`
- `300-tasks.database-setup.md`
- `900-tasks.maintenance.md` (for maintenance items)

### Legacy Task File Patterns
Previously used patterns (now deprecated):
- `tasks.[category].[component/feature].[additional-info].md`
- `{section}-tasks-phase-4.md`
- `nn-tasks-{section}.md` (2-digit index, replaced by nnn-tasks pattern)
- `tasks.code-review.{filename}.{date}.md` (still used for code review tasks)

## Slice Files
Slice design files should follow this convention:

```
nnn-slice.{slice-name}.md
```

Where:
- `nnn` is a 3-digit sequential index (typically 100-799 for active work)
- `{slice-name}` is the slice name in lowercase with spaces replaced by hyphens

Examples:
- `100-slice.user-authentication.md`
- `200-slice.trading-dashboard.md`
- `300-slice.portfolio-management.md`

## Feature Files
Feature files link to their parent slice via the index number (slice name is omitted to avoid redundancy):

```
{sliceindex}-feature.{feature-name}.md
```

Where:
- `{sliceindex}` matches the parent slice's index number (creates the link)
- `{feature-name}` describes the specific feature

Examples:
- `120-feature.remember-me.md` (extends 120-slice.auth.md)
- `120-feature.oauth-providers.md` (extends 120-slice.auth.md)
- `200-feature.widgets.md` (extends 200-slice.dashboard.md)

## Feature Task Files
Feature-specific task files follow the same pattern as feature files:

```
{sliceindex}-tasks.{feature-name}.md
```

Examples:
- `120-tasks.auth.md` (main slice tasks for 120-slice.auth.md)
- `120-tasks.remember-me.md` (feature-specific tasks for 120-feature.remember-me.md)
- `200-tasks.widgets.md` (feature-specific tasks for 200-feature.widgets.md)


## File Size Limits and Splitting

To maintain manageable file sizes and improve readability:

### Size Guidelines
- **Non-architecture files**: Target ~350 lines maximum
- **Architecture files**: Allowed to grow larger as needed
- **Trigger for splitting**: When a file exceeds limits by >33% (~465 lines for non-architecture files)

### File Splitting Procedure
When a file considerably overruns the size limit (>33% over):

1. **First split**: Rename existing file from `{filename}.md` to `{filename}-1.md`
2. **Create continuation**: Add new file `{filename}-2.md` for additional content
3. **Subsequent splits**: Continue with `-3.md`, `-4.md`, etc. as needed

### Examples
- `120-tasks.auth.md` → exceeds 465 lines
- Rename to: `120-tasks.auth-1.md`
- Create: `120-tasks.auth-2.md`
- If needed: `120-tasks.auth-3.md`

### Rationale
- Keeps files navigable and focused
- Prevents overwhelming AI context windows
- Maintains clear organization within the index system
- Each continuation file still links to parent via index number

## Architectural Index Semantic Map

The index structure provides a machine-readable project architecture. This enables automated project analysis, cross-project pattern detection, and meta-agent coordination.

### Semantic Ranges and Directory Mapping

**000-009: Foundation** → `user/project-guides/`
- Project genesis documents (concept, spec, slice plan)
- Defines project vision and scope
- Example: `001-concept.trading.md`, `002-spec.trading.md`

**050-089: System Architecture** → `user/architecture/`
- High-level designs, system diagrams, technology decisions
- Architectural patterns and infrastructure
- Example: `050-arch.hld-trading.md`

**100-799: Active Development** → `user/slices/`, `user/features/`, `user/tasks/`
- Current features and slices being implemented
- Organized by work item, not sprints or arbitrary time periods
- Each project has a current focus item; items receive time based on priority
- Example: `100-slice.auth.md`, `120-tasks.auth.md`

**800-899: Reserved** (100 slots)
- Available for future semantic categorization
- Not currently in use

**900-939: Quality Assurance** → `user/reviews/`
- Code reviews, audits, quality gates
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
  "architecture": ["050-arch.hld-trading.md"],
  "activeWork": ["100-slice.timescale-data.md", "200-slice.realtime-ws.md"],
  "quality": ["900-review.timescale-layer.md"],
  "investigation": ["940-analysis.async-sync.md"],
  "maintenance": ["950-tasks.maintenance.md"]
}
```

## Benefits
This naming convention provides:
- Clear visual hierarchy in filenames
- Easier tab completion in terminals
- Better compatibility with various systems
- Consistent pattern for all project documentation
- Logical grouping when viewing directory contents
- Manageable file sizes through systematic splitting
- Machine-readable architectural map for meta-agent coordination

## Project Log Files

### DEVLOG.md

**Location**: Project root (`DEVLOG.md`)

**Purpose**: Internal session log for documenting development work, enabling easy project resumption by humans or AI agents.

**Format**:
```markdown
## YYYYMMDD
- Brief bullet points of work completed
- Decisions made and rationale
- Issues encountered or deferred
- Context for next session
```

**Distinction from CHANGELOG.md**:
- `CHANGELOG.md`: External-facing, version-oriented release notes
- `DEVLOG.md`: Internal-facing, session-oriented work log

**Guidelines**:
- Entries should be brief and timestamped
- Focus on "what changed" not "how"
- Include decisions and their rationale
- Note any WIP or deferred items

## Legacy Files
Existing files may follow different conventions. When updating or creating new versions of these files, convert to the new naming convention. Do not rename existing files solely for convention compliance unless part of a coordinated effort.
