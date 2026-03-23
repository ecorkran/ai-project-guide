---
docType: index
layer: process
audience: [human, ai]
description: Quick reference and navigation for AI Project Guide methodology files
dateUpdated: 20260214
---

# Project Guides Index

Quick reference and navigation for AI Project Guide methodology files.

> **For usage documentation**, see [main readme](../readme.md). This index is for navigating the guide files themselves.

## Core Process Guides

| Phase                | Primary guide                          | Quick link                                                                   |
| -------------------- | -------------------------------------- | ---------------------------------------------------------------------------- |
| Meta                 | AI Project Process                     | [guide.ai-project.process.md](guide.ai-project.process.md)                          |
| 0 – Concept          | Concept Guide                          | [guide.ai-project.000-concept.md](guide.ai-project.000-concept.md)                   |
| 1 – Initiative Plan  | Initiative Plan Guide                  | [guide.ai-project.001-initiative-plan.md](guide.ai-project.001-initiative-plan.md)   |
| 2 – Architecture     | _see Process Guide & System Prompts_   | [guide.ai-project.process.md](guide.ai-project.process.md)                          |
| 3 – Slice Planning   | Slice Planning Guide                   | [guide.ai-project.003-slice-planning.md](guide.ai-project.003-slice-planning.md)     |
| 4 – Slice Design     | Slice Design Guide                     | [guide.ai-project.004-slice-design.md](guide.ai-project.004-slice-design.md)         |
| 5 – Task Breakdown   | Task Breakdown Guide                   | [guide.ai-project.005-task-breakdown.md](guide.ai-project.005-task-breakdown.md)     |
| 5v – Task Expansion  | Task-Expansion Guide (optional)        | [guide.ai-project.005-variant-task-expansion.md](guide.ai-project.005-variant-task-expansion.md) |
| 6 – Execution        | _see Process Guide_                    | [guide.ai-project.process.md](guide.ai-project.process.md)                          |
| 7 – Integration      | _see Process Guide_                    | [guide.ai-project.process.md](guide.ai-project.process.md)                          |

## Supplemental Guides (90+)

| Guide                    | Purpose                                  | Quick link                                                                   |
| ------------------------ | ---------------------------------------- | ---------------------------------------------------------------------------- |
| Code Review              | Systematic code review processes         | [guide.ai-project.090-code-review.md](guide.ai-project.090-code-review.md)           |
| Legacy Task Migration    | Migrate old projects to current structure | [guide.ai-project.091-legacy-task-migration.md](guide.ai-project.091-legacy-task-migration.md) |

## Additional Resources

| Resource                 | Purpose                                  | Quick link                                                                   |
| ------------------------ | ---------------------------------------- | ---------------------------------------------------------------------------- |
| System Prompts           | Parameterized prompt templates           | [prompt.ai-project.system.md](prompt.ai-project.system.md)                         |
| UI Development           | UI/UX specific guidance                  | [guide.ui-development.ai.md](guide.ui-development.ai.md)                           |
| Onboarding Notes         | Human developer onboarding               | [notes.ai-project.onboarding.md](notes.ai-project.onboarding.md)                   |
| Code Review Crawler      | Automated code review prompt             | [prompt.code-review-crawler.md](prompt.code-review-crawler.md)                     |
| Migration Guides         | Version-specific migration instructions  | [migrations/](migrations/)                                                         |

## Agents & Rules

| Resource                 | Purpose                                  | Location                                                                     |
| ------------------------ | ---------------------------------------- | ---------------------------------------------------------------------------- |
| Agents (Claude Code)     | Specialized agent definitions            | [agents/](agents/)                                                                 |
| Rules                    | IDE-specific coding rules                | [rules/](rules/)                                                                   |

## IDE Integration

Use the `setup-ide` script to copy rules to your IDE:

```bash
# From project root
./project-documents/ai-project-guide/scripts/setup-ide cursor
./project-documents/ai-project-guide/scripts/setup-ide windsurf
./project-documents/ai-project-guide/scripts/setup-ide claude
```

This copies `agents/` and `rules/` to your IDE's configuration directory.

## For Guide Authors

When creating new guides in this directory, use this YAML frontmatter schema:

| Key           | Type   | Required | Values / Notes                                                                  |
| ------------- | ------ | -------- | ------------------------------------------------------------------------------- |
| `layer`       | enum   | ✓        | Always **`process`** in this folder                                             |
| `phase`       | int    | ✓        | `0`=meta, `1`-`8`=workflow phases, `90+`=supplemental guides                    |
| `phaseName`   | string | ✓        | `meta`, `concept`, `spec`, `slice-planning`, `slice-design`, etc.               |
| `guideRole`   | enum   | ✓        | `primary`, `support`, `onboarding`                                              |
| `audience`    | list   | ✓        | `human`, `ai`, `pm`                                                             |
| `description` | string | ✓        | One-line summary                                                                |
| `dependsOn`   | list   | –        | Other guide filenames this depends on                                           |
| `dateCreated` | int    | –        | YYYYMMDD format, immutable once set                                             |
| `dateUpdated` | int    | –        | YYYYMMDD format, update on modification                                         |
