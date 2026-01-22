---
layer: project
docType: slice
project: ai-project-guide
sliceIndex: 105
sliceName: project-guide-restructure
status: completed
completedVersion: 0.9.0
dependencies: []
description: Migration from git subtree to git submodule architecture
lastUpdated: 2025-10-06
---

# Slice: Restructured ai-project-guide Layout

## User-Provided Concept

**Problem:** Current git subtree integration for ai-project-guide is awkward and creates barriers for non-npm/pnpm projects (Python, etc.). Users can't easily update guides, and the mixing of framework guides with user project documents in the same directory creates confusion.

**Goal:** Restructure the layout to use git submodule for clean separation between:
- Framework guides (frequently updated, read-only)
- User project documents (constantly updated, git-tracked in user's repo)

This should work seamlessly for:
- npm/pnpm projects (existing tooling)
- Non-npm projects (Python, Go, etc.)
- Monorepo template development (existing project-artifacts pattern)

## HLD

### Target Directory Structure

```
/user-project/                           # User's main project (Python, React, etc.)
├── project-documents/                   # All project documentation
│   ├── ai-project-guide/               # Submodule (framework guides)
│   │   ├── project-guides/
│   │   ├── tool-guides/
│   │   ├── framework-guides/
│   │   ├── snippets/
│   │   └── ... (all framework content)
│   └── user/                        # User's project-specific work
│       ├── architecture/
│       ├── slices/
│       ├── tasks/
│       ├── features/
│       ├── reviews/
│       └── analysis/
```

### Key Principles

1. **Clean Separation**: Framework guides are isolated in submodule, user work stays in parent repo
2. **Easy Updates**: `git submodule update --remote` for guide updates
3. **No Conflicts**: User files never conflict with guide updates
4. **Backward Compatible**: Existing path references to `user/` work unchanged
5. **Universal**: Works for any language/toolchain

### Migration Path

**For existing projects using git subtree:**
1. Remove subtree content making sure to not accidentally lose existing project-documents/user
2. Add as submodule at `project-documents/ai-project-guide/`
3. Move user files to `project-documents/user/` (if not already there)

**For new projects:**
- Simple setup: `git submodule add https://github.com/ecorkran/ai-project-guide.git project-documents/ai-project-guide`

## LLD

### 1. Update npm Scripts (package.json)

**Current scripts that need updating:**
- `setup-guides`: Create new directory structure
- `update-guides`: Pull submodule updates (simplify - no more user/ preservation)
- `sync-guides`: May become simpler or obsolete

**New `setup-guides` behavior:**
```bash
# Create directory structure
mkdir -p project-documents/user/{architecture,slices,tasks,features,reviews,analysis}

# Add submodule
cd project-documents
git submodule add https://github.com/ecorkran/ai-project-guide.git

# Create .gitignore if needed
echo "# Keep user/ in version control" > user/.gitkeep
```

**New `update-guides` behavior:**
```bash
# Simply update the submodule
git submodule update --remote project-documents/ai-project-guide

# No longer needs to:
# - Copy out user/
# - Delete old files
# - Copy user/ back
```

### 2. Path References

**Current references (stay the same for user files):**
- `user/slices/...` ✓
- `user/tasks/...` ✓
- `user/architecture/...` ✓

**Guide references (need updating):**
- Change: `project-guides/...` → `project-documents/ai-project-guide/project-guides/...`
- Change: `tool-guides/...` → `project-documents/ai-project-guide/tool-guides/...`
- Change: `framework-guides/...` → `project-documents/ai-project-guide/framework-guides/...`

**Or use relative paths from project-documents context:**
- `ai-project-guide/project-guides/...`
- `ai-project-guide/tool-guides/...`
- `ai-project-guide/framework-guides/...`

### 3. Monorepo Compatibility

**Current monorepo pattern (preserves):**
```
project-artifacts/{template}/
├── slices/
├── tasks/
└── ... (project work, not checked into template)
```

**Guides move to submodule:**
```
project-documents/
└── ai-project-guide/          # Submodule
    ├── project-guides/
    └── ...
```

**Monorepo-specific changes:**
- Guides reference: `project-documents/ai-project-guide/...`
- Project work: Stays in `project-artifacts/` (unchanged)
- No contamination of templates with development documents

### 4. Documentation Updates

**Files needing path updates:**
- `readme.md` - Installation instructions
- `prompt.ai-project.system.md` - Guide references
- `CLAUDE.md` - Any path references
- All `project-guides/*.md` files - Cross-references

**Search pattern for updates:**
```bash
# Find references to old paths
grep -r "project-guides/" --include="*.md"
grep -r "tool-guides/" --include="*.md"
grep -r "framework-guides/" --include="*.md"
```

### 5. Benefits

**For npm/pnpm projects:**
- Simpler scripts (no file copying dance)
- Standard git submodule workflow
- Existing `pnpm update-guides` just needs path update

**For non-npm projects:**
- Standard git commands work
- No special tooling required
- Same structure as npm projects

**For all projects:**
- Clean separation of concerns
- No merge conflicts between framework and user work
- Easy to understand what's what
- Framework updates don't touch user files

## Implementation Tasks

1. **Update npm scripts** (package.json)
   - Modify `setup-guides` for new structure
   - Simplify `update-guides` (just submodule update)
   - Review `sync-guides` necessity

2. **Update path references**
   - Search and replace guide paths in all documentation
   - Test all prompts work with new paths
   - Update monorepo-specific references

3. **Update readme.md**
   - New installation instructions
   - Submodule setup for both npm and non-npm
   - Migration guide for existing projects

4. **Test migration**
   - Test in npm/pnpm project
   - Test in Python project
   - Test in monorepo development
   - Verify all prompts work

5. **Create migration documentation**
   - Step-by-step for existing projects
   - Troubleshooting guide
   - FAQ for common issues

## Success Criteria

- ✓ New project setup works for npm, pnpm, Python projects
- ✓ Guide updates via standard `git submodule update --remote`
- ✓ User files stay in parent repo, never conflict with guide updates
- ✓ Monorepo development unaffected (continues using project-artifacts)
- ✓ All existing prompts work with new structure
- ✓ Documentation clearly explains new layout
- ✓ Migration path documented for existing projects

## Notes

- This is a breaking change for project layout, requires migration
- Consider versioning: announce as 0.9.0 or 1.0.0
- Provide migration script/guide for smooth transition
- Old subtree approach can be documented as "legacy" in migration guide
