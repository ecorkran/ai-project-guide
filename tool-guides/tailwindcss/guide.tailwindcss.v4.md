---
docType: guide
layer: tool-guide
tool: tailwindcss
subject: v4-migration
audience: [human, ai]
description: Key changes, migration guide, and setup for Tailwind CSS v4
---

# Tailwind CSS v4 Guide: Key Changes, Migration, and Setup

Tailwind CSS v4 introduces major changes that break compatibility with v3, but also greatly simplify and modernize the framework. Here's a concise guide to help you get started and avoid the pitfalls that are likely causing your project issues.

---

**Major Changes in Tailwind CSS v4**

- **CSS-First Configuration**: No more `tailwind.config.js`. All configuration is now done directly in your CSS file using the new `@theme` directive. This means you define design tokens, custom colors, breakpoints, etc., right inside your CSS[1][4][5].
- **Performance**: Build times are dramatically faster-full builds up to 5x faster, incremental builds over 100x faster[1].
- **Modern CSS Features**: Uses cascade layers, registered custom properties, logical properties, and the `color-mix()` function for more powerful and flexible styling[1].
- **Automatic Content Detection**: Tailwind now automatically finds your template files, so you don’t need to manually specify content paths[1].
- **New Utilities & Variants**: Includes new utilities like 3D transforms, expanded gradients, `not-*` variants, `field-sizing`, `color-scheme`, and more[1][3].
- **Browser Support**: v4 targets modern browsers only (Safari 16.4+, Chrome 111+, Firefox 128+). If you need to support older browsers, stick to v3.4[4].

---

**Migrating from Tailwind v3 to v4**

1. **Update Node.js**: You need Node.js 20 or later[2][4].
2. **Use the Official Upgrade Tool**:
   ```bash
   npx @tailwindcss/upgrade
   ```
   - This tool updates dependencies, migrates your config from JS to CSS, and adapts your template files[2][4].
   - Run it in a new Git branch to easily review and test changes[2][4].

3. **Review and Test**: After running the tool, check your project in a browser and tweak as needed. Some manual adjustments may be necessary for complex setups[2][4].

---

**Setting Up a New Tailwind CSS v4 Project**

1. **Install Tailwind CSS v4**:
   ```bash
   npm install tailwindcss@latest @tailwindcss/cli@latest
   ```
   Or with Vite:
   ```bash
   npm install tailwindcss@latest @tailwindcss/vite@latest
   ```

2. **Create Your CSS File** (e.g., `styles.css`):
   ```css
   @import "tailwindcss";

   @theme {
     --color-primary: hsl(220, 90%, 56%);
     --font-display: "Inter", sans-serif;
     --breakpoint-xl: 1280px;
     /* Add more tokens as needed */
   }
   ```

   - All your design tokens (colors, fonts, breakpoints, etc.) go inside the `@theme` block[1][5].
   - Tailwind will auto-generate utility classes for these tokens (e.g., `bg-primary`, `text-primary`)[5].

3. **Remove Old JS Config**: Delete any `tailwind.config.js` files. All configuration now lives in your CSS[1][5].

4. **Build Your CSS**: Use the CLI or your build tool as before, but now with the simplified setup.

---

**Common Gotchas**

- **No More `tailwind.config.js`**: Trying to use JS config will break your setup. Move all config to CSS.
- **Token Naming**: Use the right prefixes (`--color-*`, `--font-*`, etc.) for Tailwind to generate the correct utilities[5].
- **Browser Support**: If your users need older browsers, v4 may not be for you yet[4].
- **Plugins**: Some third-party plugins may not be v4-ready; check compatibility.

---

**Extra Tips**

- **New Features**: Explore new utilities like `text-shadow-*`, `mask-*`, and advanced variants for more control[3].
- **Performance**: Enjoy much faster builds, especially for incremental changes[1].

---

## Example: Minimal Tailwind v4 CSS Config

```css
@import "tailwindcss";

@theme {
  --color-primary: #2563eb;
  --color-secondary: #64748b;
  --font-display: "Inter", sans-serif;
  --breakpoint-lg: 1024px;
}
```
This will generate classes like `bg-primary`, `text-secondary`, `font-display`, and responsive utilities for your custom breakpoints[5].

---

## Summary Table: Tailwind v3 vs v4

| Feature                | Tailwind v3                     | Tailwind v4                        |
|------------------------|---------------------------------|------------------------------------|
| Config file            | `tailwind.config.js` (JS)       | `@theme` in CSS                    |
| Custom tokens          | JS object                       | CSS custom properties              |
| Content detection      | Manual paths in config          | Automatic                          |
| Build speed            | Fast                            | Much faster                        |
| Browser support        | Broad (incl. older browsers)    | Modern only (Safari 16.4+, etc.)   |
| Plugins                | Many, but check v4 compatibility| Many, but check v4 compatibility   |

---

**For the official upgrade guide and more details, see the [Tailwind CSS v4 Upgrade Guide][4].**

If your AI is still writing v3 code, prompt it to use the new CSS-based config and point it to the v4 documentation. This should resolve most breaking issues and save you hours of frustration.

Sources
[1] Tailwind CSS v4.0 https://tailwindcss.com/blog/tailwindcss-v4
[2] What's New and Migration Guide: Tailwind CSS v4.0 https://dev.to/kasenda/whats-new-and-migration-guide-tailwind-css-v40-3kag
[3] Tailwind CSS v4.1: Text shadows, masks, and tons more https://tailwindcss.com/blog/tailwindcss-v4-1
[4] Upgrade guide - Getting started - Tailwind CSS https://tailwindcss.com/docs/upgrade-guide
[5] A First Look at Setting Up Tailwind CSS v4.0 https://bryananthonio.com/blog/configuring-tailwind-css-v4/
[6] All in on v4 or support v3? : r/tailwindcss - Reddit https://www.reddit.com/r/tailwindcss/comments/1izqz6m/all_in_on_v4_or_support_v3/
[7] Tailwind CSS 4.0 Crash Course: Full Overview of New Features and ... https://www.youtube.com/watch?v=7IK9j9-H0vQ
[8] Tailwind v4 - Shadcn UI https://ui.shadcn.com/docs/tailwind-v4
[9] TailwindCSS v4.0: Upgrading from v3 with some plugins https://dev.to/sirneij/tailwindcss-v40-upgrading-from-v3-with-some-plugins-572f
[10] Tailwind CSS v4: Key Updates and Features - Tailkits https://tailkits.com/blog/tailwind-css-v4-updates-features/
[11] tailwind v4 css order different to tailwind v3 - how to fix? #16160 https://github.com/tailwindlabs/tailwindcss/discussions/16160
[12] Tailwind CSS 4.0: Everything you need to know in one place https://daily.dev/blog/tailwind-css-40-everything-you-need-to-know-in-one-place
[13] Installing Tailwind CSS with Vite https://tailwindcss.com/docs
[14] Tailwind V4 migration : r/nextjs - Reddit https://www.reddit.com/r/nextjs/comments/1ilo0o7/tailwind_v4_migration/
[15] What's New in Tailwind v4 - DEV Community https://dev.to/best_codes/exciting-updates-in-tailwind-version-4-40i0
[16] [v4] Upgrading to tailwind v4 produces a larger css than v3. #15544 https://github.com/tailwindlabs/tailwindcss/discussions/15544
[17] A Complete Guide to Installing Tailwind CSS 4 in Backend ... - Reddit https://www.reddit.com/r/tailwindcss/comments/1ittpy3/a_complete_guide_to_installing_tailwind_css_4_in/
[18] Tailwind CSS v4 Full Course 2025 | Master Tailwind in One Hour https://www.youtube.com/watch?v=6biMWgD6_JY
[19] Getting started with Tailwind v4 - DEV Community https://dev.to/plainsailing/getting-started-with-tailwind-v4-3cip
[20] Open-sourcing our progress on Tailwind CSS v4.0 https://tailwindcss.com/blog/tailwindcss-v4-alpha
