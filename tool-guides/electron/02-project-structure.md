---
layer: tool-guide
tool: Electron
docType: guide
description: Canonical project structure, file placement rules, and the IPC workflow for adding new backend capabilities
dependsOn: [00-introduction.md, 01-architecture.md]
dateCreated: 20260213
dateUpdated: 20260213
---

# Electron Project Structure Guide

This guide defines the canonical file layout for Electron applications and the step-by-step workflow for common structural changes. It is designed so that both human developers and AI agents can determine exactly where to place new code without ambiguity.

## Canonical Project Structure

```
{project-root}/
├── src/
│   ├── main/                    # Main process (Node.js runtime)
│   │   ├── main.ts              # App lifecycle: window creation, menu, CSP, single-instance lock
│   │   ├── ipc/                 # IPC handler registration (thin adapters to services)
│   │   │   ├── storage.ts       # Handlers for storage:* channels
│   │   │   └── context.ts       # Handlers for context service channels
│   │   └── services/            # Business logic (process-agnostic, no Electron imports)
│   │       ├── storage-service.ts
│   │       └── context/
│   │           ├── statement-manager.ts
│   │           └── prompt-parser.ts
│   │
│   ├── preload/                 # Bridge between main and renderer
│   │   └── preload.cts          # contextBridge.exposeInMainWorld (CJS required)
│   │
│   ├── renderer/                # Renderer process entry
│   │   └── index.html           # HTML entry point for Chromium
│   │
│   ├── shared/                  # Types and contracts shared across ALL processes
│   │   ├── ipc-contract.ts      # IPC channel definitions (THE source of truth)
│   │   ├── ipc-helpers.ts       # Type-safe invoke/handle wrappers
│   │   └── types/               # Shared domain types
│   │       └── project.ts
│   │
│   ├── components/              # React components (renderer-only)
│   ├── features/                # Feature modules (renderer-only)
│   ├── hooks/                   # React hooks (renderer-only)
│   ├── pages/                   # Page-level components (renderer-only)
│   ├── services/                # Renderer-side service wrappers (call window.electronAPI)
│   ├── lib/                     # Renderer-side utilities
│   │
│   ├── App.tsx                  # React root component
│   ├── index.css                # Global styles (Tailwind entry)
│   └── vite-env.d.ts            # Vite type declarations
│
├── tests/                       # Test files
│   ├── unit/                    # Unit tests (services, utilities)
│   │   └── services/            # Mirror src/main/services/ structure
│   └── integration/             # Integration tests (IPC flows)
│
├── electron.vite.config.ts      # Build config for main, preload, and renderer
├── package.json
├── tsconfig.json
└── vitest.config.ts
```

## File Placement Rules

These rules are the decision matrix for "where does this code go?" Follow them in order.

### Rule 1: What Process Does It Run In?

| If the code... | It goes in... |
|----------------|---------------|
| Uses `electron` APIs (BrowserWindow, app, ipcMain, dialog, shell, Menu) | `src/main/` |
| Uses `contextBridge` or `ipcRenderer` | `src/preload/` |
| Is a React component, hook, or UI logic | `src/components/`, `src/pages/`, `src/hooks/`, `src/features/` |
| Is a type or interface used by BOTH main and renderer | `src/shared/` |
| Is business logic with NO Electron dependency | `src/main/services/` (runs in main, but portable) |

### Rule 2: Main Process Subdirectory

| If the main-process code... | It goes in... |
|-----------------------------|---------------|
| Registers IPC handlers | `src/main/ipc/` |
| Contains business logic (parsing, validation, data management) | `src/main/services/` |
| Manages app lifecycle (windows, menus, CSP, startup) | `src/main/main.ts` |

### Rule 3: Is It a Service or an IPC Handler?

This is the most common point of confusion. The distinction:

**IPC handler** (`src/main/ipc/`): Thin adapter that receives IPC calls and delegates to a service. Should be 2-5 lines per handler. Contains NO business logic.

```typescript
// src/main/ipc/storage.ts — THIS IS AN IPC HANDLER
handleIpc('storage:read', (filename) => storageService.read(filename))
```

**Service** (`src/main/services/`): Business logic that does the actual work. Does NOT import from `electron`. Takes injected dependencies.

```typescript
// src/main/services/storage-service.ts — THIS IS A SERVICE
export class StorageService {
  constructor(private readonly basePath: string) {}
  
  async read(filename: string): Promise<StorageResult> {
    // Actual logic: validation, reading, error recovery
  }
}
```

**Why this matters**: Services are testable without Electron, portable to other runtimes, and clear about their responsibilities. IPC handlers are glue code.

### Rule 4: Shared Types

Any type, interface, or enum referenced by both main and renderer code belongs in `src/shared/`. Never duplicate a type definition across process boundaries.

Common shared types:
- IPC contract (channel definitions, argument types, return types)
- Domain models (Project, Statement, Configuration)
- Enums and constants used cross-process

**Exception**: Types used only within one process stay in that process's directory.


## The IPC Workflow: Adding a New Backend Capability

This is the most common structural change in Electron development and the most error-prone for AI agents. Follow these steps exactly, in order.

### Step-by-Step Checklist

When you need to add a new capability that the renderer needs from the main process:

**Step 1: Define the contract** in `src/shared/ipc-contract.ts`

```typescript
// Add to IpcContract interface
'projects:scan': {
  args: [projectPath: string]
  return: { files: string[]; error?: string }
}
```

**Step 2: Implement the service** in `src/main/services/`

Create or update the relevant service. The service must NOT import from `electron`.

```typescript
// src/main/services/project-scanner.ts
export class ProjectScanner {
  async scanDirectory(projectPath: string): Promise<string[]> {
    // Pure Node.js logic: readdir, filter, etc.
  }
}
```

**Step 3: Register the IPC handler** in `src/main/ipc/`

Create or update the relevant IPC file. Handler delegates to service.

```typescript
// src/main/ipc/projects.ts
import { handleIpc } from '../../shared/ipc-helpers'
import { projectScanner } from '../services/project-scanner'

handleIpc('projects:scan', async (projectPath) => {
  try {
    const files = await projectScanner.scanDirectory(projectPath)
    return { files }
  } catch (error) {
    return { files: [], error: error.message }
  }
})
```

**Step 4: Wire up IPC registration** in `src/main/main.ts`

Ensure the IPC file is imported and called during app initialization. IPC handlers must be registered ONCE, GLOBALLY — never inside `createWindow()`.

```typescript
// src/main/main.ts
import { setupProjectHandlers } from './ipc/projects'

app.whenReady().then(() => {
  setupProjectHandlers()  // Register before createWindow
  createWindow()
})
```

**Step 5: Expose in preload** in `src/preload/preload.cts`

```typescript
contextBridge.exposeInMainWorld('electronAPI', {
  // ...existing methods...
  scanProjects: (path: string) => ipcRenderer.invoke('projects:scan', path),
})
```

**Step 6: Add type declaration** for `window.electronAPI`

```typescript
// src/shared/types/electron-api.d.ts (or in vite-env.d.ts)
interface ElectronAPI {
  // ...existing...
  scanProjects: (path: string) => Promise<{ files: string[]; error?: string }>
}

interface Window {
  electronAPI: ElectronAPI
}
```

**Step 7: Call from renderer**

```typescript
// Any React component
const result = await window.electronAPI.scanProjects('/path/to/project')
```

### Common Mistakes (AI Agent Checklist)

Before submitting changes that involve IPC:

- [ ] **Channel name matches everywhere**: Contract, handler registration, preload, and any renderer calls all use the same string
- [ ] **Handler registered globally**: Not inside `createWindow()` or any function called per-window
- [ ] **Preload is CJS**: File uses `.cts` extension or `require()` syntax, not ESM `import`
- [ ] **No Electron imports in services**: Services in `src/main/services/` must not `import` from `electron`
- [ ] **No Node.js in renderer**: Components don't import `fs`, `path`, `child_process`, etc.
- [ ] **Type declaration updated**: `window.electronAPI` type includes the new method
- [ ] **Return types match**: What the handler returns matches what the contract and type declaration promise


## Renderer-Side Organization

The renderer side is a standard React application. These directories follow common React conventions:

| Directory | Contains | Notes |
|-----------|----------|-------|
| `src/components/` | Reusable UI components | Buttons, cards, form elements. No IPC calls. |
| `src/features/` | Feature modules | May contain components, hooks, and logic grouped by feature |
| `src/pages/` | Page-level components | Top-level routes or views |
| `src/hooks/` | Custom React hooks | Including hooks that wrap `window.electronAPI` calls |
| `src/services/` | Renderer-side service wrappers | Thin wrappers around `window.electronAPI` for cleaner imports |
| `src/lib/` | Utilities | Formatters, validators, constants — no Electron dependency |

### Renderer Service Wrappers

For cleaner imports and easier mocking in tests, wrap `window.electronAPI` calls:

```typescript
// src/services/storage.ts
export const storageService = {
  async readProjects(): Promise<Project[]> {
    const result = await window.electronAPI.storageRead('projects.json')
    if (!result.success) throw new Error(result.error)
    return JSON.parse(result.data!)
  },

  async saveProjects(projects: Project[]): Promise<void> {
    const data = JSON.stringify(projects, null, 2)
    const result = await window.electronAPI.storageWrite('projects.json', data)
    if (!result.success) throw new Error(result.error)
  }
}
```

This keeps React components clean — they call `storageService.readProjects()` instead of dealing with raw IPC results and JSON parsing.


## electron-vite Build Targets

When using `electron-vite` (recommended toolchain), the build configuration in `electron.vite.config.ts` defines three separate build targets:

```typescript
// electron.vite.config.ts
export default defineConfig({
  main: {
    // Builds src/main/ → out/main/
    // Node.js target, CJS or ESM output
    build: { rollupOptions: { external: ['electron'] } }
  },
  preload: {
    // Builds src/preload/ → out/preload/
    // Node.js target, MUST be CJS for contextIsolation
    build: { rollupOptions: { external: ['electron'] } }
  },
  renderer: {
    // Builds src/renderer/ (and everything it imports from src/) → out/renderer/
    // Browser target, standard Vite/React build
    root: '.',  // or 'src/renderer/' depending on setup
    build: { rollupOptions: { input: 'index.html' } }
  }
})
```

**Key understanding**: The renderer build includes everything imported from `src/components/`, `src/features/`, `src/hooks/`, etc. — the build target is defined by the entry point (`index.html` → `App.tsx` → all imports), not by directory location.

**The `shared/` directory** is special: its files are imported by BOTH the main and renderer builds. TypeScript types are erased at build time (zero runtime cost), but any runtime code in `shared/` will be bundled into both outputs.


## Testing Strategy

### Unit Tests: Services (No Electron Required)

The process-agnostic service layer is straightforward to test:

```typescript
// tests/unit/services/storage-service.test.ts
import { StorageService } from '../../../src/main/services/storage-service'

const mockFs = {
  readFile: vi.fn(),
  writeFile: vi.fn(),
  exists: vi.fn(),
}

describe('StorageService', () => {
  it('reads and parses JSON files', async () => {
    mockFs.readFile.mockResolvedValue('{"projects": []}')
    const service = new StorageService(mockFs, '/fake/path')
    const result = await service.read('projects.json')
    expect(result.success).toBe(true)
  })
})
```

### Unit Tests: React Components (No Electron Required)

Mock `window.electronAPI` or use the renderer service wrappers:

```typescript
// tests/unit/components/project-list.test.tsx
vi.mock('../../../src/services/storage', () => ({
  storageService: {
    readProjects: vi.fn().mockResolvedValue([{ name: 'Test Project' }]),
  }
}))
```

### Integration Tests: IPC Flows

Testing actual IPC requires either Electron test runners (heavy) or mocking the IPC layer. For most projects, thorough unit tests on services + manual testing of IPC wiring is the pragmatic approach.

### What NOT to Over-Test

- **Preload bridge**: It's glue code. If the types match and the channel strings match, it works. TypeScript + the shared contract catches most errors at compile time.
- **E2E with Playwright/Spectron**: High maintenance cost, low incremental value for solo/small-team projects. Reserve for critical user flows if needed.


## Migration Notes

### Migrating Existing Apps to This Structure

If you have an Electron app with IPC handlers defined directly in `main.ts`:

1. **Extract services first**: Move business logic from handlers into `src/main/services/`. This is the highest-value refactor.
2. **Create the shared contract**: Define `src/shared/ipc-contract.ts` based on existing channel names.
3. **Create IPC adapter files**: Move handler registrations from `main.ts` to `src/main/ipc/` files that delegate to services.
4. **Move global handler registration**: Ensure all `ipcMain.handle()` calls happen before `createWindow()`.

This can be done incrementally — migrate one service domain at a time (storage, then context, then application, etc.).


## Quick Reference: Where Does This Go?

| I need to... | Create/modify file in... |
|--------------|--------------------------|
| Add a new IPC channel | `src/shared/ipc-contract.ts` → `src/main/services/` → `src/main/ipc/` → `src/preload/preload.cts` → type declaration |
| Add a React component | `src/components/` or `src/features/{feature}/` |
| Add a page/view | `src/pages/` |
| Add a React hook | `src/hooks/` |
| Add a shared type | `src/shared/types/` |
| Add business logic | `src/main/services/` (even if only main process uses it now) |
| Add a utility function | `src/lib/` (renderer) or `src/main/services/` (main) |
| Add a native Electron feature (dialog, menu, tray) | `src/main/main.ts` or a dedicated file in `src/main/` |
| Add a test | `tests/unit/` mirroring the source structure |

---

## Version History

- **2026-02-13** — Initial guide: canonical structure, file placement rules, IPC workflow, testing strategy
