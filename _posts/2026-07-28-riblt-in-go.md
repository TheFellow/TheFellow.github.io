---
title: "Building a Generic RIBLT in Go"
date: 2026-07-28 12:00:00 -0700
last_modified_at: 2026-08-02 12:00:00 -0700
permalink: /notes/riblt-in-go/
excerpt: "A step-by-step implementation of generic, rateless set reconciliation in Go, from XOR-coded cells through peeling and measured communication."
icon: "sitemap"
tags: ["Go", "Generics", "RIBLT", "Distributed Systems", "Algorithms"]
---

Suppose an upstream and a downstream each hold a large set, most entries agree, and I need to discover the few that do not. Sending the whole upstream set works, but makes communication follow the size of the data instead of the size of the disagreement.

A Rateless Invertible Bloom Lookup Table, or RIBLT, changes that relationship. The upstream emits an open-ended stream of coded cells. The downstream folds its local set into those cells and keeps peeling. Once the prefix contains enough information, it has both sides of the symmetric difference and tells the upstream to stop. Neither side has to estimate the difference before transmission begins.

I built [go-riblt](https://github.com/TheFellow/go-riblt) to make that process executable. The repository has a generic library, a cell-by-cell walkthrough, examples for records and documents, a scaling experiment, property and fuzz tests, and benchmarks. I will follow the walkthrough's concrete sets throughout this note:

```text
upstream:   [100 101 102 103]
downstream: [100 102 104]
```

The answer is small: add `101` and `103` downstream, then remove `104`.

## Start with the algebra a symbol needs

The RIBLT does not need to know what a symbol means. It does need an identity, a reversible way to combine symbols, a clear ownership boundary, and two hashes with separate jobs. Go generics let the library state that contract without requiring methods on `T`:

```go
type Codec[T any] interface {
    Zero() T
    IsZero(T) bool
    Clone(T) T
    Equal(a, b T) bool
    Validate(T) error
    XOR(a, b T) T
    MappingHash(T) uint64
    Checksum(T) uint64
    CompatibilityID() [32]byte
}
```

XOR supplies a Boolean group. Its identity and self-inverse properties are what make coding reversible, while `IsZero` lets the decoder recognize that identity without requiring `T` to be comparable:

```text
x XOR 0 = x
x XOR x = 0
(a XOR b) XOR b = a
```

The demonstration's `Symbol` contains one `uint64`, so its XOR is ordinary bitwise XOR. A richer record still works when its codec has a fixed-width, reversible representation. `XOR` must be pure. `Clone` gives the library independent storage for a slice or other mutable representation, `Equal` distinguishes actual duplicates even when both hashes collide, and `Validate` rejects values outside the algebra before they enter a sketch. `CompatibilityID` identifies the complete codec configuration, including its key and representation parameters.

This pluggability is the central generic design choice, rather than an optional abstraction around the algorithm. Go cannot derive a reversible XOR for `T any`. A struct may contain padding, a string has variable length, a map has no canonical order, and a slice needs an ownership policy. `Encoder[T]`, `Decoder[T]`, `Sketch[T]`, `HashedSymbol[T]`, and `CodedSymbol[T]` carry the application's symbol type, while `Codec[T]` supplies the exact algebra the algorithm uses.

Most applications do not need to write that contract themselves. The package includes keyed defaults for `uint64` and fixed-width byte strings:

```go
key := []byte("0123456789abcdef0123456789abcdef")
uints, err := riblt.NewUint64Codec(key)
if err != nil {
    log.Fatal(err)
}
ids, err := riblt.NewBytesCodec(32, key)
if err != nil {
    log.Fatal(err)
}
```

The example key is deliberately visible, so it is only suitable for a walkthrough. A real deployment provisions at least 16 bytes of secret key material through its authenticated surrounding protocol. `BytesCodec` requires one width because zero-padding variable-length values would make XOR ambiguous. Constructor errors must be checked. A failed construction returns an unusable zero codec, and `NewEncoder`, `NewDecoder`, `NewSketch`, and `Hash` reject failed or otherwise uninitialized built-in codecs.

## Give the two hashes different responsibilities

`Hash` validates and clones a value, computes both hashes, and packages them for diagnostics:

```go
type HashedSymbol[T any] struct {
    Symbol      T
    MappingHash uint64
    Checksum    uint64
}
```

Insertion does not accept a `HashedSymbol`. Each public insertion boundary validates, clones, and hashes the value itself, so a caller cannot inject cached hashes that disagree with the symbol. The mapping hash seeds a deterministic sequence of cell indexes. Every symbol begins in cell zero, then follows an increasingly sparse sequence generated with the gap distribution from the RIBLT paper. The implementation keeps each symbol's next index in a min-heap. To emit cell `i`, the encoder XORs precisely the symbols whose next index is `i`, advances those mappings, and moves on to `i+1`.

The checksum has a separate role. The built-in codecs derive both 64-bit hashes with HMAC-SHA-256, using separate domains for placement and singleton validation. A coded cell has three fields:

```go
type CodedSymbol[T any] struct {
    Symbol   T
    Checksum uint64
    Count    int64
}
```

The symbol and checksum fields are accumulated with XOR. The signed count is accumulated with addition. A count of `+1` or `-1` only suggests that the XOR field contains one remaining symbol. The decoder accepts it as a singleton only when `Checksum(cell.Symbol)` equals the accumulated checksum. Domain separation between placement and validation matters because these are independent decisions.

Keying prevents a party that does not know the key from cheaply choosing collisions. It does not make a synchronization peer that shares the key non-adversarial, so the surrounding protocol still has to authenticate peers and bound their work. The two hashes also fail differently. A checksum collision can admit a false singleton, while a mapping-hash collision gives distinct symbols the same placement sequence and can prevent reconciliation from converging. An independent checksum cannot repair that identical placement. Both 64-bit collision cases are unlikely, not impossible.

## Stream cells without guessing a table size

The upstream registers its complete set, then starts the stream:

```go
codec, err := riblt.NewUint64Codec(key)
if err != nil {
    log.Fatal(err)
}
encoder, err := riblt.NewEncoder[uint64](codec)
if err != nil {
    log.Fatal(err)
}
for _, value := range upstream {
    _ = encoder.Add(value)
}

cells := encoder.Cells()
```

`Cells` returns an `iter.Seq2[CodedSymbol[T], error]`. Constructing the sequence does not emit anything. Each range iteration asks for exactly one more coded cell, which fits the rateless algorithm directly: computation follows demand, and breaking the range stops production without preparing another cell. The sequence is tied to the encoder's current position rather than replayable. A later range resumes with the following cell.

The encoder exposes this iterator as its only streaming interface. A transport or event loop that needs pull-style control can adapt it with the standard library rather than requiring a second encoder API:

```go
next, stop := iter.Pull2(encoder.Cells())
defer stop()

cell, err, ok := next()
```

The caller must invoke `stop` when it finishes early. Starting iteration also seals the source set. Adding another source symbol after the first cell is requested is rejected because it would change cells the receiver has already consumed.

The downstream similarly registers its local set before the first coded cell:

```go
decoder, err := riblt.NewDecoderWithLimits[uint64](codec, riblt.DecoderLimits{
    MaxCells:          10_000,
    MaxLocalSymbols:   1_000_000,
    MaxDecodedSymbols: 10_000,
})
if err != nil {
    log.Fatal(err)
}
for _, value := range downstream {
    _ = decoder.AddLocal(value)
}
```

For each incoming cell, `AddCoded` subtracts the initial downstream symbols scheduled for that index. Because subtraction and addition are the same operation for the XOR fields, the sign appears in `Count`. Shared symbols cancel, an upstream-only symbol contributes `+1`, and a downstream-only symbol contributes `-1`.

Cells are positional and must arrive in order. An actual protocol therefore needs ordered delivery or sequence and retransmission machinery, plus a completion acknowledgement so the upstream knows when to stop. The decoder limits bound cells admitted, local symbols registered, and symbols peeled. The transport must separately bound bytes and time.

## Peel one discovery into the rest of the sketch

After adding a cell, `TryDecode` processes every cell currently known to be a validated singleton or a resolved zero. A zero is resolved only when its count and accumulated checksum are both zero and `IsZero` confirms that its XOR symbol is the identity. A `+1` singleton is recorded as remote, meaning upstream-only. A `-1` singleton is recorded as local, meaning downstream-only.

The important step is propagation. Once the decoder learns a symbol, its mapping hash reconstructs every cell in the received prefix that contains that symbol. The decoder removes it from those cells. That can expose another singleton, which enters the ready queue and repeats the process. Peeling is therefore not a collection of isolated cell decisions. Each discovery simplifies the remaining system.

The runnable walkthrough makes the chain visible:

```sh
go run ./cmd/walkthrough
```

For the sample sets, the upstream sends four cells. After the second cell is incorporated, the decoder has peeled downstream-only `104`. The fourth cell triggers enough propagation to peel upstream-only `101` and `103`; all four received cells are then resolved, and `Complete` becomes true.

```text
add to downstream:      [101 103]
remove from downstream: [104]
communication: 4 coded cells, about 96 payload bytes
```

The 96-byte figure uses the demonstration's accounting convention of three eight-byte fields per cell. It does not include framing or serialization. Result order is also an implementation detail, so callers should treat both result slices as sets.

## The protocol loop is deliberately small

With setup complete, reconciliation is this loop:

```go
for cell, err := range encoder.Cells() {
    if err != nil {
        return err
    }
    if err := decoder.AddCoded(cell); err != nil {
        return err
    }
    if err := decoder.TryDecode(); err != nil {
        return err
    }
    if decoder.Complete() {
        break
    }
}

add := decoder.Remote()
remove := decoder.Local()
```

The early `break` is the downstream's completion signal inside this in-process example. Over a network, the receiver sends that acknowledgement to the upstream, which stops pulling from the same sequence.

`Remote` is what exists only at the upstream, and `Local` is what exists only at the downstream. Those names describe the decoder's perspective, which is worth keeping explicit when the result becomes an application update. The library clones mutable symbols on ingestion, storage, coded-cell output, and decoded-result output. Mutating a caller-owned byte slice after `Add`, or mutating a returned result, does not change internal state.

The package also includes `Sketch[T]` for a fixed-length prefix. Two sketches of the same length and `CompatibilityID` can be built independently, subtracted cell by cell, and decoded. A mismatch in codec semantics, key, byte width, or protocol version is rejected instead of producing meaningless cells. Successful subtraction seals its receiver as a signed difference. `Cells` and `Decode` remain available, but the sealed sketch cannot be mutated or used as either operand of another subtraction. This makes the membership lifecycle explicit instead of letting later `Add` or `Remove` calls consult the original left-hand set. That is useful when a prefix length is already part of the surrounding protocol. The streaming encoder and decoder preserve the rateless advantage: no table length has to be chosen before seeing whether peeling succeeds.

## Choose a symbol representation for the project

The integer walkthrough isolates the algorithm, but a project still has to decide what one set member means. The representation must have a fixed-width XOR algebra because an encoded cell can contain a combination of several symbols. It is not enough for only the original application values to be valid. Every intermediate bit pattern produced by XOR must also be accepted by the codec.

That gives me four useful patterns:

| Project value | RIBLT symbol | Encoding choice |
| --- | --- | --- |
| Numeric ID or version | `uint64` | Use `NewUint64Codec`. |
| UUID, digest, or fixed binary key | fixed-width `[]byte` | Use `NewBytesCodec`. |
| Fixed-layout record | the complete struct | XOR each fixed-width field and hash one canonical encoding. |
| Large or variable value | content digest | Reconcile digests, then transfer missing bodies separately. |

Strings, maps, pointers, and variable-length slices do not directly provide that algebra. I can place a small bounded value into a fixed-width byte slot, or I can move the variable value out of the RIBLT and use its digest as the symbol.

### Carry a complete record

The records example runs an `Encoder[Record]` and `Decoder[Record]` where the symbol is the whole application value:

```go
type Record struct {
    ID       uint64
    Revision uint64
    Owner    [16]byte
    Digest   [32]byte
}
```

Its custom codec XORs `ID` and `Revision` as integers, XORs each byte of `Owner` and `Digest`, and hashes a canonical 64-byte encoding through `BytesCodec`. The codec's `CompatibilityID` also includes a record-specific version, so it cannot be confused with an unrelated 64-byte representation.

The example gives record `2` revision `2` downstream and revision `3` upstream. Because the complete record is the set member, a mutation is a set difference. Decoding reports the old record in `Local` and the new record in `Remote`:

```text
add or replace from upstream:
  id=2 revision=3 owner="Grace" digest=24571a7d
  id=3 revision=1 owner="Linus" digest=1dcefb97
remove downstream versions:
  id=2 revision=2 owner="Grace" digest=100802fe
decoded after 4 coded cells
```

The application can pair those values by `ID` and apply them as one update. This keeps conflict and update semantics outside the set-reconciliation primitive while preserving the complete values needed to make that decision.

```sh
go run ./cmd/structs
```

### Carry a bounded text value

The documents example places an actual UTF-8 body in a 256-byte slot. The first two bytes hold the payload length, the body follows, and the remaining bytes are zero padding. `BytesCodec` then treats the entire slot as one symbol. The explicit length distinguishes the text from its padding and permits embedded zero bytes.

This pattern fits a project with a meaningful maximum record size. One changed sentence appears as one downstream-only slot and one upstream-only slot, just like the mutated struct:

```text
documents to add:
  "Go generics let the algorithm remain independent of its symbols."
  "This paragraph exists only upstream."
documents to remove:
  "Go generics separate the algorithm from its symbols."
decoded after 3 coded cells
```

```sh
go run ./cmd/documents
```

Padding every large document to one shared maximum would waste coded-cell bandwidth. Large values need another layer.

### Reconcile content-addressed chunks

The chunks example splits a document into fixed-size pieces and computes a SHA-256 digest for each piece. Those 32-byte digests are the RIBLT symbols. An ordered manifest stores the digest sequence, while a content-addressed map stores one body per digest:

```text
manifest: [digest-A digest-new digest-B digest-added]
chunks:   digest -> body
```

This separation matters because RIBLT reconciles sets. The chunk store naturally deduplicates repeated content, but the manifest preserves ordering and repeated occurrences. After decoding, `Remote` is precisely the set of chunk bodies the downstream should request. Each received body is checked against its digest, then the complete rebuilt document is checked against the document digest.

The runnable example shares two of four upstream chunks. It discovers two chunks to fetch and one old downstream chunk that the new manifest no longer references:

```text
upstream manifest: 4 chunks, 128 bytes
missing downstream: 2 chunks
obsolete downstream: 1 chunks
RIBLT decoded after 5 coded cells
transferred 64 chunk bytes instead of 128 document bytes
rebuilt document verified: true
```

```sh
go run ./cmd/chunks
```

The demonstration uses fixed-size chunks, so an insertion can shift later boundaries. A content-defined chunker can retain more shared chunks across insertions without changing the RIBLT layer. The surrounding protocol carries the ordered manifest and requested chunk bodies; RIBLT only discovers which fixed-width identities differ.

## Measure difference rather than set size

The repository's experiment holds the symmetric difference fixed while increasing each set from 1,000 to 10,000 entries:

```text
set size  difference  cells sent  cells/difference
    1000           2           3              1.50
   10000           2           3              1.50
    1000          10          14              1.40
   10000          10          13              1.30
    1000          50          76              1.52
   10000          50          69              1.38
```

These are deterministic observations for the demonstration's generated sets and hashes. They show the behavior I wanted to inspect: a tenfold increase in total set size did not produce a tenfold increase in transmitted cells. They are not a proof of an exact ratio for every set.

The Go benchmark uses 10,000 shared entries and varies the symmetric difference. On an Intel i5-1038NG7, the original deterministic demonstration codec reported between `1.000` and `1.906 coded/difference` for differences from 1 through 1,024. Its end-to-end timings ranged from about 7.7 ms to 61.6 ms per reconciliation. The benchmark deliberately rebuilds and hashes both 10,000-entry inputs on every iteration, so it measures setup and hashing as well as peeling.

The safer default changes that profile. A local microbenchmark of `Uint64Codec` computing both HMAC-SHA-256 hashes took about 1.94 microseconds, 1,088 bytes, and 16 allocations per value, while one mapping step took about 14 ns with no allocations. The default favors an understandable keyed boundary over maximum throughput. A deployment should benchmark its complete workload, then consider an audited custom codec or internal immutable hash caching when that cost matters. Public insertion still recomputes hashes at the trust boundary.

## What the tests establish

`go test ./...` exercises more than the happy path. The suite checks known reconciliation results, equal sets, fixed-length sketch subtraction, deterministic mapping and keyed-hash vectors, reset behavior, duplicate and lifecycle errors, and 100 seeded random set constructions. It also verifies mutable-value ownership, wrong-width rejection, failed and zero-value codec rejection at every public boundary, collision-correct duplicate detection, mapping-collision non-convergence, incompatible and sealed sketch rejection, side-effect-free decoder admission failures, and decoder limits. The examples add tests for the record codec's XOR algebra, changed record and document reconciliation, UTF-8 and bounded document sizes, chunk deduplication, missing chunk discovery, reconstruction, and corrupt chunk rejection.

Ordinary `go test ./...` runs the fuzz seed corpus, not sustained fuzzing. The two fuzz targets need separate invocations because Go runs one target at a time:

```sh
go test -fuzz=FuzzReconcile -fuzztime=30s
go test -fuzz=FuzzMalformedCodedBytes -fuzztime=30s
```

They generate additional set constructions and malformed coded byte symbols.

Together, those tests demonstrate the implementation's behavior for the exercised codecs and inputs. The probabilistic algorithm still depends on good mapping hashes, and checksum collisions remain possible in principle.

## Keep the algorithm inside a complete protocol

The built-in codecs provide keyed, domain-separated hashing and the decoder can enforce finite symbol and cell limits. Those properties make the library a more suitable component for a deployed design, but they do not turn the component into a complete synchronization protocol.

`ProtocolVersion`, currently `go-riblt/v1`, fixes mapping constants, floating-point gap calculation, cell semantics, and built-in hash domains. A surrounding authenticated handshake should exchange that version and `CompatibilityID`, then reject either mismatch. The synchronization protocol still has to define canonical cell serialization and framing, authentication and key agreement, byte limits and deadlines, ordering and retransmission, completion acknowledgement, and atomic application of additions and removals. The mutable encoder, decoder, and sketch types are not safe for concurrent method calls, so callers must also serialize access or provide their own synchronization.

RIBLT reconciles sets, not arbitrary collections or application state. The implementation rejects true duplicates using `Equal` within a hash bucket rather than treating a hash pair as identity. If multiplicity matters, I would encode a unique occurrence identifier or choose a multiset protocol.

The result is a hardened reconciliation primitive with explicit algebra, ownership, compatibility, and resource contracts. Running the walkthrough turns those pieces from a paper description into a sequence I can inspect: combine symbols, subtract local state, validate a singleton, propagate it, and stop when every received cell is resolved. Building a production synchronization system still means supplying the wire and state-transition guarantees around that primitive.

The [go-riblt repository](https://github.com/TheFellow/go-riblt) contains the implementation and every command discussed here. Start with `go run ./cmd/walkthrough`, then read `codec.go`, `window.go`, and `decoder.go` in that order. After the algorithm is familiar, run `cmd/structs`, `cmd/documents`, and `cmd/chunks` to compare how the same generic core fits different application data. That path moves from the reconciliation mechanics to the representation decision a project has to make.
