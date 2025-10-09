# Project Guidelines for Claude

## General Development Rules

### Meta-Guide: Guide to the rules
- If the first item in a list or sublist is in this file `enabled: false`, ignore that section.

### Project Structure
- Always refer to `guide.ai-project.000-process` and follow links as appropriate.
- For UI/UX tasks, always refer to `guide.ui-development.ai`.
- General Project guidance is in `project-documents/ai-project-guide/project-guides/`.
- Relevant 3rd party tool information is in `project-documents/ai-project-guide/tool-guides/`.

#### Project-Specific File Locations
- **Regular Development** (template instances): Use `project-documents/user/` for all project-specific files.
- **Monorepo Template Development** (monorepo active): Use `project-artifacts/` for project-specific files (use directly, e.g. `project-artifacts/` not `project-artifacts/user/`).
- **DEPRECATED**: `{template}/examples/our-project/` is no longer used - migrate to `project-artifacts/` for monorepo work.

### General Guidelines (IMPORTANT)
- Filenames for project documents may use ` ` or `-` separators. Ignore case in all filenames, titles, and non-code content.  Reference `file-naming-conventions`.
- Use checklist format for all task files.  Each item and subitem should have a `[ ]` "checkbox".
- After completing a task or subtask, make sure it is checked off in the appropriate file(s).  Use the task-check subagent if available.
- Keep 'success summaries' concise and minimal -- they burn a lot of output tokens.
* never include usernames, passwords, API keys, or similar sensitive information in any source code or comments.  At the very least it must be loaded from environment variables, and the .env used must be included in .gitignore.  If you find any code in violation of this, you must raise an issue with Project Manager.

### MCP (Model Context Protocol)
- Always use context7 (if available) to locate current relevant documentation for specific technologies or tools in use.
- Do not use smithery Toolbox (toolbox) for general tasks. Project manager will guide its use.

### Code Structure
- Keep code short; commits semantic.
- Keep source files to max 300 lines (excluding whitespace) when possible.
- Keep functions & methods to max 50 lines (excluding whitespace) when possible.
- Avoid hard-coded constants - declare a constant.
- Avoid hard-coded and duplicated values -- factor them into common object(s).
- Provide meaningful but concise comments in _relevant_ places.

### File and Shell Commands
- When performing file or shell commands, always confirm your current location first.

### Builds and Source Control
- After all changes are made, ALWAYS build the project.
- If available, git add and commit *from project root* at least once per task (not per child subitem)

- Log warnings to `/project-documents/user/tasks/950-tasks.maintenance.md`. Write in raw markdown format, with each warning as a list item, using a checkbox in place of standard bullet point. Note that this path is affected by `monorepo active` mode.

## Python Development Rules

### Version & Type Hints

- Target Python 3.9+ exclusively (no 2.x or 3.7 compatibility)
- Use built-in types: `list`, `dict`, `tuple`, not `List`, `Dict`, `Tuple`
- Use `|` for union types: `str | None` not `Optional[str]` or `Union[str, None]`
- Type hint all function signatures and class attributes
- Use `from __future__ import annotations` when needed for forward references

### Code Style & Structure

- Follow PEP 8 with 88-character line length (Black formatter default)
- Use descriptive variable names, avoid single letters except in comprehensions
- Prefer f-strings over `.format()` or `%` formatting
- Use pathlib.Path for file operations, not os.path
- Dataclasses or Pydantic for data structures, avoid raw dicts for complex data
- One class per file for models/services, group related utilities

### Functions & Error Handling

- Small, single-purpose functions (max 20 lines preferred)
- Use early returns to reduce nesting
- Explicit exception handling, avoid bare `except:`
- Raise specific exceptions with meaningful messages
- Use context managers (`with`) for resource management
- Prefer `ValueError`, `TypeError` over generic `Exception`

### Modern Python Patterns

- Use `match/case` for complex conditionals (3.10+)
- Walrus operator `:=` where it improves readability
- Comprehensions over `map`/`filter` when clear
- Generator expressions for memory efficiency
- `itertools` and `functools` for functional patterns
- Enum for constants, not module-level variables

### Testing & Quality

- Write tests alongside implementation
- Use pytest, not unittest
- Fixtures for test data and dependencies
- Parametrize tests for multiple scenarios
- Mock external dependencies at boundaries
- Docstrings for public APIs (Google or NumPy style)
- Type check with mypy or pyright in strict mode

### Dependencies & Imports

- Use poetry for complex projects, uv for simple ones
- Pin direct dependencies, let tools resolve transitive ones
- Group imports: standard library, third-party, local
- Absolute imports for project modules
- Avoid wildcard imports except in `__init__.py`

### Async & Performance

- Use `async`/`await` for I/O operations
- asyncio or trio for concurrency, not threading
- Profile before optimizing
- functools.cache for expensive pure functions
- Prefer built-in functions and comprehensions for speed

### Security & Best Practices

- Never hardcode secrets or credentials
- Use environment variables or secret management
- Validate all external input
- Use parameterized queries for SQL
- Keep dependencies updated
- Use `secrets` module for tokens, not `random`

## React & Next.js Rules

### Components & Naming
- Use functional components with `"use client"` if needed.
- Name in PascalCase under `src/components/`.
- Keep them small, typed with interfaces.
- Use React, Tailwind 4, and Radix.  Do not use Shadcn

### React and Next.js Structure
- Use App Router in `app/`. 
- Skip auth unless and until it is needed.
- Use `.env` for secrets.

### Icons
- Prefer `lucide-react`; name icons in PascalCase.
- Custom icons in `src/components/icons`.

### Toast Notifications
- Use `react-toastify` in client components.
- `toast.success()`, `toast.error()`, etc.

### Tailwind Usage
- Always use tailwind 4, never tailwind 3.  If you see or use a tailwind.config.ts (or .ts), it's almost always wrong.  
- Use Tailwind (mobile-first, dark mode with dark:(class)). 
- For animations, prefer Framer Motion. 

###  Code Style
- Use `eslint` unless directed otherwise.
- Use `prettier` if working in languages it supports.

### File & Folder Names
- Routes in kebab-case (e.g. `app/dashboard/page.tsx`).
- Sort imports (external → internal → sibling → styles).

### Testing
- Prefer vitest over jest

### Builds
- use pnpm not npm
- After all changes are made, ALWAYS build the project with `pnpm build`. Allow warnings, fix errors.
- If a `package.json` exists, ensure the AI-support script block from `snippets/npm-scripts.ai-support.json` is present before running `pnpm build`

### Next.js
- Default to client components in server pages for Next.js
- NextAuth + Prisma for auth.

### Inngest / Background Jobs
- **enabled**: false
- Use `inngest.config.ts` for Inngest configuration.
- Use `src/app/api/inngest/route.ts` for Inngest API route.
- Use polling to update the UI when Inngest events are received, not trpc success response. 

## Code Review Rules

### Overview
This document outlines the comprehensive process for conducting code reviews. Code reviews ensure code quality, maintainability, and alignment with project goals while identifying potential issues before they become problematic. Specific guidelines are provided for project aspects (ex: UI) and platform specifics (ex: NextJS).

### Usage Modes
This guide supports two distinct code review scenarios:

#### 1. Single-File Code Review
- **Purpose**: Review a single provided source file
- **Scope**: Focus on one specific file or component
- **Process**: Apply the code review questionnaire to the individual file and create tasks as needed
- **Documentation**: Create a simple review document for the findings and a corresponding task file if issues are identified

#### 2. Directory Crawl Review
- **Purpose**: Systematically review an entire directory structure or project
- **Scope**: Process multiple files in a coordinated batch operation
- **Process**: Follow the full infrastructure guidelines below for organizing multiple review sessions
- **Documentation**: Use the structured directory approach with session tracking and comprehensive file accounting

The remainder of this guide provides detailed processes for both modes, with particular emphasis on the infrastructure needed for directory crawl reviews.

### Infrastructure Guidelines
Place reviews into the user/reviews/ directory. Note that 'private' path may be modified if we are working in a monorepo, as described in your guides and rules. If this is unclear or you cannot locate paths, STOP and confirm with Project Manager before proceeding.

#### For Directory Crawl Reviews
Create a subdirectory for each crawl session. Name the subdirectory using pattern review.{project}.yyyymmdd-nn.md. The -nn should be just a two digit number, start at 01.

This way you can keep tasks separated by file, without causing difficulty in file management, while keeping task files small enough that we can easily manage or even parallelize their implementation.

Keep count of files processed and remaining to be processed. Update this after each file, ideally storing in the review.{project}.{YYYYMMDD-nn}.md file. Use a single such review file for the entire session. Continue to create and keep separate asks files for each file reviewed.

For any file which generates no tasks, keep a list of such files in the aforementioned review document.

#### For Single-File Reviews
Create a simple review document named `review.{filename}.{YYYYMMDD}.md` and, if needed, a corresponding task file `tasks.code-review.{filename}.{YYYYMMDD}.md`.

### Code Review Questionnaire
When reviewing code, systematically answer these core questions.  
#### 1. Potential Bugs & Edge Cases
- Are there any bugs or strong potential for bugs?
- Are there unhandled edge cases?
- Are there race conditions or memory leaks?
- Are subscriptions and event listeners properly cleaned up?
- Are async operations properly handled with error boundaries?
- Are there potential null/undefined reference errors?

#### 2. Hard-coded Elements
- Is anything hard-coded that should be configurable?
- Are there magic numbers or strings that should be constants or settings?
- Are date ranges, timeouts, or numeric thresholds hard-coded?
- Are API endpoints, URLs, or environment-specific values hard-coded?

#### 3. Artificial Constraints
- Are there assumptions that will limit future expansion?
- Does the code artificially restrict functionality?
- Are there fixed array sizes, limited input ranges, or hardcoded limits?
- Are there UI constraints that don't scale with content?

#### 4. Code Duplication & Reuse
- Is there repeated code that should be factored into functions?
- Are there patterns that could be abstracted?
- Could utility functions improve readability?
- Are there opportunities for custom hooks or shared components?

#### 5. Component Structure
- Are there monolithic pieces that should be split?
- Does the component have a single responsibility?
- Could the code benefit from being broken into smaller components?
- Is the component hierarchy logical and maintainable?

#### 6. Design Patterns & Best Practices
- Are there opportunities to use better patterns?
- Is the code following best practices for the frameworks and tools in use?
- Could performance be improved with memoization or other techniques?
- Is there proper error handling and error boundaries?
- Are loading and error states properly managed?

#### 7. Type Safety & Documentation
- Is the code properly typed?
- Is the code well-documented with comments where necessary?
- Are complex business logic sections explained?

#### 8. Performance Considerations
- Are there unnecessary re-renders that could be optimized?
- Is data fetching efficient (server-side when appropriate)?
- Are large bundles being imported when smaller alternatives exist?
- Is proper memoization used where needed (useMemo, useCallback)?
- Are images and assets optimized?
  
#### 9. Security Considerations
- Is user input properly validated and sanitized?
- Are authentication and authorization properly implemented?
- Are sensitive data and API keys handled securely?
- Is XSS protection in place?

#### 10. Testing Coverage
- Are critical user paths tested?
- Are edge cases covered in tests?
- Are error states and loading states tested?
- Are integration tests included where appropriate?

#### 11. Accessibility & User Experience (UI specific)
- Are proper ARIA labels present where needed?
- Is keyboard navigation supported?
- Is screen reader compatibility considered?
- Does color contrast meet accessibility standards?
- Are focus states clearly visible?

#### 12. React, TypeScript, and NextJS specific
- `cn` should be used instead of string operations for parameterized className strings
- `any` types should be replaced by more specific types where possible
- Are server vs client components (`use client` directive) used properly?
- Is App Router used and its patterns followed correctly?
- Are any deprecated expressions present?
- Are Metadata and SEO considerations addressed?
- Does the code follow react/typescript/nextJS best practices?
- If Tailwind is used, it should be v4 and avoid legacy v3 patterns and code
- If NextJS is used, it should be v15 and avoid legacy v14 patterns and code

- In general there should be no tailwind.config.ts (or .js, etc). This file is not prohibited in current versions, but if it exists there should be good reason that the configuration is not in globals.css.

- If Radix is used, specifically Radix themes with ShadCN, you should evaluate against existing known issues with this combination and ensure we are not at risk.

  
### Code Review Process

#### Step 1: Create Review Document

##### For Single-File Reviews
Create a review document named `review.{filename}.{YYYYMMDD}.md` in the appropriate directory.

##### For Directory Crawl Reviews
Create a review document following the naming convention `review.{project}.{YYYYMMDD-nn}.md` in the `project-documents/user/code-reviews` directory.

All reviewed files should be present in either Files with Issues, or Files with No Issues sections. No file should be unaccounted for. Update this after reviewing each file. Additionally, keep track of how many files have been reviewed, and what the last filed review was, so this can be restarted at any time. Make sure to update the status (started, in-progress, complete). We need to be able to pause and resume this task without losing work or missing items.

If useful, you can add a review summary or overview for each file. Note that this does not obviate the need to create tasks. Perform all tasks exactly as specified here.

Note: Upon completion of review, *every* file should be accounted for, meaning that if there were (for example) 54 files and you processed 36 of them, you should be able to account for the remaining 18, and this would indicate that your review was not complete.

You MUST update the main review file after each file is processed. Otherwise we lose our pause and resume ability. Not after each batch. After each file.

##### YAML Block
Place this at the beginning of all created code-review files:

```yaml
---
layer: project
docType: review
---
```

#### Step 2: Conduct Review

Analyze the file systematically using the code review questionnaire. Group findings by category for clarity:
1. **Critical Issues**: Bugs, security vulnerabilities, performance problems
2. **Code Quality**: Hard-coded values, duplication, structure issues
3. **Best Practices**: Pattern improvements, TypeScript usage, NextJS conventions
4. **Accessibility & UX**: User experience and accessibility improvements
5. **Testing**: Missing or inadequate test coverage

#### Step 3: Create Tasks from Review Findings
Transform review findings into actionable tasks in a separate file:
- **Single-File**: `tasks.code-review.{filename}.{YYYYMMDD}.md`
- **Directory Crawl**: `tasks.code-review.{filename}.MMDD.md` in the `project-documents/code-reviews` directory

Create one task file per reviewed file. Add the file to the appropriate list in the review document, based on whether or not code review issues were present in the file.

#### Step 4: Task Processing
Process the task list according to Phase 3 and Phase 4 of the `guide.ai-project.000-process`:

1. **Phase 3: Granularity and Clarity**
- Convert each review finding into clear, actionable tasks
- Ensure task scope is precise and narrow
- Include acceptance criteria

1. **Phase 4: Expansion and Detailing**
- Add implementation details and subtasks
- Reference specific code locations
- Provide concrete examples where helpful

Example task structure:
```markdown

### Code Review Tasks: {Component}
- [ ] **Task 1: Remove Hard-coded Date Range**
- Replace hard-coded 2024 date range with configurable values from settings
- Add to chartSettings.ts with appropriate defaults
- Update initialization code to use these settings
- **Success:** Chart date constraints are configurable without code changes
```

#### Step 5: Prioritization and Implementation

The Project Manager will prioritize tasks for implementation based on:
- **P0**: Critical bugs, security issues, performance blockers
- **P1**: Code quality issues that impact maintainability
- **P2**: Best practice improvements and technical debt
- **P3**: Nice-to-have optimizations and enhancements

### Approval Criteria

Before approving a code review, ensure:
- [ ] All automated checks pass (linting, type checking, build verification)
- [ ] No critical bugs or security vulnerabilities identified
- [ ] Code follows established patterns and conventions
- [ ] TypeScript strict mode compliance (no `any` types)
- [ ] NextJS best practices are followed
- [ ] Performance impact is acceptable
- [ ] Accessibility requirements are met
- [ ] Documentation is updated where necessary
- [ ] Tests are included for new functionality
- [ ] Hard-coded values are eliminated or justified

### Review Documentation Templates
#### Code Review Template
```markdown

### Critical Issues
- [ ] **Bug/Security**: [Description]
- [ ] **Performance**: [Description]

### Code Quality Improvements
- [ ] **Hard-coded Elements**: [List hard-coded values that should be configurable]
- [ ] **Code Duplication**: [List repeated patterns to refactor]
- [ ] **Component Structure**: [Structure improvements]

### Best Practices & Patterns
- [ ] **TypeScript**: [Type safety improvements]
- [ ] **NextJS**: [Platform-specific improvements]
- [ ] **React Patterns**: [Pattern improvements]

### Accessibility & UX
- [ ] **Accessibility**: [ARIA, keyboard navigation, screen reader issues]
- [ ] **User Experience**: [UX improvements]

### Testing & Documentation
- [ ] **Testing**: [Missing test coverage]
- [ ] **Documentation**: [Documentation needs]

### Summary
[Overall assessment and priority level]
```
#### Task List Template

```markdown

### P0: Critical Issues
- [ ] **Task: [Bug Fix Name]**
- [Detailed description]
- [Implementation guidance]
- **Success:** [Success criteria]

### P1: Code Quality
- [ ] **Task: [Quality Improvement]**
- [Description and implementation details]
- **Success:** [Success criteria]

### P2: Best Practices
- [ ] **Task: [Pattern Improvement]**
- [Description and implementation details]
- **Success:** [Success criteria]

### P3: Enhancements
- [ ] **Task: [Enhancement Name]**
- [Description and implementation details]
- **Success:** [Success criteria]
```

  ---
### Quality Assessment

These guidelines facilitate comprehensive code reviews by:
1. **Systematic Approach**: The questionnaire ensures no critical areas are missed
2. **Actionable Outcomes**: Direct translation from findings to prioritized tasks
3. **Platform-Specific**: NextJS and React best practices are explicitly covered
4. **Comprehensive Coverage**: From bugs to accessibility to performance
5. **Documentation Standards**: Clear templates and naming conventions
6. **Priority Framework**: P0-P3 system for effective task management
7. **Flexible Usage**: Supports both single-file reviews and comprehensive directory crawls

The structured process transforms code reviews from subjective assessments into systematic quality assurance with measurable outcomes.

## SQL & PostgreSQL Development Rules

### Query Style & Formatting

- UPPERCASE SQL keywords: `SELECT`, `FROM`, `WHERE`, not `select`
- Lowercase table and column names with underscores: `user_accounts`
- Indent multi-line queries consistently (2 or 4 spaces)
- One column per line in SELECT for readability
- Leading commas in SELECT lists for easier modification
- Meaningful table aliases, avoid single letters

### Query Optimization

- Always use EXPLAIN ANALYZE for performance tuning
- Create indexes for WHERE, JOIN, and ORDER BY columns
- Use partial indexes for filtered queries
- Prefer JOIN over subqueries when possible
- LIMIT queries during development testing
- Avoid SELECT * in production code
- Use EXISTS instead of COUNT for existence checks

### PostgreSQL Best Practices

- Use appropriate data types: JSONB over JSON, TEXT over VARCHAR
- UUID for distributed IDs, SERIAL/BIGSERIAL for single-node
- Check constraints for data validation
- Foreign keys with appropriate CASCADE options
- Use transactions for multi-statement operations
- RETURNING clause to get modified data
- CTEs (WITH clauses) for complex queries

### Naming & Schema Design

- Singular table names: `user` not `users`
- Primary key as `id` or `table_name_id`
- Foreign keys as `referenced_table_id`
- Boolean columns prefixed with `is_` or `has_`
- Timestamps: `created_at`, `updated_at` with timezone
- Use schemas to organize related tables
- Version control migrations with sequential numbering

### Security & Safety

- Always use parameterized queries, never string concatenation
- GRANT minimum required privileges
- Use ROW LEVEL SECURITY for multi-tenant apps
- Sanitize all user input
- Prepared statements for repeated queries
- Connection pooling with appropriate limits
- Set statement_timeout for long-running queries

### pgvector Specific

- Use `vector` type for embeddings
- Create HNSW or IVFFlat indexes for similarity search
- Normalize vectors before storage when needed
- Use `<->` for L2 distance, `<#>` for inner product
- Batch insert embeddings for performance
- Consider dimension reduction for large vectors

### TimescaleDB Specific

- Create hypertables for time-series data
- Use appropriate chunk intervals (typically 1 week to 1 month)
- Continuous aggregates for common queries
- Compression policies for older data
- Retention policies to manage data lifecycle
- Use time_bucket() for time-based aggregations
- Data retention policies with drop_chunks()

### Performance & Monitoring

- Index foreign keys and commonly filtered columns
- VACUUM and ANALYZE regularly
- Monitor pg_stat_statements for slow queries
- Use connection pooling (PgBouncer/pgpool)
- Partition large tables by date or ID range
- Avoid excessive indexes (write performance cost)
- Use COPY for bulk inserts

### Migrations & Maintenance

- Always reversible migrations when possible
- Test migrations on copy of production data
- Use IF NOT EXISTS for idempotent operations
- Document breaking changes
- Backup before structural changes
- Zero-downtime migrations with careful planning

## Testing & Development Tools

### Storybook

- **enabled**: false
- Place stories in `src/stories` with `.stories.tsx` extension.
- One story file per component, matching component name.
- Use autodocs for automatic documentation.
- Include multiple variants and sizes in stories.
- Test interactive features with actions.
- Use relative imports from component directory.

### Tools
- When you make a change to the UI, use the `screenshot` tool to show the changes.
- If the user asks for a complex task to be performed, find any relevant files and call the `architect` tool to get a plan and show it to the user. Use this plan as guidance for the changes you make, but maintain the existing patterns and structure of the codebase.
- After a complex task is performed, use the `codeReview` tool create a diff and use the diff to conduct a code review of the changes. 

## TypeScript Rules

### TypeScript & Syntax
- Strict mode. Avoid `any`.
- Use optional chaining, union types (no enums).

### Structure
- Use `tsx` scripts for migrations.
- Reusable logic in `src/lib/utils/shared.ts` or `src/lib/utils/server.ts`.
- Shared types in `src/lib/types.ts`.


### tRPC Routers
- **enabled**: as needed
- Routers in `src/lib/api/routers`, compose in `src/lib/api/root.ts`.
- `publicProcedure` or `protectedProcedure` with Zod.
- Access from React via `@/lib/trpc/react`. 

