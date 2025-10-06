---
layer: process
phase: 5
phaseName: execution
guideRole: support
audience: [human, ai]
description: Checklist and tips for Phase 5 code reviews (human ↔ AI pair).
dependsOn:
  - guide.ai-project.002-spec.md
  - guide.ai-project.006-task-expansion.md
---
# Code Review Guidelines

## Overview
This document outlines the comprehensive process for conducting code reviews. Code reviews ensure code quality, maintainability, and alignment with project goals while identifying potential issues before they become problematic. Specific guidelines are provided for project aspects (ex: UI) and platform specifics (ex: NextJS).

## Usage Modes
This guide supports two distinct code review scenarios:

### 1. Single-File Code Review
- **Purpose**: Review a single provided source file
- **Scope**: Focus on one specific file or component
- **Process**: Apply the code review questionnaire to the individual file and create tasks as needed
- **Documentation**: Create a simple review document for the findings and a corresponding task file if issues are identified

### 2. Directory Crawl Review
- **Purpose**: Systematically review an entire directory structure or project
- **Scope**: Process multiple files in a coordinated batch operation
- **Process**: Follow the full infrastructure guidelines below for organizing multiple review sessions
- **Documentation**: Use the structured directory approach with session tracking and comprehensive file accounting

The remainder of this guide provides detailed processes for both modes, with particular emphasis on the infrastructure needed for directory crawl reviews.

## Infrastructure Guidelines

**File Locations:**
- Review documents: `private/reviews/nnn-review.{name}.md` (range 900-939)
- Task files: `private/tasks/nnn-tasks.code-review.{filename}.md` (same nnn as review)

Note: The `private/` path may map to `project-artifacts/` in monorepo development. If unclear, confirm with Project Manager.

### For Directory Crawl Reviews

**Batching Strategy:**
Use a single review document per review session with sequential index. **Group related files together in one review session** (same `nnn`) to keep the review organized and maintain context.

- Format: `nnn-review.{project}.md` where nnn is 900-939
- **All task files from this session use the same `nnn`** - this keeps the review batch together
- Track all files reviewed (with and without issues)
- Update status after each file for pause/resume capability

**Benefits of batching:**
- Maintains review context across related files
- Easy to see all work from one review session
- Sequential numbering prevents file sprawl

**Example:** Review session 900
- Review: `900-review.dashboard-components.md`
- Tasks: `900-tasks.code-review.header.md`, `900-tasks.code-review.sidebar.md`

### For Single-File Reviews
Use format: `nnn-review.{filename}.md` and `nnn-tasks.code-review.{filename}.md` if issues found.

## Code Review Questionnaire
When reviewing code, systematically answer these core questions.  
### 1. Potential Bugs & Edge Cases
- Are there any bugs or strong potential for bugs?
- Are there unhandled edge cases?
- Are there race conditions or memory leaks?
- Are subscriptions and event listeners properly cleaned up?
- Are async operations properly handled with error boundaries?
- Are there potential null/undefined reference errors?

### 2. Hard-coded Elements
- Is anything hard-coded that should be configurable?
- Are there magic numbers or strings that should be constants or settings?
- Are date ranges, timeouts, or numeric thresholds hard-coded?
- Are API endpoints, URLs, or environment-specific values hard-coded?

### 3. Artificial Constraints
- Are there assumptions that will limit future expansion?
- Does the code artificially restrict functionality?
- Are there fixed array sizes, limited input ranges, or hardcoded limits?
- Are there UI constraints that don't scale with content?

### 4. Code Duplication & Reuse
- Is there repeated code that should be factored into functions?
- Are there patterns that could be abstracted?
- Could utility functions improve readability?
- Are there opportunities for custom hooks or shared components?

### 5. Component Structure
- Are there monolithic pieces that should be split?
- Does the component have a single responsibility?
- Could the code benefit from being broken into smaller components?
- Is the component hierarchy logical and maintainable?

### 6. Design Patterns & Best Practices
- Are there opportunities to use better patterns?
- Is the code following best practices for the frameworks and tools in use?
- Could performance be improved with memoization or other techniques?
- Is there proper error handling and error boundaries?
- Are loading and error states properly managed?

### 7. Type Safety & Documentation
- Is the code properly typed?
- Is the code well-documented with comments where necessary?
- Are complex business logic sections explained?

### 8. Performance Considerations
- Are there unnecessary re-renders that could be optimized?
- Is data fetching efficient (server-side when appropriate)?
- Are large bundles being imported when smaller alternatives exist?
- Is proper memoization used where needed (useMemo, useCallback)?
- Are images and assets optimized?
  
### 9. Security Considerations
- Is user input properly validated and sanitized?
- Are authentication and authorization properly implemented?
- Are sensitive data and API keys handled securely?
- Is XSS protection in place?

### 10. Testing Coverage
- Are critical user paths tested?
- Are edge cases covered in tests?
- Are error states and loading states tested?
- Are integration tests included where appropriate?

### 11. Accessibility & User Experience (UI specific)
- Are proper ARIA labels present where needed?
- Is keyboard navigation supported?
- Is screen reader compatibility considered?
- Does color contrast meet accessibility standards?
- Are focus states clearly visible?

### 12. React, TypeScript, and NextJS specific
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

  
## Code Review Process

### Step 1: Create Review Document

#### For Single-File Reviews
Create a review document named `nnn-review.{filename}.md` in `private/reviews/`, where `nnn` is in the 900-939 range.

#### For Directory Crawl Reviews
Create a review document following the naming convention `nnn-review.{project}.md` in the `private/reviews/` directory, where `nnn` is in the 900-939 range. Use the same `nnn` for all task files in this review session.

All reviewed files should be present in either Files with Issues, or Files with No Issues sections. No file should be unaccounted for. Update this after reviewing each file. Additionally, keep track of how many files have been reviewed, and what the last filed review was, so this can be restarted at any time. Make sure to update the status (started, in-progress, complete). We need to be able to pause and resume this task without losing work or missing items.

If useful, you can add a review summary or overview for each file. Note that this does not obviate the need to create tasks. Perform all tasks exactly as specified here.

Note: Upon completion of review, *every* file should be accounted for, meaning that if there were (for example) 54 files and you processed 36 of them, you should be able to account for the remaining 18, and this would indicate that your review was not complete.

You MUST update the main review file after each file is processed. Otherwise we lose our pause and resume ability. Not after each batch. After each file.

#### YAML Block
Place this at the beginning of all created code-review files:

```yaml
---
layer: project
docType: review
---
```

### Step 2: Conduct Review

Analyze the file systematically using the code review questionnaire. Group findings by category for clarity:
1. **Critical Issues**: Bugs, security vulnerabilities, performance problems
2. **Code Quality**: Hard-coded values, duplication, structure issues
3. **Best Practices**: Pattern improvements, TypeScript usage, NextJS conventions
4. **Accessibility & UX**: User experience and accessibility improvements
5. **Testing**: Missing or inadequate test coverage

### Step 3: Create Tasks from Review Findings
Transform review findings into actionable tasks in `private/tasks/`:
- Use format: `nnn-tasks.code-review.{filename}.md`
- Use the **same nnn** as the review document for all files in the review session
- Create one task file per reviewed file that has issues
- Add the file to the appropriate list in the review document

**Example:** Review session 900 examining multiple components:
- Review doc: `900-review.dashboard-components.md`
- Task files: `900-tasks.code-review.header.md`, `900-tasks.code-review.sidebar.md`, etc.

### Step 4: Task Processing
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

## Code Review Tasks: {Component}
- [ ] **Task 1: Remove Hard-coded Date Range**
- Replace hard-coded 2024 date range with configurable values from settings
- Add to chartSettings.ts with appropriate defaults
- Update initialization code to use these settings
- **Success:** Chart date constraints are configurable without code changes
```

### Step 5: Prioritization and Implementation

The Project Manager will prioritize tasks for implementation based on:
- **P0**: Critical bugs, security issues, performance blockers
- **P1**: Code quality issues that impact maintainability
- **P2**: Best practice improvements and technical debt
- **P3**: Nice-to-have optimizations and enhancements

## Approval Criteria

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

## Review Documentation Templates
### Code Review Template
```markdown
# Code Review: {Filename}

## Critical Issues
- [ ] **Bug/Security**: [Description]
- [ ] **Performance**: [Description]

## Code Quality Improvements
- [ ] **Hard-coded Elements**: [List hard-coded values that should be configurable]
- [ ] **Code Duplication**: [List repeated patterns to refactor]
- [ ] **Component Structure**: [Structure improvements]

## Best Practices & Patterns
- [ ] **TypeScript**: [Type safety improvements]
- [ ] **NextJS**: [Platform-specific improvements]
- [ ] **React Patterns**: [Pattern improvements]

## Accessibility & UX
- [ ] **Accessibility**: [ARIA, keyboard navigation, screen reader issues]
- [ ] **User Experience**: [UX improvements]

## Testing & Documentation
- [ ] **Testing**: [Missing test coverage]
- [ ] **Documentation**: [Documentation needs]

## Summary
[Overall assessment and priority level]
```
### Task List Template

```markdown
# Code Review Tasks: {Filename}

## P0: Critical Issues
- [ ] **Task: [Bug Fix Name]**
- [Detailed description]
- [Implementation guidance]
- **Success:** [Success criteria]

## P1: Code Quality
- [ ] **Task: [Quality Improvement]**
- [Description and implementation details]
- **Success:** [Success criteria]

## P2: Best Practices
- [ ] **Task: [Pattern Improvement]**
- [Description and implementation details]
- **Success:** [Success criteria]

## P3: Enhancements
- [ ] **Task: [Enhancement Name]**
- [Description and implementation details]
- **Success:** [Success criteria]
```

  ---
## Quality Assessment

These guidelines facilitate comprehensive code reviews by:
1. **Systematic Approach**: The questionnaire ensures no critical areas are missed
2. **Actionable Outcomes**: Direct translation from findings to prioritized tasks
3. **Platform-Specific**: NextJS and React best practices are explicitly covered
4. **Comprehensive Coverage**: From bugs to accessibility to performance
5. **Documentation Standards**: Clear templates and naming conventions
6. **Priority Framework**: P0-P3 system for effective task management
7. **Flexible Usage**: Supports both single-file reviews and comprehensive directory crawls

The structured process transforms code reviews from subjective assessments into systematic quality assurance with measurable outcomes.