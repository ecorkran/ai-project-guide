# Overview
This file provide a guide to designing and implementing authentication using Supabase.

> **Scope**: Add Supabase Auth and basic user management to an existing **React 19+** app (Vite-based) with **Tailwind v4**.  
> **Out of scope**: Next.js specifics (create a separate guide later), server frameworks, and non‑auth Supabase modules beyond small notes.

## User-Provided Concept
*(Preserved. Populate here if the PM provides one later.)*

---

## 1) Why this slice & constraints
- We need email/password, magic link, and OAuth sign-in; sessions persist and react to changes in real time.
- Must integrate without taking over routing, layout, or styling.
- Works with React Router or any router; **no Next.js assumptions**. fileciteturn1file4 fileciteturn1file3
- Follow our slice-based docs when turning this guide into tasks. fileciteturn1file6 fileciteturn1file5

---

## 2) Supabase project setup
1. Create a Supabase project in the dashboard.
2. Copy **Project URL** and **Anon (Publishable) Key** from **Settings → API**.
3. Add environment vars to the Vite app:

```bash
# .env (never commit secrets; .env should be gitignored)
VITE_SUPABASE_URL=https://YOUR-PROJECT.supabase.co
VITE_SUPABASE_ANON_KEY=YOUR-PUBLISHABLE-KEY
```

> Notes  
> - Only use the **anon/publishable** key in the browser; **never** the service role key.  
> - RLS guards actual access on the server; client key is not privileged.

---

## 3) Install dependencies

```bash
pnpm add @supabase/supabase-js
```

> Keep TypeScript strict; avoid `any`. fileciteturn1file11

---

## 4) Create a singleton Supabase client

**src/lib/supabaseClient.ts**
```ts
import { createClient } from '@supabase/supabase-js'

const url = import.meta.env.VITE_SUPABASE_URL
const anon = import.meta.env.VITE_SUPABASE_ANON_KEY

if (!url || !anon) {
  throw new Error('Missing Supabase env vars (VITE_SUPABASE_URL / VITE_SUPABASE_ANON_KEY)')
}

export const supabase = createClient(url, anon, {
  auth: {
    persistSession: true,
    autoRefreshToken: true,
    detectSessionInUrl: true,
  },
})
```

> Keep this module outside of React render paths to avoid duplicate subscriptions.

---

## 5) Session hook (framework-neutral)

**src/hooks/useSupabaseAuth.ts**
```ts
import { useEffect, useState } from 'react'
import type { Session, User } from '@supabase/supabase-js'
import { supabase } from '@/lib/supabaseClient'

type UseSupabaseAuth = {
  session: Session | null
  user: User | null
  loading: boolean
}

export function useSupabaseAuth(): UseSupabaseAuth {
  const [session, setSession] = useState<Session | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let isMounted = true

    supabase.auth.getSession().then(({ data: { session } }) => {
      if (!isMounted) return
      setSession(session ?? null)
      setLoading(false)
    })

    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session ?? null)
    })

    return () => {
      isMounted = false
      subscription?.unsubscribe()
    }
  }, [])

  return { session, user: session?.user ?? null, loading }
}
```

---

## 6) Optional Auth context (for convenience)

**src/contexts/AuthContext.tsx**
```tsx
import { createContext, useContext, ReactNode } from 'react'
import { useSupabaseAuth } from '@/hooks/useSupabaseAuth'

type AuthValue = ReturnType<typeof useSupabaseAuth>

const AuthCtx = createContext<AuthValue | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const auth = useSupabaseAuth()
  return <AuthCtx.Provider value={auth}>{children}</AuthCtx.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthCtx)
  if (!ctx) throw new Error('useAuth must be used within <AuthProvider>')
  return ctx
}
```

Wrap your app root (e.g., `<Router>`) with `<AuthProvider>`.

---

## 7) Route guards (React Router example)

**src/components/auth/RequireAuth.tsx**
```tsx
import { Navigate, useLocation } from 'react-router-dom'
import { useAuth } from '@/contexts/AuthContext'

export function RequireAuth({ children }: { children: JSX.Element }) {
  const { user, loading } = useAuth()
  const location = useLocation()

  if (loading) return null // or a spinner

  if (!user) {
    return <Navigate to="/login" replace state={{ from: location }} />
  }
  return children
}
```

Usage:
```tsx
// inside your routes
<Route
  path="/dashboard"
  element={
    <RequireAuth>
      <DashboardPage />
    </RequireAuth>
  }
/>
```

---

## 8) UI options

### A) Prebuilt (fastest for prototypes)
```tsx
import { Auth } from '@supabase/auth-ui-react'
import { ThemeSupa } from '@supabase/auth-ui-shared'
import { supabase } from '@/lib/supabaseClient'

<Auth supabaseClient={supabase} appearance={{ theme: ThemeSupa }} providers={['github', 'google']} />
```
Good for speed; not ideal for production UX.

### B) Custom forms (recommended)
```ts
// Email/password
await supabase.auth.signInWithPassword({ email, password })

// Magic link
await supabase.auth.signInWithOtp({ email, options: { emailRedirectTo: `${location.origin}/auth/callback` } })

// OAuth
await supabase.auth.signInWithOAuth({ provider: 'github', options: { redirectTo: `${location.origin}/auth/callback` } })

// Sign out
await supabase.auth.signOut()
```

> Configure **Auth → URL Configuration** (redirects) in the Supabase dashboard for magic link/OAuth callbacks to your app URLs.

---

## 9) Profiles table, RLS, and automatic provisioning

Never write to `auth.users` directly. Use a 1:1 `profiles` table.

```sql
create table if not exists public.profiles (
  id uuid primary key references auth.users on delete cascade,
  display_name text,
  avatar_url text,
  created_at timestamptz default now()
);

alter table public.profiles enable row level security;

create policy "read own profile" on public.profiles
for select using (auth.uid() = id);

create policy "update own profile" on public.profiles
for update using (auth.uid() = id);
```

Auto-create profile rows on signup (database trigger):

```sql
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
as $$
begin
  insert into public.profiles (id) values (new.id)
  on conflict (id) do nothing;
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
after insert on auth.users
for each row execute procedure public.handle_new_user();
```

Client upsert example:
```ts
await supabase.from('profiles').upsert({ id: user.id, display_name: name })
```

---

## 10) Email flows, MFA, and SSO (notes)
- **Password reset**: call `supabase.auth.resetPasswordForEmail(email, { redirectTo: `${location.origin}/auth/reset` })` and implement a reset page that calls `updateUser({ password })`.
- **MFA (TOTP)** and **SSO (SAML)** are supported by Supabase on certain tiers; integrate later if required. Keep UI and routes ready to extend.

---

## 11) Storage (avatars) & Realtime (optional)
- Storage bucket `avatars`: store public URLs and write them into `profiles.avatar_url`.
- Realtime (presence/changes): `supabase.channel(...).on('postgres_changes', ...)` scoped by user id for per-user streams.

---

## 12) Security & hardening checklist
- [ ] Only publish **anon** key to client; never service role in browser.
- [ ] RLS enabled and policies tested early (use SQL editor to verify denied/allowed).
- [ ] Configure allowed redirect URLs for OAuth/magic link (**Auth → URL Configuration**).
- [ ] Validate and sanitize form inputs (Zod + react-hook-form recommended). fileciteturn1file10
- [ ] Never silently fallback envs—throw on missing config (see client factory). fileciteturn1file8
- [ ] Log out clears cached state and navigates to a public route.

---

## 13) Developer UX & patterns (house style)
- React function components, small and typed. Tailwind v4 utilities in CSS (no tailwind.config). fileciteturn1file10
- Prefer local state/hooks; if you add server state, use TanStack Query. fileciteturn1file10
- Keep files/components under 300/50 lines where possible. fileciteturn1file8
- Use `pnpm` and run `pnpm build` to verify after changes. fileciteturn1file10

---

## 14) Minimal pages/components to add

```
src/
  lib/supabaseClient.ts
  hooks/useSupabaseAuth.ts
  contexts/AuthContext.tsx
  components/auth/RequireAuth.tsx
  pages/LoginPage.tsx             # uses custom form or Auth UI
  pages/AuthCallbackPage.tsx      # handles oauth/magic-link redirects
  pages/ResetPasswordPage.tsx     # optional
```

**LoginPage.tsx** (sketch)
```tsx
import { useState } from 'react'
import { supabase } from '@/lib/supabaseClient'
import { useAuth } from '@/contexts/AuthContext'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const { user } = useAuth()

  async function onPasswordLogin(e: React.FormEvent) {
    e.preventDefault()
    const { error } = await supabase.auth.signInWithPassword({ email, password })
    if (error) {
      // toast.error(error.message)
      return
    }
    // navigate to dashboard
  }

  return (
    <form onSubmit={onPasswordLogin} className="max-w-sm space-y-3">
      <input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="you@example.com" className="input" />
      <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="••••••••" className="input" />
      <button className="btn">Sign in</button>
    </form>
  )
}
```

---

## 15) Testing & verification
- [ ] **Happy path**: register/login → protected route renders.
- [ ] **Guarding**: unauthenticated users redirected to `/login`.
- [ ] **Auth changes**: sign-out updates UI without full reload.
- [ ] **RLS**: profile read/update allowed only for self; denied for other `id`s.
- [ ] **Callbacks**: OAuth/magic-link flows return to app successfully.
- [ ] **Env**: app throws early if env vars missing.

Use our code review checklist during PRs. fileciteturn1file7 fileciteturn1file9

---

## 16) Turn this guide into tasks (Phase 5→6)
When ready to execute, convert this guide to a task file with granular checklists and success criteria following our **Phase 5/6** playbooks. fileciteturn1file2 fileciteturn1file1

**Success definition for the slice**
- Users can sign up/sign in/out with email & OAuth.
- Protected routes gated; session persists & reacts to changes.
- `profiles` table created with RLS + trigger; CRUD for own profile works.
- Redirects configured; flows verified.
- Basic tests/checklist above pass.

---