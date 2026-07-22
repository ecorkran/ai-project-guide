---
docType: tool-guide
tool: timescaledb
audience: [human, ai]
description: >
  TimescaleDB tool guide — core mental model, then hard-won operational rules
  for chunk sizing, restructuring, continuous aggregates, and production query
  discipline. Written from measured production evidence, not vendor docs.
dateCreated: 20260722
dateUpdated: 20260722
---

# AI Tool Overview: TimescaleDB

TimescaleDB extends PostgreSQL with time-series storage: hypertables
(time-partitioned tables), continuous aggregates (incrementally maintained
materialized rollups), and columnstore compression. This guide captures the
operational knowledge that vendor documentation states weakly or not at all —
each rule here was learned from a measured production failure or a rehearsal
that surfaced one.

Written against TimescaleDB 2.23 / PostgreSQL 17. Verify version-specific
behavior against release notes when working on other versions.

## Core mental model

Four facts drive almost every rule in this guide:

1. **A hypertable is a set of chunks, and the planner pays per chunk.** Every
   query that cannot be pruned to a few chunks pays planning and lock-manager
   cost proportional to *chunk count* — regardless of how small the chunks
   are. Chunk count, not chunk size, is the primary health metric.
2. **A continuous aggregate (cagg) is a separate materialized hypertable plus
   an invalidation log.** Refresh policies consume the log to decide what to
   re-materialize. If the log is consumed without materialization happening
   (a known collision, see below), the cagg is silently and permanently
   wrong while reporting itself up to date.
3. **Columnstore compression stores batches segmented and ordered by chosen
   columns.** Queries the batch metadata can answer (plain `count(*)`,
   `MIN`/`MAX` on the orderby column) are near-free; anything over an
   *expression* decompresses everything. Two queries that look similar can
   differ in cost by five orders of magnitude.
4. **Defaults are not neutral.** The default chunk interval, and the
   automatic 10×-source-interval sizing of a cagg's materialized hypertable,
   both produced production pathologies. Every interval choice is a decision;
   make it explicitly (see chunk-sizing).

## Guide map

| File | Consult when |
|---|---|
| `02-chunk-sizing.md` | Creating any hypertable or cagg; choosing or changing `chunk_time_interval` |
| `03-restructuring.md` | Fixing chunk pathology on a populated table; any operation that drops/merges/rewrites chunks |
| `04-caggs.md` | Creating caggs; refresh policies; diagnosing missing or stale aggregate data |
| `05-query-discipline.md` | Any ad-hoc or analytical query against a production hypertable; row-count claims; capacity planning |

## Meta-rules (apply to everything below)

- **Rehearse destructive operations on a gap-faithful scratch hypertable** —
  synthetic data reproducing the real table's *empty ranges* (e.g.
  market-hours data has no overnight/weekend chunks), with an attached cagg
  and a live refresh policy. A 24/7-continuous scratch table hides both the
  chunk-adjacency restriction and realistic policy-collision windows.
- **Correctness controls must be structural, not circumstantial.** "The
  writer process is stopped" is operator guidance; a lock or a pre-flight
  refusal is a control. Circumstance is what erodes first when a tool is
  reused months later by someone who didn't read the original design.
- **Define every interval/threshold once as a code constant** and render it
  into migrations and tooling. Scattered literal intervals drift.

## Evidence provenance

The measured figures cited throughout ("846 s planning", "~66% high",
"17 bytes/row") come from a production system: a ~4.4-billion-row minute-bar
OHLCV hypertable and four attached caggs on TimescaleDB 2.23.0 /
PostgreSQL 17.7, diagnosed and repaired in 2026. Figures are anchors for
orders of magnitude, not universal constants — re-measure on your own data
before making capacity decisions.
