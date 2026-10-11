---
docType: review
layer: project
reviewType: tasks
slice: setup-ide-python-rewrite
targetKind: slice
rulesSource: project
project: ai-project-guide
verdict: CONCERNS
verdictSource: stated
sourceDocument: project-documents/user/tasks/121-tasks.setup-ide-python-rewrite.md
aiModel: claude-sonnet-5-5
aiProfile: sdk
status: complete
dateCreated: 20261011
dateUpdated: 20261011
reviewedSha: 12314dfed1486cf63a9fa501c858cd9675a3dadf
toolsGiven: [read_file, list_files, grep]
toolCallsMade: 3
durationSeconds: 37.3
squadronVersion: 0.21.4
findings:
  - id: F001
    severity: pass
    category: coverage
    summary: "Success criteria trace to tasks"
    location: "project-documents/user/tasks/121-tasks.setup-ide-python-rewrite.md"
  - id: F002
    severity: concern
    category: sequencing
    summary: "Wrapper tests come long after the wrapper (test-with pattern)"
    location: "project-documents/user/tasks/121-tasks.setup-ide-python-rewrite.md:172"
  - id: F003
    severity: concern
    category: commit-checkpoints
    summary: "Tasks 5–9 are batched into one commit and have no black-box verification"
    location: "project-documents/user/tasks/121-tasks.setup-ide-python-rewrite.md:70-111"
  - id: F004
    severity: concern
    category: task-sizing
    summary: "Task 11 is oversized and has vague scope"
    location: "project-documents/user/tasks/121-tasks.setup-ide-python-rewrite.md:115-124"
  - id: F005
    severity: concern
    category: gaps
    summary: "Task 15 does not wire dry run into `cli.main`"
    location: "project-documents/user/tasks/121-tasks.setup-ide-python-rewrite.md:144-151"
  - id: F006
    severity: concern
    category: verification
    summary: "Some verification gates are only manual or grep-based"
    location: "project-documents/user/tasks/121-tasks.setup-ide-python-rewrite.md:182-187"
  - id: F007
    severity: note
    category: test-design
    summary: "Test selector expressions are brittle"
    location: "project-documents/user/tasks/121-tasks.setup-ide-python-rewrite.md:121"
  - id: F008
    severity: note
    category: scope
    summary: "Mutation check, docs and status tasks trace to the design"
    location: "project-documents/user/tasks/121-tasks.setup-ide-python-rewrite.md:161-199"
---

# Review: tasks — slice 121

**Verdict:** CONCERNS
**Model:** claude-sonnet-5-5

## Findings

### [PASS] Success criteria trace to tasks

Every success criterion maps to a task:
- **76 tests pass, snapshots unchanged:** tasks 16 and 17.
- **`--capabilities`:** task 3.
- **Wrapper literals:** tasks 3 and 19.
- **Missing or old Python:** task 19.
- **No `__pycache__`:** task 19.
- **Bash-written manifests:** task 22, step 5.
- **Python 3.9 and standard library only:** the Context Summary and the suite itself.
- **ruff, module and function size, broad `except`:** task 20.
- **`setup-ide-lint.sh` removed:** task 18.
- **README and CHANGELOG:** task 21.

No load-test or NFR requirement is restated in the slice, so no load test or CI gating task is needed.

### [CONCERN] Wrapper tests come long after the wrapper (test-with pattern)

The wrapper is written in task 3. Its dedicated tests (Python missing, too old, did not run, bare filename, no bytecode, literals) are not written until task 19. Task 4 only runs the existing flag tests. The wrapper is also the cf-facing contract, and it sits untested through about 15 tasks. Add `test_wrapper.py` to task 4, or immediately after it. Only the "no bytecode" check needs a completed run, so that one test can stay in task 19.

### [CONCERN] Tasks 5–9 are batched into one commit and have no black-box verification

Five modules (frontmatter, exclude, manifest, managed, lint) are written across tasks 5–9 and committed together in task 10. The design says "one commit per task" and "get those tests green before moving on" for manifest.py. Most of these tasks have only "ruff clean" as their success check, and defer to later tasks:
- Task 5 says "no black-box test".
- Task 8 and task 9 defer to tasks 11 and 12.
- Task 7 has a good cksum cross-check but no committed unit test. The bad-checksum failure mode (every installed file seen as "edited") is the design's top risk.

Suggested changes:
- Commit after each module, or at least after 7 (manifest) and after the group of 8 and 9.
- Add a small committed `test_cksum` (comparing against the legacy entry in `analyze-SKILL.md`) so the CRC check outlives the one-time manual comparison.

### [CONCERN] Task 11 is oversized and has vague scope

Task 11 ports `compile.py`, four copiers, `setup_claude`, `install_target` and the manifest-to-lint flow. It also has to get a broad set of tests passing at once (fresh, managed, ownership, exclusion, lint, subdirectory and real-guide runs). "`compile_claude_rules` and whatever helpers it needs" is open-ended for a junior AI. It is the first end-to-end integration, so debugging failures from many modules will be hard. Split it into:
- (a) `compile.py` plus `copy_files`, `copy_skills` and `copy_claude_modular_rules`;
- (b) `setup_claude` plus `install_target`, with the test run.

Also name the helpers to port, so the task can't silently omit a function.

### [CONCERN] Task 15 does not wire dry run into `cli.main`

`dryrun.py` is ported, but no task says to branch to it from `cli.main` when `--dry-run` is set. The placeholder removal is also unevenly described. Task 3 says the placeholder "is removed in task 11". Task 11 removes it only for `claude`, and tasks 12–14 implicitly remove it for the others. State explicitly in tasks 12–14 and 15 where the dispatch and placeholder edits happen.

### [CONCERN] Some verification gates are only manual or grep-based

- **"Constants defined once":** this is a technical requirement, but task 20 has no check for it, for example a grep for the marker literals outside `context.py`.
- **`except` check:** the `grep "except Exception\|except:"` check would miss `except (OSError, Exception)`, though it is fine for the common cases.
- **"No more than ~300 lines":** task 20 says "much over 300" without a threshold. Give a number.

### [NOTE] Test selector expressions are brittle

Task 11 uses a compound `-k` expression. Names such as `test_rules_exclude_cf_failure_stops_setup`, `test_flags_before_target` and `test_flags_root_outside_guide` exist in `tests/setup_ide`. Several fragments (`fresh and claude`, `CLAUDE-claude`, `subdirectory`) match parametrized IDs I did not verify. The task already tells the implementer to check which target each selected test runs. Task 16's full run is the real backstop.

### [NOTE] Mutation check, docs and status tasks trace to the design

Task 17 (mutation check), task 21 (README and CHANGELOG), and task 22 (walkthrough and status) all come from the design's Migration Plan and Success Criteria. The task file does not violate the rule against merge tasks: task 22 says "Do not merge". Task 22 also checks off slice 121 in the slice plan. That is reasonable, but it is not in the design's success criteria.

### Run Digest

- Response length: 5782 chars
- Response is newline-free: no
- Tool calls made: 3
- Tool calls failed: 0
- Stop reason: end_turn
- Output budget: backend default
- System prompt: preset+append
- Settings sources: project
- Reasoning characters: 0
- Effort: backend default
- Turns: not computed
- Tokens — prompt / cached / completion / reasoning: not computed / not computed / not computed / not computed
- Duration: 37.3 s
- `## Summary` located: yes
- `## Findings` located: yes
- Finding-shaped matches — whole response: 8
- Finding-shaped matches — inside fences: 0
- Finding-shaped matches — in findings section: 8
- Finding-shaped matches — surviving validation: 8
