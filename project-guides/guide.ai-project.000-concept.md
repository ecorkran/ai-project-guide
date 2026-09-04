---
layer: process
phase: 0
phaseName: concept
guideRole: primary
audience: [human, ai]
description: How to create a Phase 0 Concept document.
dependsOn: [guide.ai-project.process.md]
dateUpdated: 20260904
---

This guide covers creating a Phase 0 Concept document as described in `guide.ai-project.process`. If you do not have access to the process guide, stop and request it from the Project Manager.

### Purpose

The concept document captures what we're building, why, and the initial technical direction. It is the lightest-weight planning artifact — enough to anchor Phase 2 (Architecture) without over-committing to details that belong in later phases.

**Phase 0 Outcome** (from process guide): _A short doc describing the problem, target users, overall solution approach, and initial technology direction._

### How It's Created

Concept documents follow the **Living Document Pattern** described in the process guide. The typical flow:

1. **PM describes the project** — usually conversationally, sometimes as a starter document. Either works.
2. **AI asks clarifying questions** — do not assume or guess. This is especially important at the concept stage where ambiguity is highest and early misunderstandings compound through later phases.
3. **AI researches and/or runs small experiments before finalizing the Refined Concept** — do not rely solely on Q&A with the PM, and do not settle for what the model already assumes it knows. When the concept touches a domain with established techniques, standards, or prior art (e.g. color-contrast models, auth approaches, data-sync strategies), look them up and/or prototype a quick spike before writing the Refined Concept. Genuinely reconsider the concept in light of what's found — bring back concrete options with tradeoffs instead of picking one silently, rubber-stamping an assumption, or leaving it unexamined. Cite sources with verifiable URLs, and re-check each URL *after* writing it to confirm it resolves and says what the surrounding text claims. This is proactive — do it even if the PM didn't ask for it.
4. **Separate findings from decisions.** Research output belongs in the document as *what we learned and what the options are*. Anything that narrows scope, picks a subset, or commits to an approach is a **decision the PM makes** — surface it as a recommendation with reasoning and *ask*, don't quietly write it in as settled. When in doubt about whether something is a finding or a decision, ask.
5. **Together they produce the concept document** — the PM's original vision is preserved in the User-Provided Concept section; the AI adds structured analysis as the Refined Concept.
6. **Iterative refinement** — both continue to evolve the document as understanding develops.

### Document Structure

See `file-naming-conventions.md` for the canonical YAML schema reference.

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

### Open Questions / Research Needed
Questions that are **genuinely blocked** — waiting on a decision, on
access you don't have, or on context that only exists later.

This is not a to-do list for research you could do now. If a
question can be answered by reading a spec or running a short
script, answer it before writing this section, and record the
finding instead of the question. Name specific candidate
approaches (never just "needs research") and cite sources with
verifiable URLs.
```

Not every section needs substantial content. A small utility project might have a one-liner for Target Users and nothing for Development Approach. Scale to fit.

### Guidelines

- **Keep it high-level.** Architecture, component boundaries, and API design belong in Phase 2. If you're drawing system diagrams, you've gone too far.
- **Capture decisions and constraints, not solutions.** "Must run on GCP" is concept-level. "Use Cloud Run with a Redis sidecar" is architecture-level.
- **Flag unknowns explicitly.** It's better to say "platform TBD pending cost analysis" than to leave it out.
- **Do independent research before finalizing, not just Q&A.** If the concept depends on a technique or standard that already has established prior art, look it up — or run a tiny experiment — rather than asking the PM to supply the answer or silently assuming one. Surface what you found as named options in Open Questions / Research Needed, even if the PM never explicitly asked for research.
- **Do the research now, not "in Phase 2".** Deferring is the default failure mode, because "Open Questions / Research Needed" looks like a legitimate place to park work. Before writing a question there, ask: *could I answer this right now with a web search or a twenty-line script?* If yes, do it — the phase you are in does not make the answer harder to get, and an unexamined assumption compounds through every later phase. Reserve that section for questions genuinely blocked on a decision or on information that does not yet exist.
- **Never make a scoping decision on the PM's behalf.** Research tells you what the options *are*; choosing among them (which subset to build, which approach to commit to, what to leave out) is the PM's call. Present a recommendation with reasoning and then ask. A finding written as though it were settled is the single easiest way to smuggle an unreviewed decision into a project.
- In general, favor simplicity and avoid over-engineering. Use industry-standard solutions where practical and available.

### Output Location

Save as `000-concept.{project}.md` in the `user/project-guides/` directory.
