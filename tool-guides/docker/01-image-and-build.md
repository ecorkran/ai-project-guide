---
layer: tool-guide
tool: Docker
docType: guide
description: Building images correctly — build-time vs runtime work, pinning for reproducibility, generated config
dependsOn: [00-introduction.md]
dateCreated: 20260915
dateUpdated: 20260915
---

# Docker Image & Build Guide

Covers what belongs in the Dockerfile versus the entrypoint, and how to keep a build reproducible.

## Build-Time vs. Runtime Work

Anything that can fail should fail as early as possible, and as loudly as possible. A build step fails the build, with full log output, blocking a bad image from ever being tagged. The same failure moved to runtime (or worse, to first-request handling) surfaces as a production incident.

**Belongs at build time:**
- Dependency installation (`npm ci`, `pip install`, `bundle install`)
- Asset compilation (webpack/vite bundles, CSS builds, static site generation)
- Code generation and compilation steps
- Anything that only depends on the source tree, not on runtime secrets or a live backing service

**Belongs at runtime (entrypoint or application startup):**
- Anything that needs a secret not available at build time
- Anything that needs a live connection to another service (a database migration that must run against the actual target database, for example)
- Anything that legitimately differs per-environment and isn't just config

**A build step can often run without its usual backing services.** Asset compilation, static analysis, and dependency installs frequently don't need a database or cache running — they need the source tree and a package registry. If a build step in your pipeline requires a live service, check whether that's a real requirement or an artifact of running the same command in dev and in CI without separating the two concerns.

```dockerfile
# Wrong: install and start assumed to happen in the same environment
FROM node:20
COPY . .
RUN npm ci
CMD ["npm", "run", "start"]
```

```dockerfile
# Better: multi-stage — build artifacts don't carry devDependencies or source into the runtime image
FROM node:20 AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-slim AS runtime
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY --from=build /app/node_modules ./node_modules
COPY package*.json ./
CMD ["node", "dist/main.js"]
```

## Pinning for Reproducibility

A build that resolves a different artifact tomorrow is not the build that was verified today. This applies to three layers, each with its own failure mode:

**Base images.** `FROM node:20` floats across patch releases; `FROM node:20.11.1-slim` or a digest pin (`FROM node@sha256:...`) does not. Prefer a digest pin when the base image is a security-sensitive dependency (it usually is); a full version tag is an acceptable minimum.

**Downloaded binaries.** A `curl | tar` step that fetches "latest" from a release page is a floating dependency exactly like an unpinned package. Pin the exact version in the URL, and verify the download against a published checksum:

```dockerfile
# Wrong: resolves whatever "latest" points to on the day this layer builds
RUN curl -fsSL https://example.com/tool/latest/tool-linux-amd64 -o /usr/local/bin/tool

# Correct: exact version, checksum verified
ARG TOOL_VERSION=1.4.2
ARG TOOL_SHA256=<published checksum for this exact version/arch>
RUN curl -fsSL "https://example.com/tool/v${TOOL_VERSION}/tool-linux-amd64" -o /usr/local/bin/tool \
    && echo "${TOOL_SHA256}  /usr/local/bin/tool" | sha256sum -c - \
    && chmod +x /usr/local/bin/tool
```

**Package manager lockfiles.** Commit and use the lockfile (`package-lock.json`, `poetry.lock`, `Gemfile.lock`) and install from it (`npm ci`, not `npm install`) so the build doesn't silently pick up a new transitive version.

## Generated Config Over a Second Hand-Maintained Copy

When a container needs a config file that's a variant of one that already exists elsewhere in the project (a cron schedule derived from an app-level job registry, a nginx config derived from a shared route table), generate it from the source of truth at build or start time rather than hand-maintaining a parallel copy.

A hand-maintained second copy drifts silently: nothing fails when the source changes and the copy doesn't, until behavior diverges in a way that's hard to trace back to "the container's copy is stale."

```dockerfile
# Wrong: crontab hand-written and copied in, independent of the app's own job definitions
COPY docker/crontab /etc/cron.d/app-cron

# Better: generate the crontab from the app's existing job registry at build time
COPY docker/generate-crontab.sh /tmp/generate-crontab.sh
RUN /tmp/generate-crontab.sh app/jobs.yaml > /etc/cron.d/app-cron
```

If the filter/generation script doesn't exist yet, writing it is usually cheaper over the project's lifetime than maintaining the drift by hand — treat request for "just copy this file in" as a prompt to check whether a source of truth already exists.

## Multi-Stage Builds

Use multi-stage builds whenever the toolchain needed to build differs from the toolchain needed to run:

- Compilers, dev dependencies, and source-only tooling stay in the `build` stage and never reach the final image.
- The final stage copies only build **artifacts** (compiled binaries, `dist/` output, production dependencies).
- This shrinks the attack surface and image size, and prevents dev-only tooling from being reachable in production.

## Version History

- **2026-09-15** — Initial guide: build-time vs runtime work, pinning, generated config, multi-stage builds.
