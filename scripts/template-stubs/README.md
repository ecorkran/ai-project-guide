# Template Stub Scripts

These are minimal stub scripts to be included in project templates.

## Purpose

Templates need a way to bootstrap the ai-project-guide without having the full scripts pre-installed. These stubs download and execute the canonical scripts from this repository.

## Usage in Templates

Copy these files to your template's `scripts/` directory:

```bash
your-template/
└── scripts/
    ├── setup-guides.sh    # Copy from here
    └── update-guides.sh   # Copy from here
```

Then add npm scripts to your template's `package.json`:

```json
{
  "scripts": {
    "setup-guides": "bash scripts/setup-guides.sh",
    "update-guides": "bash scripts/update-guides.sh"
  }
}
```

## What Each Script Does

### `setup-guides.sh`
- Downloads `bootstrap.sh` from ai-project-guide main branch
- Executes it to create directory structure and add submodule
- One-time setup for new projects

### `update-guides.sh`
- Updates the ai-project-guide submodule to latest version
- Fixes detached HEAD state (ensures on main branch)
- Updates external guides if `EXTERNAL_PROJECT_DOC_URL` is set
- Auto-commits changes with version tag
- Run periodically to get guide updates

## Benefits

- **Single Source of Truth**: Full scripts live in ai-project-guide
- **Easy Updates**: Update ai-project-guide, all templates benefit
- **Minimal Overhead**: Only 2 tiny files per template
- **Works Offline After Setup**: Only initial setup requires internet

## For Non-NPM Projects

Projects without npm/package.json can use the bootstrap scripts directly:

```bash
# Bash/Shell projects:
curl -fsSL https://raw.githubusercontent.com/ecorkran/ai-project-guide/main/scripts/bootstrap.sh | bash

# Python projects:
curl -fsSL https://raw.githubusercontent.com/ecorkran/ai-project-guide/main/scripts/bootstrap.py | python3
```

## Monorepo Usage

These same stubs work in monorepo templates. No special handling needed - the submodule path structure is identical whether in a monorepo or standalone project.
