---
docType: repository-overview
---
# AI Project Guides & Methodology

> Structured project guides and parameterized prompts that dramatically expand what AI tools can help you build. Helps turn complex issues into manageable, AI-assisted workflows.  Setup scripts provided for Claude Code, Windsurf and Cursor.  Highly recommended to use with context-builder, available here (free):
[text](https://github.com/ecorkran/context-builder)

The repository contains a comprehensive methodology for AI-assisted development, including:
- **8-phase slice-based process** with clear roles and workflows
- **Living document pattern** for collaborative human-AI design
- **Tool-specific guides** for frameworks, libraries, and APIs
- **Code rules and patterns** for consistent, maintainable code


## 🚀 Quick Start

### For manta-templates Projects
The easiest way to get going, currently supporting React, Electron, and Next.js. Available here: [manta-templates](https://github.com/manta-digital/manta-templates)

For a complete template with easy setup scripts and pre-configured project structure, this is the recommended starting point. See demo at https://templates.manta.digital.

Scripts are set up for you, just run:
```bash
pnpm setup-guides    # Initial setup
pnpm update-guides   # Update guides later
```

### For other npm/pnpm Projects
Add these scripts to your `package.json`:

```json
"scripts": {
  "setup-guides": "mkdir -p project-documents/private/{architecture,slices,tasks,features,reviews,analysis} && git submodule add https://github.com/ecorkran/ai-project-guide.git project-documents/ai-project-guide && echo '# Keep private/ in version control' > project-documents/private/.gitkeep || echo 'Submodule already exists—run npm run update-guides to update.'",
  "update-guides": "git submodule update --remote --merge project-documents/ai-project-guide && cd project-documents/ai-project-guide && git checkout main && git pull origin main && cd ../..",
  "setup-cursor": "project-documents/ai-project-guide/scripts/setup-ide cursor",
  "setup-windsurf": "project-documents/ai-project-guide/scripts/setup-ide windsurf",
  "setup-claude": "project-documents/ai-project-guide/scripts/setup-ide claude"
}
```

Then run:
```bash
pnpm setup-guides    # Initial setup
pnpm update-guides   # Update guides later
```

### For Python, Go, Rust, or Any Project
One command setup using our bootstrap script:

```bash
# Bash version (recommended)
curl -fsSL https://raw.githubusercontent.com/ecorkran/ai-project-guide/main/scripts/bootstrap.sh | bash

# Or Python version
curl -fsSL https://raw.githubusercontent.com/ecorkran/ai-project-guide/main/scripts/bootstrap.py | python3
```

This will:
- Auto-initialize git repo if needed
- Create `project-documents/private/` structure for your work
- Add ai-project-guide as a git submodule at `project-documents/ai-project-guide/`
- Provide clear next steps

**Update guides later:**
```bash
git submodule update --remote --merge project-documents/ai-project-guide
cd project-documents/ai-project-guide
git checkout main
git pull origin main
cd ../..
```

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

### 💡 Recommended: Use with Context Builder
**The easiest and most effective way to use AI Project Guide is with [Context Builder](https://github.com/ecorkran/context-builder)** (soon to become Context Forge). It automatically manages guide context, handles file organization, and streamlines the entire workflow. Within a few weeks, Context Forge will include a "pick a prompt" feature making it the complete solution for 99% of users.

For manual usage or to understand the underlying process, continue reading below.

### 🆕 New Projects
The project guide uses an 8-phase slice-based methodology. For simple projects, you can skip directly to task creation (Phases 1-2, then 5-8). For complex projects with multiple features, follow the full slice-based approach.  


#### 📝 Phase 1: Concept Document
Create a concept document that you and the AI will collaborate on:

1. **Create the file**: `project-documents/private/project-guides/001-concept.{project}.md`
2. **Add this structure**:
   ```markdown
   # Overview
   [One-sentence description of what this project is]

   ## User-Provided Concept
   [Your project description: goals, design ideas, target environments, technical details]
   ```
3. **Fill in your concept**: Describe your project in the User-Provided Concept section—can be simple or detailed
4. **Let AI enhance it**: The AI will preserve your concept and add structured sections (Project Concept, Design, Technical Approach, etc.)

This single living document approach keeps everything together instead of fragmenting across multiple files.


#### 📋 Phase 2: Specification
Same pattern—create `002-spec.{project}.md` with User-Provided Concept section. AI enhances it with detailed requirements, technical stack, architecture, and feature breakdown.


#### 🗺️ Phase 3: Slice Planning (Complex Projects Only)
For projects with multiple features, AI helps break the work into vertical slices—complete workflows that can be built independently. Simple projects skip to Phase 5.


#### 🔧 Phase 4: Slice Design (Complex Projects Only)
Create detailed low-level design for each slice. Saved as `nnn-slice.{slice-name}.md` in `private/slices/`.


#### 📝 Phase 5: Task Breakdown
AI converts your concept/spec/slices into actionable tasks:
- Creates `nnn-tasks.{project}.md` or `nnn-tasks.{slice}.md` in `private/tasks/`
- Each task has clear scope, instructions, and success criteria


#### ✨ Phase 6: Task Enhancement
AI examines tasks and expands/subdivides them to improve implementability. Tasks become more detailed and easier for AI to execute reliably.


#### 💻 Phase 7: Implementation
Work with AI to implement tasks:
- Provide context: `{ project: your-project, taskFile: nnn-tasks.section }`
- Tackle subsections for complex work: `{ subsection: subsection-name }`
- AI implements code, runs tests, checks off completed items


#### 🔁 Phase 8: Integration & Iteration
Integrate completed work, verify everything works together, and plan next steps. For ongoing development, return to Phase 1 for new features.


## ⚡ Ongoing Development

### 🔄 Starting New Sessions
When starting a new conversation in an existing project (recommended to avoid context bloat), provide context parameters to help the AI re-orient: `{ project: your-project, taskFile: current-task-file }`.

### ✨ Feature Development
For major new features or architectural work, use the same living document pattern:

1. **Create feature document**: `project-documents/private/features/nnn-feature.{feature}.md`
2. **Add structure**:
   ```markdown
   # Overview
   [One-sentence feature description]

   ## User-Provided Concept
   [Your feature goals, requirements, design ideas]
   ```
3. **Let AI enhance**: AI adds technical design, specifications, integration points
4. **Generate tasks**: AI creates task sections that integrate with your existing tasks
5. **Implement**: Follow the same Phase 4-5 process

### 🎯 Ad-Hoc Work
For smaller items not requiring full feature specs:

1. Add a new section directly to your task file
2. Describe what needs to be done
3. Let AI expand and implement using the standard process

The same structured approach works whether you're building from scratch or adding to existing work.


### 📋 Working with the AI

#### Input Parameters
When working with AI Project Guide, provide input in a format like this, and your parameters should be used throughout the project.  When you update to work on a new section or subsection, just provide that input.  Just provide what is in use, you do not need every field.

```
{
  project: ,    # your project name
  section: ,    # (when working with a section)
  subsection: , # (for subsections)
  framework: ,  # (main framework in use for example NextJS)
  tools: ,      # (tools in use such as ShadCN, Tailwind, etc)
  apis: ,       # (any specific apis in use)
}
```

#### Core Files
- **`project-guides/guide.ai-project.000-process.md`** - This is *the* core file that instructs your AI on the overall process.
- **`project-guides/rules/`** - Use the `setup-ide` script to copy for your IDE, or copy manually if using other than Cursor and Windsurf.  

#### TroubleShooting
In Windsurf, the rules are sometimes not recognized until you manually access them in settings.  *todo: add tip for fixing this here, and verifying that rules are loaded correctly in Cursor*



## 📚 Guide System Overview

The AI project guide system operates on three layers, designed to work together seamlessly:

### **1. Public Guides** (This Repository)
- **Source**: `ai-project-guide.git`
- **Content**: Core methodology, tool guides, framework guides
- **Behavior**: Updated frequently, safe to overwrite
- **Usage**: Everyone gets these automatically

### **2. Organization Private Guides** (Advanced Feature)
- **Source**: Configurable via `PRIVATE_GUIDES_URL` environment variable
- **Content**: Company procedures, specialized knowledge, internal standards
- **Behavior**: Fail silently if not configured, overlay on public guides
- **Usage**: Advanced teams with private knowledge repositories

### **3. Project Private Guides** (Your Work)
- **Location**: `project-documents/private/`
- **Content**: Project-specific concept docs, specs, tasks, code reviews
- **Behavior**: Never overwritten, always preserved
- **Usage**: Your valuable project work that should be committed to git

### **Update Strategy**
- **Public guides**: Safe to update (overwrite)
- **Organization guides**: Overlay carefully (project wins in conflicts)
- **Project guides**: Never touched, always preserved

### **Collision Resolution**
- **Public vs Private**: Public wins (safe to update)
- **Organization vs Project Private**: Project wins (preserve user work)
- **Same file in both**: Project version preserved



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
mkdir -p project-documents/private/{architecture,slices,tasks,features,reviews,analysis}

# Add submodule
git submodule add https://github.com/ecorkran/ai-project-guide.git project-documents/ai-project-guide

# Create .gitkeep to track empty directories
echo '# Keep private/ in version control' > project-documents/private/.gitkeep

# Commit
git add .
git commit -m 'Add ai-project-guide'
```

### Migrating from Git Subtree (Legacy)
If you previously used git subtree, migrate to submodule:

```bash
# 1. Backup your work
cp -r project-documents/private ~/backup-private

# 2. Remove old subtree
git rm -r project-documents
git commit -m 'Remove subtree for migration to submodule'

# 3. Restore your work
git checkout HEAD~1 -- project-documents/private
# Or restore from backup if needed:
# cp -r ~/backup-private project-documents/private

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



## 🔄 Directory Structure Migration Guide

### From `our-project/` to Current Structure
If you're working with an existing project that uses the old `our-project/` structure, choose the appropriate migration path:

#### For Regular Development (Template Instances)
Migrate to `project-documents/private/`:

**Quick Migration Steps:**
1. **Rename the directory**: `mv project-documents/our-project project-documents/private`
2. **Create new subdirectories** (if they don't exist):
   ```bash
   mkdir -p project-documents/private/tasks
   ```
3. **Move project documents** to the `private/project-guides/` directory:
   ```bash
   # Create project-guides directory if it doesn't exist
   mkdir -p project-documents/private/project-guides
   
   # Move concept, spec, and notes files to private/project-guides/
   mv project-documents/private/concept/* project-documents/private/project-guides/ 2>/dev/null || true
   mv project-documents/private/spec/* project-documents/private/project-guides/ 2>/dev/null || true
   ```
4. **Update any references** in your project-specific files from `our-project/` to `private/`

#### For Monorepo Template Development
Migrate to `project-artifacts/`:

**Quick Migration Steps:**
1. **Rename the directory**: `mv {template}/examples/our-project project-artifacts`
2. **Create new subdirectories** (if they don't exist):
   ```bash
   mkdir -p project-artifacts/tasks
   mkdir -p project-artifacts/project-guides
   ```
3. **Update any references** in your project-specific files to use `project-artifacts/`

### New Structure After Migration

#### Regular Development (`private/`):
```
private/
├── code-reviews/        # review docs & follow-up actions
├── maintenance/         # maintenance tasks & outcomes 
├── features/            # feature definitions & specifications
├── project-guides/      # project-specific guide customizations
│   ├── 001-concept.{project}.md # project concept documents
│   ├── 002-spec.{project}.md    # project specifications
│   └── 03-notes.{project}.md   # project-specific notes
├── tasks/               # task breakdowns & phase documents
└── ui/                  # UI tasks & resources
    └── screenshots/     # mock-ups, design references
```

#### Monorepo Template Development (`project-artifacts/`):
```
project-artifacts/
├── code-reviews/        # review docs & follow-up actions
├── maintenance/         # maintenance tasks & outcomes
├── features/            # feature definitions & specifications
├── project-guides/      # project-specific guide customizations
├── tasks/               # task breakdowns & phase documents
└── ui/                  # UI tasks & resources
    └── screenshots/     # mock-ups, design references
```

> **Note**: The guides in this repository have been updated to clarify the distinction between `private/` (regular development) and `project-artifacts/` (monorepo template development). References to `{template}/examples/our-project/` are deprecated.



## 🤝 Contributing
First, if you are using the AI Project Guide and found it useful enough to contribute or even report and issue, thank you. I'll try to respond to review PRs, and respond to issues & comments.
