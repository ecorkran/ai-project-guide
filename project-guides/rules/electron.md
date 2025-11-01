---
description: TypeScript syntax rules, tRPC router guidelines, and strict typing standards
globs: ["**/*.ts", "**/*.tsx", "**/*.cjs", "**/*.mjs"]
alwaysApply: false
---

Module Loading: ESM vs CJS (Electron)
	•	Use ESM for main and renderer processes — modern syntax, async loading, cleaner imports.
	•	Keep preload scripts CJS if contextIsolation: true (default and secure).
	•	Avoid disabling contextIsolation just to use ESM — security outweighs convenience.
	•	When preload uses CJS, expose a minimal API via contextBridge.exposeInMainWorld().
	•	Build config: Set main output format: 'es', preload output format: 'cjs'
	•	Future-proof: when Electron supports isolated ESM preload officially, revisit this rule.
