---
layer: tool-guide
tool: Electron
docType: guide
description: Testing strategies for Electron apps - unit testing services, mocking IPC, testing React components
dependsOn: [01-architecture.md, 02-project-structure.md]
dateCreated: 20260213
dateUpdated: 20260213
---

# Electron Testing Guide

Testing Electron apps is tricky because code runs in different processes with different capabilities. This guide provides practical strategies that work without heavyweight E2E frameworks.

## Testing Philosophy

The key insight: **most of your code doesn't need Electron to be tested.** If you follow the architecture guide's process-agnostic service layer pattern, the majority of your business logic runs as plain TypeScript/Node.js code. The Electron-specific parts (IPC wiring, preload bridge, window management) are thin glue code where type safety provides more value than unit tests.

### Testing Pyramid for Electron

```
        ╱ ╲
       ╱ E2E ╲          Rarely needed. Manual testing + typed IPC
      ╱───────╲          contract catches most integration bugs.
     ╱  IPC    ╲         Optional integration tests for complex
    ╱  Flows    ╲        multi-step IPC workflows.
   ╱─────────────╲
  ╱   Services    ╲      High value. Unit test all business logic.
 ╱   + Components  ╲     Mock dependencies, no Electron needed.
╱───────────────────╲
```

**Invest heavily in**: Service unit tests, React component tests.
**Invest selectively in**: IPC integration tests for complex flows.
**Avoid unless necessary**: Full E2E tests with Playwright/Spectron.


## Setup: Vitest Configuration

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',    // For React component tests
    include: ['tests/**/*.test.{ts,tsx}'],
    exclude: ['node_modules', 'out', 'dist'],
    coverage: {
      provider: 'v8',
      include: ['src/main/services/**', 'src/components/**', 'src/hooks/**', 'src/lib/**'],
      exclude: ['src/main/ipc/**', 'src/preload/**']  // Glue code, not worth covering
    }
  }
})
```

### Why jsdom?

Most tests are either pure Node.js (services) or React components. The `jsdom` environment handles both. Pure Node.js tests ignore the DOM environment; React tests need it. This avoids maintaining separate configs.


## Unit Testing: Services

Services are the highest-value test target. They contain business logic and, if following the architecture guide, have no Electron dependency.

### Testing a Service with Injected Dependencies

```typescript
// tests/unit/services/storage-service.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { StorageService } from '../../../src/main/services/storage-service'

// Mock the filesystem dependency
const mockFs = {
  readFile: vi.fn(),
  writeFile: vi.fn(),
  exists: vi.fn(),
}

describe('StorageService', () => {
  let service: StorageService

  beforeEach(() => {
    vi.clearAllMocks()
    service = new StorageService(mockFs, '/fake/storage/path')
  })

  it('reads and parses a JSON file', async () => {
    mockFs.readFile.mockResolvedValue('{"projects": [{"name": "Test"}]}')

    const result = await service.read('projects.json')

    expect(result.success).toBe(true)
    expect(JSON.parse(result.data!)).toEqual({ projects: [{ name: 'Test' }] })
    expect(mockFs.readFile).toHaveBeenCalledWith('/fake/storage/path/projects.json')
  })

  it('returns error for missing files', async () => {
    mockFs.readFile.mockRejectedValue(new Error('ENOENT: no such file'))

    const result = await service.read('missing.json')

    expect(result.success).toBe(false)
    expect(result.error).toContain('ENOENT')
  })

  it('validates JSON before writing', async () => {
    const result = await service.write('data.json', 'not valid json{{{')

    expect(result.success).toBe(false)
    expect(mockFs.writeFile).not.toHaveBeenCalled()
  })

  it('creates backup before overwriting', async () => {
    mockFs.exists.mockResolvedValue(true)
    mockFs.writeFile.mockResolvedValue(undefined)

    await service.write('projects.json', '{"valid": true}')

    // Verify backup was created before write
    const calls = mockFs.writeFile.mock.calls
    // Implementation-specific: check backup logic
  })
})
```

### Testing Services That Currently Import Electron

If a service directly imports from `electron` (e.g., uses `app.getPath()`), that's a sign the architecture needs refactoring. Extract the Electron dependency:

```typescript
// ❌ Hard to test — imports electron
import { app } from 'electron'

export class StorageService {
  private basePath = app.getPath('userData')
  // ...
}

// ✅ Easy to test — dependency injected
export class StorageService {
  constructor(private readonly basePath: string) {}
  // ...
}

// Wire up in main.ts or ipc handler:
const service = new StorageService(app.getPath('userData'))
```

This is the single most important refactoring pattern for testability in Electron apps.


## Unit Testing: React Components

React components in Electron apps are standard React components. Test them the same way you would in any React app.

### Mocking window.electronAPI

The renderer calls the main process through `window.electronAPI`. Mock this global:

```typescript
// tests/helpers/mock-electron-api.ts
export function mockElectronAPI(overrides = {}) {
  const defaultApi = {
    storageRead: vi.fn().mockResolvedValue({ success: true, data: '{}' }),
    storageWrite: vi.fn().mockResolvedValue({ success: true }),
    getAppVersion: vi.fn().mockResolvedValue('1.0.0'),
    updateWindowTitle: vi.fn().mockResolvedValue(undefined),
  }

  Object.defineProperty(window, 'electronAPI', {
    value: { ...defaultApi, ...overrides },
    writable: true,
    configurable: true,
  })

  return window.electronAPI
}
```

### Testing a Component That Uses IPC

```typescript
// tests/unit/components/project-selector.test.tsx
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, beforeEach } from 'vitest'
import { mockElectronAPI } from '../../helpers/mock-electron-api'
import { ProjectSelector } from '../../../src/components/ProjectSelector'

describe('ProjectSelector', () => {
  beforeEach(() => {
    mockElectronAPI({
      storageRead: vi.fn().mockResolvedValue({
        success: true,
        data: JSON.stringify({
          projects: [
            { name: 'Project A', template: 'react' },
            { name: 'Project B', template: 'electron' },
          ]
        })
      })
    })
  })

  it('loads and displays projects', async () => {
    render(<ProjectSelector />)

    await waitFor(() => {
      expect(screen.getByText('Project A')).toBeInTheDocument()
      expect(screen.getByText('Project B')).toBeInTheDocument()
    })
  })

  it('calls storage write when project is selected', async () => {
    render(<ProjectSelector />)

    await waitFor(() => screen.getByText('Project A'))
    await userEvent.click(screen.getByText('Project A'))

    expect(window.electronAPI.storageWrite).toHaveBeenCalled()
  })
})
```

### Mocking Renderer Service Wrappers (Preferred)

If using the renderer service wrapper pattern from the project structure guide, mock the wrapper instead of `window.electronAPI` directly:

```typescript
// tests/unit/components/project-selector.test.tsx
vi.mock('../../../src/services/storage', () => ({
  storageService: {
    readProjects: vi.fn().mockResolvedValue([
      { name: 'Project A', template: 'react' },
    ]),
    saveProjects: vi.fn().mockResolvedValue(undefined),
  }
}))
```

This is cleaner because tests don't need to know about IPC result formats (`{ success, data }` wrapping).


## Unit Testing: Custom Hooks

Hooks that wrap IPC calls are testable with `@testing-library/react-hooks` (or `renderHook` from `@testing-library/react` v14+):

```typescript
// tests/unit/hooks/use-projects.test.ts
import { renderHook, waitFor } from '@testing-library/react'
import { useProjects } from '../../../src/hooks/useProjects'
import { mockElectronAPI } from '../../helpers/mock-electron-api'

describe('useProjects', () => {
  beforeEach(() => {
    mockElectronAPI({
      storageRead: vi.fn().mockResolvedValue({
        success: true,
        data: JSON.stringify({ projects: [{ name: 'Test' }] })
      })
    })
  })

  it('loads projects on mount', async () => {
    const { result } = renderHook(() => useProjects())

    await waitFor(() => {
      expect(result.current.projects).toHaveLength(1)
      expect(result.current.projects[0].name).toBe('Test')
    })
  })
})
```


## Integration Testing: IPC Flows (Optional)

For complex multi-step IPC workflows, you may want integration tests that verify the full flow without Electron. The approach: test the IPC handler + service together, mocking only the system boundary (filesystem, network).

```typescript
// tests/integration/storage-flow.test.ts
import { describe, it, expect, vi } from 'vitest'
import { StorageService } from '../../src/main/services/storage-service'

// This tests the service logic that the IPC handler delegates to.
// If the handler is a thin adapter (as it should be), this effectively
// tests the IPC flow without needing Electron.

describe('Storage flow: read → modify → write', () => {
  it('reads, modifies, and writes back with backup', async () => {
    const files: Record<string, string> = {
      'projects.json': JSON.stringify({ projects: [{ name: 'Original' }] })
    }

    const mockFs = {
      readFile: vi.fn((path: string) => Promise.resolve(files[path.split('/').pop()!])),
      writeFile: vi.fn((path: string, data: string) => {
        files[path.split('/').pop()!] = data
        return Promise.resolve()
      }),
      exists: vi.fn(() => Promise.resolve(true)),
      copyFile: vi.fn((src: string, dest: string) => {
        files[dest.split('/').pop()!] = files[src.split('/').pop()!]
        return Promise.resolve()
      }),
    }

    const service = new StorageService(mockFs, '/storage')

    // Read
    const readResult = await service.read('projects.json')
    expect(readResult.success).toBe(true)

    // Modify
    const data = JSON.parse(readResult.data!)
    data.projects.push({ name: 'New Project' })

    // Write
    const writeResult = await service.write('projects.json', JSON.stringify(data))
    expect(writeResult.success).toBe(true)

    // Verify
    const verifyResult = await service.read('projects.json')
    const parsed = JSON.parse(verifyResult.data!)
    expect(parsed.projects).toHaveLength(2)
  })
})
```


## What NOT to Test (and Why)

### Preload Bridge

The preload script is pure glue code: it calls `contextBridge.exposeInMainWorld` and maps method names to `ipcRenderer.invoke` calls. If you're using a typed IPC contract, TypeScript catches mismatches at compile time. Testing this manually is sufficient.

### IPC Handler Registration Order

The fact that `ipcMain.handle('channel', handler)` works is an Electron guarantee. Test the handler logic (via the service), not the registration mechanism.

### Window Creation / App Lifecycle

Testing `createWindow()`, `app.whenReady()`, menus, and CSP headers requires a running Electron instance. This is E2E territory. For solo/small-team projects, manual testing of these paths is more practical than automated E2E.

### E2E with Playwright / Spectron

Full E2E testing for Electron is high-cost, high-maintenance, and provides diminishing returns for most projects. Consider it only if:
- The app is distributed commercially with many users
- Critical user flows involve complex multi-step interactions
- You've had recurring regression bugs that unit tests couldn't catch

For most developer tools and personal productivity apps, the combination of typed IPC contracts + service unit tests + component tests + manual testing provides sufficient confidence.


## Test File Organization

```
tests/
├── helpers/
│   ├── mock-electron-api.ts     # Shared electronAPI mock
│   └── test-fixtures.ts         # Shared test data
├── unit/
│   ├── services/                # Mirror src/main/services/
│   │   ├── storage-service.test.ts
│   │   └── context/
│   │       ├── statement-manager.test.ts
│   │       └── prompt-parser.test.ts
│   ├── components/              # Mirror src/components/
│   │   └── project-selector.test.tsx
│   └── hooks/                   # Mirror src/hooks/
│       └── use-projects.test.ts
└── integration/                 # Cross-layer flows
    └── storage-flow.test.ts
```

Mirror the source directory structure in tests. This makes it obvious which test covers which source file.

---

## Version History

- **2026-02-13** — Initial guide: testing philosophy, service tests, component tests, integration patterns
