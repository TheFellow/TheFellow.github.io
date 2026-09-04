---
title: "go-merkletrie"
date: 2026-09-03 12:00:00 -0700
last_modified_at: 2026-09-03 12:00:00 -0700
excerpt: "An immutable, generic Merkle trie for Go with canonical codecs, content-addressed persistence, and lazy snapshots."
language: "Go"
license: "MIT"
repository_url: "https://github.com/TheFellow/go-merkletrie"
last_updated: 2026-09-03
order: 27
icon: "branch"
accent: "#74c0fc"
topics: ["Content addressing", "Persistent data structures", "Generics"]
---

<div class="project-meta"><span>Go</span><span>Content addressing</span><span>Persistent data structures</span><span>MIT</span><span>Updated {{ page.last_updated | date: "%B %-d, %Y" }}</span></div>

[View the repository](https://github.com/TheFellow/go-merkletrie){: .btn .btn--primary }
[Read the implementation walkthrough](/notes/building-a-persistent-merkle-trie-in-go/){: .btn }

go-merkletrie is a generic, immutable radix trie for Go 1.27.1 and later whose nodes are addressed by their SHA-256 digests. A `Put` or `Delete` returns a new tree while earlier versions remain available to concurrent readers. The resulting root is a compact commitment to the tree's encoded structure and contents.

Applications choose their key and value types through canonical encodings. Built-in codecs cover strings, byte slices, and fixed-width integers, while `NewEncoding` adapts an application type without teaching the trie its meaning. Compatibility IDs and optional namespaces make those representation choices part of the persisted format, so opening data with a different schema fails explicitly.

Persistence follows the same immutable model. `Objects` emits each reachable object in children-before-parent order for content-addressed storage. `Load` validates a complete generation eagerly, while `Open` creates a lazy snapshot that resolves only the paths an operation touches. Snapshot updates accumulate an in-memory overlay, and `FinalChange` returns the new reachable objects that must become durable before the new root is published.

The implementation separates two kinds of identity. Matching physical roots prove that the canonical encoded graphs are identical. A shape-independent semantic summary gives a fast equality hint when deletion history leaves two equivalent maps with different shapes. The distinction stays explicit because the summary is useful for comparison, but is not a cryptographic proof.

### Why it is worth exploring

- It connects a persistent data structure directly to a safe object-publication protocol.
- Canonical generic codecs make schema identity and deterministic encoding part of the API.
- Lazy snapshots preserve immutability while avoiding a full-tree read for a lookup or small update.
- Strict decoding validates hashes, references, depth, routing, summaries, and canonical round trips at the storage boundary.

Start with `examples/basic`, then follow the [walkthrough note](/notes/building-a-persistent-merkle-trie-in-go/) into radix routing and structural sharing. `examples/custom-codec` shows an application type, and `examples/lazy-storage` demonstrates the objects-first, root-last persistence sequence.
