---
description: SQL coding standards for PostgreSQL, pgvector, and TimescaleDB. Use when writing queries, migrations, schema definitions, or database functions. Covers naming, indexing, query optimization, and extension-specific patterns.
paths: 
  - "**/*.sql"
  - "**/*.psql"
  - "**/migrations/*.sql"
  - "**/schema.sql"
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
