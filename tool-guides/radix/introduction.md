---
docType: intro-guide
platform: radix-ui
audience: [ai, human]
features: [theming, colors, ui-components, accessibility]
purpose: Guide to using Radix UI Colors and Components for accessible theming
dateUpdated: 20250718
---

# Radix UI Tool Guide

## Summary

Radix UI provides unstyled, accessible components and a comprehensive color system designed for building modern user interfaces. This guide covers Radix Colors integration with Tailwind CSS v4 and ShadCN UI components for dynamic theming.

## Prerequisites

- Node.js ≥ 18
- Next.js 15+ (App Router)
- Tailwind CSS v4
- Basic understanding of CSS custom properties

## What's Included

This tool guide contains the following resources:

### Core Documentation

- **`radix-theming-guide.md`** - Comprehensive guide covering:
  - Radix Colors 12-step scale system
  - Integration with Tailwind CSS v4
  - Dynamic palette switching
  - Custom theme creation
  - Best practices for accessibility

- **`radix-colors-quick-reference.md`** - Quick reference for:
  - Essential semantic color variables
  - Palette switching syntax
  - Common usage patterns
  - Copy-paste code snippets

## Key Features

- **12-step color scales** with semantic meaning for each step
- **Automatic light/dark mode pairing** that maintains visual relationships
- **P3 wide-gamut support** with sRGB fallbacks
- **30+ pre-built color palettes** covering the full spectrum
- **Accessibility-first design** with WCAG-compliant contrast ratios
- **Zero runtime JavaScript** - pure CSS custom properties

## Quick Start

```bash
npm install @radix-ui/colors
```

```css
/* In your globals.css */
@import "@radix-ui/colors/blue.css";
@import "@radix-ui/colors/blue-dark.css";

:root {
  --color-accent-1: var(--blue-1);
  --color-accent-9: var(--blue-9);
  --color-accent-12: var(--blue-12);
}
```

## Next Steps

1. Read `radix-theming-guide.md` for comprehensive implementation details
2. Use `radix-colors-quick-reference.md` for quick lookups during development
3. Explore the semantic color scale system for consistent theming
4. Implement dynamic palette switching for user customization

## External Resources

- [Radix Colors Documentation](https://www.radix-ui.com/colors)
- [Radix UI Components](https://www.radix-ui.com/primitives)
- [Color Scale Playground](https://www.radix-ui.com/colors/docs/palette-composition/the-scales) 