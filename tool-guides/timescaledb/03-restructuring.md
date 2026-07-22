---
docType: tool-guide
tool: timescaledb
audience: [human, ai]
description: >
  Playbook for restructuring chunks on a populated hypertable: why
  merge_chunks fails on gap-structured data, the per-window rewrite
  mechanism for source tables vs caggs, mandatory job-pause pre-flight,
  and the silent cagg-corruption collision.
dateCreated: 20260722
dateUpdated: 20260722
---

# Restructuring Chunks on a Populated Hypertable

Needed when a table was created with a wrong `chunk_time_interval`
(see `02-chunk-sizing.md`) — `set_chunk_time_interval()` only affects future
chunks, so existing data must be rewritten into new boundaries.

## `merge_chunks` cannot cross empty ranges

TimescaleDB's `merge_chunks` (and `compress_chunk_time_interval` roll-up)
refuse to merge chunks separated by an **empty range** ("cannot create new
chunk partition boundaries"). Any gap-structured dataset — market hours,
business days, sensor duty cycles — guarantees empty ranges, capping these
mechanisms at merging within each contiguous run. Measured: 25,256 chunks
formed 5,671 per-day runs, capping improvement at ~4.4× when ~21× was
required. Rehearse on a gap-faithful scratch table before assuming either
mechanism applies.

## The working mechanism: per-window rewrite, oldest → newest

Process one target-interval window at a time. Windows must be **grid-aligned**
to TimescaleDB's epoch grid (1970-01-01 + k × interval; e.g. 7-day windows
start on Thursdays) — a straddling window yields two chunks instead of one.

The mechanism differs by data class, and the difference is load-bearing:

### Source-of-truth hypertable (rows exist nowhere else)

Per window, in **one transaction**:

1. `LOCK TABLE <hypertable> IN EXCLUSIVE MODE` — **first statement, before
   the snapshot.** EXCLUSIVE blocks writers (readers unaffected) so a
   concurrent writer lands wholly before the snapshot (and is staged) or
   wholly after the commit (and writes into the new chunk) — never between.
2. Stage the window's rows to a temp table.
3. `drop_chunks()` over the window — removes old chunks *and their dimension
   slices*, allowing the reinsert to create one fresh full-width chunk.
4. Reinsert from the temp table. Compression follows outside the transaction.

Row-count guards (staged == reinserted) are kept as invariant checks but are
**not concurrency protection**: a writer that commits between snapshot and
drop is invisible to both sides of the guard — the check passes while rows
are destroyed. This exact silent-loss race was found in review; the lock
ordering is the fix. Interrupted runs are safe by construction: each window
either committed or rolled back, and window state is re-derived from the
catalog on every run.

### Derived data (cagg materialized hypertables)

The raw table is the source of truth, so no stage, no lock. Per window:

1. `drop_chunks()` on the cagg over the window.
2. `refresh_continuous_aggregate(cagg, start, end, force => true)` —
   rebuilds from source. `force` is required when invalidation entries were
   already consumed (see `04-caggs.md`).
3. `compress_chunk()` on the new chunk(s) (compress-behind-frontier bounds
   peak uncompressed footprint to ~one window).

`refresh_continuous_aggregate` **cannot run inside a transaction block**, so
these steps commit independently. Resumability is **parity-derived**, not
transactional: a window is done iff the cagg's aggregate row count over the
window equals the source's bounded count. A kill between steps leaves either
a bounded zero-coverage window (rebuilt on re-run) or an uncompressed-but-
correct chunk (compression re-attempted) — bounded unavailability, never
wrong data. Note the serving impact: with `materialized_only = true`,
consumers see zero rows for a window mid-rebuild; run sweeps off-hours.

## Mandatory pre-flight: pause the background-job family

**Any chunk restructuring must first pause the table's full job family**:
its columnstore policy plus *every attached cagg's* refresh policy.

Why this is a correctness control, not a performance courtesy — the measured
collision: a cagg refresh policy fired against a chunk mid-restructure,
blocked behind the restructuring transaction, then completed against a
pre-restructure snapshot. It **consumed the invalidation log but
materialized nothing**, leaving the cagg permanently missing rows while
reporting "up-to-date". No later refresh heals it; only a direct
cagg-vs-source comparison detects it (see `04-caggs.md`).

Pre-flight rules:

- Resolve job IDs at runtime from `timescaledb_information.jobs` — never
  hardcode them; they differ across environments and re-creations.
- **Refuse to run, don't warn**, if required jobs are unpaused. Print the
  offending job IDs and the pause command.
- After resume, verify every job's `last_run_status = 'Success'` and zero
  unscheduled jobs.

## After any restructuring: verify cagg parity

Restructuring a source table invalidates its caggs' materialized regions,
and trailing refresh policies (small `start_offset`) can never heal history.
Standing rule: **after any chunk restructuring, run a cagg-vs-source parity
check; on failure, run the force-refresh repair sweep.** A parity-based
done-check makes the repair exactly incremental — it rebuilds only the
windows the restructuring invalidated.

## Testing restructuring tools

- Rehearse on a **gap-faithful scratch hypertable** with an attached cagg
  and a live refresh policy (see `01-overview.md`, meta-rules).
- Concurrency claims get **deterministic tests via injection seams** (e.g.
  an `after_stage` hook that attempts a concurrent write inside the critical
  span and asserts refusal) — never sleep-based races.
- Prove resumability by killing the tool mid-window on the rehearsal table
  and asserting clean resume.
