---
docType: repository-overview
---
# AI Project Guide

A structured methodology for AI-assisted software development. Gives your AI coding tools the context, process, and conventions they need to produce consistently good results on complex projects.

**What it does:**

- Structures project knowledge so AI agents can consume it effectively
- Provides a phase-based workflow for breaking complex work into implementable pieces
- Includes guides for frameworks, tools, and coding conventions
- Ships with rules files for Claude Code, Cursor, and other AI coding tools

**Works with:** Claude Code, Cursor, Windsurf, and any AI coding tool that reads project files.

**Best with [Context Forge](https://github.com/ecorkran/context-forge):** An MCP server that automatically assembles structured context prompts from your project configuration and these templates. Install it alongside ai-project-guide for the full workflow — see [Context Forge on npm](https://www.npmjs.com/package/@context-forge/mcp).


## Install

**Prerequisites:** A git repository (`git init` if needed — no remote required).

```bash
curl -fsSL https://raw.githubusercontent.com/ecorkran/ai-project-guide/main/scripts/bootstrap.sh | bash
```

This creates the project directory structure and adds ai-project-guide as a git submodule at `project-documents/ai-project-guide/`. Your project-specific work goes in `project-documents/user/` — the guide never touches that directory.

**Update to latest version:**

```bash
git submodule update --remote project-documents/ai-project-guide
git add project-documents/ai-project-guide
git commit -m "Update ai-project-guide"
```

### IDE Rules Setup

After installing, generate rules files for your AI coding tool:

```bash
# From project root
./project-documents/ai-project-guide/scripts/setup-ide claude     # generates CLAUDE.md
./project-documents/ai-project-guide/scripts/setup-ide cursor     # generates .cursor/ rules
./project-documents/ai-project-guide/scripts/setup-ide windsurf   # generates .windsurf/ rules
```

This assembles the rules from `project-guides/rules/` into the format your IDE expects. You can customize the generated files afterward — they're yours.

### For npm/pnpm Projects

You can add convenience scripts to `package.json`:

```json
"scripts": {
  "setup-guides": "mkdir -p project-documents/user/{analysis,architecture,features,project-guides,reviews,slices,tasks} && git submodule add https://github.com/ecorkran/ai-project-guide.git project-documents/ai-project-guide && echo '# Keep user/ in version control' > project-documents/user/.gitkeep || echo 'Submodule already exists'",
  "setup-claude": "project-documents/ai-project-guide/scripts/setup-ide claude"
}
```


## How It Works

The methodology breaks development into phases. You don't need to follow all of them rigidly — use what fits your project.

**Planning phases (1–4):** You describe what you want to build. AI helps refine it into a concept document, specification, slice plan, and detailed slice designs.

**Execution phases (5–7):** AI breaks slice designs into task lists, refines them, and implements the code. This is where most of the time goes — you cycle through slices continuously as the project evolves.

### The Phases

**Phase 1 — Concept:** Write up what you're building in `project-documents/user/project-guides/001-concept.{project}.md`. AI enhances it with structured analysis.

**Phase 2 — Specification:** Create `002-spec.{project}.md`. AI fills in requirements, tech stack, architecture decisions.

**Phase 3 — Slice Planning:** Break the project into slices — independently implementable pieces of work (e.g., "user auth", "data pipeline", "reporting dashboard"). Each slice is a complete vertical of functionality.

**Phase 4 — Slice Design:** Detailed design for each slice in `user/slices/nnn-slice.{name}.md`. Dependencies, interfaces, technical decisions, success criteria.

**Phase 5 — Task Breakdown:** AI converts slice designs into task lists in `user/tasks/nnn-tasks.{name}.md`. Each task is specific enough for an AI agent to implement.

**Phase 6 — Task Enhancement:** AI refines tasks for clarity — adds file paths, test expectations, edge cases.

**Phase 7 — Implementation:** AI implements the code, runs tests, checks off tasks.

**Architecture documents** live in `user/architecture/` and are created when needed. High-level design typically starts at `050-arch.hld-{project}.md`.

For the full methodology details, see `project-guides/guide.ai-project.000-process.md`.


## Project Structure

After installation, your project has:

```
project-documents/
  ai-project-guide/           ← this repo (submodule, don't edit directly)
    project-guides/             methodology docs, prompt templates, rules
    framework-guides/           Next.js, Astro, etc.
    tool-guides/                Tailwind, Three.js, Radix, etc.
    domain-guides/              cross-cutting subject knowledge
  user/                        ← your work (committed to your repo)
    architecture/               HLD, component architecture docs
    slices/                     slice designs
    tasks/                      task breakdowns
    features/                   feature specs
    reviews/                    code review outputs
    analysis/                   codebase analysis docs
```

### Guide Directories

| Directory | Contains |
|---|---|
| `project-guides/` | Core methodology — process docs, prompt templates, rules files. Applies to every project. |
| `framework-guides/` | Runtime/platform guides (Next.js, Astro, Electron). |
| `tool-guides/` | Library and toolkit guides (Tailwind, Three.js, Radix, SciChart). |
| `domain-guides/` | Subject-matter knowledge (game development, hydrology, financial visualization). |

Full details in [`directory-structure.md`](directory-structure.md). File naming conventions in [`file-naming-conventions.md`](file-naming-conventions.md).


## Using with Context Forge

[Context Forge](https://github.com/ecorkran/context-forge) is an MCP server that generates structured context prompts from your project configuration and ai-project-guide's templates. It eliminates the manual work of assembling context at the start of each AI coding session.

```bash
# Install the MCP server (works immediately with bundled templates)
npx @context-forge/mcp

# Add to Claude Code
claude mcp add --transport stdio context-forge -- npx @context-forge/mcp
```

Context Forge works out of the box with bundled prompt templates. Having ai-project-guide installed in your project unlocks the full experience — the generated prompts reference the methodology guides, and your AI agent can browse the phase documentation, rules files, and framework guides directly.


## Manual Setup

If you prefer not to use the bootstrap script:

```bash
# Create directory structure
mkdir -p project-documents/user/{analysis,architecture,features,project-guides,reviews,slices,tasks}

# Add submodule
git submodule add https://github.com/ecorkran/ai-project-guide.git project-documents/ai-project-guide

# Track the user directory
echo '# Keep user/ in version control' > project-documents/user/.gitkeep

git add .
git commit -m 'Add ai-project-guide'
```


## Contributing

Issues and pull requests are welcome at [github.com/ecorkran/ai-project-guide](https://github.com/ecorkran/ai-project-guide). This is actively developed — expect frequent changes.

If you're using ai-project-guide and found it useful enough to contribute or report an issue, thank you.


## License

MIT
