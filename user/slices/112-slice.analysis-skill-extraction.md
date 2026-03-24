---
docType: slice-design
slice: analysis-skill-extraction
project: ai-project-guide
parent: user/architecture/110-slices.schema-and-phases-update.md
dependencies: [111-phase-renumbering-and-initiative-plan]
interfaces: [113-cross-reference-verification]
dateCreated: 20260324
dateUpdated: 20260324
status: not_started
---

# Slice Design: Analysis Skill Extraction

## Overview

Extract the five analysis prompts from `prompt.ai-project.system.md` into a single combined Claude Code skill (`/analyze`), add skill deployment to the `setup-ide` script, and remove the prompts from the system prompt file. This reduces token cost for non-analysis sessions while keeping the analysis workflow accessible on demand.

## Value

The five analysis prompts (~180 lines) are injected into every context assembly but used rarely. Moving them to a skill means:
- Zero token cost when not in use (only the skill description is in context)
- Single `/analyze` command surfaces the full analysis workflow
- `setup-ide` handles deployment — same pattern as rules and agents

## Technical Scope

### Included

- New skill file: `project-guides/skills/analyze/SKILL.md`
- `setup-ide` update: add skills copy step for `claude` target
- Remove five analysis prompts from `prompt.ai-project.system.md`
- Retain analysis context profiles in the prompt file (needed by cf)

### Excluded

- Changes to context-forge's ContextProfileParser (separate project)
- New analysis prompts or workflow changes — this is a move, not a rewrite
- Cursor skill support (Cursor doesn't have a skills mechanism)

## Architecture

### Skill Structure

```
project-guides/skills/
  analyze/
    SKILL.md
```

The skill combines five existing prompts into workflow stages within one document:

1. **Analyze Codebase** — discovery/reconnaissance of an existing codebase
2. **Analysis Processing** — categorize findings by priority (P0-P3), create analysis document
3. **Analysis Task Creation** — convert analysis findings into granular task files
4. **Analysis to LLD** — (rare) create a low-level design from analysis findings
5. **Analysis Task Implementation** — execute tasks from analysis findings

### Skill Frontmatter

```yaml
---
name: analyze
description: Codebase analysis workflow — discover, categorize findings, create tasks, and implement fixes
disable-model-invocation: true
---
```

`disable-model-invocation: true` ensures the skill only activates on explicit `/analyze` invocation, not automatically.

### setup-ide Update

Add a skills copy function to the `claude` target in `scripts/setup-ide`, following the same pattern as agents:

```
project-guides/skills/ → .claude/skills/
```

Copy entire skill directories (preserving the `name/SKILL.md` structure). Skip if no skills directory exists.

### Prompt File Changes

- Remove the five analysis prompt sections (Analyze Codebase, Analysis Processing, Analysis Task Creation, Analysis to LLD, Analysis Task Implementation)
- Keep the analysis context profiles (lines 36-39 in the context_profiles block) — these are lightweight key-value mappings used by cf
- Keep the Analyze Codebase note comment if useful, or remove if the skill replaces it entirely

## Success Criteria

### Functional Requirements
- [ ] Skill file exists at `project-guides/skills/analyze/SKILL.md`
- [ ] Skill contains all five analysis workflow stages
- [ ] `setup-ide claude` copies skills to `.claude/skills/`
- [ ] Five analysis prompts removed from `prompt.ai-project.system.md`
- [ ] Analysis context profiles retained in prompt file
- [ ] `/analyze` is usable in Claude Code after running `setup-ide claude`

### Verification Walkthrough
1. Confirm `project-guides/skills/analyze/SKILL.md` exists and contains all five stages
2. Run `scripts/setup-ide claude` (or dry-run equivalent) — verify `.claude/skills/analyze/SKILL.md` is created
3. `grep -c "Analysis Processing\|Analysis Task Creation\|Analysis to LLD\|Analysis Task Implementation\|Analyze Codebase" project-guides/prompt.ai-project.system.md` — should return 0 for prompt sections (context profile keys may still match)
4. Verify context_profiles block still contains analysis entries
