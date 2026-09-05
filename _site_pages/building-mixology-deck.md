---
title: "Building Mixology: The Slide Deck"
date: 2026-09-05
last_modified_at: 2026-09-05
permalink: /talks/building-mixology/
excerpt: "A visual, chapter-by-chapter walkthrough of the architecture, domain workflows, presentation surfaces, authorization, filtering, and SQLite persistence in go-modular-monolith."
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
      <svg class="domain-lines" viewBox="0 0 1000 450" aria-hidden="true"><defs><marker id="arrowhead" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><polygon points="0 0, 7 3.5, 0 7" fill="#63e6be"/></marker></defs><line x1="180" y1="220" x2="320" y2="90"/><line x1="180" y1="230" x2="320" y2="350"/><line x1="390" y1="90" x2="570" y2="90"/><line x1="390" y1="350" x2="790" y2="230" class="event"/><line x1="630" y1="90" x2="790" y2="200"/><line x1="790" y1="245" x2="390" y2="350" class="event"/><line x1="460" y1="220" x2="785" y2="220"/><line x1="460" y1="240" x2="590" y2="350"/></svg>
      <div class="domain ingredients">Ingredients<small>catalog + retirement</small></div><div class="domain drinks">Drinks<small>recipes</small></div><div class="domain inventory">Inventory<small>stock</small></div><div class="domain menus">Menus<small>curation + publication</small></div><div class="domain orders">Orders<small>lifecycle</small></div><div class="domain audit">Audit<small>append-only activity</small></div><div class="domain tagging">Tagging<small>associations</small></div>
    </div>
    <div class="legend"><span><i></i> public query</span><span><i class="event"></i> public event</span></div>
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
    <div class="eyebrow">Chapter one</div><h1>Make architectural intent executable</h1>
    <p class="lede">Eleven lessons for turning design claims into properties the repository can defend.</p><div class="section-no">01</div>
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
  <section class="centered section-slide">
    <div class="eyebrow">Chapter two</div><h1>Turn calls into boundaries</h1>
    <p class="lede">Ingredient retirement changes four domains without giving Ingredients four collaborators.</p><div class="section-no">02</div>
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
    <h2>Package rules preserve the dependency direction</h2>
    <div class="rule-list"><div class="rule"><b>×</b><span><code>commands-emit-own-domain-events</code></span></div><div class="rule"><b>×</b><span><code>handlers-no-commands</code></span></div><div class="rule"><b>×</b><span><code>handlers-no-modules</code></span></div><div class="rule"><b>×</b><span><code>queries-no-commands</code></span></div></div>
    <div class="big-statement">The event changes the dependency direction. The analyzer keeps it changed.</div>
  </section>
</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Chapter three</div><h1>Preserve truth through degradation</h1><p class="lede">A system can remain operational without pretending its state is healthy.</p><div class="section-no">03</div></section>

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
  <section class="centered section-slide"><div class="eyebrow">Chapter four</div><h1>Grow a reciprocal workflow</h1><p class="lede"><span class="decision">planned workshop</span><br>Add Procurement only when the new business loop teaches something the current seven contexts cannot.</p><div class="section-no">04</div></section>

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
  <section class="centered section-slide"><div class="eyebrow">Chapter five</div><h1>Build a TUI toolkit without hiding the app</h1><p class="lede">Borrow MVVM’s presentation seam and Elm’s explicit loop, then let Go set the shape.</p><div class="section-no">05</div></section>

  <section>
    <h2>Two lineages, one adaptation</h2>
    <div class="split"><div class="side"><h3>MVVM contributes</h3><p>Screen-owned presentation state, commands, standard view shapes, and testable view models.</p></div><div class="bridge">+</div><div class="side"><h3>The Elm Architecture contributes</h3><p><code>Model</code>, typed messages, explicit <code>Update</code>, rendered <code>View</code>, and effects as commands.</p></div></div>
    <div class="big-statement">Interfaces replace base classes. Messages replace binding notifications. Constructors replace runtime discovery.</div>
  </section>

  <section>
    <h2>The shell owns application concerns</h2>
    <div class="ownership"><div><h3>Domain surface</h3><ul><li>drink workflows</li><li>menu publication</li><li>order lifecycle</li><li>domain action keys</li></ul></div><div class="shared"><h3>Root application shell</h3><ul><li>current route and back stack</li><li>cached view models</li><li>global title, status, help</li><li>terminal size and global keys</li><li>explicit domain construction</li></ul></div><div><h3>TUI toolkit</h3><ul><li>list/detail</li><li>forms and dialogs</li><li>spinners and layout</li><li>test drivers</li></ul></div></div>
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
    <h2>Typed messages keep ownership visible</h2>
    <div class="flow"><div class="node"><strong>Interaction</strong>shell routes input</div><div class="arrow">→</div><div class="node"><strong>Update</strong>domain screen</div><div class="arrow">→</div><div class="node"><strong>Cmd</strong>application call</div><div class="arrow">→</div><div class="node"><strong>typed Msg</strong>result returns</div></div>
    <div class="cards two"><div class="card"><h3>Reusable mechanics</h3><p>Generic list items retain their typed domain values while satisfying Bubbles interfaces.</p></div><div class="card"><h3>Domain choices</h3><p>Publish, complete, cancel, adjust, and retire remain bindings owned by their domain adapters.</p></div></div>
  </section>

  <section>
    <h2>Tests follow the ownership</h2>
    <div class="evidence-ladder"><div class="rung">pure presentation model tests</div><div class="rung">component update and rendering tests</div><div class="rung">domain surface tests</div><div class="rung">real Bubble Tea program driver</div><div class="rung">root navigation and input ownership</div><div class="rung">cross-surface persisted behavior</div></div>
  </section>
</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Chapter six</div><h1>Grow a retained-mode GUI in slices</h1><p class="lede">Fyne changes the interaction model, so the adapter should change too.</p><div class="section-no">06</div></section>

  <section>
    <h2>Start from the application seam</h2>
    <div class="layers"><div class="layer"><strong><code>main/gui</code></strong><span>database, actor, logs, application, session, native lifecycle</span></div><div class="layer"><strong>domain GUI surfaces</strong><span>presenters and views shaped for each bounded context</span></div><div class="layer"><strong><code>pkg/toolkits/gui</code></strong><span>shell, forms, tables, semantic controls, dialogs, executors</span></div><div class="layer private"><strong>Fyne runtime</strong><span>retained widgets, callbacks, windows, platform event loop</span></div></div>
  </section>

  <section>
    <h2>Adapt MVVM to retained widgets</h2>
    <div class="ownership"><div><h3>Presentation model</h3><ul><li>plain state</li><li>validation</li><li>latest-request ownership</li><li>no native widgets</li></ul></div><div class="shared"><h3>Presenter</h3><ul><li>loads through application</li><li>publishes deterministic state</li><li>owns submission and errors</li><li>uses injected dialogs</li></ul></div><div><h3>View</h3><ul><li>Fyne controls</li><li>focus and selection</li><li>pointer bindings</li><li>native rendering</li></ul></div></div>
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
  <section class="centered section-slide"><div class="eyebrow">Chapter seven</div><h1>Use the third surface as an architecture test</h1><p class="lede">Difference creates pressure. Pressure reveals misplaced ownership.</p><div class="section-no">07</div></section>

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
  <section class="centered section-slide"><div class="eyebrow">Chapter eight</div><h1>Share behavior, keep views bespoke</h1><p class="lede">Consistency lives in contracts and outcomes, not identical presentation internals.</p><div class="section-no">08</div></section>

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
  <section class="centered section-slide"><div class="eyebrow">Chapter nine</div><h1>Test native desktop behavior headlessly</h1><p class="lede">Confidence comes from a ladder of distinct evidence, not one giant simulated UI test.</p><div class="section-no">09</div></section>

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
  <section class="centered section-slide"><div class="eyebrow">Chapter ten</div><h1>Authorization is part of navigation</h1><p class="lede">A policy decision changes what can be discovered, counted, selected, and attempted.</p><div class="section-no">10</div></section>

  <section>
    <h2>One decision appears at four scales</h2>
    <div class="cards four"><div class="card"><h3>Workspace</h3><p>Can the actor discover this area?</p></div><div class="card"><h3>Aggregate</h3><p>Can a count reveal hidden records?</p></div><div class="card"><h3>Row</h3><p>Which results survive authorization?</p></div><div class="card"><h3>Action</h3><p>What may happen to this resource now?</p></div></div>
    <div class="callout">A route is a promise of an authorized read path, not a hard-coded item in a global menu.</div>
  </section>

  <section>
    <h2>Lists filter; failures still fail</h2>
    <div class="flow"><div class="node"><strong>DAO</strong>stable cursor stream</div><div class="arrow">→</div><div class="node"><strong>hydrate</strong>complete domain model</div><div class="arrow">→</div><div class="node"><strong>Cedar</strong>authorize each row</div><div class="arrow">→</div><div class="node"><strong>page</strong>fill with visible rows</div></div>
    <div class="cards two"><div class="card"><h3>Permission denial</h3><p>Omit the row and continue until the page is full or input ends.</p></div><div class="card stop"><h3>Evaluation failure</h3><p>Return the error. Infrastructure trouble is not “no results.”</p></div></div>
  </section>

  <section>
    <h2>Denied is different from unavailable</h2>
    <table class="matrix"><thead><tr><th>State</th><th>Presentation</th><th>Meaning</th></tr></thead><tbody><tr><td>Denied</td><td class="no">omit action</td><td>The actor lacks permission.</td></tr><tr><td>Authorized + blocked</td><td class="maybe">visible, disabled, explained</td><td>A domain prerequisite is unmet.</td></tr><tr><td>Authorized + ready</td><td class="yes">visible, enabled</td><td>The projected state permits an attempt.</td></tr></tbody></table>
    <div class="callout">The command re-authorizes and re-checks current state inside the transaction, then commits mutation, events, and audit atomically.</div>
  </section>

  <section>
    <h2>Counts are queries too</h2>
    <div class="big-statement">A dashboard that hides rows but shows the total still leaks the hidden rows.</div>
    <div class="split"><div class="side"><h3>Wrong</h3><p><code>SELECT count(*)</code>, then authorize the widget.</p><p class="coral">The number already escaped.</p></div><div class="bridge">→</div><div class="side"><h3>Correct</h3><p>Compute the count after row-level authorization, or expose unavailable when the aggregate cannot be authorized.</p><p class="accent">No hidden existence leak.</p></div></div>
    <p class="source">authorized and empty = 0 · denied = omitted · operational failure = unavailable</p>
  </section>
</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Chapter eleven</div><h1>Give people and programs one filter language</h1><p class="lede">Typed expressions remain the contract. SQLite is an execution detail that may optimize only what stays exact.</p><div class="section-no">11</div></section>

  <section>
    <h2>Borrow a compiler, own the contract</h2>
    <div class="flow five"><div class="node"><strong>text</strong>user expression</div><div class="arrow">→</div><div class="node"><strong>parse</strong>AST</div><div class="arrow">→</div><div class="node"><strong>type check</strong>domain environment</div><div class="arrow">→</div><div class="node"><strong>plan</strong>pushdown + residual</div><div class="arrow">→</div><div class="node"><strong>evaluate</strong>exact semantics</div></div>
    <div class="callout">The public language stays above persistence. A domain exposes fields and types, not JSON paths or SQL fragments.</div>
  </section>

  <section>
    <h2>Push down only what remains true</h2>
    <table class="matrix"><thead><tr><th>Expression shape</th><th>SQLite candidate plan</th><th>Exact evaluation</th></tr></thead><tbody><tr><td>persisted equality / range</td><td class="yes">push down</td><td>complete compiled expression</td></tr><tr><td>set membership</td><td class="yes">push down</td><td>complete compiled expression</td></tr><tr><td>safe conjunction</td><td class="yes">push safe terms</td><td>complete compiled expression</td></tr><tr><td>unsafe disjunction</td><td class="no">do not partially narrow</td><td>complete compiled expression</td></tr><tr><td>derived or hydrated field</td><td class="no">cannot push</td><td>hydrate, then evaluate all</td></tr></tbody></table>
  </section>

  <section>
    <h2>Partial <code>AND</code> can be safe. Partial <code>OR</code> cannot.</h2>
    <div class="split"><div class="side"><h3><code>A AND B</code></h3><p>If SQLite safely selects every possible <code>A</code>, residual <code>B</code> can narrow the candidates.</p><p class="accent">No true result is lost.</p></div><div class="bridge">≠</div><div class="side"><h3><code>A OR B</code></h3><p>Selecting only pushable <code>A</code> would discard rows that satisfy residual <code>B</code>.</p><p class="coral">Semantics change.</p></div></div>
  </section>

  <section>
    <h2>Hydrate before exact evaluation</h2>
    <div class="flow"><div class="node"><strong>SQL</strong>candidate rows</div><div class="arrow">→</div><div class="node"><strong>domain DAO</strong>hydrate related state</div><div class="arrow">→</div><div class="node"><strong>typed filter</strong>exact predicate</div><div class="arrow">→</div><div class="node"><strong>authorization</strong>visible page</div></div>
    <div class="callout">Concrete DAOs remain concrete because only the owning domain knows how a stored row becomes a complete model.</div>
  </section>
</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Chapter twelve</div><h1>Project actions, not widgets</h1><p class="lede">Share durable action meaning across interfaces without sharing runtime state.</p><div class="section-no">12</div></section>

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
  <section class="centered section-slide"><div class="eyebrow">Chapter thirteen</div><h1>Replace persistence without replacing the app</h1><p class="lede">The bstore-to-SQLite migration tested whether the store was truly a boundary.</p><div class="section-no">13</div></section>

  <section>
    <h2>Preserve the contract, replace the engine</h2>
    <div class="split"><div class="side"><h3>Application keeps</h3><p>Typed queries, transactions, errors, revisions, domain-owned DAOs, middleware ordering, and observable behavior.</p></div><div class="bridge">⇄</div><div class="side"><h3>Store changes</h3><p>SQLite records, migrations, JSON-field plans, WAL, busy handling, immediate writes, and connection-local invalidation.</p></div></div>
  </section>

  <section>
    <h2>SQLite without SQL in every domain</h2>
    <div class="layers"><div class="layer"><strong>Domain model</strong><span>owns meaning, validation, and hydrated relationships</span></div><div class="layer"><strong>Private row</strong><span>declares ID, revision, JSON data, uniqueness, and expression indexes</span></div><div class="layer"><strong>Typed store query</strong><span>equality, ranges, membership, ordering, cursor, pushdown</span></div><div class="layer private"><strong>SQLite</strong><span>generic record table plus domain-declared indexes and migrations</span></div></div>
  </section>

  <section>
    <h2>Several processes, one local file</h2>
    <div class="cards four"><div class="card"><h3>WAL</h3><p>Readers continue while another connection commits.</p></div><div class="card"><h3>10 s busy timeout</h3><p>Writers wait for the single write slot.</p></div><div class="card"><h3>Immediate writes</h3><p>Avoid deferred read-to-write upgrade races.</p></div><div class="card"><h3>Local filesystem</h3><p>One machine, never a shared network filesystem.</p></div></div>
    <div class="callout">Concurrency is explicit, not magical. SQLite serializes writes, and application transactions stay short.</div>
  </section>

  <section>
    <h2>Stale writes fail at the boundary</h2>
    <div class="flow"><div class="node"><strong>read</strong>revision 7</div><div class="arrow">→</div><div class="node"><strong>another process</strong>updates to 8</div><div class="arrow">→</div><div class="node"><strong>UPDATE</strong>WHERE revision = 7</div><div class="arrow">→</div><div class="node"><strong>typed conflict</strong>no overwrite</div></div>
    <pre><code class="language-sql">UPDATE records
SET data = ?, revision = revision + 1
WHERE model = ? AND id = ? AND revision = ?;</code></pre>
  </section>

  <section>
    <h2>Invalidation means “query again”</h2>
    <div class="flow"><div class="node"><strong>pinned connection</strong>PRAGMA data_version</div><div class="arrow">→</div><div class="node"><strong>lossy signal</strong>coalesced edge</div><div class="arrow">→</div><div class="node"><strong>persistent client</strong>refresh request</div><div class="arrow">→</div><div class="node"><strong>application query</strong>auth + hydrate</div></div>
    <div class="callout">The monitor carries no record payload and is not a durable event stream. Multiple commits may collapse into one signal.</div>
    <p class="source">Rolled-back writes do not signal. Reconnect emits one invalidation because commits may have been missed.</p>
  </section>

  <section>
    <h2>Treat the file format honestly</h2>
    <div class="big-statement">A bstore database is not a SQLite database.</div>
    <div class="cards two"><div class="card"><h3>Disposable data</h3><p>Reseed into a fresh SQLite file.</p></div><div class="card warn"><h3>Valuable data</h3><p>Export with the previous version, import into a fresh database, verify, and keep the backup.</p></div></div>
  </section>
</section>

<section>
  <section class="centered section-slide"><div class="eyebrow">Build path</div><h1>Walk the pressure, not the package tree</h1><p class="lede">Each chapter starts with a decision the business forces, then follows the mechanism that makes it durable.</p><div class="section-no">→</div></section>

  <section>
    <h2>The recording arc</h2>
    <div class="timeline"><div class="step"><strong>Premise</strong><span>ownership + executable rules</span></div><div class="step"><strong>Pressure</strong><span>retirement + degradation</span></div><div class="step"><strong>Coordination</strong><span>transactional fan-out</span></div><div class="step"><strong>Interfaces</strong><span>TUI + GUI + parity</span></div><div class="step"><strong>Policy</strong><span>navigation + actions</span></div><div class="step"><strong>Queries</strong><span>filters + authorization</span></div><div class="step"><strong>Persistence</strong><span>SQLite + concurrency</span></div></div>
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
