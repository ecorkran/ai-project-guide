---
layer: tool-guide
tool: Docker
docType: guide
description: Entrypoint design, multi-mode dispatch, PID 1, signal handling, and network binding inside containers
dependsOn: [00-introduction.md]
dateCreated: 20260915
dateUpdated: 20260915
---

# Docker Entrypoint & Process Model Guide

Covers what runs as a container's main process, how it starts, how it responds to signals, and how it binds to the network.

## Multi-Mode Images and Entrypoint Dispatch

A common pattern: one image serves several roles (web server, background worker, scheduler) via an entrypoint script that dispatches on an argument or environment variable.

```bash
#!/bin/sh
set -e

case "$1" in
  web)
    exec gunicorn app:server --bind 0.0.0.0:8000
    ;;
  worker)
    exec celery -A app worker
    ;;
  scheduler)
    exec celery -A app beat
    ;;
  *)
    echo "Unknown mode: '$1'. Expected one of: web, worker, scheduler" >&2
    exit 1
    ;;
esac
```

**The load-bearing detail is the `*)` branch.** A hand-rolled dispatcher that falls through to a default mode when the argument is unrecognized or missing fails silently: the container starts, looks healthy, and is running the wrong role. There is no error to see — only a service that mysteriously isn't doing what it should. Always reject an unknown or missing mode with a non-zero exit and a message naming what was expected.

## PID 1, Zombie Reaping, and Signal Forwarding

The first process started in a container's PID namespace is PID 1, whether or not it was written with that responsibility in mind. Two things make this matter:

**Zombie reaping.** PID 1 is responsible for reaping orphaned child processes. A shell script or application that isn't written to do this will accumulate zombie processes under any workload that spawns and reaps subprocesses.

**Signal handling.** By default, PID 1 does not get default signal dispositions — a plain shell script as PID 1 often does not forward SIGTERM to a child it launched without `exec`, meaning `docker stop` has no visible effect until the grace period elapses and SIGKILL arrives, discarding whatever cleanup the process would otherwise have done.

Two fixes, both commonly needed together:

1. **Use `exec` for the final foreground process** in an entrypoint script, so the application replaces the shell as PID 1 instead of running as a child of it:
   ```bash
   # Wrong: shell stays as PID 1, app is a child that may not receive forwarded signals
   gunicorn app:server --bind 0.0.0.0:8000

   # Correct: exec replaces the shell process with gunicorn, which becomes PID 1
   exec gunicorn app:server --bind 0.0.0.0:8000
   ```
2. **Use a minimal init when the main process itself doesn't reap zombies** (e.g. it shells out to subprocesses of its own) — `tini` or `docker run --init` / Compose's `init: true`. This is a real init system running as PID 1, with the application as its child, rather than a substitute for `exec`.

## Loopback Binds Do Not Survive Containerization

Each container gets its own network namespace with its own loopback interface. A process bound to `127.0.0.1` inside a container is reachable **only from within that same container** — not from other containers, not from the host, and not through the container runtime's port mapping (`-p 8080:8080` publishes nothing if the process inside is listening on loopback).

The fix: bind to `0.0.0.0` (all interfaces) inside the container, and do access restriction at the host or network layer — the published port mapping, a firewall rule, or the Compose network topology — not by relying on the loopback restriction that worked when the process ran directly on a host.

```dockerfile
# Wrong for containerized use: only reachable from inside the container itself
CMD ["myserver", "--bind", "127.0.0.1:8080"]

# Correct: bind all interfaces inside the container; restrict externally instead
CMD ["myserver", "--bind", "0.0.0.0:8080"]
```

**Watch for binds with no environment seam.** Some servers take the bind address only as a command-line flag baked into the image or a config file, with no environment variable override. When containerizing such a service, that flag needs to become configurable (env var, templated config, or a build/entrypoint-time substitution) — otherwise every deployment of the image is stuck with whatever was hard-coded. This matters especially when one Compose stack runs two services that legitimately need different bind behavior (e.g. an internal-only admin service versus a public API) — a single hard-coded bind can't serve both, and each needs its own explicit configuration.

## Env Files and `set -e`

An entrypoint that unconditionally sources an env file to populate configuration is a common pattern:

```bash
# Dangerous under set -e if .env is gitignored and absent from the image
source .env
exec "$@"
```

If `.env` is gitignored (as it should be for anything with secrets), it is **absent from the built image**. Under `set -e`, `source .env` failing kills the entrypoint before it reaches any mode-specific logic — every mode fails at startup, and the error is "file not found" rather than something that points at the actual missing configuration.

**The guard is the fix, not a fallback default:**

```bash
# Correct: only source if present; do not invent defaults for what's missing
if [ -f .env ]; then
  source .env
fi
exec "$@"
```

The anti-pattern to avoid is filling the gap with invented default values for whatever the env file would have provided. If a required variable is genuinely missing, let the real consumer of that variable fail with its own real error message — that error points at the actual missing config. A silently-substituted default produces a container that starts, appears to work, and behaves wrong in a way that's much harder to trace.

## Graceful Stop Windows

`docker stop` sends SIGTERM, waits a grace period (default 10 seconds, configurable per-container or in Compose via `stop_grace_period`), then sends SIGKILL to anything still running.

This window is fine for a process that has no state to flush. It is a problem when the main process has **backgrounded work attached to it that isn't tracked** — for example, a web server that dispatches a long export job to a detached background thread or subprocess and returns immediately. If that job takes longer than the grace period, it is killed mid-flight with no chance to finish or clean up, and the default grace period will look "fine" in testing (short jobs) and fail only under real workloads (long jobs).

Two ways to reason about the size of this window, both requiring being explicit rather than accepting the default silently:

1. **Size the grace period to the actual work.** If backgrounded jobs can legitimately take minutes, set `stop_grace_period` (Compose) or `--stop-timeout` (docker run) to comfortably exceed the longest expected job, and have the application's SIGTERM handler stop accepting new work while letting in-flight work finish.
2. **Make shutdown wait for in-flight work explicitly**, rather than only extending the timeout — a SIGTERM handler that sets a "draining" flag, stops accepting new requests, and blocks until tracked background work completes (or a hard deadline is hit) is more robust than only lengthening the grace period, because it degrades to a bounded wait instead of an unbounded one.

**Forcing the background work to be blocking (i.e., removing the backgrounding entirely) is usually the wrong fix.** It looks like it solves the shutdown problem, but it reintroduces the original problem the backgrounding was solving (e.g. a request handler that now blocks for the duration of a long job) and just relocates where the pain shows up.

## Version History

- **2026-09-15** — Initial guide: entrypoint dispatch, PID 1, signal handling, network binding, env file guards, stop windows.
