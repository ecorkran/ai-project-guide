---
slice: analysis-skill-extraction
project: ai-project-guide
lld: user/slices/112-slice.analysis-skill-extraction.md
dependencies: [111-phase-renumbering-and-initiative-plan]
projectState: Slice 111 complete (v0.14.0). Prompt file still contains five analysis prompts.
dateCreated: 20260324
dateUpdated: 20260324
status: not_started
---

## Context Summary
- Working on analysis-skill-extraction slice (112)
- Moving five analysis prompts from prompt.ai-project.system.md into a single /analyze skill
- Adding skill deployment to setup-ide script
- Next planned slice: 110 (YAML Schema Standardization)

---

### Task 1: Create Combined Analysis Skill
**Objective**: Create `project-guides/skills/analyze/SKILL.md` combining all five analysis prompts into workflow stages.

- [ ] Create directory `project-guides/skills/analyze/`
- [ ] Create `SKILL.md` with frontmatter:
  ```yaml
  ---
  name: analyze
  description: Codebase analysis workflow — discover, categorize findings, create tasks, and implement fixes
  disable-model-invocation: true
  ---
  ```
- [ ] Include an overview section explaining the analysis workflow and its stages
- [ ] Include all five stages, each as a clearly labeled section:
  - [ ] **Stage 1: Analyze Codebase** — discovery/reconnaissance (from current "Analyze Codebase" prompt). Note: the front-end-specific sections (NextJS, React, Tailwind) should be included but marked as applicable only to front-end projects.
  - [ ] **Stage 2: Analysis Processing** — categorize findings by P0-P3 priority, create analysis document (from current "Analysis Processing" prompt)
  - [ ] **Stage 3: Analysis Task Creation** — convert findings to granular task files (from current "Analysis Task Creation" prompt)
  - [ ] **Stage 4: Analysis to LLD** — create low-level design from findings (from current "Analysis to LLD" prompt). Note this is rarely used.
  - [ ] **Stage 5: Analysis Task Implementation** — execute analysis tasks (from current "Analysis Task Implementation" prompt)
- [ ] Include usage guidance: user invokes `/analyze` and specifies which stage, or starts from stage 1 for a full workflow
- [ ] Preserve all substantive content from the original prompts — this is a move, not a rewrite
- [ ] Success criteria:
  - [ ] File exists at `project-guides/skills/analyze/SKILL.md`
  - [ ] All five workflow stages present with complete content
  - [ ] Frontmatter includes `disable-model-invocation: true`

**Commit**: `guides: create combined /analyze skill from analysis prompts`

---

### Task 2: Update setup-ide Script for Skills
**Objective**: Add skills copy support to `scripts/setup-ide` for the `claude` target.

- [ ] Add a `copy_skills` function that:
  - [ ] Takes source dir and target dir as parameters
  - [ ] Copies entire skill directories (preserving `name/SKILL.md` structure)
  - [ ] Follows the same logging/output pattern as existing `copy_files` function
- [ ] Set skills source directory alongside existing source dirs:
  ```
  SKILLS_SOURCE_DIR="$SCRIPT_DIR/../project-guides/skills"
  ```
  (and the equivalent for submodule path)
- [ ] Add skills copy step to the `claude` section of `main()`, after agents:
  - [ ] `mkdir -p "$TARGET_ROOT/.claude/skills"`
  - [ ] Copy from `$SKILLS_SOURCE_DIR` to `.claude/skills/`
  - [ ] Skip gracefully if no skills directory exists (matching agents pattern)
- [ ] Update the setup complete output to mention skills:
  ```
  echo "   • Skills copied to .claude/skills/"
  ```
- [ ] Success criteria:
  - [ ] Running `setup-ide claude` copies `project-guides/skills/analyze/` to `.claude/skills/analyze/`
  - [ ] Script handles missing skills directory gracefully (no error)
  - [ ] Output messages follow existing style

**Commit**: `feat: add skills deployment to setup-ide script`

---

### Task 3: Remove Analysis Prompts from System Prompt File
**Objective**: Remove the five analysis prompt sections from `prompt.ai-project.system.md` while retaining context profiles.

- [ ] Remove the following prompt sections from the file:
  - [ ] "##### Analyze Codebase" section and its code block
  - [ ] "##### Analysis Processing" section and its code block
  - [ ] "##### Analysis Task Creation" section and its code block
  - [ ] "##### Analysis to LLD" section and its code block
  - [ ] "##### Analysis Task Implementation" section and its code block
- [ ] Verify the context_profiles block still contains analysis entries:
  ```yaml
  analysis-processing:               [fileSlice, fileTasks]
  analysis-task-creation:            [fileTasks]
  analysis-to-lld:                   [fileSlice]
  analysis-task-implementation:      [fileSlice, fileTasks]
  analyze-codebase:                  []
  ```
- [ ] Verify no orphaned headings or extra whitespace left behind
- [ ] Success criteria:
  - [ ] Zero analysis prompt sections in the file
  - [ ] Context profiles block still contains all analysis entries
  - [ ] File structure remains clean

**Commit**: `guides: remove analysis prompts from system prompt file (moved to /analyze skill)`

---

### Task 4: Verification
**Objective**: Confirm the extraction is complete and functional.

- [ ] `ls project-guides/skills/analyze/SKILL.md` — file exists
- [ ] `grep -c "disable-model-invocation" project-guides/skills/analyze/SKILL.md` — returns 1
- [ ] Verify all five stages are present in the skill file
- [ ] `grep "##### Analyze Codebase\|##### Analysis Processing\|##### Analysis Task Creation\|##### Analysis to LLD\|##### Analysis Task Implementation" project-guides/prompt.ai-project.system.md` — should return no matches
- [ ] `grep "analysis-processing\|analysis-task-creation\|analysis-to-lld\|analysis-task-implementation\|analyze-codebase" project-guides/prompt.ai-project.system.md` — should return matches (context profiles retained)
- [ ] Dry-run or actual run of `setup-ide claude` in the ai-project-guide repo — verify `.claude/skills/analyze/SKILL.md` is created
- [ ] Success criteria:
  - [ ] All checks pass

**Commit**: `guides: verify analysis skill extraction complete`
