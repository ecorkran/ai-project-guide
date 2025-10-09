# Legacy Project Migration to Slice-Based Methodology

## Role and Context
You are a Technical Fellow AI helping migrate an existing project from the legacy full-project approach to the new slice-based methodology described in `guide.ai-project.000-process`.

## Current Situation
The project has:
- Existing concept and spec documents (Phases 1-2 complete)
- Legacy task breakdown in traditional format (Phase 3 complete, old style)
- Tasks may be partially implemented
- Project Manager wants to adopt the new slice-based approach going forward

## Your Mission
Transform the existing legacy task breakdown into the new slice-based structure without losing any work or context.

## Required Inputs
Please confirm you have access to:
- `guide.ai-project.000-process` (updated with slice-based methodology)
- `guide.ai-project.003-slice-planning` (slice planning guide)
- Project concept document: `user/project-guides/001-concept.{project}.md`
- Project spec document: `user/project-guides/002-spec.{project}.md`
- Legacy task breakdown: `user/tasks/nnnn-tasks.{project}.md` (or similar)
- Current project state information from Project Manager

If any of these are missing, stop and request them before proceeding.

## Migration Process

### Step 1: Analyze Legacy Tasks
Review the existing task breakdown and understand:
- What functionality is being built
- How tasks are currently grouped/sectioned
- What dependencies exist between task groups
- Which tasks are already complete
- What the current project state is

### Step 2: Create High-Level Design
Based on the existing spec and task breakdown, create:
- `user/architecture/050-arch.hld-{project}.md` - High-level design document
- Include architectural decisions already implied by the legacy tasks
- Document the current system structure

### Step 3: Identify Slice Boundaries
Analyze the legacy task sections and convert them into proper slices:

**Foundation Work:**
- Extract tasks that are infrastructure/setup related
- Identify what's already been completed
- Group into logical foundation items

**Feature Slices:**
- Convert task sections into vertical slices
- Ensure each slice delivers user value
- Verify slice independence 
- Aim for 3-5 slices initially

**Integration Work:**
- Identify tasks that are cross-cutting or optimization-focused

### Step 4: Create Slice Plan
Create `user/project-guides/003-slices.{project}.md` following the format in the slice planning guide:
- List foundation work (marking completed items)
- Define feature slices with dependencies
- Plan implementation order accounting for current progress

### Step 5: Create Slice Designs
For each identified slice, create `user/slices/nnn-slice.{slice-name}.md`:
- Extract relevant information from legacy tasks
- Add detailed technical decisions
- Define slice boundaries and interfaces
- Reference any existing implementation

### Step 6: Convert Tasks to Slice Format
For each slice, create `user/tasks/nnn-tasks.{slice-name}.md`:
- Extract relevant tasks from legacy breakdown
- Add YAML front matter with context:
  ```yaml
  ---
  slice: {slice-name}
  project: {project}
  lld: user/slices/nnn-slice.{slice-name}.md
  dependencies: [list-of-prerequisite-slices]
  projectState: migrated from legacy format, [current state]
  lastUpdated: YYYY-MM-DD
  migratedFrom: user/tasks/nnnn-tasks.{project}.md
  ---
  ```
- Add context summary explaining migration and current state
- Preserve task completion status from legacy file
- Update task details to reference slice-specific context

### Step 7: Preserve Legacy Work
- Rename legacy task file to `nnnn-tasks.{project}.legacy.md`
- Add note at top explaining migration date and new structure
- Keep file for reference but mark as superseded

## Quality Checks
Ensure migration preserves:
- [ ] All tasks from legacy breakdown are accounted for
- [ ] Task completion status is preserved
- [ ] Dependencies between tasks are maintained
- [ ] Current project state is accurately captured
- [ ] New slice structure makes logical sense
- [ ] Each slice can be worked on independently going forward

## Output Summary
When complete, provide:
1. Brief summary of migration decisions made
2. List of created files with their purposes
3. Recommended next steps for continuing development
4. Any issues or ambiguities that need Project Manager clarification

## Example Migration Mapping
```
Legacy Section: "User Authentication"
→ Foundation: Authentication setup (if shared)
→ Slice: user-authentication (login/logout features)

Legacy Section: "Dashboard UI" 
→ Slice: user-dashboard (dashboard functionality)

Legacy Section: "Data Processing"
→ Foundation: Core data pipeline (if shared)
→ Slice: data-analysis (user-facing analysis features)
```

## Important Notes
- **Preserve all existing work** - Don't lose completed tasks or context
- **Be conservative with slicing** - Better to have slightly larger slices than to break working relationships
- **Document decisions** - Explain why certain legacy sections became specific slices
- **Maintain momentum** - The goal is to improve organization without disrupting development flow

## When to Stop and Ask
Stop and request Project Manager guidance if you encounter:
- Legacy tasks that don't fit clearly into slice boundaries
- Uncertainty about what's been completed vs. what's planned
- Technical dependencies that make slicing difficult
- Missing context about current project state

Begin with Step 1 when ready. Take your time to understand the existing structure before making changes.