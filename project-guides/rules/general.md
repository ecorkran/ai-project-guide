---
name: general-rules
description: Core project conventions for AI-assisted development.
alwaysApply: true
---

### Core Principles

- Always resist adding complexity. Ensure it is truly necessary.
- Never use silent fallback values. Fail explicitly with errors or 
  obviously-placeholder values.
- Never use cheap hacks or well-known anti-patterns.
- Never include credentials, API keys, or secrets in source code 
  or comments. Load from environment variables; ensure .env is 
  in .gitignore. Raise an issue if violations are found.

### Code Structure

- Keep source files to ~300 lines, functions to ~50 lines 
  (excluding whitespace) where practical.
- Avoid hard-coded constants and duplicated values.
- Avoid "magic strings" where possible, prefer enums.
- Never use user-accessible labels as logical structure.  They are fragile.
- Program to interfaces (contracts).  Maintain clear separation between components.
- Do not duplicate logic.  Respect DRY (don't repeat yourself).
- Provide meaningful but concise comments in relevant places.

### Source Control and Builds
- Keep commits semantic; build after all changes.
- Git add and commit from project root at least once per task.
- Confirm your current working directory before file/shell commands.

## Parsing & Pattern Matching

- Prefer lenient parsing over strict matching. A regex that silently
  fails on valid input (e.g. requiring exact whitespace counts or
  line-ending positions) is a bug. Parse the semantic content, not
  the formatting.
- When parsing structured text (YAML, key-value pairs, etc.), handle
  common format variations (compact vs multi-line, varying indent
  levels, trailing whitespace) rather than requiring one exact layout.
- If a parser returns empty/default on bad input, add at least one
  test using real-world input (e.g. the actual file it will parse)
  to catch silent failures.
  
### Project Navigation

- Follow `guide.ai-project.process` and its links for workflow.
- Follow `file-naming-conventions` for all document naming and metadata.
- Project guides: `project-documents/ai-project-guide/project-guides/`
- Tool guides: `project-documents/ai-project-guide/tool-guides/`
- Modular rules for specific technologies may exist in 
  `project-guides/rules/`.

### Document Conventions

- All markdown files must include YAML frontmatter as specified in `file-naming-conventions.md`
- Use checklist format for all task files.  Each item and subitem should have a `[ ]` "checkbox".
- After completing a task or subtask, make sure it is checked off in the appropriate file(s).  Use the task-check subagent if available.- Preserve sections titled "## User-Provided Concept" exactly as 
  written — never modify or remove.
- Keep success summaries concise and minimal.
