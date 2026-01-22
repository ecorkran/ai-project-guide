---
docType: guide
scope: project-wide
audience: [human]
description: IDE setup instructions for Cursor, Windsurf, and Claude Code
---

# IDE Setup Guide

This guide explains how to set up AI project rules in your IDE (Cursor or Windsurf) for enhanced AI assistance.

**Path Convention:** In this guide, `ai-project-guide/` refers to `{project-root}/project-documents/ai-project-guide/`.

## Quick Setup (Recommended)

Use the automated setup script from your project root:

```bash
# For Cursor IDE
./project-documents/ai-project-guide/scripts/setup-ide cursor

# For Windsurf IDE
./project-documents/ai-project-guide/scripts/setup-ide windsurf
```

The script will:
- Copy all rule files to the appropriate IDE directory
- Rename `.md` files to `.mdc` for Cursor compatibility
- Validate frontmatter requirements
- Provide setup confirmation and next steps

## Manual Setup (Alternative)

If you prefer manual setup or need to troubleshoot the automated process:

### For Cursor IDE

1. **Create the rules directory:**
   ```bash
   mkdir -p .cursor/rules
   ```

2. **Copy rule files:**
   ```bash
   cp project-documents/ai-project-guide/project-guides/rules/*.md .cursor/rules/
   cp project-documents/ai-project-guide/project-guides/agents/*.md .cursor/rules/
   ```

3. **Rename files to .mdc extension:**
   ```bash
   cd .cursor/rules
   for file in *.md; do
       mv "$file" "${file%.md}.mdc"
   done
   ```

4. **Verify frontmatter** (required for Cursor):
   Each `.mdc` file must start with YAML frontmatter:
   ```yaml
   ---
   description: Brief description of what this rule does
   globs: ["**/*.ext", "pattern/**/*"]
   alwaysApply: false
   ---
   ```

5. **Restart Cursor** to load the new rules.

### For Windsurf IDE

1. **Create the rules directory:**
   ```bash
   mkdir -p .windsurf/rules
   ```

2. **Copy rule files** (keep .md extension):
   ```bash
   cp project-documents/ai-project-guide/project-guides/rules/*.md .windsurf/rules/
   cp project-documents/ai-project-guide/project-guides/agents/*.md .windsurf/rules/
   ```

3. **Verify frontmatter** (recommended):
   Each `.md` file should have YAML frontmatter for best compatibility:
   ```yaml
   ---
   description: Brief description of what this rule does
   globs: ["**/*.ext", "pattern/**/*"]
   alwaysApply: false
   ---
   ```

4. **Restart Windsurf** to load the new rules.

## Available Rules

### Core Rules (`ai-project-guide/project-guides/rules/`)
- **general.md** - General coding rules and project structure guidelines
- **react.md** - React and Next.js component rules and best practices
- **typescript.md** - TypeScript syntax rules and typing standards
- **python.md** - Python development rules and best practices
- **sql.md** - SQL and PostgreSQL development rules (including pgvector, TimescaleDB)
- **testing.md** - Testing guidelines and development tools
- **review.md** - Comprehensive code review guidelines

### Agent Configurations (`project-guides/agents/`)
- **code-review-agent.md** - Automated code review agent configuration

## Frontmatter Requirements

All rule files include YAML frontmatter with three key fields:

- **description**: Brief explanation of when/how to use this rule
- **globs**: Array of file patterns that trigger this rule
- **alwaysApply**: Boolean (usually `false` for selective application)

### Example Frontmatter:
```yaml
---
description: React and Next.js component rules, naming conventions, and best practices
globs: ["**/*.tsx", "**/*.jsx", "**/*.ts", "**/*.js", "src/components/**/*", "app/**/*"]
alwaysApply: false
---
```

## IDE-Specific Notes

### Cursor IDE
- Requires `.mdc` file extension for project rules
- Frontmatter is mandatory for proper rule loading
- Rules appear in the Agent sidebar when active
- Access via Settings → Rules to manage rule types

### Windsurf IDE
- Uses `.md` file extension
- Frontmatter recommended but not strictly required
- Rules integrate with Windsurf's AI assistance features

## Troubleshooting

### Rules Not Loading
1. **Check file location**: Ensure files are in `.cursor/rules/` or `.windsurf/rules/`
2. **Verify extensions**: `.mdc` for Cursor, `.md` for Windsurf
3. **Validate frontmatter**: Ensure proper YAML syntax
4. **Restart IDE**: Rules are loaded at startup

### Frontmatter Validation Errors
```yaml
# ❌ Invalid (missing quotes around globs)
globs: [**/*.ts]

# ✅ Valid (properly quoted)
globs: ["**/*.ts"]
```

### Script Permission Issues
```bash
# Make script executable
chmod +x project-documents/ai-project-guide/scripts/setup-ide
```

## Advanced Configuration

### Custom Rule Types (Cursor)
Rules can be configured as:
- **Always**: Always included in context
- **Auto Attached**: Triggered by file patterns
- **Agent Requested**: AI decides when to include
- **Manual**: Only when explicitly referenced

### Rule Scoping
Use glob patterns to target specific files:
```yaml
# Target React components
globs: ["src/components/**/*.tsx"]

# Target test files
globs: ["**/*.test.*", "**/*.spec.*"]

# Target everything
globs: ["**/*"]
```

## Integration with AI Project Methodology

These rules are designed to work with the 6-phase AI project methodology:

1. **Concept** - General and review rules provide structure
2. **Specification** - TypeScript and React rules ensure consistency  
3. **Task Breakdown** - All rules help AI understand project patterns
4. **Task Expansion** - Specific rules guide detailed implementation
5. **Execution** - Rules provide real-time guidance during coding
6. **Iteration** - Review rules support continuous improvement

For more information, see the main project guides in `project-guides/`. 