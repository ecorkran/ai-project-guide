---
docType: tool-guide
layer: tool-guide
platform: threejs
audience: [human, ai]
purpose: 3d graphics and animation — fundamentals and best practices
dateCreated: 20250718
dateUpdated: 20260405
status: in_progress
---

## Essential Three.js Knowledge for Developers

Creating robust and efficient Three.js applications requires understanding both the fundamentals and the common pitfalls. This guide covers configuration, best practices, performance, and common challenges for Three.js r183+.

For WebGPU-specific guidance (TSL shaders, NodeMaterials, RenderPipeline post-processing), see `guide.webgpu.md`.

---

### Initial Setup and Configuration

- **Import path:** Use `import * as THREE from 'three/webgpu'` for new projects. This entry point provides `WebGPURenderer` with automatic WebGL 2 fallback — no detection code needed. The `three` entry point still works but does not include `WebGPURenderer` or NodeMaterials.
- **Scene basics:** Always create a scene, camera, and renderer. Set renderer size and append its `domElement` to the document.
- **Render loop:** Use `renderer.setAnimationLoop(fn)` rather than bare `requestAnimationFrame`. `WebGPURenderer` initialises asynchronously; `setAnimationLoop` defers the first frame until ready.
- **WebGL 2 support check:** With `three/webgpu`, fallback is automatic. You no longer need manual `WebGL.isWebGLAvailable()` checks for the renderer itself — focus feature detection on capabilities your application specifically needs (e.g. compute shaders, which are WebGPU-only).

---

### Rendering and Scene Management

- **Lighting:** Most materials require proper lighting to be visible. If you see only black objects, check your lights. Use `MeshBasicMaterial` to debug lighting issues — it does not respond to lights and will always render at full colour.
- **Camera positioning:** Objects are created at the origin by default. Move the camera back before rendering (e.g. `camera.position.z = 5`).
- **Background colour:** Set a non-black background immediately so rendering issues are obvious.
- **Scene scale:** One Three.js unit equals one metre. Scale mismatches (e.g. a model that is 0.001 units tall) can make objects invisible or tiny. Check your model's coordinate system on import.

---

### Performance Optimization

- **Reduce draw calls:** Combine geometries where possible and minimise the number of individually drawn objects. Use `InstancedMesh` for repeated geometry, `BatchedMesh` for varied static geometry.
- **`BufferGeometry`:** This is the only geometry class in Three.js — the old `Geometry` class was removed years ago. All built-in helpers and loaders already use `BufferGeometry`.
- **Texture optimisation:** Use texture atlases to reduce texture switches. Avoid textures larger than needed for the display resolution. Compress with KTX2/Basis where possible.
- **Level of Detail (LOD):** Use Three.js's `LOD` class to swap complex models for simpler ones at distance.
- **Frustum culling:** Automatic in Three.js. Objects with `mesh.frustumCulled = true` (the default) are skipped when outside the camera view.
- **Object pooling:** Reuse `Vector3`, `Matrix4`, and similar objects in hot paths to avoid GC pressure.
- **Render loop:** Keep your loop lean — avoid allocations, heavy computation, or object creation inside `setAnimationLoop`.
- **Many-draw-call scenes:** For scenes with thousands of individually drawn meshes, `WebGLRenderer` currently outperforms `WebGPURenderer` due to an acknowledged UBO overhead issue in the Three.js WebGPU implementation. Use `InstancedMesh` or `BatchedMesh` to mitigate this regardless of renderer. WebGPU is significantly faster for compute workloads and procedural/TSL materials.

---

### User Interaction and Animation

- **Input handling:** Capture pointer and keyboard events for interactive scenes. Use `Raycaster` for object picking and selection.
- **Animation timing:** Use `THREE.Timer` (not the deprecated `THREE.Clock`) for delta time in r183+. Pass delta to animation systems rather than relying on fixed increments, so animation speed is frame-rate independent.
- **Animation clips:** Use `AnimationMixer` for skeletal and morph-target animations loaded from glTF.

---

### Project Structure and Integration

- **Modular code:** Organise into ES modules — one class or concept per file. Avoid a single monolithic `main.ts`.
- **React integration:** `react-three-fiber` (R3F) v9+ provides a declarative React wrapper around Three.js with access to the full Three.js API. `@react-three/drei` is the standard companion library for helpers and abstractions. R3F v10 (in alpha) makes WebGPU first-class. See R3F docs for setup.
- **State management in R3F:** Avoid storing Three.js objects in React state — keep them in refs or Zustand stores to prevent unnecessary re-renders.

---

### Common Pitfalls

- **Memory leaks:** Always call `.dispose()` on geometries, materials, textures, and render targets when removing objects from the scene. Three.js does not automatically free GPU memory.
- **`ShaderMaterial` with WebGPURenderer:** Not supported. Custom GLSL shaders must be converted to TSL (Three.js Shading Language) for WebGPU projects. See `guide.webgpu.md`.
- **`EffectComposer` with WebGPURenderer:** Not supported. Use the `RenderPipeline` class with TSL effect nodes. `EffectComposer` still works with `WebGLRenderer` for WebGL-only projects.
- **Stale lighting intensity values:** The r155 physically-correct lighting change (2023) removed the `useLegacyLights` escape hatch as of r165. Intensity values from pre-r155 tutorials may look ~π times too dark. See `guide.lighting.md` for the current intensity model.
- **`RGBELoader` rename:** Renamed to `HDRLoader` in r179. Update imports: `import { HDRLoader } from 'three/addons/loaders/HDRLoader.js'`.
- **`Clock` deprecation:** `THREE.Clock` is deprecated in r183. Use `THREE.Timer`.
- **Cross-browser testing:** Test on multiple browsers and devices. Pay attention to WebGPU capability on mobile — Android support is hardware-dependent.

---

### Debugging Tips

- Use `scene.overrideMaterial = new THREE.MeshBasicMaterial({ color: 0xff0000 })` to confirm objects are being rendered, independent of lighting.
- Use light helpers (`DirectionalLightHelper`, `PointLightHelper`) to visualise light positions during development. Remove before shipping.
- Check the browser console for Three.js warnings — they are specific and usually point directly at the problem.
- Use the browser's built-in WebGPU inspector (Chrome DevTools → "WebGPU" panel) to profile GPU command encoding and texture usage.
- Add `renderer.debug.checkShaderErrors = true` during development to surface TSL/shader compilation errors clearly.

---

### Summary: Key Best Practices

| Area | Best Practice | Pitfall to Avoid |
|---|---|---|
| Renderer | `WebGPURenderer` via `three/webgpu` | Using `three` import — no WebGPU, no NodeMaterials |
| Render loop | `setAnimationLoop` | Bare `requestAnimationFrame` with WebGPURenderer |
| Scene setup | Proper lighting, camera position, background colour | Black screen, invisible objects |
| Performance | `InstancedMesh`, `BatchedMesh`, LOD, texture compression | Thousands of individual draw calls |
| Memory | `.dispose()` all GPU resources on removal | Memory leaks, GPU OOM crashes |
| Custom shaders | TSL via `three/tsl` + NodeMaterial | `ShaderMaterial` (not supported in WebGPURenderer) |
| Post-processing | `RenderPipeline` + TSL effects | `EffectComposer` (not supported in WebGPURenderer) |
| Timing | `THREE.Timer` | Deprecated `THREE.Clock` |
| HDR environment | `HDRLoader` + `PMREMGenerator` | `RGBELoader` (renamed in r179) |
| Project structure | ES modules, one concept per file | Monolithic `main.ts` |
