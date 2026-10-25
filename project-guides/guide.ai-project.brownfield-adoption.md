---
layer: process
phase: 0
phaseName: brownfield-adoption
guideRole: supplemental
audience: [human, ai]
description: How to adopt an existing codebase that has no planning artifacts into the slice-based process.
dependsOn: [guide.ai-project.process.md, guide.ai-project.000-concept.md]
dateUpdated: 20261025
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
- **Existing docs are linked, not moved.** Run `cf docs map` before writing the architecture. It generates `050-docs-map.{project}.md` (see `file-naming-conventions`), which links the README, `docs/` Markdown and ADRs where they live. The derived architecture links the docs map; it never copies or moves those docs.

### After Adoption

If the Adoption Facts list project rule files (CLAUDE.md, AGENTS.md, editor rule folders and similar), the project's own rules may conflict with the guide's. Offer the PM the Conventions Reconciliation prompt in `prompt.ai-project.system` (key `conventions-reconciliation`) as the closing step.

### Retroactive Slices

Built work is recorded as retroactive completed slices. A retroactive slice:

- counts as complete for every "done" check;
- is never treated as reviewed, because no review took place;
- is never the PM-only review exemption (`review: none`). The review gate skips it. Do not describe it as reviewed, cleared or exempt.

#### Marker

A retroactive slice is a slice plan entry written only by the adoption flow, in this form:

```markdown
1. [x] **(100) Existing System** `retroactive` — the system as built at adoption.
```

- The token is a backticked `retroactive` immediately after the closing `**` of the title, before the description. The backticks are required; a bare "retroactive" is ordinary prose. Case and whitespace are lenient. Context Forge strips the token from the description.
- Put the token after the title, never as a prefix. Squadron's plan parser needs `**(NNN)` right after the checkbox and would silently drop a prefixed entry.
- The entry must be checked `[x]`, must have an explicit `(NNN)` index, and must have no slice design and no task file. `cf check` reports each violation as an error. Work that gets a design or task file is new work, not retroactive.
- Retroactive entries precede all new work in index order. They start at the first initiative's base index, and the PM's new work continues the sequence after them. The derived architecture and slice plan take that same base index (`100-arch.{name}.md`, `100-slices.{name}.md`).
- One coarse entry for the whole system, as in the example above, is allowed. Use finer entries when the built work groups naturally.
- The derived architecture carries `provenance: derived` in its frontmatter. This is informational; it marks the document as reverse-engineered.
- `cf list slices --json` reports `retroactive: true` on these entries, with status `complete`.
