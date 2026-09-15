---
layer: tool-guide
tool: Docker
docType: guide
description: Decision framework for porting an existing service into a container, especially from a systemd unit
dependsOn: [00-introduction.md]
dateCreated: 20260915
dateUpdated: 20260915
---

# Docker Decision Guide

This guide covers the decisions that come up when moving an existing service into a container — most acutely, when the service already runs under systemd (or an equivalent service manager) on a host. Nearly every item below is a fork where the obvious choice is the wrong one: reverting to defaults, dropping "boilerplate," or accepting whatever a naive Dockerfile produces.

## Porting a systemd Unit to a Container

An existing systemd unit file encodes operational knowledge, not just a start command. Before containerizing, read the unit file line by line and account for each directive — don't just extract `ExecStart` and discard the rest.

**What to carry over, and why it's usually load-bearing rather than boilerplate:**

- **Resource limits** (`LimitNOFILE`, `MemoryMax`, `CPUQuota`) — these were often tuned in response to a real incident (a file-descriptor exhaustion, an OOM). Dropping them reverts the service to platform defaults, which is exactly the condition that caused the original tuning. Map these to the container runtime's equivalent (`ulimits:` in Compose, `mem_limit`, `cpus`).
- **Restart policy** (`Restart=on-failure`, `RestartSec`) — maps to `restart:` in Compose or `--restart` in `docker run`. A service that was tuned to restart with backoff on failure should not silently become "never restarts" or "restarts instantly in a crash loop."
- **Environment and working directory** (`Environment=`, `EnvironmentFile=`, `WorkingDirectory=`) — these often carry tuning flags (thread pool sizes, buffer sizes, feature flags) set for a specific reason. Treat each one as a question — "why was this set?" — not a default to drop because the container "works" without it.
- **User/permissions** (`User=`, `Group=`) — a unit that deliberately runs as a non-root user should not become a container running as root just because that's the image's default.
- **Pre/post hooks** (`ExecStartPre`, `ExecStopPost`) — often contain setup or cleanup steps (creating a directory, flushing a cache) that have no obvious container equivalent and are easy to lose entirely if only `ExecStart` is read.

**Why reverting to defaults passes every naive smoke test:** a container that drops all of the above will still start, respond to a request, and look correct in a demo. The tuning a unit file carries exists specifically for conditions a smoke test doesn't reach — sustained load, a slow memory leak, a crash under a specific input. The absence of a symptom during testing is not evidence the tuning was unnecessary.

## Whether to Containerize at All

Containerization is usually a good default for a network service with clear dependencies, but a few situations are worth a second look before treating it as a given:

| Situation | Consideration |
|---|---|
| Service needs privileged host access (raw device access, host networking for performance) | May need `--privileged`, `network_mode: host`, or specific capability grants — check whether the containerized form still delivers the same guarantees before assuming a straightforward port |
| Service is tightly coupled to host-specific state (a local hardware sensor, a host-only filesystem path) | Containerizing without addressing the coupling just relocates the host-dependency problem behind a volume mount |
| Existing unit already runs reliably and isn't being scaled, replicated, or redeployed differently | Containerize when it buys something operationally (portability, reproducible builds, orchestration) — not for its own sake |

## Decision Checklist for a New Containerization Effort

1. Read the existing service's full startup configuration (unit file, launch script, or equivalent) before writing a Dockerfile — see systemd porting above.
2. Decide build-time vs. runtime for each step in the current startup sequence (see **01-image-and-build.md**).
3. Design the entrypoint's mode dispatch and its failure behavior for unknown input (see **02-entrypoint-and-process-model.md**).
4. Confirm every network bind is `0.0.0.0` inside the container, with access control moved to the host/network layer (see **02-entrypoint-and-process-model.md**).
5. Define real health checks for every service the new container depends on, and gate startup on them rather than on creation order (see **03-compose-and-orchestration.md**).
6. Decide the stop grace period based on the longest backgrounded work the process can have in flight, not the runtime default (see **02-entrypoint-and-process-model.md**).
7. Pin every external dependency — base image, downloaded binary, package lockfile (see **01-image-and-build.md**).

## Version History

- **2026-09-15** — Initial guide: systemd-to-container porting checklist, containerization fit considerations.
