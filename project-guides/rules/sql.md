---
description: SQL coding standards for PostgreSQL, pgvector, and TimescaleDB. Use when writing queries, migrations, schema definitions, database functions, or any code that connects to a database — including test fixtures and runners. Covers naming, indexing, query optimization, extension-specific patterns, and production-database protection.
paths: 
  - "**/*.sql"
  - "**/*.psql"
  - "**/migrations/**"
  - "**/schema.sql"
  - "**/test/**/*.py"
  - "**/tests/**/*.py"
  - "**/conftest.py"
---

### SQL and PostgreSQL Development Rules

#### Query Style & Formatting

- UPPERCASE SQL keywords: `SELECT`, `FROM`, `WHERE`, not `select`
- Lowercase table and column names with underscores: `user_accounts`
- Indent multi-line queries consistently (2 or 4 spaces)
- One column per line in SELECT for readability
- Leading commas in SELECT lists for easier modification
- Meaningful table aliases, avoid single letters

#### Query Optimization

- Always use EXPLAIN ANALYZE for performance tuning
- Create indexes for WHERE, JOIN, and ORDER BY columns
- Use partial indexes for filtered queries
- Prefer JOIN over subqueries when possible
- LIMIT queries during development testing
- Avoid SELECT * in production code
- Use EXISTS instead of COUNT for existence checks

#### PostgreSQL Best Practices

- Use appropriate data types: JSONB over JSON, TEXT over VARCHAR
- UUID for distributed IDs, SERIAL/BIGSERIAL for single-node
- Check constraints for data validation
- Foreign keys with appropriate CASCADE options
- Use transactions for multi-statement operations
- RETURNING clause to get modified data
- CTEs (WITH clauses) for complex queries

#### Naming & Schema Design

- Singular table names: `user` not `users`
- Primary key as `id` or `table_name_id`
- Foreign keys as `referenced_table_id`
- Boolean columns prefixed with `is_` or `has_`
- Timestamps: `created_at`, `updated_at` with timezone
- Use schemas to organize related tables
- Version control migrations with sequential numbering

#### Security & Safety

- Always use parameterized queries, never string concatenation
- GRANT minimum required privileges
- Use ROW LEVEL SECURITY for multi-tenant apps
- Sanitize all user input
- Prepared statements for repeated queries
- Connection pooling with appropriate limits
- Set statement_timeout for long-running queries

#### Production Database Protection

Distilled from a real production incident (test fixture truncated prod metadata)
and its recovery. These are deterministic-first: prefer a control the server or a
test can enforce over a rule someone must remember.

- **Split connection roles.** The application role gets DML only — no TRUNCATE
  (a separate grantable privilege), no DDL, no ownership, read-only on the
  migration ledger. Migrations and maintenance use a separate role/URL supplied
  only when doing that work. With this split, a test that leaks production
  credentials dies on `permission denied` instead of destroying tables.
- **Tests never read the production URL variable.** Test tiers use a dedicated
  test variable and throwaway databases created by the fixture itself. A fixture
  that issues TRUNCATE/DROP/ALTER/DELETE may only target a database it created.
  "Unit" is a directory name, not a property — nothing stops a file under
  `test/unit/` from opening a connection.
- **Enforce it mechanically, per tier.** A guard test scans every test file for
  reads of the production variable and fails on offenders (ratchet with a
  shrink-only allowlist if legacy readers exist). The scan must be
  multiline-aware — `os.environ.get(\n "VAR")` defeats a per-line grep.
  The absence of a guard in a tier is not evidence of safety.
- **Never inject a whole `.env` into a child process.** Pass an explicit list of
  named variables. A runner built to fix a parsing problem must not widen
  credential scope as a side effect.
- **`TRUNCATE ... CASCADE` destroys the FK closure, not the named tables.**
  Enumerate the closure before any CASCADE against a shared database.
- **Restore-by-replay heals the ledger, not the catalog.** Objects dropped while
  their creating migration is still recorded are invisible to replay. A restore
  tool must diff the live catalog against expectations; and after any incident,
  verify derived objects (matviews, continuous aggregates) by **content parity
  against source**, never by catalog presence — an object created or interrupted
  mid-incident is presumed damaged, and for an empty derived object,
  drop-and-recreate from its migration beats in-place repair.
- **Size backup priority by what cannot be re-derived** from providers or raw
  data, not by the last incident's blast radius.
- **Protect the host from runaway sessions:** `vm.overcommit_memory=2` on
  dedicated Postgres hosts so allocation failure hits the statement, not the
  OOM killer hitting the postmaster. For bulk rebuilds, run a watchdog that
  `pg_cancel_backend`s the working backend when free memory crosses a floor —
  cancellation releases memory instantly; the OOM killer takes the cluster.
  Note `work_mem` does not bound extension-internal allocations (e.g.
  TimescaleDB cagg materialization).
- **After a client-side timeout, `pg_cancel_backend` the server side** before
  running anything else; client disconnect does not cancel the backend.

#### pgvector Specific

- Use `vector` type for embeddings
- Create HNSW or IVFFlat indexes for similarity search
- Normalize vectors before storage when needed
- Use `<->` for L2 distance, `<#>` for inner product
- Batch insert embeddings for performance
- Consider dimension reduction for large vectors

#### TimescaleDB Specific

- Create hypertables for time-series data
- Use appropriate chunk intervals (typically 1 week to 1 month)
- Continuous aggregates for common queries
- Compression policies for older data
- Retention policies to manage data lifecycle
- Use time_bucket() for time-based aggregations
- Data retention policies with drop_chunks()

#### Performance & Monitoring

- Index foreign keys and commonly filtered columns
- VACUUM and ANALYZE regularly
- Monitor pg_stat_statements for slow queries
- Use connection pooling (PgBouncer/pgpool)
- Partition large tables by date or ID range
- Avoid excessive indexes (write performance cost)
- Use COPY for bulk inserts

#### Migrations & Maintenance

- Always reversible migrations when possible
- Test migrations on copy of production data
- Use IF NOT EXISTS for idempotent operations
- Document breaking changes
- Backup before structural changes
- Zero-downtime migrations with careful planning
