---
title: "Building Mixology: The Slide Deck"
date: 2026-09-05
last_modified_at: 2026-09-05
permalink: /talks/building-mixology/
excerpt: "A visual walkthrough of the foundational domain, module, middleware, event, audit, tagging, filtering, persistence, and presentation choices behind go-modular-monolith."
layout: deck
author_profile: false
search: false
---

<section class="centered title-slide">
  <div class="eyebrow">Building Mixology</div>
  <h1>A modular monolith that has to prove it</h1>
  <p class="lede">One Go application. Seven bounded contexts. Three native interfaces. One architecture made executable.</p>
  <div class="chapter-path"><span>← / → chapter</span><span>↑ / ↓ detail</span><span><b>S</b> speaker view</span><span><b>Esc</b> map</span></div>
  <aside class="notes">This is the map behind the video series. Each horizontal chapter can stand alone. The vertical slides are the concrete route through that chapter.</aside>
</section>

<section>
  <section class="centered section-slide">
    <div class="eyebrow">Orientation</div>
    <h1>Why this application exists</h1>
    <p class="lede">Architecture is the set of changes the codebase makes easy, and the shortcuts it refuses.</p>
    <div class="section-no">00</div>
  </section>

  <section>
    <h2>The problem is not folders</h2>
    <div class="split">
      <div class="side"><h3>A package diagram</h3><p>Shows the path we intended when the repository was young.</p><p class="muted">It cannot stop the next convenient import.</p></div>
      <div class="bridge">≠</div>
      <div class="side"><h3>An executable boundary</h3><p>Makes ownership visible in APIs, types, transactions, generators, tests, and import rules.</p><p class="accent">The shortest wrong path fails.</p></div>
    </div>
    <div class="callout">The reference application is a cocktail bar because inventory, recipes, menus, and orders create real pressure between domains.</div>
  </section>

  <section>
    <h2>One deployable, seven owners</h2>
    <div class="domain-map">
      <svg class="domain-lines" viewBox="0 0 1000 450" aria-hidden="true"><defs><marker id="arrowhead" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><polygon points="0 0, 7 3.5, 0 7" fill="#63e6be"/></marker></defs><line x1="320" y1="90" x2="180" y2="220"/><line x1="320" y1="350" x2="180" y2="230"/><line x1="570" y1="90" x2="390" y2="90"/><line x1="790" y1="200" x2="630" y2="90"/><line x1="180" y1="220" x2="570" y2="90" class="event"/><line x1="180" y1="230" x2="790" y2="220" class="event"/><line x1="390" y1="350" x2="790" y2="230" class="event"/><line x1="790" y1="245" x2="390" y2="350" class="event"/></svg>
      <div class="domain ingredients">Ingredients<small>catalog + retirement</small></div><div class="domain drinks">Drinks<small>recipes</small></div><div class="domain inventory">Inventory<small>stock</small></div><div class="domain menus">Menus<small>curation + publication</small></div><div class="domain orders">Orders<small>lifecycle</small></div><div class="domain audit">Audit<small>append-only activity</small></div><div class="domain tagging">Tagging<small>associations</small></div>
    </div>
    <div class="legend"><span><i></i> caller → public query owner</span><span><i class="event"></i> event owner ⇢ reacting owner</span></div>
  </section>

  <section>
    <h2>The current trace</h2>
    <div class="flow">
      <div class="node"><strong>main/&lt;surface&gt;</strong>process composition</div><div class="arrow">→</div>
      <div class="node"><strong>surfaces/&lt;surface&gt;</strong>domain presentation</div><div class="arrow">→</div>
      <div class="node"><strong>module.go</strong>public facade</div><div class="arrow">→</div>
      <div class="node"><strong>queries / internal</strong>behavior + storage</div>
    </div>
    <div class="cards three">
      <div class="card"><h3>CLI</h3><p>One command, one fresh operation context.</p></div><div class="card"><h3>Bubble Tea TUI</h3><p>Persistent session, message-driven presentation.</p></div><div class="card"><h3>Fyne GUI</h3><p>Retained native widgets and managed lifecycle.</p></div>
    </div>
    <div class="callout">All three enter the same application behavior and local SQLite database. Views are adapters, not alternate applications.</div>
  </section>
</section>

<section>
  <section class="centered section-slide">
    <div class="eyebrow">Foundation 1.1</div><h1>Shape modules around business ownership</h1>
    <p class="lede">A modular monolith begins with decisions, language, and collaboration contracts, not a folder template.</p><div class="section-no">1.1</div>
  </section>

  <section>
    <h2>A boundary should resist the shortest path</h2>
    <div class="layers">
      <div class="layer"><strong>Public facade</strong><span><code>app/domains/drinks</code> composes and exposes supported behavior.</span></div>
      <div class="layer"><strong>Public contracts</strong><span><code>models</code>, <code>queries</code>, and <code>events</code> are deliberate collaboration seams.</span></div>
      <div class="layer"><strong>Event handlers</strong><span><code>handlers</code> consume public facts and mutate only their owning domain.</span></div>
      <div class="layer private"><strong>Private work</strong><span><code>internal/commands</code> and <code>internal/dao</code> remain implementation details.</span></div>
    </div>
    <div class="big-statement">If a neighboring domain can import the command that “just does the thing,” ownership is only a suggestion.</div>
  </section>

  <section>
    <h2>Start with seven different kinds of ownership</h2>
    <table class="matrix"><thead><tr><th>Profile</th><th>Contexts</th><th>Why it exists</th></tr></thead><tbody><tr><td>Operational</td><td>Ingredients, Drinks, Inventory, Menus, Orders</td><td>business state, commands, queries, events, persistence, policy</td></tr><tr><td>Activity</td><td>Audit</td><td>append-only evidence written by the operation pipeline</td></tr><tr><td>Cross-cutting domain</td><td>Tagging</td><td>owned associations over registered operational targets</td></tr></tbody></table>
    <div class="callout">Consistency does not require identical package trees. Audit and Tagging use smaller profiles because their responsibilities differ.</div>
  </section>

  <section>
    <h2>A module has a public edge and a private center</h2>
    <div class="layers"><div class="layer"><strong><code>module.go</code></strong><span>application-facing facade chooses a typed operation path</span></div><div class="layer"><strong><code>models / queries / events</code></strong><span>deliberate vocabulary for callers and neighboring domains</span></div><div class="layer"><strong><code>handlers</code></strong><span>consume public peer facts and mutate only owned state</span></div><div class="layer private"><strong><code>internal/commands + internal/dao</code></strong><span>business decisions and persistence stay private</span></div></div>
    <div class="callout">Queries answer another domain's question. Events announce a fact. Neither exposes the command that owns the decision.</div>
  </section>

  <section>
    <h2>Composition is ordinary, visible Go</h2>
    <div class="timeline"><div class="step"><strong>Foundation</strong><span>Audit + Tagging schemas</span></div><div class="step"><strong>Ports</strong><span>tag repository + empty registry</span></div><div class="step"><strong>Evidence</strong><span>separate audit writer</span></div><div class="step"><strong>Pipeline</strong><span>dispatcher + writer callback</span></div><div class="step"><strong>Operational modules</strong><span>rows + tag targets</span></div><div class="step"><strong>Public facades</strong><span>Tagging + Audit</span></div></div>
    <div class="cards two"><div class="card"><h3>No import side effects</h3><p>Private SQLite rows register during construction. Invalid or missing registration fails at startup or in architecture tests.</p></div><div class="card"><h3>No second manifest</h3><p><code>TestEveryDomainIsComposed</code> treats domain directories as the source of truth and verifies <code>app.New</code>.</p></div></div>
    <div class="callout">The private Audit writer exists before the public Audit facade, breaking the construction cycle between pipeline activity and authorized audit reads.</div>
  </section>

  <section>
    <h2>Application state is not request state</h2>
    <div class="split"><div class="side"><h3><code>App</code></h3><p>Store and public modules whose private composition retains the configured pipeline. No actor identity.</p></div><div class="bridge">+</div><div class="side"><h3><code>Session</code></h3><p>Binds a persistent TUI or GUI to an authenticated base context, then creates a fresh operation context every time.</p></div></div>
    <div class="flow"><div class="node"><strong>base context</strong>actor + logger + metrics</div><div class="arrow">→</div><div class="node"><strong><code>Session.Context()</code></strong>fresh mutable state</div><div class="arrow">→</div><div class="node"><strong>operation</strong>events + activity + attributes</div><div class="arrow">→</div><div class="node"><strong>discard</strong>nothing leaks forward</div></div>
    <div class="callout">The CLI starts fresh per invocation. Persistent clients reuse authentication, never accumulated operation state.</div>
  </section>

</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Foundation 1.2</div><h1>Let types carry cheap invariants</h1><p class="lede">Use the compiler for distinctions it can defend, and domain behavior for transitions it cannot.</p><div class="section-no">1.2</div></section>

  <section>
    <h2>Let types carry the distinctions they can</h2>
    <div class="cards">
      <div class="card"><h3>Generated entity IDs</h3><p><code>DrinkID</code> and <code>IngredientID</code> share the same generated Cedar method shape without becoming interchangeable parameters.</p></div>
      <div class="card"><h3>Closed amount variants</h3><p>An unexported <code>isAmount</code> method limits <code>Amount</code> to volume and discrete quantities owned by the kernel.</p></div>
      <div class="card"><h3>Validated values</h3><p>Currency, price, quantity, and tag parsers turn accepted external text into domain-shaped values.</p></div>
    </div>
    <div class="callout">Go still permits zero values and package-local construction. Constructors, decoding validation, and boundary checks carry the guarantees the type system cannot.</div>
    <p class="source"><a href="/articles/making-illegal-states-unrepresentable-in-go/">Adjacent article: Making Illegal States Unrepresentable in Go</a></p>
  </section>

  <section>
    <h2>Identity should reveal the entity</h2>
    <div class="split"><div class="side"><h3>Raw string</h3><pre><code class="language-go">func Load(id string)

Load(orderID) // compiles</code></pre><p class="muted">Meaning survives only in names and review.</p></div><div class="bridge">→</div><div class="side"><h3>Generated ID</h3><pre><code class="language-go">func Load(id DrinkID)

Load(orderID) // compiler error</code></pre><p class="accent">Parsing, prefixes, Cedar identity, and JSON behavior stay consistent.</p></div></div>
    <div class="callout">Six entity ID types share generated mechanics without becoming interchangeable values.</div>
  </section>

  <section>
    <h2>Model absence, variants, and concurrency explicitly</h2>
    <div class="cards"><div class="card"><h3>Closed variants</h3><p><code>Amount</code> accepts only kernel-owned volume or discrete quantity implementations.</p></div><div class="card"><h3>Intentional absence</h3><p><code>optional.Value[T]</code> distinguishes absent from present, including a deliberately present zero value.</p></div><div class="card"><h3>Opaque revision</h3><p>Mutable public models round-trip the store token. Surfaces never compare or increment it.</p></div></div>
    <div class="big-statement">Make invalid combinations expensive to express, then validate every decoding boundary.</div>
  </section>

  <section>
    <h2>Capability types remove forbidden moves</h2>
    <div class="split"><div class="side"><h3><code>middleware.Context</code></h3><p>Transaction, principal, activity, <code>AddEvent</code>, and <code>TouchEntity</code>.</p><p class="accent">Commands may originate owned facts.</p></div><div class="bridge">⊃</div><div class="side"><h3><code>HandlerContext</code></h3><p>Transaction, principal, and <code>TouchEntity</code>. No event accumulator.</p><p class="gold">Reactions cannot cascade.</p></div></div>
    <div class="callout">The most reliable prohibition is an API that cannot express the forbidden operation.</div>
  </section>
</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Foundation 1.3</div><h1>Make errors part of the application protocol</h1><p class="lede">Domains choose meaning once. Every present and future edge chooses only how to render it.</p><div class="section-no">1.3</div></section>

  <section>
    <h2>Failure kind is not presentation</h2>
    <div class="flow"><div class="node"><strong>Domain / store</strong>typed failure</div><div class="arrow">→</div><div class="node"><strong><code>pkg/errors</code></strong>semantic kind</div><div class="arrow">→</div><div class="node"><strong>CLI / TUI / GUI</strong>native feedback</div><div class="arrow">→</div><div class="node"><strong>HTTP / gRPC</strong>future mapping</div></div>
    <div class="callout">Lower layers never choose exit codes, colors, dialogs, HTTP status, or gRPC codes.</div>
  </section>

  <section>
    <h2>Six meanings cover the application boundary</h2>
    <table class="matrix"><thead><tr><th>Kind</th><th>Meaning</th><th>Typical response</th></tr></thead><tbody><tr><td>Invalid</td><td>the request is malformed</td><td>fix input</td></tr><tr><td>NotFound</td><td>the resource does not exist</td><td>choose another</td></tr><tr><td>Permission</td><td>the actor is not allowed</td><td>hide or deny</td></tr><tr><td>Conflict</td><td>state collides or revision is stale</td><td>reload or rename</td></tr><tr><td>FailedPrecondition</td><td>valid request, invalid current state</td><td>resolve prerequisite</td></tr><tr><td>Internal</td><td>invariant or dependency failed</td><td>safe message + diagnostics</td></tr></tbody></table>
  </section>

  <section>
    <h2>Diagnostics and safe text are different data</h2>
    <div class="split code-split"><div class="side"><h3>For operators</h3><pre><code class="language-go">errors.Internalf(
  "load inventory: %w", err,
)</code></pre><p><code>Error()</code> retains the cause for logs and wrapping.</p></div><div class="bridge">∥</div><div class="side"><h3>For people</h3><pre><code class="language-go">err.WithUserMessage(
  "Inventory is temporarily unavailable",
)</code></pre><p>Internal detail is generic unless explicitly made safe.</p></div></div>
    <div class="callout">Unknown errors do not inherit this safety guarantee. Classify unexpected failures before a presentation boundary.</div>
  </section>

  <section>
    <h2>Generate the repetitive family, enforce one vocabulary</h2>
    <div class="cards"><div class="card"><h3>Generated</h3><p>Typed constructors, classifiers, metadata, and matching test assertions.</p></div><div class="card"><h3>Wrapped</h3><p><code>%w</code>, <code>Is</code>, and <code>As</code> preserve semantic inspection through context.</p></div><div class="card"><h3>Enforced</h3><p><code>arch-lint</code> rejects direct standard-library <code>errors</code> imports outside <code>pkg/errors</code>.</p></div></div>
    <div class="big-statement">One immutable kind survives every layer without turning the core into a transport library.</div>
  </section>
</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Foundation 1.4</div><h1>Give every operation one trustworthy path</h1><p class="lede">Commands and queries should state intent while the pipeline owns the guarantees around them.</p><div class="section-no">1.4</div></section>

  <section>
    <h2>One path through the application</h2>
    <div class="pipeline">
      <div class="pipe">SerializeTransaction</div><div class="pipe">Logging + Metrics</div><div class="pipe">TrackActivity</div><div class="pipe tx">UnitOfWork begins</div><div class="pipe">load → authorize → handle → authorize result</div><div class="pipe">dispatch events → record success</div><div class="pipe tx">commit everything, or nothing</div>
    </div>
    <div class="callout">Commands do not opt into transactions, authorization, events, or audit independently. The shared path owns the ordering.</div>
    <aside class="notes">This is runtime and unwind order. NewChain lists nested middleware outside-in, so the source declaration reads differently around dispatch and successful activity.</aside>
  </section>

  <section>
    <h2>Go 1.27 puts the operation on its owner</h2>
    <div class="split code-split">
      <div class="side"><div class="eyebrow">Before</div><pre><code class="language-go">spec := middleware.CommandSpec[
    Input, Output,
]{
    Action: authz.ActionCreate,
    Load:   load,
    Handle: m.commands.Create,
}
return middleware.RunCommand(
    m.pipeline, ctx, spec,
)</code></pre></div>
      <div class="bridge">→</div>
      <div class="side"><div class="eyebrow">Go 1.27</div><pre><code class="language-go">m.pipeline.Command(
    ctx,
    authz.ActionCreate,
    input,
    m.commands.Create,
)</code></pre><p class="accent">The configured pipeline is the obvious starting point.</p></div>
    </div>
    <div class="callout">The completed migration removed <code>RunCommand</code> and <code>CommandSpec</code>. Domain facades now enter through the pipeline methods directly.</div>
  </section>

  <section>
    <h2>Six typed entries, one middleware model</h2>
    <div class="cards">
      <div class="card"><h3><code>Query</code></h3><p>Load a Cedar entity, then authorize the result.</p></div><div class="card"><h3><code>QueryResource</code></h3><p>Authorize a known resource around a non-entity result.</p></div><div class="card"><h3><code>PageQuery</code></h3><p>Fill a page with authorized rows without leaking denied ones.</p></div>
      <div class="card"><h3><code>Command</code></h3><p>Authorize caller input and resulting state.</p></div><div class="card"><h3><code>LoadCommand</code></h3><p>Load trusted state inside the transaction.</p></div><div class="card"><h3><code>LoadCommandActions</code></h3><p>Derive transition-specific action requirements from loaded state.</p></div>
    </div>
    <div class="callout">This removed wrappers and specification ceremony. Transactions, authorization, events, audit, paging, and failure behavior did not change.</div>
    <p class="source"><a href="/notes/go-1-27-generic-methods-and-the-mixology-pipeline/">Adjacent note: Go 1.27 Generic Methods and the Mixology Pipeline</a></p>
  </section>

  <section>
    <h2>The chain runs inward, then proves the result outward</h2>
    <div class="split"><div class="side"><h3>Enter</h3><p>Serialize, enrich logs, start metrics and activity, open the unit of work, load trusted state, authorize, handle.</p></div><div class="bridge">↩</div><div class="side"><h3>Unwind</h3><p>Authorize result, dispatch facts, record successful activity, commit, observe final duration and error.</p></div></div>
    <div class="callout">Declaration order and completion order differ. Moving one middleware can move work outside the transaction or hide an unwind failure from telemetry.</div>
  </section>

  <section>
    <h2>The unit of work is the consistency membrane</h2>
    <div class="transaction">domain mutation + prepared event reactions + touched entities + successful audit</div>
    <div class="split"><div class="side"><h3>Success</h3><p>Every write and the durable activity record commit together.</p><p class="accent">One business operation.</p></div><div class="bridge">or</div><div class="side"><h3>Any failure</h3><p>Result authorization, handler, audit, or storage error rolls the complete write graph back.</p><p class="gold">No partial truth.</p></div></div>
    <div class="callout">A caller-supplied transaction retains commit and rollback ownership. Ordinary domain calls use the middleware-managed SQLite transaction.</div>
  </section>

  <section>
    <h2>Load trusted state inside the transaction</h2>
    <div class="flow"><div class="node"><strong>ID + intent</strong>small request</div><div class="arrow">→</div><div class="node"><strong><code>LoadCommand</code></strong>current persisted value</div><div class="arrow">→</div><div class="node"><strong>authorize</strong>before + after</div><div class="arrow">→</div><div class="node"><strong>commit</strong>revision still current</div></div>
    <div class="cards two"><div class="card"><h3>Why not trust a UI model?</h3><p>It may be stale, incomplete, or shaped for display rather than authority.</p></div><div class="card"><h3>Why authorize twice?</h3><p>A policy may allow editing a draft without allowing the transition to produce a published resource.</p></div></div>
  </section>

</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Foundation 1.5</div><h1>Make the architecture executable</h1><p class="lede">The compiler provides privacy. Generators, analyzers, and adversarial tests defend the dependency graph.</p><div class="section-no">1.5</div></section>

  <section>
    <h2>Compiler, generator, analyzer, test</h2>
    <table class="matrix"><thead><tr><th>Rule</th><th>Best carrier</th><th>Example</th></tr></thead><tbody>
      <tr><td>Coarse package privacy</td><td>Go compiler</td><td><code>internal</code> blocks callers outside the owning tree</td></tr>
      <tr><td>Fine package allowlist</td><td><code>arch-lint</code></td><td>only facades, queries, handlers, and internals may consume domain internals</td></tr>
      <tr><td>Repetitive wiring</td><td>Generator</td><td>Event and Cedar registration</td></tr>
      <tr><td>Repository topology</td><td><code>arch-lint</code></td><td>Surfaces stay bespoke; handlers cannot import commands</td></tr>
      <tr><td>Composition completeness</td><td>Architecture test</td><td>Every domain is initialized by <code>app.New</code></td></tr>
      <tr><td>Business behavior</td><td>Integration test</td><td>Retirement rolls back as one operation</td></tr>
    </tbody></table>
  </section>

  <section>
    <h2>Capture ownership instead of naming every module</h2>
    <div class="split code-split">
      <div class="side"><h3>Capture the imported target</h3><pre><code class="language-yaml"># imported target
forbid:
  - app/domains/{module}/internal/**

# permitted importers reuse {module}
except:
  - app/domains/{module}
  - app/domains/{module}/queries/**
  - app/domains/{module}/handlers/**
  - app/domains/{module}/internal/**</code></pre></div>
      <div class="bridge">∧</div>
      <div class="side"><h3>Importer must share ownership</h3><p>The forbidden import captures <code>{module}</code>. Importer exceptions reuse that value, so Drinks cannot claim Ingredients’ private implementation.</p><p class="accent">One rule covers every current and future domain.</p></div>
    </div>
  </section>

  <section>
    <h2>Future adapters inherit the rule</h2>
    <div class="flow"><div class="node"><strong>capture</strong><code>{module}</code> + <code>{surface}</code></div><div class="arrow">→</div><div class="node"><strong>forbid</strong>concrete surface imports</div><div class="arrow">→</div><div class="node"><strong>except</strong>same module + surface</div><div class="arrow">→</div><div class="node"><strong>fixture</strong>CLI, TUI, GUI, and Web</div></div>
    <div class="cards two"><div class="card go"><h3>Allowed fixture</h3><p><code>drinks/surfaces/web/valid</code> imports its own <code>drinks/surfaces/web</code> implementation.</p></div><div class="card stop"><h3>Rejected fixture</h3><p><code>drinks/surfaces/web/invalid-gui</code> imports the GUI surface and domain-internal storage.</p></div></div>
    <div class="callout">The same adversarial fixture separately rejects cross-domain surfaces, mismatched toolkits, and <code>main</code> imports across the current adapters. It proves the configuration, not merely a clean tree.</div>
    <p class="source"><a href="/projects/arch-lint/">Adjacent project: arch-lint</a> · <code>architecture/arch_lint_test.go</code></p>
  </section>

  <section>
    <h2>Spend complexity when the pressure appears</h2>
    <div class="timeline">
      <div class="step"><strong>Folders</strong><span>make ownership legible</span></div><div class="step"><strong>Public contracts</strong><span>separate questions from decisions</span></div><div class="step"><strong>Events</strong><span>reverse reactive dependencies</span></div><div class="step"><strong>Two phases</strong><span>preserve pre-mutation facts</span></div><div class="step"><strong>Projection</strong><span>share action meaning</span></div><div class="step"><strong>SQLite</strong><span>enable concurrent local clients</span></div><div class="step"><strong>Rules</strong><span>freeze lessons into checks</span></div>
    </div>
    <div class="callout">The sequence matters. Each mechanism pays rent by solving a problem the working application has already made concrete.</div>
  </section>
</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Foundation 1.6</div><h1>Make authorization part of the domain</h1><p class="lede">Policy belongs beside the resource language, and enforcement belongs on every trustworthy operation path.</p><div class="section-no">1.6</div></section>

  <section>
    <h2>Each domain owns its policy vocabulary</h2>
    <div class="flow"><div class="node"><strong>Domain model</strong>complete business state</div><div class="arrow">→</div><div class="node"><strong>Generated authz model</strong>Cedar shape</div><div class="arrow">→</div><div class="node"><strong>Principal + action</strong>operation intent</div><div class="arrow">→</div><div class="node"><strong>Cedar evaluator</strong>permit or deny</div></div>
    <div class="callout">The shared evaluator knows Cedar. Ingredients, Menus, and Orders decide what their resources and actions mean.</div>
  </section>

  <section>
    <h2>One decision appears at four scales</h2>
    <div class="cards four"><div class="card"><h3>Workspace</h3><p>Can this actor discover and enter the domain?</p></div><div class="card"><h3>Collection</h3><p>Which rows and counts may become visible?</p></div><div class="card"><h3>Entity</h3><p>May this exact resource be read or selected?</p></div><div class="card"><h3>Action</h3><p>May this exact resource transition now?</p></div></div>
    <div class="callout">Navigation, summaries, lists, and mutations are all application reads. None gets a policy exemption for being convenient UI.</div>
  </section>

  <section>
    <h2>Fill the visible page, not the storage page</h2>
    <div class="flow"><div class="node"><strong>stable candidates</strong>filter + hydrate</div><div class="arrow">→</div><div class="node"><strong>authorize each</strong>deny disappears</div><div class="arrow">→</div><div class="node"><strong>continue scanning</strong>until N visible</div><div class="arrow">→</div><div class="node"><strong>look ahead</strong>safe cursor</div></div>
    <div class="cards two"><div class="card"><h3>Permission denial</h3><p>Expected list behavior. Omit the entity and keep scanning.</p></div><div class="card stop"><h3>Evaluation or storage failure</h3><p>Not a denial. Fail the query instead of returning a believable partial result.</p></div></div>
  </section>

  <section>
    <h2>Counts can leak what lists conceal</h2>
    <div class="split"><div class="side"><h3>Unsafe</h3><p><code>SELECT COUNT(*)</code> reports hidden entities even when the list omits them.</p></div><div class="bridge">→</div><div class="side"><h3>Current contract</h3><p>Count the same authorized page stream the actor is allowed to observe.</p></div></div>
    <div class="big-statement">Authorization changes information architecture, not just button state.</div>
  </section>

  <section>
    <h2>Projection guides. Commands enforce.</h2>
    <div class="split"><div class="side"><h3>Presentation projection</h3><p>Combines permission with durable prerequisites so a view can hide denied actions and explain unavailable ones.</p></div><div class="bridge">≠</div><div class="side"><h3>Authoritative command</h3><p>Reloads current state, repeats authorization, and checks invariants inside the write transaction.</p></div></div>
    <div class="callout">A stale screen may offer an action that just became invalid. That is a normal race, not authority granted by the UI.</div>
  </section>
</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Foundation 1.7</div><h1>Observe the operation, not random functions</h1><p class="lede">Logs diagnose one execution. Metrics describe the population. Neither replaces durable business activity.</p><div class="section-no">1.7</div></section>

  <section>
    <h2>Three lenses answer three questions</h2>
    <div class="cards"><div class="card"><h3>Structured logs</h3><p>What happened during this execution, with actor, action, resource, duration, and diagnostic error?</p></div><div class="card"><h3>Bounded metrics</h3><p>How often, how slowly, and how unsuccessfully do operation classes behave?</p></div><div class="card"><h3>Audit activity</h3><p>Who attempted which business action, against what, and what else changed?</p></div></div>
    <div class="callout">One middleware boundary provides consistent meaning without scattering instrumentation through domain code.</div>
  </section>

  <section>
    <h2>Context accumulates useful log meaning</h2>
    <div class="flow"><div class="node"><strong>Entrypoint</strong>logger + actor</div><div class="arrow">→</div><div class="node"><strong>Pipeline</strong>Cedar action</div><div class="arrow">→</div><div class="node"><strong>Command</strong>primary resource</div><div class="arrow">→</div><div class="node"><strong>Unwind</strong>duration + final error</div></div>
    <div class="cards two"><div class="card"><h3>Deliberate levels</h3><p>Permission denial is informational; query failures warn; command failures error.</p></div><div class="card"><h3>Fresh scope</h3><p>Enriched attributes live only for one operation and cannot bleed into the next session call.</p></div></div>
  </section>

  <section>
    <h2>Metric labels must stay boring</h2>
    <div class="split"><div class="side"><h3>Current instruments</h3><p>Command/query totals use action + result. Error counters and durations use action. Store read/write durations have no labels.</p><p class="accent">Small, stable cardinality.</p></div><div class="bridge">≠</div><div class="side"><h3>Never labels</h3><p>Entity IDs, user filter text, error messages, tag values, or arbitrary resource names.</p><p class="gold">Unbounded and operationally expensive.</p></div></div>
    <div class="callout">Authorization and event metric names are reserved but not currently emitted. The deck distinguishes available vocabulary from actual instrumentation.</div>
  </section>

  <section>
    <h2>Libraries expose a contract; executables own lifecycle</h2>
    <div class="layers"><div class="layer"><strong>Domain + store</strong><span>record through a tiny <code>Metrics</code> interface</span></div><div class="layer"><strong><code>pkg/telemetry</code></strong><span>no-op, memory, OTEL, and Prometheus-backed implementations</span></div><div class="layer"><strong><code>main/&lt;surface&gt;</code></strong><span>address, HTTP server, startup, and shutdown</span></div><div class="layer private"><strong>Runtime constraint</strong><span>concurrent local surfaces need distinct metrics ports</span></div></div>
  </section>
</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Foundation 1.8</div><h1>Treat auditing as a domain</h1><p class="lede">An audit trail is durable business evidence with transaction semantics, policy, filtering, and its own read model.</p><div class="section-no">1.8</div></section>

  <section>
    <h2>An activity is more than a log line</h2>
    <div class="cards"><div class="card"><h3>Who + what</h3><p>Principal, Cedar action, and primary resource identify the attempted operation.</p></div><div class="card"><h3>When + outcome</h3><p>Start, completion, success, and diagnostic error preserve what happened.</p></div><div class="card"><h3>Blast radius</h3><p>Deduplicated touched entity IDs reveal every indirect resource changed by handlers.</p></div></div>
    <div class="callout">Audit is append-only evidence. It is not diagnostic logging and it is not a replayable domain event stream.</div>
  </section>

  <section>
    <h2>Success and failure take different transaction paths</h2>
    <div class="split"><div class="side"><h3>Successful command</h3><div class="transaction">mutation + handlers + success audit</div><p>If recording fails, the business operation rolls back.</p></div><div class="bridge">∥</div><div class="side"><h3>Failed managed command</h3><div class="transaction">rollback first</div><p>Then persist the failed attempt in a separate managed write.</p></div></div>
    <div class="callout"><code>recordSuccessfulActivity</code> runs inside the unit of work. <code>TrackActivity</code> records a managed failure only after rollback. Caller-owned transactions keep failure activity under the caller's decision.</div>
  </section>

  <section>
    <h2>Touches turn fan-out into explainable history</h2>
    <div class="flow"><div class="node"><strong>Ingredients</strong>retire catalog item</div><div class="arrow">→</div><div class="node"><strong>Drinks</strong>touch recipes</div><div class="arrow">→</div><div class="node"><strong>Inventory</strong>touch stock</div><div class="arrow">→</div><div class="node"><strong>Menus + Orders</strong>touch dependents</div></div>
    <div class="big-statement">One originating activity can answer “what changed because of this decision?” without pretending every reaction was a separate user command.</div>
  </section>

  <section>
    <h2>Failure to record has an explicit policy</h2>
    <table class="matrix"><thead><tr><th>Situation</th><th>Audit behavior</th><th>Returned result</th></tr></thead><tbody><tr><td>successful command, success audit fails</td><td>inside UoW</td><td>internal error; command rolls back</td></tr><tr><td>failed command, failure audit succeeds</td><td>after managed rollback</td><td>original command error</td></tr><tr><td>failed command, failure audit also fails</td><td>recording failure is logged</td><td>original command error remains authoritative</td></tr></tbody></table>
  </section>

  <section>
    <h2>The read side is still an application boundary</h2>
    <div class="layers"><div class="layer"><strong>Audit module</strong><span>list, count, entity history, and actor activity</span></div><div class="layer"><strong>Query contract</strong><span>action, principal, entity, time window, typed expression, cursor</span></div><div class="layer"><strong>Pipeline</strong><span>Cedar authorization and permission-safe paging</span></div><div class="layer private"><strong>Surfaces</strong><span>CLI, TUI, and GUI adapt the same append-only evidence</span></div></div>
    <div class="callout">The system that records activity automatically does not grant everyone permission to inspect it.</div>
  </section>
</section>

<section>
  <section class="centered section-slide">
    <div class="eyebrow">Foundation 2.1</div><h1>Turn calls into bounded event fan-out</h1>
    <p class="lede">Ingredient retirement changes four domains without giving Ingredients four collaborators.</p><div class="section-no">2.1</div>
  </section>

  <section>
    <h2>The tempting implementation</h2>
    <pre><code class="language-go">func (m *Ingredients) Retire(ctx Context, id ID) error {
    m.inventory.Remove(ctx, id)
    m.drinks.ReplaceOrReview(ctx, id)
    m.orders.BlockSnapshots(ctx, id)
    m.menus.Recalculate(ctx, id)
    return m.ingredients.Retire(ctx, id)
}</code></pre>
    <div class="rule-list"><div class="rule"><b>×</b><span>Ingredients decides what retirement means everywhere.</span></div><div class="rule"><b>×</b><span>The source domain imports every consumer.</span></div><div class="rule"><b>×</b><span>Adding a reaction edits the initiating command.</span></div><div class="rule"><b>×</b><span>The “simple” path becomes the system map.</span></div></div>
  </section>

  <section>
    <h2>Separate questions from decisions</h2>
    <div class="split"><div class="side"><h3>Public query</h3><p>“Is this ingredient referenced?”</p><p>Safe when the caller owns the decision that follows.</p></div><div class="bridge">vs</div><div class="side"><h3>Public event</h3><p>“This ingredient was retired with this explicit replacement intent.”</p><p>Each consumer owns its reaction.</p></div></div>
    <div class="callout"><strong>Queries move information.</strong> Events move facts. Neither exposes another domain’s command implementation.</div>
  </section>

  <section>
    <h2>One fact, bounded fan-out</h2>
    <div class="fanout"><div class="event-source"><strong>Ingredients</strong><span class="small">IngredientDeleted</span></div><div class="event-bus">⇢</div><div class="handler-stack"><div class="handler"><strong>Drinks</strong>rewrite future recipes or require review</div><div class="handler"><strong>Inventory</strong>remove unusable stock</div><div class="handler"><strong>Orders</strong>block affected snapshots, never rewrite history</div><div class="handler"><strong>Menus</strong>recompute availability, preserve curation</div></div></div>
    <div class="transaction">command mutation + four leaf reactions + touched entities + successful audit = one SQLite transaction</div>
  </section>

  <section>
    <h2>The event dispatcher is generated glue</h2>
    <div class="flow five"><div class="node"><strong>AddEvent</strong>owned fact</div><div class="arrow">→</div><div class="node"><strong>command returns</strong>still in UoW</div><div class="arrow">→</div><div class="node"><strong>Handling</strong>all snapshots</div><div class="arrow">→</div><div class="node"><strong>Handle</strong>all reactions</div><div class="arrow">→</div><div class="node"><strong>audit + commit</strong>atomic result</div></div>
    <pre><code class="language-go">func (h *IngredientDeleted) Handling(
    ctx *middleware.HandlerContext,
    event ingredientsevents.IngredientDeleted,
) error // snapshot pre-mutation state

func (h *IngredientDeleted) Handle(
    ctx *middleware.HandlerContext,
    event ingredientsevents.IngredientDeleted,
) error // apply the owned reaction</code></pre>
    <div class="callout"><code>HandlerContext</code> has transaction, principal, and <code>TouchEntity</code>. It deliberately has no <code>AddEvent</code>.</div>
  </section>

  <section>
    <h2>Prepare every reader before mutating anything</h2>
    <div class="flow"><div class="node"><strong>fresh handlers</strong>one event-local receiver each</div><div class="arrow">→</div><div class="node"><strong>optional <code>Handling</code></strong>all snapshots finish</div><div class="arrow">┃</div><div class="node"><strong>every <code>Handle</code></strong>apply owned reactions</div><div class="arrow">→</div><div class="node"><strong>commit</strong>one outcome</div></div>
    <div class="callout"><code>Handling</code> is a generator-recognized method convention, not a shared Go interface. Correctness never depends on generated handler order.</div>
  </section>

  <section>
    <h2>No cascades is defended twice</h2>
    <div class="split"><div class="side"><h3>Capability boundary</h3><p><code>HandlerContext</code> omits <code>AddEvent</code>, so ordinary handlers cannot enqueue another fact.</p></div><div class="bridge">+</div><div class="side"><h3>Runtime boundary</h3><p><code>DispatchEvents</code> clones the original event slice before delivery, so accidental later additions are not dispatched.</p></div></div>
    <div class="big-statement">Every event has a bounded, reviewable leaf fan-out. Multi-step time-spanning work deserves an explicit workflow.</div>
  </section>

  <section>
    <h2>Package rules preserve the dependency direction</h2>
    <div class="rule-list"><div class="rule"><b>×</b><span><code>commands-emit-own-domain-events</code></span></div><div class="rule"><b>×</b><span><code>handlers-no-commands</code></span></div><div class="rule"><b>×</b><span><code>handlers-no-modules</code></span></div><div class="rule"><b>×</b><span><code>queries-no-commands</code></span></div></div>
    <div class="big-statement">The event changes the dependency direction. The analyzer keeps it changed.</div>
  </section>
</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Foundation 2.2</div><h1>Give cross-cutting tags an owner</h1><p class="lede">Shared vocabulary does not require ownerless persistence, global meaning, or private-domain reach-through.</p><div class="section-no">2.2</div></section>

  <section>
    <h2>Tagging is a bounded context</h2>
    <div class="split"><div class="side"><h3>Kernel value</h3><p><code>tag.Tag</code> owns canonical key/value parsing, validation, ordering, and formatting.</p></div><div class="bridge">→</div><div class="side"><h3>Tagging domain</h3><p>Owns polymorphic associations, authorized mutations, discovery, summary, and target registration.</p></div></div>
    <div class="callout">A tag may influence filtering, presentation, or Cedar ABAC. Its business meaning remains with the policy and domain that interpret it.</div>
  </section>

  <section>
    <h2>The registry reverses the dependency</h2>
    <div class="fanout"><div class="event-source"><strong>Tagging</strong><span class="small">target registry</span></div><div class="event-bus">⇄</div><div class="handler-stack"><div class="handler"><strong>Operational domain provides</strong>load complete Cedar state</div><div class="handler"><strong>Operational domain provides</strong>bulk active-target check</div><div class="handler"><strong>Operational domain provides</strong>get, tag, and untag action IDs</div><div class="handler"><strong>Tagging provides</strong>one narrow association repository port</div></div></div>
    <div class="callout">Tagging never imports Ingredients, Drinks, Inventory, Menus, or Orders models and private DAOs.</div>
  </section>

  <section>
    <h2>Hydration stays with the entity owner</h2>
    <div class="flow"><div class="node"><strong>Domain DAO</strong>load owned rows</div><div class="arrow">→</div><div class="node"><strong>tag repository</strong>batch associations</div><div class="arrow">→</div><div class="node"><strong>Domain model</strong>complete tags</div><div class="arrow">→</div><div class="node"><strong>Cedar + filter</strong>evaluate full state</div></div>
    <div class="callout">The association store is shared infrastructure. The complete Ingredient or Drink is still assembled by its owner before authorization and exact filtering.</div>
  </section>

  <section>
    <h2>Replace is one intent with dynamic authority</h2>
    <table class="matrix"><thead><tr><th>Difference</th><th>Required action</th><th>Recorded activity</th></tr></thead><tbody><tr><td>add or change values</td><td>tag</td><td rowspan="3">one stable tag operation</td></tr><tr><td>remove keys</td><td>untag</td></tr><tr><td>mixed replacement</td><td>tag + untag</td></tr></tbody></table>
    <div class="callout"><code>LoadCommandActions</code> derives the complete Cedar action set from current tags and the desired complete set.</div>
  </section>

  <section>
    <h2>Compose domain change and tag change atomically</h2>
    <div class="transaction">non-nil tag intent: <code>RunTaggedMutation</code> owns or joins one shared transaction</div>
    <div class="flow"><div class="node"><strong>validate tags</strong>before write</div><div class="arrow">→</div><div class="node"><strong>domain command</strong>normal pipeline</div><div class="arrow">+</div><div class="node"><strong><code>Tags.Replace</code></strong>normal pipeline</div><div class="arrow">→</div><div class="node"><strong>commit</strong>both or neither</div></div>
    <div class="cards two"><div class="card"><h3><code>nil</code> desired set</h3><p>Preserve existing tags and run only the domain mutation.</p></div><div class="card"><h3>Non-nil empty set</h3><p>Explicitly clear every tag as part of the same application operation.</p></div></div>
    <div class="callout">The domain command and <code>Tags.Replace</code> remain two normal pipeline commands with two audit activities, committed atomically together.</div>
  </section>

  <section>
    <h2>Discovery is its own authorized workflow</h2>
    <div class="cards"><div class="card"><h3>Show</h3><p>Find active entity references for an exact tag or every value of a key.</p></div><div class="card"><h3>Summary</h3><p>Aggregate canonical tags across active registered entity types.</p></div><div class="card"><h3>Policy</h3><p>Tagging-owned Cedar actions govern discovery; referenced entity authorization is not silently replayed.</p></div></div>
    <div class="callout">Inactive targets are excluded from discovery through each owner's registered bulk check. Stale association rows are not silently deleted.</div>
  </section>
</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Foundation 2.3</div><h1>Give people and programs one filter language</h1><p class="lede">Own exact expression semantics above storage, authorization, and every presentation surface.</p><div class="section-no">2.3</div></section>

  <section>
    <h2>The schema is a public domain contract</h2>
    <div class="flow"><div class="node"><strong>typed filter view</strong>stable field names</div><div class="arrow">→</div><div class="node"><strong>Expr parser + checker</strong>accepted syntax</div><div class="arrow">→</div><div class="node"><strong>owned tree</strong>stable semantics</div><div class="arrow">→</div><div class="node"><strong>surface help</strong>fields + examples</div></div>
    <div class="callout">The filter view need not mirror a SQLite row or returned model. It can expose nested and hydrated values without leaking persistence.</div>
  </section>

  <section>
    <h2>Borrow a compiler, keep ownership</h2>
    <div class="cards"><div class="card"><h3><code>Source</code></h3><p>The trimmed expression a person supplied.</p></div><div class="card"><h3><code>String</code></h3><p>Canonical syntax for display and reparsing.</p></div><div class="card"><h3><code>Tree</code></h3><p>Mixology's stable node model for integrations and SQL planning.</p></div></div>
    <div class="callout">Expr optimization is deliberately disabled. Expr parses, checks, and executes; Mixology owns the restricted language and pushdown plan.</div>
  </section>

  <section>
    <h2>One expression, two execution stages</h2>
    <div class="flow"><div class="node"><strong>checked expression</strong>exact contract</div><div class="arrow">→</div><div class="node"><strong>safe SQL pushdown</strong>candidate reduction</div><div class="arrow">→</div><div class="node"><strong>hydrate</strong>tags + derived values</div><div class="arrow">→</div><div class="node"><strong><code>Match</code></strong>authoritative result</div></div>
    <div class="callout"><code>ApplySQLPushdowns</code> returns candidates, never proof. Every operational DAO evaluates the complete hydrated view afterward.</div>
  </section>

  <section>
    <h2>Push down only what the full expression requires</h2>
    <div class="split"><div class="side"><h3>Conjunction</h3><p><code>A && tags.contains("x")</code></p><p>Persisted <code>A</code> is required even when tags need memory evaluation.</p><p class="accent">Push down A safely.</p></div><div class="bridge">≠</div><div class="side"><h3>Disjunction</h3><p><code>A || tags.contains("x")</code></p><p>A row failing <code>A</code> may still match after tag hydration.</p><p class="gold">Do not push down A alone.</p></div></div>
  </section>

  <section>
    <h2>Common constraints survive alternatives</h2>
    <pre><code class="language-text">(category == "spirit" && tags contains "featured")
||
(category == "spirit" && name.contains("gin"))</code></pre>
    <div class="flow"><div class="node"><strong>both branches require</strong><code>category == "spirit"</code></div><div class="arrow">→</div><div class="node"><strong>SQL candidate set</strong>spirits only</div><div class="arrow">→</div><div class="node"><strong>exact Match</strong>full OR expression</div></div>
    <div class="callout">Optimization is a theorem about preserved truth, not a list of AST nodes the translator happens to understand.</div>
  </section>

  <section>
    <h2>Filtering and authorization compose in order</h2>
    <div class="flow"><div class="node"><strong>parse once</strong>typed invalid on error</div><div class="arrow">→</div><div class="node"><strong>filter + hydrate</strong>domain semantics</div><div class="arrow">→</div><div class="node"><strong>authorize each</strong>elide denies</div><div class="arrow">→</div><div class="node"><strong>page</strong>fill visible count</div></div>
    <div class="callout">Audit can use direct <code>ApplySQL</code> because its filter view comes from one row. Operational domains use staged hydration.</div>
    <p class="source"><a href="/articles/typed-filtering-over-sqlite/">Adjacent article: Typed Filtering over SQLite</a></p>
  </section>
</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Foundation 2.4</div><h1>Make persistence a replaceable boundary</h1><p class="lede">The bstore-to-SQLite migration proved which contracts belonged to the application and which belonged to an engine.</p><div class="section-no">2.4</div></section>

  <section>
    <h2>Preserve the contract, replace the engine</h2>
    <table class="matrix"><thead><tr><th>Preserved</th><th>Rebuilt</th></tr></thead><tbody><tr><td>domain ownership and public module contracts</td><td>DAO implementations, rows, and hydration adapters</td></tr><tr><td>models, commands, queries, policies, events</td><td>schema registration and row conversion</td></tr><tr><td>transaction participation</td><td>query builder and cursor predicates</td></tr><tr><td>typed errors and filter semantics</td><td>SQLite mapping and safe pushdowns</td></tr><tr><td>surface-observable behavior</td><td>change monitoring and concurrency coordination</td></tr></tbody></table>
  </section>

  <section>
    <h2>SQLite stays below domain persistence</h2>
    <div class="layers"><div class="layer"><strong>Domain DAO</strong><span>owned queries, row conversion, hydration</span></div><div class="layer"><strong>Typed store API</strong><span><code>Register</code>, <code>Get</code>, <code>Insert</code>, <code>Update</code>, <code>Query</code></span></div><div class="layer"><strong>Unit of work</strong><span>shared transaction carried by operation context</span></div><div class="layer private"><strong>modernc SQLite</strong><span>WAL, constraints, revisions, migration ledger, data version</span></div></div>
  </section>

  <section>
    <h2>Several processes can share one local truth</h2>
    <div class="flow"><div class="node"><strong>CLI</strong>short write</div><div class="arrow">→</div><div class="node"><strong>SQLite WAL</strong>one writer, many readers</div><div class="arrow">←</div><div class="node"><strong>TUI</strong>persistent reader</div><div class="arrow">↔</div><div class="node"><strong>GUI</strong>persistent reader</div></div>
    <div class="cards two"><div class="card"><h3>Process coordination</h3><p>Busy timeout and immediate transactions make writer contention explicit.</p></div><div class="card"><h3>Application coordination</h3><p>Keep commands short; never hold a transaction while waiting for user input.</p></div></div>
  </section>

  <section>
    <h2>Revisions turn stale writes into typed conflicts</h2>
    <div class="state-line"><div class="state">read rev 7</div><div class="arrow">→</div><div class="state active">other client writes rev 8</div><div class="arrow">→</div><div class="state blocked">update WHERE rev = 7</div><div class="arrow coral">⤫</div><div class="state review">Conflict</div></div>
    <div class="callout">Public mutable models carry an opaque revision. The store performs the atomic comparison and increment.</div>
  </section>

  <section>
    <h2>Invalidation carries no domain truth</h2>
    <div class="flow"><div class="node"><strong>SQLite <code>data_version</code></strong>external commit observed</div><div class="arrow">→</div><div class="node"><strong><code>Signals</code></strong>coalesced edge</div><div class="arrow">+</div><div class="node"><strong><code>Epoch</code></strong>level guard</div><div class="arrow">→</div><div class="node"><strong>ordinary query</strong>reload authorized state</div></div>
    <div class="callout">The epoch closes lost-wakeup gaps around coalesced signals. Neither carries records or bypasses application policy, filters, and request-order guards.</div>
  </section>

  <section>
    <h2>Treat the file format honestly</h2>
    <div class="cards"><div class="card"><h3>Migration ledger</h3><p>Ordered migrations advance deliberately; a database from a newer schema is rejected.</p></div><div class="card"><h3>Registration</h3><p>Explicit model schemas fail early; imports do not mutate global persistence state.</p></div><div class="card"><h3>Errors</h3><p>Constraints and stale revisions become application kinds, not leaked driver strings.</p></div></div>
    <p class="source"><a href="/articles/migrating-mixology-from-bstore-to-sqlite/">Adjacent article: Migrating Mixology from bstore to SQLite</a></p>
  </section>
</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Domain workshop 3.1</div><h1>Preserve truth through degradation</h1><p class="lede">A system can remain operational without pretending its state is healthy.</p><div class="section-no">3.1</div></section>

  <section>
    <h2>Retirement is a business decision</h2>
    <table class="matrix"><thead><tr><th>Reference</th><th>No replacement</th><th>Permanent replacement</th></tr></thead><tbody><tr><td>Required recipe component</td><td class="maybe">keep visible, review required</td><td class="yes">rewrite compatible future recipe</td></tr><tr><td>Optional component</td><td class="yes">remove from future recipe</td><td class="yes">rewrite when compatible</td></tr><tr><td>Accepted order snapshot</td><td class="no">block, preserve snapshot</td><td class="no">block, preserve snapshot</td></tr><tr><td>Published menu item</td><td class="maybe" colspan="2">preserve curation and recalculate current availability</td></tr></tbody></table>
  </section>

  <section>
    <h2>Three substitutions, three meanings</h2>
    <div class="cards"><div class="card"><h3>Recipe substitute</h3><p>A modeled alternative inside the drink. It is not permission to rewrite the canonical recipe.</p></div><div class="card"><h3>Operational substitution</h3><p>A temporary way to fulfill a drink. It affects readiness and availability.</p></div><div class="card"><h3>Permanent replacement</h3><p>Explicit retirement intent carried by the source event, including conversion.</p></div></div>
    <p class="source"><code>IngredientDeleted{Replacement, ReplacementRatio}</code> carries explicit permanent intent.</p>
    <div class="callout">Similarity is not intent. Consumers must not infer permanent replacement from whatever substitute happens to be available.</div>
  </section>

  <section>
    <h2>Rewrite plans. Preserve records.</h2>
    <div class="split"><div class="side"><h3>Future intent</h3><p>Draft recipes and menus may be rewritten, reviewed, or prevented from publication.</p><p class="accent">Plans can absorb new truth.</p></div><div class="bridge">∥</div><div class="side"><h3>Historical truth</h3><p>Accepted order snapshots keep the ingredient the customer actually ordered.</p><p class="gold">History can be blocked, never laundered.</p></div></div>
  </section>

  <section>
    <h2>Degradation is not promotion</h2>
    <div class="state-line"><div class="state active">published</div><div class="arrow">→</div><div class="state review">degraded but honest</div><div class="arrow">│</div><div class="state">draft</div><div class="arrow coral">⤫</div><div class="state blocked">known-bad publish</div></div>
    <div class="cards two"><div class="card"><h3>Existing published menu</h3><p>May remain published while item availability reflects new operational truth.</p></div><div class="card stop"><h3>Draft promotion</h3><p>Readiness blockers prevent publishing state already known to be unsuitable.</p></div></div>
  </section>

  <section>
    <h2>Readiness belongs to Menus</h2>
    <div class="flow"><div class="node"><strong>Load menu</strong>authorized state</div><div class="arrow">→</div><div class="node"><strong>Evaluate</strong>recipes + stock</div><div class="arrow">→</div><div class="node"><strong>Report</strong>blockers + warnings</div><div class="arrow">→</div><div class="node"><strong>Publish</strong>re-check in command</div></div>
    <div class="cards two"><div class="card stop"><h3>Blockers</h3><p>Invalid canonical state, unavailable items, or temporary substitution.</p></div><div class="card warn"><h3>Warnings</h3><p>Operational concerns such as low stock that deserve visibility but not a false invariant.</p></div></div>
  </section>
</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Domain workshop 3.2</div><h1>Grow a reciprocal workflow</h1><p class="lede"><span class="decision">planned workshop</span><br>Add Procurement only when the new business loop teaches something the current seven contexts cannot.</p><div class="section-no">3.2</div></section>

  <section>
    <h2>The next build: stock creates demand</h2>
    <div class="flow five"><div class="node"><strong>Inventory</strong>stock becomes low</div><div class="arrow">⇢</div><div class="node"><strong>Procurement</strong>record demand</div><div class="arrow">→</div><div class="node"><strong>Explicit operation</strong>draft purchase order</div><div class="arrow">→</div><div class="node"><strong>Supplier</strong>ships goods</div><div class="arrow">⇢</div><div class="node"><strong>Inventory</strong>records receipt</div></div>
    <div class="callout">This chapter is a workshop plan, not current shipped behavior. The deck keeps that status explicit.</div>
  </section>

  <section>
    <h2>Establish ownership before packages</h2>
    <div class="cards"><div class="card"><h3>Inventory owns</h3><p>On-hand amount, reservation, thresholds, and stock facts.</p></div><div class="card"><h3>Procurement owns</h3><p>Suppliers, offerings, purchase orders, receiving workflow, and commercial intent.</p></div><div class="card warn"><h3>Later: Analytics observes</h3><p>Queryable facts beside the completed slice. It does not become a dependency of the write path.</p></div></div>
  </section>

  <section>
    <h2>Build the slice in visible increments</h2>
    <div class="timeline"><div class="step"><strong>Suppliers</strong><span>identity and offerings</span></div><div class="step"><strong>Purchase orders</strong><span>stateful lifecycle</span></div><div class="step"><strong>Low-stock facts</strong><span>draft demand, idempotently</span></div><div class="step"><strong>Receipt facts</strong><span>inventory reacts</span></div><div class="step"><strong>Consistency view</strong><span>show what converged</span></div><div class="step"><strong>Workflow limit</strong><span>find hidden coordination</span></div><div class="step"><strong>Outbox</strong><span>only if commit boundary moves</span></div></div>
  </section>

  <section>
    <h2>When a handler becomes a workflow</h2>
    <div class="split"><div class="side"><h3>Leaf reaction</h3><p>One fact, bounded local mutation, same transaction, no new event.</p><p class="accent">Keep it in a handler.</p></div><div class="bridge">→</div><div class="side"><h3>Process manager</h3><p>Waits over time, coordinates retries or compensations, tracks intermediate state, spans commits.</p><p class="gold">Name the workflow.</p></div></div>
    <div class="callout">Add an outbox when delivery must survive a transaction boundary. Do not use it to decorate a transaction that is already atomic.</div>
  </section>
</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Surfaces 4.1</div><h1>Build a reusable MVVM toolkit for the terminal</h1><p class="lede">Bubble Tea supplies the runtime. Mixology owns the view-model contract.</p><div class="section-no">4.1</div></section>

  <section>
    <h2>Adapt the pattern to the runtime</h2>
    <div class="split"><div class="side"><h3>Reusable MVVM seam</h3><p>A screen owns presentation state and commands behind a testable view-model contract.</p></div><div class="bridge">+</div><div class="side"><h3>Bubble Tea runtime</h3><p>Messages drive explicit updates, commands carry effects, and a string view renders each frame.</p></div></div>
    <div class="big-statement">The framework is an implementation detail of the toolkit, not the architecture of every screen.</div>
  </section>

  <section>
    <h2>The shell owns application concerns</h2>
    <div class="ownership"><div><h3>Domain surface</h3><ul><li>typed presentation state</li><li>queries and commands</li><li>domain workflows</li><li>action projection</li></ul></div><div class="shared"><h3>Root application shell</h3><ul><li>route and back stack</li><li>cached view models</li><li>title, status, help</li><li>global keys and sizing</li><li>deferred invalidation</li></ul></div><div><h3>TUI toolkit</h3><ul><li>view-model contract</li><li>list/detail and viewports</li><li>forms and dialogs</li><li>layout, keys, styles</li></ul></div></div>
  </section>

  <section>
    <h2>Only the root is a <code>tea.Model</code></h2>
    <div class="split"><div class="side"><h3>Bubble Tea contract</h3><pre><code class="language-go">Update(tea.Msg) (
    tea.Model, tea.Cmd,
)</code></pre><p>The executable shell satisfies this runtime boundary.</p></div><div class="bridge">≠</div><div class="side"><h3>Mixology contract</h3><pre><code class="language-go">Update(tea.Msg) (
    ViewModel, tea.Cmd,
)</code></pre><p>Every domain screen stays inside the richer repository-owned abstraction.</p></div></div>
    <div class="callout">Returning <code>ViewModel</code> preserves help and interaction contracts after every update. Domain screens neither embed nor pretend to be <code>tea.Model</code>.</div>
  </section>

  <section>
    <h2>A deliberately small contract</h2>
    <pre><code class="language-go">type ViewModel interface {
    Init() tea.Cmd
    Update(tea.Msg) (ViewModel, tea.Cmd)
    View() string
    ShortHelp() []key.Binding
    FullHelp() [][]key.Binding
    Interaction() Interaction
}

type Interaction struct {
    CapturesText bool
    HandlesBack  bool
}</code></pre>
    <div class="callout">The toolkit knows Bubble Tea. It does not know Drinks, Menus, Cedar actors, or the application composition root.</div>
  </section>

  <section>
    <h2>The toolkit is a kit, not a base screen</h2>
    <div class="cards four"><div class="card"><h3>Browse</h3><p><code>ListDetail</code>, typed <code>ListItem[T]</code>, summaries, loading, filtering, paging, and selection.</p></div><div class="card"><h3>Compose</h3><p><code>DetailViewport</code>, <code>FormViewport</code>, layout arithmetic, reusable components.</p></div><div class="card"><h3>Interact</h3><p>Forms, dialogs, keys, styles, help bindings, and explicit input ownership.</p></div><div class="card"><h3>Refresh</h3><p>Domain-payload-free invalidation starts an ordinary query; request tokens reject stale results.</p></div></div>
    <div class="callout"><code>pkg/testutil/tuitest</code> is the deterministic program driver. It tests the toolkit and completed application without becoming part of either.</div>
  </section>

  <section>
    <h2>Typed messages keep ownership visible</h2>
    <div class="flow"><div class="node"><strong><code>tea.Msg</code></strong>input arrives</div><div class="arrow">→</div><div class="node"><strong>Root shell</strong>consults <code>Interaction</code></div><div class="arrow">→</div><div class="node"><strong>ViewModel</strong>updates state</div><div class="arrow">→</div><div class="node"><strong><code>tea.Cmd</code></strong>returns typed result</div></div>
    <div class="cards two"><div class="card"><h3>Reusable mechanics</h3><p>Generic list items retain their typed domain values while satisfying Bubbles interfaces.</p></div><div class="card"><h3>Domain choices</h3><p>Publish, complete, cancel, adjust, and retire remain bindings owned by their domain adapters.</p></div></div>
    <div class="callout">External change? Inactive screens become stale. Active input finishes first, then a domain-payload-free invalidation starts the screen's normal tokenized query.</div>
  </section>

  <section>
    <h2>Tests follow the ownership</h2>
    <div class="evidence-ladder"><div class="rung">pure presentation model tests</div><div class="rung">component update and rendering tests</div><div class="rung">domain surface tests</div><div class="rung">real Bubble Tea program driver</div><div class="rung">root navigation and input ownership</div><div class="rung">cross-surface persisted behavior</div></div>
  </section>
</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Surfaces 4.2</div><h1>Adapt the MVVM toolkit to retained widgets</h1><p class="lede">Fyne changes the interaction model, so the reusable mechanics change with it.</p><div class="section-no">4.2</div></section>

  <section>
    <h2>Start from the application seam</h2>
    <div class="layers"><div class="layer"><strong><code>main/gui</code></strong><span>database, actor, logs, application, session, native lifecycle</span></div><div class="layer"><strong>domain GUI surfaces</strong><span>presenters and views shaped for each bounded context</span></div><div class="layer"><strong><code>pkg/toolkits/gui</code></strong><span>shell, forms, tables, semantic controls, dialogs, executors</span></div><div class="layer private"><strong>Fyne runtime</strong><span>retained widgets, callbacks, windows, platform event loop</span></div></div>
  </section>

  <section>
    <h2>Make state publication the binding seam</h2>
    <div class="ownership"><div><h3>State</h3><ul><li>plain typed snapshot</li><li>items and selection</li><li>mode, form, errors</li><li>busy and action state</li></ul></div><div class="shared"><h3>Presenter</h3><ul><li>calls the application</li><li>owns latest loads</li><li>admits one submission</li><li>publishes clones via <code>OnChange</code></li></ul></div><div><h3>View</h3><ul><li>subscribes to state</li><li>updates Fyne controls</li><li>binds pointer and keys</li><li>owns widget-local state</li></ul></div></div>
    <div class="callout">Synchronous UI actions can publish directly. Async completions and external invalidation cross the injected <code>Dispatcher</code> before touching presenter or widget state.</div>
  </section>

  <section>
    <h2>The GUI toolkit owns retained-mode mechanics</h2>
    <div class="flow"><div class="node"><strong>Shell + Route</strong>cache and activate views</div><div class="arrow">→</div><div class="node"><strong>Standard pages</strong>layout and hierarchy</div><div class="arrow">→</div><div class="node"><strong>Semantic controls</strong>stable test identities</div><div class="arrow">→</div><div class="node"><strong>Domain view</strong>renders state</div></div>
    <div class="cards"><div class="card"><h3>Navigation</h3><p><code>UnsavedChanges</code> guards route changes. <code>Commander</code> gives menus, shortcuts, and controls the same intents.</p></div><div class="card"><h3>Presentation</h3><p>List, form, filter, paging, table, tag, validation, dialog, and error mechanics stay domain-free.</p></div><div class="card"><h3>Testing</h3><p>Semantic controls preserve visible guards so tests trigger the same behavior as a person.</p></div></div>
  </section>

  <section>
    <h2>Async work has two boundaries</h2>
    <div class="flow"><div class="node"><strong>Presenter</strong>requests work</div><div class="arrow">→</div><div class="node"><strong>Executor</strong>runs application call</div><div class="arrow">→</div><div class="node"><strong>Dispatcher</strong>publishes on UI thread</div><div class="arrow">→</div><div class="node"><strong>View</strong>updates widgets</div></div>
    <div class="cards"><div class="card"><h3><code>LatestRequest[T]</code></h3><p>Cancels superseded loads and rejects stale queued publications.</p></div><div class="card"><h3><code>Submission</code></h3><p>Admits one mutation, then releases on dispatched completion before presenting its result.</p></div><div class="card"><h3><code>GatedDispatcher</code></h3><p>Drops widget publications after desktop shutdown closes the publication gate.</p></div></div>
  </section>

  <section>
    <h2>Reviewable slices kept the change surface small</h2>
    <div class="timeline"><div class="step"><strong>Shell</strong><span>routes + lifecycle</span></div><div class="step"><strong>Models</strong><span>state + errors</span></div><div class="step"><strong>Toolkits</strong><span>standard mechanics</span></div><div class="step"><strong>Domains</strong><span>workspace by workspace</span></div><div class="step"><strong>Parity</strong><span>paging + workflows</span></div><div class="step"><strong>Lifecycle</strong><span>drain accepted work</span></div><div class="step"><strong>Evidence</strong><span>process + visual checks</span></div></div>
  </section>

  <section>
    <h2>The integration gaps were architectural clues</h2>
    <div class="cards four"><div class="card"><h3>Dashboard</h3><p>Moved business-shaped aggregation into <code>app</code>.</p></div><div class="card"><h3>Tags</h3><p>Needed one atomic application mutation.</p></div><div class="card"><h3>Paging</h3><p>Had to remain explicit and domain-backed.</p></div><div class="card"><h3>Shutdown</h3><p>Required admission, drain, then store close.</p></div></div>
    <div class="callout">A third interface is useful precisely because it refuses to fit abstractions built around the first two.</div>
  </section>
</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Surfaces 4.3</div><h1>Use the third surface as an architecture test</h1><p class="lede">Difference creates pressure. Pressure reveals misplaced ownership.</p><div class="section-no">4.3</div></section>

  <section>
    <h2>Parity is a union, not a porting checklist</h2>
    <div class="split"><div class="side"><h3>What every surface must preserve</h3><p>Application capabilities, authorization, invariants, error meaning, atomicity, and persisted results.</p></div><div class="bridge">∪</div><div class="side"><h3>What each runtime teaches</h3><p>CLI composability, TUI keyboard flow, GUI retained state, async lifecycle, dialogs, and focus.</p></div></div>
  </section>

  <section>
    <h2>Hidden ownership fails under a different runtime</h2>
    <table class="matrix"><thead><tr><th>Pressure</th><th>Revealed mistake</th><th>Durable correction</th></tr></thead><tbody><tr><td>Persistent dashboard</td><td>views assembled business aggregates</td><td>shared application read model</td></tr><tr><td>Tag editing</td><td>two commands could partially commit</td><td>atomic <code>RunTaggedMutation</code></td></tr><tr><td>GUI action state</td><td>views duplicated policy-shaped logic</td><td>domain action projectors</td></tr><tr><td>Native shutdown</td><td>store could close under accepted work</td><td>managed executor and gated dispatcher</td></tr></tbody></table>
  </section>

  <section>
    <h2>Cross-surface evidence crosses a boundary</h2>
    <div class="flow"><div class="node"><strong>CLI process</strong>mutate</div><div class="arrow">→</div><div class="node"><strong>SQLite</strong>commit</div><div class="arrow">→</div><div class="node"><strong>data_version</strong>invalidate</div><div class="arrow">→</div><div class="node"><strong>GUI / TUI</strong>re-query</div></div>
    <div class="callout">Asserting that two presenters format similar fixtures is not cross-surface proof. Observe the same persisted application state through both adapters.</div>
  </section>

  <section>
    <h2>A repeatable audit</h2>
    <div class="cards four"><div class="card"><div class="number">1</div><h3>Choose difference</h3><p>Add a runtime with a different interaction model.</p></div><div class="card"><div class="number">2</div><h3>Define parity</h3><p>List durable behavior, not screen shapes.</p></div><div class="card"><div class="number">3</div><h3>Route findings</h3><p>Name the owning boundary and add an executable rule.</p></div><div class="card"><div class="number">4</div><h3>Repair inward</h3><p>Improve shared seams, then update every surface.</p></div></div>
  </section>
</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Surfaces 4.4</div><h1>Share behavior, keep views bespoke</h1><p class="lede">Consistency lives in contracts and outcomes, not identical presentation internals.</p><div class="section-no">4.4</div></section>

  <section>
    <h2>Each runtime has a different unit of interaction</h2>
    <div class="cards"><div class="card"><h3>CLI</h3><p>Invocation, flags, stdin, stdout, exit status. State ends when the process ends.</p></div><div class="card"><h3>TUI</h3><p>Messages, commands, focus, terminal cells, key chords, and a continuous update loop.</p></div><div class="card"><h3>GUI</h3><p>Retained controls, pointer and keyboard events, background work, dispatch, and native lifecycle.</p></div></div>
  </section>

  <section>
    <h2>The least common denominator is not neutral</h2>
    <div class="big-statement">A universal view model either leaks one runtime into the others, or erases the affordances that made each runtime useful.</div>
    <div class="ownership"><div><h3>Shared contracts</h3><ul><li>public models</li><li>queries and events</li><li>action meaning</li><li>typed errors</li><li>observable outcomes</li></ul></div><div class="shared"><h3>Application boundary</h3><ul><li>the narrow waist</li><li>durable semantics</li><li>authorization</li><li>transaction ownership</li><li>atomic composition</li></ul></div><div><h3>Bespoke</h3><ul><li>focus and selection</li><li>widget or terminal state</li><li>async request state</li><li>navigation mechanics</li><li>rendering</li></ul></div></div>
  </section>

  <section>
    <h2>Reuse mechanics within a surface</h2>
    <div class="layers"><div class="layer"><strong>CLI toolkit</strong><span>JSON input and output, reflection-based tables</span></div><div class="layer"><strong>TUI toolkit</strong><span>view contracts, list/detail, forms, dialogs, layout</span></div><div class="layer"><strong>GUI toolkit</strong><span>shell, tables, semantic controls, executors, dispatchers</span></div><div class="layer private"><strong>Domain surfaces</strong><span>compose only the matching toolkit with domain workflows</span></div></div>
  </section>

  <section>
    <h2>Reusable does not mean symmetrical</h2>
    <table class="matrix"><thead><tr><th>Toolkit</th><th>Reusable shape</th><th>Why it differs</th></tr></thead><tbody><tr><td>CLI</td><td>encoders, decoders, tables</td><td>one invocation, then exit</td></tr><tr><td>TUI</td><td>autonomous forms, dialogs, and view models</td><td>messages repeatedly advance explicit state</td></tr><tr><td>GUI</td><td>shell, page objects, controls, async coordinators</td><td>widgets persist and callbacks publish state</td></tr></tbody></table>
    <div class="callout">Package shape follows the runtime’s interaction model. Shared application meaning sits below all three.</div>
  </section>

  <section>
    <h2>Cross-cutting does not mean ownerless</h2>
    <div class="flow"><div class="node"><strong>surface</strong>desired tags</div><div class="arrow">→</div><div class="node"><strong>RunTaggedMutation</strong>validate + compose</div><div class="arrow">→</div><div class="node"><strong>domain mutation</strong>owned behavior</div><div class="arrow">+</div><div class="node"><strong>Tags.Replace</strong>owned association</div></div>
    <div class="transaction">domain result + complete tag set = one transaction</div>
    <div class="cards"><div class="card"><h3>Application seam</h3><p>Participates in a caller transaction or opens one shared unit of work.</p></div><div class="card"><h3>Narrow contract</h3><p><code>TaggableEntity</code> exposes only <code>EntityUID</code> and <code>SetTags</code>.</p></div><div class="card"><h3>Bespoke interaction</h3><p>Each surface keeps parsing, confirmation, form state, and feedback native.</p></div></div>
    <div class="callout">Invalid tags never start the mutation. A replacement failure rolls the domain change back with it.</div>
    <p class="source"><a href="/projects/go-modular-monolith/">Adjacent project commentary: atomic tagged mutations</a></p>
  </section>

  <section>
    <h2>Triangulation finds the durable seam</h2>
    <div class="split"><div class="side"><h3>If all three need it</h3><p>It may belong in the application: dashboard aggregation, atomic tagged mutation, action projection.</p></div><div class="bridge">△</div><div class="side"><h3>If only one runtime needs it</h3><p>It probably belongs in that toolkit or surface: cursor history, dialog ownership, terminal layout.</p></div></div>
    <div class="callout">Share meaning. Specialize interaction. Test equality at the application boundary.</div>
  </section>
</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Surfaces 4.5</div><h1>Test native desktop behavior headlessly</h1><p class="lede">Confidence comes from a ladder of distinct evidence, not one giant simulated UI test.</p><div class="section-no">4.5</div></section>

  <section>
    <h2>The evidence ladder</h2>
    <div class="evidence-ladder"><div class="rung">pure state + presenter with fake executor and dispatcher</div><div class="rung">real Fyne controls in the in-memory driver</div><div class="rung">dialogs, composed shell, and close ordering</div><div class="rung">fresh-process and cross-surface behavior</div><div class="rung">race detector and target compilation</div><div class="rung">pixels and manual accessibility evidence</div></div>
  </section>

  <section>
    <h2>Inject execution and publication separately</h2>
    <div class="flow"><div class="node"><strong>Presenter</strong>requests work</div><div class="arrow">→</div><div class="node"><strong>Executor</strong>runs off UI thread</div><div class="arrow">→</div><div class="node"><strong>Dispatcher</strong>returns to UI thread</div><div class="arrow">→</div><div class="node"><strong>View</strong>renders state</div></div>
    <div class="cards two"><div class="card"><h3>Deterministic test</h3><p>Immediate executor and dispatcher expose state transitions without timing guesses.</p></div><div class="card"><h3>Production runtime</h3><p>Managed executor and Fyne dispatcher preserve thread and shutdown ownership.</p></div></div>
  </section>

  <section>
    <h2>Semantic controls carry behavior</h2>
    <div class="cards"><div class="card"><h3>Pointer</h3><p>Button activation reaches the guarded command.</p></div><div class="card"><h3>Keyboard</h3><p>Shortcuts invoke the same enabled control, not a parallel code path.</p></div><div class="card"><h3>Test</h3><p>The control exposes state and behavior without pixel coordinates.</p></div></div>
    <div class="callout">A disabled button, its shortcut, and its command must agree. Semantic controls make that one assertion.</div>
  </section>

  <section>
    <h2>Pixels are different evidence</h2>
    <table class="matrix"><thead><tr><th>Question</th><th>Evidence</th></tr></thead><tbody><tr><td>Did the presenter compute the right state?</td><td>pure model and presenter tests</td></tr><tr><td>Did the widget wire that state correctly?</td><td>virtual window and semantic control tests</td></tr><tr><td>Does the composed process close safely?</td><td>lifecycle and fresh-process tests</td></tr><tr><td>Does it look right?</td><td>targeted screenshots and human review</td></tr><tr><td>Does assistive technology work?</td><td>manual platform protocol, not inferred from pixels</td></tr></tbody></table>
  </section>
</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Surfaces 4.6</div><h1>Project actions, not widgets</h1><p class="lede">Share durable action meaning across interfaces without sharing runtime state.</p><div class="section-no">4.6</div></section>

  <section>
    <h2>Give each state one meaning</h2>
    <div class="cards"><div class="card stop"><h3>Hidden</h3><p>Authorization denied. Do not advertise an operation the actor cannot perform.</p></div><div class="card warn"><h3>Disabled</h3><p>Authorized, but a durable domain prerequisite is unmet. Keep the reason.</p></div><div class="card go"><h3>Enabled</h3><p>Authorized and currently eligible. The command still remains authoritative.</p></div></div>
  </section>

  <section>
    <h2>Declare permission at the right scope</h2>
    <pre><code class="language-go">declaration := actions.Group{
    Permission: actions.Require(canEdit),
    Controls: []actions.Control{
        {ID: "name"},
        {ID: "publish",
         Permission: actions.Require(canPublish),
         Conditions: []actions.Condition{saved, publishable}},
    },
}</code></pre>
    <div class="callout">A group permission is an inherited default, not a permanent decision. Distinct operations override it explicitly.</div>
    <p class="source">Permission runs before conditions, so denial never leaks disabled reasons.</p>
  </section>

  <section>
    <h2>Project once, adapt natively</h2>
    <div class="fanout"><div class="event-source"><strong>Domain projector</strong><span class="small">authorization + durable prerequisites</span></div><div class="event-bus">⇢</div><div class="handler-stack"><div class="handler"><strong>TUI</strong>bindings and help</div><div class="handler"><strong>GUI</strong>buttons, menus, shortcuts</div><div class="handler"><strong>Future web</strong>controls and explanations</div><div class="handler"><strong>Evaluation failure</strong>operational error, never action state</div></div></div>
  </section>

  <section>
    <h2>Projection guides. Commands enforce.</h2>
    <div class="state-line"><div class="state active">load</div><div class="arrow">→</div><div class="state active">authorize + project</div><div class="arrow">→</div><div class="state review">state changes</div><div class="arrow">→</div><div class="state active">command re-checks</div></div>
    <div class="big-statement">A polished control state is not a lock. Current authorization, revision, and invariants are checked inside the write transaction.</div>
  </section>
</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Build path</div><h1>Walk the pressure, not the package tree</h1><p class="lede">Each chapter starts with a decision the business forces, then follows the mechanism that makes it durable.</p><div class="section-no">→</div></section>

  <section>
    <h2>The recording arc</h2>
    <div class="timeline"><div class="step"><strong>Ownership</strong><span>contexts + module contracts</span></div><div class="step"><strong>Protocol</strong><span>types + errors + policy</span></div><div class="step"><strong>Execution</strong><span>pipeline + transactions</span></div><div class="step"><strong>Evidence</strong><span>logs + metrics + audit</span></div><div class="step"><strong>Coordination</strong><span>events + tags + filters</span></div><div class="step"><strong>Pressure</strong><span>degradation + workflows</span></div><div class="step"><strong>Surfaces</strong><span>CLI + TUI + GUI</span></div></div>
  </section>

  <section>
    <h2>Keep one code trace in frame</h2>
    <pre><code class="language-text">main/&lt;surface&gt;
  → app/domains/&lt;domain&gt;/surfaces/&lt;surface&gt;
  → app/domains/&lt;domain&gt;/module.go
  → queries/ or internal/commands/
  → middleware pipeline
  → dispatcher + audit
  → store transaction</code></pre>
    <div class="callout">Return to this trace whenever a mechanism feels abstract. The architecture is a path a real operation takes.</div>
  </section>

  <section class="centered">
    <div class="eyebrow">The destination</div>
    <h1>One application.<br>Many honest boundaries.</h1>
    <p class="lede">The monolith is the deployment choice. Modularity is the behavior we keep proving.</p>
    <p class="source">github.com/TheFellow/go-modular-monolith · thefellow.github.io/series/mixology/</p>
  </section>
</section>
