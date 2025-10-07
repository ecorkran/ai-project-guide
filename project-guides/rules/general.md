---
description: General coding rules and project structure guidelines for AI-assisted development
globs: 
alwaysApply: true
---

# General Coding Rules

## Meta-Guide: Guide to the rules
- If the first item in a list or sublist is in this file `enabled: false`, ignore that section.

## Project Structure
- Always refer to `guide.ai-project.000-process` and follow links as appropriate.
- For UI/UX tasks, always refer to `guide.ui-development.ai`.
- General Project guidance is in `project-documents/ai-project-guide/project-guides/`.
- Relevant 3rd party tool information is in `project-documents/ai-project-guide/tool-guides/`.

### Project-Specific File Locations
- **Regular Development** (template instances): Use `project-documents/private/` for all project-specific files.
- **Monorepo Template Development** (monorepo active): Use `project-artifacts/` for project-specific files (use directly, e.g. `project-artifacts/` not `project-artifacts/private/`).
- **DEPRECATED**: `{template}/examples/our-project/` is no longer used - migrate to `project-artifacts/` for monorepo work.

## General Guidelines (IMPORTANT)
- Filenames for project documents may use ` ` or `-` separators. Ignore case in all filenames, titles, and non-code content.  Reference `file-naming-conventions`.
- Use checklist format for all task files.  Each item and subitem should have a `[ ]` "checkbox".
- After completing a task or subtask, make sure it is checked off in the appropriate file(s).  Use the task-check subagent if available.
- Keep 'success summaries' concise and minimal -- they burn a lot of output tokens.
* never include usernames, passwords, API keys, or similar sensitive information in any source code or comments.  At the very least it must be loaded from environment variables, and the .env used must be included in .gitignore.  If you find any code in violation of this, you must raise an issue with Project Manager.

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

- Log warnings to `/project-documents/private/tasks/950-tasks.maintenance.md`. Write in raw markdown format, with each warning as a list item, using a checkbox in place of standard bullet point. Note that this path is affected by `monorepo active` mode.