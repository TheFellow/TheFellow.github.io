<!-- Generated from https://thefellow.github.io/notes/riblt-in-go/ by scripts/generate_llm_content.py; do not edit. -->

# Building a Generic RIBLT in Go

Source: [https://thefellow.github.io/notes/riblt-in-go/](https://thefellow.github.io/notes/riblt-in-go/)

## Pyramid summary

- **~2 words:** Rateless reconciliation
- **~8 words:** A generic Go RIBLT reveals streaming set reconciliation step by step.
- **Expanded:** A step-by-step implementation of generic, rateless set reconciliation in Go, from XOR-coded cells through peeling and measured communication.

## Full content

Suppose an upstream and a downstream each hold a large set, most entries agree, and I need to discover the few that do not. Sending the whole upstream set works, but makes communication follow the size of the data instead of the size of the disagreement.

A Rateless Invertible Bloom Lookup Table, or RIBLT, changes that relationship. The upstream emits an open-ended stream of coded cells. The downstream folds its local set into those cells and keeps peeling. Once the prefix contains enough information, it has both sides of the symmetric difference and tells the upstream to stop. Neither side has to estimate the difference before transmission begins.

I built [go-riblt](https://github.com/TheFellow/go-riblt) to make that process executable. The repository has a generic library, a cell-by-cell walkthrough, a scaling experiment, property and fuzz tests, and benchmarks. I will follow the walkthrough's concrete sets throughout this note:

```text
upstream:   [100 101 102 103]
downstream: [100 102 104]
```

The answer is small: add `101` and `103` downstream, then remove `104`.

## Start with the algebra a symbol needs

The RIBLT does not need to know what a symbol means. It needs an identity, a reversible way to combine symbols, and two hashes with separate jobs. Go generics let the library state that contract without requiring methods on `T`:

```go
type Codec[T any] interface {
    Zero() T
    IsZero(T) bool
    XOR(a, b T) T
    MappingHash(T) uint64
    Checksum(T) uint64
}
```

XOR supplies a Boolean group. Its identity and self-inverse properties are what make coding reversible, while `IsZero` lets the decoder recognize that identity without requiring `T` to be comparable:

```text
x XOR 0 = x
x XOR x = 0
(a XOR b) XOR b = a
```

The demonstration's `Symbol` contains one `uint64`, so its XOR is ordinary bitwise XOR. A richer record still works when its codec has a fixed-width, reversible representation. The operation must be pure. For a slice, map, or pointer-backed `T`, the codec must return independent storage rather than mutating or retaining either argument.

This is the central generic design choice. `Encoder[T]`, `Decoder[T]`, `Sketch[T]`, `HashedSymbol[T]`, and `CodedSymbol[T]` carry the application's symbol type, while `Codec[T]` injects the operations the algorithm actually uses. Built-in and third-party types need no RIBLT-specific methods.

## Give the two hashes different responsibilities

`Hash` computes both hashes once and packages them with the original value:

```go
type HashedSymbol[T any] struct {
    Symbol      T
    MappingHash uint64
    Checksum    uint64
}
```

The mapping hash seeds a deterministic sequence of cell indexes. Every symbol begins in cell zero, then follows an increasingly sparse sequence generated with the gap distribution from the RIBLT paper. The implementation keeps each symbol's next index in a min-heap. To emit cell `i`, the encoder XORs precisely the symbols whose next index is `i`, advances those mappings, and moves on to `i+1`.

The checksum has a separate role. A coded cell has three fields:

```go
type CodedSymbol[T any] struct {
    Symbol   T
    Checksum uint64
    Count    int64
}
```

The symbol and checksum fields are accumulated with XOR. The signed count is accumulated with addition. A count of `+1` or `-1` only suggests that the XOR field contains one remaining symbol. The decoder accepts it as a singleton only when `Checksum(cell.Symbol)` equals the accumulated checksum. Domain separation between placement and validation matters because these are independent decisions.

## Stream cells without guessing a table size

The upstream registers its complete set, then starts the stream:

```go
encoder, _ := riblt.NewEncoder[Symbol](codec)
for _, value := range upstream {
    _ = encoder.Add(value)
}

cell, _ := encoder.Next()
```

Calling `Next` produces the next cell, so the sender can continue for as long as decoding requires. Adding another source symbol after streaming starts is rejected because it would change cells the receiver has already consumed.

The downstream similarly registers its local set before the first coded cell:

```go
decoder, _ := riblt.NewDecoder[Symbol](codec)
for _, value := range downstream {
    _ = decoder.AddLocal(value)
}
```

For each incoming cell, `AddCoded` subtracts the initial downstream symbols scheduled for that index. Because subtraction and addition are the same operation for the XOR fields, the sign appears in `Count`. Shared symbols cancel, an upstream-only symbol contributes `+1`, and a downstream-only symbol contributes `-1`.

Cells are positional and must arrive in order. An actual protocol therefore needs ordered delivery or sequence and retransmission machinery, plus a completion acknowledgement so the upstream knows when to stop.

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
for !decoder.Complete() {
    cell, _ := encoder.Next()
    _ = decoder.AddCoded(cell)
    _ = decoder.TryDecode()
}

add := decoder.Remote()
remove := decoder.Local()
```

`Remote` is what exists only at the upstream, and `Local` is what exists only at the downstream. Those names describe the decoder's perspective, which is worth keeping explicit when the result becomes an application update.

The package also includes `Sketch[T]` for a fixed-length prefix. Two sketches of the same length can be built independently, subtracted cell by cell, and decoded. That is useful when a prefix length is already part of the surrounding protocol. The streaming encoder and decoder preserve the rateless advantage: no table length has to be chosen before seeing whether peeling succeeds.

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

The Go benchmark uses 10,000 shared entries and varies the symmetric difference. On an Intel i5-1038NG7, one run reported between `1.000` and `1.906 coded/difference` for differences from 1 through 1,024. Its end-to-end timings ranged from about 7.7 ms to 61.6 ms per reconciliation. The same output reports roughly 7.2 to 7.5 MB and 20,000 to 22,000 allocations per operation because the benchmark deliberately rebuilds and hashes both 10,000-entry inputs on every iteration. Those figures establish a baseline and expose optimization opportunities; they do not isolate network cost or only the peeling loop. The mapping microbenchmark reported about 10 ns with zero allocations for one mapping step on that machine.

## What the tests establish

`go test ./...` exercises more than the happy path. The suite checks known reconciliation results, equal sets, fixed-length sketch subtraction, deterministic mapping vectors, reset behavior, duplicate and lifecycle errors, and 100 seeded random set constructions. A fuzz target generates additional shared and one-sided values and checks that both decoded difference sizes are recovered.

Together, those tests demonstrate the implementation's behavior for the exercised codecs and inputs. The probabilistic algorithm still depends on good mapping hashes, and checksum collisions remain possible in principle.

## Keep the algorithm inside a complete protocol

The demonstration hashes are deterministic and useful for repeatable examples. They are not an adversarial security boundary. With untrusted input, an unkeyed checksum allows an attacker to search for collisions that can make a false singleton look valid. A deployed design should use a keyed, domain-separated checksum, authenticate messages, and enforce bounds on cells, memory, and work.

RIBLT also reconciles sets, not arbitrary collections or application state. The implementation rejects duplicate symbol identities. If multiplicity matters, I would encode a unique occurrence identifier or choose a multiset protocol. A synchronization system still has to define serialization, versions, ordering, retransmission, acknowledgement, and how additions and removals are applied atomically.

Those boundaries do not diminish the useful result. The generic core is small because the algorithm needs only XOR, two hashes, counts, deterministic sparse placement, and peeling. Running the walkthrough turns those pieces from a paper description into a sequence I can inspect: combine symbols, subtract local state, validate a singleton, propagate it, and stop when every received cell is resolved.

The [go-riblt repository](https://github.com/TheFellow/go-riblt) contains the implementation and every command discussed here. Start with `go run ./cmd/walkthrough`, then read `codec.go`, `window.go`, and `decoder.go` in that order. That path follows the same dependency chain as the algorithm itself.
