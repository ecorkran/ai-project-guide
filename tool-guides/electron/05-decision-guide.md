---
layer: tool-guide
tool: Electron
docType: guide
description: Decision framework for choosing Electron vs web-based architectures
dependsOn: [00-introduction.md]
dateCreated: 20260213
dateUpdated: 20260213
---

# Electron Decision Guide

When to use Electron, when not to, and what the alternatives look like. This guide helps make the architectural choice before writing code.


## The Core Tradeoff

Electron fuses a Node.js backend and Chromium frontend into a single desktop application. This gives you native desktop UX (dock icon, Cmd+Tab, system tray, global shortcuts, local filesystem) at the cost of managing a cross-process architecture (the "lichen pattern" — see Architecture Guide).

The question is always: **does the desktop UX and local-first capability justify the architectural overhead?**


## Decision Matrix

Answer these questions for your project. If most answers point to one column, that's your architecture.

| Question | Electron | Web App |
|----------|----------|---------|
| Does the app need local filesystem access as a **core** feature? | ✅ Yes | ❌ No, or can use file picker API |
| Is it a single-user tool? | ✅ Yes | Either |
| Will users run it 10+ times daily? | ✅ Desktop presence matters | ❌ Occasional use is fine in browser |
| Does the backend logic need independent scaling? | ❌ No | ✅ Yes |
| Will the app serve multiple concurrent users? | ❌ No | ✅ Yes |
| Is the app primarily an API orchestration layer? | ❌ Backend is the product | ✅ Yes |
| Do you plan to commercialize with cloud distribution? | ❌ Harder | ✅ Natural fit |
| Will the app definitely need web/mobile versions? | ❌ Extraction is costly | ✅ Start here |


## When Electron Is the Right Choice

**Local-first developer tools.** Context builders, prompt assemblers, file managers, code generators — anything that reads from and writes to the local filesystem as a core workflow. These tools benefit from instant access (dock icon, keyboard shortcut) and need no cloud backend.

**Personal productivity apps.** Note-taking, project management, time tracking — tools you reach for constantly throughout the day. The desktop presence reduces friction. Obsidian, Notion (desktop), and Todoist all use Electron for this reason.

**Creative tools with local assets.** Image editors, audio tools, video utilities that process local files. The main process handles heavy computation; the renderer provides the interactive UI.

**Monitoring dashboards for local services.** Docker management, local dev server dashboards, database GUIs. These connect to local services and benefit from always-on desktop presence.

### Real-world Electron success stories

VS Code, Obsidian, Discord, Slack, Spotify, Claude Desktop, Figma (desktop), GitHub Desktop, Notion (desktop), Postman — all Electron or Electron-like (some use Tauri or similar). The common thread: desktop presence provides genuine workflow value, and the apps are primarily single-user on a single machine.


## When to Avoid Electron

**API orchestration platforms.** If the core value is coordinating API calls, managing message queues, or routing between services, the "backend" is the product. Electron's main process adds window management overhead to what should be a clean service. Use a proper Node.js/Python server with a web dashboard.

**Multi-user collaborative tools.** Electron is one user, one machine. If the core value requires real-time collaboration between multiple users, you need a server anyway. Start with web.

**Apps destined for cloud/mobile distribution.** Building Electron first and extracting later is expensive. If you know the app will be a web or mobile product, start with web. You can always wrap the web app in Electron later for desktop distribution (the reverse is cheaper than the forward direction).

**Complex backend logic that needs its own lifecycle.** If your backend would benefit from independent deployment, scaling, monitoring, and testing, it shouldn't be fused to a desktop shell. The lichen pattern means every backend change requires a desktop app rebuild.


## The Alternatives

### React + Express/Fastify (Separate Backend)

**Architecture**: React SPA served by any HTTP server. Backend runs as a separate Node.js process (local or remote).

**Pros**: Clean separation of concerns. Backend testable independently. Natural path to cloud deployment. AI agents work on one process at a time.

**Cons**: Two processes to manage locally. No native desktop integration (no dock icon, no system tray, no global shortcuts). Users find it in a browser tab.

**Best for**: Apps with backend logic that will scale, apps targeting multiple platforms, apps where the backend is the core value.

### Next.js

**Architecture**: Full-stack React framework with server-side rendering, API routes, and file-based routing.

**Pros**: Single project for frontend + backend. Good DX. Large ecosystem. Built-in SSR for SEO.

**Cons**: Deployment can be complex (Vercel lock-in or self-hosting overhead). SSR restrictions can feel heavy for interactive apps. API routes are limited compared to a dedicated backend.

**Best for**: Content-heavy apps, apps that need SEO, apps where Vercel deployment is acceptable.

### React SPA (No Backend)

**Architecture**: Pure client-side React. Static hosting (Netlify, Vercel, S3). No server-side logic.

**Pros**: Simplest architecture. Cheapest hosting. No backend maintenance.

**Cons**: No server-side logic. No filesystem access. No secrets management. Limited to browser APIs.

**Best for**: Calculators, visualization tools, documentation sites, configuration generators — anything that transforms input to output without persistent state or secrets.

### The Hybrid Path: Web First, Electron Later

Build the web app first. Once it's stable and you want desktop distribution, wrap it in Electron:

```typescript
// main.ts — minimal Electron wrapper around existing web app
const win = new BrowserWindow({ width: 1200, height: 800 })

if (isDev) {
  win.loadURL('http://localhost:3000')  // Dev server
} else {
  win.loadFile('out/index.html')  // Built web app
}
```

This gives you the dock icon and desktop presence without the lichen architecture. The web app remains the source of truth. Add native features (filesystem, tray, shortcuts) incrementally as needed.

**When this works well**: The app is primarily a UI with a remote backend. Desktop is a distribution convenience, not an architectural requirement.

**When this doesn't work**: The app needs deep filesystem integration, local processing, or offline-first capability. These require Electron's main process from the start.


## Mitigating Electron Complexity

If you choose Electron, these patterns (detailed in the Architecture Guide) reduce the lichen tax:

1. **Typed IPC contract** — Single source of truth for all IPC channels, compile-time safety across process boundary
2. **Process-agnostic services** — Business logic with no Electron imports, testable and portable
3. **Thin IPC handlers** — 2-5 lines per handler, delegate to services
4. **Shared types directory** — Never duplicate types across processes
5. **Renderer service wrappers** — Clean API for components, hide IPC details

With these patterns, the Electron-specific code becomes a thin shell around portable business logic. If you later need to extract the backend (as discussed for orchestration-type apps), the services move unchanged.


## Template Recommendations

For a template ecosystem covering different project types:

| Template | Architecture | Use When |
|----------|-------------|----------|
| **Electron + React** | Full Electron with typed IPC | Local-first tools, desktop productivity apps |
| **React + Express** | SPA + API server | Apps with backend logic, future cloud deployment |
| **React SPA** | Client-only | Pure frontend tools, no backend needed |
| **Next.js** | Full-stack framework | Content-heavy, SEO-important, Vercel-friendly |

Each template should include the appropriate architecture guide and testing strategy for its pattern.

---

## Version History

- **2026-02-13** — Initial guide: decision matrix, alternatives comparison, mitigation strategies
