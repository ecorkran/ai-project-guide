---
layer: tool-guide
tool: Electron
docType: introduction
description: Entry point for Electron tool guides. Read this first to determine which guide you need.
dateCreated: 20250117
dateUpdated: 20260213
---

# Electron Tool Guide — Introduction

This is the entry point for Electron development guidance. **Read the guide selection table below to find the right document for your task, rather than loading all guides into context.**

## Guide Selection

| I need to... | Read this guide |
|--------------|----------------|
| Understand Electron's process model, IPC basics, preload scripts | **This file** (sections below) |
| Design IPC contracts, service layers, state management | **01-architecture.md** |
| Know where to put files, add a new IPC channel (step-by-step) | **02-project-structure.md** |
| Configure electron-vite, debug dev vs prod differences | **03-electron-vite.md** |
| Write tests for services, components, or IPC flows | **04-testing.md** |
| Decide whether to use Electron for a new project | **05-decision-guide.md** |
| Implement OAuth / authentication | **This file** (OAuth section below) |
| Package and distribute the app | **This file** (Packaging section) + **03-electron-vite.md** |

### For AI Agents: Which Guide to Load

- **Adding a feature that needs backend capability**: Load **02-project-structure.md** (has the 7-step IPC checklist)
- **Refactoring or designing IPC/service architecture**: Load **01-architecture.md**
- **Build is broken or dev/prod mismatch**: Load **03-electron-vite.md**
- **Writing or fixing tests**: Load **04-testing.md**
- **Starting a new project or evaluating architecture**: Load **05-decision-guide.md**
- **Auth implementation**: Read the OAuth section in **this file**

You should rarely need more than one guide per task. This introduction provides foundational knowledge that all other guides assume.

---

## Process Architecture

### Main Process vs Renderer Process

Electron has two types of processes:

**Main Process** (`src/main/`)
- Runs Node.js with full system access
- One per application
- Can use `fs`, `path`, `http`, native modules
- Handles window creation, system APIs, IPC handlers
- Runs `main.ts` on startup

**Renderer Process** (`src/renderer/`)
- Runs Chromium/web content
- One per `BrowserWindow`
- Should NOT have Node.js access (security)
- Uses `contextIsolation: true` and `nodeIntegration: false`
- Communicates with main via IPC (Inter-Process Communication)

### Critical Rules

**NEVER use Node.js APIs in renderer code:**
```typescript
// ❌ WRONG - Don't do this in renderer
import fs from 'node:fs'
fs.readFileSync('/some/file')

// ✅ CORRECT - Use IPC to ask main process
const data = await window.electronAPI.readFile('/some/file')
```

**Why:** Renderer process runs untrusted web content. Giving it Node.js access is a massive security hole.

### Preload Script

The preload script (`src/preload/`) bridges main and renderer:

```typescript
// preload.cts (CJS required for contextIsolation)
const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('electronAPI', {
  readFile: (path: string) => ipcRenderer.invoke('read-file', path)
})
```

```typescript
// main.ts — handler
ipcMain.handle('read-file', async (event, path) => {
  return fs.readFileSync(path, 'utf-8')
})
```

```typescript
// renderer (React component)
const content = await window.electronAPI.readFile('/path/to/file')
```

For the full typed IPC contract pattern that eliminates string-based channel mismatches, see **01-architecture.md**.

### Module Loading: CJS vs ESM

- Use **ESM** for main and renderer processes — modern syntax, cleaner imports
- Keep preload scripts **CJS** (`contextIsolation: true` requires it)
- Never disable `contextIsolation` just to use ESM — security outweighs convenience
- When preload uses CJS, expose a minimal API via `contextBridge.exposeInMainWorld()`

---

## Security Best Practices

### Context Isolation

**Always enable context isolation:**

```typescript
const win = new BrowserWindow({
  webPreferences: {
    preload: preloadPath,
    contextIsolation: true,   // Required
    nodeIntegration: false,   // Required
    sandbox: true             // Recommended
  }
})
```

**Never disable these for convenience.** Use IPC instead.

### Navigation Security

**Prevent navigation to malicious sites:**

```typescript
win.webContents.on('will-navigate', (event, url) => {
  if (!isAllowedUrl(url)) {
    event.preventDefault()
  }
})

win.webContents.setWindowOpenHandler(({ url }) => {
  if (isAllowedUrl(url)) {
    shell.openExternal(url)  // Open in default browser
  }
  return { action: 'deny' }  // Don't open new Electron window
})
```

### IPC Security

**Validate all IPC messages:**

```typescript
ipcMain.handle('read-file', async (event, filePath) => {
  // ❌ WRONG - No validation
  return fs.readFileSync(filePath)

  // ✅ CORRECT - Validate input
  if (!isValidPath(filePath)) {
    throw new Error('Invalid file path')
  }
  return fs.readFileSync(filePath)
})
```

**Why:** Renderer can be compromised by malicious website. Treat all IPC input as untrusted.

---

## OAuth & Authentication

### The Problem: Custom Protocols

Many guides suggest using custom protocols (e.g., `myapp://callback`) for OAuth callbacks. **This is the hardest approach** and causes massive headaches:

- Requires OS-level protocol registration
- macOS caches protocol registrations system-wide
- Multiple apps with same protocol conflict
- Different bundle IDs in dev vs production
- Protocol registration breaks randomly

**Avoid custom protocols unless you have a specific reason (deep linking, etc.).**

### The Solution: Localhost Callbacks

Use a local HTTP server on a fixed port:

```typescript
const server = http.createServer(handleCallback)
server.listen(52847, '127.0.0.1')
// Auth0 callback URL: http://localhost:52847/callback
```

**Benefits:** No protocol registration, works identically in dev and production, no bundle ID conflicts.

### OAuth Provider Limitations

**Critical Issue:** Most OAuth providers (Auth0, Okta) **DO NOT support RFC 8252** dynamic ports despite the OAuth standard requiring it for native apps.

**Workaround:** Use a fixed high port (52847) to minimize conflicts.

### OAuth Provider Comparison for Electron

| Provider | Ephemeral Port Support | Electron Maturity | Status |
|----------|----------------------|-------------------|--------|
| **Firebase Auth** | ✅ Yes | ✅ Proven | **Best choice for new projects** |
| **Stytch** | ✅ Yes | ⚠️ Limited docs | Good alternative |
| **Auth0** | ❌ No (fixed port) | ✅ Works | **Acceptable (current choice)** |
| **Okta** | ❌ No (fixed port) | ✅ Works | Similar to Auth0 |
| **Supabase** | ❓ Unknown | ❌ Problematic | **Avoid** — multiple unresolved Electron issues |

**Recommendation:** Firebase for new projects. Auth0 if already in use (works reliably with fixed port).

### Implementation Flow

1. Start localhost callback server before login
2. Open browser for OAuth provider login
3. Server catches callback redirect, extracts authorization code
4. Exchange code for tokens
5. Stop callback server
6. Restore and reload main window to show authenticated state

### Common Auth Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| "Callback URL mismatch" | Port mismatch | Verify port matches provider config |
| White screen after auth | Window not restored | Call `mainWindow.reload()` after auth |
| Works in dev, fails in prod | `.env` not bundled | Add `.env` to `extraResources` |

---

## Packaging & Distribution

### Environment Variables: Dev vs Production

```typescript
// Correct pattern for finding files
const envPath = app.isPackaged
  ? join(process.resourcesPath, '.env')  // Production
  : join(process.cwd(), '.env')          // Development
```

**Key difference:** `process.cwd()` in production does NOT point to your project root. Use `process.resourcesPath` for bundled files and `app.getPath('userData')` for persistent user data.

For full packaging configuration, build targets, and troubleshooting, see **03-electron-vite.md**.

### Single Instance Lock

**Always use for apps with auth or callback servers:**

```typescript
const gotTheLock = app.requestSingleInstanceLock()
if (!gotTheLock) {
  app.quit()
} else {
  app.on('second-instance', () => {
    const mainWindow = BrowserWindow.getAllWindows()[0]
    mainWindow?.focus()
  })
}
```

---

## Common Pitfalls (Quick Reference)

| Pitfall | Problem | Solution |
|---------|---------|----------|
| IPC handlers in `createWindow()` | Crashes on second window | Register handlers globally, once |
| `__dirname` in packaged apps | Points inside `app.asar` | Use `process.resourcesPath` or `import.meta.url` |
| Node.js APIs in renderer | Security hole | Use IPC through preload bridge |
| Duplicate types across processes | Drift and mismatch | Put shared types in `src/shared/` |
| `file://` protocol for renderer | Various issues | Use `loadFile()` or dev server URL |
| ESM in preload scripts | Fails with contextIsolation | Use `.cts` extension (CJS) |

For detailed solutions, see the specific guide for your area (architecture, project structure, or electron-vite).

---

## Development Workflow

### Build Commands

```bash
pnpm dev          # Development mode with HMR (renderer only)
pnpm build        # Compile all three targets to out/
pnpm package      # Build + package into .app/.exe/.AppImage
pnpm preview      # Run packaged build locally
```

### Debugging

- **Main Process**: Logs appear in terminal where `pnpm dev` runs
- **Renderer Process**: DevTools (F12 or `win.webContents.openDevTools()`)
- **Packaged App**: `open /path/to/App.app --args --remote-debugging-port=9222`

**Always test auth and file operations in packaged builds** — dev mode uses different paths and environment variables.

---

## Resources

- [Electron Security](https://www.electronjs.org/docs/tutorial/security)
- [RFC 8252 — OAuth for Native Apps](https://tools.ietf.org/html/rfc8252)
- [electron-builder docs](https://www.electron.build/)
- [electron-vite docs](https://electron-vite.org/)

---

## Version History

- **2025-01-17** — Initial guide based on auth implementation experience
- **2026-02-13** — Restructured as guide entry point with routing table. Detailed architecture, project structure, build, testing, and decision content moved to dedicated guides.
