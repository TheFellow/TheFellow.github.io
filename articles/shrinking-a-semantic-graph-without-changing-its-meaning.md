<!-- Generated from https://thefellow.github.io/articles/shrinking-a-semantic-graph-without-changing-its-meaning/ by scripts/generate_llm_content.py; do not edit. -->

# Shrinking a Semantic Graph Without Changing Its Meaning

Source: [https://thefellow.github.io/articles/shrinking-a-semantic-graph-without-changing-its-meaning/](https://thefellow.github.io/articles/shrinking-a-semantic-graph-without-changing-its-meaning/)

## Pyramid summary

- **~2 words:** Compact graph storage
- **~8 words:** Numeric identities and hot/cold records preserve one stable public graph.
- **Expanded:** How Weave separates its stable graph model from a compact private schema with numeric identities, interned strings, hot and cold records, exact ordering, and rebuild-only evolution.

## Full content

**Part 6 of [Building Weave](/series/weave.md).**

The first repository-scale Weave measurement made an uncomfortable fact visible. Compact semantic identities reduced a 7.54 GB graph to 1.11 GB, but the remaining database was still much larger than the source it described. A normalized graph repeats exactly the strings that tend to be longest: stable symbol IDs, unit IDs, document IDs, providers, versions, languages, roles, evidence classes, and relationship endpoints.

Changing those public identities would make the storage problem look smaller by weakening the product. [Weave](https://github.com/TheFellow/weave) instead gives its private storage schema an independent version. [`graph.SchemaVersion`](https://github.com/TheFellow/weave/blob/main/internal/graph/model.go) continues to describe stable normalized facts and exports. Storage v2 changes how those same facts are encoded, indexed, verified, and rebuilt.

<figure class="article-figure">
  <img src="/assets/images/articles/weave/compact-storage.svg" alt="Stable public graph facts enter a private storage codec. Long repeated strings become reference-counted intern and entity records. Narrow hot records hold numeric lookup keys and canonical ordering fields, while cold detail records hold ranges, providers, evidence, and document references. Batched hydration reconstructs the unchanged public graph, and verification checks every indirection and reference count.">
  <figcaption>Storage v2 changes representation, not meaning. Compact hot indexes answer bounded queries; cold details and shared dictionaries reconstruct the same public facts.</figcaption>
</figure>

## Version representation separately from meaning

A graph schema and a database schema answer different compatibility questions. The graph schema defines units, documents, symbols, occurrences, relationships, evidence, and canonical order. Agents, exports, adapters, and query responses depend on it. The storage schema describes bstore records inside disposable per-worktree state.

Keeping those versions separate lets the internal representation change without creating a new semantic format. Tests build the same rich facts in legacy v1 and v2 databases, export both through the public model, and require deep equality. Unicode identities, long paths, long display names, large ranges, providers, evidence, and relationships all have to survive the round trip.

The same rule applies to bounded reads. Storage v2 returns forward and reverse adjacency in the same canonical order as v1 and reports truncation at the same boundary. A smaller index is not an excuse to make `--limit 3` select a different three edges.

## Replace repeated strings with internal identities

Stable graph IDs remain strings at the application boundary, but v2 maps them to compact unsigned integers inside the database. An entity table assigns one numeric identity to each stable symbol or relationship endpoint. It represents both materialized symbols and open external endpoints, so an edge can retain a target that has no local symbol record.

Provider names, provider versions, languages, symbol kinds, occurrence roles, and other repeated values use a smaller intern table. Evidence and relationship kinds have checked numeric codes. Edge-kind codes deliberately follow lexical public order so a compound index can return canonical results before applying a bound.

Both shared tables carry reference counts. Replacing or deleting a unit releases exactly the strings and entities its documents, symbols, occurrences, details, and edges used. A cross-unit edge can keep an entity alive after the unit that materialized its symbol disappears. Once the final reference is gone, the dictionary row can disappear too.

That lifecycle is more involved than copying strings into every row, so it is tested as a first-class invariant. Two units share providers and identities, one unit is removed, the remaining external edge retains its endpoint, and deleting the second unit must leave no intern, entity, or detail records behind.

## Keep hot rows narrow

Most graph queries do not need every field. Symbol search needs internal identity, names, kind, unit, and document lookup. Adjacency needs numeric endpoints, relationship kind, and fields required for deterministic order. Provider, evidence, source range, and optional document provenance are important when returning a complete fact but make every hot index wider if stored inline.

Storage v2 splits those shapes. A narrow symbol record carries searchable names and numeric references; a symbol-detail record carries definition range, provider, and evidence. Occurrences and edges receive the same hot/cold pairing. Queries fetch details only for the bounded rows they will return.

Edges preserve stable endpoint strings beside their numeric `From` and `To` lookup keys. Those strings are not redundant by accident. They are ordering keys that keep the result byte-for-byte equivalent to `graph.CompareEdges` before truncation. Numeric identity accelerates lookup; stable identity preserves public determinism.

Token postings also use numeric symbol and unit IDs. A prefix search can find a bounded candidate set without repeating full stable identities throughout the index, then hydrate only the selected symbols.

## Hydrate in batches, fail on broken indirection

Compact rows become useful only if reconstruction stays bounded. Hydration collects the internal unit, document, entity, detail, and intern IDs needed for a result, sorts and compacts them, loads each record family in batches, then rebuilds public graph values.

Missing dictionary entries, missing entities, absent cold details, or invalid enum codes are logical corruption. The codec does not return a partly populated fact or replace an unknown provider with an empty string. It classifies the index as corrupt and tells the caller to rebuild disposable state.

Full export performs the same reconstruction across every record family and sorts the public snapshot canonically. The machine-wide [aggregate cache](/articles/caching-a-federated-graph-without-weakening-freshness.md) receives its hot symbol and edge stream through this codec too. Compact local storage does not create an alternative fact type for acceleration.

## Replace one unit atomically

Incremental indexing still owns facts by compilation unit. Before a replacement, Weave validates every incoming batch. Inside the write transaction it loads the old unit's owned rows and cold details, counts the intern and entity references they hold, removes tokens and dependent records in safe order, releases shared references, and inserts the replacement in canonical stable-ID order.

That transaction either installs the complete new unit or retains the complete old one. A conflicting symbol identity after the unit and document have begun staging must roll everything back. Multi-unit incremental publication still prevalidates all batches before its bounded transaction sequence begins, while the freshness-generation marker makes an interrupted larger refresh observably stale.

## Verify the representation as well as the graph

Public graph verification can catch a dangling edge after facts are hydrated. It cannot explain why hydration itself failed. Storage v2 adds a lower-level verification pass over its private invariants.

The verifier checks unit ownership, document references, numeric symbol identities, occurrence identities, edge endpoints, matching hot and cold rows, orphaned detail records, intern reference counts, and entity reference counts. Issues retain stable record and document context when it can be recovered. A missing edge-detail row, for example, becomes a fatal `missing-edge-detail` issue rather than an opaque export failure.

Physical compaction remains separate. It copies a closed database through bbolt's compactor into a temporary file and replaces the original only after the compacted database is complete. Logical verification proves relationships among records; compaction reclaims pages. Neither changes public facts.

## Reject legacy state before touching it

Per-worktree indexes are derived state, so storage v2 does not carry a migration that rewrites a large v1 database in place. It rejects the old schema with a direct instruction to remove that exact index and run `weave index` again.

There is a subtle safety problem: registering new bstore record definitions against an old file can begin automatic structural conversion before Weave decides the version is unsupported. The open path therefore reads the frozen metadata record through bbolt's read-only API first. Only a supported v2 marker allows the process to reopen the file and register v2 records. A regression test compares every legacy byte before and after rejection.

This is one of the advantages of disposable state. Source, configuration, and reviewed relationships remain authoritative. A schema change can prefer a clean rebuild over a risky compatibility layer, while a stable graph export preserves the meaning users and tools depend on.

## Borrow storage mechanics without borrowing a new product

The design review kept the boundary deliberately narrow: retain bstore and bbolt, preserve Weave's normalized graph, and improve the representation with measured changes. bstore already provides packed records, integer sequences, compound indexes, and transactions. Its constraint is equally important. Every index repeats its indexed fields and primary key, so long string identities become expensive quickly. It also has no join or projection API, which leaves interning, hot/cold splits, and lifecycle accounting to Weave.

bbolt remains a good match for single-file local derived state, one writer with many readers, and explicit physical compaction. Its files are not portable release artifacts, and deleted pages do not shrink the file until a rewrite. Those properties reinforce Weave's existing contract: back up source, not the index.

[Source Code Intelligence Protocol](https://github.com/sourcegraph/scip) provides the most important counterweight. SCIP keeps human-readable stable symbol strings at its interchange boundary because opaque global IDs make debugging and incremental index production harder. Weave adopts the same public stance while using numeric identities only as private join keys. Graph databases such as MillenniumDB support the internal choice by showing how fixed-width identities reduce repetition in adjacency indexes, but Weave does not adopt a second graph engine, a whole-graph memory mirror, or a columnar snapshot. Atomic per-unit replacement matters more here than analytical scan throughput.

## Measure the representation, not the aspiration

The retained comparison builds representative v1 and v2 databases from exactly the same facts: one unit, 200 documents, 5,000 long SCIP-like symbol IDs, 5,000 definition occurrences, 4,999 call edges, full ranges, long fingerprints, and repeated categorical strings. V1 occupies 96,784,384 bytes. V2 occupies 63,553,536 bytes, a 34.3% reduction.

That win is intentionally smaller than an early spike. Letting numeric row IDs break ties in candidate indexes saved more space but changed which bounded results survived after unit replacement. The final schema spends bytes on stable-ID ordering keys because exact query and truncation behavior outrank a prettier size ratio.

The performance results are mixed in useful ways. A full prefix search limited to 50 symbols has overlapping latency and roughly 22% fewer allocations. One-edge adjacency is slower because returning full evidence now fetches a separate cold detail. Complete export is 34% slower, and replacing the roughly 15,200-fact unit is 17% slower. Those paths pay for joining more record families. Opening the fixture is effectively equivalent, while physical compaction is about 24% faster and allocates 42% fewer bytes.

This is the result I want from a storage benchmark: a decision boundary, not a victory lap. Storage v2 materially reduces the representative file, keeps prefix lookup interactive, and preserves stable identities, deterministic export, bounded ordering, provenance, and generation semantics. It also records the cost of full materialization instead of hiding it by dropping evidence or moving verbose fields back into every hot index.

The important contract is already testable: public snapshots, bounded ordering, truncation, and hot-fact scans remain equivalent; invalid indirection is visible; legacy bytes are not mutated; incremental deletion releases shared state correctly. Storage can become denser without asking the rest of Weave to learn a new meaning for its graph.
