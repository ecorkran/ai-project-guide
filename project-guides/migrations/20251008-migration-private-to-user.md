---
docType: migration
scope: project-wide
description: v0.10.0 migration - private/ to user/ directory rename
version: "0.10.0"
status: obsolete
created: 20251008
lastUpdated: 20260121
---

# v0.10.0 Migration: private/ → user/

> **Status: OBSOLETE** - This migration applies to projects upgrading from v0.9.x to v0.10.0. If you're on v0.10.0 or later, this has already been applied.

This release renames `project-documents/private/` to `project-documents/user/` for clarity and includes environment variable updates.

### What Changed

1. **Directory Rename**: `project-documents/private/` → `project-documents/user/`
2. **Environment Variable**: `ORG_PRIVATE_GUIDES_URL` → `EXTERNAL_PROJECT_DOC_URL`
3. **All Documentation**: Updated to reference `user/` instead of `private/`

### Why This Change?

- **Clearer naming**: "private" implied secrecy, but this directory contains your project work (which should be committed)
- **Better mental model**: "user" clearly indicates "your work" vs "framework" (ai-project-guide) vs "external" (imported guides)
- **Reduced confusion**: Eliminates questions about whether files should be committed or kept private

### Migration Steps

#### Automatic Migration (Recommended)

Use the provided migration script:

```bash
# From your project root
bash project-documents/ai-project-guide/scripts/migrate-private-to-user.sh
```

This script will:
- Rename `project-documents/private/` → `project-documents/user/`
- Update all internal references in your files
- Preserve git history
- Report what was changed

#### Manual Migration

If you prefer manual migration:

```bash
# 1. Rename the directory
git mv project-documents/private project-documents/user

# 2. Update references in your files (if any)
# Search for "private/" in your user/ directory and replace with "user/"
grep -r "private/" project-documents/user/
# Then manually update those files

# 3. Commit
git add -A
git commit -m "Migrate private/ to user/"
```

### Environment Variables

If you're using external guides:

**Old**:
```bash
export ORG_PRIVATE_GUIDES_URL=git@github.com:yourorg/guides.git
```

**New**:
```bash
export EXTERNAL_PROJECT_DOC_URL=git@github.com:yourorg/guides.git
```

Update in:
- Your shell profile (`~/.bashrc`, `~/.zshrc`, etc.)
- CI/CD environment variables
- Team documentation

### Verification

After migration, verify:

```bash
# Check directory exists
ls project-documents/user/

# Check git history preserved
git log --follow project-documents/user/tasks/

# Ensure ai-project-guide submodule updated
git submodule update --remote project-documents/ai-project-guide
```

### What If I Don't Migrate?

- ❌ New versions of ai-project-guide reference `user/`, not `private/`
- ❌ Documentation and prompts won't find your files
- ❌ Scripts will look in wrong directory

**Recommendation**: Migrate as soon as possible.

### Rollback

If you need to rollback temporarily:

```bash
git mv project-documents/user project-documents/private
# Then restore to previous ai-project-guide version
cd project-documents/ai-project-guide
git checkout <previous-version-tag>
```

### Support

- **Issues**: [GitHub Issues](https://github.com/ecorkran/ai-project-guide/issues)
- **Questions**: Check updated documentation in `readme.md`
- **Script problems**: The migration script is idempotent - safe to run multiple times
