---
docType: tool-guide
layer: tool-guide
platform: threejs
audience: [human, ai]
purpose: deploying Vite + Three.js apps to GitHub Pages with custom domains
dateCreated: 20260121
dateUpdated: 20260405
status: in_progress
---

# Deploying to GitHub Pages

Overview: Deploying modern JS apps (Vite + Three.js) to GitHub Pages with custom domains.

## Hub Repository Setup

- Create a repository named `{your-username}.github.io` (the "hub" repository).
- Can be public or private (private requires GitHub Pro).
- Set your custom domain (e.g. `projects.mydomain.com`) in the hub repository's Pages settings.

## Project Repository Setup

- In your project repository (not the hub), enable GitHub Pages with the GitHub Actions workflow.
- **Do not** set a custom domain in the project repo; only set it in the hub.
- Use the official Pages Actions workflow to deploy.

## Why Vite (or a Bundler) is Needed

- Modern JS projects using `import` statements (e.g. `import * as THREE from 'three/webgpu'`) require a build step.
- Browsers cannot load npm packages directly; Vite bundles dependencies and rewrites asset paths.
- Vite's `base` config ensures correct asset URLs when deploying to a subpath (e.g. `/three-toy/`).

## Configure Vite

Install Vite and dependencies with pnpm:

```bash
pnpm add -D vite
pnpm add three
```

Add `vite.config.js`:

```js
import { defineConfig } from 'vite';

export default defineConfig({
  base: '/{repo-name}/', // e.g. '/three-toy/'
});
```

Add scripts to `package.json`:

```json
"scripts": {
  "dev": "vite",
  "build": "vite build",
  "preview": "vite preview"
}
```

## GitHub Actions Workflow (`.github/workflows/deploy.yml`)

Uses pnpm for installation. Node 22 LTS is recommended for new projects; Node 20 LTS is also supported.

```yaml
name: Deploy static site to Pages

on:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages

    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v4
        with:
          version: latest

      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: pnpm

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Build site
        run: pnpm build

      - uses: actions/upload-pages-artifact@v3
        with:
          path: dist

      - uses: actions/deploy-pages@v4
```

> **`pnpm/action-setup`** must appear before `actions/setup-node` so the `cache: pnpm` option resolves correctly.

## Local Preview

Use `pnpm preview` (or `npx serve dist`) to serve the built site locally and verify production behaviour before pushing:

```bash
pnpm build
pnpm preview
```

This emulates how GitHub Pages serves your static files from the `dist/` directory, including the `base` path rewriting.

---

## Summary

- Use a hub repo for the custom domain.
- Project repos use GitHub Actions to deploy to Pages, with Vite handling bundling and asset paths.
- Always build with Vite before deploying — never deploy raw source files.
- Use pnpm throughout (local dev and CI) for consistency.
- `pnpm preview` verifies production build behaviour locally.
