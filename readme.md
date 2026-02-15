---
docType: repository-overview
---
# AI Project Guide

> **A structured methodology and toolset for AI-assisted software development**. Organizes project knowledge and provides workflows for effective human+AI collaboration on complex projects.

**What it does:**
- Organizes project knowledge into AI-readable formats
- Provides methodology for breaking down complex work
- Includes guides for frameworks, libraries, and APIs
- Enforces consistent code patterns and architecture

**Works with:** Claude Code, Cursor, Windsurf, and any AI coding tool

**Highly recommended:** Use with [Context Forge](https://github.com/ecorkran/context-forge) (free) - automatically manages contexts and streamlines the entire workflow.


## 🚀 Quick Start

### For manta-templates Projects
**Easiest option** - Complete templates with pre-configured setup. Currently supporting React, Electron, and Next.js.

See: [manta-templates](https://github.com/manta-digital/manta-templates) | Demo: https://templates.manta.digital

```bash
pnpm setup-guides
pnpm update-guides
```

### For Python, Go, Rust, or Any Project
**Prerequisites:** Ensure you're in a git repository (`git init` if needed - no remote required).

**One-command setup:**

```bash
curl -fsSL https://raw.githubusercontent.com/ecorkran/ai-project-guide/main/scripts/bootstrap.sh | bash
```

Creates directory structure and adds ai-project-guide as submodule.

**Update later, explicit:**
```sh
git submodule update --remote project-documents/ai-project-guide
git add project-documents/ai-project-guide
git commit -m "Update ai-project-guide submodule"
```

**Update later, script utility:**
```bash
./scripts/update-guides
```


(Bootstrap creates this script for you)

### IDE Setup (Cursor/Windsurf/Claude)

After adding the guides to your project, set up IDE rules for enhanced AI assistance:

```bash
# For npm/pnpm projects
pnpm setup-cursor     # For Cursor IDE
pnpm setup-windsurf   # For Windsurf IDE
pnpm setup-claude     # For Claude Code agent

# For other projects (run from project root)
./project-documents/ai-project-guide/scripts/setup-ide cursor
./project-documents/ai-project-guide/scripts/setup-ide windsurf
./project-documents/ai-project-guide/scripts/setup-ide claude
```

This copies all project rules to your IDE's configuration directory, handles file renaming (`.md` to `.mdc` for Cursor), generates `CLAUDE.md` for Claude Code, and validates frontmatter requirements.

**📍 Important:** The script creates `.cursor/` and `.windsurf/` directories in your project root (not inside `project-documents/`). For Claude, it creates `CLAUDE.md` in your project root (currently has a known issue where it may create in `project-documents/ai-project-guide/` - will be fixed soon).



## 🛠️ How to Use

### 💡 Recommended: Use with Context Forge
**[Context Forge](https://github.com/ecorkran/context-forge)** (free) automatically manages contexts and provides initialization prompts - making the workflow seamless. Highly recommended.

### The Workflow

**Initial planning** (Phases 1-4): Describe your concept, work with AI to refine it into specs and plans.

**Ongoing development** (Phases 5-7): Create tasks and implement features. This is where you'll spend most of your time - continuously adding slices, breaking them into tasks, and implementing.

### 🆕 New Projects

#### Phase 1: Concept Document
1. Create: `project-documents/user/project-guides/001-concept.{project}.md`
2. Add your concept in "User-Provided Concept" section
3. AI enhances with structured analysis

#### Phase 2: Specification
Create `002-spec.{project}.md` - AI adds detailed requirements, tech stack, architecture.

#### Phase 3: Slice Planning
Break work into **slices** - complete, independently implementable pieces (e.g., "user auth", "data pipeline", "reporting dashboard").

#### Phase 4: Slice Design
Detailed design for each slice: `nnn-slice.{slice-name}.md` in `user/slices/`

#### Phase 5: Task Breakdown
AI converts slices into tasks: `nnn-tasks.{slice}.md` in `user/tasks/`

#### Phase 6: Task Enhancement
AI refines tasks for clarity and implementability.

#### Phase 7: Implementation
AI implements code, runs tests, checks off completed items.

**Architecture**: Add when needed - HLD typically at `user/architecture/050-arch.hld-{project}.md`, additional docs use next available index (051, 052, etc.)

**Ongoing**: Continue building slices, features, and tasks as project evolves.


## ⚡ Ongoing Development

**Context Forge handles this automatically.** For manual workflow, Context Forge provides initialization prompts for each session.

### ✨ Feature Development
Create: `user/features/nnn-feature.{feature}.md` with "User-Provided Concept" section. AI enhances and generates tasks.

### 🎯 Ad-Hoc Work
For small maintenance items, add to `user/tasks/950-tasks.maintenance.md`. Larger items need their own task file.



## 📚 Guide System Overview

### **1. Public Guides** (This Repository)
- Core methodology, tool guides, framework guides
- Updated frequently via git submodule
- Everyone gets these automatically

### **2. External Guides** (Optional, Advanced)
- Set via `EXTERNAL_PROJECT_DOC_URL` environment variable
- Imported into `user/` during bootstrap
- Gets committed with your project (not separate)
- **Note**: Advanced feature - additional functionality on hold pending demand

### **3. Project User Guides** (Your Work)
- **Location**: `project-documents/user/`
- Your project-specific work: concept, specs, tasks, reviews, architecture
- Always preserved, never overwritten
- Committed to your project's git repository




## 🔑 What lives where?

| Folder | Look here when you need…                                                                                                      |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **`project-guides/`** | Process & methodology docs that apply to *every* project (e.g., guide.ai-project.000-process, guide.ai-project.002-spec, Code Rules). |
| **`framework-guides/`** | App-level runtimes or platforms that own the entire build/runtime cycle (Next.js, Astro, Flutter, Qt…).                       |
| **`tool-guides/`** | Importable libraries or UI kits you slot *into* an app (SciChart, Three.js, Tailwind…).                                       |
| **`api-guides/`** | External data or service endpoints accessed over HTTP/gRPC (USGS Water Services, ArcGIS, Alpha Vantage…).                     |
| **`domain-guides/`** | Cross-cutting subject knowledge useful across many projects (game-development, hydrology, financial-visualisation…).          |
| **`snippets/`** | Language-agnostic code fragments and quick copy-paste helpers.                                                                |

*Full details and rationale live in [`project-documents/directory-structure.md`](project-documents/directory-structure.md).*




## 📐 Naming & formatting conventions

All file and folder names follow our kebab-case pattern and document-type prefixes outlined in [`file-naming-conventions.md`](project-documents/file-naming-conventions.md).    Please review that doc before adding or renaming files.



## 📦 Advanced Usage

### Manual Git Submodule Setup
If you prefer manual setup or need more control:

```bash
# Create directory structure
mkdir -p project-documents/user/{analysis,architecture,features,project-guides,reviews,slices,tasks}

# Add submodule
git submodule add https://github.com/ecorkran/ai-project-guide.git project-documents/ai-project-guide

# Create .gitkeep to track empty directories
echo '# Keep user/ in version control' > project-documents/user/.gitkeep

# Commit
git add .
git commit -m 'Add ai-project-guide'
```

### Migrating from Git Subtree (Legacy)
If you previously used git subtree, migrate to submodule:

```bash
# 1. Backup your work
cp -r project-documents/user ~/backup-user

# 2. Remove old subtree
git rm -r project-documents
git commit -m 'Remove subtree for migration to submodule'

# 3. Restore your work
git checkout HEAD~1 -- project-documents/user
# Or restore from backup if needed:
# cp -r ~/backup-user project-documents/user

# 4. Add as submodule
git submodule add https://github.com/ecorkran/ai-project-guide.git project-documents/ai-project-guide

# 5. Commit
git add .
git commit -m 'Migrate to git submodule structure'
```

**Benefits of submodule over subtree:**
- No merge conflicts between framework updates and your work
- Simpler update process
- Works universally (Python, Go, Rust, npm/pnpm, etc.)
- Standard git workflow



### For Other npm/pnpm Projects

Add to your `package.json`:
```json
"scripts": {
  "setup-guides": "mkdir -p project-documents/user/{analysis,architecture,features,project-guides,reviews,slices,tasks} && git submodule add https://github.com/ecorkran/ai-project-guide.git project-documents/ai-project-guide && echo '# Keep user/ in version control' > project-documents/user/.gitkeep || echo 'Submodule already exists—run npm run update-guides to update.'",
  "update-guides": "git submodule update --remote --merge project-documents/ai-project-guide && cd project-documents/ai-project-guide && git checkout main && git pull origin main && cd ../..",
  "setup-cursor": "project-documents/ai-project-guide/scripts/setup-ide cursor",
  "setup-windsurf": "project-documents/ai-project-guide/scripts/setup-ide windsurf",
  "setup-claude": "project-documents/ai-project-guide/scripts/setup-ide claude"
}
```

Then:
```bash
pnpm setup-guides
pnpm update-guides
```

### Monorepo Template Development

When working on templates in monorepo, `user/` maps to `project-artifacts/{template}/`. Same structure:
```
project-artifacts/
├── analysis/
├── architecture/
├── features/
├── project-guides/
├── reviews/
├── slices/
└── tasks/
```



## 🔄 Upgrading Existing Projects to v0.9.2+

If you're upgrading from an older version (v0.9.1 or earlier), you need a one-time update to use the new update system. After this, future updates work automatically.

### Upgrading npm/pnpm Projects

```bash
# 1. Update the ai-project-guide submodule
git submodule update --remote --merge
cd project-documents/ai-project-guide
git checkout main
git pull origin main
cd ../..

# 2. Edit package.json - change this line:
#    FROM: "update-guides": "bash scripts/update-guides.sh"
#    TO:   "update-guides": "bash project-documents/ai-project-guide/scripts/template-stubs/update-guides.sh"
# Open package.json in your editor and make this one-line change

# 3. Test the update
pnpm update-guides

# 4. Commit the changes
git add .
git commit -m "Update ai-project-guide to v0.9.2"
git push
```

**After this one-time update**, `pnpm update-guides` will always use the latest script from the submodule. No manual updates ever again.

### Upgrading Python/Other Projects

```bash
# 1. Update the ai-project-guide submodule
git submodule update --remote --merge
cd project-documents/ai-project-guide
git checkout main
git pull origin main
cd ../..

# 2. Create update-guides wrapper script
mkdir -p scripts
cat > scripts/update-guides << 'EOF'
#!/bin/bash
exec project-documents/ai-project-guide/scripts/template-stubs/update-guides.sh "$@"
EOF
chmod +x scripts/update-guides

# 3. Test the update
bash scripts/update-guides

# 4. Commit the changes
git add .
git commit -m "Update ai-project-guide to v0.9.2"
git push
```

**After this one-time update**, `bash scripts/update-guides` will always use the latest script from the submodule. No manual updates ever again.

---

## 📋 For Claude

Claude: please find code analysis details in [user/analysis/940-analysis.initial-codebase.md](user/analysis/940-analysis.initial-codebase.md).

---

## 🤝 Contributing
First, if you are using the AI Project Guide and found it useful enough to contribute or even report and issue, thank you. I'll try to respond to review PRs, and respond to issues & comments.
