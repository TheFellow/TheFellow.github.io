---
title: "Building a File-Backed Columnar Event Pipeline"
date: 2026-02-07
last_modified_at: 2026-08-06 16:40:00 -0700
excerpt: "How immutable Parquet batches, snapshot metadata, DuckDB, Arrow, and Protobuf form a columnar event path from storage to results."
permalink: /articles/building-a-file-backed-columnar-event-pipeline/
redirect_from: /guides/building-a-file-backed-columnar-event-pipeline/
order: 55
status: "Architecture guide"
icon: "bird"
accent: "#22b8cf"
topics: ["Parquet", "DuckDB", "Arrow"]
---

Structured logs and event records are often written one at a time but read in a different shape. Investigations select a time range, project a few fields, group by an event type or resource, and scan many records at once. That makes an append-heavy write path and a columnar analytical read path a useful combination.

This guide explores that combination with Parquet, DuckDB, and Apache Arrow. Parquet stores immutable batches of typed records, DuckDB queries the visible files directly, and Arrow carries typed result batches to analytical consumers. Arrow Flight can extend that result boundary across processes.

The interesting property is columnar continuity. Storage, execution, and result delivery retain compatible column-oriented shapes. The formats are not identical, and moving between them still requires I/O, decoding, allocation, and sometimes copying. Their alignment avoids repeatedly turning a tabular workload into row-oriented documents and back again.

This composition follows an established line of analytical systems rather than introducing a new storage model. Google's [Dremel paper](https://research.google/pubs/dremel-interactive-analysis-of-web-scale-datasets/) described interactive analysis over a columnar representation of nested records. The [original DuckDB paper](https://duckdb.org/library/duckdb/) brought vectorized analytical SQL into the application process. Parquet, Arrow, and modern table formats make those ideas available as interoperable storage, memory, and metadata boundaries.

The file format and query engine are only part of the design. A durable pipeline also needs a logical event model, a commit boundary, an authoritative definition of visible files, retry semantics, schema evolution, compaction, and retention. Those concerns determine whether the collection of files behaves like a trustworthy dataset.

## Start with the event model

Storage layout should follow the questions the records need to answer. A useful event schema normally separates stable, frequently queried fields from irregular attributes and human-readable content. It also distinguishes the time an event occurred from the time the pipeline observed it, because delayed and replayed records can make those values differ.

A physical schema might begin with fields such as:

```text
event_id
occurred_at
observed_at
event_type
attributes
body
schema_version
```

This is a starting shape rather than a fixed schema. Fields used frequently for filtering, grouping, and correlation benefit from stable types and dedicated columns. Less common fields can remain in a structured attribute collection. Leaving every value inside an opaque body gives up much of the projection and data-skipping value of columnar storage, while promoting every possible attribute creates a wide and unstable schema.

`occurred_at` and `observed_at` deserve separate columns. A delayed or replayed record can describe an earlier event while arriving now. Preserving both timestamps makes ingestion delay and late data observable instead of silently changing the meaning of time-based queries.

A stable `event_id`, or another source-defined identity, gives retries something concrete to preserve. It does not require every query to deduplicate records, but it makes duplicate detection and repair possible when the delivery contract permits replay.

## Treat the visible dataset as a snapshot

<figure class="article-figure">
  <img src="{{ '/assets/images/articles/columnar-pipeline/snapshot-flow.png' | relative_url }}" alt="Events are written into immutable Parquet batches, selected by a snapshot manifest, queried by DuckDB, and returned as Arrow columns. Compaction creates a replacement file before atomically changing the manifest.">
  <figcaption>The manifest is the visibility boundary. Writers and compactors finish files first, then publish one atomic change to the set DuckDB may query.</figcaption>
</figure>

The logical data flow has two related paths: data files carry records, while metadata decides which data files readers may see.

```text
structured events
       |
       v
buffered micro-batch
       |
       v
unpublished Parquet file
       |
       +------------------+
       | metadata commit  |
       v                  v
immutable data files   current snapshot
       |                  |
       +--------+---------+
                |
                v
          DuckDB query
                |
                v
       Arrow record batches
                |
                +--> in-process consumer
                |
                +--> Arrow Flight client
```

A directory glob is convenient for exploration, but it is a weak definition of committed data. It cannot by itself distinguish a complete file from an interrupted write, an uncompacted source file from its replacement, or a file that belongs to a newer publication than the reader intended to observe.

Instead, each published data file is immutable and a small metadata record defines the current visible set. A reader resolves one snapshot and uses that exact file set for the duration of its query. A writer creates a complete file under a unique identity, durably stores it, and then commits new metadata that adds it to a snapshot. Publication is a metadata transition, not an in-place mutation of a data file.

This framing works across local filesystems and object stores because it does not depend on rename having the same atomicity everywhere. The storage system still needs a way to update the current metadata reference conditionally or transactionally, but data files can remain immutable objects with unique names.

## Publish complete Parquet micro-batches

Parquet is a durable encoded columnar format. A file contains row groups, each row group contains one column chunk for every column, and those chunks contain encoded pages. The layout lets analytical readers project selected columns and use statistics to avoid row groups that cannot match a filter. The [Parquet format documentation](https://parquet.apache.org/docs/concepts/) describes those physical units.

A writer groups event records into a micro-batch and periodically emits a Parquet file. Flush policy can consider elapsed time, record count, encoded size, or memory pressure. More frequent flushes reduce visibility latency but create more files and spend proportionally more work on file discovery and metadata. Larger batches reduce file count and can improve compression, but hold more uncommitted state and delay visibility.

Parquet metadata, including the file footer, must be complete before readers can use the file. The writer therefore produces an unpublished file first. Only after the complete object is durable does it add the file to the visible snapshot.

The acknowledgement boundary follows the desired delivery contract. A pipeline can acknowledge an input after its data file and snapshot commit are durable. It can also acknowledge earlier when an upstream system retains a replayable source position. The second choice moves durability responsibility upstream and makes idempotent replay part of the design.

Useful identities include:

- a source partition and position, when the source exposes them;
- a stable event ID, when the producer can assign one;
- a unique data-file ID;
- the input file IDs and operation ID of a compaction run;
- a monotonically advancing snapshot identity.

These identities do different jobs. Event identity supports record-level duplicate handling. File and operation identity make publication and compaction retries inspectable. Snapshot identity gives readers a stable view. Deterministic file names alone do not establish exactly-once delivery.

## Compact files without changing visibility twice

Incremental writers naturally create small files. Repeated analytical scans then pay discovery, metadata, open, and scheduling costs for every file. Compaction rewrites a bounded set of small files into fewer files that better match the read workload.

The safe unit of compaction is a snapshot operation:

1. Select a stable set of visible input files from one snapshot.
2. Read those inputs and write complete replacement files under new identities.
3. Commit a new snapshot that removes the inputs and adds the replacements together.
4. Retain the old files while any reader may still be using the previous snapshot.
5. Delete unreferenced files later through a separate garbage-collection policy.

Readers therefore see either the original input files or their replacements. They never infer visibility by noticing whichever files happen to be present in a directory.

DuckDB can perform the rewrite with SQL. The application supplies the input files selected from the snapshot rather than a mutable directory glob:

```sql
COPY (
    SELECT *
    FROM read_parquet(?, union_by_name = true)
    ORDER BY occurred_at
)
TO 'unpublished/compact-run-42.parquet'
(FORMAT PARQUET, COMPRESSION ZSTD);
```

The parameter represents a stable list of input files. The output path is not visible to readers until the snapshot commit replaces those inputs with the completed output.

Compaction can also normalize compatible schemas, choose row-group boundaries, and cluster records by common filters. Combining files and rewriting their meaning are separate decisions, however. A maintenance run that only reduces file count should not silently reinterpret historical fields.

This immutable-files-plus-snapshots design is a small table format. As it grows to support concurrent writers, optimistic commits, deletes, time travel, partition evolution, and safe garbage collection, it begins to reproduce the responsibilities of Apache Iceberg, Delta Lake, or Apache Hudi. Iceberg represents each table version as a snapshot whose manifest metadata identifies the applicable data files. [Delta Lake](https://docs.delta.io/delta-faq/) records commits in a transaction log alongside versioned Parquet files. [Hudi clustering](https://hudi.apache.org/docs/next/clustering/) plans file replacement and records it on a metadata timeline. The [Iceberg specification](https://iceberg.apache.org/spec/) and [maintenance documentation](https://iceberg.apache.org/docs/latest/maintenance/) show the same responsibilities through snapshots, manifests, compaction, and snapshot expiration.

The simple manifest remains useful when the requirements are genuinely small. An established table format becomes attractive when metadata behavior starts becoming a system of its own.

## Partition coarsely and cluster deliberately

Partitioning and clustering solve different parts of the read problem.

Partitioning selects whole files or directories before a Parquet scan begins. A coarse event-date partition can keep a query for one day from discovering years of data. High-cardinality keys such as request IDs, user IDs, or trace IDs usually make poor partition columns because they create many small partitions and files.

Clustering orders related records within the selected files. Sorting by `occurred_at`, or by a stable resource key followed by time, can tighten row-group min/max statistics and improve data skipping for common predicates. The best order follows measured query shapes rather than a universal rule.

Row-group size introduces another tradeoff. Larger groups offer longer sequential column chunks and more compression opportunity. Smaller groups provide more independent work and finer pruning when their statistics are selective. DuckDB's [Parquet guidance](https://duckdb.org/docs/stable/data/parquet/tips) recommends considering query parallelism, scan shape, memory use, and filter selectivity together.

These controls form a hierarchy:

```text
snapshot metadata  -> selects the authoritative file set
partitioning       -> excludes coarse ranges of files
row-group metadata -> skips ranges inside selected files
column projection  -> reads only needed fields
query predicates   -> evaluates the remaining values
```

Performance depends on the complete hierarchy. A columnar file format cannot compensate for a file layout unrelated to the queries being run.

## Query the snapshot directly with DuckDB

DuckDB can query Parquet without first loading the records into a long-running database service. The application resolves the current snapshot, supplies its file list, and executes SQL over that stable view:

```sql
SELECT event_type, count(*) AS event_count
FROM read_parquet(?)
WHERE occurred_at >= ? AND occurred_at < ?
GROUP BY event_type
ORDER BY event_count DESC;
```

DuckDB automatically applies projection pushdown so a query can read only the referenced columns. It also applies filter pushdown and can use Parquet statistics to skip row groups whose ranges cannot match the predicate. Its [Parquet documentation](https://duckdb.org/docs/stable/data/parquet/overview) describes both behaviors.

Skipping remains conditional. It depends on the predicate, available statistics, physical ordering, value distribution, and reader support for the relevant Parquet features. Query cost still includes metadata planning, I/O, decompression, decoding, and execution. Profiling representative queries is more useful than deriving a target file or row-group size from format folklore.

Query-in-place is a good fit when selected scans and aggregations dominate and storage files should remain the durable source of truth. Loading data into a managed database or search index can be a better read path when point lookups, low-latency full-text search, frequent updates, or continuously changing indexes dominate. A system may also retain Parquet as its durable analytical record while building a separate serving index for those access patterns.

## Evolve schemas by identity and meaning

File-backed datasets accumulate schema generations. Adding a nullable field is usually manageable because older records can supply null. Renaming a field, changing its type, changing its unit, or changing its semantic meaning requires more care.

`union_by_name` is convenient for reading additive schemas, but names are not durable field identity. A rename can appear indistinguishable from deleting one field and adding another. Parquet field IDs and table-format schema metadata provide stronger identity across renames. DuckDB also supports reading Parquet against an explicit field-ID-based schema.

A durable evolution policy records a schema version and defines how each supported generation maps into the current logical event model. That policy should distinguish:

- adding an optional field;
- widening a compatible physical type;
- renaming a field while preserving identity;
- changing a field's unit or interpretation;
- splitting one event type into several event types;
- retiring fields while historical files still contain them.

Compaction can materialize a normalized schema for older files, but readers may still need to understand earlier snapshots until retention removes them. Syntactic compatibility does not establish semantic compatibility.

## Return typed Arrow batches

Apache Arrow defines a language-independent columnar memory layout whose serialized unit is a record batch. A DuckDB integration can expose query results as Arrow batches, allowing compatible analytical libraries to consume typed arrays without first formatting every row as JSON or another text representation. The [Arrow columnar format](https://arrow.apache.org/docs/format/Columnar.html) is designed for vectorized access and permits zero-copy reconstruction in supported IPC and shared-memory arrangements.

That property should not be extended to the whole pipeline. Parquet is an encoded storage format, so reading normally requires I/O, decompression, decoding, and construction of execution vectors. DuckDB has its own vectorized representation. Whether a result shares buffers with Arrow depends on the integration, types, ownership rules, and operations used.

The reliable claim is that aligned columnar representations avoid some row-wise serialization and transposition. Stronger zero-copy claims belong to benchmarks and buffer-level inspection of the exact library versions and execution path.

## Carry columnar buffers through a Protobuf envelope

[Arrow Flight](https://arrow.apache.org/docs/format/Flight.html) is useful here less because it defines another RPC surface and more because of how its Protobuf messages carry Arrow IPC data. The protocol separates a small descriptive envelope from the bulk columnar payload:

```protobuf
message FlightData {
    FlightDescriptor flight_descriptor = 1;
    bytes data_header = 2;
    bytes app_metadata = 3;
    bytes data_body = 1000;
}
```

`data_header` contains the Arrow IPC message metadata that describes the schema or record-batch layout. `data_body` contains the corresponding Arrow buffers. `app_metadata` carries application-defined coordination data. The descriptor is included when a client begins an upload stream; downloads are selected through the preceding Flight request and ticket exchange.

This arrangement avoids representing an analytical result as a repeated Protobuf message for every row. A row-oriented Protobuf response would normally require the producer to walk execution vectors, construct messages field by field, serialize their tags and values, and make the consumer reconstruct columns if its next operation is analytical. Flight instead puts the record-batch description in the header and carries the already columnar buffers as an opaque byte payload. The official [Protocol Buffers encoding guide](https://protobuf.dev/programming-guides/encoding/) describes `bytes` as a length-delimited wire value, which lets the envelope frame the Arrow body without interpreting its individual columns and values.

The large `data_body` field is deliberately separate from the descriptive fields and appears last in the Protobuf definition. Flight implementations can use that shape to handle the body as a sidecar and minimize intermediate copying. Protobuf still supplies a portable, evolvable contract for the envelope, while Arrow IPC supplies the physical representation of the tabular data.

```text
Protobuf FlightData
    |
    +--> descriptor and application metadata
    |
    +--> Arrow IPC header
    |       schema, field nodes, buffer offsets, buffer lengths
    |
    +--> Arrow IPC body
            validity bitmaps, offsets, values, dictionary data
```

The mapping is efficient because the IPC header tells the receiver how to reconstruct typed Arrow arrays from the body buffers. The receiver does not need to parse a message for every record or transpose row objects back into columns. Compatible implementations can expose those buffers directly or with few transformations, subject to alignment, ownership, compression, transport, and language-runtime constraints.

This still does not make the network path universally zero-copy. Protobuf and gRPC add framing, the operating system moves bytes through network buffers, TLS may introduce more work, and an implementation may copy data while assembling or receiving a message. The defensible property is that the protocol preserves the Arrow batch layout and avoids mandatory row-wise serialization of the bulk result.

Flight uses gRPC for streaming and transport concerns, but those mechanics are secondary to this data representation. The same separation is useful in an application-specific protocol: small typed Protobuf commands and metadata can coordinate work while Arrow IPC carries large tabular inputs or results. Flight SQL standardizes that composition for SQL commands and database metadata.

An in-process consumer can use Arrow batches without Flight or Protobuf. Once the boundary crosses processes, authentication, TLS, authorization, query limits, cancellation, timeouts, result-size limits, and resource governance matter alongside the encoding and transfer path.

## Make lifecycle and correctness explicit

The storage composition does not determine the pipeline's correctness policy. A complete design states its answers to these questions:

- When is an input record durably committed and acknowledged?
- Which upstream source positions can be replayed?
- Can a retry create another physical copy of the same logical event?
- How does a reader choose and retain one snapshot?
- How are concurrent snapshot commits detected and retried?
- How are interrupted or orphaned files distinguished from visible files?
- How do late events enter a time range that has already been compacted?
- When can files removed from the current snapshot be deleted safely?
- Which schema generations must remain readable?
- How do retention and deletion interact with replay, audit, and legal requirements?
- Where are encryption, access control, tenant isolation, and sensitive-field handling enforced?

Late data is an ordinary lifecycle case rather than a special failure. A new file can be added to an older event-time partition through a later snapshot. A subsequent compaction may incorporate it. Queries that require reproducibility can retain the snapshot identity they used, while queries for the latest state resolve the current snapshot.

Retention should also operate through metadata. Removing a file from the latest snapshot and deleting its object are separate events. Keeping them separate protects readers of older snapshots and makes recovery possible within the retention window.

## When the pattern fits

This architecture fits structured, append-heavy events queried through time ranges, projections, filters, and aggregations. It is attractive when immutable file storage should remain the durable record, query latency can accommodate selected scans, and the team is prepared to own or adopt explicit file-lifecycle metadata.

It fits less naturally when every event must be searchable immediately, substring and relevance search dominate, records are updated frequently, point reads are the primary operation, or cross-record transactions define the workload. Those requirements favor a database or search system designed around the corresponding access path, possibly alongside the file-backed analytical record.

The scale threshold is not only data volume. A modest dataset with many concurrent writers, strict snapshot isolation, frequent schema changes, and complex deletion rules can justify a table format. A much larger append-only dataset with one writer and simple retention may remain understandable with a small manifest.

## Synthesis

Parquet, DuckDB, and Arrow compose around a shared analytical shape. Parquet stores immutable typed columns, DuckDB applies vectorized SQL to a selected file set, and Arrow exposes typed result columns to downstream consumers. Flight carries those batches across a service boundary when remote access warrants one.

The durable architecture comes from the boundaries around those tools. Events have explicit logical identities and timestamps. Writers publish complete immutable files. Snapshot metadata defines visibility. Compaction replaces a stable input set in one commit. Partitioning excludes coarse ranges, clustering improves row-group pruning, and schema evolution preserves both field identity and meaning.

A directory of Parquet files becomes a dependable dataset when its publication and lifecycle rules are as explicit as its file format. The same rules also reveal when the design has grown into a table format and should adopt the machinery already built for that job.
