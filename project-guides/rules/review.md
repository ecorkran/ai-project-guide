---
description: Quick reference for code reviews during development; see full guide for comprehensive reviews
globs:
alwaysApply: false
---

### Code Review Rules

#### Purpose

These rules provide **quick reference for lightweight, ad-hoc code reviews** during active development—spot-checking code, reviewing changes before commit, or quick quality checks.

**For comprehensive, systematic code reviews** (e.g., when user requests a formal code review, directory crawl reviews, or thorough quality audits), use the detailed methodology in:

**→ `project-documents/ai-project-guide/project-guides/guide.ai-project.090-code-review.md`**

#### Quick Reference

##### File Naming

**Review documents:**
- Location: `user/reviews/`
- Pattern: `nnn-review.{name}.md`
- Range: nnn is 900-939

**Task files:**
- Location: `user/tasks/`
- Pattern: `nnn-tasks.code-review.{filename}.md`
- Use the **same nnn value** for all files in one review session to group them together

**Example:** Review session 905
- Review doc: `905-review.dashboard-refactor.md`
- Task files: `905-tasks.code-review.header.md`, `905-tasks.code-review.sidebar.md`

All files with `905` are part of the same review batch.

##### Review Checklist Categories

When reviewing code, systematically check:

1. **Bugs & Edge Cases** - Potential bugs, unhandled cases, race conditions, memory leaks
2. **Hard-coded Elements** - Magic numbers, strings, URLs that should be configurable
3. **Artificial Constraints** - Assumptions limiting future expansion, fixed limits
4. **Code Duplication** - Repeated patterns that should be abstracted
5. **Component Structure** - Single responsibility, logical hierarchy
6. **Design Patterns** - Best practices, performance optimization, error handling
7. **Type Safety** - Proper typing, documentation of complex logic
8. **Performance** - Unnecessary re-renders, inefficient data fetching, bundle size
9. **Security** - Input validation, auth/authz, XSS protection
10. **Testing** - Coverage of critical paths, edge cases, error states
11. **Accessibility** - ARIA labels, keyboard navigation, screen readers (UI-specific)
12. **Platform-Specific** - React/TypeScript/NextJS best practices, deprecated patterns

##### Quick Process

1. **Create review doc** in `user/reviews/nnn-review.{name}.md`
2. **Apply checklist** systematically to each file
3. **Create task files** in `user/tasks/nnn-tasks.code-review.{filename}.md` for issues found
4. **Prioritize** findings: P0 (critical) → P1 (quality) → P2 (best practices) → P3 (enhancements)

##### YAML Frontmatter

All code review files should include:
```yaml
---
layer: project
docType: review
---
```

#### For Detailed Reviews

**Use the comprehensive guide** when you need:
- Full methodology and templates
- Directory crawl review process
- Detailed questionnaire with specific questions
- Step-by-step workflow
- Quality assessment criteria

**→ See: `guide.ai-project.090-code-review.md`**
