---
docType: reference
scope: project-wide
audience: [human, ai]
description: Canonical contract for where every guide, snippet, and asset lives
dateCreated: 20250117
dateUpdated: 20261011
---

# Directory Structure

_This file is the canonical contract for where every guide, snippet, and asset lives._

## Project Root Files

| File | Purpose |
|------|---------|
| `DEVLOG.md` | Lightweight, append-only development activity log. Newest entries first. Format: date headers (`## YYYYMMDD`) followed by 1-3 line notes per session. Essential for project continuity after breaks. |
| `CLAUDE.md` | AI development guidelines, code standards, project-specific rules. |
| `README.md` | Public-facing project documentation. |

## Directory Structure

```
project-documents/
├── ai-project-guide/        # Git submodule (framework guides)
│   ├── project-guides/      # project-process & meta-methodology
│   ├── framework-guides/    # app-level runtimes & platforms
│   │   └── nextjs/ …
│   ├── tool-guides/         # importable libraries / UI kits
│   │   └── scichart/ …
│   ├── api-guides/          # external data / service endpoints
│   │   └── usgs/ …
│   ├── domain-guides/       # cross-cutting subject knowledge
│   │   └── hydrology/ …
│   ├── snippets/            # copyable code/config examples
│   └── scripts/             # setup and utility scripts
└── user/                 # Your project-specific work (parent repo)
    ├── analysis/            # analysis & investigation (initiative index, or 900+ in order)
    ├── architecture/        # high-level designs & system architecture (050-089)
    ├── project-guides/      # project-specific guide customizations (001-009)
    │   ├── 000-concept.{project}.md # project concept documents
    │   ├── 002-spec.{project}.md    # project specifications
    │   └── 003-slices.{project}.md  # slice planning
    ├── reviews/             # slice reviews (slice index) & ad-hoc reviews (900-999)
    ├── slices/              # slice design documents (100-749)
    └── tasks/               # task breakdowns & all work items
        └── 9nn-tasks.standing-fixes.md # multi-step fixes (see rules/fixes.md)
```
> **Directory Structure:**
> - Your project work goes in `project-documents/user/`
> - Framework guides are in `project-documents/ai-project-guide/` (git submodule)
> - This is the standard structure shown above
>

## Zero-ambiguity decision matrix

| Ask in order | Folder |
|--------------|--------|
| Process / methodology? | `project-guides/` |
| Owns whole app lifecycle? | `framework-guides/` |
| External network API? | `api-guides/` |
| Importable library? | `tool-guides/` |
| Broad subject knowledge? | `domain-guides/` |

> **One-path rule:** a doc lives in exactly one folder.  
> **Metadata override:** if a file has YAML front-matter key `layer`, that wins if it contradicts the path.

#### Attachment policy
Put images in an `images/` folder next to the document that uses them, and link them with a relative path (e.g. `![alt text](images/diagram.png)`).  Give images descriptive names and alt text.
#### Snippets
* Process-wide prompts: `project-guides/prompt.ai-project.system.md`
* Ad-hoc code snippets and examples: `snippets/`
### Naming reminder
Follow the pattern `[doc-type].[subject].[info].md`. See `file-naming-conventions.md` for full details.

