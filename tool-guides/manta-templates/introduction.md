---
docType: intro-guide
platform: manta-templates
audience: [ ai, human ]
features: [ layouts, cards, grids, components, responsive-design ]
purpose: Comprehensive guide to manta-templates component system and layouts
dateUpdated: 20250724
---

# Manta Templates - Component & Layout System 🎯

_Modern React components with flexible grid layouts for AI-powered applications._

> **Why manta-templates?** Pre-built, responsive components and layouts that streamline building modern web applications with consistent design patterns and excellent developer experience.

---

## Summary

Manta Templates provides a comprehensive component library built on Next.js 15, Tailwind CSS v4, and ShadCN components. The system features flexible grid layouts (Bento and GridLayout), specialized cards for different content types, and responsive design patterns optimized for both human users and AI development workflows.

---

## Prerequisites

- Node.js ≥ 18
- pnpm ≥ 8
- TypeScript knowledge
- Basic React familiarity
- Tailwind CSS understanding

---

## Quickstart (copy-paste)

```bash
# Create new project from template
pnpm dlx degit manta-digital/manta-templates/templates/nextjs my-project
cd my-project
pnpm install

# Set up project guides (optional)
pnpm setup-guides

# Start development
pnpm dev
```

---

## Component Architecture

### Core Philosophy
- **Composable**: All components work together seamlessly
- **Responsive**: Mobile-first design with breakpoint-aware layouts  
- **Accessible**: Built on ShadCN's accessible component primitives
- **AI-Friendly**: Clear props, predictable behavior, excellent TypeScript support

### Component Categories

| Category | Purpose | Examples |
|----------|---------|----------|
| **Layouts** | Grid systems and containers | `BentoLayout`, `GridLayout`, `Container` |
| **Cards** | Content display components | `BlogCard`, `ProjectCard`, `VideoCard`, `QuoteCard` |
| **UI Primitives** | Base interactive elements | `BaseCard`, `Button`, `ThemeToggle` |
| **Containers** | Data-fetching wrappers | `BlogCardContainer`, `ProjectCardContainer` |

---

## Layout Systems

### BentoLayout - Item-Driven Grids
Use when individual items need to control their own placement and spanning:

```tsx
import { BentoLayout } from '@/components/layouts';
import { BaseCard } from '@/components/cards';

<BentoLayout gap={6} rowHeight="minmax(180px, auto)" columns="grid-cols-6">
  <BaseCard className="col-span-2 row-span-2">Hero Content</BaseCard>
  <BaseCard className="col-span-4 row-span-1">Wide Content</BaseCard>
  <BaseCard className="col-span-3 row-span-1">Regular Content</BaseCard>
</BentoLayout>
```

### GridLayout - Data-Driven Grids  
Use when you need strict, predetermined grid patterns:

```tsx
import { GridLayout } from '@/components/layouts/grid-layout';

const gridData = {
  mobile: [[6], [6], [6]], // Full width on mobile
  tablet: [[3, 3], [6]],   // 2-col then full on tablet  
  desktop: [[2, 2, 2]]     // 3-col on desktop
};

<GridLayout gridData={gridData}>
  <Card>Item 1</Card>
  <Card>Item 2</Card>
  <Card>Item 3</Card>
</GridLayout>
```

---

## Essential Cards

### Content Cards
- **BlogCard**: Article previews with metadata
- **ProjectCard**: Project showcases with links and descriptions  
- **VideoCard**: Video embeds with React Player integration
- **QuoteCard**: Styled quotations with attribution

### Specialized Cards
- **FeatureCard**: Feature highlights with status indicators
- **GuidesFeatureCard**: Documentation feature displays
- **ThreeJSCard**: 3D content integration

### Usage Pattern
```tsx
import { BlogCard, ProjectCard } from '@/components/cards';

// Direct usage
<BlogCard 
  title="Getting Started"
  description="Learn the basics"
  slug="getting-started"
  readTime="5 min"
/>

// Container pattern (with data fetching)
<BlogCardContainer slug="getting-started" />
```

---

## Responsive Breakpoints

Built-in breakpoint system using Tailwind CSS:

| Breakpoint | Size | Usage |
|------------|------|-------|
| `mobile` | < 768px | 1-column layouts |
| `tablet` | 768px - 1024px | 2-3 column layouts |
| `desktop` | > 1024px | Multi-column grids |

Use `useBreakpoint()` hook for conditional rendering:

```tsx
import { useBreakpoint } from '@/hooks/useBreakpoint';

const currentBreakpoint = useBreakpoint();
// Returns: 'mobile' | 'tablet' | 'desktop'
```

---

## Common Patterns

### Hero + Content Grid
```tsx
<BentoLayout gap={6} className="max-w-7xl mx-auto">
  <BaseCard className="col-span-6 md:col-span-4 row-span-2">
    <HeroContent />
  </BaseCard>
  <BaseCard className="col-span-6 md:col-span-2">
    <SidebarContent />
  </BaseCard>
</BentoLayout>
```

### Blog Layout
```tsx
<Container>
  <GridLayout gridData={blogGridData}>
    <BlogHeroCard slug="featured-post" />
    <BlogCard slug="post-1" />
    <BlogCard slug="post-2" />
  </GridLayout>
</Container>
```

### Project Showcase
```tsx
<BentoLayout columns="grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
  {projects.map(project => (
    <ProjectCard key={project.slug} {...project} />
  ))}
</BentoLayout>
```

---

## Styling System

### Tailwind CSS v4
- CSS-based configuration (no `tailwind.config.js`)
- Custom properties for theming
- Radix Colors integration for consistent color palettes

### Theme System
```tsx
import { ThemeProvider } from '@/context/themecontext';

// Automatic dark/light mode with system preference detection
<ThemeProvider defaultTheme="dark" storageKey="ui-theme">
  <App />
</ThemeProvider>
```

---

## Next Steps

- **Setup Guide**: `tool-guides/manta-templates/setup.md` - Detailed installation and configuration
- **Component Reference**: `tool-guides/manta-templates/knowledge.md` - Complete component API
- **Examples**: `/src/app/examples/` - Live component demonstrations
- **Source Code**: Browse `/src/components/` for implementation details

### External Resources
- [Tailwind CSS v4 Docs](https://tailwindcss.com/docs) ↗
- [ShadCN Components](https://ui.shadcn.com) ↗  
- [Radix Colors](https://www.radix-ui.com/colors) ↗
- [Next.js 15 Guide](https://nextjs.org/docs) ↗

---

**Ready to build?** Start with the examples in `/src/app/examples/` to see components in action, then dive into the setup guide for detailed configuration options. 