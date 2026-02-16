---
docType: guide
layer: tool-guide
tool: radix
subject: theming
audience: [human, ai]
description: Comprehensive guide to Radix Colors for dynamic theming with Tailwind v4
dateUpdated: 20260121
---

# Radix Color Theming Guide

A comprehensive guide to using Radix Colors for dynamic theming in your Next.js application with Tailwind CSS v4 and ShadCN UI components.

## Table of Contents

- [What is Radix Colors?](#what-is-radix-colors)
- [Understanding the Color Scale](#understanding-the-color-scale)
- [Our Implementation](#our-implementation)
- [File Structure](#file-structure)
- [Using Colors in Components](#using-colors-in-components)
- [Palette Switching](#palette-switching)
- [Creating Custom Palettes](#creating-custom-palettes)
- [Best Practices](#best-practices)
- [Testing Your Colors](#testing-your-colors)

## What is Radix Colors?

[Radix Colors](https://www.radix-ui.com/colors) is a color system designed for building accessible, beautiful user interfaces. It provides:

- **12-step color scales** with semantic meaning for each step
- **Automatic light/dark mode pairing** that maintains visual relationships
- **P3 wide-gamut support** with sRGB fallbacks
- **30+ pre-built color palettes** covering the full spectrum
- **Accessibility-first design** with WCAG-compliant contrast ratios

### Why Use Radix Colors?

Traditional color systems often break down when switching themes or require manual contrast calculations. Radix Colors solves this by providing semantically meaningful color steps that work consistently across light and dark themes.

## Understanding the Color Scale

Each Radix color palette has 12 steps with specific semantic purposes:

| Step | Purpose | Example Use |
|------|---------|-------------|
| 1-2  | App backgrounds | Page backgrounds, card surfaces |
| 3-5  | Component backgrounds | Subtle fills, hover states |
| 6-8  | Borders and separators | Input borders, dividers |
| 9-10 | Solid colors | Primary buttons, accent elements |
| 11-12| Text colors | Body text, high contrast text |

**Key Principle**: Use the same step number across different palettes to maintain consistent visual hierarchy when switching themes.

## Our Implementation

Our theming system uses a **hybrid approach** that combines:

1. **Custom brand palettes** (teal, mintteal) generated using [Radix Custom Palette Generator](https://www.radix-ui.com/colors/custom)
2. **Standard Radix palettes** (blue, purple, green) for variety
3. **Semantic color mapping** that abstracts specific colors behind meaningful names
4. **Dynamic palette switching** via CSS custom properties

### Architecture Overview

```
Radix Color Palettes → Semantic Color System → Component Variants → UI Components
```

## File Structure

### Core Color Files

```
src/styles/
├── radixCustomColors.css    # Custom brand palettes + standard Radix palettes
├── semanticColors.css       # Semantic color mapping system
└── cardThemes.css          # Card-specific theme implementations

src/lib/
└── cardVariants.ts         # Component variant definitions using semantic colors
```

### `radixCustomColors.css`

Defines all available color palettes with full light/dark mode support:

```css
/* Custom brand palettes */
:root {
  --teal-1: #f9fefd;
  --teal-9: #14b8ad;
  --teal-12: #0d5d56;
  /* ... all 12 steps */
}

.dark {
  --teal-1: #0b1312;
  --teal-9: #14b8ad;
  --teal-12: #a9f0e8;
  /* ... all 12 steps */
}
```

### `semanticColors.css`

Maps semantic roles to specific color steps, enabling easy palette switching:

```css
:root {
  /* Default palette mapping */
  --color-accent-1: var(--teal-1);
  --color-accent-9: var(--teal-9);
  --color-accent-12: var(--teal-12);
  
  /* Card-specific semantic colors */
  --color-card-accent: var(--color-accent-9);
  --color-card-border: var(--color-accent-7);
  --color-card-text-primary: var(--color-accent-12);
}

/* Palette switching via data attribute */
[data-palette="blue"] {
  --color-accent-1: var(--blue-1);
  --color-accent-9: var(--blue-9);
  --color-accent-12: var(--blue-12);
}
```

## Using Colors in Components

### In Tailwind Classes

Use semantic color variables in your Tailwind classes:

```tsx
// ✅ Good - Uses semantic colors
<div className="bg-[var(--color-card-accent-subtle)] text-[var(--color-accent-12)]">
  Content
</div>

// ❌ Avoid - Hardcoded colors
<div className="bg-teal-100 text-teal-900">
  Content
</div>
```

### In Component Variants

Our `cardVariants` utility uses semantic colors for consistent theming:

```typescript
export const cardVariants = cva('...', {
  variants: {
    variant: {
      accent: 'bg-[var(--color-card-accent-subtle)] text-[var(--color-accent-12)]',
      surface: 'bg-[var(--card-surface-accessible)] text-[var(--card-surface-text)]',
      gradient: 'text-white bg-gradient-to-br from-[var(--color-accent-9)] to-green-500',
    }
  }
});
```

### Available Semantic Colors

| Semantic Variable | Purpose | Radix Step |
|-------------------|---------|------------|
| `--color-accent-1` | App background | Step 1 |
| `--color-accent-9` | Primary accent | Step 9 |
| `--color-accent-12` | High contrast text | Step 12 |
| `--color-card-accent` | Card accent elements | Step 9 |
| `--color-card-border` | Card borders | Step 7 |
| `--color-card-text-primary` | Card text | Step 12 |

## Palette Switching

### Current Implementation

Palette switching is handled via the `data-palette` attribute:

```tsx
// Switch to blue palette
<div data-palette="blue">
  <Card variant="accent">Blue themed card</Card>
</div>

// Switch to purple palette  
<div data-palette="purple">
  <Card variant="accent">Purple themed card</Card>
</div>
```

### Available Palettes

- `custom` (default) - Your brand teal
- `mintteal` - Lighter brand variant
- `blue` - Standard Radix blue
- `purple` - Standard Radix purple
- `green` - Standard Radix green

### Interactive Palette Switching

For a live demonstration of palette switching with all card variants, visit the comprehensive gallery at [templates.manta.digital](https://templates.manta.digital).

## Creating Custom Palettes

### Using Radix Custom Palette Generator

1. Visit [Radix Custom Palette Generator](https://www.radix-ui.com/colors/custom)
2. Input your brand color (e.g., `#14b8ad`)
3. Copy the generated CSS
4. Add to `radixCustomColors.css`:

```css
/* Your new palette */
:root {
  --brand-1: #f9fefd;
  --brand-2: #f1fcfa;
  /* ... all 12 steps */
}

.dark {
  --brand-1: #0b1312;
  --brand-2: #101c1b;
  /* ... all 12 steps */
}
```

5. Add semantic mapping in `semanticColors.css`:

```css
[data-palette="brand"] {
  --color-accent-1: var(--brand-1);
  --color-accent-2: var(--brand-2);
  /* ... map all 12 steps */
}
```

### P3 Wide-Gamut Support

For enhanced color on modern displays, include P3 variants:

```css
@supports (color: color(display-p3 1 1 1)) {
  :root {
    --brand-9: color(display-p3 0.0784 0.7216 0.6784);
  }
}
```

## Best Practices

### Color Usage Guidelines

1. **Use semantic variables** instead of direct color references
2. **Maintain step consistency** across palettes for visual hierarchy
3. **Test accessibility** with all palette combinations
4. **Provide fallbacks** for older browsers

### Component Design

```tsx
// ✅ Good - Semantic and flexible
const Button = ({ variant = "primary" }) => (
  <button className={cn(
    "px-4 py-2 rounded",
    variant === "primary" && "bg-[var(--color-accent-9)] text-white",
    variant === "secondary" && "bg-[var(--color-accent-3)] text-[var(--color-accent-11)]"
  )}>
    Button
  </button>
);

// ❌ Avoid - Hardcoded and inflexible
const Button = () => (
  <button className="px-4 py-2 rounded bg-teal-500 text-white">
    Button
  </button>
);
```

### Accessibility Considerations

- **Step 12** is designed for high contrast text
- **Steps 1-2** provide sufficient contrast for backgrounds
- **Steps 9-10** work well for interactive elements
- Always test color combinations with accessibility tools

## Testing Your Colors

### Interactive Test Page

Visit the comprehensive gallery at [templates.manta.digital](https://templates.manta.digital) to:

- Switch between all available palettes
- View color scales and semantic mappings
- Test card variants with different themes
- Validate contrast and accessibility

### Manual Testing

```tsx
// Test component with different palettes
<div data-palette="blue">
  <YourComponent />
</div>

<div data-palette="purple">
  <YourComponent />
</div>
```

### Accessibility Testing

Use browser dev tools or accessibility checkers to verify:
- Contrast ratios meet WCAG AA/AAA standards
- Colors work for users with color vision deficiencies
- Text remains readable across all palette combinations

## Advanced Usage

### Dynamic Palette Switching with React

For app-wide palette switching, consider implementing a React context:

```tsx
const ThemeContext = createContext();

const ThemeProvider = ({ children }) => {
  const [palette, setPalette] = useState('custom');
  
  useEffect(() => {
    document.documentElement.setAttribute('data-palette', palette);
  }, [palette]);
  
  return (
    <ThemeContext.Provider value={{ palette, setPalette }}>
      {children}
    </ThemeContext.Provider>
  );
};
```

### CSS Transitions

Add smooth transitions between palette changes:

```css
:root {
  transition: 
    background-color 0.3s ease,
    border-color 0.3s ease,
    color 0.3s ease;
}

@media (prefers-reduced-motion: reduce) {
  :root {
    transition: none;
  }
}
```

## Troubleshooting

### Common Issues

**Colors not updating when switching palettes**
- Ensure `data-palette` attribute is set on a parent element
- Check that semantic color mappings exist for the palette
- Verify CSS custom property syntax: `var(--color-name)`

**Poor contrast in custom palettes**
- Use the Radix Custom Palette Generator for proper contrast ratios
- Test with accessibility tools
- Consider using higher contrast steps (11-12) for text

**Colors look different than expected**
- Check if P3 wide-gamut colors are being used
- Verify light/dark mode mappings are correct
- Ensure fallback colors are defined

### Getting Help

- Review the [Radix Colors documentation](https://www.radix-ui.com/colors)
- Test your implementation at [templates.manta.digital](https://templates.manta.digital)
- Check browser dev tools for CSS custom property values

---

This theming system provides a robust foundation for building beautiful, accessible interfaces that can adapt to different brand requirements while maintaining design consistency. The semantic approach ensures your components remain flexible and maintainable as your design system evolves.
