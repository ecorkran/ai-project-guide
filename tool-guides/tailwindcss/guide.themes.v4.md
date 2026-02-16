---
docType: guide
layer: tool-guide
tool: tailwindcss
subject: theming-v4
audience: [human, ai]
description: Color palettes and multi-theme setup for Tailwind CSS v4
dateUpdated: 20260121
---

# Tailwind CSS v4 Theming Guide

How to format your color palettes for the `@theme` block and handle multiple color themes (like light/dark mode or custom themes) in Tailwind CSS v4.

---

## 1. Formatted Color Tokens for `@theme`

Paste the following inside your `@theme` block in your global CSS file (e.g., `globals.css`):

```css
@theme {
  /* Green palette */
  --color-green-50:  #f0fdf4;
  --color-green-100: #dcfce7;
  --color-green-200: #bbf7d0;
  --color-green-300: #86efac;
  --color-green-400: #4ade80;
  --color-green-500: #22c55e;
  --color-green-600: #16a34a;
  --color-green-700: #15803d;
  --color-green-800: #166534;
  --color-green-900: #14532d;
  --color-green-950: #052e16;

  /* Teal palette */
  --color-teal-50:  #f0fdfa;
  --color-teal-100: #ccfbf1;
  --color-teal-200: #99f6e4;
  --color-teal-300: #5eead4;
  --color-teal-400: #2dd4bf;
  --color-teal-500: #14b8a6;
  --color-teal-600: #0d9488;
  --color-teal-700: #0f766e;
  --color-teal-800: #115e59;
  --color-teal-900: #134e4a;
  --color-teal-950: #042f2e;

  /* Mintteal palette */
  --color-mintteal-50:  #A7F5D8;
  --color-mintteal-100: #A7F5D8;
  --color-mintteal-200: #A7F5D8;
  --color-mintteal-300: #A7F5D8;
  --color-mintteal-400: #A7F5D8;
  --color-mintteal-500: #A7F5D8;
  --color-mintteal-600: #A7F5D8;
  --color-mintteal-700: #A7F5D8;
  --color-mintteal-800: #A7F5D8;
  --color-mintteal-900: #A7F5D8;
  --color-mintteal-950: #A7F5D8;

  /* Optional: Set dark mode strategy to class */
  --dark-mode: class;
}
```

---

## 2. **How to Support Multiple Themes (e.g., Dark Mode)**

Tailwind v4 uses CSS custom properties, so you can override them for different themes!

### **Dark Mode Example**

Add a dark theme override by using the `.dark` class (if you use `--dark-mode: class;`):

```css
@theme {
  /* ...your default (light) colors above... */
  --dark-mode: class;
}

/* Dark theme overrides */
.dark {
  --color-green-500: #16a34a;
  --color-teal-500: #0d9488;
  --color-mintteal-500: #0fdac7;
  /* ...override other colors as needed... */
}
```

- Now, when `<body class="dark">` is present, Tailwind will use the overridden color values for your utility classes (`bg-green-500`, etc).

### **Custom Themes Example**

You can define custom themes using any class or attribute selector:

```css
/* Default theme */
@theme {
  --color-primary: #2563eb;
}

/* Custom theme (e.g., for a "brand" theme) */
.brand-theme {
  --color-primary: #eab308;
}
```

Switch themes by toggling the class on a parent element (e.g., `<body class="brand-theme">`).

---

## 3. **How This Works in Practice**

- Use Tailwind classes as normal: `bg-green-500`, `text-teal-700`, etc.
- The color values will change automatically based on the active theme (e.g., `.dark` or `.brand-theme`).

---

## 4. **Paste-Ready Example for `globals.css`**

```css
@import "tailwindcss";
@import "tw-animate-css";

@theme {
  --color-green-50:  #f0fdf4;
  --color-green-100: #dcfce7;
  --color-green-200: #bbf7d0;
  --color-green-300: #86efac;
  --color-green-400: #4ade80;
  --color-green-500: #22c55e;
  --color-green-600: #16a34a;
  --color-green-700: #15803d;
  --color-green-800: #166534;
  --color-green-900: #14532d;
  --color-green-950: #052e16;

  --color-teal-50:  #f0fdfa;
  --color-teal-100: #ccfbf1;
  --color-teal-200: #99f6e4;
  --color-teal-300: #5eead4;
  --color-teal-400: #2dd4bf;
  --color-teal-500: #14b8a6;
  --color-teal-600: #0d9488;
  --color-teal-700: #0f766e;
  --color-teal-800: #115e59;
  --color-teal-900: #134e4a;
  --color-teal-950: #042f2e;

  --color-mintteal-50:  #A7F5D8;
  --color-mintteal-100: #A7F5D8;
  --color-mintteal-200: #A7F5D8;
  --color-mintteal-300: #A7F5D8;
  --color-mintteal-400: #A7F5D8;
  --color-mintteal-500: #A7F5D8;
  --color-mintteal-600: #A7F5D8;
  --color-mintteal-700: #A7F5D8;
  --color-mintteal-800: #A7F5D8;
  --color-mintteal-900: #A7F5D8;
  --color-mintteal-950: #A7F5D8;

  --dark-mode: class;
}

/* Dark theme overrides */
.dark {
  --color-green-500: #16a34a;
  --color-teal-500: #0d9488;
  --color-mintteal-500: #0fdac7;
  /* ...add more overrides as needed... */
}
```

---

## **Summary**

- **Paste the color tokens inside the `@theme` block** in your global CSS file.
- **Override them for dark or custom themes** using a class selector (like `.dark` or `.brand-theme`).
- Use Tailwind utility classes as usual; they’ll pick up your custom colors!

## Checklist

Here’s a checklist and recommendations for finalizing your Tailwind v4 migration before committing:

---

### **Before You Commit: Tailwind v4 Migration Checklist**

- **Review All Upgrade Tool Changes:**  
  Go through the diff in your branch and verify all changes made by the upgrade tool. Make sure nothing important was unintentionally altered or removed, especially in non-Tailwind files[1][6].

- **Test Your Site Thoroughly:**  
  Manually browse your site and test all major pages, components, and interactive features. Look for subtle UI bugs or styling regressions that automated tools might miss[5][1].

- **Check for Legacy/Obsolete Files:**  
  - Ensure `tailwind.config.js` is deleted if you’ve moved all config to CSS.
  - Remove any unused PostCSS plugins like `postcss-import` and `autoprefixer` from your build pipeline, as Tailwind v4 handles imports and vendor prefixing automatically[1][2][4].
  - If you were using Vite, consider switching to the new `@tailwindcss/vite` plugin for better performance[1][4].

- **Update Build Scripts:**  
  - Make sure your build scripts use the new `@tailwindcss/cli` package, not the old PostCSS CLI[2][4].
  - Example:  
    ```json
    "scripts": {
      "build:css": "npx @tailwindcss/cli -i ./path/to/your/input.css -o ./path/to/your/output.css --minify"
    }
    ```

- **Browser Support:**  
  Double-check that your target browsers are supported by Tailwind v4 (Safari 16.4+, Chrome 111+, Firefox 128+). If you need to support older browsers, stay on v3.4[1].

- **Regression Testing:**  
  If possible, run regression tests or use visual diff tools (like Playwright or Percy) to catch subtle visual bugs before deploying[5].

- **Restore/Exclude Non-Tailwind Files:**  
  You already restored `.obsidian/plugins/*`-make sure any other project-specific or IDE files are as you want them before committing.

- **Documentation:**  
  Update any developer docs or README sections that reference old Tailwind config or build steps, so your team (or future you) isn’t confused[3][1].

---

### **Summary Table**

| Task                                     | Completed? |
|-------------------------------------------|:----------:|
| Review upgrade tool changes/diff          |            |
| Test all pages/components in browser      |            |
| Remove legacy config/build files/plugins  |            |
| Update build scripts to use new CLI       |            |
| Confirm browser support                   |            |
| Run regression/visual tests (if possible) |            |
| Restore/exclude non-Tailwind files        |            |
| Update documentation/README               |            |

---

**If all these are checked off and your site works as expected, you’re ready to commit and push your changes!**  
This will help ensure your Tailwind v4 migration is clean, robust, and future-proof[1][2][5][6].

### Additional Directions
We will update to a more advanced example supporting three or more themes, and using CSS variables for additional properties.




Sources
[1] Upgrade guide - Getting started - Tailwind CSS https://tailwindcss.com/docs/upgrade-guide
[2] Upgrading a Rails App to Tailwind v4 - HYBRD https://hybrd.co/posts/upgrading-a-rails-app-to-tailwind-v4
[3] A First Look at Setting Up Tailwind CSS v4.0 https://bryananthonio.com/blog/configuring-tailwind-css-v4/
[4] Getting ready for Tailwind v4.0 - LogRocket Blog https://blog.logrocket.com/getting-ready-tailwind-v4/
[5] The last step in updating to Tailwind CSS 4 | maciek palmowski https://maciekpalmowski.dev/blog/the-last-step-in-updating-to-tailwind-css-4/
[6] What's New and Migration Guide: Tailwind CSS v4.0 https://dev.to/kasenda/whats-new-and-migration-guide-tailwind-css-v40-3kag
[7] Why Upgrading to Tailwind CSS 4.1.4 Might Be the Best Decision ... https://dev.to/gerryleonugroho/why-upgrading-to-tailwindcss-414-might-be-the-best-decision-you-make-this-year-4bc5
[8] Tailwind CSS v4.0 https://tailwindcss.com/blog/tailwindcss-v4
[9] TailwindCSS “Best Practices”? - Reddit https://www.reddit.com/r/tailwindcss/comments/1i2rcs3/tailwindcss_best_practices/
[10] Tailwind CSS v4: what developers need to know - Eagerworks https://eagerworks.com/blog/tailwind-css-v4
[11] How to Upgrade Your Astro Site to Tailwind v4 - Brian Douglass https://bhdouglass.com/blog/how-to-upgrade-your-astro-site-to-tailwind-v4/
[12] Upgrading from v3 to v4 : r/tailwindcss - Reddit https://www.reddit.com/r/tailwindcss/comments/1icx7f9/upgrading_from_v3_to_v4/
[13] Migration to v4 css based config · tailwindlabs tailwindcss - GitHub https://github.com/tailwindlabs/tailwindcss/discussions/13813
[14] Safelist in V4 · tailwindlabs tailwindcss · Discussion #15291 - GitHub https://github.com/tailwindlabs/tailwindcss/discussions/15291
[15] UPGRADE Tailwind CSS v3 to v4 - YouTube https://www.youtube.com/watch?v=dIu_HnGPleg
[16] css - How to upgrade TailwindCSS? - Stack Overflow https://stackoverflow.com/questions/79380519/how-to-upgrade-tailwindcss
[17] How to setting Tailwind CSS v4 global class? - Stack Overflow https://stackoverflow.com/questions/79383758/how-to-setting-tailwind-css-v4-global-class
[18] Tailwind CSS v4 Full Course 2025 | Master Tailwind in One Hour https://www.youtube.com/watch?v=6biMWgD6_JY
[19] Migrating from Tailwind CSS V3 to V4 - YouTube https://www.youtube.com/watch?v=WaYgFtYiYdw
[20] Upgrading to Tailwind CSS v4: A Practical Guide - Villa Plus - LinkedIn https://www.linkedin.com/pulse/upgrading-tailwind-css-v4-practical-guide-villa-plus-ruxnf
