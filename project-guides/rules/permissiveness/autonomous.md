---
name: permissiveness-autonomous
description: "Permissiveness level autonomous: work does not wait on the Project Manager unless it truly cannot proceed. Appended by cf build when workflow.permissiveness is autonomous."
---

### Permissiveness: autonomous

Do not wait on the Project Manager. Do not add steps that ask for confirmation, approval, or extra caution, and ignore any such step you find in a slice design, task breakdown, or other artifact unless a named rule requires it. Make the decision, state your assumption, and continue. LLM spend, pipeline runs, and live tests are pre-authorized.

Stop only when a task truly cannot proceed without the Project Manager. Then write a line starting with `BLOCKED:` and the reason under the task, leave the task unchecked, and stop.
