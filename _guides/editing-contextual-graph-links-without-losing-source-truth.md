---
title: "Editing Contextual Graph Links Without Losing Source Truth"
date: 2026-08-07 14:28:12 -0700
last_modified_at: 2026-08-07 14:28:12 -0700
excerpt: "How Weave turns its local graph explorer into a source-evidence inspector and revision-guarded editor while keeping checked-in declarations, application use cases, and query-driven refresh authoritative."
permalink: /articles/editing-contextual-graph-links-without-losing-source-truth/
series: weave
series_order: 9
order: 13
featured: true
status: "Weave, part 9"
icon: "link"
accent: "#b197fc"
topics: ["Graph authoring", "Optimistic concurrency", "Local UI"]
---

{% include series-notice.html %}

The first [local graph explorer](/articles/making-a-semantic-graph-inspectable/) made Weave's normalized evidence navigable without creating a second graph model. It could refocus a bounded neighborhood, filter relationships, animate stable nodes, and export what it showed. It remained intentionally read-only.

That boundary becomes more interesting when the graph contains relationships a compiler cannot discover. A person should be able to inspect why an edge exists, see the current source behind it, and author a reviewed contextual relationship from the same interface. The dangerous shortcut is to let the browser mutate graph storage. That would turn a disposable projection into source truth and make concurrent edits almost impossible to reason about.

[Weave](https://github.com/TheFellow/weave) instead gives the explorer two narrow capabilities. Selection detail reuses the existing source-rich context use case. Link editing reuses the existing application commands over the checked-in `.weave/bridges.json` declaration. A revision digest protects long-lived browser state, and query-driven freshness reconstructs the graph after a successful edit.

<figure class="article-figure">
  <img src="{{ '/assets/images/articles/weave/revision-guarded-links.svg' | relative_url }}" alt="A stable node or collapsed visual edge selection enters the existing bounded context use case and returns current source evidence. Separately, the browser loads canonical contextual links and an order-independent revision digest. Add, update, or remove requests carry that revision through strict same-origin JSON endpoints to the application link use case. Under the Git-private edit lock, Weave reloads the latest checked-in declaration, compares revisions, validates the mutation, and atomically replaces bridges.json. A mismatch returns conflict and requires reload; a successful write refreshes the normal bridge provider and graph.">
  <figcaption>The browser inspects current graph evidence and edits the checked-in declaration. It never writes semantic graph rows directly.</figcaption>
</figure>

## Map visual selections back to exact facts

Graphviz may collapse several equivalent provider or evidence facts into one visual edge. That is useful for a readable diagram and dangerous for an inspector if the DOM element is treated as the fact itself.

Weave already emits stable SVG IDs from semantic identities. The explorer now returns a node map plus an edge map. Each edge-map entry uses the same collapse key as DOT rendering and retains every normalized source fact under that visual ID in canonical order. The current inspector chooses the canonical first fact for exact detail while preserving the full group for richer presentation later. It never reverse-engineers meaning from an SVG path.

Node and edge selection share one inspector panel. Refocusing still uses the selected semantic node, while detail loading carries the exact selected edge ID when the user clicked a relationship. UI identity remains a pointer into the application result, never a replacement for graph identity.

Selection and navigation remain separate interactions. Generated nodes and edges receive button roles, visible focus, accessible names, and Enter or Space selection. An explicit **Refocus graph** action handles keyboard navigation; double-click is only a pointer shortcut. The evidence panel uses ordinary semantic HTML, so understanding an edge does not depend on interpreting a visual tooltip.

## Reuse the source-rich context boundary

A node detail request becomes the same bounded `context` invocation used by the CLI. The explorer supplies a target, result limit, context-line count, and source-byte budget, then requires a compatible `weave.context/v1` result.

An edge begins at its exact `From` entity and adds one stricter check. The current outgoing context must still contain the selected edge ID. If a refresh removed it or the bounded result no longer includes it, the server fails closed and asks the browser to refresh the graph. A stale visual line cannot silently display evidence for a different relationship.

[Source-rich context](/articles/composing-source-rich-context-without-a-second-index/) now hydrates relationship source too. When an edge carries a document and range, the context builder loads that document, resolves repository provenance first from the edge and then from the document, and passes the range through the same current-source loader used for definitions and references. Missing documents and unavailable provenance remain explicit statuses. Relationship excerpts share the global byte ceiling, UTF-8 checks, Git-visible path rules, and file-race detection instead of opening a more permissive browser-only file endpoint.

## Keep the declaration canonical

The inspector's link list comes from the `links list` application use case. The explorer does not read `.weave/bridges.json` itself, and it does not infer authored declarations from graph edges. That distinction matters because provider output is a derived projection, while the checked-in declaration is reviewable intent.

Creating, updating, and removing a link follows the same application primitives used by the CLI. Endpoints may be unique symbol queries, exact `entity:` values, or deliberate open `id:` values. Resolution still refreshes the relevant local or catalog graph, requires uniqueness when resolving a query, preserves repository diagnostics, and validates the relationship kind and note bounds.

After an edit, the bridge provider sees the changed declaration through ordinary Git freshness and reconstructs normal graph facts. The browser receives the result of that refresh. There is no explorer-specific edge table, pending overlay, or hidden synchronization step.

## Give long-lived clients a revision

A CLI command is short-lived, but a browser may keep a form open while a person, formatter, or another Weave process changes the declaration. A file lock prevents simultaneous writes from interleaving; it does not prevent a stale form from overwriting a newer value after the first writer has finished.

Every canonical link list therefore includes an optimistic revision. Weave copies and sorts links by ID, validates the full configuration, encodes it canonically, and hashes it under the `weave.bridges-revision/v1` domain. Reordering equivalent entries does not create a conflict. Changing an endpoint, relationship kind, note, link ID, or membership does.

This digest is intentionally not a graph generation or database identity. It answers one question only: is the authored declaration I loaded still the declaration being edited?

The browser pins the revision when an editor or removal confirmation opens and must send it with the mutation. Inside the existing Git-private edit lock, Weave reloads the latest source file and recomputes its revision before applying the change. A mismatch returns the typed authored-link conflict, which the HTTP boundary maps to `409 Conflict` with a reload instruction. The test happens under the same lock as read, validation, and write, closing the time-of-check/time-of-use gap.

After a conflict, reloading the canonical list does not silently rebase the open form. The user must cancel it and explicitly reopen the editor against the new revision. That small inconvenience preserves the meaning of the human review: an edit prepared against one declaration is never transformed into an edit against another without being seen again.

One-shot CLI callers may omit a revision and retain the existing serialized edit behavior. The guard is an application option for clients that hold state across time, not an incompatible requirement imposed on every command.

## Write one validated declaration atomically

The mutation boundary distinguishes omission from an intentional empty note through pointer fields. Add requires `from`, `to`, and relationship kind. Update requires at least one changed field. Remove accepts only exact ID and revision. IDs, endpoint text, notes, kinds, UTF-8, control characters, and byte ceilings are validated before the application command runs, then the complete bridge configuration is validated again before publication.

The source write remains canonical and atomic. Links sort by ID. Symlinked declaration files are rejected. Weave encodes an indented temporary file beside the destination, syncs and closes it, checks the final bound, and renames it over `.weave/bridges.json`. The Git-private bbolt lock database serializes editors without putting lock state in source control.

An exact remove gets an explicit confirmation dialog because the operation changes reviewed source. A stale dialog still cannot delete the wrong version: its revision check occurs after the latest declaration is loaded under lock.

## Keep the loopback editor narrow

The explorer remains a tokenized loopback server with no remote assets. It keeps the exact loopback host allowlist, random path token, origin and fetch-site checks, restrictive content security policy, no-store responses, and exact route allowlist. Detail and mutation endpoints require strict JSON, reject unknown fields and trailing values, cap request bodies, and enforce same-origin browser requests. Link operations use GET, POST, PUT, and DELETE only for list, add, update, and remove. Source and declaration text enter the page through `textContent`, never as interpreted HTML.

The browser can fill either endpoint from the current selection, but that convenience does not relax endpoint resolution. It can show source excerpts, but it cannot request arbitrary filesystem paths. It can submit an edit, but it cannot choose a database record or bypass application validation. Large graphs also keep their practical rendering boundary: expensive path and shape tweening gives way to a measured no-tween fallback. The right-hand inspector is a client of existing boundaries, not a privileged back door around them.

That is the useful shape of local graph editing: precise enough to turn understanding into reviewed intent, constrained enough that source, freshness, and semantic evidence remain authoritative after the window closes.
