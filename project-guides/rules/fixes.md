---
name: fixes-rules
description: "How to make a fix (any work committed as fix:) without slice ceremony. Use for bugs, regressions, broken behavior, or an issue to be closed with Fixes #n."
alwaysApply: true
---

### Fixes

A fix is any work that will be committed as `fix:`. Decide the commit type before starting. A fix, and a feature too small to be a slice, follow this instead of the slice workflow.

- **Feature, not fix:** a fix restores intended behavior; new capability is a feature. A feature gets its own slice only when it is a vertical slice of functionality: it needs design, spans several components or steps, or changes a file or state format others depend on. Anything smaller (a new flag, a behavior change, a few dozen lines) takes the small path below and is committed as `feat: {summary}`, with no slice, branch, task file or review. Say which path in one line before starting. Size alone never turns a fix into a feature.
- **Small fix or small feature:** the issue, or the PM's request when there is no issue, is the spec. Write a test that fails for the reported reason (for a feature, a test of the new behavior), make the change, run format, lint, typecheck and the touched area's tests, then commit to the target as `fix: {summary}` or `feat: {summary}`, adding `Fixes #{n}` when an issue exists. No branch, task file or review.
- **Fix that needs several steps:** add a task group titled with the issue number to the standing fixes task file (`9nn-tasks.standing-fixes.md`) and work it on the target, one commit per task. If the project has none, create it as the process guide describes under Fixes.
- **Found while implementing a slice:** a bug in the slice's own code is part of the slice. Anything else: file an issue and continue.
- No review unless the Project Manager asks.
