---
name: general-rules
description: Core project conventions for AI-assisted development.
alwaysApply: true
---

### Core Principles

- Always resist adding complexity. Ensure it is truly necessary.
- Never use silent fallback values. Fail explicitly with errors or obviously-placeholder values.
- Never use cheap hacks or well-known anti-patterns.
- Never include credentials, API keys, or secrets in source code or comments. Load from environment variables; ensure .env is in .gitignore. Raise an issue if violations are found.
- When debugging a failure, get the actual error message before attempting any fix. Never apply more than one speculative fix without first obtaining concrete evidence (logs, error text, stack trace) that diagnoses the root cause. If you cannot get the evidence yourself, ask the Project Manager for it.

### Code Structure

- Keep source files to ~300 lines, functions to ~50 lines (excluding whitespace) where practical.
- Program to interfaces (contracts).  Maintain clear separation between components.
- Do not duplicate logic.  Respect DRY (don't repeat yourself).
- Provide meaningful but concise comments in relevant places.

- Never scatter comparison values across code. If a value is used in conditionals, switch cases, or lookups, define it once (enum, constant, or config) and reference that definition everywhere. Changing a value should require editing exactly one place.
- Do not hard-code magic defaults.  In the example below, the defaults for model and n are both wrong.  If such defaults are needed they should be centralized at the config level.  This applies in all languages.
```python
  async def _model_start(promt:str) -> str {
    model = self._config.model or "gpt-5.3-codex"
    n = self._config.index or 1234
  }
```
- NEVER use user-accessible labels as logical structure.  They are fragile.

#### Exception Handling
- Every try/except must either: (a) re-raise after logging at ERROR level with logger.exception, (b) handle a specific exception with a comment explaining why swallowing is correct (e.g., ConnectionClosed: pass for normal teardown), or (c) be a top-level handler at a process boundary. Bare except: and except Exception: pass are bugs by definition.

### Source Control and Builds
- Keep commits semantic; build after all changes.
- Git add and commit from project root at least once per task.
- Confirm your current working directory before file/shell commands.

### Parsing & Pattern Matching
- Prefer lenient parsing over strict matching. A regex that silently fails on valid input (e.g. requiring exact whitespace counts or line-ending positions) is a bug. Parse the semantic content, not the formatting.
- When parsing structured text (YAML, key-value pairs, etc.), handle common format variations (compact vs multi-line, varying indent levels, trailing whitespace) rather than requiring one exact layout.
- When writing a parser, the test fixture must include the actual format that parser will consume in production.  A test that only passes on a format the real data never uses only provides false confidence.
- If a parser returns empty/default on bad input, add at least one test using real-world input (e.g. the actual file it will parse) to catch silent failures.
  
### Hallucination traps in prompts
If an instruction tells a reader to retrieve a value from some source, and
that source might return empty, do not place a hardcoded example of an
acceptable value nearby. When the source is empty, a model will reach for
the nearest plausible token — and the example is it. This is a
hallucination trap.

#### Bad

    Print the filename (from stderr, e.g. `squadron-P4.md`).

#### Good

    Print the filename. The CLI emits it on a line prefixed with
    `Using: ` on stderr. If no such line is present, stop with an error.


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
- After completing a task or subtask, delegate checklist updates to the `task-checker` agent rather than editing task files inline. This keeps the main agent's context focused on implementation. If task-checker is unavailable, check off tasks directly.
- Preserve sections titled "## User-Provided Concept" exactly as 
  written — never modify or remove.
- Keep success summaries concise and minimal.
