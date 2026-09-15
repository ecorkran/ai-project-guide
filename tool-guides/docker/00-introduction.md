---
layer: tool-guide
tool: Docker
docType: introduction
description: Entry point for Docker/container tool guides. Read this first to determine which guide you need.
dateCreated: 20260915
dateUpdated: 20260915
---

# Docker Tool Guide — Introduction

This is the entry point for containerization guidance. **Read the guide selection table below to find the right document for your task, rather than loading all guides into context.**

Containerization has an unusually high ratio of decisions that *look* cosmetic but are load-bearing, and they fail quietly rather than loudly. A Dockerfile written from general knowledge will typically build and start, and still be wrong in ways that only surface under load or during shutdown. These guides exist to name those decisions explicitly.

## Guide Selection

| I need to... | Read this guide |
|--------------|----------------|
| Understand what a container actually is, and the core vocabulary | **This file** (sections below) |
| Write a Dockerfile: build stages, pinning, build-time vs runtime work | **01-image-and-build.md** |
| Design an entrypoint: multi-mode dispatch, PID 1, signals, env files | **02-entrypoint-and-process-model.md** |
| Write a Compose file: health gating, startup ordering, stop windows | **03-compose-and-orchestration.md** |
| Decide whether/how to containerize a service, or port a systemd unit | **04-decision-guide.md** |

### For AI Agents: Which Guide to Load

- **Writing or reviewing a Dockerfile**: Load **01-image-and-build.md**
- **Writing or reviewing an entrypoint script, or a service that runs as several roles**: Load **02-entrypoint-and-process-model.md**
- **Writing or reviewing docker-compose.yml, `depends_on`, healthchecks**: Load **03-compose-and-orchestration.md**
- **Porting an existing systemd/service-manager unit into a container, or deciding whether containerization is the right move at all**: Load **04-decision-guide.md**

You should rarely need more than one or two guides per task. This introduction provides foundational vocabulary that all other guides assume.

---

## Core Vocabulary

**Image** — A read-only, layered filesystem snapshot plus metadata (entrypoint, default command, exposed ports, env). Built once from a Dockerfile, run many times.

**Container** — A running (or stopped) instance of an image: the image's filesystem plus a writable layer, an isolated process namespace, and its own network namespace.

**Build time vs. runtime** — Build time is `docker build`: it produces the image and nothing else is running. Runtime is `docker run` / `docker compose up`: the image becomes a live process. Anything that can fail should fail as early as possible — prefer build time over runtime, and runtime startup over first-request handling. See **01-image-and-build.md**.

**Entrypoint vs. command** — The entrypoint is the fixed executable a container always runs; the command is the (often overridable) arguments passed to it. Conflating them makes a container hard to invoke in more than one way. See **02-entrypoint-and-process-model.md**.

**PID 1** — The first process in a container's PID namespace inherits init-like responsibilities (reaping zombies, handling signals) whether or not it was written to do so. See **02-entrypoint-and-process-model.md**.

**Network namespace and port publishing** — Each container gets its own loopback interface, separate from the host's. A process bound only to `127.0.0.1` inside a container is unreachable from outside that container, no matter what ports are published. See **02-entrypoint-and-process-model.md**.

**Health check vs. dependency ordering** — Compose's `depends_on` controls *creation order* only, not readiness. A health check is a separate, explicit declaration of what "ready" means. See **03-compose-and-orchestration.md**.

**Stop grace period** — On `docker stop`, the runtime sends SIGTERM, waits a configurable grace period (default 10s), then sends SIGKILL. Any backgrounded work not tracked by the main process can be killed mid-flight when that window elapses. See **02-entrypoint-and-process-model.md** and **03-compose-and-orchestration.md**.

---

## Common Pitfalls (Quick Reference)

| Pitfall | Problem | Solution |
|---------|---------|----------|
| Binding to `127.0.0.1` inside the container | Unreachable via published ports | Bind to `0.0.0.0` inside the container; restrict access at the host/network layer instead |
| Unknown entrypoint mode falls through to a default | Wrong role starts silently | Reject unrecognized/missing mode with a non-zero exit |
| `source .env` in an entrypoint under `set -e` | Missing (gitignored) env file kills every mode at startup | Guard the source with an existence check; let the real consumer fail with a real error if a required var is missing |
| Shell script as PID 1 | Doesn't reap zombies or forward signals | Use `exec` for the final process, or a minimal init (e.g. `tini`) |
| `depends_on` without a healthcheck | Dependent starts before dependency is ready | Add a real healthcheck and `depends_on: condition: service_healthy` |
| `FROM base:latest` | Build resolves a different artifact tomorrow | Pin exact versions/digests for base images and downloaded binaries |
| Long-running background job attached to a request handler | Killed by the default stop grace period | Size the grace period to the job, or make shutdown wait for in-flight work explicitly |
| Hand-maintained copy of a generated config (e.g. crontab) | Drifts from the source template | Generate it from the template at build or start time |

For detailed treatment of any of these, see the specific guide named above.

---

## Version History

- **2026-09-15** — Initial guide: introduction, vocabulary, and pitfall quick reference.
