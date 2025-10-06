---
layer: process
phase: 3
phaseName: slice-planning
guideRole: primary
audience: [human, ai]
description: Phase 3 playbook for breaking projects into manageable vertical slices.
dependsOn:
  - guide.ai-project.000-process.md
  - guide.ai-project.002-spec.md
---

#### Summary
This guide provides instructions for Phase 3: High-Level Design & Slice Planning. This phase takes the project specification and breaks it into manageable, independent slices that can be designed and implemented separately. This approach reduces complexity, improves context management, and enables future parallelization.

#### Inputs and Outputs
**Inputs:**
* `guide.ai-project.000-process` (this process guide)
* `guide.ai-project.003-slice-planning` (this document)
* Project concept document (Phase 1 output)
* Project specification (Phase 2 output)
* Any existing architecture documentation

**Output:**
* High-level design document: `private/architecture/050-arch.hld-{project}.md`
* Slice planning document: `private/project-guides/003-slices.{project}.md`

#### Core Principles

##### Slice Independence
Each slice should:
- Deliver meaningful user value on its own
- Have minimal dependencies on other slices
- Be completable in a single development context (1-2 weeks of work)
- Have clear interfaces with other parts of the system

##### Three Types of Work
All project work falls into these categories:

**Foundation Work**
- Must be completed before feature slices can begin
- Hard to split further (e.g., project setup, database schema, core architecture)
- Usually done first, in dependency order
- Examples: Next.js setup, authentication system, database design, core UI framework

**Independent Features**
- Can be implemented as vertical slices
- Deliver user-facing functionality
- Should be prioritized by user value and technical risk
- Examples: user registration, dashboard, reporting, search functionality

**Integration Work**
- Happens after feature slices are complete
- Focuses on performance, deployment, cross-feature concerns
- Examples: performance optimization, advanced analytics, deployment automation

#### Slice Planning Process

##### Step 1: Create High-Level Design
Document the overall system architecture in `private/architecture/050-arch.hld-{project}.md`:

```markdown
# High-Level Design: {Project}

## System Overview
- Brief description of the overall system
- Key architectural decisions
- Technology stack summary

## Major Components
- List main system components
- How they interact
- External dependencies

## Data Flow
- Key data flows through the system
- Integration points
- Storage considerations

## Infrastructure Requirements
- Hosting and deployment needs
- Performance considerations
- Security requirements
```

##### Step 2: Identify Foundation Work
List all work that must be completed before features can be built:
- Project initialization and configuration
- Core infrastructure (database, authentication, etc.)
- Shared UI components and design system
- Third-party integrations that affect multiple features

Order foundation work by dependencies.

##### Step 3: Define Feature Slices
For each major feature area:

**Slice Criteria:**
- Represents a complete user workflow
- Can be demonstrated independently
- Has clear success criteria
- Size: 1-2 weeks of development work maximum

**Slice Definition Template:**
```markdown
## Slice: {slice-name}
**User Value:** What user need does this address?
**Success Criteria:** How do we know it's complete?
**Dependencies:** What foundation work or other slices must be done first?
**Interfaces:** What APIs or contracts does this provide/consume?
**Risk Level:** Low/Medium/High based on technical complexity
```

Use as many slices as needed to fully capture the project's functionality and scope.  Use the Example Slice Breakdown to guide you.

##### Step 4: Plan Implementation Order
Order slices by:
1. **Dependencies:** Foundation work first, then slices in dependency order
2. **Testability:** Strive for early vertical slice testability.  Core first then expand.
3. **Risk:** High-risk slices earlier to surface problems
4. **User Value:** Most valuable features first within each risk tier
5. **Technical Learning:** Slices that teach you about the domain/tech stack

##### Step 5: Create Slice Sketches (Optional)
For complex projects, create brief design sketches for each slice to identify potential conflicts:
- Key technical decisions
- Database schema needs
- API contracts
- UI patterns

This helps catch "Slice A needs X but Slice B needs Y" conflicts early.

#### Example Slice Breakdown

**Project:** Trading Application

**Foundation Work:**
1. Next.js project setup with TypeScript, Tailwind
2. Database schema
3. Authentication system (Auth0)
4. Core UI components (Tailind, Radix, design system)

**Feature Slices:**
1. **User Dashboard** - Login, basic profile, navigation
2. **Market Data Display** - Real-time price charts and data
3. **Portfolio Management** - View holdings, track performance
4. **Trade Execution** - Buy/sell interface and order management
5. **Reporting** - Generate reports, export data

**Integration Work:**
- Performance optimization
- Advanced analytics
- Mobile responsiveness
- Deployment automation

#### Common Pitfalls

**Slices Too Large**
- If a slice feels overwhelming, split it further
- Aim for "demo-able in a week" size

**Hidden Dependencies**
- Slices that seem independent but share data models
- UI patterns that need to be consistent across slices
- Authentication/authorization that affects multiple slices

**Premature Optimization**
- Don't over-engineer slice boundaries
- Some duplication between slices is acceptable
- Perfect abstractions can wait until integration phase

#### Working with AI

**Technical Fellow Role:**
- Help identify logical slice boundaries
- Spot potential conflicts between slices
- Suggest alternative slice organizations
- Validate that slices are appropriately sized

**Common AI Questions:**
- "What would be the implications of combining these two slices?"
- "Are there any technical conflicts between these slice designs?"
- "Is this slice too large to complete in a single context?"
- "What foundation work is needed before this slice can begin?"

#### Output Format

Create two documents:

**High-Level Design** (`private/architecture/050-arch.hld-{project}.md`):
- System architecture overview
- Technology decisions
- Component interactions

**Slice Plan** (`003-slices.{project}.md`):
```markdown
# Slice Plan: {Project}

## Foundation Work
1. [ ] Foundation item 1
2. [ ] Foundation item 2

## Feature Slices (in implementation order)
1. [ ] **Slice Name** - Brief description, Dependencies: [list], Risk: Low/Med/High
2. [ ] **Next Slice** - Brief description, Dependencies: [list], Risk: Low/Med/High

## Integration Work
1. [ ] Integration item 1
2. [ ] Integration item 2

## Notes
- Key decisions made during planning
- Alternative approaches considered
- Open questions for later phases
```

#### Success Criteria
Phase 3 is complete when:
- [ ] High-level design document exists and is approved
- [ ] All work is categorized as Foundation/Feature/Integration
- [ ] Feature slices are appropriately sized (1-2 weeks each)
- [ ] Dependencies between slices are clearly identified
- [ ] Implementation order is logical and accounts for risk
- [ ] Each slice has clear success criteria
- [ ] Project Manager approves the slice plan

#### Next Steps
With approved slice plan:
1. For each feature slice: Phase 4 → Phase 5 → Phase 6 → Phase 7 → Phase 8
2. Complete integration work as needed
3. Iterate and add new slices as requirements evolve

This approach transforms overwhelming projects into manageable, independent chunks that can be tackled with confidence.