---
title: "Building Mixology: The Slide Deck"
date: 2026-09-05
last_modified_at: 2026-09-06
permalink: /talks/building-mixology/
excerpt: "A visual walkthrough of the foundational domain, module, middleware, event, audit, tagging, filtering, persistence, and presentation choices behind go-modular-monolith."
layout: deck
author_profile: false
search: false
---

<section class="centered title-slide">
  <div class="eyebrow">Building Mixology</div>
  <h1>Building a modular monolith in Go</h1>
  <p class="lede">A cocktail bar application with seven business owners, three interfaces, and tests that keep their boundaries intact.</p>
  <div class="chapter-path"><span>← / → chapter</span><span>↑ / ↓ detail</span><span><b>S</b> speaker view</span><span><b>Esc</b> map</span></div>
  <aside class="notes">This is the backing presentation for peers at staff/principal level who are comfortable in Go and new to this modular-monolith design. Each horizontal chapter is a recording unit; vertical slides move from the design decision into concrete types, execution paths, and adversarial tests. Snippets identify their source and label omitted or illustrative code. The goal is to explain where a change belongs, why it belongs there, and how to prove it works. Explain the current design through its responsibilities and tradeoffs, without requiring knowledge of earlier implementations. Procurement is an optional future workshop. Code links pin the reviewed repository snapshot 635c59b from go-modular-monolith PR #62; use that revision for reproducible demonstrations.</aside>
</section>

<section>
  <section class="centered section-slide">
    <div class="eyebrow">Orientation</div>
    <h1>Why this application exists</h1>
    <p class="lede">Architecture is the set of changes the codebase makes easy, and the shortcuts it refuses.</p>
    <div class="section-no">00</div>
  </section>

  <section>
    <h2>Why a cocktail bar makes a useful teaching repo</h2>
    <div class="cards"><div class="card"><h3>Understandable business</h3><p>Ingredients make drinks. Menus offer drinks. Orders reserve and consume ingredients.</p></div><div class="card"><h3>Connected decisions</h3><p>A stock correction can block an order. Retiring an ingredient can require recipe review and change menu availability.</p></div><div class="card"><h3>Visible consequences</h3><p>The CLI, TUI, and GUI must agree about state, permission, failure, and what committed.</p></div></div>
    <div class="callout">I chose a small business model with enough interaction to make ownership and consistency problems unavoidable.</div>
    <aside class="notes">Begin with a customer ordering a cocktail, then discover that the stock count was wrong. Ask what the system must preserve: the accepted order, the reservation, an honest availability indicator, and the identity of the person who corrected stock. These requirements motivate the architecture throughout the series. The opinion here is that explicit owners and one consistent operation path make this complexity easier to change.</aside>
  </section>

  <section>
    <h2>What “modular monolith” means here</h2>
    <div class="split"><div class="side"><h3>Monolith</h3><p>The domains run together in a Go process and collaborate through ordinary calls. Related writes can share one SQLite transaction.</p></div><div class="bridge">+</div><div class="side"><h3>Modular</h3><p>Each domain owns its decisions and storage. Other domains use its public read contracts and events.</p></div></div>
    <div class="callout">CLI, TUI, and GUI are separate executables built around the same application. They can run together against one database file on the same machine.</div>
    <aside class="notes">A bounded context is an owner of business language and rules. A module is the Go package structure implementing that ownership. Neither means a separately deployed service or a Go module with its own go.mod. Shared storage makes atomic collaboration practical; it does not grant permission to import a neighbor's DAO. This is the central tradeoff: coordinated deployment and a shared transaction in exchange for explicit package discipline.</aside>
  </section>

  <section>
    <h2>Turn ownership into checks</h2>
    <div class="split">
      <div class="side"><h3>A package diagram</h3><p>Shows the intended dependency direction.</p><p class="muted">It cannot stop the next convenient import.</p></div>
      <div class="bridge">≠</div>
      <div class="side"><h3>An executable boundary</h3><p>Makes ownership visible in APIs, types, transactions, generators, tests, and import rules.</p><p class="accent">The shortest wrong path fails.</p></div>
    </div>
    <div class="callout">The reference application is a cocktail bar because inventory, recipes, menus, and orders create real pressure between domains.</div>
  </section>

  <section>
    <h2>Seven business owners</h2>
    <div class="domain-map">
      <svg class="domain-lines" viewBox="0 0 1000 450" aria-hidden="true"><defs><marker id="arrowhead" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><polygon points="0 0, 7 3.5, 0 7" fill="#63e6be"/></marker></defs><line x1="320" y1="90" x2="180" y2="220"/><line x1="320" y1="350" x2="180" y2="230"/><line x1="570" y1="90" x2="390" y2="90"/><line x1="790" y1="200" x2="630" y2="90"/><line x1="180" y1="220" x2="570" y2="90" class="event"/><line x1="180" y1="230" x2="790" y2="220" class="event"/><line x1="390" y1="350" x2="790" y2="230" class="event"/><line x1="790" y1="245" x2="390" y2="350" class="event"/></svg>
      <div class="domain ingredients">Ingredients<small>catalog + retirement</small></div><div class="domain drinks">Drinks<small>recipes</small></div><div class="domain inventory">Inventory<small>stock</small></div><div class="domain menus">Menus<small>curation + publication</small></div><div class="domain orders">Orders<small>lifecycle</small></div><div class="domain audit">Audit<small>append-only activity</small></div><div class="domain tagging">Tagging<small>associations</small></div>
    </div>
    <div class="legend"><span><i></i> caller → public query owner</span><span><i class="event"></i> event owner ⇢ reacting owner</span></div>
    <p class="source">Selected collaborations; Audit and Tagging connections omitted.</p>
    <aside class="notes">Use this as an orientation map, not a complete dependency graph. Ingredients owns the catalog, Drinks owns recipes, Inventory owns quantities and reservations, Menus owns curation and publication, and Orders owns accepted orders. Audit and Tagging have different responsibilities and smaller module shapes. Read docs/architecture.md for the complete synchronous dependency table. The arrows show information flow, not network calls.</aside>
  </section>

  <section>
    <h2>Find the owner of an operation</h2>
    <div class="flow">
      <div class="node"><strong>main/&lt;surface&gt;</strong>process composition</div><div class="arrow">→</div>
      <div class="node"><strong>surfaces/&lt;surface&gt;</strong>domain presentation</div><div class="arrow">→</div>
      <div class="node"><strong>domain root</strong>facade + pipeline</div><div class="arrow">→</div>
      <div class="node"><strong>queries / internal</strong>behavior + storage</div>
    </div>
    <div class="cards three">
      <div class="card"><h3>CLI</h3><p>One command, one fresh operation context.</p></div><div class="card"><h3>Bubble Tea TUI</h3><p>Persistent session, message-driven presentation.</p></div><div class="card"><h3>Fyne GUI</h3><p>Retained native widgets and managed lifecycle.</p></div>
    </div>
    <div class="callout">All three enter the same application behavior and local SQLite database. Views are adapters, not alternate applications.</div>
    <aside class="notes">A surface is this repository's name for an interface adapter. main composes the process; the domain's surface parses input and renders output; the public facade selects a pipeline method; the pipeline invokes a query or command. module.go constructs the facade, while methods also live in files such as orders/place.go. A DAO is the private data access object that maps between domain values and stored rows.</aside>
  </section>

  <section>
    <h2>Start by running and reading one list</h2>
    <pre><code class="language-sh"># From go-modular-monolith, with Go 1.27.1+
go run ./main/seed
go run ./main/cli ingredients list --limit 5 --json
go run ./main/cli ingredients list --filter-help
go run ./main/cli --actor bartender menus list
go run ./main/tui</code></pre>
    <div class="callout">Start with sample data and one visible result. Then follow the same list from its CLI adapter to the module, query, DAO, and authorization step.</div>
    <aside class="notes">Use a fresh demo database for recording and prepare seeded data before the take. Current domain-schema changes require fresh seed data: they do not migrate older order snapshots or backfill historical acceptance. The default file is data/mixology.db; set MIXOLOGY_DB to a separate new path in the recording shell to preserve an existing database. The seed executable inserts fixtures, not an in-place historical upgrade. Open README.md for the repository map and main/gui/README.md before running the desktop client, which has native build prerequisites. Actor selection is a demo persona mechanism; authn provides identity and Cedar decides permissions.</aside>
  </section>

  <section>
    <h2>The route through the series</h2>
    <table class="matrix"><thead><tr><th>Chapters</th><th>Question we will answer</th></tr></thead><tbody><tr><td>1.1–1.8 · foundations</td><td>Who owns a change, and what happens on every operation?</td></tr><tr><td>2.1–2.4 · collaboration</td><td>How do events, tags, filters, and storage preserve those rules?</td></tr><tr><td>3.1a–d · business walkthroughs</td><td>What happens when stock, recipes, and accepted orders disagree?</td></tr><tr><td>4.0–4.6 · interfaces</td><td>How do three runtimes expose the same application correctly?</td></tr><tr><td>3.2 · optional future workshop</td><td>What would a Procurement workflow add?</td></tr></tbody></table>
    <div class="callout">This is a teaching order through today's application. Each chapter connects a business problem to code, a design choice, and a test.</div>
    <aside class="notes">Record each chapter around current behavior: demonstrate an operation, trace its implementation, explain the responsibility or failure mode that motivates the design, and inspect the test that protects it. Authorization has three recording units: 1.6a covers Cedar and policy data, 1.6b covers command state transitions, and 1.6c covers fine-grained disclosure. Chapters 2.3, 2.4, 3.1, and 4.2 each pair an application walkthrough (a) with an implementation deep dive (b): filter correctness, cross-process persistence, shared-stock allocation, and GUI lifecycle. Skip the explicitly planned Procurement chapter on the initial onboarding pass. The closing chapter includes an exercise for making a change in the existing application.</aside>
  </section>
</section>

<section>
  <section class="centered section-slide">
    <div class="eyebrow">Foundation 1.1</div><h1>Shape modules around business ownership</h1>
    <p class="lede">A modular monolith begins with decisions, language, and collaboration contracts, not a folder template.</p><div class="section-no">1.1</div>
  </section>

  <section>
    <h2>Give each business decision one owner</h2>
    <div class="layers">
      <div class="layer"><strong>Public facade</strong><span><code>app/domains/drinks</code> composes and exposes supported behavior.</span></div>
      <div class="layer"><strong>Public contracts</strong><span><code>models</code>, <code>queries</code>, and <code>events</code> are explicit collaboration contracts.</span></div>
      <div class="layer"><strong>Event handlers</strong><span><code>handlers</code> consume public facts and mutate only their owning domain.</span></div>
      <div class="layer private"><strong>Private work</strong><span><code>internal/commands</code> and <code>internal/dao</code> remain implementation details.</span></div>
    </div>
    <div class="big-statement">If a neighboring domain can import the command that “just does the thing,” ownership is only a suggestion.</div>
  </section>

  <section>
    <h2>Seven contexts, three module profiles</h2>
    <table class="matrix"><thead><tr><th>Profile</th><th>Contexts</th><th>Why it exists</th></tr></thead><tbody><tr><td>Operational</td><td>Ingredients, Drinks, Inventory, Menus, Orders</td><td>business state, commands, queries, events, persistence, policy</td></tr><tr><td>Activity</td><td>Audit</td><td>append-only evidence written by the operation pipeline</td></tr><tr><td>Cross-cutting domain</td><td>Tagging</td><td>owned associations over registered operational targets</td></tr></tbody></table>
    <div class="callout">Consistency does not require identical package trees. Audit and Tagging use smaller profiles because their responsibilities differ.</div>
  </section>

  <section>
    <h2>Public does not mean interchangeable</h2>
    <div class="split"><div class="side"><h3>Application caller</h3><p>A surface calls <code>Orders.Place</code> on the public module. The module enters the pipeline that authorizes, executes, and audits the operation.</p></div><div class="bridge">∥</div><div class="side"><h3>Collaborating domain</h3><p>Orders reads a published menu through public query contracts. Inventory reacts to <code>OrderPlaced</code> through its own handler.</p></div></div>
    <div class="callout">A public query package supports internal collaboration. It does not itself promise the authorized application boundary supplied by the module facade.</div>
    <aside class="notes">Open orders/module.go, orders/place.go, and orders/internal/commands/place.go together. NewModule wires dependencies; Place chooses pipeline.Command; the private command validates the menu and captures ingredient usage. Peer queries reuse the current transaction and answer business questions without starting a second user operation. This is why surfaces go through modules and why a handler cannot import another module or command.</aside>
  </section>

  <section>
    <h2>Composition is ordinary, visible Go</h2>
    <div class="timeline"><div class="step"><strong>Foundation</strong><span>Audit + Tagging schemas</span></div><div class="step"><strong>Ports</strong><span>tag repository + empty registry</span></div><div class="step"><strong>Evidence</strong><span>separate audit writer</span></div><div class="step"><strong>Pipeline</strong><span>dispatcher + writer callback</span></div><div class="step"><strong>Operational modules</strong><span>rows + tag targets</span></div><div class="step"><strong>Public facades</strong><span>Tagging + Audit</span></div></div>
    <div class="cards two"><div class="card"><h3>No import side effects</h3><p>Private SQLite rows register during construction. Invalid or missing registration fails at startup or in architecture tests.</p></div><div class="card"><h3>No second manifest</h3><p><code>TestEveryDomainIsComposed</code> treats domain directories as the source of truth and verifies <code>app.New</code>.</p></div></div>
    <div class="callout">The private Audit writer exists before the public Audit facade, breaking the construction cycle between pipeline activity and authorized audit reads.</div>
    <aside class="notes">Code walk: app/app.go. The pipeline needs a callback that writes activities, while the public Audit module needs the pipeline to authorize reads. Constructing the writer separately resolves that dependency directly. Likewise, Tagging's registry starts empty; operational modules register their own loaders before the public tagging workflow is exposed. These are constructor dependencies that can be inspected in one function.</aside>
  </section>

  <section>
    <h2>Application state is not request state</h2>
    <div class="split"><div class="side"><h3><code>App</code></h3><p>Store and public modules whose private composition retains the configured pipeline. No actor identity.</p></div><div class="bridge">+</div><div class="side"><h3><code>Session</code></h3><p>Binds a persistent TUI or GUI to an authenticated base context, then creates a fresh operation context every time.</p></div></div>
    <div class="flow"><div class="node"><strong>base context</strong>actor + logger + metrics</div><div class="arrow">→</div><div class="node"><strong><code>Session.Context()</code></strong>fresh mutable state</div><div class="arrow">→</div><div class="node"><strong>operation</strong>events + activity + attributes</div><div class="arrow">→</div><div class="node"><strong>discard</strong>nothing leaks forward</div></div>
    <div class="callout">The CLI starts fresh per invocation. Persistent clients reuse authentication, never accumulated operation state.</div>
    <aside class="notes">Open app/session.go and pkg/middleware/context.go. The stable context supplies cancellation, actor, and logging. Each operation has a separate event accumulator, activity, and log attributes. Chain.Execute also isolates mutable state for each command when several commands share a caller-owned transaction. Otherwise, a later click could inherit an earlier event or audit resource.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Construct the dependency graph in one place</h2>
    <pre><code class="language-go">tags := tagging.NewRepository(s)
targets := tagging.NewRegistry()
auditWriter := audit.NewWriter(s)
pipeline := middleware.NewPipeline(middleware.PipelineConfig{
    Store:          s,
    Dispatcher:     dispatcher.New(s, tags),
    Metrics:        telemetry.FromContext(ctx),
    RecordActivity: auditWriter.RecordActivity,
})
ingredientsModule := ingredients.NewModule(
    ctx, s, tags, targets, pipeline,
)</code></pre>
    <div class="callout">The pipeline receives an audit-writing capability. The public Audit module is constructed later with that same pipeline.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/app.go">Code: app/app.go</a></p>
    <aside class="notes">Excerpt from app.New after schema registration. Follow NewModule into its private DAO, peer queries, and tag registration. There is no runtime service locator: the dependencies are visible in constructor parameters. The application owns this graph; the session adds actor context without rebuilding it.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Copy operation state, retain transaction identity</h2>
    <pre><code class="language-go">func (c *Context) forOperation() *Context {
    derived := *c
    derived.Context = c.Context
    derived.events = make([]any, 0, 4)
    derived.activity = nil
    return &amp;derived
}</code></pre>
    <div class="callout">The principal and optional transaction survive the copy. The event slice and activity do not: two commands can share a commit without sharing an operation.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/middleware/context.go">Code: pkg/middleware/context.go</a></p>
    <aside class="notes">Exact method. Follow Chain.Execute to its final next(ctx.forOperation()) call. Then inspect WithTransaction: it starts another event slice but preserves the activity pointer, so handler touches and successful recording belong to the originating command. This distinction is easy to miss when reading shallow copies.</aside>
  </section>

</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Foundation 1.2</div><h1>Use types to prevent easy mistakes</h1><p class="lede">An invariant is a rule that must remain true. Types enforce some rules; validation and transactions enforce the rest.</p><div class="section-no">1.2</div><aside class="notes">Compare passing an OrderID where a DrinkID is required with requesting more stock than is available. The compiler can reject the first. The second requires current business state inside a transaction. This chapter explains where each guarantee belongs.</aside></section>

  <section>
    <h2>Let types carry the distinctions they can</h2>
    <div class="cards">
      <div class="card"><h3>Generated entity IDs</h3><p><code>DrinkID</code> and <code>IngredientID</code> share the same generated Cedar method shape without becoming interchangeable parameters.</p></div>
      <div class="card"><h3>Closed amount variants</h3><p>An unexported <code>isAmount</code> method limits <code>Amount</code> to volume and discrete quantities owned by the kernel.</p></div>
      <div class="card"><h3>Validated values</h3><p>Currency, price, quantity, and tag parsers turn accepted external text into domain-shaped values.</p></div>
    </div>
    <div class="callout">Go still permits zero values and package-local construction. Constructors, decoding validation, and boundary checks carry the guarantees the type system cannot.</div>
    <aside class="notes">Code walk: app/kernel/readme.md and app/kernel/entity. Generated IDs share parsing, JSON, prefixes, and Cedar identity but stay distinct Go types. Cedar is the policy language used by the application; an entity UID identifies the resource being authorized. For quantities, dimensional validation matters too: a recipe cannot silently replace milliliters with a count of items.</aside>
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
    <div class="big-statement">Use types to preserve meaning, then validate values read from input or storage.</div>
  </section>

  <section>
    <h2>Capability types remove forbidden moves</h2>
    <div class="split"><div class="side"><h3><code>middleware.Context</code></h3><p>Transaction, principal, activity, <code>AddEvent</code>, and <code>TouchEntity</code>.</p><p class="accent">Commands may originate owned facts.</p></div><div class="bridge">⊃</div><div class="side"><h3><code>HandlerContext</code></h3><p>Transaction, principal, and <code>TouchEntity</code>. No event accumulator.</p><p class="gold">Reactions cannot cascade.</p></div></div>
    <div class="callout">The most reliable prohibition is an API that cannot express the forbidden operation.</div>
  </section>
  <section class="implementation-slide">
    <h2>The ID is a defined type, with generated behavior</h2>
    <pre><code class="language-go">type DrinkID cedar.EntityUID

func ParseDrinkID(id string) (DrinkID, error) {
    uid, err := parseID(TypeDrink, PrefixDrink, id)
    return DrinkID(uid), err
}
func (id DrinkID) EntityUID() cedar.EntityUID {
    return cedar.EntityUID(id)
}
func (id DrinkID) String() string {
    return string(cedar.EntityUID(id).ID)
}</code></pre>
    <div class="callout">Domain signatures retain DrinkID. Conversion to Cedar is explicit at the policy boundary; parsing validates external IDs at entry.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/kernel/entity/entities_gen.go">Code: app/kernel/entity/entities_gen.go</a></p>
    <aside class="notes">Selected generated methods. Compare IngredientID beside this code: identical mechanics, distinct parameter types. A Go type conversion can still be written deliberately; the guarantee is against accidental interchange, not a security boundary. Show the generator input and the ID parsing tests before navigating to the next type.</aside>
  </section>

  <section class="implementation-slide">
    <h2>A closed variant still needs runtime validation</h2>
    <pre><code class="language-go">// Selected Amount methods.
type Amount interface {
    Unit() Unit
    Value() float64
    Add(Amount) (Amount, error)
    Convert(Unit) (Amount, error)
    isAmount()
}

// Executable example.
volume := measurement.MustAmount(30, measurement.UnitMl)
pieces := measurement.MustAmount(1, measurement.UnitPiece)
_, err := volume.Add(pieces)
// Invalid: "unit mismatch: ml vs piece"</code></pre>
    <div class="callout">The unexported marker controls direct implementations. Add and Convert enforce dimensional compatibility between valid variants.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/kernel/measurement/amount.go">Code: app/kernel/measurement/amount.go</a></p>
    <aside class="notes">The interface is abbreviated; the executable statements use the actual package. MustAmount is appropriate for known-good fixture literals, while NewAmount returns errors for external values. Open VolumeAmount.Add to see its type switch and typed Invalid result. A nil interface, zero value, or embedded implementation still requires ordinary Go reasoning; this is not a proof of every numeric invariant.</aside>
  </section>


  <section class="implementation-slide">
    <h2>Represent physical quantity separately from display units</h2>
    <pre><code class="language-go">type Volume struct { ml float64 }
type Quantity struct {
    Volume Volume
    Unit   Unit // preferred display unit
}

// Convert retains the same Volume; it changes the display unit.
q := measurement.MustQuantity(1, measurement.UnitOz)
ml, _ := q.Convert(measurement.UnitMl)
q.Value()  // 1
ml.Value() // 29.5735

// Pieces, dashes, and splashes cannot convert to liquid volume.</code></pre>
    <div class="callout">Amounts prevent dimensional mistakes. They do not make floating-point arithmetic exact or enforce every business quantity constraint.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/kernel/measurement/quantity.go">Code: app/kernel/measurement/quantity.go</a></p>
    <aside class="notes">Selected declarations and an illustrative conversion using the current constant. Add/Sub operate on normalized volume and preserve the left operand's display unit. DiscreteQuantity retains its own unit and also uses float64; discrete does not imply integer-only validation. Nonnegative stock, positive recipe amounts, and acceptable scaling belong to domain validation. Follow this representation into fulfillment's unit conversion before comparing availability.</aside>
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
  "Inventory is unavailable",
)</code></pre><p>Internal detail is generic unless explicitly made safe.</p></div></div>
    <div class="callout">Unknown errors do not inherit this safety guarantee. Classify unexpected failures before a presentation boundary.</div>
    <aside class="notes">Code walk: pkg/errors/README.md, then a command returning FailedPrecondition and a DAO returning Conflict. These kinds tell callers whether to fix input, reload state, or resolve a prerequisite. The diagnostic cause is for logs; UserMessage is for the person using the application. Keeping both avoids exposing database details or losing the information needed to debug a failure.</aside>
  </section>

  <section>
    <h2>Generate the repetitive family, enforce one vocabulary</h2>
    <div class="cards"><div class="card"><h3>Generated</h3><p>Typed constructors, classifiers, metadata, and matching test assertions.</p></div><div class="card"><h3>Wrapped</h3><p><code>%w</code>, <code>Is</code>, and <code>As</code> preserve semantic inspection through context.</p></div><div class="card"><h3>Enforced</h3><p><code>arch-lint</code> rejects direct standard-library <code>errors</code> imports outside <code>pkg/errors</code>.</p></div></div>
    <div class="big-statement">Contextual wrappers preserve discoverable error meaning. A new typed wrapper deliberately changes the outer classification.</div>
  </section>
  <section class="implementation-slide">
    <h2>Two types separate classification from payload</h2>
    <pre><code class="language-go">// Shared payload (error.go).
type Error struct {
    kind        Kind
    detail      string
    userMessage string
    cause       error
}

// Generated wrapper (errors_gen.go).
type InternalError struct { err *Error }

func Internalf(format string, args ...any) *InternalError {
    return &amp;InternalError{err: newErrorf(KindInternal, format, args...)}
}</code></pre>
    <div class="callout">InternalError identifies the failure family. Error carries the immutable kind, diagnostic detail, safe override, and one wrapped cause.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/errors/errors_gen.go">Code: pkg/errors/errors_gen.go</a></p>
    <aside class="notes">Selected declarations. newErrorf uses fmt.Errorf to format detail and standard errors.Unwrap to retain a single cause. It does not capture runtime PCs or a stack trace. Avoid treating multiple %w operands as the same contract; this constructor stores one cause. Generated methods supply Kind, UserMessage, ExitCode, and the custom As bridge.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Build one failure and let the real evaluator wrap it</h2>
    <pre><code class="language-go">{% raw %}// Injected failure; the evaluator and wrapping are real.
cause := errors.New("database is locked")
failure := errors.Internalf("load readiness: %w", cause).
    WithUserMessage("Readiness is temporarily unavailable")

_, err := actions.Evaluate(ctx, actions.Group{
    Permission: actions.Public(),
    Controls: []actions.Control{{ID: "publish",
        Conditions: []actions.Condition{
            func(context.Context) (bool, string, error) {
                return false, "", failure
            },
        },
    }},
}){% endraw %}</code></pre>
    <div class="callout">The condition returns a typed error. evaluateControl adds the condition index; evaluateGroup adds the control ID. Neither layer needs a CLI or GUI type.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/presentation/actions/actions.go">Code: pkg/presentation/actions/actions.go</a></p>
    <aside class="notes">Runnable illustration using the repository APIs, with an injected dependency failure rather than a real database lock. Imports are context, pkg/errors, and pkg/presentation/actions; ctx is context.Background(). Keep this example open for the next three slides. This call was executed to verify the exact chain and surface outputs.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Read the complete error chain</h2>
    <pre><code class="language-text">Evaluate → evaluateGroup → evaluateControl → condition
                                               ↓
*fmt.wrapError
  actions: control "publish": condition 0:
    load readiness: database is locked
  └─ *fmt.wrapError
       condition 0: load readiness: database is locked
       └─ *errors.InternalError
            load readiness: database is locked
            └─ *errors.errorString
                 database is locked</code></pre>
    <div class="callout">This is a causal wrapping chain, not a captured Go runtime stack. Error() includes every added prefix; Unwrap preserves the path to the original cause.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/presentation/actions/actions.go">Code: pkg/presentation/actions/actions.go</a></p>
    <aside class="notes">The repository wrappers are fmt.Errorf("condition %d: %w", i, err) and fmt.Errorf("actions: control %q: %w", control.ID, err). The tree is the observed chain from the previous example; diagnostic lines are wrapped here for slide width. InternalError.Unwrap delegates directly to its underlying cause rather than exposing the shared Error as another chain node.</aside>
  </section>

  <section class="implementation-slide">
    <h2>As reaches both the typed wrapper and shared payload</h2>
    <pre><code class="language-go">var typed *errors.InternalError
var payload *errors.Error

errors.As(err, &amp;typed)   // true
errors.As(err, &amp;payload) // true: generated As method
errors.Is(err, cause)    // true: same original cause
payload.Kind()          // KindInternal
payload.UserMessage()   // "Readiness is temporarily unavailable"

// The generated bridge, abbreviated:
if p, ok := target.(**Error); ok {
    *p = e.err
    return true
}</code></pre>
    <div class="callout">A domain caller can classify the concrete failure. A generic adapter can extract the common payload without switching over six wrapper types.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/errors/errors_gen.go">Code: pkg/errors/errors_gen.go</a></p>
    <aside class="notes">As walks through both fmt wrappers and calls InternalError.As. The shared payload is reachable even though it is not an Unwrap node. No string matching is required. These results were checked against the real package; use errors.Is for a particular sentinel and the generated IsInternal helper for the typed family.</aside>
  </section>

  <section class="implementation-slide">
    <h2>The same failure has different diagnostic and UI output</h2>
    <pre><code class="language-text">Diagnostic Error():
  actions: control "publish": condition 0:
  load readiness: database is locked

CLI: exit code 50
  Readiness is temporarily unavailable

TUI: style "error", original cause retained
  Readiness is temporarily unavailable

Without WithUserMessage:
  internal error</code></pre>
    <div class="callout">The safe message comes from the classified payload, so outer diagnostic prefixes do not leak into CLI or TUI output.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/errors/cli.go">Code: pkg/errors/cli.go</a></p>
    <aside class="notes">Observed from ToCLIExit and ToTUIError using the previous example. ToCLIExit creates a terminal cli.Exit value with a message and code; ToTUIError also retains Err for diagnostics. Perform semantic inspection before converting to a terminal CLI result. The GUI uses the same classification through PresentError.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Choose where to preserve, translate, or classify</h2>
    <pre><code class="language-go">// Current store mapping, selected branches.
if errors.IsConflict(err) || isUniqueConstraint(err) {
    return errors.Conflictf(format, args...)
}
return errors.Internalf(format+": %w", append(args, err)...)

// Adding context without changing a known kind:
return fmt.Errorf("publish menu: %w", err)

// Unknown errors have no automatic safe-message guarantee.
errors.ToCLIExit(errors.New("raw dependency detail"))
// exit 1, message "raw dependency detail"</code></pre>
    <div class="callout">Expected store failures become domain-facing kinds. Unexpected failures retain their cause under Internal. A new typed wrapper is a semantic decision, not routine decoration.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/store/errors.go">Code: pkg/store/errors.go</a></p>
    <aside class="notes">MapError intentionally replaces the message for expected NotFound, Conflict, and Invalid branches; those branches do not preserve the incoming cause. The Internal branch does. Wrapping a Conflict inside Internal leaves both types discoverable in the chain, while a generic payload lookup finds the outer classification. Explain this before asserting that an immutable kind means no layer can ever reclassify a failure. The policy is to preserve existing meaning unless a boundary deliberately changes it.</aside>
  </section>

</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Foundation 1.4</div><h1>Give every operation one trustworthy path</h1><p class="lede">Commands and queries should state intent while the pipeline owns the guarantees around them.</p><div class="section-no">1.4</div></section>

  <section>
    <h2>One path for application commands</h2>
    <div class="pipeline">
      <div class="pipe">SerializeTransaction</div><div class="pipe">Logging + Metrics</div><div class="pipe">TrackActivity</div><div class="pipe tx">UnitOfWork begins</div><div class="pipe">load → authorize → handle → authorize result</div><div class="pipe">dispatch events → record success</div><div class="pipe tx">commit everything, or nothing</div>
    </div>
    <div class="callout">A unit of work is the transaction containing one command and its reactions. Queries use a smaller chain: serialization, logging, metrics, and authorization.</div>
    <aside class="notes">Open pkg/middleware/README.md beside the pipeline construction. This is runtime completion order, not declaration order. NewChain nests middleware outside-in; work after next returns unwinds inside-out. SerializeTransaction coordinates operations sharing a caller-owned transaction, while SQLite coordinates separate database writers. Queries do not create command activity or dispatch events.</aside>
  </section>

  <section>
    <h2>Six typed entries, one middleware model</h2>
    <div class="cards">
      <div class="card"><h3><code>Query</code></h3><p>Load a Cedar entity, then authorize the result.</p></div><div class="card"><h3><code>QueryResource</code></h3><p>Authorize a known resource around a non-entity result.</p></div><div class="card"><h3><code>PageQuery</code></h3><p>Fill a page with authorized rows without leaking denied ones.</p></div>
      <div class="card"><h3><code>Command</code></h3><p>Authorize caller input and resulting state.</p></div><div class="card"><h3><code>LoadCommand</code></h3><p>Load trusted state inside the transaction.</p></div><div class="card"><h3><code>LoadCommandActions</code></h3><p>Derive transition-specific action requirements from loaded state.</p></div>
    </div>
    <div class="callout">Choose the method by the operation's input and authorization needs. The shared pipeline still owns transaction and failure behavior.</div>
    <aside class="notes">Open orders/place.go to see a facade select Command, then menus/publish.go for LoadCommand. The distinction is where trusted authorization state comes from. Query authorizes a returned entity; QueryResource authorizes a separate known resource before executing its query; PageQuery authorizes each visible row. LoadCommand loads trusted state first. LoadCommandActions is used for tag replacement because adding and removing tags require different actions.</aside>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/middleware/README.md">Code guide: pkg/middleware/README.md</a></p>
  </section>

  <section>
    <h2>The chain runs inward, then proves the result outward</h2>
    <div class="split"><div class="side"><h3>Enter</h3><p>Serialize, enrich logs, start metrics and activity, open the unit of work, load trusted state, authorize, handle.</p></div><div class="bridge">↩</div><div class="side"><h3>Unwind</h3><p>Authorize result, dispatch facts, record successful activity, commit, observe final duration and error.</p></div></div>
    <div class="callout">Declaration order and completion order differ. Moving one middleware can move work outside the transaction or hide an unwind failure from telemetry.</div>
  </section>

  <section>
    <h2>Commit the command and its reactions together</h2>
    <div class="transaction">domain mutation + prepared event reactions + touched entities + successful audit</div>
    <div class="split"><div class="side"><h3>Success</h3><p>Every write and the durable activity record commit together.</p><p class="accent">One business operation.</p></div><div class="bridge">or</div><div class="side"><h3>Any failure</h3><p>Result authorization, handler, audit, or storage error rolls the complete write graph back.</p><p class="gold">No partial truth.</p></div></div>
    <div class="callout">A caller-supplied transaction retains commit and rollback ownership. Ordinary domain calls use the middleware-managed SQLite transaction.</div>
    <aside class="notes">Inserting an Order is not success if Inventory cannot reserve every required ingredient. A later handler or audit failure must undo the earlier writes. Open pkg/middleware/command_tx_test.go for rollback examples. Atomicity has a cost: all handlers run before commit and extend the write transaction. Keep this path bounded and free of user interaction.</aside>
  </section>

  <section>
    <h2>Load trusted state inside the transaction</h2>
    <div class="flow"><div class="node"><strong>ID + intent</strong>small request</div><div class="arrow">→</div><div class="node"><strong><code>LoadCommand</code></strong>current persisted value</div><div class="arrow">→</div><div class="node"><strong>authorize</strong>before + after</div><div class="arrow">→</div><div class="node"><strong>commit</strong>revision still current</div></div>
    <div class="cards two"><div class="card"><h3>Trusted input state</h3><p>Authority over the existing resource comes from persisted state, not attributes supplied by the caller.</p></div><div class="card"><h3>Authorized result state</h3><p>The actual result must also satisfy policy. A denial rolls back the mutation before event dispatch or commit.</p></div></div>
    <aside class="notes">This is the execution overview. Chapters 1.6a–1.6c develop the authorization model in depth: Cedar vocabulary, the two state boundaries, tag-derived grants, and disclosure. In 1.6b, follow the sommelier category policy through Drinks.Update and a result-denial rollback probe. Input and result authorization are independent security requirements, not duplicate checks.</aside>
  </section>

  <section class="implementation-slide">
    <h2>The actual command chain is nested function calls</h2>
    <pre><code class="language-go">command: NewChain(
    SerializeTransaction(),
    Logging(),
    Metrics(config.Metrics),
    TrackActivity(config.Store, config.RecordActivity),
    UnitOfWork(config.Store),
    recordSuccessfulActivity(config.RecordActivity),
    DispatchEvents(config.Dispatcher),
)</code></pre>
    <div class="callout">Enter top to bottom; unwind bottom to top. Dispatch and successful audit complete before UnitOfWork returns and commits.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/middleware/chains.go">Code: pkg/middleware/chains.go</a></p>
    <aside class="notes">Exact chain from NewPipeline. Put the code next to its stack in the earlier slide. Next is a function, not a queue. Every after-next branch can change the final error, so logging and metrics stay outside the transaction. UnitOfWork joins an injected transaction or calls Store.Write; it does not silently commit a caller's transaction.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Publish authorizes persisted state, then the result</h2>
    <pre><code class="language-go">func (m *Module) Publish(
    ctx *middleware.Context, menu *models.Menu,
) (*models.Menu, error) {
    return m.pipeline.LoadCommand(ctx, authz.ActionPublish,
        func(ctx *middleware.Context) (*models.Menu, error) {
            return m.queries.Get(ctx, menu.ID)
        },
        m.commands.Publish,
    )
}</code></pre>
    <div class="callout">The submitted ID selects the resource. Its current fields are loaded inside the transaction before authorization; the returned entity is authorized again before dispatch.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/menus/publish.go">Code: app/domains/menus/publish.go</a></p>
    <aside class="notes">Exact facade with a reflowed signature. In run.go, trace load → actions → authorizeCommandActions → handler → result authorization. The returned Go value alone is not proof of success: a later dispatch, audit, or commit error can still invalidate the operation. Callers must check err before using the result.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Inject a late failure and inspect what persisted</h2>
    <pre><code class="language-go">// Selected recorder branches from the rollback test.
recordCalls++
if !activity.Success {
    return insertTransactionProbe(ctx, "failure-audit")
}
if err := insertTransactionProbe(ctx, "success-audit"); err != nil {
    return err
}
return errors.Internalf("audit unavailable")

// After the pipeline call that also inserted "business-write":
testutil.Equals(t, recordCalls, 2)
testutil.Equals(t, transactionProbeKinds(t, ctx, s),
    []string{"failure-audit"})</code></pre>
    <div class="callout">Business and success-audit rows roll back. Only the separately recorded failed attempt survives.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/middleware/command_tx_test.go">Code: pkg/middleware/command_tx_test.go</a></p>
    <aside class="notes">Excerpt from TestLoadCommand_ActivityRecorderFailureRollsBackBusinessWrite; setup and error assertions omitted. TrackActivity retries as a failure after rollback even when successful activity was already finalized. It skips recording only when CompletedAt is set AND err is nil. Run this test before tracing the workflow case in chapter 1.8.</aside>
  </section>


  <section class="implementation-slide">
    <h2>Store.Write and store.Write have different ownership</h2>
    <pre><code class="language-go">// Managed boundary: opens, commits, or rolls back a transaction.
err := s.Write(ctx, func(tx *store.Tx) error {
    // Return an error to reject the entire unit of work.
    return nil
})

// DAO helper: joins an existing transaction; never opens one.
func Write(ctx Context, f func(*Tx) error) error {
    tx, ok := ctx.Transaction()
    if !ok || tx == nil {
        return errors.Internalf("missing transaction")
    }
    return f(tx)
}</code></pre>
    <div class="callout">The lowercase package helper requires a transaction. Domain DAOs cannot accidentally turn one business operation into several commits.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/store/access.go">Code: pkg/store/access.go</a></p>
    <aside class="notes">First block is illustrative; second is the exact store.Write implementation. Store.ReadContext similarly reuses an injected transaction so queries and handlers see its tentative writes. UnitOfWork owns the default outer boundary. Neither the helper nor a joined pipeline command creates a savepoint. A callback error must reach the actual transaction owner.</aside>
  </section>

  <section class="implementation-slide">
    <h2>A caller-owned transaction owns every nested outcome</h2>
    <pre><code class="language-text">application composition opens transaction T
  command A joins T
    business write + reactions + success activity
  command B joins T
    business write + reactions + success activity
  caller returns nil  → commit all of T
  caller returns err  → roll back all of T

If B fails:
  propagate the error; do not commit A's tentative success
  joined middleware does not open a separate failure-audit write</code></pre>
    <div class="callout">A successful inner call is provisional until the caller commits. Transaction ownership includes error handling and audit policy.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/middleware/track_activity.go">Code: pkg/middleware/track_activity.go</a></p>
    <aside class="notes">Trace middleware.RunWorkflow and UnitOfWork. RunTaggedMutation supplies RunWorkflow as the owning boundary when it opens the transaction; that owner records the correlated failed attempt afterward. In TrackActivity, a context already carrying a transaction bypasses separate managed failure recording. An outer rollback removes earlier successful activities too. TestLoadCommand_UsesCallerTransactionForBusinessAndSuccessActivity verifies business and audit rows disappear together after caller rollback. The Store callback contract is error-based; it does not promise rollback on recovered panics.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Serialize shared transactions, not whole application instances</h2>
    <pre><code class="language-go">func SerializeTransaction() Middleware {
    return func(ctx *Context, _ Operation, next Next) error {
        if tx, ok := ctx.Transaction(); ok &amp;&amp; tx != nil {
            defer store.LockTransaction(tx)()
        }
        return next(ctx)
    }
}

// LockTransaction keys a sync.Mutex by *store.Tx.
// Separate transactions are coordinated by SQLite.</code></pre>
    <div class="callout">The lock protects concurrent operations sharing one caller-owned transaction. It is not a process-wide writer lock or a reentrant transaction primitive.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/middleware/transaction.go">Code: pkg/middleware/transaction.go</a></p>
    <aside class="notes">Exact middleware. app.RunTaggedMutation calls sibling operations sequentially from outside their pipelines. Do not recursively enter a facade pipeline with the same injected Tx while holding this mutex: a sync.Mutex is not reentrant. Domain collaboration uses public query packages and handlers rather than nested module calls. Direct store helpers do not independently acquire this pipeline lock.</aside>
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
    <aside class="notes">This is a rationale map, not a literal commit timeline. Open .arch-lint.yaml and architecture/arch_lint_test.go. A green import check shows that today's tree obeys the rules; intentionally invalid fixtures show that the rules reject the mistakes we care about. Neither proves a reservation rule. That needs behavior tests through the application.</aside>
  </section>
  <section class="implementation-slide">
    <h2>An import can compile and still violate ownership</h2>
    <pre><code class="language-text">Importer: app/domains/drinks/surfaces/gui

Import drinks/internal/dao
  Go internal rule: allowed, importer is inside drinks/
  arch-lint: rejected, a surface is not an allowed consumer

Import ingredients/internal/dao
  Go internal rule: rejected, importer is outside ingredients/

Import drinks/surfaces/tui
  Go compiler: allowed
  arch-lint: rejected, GUI must not depend on TUI

Run: go tool arch-lint -config=.arch-lint.yaml</code></pre>
    <div class="callout">Go protects the owning subtree. Architecture rules narrow the permitted layers within it and prevent coupling between presentation runtimes.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/.arch-lint.yaml">Code: .arch-lint.yaml</a></p>
    <aside class="notes">Derived examples from domain-internals-have-explicit-consumers and surfaces-are-bespoke. These are expected outcomes, not pasted diagnostic wording. Open architecture/arch_lint_test.go for fixtures that test allowed and forbidden imports, including an invented Web surface. Adding another domain should not require enumerating its name in every rule.</aside>
  </section>


  <section class="implementation-slide">
    <h2>Generated registration depends on concrete source conventions</h2>
    <pre><code class="language-text">Event:   struct under an events directory
Handler: method under app/.../handlers

func (h *StockAdjusted) Handle(
    ctx *middleware.HandlerContext,
    e inventoryevents.StockAdjusted,
) error

func NewStockAdjusted(
    s *store.Store, tags tag.Repository,
) *StockAdjusted

go generate ./pkg/dispatcher</code></pre>
    <div class="callout">The generator converts discoverable source structure into ordinary, reviewable calls. A package's presence alone does not register a reaction.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/dispatcher/README.md">Code: pkg/dispatcher/README.md</a></p>
    <aside class="notes">Signature/constructor shapes from the dispatcher guide. The scanner ignores test files and discovers event structs under app and pkg, then matching handler methods under app. New&lt;Type&gt; must satisfy the generated constructor convention. Review dispatcher_gen.go after generation, build it, and run a behavioral fixture test: valid generated wiring does not prove the reaction's business semantics.</aside>
  </section>

  <section class="implementation-slide">
    <h2>A fixture must exercise the real commit boundary</h2>
    <pre><code class="language-go">f := testutil.NewFixture(t)
_, hasTx := f.OwnerContext().Transaction()
testutil.IsFalse(t, hasTx)

// Complete an order using 2 oz from 10 oz.
f.Orders.Complete(ctx, &amp;ordersmodels.Order{ID: order.ID})
// stock == 8 oz

// Reuse ctx for an unrelated command.
f.Ingredients.Create(ctx, &amp;ingredient)
// stock must still be 8 oz; old events must not replay.</code></pre>
    <div class="callout">Tests should preserve the production unit of work. A fixture-wide transaction can hide commit, rollback, and operation-state bugs.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/testutil/transaction_test.go">Code: pkg/testutil/transaction_test.go</a></p>
    <aside class="notes">Illustrative excerpt from two testutil transaction tests; setup and error assertions are omitted here. Run TestFixtureContextsUseProductionTransactionBoundaries and TestFixtureCommandsDoNotReplayPriorEvents. The latter reuses one context deliberately: Chain.Execute must reset events and activity on every operation. This is a behavioral check for the context-copying design from chapter 1.1.</aside>
  </section>
</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Authorization 1.6a</div><h1>Model fine-grained access with Cedar</h1><p class="lede">Policies combine identity, action, resource attributes, and tags. Domain-owned contracts make those decisions consistent across every interface.</p><div class="section-no">1.6a</div><aside class="notes">First of three authorization recordings: policy vocabulary, real grants, entity mapping, and evaluator semantics. Follow with command transition enforcement in 1.6b and disclosure in 1.6c.</aside></section>

  <section>
    <h2>Fine-grained access is a resource decision</h2>
    <div class="cards"><div class="card"><h3>Identity</h3><p>Which principal is making this request?</p></div><div class="card"><h3>Capability</h3><p>Which domain action is requested?</p></div><div class="card"><h3>Scope</h3><p>Which resource attributes and tags make that action permissible?</p></div></div>
    <div class="callout">A sommelier can manage wine, read a tagged cocktail, and still be denied permission to update that cocktail.</div>
    <aside class="notes">Introduce attribute-based access control (ABAC) with this concrete distinction. A persona is not a blanket grant to a screen or endpoint. The same method and action can be allowed for one resource and denied for another. Keep the wine/cocktail example throughout all three authorization chapters.</aside>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/drinks/authz/policies.cedar">Code: app/domains/drinks/authz/policies.cedar</a></p>
  </section>

  <section class="implementation-slide">
    <h2>Identity enters through the operation context</h2>
    <pre><code class="language-text">principal := authn.Sommelier()
// Mixology::Actor::"sommelier"

ctx := authn.ToContext(context.Background(), principal)
// The application's session/fixture constructs middleware.Context.
// The pipeline reads middleware.Context.Principal().

// Current demo actors:
owner, manager, sommelier, bartender, anonymous</code></pre>
    <div class="callout">Actor selection is a demo identity mechanism. Cedar determines that actor's access; it does not authenticate the caller.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/authn/authn.go">Code: pkg/authn/authn.go</a></p>
    <aside class="notes">Illustrative context setup followed by a list of actor names, not one compilable block. ParseActor accepts these personas and defaults an empty selection to owner. The current evaluator gives the principal no attributes or parent memberships. These are named identities, not an implemented group hierarchy or tenant model. A real identity provider would need a trusted mapping into the authorization request.</aside>
  </section>

  <section>
    <h2>Each domain owns its policy vocabulary</h2>
    <div class="flow"><div class="node"><strong>Domain model</strong>complete business state</div><div class="arrow">→</div><div class="node"><strong>Authorization model</strong>resource attributes for Cedar</div><div class="arrow">→</div><div class="node"><strong>Principal + action</strong>operation intent</div><div class="arrow">→</div><div class="node"><strong>Cedar evaluator</strong>permit or deny</div></div>
    <div class="callout">The shared evaluator knows Cedar. Ingredients, Menus, and Orders decide what their resources and actions mean.</div>
  </section>

  <section class="implementation-slide">
    <h2>Inspect the request and the entity separately</h2>
    <pre><code class="language-go">// Selected fields from AuthorizeWithEntity.
req := cedar.Request{
    Principal: principal,
    Action:    action,
    Resource:  resource.UID,
    Context:   cedar.NewRecord(nil),
}
entities := cedar.EntityMap{
    principal:    {/* UID; empty attributes, parents, tags */},
    resource.UID: resource,
}
decision, diagnostic := cedar.Authorize(ps, entities, req)</code></pre>
    <div class="callout">The request names the resource. The entity map supplies its attributes and tags. Cedar does not fetch missing domain state.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/authz/authorize.go">Code: pkg/authz/authorize.go</a></p>
    <aside class="notes">Abbreviated entity-map entry; the request and evaluator call match authorize.go. Principal, action, resource, context form the decision request. This adapter supplies only the principal and resource entities and an empty context. Policy expressiveness is bounded by that supplied data: referenced entity IDs do not automatically load an entity graph.</aside>
  </section>

  <section class="implementation-slide">
    <h2>The schema defines what a policy can inspect</h2>
    <pre><code class="language-text">namespace Mixology {
    entity Actor enum [
        "owner", "manager", "sommelier", "bartender", "anonymous"
    ];
    entity Drink {
        Name: String,
        Category: String,
        Glass: String,
        Description: String
    } tags String;
}
namespace Mixology::Drink {
    action list, get, create, update, delete, tag, untag appliesTo {
        principal: Mixology::Actor,
        resource: Mixology::Drink,
        context: {}
    };
}</code></pre>
    <div class="callout">Drink has four declared attributes and string-valued Cedar tags. An attribute is not available to policy merely because it exists on the Go model.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/drinks/authz/schema.cedarschema">Code: app/domains/drinks/authz/schema.cedarschema</a></p>
    <aside class="notes">Exact schema, with the actor list reflowed. Revision, recipe, and review status are Go model fields but are not declared in this authorization shape. Extending policy to one of them requires an intentional schema and conversion change. The generator produces action IDs, the resource model, and schema validation support.</aside>
  </section>

  <section class="implementation-slide">
    <h2>CedarEntity is security-sensitive mapping code</h2>
    <pre><code class="language-go">func (d Drink) CedarEntity() cedar.Entity {
    return drinkauthz.Drink{
        UID: d.ID.EntityUID(), Name: d.Name,
        Category: string(d.Category),
        Glass: string(d.Glass), Description: d.Description,
        Tags: d.Tags.Map(),
    }.CedarEntity()
}</code></pre>
    <div class="callout">Hydrate authoritative state before this conversion. A valid schema proves shape, not that an attribute or tag came from a trusted source.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/drinks/models/drink.go">Code: app/domains/drinks/models/drink.go</a></p>
    <aside class="notes">Exact method, reflowed. Follow the domain DAO's tag hydration into this mapping. An empty Category is still a String and could satisfy a policy using != wine, so schema validation cannot substitute for trusted loading and business validation. Generated CedarEntity fixes the resource type, preserves the ID, and converts the declared attributes and tags.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Read the actual sommelier management policy</h2>
    <pre><code class="language-text">permit(
    principal == Mixology::Actor::"sommelier",
    action in [
        Mixology::Drink::Action::"create",
        Mixology::Drink::Action::"update",
        Mixology::Drink::Action::"delete",
        Mixology::Drink::Action::"tag",
        Mixology::Drink::Action::"untag"
    ],
    resource is Mixology::Drink
) when {
    resource.Category == "wine"
};</code></pre>
    <div class="callout">The grant is the intersection of principal, action, resource type, and category. Changing category changes the decision.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/drinks/authz/policies.cedar">Code: app/domains/drinks/authz/policies.cedar</a></p>
    <aside class="notes">Exact permit from the shipped policy. The manager permit has no category condition; the bartender permit requires Category != wine. Do not describe this as a role check followed by arbitrary command code: the resource restriction is part of the policy decision itself.</aside>
  </section>

  <section class="implementation-slide">
    <h2>A separate permit grants narrower, tag-based access</h2>
    <pre><code class="language-text">permit(
    principal == Mixology::Actor::"sommelier",
    action in [
        Mixology::Drink::Action::"list",
        Mixology::Drink::Action::"get"
    ],
    resource is Mixology::Drink
) when {
    resource.hasTag("audience") &amp;&amp;
    resource.getTag("audience") == "sommelier"
};</code></pre>
    <div class="callout">This extends reading to an individual resource. It does not grant update, tag, or untag.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/drinks/authz/policies.cedar">Code: app/domains/drinks/authz/policies.cedar</a></p>
    <aside class="notes">Exact shipped permit. hasTag guards the lookup when a key is absent. Tags are ordinary data until an authored policy gives them meaning. The wine permit and audience permit are additive; removing the audience tag from a wine does not revoke category-based access.</aside>
  </section>

  <section>
    <h2>Evaluate a policy matrix, not a persona label</h2>
    <table class="matrix"><thead><tr><th>Sommelier resource</th><th>Get</th><th>Update</th><th>Tag</th></tr></thead><tbody><tr><td>Wine, no audience tag</td><td>Allow</td><td>Allow</td><td>Allow</td></tr><tr><td>Cocktail, no audience tag</td><td>Deny</td><td>Deny</td><td>Deny</td></tr><tr><td>Cocktail, audience=sommelier</td><td>Allow</td><td>Deny</td><td>Deny</td></tr></tbody></table>
    <div class="callout">Being able to read a resource never implies permission to mutate it or change who can read it.</div>
    <aside class="notes">These nine decisions were executed against AuthorizeWithEntity and the current assembled policy set. The tag grant is scoped to list/get, while update/tag still use category rules. Use this matrix as the starting fixture for command and UI tests.</aside>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/authz/authorize.go">Code: pkg/authz/authorize.go</a></p>
  </section>

  <section class="implementation-slide">
    <h2>Permits compose; an applicable forbid overrides them</h2>
    <pre><code class="language-text">// Application-wide base.cedar:
permit(
    principal == Mixology::Actor::"owner", action, resource
);

// Audit domain, one of its explicit non-owner forbids:
forbid(
    principal == Mixology::Actor::"manager",
    action in [
        Mixology::AuditEntry::Action::"list",
        Mixology::AuditEntry::Action::"get"
    ],
    resource
);</code></pre>
    <div class="callout">Cedar denies without a matching permit. A matching forbid wins over a matching permit, regardless of document order.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/audit/authz/policies.cedar">Code: app/domains/audit/authz/policies.cedar</a></p>
    <aside class="notes">Source excerpts, reflowed. All embedded domain documents join one policy set. The owner grant is a permit, not a privileged evaluator bypass; a forbid that matched owner would still deny. Current audit forbids name the four non-owner personas. Document sorting makes assembly deterministic, not priority-ordered. Cedar combines policies without a first-match rule. See https://docs.cedarpolicy.com/auth/authorization.html for the algorithm.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Mixology treats evaluator diagnostics as failure</h2>
    <pre><code class="language-go">decision, diagnostic := cedar.Authorize(ps, entities, req)
if len(diagnostic.Errors) &gt; 0 {
    return errors.Internalf(
        "authz evaluation error: %s",
        diagnostic.Errors[0].Message,
    )
}
if decision == cedar.Deny {
    return errors.Permissionf(/* principal, action, resource */)
}
return nil</code></pre>
    <div class="callout">Cedar skips an erroneous policy when combining decisions. Mixology additionally rejects any diagnostic error, even if Cedar reports Allow.</div>
    <p class="source"><a href="https://docs.cedarpolicy.com/auth/authorization.html">Cedar reference</a></p>
    <aside class="notes">Excerpt with the Permissionf payload abbreviated. This deliberately distinguishes a legitimate denial from an evaluation failure. AuthorizeWithEntity first rejects unknown resource types and schema-invalid entities as Internal. Do not turn malformed data or a policy error into a hidden control or a skipped list row. Cedar's skip-on-error semantics are documented in the linked reference.</aside>
  </section>

  <section>
    <h2>Generate and validate the authorization contract</h2>
    <div class="layers"><div class="layer"><strong>Authored</strong><span>domain schema, policies, and Go model conversion</span></div><div class="layer"><strong>Generated</strong><span>action IDs, Cedar resource model, validator, tests, policy registry</span></div><div class="layer"><strong>At runtime</strong><span>validate resource shape, evaluate the assembled policies, classify the result</span></div></div>
    <div class="callout">Changing policy is a behavior change. Changing the schema also changes the data contract that every authorization call must supply.</div>
    <aside class="notes">Run go generate ./... after schema or policy changes and review generated output with its source. The generator validates policy syntax and schema consistency. Its supported profile is intentionally narrow: required supported scalar/entity-reference attributes, string tags, no resource parent types, and empty action contexts. Policy validation does not prove intended access or business-state authenticity; test the matrix.</aside>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/authz/README.md">Code: pkg/authz/README.md</a></p>
  </section>
</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Authorization 1.6b</div><h1>Authorize the state a command may produce</h1><p class="lede">Trusted input and actual result are separate authorization boundaries. Both must permit the action before the transaction can commit.</p><div class="section-no">1.6b</div><aside class="notes">Second authorization recording. Work from the wine policy into the facade, both middleware gates, and an executed rollback probe. Distinguish resource-state authorization from input validation, optimistic concurrency, and business transition rules.</aside></section>

  <section>
    <h2>Authority must cover both sides of the change</h2>
    <div class="split"><div class="side"><h3>Input authorization</h3><p>May this principal perform this action on the resource we are about to change?</p><p class="accent">Reject before business mutation.</p></div><div class="bridge">∩</div><div class="side"><h3>Result authorization</h3><p>May this principal perform this action on the resource state the handler actually produced?</p><p class="gold">Reject before effects can commit.</p></div></div>
    <div class="callout">Permission to start a mutation is not permission to produce every possible resulting state.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/middleware/run.go">Code: pkg/middleware/run.go</a></p>
    <aside class="notes">The same principal and required action set are evaluated against two different resource snapshots. The second check is not a redundant role lookup and is not a read check on the response. Both must succeed. This gives attribute-based rules authority over the state a command may produce, including values assigned by command code.</aside>
  </section>

  <section>
    <h2>The wine boundary constrains an update</h2>
    <table class="matrix"><thead><tr><th>Sommelier update</th><th>Loaded state</th><th>Result state</th><th>Outcome</th></tr></thead><tbody><tr><td>Wine → wine</td><td>Allow</td><td>Allow</td><td>May commit</td></tr><tr><td>Cocktail → wine</td><td>Deny</td><td>Not reached</td><td>Handler blocked</td></tr><tr><td>Wine → beer</td><td>Allow</td><td>Deny</td><td>Rollback</td></tr></tbody></table>
    <div class="callout">An input-only check permits escape from the authorized category. A result-only check permits taking control of an unauthorized resource.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/middleware/command_tx_test.go">Code: pkg/middleware/command_tx_test.go</a></p>
    <aside class="notes">This matrix isolates the pipeline contract using the shipped sommelier policy. The result-denial row uses a handler that produces beer; the public Drinks.Update facade also checks the submitted proposal and can reject earlier. Allow/Allow is necessary, not sufficient: validation, revision checks, event reactions, auditing, and commit can still fail.</aside>
  </section>

  <section class="implementation-slide">
    <h2>The pipeline checks every action at both gates</h2>
    <pre><code class="language-go">// Inside authorizeCommandActions; declarations omitted.
for _, action := range actions {
    err := authz.AuthorizeWithEntity(
        ctx.Principal(), action, in.CedarEntity())
    if err != nil { return zero, err }
}

out, err := next(ctx, in)
if err != nil { return zero, err }

for _, action := range actions {
    err := authz.AuthorizeWithEntity(
        ctx.Principal(), action, out.CedarEntity())
    if err != nil { return zero, err }
}
return out, nil</code></pre>
    <div class="callout">Result authorization uses the same required actions as input authorization. One denial or evaluation error aborts the operation.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/middleware/run.go">Code: pkg/middleware/run.go</a></p>
    <aside class="notes">Reflowed excerpt with the if initializers expanded; behavior matches run.go. The action set is derived once from loaded state before the handler executes. The wrapper returns the zero result on an authorization error. LoadCommand then propagates the error through the command chain to the transaction owner.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Drinks.Update checks three distinct resource states</h2>
    <pre><code class="language-text">LoadCommand
  load persisted drink in the transaction
  authorize update on PERSISTED state
  │
  └─ AuthorizeCommand around commands.Update
       authorize update on SUBMITTED proposal
       run commands.Update
       authorize update on ACTUAL result
  │
  authorize update on ACTUAL result
  dispatch events → record success → commit</code></pre>
    <div class="callout">The current composition makes four authorization calls over three state roles. The outer pipeline protects trusted state; the inner wrapper also constrains the proposal.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/drinks/update.go">Code: app/domains/drinks/update.go</a></p>
    <aside class="notes">Exact call structure of drinks/update.go, not a claim that every command needs four evaluations. The actual result is checked by both wrappers. Persisted state prevents a caller from changing authorization attributes in a submitted payload to acquire authority over an existing resource. The proposal check can reject a forbidden requested category before the handler runs. Result checks cover the state command code actually returns.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Read the complete update facade</h2>
    <pre><code class="language-go">func (m *Module) Update(
    ctx *middleware.Context, drink *models.Drink,
) (*models.Drink, error) {
    authorizedUpdate := middleware.AuthorizeCommand(
        authz.ActionUpdate, m.commands.Update)
    return m.pipeline.LoadCommand(ctx, authz.ActionUpdate,
        func(ctx *middleware.Context) (*models.Drink, error) {
            return m.queries.Get(ctx, drink.ID)
        },
        func(
            ctx *middleware.Context, _ *models.Drink,
        ) (*models.Drink, error) {
            return authorizedUpdate(ctx, drink)
        },
    )
}</code></pre>
    <div class="callout">The persisted object establishes authority over the target. The caller's object supplies the requested replacement, not proof of authority.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/drinks/update.go">Code: app/domains/drinks/update.go</a></p>
    <aside class="notes">Exact facade with reflowed signature and wrapper call. Open internal/commands/update.go next: it validates fields and recipe dependencies, preserves persisted tags, sets status, writes through the DAO, and returns the updated model. A submitted model is not necessarily the resulting model. The DAO's revision check is an additional concurrency guarantee, not an authorization substitute.</aside>
  </section>

  <section class="implementation-slide">
    <h2>A forged category cannot authorize an existing target</h2>
    <pre><code class="language-text">Persisted target:  ID=drk-X, Category=cocktail
Submitted update: ID=drk-X, Category=wine
Principal:        sommelier
Action:           Drink::Action::"update"

If we authorize only the proposal:
  wine satisfies the sommelier policy

Current LoadCommand path:
  load drk-X → cocktail → Permission
  commands.Update never runs</code></pre>
    <div class="callout">An authorized-looking proposal does not grant authority over the record it names.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/drinks/update.go">Code: app/domains/drinks/update.go</a></p>
    <aside class="notes">Illustrative request, derived from the real facade and category policy. This is why the loader is inside the command transaction and uses the submitted ID only as a selector. It is not sufficient to authorize a detached UI model, even if its revision token is valid. Result-only authorization would also miss this attack if the command produced wine.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Isolate the result gate with a real pipeline test</h2>
    <pre><code class="language-go">// TestLoadCommand_AuthorizesResultAfterHandle, excerpt.
handled := false
_, err := pipeline.LoadCommand(
    fix.ActorContext("sommelier"), drinksauthz.ActionUpdate,
    func(*middleware.Context) (testEntity, error) {
        return wine, nil
    },
    func(_ *middleware.Context, out testEntity) (testEntity, error) {
        handled = true
        out.Attributes["Category"] = cedar.String("beer")
        return out, nil
    },
)
testutil.ErrorIsPermission(t, err)
testutil.IsTrue(t, handled)</code></pre>
    <div class="callout">The handler ran, but its successful Go return did not make the command authorized.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/middleware/command_tx_test.go">Code: pkg/middleware/command_tx_test.go</a></p>
    <aside class="notes">Existing repository test, reflowed. The fixture and wine entity are defined above the excerpt; testEntity fills the schema's required String fields. Run go test ./pkg/middleware -run TestLoadCommand_AuthorizesResultAfterHandle -v. Separately, the domain test TestDrinks_ABAC_SommelierCannotChangeWineToCocktail verifies the public facade rejects a forbidden proposal and preserves wine; do not mislabel that earlier rejection as proof of result-gate execution.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Result denial must undo work, not just hide output</h2>
    <pre><code class="language-go">// Probe handler inside LoadCommand, using the real store:
func(
    ctx *middleware.Context, out drinkauthz.Drink,
) (drinkauthz.Drink, error) {
    if err := store.Write(ctx, func(tx *store.Tx) error {
        return tx.Insert(&amp;probe{Kind: "tentative-write"})
    }); err != nil {
        return out, err
    }
    ctx.AddEvent("tentative-event")
    out.Category = "beer"
    return out, nil
}</code></pre>
    <div class="callout">The write is tentative. Output denial must propagate to UnitOfWork; returning an error only after commit would be too late.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/middleware/uow.go">Code: pkg/middleware/uow.go</a></p>
    <aside class="notes">Verification probe, not a shipped domain handler. Use the preceding test's sommelier/wine setup, register probe{ID int; Kind string}, and attach counting dispatcher/activity callbacks. This probe was executed against the real pipeline and SQLite store. It adds a write to the result-gate scenario so rollback, suppressed event dispatch, and failure-audit behavior are directly observable.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Follow result denial all the way out</h2>
    <pre><code class="language-text">Observed probe:
  handler ran                     true
  returned error kind             Permission
  persisted tentative-write rows  0
  dispatched tentative events     0
  successful activity callbacks   0
  failed activity callbacks       1

Result gate denies
  → DispatchEvents returns the error without dispatch
  → success activity is skipped
  → managed transaction rolls back
  → failure activity is attempted separately</code></pre>
    <div class="callout">Both authorization gates live inside the transaction. Denial of the produced state prevents that state from becoming durable.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/middleware/chains.go">Code: pkg/middleware/chains.go</a></p>
    <aside class="notes">Observed values from the preceding verification probe. Activity callbacks were counters; this output does not claim they persisted audit rows. Existing middleware tests cover durable failure activities separately. With a caller-owned transaction, the caller must propagate the error and roll back the outer composition. Never swallow an error and commit tentative writes. Irreversible external side effects do not belong in this transaction path.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Tag replacement can require several permissions</h2>
    <pre><code class="language-text">current: audience=sommelier, featured
desired: audience=bartender

replaceActions(current, desired):
  changed audience value → tag
  removed featured key   → untag

Before mutation: allow(tag, current) AND allow(untag, current)
After mutation:  allow(tag, result)  AND allow(untag, result)

No derived actions → Internal, handler does not run
No-op replacement → tag is still required</code></pre>
    <div class="callout">The submitted replacement is one intent, but its authority is the complete set of actions implied by the change.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/tagging/module.go">Code: app/domains/tagging/module.go</a></p>
    <aside class="notes">Trace replaceActions in tagging/module.go and authorizeCommandActions in run.go. No-op replacement deliberately selects TagAction; an empty callback result is a pipeline misuse and fails closed. The same action set is checked against both snapshots, including reloaded tags. The stable activity action is tag even when untag is additionally required. Chapter 2.2 follows the registry and persistence composition.</aside>
  </section>

  <section>
    <h2>Endpoint checks constrain transitions, not arbitrary pairs</h2>
    <div class="cards"><div class="card"><h3>Same request intent</h3><p>The principal and action set stay fixed while the resource snapshot changes.</p></div><div class="card"><h3>Both states must qualify</h3><p>A policy requiring Category=wine restricts both the source and destination.</p></div><div class="card"><h3>Business transition rules</h3><p>Readiness and legal lifecycle changes still require command validation.</p></div></div>
    <div class="callout">Cedar is called twice with one resource at a time. The current adapter does not supply an old/new pair or a phase flag.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/authz/authorize.go">Code: pkg/authz/authorize.go</a></p>
    <aside class="notes">This distinction matters for fine-grained policy design. A publish policy that permits only draft resources would also reject the published result. A policy for the same action must admit legitimate source and destination states; the command enforces their legal relationship. More expressive pairwise conditions would need an explicit authorization-model design beyond today's empty request context. Current menu policies grant manager publication without a status condition.</aside>
  </section>

  <section>
    <h2>The result gate has a precise enforcement boundary</h2>
    <div class="layers"><div class="layer"><strong>Authorized result</strong><span>the resource returned by the command, before event dispatch</span></div><div class="layer"><strong>Consumer-owned effects</strong><span>trusted handlers perform bounded reactions in the same transaction</span></div><div class="layer"><strong>Domain obligation</strong><span>return accurate policy state and validate every owned business effect</span></div></div>
    <div class="callout">The pipeline does not independently authorize every row written by every event handler.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/middleware/dispatch_events.go">Code: pkg/middleware/dispatch_events.go</a></p>
    <aside class="notes">The command authorization contract must account for its business consequences. A caller authorized to place an order need not independently hold a stock-management action for Inventory's reservation reaction. Handlers are internal collaboration, not arbitrary user-callable commands. Result authorization occurs before those reactions and is not a global scan of final database state. When adding an effect that needs independent user authority, express that requirement explicitly in the originating workflow.</aside>
  </section>
</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Authorization 1.6c</div><h1>Expose only what the operation permits</h1><p class="lede">Reads, counts, discovery, and action projections each disclose information. Their authority must be as explicit as a command's.</p><div class="section-no">1.6c</div><aside class="notes">Third authorization recording. Demonstrate a manager granting and revoking sommelier access to one cocktail, then trace the effect through Get, List, counts, and controls. Finish with the verification matrix and the separate discovery contract.</aside></section>

  <section>
    <h2>One decision appears at four scales</h2>
    <div class="cards four"><div class="card"><h3>Workspace</h3><p>Can this actor discover and enter the domain?</p></div><div class="card"><h3>Collection</h3><p>Which rows and counts may become visible?</p></div><div class="card"><h3>Entity</h3><p>May this exact resource be read or selected?</p></div><div class="card"><h3>Action</h3><p>May this exact resource transition now?</p></div></div>
    <div class="callout">Navigation, summaries, and lists disclose information; commands change it. Each needs authorization at its own application boundary.</div>
  </section>

  <section class="implementation-slide">
    <h2>Walk an individual grant through the application</h2>
    <pre><code class="language-go">// Existing tag ABAC test; fixture setup omitted.
grant := tag.Tag{Key: "audience", Value: "sommelier"}

_, err := f.App.Tags.Upsert(sommelier, cocktail.EntityUID(), grant)
testutil.ErrorIsPermission(t, err) // cannot self-grant

_, err = f.App.Tags.Upsert(manager, cocktail.EntityUID(), grant)
testutil.Ok(t, err)
_, err = f.Drinks.Get(sommelier, cocktail.ID)
testutil.Ok(t, err)

_, err = f.App.Tags.Remove(manager, cocktail.EntityUID(), "audience")
testutil.Ok(t, err)
_, err = f.Drinks.Get(sommelier, cocktail.ID)
testutil.ErrorIsPermission(t, err)</code></pre>
    <div class="callout">An authorized manager can grant and revoke read access by changing policy-relevant data. No policy reload is needed for that resource change.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/tag_abac_test.go">Code: app/tag_abac_test.go</a></p>
    <aside class="notes">Adapted excerpt from TestDrinkAudienceTagExtendsSommelierReadPolicy; the repeated tag literal is named grant. The full test also proves unrelated tags do nothing, list filtering sees the same grant, and changing the audience value revokes it. The tag operation itself loads and authorizes current state before mutation, so the sommelier cannot opt an unauthorized cocktail into its own read access. Policy documents are embedded and parsed once; changing policy text is a different deployment operation.</aside>
  </section>

  <section>
    <h2>Fill the visible page, not the storage page</h2>
    <div class="flow"><div class="node"><strong>stable candidates</strong>filter + hydrate</div><div class="arrow">→</div><div class="node"><strong>authorize each</strong>deny disappears</div><div class="arrow">→</div><div class="node"><strong>continue scanning</strong>until N visible</div><div class="arrow">→</div><div class="node"><strong>look ahead</strong>safe cursor</div></div>
    <div class="cards two"><div class="card"><h3>Permission denial</h3><p>Expected list behavior. Omit the entity and keep scanning.</p></div><div class="card stop"><h3>Evaluation or storage failure</h3><p>Not a denial. Fail the query instead of returning a believable partial result.</p></div></div>
    <aside class="notes">The caller asks for two rows. Candidate A is denied, B allowed, C denied, and D allowed. The page contains B and D. Look for another allowed row to decide whether Next exists; use D's cursor, not a denied row's identity. The same authorized traversal supplies counts. This costs more scanning than raw SQL pagination, but keeps results consistent with policy. Open PageQuery and a domain List method.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Permission denial is a branch in the paging loop</h2>
    <pre><code class="language-go">err = authz.AuthorizeWithEntity(
    c.Principal(), action, item.CedarEntity(),
)
switch {
case err == nil:
    if len(page.Items) == pageRequest.Limit {
        page.Next = cursor(page.Items[len(page.Items)-1])
        return nil
    }
    page.Items = append(page.Items, item)
case errors.IsPermission(err):
    continue
default:
    return err
}</code></pre>
    <div class="callout">The extra authorized item proves there is a next page. A denied item neither consumes a page slot nor becomes the returned cursor.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/middleware/run.go">Code: pkg/middleware/run.go</a></p>
    <aside class="notes">Exact inner switch from PageQuery with the call reflowed. Work through candidates A denied, B allowed, C denied, D allowed, E allowed with limit two: return B/D and cursor D. E is the lookahead. If evaluating E fails, the operation returns an error; callers must not present the partially accumulated page as a successful result.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Counts reuse the authorized list, not raw SQL</h2>
    <pre><code class="language-go">func (m *Module) Count(
    ctx *middleware.Context, req ListRequest,
) (int, error) {
    return paging.Count(func(
        cursor paging.Cursor,
    ) (paging.Page[*models.Drink], error) {
        req.Cursor = cursor
        req.Limit = paging.DefaultLimit
        return m.List(ctx, req)
    })
}</code></pre>
    <div class="callout">The displayed total describes the actor's visible collection, with the same filters and policy decisions as the list.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/drinks/list.go">Code: app/domains/drinks/list.go</a></p>
    <aside class="notes">Exact method with reflowed signature. Open List above it: parsing, domain DAO hydration, and PageQuery all remain in the count path. A raw database count would disclose hidden resources and disagree with the UI. This is more work than a single COUNT query; any optimization must preserve the authorized result set. This design does not claim to eliminate timing side channels or provide field-level redaction.</aside>
  </section>

  <section>
    <h2>Discovery has an explicit disclosure contract</h2>
    <table class="matrix"><thead><tr><th>Operation</th><th>Authority</th><th>Disclosure</th></tr></thead><tbody><tr><td>Drinks.Get / List</td><td>Drink action on each resource</td><td>allowed domain models</td></tr><tr><td>Tags.List(target)</td><td>target domain's Get action</td><td>that target's tags</td></tr><tr><td>Tags.Show / Summary</td><td>TagDiscovery action, owner-only today</td><td>matching references or aggregates</td></tr></tbody></table>
    <div class="callout">Tag discovery deliberately does not replay every target's Get permission. Its own grant authorizes that broader disclosure.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/tagging/module.go">Code: app/domains/tagging/module.go</a></p>
    <aside class="notes">Show uses QueryResource on TagDiscovery and returns active target type, ID, name, and tag; Summary returns tag aggregates. The owner-only discovery policy is authored beside Tagging. This is a different contract from per-resource paging, not a shortcut around it. If the discovery grant is broadened, review exactly which references and counts the newly authorized principal may learn. Opening a target remains separately authorized.</aside>
  </section>

  <section class="implementation-slide">
    <h2>A real policy separates reading from management</h2>
    <pre><code class="language-text">permit(
    principal,
    action in [
        Mixology::Menu::Action::"list",
        Mixology::Menu::Action::"get"
    ],
    resource
);

// The manager permit includes these actions, among others:
principal == Mixology::Actor::"manager"
action in [Mixology::Menu::Action::"publish",
           Mixology::Menu::Action::"readiness"]
resource is Mixology::Menu</code></pre>
    <div class="callout">Permission answers whether the actor may publish. The command's readiness check answers whether this menu can be published now.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/menus/authz/policies.cedar">Code: app/domains/menus/authz/policies.cedar</a></p>
    <aside class="notes">The first permit is exact; the second block lists selected clauses from the larger manager permit and is not a standalone policy. Owner permission comes from the assembled policy set. Do not invent a draft visibility rule: the current Menu list/get permit is public. Contrast that policy with another domain's restricted resources when showing row elision.</aside>
  </section>

  <section>
    <h2>Projection guides. Commands enforce.</h2>
    <div class="split"><div class="side"><h3>Presentation projection</h3><p>Combines permission with durable prerequisites so a view can hide denied actions and explain unavailable ones.</p></div><div class="bridge">≠</div><div class="side"><h3>Authoritative command</h3><p>Reloads current state, repeats authorization, and checks invariants inside the write transaction.</p></div></div>
    <div class="callout">A stale screen may offer an action that just became invalid. That is a normal race, not authority granted by the UI.</div>
  </section>

  <section class="implementation-slide">
    <h2>A Publish control carries its own permission</h2>
    <pre><code class="language-go">// Selected declaration from Menus' action projector.
Permission: permission(menusauthz.ActionUpdate, resource),
Controls: []actions.Control{
    {
        ID:         ControlPublish,
        Permission: permission(menusauthz.ActionPublish, resource),
        Conditions: []actions.Condition{publishCondition(selected)},
    },
}

// Control permission replaces the inherited default.
// Permission runs first; conditions run only when authorized.</code></pre>
    <div class="callout">Being allowed to edit does not imply being allowed to publish. A control with a distinct action must project that action's permission.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/menus/actions.go">Code: app/domains/menus/actions.go</a></p>
    <aside class="notes">Selected fields from the Group declaration, with other controls omitted. The shared evaluator treats an explicit control permission as an override of the inherited default, not an additional Edit requirement. This permits publish-only policy designs without changing widget logic. Current manager policies allow both. Permission denial hides the control; an allowed but unmet lifecycle/readiness condition disables it with a reason; evaluation errors propagate. Chapter 4.6 follows the evaluator and native adapters.</aside>
  </section>

  <section>
    <h2>Test the authorization contract at every boundary</h2>
    <table class="matrix"><thead><tr><th>Evidence</th><th>Failure it catches</th></tr></thead><tbody><tr><td>Policy matrix + schema tests</td><td>wrong grants, malformed resource data</td></tr><tr><td>Loaded-state denial</td><td>unauthorized target reaches the handler</td></tr><tr><td>Handler runs, result denied</td><td>input-only authorization</td></tr><tr><td>Stored rows, events, activity</td><td>denial occurs after effects escape</td></tr><tr><td>Get, List, Count, discovery, controls</td><td>inconsistent disclosure or advertised authority</td></tr></tbody></table>
    <div class="callout">Test permits and denials through the public facade, and isolate both pipeline gates so an earlier denial cannot hide a missing result check.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/middleware/command_tx_test.go">Code: pkg/middleware/command_tx_test.go</a></p>
    <aside class="notes">Code walk: pkg/authz/authorize_test.go, pkg/middleware/command_tx_test.go, drinks/update_test.go and permissions_test.go, app/tag_abac_test.go, and menus/actions_test.go. Include every derived action in before/after tests and assert empty action sets fail closed. The focused suites and an additional SQLite rollback probe were executed for this chapter. When extending the authorization model, add both positive and adversarial cases before treating the new attribute as a trusted policy boundary.</aside>
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
    <h2>Keep metric label values bounded</h2>
    <div class="split"><div class="side"><h3>Current instruments</h3><p>Command/query totals use action + result. Error counters and durations use action. Store read/write durations have no labels.</p><p class="accent">Small, stable cardinality.</p></div><div class="bridge">≠</div><div class="side"><h3>Never labels</h3><p>Entity IDs, user filter text, error messages, tag values, or arbitrary resource names.</p><p class="gold">Unbounded and operationally expensive.</p></div></div>
    <div class="callout">Authorization and event metric names are reserved but not currently emitted. The deck distinguishes available vocabulary from actual instrumentation.</div>
    <aside class="notes">Cardinality means the number of distinct label combinations. An action such as Place has a bounded vocabulary; OrderID would create another series for every order. Use logs and audit to find an order, and metrics to understand Place across many orders. Open pkg/telemetry/README.md and the logging/metrics middleware. The in-memory metrics implementation is useful for recording without a monitoring server.</aside>
  </section>

  <section>
    <h2>Libraries expose a contract; executables own lifecycle</h2>
    <div class="layers"><div class="layer"><strong>Domain + store</strong><span>record through a tiny <code>Metrics</code> interface</span></div><div class="layer"><strong><code>pkg/telemetry</code></strong><span>no-op, memory, OTEL, and Prometheus-backed implementations</span></div><div class="layer"><strong><code>main/&lt;surface&gt;</code></strong><span>address, HTTP server, startup, and shutdown</span></div><div class="layer private"><strong>Runtime constraint</strong><span>concurrent local surfaces need distinct metrics ports</span></div></div>
  </section>
  <section class="implementation-slide">
    <h2>One denied command, two observability decisions</h2>
    <pre><code class="language-go">// Logging: expected denial is informational.
case errors.IsPermission(err):
    logger.Info(string(op.Kind)+" denied",
        slog.Duration("duration", duration), log.Err(err))

// Metrics: every non-nil result is counted as an error.
if err != nil {
    mc.commandTotal.Inc(actionLabel, "error")
    mc.commandErrors.Inc(actionLabel)
}</code></pre>
    <div class="callout">A denial is informational in logs but still increments command error metrics. Interpret the counters according to this implementation.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/middleware/logging.go">Code: pkg/middleware/logging.go</a></p>
    <aside class="notes">Selected branches from logging.go and metrics.go. For Menu.publish, the action label is Menu.publish; the instruments are mixology_command_total, mixology_command_errors_total, and mixology_command_duration_seconds. Example label sets are action=Menu.publish,result=error for total and action=Menu.publish for errors/duration. IDs live in diagnostic log fields, not metric labels. No fake latency or measured sample is implied.</aside>
  </section>


  <section class="implementation-slide">
    <h2>Measure the operation's final outcome, including unwind</h2>
    <pre><code class="language-text">command body returns nil
  → result authorization permits
  → event reaction succeeds
  → successful activity recorder fails
  → transaction rolls back
  → Metrics records error, not success
  → Logging emits "command failed"

Duration includes everything inside those wrappers.
Caller transaction lock wait happens outside both wrappers.</code></pre>
    <div class="callout">Where instrumentation sits defines what its numbers mean. Handler success is not operation success.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/middleware/chains.go">Code: pkg/middleware/chains.go</a></p>
    <aside class="notes">Trace NewPipeline, Metrics, and Logging. Both observation wrappers sit outside TrackActivity and UnitOfWork, so their measured work includes managed failure-audit attempts and transaction completion. SerializeTransaction is outside them; time waiting for its per-Tx mutex is excluded. Store read/write durations are a different measurement boundary, not additive independent work.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Test metric meaning without a running exporter</h2>
    <pre><code class="language-go">memory := telemetry.Memory()
// Supply memory as PipelineConfig.Metrics.

// After a denied or otherwise failed Drink update:
memory.CounterValue(
    telemetry.MetricCommandTotal, "Drink.update", "error",
) // 1
memory.CounterValue(
    telemetry.MetricCommandErrors, "Drink.update",
) // 1

// The equivalent successful call uses result="success".</code></pre>
    <div class="callout">The application owns names and label meaning. Backend choice must not change the operation's observable outcome.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/middleware/metrics.go">Code: pkg/middleware/metrics.go</a></p>
    <aside class="notes">Illustrative MemoryMetrics assertions, with pipeline setup omitted. Label values are positional: action then result on totals, only action on errors/duration. Use an isolated backend so expected counts are local to the example. A permission denial remains an error metric even though the log uses informational severity. The backend is metrics-only; this is not distributed tracing.</aside>
  </section>
</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Foundation 1.8</div><h1>Treat auditing as a domain</h1><p class="lede">An audit trail is durable business evidence with transaction semantics, policy, filtering, and its own read model.</p><div class="section-no">1.8</div></section>

  <section>
    <h2>An activity is more than a log line</h2>
    <div class="cards"><div class="card"><h3>Who + what</h3><p>Principal, Cedar action, and primary resource identify the attempted operation.</p></div><div class="card"><h3>When + outcome</h3><p>Start, completion, success, and diagnostic error preserve what happened.</p></div><div class="card"><h3>Affected entities</h3><p>Changed-resource IDs, referenced participants, and domain-authored effects distinguish what changed from what was inspected.</p></div></div>
    <div class="callout">Audit is append-only evidence. It is not diagnostic logging and it is not a replayable domain event stream.</div>
  </section>

  <section>
    <h2>Success and failure take different transaction paths</h2>
    <div class="split"><div class="side"><h3>Successful command</h3><div class="transaction">mutation + handlers + success audit</div><p>If recording fails, the business operation rolls back.</p></div><div class="bridge">∥</div><div class="side"><h3>Failed managed command</h3><div class="transaction">rollback first</div><p>Then persist the failed attempt in a separate managed write.</p></div></div>
    <div class="callout"><code>recordSuccessfulActivity</code> runs inside the unit of work. <code>TrackActivity</code> records a managed failure only after rollback. Caller-owned transactions keep failure activity under the caller's decision.</div>
    <aside class="notes">Open pkg/middleware/track_activity.go and app/domains/audit. A successful activity must describe writes that actually committed, so it belongs in their transaction. A failed attempt must survive their rollback, so managed commands record it afterward. A caller composing several commands owns the outer transaction and must handle its error. TouchEntity, ReferenceEntity, and RecordEffect are explicit attribution, not automatic change detection; tests must verify changed entities, references, and effects.</aside>
  </section>

  <section>
    <h2>Separate changes, references, and explanations</h2>
    <table class="matrix"><thead><tr><th>Activity field</th><th>Meaning</th><th>Example</th></tr></thead><tbody><tr><td>Touches</td><td>Attributed changed resources</td><td>rewritten Drink</td></tr><tr><td>Participants</td><td>Referenced resources</td><td>inspected, unchanged Menu</td></tr><tr><td>Effects</td><td>Domain-authored before/after explanation</td><td>recipe or stock disposition change</td></tr><tr><td>WorkflowID</td><td>Correlation across commands</td><td>domain edit + tag replacement</td></tr></tbody></table>
    <div class="callout">A reference is not a mutation. An effect explains selected facts; it is not an automatic database diff.</div>
    <aside class="notes">Open pkg/middleware/activity.go and events/activity.go. RecordEffect also touches its resource; ReferenceEntity deduplicates references. Domain writers choose the effect kind and fields, serialized as strings. This is not event sourcing or a complete replay model.</aside>
  </section>

  <section>
    <h2>Failure to record has an explicit policy</h2>
    <table class="matrix"><thead><tr><th>Situation</th><th>Audit behavior</th><th>Returned result</th></tr></thead><tbody><tr><td>success recorder or commit fails</td><td>rollback, attempt failure record</td><td>operation failure</td></tr><tr><td>managed command fails</td><td>record after rollback</td><td>original error</td></tr><tr><td>failure recording also fails</td><td>durability cannot be promised</td><td>errors.Join preserves both</td></tr><tr><td>caller supplies transaction</td><td>record inside caller transaction</td><td>caller owns failure policy</td></tr></tbody></table>
    <aside class="notes">Read TrackActivity and RunWorkflow. Both preserve the initiating failure if post-rollback recording fails. They detach cancellation for the evidence write, not for continuing business work. A joined error is a tree; do not assume every error has one unwrap successor. No retry queue is implied.</aside>
  </section>

  <section>
    <h2>The read side is still an application boundary</h2>
    <div class="layers"><div class="layer"><strong>Audit module</strong><span>list, count, entity history, and actor activity</span></div><div class="layer"><strong>Query contract</strong><span>action, principal, entity, time window, typed expression, cursor</span></div><div class="layer"><strong>Pipeline</strong><span>Cedar authorization and permission-safe paging</span></div><div class="layer private"><strong>Surfaces</strong><span>CLI, TUI, and GUI adapt the same append-only evidence</span></div></div>
    <div class="callout">The system that records activity automatically does not grant everyone permission to inspect it.</div>
  </section>
  <section class="implementation-slide">
    <h2>The activity stores explanations, not a replay log</h2>
    <pre><code class="language-go">// Selected fields; actor, action, resource and times omitted.
type Activity struct {
    WorkflowID   string
    Touches      []cedar.EntityUID
    Participants []cedar.EntityUID
    Effects      []Effect
    Success      bool
    Error        string
}
type Effect struct {
    Kind     string
    Resource cedar.EntityUID
    Changes  []Change // Field, Before, After are strings.
}</code></pre>
    <div class="callout">On a failed activity, effects describe attempts that rolled back, not committed state.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/middleware/events/activity.go">Code: pkg/middleware/events/activity.go</a></p>
    <aside class="notes">Selected declarations. Effects do not replace domain snapshots, amendment history, or inventory movement records. Correlation connects operations; domain history preserves accepted facts. Diagnostic Error remains subject to Audit's separate authorization policy.</aside>
  </section>

  <section class="implementation-slide">
    <h2>A composed failure has one outer owner</h2>
    <pre><code class="language-go">// RunWorkflow control flow, success/failure construction omitted.
state := &amp;workflowState{id: ksuid.New().String()}
derived := *ctx
derived.workflow = state
err := s.Write(ctx, func(tx *store.Tx) error {
    return run(derived.WithTransaction(tx))
})
// On failure, aggregate child touches, participants and effects.
// Complete a failed Mixology::Workflow::Action activity.
// Record it in a new write after the business rollback.
return errors.Join(err, auditErr)</code></pre>
    <div class="callout">Successful child activities share WorkflowID and commit with business writes. Outer failure replaces them with one correlated failed attempt.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/middleware/workflow.go">Code: pkg/middleware/workflow.go</a></p>
    <aside class="notes">Control-flow excerpt, not a complete function. RunWorkflow joins an existing transaction without creating another owner or savepoint. The owner must propagate errors and handle rollback. Invalid tags rejected before the workflow do not produce a workflow activity. TestFailedSelectedAmendmentsRollBackAllEffectsAndPersistFailure and TestLateWorkflowFailureRollsBackEveryDomain exercise this owning boundary.</aside>
  </section>

</section>

<section>
  <section class="centered section-slide">
    <div class="eyebrow">Foundation 2.1</div><h1>Coordinate domains with bounded event fan-out</h1>
    <p class="lede">Ingredient retirement changes four domains without giving Ingredients four collaborators.</p><div class="section-no">2.1</div>
  </section>

  <section>
    <h2>Why Ingredients does not call every consumer</h2>
    <pre><code class="language-go">func (m *Ingredients) Retire(ctx Context, id ID) error {
    m.inventory.Remove(ctx, id)
    m.drinks.ReplaceOrReview(ctx, id)
    m.orders.BlockSnapshots(ctx, id)
    m.menus.Recalculate(ctx, id)
    return m.ingredients.Retire(ctx, id)
}</code></pre>
    <div class="rule-list"><div class="rule"><b>×</b><span>Ingredients decides what retirement means everywhere.</span></div><div class="rule"><b>×</b><span>The source domain imports every consumer.</span></div><div class="rule"><b>×</b><span>Adding a reaction edits the initiating command.</span></div><div class="rule"><b>×</b><span>The “simple” path becomes the system map.</span></div></div>
    <aside class="notes">This is a hypothetical alternative, not an earlier implementation. Use it to explain the ownership constraint: Ingredients declares retirement; each affected domain owns its reaction. The following slides trace the actual dispatcher and handlers.</aside>
  </section>

  <section>
    <h2>Separate questions from decisions</h2>
    <div class="split"><div class="side"><h3>Public query</h3><p>“Is this ingredient referenced?”</p><p>Safe when the caller owns the decision that follows.</p></div><div class="bridge">vs</div><div class="side"><h3>Public event</h3><p>“This ingredient was retired with this explicit replacement intent.”</p><p>Each consumer owns its reaction.</p></div></div>
    <div class="callout"><strong>Queries move information.</strong> Events move facts. Neither exposes another domain’s command implementation.</div>
  </section>

  <section>
    <h2>One fact, bounded fan-out</h2>
    <div class="fanout"><div class="event-source"><strong>Ingredients</strong><span class="small">IngredientDeleted</span></div><div class="event-bus">⇢</div><div class="handler-stack"><div class="handler"><strong>Drinks</strong>rewrite future recipes or require review</div><div class="handler"><strong>Inventory</strong>retain stock; discontinue or quarantine</div><div class="handler"><strong>Orders</strong>block withdrawn stock; preserve acceptance</div><div class="handler"><strong>Menus</strong>recompute availability, preserve curation</div></div></div>
    <div class="transaction">command mutation + four leaf reactions + touched entities + successful audit = one SQLite transaction</div>
    <aside class="notes">The Go event is named IngredientDeleted; the business operation and Cedar action are retirement. Point out that mapping in app/domains/ingredients/events/ingredient-deleted.go so viewers can find the implementation. The payload carries the retired ingredient and optional permanent replacement intent. These are in-process events delivered before commit, so “fact” means a fact of the tentative transaction. If a reaction fails, that whole transaction is rolled back.</aside>
  </section>

  <section>
    <h2>The event dispatcher is generated glue</h2>
    <div class="flow five"><div class="node"><strong>AddEvent</strong>owned fact</div><div class="arrow">→</div><div class="node"><strong>command returns</strong>still in UoW</div><div class="arrow">→</div><div class="node"><strong>Handling</strong>all snapshots</div><div class="arrow">→</div><div class="node"><strong>Handle</strong>all reactions</div><div class="arrow">→</div><div class="node"><strong>audit + commit</strong>atomic result</div></div>
    <pre><code class="language-go">func (h *IngredientDeleted) Handling(
    ctx *middleware.HandlerContext,
    event ingredientsevents.IngredientDeleted,
) error // capture state before any reaction

func (h *IngredientDeleted) Handle(
    ctx *middleware.HandlerContext,
    event ingredientsevents.IngredientDeleted,
) error // apply the owned reaction</code></pre>
    <div class="callout"><code>HandlerContext</code> has transaction, principal, and <code>TouchEntity</code>. It deliberately has no <code>AddEvent</code>.</div>
  </section>

  <section>
    <h2>Capture dependencies before any handler changes them</h2>
    <div class="flow"><div class="node"><strong>fresh handlers</strong>one event-local receiver each</div><div class="arrow">→</div><div class="node"><strong>optional <code>Handling</code></strong>all snapshots finish</div><div class="arrow">┃</div><div class="node"><strong>every <code>Handle</code></strong>apply owned reactions</div><div class="arrow">→</div><div class="node"><strong>commit</strong>one outcome</div></div>
    <div class="callout">The command has already mutated state. For each event, all <code>Handling</code> calls finish before any <code>Handle</code> call begins.</div>
    <aside class="notes">Handling is a generator-recognized method convention, not a shared Go interface. The preparation barrier applies to one event at a time; command events are dispatched sequentially. It preserves data a later reaction would otherwise lose. It does not automatically make arbitrary handlers order-independent: each handler must use captured state or otherwise remain correct when peer reactions run in a different order.</aside>
  </section>

  <section>
    <h2>Why Menus needs a preparation step</h2>
    <div class="layers"><div class="layer"><strong>Before reactions</strong><span>A recipe still references the retired ingredient. Menus finds the affected drinks and menus.</span></div><div class="layer"><strong>Drinks reacts</strong><span>An explicit replacement may rewrite that recipe, removing the old reference.</span></div><div class="layer"><strong>Menus reacts</strong><span>It persists availability fully calculated during preparation, without reading a sibling's writes.</span></div></div>
    <div class="callout">Querying only after recipe rewrite could return no matches for the retired ingredient and leave affected menus untouched.</div>
    <aside class="notes">Open app/domains/menus/handlers/ingredient-deleted.go. Handling delegates to preparedMenus.retire, which uses the same pure recipe-retirement rule as Drinks and overrides future stock availability. It prepares complete Menu values; Handle only persists them. Discovering affected IDs is necessary but insufficient when the calculation would otherwise depend on sibling writes.</aside>
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
  <section class="implementation-slide">
    <h2>Generated dispatch constructs event-local receivers</h2>
    <pre><code class="language-text">IngredientDeleted case (error branches omitted here):

construct drinksHandler, inventoryHandler,
          menusHandler, ordersHandler

drinksHandler.Handling(hctx, e)
inventoryHandler.Handling(hctx, e)
menusHandler.Handling(hctx, e)
────────────────────────────────── preparation barrier
drinksHandler.Handle(hctx, e)
inventoryHandler.Handle(hctx, e)
menusHandler.Handle(hctx, e)
ordersHandler.Handle(hctx, e)</code></pre>
    <div class="callout">The same receiver holds preparation data and later applies its reaction. Generated order is visible, but must not become an undocumented dependency.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/dispatcher/dispatcher_gen.go">Code: pkg/dispatcher/dispatcher_gen.go</a></p>
    <aside class="notes">This is the actual call order in the generated case, expressed as a trace. Open the full case to inspect each handlerError branch, then change to menus/handlers/ingredient-deleted.go. Handling calculates menu changes using projected stock and the public pure Drink.RetireIngredient rule. Handle persists prepared values without reading sibling state. The barrier alone does not guarantee independence; prepared data and permutation tests establish it.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Prepare the resulting state, not just a list of IDs</h2>
    <pre><code class="language-text">OrderPlaced.Handling:
  capture stock; project the added reservations
  calculate resulting availability for active menus
  retain only changed Menu values

IngredientDeleted.Handling:
  override retired stock as unavailable for future service
  project recipes with Drink.RetireIngredient (pure rule)
  calculate resulting Menu values

Handle:
  persist prepared values; do not re-read sibling state</code></pre>
    <div class="callout">All preparations precede all reactions. Independence comes from what is prepared, not from the barrier alone.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/menus/handlers/prepared.go">Code: app/domains/menus/handlers/prepared.go</a></p>
    <aside class="notes">The originating command has already written in the transaction. preparedMenus projects peer effects that have not happened yet, then applies only its own domain's values. It scans active draft/published menus to cover implicit substitutions, caches each drink calculation per preparation, references inspected menus, and records effects only for changed menus. Publication limits refresh to its own menu. TestRetirementPreparationIsIndependentOfEveryHandlerOrder and TestCancellationPreparationRecoversPeersInEveryHandlerOrder permute siblings. This scan is an explicit completeness/cost tradeoff, not a reverse index.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Dispatch snapshots the event list and wraps failures</h2>
    <pre><code class="language-go">if err := next(ctx); err != nil {
    return err
}
if d == nil {
    return nil
}
events := slices.Clone(ctx.Events())
for _, event := range events {
    if err := d.Dispatch(ctx, event); err != nil {
        return errors.Internalf("dispatch event %T: %w", event, err)
    }
}
return nil</code></pre>
    <div class="callout">A command failure prevents delivery. A delivery failure aborts the transaction. New events appended during delivery are outside this snapshot.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/middleware/dispatch_events.go">Code: pkg/middleware/dispatch_events.go</a></p>
    <aside class="notes">Exact core from DispatchEvents. The dispatcher is configured in app.New; the nil branch supports a pipeline without it. HandlerContext also omits AddEvent. Notice the explicit Internal wrapper on dispatch failure: classify the returned operation error before rendering it, while retaining the cause for investigation. Delivery is synchronous and has no retry queue.</aside>
  </section>


  <section class="implementation-slide">
    <h2>The preparation barrier is per event, not per command</h2>
    <pre><code class="language-text">command queues E1, then E2
  E1: construct fresh receivers
      all Handling calls
      all Handle calls
  E2: construct fresh receivers
      all Handling calls
      all Handle calls
  record successful activity
  commit

A failure stops remaining delivery and rolls back the operation.</code></pre>
    <div class="callout">Preparing E2 can observe effects of E1. Preparing handlers for E1 cannot assume another E1 handler has already reacted.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/middleware/dispatch_events.go">Code: pkg/middleware/dispatch_events.go</a></p>
    <aside class="notes">Trace DispatchEvents' sequential loop and one generated switch case. Handling sees the originating command's tentative writes, not a pre-command database snapshot. Its purpose is to capture dependencies before peer reactions erase them. It does not make arbitrary Handle reads order-independent; each consumer must preserve that property explicitly.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Unhandled events and durable delivery are different contracts</h2>
    <pre><code class="language-text">Known event, no matching reaction → debug log; success
Unknown event type               → debug log; success
Handler error                    → remaining delivery stops

Current delivery:
  synchronous Go calls
  one local transaction
  no durable event log, retry queue, or replay cursor</code></pre>
    <div class="callout">An event may be a valid extension point without subscribers. A successful dispatch does not prove that an intended handler was generated.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/dispatcher/dispatcher_test.go">Code: pkg/dispatcher/dispatcher_test.go</a></p>
    <aside class="notes">TestDispatcher_IgnoresUnknownEvents asserts this behavior. When adding a reaction, review generated wiring and verify a persisted business effect in an integration test. Audit records the operation and touched resources, not a replayable event stream. If a future requirement introduces durable asynchronous delivery, that is a different transaction and retry contract, not a configuration change to this dispatcher.</aside>
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
    <aside class="notes">A port is a small interface supplied by another component. Tagging needs to load a complete target for policy and find whether targets are active. Each domain registers functions that answer those questions using its own model and storage. Open app/app.go, app/domains/tagging, and one domain's tag-target registration. This adds registration work but avoids a tagging package that must know every domain's internals.</aside>
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
    <div class="callout">The domain command and <code>Tags.Replace</code> remain two normal pipeline commands with correlated audit activities, committed atomically together. Managed failure records one failed workflow after rollback.</div>
    <aside class="notes">Open app/tagged_mutation.go and its tests. Suppose a drink edit succeeds but removing a tag is denied. Two independent commits would leave a partially applied form. RunTaggedMutation validates the requested tag set, runs both commands with one transaction, and returns only after both succeed. A nil pointer means the caller made no tag request; a pointer to an empty set explicitly clears tags. The rollback test makes that distinction and the atomic outcome concrete.</aside>
  </section>

  <section>
    <h2>Discovery is its own authorized workflow</h2>
    <div class="cards"><div class="card"><h3>Show</h3><p>Find active entity references for an exact tag or every value of a key.</p></div><div class="card"><h3>Summary</h3><p>Aggregate canonical tags across active registered entity types.</p></div><div class="card"><h3>Policy</h3><p>Tagging-owned Cedar actions govern discovery; referenced entity authorization is not silently replayed.</p></div></div>
    <div class="callout">Inactive targets are excluded from discovery through each owner's registered bulk check. Stale association rows are not silently deleted.</div>
    <aside class="notes">This policy choice is different from per-entity catalog lists. Permission to discover tags governs disclosure of each matching target's type, ID, and display name; discovery does not also require that target's Get permission. Opening a target still goes through its normal domain boundary. State this deliberately so a viewer does not assume PageQuery's per-resource authorization rule describes every discovery workflow.</aside>
  </section>
  <section class="implementation-slide">
    <h2>The target registry contains capabilities, not domain models</h2>
    <pre><code class="language-go">type Target struct {
    Type        cedar.EntityType
    GetAction   cedar.EntityUID
    TagAction   cedar.EntityUID
    UntagAction cedar.EntityUID
    Load        LoadTarget
    Active      ActiveTargets
}
type TargetState struct {
    Entity      cedar.Entity
    DisplayName string
    Tags        tag.Tags
}</code></pre>
    <div class="callout">Ingredients supplies Load and Active. Tagging can authorize and discover targets without importing Ingredient or its DAO.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/tagging/registry.go">Code: app/domains/tagging/registry.go</a></p>
    <aside class="notes">Exact declarations. Open app/domains/ingredients/tagging.go: the registered loader parses the typed ID, calls the domain query, and returns value.CedarEntity(), value.Name, and value.Tags. Complete current tags matter because policy can interpret them. Registry.Register panics for incomplete or duplicate registrations during composition.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Replace derives authority from the tag delta</h2>
    <pre><code class="language-text">Current:  featured, region=west
Desired:  region=east, seasonal

region changes west → east  : requires tag
seasonal is added           : requires tag
featured is removed         : requires untag
──────────────────────────────────────────
authorize {tag, untag} against loaded state
replace associations
load complete resulting state
authorize {tag, untag} against result
record one tag activity</code></pre>
    <div class="callout">The stable audit action is tag; the authorization action set can include both tag and untag.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/tagging/module.go">Code: app/domains/tagging/module.go</a></p>
    <aside class="notes">Concrete example of replaceActions and LoadCommandActions. A user allowed to add a label is not automatically allowed to remove another one. Inspect the action derivation callback passed to LoadCommandActions and its before/after authorization loop. A permission failure rolls back the association replacement.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Two pipeline commands share one transaction</h2>
    <pre><code class="language-go">compose := func(txCtx *middleware.Context) error {
    var err error
    result, err = mutate(txCtx)
    if err != nil { return err }

    replaced, err := application.Tags.Replace(
        txCtx, result.EntityUID(), *desired, expected...,
    )
    if err != nil { return err }
    result.SetTags(replaced.Tags)
    return nil
}
err := middleware.RunWorkflow(ctx, application.Store,
    "tagged_mutation", audit.NewWriter(application.Store).RecordActivity,
    compose)</code></pre>
    <div class="callout">The domain command and tag command each authorize and audit. Returning an error from either prevents the outer transaction from committing.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/tagged_mutation.go">Code: app/tagged_mutation.go</a></p>
    <aside class="notes">Excerpt of the non-nil tag path. The full function validates tags first and joins an already supplied transaction rather than nesting another write. Show TestRunTaggedMutationRollsBackDomainMutationWhenTagReplacementFails. This is the shared application workflow invoked from each native surface, not a transaction opened by a widget.</aside>
  </section>


  <section class="implementation-slide">
    <h2>Protect the editor's intent, not only the latest row</h2>
    <pre><code class="language-text">Editor loads: entity revision=7; tags={region=west}
Another actor adds: seasonal
Editor submits: revision=7; tags={region=east}

The entity revision alone cannot detect the tag change.

RunTaggedMutation(..., expectedTags)
  domain command checks its captured revision
  Tags.Replace compares the expected complete tag set
  mismatch → Conflict → both changes roll back</code></pre>
    <div class="callout">SQLite serializes writes. It does not know that a stale form would erase someone else's intent.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/tagged_mutation.go">Code: app/tagged_mutation.go</a></p>
    <aside class="notes">Read Tags.Replace's variadic expected set and Session.TagReplacer. The expected set is optional in the module API: when supplied, a mismatch is rejected; omission performs replacement against current state. GUI/TUI editors capture their original tags. Do not infer the same stale-editor guarantee from a caller that omits expected tags. The checks may occur after a provisional domain write, but the shared transaction prevents partial commit. TestComposedEditorRejectsStaleTagsAndRollsBackDomainUpdate also verifies the failed workflow record.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Association identity belongs in a database invariant</h2>
    <pre><code class="language-text">target = (EntityType, EntityID)
association = (EntityType, EntityID, Key)

audience=sommelier → audience=bartender
  same association; replace Value

Repeat identical Upsert / Replace
  successful no-op; Changed=false

Repeat the same business command
  not automatically an idempotent request</code></pre>
    <div class="callout">The tag service's idempotent set semantics do not create system-wide command deduplication.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/tagging/repository.go">Code: app/domains/tagging/repository.go</a></p>
    <aside class="notes">Read the association row's compound unique store tag and repository Upsert/Replace tests. A label is represented by an empty Value, while Key remains the association identity. Changed controls whether the target is added to activity touches; the command can still produce an activity for a no-op. Do not infer request idempotency from deterministic target identity or from SQLite transaction atomicity.</aside>
  </section>
</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Foundation 2.3a</div><h1>Give people and programs one filter language</h1><p class="lede">Own exact expression semantics above storage, authorization, and every presentation surface.</p><div class="section-no">2.3a</div></section>

  <section>
    <h2>The schema is a public domain contract</h2>
    <div class="flow"><div class="node"><strong>typed filter view</strong>stable field names</div><div class="arrow">→</div><div class="node"><strong>Expr parser + checker</strong>accepted syntax</div><div class="arrow">→</div><div class="node"><strong>owned tree</strong>stable semantics</div><div class="arrow">→</div><div class="node"><strong>surface help</strong>fields + examples</div></div>
    <div class="callout">The filter view need not mirror a SQLite row or returned model. It can expose nested and hydrated values without leaking persistence.</div>
    <aside class="notes">A filter schema says which fields people can ask about and what those fields mean. Hydration means assembling a complete value from stored rows plus related data, such as tags. SQL pushdown means applying a safe part of the filter in the database to fetch fewer candidates. These are separate responsibilities: user syntax, exact matching, and storage optimization. Open pkg/filter/README.md and a domain's public filter view.</aside>
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
    <h2>Filtering and authorization compose in order</h2>
    <div class="flow"><div class="node"><strong>parse once</strong>typed invalid on error</div><div class="arrow">→</div><div class="node"><strong>filter + hydrate</strong>domain semantics</div><div class="arrow">→</div><div class="node"><strong>authorize each</strong>omit denied rows</div><div class="arrow">→</div><div class="node"><strong>page</strong>fill visible count</div></div>
    <div class="callout">Audit can use direct <code>ApplySQL</code> because its filter view comes from one row. Operational domains use staged hydration.</div>
    <p class="source"><a href="/articles/typed-filtering-over-sqlite/">Adjacent article: Typed Filtering over SQLite</a></p>
  </section>
  <section class="implementation-slide">
    <h2>The schema makes the query contract inspectable</h2>
    <pre><code class="language-go">type ListFilterView struct {
    Name string `expr:"name" filter:"Drink name" filter-column:"Name"`
    Tags []string `expr:"tags" filter:"Tags (key or key=value)"`
    Recipe RecipeFilterView `expr:"recipe"`
}
type RecipeFilterView struct {
    Garnish string `expr:"garnish" filter:"Recipe garnish"`
}

expr, err := filter.Parse(models.ListFilterSchema(),
    `name == "Daiquiri" &amp;&amp; tags contains "featured"`)</code></pre>
    <div class="callout">Name has a persisted column mapping. Tags and recipe.garnish are part of the public language without claiming that same storage representation.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/drinks/models/filter.go">Code: app/domains/drinks/models/filter.go</a></p>
    <aside class="notes">Selected actual fields plus a Parse call using the full repository schema. Struct tags support both validation and help output. filter-column is an optimization promise, so giving a hydrated field a misleading column mapping can change results. Show invalid field/type errors before moving into the planner.</aside>
  </section>

  <section class="implementation-slide">
    <h2>The DAO hydrates before the final predicate</h2>
    <pre><code class="language-go">// Inside the row loop, after tags were loaded in one batch:
drink, err := toModel(row)
if err != nil { return err }
drink.Tags = tagsByTarget[drink.EntityUID()]
matched, err := filter.Expression.Match(
    listFilterView(row, drink.Tags.Strings()),
)
if err != nil { return err }
if !matched { continue }
if !yield(&amp;drink, nil) { return nil }</code></pre>
    <div class="callout">SQL only reduces candidates. Match evaluates the complete value; PageQuery then decides which matched entities the actor may see.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/drinks/internal/dao/list.go">Code: app/domains/drinks/internal/dao/list.go</a></p>
    <aside class="notes">Reflowed excerpt from DAO.List. Inspect d.query to find ApplySQLPushdowns. The current implementation materializes candidate rows with List and batches tag hydration before yielding, so do not describe this as a database cursor that streams exactly one page. Permission-aware paging can scan more candidates than the visible page size. This tradeoff keeps exact semantics explicit while leaving room for a later storage optimization.</aside>
  </section>

</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Deep dive 2.3b</div><h1>Prove filter optimization preserves meaning</h1><p class="lede">A checked expression is a language contract. SQL pushdowns are conservative candidate selectors, not a second definition of matching.</p><div class="section-no">2.3b</div><aside class="notes">Follow the public filter walkthrough with logical counterexamples, actual optimizer control flow, and tests. This recording explains the proof obligation behind each optimization.</aside></section>

  <section class="implementation-slide">
    <h2>A pushdown must be necessary, not merely useful</h2>
    <pre><code class="language-text">E = the complete expression on a hydrated domain view
P = the predicates applied to persisted rows

Required safety property:
  E(record) = true  ⇒  P(row) = true

Candidate rows may include false positives.
A false negative cannot be recovered by later hydration.

Final result = candidates that satisfy E</code></pre>
    <div class="callout">The optimizer may do less work. It may not change which records the expression means.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/filter/sql.go">Code: pkg/filter/sql.go</a></p>
    <aside class="notes">Explain implication with an unsafe OR before opening code. A SQL predicate that drops a valid row is not repaired by running Match afterward. filter-column is a semantic promise: the persisted field must represent the same value as the public filter field. The optimizer is conservative, not a general theorem prover.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Walk the OR counterexample with two rows</h2>
    <pre><code class="language-text">Expression:
  category == "spirit" || name == "Beer"

Rows:
  Gin   / spirit → true from the left branch
  Beer  / mixer  → true from the right branch

Unsafe SQL: WHERE Category = 'spirit'
  drops Beer, which satisfies the full expression

Current behavior: retain both candidates; evaluate the OR</code></pre>
    <div class="callout">Neither branch alone is a requirement of the whole OR.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/filter/sql_test.go">Code: pkg/filter/sql_test.go</a></p>
    <aside class="notes">This is the data and expression from TestApplySQLDoesNotPushUnsafeOR. Show both returned rows in the test, not only the AST. Contrast it with AND, where each conjunct is necessary. Some constraints common to both OR branches are safe, which is the next case.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Widen alternatives only when both constrain the same field</h2>
    <pre><code class="language-text">(category == "spirit" &amp;&amp; tags contains "featured")
||
(category == "mixer" &amp;&amp; tags contains "seasonal")

Safe candidate constraint:
  Category IN ("spirit", "mixer")

Still requires exact matching:
  a spirit tagged only seasonal must be rejected
  a mixer tagged only featured must be rejected</code></pre>
    <div class="callout">The widened candidate set deliberately forgets which tag belongs to which branch. The residual expression restores that relationship.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/filter/sql.go">Code: pkg/filter/sql.go</a></p>
    <aside class="notes">TestApplySQLPushdownsExtractNecessaryORConstraints proves candidate narrowing. disjunctionPushdowns preserves equivalent predicates and unions compatible equality values for a shared column. It does not generally combine differing range predicates. Returning the candidate set directly would admit cross-branch false positives.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Negation changes the connective before extracting constraints</h2>
    <pre><code class="language-text">if node.Kind == KindUnary &amp;&amp; node.Operator == "!" {
    return e.impliedPushdowns(node.Children[0], !negated)
}
// For a binary boolean node under negation:
// &amp;&amp; becomes ||; || becomes &amp;&amp;
// comparison leaves use negateComparison

!(category == "spirit" || category == "mixer")
  ⇒ Category != "spirit" AND Category != "mixer"

!(category == "spirit" &amp;&amp; tags contains "featured")
  ⇒ no category-only constraint is necessary</code></pre>
    <div class="callout">Negating a conjunction does not let us push down the negation of whichever field happens to be stored.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/filter/sql.go">Code: pkg/filter/sql.go</a></p>
    <aside class="notes">Abbreviated control flow from impliedPushdowns; its actual unary branch also checks child count. Trace De Morgan through the two examples. Negated supported comparison leaves can produce predicates, but a hydrated tag branch may leave no common condition under OR. The complete expression remains unchanged for exact evaluation.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Own the supported language even when borrowing its compiler</h2>
    <pre><code class="language-go">program, err := expr.Compile(source,
    expr.Env(zero),
    expr.AsBool(),
    expr.Optimize(false),
    expr.Patch(dotPredicatePatcher{}),
    expr.Patch(collectionContainsPatcher{fields: collectionFields(schema)}),
)
// Compile errors become Invalid.
tree, err := buildTree(program.Node())
// Unsupported constructs also become Invalid.

// Source: user's trimmed text
// String: canonical syntax
// Tree:   application-owned nodes, not Expr AST</code></pre>
    <div class="callout">Successful library compilation is only the first gate. The owned tree restricts the language the application promises to support.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/filter/filter.go">Code: pkg/filter/filter.go</a></p>
    <aside class="notes">Selected Parse code; error branches are described in comments. String-method spelling and collection membership are normalized, then buildTree rejects unsupported constructs. Accepted language excludes arbitrary functions and arithmetic; regex patterns and date/duration literals are checked. A compiler upgrade must preserve these semantics, canonical formatting, evaluation, and pushdown behavior together.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Test candidate safety and final truth separately</h2>
    <pre><code class="language-text">TestApplySQLPushdownsDeferHydratedFields:
  three stored rows → two spirit candidates
  attach tags → Match the complete view

TestApplySQLDoesNotPushUnsafeOR:
  Gin/spirit and Beer/mixer must both survive

TestApplySQLPushdownsExtractNecessaryORConstraints:
  alternative categories produce a safe widened set

TestApplySQLPushdownBooleanSemantics:
  negation and boolean columns keep their meaning</code></pre>
    <div class="callout">An optimization test should prove both that no true match is lost and that residual false positives are rejected.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/filter/sql_test.go">Code: pkg/filter/sql_test.go</a></p>
    <aside class="notes">Run go test ./pkg/filter -count=1. ApplySQL installs an exact FilterFn and panics if its supposedly checked expression fails at runtime; the staged domain path instead calls Match explicitly and propagates its error. Neither path should silently interpret an evaluator failure as a non-match. The suite covers candidate extraction and exact evaluation through distinct tests.</aside>
  </section>
</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Foundation 2.4a</div><h1>Keep storage mechanics behind domain contracts</h1><p class="lede">Domain DAOs own persistence mapping. The shared SQLite store supplies transactions, concurrency checks, and change signals for all three interfaces.</p><div class="section-no">2.4a</div></section>

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
    <h2>A change notification means “query again”</h2>
    <div class="flow"><div class="node"><strong><code>data_version</code></strong>detect another connection's commit</div><div class="arrow">→</div><div class="node"><strong><code>Signals</code></strong>wake the client</div><div class="arrow">+</div><div class="node"><strong><code>Epoch</code></strong>remember a change occurred</div><div class="arrow">→</div><div class="node"><strong>ordinary query</strong>reload authorized state</div></div>
    <div class="callout">Several changes can share one notification. The increasing epoch lets a client notice missed changes and re-query through normal authorization and filtering.</div>
    <aside class="notes">Contrast this with the synchronous domain events from chapter 2.1. Database notifications happen after commits and contain no business payload. They keep clients fresh; they do not perform domain reactions. Preserve an active editor until its workflow finishes. A refresh signal protects display freshness, an opaque revision protects writes, and a request token prevents an older async result from replacing a newer display. Each solves a different race.</aside>
  </section>

  <section>
    <h2>Treat the file format honestly</h2>
    <div class="cards"><div class="card"><h3>Migration ledger</h3><p>Ordered migrations advance deliberately; a database from a newer schema is rejected.</p></div><div class="card"><h3>Registration</h3><p>Explicit model schemas fail early; imports do not mutate global persistence state.</p></div><div class="card"><h3>Errors</h3><p>Constraints and stale revisions become application kinds, not leaked driver strings.</p></div></div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/store/README.md">Code guide: pkg/store/README.md</a></p>
  </section>
  <section class="implementation-slide">
    <h2>The SQLite storage shape is more specific than “tables”</h2>
    <pre><code class="language-sql">-- Selected SQL actually issued by the store:
INSERT INTO records(model, id, data, revision)
VALUES (?, ?, ?, 1);

SELECT data, revision
FROM records
WHERE model = ? AND id = ?;

UPDATE records
SET data = ?, revision = revision + 1
WHERE model = ? AND id = ? AND revision = ?;</code></pre>
    <div class="callout">The generic store keeps typed row data as JSON in records, partitioned by model identity. Domain DAOs still own conversion and query meaning.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/store/query.go">Code: pkg/store/query.go</a></p>
    <aside class="notes">SQL statements selected from query.go. Open store.go to inspect schema migrations and model registration, then query.go for JSON-backed predicates and indexes. This is not one hand-designed SQL table per aggregate. The replaceable boundary preserves the application contract, while this particular engine adapter makes a concrete representation choice.</aside>
  </section>

  <section class="implementation-slide">
    <h2>A stale revision becomes a typed conflict</h2>
    <pre><code class="language-go">n, _ := r.RowsAffected()
if n == 0 {
    var current uint64
    err := t.tx.QueryRowContext(t.ctx,
        "SELECT revision FROM records WHERE model=? AND id=?",
        modelName(typ), idString(id),
    ).Scan(&amp;current)
    if errors.Is(err, sql.ErrNoRows) {
        return errors.NotFoundf("record absent")
    }
    if err != nil { return err }
    return errors.Conflictf(
        "record changed: expected revision %d, current revision %d",
        revision, current)
}</code></pre>
    <div class="callout">Zero updated rows can mean absence or a stale edit. The store distinguishes those meanings before the DAO maps them to its own operation context.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/store/query.go">Code: pkg/store/query.go</a></p>
    <aside class="notes">Reflowed exact branch following the conditional UPDATE. Success calls setRevision(v, revision+1). Open drinks/internal/dao/update.go: toRow carries the revision, MapError adds the operation message, and drink.Revision receives the new token after success. MapError's Conflict branch preserves the kind but replaces the lower-level message, so not every surface displays the expected/current numbers.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Three counters protect three different races</h2>
    <pre><code class="language-text">Database change epoch:
  commit observed → epoch increases → cached screen becomes stale

UI request generation:
  load A starts → load B starts → A finishes late → A is ignored

Entity revision:
  read revision 7 → another writer saves revision 8
  submit revision 7 → conditional UPDATE changes 0 rows → Conflict</code></pre>
    <div class="callout">An epoch is a refresh hint, a generation selects a result, and a revision guards a write. None substitutes for the others.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/store/changes.go">Code: pkg/store/changes.go</a></p>
    <aside class="notes">Trace the epoch in pkg/store/changes.go, generation in pkg/toolkits/gui/async.go, and revision in pkg/store/query.go. The change monitor polls a dedicated connection's PRAGMA data_version. Compare values on that connection, not as a global sequence shared by all processes. A re-query still passes through authorization.</aside>
  </section>

</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Deep dive 2.4b</div><h1>Coordinate persistence across processes</h1><p class="lede">Write acquisition, schema evolution, row identity, and invalidation each have a distinct consistency contract.</p><div class="section-no">2.4b</div><aside class="notes">Follow chapter 2.4a's storage API and revision examples into the engine adapter and cross-process observation. Keep durable events separate from lossy refresh notifications.</aside></section>

  <section class="implementation-slide">
    <h2>Acquire write intent before reading mutation state</h2>
    <pre><code class="language-text">Store.Begin(ctx, writable=true):
  pin a connection
  BEGIN IMMEDIATE
  return a Tx using that connection

Command:
  load current state
  authorize → mutate → authorize result
  dispatch → audit → COMMIT

Competing writer waits or returns an error at acquisition.</code></pre>
    <div class="callout">The loaded authorization state and the mutation share one write transaction. WAL does not make SQLite a multi-writer database.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/store/store.go">Code: pkg/store/store.go</a></p>
    <aside class="notes">Trace Store.Begin and UnitOfWork. Immediate acquisition avoids starting with a read snapshot that later cannot be upgraded after another writer commits. Readers on other WAL connections can continue seeing their own snapshots. Long handlers extend the sole writer's occupancy. SQLite isolation details: https://www.sqlite.org/isolation.html. Cancellation and busy timeout can still make acquisition fail.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Persistent identity includes the Go row type</h2>
    <pre><code class="language-text">func modelName(t reflect.Type) string {
    return t.PkgPath() + "." + t.Name()
}

records primary key:
  (model, id)

Example model discriminator:
  .../app/domains/drinks/internal/dao.DrinkRow

Domain values ↔ row conversion ↔ JSON-backed record</code></pre>
    <div class="callout">A package or row-type rename can be a data migration, not just a refactor.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/store/store.go">Code: pkg/store/store.go</a></p>
    <aside class="notes">Exact modelName. Open the real row type to confirm its name when walking the database. The model discriminator partitions records and expression indexes within the shared records table. Changing a persisted JSON field name or its interpretation also requires compatibility review. Explicit registration describes storage, but does not automatically migrate data between model names.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Migration startup is itself a coordinated write</h2>
    <pre><code class="language-text">BEGIN IMMEDIATE
  CREATE TABLE IF NOT EXISTS schema_migrations
  read highest version and applied count
  reject a version newer than this binary understands
  reject a non-contiguous ledger
  apply each outstanding statement
  record each version in the same transaction
COMMIT

On error: rollback using a non-cancelled cleanup context.</code></pre>
    <div class="callout">Two starting processes must agree on the same schema transition. Recording a version separately from its schema change would break that guarantee.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/store/store.go">Code: pkg/store/store.go</a></p>
    <aside class="notes">Trace migrate in store.go and TestConcurrentMigrationInitialization. The implementation checks highest version and count before applying its ordered migrations. TestMigrationVersionBookkeepingAndFutureVersion and TestRevisionMigrationUpgradesExistingRows exercise compatibility behavior. This is current startup behavior, not a historical engine-migration walkthrough.</aside>
  </section>

  <section class="implementation-slide">
    <h2>The monitor pins the connection whose counter it compares</h2>
    <pre><code class="language-text">conn, version := openChangeConnection(...)
repeat:
  current := dataVersion(conn)
  if current != version:
    version = current
    publish invalidation

If the connection fails:
  reconnect with backoff
  establish a new baseline
  publish anyway: changes may have occurred in the gap</code></pre>
    <div class="callout">A data_version value is meaningful across observations on the same connection. It is not a global commit sequence.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/store/changes.go">Code: pkg/store/changes.go</a></p>
    <aside class="notes">Control-flow summary of changes.go, not Go pseudocode intended to compile. The pinned connection observes commits by other connections, including this process's writer connections. A reconnect invalidates even without a comparable old counter. Backoff starts at 25 ms and caps at one second. SQLite documents the per-connection comparison contract at https://www.sqlite.org/pragma.html#pragma_data_version.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Coalescing drops edges but retains an invalidation level</h2>
    <pre><code class="language-go">func (m *ChangeMonitor) publish() {
    m.epoch.Add(1)
    select {
    case m.signals &lt;- struct{}{}:
    default:
    }
}

// signals has capacity one.
// Epoch counts monitor publications, not database commits.
// A signal carries no entity ID or business payload.</code></pre>
    <div class="callout">A full notification channel must not block the writer-observation loop. Consumers reload state rather than reconstructing changes.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/store/changes.go">Code: pkg/store/changes.go</a></p>
    <aside class="notes">Exact publish implementation. Multiple commits may be noticed in one poll, and multiple monitor publications may occupy one queued signal. Epoch therefore cannot count commits or identify changed resources. The TUI owns deferred invalidation while editing; GUI activation/refresh also re-queries through the application. Do not describe this as a durable event bus or promise one callback per write.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Prove commit visibility using two store instances</h2>
    <pre><code class="language-text">reader := Open(path)
writer := Open(path)
monitor := reader.MonitorChanges(...)

writer.Write(insert "committed")
  → monitor signals
  → Epoch &gt; 0

tx := writer.Begin(writable=true)
tx.Insert("rolled back")
writer.Rollback(tx)
  → no invalidation for that rollback</code></pre>
    <div class="callout">Use separate connections to test freshness. Reading your own uncommitted write proves a different property.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/store/changes_test.go">Code: pkg/store/changes_test.go</a></p>
    <aside class="notes">Scenario from TestChangeMonitorSignalsCommittedWritesAndIgnoresRollback; error handling and timing bounds omitted. TestIndependentStoresShareOneDatabase separately verifies shared persistence, and GUI integration tests prove a client reacts to external commits. A monitor-only test is not evidence that an active editor survives refresh or that a UI publishes on its correct thread.</aside>
  </section>
</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Domain workshop 3.1a</div><h1>Follow an order as reality changes</h1><p class="lede">Reservations, stock corrections, and ingredient retirement connect the architecture to business behavior.</p><div class="section-no">3.1a</div></section>

  <section>
    <h2>Placing an order creates a commitment</h2>
    <div class="layers"><div class="layer"><strong>Orders decides</strong><span>Validate the published menu and requested drinks, choose ingredient usage, and save the accepted snapshot.</span></div><div class="layer"><strong>Inventory reacts</strong><span>Reserve every included quantity, including optionals, when it receives <code>OrderPlaced</code>.</span></div><div class="layer"><strong>Menus reacts</strong><span>Recalculate published availability as stock becomes committed.</span></div><div class="layer"><strong>Pipeline finishes</strong><span>Record touched entities and the successful activity, then commit all writes together.</span></div></div>
    <div class="callout">If any reservation fails, the order and earlier reservation writes roll back together.</div>
    <aside class="notes">Code walk: orders/place.go → orders/internal/commands/place.go → inventory/handlers/order-placed.go and menus/handlers/order-placed.go. The facade enters the pipeline before the command runs. The command inserts an Order and queues OrderPlaced. Dispatch runs before success audit and commit. Read the fulfillment tests alongside this trace to show that a dependency failure remains an error rather than becoming a misleading stock shortage.</aside>
  </section>

  <section>
    <h2>Reserved stock is different from consumed stock</h2>
    <table class="matrix"><thead><tr><th>Example, in one unit</th><th>On hand</th><th>Reserved</th><th>Available</th></tr></thead><tbody><tr><td>Before an order</td><td>10</td><td>0</td><td>10</td></tr><tr><td>Place an order requiring 4</td><td>10</td><td>4</td><td>6</td></tr><tr><td>Complete that order</td><td>6</td><td>0</td><td>6</td></tr><tr><td>Or cancel it instead</td><td>10</td><td>0</td><td>10</td></tr></tbody></table>
    <div class="callout">Placement protects a future commitment. Completion consumes stock. Cancellation releases the commitment.</div>
    <aside class="notes">Completion and cancellation are alternative outcomes from the placed state. Keep the same ingredient and unit throughout the example. Inventory owns reservation storage; Orders owns the lifecycle decision that emits the event. The snapshot preserves the concrete ingredients accepted at placement, even if someone edits the recipe later.</aside>
  </section>

  <section>
    <h2>Stock corrections flow back to Orders</h2>
    <div class="state-line"><div class="state active">pending</div><div class="arrow">→</div><div class="state review">stock below reservations</div><div class="arrow">→</div><div class="state blocked">blocked</div></div>
    <div class="cards two"><div class="card"><h3>Replenish</h3><p>Inventory emits another adjustment. An order returns to pending when none of its committed ingredients remain blocked.</p></div><div class="card"><h3>Cancel</h3><p>A blocked order can be cancelled to release reservations and reconcile peers. It cannot be completed.</p></div></div>
    <div class="callout">Orders → Inventory and Inventory → Orders are separate business operations with leaf reactions, not an event cascade.</div>
    <aside class="notes">Continue the numerical example: correct on-hand stock from 10 to 3 while 4 is reserved. The system preserves the reservation and blocks affected orders instead of claiming they can be fulfilled. Open orders/handlers/stock-adjusted.go and TestReservationShortageBlocksRestockUnblocksAndCancellationReleases in orders/reservation_lifecycle_test.go. Several ingredients may block one order; replenishing one must not clear the others.</aside>
  </section>

  <section>
    <h2>A substitute must satisfy the whole recipe</h2>
    <div class="split"><div class="side"><h3>Local choice</h3><p>Requirement A can use X or Y. Requirement B can use only X. There is enough X for one requirement.</p><p>Choosing X for A first leaves B unfulfilled.</p></div><div class="bridge">→</div><div class="side"><h3>Complete plan</h3><p>Try Y for A and reserve X for B. Compare quantities in compatible units and account for conversion ratios.</p><p>Accept a plan only when every requirement fits.</p></div></div>
    <div class="callout">The planner backtracks when a preferred substitute prevents a complete solution. The accepted order keeps the resulting usage snapshot.</div>
    <aside class="notes">Open PlanIngredients in menus/internal/availability/calculator.go and TestCompleteOrderBacktracksWhenPreferredSubstituteIsShared in orders/fulfillment_test.go. The reserved map here is temporary planning state; Inventory later persists actual reservations in its event handler. Keeping both ideas distinct explains why planning alone cannot protect stock from a competing operation.</aside>
  </section>

  <section>
    <h2>Retirement is a business decision</h2>
    <table class="matrix"><thead><tr><th>Reference</th><th>No replacement</th><th>Permanent replacement</th></tr></thead><tbody><tr><td>Required recipe component</td><td class="maybe">keep visible, review required</td><td class="yes">rewrite compatible future recipe</td></tr><tr><td>Optional component</td><td class="yes">remove from future recipe</td><td class="yes">rewrite when compatible</td></tr><tr><td>Pending order using retired ingredient</td><td class="maybe" colspan="2">discontinue: honor reservations; withdraw: block; preserve acceptance</td></tr><tr><td>Published menu item</td><td class="maybe" colspan="2">preserve curation and recalculate current availability</td></tr></tbody></table>
    <aside class="notes">Retirement excludes an ingredient from future service. Discontinuation honors usable accepted reservations; explicit withdrawal quarantines stock and blocks affected open orders. Removing the final optional component leaves the empty recipe requiring review. A manager may explicitly approve a compatible replacement; matching category and units validate mechanical compatibility, while the manager supplies product judgment. Completed historical orders are not rewritten or newly blocked. Open drinks/handlers/handlers_test.go and the retirement test in orders/reservation_lifecycle_test.go to compare future recipe intent with an outstanding accepted commitment.</aside>
  </section>

  <section>
    <h2>Three substitutions, three meanings</h2>
    <div class="cards"><div class="card"><h3>Recipe substitute</h3><p>A modeled alternative inside the drink. It is not permission to rewrite the canonical recipe.</p></div><div class="card"><h3>Operational substitution</h3><p>A temporary way to fulfill a drink. It affects readiness and availability.</p></div><div class="card"><h3>Permanent replacement</h3><p>Explicit retirement intent carried by the source event, including conversion.</p></div></div>
    <p class="source"><code>IngredientDeleted{Replacement, ReplacementRatio}</code> carries explicit permanent intent.</p>
    <div class="callout">Similarity is not intent. Consumers must not infer permanent replacement from whatever substitute happens to be available.</div>
  </section>

  <section>
    <h2>Rewrite plans. Preserve records.</h2>
    <div class="split"><div class="side"><h3>Future recipe</h3><p>An approved replacement changes what future orders will use. A recipe without a valid replacement may require review.</p><p class="accent">Recipe edits express future intent.</p></div><div class="bridge">∥</div><div class="side"><h3>Accepted order</h3><p>The usage snapshot keeps the ingredients selected when the order was placed.</p><p class="gold">An outstanding order can be blocked; its snapshot stays intact.</p></div></div>
  </section>

  <section>
    <h2>Staying published and becoming published differ</h2>
    <div class="state-line"><div class="state active">published</div><div class="arrow">→</div><div class="state review">degraded but honest</div><div class="arrow">│</div><div class="state">draft</div><div class="arrow coral">⤫</div><div class="state blocked">known-bad publish</div></div>
    <div class="cards two"><div class="card"><h3>Existing published menu</h3><p>May remain published while item availability reflects new operational truth.</p></div><div class="card stop"><h3>Draft promotion</h3><p>Readiness blockers prevent publishing state already known to be unsuitable.</p></div></div>
  </section>

  <section>
    <h2>Readiness belongs to Menus</h2>
    <div class="flow"><div class="node"><strong>Load menu</strong>authorized state</div><div class="arrow">→</div><div class="node"><strong>Evaluate</strong>recipes + stock</div><div class="arrow">→</div><div class="node"><strong>Report</strong>blockers + warnings</div><div class="arrow">→</div><div class="node"><strong>Publish</strong>re-check in command</div></div>
    <div class="cards two"><div class="card stop"><h3>Blockers</h3><p>Invalid canonical state, unavailable items, or temporary substitution.</p></div><div class="card warn"><h3>Warnings</h3><p>Operational concerns such as low stock that deserve visibility but not a false invariant.</p></div></div>
    <aside class="notes">Code walk: menus/readiness.go, its publication command, and menus/internal/availability/calculator.go. Demonstrate a healthy published menu, then retire a required ingredient. The menu remains published but reports degraded availability; trying to publish a draft with that problem fails. Readiness is an authorized report and the Publish command checks again. A temporary substitute may support service without approving a new canonical recipe.</aside>
  </section>
  <section class="implementation-slide">
    <h2>Place saves the concrete fulfillment plan</h2>
    <pre><code class="language-go">usage, err := c.fulfillmentSnapshot(ctx, created)
if err != nil { return nil, err }
created.IngredientUsage = usage

if err := created.Validate(); err != nil {
    return nil, err
}
if err := c.dao.Insert(ctx, &amp;created); err != nil {
    return nil, err
}
ctx.RecordEffect("order_placed", created.ID.EntityUID(),
    middleware.Change("acceptance", "", created.Acceptance))
ctx.AddEvent(events.OrderPlaced{Order: created})
return &amp;created, nil</code></pre>
    <div class="callout">The event carries the accepted usage snapshot. Inventory reserves those exact quantities; it does not plan the recipe again.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/orders/internal/commands/place.go">Code: app/domains/orders/internal/commands/place.go</a></p>
    <aside class="notes">Excerpt after ID, status, menu, and item validation. Open inventory/handlers/order-placed.go next: each usage becomes a Reservation with OrderID, IngredientID, and Amount. Then inspect order completion to see it consumes the stored reservation. Future recipe edits must not silently change an already accepted order.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Readiness is both a report and a command precondition</h2>
    <pre><code class="language-go">if err := menu.RequirePublishable(); err != nil {
    return nil, err
}
report, err := c.availability.Readiness(ctx, menu)
if err != nil { return nil, err }
if err := report.RequireReady(); err != nil {
    return nil, err
}

// Only after those checks:
updated := *menu
updated.Status = models.MenuStatusPublished
updated.PublishedAt = optional.Some(now)</code></pre>
    <div class="callout">Report findings have severity, code, entity IDs, and a message. RequireReady turns blocker messages into a typed FailedPrecondition.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/menus/internal/commands/publish.go">Code: app/domains/menus/internal/commands/publish.go</a></p>
    <aside class="notes">Selected command lines; now is captured with time.Now().UTC() in the source. Open models/readiness.go and compare a low_stock warning with review_required_drink. The manager can inspect the same findings before submission, but Publish computes them again in the transaction. Do not conflate menu availability's degradation behavior with every error path in the stricter command.</aside>
  </section>

</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Domain deep dive 3.1b</div><h1>Allocate shared stock without breaking commitments</h1><p class="lede">Fulfillment combines deterministic search, unit conversion, accepted snapshots, and transactional reservations.</p><div class="section-no">3.1b</div><aside class="notes">Use one adversarial recipe to connect the allocation algorithm to cross-domain ownership. Trace choices in Menus, accepted intent in Orders, and durable reservations in Inventory. Finish with error semantics and search limits.</aside></section>

  <section class="implementation-slide">
    <h2>Plan the whole order, not each drink independently</h2>
    <pre><code class="language-text">for each order item:
  load its recipe
  retain optional ingredients as optional requirements
  multiply each amount by item quantity
  append to one requirements slice

menus.FulfillIngredients(ctx, requirements)
  → PlanIngredients across the complete slice

Aggregate picks by ingredient ID
  → sort the resulting IngredientUsage snapshot</code></pre>
    <div class="callout">Two independently feasible recipes can compete for the same stock. The planning scope must match the accepted commitment.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/orders/internal/commands/complete.go">Code: app/domains/orders/internal/commands/complete.go</a></p>
    <aside class="notes">Trace fulfillmentSnapshot in orders/internal/commands/complete.go; despite that filename, Place calls it when creating the order. It gathers requirements across all items, invokes the shared Menus planning query, combines amounts for repeated selected ingredients, and sorts by ID. Placement stores the snapshot; completion consumes the resulting reservations rather than replanning against changed recipes.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Candidate preference is deterministic, not arbitrary</h2>
    <pre><code class="language-text">Build candidates:
  original ingredient
  explicit recipe substitutes, with catalog ratios when present
  remaining catalog rules, deduplicated by ingredient ID

Keep candidates with enough individually available stock.

Sort:
  original before substitute
  higher quality rank
  greater available amount
  ingredient ID as final tie-break</code></pre>
    <div class="callout">A preference ranks choices. It does not prove the preferred choice permits a complete allocation.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/menus/internal/availability/calculator.go">Code: app/domains/menus/internal/availability/calculator.go</a></p>
    <aside class="notes">Trace availableCandidates. Requirements are scaled by the catalog substitution ratio; explicit substitutes without a catalog rule use ratio 1 and Similar quality. Inventory NotFound removes a candidate, while other lookup or conversion errors propagate in the strict planner. The algorithm uses its declared ordering rather than a global price or quality objective. Available quantities are converted to the requirement unit before comparison.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Force a choice that a greedy planner cannot repair</h2>
    <pre><code class="language-text">Requirements, each 1 oz:
  A can use Shared or Fallback
  B can use Shared only

Available: Shared=1.5 oz, Fallback=1 oz
Both substitutes have the same quality.

Try A=Shared:
  B would need total Shared=2 oz → impossible

Undo A's reservation.
Try A=Fallback, then B=Shared → complete plan</code></pre>
    <div class="callout">Rejecting the order at the first dead end would report a shortage even though a valid plan exists.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/orders/fulfillment_test.go">Code: app/domains/orders/fulfillment_test.go</a></p>
    <aside class="notes">Illustrative adversarial variant of the repository's shared-substitute fixture, executed through Place and Complete during this pass. Candidate preference selects Shared first because its available amount is greater. Reversing which requirement has the fallback forces recursion to undo an earlier assignment, rather than merely skip an overcommitted candidate in the final requirement.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Backtracking restores the tentative reservation map</h2>
    <pre><code class="language-go">// Inside assign(index), after checking available stock.
selected[index] = pick
reserved[key] = total
if assign(index + 1) {
    return true
}
if hadPrior {
    reserved[key] = prior
} else {
    delete(reserved, key)
}

// No candidate works at this index.
return false</code></pre>
    <div class="callout">The map is search-local bookkeeping, not persisted Inventory reservations. Undoing a branch must restore the exact prior amount.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/menus/internal/availability/calculator.go">Code: app/domains/menus/internal/availability/calculator.go</a></p>
    <aside class="notes">Selected statements from PlanIngredients, with the enclosing candidate loop omitted; the final false return occurs after that loop is exhausted. Earlier code converts prior amounts into the current requirement's unit and adds the candidate requirement before comparing against pick.Available. Each recursive step records total usage by ingredient ID. A true return is the first complete feasible assignment in deterministic candidate order. The map is discarded when planning returns.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Follow the selected plan into persisted inventory</h2>
    <pre><code class="language-text">Adversarial fixture:
  A candidates: Shared, Fallback
  B candidates: Shared
  Shared=1.5 oz; Fallback=1 oz

After Place:
  IngredientUsage: Fallback=1 oz, Shared=1 oz
  two Inventory reservations
  on-hand amounts unchanged

After Complete:
  Shared on hand=0.5 oz; Fallback on hand=0 oz
  order reservations removed</code></pre>
    <div class="callout">A solver result matters only if the accepted snapshot and later inventory effects preserve that choice.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/orders/fulfillment_test.go">Code: app/domains/orders/fulfillment_test.go</a></p>
    <aside class="notes">Observed through a temporary verification test using the real application fixture, domain commands, dispatcher, and SQLite store. The shipped fulfillment tests also cover catalog ratio, quality preference, shared-stock accounting, and insufficient shared substitutes. The plan does not silently rewrite either recipe, and completion does not choose a different substitute after acceptance.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Optional means omittable, not unaccounted for</h2>
    <pre><code class="language-go">// After all candidate branches at this index fail:
if requirements[index].Optional {
    selected[index] = PickResult{Omitted: true}
    if assign(index + 1) {
        return true
    }
}
return false

// Included optional: snapshot → reserve → consume → cost.
// Omitted optional: explicit selection with Omitted=true.</code></pre>
    <div class="callout">The planner can undo an optional choice to make a required ingredient fit. It must never consume an omitted ingredient.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/menus/internal/availability/calculator.go">Code: app/domains/menus/internal/availability/calculator.go</a></p>
    <aside class="notes">Exact optional branch with surrounding search omitted. Candidate picks are tried before omission, but a later required shortage backtracks into the omission branch. TestOptionalCannotStarveRequiredAndSnapshotsSurviveCatalogEdits creates this contention; TestOptionalIngredientIsReservedAndConsumed verifies included stock. Readiness uses required ingredients to decide serviceability, while acceptance and costing account for included optionals. There is no unbounded optional garnish consumption.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Cost a feasible plan in its price unit</h2>
    <pre><code class="language-text">Whole recipe → PlanIngredients once
For each included pick:
  load the chosen stock
  convert required quantity into stock.CostUnit
  multiply by CostPerUnit
  accumulate matching-currency prices

Omitted optional → no cost
Missing price    → unknown, not zero
No complete plan → FailedPrecondition</code></pre>
    <div class="callout">A cheap per-line choice is meaningless if two lines spend the same scarce substitute.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/menus/queries/cost.go">Code: app/domains/menus/queries/cost.go</a></p>
    <aside class="notes">Calculate holds one read transaction and uses the same whole-recipe planner as fulfillment. It estimates the current recipe; order placement plans the whole order and captures agreed menu prices, so this is not a promise of identical plans across different scopes or later snapshots. Margin analytics require matching currencies. Price basis is independent of stock display unit.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Inventory rechecks availability when reserving</h2>
    <pre><code class="language-go">// Reserve, inside the originating command transaction.
requested, err := reservation.Amount.Convert(stockUnit)
// Conversion errors propagate.
reserved := sum(existingReservationRows)
if stock.Quantity-reserved &lt; requested.Value() {
    return errors.FailedPreconditionf(/* shortage details */)
}
return tx.Insert(&amp;ReservationRow{
    ID: reservationID(orderID, ingredientID),
    // OrderID, IngredientID, Quantity, Unit
})</code></pre>
    <div class="callout">Planning chooses a feasible usage snapshot. Inventory remains the owner of the durable reservation invariant.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/inventory/internal/dao/reservations.go">Code: app/domains/inventory/internal/dao/reservations.go</a></p>
    <aside class="notes">Adapted Reserve excerpt: stockUnit, existingReservationRows, and sum abbreviate the actual Unit conversion and row loop. Reserve runs from OrderPlaced's handler in the same transaction as the inserted Order. Reservations use an order/ingredient identity and quantities normalized to the stock unit. A late reservation failure rejects the whole placement, not just the last ingredient.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Blocked is a set of unresolved causes, not a toggle</h2>
    <pre><code class="language-text">Pending order uses A and B.

A shortage → BlockedIngredients={A};   status=blocked
B shortage → BlockedIngredients={A,B}; status=blocked
A restock  → BlockedIngredients={B};   status=blocked
B restock  → BlockedIngredients={};    status=pending

StockAdjusted changes only its ingredient's membership.
The stored list is sorted by ingredient ID.</code></pre>
    <div class="callout">One recovery event must not erase another unresolved shortage.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/orders/handlers/stock-adjusted.go">Code: app/domains/orders/handlers/stock-adjusted.go</a></p>
    <aside class="notes">Walk the set reconstruction in orders/handlers/stock-adjusted.go. Its DAO only selects pending or blocked orders whose accepted IngredientUsage contains the ingredient; completed and cancelled orders are not reopened. Every changed Order is written and explicitly touched for audit. The timeline is a multi-cause illustration of the actual algorithm; the lifecycle fixture tests shortage, recovery, retirement, and cancellation.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Authoritative availability preserves dependency errors</h2>
    <pre><code class="language-go">// PlanIngredients:
(picks, true, nil) // complete feasible plan
(nil, false, nil)  // no feasible plan
(nil, false, err)  // dependency or conversion failure

// Strict paths propagate err:
CalculateDetail → PlanIngredients
CalculateStrict → CalculateDetail
Readiness → CalculateDetail
FulfillIngredients → PlanIngredients

// Presentation fallback remains separate:
Calculate → unavailable on error
PickIngredients → (nil, false) on error</code></pre>
    <div class="callout">Persisted projections, readiness, costing, and order planning must not turn infrastructure failure into an ordinary shortage.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/menus/internal/availability/calculator.go">Code: app/domains/menus/internal/availability/calculator.go</a></p>
    <aside class="notes">Control-flow summary, not executable Go. Read preparedMenus.prepare, queries/readiness.go and queries/cost.go. Missing stock is modeled candidate absence; database and conversion failures propagate. Tolerant Calculate/PickIngredients are not the authoritative mutation path.</aside>
  </section>

  <section class="implementation-slide">
    <h2>A bounded search still has a real cost model</h2>
    <pre><code class="language-text">N requirements, candidate counts C1 ... CN
Worst-case branches grow like the product of candidate counts,
with an extra omission branch for each optional requirement.

The implementation:
  builds candidate sets before recursion
  prunes when cumulative stock exceeds availability
  returns the first complete feasible assignment
  has no memoization or explicit search budget

It does not split one requirement across several sources.</code></pre>
    <div class="callout">Determinism makes choices explainable. It does not make the search globally optimal or constant-time.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/menus/internal/availability/calculator.go">Code: app/domains/menus/internal/availability/calculator.go</a></p>
    <aside class="notes">Complexity and limits inferred directly from PlanIngredients' nested candidate recursion. The small teaching domain keeps this tractable; adding many substitutes or order lines changes the cost inside a write transaction. The recursion also has no explicit context-cancellation check, though preceding database operations use context. If scale requires a different planner, preserve the usage snapshot and reservation contracts while testing the new selection policy.</aside>
  </section>
</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Domain workshop 3.1c</div><h1>Preserve acceptance while changing fulfillment</h1><p class="lede">Explicit amendments separate what was accepted from what is now approved to be prepared.</p><div class="section-no">3.1c</div></section>

  <section class="implementation-slide">
    <h2>One order carries three different records</h2>
    <pre><code class="language-text">AcceptanceSnapshot
  menu identity/name; ordered items and notes
  agreed prices; recipe steps and garnish
  selected and omitted ingredients, quantities and ratios

Plan
  current approved line-by-line preparation

Amendments[]
  actor, time, reason, before/after Plan

IngredientUsage
  aggregated quantities backing current reservations</code></pre>
    <div class="callout">Catalog edits affect future service. They must not reinterpret a customer's accepted order.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/orders/models/snapshot.go">Code: app/domains/orders/models/snapshot.go</a></p>
    <aside class="notes">Trace fulfillmentSnapshot during Place. Acceptance and Plan initially contain the selected items; Amend clones the plan and affected nested slices before changing it, preserving acceptance. Historical GUI/TUI details use snapshots rather than looking up today's names and recipe steps. Order-level Notes remain on Order; per-line notes are in ItemSnapshot.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Placement owns lifecycle initialization</h2>
    <pre><code class="language-go">created := models.Order{
    MenuID: order.MenuID,
    Items:  order.Items,
    Notes:  order.Notes,
}
created.ID = entity.NewOrderID()
created.Status = models.OrderStatusPending
created.CreatedAt = now
created.CompletedAt = optional.None[time.Time]()

// fulfillmentSnapshot populates Plan and Acceptance.
// DAO insert owns the initial revision.</code></pre>
    <div class="callout">Do not copy an input model wholesale. A caller cannot smuggle terminal state, acceptance, or reservations through placement.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/orders/internal/commands/place.go">Code: app/domains/orders/internal/commands/place.go</a></p>
    <aside class="notes">Exact selected initialization. Active Ingredient, Drink, Menu and Order contracts do not expose DeletedAt; catalog deletion metadata remains private. Creation and update own writable fields and lifecycle rules. TestActiveContractsDoNotExposeDeletion protects the model shape; lifecycle tests protect behavior.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Amendment is explicit, revisioned intent</h2>
    <pre><code class="language-go">type Amendment struct {
    OrderID      entity.OrderID
    Revision     uint64
    Reason       string
    Replacements []Replacement
    Preparation  []PreparationAmendment
}

// Replacement: current selected ID → replacement ID + ratio.
// Preparation: approved steps/garnish for selected drink lines.
// Unspecified preparation retains the previous approved values.</code></pre>
    <div class="callout">Only pending or blocked orders can be amended. Original acceptance and agreed prices stay unchanged.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/orders/models/snapshot.go">Code: app/domains/orders/models/snapshot.go</a></p>
    <aside class="notes">Exact Amendment declaration. The command requires a reason and at least one replacement; this is not a general standalone preparation editor. A zero ratio defaults to 1; other ratios must be finite and positive. Replacement keys refer to currently selected ingredients, not merely original recipe IDs. Omitted selections remain omitted. Orders has a dedicated amend Cedar action, permitted to manager and owner; the loaded and resulting Order still pass both pipeline gates.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Replan without spending your own reservation twice</h2>
    <pre><code class="language-text">Load current order and validate expected revision
Copy Plan; apply approved replacements and quantity ratios
Project stock with this order's reservations released
Plan every included requirement as required
Preserve unchanged preparation unless explicitly amended
Save current Plan + aggregate IngredientUsage + amendment
Emit OrderAmended{Before, Order, Reason}

Inventory: validate old reservations, release, reserve new
Menus: prepare availability from net reservation change
Orders: reconcile peers helped by the released commitment</code></pre>
    <div class="callout">All steps share one transaction. A late reservation failure restores the original plan and commitments.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/orders/internal/commands/amend.go">Code: app/domains/orders/internal/commands/amend.go</a></p>
    <aside class="notes">Follow FulfillWithReservations and inventory/handlers/order-amended.go. Original acceptance is never overwritten. The planner receives the amended requirements and its configured candidate rules; inspect the actual returned plan rather than assuming the requested replacement alone describes all picks. Ratios multiply current selected quantity. Completion and amendment verify reservation identities and quantities before consuming or replacing them.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Validate a batch before its own effects change revisions</h2>
    <pre><code class="language-text">App.AmendOrders(requests):
  reject duplicate order IDs
  load every selected order
  require every submitted revision to match

  then, for each request:
    reload the current order in this transaction
    use that revision for Orders.Amend

App.RetireIngredient(..., requests):
  amend the explicit selection
  retire the ingredient in the same workflow</code></pre>
    <div class="callout">Reconciliation may legitimately advance a peer's revision within the batch. Validate stale user intent before that begins.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/amend_orders.go">Code: app/amend_orders.go</a></p>
    <aside class="notes">RunWorkflow owns the outer transaction and failure evidence. Re-reading a token after validating the full selection is not a general stale-write bypass; it accounts for effects caused by this very transaction. Unselected orders retain their plan and follow discontinuation/withdrawal policy. The operator supplies approval and reason; the system does not infer customer consent.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Prove that the second failure undoes the first success</h2>
    <pre><code class="language-text">Two selected orders; replacement stock can fulfill only one.

Attempt App.RetireIngredient with both amendments:
  first amendment provisionally succeeds
  second amendment fails
  outer transaction rolls back

Assert:
  first order equals its original value
  replacement reserved amount = 0
  original ingredient remains active
  audit count = before + 1; failed workflow has effects</code></pre>
    <div class="callout">The surviving activity describes the attempted changes. It must not look like committed amendment history.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/cross_domain_regression_test.go">Code: app/cross_domain_regression_test.go</a></p>
    <aside class="notes">Scenario and assertions from TestFailedSelectedAmendmentsRollBackAllEffectsAndPersistFailure. It checks a nonempty WorkflowID and touches containing the first order. TestAtomicRetirementAmendmentKeepsAcceptanceAndApprovedPreparation covers successful composition; TestLateWorkflowFailureRollsBackEveryDomain injects failure after the domain work.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Historical references can veto deletion</h2>
    <pre><code class="language-text">Delete Drink:
  Menus checks active menu references
  Orders checks all historical order usage

Delete Menu:
  Orders checks all historical order usage

A veto during Handling rolls back the source deletion.
Errors identify dependencies and the corrective action.
Redrafting preserves the previous PublishedAt value.</code></pre>
    <div class="callout">A retained snapshot does not automatically authorize removal of its referenced catalog identity.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/orders/internal/dao/usage.go">Code: app/domains/orders/internal/dao/usage.go</a></p>
    <aside class="notes">Trace DrinkDeleted and MenuDeleted handlers. An active menu reference can be removed through normal draft curation; historical order references remain a deletion veto, including terminal orders. There is no force flag. Handler wrappers may add an outer Internal classification while retaining the FailedPrecondition cause; do not promise an unwrapped top-level error kind for every reaction.</aside>
  </section>
</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Domain workshop 3.1d</div><h1>Separate physical stock from service eligibility</h1><p class="lede">Discontinuation, quarantine, release, and disposal are different business decisions.</p><div class="section-no">3.1d</div></section>

  <section class="implementation-slide">
    <h2>Canonical quantity, display unit, price basis</h2>
    <pre><code class="language-text">Stock row:
  Quantity + Unit       canonical physical amount (ml for volume)
  DisplayUnit           operator-facing quantity unit
  CostPerUnit + CostUnit explicit price basis

Example:
  10 oz on hand → stored as 295.735 ml
  change display to ml → same stock and reservations
  $2 per oz remains $2 per oz, not $2 per ml

Discrete units retain their own canonical unit.</code></pre>
    <div class="callout">A compatible catalog unit change must not change physical stock, accepted usage, or the meaning of its price.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/inventory/internal/dao/convert.go">Code: app/domains/inventory/internal/dao/convert.go</a></p>
    <aside class="notes">Quantity example uses the kernel's 29.5735 ml/oz constant. Reservations persist canonical quantities too. IngredientUpdated changes stock presentation, retaining cost basis. Incompatible dimensional changes require a replacement identity. TestCanonicalStockSurvivesDisplayUnitChange proves reservation and completion behavior across the display change. New explicit prices default to the catalog unit unless CostUnit is supplied.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Retirement does not mean throwing stock away</h2>
    <pre><code class="language-text">Discontinue:
  exclude ingredient from new service
  retain stock, tags, identity and usable reservations

Withdraw (Retirement.Withdraw=true):
  quarantine retained stock
  block affected open orders

Release quarantine:
  active catalog item → active stock
  retired catalog item → discontinued stock

Neither replacement nor release transfers physical inventory.</code></pre>
    <div class="callout">Future product intent and existing physical commitments have different owners and lifecycle rules.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/inventory/handlers/ingredient-deleted.go">Code: app/domains/inventory/handlers/ingredient-deleted.go</a></p>
    <aside class="notes">Inventory prepares the retained row before handlers apply. Existing quarantine is not cleared by a later ordinary discontinuation; disposed stock is not revived. Orders' retirement handler blocks only when Withdraw is true. Separate Inventory.Disposition supports quarantine and release with reason and revision. Completion may use discontinued stock but refuses quarantined or inconsistent reservations.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Disposal preserves evidence of physical loss</h2>
    <pre><code class="language-text">Inventory.Dispose:
  require expected stock revision
  require discontinued/quarantined eligibility
  require positive amount and reason
  subtract from physical stock; reject negative remainder
  at zero, mark disposed
  save movement history and retain the stock row
  emit StockAdjusted to reconcile commitments

Inventory.History reads retained movements.</code></pre>
    <div class="callout">The absence of a row cannot explain what was discarded, why, or which commitments it affected.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/inventory/internal/commands/dispose.go">Code: app/domains/inventory/internal/commands/dispose.go</a></p>
    <aside class="notes">Trace DAO.Upsert and movement.go for the quantity movement. Stock tags and identity are retained after disposal; no implicit transfer to a replacement occurs. Physical loss can create shortage and block existing orders. The stock event, order reactions, menu projections and audit remain in the originating transaction.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Recovery must be as complete as blocking</h2>
    <pre><code class="language-text">On hand=3; two orders each reserve 2
Aggregate reserved=4 → both orders blocked

Cancel one order:
  release its reservation
  project remaining reserved=2
  clear that ingredient's blocker on the other order
  return to pending only if no blockers remain

Amendment release and quarantine release also reconcile.</code></pre>
    <div class="callout">The policy blocks all affected orders during an aggregate deficit. It does not allocate winners by FIFO or priority.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/orders/handlers/order-cancelled.go">Code: app/domains/orders/handlers/order-cancelled.go</a></p>
    <aside class="notes">Illustrative values for the shipped aggregate policy. Cancellation prepares peer changes before Inventory releases rows, using projected remaining reservations. TestCancellationPreparationRecoversPeersInEveryHandlerOrder proves independence. Quarantined/disposed stock remains blocked even if the numeric deficit disappears. A restored ingredient must not erase other blockers.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Persist substitution rules by identity</h2>
    <pre><code class="language-go">type SubstitutionRule struct {
    Revision      uint64
    Disabled      bool
    IngredientID  entity.IngredientID
    SubstituteID  entity.IngredientID
    Ratio         float64
    QualityImpact Quality
    Notes         string
}

// SetSubstitution authorizes update on the original ingredient.
// SubstitutionRules includes disabled rules for administration.</code></pre>
    <div class="callout">Renaming an ingredient must not change which substitute it means. A rule edit also refreshes dependent availability.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/ingredients/models/substitution.go">Code: app/domains/ingredients/models/substitution.go</a></p>
    <aside class="notes">Selected fields, JSON tag omitted. Rule updates require the returned revision. The command verifies dimensional compatibility and Get authority on the substitute, but does not invent permanent replacement intent or require category equality for a temporary rule. IngredientUpdated triggers the dependent refresh. TestIDSubstitutionSurvivesRenameAndTracksStock covers renaming and implicit dependency tracking. A permanent non-1 replacement of an ID-only recipe substitute is rejected until that ambiguous candidate is explicitly revised.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Walk the lifecycle through the CLI</h2>
    <pre><code class="language-bash">mixology ingredients substitution --id ing-A \
  --substitute-id ing-B --ratio 0.75 --quality similar
mixology ingredients substitutions --id ing-A
mixology orders amend --id ord-A --ingredient-id ing-A \
  --replacement-id ing-B --revision 3 --reason 'approved'
mixology orders amend-batch --file amendments.json

mixology inventory quarantine --ingredient-id ing-A --reason 'inspect'
mixology inventory release --ingredient-id ing-A --reason 'cleared'
mixology inventory dispose --ingredient-id ing-A \
  --quantity 5 --reason 'discard remainder'
mixology inventory history --ingredient-id ing-A</code></pre>
    <div class="callout">Replace illustrative IDs with seeded IDs. Capture revisions when intent must refer to the state you reviewed.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/main/cli/order_amend.go">Code: main/cli/order_amend.go</a></p>
    <aside class="notes">These are command shapes, not a sequential fixture: quarantine/release/dispose need the corresponding lifecycle preconditions. Disposal quantity uses the current stock display unit. Batch input is a JSON array of models.Amendment with each expected revision; preparation changes can be included there. CLI operations without an explicit revision load the current token immediately before writing. GUI/TUI display history and guard edits but do not yet offer dedicated forms for all these workflows. This is the bridge back to chapter 4.0's output and input toolkit.</aside>
  </section>
</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Optional extension 3.2</div><h1>Extend the model with Procurement</h1><p class="lede"><span class="decision">planned, not implemented</span><br>Orders and Inventory already demonstrate reciprocal reactions. Procurement would add a workflow that spans time and commits.</p><div class="section-no">3.2</div><aside class="notes">This chapter is an optional future recording, not part of the current repository onboarding. Continue to 4.0 for the shipped interfaces. If recording the extension, first recap the existing order/reservation loop and ask what changes when a supplier response arrives hours or days later.</aside></section>

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
  <section class="implementation-slide">
    <h2>Proposed receipt processing needs durable identity</h2>
    <pre><code class="language-text">Design exercise, not implemented:

ReceivePurchaseOrder(purchaseOrderID, receiptID, lines)
  load purchase order; authorize receiving
  reject invalid quantities
  detect an already accepted receiptID
  persist receipt and receiving state
  emit ReceiptAccepted{receiptID, ingredient quantities}
  Inventory applies the receipt in the same transaction

External delivery, if later introduced:
  store an outbox record with the receipt commit
  deliver after commit; deduplicate by receiptID</code></pre>
    <div class="callout">A supplier callback can be retried. The exercise is to place idempotency and transaction ownership before adding asynchronous delivery.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/docs/architecture.md">Code: docs/architecture.md</a></p>
    <aside class="notes">This is a proposed contract, not a claim that Procurement or an outbox exists. Use the current architecture as the constraint set. Ask whether a duplicate receipt should return the original result or a typed conflict, and which owner stores that choice. Contrast an explicit Receive operation with a handler trying to wait for a supplier or emit another event.</aside>
  </section>

</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Surfaces 4.0 · CLI toolkit</div><h1>Start with the command line</h1><p class="lede">Trace one invocation, then inspect the small toolkit shared by its commands: JSON input, structured output, and text rendering.</p><div class="section-no">4.0</div><aside class="notes">Keep the CLI toolkit in this recording rather than making a separate chapter. Start with a real operation, identify the reusable mechanics, and use that boundary to introduce the more stateful TUI and GUI toolkits.</aside></section>

  <section>
    <h2>CLI walkthrough: discover, change, inspect</h2>
    <pre><code class="language-sh">go run ./main/cli ingredients list --limit 5
go run ./main/cli ingredients list --limit 5 --json
go run ./main/cli drinks create --template
go run ./main/cli ingredients create "Demo lime" \
  --category juice --unit oz --tags featured
go run ./main/cli ingredients list \
  --filter 'name == "Demo lime" && tags contains "featured"'
go run ./main/cli audit list --limit 5</code></pre>
    <div class="callout">Show the result first, then trace the create command into the domain facade and the atomic tagged mutation.</div>
    <aside class="notes">Run this against fresh demo data. Compare table and JSON representations of the same values. The template is discovery, not a submitted mutation. Creation with --tags exercises domain creation plus tag replacement in one transaction; inspect both successful activities in Audit. Repeat a catalog read as another persona to show that output formatting does not determine permission. Use --help to find flags rather than expecting viewers to memorize them.</aside>
  </section>

  <section>
    <h2>A command is an adapter around an operation</h2>
    <div class="flow"><div class="node"><strong>flags / JSON</strong>parse user intent</div><div class="arrow">→</div><div class="node"><strong>domain module</strong>execute with fresh context</div><div class="arrow">→</div><div class="node"><strong>CLI view</strong>shape the result</div><div class="arrow">→</div><div class="node"><strong>output / exit</strong>human or script feedback</div></div>
    <div class="cards two"><div class="card"><h3>Domain adapter</h3><p>Owns input conversion, domain-specific output, and filter help.</p></div><div class="card"><h3>Shared toolkit</h3><p>Owns reusable JSON decoding, encoders, and table rendering.</p></div></div>
    <div class="callout">Business validation and authorization still run in the application, so a script and an interactive user receive the same decision.</div>
    <aside class="notes">Open main/cli/README.md, the ingredients command composition, and app/domains/ingredients/surfaces/cli. Compare table output with --json for the same list. --filter-help exposes the domain schema without opening the database. --template, --file, and --stdin make document-shaped mutations discoverable and scriptable without introducing a second application API.</aside>
  </section>

  <section>
    <h2>Scripts must preserve concurrency too</h2>
    <div class="layers"><div class="layer"><strong>Read</strong><span>Obtain the entity and its revision in JSON.</span></div><div class="layer"><strong>Edit</strong><span>Change intended fields while preserving the revision value.</span></div><div class="layer"><strong>Submit</strong><span>The store rejects a stale revision with a typed Conflict.</span></div><div class="layer"><strong>Resolve</strong><span>Reload, compare the intervening change, then decide what to submit.</span></div></div>
    <div class="callout">An opaque revision is a token to return unchanged, not a counter for the client to increment.</div>
    <aside class="notes">This applies to replace-style JSON updates for drinks, ingredients, and menus. Flag-based ingredient and menu updates fetch the current revision immediately before submission. A read/edit/write script carries an older snapshot, so the explicit revision prevents it from silently overwriting a concurrent edit. Connect this behavior to the same conflict a GUI editor can receive.</aside>
  </section>
  <section class="implementation-slide">
    <h2>CLI rows are projections of application models</h2>
    <pre><code class="language-go">type DrinkRow struct {
    ID          string `table:"ID" json:"id"`
    Name        string `table:"NAME" json:"name"`
    Status      string `table:"STATUS" json:"status"`
    Ingredients int    `table:"INGREDIENTS" json:"ingredients"`
    // Category, Glass, Tags omitted.
}

// Selected conversion fields:
ID:          d.ID.String(),
Status:      string(d.Status),
Ingredients: len(d.Recipe.Ingredients),</code></pre>
    <div class="callout">The table/JSON view can summarize a recipe without changing the domain model or exposing its persistence row.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/drinks/surfaces/cli/views.go">Code: app/domains/drinks/surfaces/cli/views.go</a></p>
    <aside class="notes">Exact selected fields from DrinkRow and ToDrinkRow. The row's ingredients count is presentation data, not a replacement for the recipe used by command validation. Follow ToDrinkRows into the CLI list output. The domain still owns filter semantics and authorization; the CLI chooses how to represent an allowed result.</aside>
  </section>

  <section class="implementation-slide">
    <h2>The command chooses the output contract</h2>
    <pre><code class="language-go">// ingredients list, after the authorized application query:
if cmd.Bool("json") {
    return clitoolkit.WriteJSON(cmd.Writer,
        paging.Page[ingredientscli.IngredientRow]{
            Items: ingredientscli.ToIngredientRows(res.Items), Next: res.Next,
        })
}
if err := clitable.PrintTable(cmd.Writer,
    ingredientscli.ToIngredientRows(res.Items)); err != nil {
    return err
}
return printNextCursor(cmd.Writer, res.Next)</code></pre>
    <div class="callout">The toolkit renders values. The command owns the page envelope, cursor reporting, and choice of representation.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/main/cli/ingredients.go">Code: main/cli/ingredients.go</a></p>
    <aside class="notes">Exact output branch with a line wrapped for the slide. Compare ingredients get: it passes ToIngredientRow to WriteJSON or PrintDetail, without a page envelope. Mutation output is chosen separately: ingredient create emits the result model as JSON or just its ID as text. Do not infer one universal output schema from the generic writer. All of these paths use cmd.Writer, so tests and embedding code can capture output without replacing process stdout. TestTableOutputUsesCommandWriter exercises the composed command with a bytes.Buffer.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Table and detail rendering have different field rules</h2>
    <pre><code class="language-go">// Selected IngredientRow fields:
ID       string `table:"ID" json:"id,omitempty"`
Revision uint64 `table:"-" json:"revision,omitempty"`
Name     string `table:"NAME" json:"name"`
// Revision is absent from the table, present in detail when nonzero.</code></pre>
    <pre><code class="language-text">TestPrintTable fixture        TestPrintDetail fixture
ID     NAME   COUNT            ID:          ord-1
ing-1  Vodka  2                Menu ID:     mnu-1
                              Created At:  2025-02-03T04:05:06Z
                              Status:      pending</code></pre>
    <div class="callout">Tables opt fields in with <code>table</code> tags. Details use <code>json</code> tags and omit zero values marked <code>omitempty</code>. Neither rule grants or denies access.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/toolkits/cli/table/table.go">Code: table/table.go</a> · <a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/toolkits/cli/table/table_test.go">Tests: table/table_test.go</a> · <a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/ingredients/surfaces/cli/views.go">IngredientRow</a></p>
    <aside class="notes">The output shows the two separate renderer test fixtures with spacing normalized, not an ingredient record. TestPrintDetail's empty Notes field is omitted; menu_id becomes Menu ID, time.Time uses RFC3339, and the status uses fmt.Stringer. Walk getTableFields, getJSONFields, formatValue, and the tabwriter flush. Reflection inspects exported fields on structs, with one optional outer pointer, rather than recursively deriving a domain view. Flatten recipes and optional prices in the domain adapter. Empty typed slices still print headers. Detail omission uses this renderer's isZero helper, not encoding/json itself; notably it dereferences pointers when testing zero. A table tag hides a column only, so never use it as an authorization boundary.</aside>
  </section>

  <section class="implementation-slide">
    <h2>The process boundary consumes the typed error</h2>
    <pre><code class="language-go">cmd := cliApp.Command()
if err := cmd.Run(context.Background(), os.Args); err != nil {
    cli.HandleExitCoder(errors.ToCLIExit(err))
    os.Exit(errors.ExitGeneral)
}</code></pre>
    <div class="callout">The application returns an error. The executable chooses process behavior through the shared adapter: Conflict → 40, Permission → 30, Internal → 50.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/main/cli/main.go">Code: main/cli/main.go</a></p>
    <aside class="notes">Exact main branch. HandleExitCoder exits with the mapped code; the following general exit is a fallback. Connect this to chapter 1.3's wrapped error example. Test the built CLI binary when demonstrating shell exit status: go run adds its own launcher behavior and is not a reliable way to demonstrate the application's exact process exit code.</aside>
  </section>


  <section class="implementation-slide">
    <h2>Trace JSON input through the validation boundaries</h2>
    <pre><code class="language-text">--template              → print example; no mutation
--file OR --stdin        → choose one input source
ReadJSONInput[DTO]       → decode the transport shape
domain CLI conversion   → parse IDs, units, revision, tags
public facade           → authorization + business validation
DAO                     → constraints + optimistic revision

JSON decoding is not business validation.</code></pre>
    <div class="callout">The toolkit handles transport mechanics. Domain-specific interpretation and authoritative rules remain separate.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/toolkits/cli/json.go">Code: pkg/toolkits/cli/json.go</a></p>
    <aside class="notes">Trace main/cli/ingredients.go and its domain surfaces/cli package. ReadJSONInput currently decodes one JSON value with the standard decoder; it does not enable DisallowUnknownFields or check for a second trailing value, and stdin is read into memory. Do not teach this helper as a strict schema validator or a streaming import API. Template handling occurs before the reader. The reader's exactly-one-source requirement applies when the command selects JSON input; ingredient create also supports a flags-only path. Conversion varies by command: ingredient update parses its ID and carries the revision, while the tagged-mutation wrapper handles the --tags flag separately.</aside>
  </section>

  <section class="implementation-slide">
    <h2>The JSON toolkit standardizes mechanics, not models</h2>
    <pre><code class="language-go">func WriteJSON(w io.Writer, v any) error {
    b, err := json.MarshalIndent(v, "", "  ")
    if err != nil {
        return err
    }
    b = append(b, '\n')
    _, err = w.Write(b)
    return err
}</code></pre>
    <div class="callout"><code>JSONFlag</code>, <code>TemplateFlag</code>, <code>StdinFlag</code>, and <code>FileFlag</code> keep command spelling consistent. <code>ReadJSONInput[T]</code> selects and decodes one source; <code>WriteJSON</code> emits an indented document and newline.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/toolkits/cli/json.go">Code: pkg/toolkits/cli/json.go</a></p>
    <aside class="notes">Exact writer implementation. Open the reader in the same file: both --stdin and --file return “set only one of --stdin or --file”; neither returns “missing input: set --stdin or --file (or use --template)”; whitespace-only stdin returns “stdin is empty”. Show that --template is handled by the composing command before this reader. The toolkit imports no application models and chooses no business defaults. JSON marshaling and writer errors propagate to the caller. This is a small document-oriented helper: both output marshaling and stdin input materialize bytes in memory.</aside>
  </section>

  <section>
    <h2>Reuse the surface mechanics as interaction grows</h2>
    <table class="matrix"><thead><tr><th>Toolkit</th><th>Reusable responsibility</th><th>Domain adapter still owns</th></tr></thead><tbody><tr><td>CLI · this chapter</td><td>Decode a document; render a result.</td><td>Flags, input interpretation, view conversion.</td></tr><tr><td>TUI · 4.1</td><td>Route messages, keys, forms, and navigation.</td><td>Screen state and application actions.</td></tr><tr><td>GUI · 4.2a–b</td><td>Compose widgets; execute and publish work safely.</td><td>Presenter state and application actions.</td></tr></tbody></table>
    <div class="callout">Add a CLI operation through the domain facade, its CLI adapter, and <code>main/cli</code> composition. Extract mechanics into the toolkit only when they are independent of the business model.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/toolkits/cli/readme.md">CLI toolkit extension guide</a> · <a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/main/cli/cli_output_test.go">Output contract tests</a></p>
    <aside class="notes">Close the code walkthrough by running go test ./pkg/toolkits/cli/... ./main/cli. TestTableColumns protects view headings, TestTableRowsIncludeDerivedValues protects domain-to-display conversion, TestEntityJSONViewsExposeCanonicalTags protects structured tag output, and TestTableOutputUsesCommandWriter protects output routing. CLI parsing tests that share package-level urfave flag instances run serially; the parser mutates those instances. For an added command, exercise its real text and JSON paths, input failures, and application errors. Segue to the terminal demo: the same operation now lives inside a persistent session, so selection, input ownership, and refresh need explicit contracts. Toolkit size follows those responsibilities, while business validation and authorization remain behind the facade.</aside>
  </section>
</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Surfaces 4.1</div><h1>Build a reusable MVVM toolkit for the terminal</h1><p class="lede">Model–View–ViewModel separates application data, screen state and actions, and rendering. Bubble Tea supplies the update loop.</p><div class="section-no">4.1</div><aside class="notes">Here MVVM describes the separation of responsibilities, not automatic data binding. A view model owns screen state and actions; View renders that state. A Bubble Tea command is a function that performs an effect and returns a message. It is a different use of the word command from a domain command that mutates business state.</aside></section>

  <section>
    <h2>TUI walkthrough: keep context between actions</h2>
    <div class="layers"><div class="layer"><strong>Browse</strong><span>Run <code>go run ./main/tui</code>, open Ingredients, filter the list, and select the demo ingredient.</span></div><div class="layer"><strong>Edit</strong><span>Use the displayed key help to edit, inspect tags, and return to the list.</span></div><div class="layer"><strong>Refresh</strong><span>Change the record from the CLI and observe the TUI query again.</span></div><div class="layer"><strong>Compare</strong><span>Run with <code>--actor bartender</code> and inspect which workspaces and actions are available.</span></div></div>
    <div class="callout">A persistent session needs navigation, selection, input ownership, and an editor that survives background refresh.</div>
    <aside class="notes">Continue from the CLI-created demo ingredient. Capture help on screen so the interaction remains understandable. Show the difference between a list refresh and an open editor: external invalidation should not replace text the person is typing. After the behavior demo, follow the root shell into the ingredient view model and its application call. The business operation is unchanged; the surrounding interaction persists.</aside>
  </section>

  <section>
    <h2>Adapt the pattern to the runtime</h2>
    <div class="split"><div class="side"><h3>View-model responsibility</h3><p>A screen owns presentation state and commands behind a testable view-model contract.</p></div><div class="bridge">+</div><div class="side"><h3>Bubble Tea runtime</h3><p>Messages drive explicit updates, commands carry effects, and a string view renders each frame.</p></div></div>
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
    <div class="cards four"><div class="card"><h3>Browse</h3><p><code>ListDetail</code>, typed <code>ListItem[T]</code>, summaries, loading, filtering, paging, and selection.</p></div><div class="card"><h3>Compose</h3><p><code>DetailViewport</code>, <code>FormViewport</code>, layout arithmetic, reusable components.</p></div><div class="card"><h3>Interact</h3><p>Forms, dialogs, keys, styles, help bindings, and explicit input ownership.</p></div><div class="card"><h3>Refresh</h3><p>A change notification starts an ordinary query; request tokens reject stale results.</p></div></div>
    <div class="callout"><code>pkg/testutil/tuitest</code> is the deterministic program driver. It tests the toolkit and completed application without becoming part of either.</div>
  </section>

  <section>
    <h2>Typed messages keep ownership visible</h2>
    <div class="flow"><div class="node"><strong><code>tea.Msg</code></strong>input arrives</div><div class="arrow">→</div><div class="node"><strong>Root shell</strong>consults <code>Interaction</code></div><div class="arrow">→</div><div class="node"><strong>ViewModel</strong>updates state</div><div class="arrow">→</div><div class="node"><strong><code>tea.Cmd</code></strong>returns typed result</div></div>
    <div class="cards two"><div class="card"><h3>Reusable mechanics</h3><p>Generic list items retain their typed domain values while satisfying Bubbles interfaces.</p></div><div class="card"><h3>Domain choices</h3><p>Publish, complete, cancel, adjust, and retire remain bindings owned by their domain adapters.</p></div></div>
    <div class="callout">An external change marks inactive screens stale. Active input finishes first, then the screen queries again with a fresh request token.</div>
    <aside class="notes">Open pkg/toolkits/tui/readme.md and one domain's list/detail view models. A refresh notification says only that displayed state may be stale. The view model issues its ordinary query and labels the request so an older result cannot overwrite it. Interaction lets the shell distinguish typing into a form from a global shortcut and lets a detail view own Back. Demonstrate opening a detail, typing into a filter, and returning to the list with selection preserved.</aside>
  </section>

  <section>
    <h2>Tests follow the ownership</h2>
    <div class="evidence-ladder"><div class="rung">pure presentation model tests</div><div class="rung">component update and rendering tests</div><div class="rung">domain surface tests</div><div class="rung">real Bubble Tea program driver</div><div class="rung">root navigation and input ownership</div><div class="rung">cross-surface persisted behavior</div></div>
  </section>
  <section class="implementation-slide">
    <h2>Capture a request before returning a Bubble Tea effect</h2>
    <pre><code class="language-go">m.loadToken++
token := m.loadToken
req := m.request
req.Cursor = cursor

return func() tea.Msg {
    page, err := m.app.Ingredients.List(m.context(), req)
    if err != nil {
        return IngredientsLoadedMsg{Err: err, Token: token}
    }
    // Convert page.Items to the message's []models.Ingredient.
    return IngredientsLoadedMsg{
        Ingredients: items, Next: page.Next, Token: token,
    }
}</code></pre>
    <div class="callout">The effect captures request values and returns a typed message. It does not mutate the visible list from a background operation.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/ingredients/surfaces/tui/list_vm.go">Code: app/domains/ingredients/surfaces/tui/list_vm.go</a></p>
    <aside class="notes">Adapted from loadIngredients: ingredientsList is shortened to page and the item-conversion loop is omitted. Capture token and req before the closure executes; reading changing view-model fields inside the effect would blur ownership. Keep fresh operation context separate from the load-generation token.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Reject a stale message before changing list state</h2>
    <pre><code class="language-go">case IngredientsLoadedMsg:
    if msg.Token != m.loadToken {
        return m, nil
    }
    if msg.Err != nil {
        m.shell.SetResult(m.items, msg.Err)
        return m, nil
    }
    m.next = msg.Next
    selected := selectedIngredientID(m.selectedIngredient())
    // Rebuild list items, then restore selection by entity ID.
    m.selectIngredient(selected)</code></pre>
    <div class="callout">Selection is an entity identity, not a row index. A late result must not replace the current page, error, cursor, or selected record.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/ingredients/surfaces/tui/list_vm.go">Code: app/domains/ingredients/surfaces/tui/list_vm.go</a></p>
    <aside class="notes">Selected Update branch; list rebuilding is omitted. Work through load token 7 followed by token 8, with 7 completing last. Then inspect the DataInvalidatedMsg branch: it only reloads while browsing and permitted to list. The shell coordinates deferred invalidation while the screen owns input.</aside>
  </section>


  <section class="implementation-slide">
    <h2>Typing and navigation require explicit input ownership</h2>
    <pre><code class="language-text">type Interaction struct {
    HandlesBack  bool
    CapturesText bool
}

// Root shell, simplified routing:
rune key + CapturesText → child gets text, not global q / ?
Escape + help open     → close help
Escape + HandlesBack   → child cancels local interaction
Escape otherwise       → navigate application history</code></pre>
    <div class="callout">A global keybinding is not global while an editor owns that input. Back must unwind the nearest interaction first.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/main/tui/app.go">Code: main/tui/app.go</a></p>
    <aside class="notes">The Interaction declaration is selected from the toolkit; routing is summarized from main/tui/app.go. Runes are protected while CapturesText is true; non-rune quit shortcuts still follow the root keymap. A child can own filter editing, a modal, or detail navigation without the root importing its state type. Run TestE2E_ListFilterOwnsPrintableShortcutsAndEscape and TestBackKey_CancelsDomainLocalStateBeforeNavigating.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Defer invalidation without losing the need to refresh</h2>
    <pre><code class="language-text">databaseChangedMsg arrives:
  mark inactive views stale
  active view owns Back or text?
    yes → mark active stale; keep interaction
    no  → send DataInvalidatedMsg now

acceptViewUpdate:
  still editing/detail-owned → keep stale flag
  returned to browse         → clear flag; issue normal reload</code></pre>
    <div class="callout">A refresh request must survive the editor, but must not replace the editor. Staleness and interaction ownership are separate state.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/main/tui/app.go">Code: main/tui/app.go</a></p>
    <aside class="notes">Trace the databaseChangedMsg branch and acceptViewUpdate. Inactive views refresh when activated; the current view defers while HandlesBack or CapturesText is true. When the interaction finishes, the root emits the ordinary invalidation message and the domain list issues its tokenized query. This is a state machine, not a timer-based workaround.</aside>
  </section>
</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Surfaces 4.2a</div><h1>Adapt the MVVM toolkit to retained widgets</h1><p class="lede">Fyne changes the interaction model, so the reusable mechanics change with it.</p><div class="section-no">4.2a</div></section>

  <section>
    <h2>GUI walkthrough: the same record in a desktop window</h2>
    <div class="layers"><div class="layer"><strong>Open</strong><span>Run <code>go run ./main/gui</code> against the same local database and find the demo ingredient.</span></div><div class="layer"><strong>Interact</strong><span>Browse, filter, edit tags, and compare pointer actions with keyboard shortcuts.</span></div><div class="layer"><strong>Change externally</strong><span>Update from the CLI; observe refresh without replacing an active form.</span></div><div class="layer"><strong>Inspect a decision</strong><span>Open Menus readiness and compare a permitted but blocked Publish action with a denied action.</span></div></div>
    <div class="callout">Widgets persist, queries complete asynchronously, and the window can close while application work is running.</div>
    <aside class="notes">Prepare native prerequisites from main/gui/README.md. Reuse the CLI/TUI scenario so viewers can compare outcomes. Prepare a draft menu with a known readiness blocker for the final step; use a manager and a restricted persona separately. Then open the domain presenter and view to show how state becomes visible controls. Use deterministic async tests to demonstrate request races and shutdown; those should not depend on getting lucky during a live recording.</aside>
  </section>

  <section>
    <h2>Start from the application boundary</h2>
    <div class="layers"><div class="layer"><strong><code>main/gui</code></strong><span>database, actor, logs, application, session, native lifecycle</span></div><div class="layer"><strong>domain GUI surfaces</strong><span>presenters and views shaped for each bounded context</span></div><div class="layer"><strong><code>pkg/toolkits/gui</code></strong><span>shell, forms, tables, semantic controls, dialogs, executors</span></div><div class="layer private"><strong>Fyne runtime</strong><span>retained widgets, callbacks, windows, platform event loop</span></div></div>
  </section>

  <section>
    <h2>Publish state for the view to render</h2>
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
    <aside class="notes">The GUI Dispatcher schedules work on the UI thread; it is unrelated to the domain event dispatcher. Consider query A followed by query B: B may finish first, and A may already have queued its callback. Cancellation alone is insufficient, so publication also checks whether the request is still current. The recent 8ddcd32 change also skips work invalidated while waiting in the executor queue. Submission admits only one mutation at a time.</aside>
  </section>

  <section>
    <h2>Closing a window must not close the store too early</h2>
    <div class="flow"><div class="node"><strong>stop producers</strong>change monitor + dashboard</div><div class="arrow">→</div><div class="node"><strong>close executor</strong>stop admission + drain work</div><div class="arrow">→</div><div class="node"><strong>close UI gate</strong>reject queued callbacks</div><div class="arrow">→</div><div class="node"><strong>close store</strong>release persistence</div></div>
    <div class="callout">A closed window does not mean an accepted database operation has finished.</div>
    <aside class="notes">Open main/gui and the managed executor and gated dispatcher in pkg/toolkits/gui. Follow the shutdown composition and its lifecycle tests. Stop new admissions, prevent publication to closed widgets, and wait for accepted work before closing persistence. Cancelling a superseded read and abandoning an accepted mutation are different lifecycle decisions.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Check freshness when the UI callback executes</h2>
    <pre><code class="language-go">func (r *LatestRequest[T]) dispatch(
    generation uint64, fn func(),
) {
    r.dispatcher.Dispatch(func() {
        r.mu.Lock()
        current := generation == r.generation
        r.mu.Unlock()
        if current {
            fn()
        }
    })
}</code></pre>
    <div class="callout">A result can become stale after background work finishes but before the UI queue runs. Checking only before Dispatch leaves that race open.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/toolkits/gui/async.go">Code: pkg/toolkits/gui/async.go</a></p>
    <aside class="notes">Exact method with a reflowed signature. Invalidate increments generation and cancels the context. LoadContext also checks ctx.Err before running queued work. The mutex protects request bookkeeping; production UI dispatch serializes presentation callbacks. Follow this with the manual-queue test in chapter 4.5.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Publication copies the mutable containers it exposes</h2>
    <pre><code class="language-go">func cloneState(state State) State {
    state.Items = append([]models.Ingredient(nil), state.Items...)
    state.History = append([]paging.Cursor(nil), state.History...)
    actionsCopy := make(map[actions.ID]actions.State, len(state.Actions))
    maps.Copy(actionsCopy, state.Actions)
    state.Actions = actionsCopy
    if state.Selected != nil {
        selected := *state.Selected
        state.Selected = &amp;selected
    }
    return state
}</code></pre>
    <div class="callout">Snapshot and OnChange publish this copy. The view gets presentation state without sharing the presenter's top-level slice or map storage.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/domains/ingredients/surfaces/gui/presenter.go">Code: app/domains/ingredients/surfaces/gui/presenter.go</a></p>
    <aside class="notes">Exact implementation. This is a targeted copy, not recursive immutability: slice element structs or selected structs can still contain nested references. Inspect those types when extending state and decide whether additional copying is necessary. This makes the ownership contract reviewable instead of implying that the word snapshot automatically prevents all aliasing.</aside>
  </section>

</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Surface deep dive 4.2b</div><h1>Own work until shutdown is actually complete</h1><p class="lede">Request freshness, mutation admission, UI publication, and store lifetime are separate concurrency boundaries.</p><div class="section-no">4.2b</div><aside class="notes">Follow the GUI walkthrough with deterministic races and real process-lifecycle tests. The central question is which component still owns work after the user closes the window.</aside></section>

  <section class="implementation-slide">
    <h2>Reads and mutations have different admission semantics</h2>
    <pre><code class="language-text">LatestRequest:
  a newer load supersedes the older load
  cancellation reduces obsolete work
  generation checks reject stale publication

Submission:
  first submit marks active=true
  another submit while active returns false
  completion is dispatched to the UI
  release active, then publish the result</code></pre>
    <div class="callout">An obsolete read may be discarded. An accepted mutation still needs an accountable completion.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/toolkits/gui/async.go">Code: pkg/toolkits/gui/async.go</a></p>
    <aside class="notes">Trace both types in async.go. Submission stays active until the UI completion callback runs, not merely until background work returns. It uses Executor.Execute, whereas LatestRequest can use the optional context-aware executor extension. This is per-presenter admission control, not database idempotency or a guarantee against another process submitting the same intent.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Stop admission atomically with work accounting</h2>
    <pre><code class="language-go">e.mu.Lock()
if e.closed {
    e.mu.Unlock()
    return false
}
e.work.Add(1)
e.mu.Unlock()

go func() {
    defer e.work.Done()
    fn()
}()
return true</code></pre>
    <div class="callout">The accepted-work count must be incremented before Close can stop admission and begin waiting.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/toolkits/gui/executor.go">Code: pkg/toolkits/gui/executor.go</a></p>
    <aside class="notes">Exact TryExecute core. Close takes the same mutex, sets closed, cancels its lifetime context, unlocks, then waits. Moving Add outside the admission lock would allow shutdown to miss work accepted just before closure. Execute intentionally discards the acceptance bool; owners that need rejection visibility use TryExecute or ExecuteContext. Producers must stop before executor shutdown.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Closing the window is an ordered protocol</h2>
    <pre><code class="language-text">desktop.Close, guarded by sync.Once:
  stop change monitor; wait for its delivery goroutine
  close dashboard's separately owned lifecycle
  close executor: reject new work, cancel reads, drain
  close UI dispatcher gate
  close application/store
  close log and telemetry resources

Dashboard stops before executor admission closes.</code></pre>
    <div class="callout">The ordering prevents a producer from counting work the executor will reject, or a worker from reaching a closed database.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/main/gui/desktop.go">Code: main/gui/desktop.go</a></p>
    <aside class="notes">Exact dependency order from desktop.Close. The dashboard has its own activation/work accounting; closing the executor first could strand that accounting. ManagedExecutor cancellation interrupts context-aware loads, while accepted plain work is drained. The UI gate prevents queued publications from reaching closed presentation state. This ordering is a composition responsibility, not something every domain presenter should implement.</aside>
  </section>

  <section class="implementation-slide">
    <h2>The publication gate checks queued callbacks again</h2>
    <pre><code class="language-go">d.dispatcher.Dispatch(func() {
    d.mu.Lock()
    if d.closed {
        d.mu.Unlock()
        return
    }
    d.active++
    d.mu.Unlock()
    defer finishAndSignalDrained()
    fn()
})

// Close sets closed and waits for active callbacks only.</code></pre>
    <div class="callout">Queued is not active. Shutdown drops queued callbacks while allowing already-active callbacks to finish.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/toolkits/gui/dispatcher.go">Code: pkg/toolkits/gui/dispatcher.go</a></p>
    <aside class="notes">Adapted GatedDispatcher body: finishAndSignalDrained abbreviates the deferred decrement and condition broadcast. There is also an early closed check before enqueueing. The callback-time check closes the race between enqueue and shutdown. Close waits only for callbacks that passed the inner gate, so it need not execute the entire UI queue. Do not call blocking Close from inside its own active callback.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Hold real domain work open while closing the desktop</h2>
    <pre><code class="language-text">start two accepted tasks:
  Ingredients.Count
  Ingredients.Create
both wait on a controlled release channel

start desktop.Close in another goroutine
assert Close has not returned
assert the store is still queryable

release both tasks
assert both domain calls succeed
assert Close then completes</code></pre>
    <div class="callout">A toolkit-only test cannot prove that process shutdown keeps the real application alive long enough.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/main/gui/desktop_test.go">Code: main/gui/desktop_test.go</a></p>
    <aside class="notes">Scenario from TestDesktopCloseDrainsRealDomainLoadAndMutationBeforeStoreShutdown. The test uses a real managed executor, isolated database, application session, and domain operations. The release channel controls timing; assertions check store lifetime and returned errors. Run with -tags ci. Separate tests cover executor rejection, cancellation, and queued publication dropping.</aside>
  </section>
</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Surfaces 4.3</div><h1>Use the third surface as an architecture test</h1><p class="lede">Difference creates pressure. Pressure reveals misplaced ownership.</p><div class="section-no">4.3</div></section>

  <section>
    <h2>Preserve application behavior in each interface</h2>
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
    <div class="cards four"><div class="card"><div class="number">1</div><h3>Choose difference</h3><p>Add a runtime with a different interaction model.</p></div><div class="card"><div class="number">2</div><h3>Define parity</h3><p>List durable behavior, not screen shapes.</p></div><div class="card"><div class="number">3</div><h3>Route findings</h3><p>Name the owning boundary and add an executable rule.</p></div><div class="card"><div class="number">4</div><h3>Update all callers</h3><p>Fix the shared behavior, then adapt each interface.</p></div></div>
  </section>
  <section class="implementation-slide">
    <h2>The parity test crosses a real process boundary</h2>
    <pre><code class="language-go">// CLI runs as a built executable in a temporary directory.
run("tags", "add", ingredientID, "origin=cli")

// A composed desktop opens the same database.
driver.Type(tagginggui.ControlValue, "origin=fyne")
driver.Tap(tagginggui.ControlSubmit)
// Assert the GUI result, then close desktop and GUI app.

output := run("tags", "list", ingredientID)
testutil.ErrorIf(t, !strings.Contains(output, "origin=fyne"),
    "CLI did not observe Fyne tag after a fresh lifecycle:\n%s", output)</code></pre>
    <div class="callout">The assertion observes persisted state through another adapter after shutdown. It cannot pass merely because two presenters share a fixture.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/main/gui/cross_surface_test.go">Code: main/gui/cross_surface_test.go</a></p>
    <aside class="notes">Excerpt from TestCLIAndComposedDesktopShareIngredientInventoryAuditAndTagContracts; navigation and selection setup is omitted. This test explicitly refreshes the composed desktop. Automatic external-commit refresh has its own test in main/gui/desktop_test.go. Distinguish those proofs rather than claiming one test covers both.</aside>
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
    <div class="ownership"><div><h3>Shared contracts</h3><ul><li>public models</li><li>queries and events</li><li>action meaning</li><li>typed errors</li><li>observable outcomes</li></ul></div><div class="shared"><h3>Application boundary</h3><ul><li>public operations</li><li>business rules</li><li>authorization</li><li>transaction ownership</li><li>atomic composition</li></ul></div><div><h3>Bespoke</h3><ul><li>focus and selection</li><li>widget or terminal state</li><li>async request state</li><li>navigation mechanics</li><li>rendering</li></ul></div></div>
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
    <div class="cards"><div class="card"><h3>Application composition</h3><p>Participates in a caller transaction or opens one shared unit of work.</p></div><div class="card"><h3>Narrow contract</h3><p><code>TaggableEntity</code> exposes only <code>EntityUID</code> and <code>SetTags</code>.</p></div><div class="card"><h3>Bespoke interaction</h3><p>Each surface keeps parsing, confirmation, form state, and feedback native.</p></div></div>
    <div class="callout">Invalid tags never start the mutation. A replacement failure rolls the domain change back with it.</div>
    <p class="source"><a href="/projects/go-modular-monolith/">Adjacent project commentary: atomic tagged mutations</a></p>
  </section>

  <section>
    <h2>Use all three interfaces to locate shared behavior</h2>
    <div class="split"><div class="side"><h3>If all three need it</h3><p>It may belong in the application: dashboard aggregation, atomic tagged mutation, action projection.</p></div><div class="bridge">△</div><div class="side"><h3>If only one runtime needs it</h3><p>It probably belongs in that toolkit or surface: cursor history, dialog ownership, terminal layout.</p></div></div>
    <div class="callout">Share meaning. Specialize interaction. Test equality at the application boundary.</div>
  </section>
  <section class="implementation-slide">
    <h2>Test atomic composition by forcing the second step to fail</h2>
    <pre><code class="language-text">TestRunTaggedMutationRollsBackDomainMutationWhenTagReplacementFails

Fixture:
  ingredient name = "Before"
  audit count = N

Mutation callback:
  update the real ingredient to "After"
  return a syntactically valid, nonexistent tag target

Tags.Replace:
  fails to load that target

Assertions after the outer call:
  error != nil; ingredient name == "Before"; audit count == N</code></pre>
    <div class="callout">Even the first command's success activity rolls back with the failed composition. The UI must not report a partially saved form.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/tagged_mutation_test.go">Code: app/tagged_mutation_test.go</a></p>
    <aside class="notes">This is the actual adversarial test scenario, not a mocked rollback callback. The domain update runs through the real pipeline, then the returned target makes the normal tagging command fail. The fixture uses the same store and policy machinery as the application. Point from the test to CLI, TUI, and GUI call sites of RunTaggedMutation.</aside>
  </section>


  <section class="implementation-slide">
    <h2>A dashboard can be partial without inventing zeros</h2>
    <pre><code class="language-go">data := UnknownDashboard() // each count starts at -1
load := func(target *int, fn func() (int, error)) {
    value, err := fn()
    if err != nil {
        if first == nil &amp;&amp; !errors.IsPermission(err) {
            first = err
        }
        return
    }
    *target = value
}
// Return data plus the first non-permission error.</code></pre>
    <div class="callout">The aggregate distinguishes unknown from zero and keeps successful values when another query fails.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/dashboard.go">Code: app/dashboard.go</a></p>
    <aside class="notes">Selected code from app.Dashboard. Permission errors leave the target unknown without becoming the returned error. Domain counts may instead succeed with zero visible rows because their page stream elides denied resources. The dashboard reuses authorized domain queries; it is not a raw SQL overview. Unless the caller injects a shared transaction, its several queries are not promised to be one consistent database snapshot. A surface must render partial state deliberately.</aside>
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
    <aside class="notes">Immediate test implementations help verify ordinary transitions. For races, queue the executor and dispatcher separately: complete B before A, then run the pending callbacks and assert that only B becomes visible. Open the async tests in pkg/toolkits/gui. Follow with real Fyne controls using the ci build tag, then composed-process tests. Each level checks something the earlier one cannot.</aside>
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
  <section class="implementation-slide">
    <h2>Make an old result wait in the UI queue</h2>
    <pre><code class="language-go">executor := &amp;fynetest.ManualExecutor{}
dispatcher := &amp;fynetest.ManualDispatcher{}
request := gui.NewLatestRequest[int](executor, dispatcher)
// publish appends only Loaded values to values.

request.Load(func() (int, error) { return 1, nil }, publish)
executor.RunNext() // Result 1 is queued for publication.
request.Load(func() (int, error) { return 2, nil }, publish)
executor.RunNext()
dispatcher.Drain()

testutil.ErrorIf(t, len(values) != 1 || values[0] != 2,
    "published values = %v, want [2]", values)</code></pre>
    <div class="callout">Both computations finish before UI publication. Only result 2 may become visible; no timing assumptions or sleeps are needed.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/toolkits/gui/async_test.go">Code: pkg/toolkits/gui/async_test.go</a></p>
    <aside class="notes">Excerpt from TestLatestRequestChecksStalenessWhenUIPublicationRuns; the publish callback is summarized. Run go test -tags ci ./pkg/toolkits/gui -run TestLatestRequestChecksStalenessWhenUIPublicationRuns -v. Compare with the separate test that invalidates a request before its queued work starts.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Exercise actual controls by semantic identity</h2>
    <pre><code class="language-go">app := test.NewApp()
t.Cleanup(app.Quit)
entry := gui.NewEntry("drink-name")
tapped := false
button := gui.NewButton("save-drink", "Save",
    func() { tapped = true })
driver := fynetest.NewDriver(t, container.NewVBox(entry, button))

driver.Type("drink-name", "Gimlet")
driver.Tap("save-drink")
testutil.ErrorIf(t, entry.Text != "Gimlet" || !tapped,
    "entry=%q tapped=%v", entry.Text, tapped)</code></pre>
    <div class="callout">This verifies real widget wiring in Fyne's test app. Presenter tests alone would not catch a field or button bound to the wrong behavior.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/toolkits/gui/semantic_test.go">Code: pkg/toolkits/gui/semantic_test.go</a></p>
    <aside class="notes">Exact test body reflowed. The ci build tag selects the in-memory driver. This does not assert that pixels, focus styling, or assistive technology are correct. Follow it with the existing disabled-control and shortcut tests, then select a screenshot for visual review.</aside>
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
    <aside class="notes">Open pkg/presentation/actions/README.md and Menus' action projector. A projector calculates control state from authorization and business prerequisites; it does not draw a button. For an actor permitted to publish, readiness blockers produce Disabled with a reason. For an actor denied Publish, the result is Hidden before evaluating those reasons. An in-flight request may further disable a control in the view, but that transient state does not belong in the domain projector.</aside>
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
  <section class="implementation-slide">
    <h2>Permission runs before prerequisites</h2>
    <pre><code class="language-go">state := State{ID: control.ID, Visible: true, Enabled: true}
if authorize != nil {
    if err := authorize(ctx); err != nil {
        if errors.IsPermission(err) {
            state.Visible = false
            state.Enabled = false
            return state, nil
        }
        return State{}, err
    }
}
// Only now evaluate Conditions in declaration order.</code></pre>
    <div class="callout">A denial returns hidden state immediately. An evaluation failure returns an error, and prerequisites are not evaluated in either case.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/presentation/actions/actions.go">Code: pkg/presentation/actions/actions.go</a></p>
    <aside class="notes">Exact beginning of evaluateControl. This ordering both avoids unnecessary work and prevents a denied actor from learning a disabled reason. The outer evaluator wraps unexpected failures with control ID and condition index, which is the real call chain used in chapter 1.3.</aside>
  </section>

  <section class="implementation-slide">
    <h2>Inspect the values a surface actually receives</h2>
    <pre><code class="language-json">// Same illustrative control, three successful evaluations:
{"id":"publish","visible":false,"enabled":false}

{"id":"publish","visible":true,"enabled":false,
 "disabled_reason":"Recipe review required"}

{"id":"publish","visible":true,"enabled":true}

// A condition returning a dependency error instead produces:
// states == nil, err != nil</code></pre>
    <div class="callout">Permission denial, an unmet prerequisite, and evaluation failure are three different results. Only the first two become ordinary control state.</div>
    <p class="source"><a href="https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/pkg/presentation/actions/actions.go">Code: pkg/presentation/actions/actions.go</a></p>
    <aside class="notes">Illustrative JSON using the actual State tags; the reason text is supplied by the condition, not a universal repository constant. PresentError handles operational failure separately. Then compare these values with Menus' domain projector and each surface's transient Busy or form state. The command still rechecks authority and prerequisites on submission.</aside>
  </section>

</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Build path</div><h1>Walk the pressure, not the package tree</h1><p class="lede">Each chapter starts with a decision the business forces, then follows the mechanism that makes it durable.</p><div class="section-no">→</div></section>

  <section>
    <h2>The recording arc</h2>
    <div class="timeline"><div class="step"><strong>Ownership</strong><span>contexts + module contracts</span></div><div class="step"><strong>Protocol</strong><span>types + errors + policy</span></div><div class="step"><strong>Execution</strong><span>pipeline + transactions</span></div><div class="step"><strong>Evidence</strong><span>logs + metrics + audit</span></div><div class="step"><strong>Coordination</strong><span>events + tags + filters</span></div><div class="step"><strong>Pressure</strong><span>degradation + workflows</span></div><div class="step"><strong>Surfaces</strong><span>CLI + TUI + GUI</span></div></div>
  </section>

  <section>
    <h2>Keep the real command trace in frame</h2>
    <pre><code class="language-text">main/cli → domain CLI adapter → Orders.Place
  pipeline.Command
    begin or join transaction
      authorize input → commands.Place → authorize result
      dispatch OrderPlaced → Inventory + Menus handlers
      record successful activity
    commit (or let the outer transaction owner commit)
  render result</code></pre>
    <div class="callout">The pipeline surrounds the command. Its transaction also contains event reactions and successful audit recording.</div>
    <aside class="notes">On failure, a middleware-owned transaction rolls back before the separate failure activity is attempted. The result returns through the adapter that received input. For reads, switch to the query chain: load, hydrate, filter where applicable, authorize, and return. Query packages do not run the command pipeline by themselves.</aside>
  </section>

  <section>
    <h2>Make the next change in the right place</h2>
    <table class="matrix"><thead><tr><th>Requested change</th><th>Start here</th><th>Prove it with</th></tr></thead><tbody><tr><td>A new publication prerequisite</td><td>Menus readiness + Publish</td><td>report and command agree; failure preserves state</td></tr><tr><td>A reaction to a business event</td><td>consumer's handlers</td><td>owned effects, audit touches, rollback, regenerated wiring</td></tr><tr><td>A searchable domain field</td><td>public filter view + DAO hydration</td><td>exact matches, safe pushdown, authorized paging</td></tr><tr><td>A keyboard or layout improvement</td><td>matching surface or toolkit</td><td>interaction behavior with application rules preserved</td></tr></tbody></table>
    <aside class="notes">Pause for an onboarding exercise: choose one row and ask the engineer to identify the files before editing. For a publication rule, ask where its disabled reason comes from and what happens if state changes after projection. For an event reaction, ask whether it needs Handling and why. These questions test ownership understanding rather than memorization of folder names.</aside>
  </section>

  <section>
    <h2>Close each recording with observable evidence</h2>
    <div class="cards"><div class="card"><h3>Show the behavior</h3><p>Perform the operation, inspect affected state, and explain the result a person sees.</p></div><div class="card"><h3>Trace the decision</h3><p>Open the owner, its collaborators, and the transaction boundary. Explain the failure this design prevents.</p></div><div class="card"><h3>Prove the guarantee</h3><p>Run the focused behavior test and relevant architecture or generation checks.</p></div></div>
    <div class="callout">Start application tests with <code>testutil.NewFixture(t)</code>. It supplies an isolated database and the real authorization, event, transaction, and audit paths.</div>
    <aside class="notes">Use docs/development.md for the complete CI sequence. Typical local steps are go generate ./..., go build ./..., go test ./..., and go tool arch-lint -config=.arch-lint.yaml; GUI tests use the documented ci build tag for the in-memory driver. Commit generated output with its source. End the video by asking what breaks if the demonstrated boundary is removed, and point to the test that catches it.</aside>
  </section>

  <section class="centered">
    <div class="eyebrow">The destination</div>
    <h1>One application.<br>Many honest boundaries.</h1>
    <p class="lede">The monolith is the deployment choice. Modularity is the behavior we keep proving.</p>
    <p class="source">github.com/TheFellow/go-modular-monolith · thefellow.github.io/series/mixology/</p>
  </section>
</section>
