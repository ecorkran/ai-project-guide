---
docType: template
layer: process
purpose: migration-prompt-for-user-projects
audience: [ai]
description: Prompt template for updating project references after submodule migration
---

# Prompt: Update Project Documentation References for Submodule Structure

## Context

This project has migrated from a git subtree to git submodule structure for ai-project-guide (version 0.9.0). The framework guides have moved from the root of `project-documents/` to a submodule at `project-documents/ai-project-guide/`.

Your task is to update all references in the project's private documentation files to point to the new submodule paths.

## Files to Update

Search and update references in ALL files under:
- `project-documents/user/slices/`
- `project-documents/user/tasks/`
- `project-documents/user/features/`
- `project-documents/user/architecture/`
- `project-documents/user/reviews/`
- `project-documents/user/analysis/`
- `project-documents/user/project-guides/` (if it exists)

## Path Transformations

Update the following path references:

### Guide Directories

**Old Path → New Path**

```
project-documents/project-guides/     → project-documents/ai-project-guide/project-guides/
project-documents/tool-guides/        → project-documents/ai-project-guide/tool-guides/
project-documents/framework-guides/   → project-documents/ai-project-guide/framework-guides/
project-documents/snippets/           → project-documents/ai-project-guide/snippets/
project-documents/domain-guides/      → project-documents/ai-project-guide/domain-guides/
```

### Relative Path References

If you find relative references like:

```
../project-guides/              → ../ai-project-guide/project-guides/
../../project-guides/           → ../../ai-project-guide/project-guides/
```

### Specific Files Often Referenced

Common file references to update:

```
project-guides/guide.ai-project.000-process.md
  → ai-project-guide/project-guides/guide.ai-project.000-process.md

project-guides/guide.ai-project.090-code-review.md
  → ai-project-guide/project-guides/guide.ai-project.090-code-review.md

tool-guides/{tool}/introduction.md
  → ai-project-guide/tool-guides/{tool}/introduction.md

snippets/npm-scripts.ai-support.json
  → ai-project-guide/snippets/npm-scripts.ai-support.json
```

## What NOT to Change

**Do NOT modify:**
- References to `user/` directories (these stay as-is)
- References like `project-documents/user/slices/` (correct, no change needed)
- File paths within the same directory (e.g., references between task files)
- External URLs or absolute paths outside the project
- Code examples or quoted text unless they're actual path references

## Process

### Step 1: Search for references

```bash
grep -r "project-guides\|tool-guides\|framework-guides\|snippets\|domain-guides" project-documents/user/
```

### Step 2: For each file with matches

- Read the file
- Identify each occurrence
- Determine if it's a path reference that needs updating
- Update the path to include `ai-project-guide/` in the correct position
- Preserve the rest of the path structure

### Step 3: Verify your changes

- Ensure no broken references
- Check that relative paths still resolve correctly
- Make sure you didn't accidentally modify code examples or non-path text

## Example Transformations

### Example 1: Task File

**Before:**
```markdown
See `project-guides/guide.ai-project.000-process.md` for the overall process.

Refer to tool-guides/nextjs/introduction.md for Next.js setup.
```

**After:**
```markdown
See `ai-project-guide/project-guides/guide.ai-project.000-process.md` for the overall process.

Refer to ai-project-guide/tool-guides/nextjs/introduction.md for Next.js setup.
```

### Example 2: Slice Design with Relative Paths

**Before:**
```markdown
---
dependsOn:
  - ../../project-guides/guide.ai-project.002-spec.md
---

Consult ../tool-guides/react/ for component patterns.
```

**After:**
```markdown
---
dependsOn:
  - ../../ai-project-guide/project-guides/guide.ai-project.002-spec.md
---

Consult ../ai-project-guide/tool-guides/react/ for component patterns.
```

### Example 3: What NOT to Change

**Keep as-is:**
```markdown
Task file location: user/tasks/100-tasks.auth.md  ✅ (correct, no change)
See user/slices/100-slice.user-auth.md           ✅ (correct, no change)
```

## Output Requirements

After completing the updates:

1. **List all files modified** with a count of changes per file
2. **Report any ambiguous cases** where you weren't sure if a reference should be updated
3. **Confirm completion** when all references have been updated

## Important Notes

- **Case sensitivity**: Path references may appear in various cases (kebab-case, etc.) - preserve the original casing
- **File extensions**: Preserve all file extensions (.md, .json, etc.)
- **Markdown links**: Update paths inside markdown link syntax `[text](path)` and inline code \`path\`
- **YAML frontmatter**: Update paths in YAML metadata blocks
- **Comments**: Update path references in comments

## Questions to Ask if Unclear

If you encounter any of these situations, stop and ask the user:

1. References to paths that don't match the patterns above
2. Files outside of `project-documents/user/` that might need updating
3. Ambiguous references that could be either paths or just text
4. Custom directory structures not covered in this prompt

---

## Usage

Give this prompt to an AI assistant working on your project:

**"Please follow the instructions in `scripts/template-stubs/prompt.legacy-migration.md` to update all path references in my project-documents/user/ files to the new submodule structure."**

---

**Ready to proceed? Start by searching for all references to the old paths in `project-documents/user/` and report what you find.**
