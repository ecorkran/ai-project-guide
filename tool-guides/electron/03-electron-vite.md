---
layer: tool-guide
tool: Electron
docType: guide
description: electron-vite build configuration, dev/prod differences, and troubleshooting build issues
dependsOn: [00-introduction.md, 02-project-structure.md]
dateCreated: 20260213
dateUpdated: 20260213
---

# Electron-Vite Build & Toolchain Guide

This guide covers the `electron-vite` build system, how it maps to Electron's process model, and the dev-vs-production differences that cause the most bugs.


## Why electron-vite

Electron apps have three distinct build targets (main, preload, renderer), each with different runtime requirements. `electron-vite` handles this by extending Vite with Electron-aware configuration, giving you fast HMR for the renderer, proper Node.js builds for main/preload, and a single config file for all three.

The alternative — manually configuring Webpack or vanilla Vite for three targets — is significantly more boilerplate and a common source of misconfiguration.


## Build Configuration

The central config file `electron.vite.config.ts` defines three build targets:

```typescript
// electron.vite.config.ts
import { defineConfig, externalizeDepsPlugin } from 'electron-vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  main: {
    // Builds: src/main/ → out/main/
    // Runtime: Node.js (full system access)
    plugins: [externalizeDepsPlugin()],
    build: {
      rollupOptions: {
        external: ['electron']
      }
    }
  },

  preload: {
    // Builds: src/preload/ → out/preload/
    // Runtime: Node.js with contextIsolation
    // MUST output CJS for contextIsolation compatibility
    plugins: [externalizeDepsPlugin()],
    build: {
      rollupOptions: {
        external: ['electron']
      }
    }
  },

  renderer: {
    // Builds: src/ (via index.html entry) → out/renderer/
    // Runtime: Chromium (browser APIs only)
    plugins: [react(), tailwindcss()],
    build: {
      rollupOptions: {
        input: 'index.html'
      }
    }
  }
})
```

### How the Three Targets Map to Processes

| Target | Entry Point | Output | Runtime | Can Import |
|--------|-------------|--------|---------|------------|
| `main` | `src/main/main.ts` | `out/main/main.js` | Node.js | `electron`, `node:*`, npm packages, `src/shared/` |
| `preload` | `src/preload/preload.cts` | `out/preload/preload.cjs` | Node.js (isolated) | `electron` (contextBridge, ipcRenderer only), `src/shared/` |
| `renderer` | `index.html` → `App.tsx` | `out/renderer/` | Chromium | React, browser APIs, `src/shared/` types, npm packages (browser-compatible) |

### The shared/ Directory

Files in `src/shared/` are imported by both the main and renderer builds. TypeScript types are erased at build time (zero runtime cost). Any runtime code in `shared/` will be bundled into both outputs — keep it to types and constants.

### externalizeDepsPlugin

This plugin tells the main and preload builds to NOT bundle npm dependencies — they'll be resolved from `node_modules` at runtime. This is correct because Electron's main process has full Node.js module resolution. The renderer build does NOT use this plugin because browser-target code must be fully bundled.


## Development vs Production

This is the single largest source of "works in dev, breaks in production" bugs.

### Development Mode (`pnpm dev`)

```
┌─────────────────────────────────────────┐
│ electron-vite dev                       │
│                                         │
│  Main process:    Compiled, run by Node │
│  Preload:         Compiled, loaded by   │
│                   BrowserWindow         │
│  Renderer:        Vite dev server       │
│                   http://localhost:5173  │
│                                         │
│  env var: ELECTRON_RENDERER_URL is set  │
│  app.isPackaged: false                  │
│  process.cwd(): project root            │
└─────────────────────────────────────────┘
```

Key behaviors in dev:
- Renderer runs on Vite's HTTP dev server with HMR
- `process.env.ELECTRON_RENDERER_URL` is set (used to detect dev mode)
- `process.cwd()` points to project root (where `.env` lives)
- `__dirname` points to compiled output in `out/main/`
- Changes to renderer files trigger instant HMR
- Changes to main process files require restart

### Production Mode (packaged app)

```
┌─────────────────────────────────────────┐
│ Packaged .app / .exe / .AppImage        │
│                                         │
│  Main process:    out/main/main.js      │
│  Preload:         out/preload/preload.cjs│
│  Renderer:        out/renderer/index.html│
│                   (loaded via loadFile)  │
│                                         │
│  ELECTRON_RENDERER_URL: undefined       │
│  app.isPackaged: true                   │
│  process.cwd(): varies by OS           │
│  process.resourcesPath: app resources   │
└─────────────────────────────────────────┘
```

Key behaviors in production:
- Renderer is static files loaded via `win.loadFile()`
- `process.env.ELECTRON_RENDERER_URL` is undefined
- `process.cwd()` is NOT the project root — it varies by OS and launch method
- `process.resourcesPath` points to the app's bundled resources
- `__dirname` points inside `app.asar` (read-only archive)
- `extraResources` files are outside `app.asar` at `process.resourcesPath`

### The Correct Pattern for Loading Renderer

```typescript
// src/main/main.ts — in createWindow()
if (process.env.ELECTRON_RENDERER_URL) {
  // Development: load from Vite dev server
  win.loadURL(process.env.ELECTRON_RENDERER_URL)
} else {
  // Production: load bundled files
  win.loadFile(fileURLToPath(new URL('../renderer/index.html', import.meta.url)))
}
```

### The Correct Pattern for Finding Files

```typescript
import { app } from 'electron'
import { join } from 'node:path'

// Files bundled via extraResources (e.g., .env, data files)
const resourcePath = app.isPackaged
  ? join(process.resourcesPath, 'myfile.json')
  : join(process.cwd(), 'myfile.json')

// User data (persistent across app updates)
const userDataPath = app.getPath('userData')
// macOS: ~/Library/Application Support/{app-name}/
// Windows: %APPDATA%/{app-name}/
// Linux: ~/.config/{app-name}/
```


## Packaging with electron-builder

### package.json Build Configuration

```json
{
  "build": {
    "appId": "com.yourname.appname",
    "productName": "App Name",
    "directories": {
      "output": "dist"
    },
    "files": [
      "out/**/*"
    ],
    "extraResources": [
      {
        "from": ".env",
        "to": ".env"
      },
      {
        "from": "content/",
        "to": "content/"
      }
    ],
    "mac": {
      "target": ["dmg", "zip"],
      "category": "public.app-category.developer-tools"
    },
    "win": {
      "target": ["nsis", "portable"]
    },
    "linux": {
      "target": ["AppImage", "deb"],
      "category": "Development"
    }
  }
}
```

### Build Commands

```bash
pnpm dev          # Development with HMR
pnpm build        # Compile all three targets to out/
pnpm package      # Build + package into distributable
pnpm preview      # Run packaged build locally (quick test)
```

### extraResources vs files

- **`files`**: Bundled inside `app.asar` (read-only, fast). Code and static assets.
- **`extraResources`**: Placed alongside `app.asar` at `process.resourcesPath` (read/write). Config files, data files, anything that needs to be modified or read by path.

**Security warning**: Never put production secrets in `extraResources`. The `.env` pattern is acceptable for development/personal tools but not for distributed commercial software. Use system keychain or user-provided credentials for production.


## TypeScript Configuration

Electron projects typically need a `tsconfig.json` that supports both Node.js (main) and browser (renderer) targets:

```json
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "jsx": "react-jsx",
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "types": ["node", "vite/client"]
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "out", "dist"]
}
```

The `"module": "ESNext"` with `"moduleResolution": "bundler"` is important — it lets TypeScript understand that the bundler (Vite/Rollup) will resolve modules, not Node.js directly.


## Common Build Issues

### "Cannot find module" in packaged app

**Cause**: Module is devDependency but used at runtime, or path resolution differs in packaged builds.

**Fix**: Ensure runtime dependencies are in `dependencies`, not `devDependencies`. For path issues, use `app.isPackaged` checks.

### Preload script fails with ESM syntax error

**Cause**: Preload script compiled as ESM but `contextIsolation` requires CJS.

**Fix**: Use `.cts` extension for preload files. Ensure electron-vite preload config outputs CJS.

### Static assets missing in production

**Cause**: Assets referenced by path aren't included in the build.

**Fix**: Import assets in code (Vite will bundle them) or add to `extraResources` and use `process.resourcesPath` to find them.

### HMR not working for main process changes

**Expected behavior**: electron-vite only provides HMR for the renderer. Main process changes require a full restart. The dev server will automatically restart the main process when main-process files change.

### "__dirname is undefined" or points to wrong location

**Cause**: ESM modules don't have `__dirname`. Or in packaged apps, `__dirname` points inside `app.asar`.

**Fix**: Use `import.meta.url` with `fileURLToPath` for ESM. Use `process.resourcesPath` for packaged app resources.

```typescript
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'

// ESM equivalent of __dirname
const __dirname = dirname(fileURLToPath(import.meta.url))

// But for packaged resources, prefer:
const resourcePath = app.isPackaged
  ? process.resourcesPath
  : process.cwd()
```

---

## Version History

- **2026-02-13** — Initial guide: build config, dev/prod differences, packaging, troubleshooting
