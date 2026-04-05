---
docType: tool-guide
layer: tool-guide
platform: threejs
audience: [human, ai]
purpose: installation & project setup
dateCreated: 20250718
dateUpdated: 20260405
status: in_progress
---

## Three.js Setup Guide

This guide scaffolds a modern Three.js project using **Vite**, **pnpm**, and **WebGPURenderer** (with automatic WebGL 2 fallback). For the full WebGPU renderer guide including TSL shaders, NodeMaterials, and post-processing, see `guide.webgpu.md`.

---

### Prerequisites

- **Node.js ≥ 20.19** (required by Vite 6+; Node 22 LTS recommended for new projects)
- **pnpm** (`npm install -g pnpm` if not installed)
- A GitHub account (for Pages deployment)
- Basic familiarity with TypeScript & the command line

---

### 1 · Scaffold with Vite

```bash
pnpm create vite@latest threejs-app -- --template vanilla-ts
cd threejs-app
```

Install Three.js:

```bash
pnpm add three
```

Install types (bundled with Three.js — no separate `@types/three` needed as of r152+, but verify your IDE picks them up):

```bash
pnpm add -D vite
```

#### 1.1 Update `tsconfig.json`

Vite's default `vanilla-ts` template sets `"moduleResolution": "bundler"` — this is required for `three/webgpu` and `three/tsl` subpath imports to resolve correctly. Verify it's present:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true
  }
}
```

#### 1.2 Update `vite.config.js`

Ensure the project can be served from a sub-path when hosted on GitHub Pages.
Replace `{repo-name}` with your repository name (e.g. `threejs-app`).

```js
// vite.config.js
import { defineConfig } from 'vite';

export default defineConfig({
  base: '/{repo-name}/', // e.g. '/threejs-app/'
});
```

> **Tip:** Omit the `base` property if serving from the domain root (e.g. `username.github.io`).

---

### 2 · Project Structure

```
threejs-app/
├─ public/
│  └─ assets/           ← static assets (HDR files, textures, models)
├─ src/
│  ├─ main.ts           ← entry; creates scene & renderer
│  └─ styles.css        ← basic stylesheet
├─ index.html           ← Vite entry point (not in public/)
├─ vite.config.js
├─ tsconfig.json
└─ package.json
```

> **Note:** Vite's `vanilla-ts` template places `index.html` at the project root, not in `public/`. The `<script type="module">` tag inside it is Vite's entry point.

---

### 3 · HTML Boilerplate (`index.html`)

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Three.js Starter</title>
    <link rel="stylesheet" href="/src/styles.css" />
  </head>
  <body>
    <canvas id="three-canvas"></canvas>
    <script type="module" src="/src/main.ts"></script>
  </body>
</html>
```

---

### 4 · Styling (`src/styles.css`)

Set the background colour on both `body` and `canvas` so it's visible before Three.js initialises.

```css
:root {
  --bg-colour: #0e1129; /* deep navy */
}

html,
body {
  margin: 0;
  height: 100%;
  background: var(--bg-colour);
  overflow: hidden;
}

#three-canvas {
  display: block;
  width: 100%;
  height: 100%;
  background: var(--bg-colour);
}
```

---

### 5 · Scene Boilerplate (`src/main.ts`)

Use `three/webgpu` — it provides WebGPU natively and falls back to WebGL 2 automatically when WebGPU is unavailable. No extra detection code is needed.

```ts
import * as THREE from 'three/webgpu';

// Grab canvas element
const canvas = document.getElementById('three-canvas') as HTMLCanvasElement;

// Renderer — WebGPU with automatic WebGL 2 fallback
const renderer = new THREE.WebGPURenderer({ canvas, antialias: true });
renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize(window.innerWidth, window.innerHeight);

// Background colour
const backgroundColour = 0x0e1129;
renderer.setClearColor(backgroundColour);

// Scene & Camera
const scene = new THREE.Scene();
scene.background = new THREE.Color(backgroundColour);

const camera = new THREE.PerspectiveCamera(
  60,
  window.innerWidth / window.innerHeight,
  0.1,
  1000,
);
camera.position.set(0, 0, 5);

// Simple geometry for validation
const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshStandardMaterial({ color: 0x55aaff });
const cube = new THREE.Mesh(geometry, material);
scene.add(cube);
scene.add(new THREE.AmbientLight(0xffffff, 1.5));

// Render loop — setAnimationLoop is the WebGPU-idiomatic pattern.
// It defers the first frame until async GPU init is complete.
renderer.setAnimationLoop(() => {
  cube.rotation.x += 0.01;
  cube.rotation.y += 0.015;
  renderer.render(scene, camera);
});

// Resize handler
window.addEventListener('resize', () => {
  const { innerWidth: w, innerHeight: h } = window;
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
  renderer.setSize(w, h);
});
```

> **`setAnimationLoop` vs `requestAnimationFrame`:** `WebGPURenderer` initialises asynchronously. `setAnimationLoop` defers the first render until init is complete. Using bare `requestAnimationFrame` before the GPU is ready will silently produce nothing. Always use `setAnimationLoop` with `WebGPURenderer`.

> **`Timer` vs `Clock`:** `THREE.Clock` is deprecated as of r183. Use `THREE.Timer` for elapsed/delta time in new projects:
> ```ts
> const timer = new THREE.Timer();
> renderer.setAnimationLoop(() => {
>   timer.update();
>   const delta = timer.getDelta();
>   // ...
> });
> ```

---

### 6 · Local Development

```bash
pnpm dev
```

Visit the printed localhost URL and verify:

1. Background colour fills the viewport immediately.
2. The spinning cube renders correctly.
3. Resizing the window maintains aspect ratio and fills the viewport.

---

### 7 · Deploy to GitHub Pages

See `guide.deployment.github-pages.md` for the full workflow. Key steps:

1. Commit & push to GitHub.
2. Add the Pages workflow (sample YAML in the deployment guide).
3. Ensure `vite.config.js` `base` matches your repo path.
4. Enable Pages on the repository and set the source to **GitHub Actions**.

> **Note:** Always deploy the built `dist/` output, never raw source. Vite rewrites asset paths during build.

---

### Further Reading

- `guide.webgpu.md` — WebGPURenderer in depth: TSL shaders, NodeMaterials, RenderPipeline post-processing
- `guide.lighting.md` — lighting patterns, intensity model, HDR environment maps
- [Three.js Fundamentals](https://threejsfundamentals.org/)
- [Discover Three.js](https://discoverthreejs.com/)
- [Vite docs](https://vitejs.dev/)
