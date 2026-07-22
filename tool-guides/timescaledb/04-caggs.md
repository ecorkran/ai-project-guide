---
docType: tool-guide
tool: timescaledb
audience: [human, ai]
description: >
  Continuous aggregates: the invalidation-log mental model, why trailing
  refresh policies never heal history, the materialized_only serving trap,
  force-refresh semantics, and parity verification as the only detector
  for self-hiding corruption.
dateCreated: 20260722
dateUpdated: 20260722
---

# Continuous Aggregates (caggs)

## Mental model

A cagg is three cooperating parts:

1. A **materialized hypertable** holding pre-computed buckets (a real
   hypertable with its own chunks, compression, and jobs — see the
   auto-sizing trap in `02-chunk-sizing.md`).
2. An **invalidation log**: source-table writes append entries marking
   regions as stale.
3. A **refresh policy** (background job) that consumes log entries within
   its `[start_offset, end_offset]` window and re-materializes those
   regions.

Everything below follows from one asymmetry: *the log is consumed on
refresh, whether or not materialization actually covered the region.*

## Trailing policies never heal history

A policy with `start_offset = 1 day` re-materializes only the trailing day.
Any invalidation older than `start_offset` — from a backfill, a historical
correction, or a restructuring sweep — is **outside the policy window
forever**. The policy keeps reporting `Success` while the historical region
stays stale or empty. Widening the window to cover all history on every tick
is infeasible on large tables; the correct posture is:

- trailing policy for steady-state (recent writes), **plus**
- an explicit rule: any code path or operation that writes *historical*
  source rows is followed by a parity check and, on failure, a windowed
  force-refresh repair (see below and `03-restructuring.md`).

## `materialized_only = true` serves missing data as truth

With `materialized_only = true` (required for some layouts, and the default
in recent versions), queries read **only** the materialized hypertable — no
real-time union with source. An under-materialized cagg therefore returns
incomplete aggregates *as if they were complete*: no error, no NULL, just
silently smaller numbers. Measured production case: four caggs served ~21%
of the true data for weeks; every consumer — API, CLI, and an operator
estimating table scale from the cagg — got wrong answers that looked right.

Corollary: **never derive authoritative facts from a cagg without first
verifying parity** (see `05-query-discipline.md` on row-count claims).

## `force => true` refresh

`refresh_continuous_aggregate(cagg, start, end)` no-ops over regions the
invalidation log says are clean — including regions whose entries were
consumed without materialization (the collision in `03-restructuring.md`)
and regions dropped by `drop_chunks` on the cagg. Repairing such regions
requires `force => true`, which rebuilds unconditionally from source.

Also: `refresh_continuous_aggregate` **cannot run inside a transaction
block**. Any tooling that sequences drop → refresh → compress commits those
steps independently and must derive resumability from observable state
(parity), not transactionality.

## Parity verification: the only detector

The corruption classes above are **self-hiding**: the cagg's own bookkeeping
(job status, invalidation log) reports healthy. The only detector is a
direct cagg-vs-source comparison:

> Per bounded window: cagg `SUM(<count column>)` == source `COUNT(*)` over
> the same window.

This requires the cagg to carry a per-bucket row count (e.g.
`count(*) AS minute_count` in the cagg definition) — **include one in every
cagg you define**; it costs one bigint per bucket and is the difference
between verifiable and unverifiable. Build the parity check as a standing,
cheap, read-only tool and run it after any restructuring, backfill, or
historical write — and periodically as a health check.

## Compression on cagg materialized hypertables

- Set `compress_after` **greater than** the refresh policy's `start_offset`,
  so the columnstore policy never compresses inside the actively-refreshed
  head. (Refreshing into compressed chunks works but churns.)
- Segment/order settings follow the same logic as the source table
  (`05-query-discipline.md`): segment by the filter column, order by the
  bucket time.

## Bucket/window alignment

When sweeping a cagg window-by-window, choose windows that cover whole
buckets: bucket widths that divide 24 h (5 min, 15 min, 1 h, 4 h) are always
covered by day-aligned windows. A window boundary that splits a bucket
produces partial-bucket artifacts at the seam.

## Checklist when defining a cagg

- [ ] Per-bucket row-count column included (parity verifiability)
- [ ] Materialized hypertable chunk interval verified post-creation
      (`02-chunk-sizing.md`)
- [ ] Refresh policy offsets chosen; historical-write paths identified and
      covered by the parity rule
- [ ] `compress_after` > refresh `start_offset` if compressing
- [ ] Consumers audited for the `materialized_only` serving implication
