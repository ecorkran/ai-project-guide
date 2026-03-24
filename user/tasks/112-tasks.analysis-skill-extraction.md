---
slice: analysis-skill-extraction
project: ai-project-guide
lld: user/slices/112-slice.analysis-skill-extraction.md
dependencies: [111-phase-renumbering-and-initiative-plan]
projectState: Slice 111 complete (v0.14.0). Prompt file still contains five analysis prompts.
dateCreated: 20260324
dateUpdated: 20260324
status: complete
---

## Context Summary
- Working on analysis-skill-extraction slice (112)
- Moving five analysis prompts from prompt.ai-project.system.md into a single /analyze skill
- Adding skill deployment to setup-ide script
- Next planned slice: 110 (YAML Schema Standardization)

---

### Task 1: Create Combined Analysis Skill
**Objective**: Create `project-guides/skills/analyze/SKILL.md` combining all five analysis prompts into workflow stages.

- [x] Create directory `project-guides/skills/analyze/`
- [x] Create `SKILL.md` with frontmatter:
  ```yaml
  ---
  name: analyze
  description: Codebase analysis workflow — discover, categorize findings, create tasks, and implement fixes
  disable-model-invocation: true
  ---
  ```
- [x] Include an overview section explaining the analysis workflow and its stages
- [x] Include all five stages, each as a clearly labeled section:
  - [x] **Stage 1: Analyze Codebase** — discovery/reconnaissance (from current "Analyze Codebase" prompt). Note: the front-end-specific sections (NextJS, React, Tailwind) should be included but marked as applicable only to front-end projects.
  - [x] **Stage 2: Analysis Processing** — categorize findings by P0-P3 priority, create analysis document (from current "Analysis Processing" prompt)
  - [x] **Stage 3: Analysis Task Creation** — convert findings to granular task files (from current "Analysis Task Creation" prompt)
  - [x] **Stage 4: Analysis to LLD** — create low-level design from findings (from current "Analysis to LLD" prompt). Note this is rarely used.
  - [x] **Stage 5: Analysis Task Implementation** — execute analysis tasks (from current "Analysis Task Implementation" prompt)
- [x] Include usage guidance: user invokes `/analyze` and specifies which stage, or starts from stage 1 for a full workflow
- [x] Preserve all substantive content from the original prompts — this is a move, not a rewrite
- [x] Success criteria:
  - [x] File exists at `project-guides/skills/analyze/SKILL.md`
  - [x] All five workflow stages present with complete content
  - [x] Frontmatter includes `disable-model-invocation: true`

**Commit**: `guides: create combined /analyze skill from analysis prompts`

---

### Task 2: Update setup-ide Script for Skills
**Objective**: Add skills copy support to `scripts/setup-ide` for the `claude` target.

- [x] Add a `copy_skills` function that:
  - [x] Takes source dir and target dir as parameters
  - [x] Copies entire skill directories (preserving `name/SKILL.md` structure)
  - [x] Follows the same logging/output pattern as existing `copy_files` function
- [x] Set skills source directory alongside existing source dirs:
  ```
  SKILLS_SOURCE_DIR="$SCRIPT_DIR/../project-guides/skills"
  ```
  (and the equivalent for submodule path)
- [x] Add skills copy step to the `claude` section of `main()`, after agents:
  - [x] `mkdir -p "$TARGET_ROOT/.claude/skills"`
  - [x] Copy from `$SKILLS_SOURCE_DIR` to `.claude/skills/`
  - [x] Skip gracefully if no skills directory exists (matching agents pattern)
- [x] Update the setup complete output to mention skills:
  ```
  echo "   • Skills copied to .claude/skills/"
  ```
- [x] Success criteria:
  - [x] Running `setup-ide claude` copies `project-guides/skills/analyze/` to `.claude/skills/analyze/`
  - [x] Script handles missing skills directory gracefully (no error)
  - [x] Output messages follow existing style

**Commit**: `feat: add skills deployment to setup-ide script`

---

### Task 3: Remove Analysis Prompts from System Prompt File
**Objective**: Remove the five analysis prompt sections from `prompt.ai-project.system.md` while retaining context profiles.

- [x] Remove the following prompt sections from the file:
  - [x] "##### Analyze Codebase" section and its code block
  - [x] "##### Analysis Processing" section and its code block
  - [x] "##### Analysis Task Creation" section and its code block
  - [x] "##### Analysis to LLD" section and its code block
  - [x] "##### Analysis Task Implementation" section and its code block
- [x] Verify the context_profiles block still contains analysis entries:
  ```yaml
  analysis-processing:               [fileSlice, fileTasks]
  analysis-task-creation:            [fileTasks]
  analysis-to-lld:                   [fileSlice]
  analysis-task-implementation:      [fileSlice, fileTasks]
  analyze-codebase:                  []
  ```
- [x] Verify no orphaned headings or extra whitespace left behind
- [x] Success criteria:
  - [x] Zero analysis prompt sections in the file
  - [x] Context profiles block still contains all analysis entries
  - [x] File structure remains clean

**Commit**: `guides: remove analysis prompts from system prompt file (moved to /analyze skill)`

---

### Task 4: Verification
**Objective**: Confirm the extraction is complete and functional.

- [x] `ls project-guides/skills/analyze/SKILL.md` — file exists
- [x] `grep -c "disable-model-invocation" project-guides/skills/analyze/SKILL.md` — returns 1
- [x] Verify all five stages are present in the skill file
- [x] `grep "##### Analyze Codebase\|##### Analysis Processing\|##### Analysis Task Creation\|##### Analysis to LLD\|##### Analysis Task Implementation" project-guides/prompt.ai-project.system.md` — should return no matches
- [x] `grep "analysis-processing\|analysis-task-creation\|analysis-to-lld\|analysis-task-implementation\|analyze-codebase" project-guides/prompt.ai-project.system.md` — should return matches (context profiles retained)
- [x] Dry-run or actual run of `setup-ide claude` in the ai-project-guide repo — verify `.claude/skills/analyze/SKILL.md` is created
- [x] Success criteria:
  - [x] All checks pass

**Commit**: `guides: verify analysis skill extraction complete`
