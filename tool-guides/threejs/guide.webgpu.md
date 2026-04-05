---
docType: tool-guide
layer: tool-guide
platform: threejs
audience: [human, ai]
purpose: WebGPURenderer, TSL shaders, NodeMaterials, and RenderPipeline post-processing
dateCreated: 20260405
dateUpdated: 20260405
status: in_progress
---

# Three.js WebGPU Guide

**Target: Three.js r183+ with `three/webgpu` as the primary renderer.**

WebGPU is the primary rendering target for new Three.js projects. Since r171 (September 2025), the `three/webgpu` entry point provides a production-ready `WebGPURenderer` with automatic WebGL 2 fallback — no detection code needed. WebGPU is supported in ~95% of browsers globally; the remaining ~5% fall back silently to WebGL 2.

---

## Browser Support (April 2026)

| Browser | Desktop | Mobile |
|---|---|---|
| Chrome | Full (v113+, 2023) | Android 12+ (v121+) |
| Edge | Full (v113+) | Same as Chrome |
| Firefox | Windows v141+; macOS Apple Silicon v145+ | In progress |
| Safari | macOS Tahoe 26+ (Safari 26, Sept 2025) | iOS 26+, iPadOS 26+ |

**Linux desktop:** Chrome v144+ on Intel Gen12+; Firefox Nightly only.

---

## Import Strategy

Use `three/webgpu` — not `three` — as the import source for all WebGPU projects. It exports everything from `three` plus `WebGPURenderer`, all NodeMaterials, and bundled TSL support.

```ts
// All core Three.js + WebGPURenderer
import * as THREE from 'three/webgpu';

// TSL functions — composable shader building blocks
import { Fn, uniform, vec2, vec3, vec4, float, color,
         uv, time, deltaTime,
         positionLocal, positionWorld, normalLocal, normalWorld,
         texture, mix, clamp, smoothstep, sin, cos, pow,
         If, Loop } from 'three/tsl';
```

**Do not mix `import * as THREE from 'three'` and `import * as THREE from 'three/webgpu'`** in the same project — they create conflicting shader compilation contexts.

Addons still come from `three/addons/`:

```ts
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { HDRLoader } from 'three/addons/loaders/HDRLoader.js';
```

### TypeScript: `tsconfig.json`

The `three/webgpu` and `three/tsl` subpath exports require `"moduleResolution": "bundler"` (Vite's default). Verify this is set:

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

---

## Renderer Setup

### Standard: `setAnimationLoop` pattern

`WebGPURenderer` initialises asynchronously (GPU adapter + device request). `setAnimationLoop` defers the first frame until init is complete — this is the recommended pattern. Do not use bare `requestAnimationFrame` with `WebGPURenderer`.

```ts
import * as THREE from 'three/webgpu';

const renderer = new THREE.WebGPURenderer({ antialias: true });
renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setAnimationLoop(render); // defers until GPU ready
document.body.appendChild(renderer.domElement);

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 5;

const timer = new THREE.Timer(); // use Timer, not deprecated Clock

function render() {
  timer.update();
  const delta = timer.getDelta();
  renderer.render(scene, camera);
}

window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
```

### When you need explicit `await renderer.init()`

If you need to use the renderer (e.g. for `PMREMGenerator` or render targets) before the loop starts, await init explicitly:

```ts
async function init() {
  const renderer = new THREE.WebGPURenderer({ antialias: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  document.body.appendChild(renderer.domElement);

  await renderer.init(); // must await before PMREMGenerator, render targets, etc.

  const pmrem = new THREE.PMREMGenerator(renderer);
  // ... setup environment, load assets ...

  renderer.setAnimationLoop(render);
}

init();
```

### Constructor Options

| Option | Default | Notes |
|---|---|---|
| `antialias` | `false` | MSAA (4 samples). Disable when using `RenderPipeline` post-processing — use `fxaa()` or `smaa()` instead |
| `alpha` | `true` | Transparent canvas background |
| `forceWebGL` | `false` | Force WebGL 2 backend (for testing fallback path) |
| `outputBufferType` | `HalfFloatType` | Use `UnsignedByteType` if you need maximum compat |
| `reversedDepthBuffer` | `false` | Improves depth precision on modern GPUs (r183+) |

### Checking which backend is active

```ts
await renderer.init();
const isWebGPU = renderer.backend.isWebGPUBackend;
console.log(isWebGPU ? 'WebGPU' : 'WebGL 2 (fallback)');
```

---

## What Works and What Doesn't

### Not Supported in WebGPURenderer

| Feature | Replacement |
|---|---|
| `ShaderMaterial` | `MeshStandardNodeMaterial` + TSL |
| `RawShaderMaterial` | `MeshBasicNodeMaterial` + TSL |
| `onBeforeCompile()` | NodeMaterial `*Node` slots |
| `EffectComposer` and its passes | `RenderPipeline` + TSL effects |
| `WebGLCubeRenderTarget` | `CubeRenderTarget` |
| `GPUComputationRenderer` (WebGL GPGPU) | TSL `compute()` nodes |
| Compute shaders (WebGL 2 fallback) | WebGPU-only; no fallback |

### Still Works Unchanged

- All standard materials (`MeshStandardMaterial`, `MeshPhysicalMaterial`, etc.)
- All built-in geometries
- `GLTFLoader`, `OBJLoader`, and most asset loaders
- `OrbitControls`, `TransformControls` (see note below), and other control addons
- `PMREMGenerator` and `HDRLoader`
- `InstancedMesh`, `BatchedMesh`
- `AnimationMixer`
- `CSS2DRenderer`, `CSS3DRenderer`

> **`TransformControls` (r170 change):** The visual helper is no longer added directly to the scene. Use `controls.getHelper()`:
> ```ts
> const controls = new TransformControls(camera, renderer.domElement);
> scene.add(controls.getHelper()); // not scene.add(controls)
> ```

---

## TSL — Three.js Shading Language

TSL is a JavaScript-based shader system that compiles to **WGSL** (WebGPU) or **GLSL** (WebGL 2 fallback). It replaces GLSL strings entirely. You compose typed node graphs using JavaScript functions — no shader strings, no manual varying declarations, no `#ifdef` guards.

### Why TSL

- Single code path for both backends — same TSL compiles to WGSL or GLSL automatically
- Full JavaScript integration — closures, imports, TypeScript types, tree-shaking
- Composable and refactorable — shader logic is a function graph, not a string
- Automatic optimization: dead code elimination, varying deduplication, expression caching
- Same system used for materials AND post-processing effects

### Core Primitives

```ts
import { Fn, uniform, vec3, vec4, float, color,
         uv, time, sin, mix, texture,
         positionLocal, normalLocal } from 'three/tsl';

// Typed value constructors
vec3(1, 0, 0)           // vec3 constant
float(0.5)              // float constant
color(0xff6600)         // Color from hex

// Chained math (method style)
vec3(1, 0, 0).mul(2).add(vec3(0, 1, 0))

// Functional style (same result)
import { add, mul } from 'three/tsl';
add(mul(vec3(1, 0, 0), 2), vec3(0, 1, 0))

// Built-in varying inputs
uv()            // UV coordinates (vec2)
time            // elapsed time in seconds (float, auto-updating)
deltaTime       // frame delta (float, auto-updating)
positionLocal   // vertex position in object space
positionWorld   // vertex position in world space
normalLocal     // vertex normal in object space
normalWorld     // vertex normal in world space
```

### `uniform()` — GPU-Updatable Values

```ts
import { uniform } from 'three/tsl';
import * as THREE from 'three/webgpu';

// Create a uniform — update .value from JavaScript at any time
const myColor = uniform(new THREE.Color(0xff6600));
const myFloat = uniform(0.5);

// Use in a material
material.colorNode = myColor;

// Update at runtime — no shader recompile
myColor.value.set(0x00ff88);
myFloat.value = 0.8;
```

### `Fn()` — Custom Shader Functions

`Fn()` defines a reusable shader function. Call it to get a node that can be assigned to a material slot.

```ts
import { Fn, uv, time, sin, mix, color, vec4 } from 'three/tsl';

const waveColor = Fn(() => {
  const wave = sin(uv().x.mul(10).add(time)).mul(0.5).add(0.5);
  return mix(color(0xff6600), color(0x0044ff), wave);
});

const material = new THREE.MeshBasicNodeMaterial();
material.colorNode = waveColor(); // call to create a node instance
```

### Control Flow

```ts
import { Fn, If, float, vec3 } from 'three/tsl';

const clampHeight = Fn(({ pos }: { pos: ReturnType<typeof vec3> }) => {
  const result = vec3(pos);
  If(result.y.greaterThan(10), () => {
    result.y.assign(10);
  }).ElseIf(result.y.lessThan(0), () => {
    result.y.assign(0);
  });
  return result;
});
```

### GLSL → TSL Quick Reference

| GLSL | TSL |
|---|---|
| `vUv` | `uv()` |
| `vWorldPosition` | `positionWorld` |
| `vNormal` | `normalView` |
| `gl_FragColor` | `material.fragmentNode` |
| `uniform float x` | `uniform(0.0)` |
| `vec3(1.0, 0.0, 0.0)` | `vec3(1, 0, 0)` |
| `a * b` | `a.mul(b)` |
| `a + b` | `a.add(b)` |
| `mix(a, b, t)` | `mix(a, b, t)` |
| `normalize(v)` | `normalize(v)` or `v.normalize()` |
| `dot(a, b)` | `dot(a, b)` |
| `texture2D(map, uv)` | `texture(map, uv())` |

---

## NodeMaterials

Every standard Three.js material has a Node counterpart. Use Node versions when you need custom shader behaviour; standard materials work unchanged for everything else.

| Standard | Node Version |
|---|---|
| `MeshStandardMaterial` | `MeshStandardNodeMaterial` |
| `MeshPhysicalMaterial` | `MeshPhysicalNodeMaterial` |
| `MeshBasicMaterial` | `MeshBasicNodeMaterial` |
| `MeshLambertMaterial` | `MeshLambertNodeMaterial` |
| `PointsMaterial` | `PointsNodeMaterial` |
| `SpriteMaterial` | `SpriteNodeMaterial` |
| `LineBasicMaterial` | `LineBasicNodeMaterial` |

Node versions accept all the same constructor properties as their standard counterparts, plus `*Node` slots that accept TSL expressions and override the corresponding property:

```ts
import * as THREE from 'three/webgpu';
import { texture, uniform, sin, time, color, float, positionLocal, normalLocal } from 'three/tsl';

const colorMap = new THREE.TextureLoader().load('/textures/color.jpg');
const roughMap = new THREE.TextureLoader().load('/textures/rough.jpg');
const tint = uniform(new THREE.Color(0xffffff));

const material = new THREE.MeshStandardNodeMaterial({
  roughness: 0.5,
  metalness: 0.0,
});

// Override individual properties with TSL nodes
material.colorNode     = texture(colorMap).mul(tint);         // replaces .color + .map
material.roughnessNode = texture(roughMap).r;                 // replaces .roughness
material.emissiveNode  = color(0x00ffff).mul(sin(time).mul(0.5).add(0.5)); // animated glow
material.aoNode        = texture(roughMap).g;                 // AO from green channel

// Vertex displacement
material.positionNode  = positionLocal.add(normalLocal.mul(sin(time).mul(0.05)));
```

When a `*Node` slot is set it completely replaces the corresponding scalar/texture property. When `null` (default), the standard property is used.

---

## RenderPipeline Post-Processing

`RenderPipeline` (renamed from `PostProcessing` in r183) is the WebGPU post-processing system. It replaces `EffectComposer` and composes effects as a TSL node graph rather than a passes array.

### Basic Setup

```ts
import * as THREE from 'three/webgpu';
import { pass, fxaa } from 'three/tsl';

// Disable MSAA on renderer — use fxaa() or smaa() in the pipeline instead
const renderer = new THREE.WebGPURenderer({ antialias: false });
renderer.setSize(window.innerWidth, window.innerHeight);

const renderPipeline = new THREE.RenderPipeline(renderer);

const scenePass = pass(scene, camera);

// Minimal: just apply FXAA
renderPipeline.outputNode = fxaa(scenePass);

// Use pipeline.render() in the loop, not renderer.render()
renderer.setAnimationLoop(() => renderPipeline.render());
```

### With Multiple Effects

```ts
import { pass, mrt, output, bloom, fxaa, ao } from 'three/tsl';
import { normalView } from 'three/tsl';

// MRT captures multiple buffers in a single render pass
scenePass.setMRT(mrt({
  output: output,
  normal: normalView,
}));

const colorTex  = scenePass.getTextureNode('output');
const normalTex = scenePass.getTextureNode('normal');
const depthTex  = scenePass.getTextureNode('depth'); // always available

// Compose effects as a node expression
const aoResult    = ao(depthTex, normalTex, camera);
const withBloom   = bloom(colorTex.mul(aoResult), { threshold: 0.8, intensity: 1.2 });
const withFXAA    = fxaa(withBloom);

renderPipeline.outputNode = withFXAA;
```

### Available Effect Nodes (import from `three/tsl`)

`bloom`, `gaussianBlur`, `grayscale`, `fxaa`, `smaa`, `ao`, `dof`, `ssr`, `ssgi`, `filmGrain`, `toneMapping`, `motionBlur`, `chromaticAberration`

### Key Differences from EffectComposer

- Effects are a **node expression tree**, not a passes array
- MRT lets a single scene render produce colour, normals, depth, and velocity simultaneously
- All effects use the same TSL compiler as materials — one backend, one code path
- Set `antialias: false` on the renderer and apply `fxaa()` or `smaa()` in the pipeline

---

## Compute Shaders (WebGPU-only)

Compute shaders run arbitrary GPU workloads outside the render pipeline. They have no WebGL 2 fallback — guard with the backend check if required.

```ts
import * as THREE from 'three/webgpu';
import { Fn, uniform, storage, float, uint, instanceIndex } from 'three/tsl';

const COUNT = 100_000;

// Storage buffer — readable and writable in compute shaders
const positionBuffer = storage(
  new THREE.StorageInstancedBufferAttribute(new Float32Array(COUNT * 3), 3),
  'vec3',
  COUNT
);

const computeFn = Fn(() => {
  const idx = instanceIndex;
  const pos = positionBuffer.element(idx);
  // Move each point upward each frame
  pos.y.addAssign(0.001);
})().compute(COUNT);

// Run compute every frame
renderer.setAnimationLoop(async () => {
  await renderer.computeAsync(computeFn);
  renderer.render(scene, camera);
});
```

> Compute workloads are where WebGPU's performance advantage is most dramatic. Particle systems that top out at ~10,000 in WebGL can run at 1,000,000+ with WebGPU compute.

---

## Performance Notes

WebGPU is not a universal speed-up over WebGL — the trade-offs depend on workload:

| Workload | WebGPU vs WebGL 2 |
|---|---|
| Compute shaders / GPU particles | Massively faster (~150x documented) |
| CPU frame overhead | ~50% lower |
| MRT post-processing | Much faster (single pass) |
| Many individual draw calls (no instancing) | Currently **slower** (~2–4x) due to a known UBO overhead issue |
| Instanced / batched rendering | Comparable or faster |

**Practical guidance:**
- Use `InstancedMesh` or `BatchedMesh` regardless of renderer — this is the single biggest draw-call optimisation
- For scenes that are currently bottlenecked on individual draw calls and cannot be instanced, `WebGLRenderer` may remain faster until the UBO issue is resolved upstream
- For everything else — especially compute-heavy or procedural work — WebGPU is the right choice

---

## Debugging

```ts
// Surface TSL/shader compilation errors clearly during development
renderer.debug.checkShaderErrors = true;

// Check which backend is active
await renderer.init();
console.log(renderer.backend.isWebGPUBackend ? 'WebGPU' : 'WebGL 2');

// Force WebGL 2 backend to test the fallback path
const renderer = new THREE.WebGPURenderer({ forceWebGL: true });
```

Chrome DevTools includes a **WebGPU** panel (alongside Network, Performance, etc.) for inspecting command encoding, texture allocations, and pipeline states.

---

## Migration from WebGLRenderer

If migrating an existing project:

1. Change import from `'three'` to `'three/webgpu'`
2. Change `new THREE.WebGLRenderer()` to `new THREE.WebGPURenderer()`
3. Change `requestAnimationFrame` render loop to `renderer.setAnimationLoop()`
4. Replace `ShaderMaterial` / `RawShaderMaterial` with TSL NodeMaterials
5. Replace `onBeforeCompile()` hooks with `*Node` material slots
6. Replace `EffectComposer` passes with `RenderPipeline` + TSL effects
7. Replace `RGBELoader` with `HDRLoader`
8. Replace `WebGLCubeRenderTarget` with `CubeRenderTarget`
9. Update `TransformControls`: use `scene.add(controls.getHelper())` not `scene.add(controls)`
10. Replace `THREE.Clock` with `THREE.Timer`
