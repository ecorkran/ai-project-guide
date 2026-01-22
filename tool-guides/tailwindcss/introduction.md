---
docType: intro-guide
layer: tool-guide
tool: tailwindcss
audience: [human, ai]
description: Tailwind CSS v4 installation and setup guide
---

# Tailwind CSS v4 Install & Setup Guide

Tailwind CSS v4 introduces a simplified, zero-config installation process. Below are concise, framework-specific setup instructions for the most common modern JavaScript frameworks.

---

## **General Installation Principles**

- **No need for `tailwind.config.js` or `init` commands by default.**
- **Use the new `@import "tailwindcss";` directive in your CSS** (replaces all `@tailwind base;`, `@tailwind components;`, and `@tailwind utilities;`).
- **Framework-specific plugins:**  
  - For Vite-based projects, use the official `@tailwindcss/vite` plugin for optimal performance.
  - For Next.js, use the `@tailwindcss/postcss` plugin in your PostCSS config[1][2][5][6][7][9].

---

## **Next.js**

Next.js uses PostCSS for Tailwind integration.

1. **Install Dependencies**
   ```bash
   npm install -D tailwindcss@latest @tailwindcss/postcss postcss
   ```
2. **Configure PostCSS**
   - Create `postcss.config.mjs` in your project root:
     ```js
     export default {
       plugins: {
         '@tailwindcss/postcss': {},
       },
     };
     ```
3. **Import Tailwind in Global CSS**
   - In your global stylesheet (e.g., `app/globals.css`):
     ```css
     @import "tailwindcss";
     ```
   - Import this stylesheet in your root layout (e.g., `app/layout.tsx`):
     ```js
     import './globals.css';
     ```
4. **Use Tailwind Classes**
   - Tailwind utility classes are now available throughout your app[5][7].

---

## **Vite (Vanilla, React, Vue, etc.)**

1. **Install Dependencies**
   ```bash
   npm install tailwindcss @tailwindcss/vite
   ```
2. **Configure Vite**
   - Edit `vite.config.js` or `vite.config.ts`:
     ```js
     import { defineConfig } from 'vite';
     import tailwindcss from '@tailwindcss/vite';

     export default defineConfig({
       plugins: [tailwindcss()],
     });
     ```
3. **Import Tailwind in CSS**
   - In your main CSS file (e.g., `src/style.css`):
     ```css
     @import "tailwindcss";
     ```
   - Ensure this CSS file is included in your project entry point[9].

---

## **Astro**

1. **Install Dependencies**
   ```bash
   npm install tailwindcss @tailwindcss/vite
   ```
2. **Configure Astro with Vite Plugin**
   - In `astro.config.mjs`:
     ```js
     import { defineConfig } from "astro/config";
     import tailwindcss from "@tailwindcss/vite";

     export default defineConfig({
       vite: {
         plugins: [tailwindcss()],
       },
     });
     ```
3. **Import Tailwind in CSS**
   - Create `src/tailwind.css`:
     ```css
     @import "tailwindcss";
     ```
   - Import this CSS in your layout, e.g., in `src/layouts/BaseLayout.astro`:
     ```js
     import "../tailwind.css";
     ```
   - Reference this layout in your pages[3].

---

## **SvelteKit**

1. **Install Dependencies**
   ```bash
   npm install tailwindcss @tailwindcss/vite
   ```
2. **Configure Vite**
   - In `vite.config.js` or `vite.config.ts`:
     ```js
     import { sveltekit } from '@sveltejs/kit/vite';
     import { defineConfig } from 'vite';
     import tailwindcss from '@tailwindcss/vite';

     export default defineConfig({
       plugins: [tailwindcss(), sveltekit()],
     });
     ```
3. **Import Tailwind in CSS**
   - Create `src/app.css`:
     ```css
     @import "tailwindcss";
     ```
   - Import `app.css` in your root layout (`src/routes/+layout.svelte`):
     ```svelte
     <script>
       import "../app.css";
     </script>
     <slot />
     ```
   - Tailwind classes are now available in your Svelte components[4].

---

## **Summary Table**

| Framework  | Install Command                                         | Config File(s)             | Import CSS Directive      | Plugin/Loader Config                 |
|------------|---------------------------------------------------------|----------------------------|--------------------------|--------------------------------------|
| Next.js    | `npm install -D tailwindcss @tailwindcss/postcss postcss` | `postcss.config.mjs`       | `@import "tailwindcss";` | `@tailwindcss/postcss` in PostCSS    |
| Vite       | `npm install tailwindcss @tailwindcss/vite`             | `vite.config.js/ts`        | `@import "tailwindcss";` | `@tailwindcss/vite` plugin           |
| Astro      | `npm install tailwindcss @tailwindcss/vite`             | `astro.config.mjs`         | `@import "tailwindcss";` | `@tailwindcss/vite` in Vite config   |
| SvelteKit  | `npm install tailwindcss @tailwindcss/vite`             | `vite.config.js/ts`        | `@import "tailwindcss";` | `@tailwindcss/vite` in Vite config   |

---

You can now use Tailwind utility classes directly in your components.  
No `init` or manual config files are required for most use cases.  
For advanced configuration, refer to Tailwind's official documentation[1][2][6][7].

---

## Tailwind CSS Config

- The file `tailwind.config.js` is **no longer strictly required** but is still fully supported for advanced configuration (custom themes, plugins, etc.)[2][3][6][7].
- For most projects, the new "CSS-first" approach (just `@import "tailwindcss";` in your CSS) is recommended.
- If you use a custom config, **explicitly reference it in your CSS with the `@config` directive** at the very top of your main CSS file:
  ```css
  @config "./tailwind.config.js";
  @import "tailwindcss";
  ```
- No need to run `tailwindcss init` unless you want to customize Tailwind's default config.

---

## v4 Utility Class Changes & Migration

- **Old utility classes have been removed or renamed.**  
  Update your codebase as follows[1][2][8]:
  | v3 Utility           | v4 Replacement         |
  |----------------------|-----------------------|
  | `bg-opacity-*`       | `bg-black/50` (etc.)  |
  | `text-opacity-*`     | `text-black/50` (etc.)|
  | `flex-shrink-*`      | `shrink-*`            |
  | `flex-grow-*`        | `grow-*`              |
  | `overflow-ellipsis`  | `text-ellipsis`       |
  | `shadow-sm`          | `shadow-xs`           |
  | `shadow`             | `shadow-sm`           |

- **Dynamic utility values:**  
  You can now use arbitrary values for spacing, width, columns, etc. (e.g., `mt-17`, `w-29`, `grid-cols-15`)[8].

- **Custom utilities:**  
  Use the new `@utility` API in your CSS for custom classes, replacing the old `@layer utilities`[2][6].

- **Upgrade tool:**  
  For existing projects, run:
  ```bash
  npx @tailwindcss/upgrade@next
  ```
  This automates most migration steps (requires Node.js 20+)[2][6][9].

---

## Browser Support

Tailwind CSS v4 requires **modern browsers** (Safari 16.4+, Chrome 111+, Firefox 128+).  
If you need to support older browsers, stick with v3.4[6].

---

## Further Reading

- [Tailwind CSS v4 Release Blog][1]
- [Official Migration Guide][6]
- [Next.js Tailwind Guide][5][7]
- [Vite Tailwind Guide][9]
- [Astro Tailwind Guide][3]
- [SvelteKit Tailwind Guide][4]

---

**You are now ready to use Tailwind CSS v4 in your modern JavaScript projects, with zero config for most setups and easy customization when needed.**

---

**End of v4-Ready Guide**

Sources
[1] Tailwind CSS 4.0: Everything you need to know in one place https://daily.dev/blog/tailwind-css-40-everything-you-need-to-know-in-one-place
[2] What's New and Migration Guide: Tailwind CSS v4.0 https://dev.to/kasenda/whats-new-and-migration-guide-tailwind-css-v40-3kag
[3] Tailwind v4 | HeroUI (Previously NextUI) https://www.heroui.com/docs/guide/tailwind-v4
[4] Getting started with Tailwind v4 - DEV Community https://dev.to/plainsailing/getting-started-with-tailwind-v4-3cip
[5] Guides: Tailwind CSS | Next.js https://nextjs.org/docs/app/guides/tailwind-css
[6] Upgrade guide - Getting started - Tailwind CSS https://tailwindcss.com/docs/upgrade-guide
[7] Styling: Tailwind CSS - Next.js https://nextjs.org/docs/app/building-your-application/styling/tailwind-css
[8] Tailwind CSS v4: what developers need to know - Eagerworks https://eagerworks.com/blog/tailwind-css-v4
[9] How to set up Tailwind CSS v4.0 in your Vite App - DEV Community https://dev.to/drprime01/how-to-set-up-tailwind-css-v40-in-your-vite-app-323
[10] TailwindCSS v4.0: Upgrading from v3 with some plugins https://dev.to/sirneij/tailwindcss-v40-upgrading-from-v3-with-some-plugins-572f
[11] UPGRADE Tailwind CSS v3 to v4 - YouTube https://www.youtube.com/watch?v=dIu_HnGPleg
[12] installing tailwind is ludicrously difficult and not worth it - Reddit https://www.reddit.com/r/tailwindcss/comments/1jhieow/installing_tailwind_is_ludicrously_difficult_and/
[13] Tailwind CSS v4.0 https://tailwindcss.com/blog/tailwindcss-v4
[14] Tailwind V4 migration : r/nextjs - Reddit https://www.reddit.com/r/nextjs/comments/1ilo0o7/tailwind_v4_migration/
[15] [v4] Upgraded to V4 with vite plugin, tailwindcss forms breaks ... https://github.com/tailwindlabs/tailwindcss/discussions/15816
[16] Upgrade guide - Getting started - Tailwind CSS https://tailwindcss.com/docs/upgrade-guide
[17] Upgrading to Tailwind v4.0 | timomeh.de - Timo Mämecke https://timomeh.de/posts/upgrading-to-tailwind-v4
[18] How can I setup tailwind.config.js with Angular & TailwindCSS v4 ... https://stackoverflow.com/questions/79450336/how-can-i-setup-tailwind-config-js-with-angular-tailwindcss-v4-application
[19] Upgrading to V4 broke my projects, is sticking with V3 the only way? https://www.reddit.com/r/tailwindcss/comments/1idw75y/upgrading_to_v4_broke_my_projects_is_sticking/
[20] How to setup TailwindCSS V4 with Gatsby? #15891 - GitHub https://github.com/tailwindlabs/tailwindcss/discussions/15891
[21] Migrating from Tailwind CSS V3 to V4 - YouTube https://www.youtube.com/watch?v=WaYgFtYiYdw
[22] Next.js + Tailwind CSS v4 Ultimate Guide - YouTube https://www.youtube.com/watch?v=1jCLlNU2fAk
[23] Install Tailwind CSS with Next.js https://tailwindcss.com/docs/guides/nextjs
[24] Migration to v4 css based config · tailwindlabs tailwindcss - GitHub https://github.com/tailwindlabs/tailwindcss/discussions/13813
[25] Framework guides - Installation - Tailwind CSS https://tailwindcss.com/docs/installation/framework-guides
[26] Tailwind CSS v4: Implement in Next.js & Upgrade from v3 - YouTube https://www.youtube.com/watch?v=obAB6nSVj1E
[27] Tailwind v4 - Shadcn UI https://ui.shadcn.com/docs/tailwind-v4
[28] A First Look at Setting Up Tailwind CSS v4.0 https://bryananthonio.com/blog/configuring-tailwind-css-v4/
[29] next.js - Regarding no tailwind config in nextjs project - Stack Overflow https://stackoverflow.com/questions/79513980/regarding-no-tailwind-config-in-nextjs-project
[30] Migrating to 4.0 · tailwindlabs tailwindcss · Discussion #15729 - GitHub https://github.com/tailwindlabs/tailwindcss/discussions/15729
[31] Tailwind v4 CRA Installation : r/tailwindcss - Reddit https://www.reddit.com/r/tailwindcss/comments/1j8qcf3/tailwind_v4_cra_installation/
[32] Open-sourcing our progress on Tailwind CSS v4.0 https://tailwindcss.com/blog/tailwindcss-v4-alpha
[33] Styling with utility classes - Core concepts - Tailwind CSS https://tailwindcss.com/docs/styling-with-utility-classes
[34] The last step in updating to Tailwind CSS 4 | maciek palmowski https://maciekpalmowski.dev/blog/the-last-step-in-updating-to-tailwind-css-4/
[35] [v4] How to add plugins? #13292 - tailwindlabs tailwindcss - GitHub https://github.com/tailwindlabs/tailwindcss/discussions/13292
[36] Tailwind CSS not generating standard utility classes however ... https://stackoverflow.com/questions/79509973/tailwind-css-not-generating-standard-utility-classes-however-arbitrary-classes-w
[37] How to setting Tailwind CSS v4 global class? - Stack Overflow https://stackoverflow.com/questions/79383758/how-to-setting-tailwind-css-v4-global-class
[38] How to set up custom utility classes with v4 and vite? : r/tailwindcss https://www.reddit.com/r/tailwindcss/comments/1irhtb1/how_to_set_up_custom_utility_classes_with_v4_and/
[39] What don't you like about Tailwind v4? : r/reactjs - Reddit https://www.reddit.com/r/reactjs/comments/1ic6pfy/what_dont_you_like_about_tailwind_v4/
[40] Tailwind CSS v4 Full Course 2025 | Master Tailwind in One Hour https://www.youtube.com/watch?v=6biMWgD6_JY
[41] How to Set up Tailwind CSS V4 Project for Beginners from Scratch ... https://www.youtube.com/watch?v=Kh3xj-5nMqw
[42] Installing Tailwind CSS with Vite https://tailwindcss.com/docs
[43] A Complete Guide to Installing Tailwind CSS 4 in Backend ... - Reddit https://www.reddit.com/r/tailwindcss/comments/1ittpy3/a_complete_guide_to_installing_tailwind_css_4_in/
[44] Tailwind CSS 4.0 is finally here - The NEW way to install with Vite + ... https://www.youtube.com/watch?v=sHnG8tIYMB4
[45] What's New and Migration Guide: Tailwind CSS v4.0 https://dev.to/kasenda/whats-new-and-migration-guide-tailwind-css-v40-3kag
[46] Tailwind CSS v4.0 is Here: Speed, Simplicity, and Migration Guide https://jsdevblog.hashnode.dev/tailwind-css-v4-migration-guide
[47] Use Tailwind CSS v4 - Rsbuild https://rsbuild.dev/guide/basic/tailwindcss
