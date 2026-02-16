---
docType: intro-guide
platform: astro
audience:
  - human
  - ai
features:
  - React integration with ShadCN UI
  - Option for zero-JS static setup
purpose: Quickstart guide for Astro projects with and without React
dateUpdated: 20250718
---


## Summary

Introduction and setup guide for Astro.  Includes React and ShadCN UI options.  Covers prerequisites, installation, directory structure, and interactive islands, usable by human and AI developers.  More info: ([Install Astro - Docs](https://docs.astro.build/en/install-and-setup/?utm_source=chatgpt.com), [Getting started - Docs](https://docs.astro.build/en/getting-started/?utm_source=chatgpt.com)).

## Prerequisites

Before you begin, ensure you have:
- **Node.js ≥ 18.17.1** and **npm**, **pnpm**, or **Yarn** installed on your machine ([Install Astro - Docs](https://docs.astro.build/en/install-and-setup/?utm_source=chatgpt.com)).
- Confirm use of React, ShadCN, Radix, and Auth or database with Project Manager *before* starting.

## 0. Installation Methods
Select an install method below.  It is suggested to use a template and install from CLI.  If you are an AI and not installing with a template, confirm with Project Manager before choosing this method.

## 1. Creating Your First Astro Project

### 1.1 — Automatic CLI Wizard

Specify template when using the CLI.  Following are a list of templates.  The Project Spec should specify the template for you.  A list of suggested templates is provided here.  

*CLI create Astro project from template*
In an empty folder, run:
```sh
# where {template} is an entry such as dansholds/astro-shadcn-starter.
npm create astro@latest my-site \
  -- --template {template}
```

*Note: you will need to specify additional options to be able to have an AI automate this creation and not get stuck at the user prompts in the CLI.*
#### 1.1.2.1 List of Suggested Astro Templates
The following list of templates is useful in case none is provided in the spec.  Start with `dansholds` or `area44`.

* https://github.com/dansholds/astro-shadcn-starter
* https://github.com/AREA44/astro-shadcn-ui-template
* https://astro.build/themes/details/astro-shadcn-ui-template/
* https://github.com/mwarf/2025-astro-starter

### 1.2 — Manual Installation
*Note: generally not needed.  Prefer CLI installation with template, see [[#1.1 — Automatic CLI Wizard]].*

1. Create `package.json` if you don’t have one:
    ```bash
    npm init --yes
    ```

2. Install Astro locally (global installs are discouraged):
    ```bash
    npm install astro
    ```

3. Update `package.json` scripts:
    ```jsonc
    {
      "scripts": {
        "dev":    "astro dev",
        "build":  "astro build",
        "preview":"astro preview"
      }
    }
    ```

4. Create your first page at `src/pages/index.astro` using YAML front matter:
    ```astro
    ---
    title: "Home"
    ---
    <h1>Welcome to Astro!</h1>
    ```

    Astro recognizes the `---` front matter by default ([Install Astro manually - Astro Documentation](https://tanggd.github.io/en/install/manual/?utm_source=chatgpt.com)).


## 2. React + ShadCN UI Integration

### 2.1 — Enable React Islands

To hydrate interactive components only where needed (Astro’s “islands architecture”):

1. Install the React integration:
    ```bash
    npm install @astrojs/react react react-dom
    ```

2. In `astro.config.mjs`, add:
    ```js
    import { defineConfig } from 'astro/config';
    import react from '@astrojs/react';
    
    export default defineConfig({
      integrations: [ react() ],
    });
    ```
    
    Astro supports React out of the box among other UI frameworks ([Getting started - Docs](https://docs.astro.build/en/getting-started/?utm_source=chatgpt.com)).

### 2.2 — Install Tailwind CSS
1. Install Tailwind and its peer deps:
    ```bash
    npm install -D tailwindcss postcss autoprefixer
    npx tailwindcss init -p
    ```
    
2. Configure `tailwind.config.cjs`:
    ```js
    module.exports = {
      content: ["./src/**/*.{astro,html,js,jsx,ts,tsx}"],
      theme: { extend: {} },
      plugins: [],
    };
    ```

### 2.3 — Scaffold ShadCN UI

1. From your project root, run:
    ```bash
    npx shadcn-ui@latest init
    ```
    
    This creates `src/components/ui`, updates your Tailwind config, and installs required deps ([Installation - shadcn/ui](https://ui.shadcn.com/docs/installation?utm_source=chatgpt.com), [How to install shadcn component library using yarn or npm?](https://stackoverflow.com/questions/77934605/how-to-install-shadcn-component-library-using-yarn-or-npm?utm_source=chatgpt.com)).
    
2. Generate any components you need, e.g.:
    
    ```bash
    npx shadcn-ui@latest add button
    ```
    
3. Import and hydrate in an Astro page or MDX:
	```astro
    ---
    import { Button } from '../components/ui/button';
    ---
    <Button client:load>Click me</Button>
    ```

## 3. Option: Static Tailwind-Only Setup

If you want zero JavaScript islands:
1. Skip the React integration step.
2. Follow the Tailwind CSS setup (as above).
3. Author all layouts and components purely in `.astro` files using HTML + Tailwind classes.
4. No `client:` directives means no client-side JS is shipped by default.

## 4. Directory Structure & Conventions

```
my-astro-project/
├── public/               # static assets (img, fonts)
├── src/
│   ├── components/       # shared UI (Astro or React)
│   ├── components/ui/    # ShadCN UI components
│   ├── layouts/          # Astro layout templates
│   ├── pages/            # .astro pages (routing)
│   ├── styles/           # global CSS (Tailwind imports)
│   └── data/             # markdown, JSON, content collections
├── astro.config.mjs      # Astro config & integrations
├── tailwind.config.cjs   # Tailwind content paths & theme
└── package.json          # scripts & dependencies
```

## 5. Hydration Modes & Usage

Astro offers fine-grained control over when your React/ShadCN components load:

- `client:load` — hydrates as soon as JS loads
- `client:idle` — hydrates when the browser is idle
- `client:visible` — hydrates when the component enters the viewport

Use these directives on your component tags to tune performance and bundle size.

---

With this markdown as your **intro guide**, both human developers and AI agents can quickly spin up an Astro project—choosing between a full React+ShadCN UI stack or a lean, zero-JS static site—while adhering to best practices around front matter, Tailwind theming, and islands-style hydration.