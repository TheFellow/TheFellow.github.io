<!-- Generated from https://thefellow.github.io/projects/weave/ by scripts/generate_llm_content.py; do not edit. -->

# Weave

Source: [https://thefellow.github.io/projects/weave/](https://thefellow.github.io/projects/weave/)

## Pyramid summary

- **~2 words:** Practical navigation
- **~8 words:** A compact Git-aware index guiding agents to current source.
- **Expanded:** A compact local navigation index that gets people and coding agents from a question to the right source without copying the repository into a graph.

## Full content

[View the repository](https://github.com/TheFellow/weave)
[Read the Weave series](/series/weave.md)
[Start with fresh queries](/articles/keeping-a-semantic-index-fresh-without-a-daemon.md)
[Read the agent dogfood](/articles/measuring-agent-research-beyond-query-latency.md)
[Inspect the indexing soak](/articles/turning-cross-repository-soaks-into-indexing-contracts.md)

Weave is a local-first, Git-aware navigation index for the knowledge encoded in a workspace. It combines language-native declaration anchors and package topology with structured documents, sections, and high-value relationships, then exposes bounded CLI queries for people and coding agents. The index is disposable derived state. It stays beside Git instead of entering commits, requires no hosted service, and refreshes its automatic provider inventories before a query can observe stale answers.

The problem is familiar when working in a large repository. A coding agent can inspect source well once it reaches the right package, type, function, document, or file. Reaching that point repeatedly is the expensive part. Weave keeps a compact set of semantic anchors and high-value navigation relationships, then hands statement-level investigation back to current source instead of persisting a second, much larger copy of what compilers and text search can recover.

```sh
weave symbols Handle --limit 20
weave definition Handle
weave explore how menu publication reaches persistence
weave context example.com/project/menu.Service.Publish
weave path PackageA PackageB --kind imports --max-depth 8
weave impact --git-diff origin/main --json
weave graph Handle --kind implements --output handle.dot
weave graph README.md --interactive
weave links add guide-documents-handler --from 'docs/guide.md#flow' --to Handle --kind documents
weave explore presentation surfaces
weave graph docs/design.md --kind links-to --kind embeds
```

`weave explore` is deliberately small. It returns a few semantic anchors plus diversified, ignore-aware ripgrep hits with paths, coordinates, previews, and exact `weave context` follow-ups. `context` then opens current Git-visible source for the selected declaration. The first stage has both an item limit and a 12 KiB encoded ceiling, so discovery cannot quietly turn into a graph dump.

Storage format 5 is a navigation profile, not a compiler-event archive. It retains documents; package, namespace, type, callable, test, and content anchors; and relationships such as imports, dependencies, implementations, tests, generation, documentation, exposure, links, and embeds. It omits occurrences, statement-level calls and references, containment duplication, fields, constants, locals, and content search terms. The same `navigation-v1` boundary now applies when built-in providers construct facts, when external adapters stream them, and again before storage.

The measured format-4 transition established the practical boundary. On a recorded 3,019,968-byte Go repository, it reduced the database from 1,034,616,832 bytes to 16,777,216 bytes, a 98.38% reduction and 5.56 times the non-Git source size. The representative `explore --json` response fell from 171,537 bytes to 3,157 bytes, and its selected `context --json` response was 3,195 bytes. Format 5 goes further by avoiding discarded facts during production; those earlier numbers remain historical evidence until the newer format is measured on the same fixture.

The native Go provider and optional .NET, Python, Rust, C/C++, TypeScript/JavaScript, JVM, and Universal Ctags adapters use their language-native tools to establish identities and navigation facts. The open process protocol keeps those runtimes outside the Go core. Every index request now requires `profile: navigation-v1`; explicit permissions, capability claims, input routing, validation, and atomic publication prevent an adapter from silently broadening its authority. Adding a precise compiler does not imply producing or retaining all of its event exhaust.

The workspace provider gives the same treatment to repositories that do not compile. It inventories Git-visible paths only to resolve links, while persisting structured Markdown documents, headings, links, embeds, and generated-from relationships without executing the site. Generic files, directories, assets, routes, code blocks, topics, and body terms are not separate stored entities. Documents and sections are found through `explore` or `symbols`, opened through `context`, and connected through graph kinds such as `documents`, `links-to`, and `embeds`. A source-only provider adds bounded facts from Protobuf, OpenAPI, GraphQL, PostgreSQL migrations, Terraform, and declarative project manifests without running builds, generators, package managers, databases, or network loaders.

Freshness remains query-authoritative. A query compares the current Git and provider observation with the published manifest and refreshes changed semantic units before reading. `weave watch` can warm that same path, and a transient local broker can amortize process, schema, and dictionary startup, but neither becomes a second authority. The broker uses shared read-only handles and reaps itself after inactivity; `WEAVE_NO_BROKER=1` keeps the one-shot path available.

Explicitly registered worktrees can participate in catalog queries, but each member proves freshness before contributing facts. Machine-wide aggregation remains a disposable acceleration layer rather than an authority. Bounded graph, path, dependency, impact, architecture, contextual-link, and semantic-diff operations work over the retained navigation relationships; statement-level investigation continues in source.

The project remains early alpha. Its current direction is intentionally less ambitious than preserving every compiler observation: keep enough exact structure to navigate, keep answers bounded, reopen current source at the point of use, and make the local index cheap enough to discard and rebuild.

### Why it is worth exploring

- It makes freshness part of every read instead of depending on a daemon or a remembered indexing step.
- It measures index and response amplification instead of treating more graph data as automatically better.
- It keeps compiler truth, explicit declarations, and weaker evidence visibly distinct in the retained navigation facts.
- It turns local adapter installation into pinned, claim-routed policy without pretending to operate a remote package registry.
- It treats repository topology and documentation as first-class knowledge without executing their renderers.
- It combines semantic anchors with bounded ripgrep discovery instead of storing statement-level source evidence twice.
- It turns the same bounded neighborhood into deterministic DOT for people and JSON for agents.
- It treats human output and versioned JSON as two presentations of the same bounded application behavior.
- It turns impact analysis and architecture checks into queries over the same facts used for code navigation.

Start with the [freshness walkthrough](/articles/keeping-a-semantic-index-fresh-without-a-daemon.md), then read `internal/repository`, `internal/freshness`, `internal/graph`, and `internal/query` in that order. Continue through `protocol/adapter/v0`, `internal/adapter/registry.go`, and `adapters` to see the language runtimes meet the same graph boundary, then follow `internal/workspaceindex`, `internal/application/links.go`, `internal/dot`, and `internal/explorer` into content, authored context, and human-readable graph views. The [Weave series](/series/weave.md) will continue outward from this lifecycle into impact analysis, federation, and executable architecture policy.
