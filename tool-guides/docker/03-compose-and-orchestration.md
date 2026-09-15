---
layer: tool-guide
tool: Docker
docType: guide
description: Compose health gating, startup ordering, and multi-service coordination
dependsOn: [00-introduction.md, 02-entrypoint-and-process-model.md]
dateCreated: 20260915
dateUpdated: 20260915
---

# Docker Compose & Orchestration Guide

Covers coordinating multiple services with Compose: what `depends_on` actually guarantees, and how to gate on real readiness instead.

## `depends_on` Controls Ordering, Not Readiness

Compose's `depends_on` guarantees only that a dependency's container is **created and started** before the dependent's container starts. It does not guarantee the dependency is ready to accept traffic — a database container can be running while Postgres itself is still performing initialization, well before it accepts connections.

```yaml
# Insufficient: api starts as soon as db's container exists, not when Postgres is ready
services:
  db:
    image: postgres:16
  api:
    image: myapp/api
    depends_on:
      - db
```

This passes a naive smoke test (both containers report "running") and fails intermittently in practice — the failure mode is a race, so it shows up more under load or on a slower machine, which makes it look like a flaky, hard-to-reproduce bug rather than what it is: a missing readiness gate.

## Gating on a Real Health Condition

Define a healthcheck that reflects actual readiness — a query against the database, an HTTP endpoint that verifies the application can serve, not just "the process exists":

```yaml
services:
  db:
    image: postgres:16
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 5s
      timeout: 3s
      retries: 5

  api:
    image: myapp/api
    depends_on:
      db:
        condition: service_healthy
```

`condition: service_healthy` makes `api` wait for `db`'s healthcheck to pass, not merely for `db`'s container to start. This is the actual fix — `depends_on` alone (as in the previous example) only sequences container creation.

**A service that never becomes healthy is a silent outcome.** With `condition: service_healthy`, a dependency that fails its healthcheck forever simply means the dependent never starts — there's no crash, no obvious error at the top level, just a container that stays in "created" or restarts and never proceeds. When a stack doesn't come up, the diagnostic path is to check the healthcheck status of each dependency (`docker compose ps`, which shows health state, or `docker inspect` on the container for the full healthcheck log) before assuming the problem is in the dependent service itself.

## Writing a Meaningful Healthcheck

A healthcheck that only confirms the process is running (e.g. checking that a port is open) provides little more than `depends_on` already does. Prefer a check that exercises the actual failure mode you care about:

- **Database**: a real connection/query (`pg_isready`, `mysqladmin ping`), not just "is the port open"
- **HTTP service**: a dedicated `/healthz` endpoint that checks the service's own dependencies (its database connection, its cache), not just that the HTTP server itself answers
- **Worker/queue consumer**: harder to healthcheck via HTTP; consider a liveness file the process touches periodically, checked by the healthcheck command

Keep the healthcheck cheap — it runs on an interval for the life of the container — and make it fail clearly when the underlying condition isn't met, rather than always returning success.

## Startup Ordering for Scheduled Jobs and Migrations

Database migrations and other one-shot startup tasks have the same readiness dependency as a long-running service, but are easy to leave ungated because they're often run via a separate `command:` override or a one-off `docker compose run`. Apply the same `condition: service_healthy` gate to migration/init containers as to long-running dependents — a migration that runs against a database that isn't accepting connections yet fails in the same silent-race way described above.

## Version History

- **2026-09-15** — Initial guide: depends_on vs healthchecks, health gating, writing meaningful healthchecks.
