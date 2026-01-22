---
layer: tool-guide
tool: shadcn
docType: setup
audience:
  - human
  - ai
description: Setup, configuration, and process (CI) details for use with ShadCN project.
dependsOn: [./introduction]
---

## Getting Started

This section is phase‑4 (“design → detailed breakdown”) and presumes the high‑level **introduction** is already clear.  Use it any time a new repo or sub‑site needs a shadcn‑powered UI on Next .js.

####  Prerequisites (once per workstation)

| Tool | Minimum version | Install |
|------|-----------------|---------|
| **Node.js** | 20 .x LTS | <https://nodejs.org> |
| **pnpm** | 9 .x | `npm i -g pnpm` |
| **Git** | 2.4+ | <https://git-scm.com> |
| **VS Code** | latest | + Extensions: ESLint, Prettier, Tailwind CSS IntelliSense |

```bash
# Confirm versions
node -v      # → 20.x
pnpm -v      # → 9.x
git --version
```


#### Repo Bootstrap

1.  Create the project
```sh
pnpm create next-app mysite.com --template app-router --eslint --tailwind \
  --ts --use-pnpm
```

2. Add shadcn-ui
```sh
npx shadcn-ui@latest init
# ? Which style — default → "New York"
# ? Use TypeScript → yes
# ? Enable RSC / App Router → yes
# ? Global CSS path → app/globals.css
```

3. Scaffold first components
```sh
npx shadcn-ui add card button
```


#### Project Baseline Configuration

1. Tailwind brand tokens (`tailwind.config.ts`).  Make sure to keep tokens in `src/ui/theme.ts` when extracting common themes.
   
```ts
export const theme = {
  extend: {
    colors: {
      primary: '#ff2e2e', // chair‑red
      accent:  '#15b0a8', // Tahoe‑teal
    },
  },
};
```

2. ESLint + Prettier
```sh
# Referenced in rules/, this provides additional detail.
pnpm add -D prettier eslint-config-prettier
echo '{ "extends": ["next/core-web-vitals","prettier"] }' > .eslintrc.json
```

3. TS Strict Mode
```json
{
  "compilerOptions": {
    "strict": true,
    "forceConsistentCasingInFileNames": true
  }
}
```   

#### Starter Content and Pages

1. Add content layer for blog sites (if applicable)
```sh
pnpm add contentlayer @next/mdx
pnpm dlx contentlayer init
```

2. Example starter page (assumes bento style)
```tsx
// app/(site)/page.tsx (snippet)
export default function Home() {
  return (
    <main className="grid grid-cols-4 gap-4 p-6">
      <Card className="col-span-4 md:col-span-2 lg:col-span-2">
        {/* Hero / latest video */}
      </Card>
      {/* More cards */}
    </main>
  );
}
```

#### Testing
Testing should be added to the project if not already configured.  Ideally this should be integrated with CI pipeline.  Github is assumed.

```sh
pnpm add -D vitest @testing-library/react @testing-library/jest-dom jsdom \
	happy-dom
```

`.github/workflows/ci.yml`
```yaml
name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
        with: { version: 9 }
      - run: pnpm install --frozen-lockfile
      - run: pnpm lint && pnpm type-check && pnpm test --run
      - run: pnpm build
```
