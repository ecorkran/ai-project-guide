---
layer: project
docType: slice
project: ai-project-guide
sliceIndex: 100
sliceName: prompt-optimization-1
phase: 4
dependencies: []
framework: markdown
tools: []
relativeEffort: 3
---

# Overview
This file provides initial information for our prompt optimization slice.  If you are an AI and this file does not contain appropriate YAML frontmatter according to the project guide -- add it.  Leave the User-Provided Concept section as-is.  Add your slice design to to the Slice Design section.  This project is an intricate and intentionally interdependent system -- it makes a cohesive whole.  For this reason, any mistake can have unexpectedly large consequences, and therefore all work here must be approached with more than the usual level of precision.  Specifics only.  Do not make any assumptions.

## User-Provided Concept
We have several issue to address in prompts, especially as they apply to the context-builder app, which is a dependent app that provides UI and persistence to this system of contexts, prompts, and guides.  The Slice Design included here should contain brief but refined descriptions of the items listed here.

### Indices and File Naming
There are numerous prompts referencing {nn}, nn, or `nn-[type].[name].  We want to change to a 3-digit system.  We need to update the system prompts (prompt.ai-project.system) replacing all nn with nnn.  Additionally, we need to establish guidelines for the naming.  This affects file-naming-conventions.md as well.

#### File Naming
##### Guides
* guide.ai-project.nn.{guidename}.md: ideally we update these to nnn but don't change numeric value.  For example guide.ai-project.000-process.md, guide.ai-project.001-concept.md.  We still reference concept as "Phase 1" when used in this context.  When discussing the file or technical details we can use 001.
* Files that we create should have matching indices, ex: `private/project-guides/001-concept.{projectname}.md`
* change guide.ai-project.090-code-review to

##### File Naming Conventions
* We will need to update the relevant file-naming-conventions.md file here.
```
00x:   ai-project guides, project-specific guides in private/project-guides/
090:   code review guide
091:   legacy task migration
0xx:   remaining 0xx indices system-reserved.
100:   slices, tasks, user created or initiated
700:   architecture, system design
800:   features
900:   maintenance items
950:   here through 999 is system use.
```

#### Indices and Existing Files
This index schema update will probably necessitate changes to numerous files.


## Slice Design

### Overview
This slice implements a comprehensive file naming and indexing system migration for the ai-project-guide project. The migration moves from a 2-digit (nn) to a 3-digit (nnn) index system with structured index ranges that provide clear semantic meaning and support for future expansion.

### Technical Scope

#### 1. Index System Migration (2-digit → 3-digit)

**Current State:**
- Guide files use 2-digit indices: `guide.ai-project.000-process.md`, `guide.ai-project.001-concept.md`, etc.
- System prompts reference `nn` or `{nn}` patterns for file naming
- File naming conventions document describes 2-digit system

**Target State:**
- Guide files use 3-digit indices: `guide.ai-project.000-process.md`, `guide.ai-project.001-concept.md`, etc.
- System prompts reference `nnn` or `{nnn}` patterns
- Numeric values remain unchanged (e.g., 00 → 000, 01 → 001, 90 → 090)

**Files Requiring Index Updates:**
- `project-guides/guide.ai-project.000-process.md` → `guide.ai-project.000-process.md`
- `project-guides/guide.ai-project.001-concept.md` → `guide.ai-project.001-concept.md`
- `project-guides/guide.ai-project.002-spec.md` → `guide.ai-project.002-spec.md`
- `project-guides/guide.ai-project.003-slice-planning.md` → `guide.ai-project.003-slice-planning.md`
- `project-guides/guide.ai-project.004-slice-design.md` → `guide.ai-project.004-slice-design.md`
- `project-guides/guide.ai-project.006-task-expansion.md` → `guide.ai-project.006-task-expansion.md`
- `project-guides/guide.ai-project.090-code-review.md` → `guide.ai-project.090-code-review.md`
- `project-guides/guide.ai-project.091-legacy-task-migration.md` → `guide.ai-project.091-legacy-task-migration.md`

#### 2. Index Range Schema Definition

**New Index Ranges:**
```
000-009: Core AI-project guides (process, concept, spec, planning, design)
010-049: Reserved for future process guides and extensions
050-089: Architecture and system design documents (40 slots)
090-099: Specialized guides (code review, legacy migration, etc.)
100-799: Slices, tasks, and user-created/initiated work items (700 slots)
800-899: Feature-specific documents
900-949: Maintenance items and ongoing operations
950-999: System use and internal tooling
```

**Semantic Meaning:**
- **0xx range**: Planning and framework - the "how and what" documentation
  - 000-009: Core process guides
  - 010-049: Process extensions
  - 050-089: Architecture and design
  - 090-099: Specialized tools
- **1xx-7xx range**: Execution - the actual work items (slices, tasks)
- **8xx range**: Features - discrete functional capabilities
- **9xx range**: Maintenance and system operations

#### 3. File Naming Convention Updates

**Updates to file-naming-conventions.md:**

Add new section before "Sequential Numbering Convention":

```markdown
## Index Ranges and Semantic Structure

The project uses 3-digit indices (000-999) with semantic range allocation:

### Range Allocation
- **000-009**: Core AI-project process guides
  - Example: `guide.ai-project.000-process.md`, `guide.ai-project.001-concept.md`
  - Matching project files: `private/project-guides/001-concept.{project}.md`

- **010-049**: Reserved for future process extensions
  - Available for new methodology guides
  - Maintain consistent guide.ai-project.nnn-{name}.md pattern

- **050-089**: Architecture and system design (40 slots)
  - High-level designs (HLD)
  - System architecture documents
  - Technology selection and rationale
  - Example: `private/project-guides/050-hld.{project}.md`

- **090-099**: Specialized utility guides
  - Example: `guide.ai-project.090-code-review.md`
  - Example: `guide.ai-project.091-legacy-task-migration.md`

- **100-799**: Active work items (700 slots)
  - Slice design documents
  - Task files
  - User-created or user-initiated work
  - Primary working range for project execution
  - Example: `private/slices/100-slice.{name}.md`

- **800-899**: Feature documents
  - Standalone feature specifications
  - Feature-specific design documents

- **900-949**: Maintenance and operations
  - Maintenance task lists
  - Operational procedures
  - Bug tracking and tech debt

- **950-999**: System-reserved
  - Internal tooling documentation
  - System configuration files
  - Reserved for framework use
```

Update "Sequential Numbering Convention" to reference 3-digit system:

```markdown
### Number Ranges
- **000-009**: Core process guides
- **010-049**: Extended process documentation
- **050-089**: Architecture documents
- **090-099**: Specialized guides (code review, legacy migration, etc.)
- **100-799**: Regular sequential content (slices, tasks, user work)
- **800-899**: Feature files
- **900-949**: Maintenance files
- **950-999**: System-reserved files

### Numbering Rules
- **Sequential within category**: Find the highest existing number in the same range category and increment by 1
- **Range boundaries**: Respect range semantics when numbering new files
- **Start appropriately**: Begin at the first number of the appropriate range (e.g., 100 for first slice)
```

#### 4. System Prompt Updates

**File:** `project-guides/prompt.ai-project.system.md`

**Changes Required:**
Replace all instances of `nn` with `nnn` in file naming patterns. Specific updates:

1. **Line 41:** `001-concept.{project}.md` (currently correct, verify consistency)
2. **Line 52:** `private/project-guides/002-spec.{project}.md` (update from 02)
3. **Line 79:** `03-hld.{project}.md` → `050-hld.{project}.md` (architecture range)
4. **Line 81:** `03-slices.{project}.md` → `003-slices.{project}.md`
5. **Line 100:** `nn-slice.{slice}.md` → `nnn-slice.{slice}.md`
6. **Throughout:** All references to `nn-` patterns should become `nnn-`

**Pattern Search Terms:**
- `nn-slice`
- `nn-tasks`
- `nn-feature`
- `{nn}`
- Any 2-digit guide references (00-process, 01-concept, etc.)

#### 5. Cross-Reference Updates

**Files with Cross-References:**
Search and update references in:
- All guide.ai-project.*.md files (guide cross-references)
- prompt.ai-project.system.md (all file naming patterns)
- file-naming-conventions.md (examples and patterns)
- directory-structure.md (file tree examples)
- readme.md in project-guides/ (table entries and links)
- CLAUDE.md (project instructions, if references exist)
- Any template files in snippets/
- All files in private/project-guides/ (spec, HLD, slice plans)
- All files in private/slices/ (YAML frontmatter, cross-references)
- All files in private/tasks/ (YAML frontmatter, cross-references)

**Reference Patterns to Update:**

*Guide file references:*
- File path references: `guide.ai-project.nn-*` → `guide.ai-project.nnn-*`
- Inline references: "Phase nn" can remain, but "guide nn" → "guide nnn"
- Markdown links: Update all `[text](guide.ai-project.nn-*.md)` patterns

*Project-specific file references:*
- `01-concept.{project}.md` → `001-concept.{project}.md`
- `02-spec.{project}.md` → `002-spec.{project}.md`
- `03-hld.{project}.md` → `050-hld.{project}.md` (note: architecture range)
- `03-slices.{project}.md` → `003-slices.{project}.md`
- `nn-slice.{name}.md` → `nnn-slice.{name}.md`
- `nn-tasks.{name}.md` → `nnn-tasks.{name}.md`
- `nn-feature.{name}.md` → `nnn-feature.{name}.md`
- Examples in documentation: `01-slice.*`, `02-tasks.*`, etc. → `nnn-*` patterns

*YAML frontmatter:*
- `dependsOn: [guide.ai-project.nn-*]` → `dependsOn: [guide.ai-project.nnn-*]`
- `lld: private/slices/nn-slice.*` → `lld: private/slices/nnn-slice.*`

#### 6. Documentation Context Updates

**Phase Numbering vs File Numbering:**
Important distinction to maintain:
- **Phase references** remain as "Phase 1", "Phase 2", etc. (human-readable process steps)
- **File references** use 3-digit: "guide 001", "file 001-concept.{project}.md" (technical precision)
- **Context switching**: Clear when discussing process ("Phase 1 Concept") vs files ("001-concept document")

Example clarifying language:
```markdown
We are in Phase 1 (Concept Creation) as defined in the Process Guide.
The concept document is located at `private/project-guides/001-concept.{project}.md`.
Phase 1 uses guide file 001-concept and creates the 001-concept project document.
```

### Data Flows

#### File Renaming Flow
```
1. Identify all guide.ai-project.nn-*.md files
2. Create renamed copies with nnn indices
3. Update internal content references within each file
4. Update cross-references in other project files
5. Verify all links functional
6. Remove old nn-indexed files
```

#### Reference Update Flow
```
1. Generate inventory of all markdown files in project
2. Search for multiple patterns:
   - guide.ai-project.nn- (guide file references)
   - nn-concept., nn-spec., nn-hld., nn-slices. (project doc patterns)
   - nn-slice., nn-tasks., nn-feature. (work item patterns)
   - `nn- or 'nn- in backticks/quotes (code examples)
   - YAML frontmatter with nn patterns
3. Analyze context (is it a file reference, example, or something else?)
4. Update to appropriate nnn pattern:
   - Most nn → nnn (preserving numeric value)
   - Special case: 03-hld → 050-hld (architecture range)
5. Validate updated references point to correct files
6. Test prompt execution with updated references
```

### Component Interactions

#### Primary Documents Affected
1. **Guide Files** (`project-guides/guide.ai-project.*.md`)
   - Directly renamed with 3-digit indices
   - Internal content references updated
   - Cross-references to other guides updated

2. **System Prompts** (`project-guides/prompt.ai-project.system.md`)
   - All nn patterns → nnn patterns
   - File path templates updated
   - Example references updated

3. **File Naming Conventions** (`project-guides/file-naming-conventions.md` and root `file-naming-conventions.md`)
   - Index range schema added
   - Sequential numbering rules updated
   - Examples updated to 3-digit system

4. **Project Documents** (`private/project-guides/*.md`, `private/slices/*.md`, `private/tasks/*.md`)
   - References to guide files updated
   - Naming patterns for new files follow nnn system

#### Dependency Chain
```
guide.ai-project.000-process.md (master process definition)
    ↓ referenced by
prompt.ai-project.system.md (prompt templates)
    ↓ used to create
private/project-guides/nnn-*.md (project-specific documents)
    ↓ follow naming from
file-naming-conventions.md (naming rules)
```

### Implementation Considerations

#### Migration Strategy
**Approach:** Atomic rename with verification

1. **Preparation Phase**
   - Generate complete inventory of affected files
   - Create backup of project-guides/ directory
   - Document all current cross-references

2. **Execution Phase**
   - Rename guide files (use git mv for tracking)
   - Update prompt.ai-project.system.md
   - Update file-naming-conventions.md
   - Update cross-references in all other files

3. **Verification Phase**
   - Grep search for remaining nn patterns
   - Manual review of guide file content
   - Test prompt execution
   - Verify example commands work

#### Risk Mitigation
- **Broken Links:** Comprehensive grep search before and after
- **Context Confusion:** Clear documentation of Phase vs File numbering
- **Incomplete Migration:** Checklist of all files requiring updates
- **Reference Ambiguity:** Search for `nn` as word boundary to avoid false matches in content

#### Testing Approach
1. Execute each prompt from prompt.ai-project.system.md
2. Verify files created follow nnn pattern
3. Confirm guide cross-references work
4. Validate that legacy nn references don't exist in critical paths

### Cross-Slice Dependencies
**None** - This slice is foundational infrastructure that affects file naming conventions. Future slices will benefit from the updated system but do not depend on this work to begin.

### Technical Decisions

#### Decision: 3-digit vs 2-digit Indexing
**Rationale:**
- Provides 1000 index values (000-999) vs 100 (00-99)
- Supports semantic range allocation (0xx = process, 1xx = architecture, etc.)
- Better visual alignment in directory listings
- Clearer separation of concerns through range semantics
- Future-proof for project growth

**Trade-offs:**
- Requires migration of existing files
- Slightly more verbose file names
- Benefits: Improved organization, semantic clarity, expansion room

#### Decision: Preserve Numeric Values During Migration
**Rationale:**
- Maintains semantic meaning (00 = foundation/core → 000 = foundation/core)
- Reduces cognitive overhead (Phase 1 maps to guide 001)
- Simplifies migration (predictable transformation)
- Historical continuity maintained

#### Decision: Range-Based Semantic Structure
**Rationale:**
- Clear purpose for each numeric range
- Self-documenting file purposes from index alone
- Supports sorting and filtering by purpose
- Enables tooling to operate on ranges (e.g., "show all architecture docs")

**Range Design Principles:**
- Low numbers (0xx) = meta/process
- Mid numbers (2xx-7xx) = active work
- High numbers (8xx-9xx) = features and maintenance
- Provide expansion room in each range

#### Decision: Maintain Phase Numbering as Human-Readable
**Rationale:**
- "Phase 1", "Phase 2" are conversational and intuitive
- File references use technical precision (001, 002)
- Separation of concerns: process (Phase n) vs files (nnn)
- Preserves existing mental models while improving file organization

### Success Criteria

1. **File Migration Complete**
   - All guide.ai-project.nn-*.md renamed to guide.ai-project.nnn-*.md
   - No broken file references in any markdown files
   - Git history preserved through git mv operations

2. **System Prompts Updated**
   - All nn patterns replaced with nnn in prompt.ai-project.system.md
   - Example file paths use 3-digit indices
   - Prompt execution creates correctly-named files

3. **Documentation Updated**
   - file-naming-conventions.md contains index range schema
   - Examples throughout documentation use 3-digit system
   - Clear explanation of Phase vs File numbering distinction

4. **Verification Clean**
   - Grep search for `\bnn[-.]` patterns returns no guide file references
   - All internal cross-references functional
   - No obsolete 2-digit guide files remain

5. **Consistency Achieved**
   - Project-specific files in private/ follow nnn pattern
   - New slices and tasks numbered in appropriate ranges (100-799)
   - Architecture files in 050-089 range
   - Maintenance files in 900 range

### Notes and Considerations

**Important:** This slice involves systematic changes across many files. The intricate interdependency of the system means errors can propagate. Execute changes methodically with verification at each step.

**Scope Boundary:** This slice addresses file naming and indexing only. It does not modify:
- Actual process methodology or phase definitions
- Content within guides (except cross-references)
- Functionality of prompts (only file name patterns)

**Future Impact:** All subsequent slices and work items will benefit from clearer semantic organization and expansion room provided by the 3-digit index system with range allocation.
