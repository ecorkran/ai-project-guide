---
docType: tool-guide
tool: timescaledb
audience: [human, ai]
description: >
  Production query discipline for compressed hypertables: statement_timeout
  and backend cancellation, metadata-assisted vs decompress-everything
  queries, row-count authority rules, and compression/capacity planning
  from measured bytes-per-row.
dateCreated: 20260722
dateUpdated: 20260722
---

# Production Query Discipline

Rules for ad-hoc and analytical queries against production hypertables.
Each exists because its violation caused, or contributed to, a measured
production incident.

## Every session sets a statement_timeout

`SET statement_timeout` sized to intent — seconds for probes, minutes only
deliberately — before anything else in any ad-hoc session against a
production hypertable.

**A client-side timeout does not cancel the server-side backend.** The query
keeps running (and holding locks, and decompressing) after your client gives
up. After any client-side timeout or interrupt:

1. Find the backend in `pg_stat_activity`.
2. `pg_cancel_backend(pid)` — **before running anything else.**

The incident shape this prevents: a decompress-everything query outlives its
client, follow-up queries stack behind it, a backend dies ("server closed
the connection unexpectedly"), and the server needs a restart. Tooling that
issues long-running queries should build both halves in: explicit timeout
on every statement, backend cancellation on client interrupt.

## Metadata-assisted vs decompress-everything

On a compressed (columnstore) hypertable, cost is determined by whether the
query can be answered from **compressed-batch metadata**:

- **Near-free**: plain `count(*)`; `MIN`/`MAX` on the orderby column.
  Measured: exact `count(*)` over ~4.4 B rows in ~1.3 s — *on a healthy
  chunk layout* (`02-chunk-sizing.md`; the same count was prohibitively
  slow at 25k chunks).
- **Decompress-everything**: any aggregate over an *expression* —
  `GROUP BY extract(year FROM time)`, function-wrapped columns, predicates
  the metadata can't bound. These decompress the entire table server-side.

The trap is the resemblance: a cheap metadata-assisted query and a
table-melting one can differ only by a function call in the GROUP BY. Treat
any expression aggregate over a compressed hypertable as a full-table
decompression and bound it (window it, or run it against a cagg — after
verifying parity).

## Row-count authority

For any row-scale claim (capacity planning, health checks, documentation):

1. **Only an exact `count(*)` on the source table is authoritative.** Cheap
   on a healthy chunk layout (see above).
2. **`approximate_row_count()` is order-of-magnitude only** on compressed
   hypertables. Measured: still ~66% high *after* `ANALYZE` (7.31 B
   reported vs 4.41 B actual).
3. **A cagg-derived count is valid only after cagg-vs-source parity is
   verified** (`04-caggs.md`). An under-materialized cagg poisons every
   estimate built on it — including human operators' mental figures.

The failure mode this prevents: three independent, authoritative-looking
sources (a doc recording the approximate count, a cagg-derived sum, an
operator estimate) held three different wrong numbers for the same table.
Estimates and derived tables drift silently; only the source table counts.

## Compression settings and capacity planning

- `segmentby` = the column queries filter on (e.g. the entity/symbol
  column); `orderby` = the time column, typically `DESC`. This is also what
  makes the metadata-assisted fast paths above work.
- **Plan capacity from measured bytes-per-row, not compression-ratio
  projections.** Divide actual on-disk size by an *exact* row count.
  Measured anchor: ~17 bytes/row for narrow numeric OHLCV rows
  (six numeric/bigint columns) under `segmentby=symbol, orderby=time DESC`.
  An earlier figure from the same table (~10 bytes/row) was wrong because
  it divided by an estimated count — the two disciplines compound.
- Uncompressed-to-compressed planning: verify disk headroom **before**
  starting any operation that materializes uncompressed data at scale;
  compress behind the write frontier to bound peak footprint
  (`03-restructuring.md`).

## Quick reference

| Intent | Do | Never |
|---|---|---|
| Probe / sanity check | `SET statement_timeout` (seconds), then query | Run unbounded "just to see" |
| Row scale | Exact `count(*)` | Trust `approximate_row_count` or a cagg without parity |
| Year/period breakdown | Query a parity-verified cagg, or window the raw query | Expression GROUP BY over the compressed table |
| Client timeout hit | `pg_cancel_backend` the backend first | Re-run or stack more queries |
| Capacity math | Measured bytes/row × exact count | Ratio projections on estimated counts |
