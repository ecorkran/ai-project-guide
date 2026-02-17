---
description: General coding rules and project structure guidelines for AI-assisted development
globs: 
alwaysApply: true
---

# General Coding Rules

## Meta-Guide: Guide to the rules
- If the first item in a list or sublist is in this file `enabled: false`, ignore that section.

## Guiding Behavior
* Always resist adding complexity.  Ensure that it is truly necessary and adds significant value.
* Never use silent fallback values.
* Never use cheap "hacks" or well-known anti-patterns to a solution.

## Project Structure
- Always refer to `guide.ai-project.000-process` and follow links as appropriate.
- For UI/UX tasks, always refer to `guide.ui-development.ai`.
- General Project guidance is in `project-documents/ai-project-guide/project-guides/`.
- Relevant 3rd party tool information is in `project-documents/ai-project-guide/tool-guides/`.

### Project-Specific File Locations
- **Regular Development** (template instances): Use `project-documents/user/` for all project-specific files.
- **Monorepo Template Development** (monorepo active): Use `project-artifacts/` for project-specific files (use directly, e.g. `project-artifacts/` not `project-artifacts/user/`).
- **DEPRECATED**: `{template}/examples/our-project/` is no longer used - migrate to `project-artifacts/` for monorepo work.

## General Guidelines (IMPORTANT)
- Filenames for project documents may use ` ` or `-` separators. Ignore case in all filenames, titles, and non-code content.  Reference `file-naming-conventions`.
- Use checklist format for all task files.  Each item and subitem should have a `[ ]` "checkbox".
- After completing a task or subtask, make sure it is checked off in the appropriate file(s).  Use the task-check subagent if available.
- Keep 'success summaries' concise and minimal -- they burn a lot of output tokens.
- **Preserve User-Provided Concept sections** - When editing project documents (concept, spec, feature, architecture, slice designs), NEVER modify or remove sections titled "## User-Provided Concept". These contain the human's original vision and must be preserved exactly as written. You may add new sections or edit AI-generated sections, but user concept sections are sacred.
- never include usernames, passwords, API keys, or similar sensitive information in any source code or comments.  At the very least it must be loaded from environment variables, and the .env used must be included in .gitignore.  If you find any code in violation of this, you must raise an issue with Project Manager.

## Document Standards
- **All markdown files must include YAML frontmatter.** Minimum: `docType` field. See `file-naming-conventions` for full metadata spec.
- **Dates in YAML**: Use `YYYYMMDD` format (no dashes). Example: `dateCreated: 20260217`
- **Document naming**: Use periods (`.`) as primary separators, hyphens (`-`) for secondary grouping: `[document-type].[subject].[additional-info].md`
- **3-digit index system (000-999)**: Files use indices for lineage tracing and categorization. Related documents share a base index. See `file-naming-conventions` for reserved ranges and initiative-based numbering.
  - 000-009: Core process guides
  - 050-099: Project-level architecture
  - 100-799: Initiative working space (claim base at increments of 10)
  - 900-999: Operational (reviews, analysis, maintenance)
- **File size limits**: Target ~350 lines for non-architecture project documents. If a file exceeds this by >33% (~465 lines), split using `-1.md`, `-2.md` suffix convention.
- **Living Document Pattern**: Human and AI collaborate on a single evolving file. Sections titled `## User-Provided Concept` are sacred and must never be modified by AI. See `guide.ai-project.000-process` for details.
- **Modular rules**: Additional platform-specific rules may exist in `project-guides/rules/`. Consult if working in a technology not covered by the rules loaded here.

## MCP (Model Context Protocol)
- Always use context7 (if available) to locate current relevant documentation for specific technologies or tools in use.
- Do not use smithery Toolbox (toolbox) for general tasks. Project manager will guide its use.

## Code Structure
- Keep code short; commits semantic.
- Keep source files to max 300 lines (excluding whitespace) when possible.
- Keep functions & methods to max 50 lines (excluding whitespace) when possible.
- Avoid hard-coded constants - declare a constant.
- Avoid hard-coded and duplicated values -- factor them into common object(s).
- Provide meaningful but concise comments in _relevant_ places.
- **Never use silent fallback values** - If a parameter/property fails to load, fail explicitly with an error or use an obviously-placeholder value (e.g., "ERROR: Failed to load", "MISSING_CONFIG"). Silent fallbacks that look like real data (e.g., `text || "some default text"`) make debugging nearly impossible. Use assertions, throw exceptions, or log errors instead.

## File and Shell Commands
- When performing file or shell commands, always confirm your current location first.

## Builds and Source Control
- After all changes are made, ALWAYS build the project.
- If available, git add and commit *from project root* at least once per task (not per child subitem)

- Log warnings to `project-documents/user/tasks/950-tasks.maintenance.md`. Write in raw markdown format, with each warning as a list item, using a checkbox in place of standard bullet point. Note that this path is affected by `monorepo active` mode.