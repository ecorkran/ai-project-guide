---
docType: tool-guide
tool: timescaledb
audience: [human, ai]
description: >
  Chunk-interval sizing rule for hypertables and continuous aggregates:
  size from wall-clock lifetime and target chunk count, never from data
  volume. Includes the cagg 10x-source auto-sizing trap.
dateCreated: 20260722
dateUpdated: 20260722
---

# Chunk Sizing

## The rule

> **`chunk_time_interval` = expected wall-clock lifetime of the table ÷
> target chunk count (~1,000–2,000 chunks over the table's lifetime).**
> Never size from per-chunk data volume alone.

A table that lives for decades needs its interval derived from the decade.
Vendor guidance framed around per-chunk memory fit answers a different
question (ingest performance) and, followed alone, produces tables with tens
of thousands of chunks.

## Why: the planner pays per chunk, on every unpruned query

The query planner and lock manager touch every chunk that cannot be pruned —
roughly 7 catalog locks per chunk — and this cost is paid at *planning* time,
before a single row is read.

Measured production evidence: a 22.5-year minute-bar hypertable at a 4-hour
interval accumulated 25,256 chunks. A trivial single-symbol `MIN`/`MAX`
query took **846 seconds of planning against 4.2 seconds of execution**
(~176k catalog locks). After re-chunking the same data to ~1,200 chunks the
same query ran in 0.7 s total.

**Small chunks are not safe chunks.** The pathological chunks above averaged
only ~5 MB. Data volume determines how *large* a chunk gets; wall-clock span
determines how *many* chunks exist — and count is what kills queries.

## The cagg auto-sizing trap

When a continuous aggregate is created, TimescaleDB sizes its materialized
hypertable's chunk interval at **10× the source hypertable's interval at
creation time** — and never revisits it. Two consequences:

- If the source interval is wrong, every cagg inherits a 10×-wrong interval.
  (Measured: caggs over the 4-hour-interval table above got ~1.67-day
  intervals → ~4,236 chunks each, versus ~117 at the intended sizing.)
- If you later fix the source interval, existing caggs **keep** their old
  sizing. New caggs created afterward get the corrected 10× value.

**After creating any cagg, check its materialized hypertable's interval**
in `timescaledb_information.dimensions` and set it explicitly with
`set_chunk_time_interval()` if it fails the wall-clock rule. Resolve the
materialized hypertable by cagg view name via
`timescaledb_information.continuous_aggregates` — never by the internal
`_materialized_hypertable_N` name, which is assigned by creation order and
differs across environments.

## Operational rules

- **`set_chunk_time_interval()` affects future chunks only.** Existing
  chunks keep their boundaries; fixing a populated table requires a
  restructuring sweep (see `03-restructuring.md`).
- **Define the interval once as a code constant** and render it into the
  migration. A literal interval in a migration, divorced from a constant,
  invites drift between the migration, tooling pre-flight checks, and docs.
- **Gap-structured data fragments harder.** If the data has recurring empty
  ranges (nights, weekends), an interval smaller than the gap spacing yields
  roughly one chunk-run per active period — chunk count approaches
  active-period count no matter how small the chunks are.
- **Space partitioning multiplies chunk count** by the number of space
  partitions. Apply the wall-clock rule to the *product*.
- **Interval changes are cheap to plan for, expensive to retrofit.** The
  restructuring sweep for the table above rewrote ~4.4 B rows over ~13
  hours. Choosing the interval correctly at creation costs one line.

## Checklist when creating a hypertable or cagg

- [ ] Expected lifetime estimated (years, not months)
- [ ] Interval = lifetime ÷ 1,000–2,000, sanity-checked against gap structure
- [ ] Interval defined as a code constant, rendered into the migration
- [ ] For caggs: materialized hypertable's actual interval verified in
      `timescaledb_information.dimensions` after creation
- [ ] Space-partitioning multiplier accounted for, if used
