---
docType: slice-design
slice: {slice-name}
project: {project}
parent: {path to the slice plan this slice comes from}
dependencies: [list-of-prerequisite-slices]
interfaces: [list-of-slices-that-depend-on-this]
dateCreated: YYYYMMDD
dateUpdated: YYYYMMDD
status: not_started
---

<!--
TEMPLATE for Phase 4 slice designs. Canonical section schema for
`scripts/validate-slice-design`. Guidance: guide.ai-project.004-slice-design.

How to use:
- Copy this file to user/slices/nnn-slice.{slice-name}.md and substitute
  every {placeholder}. Do not copy frontmatter from a sibling design.
- A heading followed by `<!-- required -->` must appear in the finished
  document, at the same level, with the same text.
- A heading followed by `<!-- optional: ... -->` may be omitted entirely
  when the stated condition applies. Omit; do not fill with boilerplate.
- Level-3 headings without a marker are guidance. Rename, replace, or drop
  them as the design needs.
- Delete these marker comments and the bullet prompts from the finished
  document.
-->

# Slice Design: {slice-name}
<!-- required -->

## Overview
<!-- required -->
Brief description of what this slice delivers and why it matters.

## Value
<!-- required -->
What does this slice deliver? This may be user-facing functionality, developer-facing improvements (testability, reduced complexity), or architectural enablement (unblocking subsequent slices). Describe how the target audience benefits.

## Technical Scope
<!-- required -->
What components, features, and functionality are included in this slice? What is explicitly excluded?

## Dependencies
<!-- required -->
### Prerequisites
- Foundation work or other slices that must be complete
- External services, APIs, or packages required

### Interfaces Required
- What this slice needs from other parts of the system
- Data contracts and API dependencies
- Shared components or utilities needed

## Architecture
<!-- required -->
### Component Structure
- Main components or modules in this slice
- How they interact with each other
- Where they fit in the overall system

### Data Flow
- How data moves through this slice
- Input sources and output destinations
- Data transformations and processing

### State Management
- What state this slice manages
- How state is persisted or shared
- State update patterns and flows

## Technical Decisions
<!-- required -->
### Technology Choices
- Specific libraries, frameworks, or tools
- Rationale for technical choices
- Alternatives considered and rejected

### Patterns and Conventions
- Code organization patterns
- Naming conventions specific to this slice
- Error handling approaches

## Implementation Details
<!-- optional: omit only when no subsection below applies to this slice -->
### Migration Plan
For migration and refactoring slices.
- What is being moved, extracted, or restructured
- Source and destination locations
- Consumers that must be updated
- Data migration strategy (if state/storage is affected)
- Verification that behavior is preserved

### API Contracts
- Endpoints or tool interfaces this slice provides
- Request/response formats
- Authentication and authorization

### Database / Storage Schema
- Tables, collections, or storage structures this slice requires
- Relationships to existing data
- Migration considerations

### UI Specifications
- Component hierarchy and layout
- Interaction patterns and user flows
- Accessibility requirements
- Responsive design considerations

## Integration Points
<!-- required -->
### Provides to Other Slices
- What interfaces this slice exposes
- What functionality other slices can use
- Data or services this slice makes available

### Consumes from Other Slices
- What this slice expects from dependencies
- How failures or changes in dependencies are handled
- Fallback or degraded functionality approaches

## Success Criteria
<!-- required -->
### Functional Requirements
- Specific features or behaviors that must work
- Workflows that must be complete
- For migration slices: the system continues to work identically from a user perspective

### Technical Requirements
- Code quality standards
- Test coverage expectations
- Documentation requirements

### Integration Requirements
- What other slices can successfully integrate after this is complete
- System-wide functionality that works correctly
- End-to-end workflows that function

### Verification Walkthrough
<!-- required -->
This section bridges the gap between abstract success criteria and concrete proof of delivery. It should read like a short tutorial, not a test plan.

- What commands can be run? (with example invocations and expected output)
- What workflows become possible or testable end-to-end?
- How does the user confirm it works? (a step-by-step "demo script")

If a command doesn't exist yet, say so. If a workflow requires manual steps, list them.

## Risk Assessment
<!-- optional: omit for low-risk slices with no genuine, non-trivial risks -->
### Technical Risks
- Complex implementations or unknown territory
- External dependencies that might cause issues

### Mitigation Strategies
- How to reduce or manage identified risks
- Fallback plans for high-risk elements

## Implementation Notes
<!-- required -->
### Development Approach
- Suggested implementation order within this slice
- Testing strategy for this slice

### Special Considerations
- Unusual requirements or constraints
- Performance-critical sections
- Security considerations specific to this slice
