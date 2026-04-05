---
docType: tool-guide
layer: tool-guide
platform: threejs
audience: [human, ai]
purpose: lighting patterns, intensity model, and environment maps
dateCreated: 20260121
dateUpdated: 20260405
status: in_progress
---

# Three.js Lighting Guide

## Physically Correct Lighting (r155+)

Three.js uses physically correct lighting by default since r155 (2023). The `useLegacyLights` escape hatch was removed in r165 — there is no way to revert to the old model.

**What this means in practice:**

- `AmbientLight`, `DirectionalLight`, `HemisphereLight` intensities are in **lux (lx)**. A sunny outdoor scene is ~100,000 lux; an indoor scene might be 100–1000 lux.
- `PointLight` and `SpotLight` intensities are in **candela (cd)**. A domestic bulb is ~800 cd.
- Pre-r155 tutorials often used intensity values of `0.5` or `1.0` for `DirectionalLight`. These were legacy-mode values. In physical mode, the same appearance requires multiplying by `Math.PI` (~3.14). A legacy `intensity: 1` DirectionalLight becomes `intensity: Math.PI` in physical mode.
- `ColorManagement.enabled = true` is the default since r152. sRGB-to-linear conversion is automatic — do not manually linearise colours.

**Practical starting values (physical mode):**

| Light type | Typical starting value | Notes |
|---|---|---|
| `AmbientLight` | `intensity: 1.5` | Very subtle fill; reduce if using HDR environment |
| `DirectionalLight` | `intensity: Math.PI` | Approximates pre-r155 `intensity: 1` appearance |
| `HemisphereLight` | `intensity: 1.5` | Good outdoor sky/ground fill |
| `PointLight` | `intensity: 100` | Decay is `2` by default (inverse-square) |
| `SpotLight` | `intensity: 100` | Same decay model as PointLight |

> **If your scene is much darker than expected:** multiply your intensity values by `Math.PI` and tune from there. This is the most common pitfall when following older tutorials.

---

## Combine Multiple Light Types

### Ambient Light

Provides uniform base illumination — no shadows, no directionality.

```js
const ambientLight = new THREE.AmbientLight(0x404040, 1.5);
scene.add(ambientLight);
```

Ambient light alone looks flat. Use it as a fill to prevent objects from being completely black on their unlit sides. When using an HDR environment map (see below), you often don't need ambient light at all.

### Directional Light

Simulates sunlight — parallel rays, casts shadows, creates depth.

```js
const directionalLight = new THREE.DirectionalLight(0xffffff, Math.PI);
directionalLight.position.set(5, 10, 7);
directionalLight.castShadow = true;
scene.add(directionalLight);
```

`castShadow = true` enables shadow maps. Configure the shadow camera frustum to tightly wrap your scene:

```js
directionalLight.shadow.camera.near = 0.5;
directionalLight.shadow.camera.far = 50;
directionalLight.shadow.camera.left = -10;
directionalLight.shadow.camera.right = 10;
directionalLight.shadow.camera.top = 10;
directionalLight.shadow.camera.bottom = -10;
directionalLight.shadow.mapSize.set(2048, 2048);
```

### Point and Spot Lights

```js
// Point light — omnidirectional from a specific position
const pointLight = new THREE.PointLight(0xffffff, 100, 20); // colour, intensity (cd), distance
pointLight.position.set(3, 5, 3);
scene.add(pointLight);

// Spot light — focused cone
const spotLight = new THREE.SpotLight(0xffffff, 100);
spotLight.position.set(5, 10, 0);
spotLight.angle = Math.PI / 8;    // cone half-angle
spotLight.penumbra = 0.2;         // soft edge
spotLight.castShadow = true;
scene.add(spotLight);
```

### Hemisphere Light

Sky-ground gradient — excellent cheap outdoor fill without needing a sun light for basic scenes.

```js
const hemiLight = new THREE.HemisphereLight(
  0x87ceeb, // sky colour (blue-ish)
  0x444444, // ground colour
  1.5
);
scene.add(hemiLight);
```

---

## HDR Environment Maps (Recommended for Realistic Scenes)

For physically realistic lighting and reflections, an HDR environment map via `PMREMGenerator` is the standard approach. It provides both diffuse and specular IBL (image-based lighting) and typically replaces or supplements direct lights.

### `RGBELoader` → `HDRLoader` (r179 breaking rename)

`RGBELoader` was renamed to `HDRLoader` in r179. Update all imports:

```js
// Old (r178 and earlier) — no longer works
import { RGBELoader } from 'three/addons/loaders/RGBELoader.js';

// Current (r179+)
import { HDRLoader } from 'three/addons/loaders/HDRLoader.js';
```

### Setup

```ts
import * as THREE from 'three/webgpu';
import { HDRLoader } from 'three/addons/loaders/HDRLoader.js';

async function setupEnvironment(renderer: THREE.WebGPURenderer, scene: THREE.Scene) {
  await renderer.init(); // ensure renderer is ready before PMREMGenerator

  const pmrem = new THREE.PMREMGenerator(renderer);
  pmrem.compileEquirectangularShader();

  const hdrLoader = new HDRLoader();
  const hdrTexture = await hdrLoader.loadAsync('/assets/env/studio.hdr');

  const envMap = pmrem.fromEquirectangular(hdrTexture).texture;
  hdrTexture.dispose();
  pmrem.dispose();

  scene.environment = envMap;   // IBL lighting for all PBR materials
  scene.background = envMap;    // optional: visible in background
  scene.backgroundBlurriness = 0.05; // optional: blur the background only
}
```

`scene.environment` applies IBL to all `MeshStandardMaterial` and `MeshPhysicalMaterial` meshes automatically. With a good HDR environment you often need only minimal or no direct lights.

### Free HDR Sources

- [Poly Haven](https://polyhaven.com/hdris) — CC0 licensed, production quality

---

## Use Appropriate Materials

- `MeshStandardMaterial` — PBR (physically based), responds to lights and environment maps. Use for most objects.
- `MeshPhysicalMaterial` — extends Standard with clearcoat, transmission, iridescence, sheen. Use for glass, wet surfaces, fabric.
- `MeshLambertMaterial` — diffuse only, no specular. Cheaper than Standard for non-metallic, non-reflective objects.
- `MeshBasicMaterial` — ignores all lights. Use for UI elements, emissive overlays, or lighting debug.

> Do not use `MeshBasicMaterial` for primary scene objects expecting lighting — they will appear flat and unlit regardless of your light setup.

---

## Light Helpers (Development Only)

Visualise light positions and directions during development. Remove before shipping.

```js
const dirHelper = new THREE.DirectionalLightHelper(directionalLight, 2);
scene.add(dirHelper);

const pointHelper = new THREE.PointLightHelper(pointLight, 0.5);
scene.add(pointHelper);

// For directional light shadow camera:
const shadowHelper = new THREE.CameraHelper(directionalLight.shadow.camera);
scene.add(shadowHelper);
```

---

## Minimal Physically Correct Setup

```js
import * as THREE from 'three/webgpu';

// Hemisphere fill (sky/ground gradient)
const hemiLight = new THREE.HemisphereLight(0x87ceeb, 0x444444, 1.5);
scene.add(hemiLight);

// Directional sun
const sun = new THREE.DirectionalLight(0xffffff, Math.PI);
sun.position.set(5, 10, 7);
sun.castShadow = true;
scene.add(sun);

// Enable shadows on renderer
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
```

---

## Summary Table

| Light Type | Purpose | Physical Unit | Typical Range |
|---|---|---|---|
| `AmbientLight` | Flat fill, no shadows | lux (lx) | 0.5 – 3 |
| `DirectionalLight` | Sunlight, shadows | lux (lx) | `Math.PI` – 10 |
| `HemisphereLight` | Sky/ground gradient fill | lux (lx) | 1 – 3 |
| `PointLight` | Omnidirectional bulb | candela (cd) | 50 – 1000 |
| `SpotLight` | Focused cone | candela (cd) | 50 – 1000 |
| HDR environment | IBL: diffuse + specular | — | `scene.environment` |

## Common Pitfalls

- **Scene too dark:** Likely pre-r155 intensity values — multiply by `Math.PI` and tune.
- **Wrong material:** `MeshBasicMaterial` ignores lights. Swap to `MeshStandardMaterial` to test lighting.
- **Light behind objects:** Lights positioned behind or inside objects may not illuminate them. Check with helpers.
- **`RGBELoader` import error:** Renamed to `HDRLoader` in r179.
- **Shadows not visible:** Check `renderer.shadowMap.enabled = true`, `light.castShadow = true`, and `mesh.receiveShadow = true` on receiving surfaces.
