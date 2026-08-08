---
title: "Making a Semantic Graph Inspectable"
date: 2026-08-07 10:28:00 -0700
last_modified_at: 2026-08-08 13:10:00 -0700
excerpt: "How Weave turns one bounded semantic neighborhood into deterministic DOT, reviewed contextual links, and an animated local explorer without creating a second graph model."
permalink: /articles/making-a-semantic-graph-inspectable/
series: weave
series_order: 3
order: 7
featured: true
status: "Weave, part 3"
icon: "sitemap"
accent: "#51cf66"
topics: ["Semantic graphs", "Graphviz", "Developer tools"]
---

{% include series-notice.html %}

A semantic graph can be correct and still be difficult to trust. JSON preserves identities and provenance, but a person reviewing a dependency direction or a documentation relationship has to reconstruct the shape mentally. Exporting the entire database does not solve that problem. Even the compact navigation index needs a focused question and explicit bounds.

[Weave](https://github.com/TheFellow/weave) takes the opposite route. [`weave graph`](https://github.com/TheFellow/weave/blob/main/.ai/decisions/0011-focused-dot-graph-export.md) begins with one resolvable entity, walks a bounded semantic neighborhood, and presents that same result as deterministic Graphviz DOT, versioned JSON, or an animated local view. The graph query remains the product boundary. Renderers do not gain a separate store, resolver, or definition of freshness.

```sh
weave graph HandleRequest --kind implements --kind documents > handle.dot
weave graph README.md --direction outgoing --max-depth 3 --output docs.dot
weave graph HandleRequest --interactive
```

<figure class="article-figure">
  <img src="{{ '/assets/images/articles/weave/inspectable-graph.svg' | relative_url }}" alt="Compiler, workspace, and authored relationship providers feed one normalized graph. A bounded graph query resolves one focus and traverses explicit depth, node, and edge budgets. The same result becomes deterministic DOT, versioned JSON, or an animated loopback explorer. Every surface retains exact identities, evidence, providers, and truncation.">
  <figcaption>One bounded application query feeds every graph presentation. A renderer can improve legibility without changing semantic truth.</figcaption>
</figure>

## Start from a question, not the database

The first design choice is refusing to render everything. `weave graph TARGET` resolves the target through the same deterministic resolver used by other queries, then traverses incoming edges, outgoing edges, or both. Depth, returned nodes, and examined edges have conservative defaults and hard maxima.

Bidirectional traversal keeps independent incoming and outgoing queues and interleaves them. That detail matters when the global node or edge budget is small. Walking every caller first could consume the entire budget before showing a single callee. The result records whether a bound truncated the view rather than letting a small picture imply a complete universe.

The default edge set is exactly the relationship vocabulary retained by format 4: dependencies, imports, extension and implementation, tests, generation, documentation, exposure, links, and embeds. Statement-level calls and references, containment duplication, reads, writes, membership, and resolution are not hidden filters; they are absent from the managed navigation index and must be investigated in current source.

The operation works over a local worktree or the bounded repository catalog. Catalog members still refresh before their databases are opened. Graph breadth does not weaken the [freshness contract](/articles/keeping-a-semantic-index-fresh-without-a-daemon/); it makes the current facts easier to inspect.

## Make the first terminal answer readable

Inspectability starts before DOT. The ordinary relationship commands have to answer a question without making a person decode internal graph IDs or join document records by hand:

```text
$ weave path fixture.Handler fixture.RequestHandler --kind implements
fixture.Handler  implements  fixture.RequestHandler  main.go:8:3
```

Weave hydrates graph responses with the materialized anchors and documents referenced by retained nodes and edges. The text renderer can therefore show stable names and repository-relative source locations, while `--json` retains exact identities and records. `dependencies`, `path`, and `impact` use the same navigation-relationship presentation. A path with no result says so directly instead of printing an ambiguous empty line, and Ctrl-C is a successful end to an interactive graph session rather than a command failure.

Human input gets the same treatment. Compiler-qualified stable names can encode ownership as segments such as `package`, `type`, and `method`, but `Server.Serve` is the spelling a person naturally reaches for. The resolver keeps exact IDs, exact stable names, and provider search order authoritative, then falls back to the concise qualified suffix when it selects exactly one symbol. An ambiguous query reports stable names, kinds, and graph IDs for several candidates, plus the remaining count, so refinement does not begin with two opaque hashes.

That hydration exposed provider details that matter to the answer. The native Go index now materializes external packages and referenced external objects as readable endpoints, includes implicit declarations such as type-switch variables, and preserves stable ownership through aliases and reconstructed type objects. Explicit open-world endpoints remain valid when another provider has not materialized them.

Dependency output also collapses repeated `imports` and `depends-on` evidence between the same endpoints, preferring the stronger direct dependency relationship before applying the user's result limit. File impact starts from retained declarations actually owned by the selected file. These are presentation and traversal corrections over the same navigation evidence, but they are what turn stored facts into a useful answer.

The help surface follows the same rule. Required operands are now visible in command usage, including `QUERY`, `FROM TO`, repository identities, adapter names and executables, and the conformance fixture directory. The CLI explains the shape of a valid question before asking the graph to answer it.

## Emit DOT without depending on Graphviz

Weave writes DOT but does not invoke `dot`. The CLI therefore works on a machine with no Graphviz installation, while a user who already has a renderer can choose an output:

```sh
weave graph AuthService --output auth.dot
dot -Tsvg auth.dot -o auth.svg
```

The DOT is a presentation of exact graph identities, not a replacement for them. Nodes receive compact readable labels and shapes based on kind. Tooltips retain stable names and semantic IDs. Materialized nodes are clustered by provider; unresolved endpoints remain visible rather than disappearing. Edge labels name the relationship, while metadata retains its provider and evidence.

Color explains traversal role. The focus is gold, incoming nodes are green, outgoing nodes are purple, and nodes reached in both directions are rose. Evidence selects line treatment. Equivalent parallel edges can collapse visually with a count, while JSON retains every selected navigation fact.

Generated node names, clusters, attributes, and edges are sorted. Every dynamic DOT string is quoted and escaped, including quotes, backslashes, newlines, and control characters. Determinism makes a graph useful in review and CI artifacts; defensive encoding keeps a hostile symbol name from becoming DOT syntax.

## Author the context compilers cannot see

Visualization exposed a second problem: some of the most useful paths do not belong to any compiler. An article documents a handler. A schema generates a client. A route exposes a service in another repository. Those facts should be reviewed source truth, but requiring a person to export opaque graph IDs and hand-edit JSON is a poor authoring interface.

[`weave links`](https://github.com/TheFellow/weave/blob/main/docs/declared-bridges.md) resolves human-facing endpoints once, then stores their exact identities:

```sh
weave links add guide-documents-handler \
  --from 'docs/guide.md#request-flow' \
  --to HandleRequest \
  --kind documents \
  --note 'The guide explains this request entry point.'

weave links list --json
weave links update guide-documents-handler --to 'id:git-commit:0123456789abcdef'
weave links remove guide-documents-handler
```

Add and update require each query to resolve uniquely. The stored `.weave/bridges.json` declaration uses `entity:<exact-id>` endpoints, so a later display-name collision cannot silently retarget it. `id:<exact-id>` deliberately creates an open endpoint for an immutable commit or resource that is not materialized yet; it is not a fuzzy-resolution escape hatch.

Endpoints are graph entities rather than only compiler symbols. A relationship can connect packages, files, Markdown sections, routes, assets, URLs, or code declarations. Catalog scope can resolve endpoints across registered worktrees. Authored relationships are limited to edge kinds retained by the navigation index, and their evidence remains `declared`, except generation relationships, which remain `generated`. A CLI flag cannot promote a human assertion to compiler-exact evidence.

Writes are strict, canonical, bounded, and atomic. A Git-private lock serializes concurrent read-modify-write operations, while the reviewed declaration remains in the worktree. After publication, Weave refreshes the current repository so the new relationship immediately participates in graph, path, impact, export, architecture, and federation queries.

## Keep one relationship contract

Authored links do not enter a side annotation database. The built-in Go, SCIP, workspace, and relationship providers construct the same normalized `graph.Edge` shape through one relationship builder. Provider ownership and evidence defaults are validated in one place.

That common shape is what makes mixed neighborhoods useful. A compiler-owned `implements` edge can meet an exposed route and a reviewed `documents` link to a Markdown section. Each edge keeps the source of its claim. The graph view can combine them without flattening `exact`, `generated`, `declared`, and `syntactic` into one confidence score.

An exact endpoint can become unmaterialized after a rename. Weave leaves that reviewed relationship explicit and inspectable instead of guessing a new target. The missing node in DOT is evidence of drift that a person can repair.

## Animate the same bounded result

Static DOT is enough for documentation and CI, but it is awkward when the question changes repeatedly. [`weave graph TARGET --interactive`](https://github.com/TheFellow/weave/tree/main/internal/explorer) starts a human-only explorer over the same application invocation. Clicking a node changes focus. Direction, depth, node and edge budgets, relationship kinds, providers, and evidence filters request another bounded snapshot. Back and forward controls retain the exploration path.

The browser does not acquire a new graph model. The Go engine calls the normal `graph` operation, filters the returned facts, and writes DOT through the same presentation package. Stable SVG IDs derive from semantic identities so D3 can preserve object constancy while Graphviz lays out the next snapshot. Nodes and edges enter, leave, and move instead of making every click look like an unrelated picture.

Animation remains a presentation optimization. Layout runs in a web worker. Large views disable expensive path and shape tweening, `prefers-reduced-motion` is honored, and a bounded render timeout turns a stuck layout into an explicit error. Pan, zoom, reset, keyboard refocus, truncation notices, and tooltips keep the view inspectable rather than decorative.

## Keep the local viewer local

Starting a browser surface creates a security boundary even when the data is local. The explorer binds an ephemeral IPv4 loopback port and places a cryptographically random token in the path. Repository and catalog scope are fixed when the server starts; a browser request cannot expand them.

The handler rejects unexpected hosts, origins, fetch sites, methods, media types, paths, control characters, unknown JSON fields, oversized bodies, and out-of-range budgets. It sends a restrictive content security policy, disables caching and framing, and applies read, write, header, and idle timeouts. `--no-open` prints the session URL without launching a browser, and Ctrl-C shuts the server down.

D3, d3-graphviz, and the WebAssembly Graphviz runtime are pinned, checksummed, licensed, and embedded into the Go binary. There is no CDN, telemetry, or runtime asset request. The only browser API talks back to the tokenized loopback session that produced the page.

This is deliberately narrower than a graph editor or IDE. The browser cannot mutate derived facts. Authored source context still goes through `weave links`; compiler and workspace facts still come from their providers; every interactive refocus still proves freshness before it reads.

## Follow one relationship through every surface

A practical walkthrough now has one sequence:

1. Use `weave explore` or `weave symbols` to identify a useful starting entity.
2. Add a reviewed relationship with `weave links add` when the graph lacks context no provider can prove.
3. Run `weave graph TARGET --json` to inspect exact nodes, edges, evidence, provenance, and truncation.
4. Emit DOT to create a stable review or documentation artifact.
5. Add `--interactive` when the next useful question is easier to express by clicking and filtering.

The important part is not that Weave gained three outputs. It gained one bounded semantic-neighborhood operation and kept every surface subordinate to it. Agents receive exact structured facts. Documentation receives deterministic DOT. People receive an animated map. None of them gets to redefine what the graph knows.
