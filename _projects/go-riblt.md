---
title: "go-riblt"
date: 2026-08-03 12:00:00 -0700
last_modified_at: 2026-08-03 12:00:00 -0700
excerpt: "A generic Go implementation of rateless set reconciliation with keyed codecs, streaming cells, and explicit resource limits."
language: "Go"
license: "MIT"
repository_url: "https://github.com/TheFellow/go-riblt"
last_updated: 2026-08-02
order: 25
icon: "matrix"
accent: "#8ce99a"
topics: ["Set reconciliation", "Distributed systems", "Generics"]
---

<div class="project-meta"><span>Go</span><span>Set reconciliation</span><span>Distributed systems</span><span>MIT</span><span>Updated {{ page.last_updated | date: "%B %-d, %Y" }}</span></div>

[View the repository](https://github.com/TheFellow/go-riblt){: .btn .btn--primary }
[Read the walkthrough note](/notes/riblt-in-go/){: .btn }

go-riblt is a generic Go implementation of a Rateless Invertible Bloom Lookup Table. When two peers hold large sets that mostly agree, it discovers the few entries that differ with communication proportional to the size of the disagreement, not the size of the data. The upstream streams coded cells until the downstream has peeled both sides of the symmetric difference; neither side estimates the difference before transmission begins.

The generic design is the interesting part. The algorithm never learns what a symbol means; a `Codec[T]` supplies the exact algebra it needs: a reversible XOR, an identity, ownership rules for mutable values, and two keyed hashes with separate jobs for placement and singleton validation. Keyed codecs for `uint64` and fixed-width byte strings come built in, and the repository's examples show the same core reconciling numeric IDs, complete fixed-layout records, bounded documents, and content-addressed chunks.

The library also treats its trust boundaries as contracts rather than conventions. Every public insertion point validates, clones, and hashes values itself, decoder limits bound cells, local symbols, and peeled results, and a `CompatibilityID` plus protocol version reject mismatched codec configurations instead of producing meaningless cells. Property tests, fuzz targets, and benchmarks exercise those contracts alongside the happy path.

### Why it is worth exploring

- It shows how Go generics can separate a probabilistic algorithm from the representation decision each application has to make.
- The runnable walkthrough prints every transmitted cell and each peeling step, turning a paper description into a sequence you can inspect.
- The scaling experiment makes the central claim observable: a tenfold increase in set size leaves the number of transmitted cells nearly unchanged.

Start with `go run ./cmd/walkthrough`, then read `codec.go`, `window.go`, and `decoder.go` in that order. The [companion note](/notes/riblt-in-go/) follows that same path through the concrete example sets, and `cmd/structs`, `cmd/documents`, and `cmd/chunks` compare how the generic core fits different application data.
