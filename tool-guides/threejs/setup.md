---
docType: tool-guide
platform: threejs
audience:
  - human
  - ai
purpose: installation & project setup
dateUpdated: 20250718
---

## Three.js Setup Guide

This guide walks you through scaffolding a modern Three.js project with **Vite**, applying a default background colour, registering a resize handler, and preparing the project for deployment to **GitHub Pages**.

---

### Prerequisites
- **Node.js ≥ 18** (ensure `npm`, `pnpm`, or `yarn` is available)
- A GitHub account (for Pages deployment)
- Basic familiarity with JavaScript & the command line

---

### 1 · Scaffold with Vite

Create a fresh project folder and initialise Vite (Vanilla TS template recommended):

```bash
npm create vite@latest threejs-app -- --template vanilla-ts
cd threejs-app
```

Install Three.js:

```bash
npm i three
```

#### 1.1 Update `vite.config.js`

Ensure the project can be served from a sub-path when hosted on GitHub Pages.  
Replace `{repo-name}` with your repository name (e.g. `threejs-app`).

```js
// vite.config.js
import { defineConfig } from 'vite';

export default defineConfig({
  base: '/{repo-name}/', // e.g. '/threejs-app/'
});
```

> **Tip:** Skip the `base` property if you will serve from the domain root (e.g. `username.github.io`).

---

### 2 · Project Structure

```
threejs-app/
├─ public/
│  └─ index.html        ← canvas lives here
├─ src/
│  ├─ main.ts           ← entry; creates scene & renderer
│  └─ styles.css        ← basic stylesheet
├─ vite.config.js
└─ package.json
```

---

### 3 · HTML Boilerplate (`public/index.html`)

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

Set a visible default background colour on **both** the `body` and the `canvas` so the colour is obvious before Three.js initialises.

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
  display: block;        /* removes scrollbars */
  width: 100%;
  height: 100%;
  background: var(--bg-colour);
}
```

---

### 5 · Scene Boilerplate (`src/main.ts`)

```ts
import * as THREE from 'three';

// Grab canvas element
const canvas = document.getElementById('three-canvas') as HTMLCanvasElement;

// Renderer
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize(window.innerWidth, window.innerHeight);

// *** Default background colour applied to BOTH renderer & scene ***
const backgroundColour = 0x0e1129; // same colour as CSS var
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
scene.add(camera);

// Simple geometry for validation
const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshStandardMaterial({ color: 0x55aaff });
const cube = new THREE.Mesh(geometry, material);
scene.add(cube);
scene.add(new THREE.AmbientLight(0xffffff, 0.8));

// Render loop
const tick = () => {
  cube.rotation.x += 0.01;
  cube.rotation.y += 0.015;
  renderer.render(scene, camera);
  requestAnimationFrame(tick);
};
requestAnimationFrame(tick);

// *** Resize Handler ***
window.addEventListener('resize', () => {
  const { innerWidth: w, innerHeight: h } = window;
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
  renderer.setSize(w, h);
});
```

---

### 6 · Local Development

```bash
npm run dev
```

Visit the printed localhost URL and verify:

1. The background colour fills the viewport immediately.
    
2. The spinning cube renders and keeps the background colour.
    
3. Resizing the window maintains aspect and fills the viewport.
    

---

### 7 · Deploy to GitHub Pages

This guide intentionally keeps deployment details concise; see **`deployment.github-pages.md`** in the same folder for full instructions. Key steps:

1. Commit & push to GitHub.
    
2. Add the Pages workflow (sample YAML in `deployment.github-pages.md`).
    
3. Ensure `vite.config.js` `base` matches your repo path.
    
4. Enable Pages on the _repository_ (or hub-repo) and set the branch to **GitHub Actions**.
    

> **Note:** Because Vite rewrites asset paths during build, never upload un-built source to Pages.

---

### Further Reading

- [Three.js Fundamentals](https://threejsfundamentals.org/)
    
- [Discover Three.js](https://discoverthreejs.com/)
    
- Vite docs: [https://vitejs.dev/](https://vitejs.dev/)