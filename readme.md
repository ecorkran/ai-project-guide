---
docType: repository-overview
---
# AI Project Guide

AI Project Guide is a structured methodology and set of guides for AI-assisted software development.  Gives your AI coding tools the context, process, and conventions they need to produce consistently good and verifiable results on complex projects.

**What it does:**
- Structures project knowledge so AI agents can consume it effectively
- Provides a phase-based workflow for breaking complex work into implementable pieces
- Includes guides for frameworks, tools, and coding conventions
- Ships with rules files for Claude Code, Cursor, and other AI coding tools

**Works with:** Claude Code, Cursor, GitHub Copilot, OpenAI Codex, and any AI coding tool that reads project files.

> **Installed into a project?** If you're reading this inside `project-documents/ai-project-guide/`, this directory is installed and managed by [Context Forge](https://github.com/ecorkran/context-forge) (`cf`). It is overwritten on `cf guides update`; any edits made here will be lost. Put project-specific customizations, including new subdirectories as needed, under `project-documents/user/` instead.
>
> If your project's CI checks out this repo as a git submodule, add `submodules: recursive` to your checkout step (e.g. `actions/checkout`) or the guide content will be missing in CI.

## How to Use

### Context Forge
ai-project-guide is used through [Context Forge](https://github.com/ecorkran/context-forge) (cf). cf installs and updates the guide, sets up your IDE rules, and assembles structured context prompts from your project configuration and these templates. See [Context Forge on npm](https://www.npmjs.com/package/@context-forge/mcp).


### Context Visualizer
[Context Visualizer](https://github.com/ecorkran/context-visualizer) functions as an MCP client and provides a visual representation of your projects' components and states.  



## Install

**Prerequisites:** A git repository (`git init` if needed — no remote required) and [Context Forge](https://www.npmjs.com/package/@context-forge/mcp).

```bash
cf init                  # registers the project, installs the guide, sets up IDE rules (default: claude)
cf init --ide cursor     # pick another IDE target: claude, cursor, copilot, agents
```

The guide lands at `project-documents/ai-project-guide/`. Your project-specific work goes in `project-documents/user/` — the guide never touches that directory. `cf init --help` lists the install strategies (tarball, submodule, clone).

**Update to the latest version:**

```bash
cf guides update
```

### IDE Rules Setup

`cf init` runs this for you. To change targets or refresh later:

```bash
cf setup-ide claude    # CLAUDE.md + .claude/{rules,agents,skills}/
cf setup-ide cursor    # .cursor/rules/ as .mdc, plus AGENTS.md
cf setup-ide copilot   # .github/ + AGENTS.md
cf setup-ide agents    # AGENTS.md only (aliases: openai, codex)
```

This assembles the rules from `project-guides/rules/` into the format your tool expects. Always-on rules are inlined; language- and tool-specific rules stay scoped by file pattern, so a React project isn't handed the Python rules. `--dry-run` previews the changes. You can customize the generated files afterward — they're yours.

See [readme.setup-ide.md](readme.setup-ide.md) for what each target writes and the frontmatter contract.

### Validating Slice Designs

Phase 4 slice designs are written from `project-guides/templates/slice-design.md`. The template doubles as the section schema, and a validator enforces it:

```bash
./project-documents/ai-project-guide/scripts/validate-slice-design project-documents/user/slices/101-slice.example.md
```

It prints `PASS`, or `FAIL` with the missing required headings, and exits non-zero on failure. Optional sections are never checked, so omitting what doesn't apply stays legal.

## How It Works

The methodology breaks development into phases. You don't need to follow all of them rigidly — use what fits your project.

**Planning phases (1–4):** You describe what you want to build. AI helps refine it into a concept document, specification, slice plan, and detailed slice designs.

**Execution phases (5–7):** AI breaks slice designs into task lists, refines them, and implements the code. This is where most of the time goes — you cycle through slices continuously as the project evolves.

### The Phases

**Phase 0 — Concept:** Write up what you're building in `project-documents/user/project-guides/000-concept.{project}.md`. AI enhances it with structured analysis.

**Phase 2 — Specification:** Create `002-spec.{project}.md`. AI fills in requirements, tech stack, architecture decisions.

**Phase 3 — Slice Planning:** Break the project into slices — independently implementable pieces of work (e.g., "user auth", "data pipeline", "reporting dashboard"). Each slice is a complete vertical of functionality.

**Phase 4 — Slice Design:** Detailed design for each slice in `user/slices/nnn-slice.{name}.md`. Dependencies, interfaces, technical decisions, success criteria.

**Phase 5 — Task Breakdown:** AI converts slice designs into task lists in `user/tasks/nnn-tasks.{name}.md`. Each task is specific enough for an AI agent to implement.

**Phase 6 — Task Enhancement:** AI refines tasks for clarity — adds file paths, test expectations, edge cases.  Rarelyneeded in 2026

**Phase 7 — Implementation:** AI implements the code, runs tests, checks off tasks.

For the full methodology details, see `project-guides/guide.ai-project.process.md`.


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

[Context Forge](https://github.com/ecorkran/context-forge) is an MCP server and CLI that generates structured context prompts from your project configuration and ai-project-guide's templates. It eliminates the manual work of assembling context at the start of each AI coding session.

```bash
# Add the MCP server to Claude Code
claude mcp add --transport stdio context-forge -- npx @context-forge/mcp
```

With the guide installed in your project, the generated prompts reference the methodology guides, and your AI agent can browse the phase documentation, rules files, and framework guides directly.


## Contributing

Issues and pull requests are welcome at [github.com/ecorkran/ai-project-guide](https://github.com/ecorkran/ai-project-guide). This is actively developed — expect frequent changes.

If you're using ai-project-guide and found it useful enough to contribute or report an issue, thank you.

### Working inside this repository

Paths written *inside* the guides assume the installed layout — the guide living at `project-documents/ai-project-guide/` of a consuming project, which is how nearly all usage happens. When working in this repository directly those paths are shifted up:

| Written in the guides | Here in this repo |
|---|---|
| `project-documents/ai-project-guide/project-guides/` | `project-guides/` |
| `project-documents/ai-project-guide/project-guides/rules/` | `project-guides/rules/` |
| `project-documents/ai-project-guide/tool-guides/` | `tool-guides/` |

Strip the `project-documents/ai-project-guide/` prefix and the path resolves. Rules are edited at `project-guides/rules/`; `setup-ide` compiles them into the generated artifacts (`CLAUDE.md`, `AGENTS.md`, `.claude/rules/`, etc.), so edit the source, never the generated copy.


## License

MIT
