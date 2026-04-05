---
docType: tool-guide
layer: tool-guide
platform: threejs
audience: [human, ai]
purpose: 3d graphics and animation
dateCreated: 20250718
dateUpdated: 20260405
status: in_progress
---

# Introduction to Three.js

## Overview

Three.js is an open-source JavaScript library for WebGL- and WebGPU-powered 3D graphics. It provides a high-level API for scenes, cameras, lights, geometries, and materials — ideal for interactive visualizations, games, and animations.

As of r171 (September 2025), Three.js ships a unified `three/webgpu` entry point that uses WebGPU natively with automatic WebGL 2 fallback. **New projects should target WebGPU as the primary renderer.** See `guide.webgpu.md` for the full WebGPU guide.

## Who should use this guide?

- **Humans:** Front-end or full-stack developers needing to embed 3D content in web apps.
- **AIs/scripts:** Scaffolding tools that want to detect "this is the Three.js tool-guide."

## Prerequisites

- A modern browser (WebGPU supported in Chrome 113+, Edge 113+, Firefox 141+, Safari 26+)
- Node.js ≥ 20.19 (required by Vite 6+)
- pnpm (preferred), npm, or yarn
- Basic familiarity with JavaScript/TypeScript and ES modules

## What you'll learn

1. How to scaffold a minimal Three.js project with Vite
2. Core concepts (scene, camera, renderer)
3. Adding lights, materials, and meshes
4. Using WebGPURenderer with automatic WebGL 2 fallback
5. Performance tuning and debugging
6. Where to find deeper dives (WebGPU, lighting, deployment)

## Structure of this folder

- `introduction.md` — this file
- `setup.md` — installation & project setup (Vite + pnpm, WebGPURenderer boilerplate)
- `overview.md` — fundamentals, best practices, and common pitfalls
- `guide.webgpu.md` — WebGPURenderer, TSL shaders, NodeMaterials, RenderPipeline post-processing
- `guide.lighting.md` — lighting patterns, intensity model, environment maps
- `guide.deployment.github-pages.md` — deploying Vite + Three.js to GitHub Pages
