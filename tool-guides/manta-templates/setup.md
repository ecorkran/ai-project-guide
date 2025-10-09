---
docType: setup-guide
platform: manta-templates
audience: [ ai, human ]
purpose: Detailed installation, configuration, and customization guide for manta-templates
---

# Manta Templates - Setup & Configuration 🔧

_Complete installation and customization guide for the manta-templates system._

---

## Installation Methods

### Method 1: Degit (Recommended)
```bash
# Clone template without git history
pnpm dlx degit manta-digital/manta-templates/templates/nextjs my-project
cd my-project
pnpm install
```

### Method 2: Git Clone
```bash
# Clone full repository
git clone https://github.com/manta-digital/manta-templates.git
cd manta-templates/templates/nextjs
pnpm install

# Optional: Remove git history for fresh start
rm -rf .git && git init
```

### Method 3: Manual Download
1. Download repository as ZIP from GitHub
2. Extract to desired location
3. Navigate to `templates/nextjs/`
4. Run `pnpm install`

---

## Project Structure

```
my-project/
├── src/
│   ├── app/                    # Next.js 15 App Router
│   │   ├── examples/          # Component demonstrations
│   │   ├── blog/             # Blog pages
│   │   ├── layout.tsx        # Root layout
│   │   └── page.tsx          # Homepage
│   ├── components/
│   │   ├── cards/            # Card components
│   │   ├── layouts/          # Layout systems
│   │   ├── ui/               # Base UI components
│   │   └── index.ts          # Component exports
│   ├── content/              # Markdown content
│   ├── context/              # React contexts
│   ├── hooks/                # Custom hooks
│   ├── lib/                  # Utilities
│   ├── styles/               # CSS files
│   └── types/                # TypeScript definitions
├── public/                   # Static assets
├── scripts/                  # Setup and utility scripts
└── project-documents/        # AI guides (after setup-guides)
```

---

## Environment Configuration

### Environment Variables
Create `.env.local` for local development:

```bash
# Site configuration
NEXT_PUBLIC_SITE_URL=http://localhost:3000

# Theme settings (optional)
NEXT_PUBLIC_DEFAULT_THEME=dark

# Analytics (optional)
NEXT_PUBLIC_GA_ID=your-ga-id
```

### Production Environment
```bash
# Vercel deployment
NEXT_PUBLIC_SITE_URL=https://your-domain.com

# Custom domain configuration
NEXT_PUBLIC_DOMAIN=your-domain.com
```

---

## Package Manager Setup

### pnpm (Recommended)
```bash
# Install pnpm globally
npm install -g pnpm

# Verify installation
pnpm --version

# Install dependencies
pnpm install

# Development server
pnpm dev
```

### npm Alternative
```bash
# Remove pnpm-lock.yaml
rm pnpm-lock.yaml

# Install with npm
npm install

# Update scripts in package.json if needed
npm run dev
```

---

## AI Project Guides Setup

### Basic Setup
```bash
# Set up public guides from GitHub
pnpm setup-guides
```

This creates:
- `project-documents/` with comprehensive AI development guides
- `project-documents/user/` for project-specific customizations
- Enables version control for project-documents

### Private Organization Guides
Create `.env` file with your private guides repository:

```bash
# .env
EXTERNAL_PROJECT_DOC_URL=git@github.com:your-org/external-guides.git
```

Then run:
```bash
# Set up public + private guides
pnpm setup-guides:private
```

### Updating Guides
```bash
# Update to latest public guides
pnpm update-guides

# This preserves your user/ directory content
```

---

## Tailwind CSS v4 Configuration

### CSS Configuration
Styles are configured in `src/app/globals.css`:

```css
@import "tailwindcss";

/* Custom theme configuration */
@theme {
  --font-family-sans: "Geist Sans", system-ui, sans-serif;
  --font-family-mono: "Geist Mono", "Courier New", monospace;
  
  /* Custom colors */
  --color-brand-50: #f0f9ff;
  --color-brand-500: #3b82f6;
  --color-brand-900: #1e3a8a;
}

/* Component styles */
@layer components {
  .card-hover {
    @apply transition-all duration-300 ease-in-out hover:shadow-lg;
  }
}
```

### No JavaScript Config
Tailwind v4 uses CSS-based configuration. No `tailwind.config.js` needed.

### Custom Utilities
Add custom utilities in `src/styles/`:

```css
/* src/styles/custom.css */
.text-gradient {
  @apply bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent;
}
```

---

## Component Customization

### Extending Base Components
```tsx
// src/components/custom/MyCard.tsx
import { BaseCard, type BaseCardProps } from '@/components/cards';
import { cn } from '@/lib/utils';

interface MyCardProps extends BaseCardProps {
  variant?: 'primary' | 'secondary';
}

export function MyCard({ variant = 'primary', className, ...props }: MyCardProps) {
  return (
    <BaseCard
      className={cn(
        'my-custom-styles',
        variant === 'primary' && 'border-blue-500',
        variant === 'secondary' && 'border-gray-300',
        className
      )}
      {...props}
    />
  );
}
```

### Custom Layout Patterns
```tsx
// src/components/layouts/CustomLayout.tsx
import { BentoLayout } from '@/components/layouts';

interface CustomLayoutProps {
  children: React.ReactNode;
}

export function CustomLayout({ children }: CustomLayoutProps) {
  return (
    <BentoLayout 
      gap={8} 
      rowHeight="minmax(200px, auto)"
      className="max-w-6xl mx-auto p-6"
    >
      {children}
    </BentoLayout>
  );
}
```

---

## Content Management

### Markdown Content
Add content files in `src/content/`:

```markdown
---
title: "My Blog Post"
description: "Post description"
pubDate: 2024-01-15
category: "tutorial"
---

# My Blog Post

Content goes here...
```

### Content Configuration
Configure content types in `src/content/config.ts`:

```typescript
import { z } from 'zod';

export const blogSchema = z.object({
  title: z.string(),
  description: z.string(),
  pubDate: z.date(),
  category: z.string(),
  featured: z.boolean().optional(),
});

export type BlogPost = z.infer<typeof blogSchema>;
```

---

## Development Workflow

### Development Server
```bash
# Start with Turbopack (faster builds)
pnpm dev

# Standard Next.js dev server
pnpm dev:legacy
```

### Build & Deploy
```bash
# Production build
pnpm build

# Start production server
pnpm start

# Type checking
pnpm type-check

# Linting
pnpm lint

# Format code
pnpm format
```

### AI-Assisted Development
```bash
# AI-friendly build command
pnpm ai-assisted-build

# Includes: type-check + lint + format + build
```

---

## Deployment Platforms

### Vercel (Recommended)
1. Connect GitHub repository to Vercel
2. Set environment variables in dashboard
3. Deploy automatically on push

Build settings:
- Build Command: `pnpm build`
- Output Directory: `.next`
- Install Command: `pnpm install`

### Netlify
```toml
# netlify.toml
[build]
  command = "pnpm build"
  publish = ".next"

[[plugins]]
  package = "@netlify/plugin-nextjs"
```

### Docker
```dockerfile
# Dockerfile
FROM node:18-alpine

WORKDIR /app
COPY package*.json pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install

COPY . .
RUN pnpm build

EXPOSE 3000
CMD ["pnpm", "start"]
```

---

## Performance Optimization

### Image Optimization
```tsx
import Image from 'next/image';

// Optimized images with Next.js
<Image
  src="/images/hero.jpg"
  alt="Hero image"
  width={1200}
  height={600}
  priority // For above-the-fold images
  placeholder="blur"
  blurDataURL="data:image/jpeg;base64,..."
/>
```

### Bundle Analysis
```bash
# Analyze bundle size
pnpm build && pnpm analyze

# Install bundle analyzer first
pnpm add -D @next/bundle-analyzer
```

### Font Optimization
Fonts are auto-optimized via `next/font`:

```tsx
// Already configured in layout.tsx
import { Geist, Geist_Mono } from "next/font/google";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});
```

---

## Troubleshooting

### Common Issues

#### Build Errors
```bash
# Clear Next.js cache
rm -rf .next

# Clear node_modules and reinstall
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

#### TypeScript Errors
```bash
# Regenerate type definitions
pnpm type-check

# Update TypeScript
pnpm update typescript
```

#### CSS Issues
```bash
# Regenerate Tailwind
touch src/app/globals.css

# Check for CSS conflicts
pnpm build 2>&1 | grep -i css
```

### Development Tools
```bash
# React Developer Tools (browser extension)
# Tailwind CSS IntelliSense (VS Code extension)
# TypeScript Hero (VS Code extension)
```

---

## Next Steps

- **Component Reference**: `tool-guides/manta-templates/knowledge.md`
- **Examples**: `/src/app/examples/` 
- **AI Guides**: Run `pnpm setup-guides` for comprehensive development guides

### Community Resources
- [GitHub Repository](https://github.com/manta-digital/manta-templates) ↗
- [Documentation Site](https://templates.manta.digital) ↗
- [Issue Tracker](https://github.com/manta-digital/manta-templates/issues) ↗

**Installation complete!** You now have a fully configured manta-templates project ready for development. 