---
layer: process
phase: 4
phaseName: slice-design
guideRole: primary
audience: [human, ai]
description: Phase 4 playbook for creating detailed low-level designs for individual slices.
dependsOn:
  - guide.ai-project.000-process.md
  - guide.ai-project.002-spec.md
  - guide.ai-project.003-slice-planning.md
dateCreated: 20250101
dateUpdated: 20260121
---

#### Summary
This guide provides instructions for Phase 4: Slice Design (Low-Level Design). This phase takes an approved slice from the slice plan and creates a detailed technical design that can be converted into implementable tasks. The slice design serves as the technical blueprint for Phase 5 (Task Breakdown) and Phase 7 (Implementation).

#### Inputs and Outputs
**Inputs:**
* `guide.ai-project.000-process` (main process guide)
* `guide.ai-project.004-slice-design` (this document)
* Project specification (Phase 2 output): `user/project-guides/002-spec.{project}.md`
* High-level design (Phase 3 output): `user/architecture/050-arch.hld-{project}.md`
* Slice plan (Phase 3 output): `user/project-guides/003-slices.{project}.md`
* Relevant tool guides from `ai-project-guide/tool-guides/{tool}/`
* Framework guides from `ai-project-guide/framework-guides/{framework}/`

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
- Deliver meaningful functionality when complete

##### Implementation Readiness
The design should bridge the gap between high-level architecture and concrete tasks:
- Include specific technical decisions
- Reference exact tools, libraries, and patterns
- Provide mockups or detailed specifications for UI components
- Define data schemas and API contracts

#### Slice Design Structure

##### Document Template
```markdown
---
layer: project
docType: slice-design
slice: {slice-name}
project: {project}
dependencies: [list-of-prerequisite-slices]
interfaces: [list-of-slices-that-depend-on-this]
lastUpdated: YYYY-MM-DD
---

# Slice Design: {Slice Name}

## Overview
Brief description of what this slice delivers and why it matters.

## User Value
What specific user need does this slice address? How will users interact with it?

## Technical Scope
What components, features, and functionality are included in this slice?

## Dependencies
### Prerequisites
- Foundation work that must be complete
- Other slices that must be implemented first
- External services or APIs required

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

### State Management
- What state this slice manages
- How state is persisted or shared
- State update patterns and flows

## Technical Decisions
### Technology Choices
- Specific libraries, frameworks, or tools
- Rationale for technical choices
- Alternatives considered and rejected

### Patterns and Conventions
- Code organization patterns
- Naming conventions specific to this slice
- Error handling approaches

## Implementation Details
### API Contracts (if applicable)
- Endpoints this slice provides
- Request/response formats
- Authentication and authorization

### Database Schema (if applicable)
- Tables or collections this slice requires
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
- Specific features that must work
- User workflows that must be complete
- Performance or reliability targets

### Technical Requirements
- Code quality standards
- Test coverage expectations
- Documentation requirements

### Integration Requirements
- What other slices can successfully integrate
- System-wide functionality that works correctly
- End-to-end workflows that function

## Risk Assessment
### Technical Risks
- Complex implementations or unknown territory
- External dependencies that might cause issues
- Performance or scalability concerns

### Integration Risks
- Potential conflicts with other slices
- Assumptions about other slice implementations
- Coordination challenges

### Mitigation Strategies
- How to reduce or manage identified risks
- Fallback plans for high-risk elements
- Early validation approaches

## Implementation Notes
### Development Approach
- Suggested implementation order
- Key milestones or checkpoints
- Testing strategy for this slice

### Special Considerations
- Unusual requirements or constraints
- Performance-critical sections
- Security considerations specific to this slice
```

#### Slice Design Patterns

##### UI-Focused Slices
For slices that primarily deliver user interface:

###### Component Architecture
- Page/route components
- Shared UI components specific to this slice
- State management patterns (local vs global)
- Form handling and validation approaches

###### Design Specifications
- Mockups or wireframes for all major screens
- Interaction patterns and user flows
- Responsive design breakpoints
- Accessibility requirements (ARIA, keyboard navigation)

###### Data Integration
- How UI components fetch and display data
- Loading and error state handling
- Real-time update requirements

##### API-Focused Slices
For slices that primarily provide backend functionality:

###### Endpoint Design
- RESTful resource patterns or GraphQL schema
- Request/response formats with examples
- Error response formats and codes
- Rate limiting and authentication requirements

###### Business Logic
- Core algorithms or processing logic
- Data validation and transformation rules
- Integration with external services
- Background job or queue requirements

###### Data Layer
- Database schema changes or additions
- Query patterns and optimization considerations
- Caching strategies
- Data migration requirements

##### Full-Stack Feature Slices
For slices that include both UI and backend:

###### Integration Strategy
- How frontend and backend communicate
- Data synchronization patterns
- Error handling across the stack
- User feedback and loading states

###### Consistency Requirements
- Shared types or interfaces between frontend/backend
- Validation rules applied in both layers
- Security considerations across the stack

#### Common Design Decisions

##### Technology Integration
When incorporating new tools or libraries:
- Justify the choice based on slice requirements
- Document configuration and setup needs
- Identify potential conflicts with existing tech stack
- Plan for learning curve or training needs

##### Performance Considerations
For each slice, consider:
- Expected load and usage patterns
- Critical performance metrics
- Caching strategies
- Database query optimization needs

##### Security Requirements
Address security at the slice level:
- Authentication and authorization needs
- Data validation and sanitization
- Secure communication requirements
- Privacy and data protection considerations

#### Working with Dependencies

##### Managing Slice Dependencies
When a slice depends on another slice:
- Define exact interface requirements
- Specify fallback behavior if dependency fails
- Document version or contract expectations
- Plan for independent testing approaches

##### Foundation Dependencies
When depending on foundation work:
- Verify foundation work is complete and stable
- Document specific foundation features needed
- Identify gaps that might need additional foundation work

#### Quality Assurance

##### Design Review Checklist
Before approving a slice design:
- [ ] User value is clearly articulated
- [ ] Technical scope is well-defined and bounded
- [ ] Dependencies are identified and realistic
- [ ] Architecture supports the intended functionality
- [ ] Success criteria are specific and measurable
- [ ] Integration points are clearly defined
- [ ] Risks are identified with mitigation strategies
- [ ] Implementation approach is realistic for the team

##### Common Issues to Avoid
- **Scope Creep:** Keep slice focused on specific user value
- **Hidden Dependencies:** Ensure all dependencies are explicit
- **Over-Engineering:** Design for current needs, not hypothetical futures
- **Under-Specification:** Include enough detail for task creation
- **Integration Gaps:** Clearly define how this slice connects to others

#### Success Criteria
Phase 4 is complete when:
- [ ] Slice design document exists and follows the template
- [ ] Technical approach is detailed enough for task creation
- [ ] Dependencies and integration points are clearly defined
- [ ] UI mockups or API specifications are included as appropriate
- [ ] Success criteria are specific and measurable
- [ ] Risks are identified with mitigation strategies
- [ ] Project Manager and Technical Fellow approve the design

#### Next Steps
With approved slice design:
1. Proceed to Phase 5: Slice Task Breakdown
2. Convert design into granular, implementable tasks
3. Begin Phase 6: Task Enhancement and Expansion
4. Move to Phase 7: Slice Execution

The slice design serves as the technical contract for implementation and the reference point for all subsequent development work on this slice.