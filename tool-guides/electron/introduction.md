---
layer: tool-guide
tool: Electron
docType: introduction
---

# Electron Tool Guide - Introduction

This guide documents critical knowledge about Electron development, including gotchas, best practices, and solutions to common problems. Written after hard-won battles in production.

## Table of Contents

1. [Process Architecture](#process-architecture)
2. [OAuth & Authentication](#oauth--authentication)
3. [Packaging & Distribution](#packaging--distribution)
4. [Security Best Practices](#security-best-practices)
5. [Common Pitfalls](#common-pitfalls)

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

**Why:** Renderer process runs untrusted web content. Giving it Node.js access = massive security hole.

### Preload Script

The preload script (`src/preload/`) bridges main and renderer:

```typescript
// preload.ts
import { contextBridge, ipcRenderer } from 'electron'

contextBridge.exposeInMainWorld('electronAPI', {
  readFile: (path: string) => ipcRenderer.invoke('read-file', path)
})
```

```typescript
// main.ts
ipcMain.handle('read-file', async (event, path) => {
  return fs.readFileSync(path, 'utf-8')
})
```

```typescript
// renderer (React component)
const content = await window.electronAPI.readFile('/path/to/file')
```

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
// Start server on fixed port
const server = http.createServer(handleCallback)
server.listen(52847, '127.0.0.1')

// Auth0 callback URL: http://localhost:52847/callback
```

**Benefits:**
- No protocol registration needed
- Works identically in dev and production
- No bundle ID conflicts
- Simple, reliable

### OAuth Provider Limitations

**Critical Issue:** Most OAuth providers (Auth0, Okta) **DO NOT support RFC 8252** dynamic ports despite the OAuth standard requiring it for native apps.

RFC 8252 says:
> "The authorization server MUST allow any port to be specified at the time of the request for loopback IP redirect URIs"

**Reality:**
- ✅ **Support dynamic ports:** Microsoft Azure AD, Keycloak, Ping
- ❌ **Don't support dynamic ports:** Auth0, Okta

**Workaround:** Use a fixed high port (52847) to minimize conflicts.

```typescript
// callback-server.ts
const AUTH_CALLBACK_PORT = 52847  // Fixed port
server.listen(AUTH_CALLBACK_PORT, '127.0.0.1')
```

**Auth0 Configuration:**
```
Allowed Callback URLs: http://localhost:52847/callback
```

This is not ideal (port conflicts possible), but Auth0 doesn't give us a better option.

### OAuth Provider Comparison for Electron

If you're choosing an OAuth provider for your Electron app, here's how they compare on RFC 8252 compliance:

| Provider | Ephemeral Port Support | Electron Maturity | Complexity | Status |
|----------|----------------------|-------------------|------------|--------|
| **Firebase Auth** | ✅ Yes | ✅ Proven | Low | **Best choice** |
| **Stytch** | ✅ Yes | ⚠️ Limited docs | Low | Good alternative |
| **Auth0** | ❌ No (fixed port) | ✅ Works | Medium | **Current choice** |
| **Okta** | ❌ No (fixed port) | ✅ Works | Medium | Similar to Auth0 |
| **Supabase** | ❓ Unknown | ❌ Problematic | Medium | **Avoid** |
| **LoginRadius** | ✅ Yes | ⚠️ Unknown | Low | Untested |
| **Frontegg** | ✅ Yes | ⚠️ Unknown | Low | Untested |
| **PingOne** | ✅ Yes | ⚠️ Unknown | Low-Med | Untested |

**Recommendation for Templates:**

**1. Firebase Authentication** - Best long-term choice:
- ✅ Free tier is generous
- ✅ 2-minute setup for end users
- ✅ RFC 8252 compliant (supports dynamic ports)
- ✅ Well-documented Electron integration
- ✅ Users already familiar with it
- ✅ No backend management required

**2. Auth0** - Acceptable current choice (what we use):
- ✅ Works reliably with fixed port (52847)
- ✅ Mature, well-tested
- ✅ Good documentation
- ❌ Requires fixed port (RFC 8252 non-compliant)
- ❌ Port conflicts possible (rare)

**3. Stytch** - Interesting alternative:
- ✅ Modern API, great DX
- ✅ Likely RFC 8252 compliant
- ❌ Less familiar to users
- ⚠️ Limited Electron documentation

**Avoid: Supabase** - Multiple unresolved issues:
- ❌ Custom protocols cause `ERR_UNEXPECTED` errors
- ❌ Session loss after OAuth (401 errors)
- ❌ No clear Electron documentation
- ❌ Developers report "multi-week" struggles
- Status as of 2025: Active unresolved GitHub issues

**Our current implementation uses Auth0** because it works reliably despite the fixed port requirement. Firebase would be a better choice for new projects.

### Implementation Notes

1. **Start server before login:**
   ```typescript
   await startCallbackServer()  // Starts server on port 52847
   await auth0Client.login()    // Opens browser
   ```

2. **Server handles callback:**
   ```typescript
   // Browser redirects to http://localhost:52847/callback?code=...
   // Server extracts code, exchanges for tokens
   await auth0Client.handleCallback(url)
   ```

3. **Stop server after auth:**
   ```typescript
   await stopCallbackServer()  // Clean up
   ```

4. **Restore main window:**
   ```typescript
   mainWindow.show()
   mainWindow.focus()
   mainWindow.reload()  // Show authenticated state
   ```

### Common Auth Issues

**Issue:** "Callback URL mismatch" error
- **Cause:** Port in code doesn't match Auth0 config
- **Fix:** Verify `AUTH_CALLBACK_PORT` matches Auth0 "Allowed Callback URLs"

**Issue:** White screen after auth callback
- **Cause:** Window not restored/reloaded
- **Fix:** Call `mainWindow.reload()` after successful auth

**Issue:** Auth works in dev but not production
- **Cause:** `.env` file not included in packaged app
- **Fix:** Add `.env` to `extraResources` in `package.json`

---

## Packaging & Distribution

### Environment Variables

**Development vs Production:**

Development (`pnpm dev`):
- Loads `.env` from project root via `dotenv`
- Uses `process.cwd()` to find `.env`

Production (packaged app):
- Cannot use `process.cwd()` (points to wrong location)
- Must use `process.resourcesPath` to find bundled files

**Correct pattern:**
```typescript
const envPath = app.isPackaged
  ? join(process.resourcesPath, '.env')  // Production
  : join(process.cwd(), '.env')          // Development

config({ path: envPath })
```

**electron-builder configuration:**
```json
{
  "build": {
    "extraResources": [
      {
        "from": ".env",
        "to": ".env"
      }
    ]
  }
}
```

**Security Warning:** Including `.env` in packaged apps exposes secrets. For production apps:
- Use environment variables set by installer
- Use system keychain for credentials
- Use a settings UI for user-provided credentials
- Never bundle production secrets in distributed apps

### File Paths

**Loading renderer in production:**

```typescript
// main.ts - createWindow()
if (process.env.ELECTRON_RENDERER_URL) {
  // Development: Vite dev server
  win.loadURL(process.env.ELECTRON_RENDERER_URL)
} else {
  // Production: bundled files
  const rendererPath = app.isPackaged
    ? path.join(process.resourcesPath, 'renderer/index.html')
    : path.join(__dirname, '../renderer/index.html')
  win.loadFile(rendererPath)
}
```

**Why:**
- Dev: Renderer runs on Vite dev server (`http://localhost:5173`)
- Prod: Renderer files bundled in `Resources/renderer/`

**Common mistake:** Using `__dirname` in packaged apps - it points inside `app.asar`, but `extraResources` are outside the asar.

### Single Instance Lock

**Always use single instance lock for apps with auth:**

```typescript
const gotTheLock = app.requestSingleInstanceLock()

if (!gotTheLock) {
  app.quit()  // Another instance running
} else {
  app.on('second-instance', () => {
    // Someone tried to open second instance
    // Focus existing window instead
    const mainWindow = BrowserWindow.getAllWindows()[0]
    mainWindow.focus()
  })
}
```

**Why:** Prevents multiple instances from fighting over callback servers, protocol registrations, etc.

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
    shell.openExternal(url)  // Open in browser
  }
  return { action: 'deny' }  // Don't open new window
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

## Common Pitfalls

### 1. IPC Handler Registration

**Problem:** Registering IPC handlers inside `createWindow()` causes crashes on second window.

```typescript
// ❌ WRONG
function createWindow() {
  const win = new BrowserWindow(...)

  ipcMain.handle('ping', () => 'pong')  // Crashes on second window
}
```

```typescript
// ✅ CORRECT
ipcMain.handle('ping', () => 'pong')  // Register once, globally

app.whenReady().then(createWindow)
```

**Error:** `Attempted to register a second handler for 'ping'`

### 2. Module Resolution in Packaged Apps

**Problem:** Imports work in dev but fail in production.

**Cause:** Different module resolution between `ts-node` and compiled code.

**Fix:** Use explicit file extensions:
```typescript
// ❌ May fail in production
import { foo } from './utils'

// ✅ Works everywhere
import { foo } from './utils.js'  // Even for .ts files
```

### 3. Hot Reload Breaking State

**Problem:** Hot reload in dev mode breaks app state.

**Solution:** Accept that dev mode !== production. Test critical flows in packaged builds.

### 4. File Protocol Loading

**Never use `file://` protocol to load renderer.** Use `loadFile()` or dev server.

```typescript
// ❌ WRONG
win.loadURL('file:///path/to/index.html')

// ✅ CORRECT
win.loadFile(path.join(__dirname, 'index.html'))
```

### 5. Async Top-Level Await

Electron supports top-level await in main process:

```typescript
// main.ts
const { auth0Client } = await import('./auth/auth0-client')
```

This works and is cleaner than wrapping everything in async IIFE.

---

## Development Workflow

### Build Commands

```bash
pnpm dev      # Development mode with hot reload
pnpm build    # Build renderer + main for production
pnpm package  # Package into .app/.exe/.AppImage
pnpm preview  # Run packaged build locally
```

### Testing Strategy

1. **Dev mode** - Fast iteration, hot reload
2. **Preview mode** - Quick check of packaged build
3. **Full package** - Final test before distribution

**Test auth in packaged builds** - Dev mode uses different paths, process.cwd(), etc.

### Debugging

**Main Process:**
```bash
# Check console output
pnpm dev  # Logs appear in terminal
```

**Renderer Process:**
```typescript
// Open dev tools programmatically
win.webContents.openDevTools()

// Or press F12 in app
```

**Packaged App:**
```bash
# Run with console output visible
open /path/to/App.app --args --remote-debugging-port=9222
```

---

## Resources

- [Electron Security](https://www.electronjs.org/docs/tutorial/security)
- [RFC 8252 - OAuth for Native Apps](https://tools.ietf.org/html/rfc8252)
- [electron-builder docs](https://www.electron.build/)

---

## Version History

- **2025-01-17** - Initial guide based on auth implementation battle
