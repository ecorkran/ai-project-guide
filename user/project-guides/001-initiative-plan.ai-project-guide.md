---
docType: initiative-plan
layer: project
project: ai-project-guide
source: none
dateCreated: 20261011
dateUpdated: 20261011
status: in_progress
---

# Initiative Plan: ai-project-guide

## Source
None. This project has no concept document. The plan was written after the fact from the existing documents in `user/architecture/` and `user/slices/`, so there is somewhere to put new initiatives.

## Index Convention
10-based (100, 110, 120). The existing work already uses this gap, and initiatives in this project are small.

## Initiatives

1. [x] **(100) Guide Foundations** — Early restructuring of the guide: prompt optimization (slice 100) and the move from subtree to submodule plus the private → user rename (slice 105). Done before initiative plans existed, so it has no architecture document. Dependencies: None (foundation). Status: complete
2. [x] **(110) Schema and Phases Update** — Canonical YAML frontmatter schemas per docType, phase renumbering, the Initiative Plan phase, and analysis skill extraction. [110-arch.schema-and-phases-update.md](../architecture/110-arch.schema-and-phases-update.md). Dependencies: [100]. Status: complete
3. [ ] **(120) Guide Tooling** — The scripts the guide ships and runs in consumer projects (setup-ide first), and the test and lint setup needed to change them safely. [120-arch.guide-tooling.md](../architecture/120-arch.guide-tooling.md). Dependencies: None. Status: in_progress

<!-- Status takes only: not_started | in_progress | complete | deferred | deprecated -->

## Cross-Initiative Dependencies
- 110 depends on 100: the schema and phase work edits the guide layout that 100 set up.
- 120 has no blocking dependencies. setup-ide installs the rules and frontmatter conventions defined by earlier work, but only copies them.

## Notes
- Indices are tentative and may be reassigned as initiatives are added or reorganized.
- New initiatives discovered during development are added here with the next available base index.
- `user/` is export-ignored, so none of these planning documents ship in release tarballs.
