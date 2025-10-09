---
docType: knowledge-guide
platform: manta-templates
audience: [ ai, human ]
purpose: Complete component API reference, patterns, and troubleshooting guide
---

# Manta Templates - Component Reference & Knowledge Base 📖

_Complete API documentation, usage patterns, and troubleshooting guide._

---

## Layout Components

### BentoLayout

**Purpose**: Item-driven grid where children control their own placement and spanning.

**Props**:
```tsx
interface BentoLayoutProps {
  children: React.ReactNode;
  className?: string;
  gap?: number | string;              // Gap between items (Tailwind number or CSS value)
  rowHeight?: string;                 // CSS grid-auto-rows value
  columns?: string;                   // Tailwind grid-cols-* classes
  autoFlow?: 'row' | 'column';       // Grid auto-flow direction
}
```

**Usage**:
```tsx
<BentoLayout 
  gap={6} 
  rowHeight="minmax(180px, auto)" 
  columns="grid-cols-1 md:grid-cols-6"
>
  <BaseCard className="col-span-2 row-span-2">Hero</BaseCard>
  <BaseCard className="col-span-4">Wide content</BaseCard>
</BentoLayout>
```

**Best Practices**:
- Use for flexible, Pinterest-style layouts
- Children should use Tailwind `col-span-*` and `row-span-*` classes
- Perfect for dashboards and marketing pages

---

### GridLayout

**Purpose**: Data-driven grid with predetermined responsive patterns.

**Props**:
```tsx
interface GridLayoutProps {
  gridData: GridData;                 // Breakpoint-to-span mapping
  children: React.JSX.Element[];      // Components to place in grid
  className?: string;
  gap?: string;                       // CSS gap value
  minRowHeight?: string;              // CSS grid-auto-rows value
}

type GridData = {
  [breakpoint: string]: number[][];   // Array of column spans per row
};
```

**Usage**:
```tsx
const gridData = {
  mobile: [[6], [6], [6]],           // Stack vertically on mobile
  tablet: [[3, 3], [6]],             // 2-col then full on tablet
  desktop: [[2, 2, 2], [4, 2]]       // Complex desktop layout
};

<GridLayout gridData={gridData} gap="1.5rem">
  <Card>Item 1</Card>
  <Card>Item 2</Card>
  <Card>Item 3</Card>
  <Card>Item 4</Card>
</GridLayout>
```

**Best Practices**:
- Use for consistent, predictable layouts
- Ideal for blogs, portfolios, galleries
- Children are automatically placed in order

---

### Container

**Purpose**: Responsive wrapper with consistent max-width and padding.

**Props**:
```tsx
interface ContainerProps {
  children: React.ReactNode;
  className?: string;
  maxWidth?: 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '7xl';
  padding?: boolean;                  // Apply default padding
}
```

**Usage**:
```tsx
<Container maxWidth="7xl" padding>
  <h1>Page content</h1>
</Container>
```

---

## Card Components

### BaseCard

**Purpose**: Foundation card component extending ShadCN Card with consistent styling.

**Props**:
```tsx
interface BaseCardProps extends React.ComponentProps<typeof ShadcnCard> {
  className?: string;
  children: React.ReactNode;
}
```

**Available Exports**:
```tsx
import { 
  BaseCard,
  CardHeader,
  CardFooter, 
  CardTitle,
  CardDescription,
  CardContent 
} from '@/components/cards';
```

**Usage**:
```tsx
<BaseCard className="p-6">
  <CardHeader>
    <CardTitle>Title</CardTitle>
    <CardDescription>Description</CardDescription>
  </CardHeader>
  <CardContent>
    Content goes here
  </CardContent>
</BaseCard>
```

---

### BlogCard

**Purpose**: Article preview with metadata and consistent blog styling.

**Props**:
```tsx
interface BlogCardProps {
  title: string;
  description: string;
  slug: string;
  readTime?: string;
  pubDate?: string;
  category?: string;
  image?: string;
  className?: string;
}
```

**Usage**:
```tsx
<BlogCard
  title="Getting Started with Next.js"
  description="Learn the fundamentals"
  slug="getting-started-nextjs"
  readTime="5 min"
  pubDate="2024-01-15"
  category="tutorial"
  image="/images/blog/nextjs.jpg"
/>
```

---

### ProjectCard

**Purpose**: Project showcase with links, tech stack, and status indicators.

**Props**:
```tsx
interface ProjectCardProps {
  title: string;
  description: string;
  slug: string;
  repoUrl?: string;
  liveUrl?: string;
  techStack?: string[];
  status: 'active' | 'completed' | 'archived';
  featured?: boolean;
  image?: string;
  className?: string;
}
```

**Usage**:
```tsx
<ProjectCard
  title="E-commerce Platform"
  description="Full-stack shopping experience"
  slug="ecommerce-platform"
  repoUrl="https://github.com/user/repo"
  liveUrl="https://demo.example.com"
  techStack={['Next.js', 'TypeScript', 'Tailwind']}
  status="active"
  featured={true}
/>
```

---

### VideoCard

**Purpose**: Video content with React Player integration.

**Props**:
```tsx
interface VideoCardProps {
  title: string;
  description?: string;
  url: string;                        // Video URL (YouTube, Vimeo, etc.)
  thumbnail?: string;
  duration?: string;
  category?: string;
  autoplay?: boolean;
  controls?: boolean;
  className?: string;
}
```

**Usage**:
```tsx
<VideoCard
  title="Component Tutorial"
  description="Learn to build components"
  url="https://youtube.com/watch?v=..."
  thumbnail="/images/video-thumb.jpg"
  duration="12:34"
  category="tutorial"
  controls={true}
/>
```

---

### QuoteCard

**Purpose**: Styled quotations with attribution and citation.

**Props**:
```tsx
interface QuoteCardProps {
  quote: string;
  author: string;
  source?: string;
  role?: string;
  avatar?: string;
  className?: string;
}
```

**Usage**:
```tsx
<QuoteCard
  quote="The best code is no code at all."
  author="Jeff Atwood"
  source="Coding Horror"
  role="Software Developer"
  avatar="/images/avatars/jeff.jpg"
/>
```

---

### FeatureCard

**Purpose**: Feature highlights with status, quick start commands, and CTAs.

**Props**:
```tsx
interface FeatureCardProps {
  title: string;
  description: string;
  status: 'available' | 'coming-soon' | 'beta';
  quickStart?: string;                // Command or snippet
  repoUrl?: string;
  category?: string;
  featured?: boolean;
  order?: number;
  className?: string;
}
```

**Usage**:
```tsx
<FeatureCard
  title="Authentication System"
  description="Secure user management"
  status="available"
  quickStart="pnpm add @manta/auth"
  repoUrl="https://github.com/manta/auth"
  category="backend"
  featured={true}
/>
```

---

## Container Components

### BlogCardContainer

**Purpose**: Data-fetching wrapper for BlogCard with content loading.

**Props**:
```tsx
interface BlogCardContainerProps {
  slug: string;
  className?: string;
}
```

**Usage**:
```tsx
<BlogCardContainer slug="my-blog-post" />
```

**Data Loading**: Automatically fetches content from `src/content/blog/{slug}.md`

---

### ProjectCardContainer

**Purpose**: Data-fetching wrapper for ProjectCard.

**Props**:
```tsx
interface ProjectCardContainerProps {
  slug: string;
  className?: string;
}
```

**Usage**:
```tsx
<ProjectCardContainer slug="my-project" />
```

**Data Loading**: Fetches from `src/content/projects/{slug}.md`

---

## Hooks

### useBreakpoint

**Purpose**: Get current responsive breakpoint for conditional rendering.

**Returns**: `'mobile' | 'tablet' | 'desktop'`

**Usage**:
```tsx
import { useBreakpoint } from '@/hooks/useBreakpoint';

function ResponsiveComponent() {
  const breakpoint = useBreakpoint();
  
  return (
    <div>
      {breakpoint === 'mobile' && <MobileView />}
      {breakpoint === 'tablet' && <TabletView />}
      {breakpoint === 'desktop' && <DesktopView />}
    </div>
  );
}
```

---

### useUniformHeight

**Purpose**: Synchronize heights across grid items for consistent layouts.

**Props**:
```tsx
interface UseUniformHeightOptions {
  selector?: string;                  // CSS selector for elements to sync
  dependencies?: any[];               // Re-sync triggers
}
```

**Usage**:
```tsx
import { useUniformHeight } from '@/hooks/useUniformHeight';

function GridComponent() {
  useUniformHeight({ 
    selector: '.grid-item',
    dependencies: [data] 
  });
  
  return (
    <div className="grid">
      <div className="grid-item">Content 1</div>
      <div className="grid-item">Content 2</div>
    </div>
  );
}
```

---

## Utility Functions

### cn (Class Names)

**Purpose**: Merge Tailwind classes with proper conflict resolution.

**Usage**:
```tsx
import { cn } from '@/lib/utils';

const buttonClass = cn(
  'px-4 py-2 rounded',           // Base classes
  variant === 'primary' && 'bg-blue-500 text-white',
  variant === 'secondary' && 'bg-gray-200 text-gray-800',
  className                      // Override classes
);
```

---

## Theme System

### ThemeProvider

**Purpose**: Manage dark/light themes with system preference detection.

**Props**:
```tsx
interface ThemeProviderProps {
  children: React.ReactNode;
  defaultTheme?: 'dark' | 'light' | 'system';
  storageKey?: string;
}
```

**Usage**:
```tsx
// In layout.tsx
<ThemeProvider defaultTheme="dark" storageKey="ui-theme">
  <App />
</ThemeProvider>
```

### ThemeToggle

**Purpose**: UI component for switching themes.

**Usage**:
```tsx
import { ThemeToggle } from '@/components';

<ThemeToggle />
```

---

## Content Management

### Content Structure

```typescript
// Blog post frontmatter
interface BlogPost {
  title: string;
  description: string;
  pubDate: Date;
  category?: string;
  featured?: boolean;
  image?: string;
  readTime?: string;
}

// Project frontmatter  
interface Project {
  title: string;
  description: string;
  status: 'active' | 'completed' | 'archived';
  techStack?: string[];
  repoUrl?: string;
  liveUrl?: string;
  featured?: boolean;
}
```

### Content Loading Patterns

```tsx
// Static content loading
import { getBlogPost } from '@/lib/content';

const post = await getBlogPost('my-slug');

// Dynamic content with error handling
try {
  const project = await getProject(slug);
  return <ProjectCard {...project} />;
} catch (error) {
  return <div>Project not found</div>;
}
```

---

## Common Patterns

### Hero Section with Grid
```tsx
<Container maxWidth="7xl">
  <BentoLayout gap={6} rowHeight="minmax(200px, auto)">
    <BaseCard className="col-span-6 md:col-span-4 row-span-2">
      <HeroContent />
    </BaseCard>
    <BaseCard className="col-span-6 md:col-span-2">
      <SidebarContent />
    </BaseCard>
  </BentoLayout>
</Container>
```

### Blog Grid with Featured Post
```tsx
<Container>
  <GridLayout gridData={{
    mobile: [[6], [6], [6]],
    tablet: [[6], [3, 3]],
    desktop: [[4, 2], [2, 2, 2]]
  }}>
    <BlogCard {...featuredPost} />
    <BlogCard {...post1} />
    <BlogCard {...post2} />
    <BlogCard {...post3} />
  </GridLayout>
</Container>
```

### Project Portfolio
```tsx
<BentoLayout columns="grid-cols-1 md:grid-cols-2 lg:grid-cols-3" gap={6}>
  {projects.map(project => (
    <ProjectCard key={project.slug} {...project} />
  ))}
</BentoLayout>
```

---

## Performance Tips

### Optimization Strategies

| Issue | Solution | Example |
|-------|----------|---------|
| Large grids | Use React.memo for cards | `export default React.memo(BlogCard)` |
| Image loading | Next.js Image with priority | `<Image priority />` for above-fold |
| Bundle size | Dynamic imports | `const Card = dynamic(() => import('./Card'))` |
| Layout shifts | Fixed aspect ratios | `aspect-video`, `aspect-square` classes |

### Bundle Splitting
```tsx
// Lazy load heavy components
const VideoCard = dynamic(() => import('@/components/cards/VideoCard'), {
  loading: () => <CardSkeleton />,
  ssr: false
});
```

---

## Troubleshooting

### Common Issues

#### Grid Layout Not Responsive
```tsx
// ❌ Missing responsive classes
<BentoLayout columns="grid-cols-6">

// ✅ Include responsive breakpoints
<BentoLayout columns="grid-cols-1 md:grid-cols-3 lg:grid-cols-6">
```

#### Cards Not Spanning Correctly
```tsx
// ❌ Missing row definition
<BaseCard className="col-span-4">

// ✅ Include both column and row spans
<BaseCard className="col-span-4 row-span-2">
```

#### Content Not Loading
```tsx
// ❌ Missing await in server component
const post = getBlogPost(slug);

// ✅ Properly await async function
const post = await getBlogPost(slug);
```

#### Theme Not Persisting
```tsx
// ❌ Missing ThemeProvider wrapper
<App />

// ✅ Wrap with ThemeProvider
<ThemeProvider storageKey="ui-theme">
  <App />
</ThemeProvider>
```

### Debug Helpers

```tsx
// Visual grid debugging
<BentoLayout className="[&>*]:border [&>*]:border-red-500">

// Component prop debugging  
console.log('GridData:', JSON.stringify(gridData, null, 2));

// Breakpoint debugging
const breakpoint = useBreakpoint();
console.log('Current breakpoint:', breakpoint);
```

---

## Advanced Customization

### Custom Card Variants
```tsx
// Create themed card variants
const cardVariants = cva(
  'transition-all duration-300', // Base classes
  {
    variants: {
      theme: {
        primary: 'bg-blue-50 border-blue-200',
        secondary: 'bg-gray-50 border-gray-200',
        accent: 'bg-purple-50 border-purple-200'
      },
      size: {
        sm: 'p-4',
        md: 'p-6', 
        lg: 'p-8'
      }
    },
    defaultVariants: {
      theme: 'primary',
      size: 'md'
    }
  }
);

interface CustomCardProps extends BaseCardProps {
  theme?: 'primary' | 'secondary' | 'accent';
  size?: 'sm' | 'md' | 'lg';
}

export function CustomCard({ theme, size, className, ...props }: CustomCardProps) {
  return (
    <BaseCard 
      className={cn(cardVariants({ theme, size }), className)}
      {...props}
    />
  );
}
```

### Custom Grid Patterns
```tsx
// Create reusable grid configurations
export const gridPatterns = {
  blog: {
    mobile: [[6], [6], [6]],
    tablet: [[6], [3, 3]],
    desktop: [[4, 2], [2, 2, 2]]
  },
  portfolio: {
    mobile: [[6]],
    tablet: [[3, 3]],
    desktop: [[2, 2, 2]]
  },
  dashboard: {
    mobile: [[6], [6]],
    tablet: [[4, 2], [6]],
    desktop: [[3, 3], [2, 2, 2]]
  }
};

// Usage
<GridLayout gridData={gridPatterns.blog}>
```

---

## Migration Guide

### From v0.6.x to v0.7.x

#### Breaking Changes
- `our-project/` directory moved to `user/`
- Tailwind config moved to CSS-based configuration
- Some card prop names standardized

#### Migration Steps
```bash
# 1. Update directory structure
mv project-documents/our-project project-documents/user

# 2. Update Tailwind configuration
# Remove tailwind.config.js, add @theme {} to globals.css

# 3. Update component imports
# BlogCardV2 → BlogCard (V2 components became default)
```

---

## API Summary

### Quick Reference Table

| Component | Primary Use | Key Props | Container Available |
|-----------|-------------|-----------|-------------------|
| `BentoLayout` | Flexible grids | `gap`, `rowHeight`, `columns` | No |
| `GridLayout` | Data-driven grids | `gridData`, `children` | No |
| `BaseCard` | Foundation card | `className`, `children` | No |
| `BlogCard` | Article previews | `title`, `slug`, `readTime` | Yes |
| `ProjectCard` | Project showcase | `title`, `status`, `techStack` | Yes |
| `VideoCard` | Video content | `url`, `thumbnail`, `controls` | Yes |
| `QuoteCard` | Quotations | `quote`, `author`, `source` | Yes |
| `FeatureCard` | Feature highlights | `status`, `quickStart` | Yes |

---

**Need more help?** Check the `/src/app/examples/` directory for live component demonstrations and usage patterns. 