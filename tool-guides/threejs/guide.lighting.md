---
docType: guide
layer: tool-guide
tool: threejs
subject: lighting
audience: [human, ai]
description: Best practices for lighting Three.js scenes
dateUpdated: 20260121
---

# Three.js Lighting Guide

To ensure your Three.js scene is properly lit and visible, follow these key steps and best practices.

## Combine Multiple Light Types

- **Ambient Light:** Start with an `AmbientLight` to provide a base level of illumination. This ensures all objects are at least partially visible, as ambient light uniformly brightens the entire scene without casting shadows.

  ```js
  const ambientLight = new THREE.AmbientLight(0x404040, 1); // Soft white light, intensity 1
  scene.add(ambientLight);
  ```
  Ambient light alone can make your scene visible but may look flat without additional light sources[1][3][6].

- **Directional Light:** Add a `DirectionalLight` to simulate sunlight or strong directional sources. This light casts shadows and creates depth.

  ```js
  const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
  directionalLight.position.set(0, 10, 10); // Position above and in front
  scene.add(directionalLight);
  ```
  Pairing ambient and directional lights is a common and effective setup for most scenes[1][3][6].

- **Point and Spot Lights:** Use `PointLight` for omnidirectional light from a specific point, or `SpotLight` for focused, cone-shaped beams. These are useful for highlighting objects or creating localized effects.

  ```js
  const pointLight = new THREE.PointLight(0xffffff, 1, 100);
  pointLight.position.set(10, 10, 10);
  scene.add(pointLight);
  ```

  Adjust the position, intensity, and color of these lights to achieve the desired effect[2][3][5].

## Adjust Light Properties

- **Intensity:** Tune the intensity of each light to avoid over- or underexposure.
- **Position:** Experiment with light positions to highlight important scene features and avoid flat or unrealistic shading.
- **Color:** Use subtle color variations for realism, but avoid extreme colors unless stylistically intended[1][3].

## Use Appropriate Materials

- Use materials that respond to lighting, such as `MeshStandardMaterial` or `MeshLambertMaterial`. Materials like `MeshBasicMaterial` do not react to lights and are only useful for debugging or stylized effects[7].

## Add Light Helpers (for Development)

- Use helpers like `THREE.DirectionalLightHelper` or `THREE.PointLightHelper` to visualize light positions and directions during development. This helps diagnose why certain objects may appear too dark or too bright[7].

## Consider Hemisphere Light

- `HemisphereLight` provides a gradient between sky and ground colors, simulating outdoor lighting and adding realism with minimal setup[6].

  ```js
  const hemiLight = new THREE.HemisphereLight(0xffffff, 0x444444, 1);
  scene.add(hemiLight);
  ```

## Common Pitfalls to Avoid

- **Too Few Lights:** Relying on a single light often results in poor visibility or flat shading. Combine different light types for best results[1][3][7].
- **Incorrect Light Position:** Lights positioned behind or inside objects may not illuminate the scene as expected. Always check and adjust positions[2][5].
- **Wrong Material:** Using non-light-reactive materials (like `MeshBasicMaterial`) will make objects appear flat regardless of lighting[7].

## Example Minimal Lighting Setup

```js
const ambientLight = new THREE.AmbientLight(0x404040, 1);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
directionalLight.position.set(0, 10, 10);
scene.add(directionalLight);
```

## Summary Table

| Light Type         | Purpose                                   | Example Use                   |
|--------------------|-------------------------------------------|-------------------------------|
| AmbientLight       | Base illumination, no shadows             | General scene visibility      |
| DirectionalLight   | Sunlight, strong shadows                  | Outdoor scenes, shadows       |
| PointLight         | Omnidirectional, localized lighting       | Lamps, bulbs                  |
| SpotLight          | Focused, cone-shaped lighting             | Spotlights, stage lights      |
| HemisphereLight    | Sky-ground gradient, soft outdoor effect  | Outdoor, natural lighting     |

By thoughtfully combining these techniques and adjusting properties, you can ensure your Three.js scene is well-lit and visually compelling[1][3][6].

Sources
[1] Illuminating Your 3D Scenes: A Guide to Lights in Three.js https://dev.to/cloudysarah/illuminating-your-3d-scenes-a-guide-to-lights-in-threejs-93i
[2] Lighting - adding lights to your three.js scene https://builderof.neocities.org/Lights
[3] How to Use Lighting in Three.js:A Step-by-Step Guide - MapToDev https://www.maptodev.com/blog/How-to-Use-Lighting-in-Three.js-A-Step-by-Step-Guide
[4] Three.js Lighting Tutorial (JavaScript) | Light Types Explained! https://www.youtube.com/watch?v=T6PhV4Hz0u4
[5] Three.js Lighting Tutorial with Examples - YouTube https://www.youtube.com/watch?v=bsLosbweLNE
[6] Ambient Lighting: Illumination from Every Direction - Discover three.js! https://discoverthreejs.com/book/first-steps/ambient-lighting/
[7] Improve lighting in three.js scene - javascript - Stack Overflow https://stackoverflow.com/questions/38020355/improve-lighting-in-three-js-scene
[8] How can I improve the lighting in my scene? White pieces are either ... https://www.reddit.com/r/threejs/comments/11wdhot/how_can_i_improve_the_lighting_in_my_scene_white/
[9] Looking for someone to help teach me lighting - three.js forum https://discourse.threejs.org/t/looking-for-someone-to-help-teach-me-lighting/14410
[10] Material ignoring specific light source? - Questions - three.js forum https://discourse.threejs.org/t/material-ignoring-specific-light-source/43747
[11] Three.js Realistic Lighting Setup Tutorial - YouTube https://www.youtube.com/watch?v=7GGNzryHfTw
[12] Rendering Lights in three js - Questions https://discourse.threejs.org/t/rendering-lights-in-three-js/58400
[13] Light – three.js docs https://threejs.org/docs/api/en/lights/Light.html
[14] Having problems with lightning - Questions - three.js forum https://discourse.threejs.org/t/having-problems-with-lightning/60606
[15] Setting up the lights - Questions - three.js forum https://discourse.threejs.org/t/setting-up-the-lights/10470
[16] Lighting advice - Questions - three.js forum https://discourse.threejs.org/t/lighting-advice/36629
[17] AmbientLight – three.js docs https://threejs.org/docs/api/en/lights/AmbientLight.html
[18] ThreeJS Lighting or Color Problems - Questions - three.js forum https://discourse.threejs.org/t/threejs-lighting-or-color-problems/74215
[19] Talk to me about point lights and performance - three.js forum https://discourse.threejs.org/t/talk-to-me-about-point-lights-and-performance/48258
[20] Showing a model only in light - Questions - three.js forum https://discourse.threejs.org/t/showing-a-model-only-in-light/26622
