---
layer: process
phase: 6
phaseName: task-expansion
guideRole: primary
audience: [human, ai]
description: Optional Phase 6 playbook for expanding complex tasks into more granular subtasks.
dependsOn:
  - guide.ai-project.000-process.md
  - guide.ai-project.005-task-breakdown.md
dateCreated: 20250101
dateUpdated: 20260218
---

#### Summary
This guide provides instructions for expanding complex slice task breakdowns into more granular, atomic subtasks. This is Phase 6 in `guide.ai-project.000-process`.

**This phase is optional.** Most task breakdowns produced in Phase 5 are sufficient for direct execution. Phase 6 should only be invoked when the Project Manager determines that specific tasks are too complex or ambiguous for a junior AI developer to execute without additional guidance.

Phase 6 cannot begin until the slice task breakdown (Phase 5 output) is approved by the Project Manager.

#### Role
Senior AI performs this phase. The Project Manager approves the output before proceeding to Phase 7 (Implementation).

#### When to Use This Phase
Invoke Phase 6 when a Phase 5 task breakdown contains tasks that:
- Require multi-step coordination across several files or systems
- Involve unfamiliar libraries or tools where the agent would benefit from explicit setup steps
- Bundle multiple distinct concerns that should be separated for reliable execution
- Have ambiguous success criteria that need to be made more specific

Do not invoke Phase 6 merely to add verbosity. If a task is clear and actionable as written, it should pass through unchanged.

#### Inputs
* guide.ai-project.000-process
* guide.ai-project.005-task-breakdown
* guide.ai-project.006-task-expansion (this document)
* {project} - spec (Phase 2 output)
* {project} - high-level design (Phase 2.5 output)
* {slice} - slice design (Phase 4 output)
* {slice} - slice task breakdown (Phase 5 output)
* rules/ - directory containing coding rules and guidelines organized by platform/technology

If any inputs are missing or insufficient, stop and resolve with the Project Manager before proceeding.

#### Output
The updated slice task file with expanded tasks. The output replaces the Phase 5 file in place. Update the `dateUpdated` field in the YAML front matter. Follow the formatting conventions established in `guide.ai-project.005-task-breakdown`.

#### Procedure
1. Review the Phase 5 task file alongside the slice design and HLD.
2. For each task, evaluate: can a junior AI developer complete this as described without making product decisions or assumptions? If yes, keep it as-is. If no, expand it.
3. When expanding, add granularity through subtasks, explicit file paths, or brief code hints — but avoid writing full implementation code. This remains a planning document.
4. Preserve the test-with ordering established in Phase 5. Tests for a component must remain immediately after that component's implementation. If the Phase 5 input does not follow this pattern, restructure during expansion. See `guide.ai-project.005-task-breakdown` for details.
5. Verify every original task is accounted for in the output.
6. Verify file length remains within the guidelines specified in `guide.ai-project.005-task-breakdown`.

#### Example: When Expansion Helps

**Phase 5 input (too vague):**

```markdown
- [ ] Set up authentication system
  - [ ] Install and configure auth library with database adapter
  - [ ] Configure providers for email/password
  - [ ] Set up session management
  - [ ] Success: Users can register and login successfully
```

**Phase 6 expansion:**

```markdown
- [ ] Install authentication dependencies
  - [ ] Install core auth package and database adapter via package manager
  - [ ] Verify no dependency conflicts with existing packages
  - [ ] Success: Dependencies installed, lock file updated

- [ ] Configure authentication provider
  - [ ] Create auth configuration file at the path specified in the framework docs
  - [ ] Configure credentials provider for email/password
  - [ ] Add required environment variables to `.env.example`
  - [ ] Success: Auth configuration loads without errors

- [ ] Configure database integration for sessions
  - [ ] Add auth-related tables to the database schema
  - [ ] Run database migration
  - [ ] Success: Session tables created, adapter connects successfully

- [ ] Write authentication tests
  - [ ] Test user registration creates database records
  - [ ] Test login succeeds with valid credentials
  - [ ] Test login fails with invalid credentials
  - [ ] Test session is cleared on logout
  - [ ] Success: All auth tests pass
```

Notice the expansion split one vague task into three focused implementation tasks with a test task immediately following, while remaining stack-agnostic.

#### Example: When Expansion Is Unnecessary

**Phase 5 input (already sufficient):**

```markdown
- [ ] Define AgentState enum
  - [ ] Create `src/project/models.py`
  - [ ] Define `AgentState(StrEnum)` with values: idle, processing, failed, terminated
  - [ ] Success: `from project.models import AgentState` works; all values match spec
```

This task is clear, narrow, and has specific success criteria. Pass it through unchanged.

#### Success Criteria
Phase 6 is complete when:
- All tasks from the Phase 5 input are accounted for
- Complex or ambiguous tasks have been expanded into actionable subtasks
- Clear tasks have been preserved as-is (not padded with unnecessary detail)
- Test-with ordering is maintained throughout
- The Project Manager approves the expanded task breakdown

#### Next Steps
With approved task expansion, proceed to Phase 7: Implementation.