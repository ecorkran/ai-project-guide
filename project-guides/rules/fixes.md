---
name: fixes-rules
description: How to make a fix (any work committed as fix:) without slice ceremony. Use for bugs, regressions, broken behavior, or an issue to be closed with Fixes #n.
alwaysApply: true
---

### Fixes

A fix is any work that will be committed as `fix:`. Decide the commit type before starting. For a fix, follow this instead of the slice workflow.

- **Feature, not fix:** a new user-facing option, a changed file or state format, or a new component is a feature and gets its own slice. Say so in one line. Size alone never makes something a feature.
- **Small fix:** the issue is the spec. Write a test that fails for the reported reason, fix the code, run format, lint, typecheck and the touched area's tests, then commit to the target as `fix: {summary}` with `Fixes #{n}`. No branch, task file or review.
- **Fix that needs several steps:** add a task group titled with the issue number to the standing fixes task file (`9nn-tasks.standing-fixes.md`) and work it on the target, one commit per task. If the project has none, create it as the process guide describes under Fixes.
- **Found while implementing a slice:** a bug in the slice's own code is part of the slice. Anything else: file an issue and continue.
- No review unless the Project Manager asks.
