---
layer: process
phase: 4
phaseName: slice-design
guideRole: primary
audience: [human, ai]
description: Phase 4 playbook for creating detailed low-level designs for individual slices. Works with slices from project-level or architecture-level slice plans.
dependsOn:
  - guide.ai-project.000-process.md
  - guide.ai-project.003-slice-planning.md
dateCreated: 20250101
dateUpdated: 20260215
---

#### Summary
This guide provides instructions for Phase 4: Slice Design (Low-Level Design). This phase takes an approved slice from a slice plan and creates a detailed technical design that can be converted into implementable tasks. The slice design serves as the technical blueprint for Phase 5 (Task Breakdown) and Phase 7 (Implementation).

Slice designs are created for slices defined in either a project-level slice plan or an architecture-level slice plan. The process is the same; what varies is which documents provide context.

#### Inputs and Outputs

**Inputs:**

Slice design typically uses two levels of input:

* **Strategic context** — the document that provides the big-picture view of where this slice fits in the overall system. This is one of:
  * Project HLD (`user/architecture/050-arch.hld-{project}.md`)
  * Architecture document (`user/architecture/nnn-arch.{name}.md`)
  * Project specification (`user/project-guides/002-spec.{project}.md`)

* **Working input** — the slice plan entry that defines what this specific slice should accomplish. This is one of:
  * Project-level slice plan (`user/project-guides/003-slices.{project}.md`)
  * Architecture-level slice plan (`user/architecture/nnn-slices.{name}.md`)
  * Slice description provided directly by the Project Manager

The strategic context tells the agent *why this slice exists and how it relates to the whole*. The working input tells the agent *what this slice needs to deliver*. Both are typically needed; the strategic context may be skipped for simple or self-contained slices at the Project Manager's discretion.

**Additional inputs (as applicable):**
* `guide.ai-project.000-process` (process guide)
* `guide.ai-project.004-slice-design` (this document)
* Relevant tool guides from `ai-project-guide/tool-guides/{tool}/`
* Framework guides from `ai-project-guide/framework-guides/{framework}/`
* Prior slice designs if this slice depends on them

**Output:**
* Slice design document: `user/slices/nnn-slice.{slice-name}.md`

#### Core Principles

##### Technical Completeness
The slice design should contain enough technical detail that:
- Tasks can be created without guessing implementation approaches
- Integration points with other slices are clearly defined
- Technology choices are explicit and justified
- Success criteria are measurable and specific

##### Slice Independence
Each slice design should:
- Minimize dependencies on other slices
- Define clean interfaces where dependencies exist
- Be implementable and testable in isolation
- Leave the system in a working state when complete
- Deliver meaningful value (user-facing, developer-facing, or architectural)

##### Implementation Readiness
The design should bridge the gap between high-level architecture and concrete tasks:
- Include specific technical decisions
- Reference exact tools, libraries, and patterns
- Provide mockups or detailed specifications for UI components (if applicable)
- Define data schemas and API contracts (if applicable)

##### Appropriate Detail
- Include sections that are relevant to this slice. Omit sections that don't apply.
- A migration slice may not need UI Specifications or API Contracts. A UI slice may not need Database Schema. Use judgment.
- The template below is comprehensive; it is not a mandatory checklist. Every section marked "(if applicable)" should be included only when relevant.

#### Slice Design Structure

##### Document Template
```markdown
---
docType: slice-design
slice: {slice-name}
project: {project}
parent: {path to the slice plan this slice comes from}
dependencies: [list-of-prerequisite-slices]
interfaces: [list-of-slices-that-depend-on-this]
dateCreated: YYYYMMDD
dateUpdated: YYYYMMDD
---

# Slice Design: {Slice Name}

## Overview
Brief description of what this slice delivers and why it matters.

## Value
What does this slice deliver? This may be user-facing functionality, developer-facing improvements (testability, reduced complexity), or architectural enablement (unblocking subsequent slices). Describe how the target audience benefits.

## Technical Scope
What components, features, and functionality are included in this slice? What is explicitly excluded?

## Dependencies
### Prerequisites
- Foundation work or other slices that must be complete
- External services, APIs, or packages required

### Interfaces Required
- What this slice needs from other parts of the system
- Data contracts and API dependencies
- Shared components or utilities needed

## Architecture
### Component Structure
- Main components or modules in this slice
- How they interact with each other
- Where they fit in the overall system

### Data Flow
- How data moves through this slice
- Input sources and output destinations
- Data transformations and processing

### State Management (if applicable)
- What state this slice manages
- How state is persisted or shared
- State update patterns and flows

## Technical Decisions
### Technology Choices (if applicable)
- Specific libraries, frameworks, or tools
- Rationale for technical choices
- Alternatives considered and rejected

### Patterns and Conventions
- Code organization patterns
- Naming conventions specific to this slice
- Error handling approaches

## Implementation Details

### Migration Plan (for migration/refactoring slices)
- What is being moved, extracted, or restructured
- Source and destination locations
- Consumers that must be updated
- Data migration strategy (if state/storage is affected)
- Verification that behavior is preserved

### API Contracts (if applicable)
- Endpoints or tool interfaces this slice provides
- Request/response formats
- Authentication and authorization

### Database / Storage Schema (if applicable)
- Tables, collections, or storage structures this slice requires
- Relationships to existing data
- Migration considerations

### UI Specifications (if applicable)
- Component hierarchy and layout
- Interaction patterns and user flows
- Accessibility requirements
- Responsive design considerations

## Integration Points
### Provides to Other Slices
- What interfaces this slice exposes
- What functionality other slices can use
- Data or services this slice makes available

### Consumes from Other Slices
- What this slice expects from dependencies
- How failures or changes in dependencies are handled
- Fallback or degraded functionality approaches

## Success Criteria
### Functional Requirements
- Specific features or behaviors that must work
- Workflows that must be complete
- For migration slices: the system continues to work identically from a user perspective

### Technical Requirements
- Code quality standards
- Test coverage expectations
- Documentation requirements

### Integration Requirements (if applicable)
- What other slices can successfully integrate after this is complete
- System-wide functionality that works correctly
- End-to-end workflows that function

## Risk Assessment (if applicable)
Include only if there are genuine, non-trivial risks. Omit for low-risk slices.

### Technical Risks
- Complex implementations or unknown territory
- External dependencies that might cause issues

### Mitigation Strategies
- How to reduce or manage identified risks
- Fallback plans for high-risk elements

## Implementation Notes
### Development Approach
- Suggested implementation order within this slice
- Testing strategy for this slice

### Special Considerations (if applicable)
- Unusual requirements or constraints
- Performance-critical sections
- Security considerations specific to this slice
```

#### Slice Design Patterns

##### Feature Slices
For slices that deliver new functionality (UI, API, or full-stack):

**UI-focused:**
- Component hierarchy, page/route structure
- State management patterns (local vs global)
- Interaction patterns and user flows
- Design specifications, responsive breakpoints, accessibility

**API-focused:**
- Endpoint or tool interface design with request/response formats
- Business logic and validation rules
- Data layer (schema, queries, caching)
- External service integration

**Full-stack:**
- Integration strategy between frontend and backend
- Shared types or interfaces across layers
- Error handling and user feedback across the stack

##### Migration / Refactoring Slices
For slices that extract, move, or restructure existing code:

**Code Extraction:**
- Identify all source files being extracted and their destination
- Map every consumer (import) of the extracted code
- Define the update strategy: do consumers change their imports, or do re-exports maintain backward compatibility?
- Verify that the extracted code has no dependencies on the source environment (e.g., Electron APIs, browser globals)

**Storage Migration:**
- Old storage mechanism and new storage mechanism
- Data format mapping (if schema changes)
- One-time migration strategy for existing data
- Concurrent access considerations (if multiple processes may read/write)

**Dependency Restructuring:**
- Before and after dependency graphs
- Build configuration changes
- Impact on existing test suites

**Key constraint:** Every migration slice must leave the application in a working state. The design must explicitly describe how this is ensured — typically by verifying that all consumers are updated within the same slice.

#### Common Design Decisions

##### Technology Integration
When incorporating new tools or libraries:
- Justify the choice based on slice requirements
- Document configuration and setup needs
- Identify potential conflicts with existing tech stack

##### Working with Dependencies
When a slice depends on another slice:
- Define exact interface requirements
- Specify fallback behavior if dependency fails or isn't available
- Document contract expectations
- Plan for independent testing approaches

When depending on foundation work:
- Verify foundation work is complete and stable
- Document specific foundation features needed
- Identify gaps that might need additional foundation work

#### Quality Assurance

##### Design Review Checklist
Before approving a slice design:
- [ ] Value is clearly articulated (user, developer, or architectural)
- [ ] Technical scope is well-defined and bounded
- [ ] Dependencies are identified and realistic
- [ ] Architecture supports the intended functionality
- [ ] Success criteria are specific and measurable
- [ ] Integration points are clearly defined
- [ ] Migration slices explicitly ensure the system remains working
- [ ] Irrelevant template sections are omitted rather than filled with boilerplate
- [ ] Project Manager approves the design

##### Common Issues to Avoid
- **Scope Creep:** Keep slice focused on its defined value delivery
- **Hidden Dependencies:** Ensure all dependencies are explicit
- **Over-Engineering:** Design for current needs, not hypothetical futures
- **Under-Specification:** Include enough detail for task creation
- **Integration Gaps:** Clearly define how this slice connects to others
- **Template Stuffing:** Don't fill in sections just because they exist in the template; omit what doesn't apply
- **Broken Intermediate State:** Migration slices that leave consumers pointing at moved code without updating imports

#### Success Criteria
Phase 4 is complete when:
- [ ] Slice design document exists with proper frontmatter
- [ ] Technical approach is detailed enough for task creation
- [ ] Dependencies and integration points are clearly defined
- [ ] Relevant specifications are included (UI, API, migration plan, etc.)
- [ ] Success criteria are specific and measurable
- [ ] Migration slices describe how the system remains working throughout
- [ ] Project Manager and Technical Fellow approve the design

#### Next Steps
With approved slice design:
1. Proceed to Phase 5: Slice Task Breakdown
2. Convert design into granular, implementable tasks
3. Begin Phase 6: Task Enhancement and Expansion
4. Move to Phase 7: Slice Execution

The slice design serves as the technical contract for implementation and the reference point for all subsequent development work on this slice.
