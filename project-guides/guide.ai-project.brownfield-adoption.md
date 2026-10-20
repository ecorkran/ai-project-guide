---
layer: process
phase: 0
phaseName: brownfield-adoption
guideRole: supplemental
audience: [human, ai]
description: How to adopt an existing codebase that has no planning artifacts into the slice-based process.
dependsOn: [guide.ai-project.process.md, guide.ai-project.000-concept.md]
dateUpdated: 20261020
---

This guide covers adopting an existing codebase into the process described in `guide.ai-project.process`. If you do not have access to the process guide, stop and request it from the Project Manager.

### When This Applies

A project is **brownfield** when the code exists but it has no concept, architecture, or slice plan from this process. A repository that already has those artifacts is not brownfield: register it and continue from where it left off.

### Purpose

Recover the planning artifacts from what is already built, so new work can use the normal phases. Adoption produces three artifacts, in order:

1. **Baseline concept** (`000-concept.{project}.md`) — what the project is and why, in the structure of `guide.ai-project.000-concept`.
2. **Architecture, reverse-engineered** — the system as built: components, boundaries, data flow, external dependencies, and the conventions the code follows.
3. **Existing-state slice plan** — the built work grouped into slices, recorded as retroactive completed slices, followed by the PM's next work as normal unbuilt slices.

After these exist, the project continues with the normal phases (slice design, task breakdown, implementation).

### How It Is Run

The Brownfield Adoption prompt in `prompt.ai-project.system` drives the work and owns the step-by-step procedure, including whether to use squadron's graph-based analysis or to work from the repo alone. This guide does not repeat those steps.

### Rules

- **Never fabricate intent.** Why the project exists, who it is for, and what it was meant to become come from the repo's own prose (README, docs, comments) or from the PM. Otherwise mark it unknown and ask. Describing what the code does is analysis; describing what it was meant to do is intent.
- **Machine-derived content is confirmed.** A concept carrying a provenance block or `[INFERRED]` markers was derived by a tool. The PM confirms or corrects it before anything builds on it.
- **Never overwrite an existing artifact** without the PM saying so.
- **Contradictions are recorded, not resolved by guessing.** Where the code disagrees with the concept or its own docs, record both and ask the PM which is intended.

### Retroactive Slices

Built work is recorded as retroactive completed slices. A retroactive slice:

- counts as complete for every "done" check;
- is never treated as reviewed, because no review took place;
- is never the PM-only review exemption.

The marker that identifies a retroactive slice is defined by Context Forge. Its format is not yet specified in this guide; do not invent one.
