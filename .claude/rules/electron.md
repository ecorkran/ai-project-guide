---
description: Electron desktop application rules including main/renderer process architecture, IPC patterns, preload scripts, and module loading. Use when working on Electron apps, desktop applications using Electron, or files involving IPC, BrowserWindow, or electron-vite.
paths:
  - "electron/**/*"
  - "src/preload/**/*"
  - "electron-builder.*"
  - "forge.config.*"
  - "**/electron.vite.*"
---

### Electron Rules
Module Loading: ESM vs CJS (Electron)
	•	Use ESM for main and renderer processes — modern syntax, async loading, cleaner imports.
	•	Keep preload scripts CJS if contextIsolation: true (default and secure).
	•	Avoid disabling contextIsolation just to use ESM — security outweighs convenience.
	•	When preload uses CJS, expose a minimal API via contextBridge.exposeInMainWorld().
	•	Build config: Set main output format: 'es', preload output format: 'cjs'
	•	Future-proof: when Electron supports isolated ESM preload officially, revisit this rule.
