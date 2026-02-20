---
description: Electron-specific development rules including module loading and process architecture
globs: ["**/*.ts", "**/*.tsx", "**/*.cjs", "**/*.mjs"]
alwaysApply: false
---

### Electron Rules
Module Loading: ESM vs CJS (Electron)
	•	Use ESM for main and renderer processes — modern syntax, async loading, cleaner imports.
	•	Keep preload scripts CJS if contextIsolation: true (default and secure).
	•	Avoid disabling contextIsolation just to use ESM — security outweighs convenience.
	•	When preload uses CJS, expose a minimal API via contextBridge.exposeInMainWorld().
	•	Build config: Set main output format: 'es', preload output format: 'cjs'
	•	Future-proof: when Electron supports isolated ESM preload officially, revisit this rule.
