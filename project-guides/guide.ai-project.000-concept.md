---
layer: process
phase: 0
phaseName: concept
guideRole: primary
audience: [human, ai]
description: How to create a Phase 0 Concept document.
dependsOn: [guide.ai-project.process.md]
dateUpdated: 20260323
---

This guide covers creating a Phase 0 Concept document as described in `guide.ai-project.process`. If you do not have access to the process guide, stop and request it from the Project Manager.

### Purpose

The concept document captures what we're building, why, and the initial technical direction. It is the lightest-weight planning artifact — enough to anchor Phase 2 (Architecture) without over-committing to details that belong in later phases.

**Phase 0 Outcome** (from process guide): _A short doc describing the problem, target users, overall solution approach, and initial technology direction._

### How It's Created

Concept documents follow the **Living Document Pattern** described in the process guide. The typical flow:

1. **PM describes the project** — usually conversationally, sometimes as a starter document. Either works.
2. **AI asks clarifying questions** — do not assume or guess. This is especially important at the concept stage where ambiguity is highest and early misunderstandings compound through later phases.
3. **Together they produce the concept document** — the PM's original vision is preserved in the User-Provided Concept section; the AI adds structured analysis as the Refined Concept.
4. **Iterative refinement** — both continue to evolve the document as understanding develops.

### Document Structure

```yaml
---
layer: project
phase: 0
phaseName: concept
guideRole: primary
audience: [human, ai]
description: Concept for {project}
dependsOn: []
dateCreated: YYYYMMDD
dateUpdated: YYYYMMDD
status: in_progress
---
```

```markdown
# {Project Name}

## Overview
[One-sentence description of what this project is]

## User-Provided Concept
[PM's original concept — goals, vision, motivation, constraints]
[This section is SACRED — AI must preserve it during all edits]

## Refined Concept

### Problem & Motivation
What are we making? What problem does it solve? Why now?

### Target Users
Who uses it? How do they access it? Will the audience evolve?

### Solution Approach
High-level description of the approach. Where does it run?
What makes it distinct? Are we building the whole thing or a
specific component/layer?

If the project involves multiple capability areas or components,
name them here. These are not yet initiatives with indices or
sequencing — just the identified pieces that Phase 1 (Initiative
Plan) will later formalize. Example: "This project needs a
behavior engine, a world server, an environment layer, and
clients."

### Initial Technical Direction
Languages, frameworks, platforms — as much as is known.
Third-party dependencies worth noting early. This is directional,
not committal; detailed stack decisions belong in Phase 2.

### Development Approach
Methodology preferences (TDD, DDD, etc.), quality vs. speed
tradeoffs, any known constraints on how we'll work.
```

Not every section needs substantial content. A small utility project might have a one-liner for Target Users and nothing for Development Approach. Scale to fit.

### Guidelines

- **Keep it high-level.** Architecture, component boundaries, and API design belong in Phase 2. If you're drawing system diagrams, you've gone too far.
- **Capture decisions and constraints, not solutions.** "Must run on GCP" is concept-level. "Use Cloud Run with a Redis sidecar" is architecture-level.
- **Flag unknowns explicitly.** It's better to say "platform TBD pending cost analysis" than to leave it out.
- In general, favor simplicity and avoid over-engineering. Use industry-standard solutions where practical and available.

### Output Location

Save as `001-concept.{project}.md` in the `user/project-guides/` directory.
