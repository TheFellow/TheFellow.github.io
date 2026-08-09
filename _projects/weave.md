---
title: "Weave"
date: 2026-08-06 22:55:00 -0700
last_modified_at: 2026-08-09 10:00:00 -0700
excerpt: "A compact local navigation index that gets people and coding agents from a question to the right source without copying the repository into a graph."
language: "Go"
license: "MIT"
repository_url: "https://github.com/TheFellow/weave"
last_updated: 2026-08-08
series_url: "/series/weave/"
order: 5
featured: true
icon: "route"
accent: "#4dabf7"
topics: ["Code intelligence", "Developer tools", "Git"]
---

<div class="project-meta"><span>Go</span><span>Code intelligence</span><span>Git</span><span>MIT</span><span>Updated {{ page.last_updated | date: "%B %-d, %Y" }}</span></div>

[View the repository](https://github.com/TheFellow/weave){: .btn .btn--primary }
[Read the Weave series](/series/weave/){: .btn }
[Start with fresh queries](/articles/keeping-a-semantic-index-fresh-without-a-daemon/){: .btn }
[Read the agent dogfood](/articles/measuring-agent-research-beyond-query-latency/){: .btn }
[Inspect the indexing soak](/articles/turning-cross-repository-soaks-into-indexing-contracts/){: .btn }

Weave is a local-first, Git-aware navigation index for people and coding agents. It stores just enough structure to find the right package, declaration, or document, then sends detailed investigation back to current source. The index is disposable, stays outside Git, needs no hosted service, and refreshes before serving a query.

```sh
weave explore how menu publication reaches persistence
weave context example.com/project/menu.Service.Publish
weave path PackageA PackageB --kind imports --max-depth 8
weave impact --git-diff origin/main --json
weave graph Handle --kind implements --output handle.dot
weave links add guide-documents-handler --from 'docs/guide.md#flow' --to Handle --kind documents
```

Format 5 implements one `navigation-v1` profile end to end. Providers emit documents, declaration anchors, and high-value relationships such as dependencies, imports, implementations, tests, generation, documentation, links, and embeds. Occurrences, calls, references, locals, fields, containment, and body terms are not produced or stored.

`weave explore` combines a few semantic anchors with bounded, ignore-aware ripgrep results. `weave context` opens source only after a useful target is selected. Graph, path, impact, architecture, links, and semantic diff operate on the same retained navigation facts.

The built-in Go provider indexes build-selected declarations and package dependencies without type checking or test variants. Optional language adapters project their compiler output into the same profile. Structured Markdown and source-only schema providers add documents and declarative relationships without running renderers, builds, package managers, databases, or network loaders.

Freshness is checked on every read. `weave watch`, the transient local broker, catalog aggregation, and other caches can reduce latency, but none can bypass that check. The project remains early alpha, with a deliberately small goal: navigate quickly, return bounded answers, and reopen authoritative source at the point of use.
