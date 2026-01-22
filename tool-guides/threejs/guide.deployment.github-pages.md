---
docType: guide
layer: tool-guide
tool: threejs
subject: deployment-github-pages
audience: [human, ai]
description: Deploying Vite + Three.js apps to GitHub Pages with custom domains
---

# Deploying to GitHub Pages

Overview: Deploying Modern JS Apps (e.g. Vite + Three.js) to GitHub Pages with Custom Domains.

## Hub Repository Setup
- Create a repository named `{your-username}.github.io` (this is the "hub" repository).
- Can be public or private (private requires GitHub Pro).
- Set your custom domain (e.g., `projects.mydomain.com`) in the hub repository’s Pages settings.

**Project Repository Setup**
- In your project repository (not the hub), enable GitHub Pages with the GitHub Actions workflow.
- **Do not** set a custom domain in the project repo; only set it in the hub.
- Use the official Pages Actions workflow to deploy.

**Why Vite (or a Bundler) is Needed**
- Modern JS projects (e.g., using Three.js with `import` statements) require a build step.
- Browsers can’t load npm packages directly; Vite bundles dependencies and rewrites asset paths.
- Vite’s `base` config ensures correct asset URLs when deploying to a subpath (e.g., `/three-toy/`).

How to Configure Vite**
- Install Vite and dependencies:

```
npm install --save-dev vite
npm install three
```

- Add `vite.config.js`:
```js
import { defineConfig } from 'vite';
export default defineConfig({
  base: '/{repo-name}/', // e.g., '/three-toy/'
});
```

- Add scripts to `package.json`:
```json
"scripts": {
	"dev": "vite",
	"build": "vite build",
	"preview": "vite preview"
}
```

**Relevant GitHub Actions Workflow (`.github/workflows/deploy.yml`):**
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
	  - name: Setup Node.js
	    uses: actions/setup-node@v4
	    with:
		  node-version: 20
	  - name: Install dependencies
  	    run: npm ci
	  - name: Build site
	    run: npm run build
	  - uses: actions/upload-pages-artifact@v3
	    with:
	      path: dist
	  - uses: actions/deploy-pages@v4
```

  
**Local Preview**
- Use `npx serve dist` to locally serve the built site and verify production behavior.
- This emulates how GitHub Pages will serve your static files from the `dist/` directory.

---

###### Summary
- Use a hub repo for the custom domain.
- Project repos use GitHub Actions to deploy to Pages, with Vite handling bundling and asset paths.
- Always build with Vite before deploying; never deploy raw source files.
- Use `npx serve dist` to preview the production build locally.