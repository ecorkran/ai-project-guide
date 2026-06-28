---
description: React component patterns, hooks conventions, and JSX best practices. Use when working with React components. Assumes TypeScript rules also apply for .tsx files.
paths: 
  - "**/*.tsx"
  - "**/*.jsx"
  - "src/components/**/*"
  - "app/**/*"
---

### React and Next.js Rules

#### Components & Naming
- Use functional components
- Prefer **client components** (`"use client"`) for interactive UI - use server components only when specifically beneficial
- Name in PascalCase under `src/components/`
- Keep them small, typed with interfaces
- Stack: React + Tailwind 4 + Radix primitives (no ShadCN)

#### React and Next.js Structure
- Use App Router in `app/` (works for both React and Next.js projects)
- **Authentication**: Don't implement auth from scratch - use established providers (Auth0, Clerk, etc.) or consult with PM first
- Use `.env` for secrets and configuration

#### State Management
- **Local state**: Use React's built-in hooks (`useState`, `useReducer`, `useContext`)
- **Global state**: For complex global state needs, consider Zustand or Jotai
- **Server state**: Use TanStack Query (React Query) for API data fetching, caching, and synchronization

#### Forms
- Use `react-hook-form` with Zod schema validation
- Integrate with Radix form primitives for accessible form controls
- Example pattern:
  ```tsx
  const schema = z.object({ email: z.string().email() });
  const form = useForm({ resolver: zodResolver(schema) });
  ```

#### Icons
- Prefer `lucide-react`; name icons in PascalCase
- Custom icons in `src/components/icons`

#### Toast Notifications
- Use `react-toastify` in client components
- `toast.success()`, `toast.error()`, etc.

#### Tailwind Usage
- **Always use Tailwind 4** - configure in `globals.css` using CSS variables and `@theme`
- **Never use Tailwind 3** patterns or `tailwind.config.ts` / `tailwind.config.js` files
- If a tailwind config file exists, there should be a very good reason it's not in `globals.css`
- Use Tailwind utility classes (mobile-first, dark mode with `dark:` prefix)
- For animations, prefer Framer Motion

#### Radix Primitives
- Use Radix primitives directly for accessible, unstyled components
- Style them with Tailwind and semantic color system
- Do not use ShadCN - use raw Radix primitives instead

#### Code Style
- Use `eslint` unless directed otherwise
- Use `prettier` if working in languages it supports

#### File & Folder Names
- Routes in kebab-case (e.g. `app/dashboard/page.tsx`)
- Sort imports (external → internal → sibling → styles)

#### Testing
- Prefer `vitest` over jest

#### Builds
- Use `pnpm` not `npm`
- After all changes are made, ALWAYS build the project with `pnpm build`. Allow warnings, fix errors
- If a `package.json` exists, ensure the AI-support script block from `snippets/npm-scripts.ai-support.json` is present before running `pnpm build`
