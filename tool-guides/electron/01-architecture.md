---
layer: tool-guide
tool: Electron
docType: guide
description: Architectural patterns, IPC design, service layering, and state management for Electron applications
dependsOn: [00-introduction.md]
dateCreated: 20250117
dateUpdated: 20260213
---

# Electron Architecture Guide

This guide covers architectural patterns for building maintainable Electron applications. It addresses the core challenge of Electron development: managing the boundary between two processes (main and renderer) that function as a single application.

## The Lichen Pattern

Electron combines a Node.js backend (main process) and a Chromium frontend (renderer process) into one application — a symbiotic relationship between two different runtimes functioning as a single organism. While this provides excellent UX (native desktop app with web technologies), it introduces architectural complexity that must be deliberately managed.

**The core challenge:** Every backend capability requires coordination across three files (main handler, preload exposure, renderer call). Every bug can exist in either process with different debugging tools. Every AI agent working on the code must understand which process they're modifying and why.

**The mitigation strategy:** Minimize the surface area of the process boundary, type it rigorously, and keep business logic process-agnostic so it can be tested and potentially reused outside Electron.


## Typed IPC Contract

The single highest-impact architectural pattern for Electron apps. Instead of string-based IPC channels scattered across files, define a single shared contract that both processes reference.

### The Problem

Typical Electron IPC is stringly-typed and scattered:

```typescript
// main.ts - handler defined here
ipcMain.handle('storage:read', async (_, filename: string) => { ... })

// preload.ts - string repeated here
contextBridge.exposeInMainWorld('electronAPI', {
  readFile: (path: string) => ipcRenderer.invoke('storage:read', path)
})

// renderer component - called here, hoping types match
const data = await window.electronAPI.readFile('/some/path')
```

Problems with this approach:
- Channel names are strings with no compile-time checking
- Argument and return types are implicit, not enforced
- Adding a new channel means updating three files with matching strings
- AI agents frequently introduce mismatches between handler and caller
- Refactoring a channel name requires find-and-replace across the codebase

### The Solution: Shared Contract

Define all IPC channels, their arguments, and return types in one place:

```typescript
// src/shared/ipc-contract.ts

export interface StorageResult {
  success: boolean
  data?: string
  error?: string
  recovered?: boolean
}

/**
 * Central IPC contract. Every channel is defined once here.
 * Main process implements handlers, preload exposes them, renderer calls them.
 */
export interface IpcContract {
  // Storage operations
  'storage:read':   { args: [filename: string];              return: StorageResult }
  'storage:write':  { args: [filename: string, data: string]; return: StorageResult }
  'storage:backup': { args: [filename: string];              return: StorageResult }

  // Application
  'app:getVersion':      { args: [];                    return: string }
  'app:updateTitle':     { args: [projectName?: string]; return: void }

  // Context services
  'statements:load':     { args: [filename?: string];   return: Record<string, TemplateStatement> }
  'statements:update':   { args: [filename: string, key: string, content: string]; return: void }
  'systemPrompts:parse': { args: [filename?: string];   return: SystemPrompt[] }
}
```

### Type-Safe Wrappers

Generate type-safe invoke/handle wrappers from the contract:

```typescript
// src/shared/ipc-helpers.ts
import { ipcMain, ipcRenderer } from 'electron'
import type { IpcContract } from './ipc-contract'

// Main process: type-safe handler registration
export function handleIpc<C extends keyof IpcContract>(
  channel: C,
  handler: (...args: IpcContract[C]['args']) => Promise<IpcContract[C]['return']> | IpcContract[C]['return']
): void {
  ipcMain.handle(channel, (_, ...args) => handler(...args as IpcContract[C]['args']))
}

// Preload: type-safe invoke (used inside contextBridge)
export function invokeIpc<C extends keyof IpcContract>(
  channel: C,
  ...args: IpcContract[C]['args']
): Promise<IpcContract[C]['return']> {
  return ipcRenderer.invoke(channel, ...args)
}
```

### Usage After Contract

```typescript
// main/ipc/storage.ts — handler
import { handleIpc } from '../../shared/ipc-helpers'

handleIpc('storage:read', async (filename) => {
  // `filename` is typed as string
  // return type is enforced as StorageResult
  const data = await readFile(join(storagePath, filename), 'utf-8')
  return { success: true, data }
})

// preload/preload.cts — exposure
const { invokeIpc } = require('../../shared/ipc-helpers')
contextBridge.exposeInMainWorld('electronAPI', {
  storageRead: (filename: string) => invokeIpc('storage:read', filename),
  storageWrite: (filename: string, data: string) => invokeIpc('storage:write', filename, data),
})

// renderer — call
const result = await window.electronAPI.storageRead('projects.json')
// result is typed as StorageResult
```

### Benefits

- **Single source of truth**: One file defines all channels, arguments, and return types
- **Compile-time safety**: Typos in channel names or argument mismatches are caught by TypeScript
- **AI-agent friendly**: Agents can read the contract to understand the entire IPC surface
- **Refactoring**: Rename a channel in the contract, TypeScript errors show every call site
- **Documentation**: The contract IS the API documentation


## Process-Agnostic Service Layer

### The Principle

Business logic should not depend on Electron. Services like file managers, parsers, and data processors are pure logic that happens to run in Electron's main process. If written with injected dependencies, they can also run in a Node server, in tests, or in a CLI tool.

### The Pattern

```typescript
// src/main/services/statement-manager.ts

// Dependencies are injected, not imported
interface FileSystem {
  readFile(path: string): Promise<string>
  writeFile(path: string, content: string): Promise<void>
  exists(path: string): Promise<boolean>
}

export class StatementManager {
  constructor(
    private readonly fs: FileSystem,
    private readonly basePath: string
  ) {}

  async loadStatements(): Promise<Record<string, TemplateStatement>> {
    const raw = await this.fs.readFile(join(this.basePath, 'statements.json'))
    return JSON.parse(raw)
  }

  async saveStatements(statements: Record<string, TemplateStatement>): Promise<void> {
    await this.fs.writeFile(
      join(this.basePath, 'statements.json'),
      JSON.stringify(statements, null, 2)
    )
  }
}
```

### Wiring It Up

```typescript
// main/ipc/context-services.ts — thin IPC adapter
import { handleIpc } from '../../shared/ipc-helpers'
import { StatementManager } from '../services/statement-manager'
import { NodeFileSystem } from '../services/node-filesystem'

const fs = new NodeFileSystem()  // implements FileSystem using node:fs
const manager = new StatementManager(fs, getStoragePath())

handleIpc('statements:load', async (filename) => {
  return manager.loadStatements()
})
```

### Why This Matters

- **Testability**: Unit tests use a mock FileSystem, no Electron needed
- **Portability**: If you later extract the backend from Electron (as discussed for orchestration), services move unchanged
- **Clarity**: IPC handlers become thin adapters (2-3 lines each), not business logic containers
- **AI-friendliness**: Agents can work on services without understanding Electron's process model


## IPC Consolidation Patterns

### The Problem with Many Handlers

As an app grows, individual handlers proliferate. Context Forge has: `storage:read`, `storage:write`, `storage:backup`, `statements:load`, `statements:save`, `statements:get`, `statements:update`, `systemPrompts:parse`, `systemPrompts:getContextInit`, `systemPrompts:getToolUse`, `systemPrompts:getForInstruction` — each requiring preload exposure.

### Option A: Service Dispatcher

Consolidate related operations behind a single channel:

```typescript
// Contract defines the dispatch pattern
export interface IpcContract {
  'service:storage': {
    args: [method: 'read' | 'write' | 'backup', ...params: unknown[]]
    return: StorageResult
  }
  'service:statements': {
    args: [method: 'load' | 'save' | 'get' | 'update', ...params: unknown[]]
    return: unknown
  }
}
```

This reduces preload surface area but sacrifices some type safety on individual methods. Better for large apps with many operations per domain.

### Option B: electron-trpc

Libraries like `electron-trpc` provide tRPC-style typed procedures over Electron IPC, giving the same developer experience as a web app:

```typescript
// Define router (main process)
const appRouter = router({
  storage: router({
    read: procedure.input(z.string()).query(({ input }) => readStorage(input)),
    write: procedure.input(z.object({ filename: z.string(), data: z.string() }))
      .mutation(({ input }) => writeStorage(input.filename, input.data)),
  }),
})

// Call from renderer — fully typed
const data = await trpc.storage.read.query('projects.json')
```

This is the most robust solution for apps with complex IPC surfaces. It eliminates manual preload wiring entirely.

### Recommendation

- **Small apps (< 10 channels)**: Typed contract (Option A or just the shared contract) is sufficient
- **Medium apps (10-30 channels)**: Service dispatcher reduces preload maintenance
- **Large apps or apps likely to grow**: electron-trpc provides the best long-term DX


## State Management Across the Boundary

### Read-on-Mount, Write-on-Change (Simple)

The simplest pattern. Renderer reads state from main on component mount, writes back through IPC on user action. This is what Context Forge uses.

```typescript
// Renderer component
useEffect(() => {
  window.electronAPI.storageRead('projects.json').then(setProjects)
}, [])

const handleSave = async (updated: Project) => {
  await window.electronAPI.storageWrite('projects.json', JSON.stringify(updated))
}
```

**When to use**: Single-window apps, data that doesn't change unless the user acts, no external data sources pushing updates.

### Main-Pushes-Updates (Reactive)

For apps where the main process has state changes the renderer needs to know about (file watchers, external events, background tasks):

```typescript
// Main process pushes updates
fileWatcher.on('change', (path) => {
  mainWindow.webContents.send('file:changed', path)
})

// Preload exposes listener
contextBridge.exposeInMainWorld('electronAPI', {
  onFileChanged: (callback: (path: string) => void) => {
    ipcRenderer.on('file:changed', (_, path) => callback(path))
  }
})

// Renderer subscribes
useEffect(() => {
  window.electronAPI.onFileChanged((path) => {
    // Refresh relevant state
  })
}, [])
```

**When to use**: File watchers, background sync, multi-window apps, orchestration dashboards.

### Shared State Store

For complex apps, consider a state store that synchronizes across the boundary. Libraries like `electron-store` handle persistence, but for runtime state synchronization, the main process acts as the source of truth and pushes diffs to renderers.

**When to use**: Multi-window apps, apps with complex state that multiple UI components depend on. Rarely needed for single-window apps.


## When to Choose Electron

### Electron Is the Right Choice When

- **Local filesystem access is a core feature** (not just "nice to have"). File parsing, directory scanning, local data management.
- **The app is a personal or small-team tool.** Single-user productivity tools, developer tools, creative tools.
- **Desktop presence provides real workflow value.** Dock icon, Cmd+Tab access, global keyboard shortcuts, system tray. Anything used 10+ times daily benefits from this.
- **You don't need a cloud backend** (or cloud sync is an optional add-on layer, not the core architecture).

### Consider Alternatives When

- **The backend IS the product.** API orchestration, data processing pipelines, multi-user coordination — these belong in a proper server, not Electron's main process.
- **You need multi-user scaling.** Electron is one user, one machine. If the core value requires multiple concurrent users, start with web.
- **The app will definitely become a web/mobile product.** Building in Electron first then extracting is more work than starting with web.
- **The backend logic is complex enough for its own lifecycle.** If your backend would benefit from independent deployment, scaling, and testing, it shouldn't be fused to a desktop shell.

### The Hybrid Path

You can always wrap a web app in Electron later for desktop distribution. This works well when the web app is mature and you want to add desktop conveniences. The reverse (extracting a backend from Electron) is harder, but the process-agnostic service layer pattern described above makes it manageable.


## Anti-Patterns

### 1. Business Logic in IPC Handlers

```typescript
// ❌ WRONG — handler contains business logic
ipcMain.handle('storage:read', async (_, filename) => {
  // 50 lines of validation, parsing, error recovery...
})

// ✅ CORRECT — handler delegates to service
handleIpc('storage:read', (filename) => storageService.read(filename))
```

### 2. Renderer Directly Accessing Node APIs

Even with `nodeIntegration: false`, some developers create workarounds. Don't. The preload bridge exists for security.

### 3. Registering Handlers Inside createWindow()

Covered in the introduction, but worth repeating: IPC handlers must be registered once globally, not inside window creation functions. Second window creation will crash.

### 4. Duplicating Types Across Processes

If you find yourself defining the same interface in both main and renderer code, extract it to `src/shared/`. The shared directory is the single source of truth for cross-process types.

### 5. Over-Granular IPC

One channel per database field, one channel per UI action — this creates maintenance burden. Group related operations into logical service boundaries.

---

## Resources

- [electron-trpc](https://github.com/jsonnull/electron-trpc) — tRPC adapter for Electron IPC
- [Electron IPC Documentation](https://www.electronjs.org/docs/latest/tutorial/ipc)
- [electron-store](https://github.com/sindresorhus/electron-store) — Simple persistent storage

## Version History

- **2025-01-17** — Initial architecture notes (typed IPC, service decoupling)
- **2026-02-13** — Expanded into full architecture guide: IPC contract pattern, service layer, state management, decision framework, anti-patterns
