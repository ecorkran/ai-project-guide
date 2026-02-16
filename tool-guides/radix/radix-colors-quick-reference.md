---
docType: reference
layer: tool-guide
tool: radix
subject: colors
audience: [human, ai]
description: Quick reference for Radix Colors semantic color system
dateUpdated: 20260121
---

# Radix Colors Quick Reference

## Essential Semantic Colors

```css
/* Primary colors */
--color-accent-1      /* App background (lightest) */
--color-accent-9      /* Primary accent color */
--color-accent-12     /* High contrast text (darkest) */

/* Card colors */
--color-card-accent-subtle    /* Subtle card backgrounds */
--color-card-border          /* Card borders */
--color-card-text-primary    /* Card text */
```

## Palette Switching

```tsx
// Switch palette via data attribute
<div data-palette="blue">
  <YourComponent />
</div>

// Available palettes: custom, mintteal, blue, purple, green
```

## Using in Components

```tsx
// ✅ Use semantic variables
className="bg-[var(--color-card-accent-subtle)] text-[var(--color-accent-12)]"

// ❌ Avoid hardcoded colors  
className="bg-teal-100 text-teal-900"
```

## Card Variants

```tsx
<Card variant="accent">   {/* Uses --color-card-accent-subtle */}
<Card variant="surface">  {/* Uses --card-surface-accessible */}
<Card variant="gradient"> {/* Uses --color-accent-9 gradient */}
```

## Testing

Visit [templates.manta.digital](https://templates.manta.digital) to test all palettes and variants interactively in the comprehensive gallery.

## Color Scale Reference

| Step | Light Mode | Dark Mode | Purpose |
|------|------------|-----------|---------|
| 1    | Lightest   | Darkest   | App background |
| 9    | Accent     | Accent    | Primary elements |
| 12   | Darkest    | Lightest  | Text |

## Quick Setup for New Palette

1. Generate at [radix-ui.com/colors/custom](https://www.radix-ui.com/colors/custom)
2. Add to `radixCustomColors.css`
3. Map in `semanticColors.css`:

```css
[data-palette="yourname"] {
  --color-accent-1: var(--yourcolor-1);
  --color-accent-9: var(--yourcolor-9);
  --color-accent-12: var(--yourcolor-12);
  /* ... map all steps */
}
```
