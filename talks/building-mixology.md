<!-- Generated from https://thefellow.github.io/talks/building-mixology/ by scripts/generate_llm_content.py; do not edit. -->

# Building Mixology: The Slide Deck

Source: [https://thefellow.github.io/talks/building-mixology/](https://thefellow.github.io/talks/building-mixology/)

## Pyramid summary

- **~2 words:** Mixology deck
- **~8 words:** A visual walkthrough of Mixology's executable modular architecture.
- **Expanded:** A visual, chapter-by-chapter walkthrough of the architecture, domain workflows, presentation surfaces, authorization, filtering, and SQLite persistence in go-modular-monolith.

## Full content

Building Mixology
  <h1>A modular monolith that has to prove it</h1>
  One Go application. Seven bounded contexts. Three native interfaces. One architecture made executable.

  ← / → chapter↑ / ↓ detail<b>S</b> speaker view<b>Esc</b> map
  <aside class="notes">This is the map behind the video series. Each horizontal chapter can stand alone. The vertical slides are the concrete route through that chapter.</aside>

    Orientation
    <h1>Why this application exists</h1>
    Architecture is the set of changes the codebase makes easy, and the shortcuts it refuses.

    00

    ## The problem is not folders

      ### A package diagramShows the path we intended when the repository was young.
It cannot stop the next convenient import.

      ≠
      ### An executable boundaryMakes ownership visible in APIs, types, transactions, generators, tests, and import rules.
The shortest wrong path fails.

    The reference application is a cocktail bar because inventory, recipes, menus, and orders create real pressure between domains.

    ## One deployable, seven owners

      Ingredients<small>catalog + retirement</small>Drinks<small>recipes</small>Inventory<small>stock</small>Menus<small>curation + publication</small>Orders<small>lifecycle</small>Audit<small>append-only activity</small>Tagging<small>associations</small>

    <i></i> public query<i class="event"></i> public event

    ## The current trace

      **main/<surface>**process composition→
      **surfaces/<surface>**domain presentation→
      **module.go**public facade→
      **queries / internal**behavior + storage

      ### CLIOne command, one fresh operation context.
### Bubble Tea TUIPersistent session, message-driven presentation.
### Fyne GUIRetained native widgets and managed lifecycle.

    All three enter the same application behavior and local SQLite database. Views are adapters, not alternate applications.

    Chapter one<h1>Make architectural intent executable</h1>
    Eleven lessons for turning design claims into properties the repository can defend.
01

    ## A boundary should resist the shortest path

      **Public facade**<code>app/domains/drinks</code> composes and exposes supported behavior.
      **Public contracts**<code>models</code>, <code>queries</code>, and <code>events</code> are deliberate collaboration seams.
      **Event handlers**<code>handlers</code> consume public facts and mutate only their owning domain.
      **Private work**<code>internal/commands</code> and <code>internal/dao</code> remain implementation details.

    If a neighboring domain can import the command that “just does the thing,” ownership is only a suggestion.

    ## Let types carry the distinctions they can

      ### Generated entity IDs<code>DrinkID</code> and <code>IngredientID</code> share the same generated Cedar method shape without becoming interchangeable parameters.

      ### Closed amount variantsAn unexported <code>isAmount</code> method limits <code>Amount</code> to volume and discrete quantities owned by the kernel.

      ### Validated valuesCurrency, price, quantity, and tag parsers turn accepted external text into domain-shaped values.

    Go still permits zero values and package-local construction. Constructors, decoding validation, and boundary checks carry the guarantees the type system cannot.
    [Adjacent article: Making Illegal States Unrepresentable in Go](/articles/making-illegal-states-unrepresentable-in-go.md)

    ## One path through the application

      SerializeTransactionLogging + MetricsTrackActivityUnitOfWork beginsload → authorize → handle → authorize resultdispatch events → record successcommit everything, or nothing

    Commands do not opt into transactions, authorization, events, or audit independently. The shared path owns the ordering.
    <aside class="notes">This is runtime and unwind order. NewChain lists nested middleware outside-in, so the source declaration reads differently around dispatch and successful activity.</aside>

    ## Go 1.27 puts the operation on its owner

      Before<code class="language-go">spec := middleware.CommandSpec[
    Input, Output,
]{
    Action: authz.ActionCreate,
    Load:   load,
    Handle: m.commands.Create,
}
return middleware.RunCommand(
    m.pipeline, ctx, spec,
)</code></pre>
      →
      Go 1.27<pre><code class="language-go">m.pipeline.Command(
    ctx,
    authz.ActionCreate,
    input,
    m.commands.Create,
)</code></pre><p class="accent">The configured pipeline is the obvious starting point.

    The completed migration removed <code>RunCommand</code> and <code>CommandSpec</code>. Domain facades now enter through the pipeline methods directly.

    ## Six typed entries, one middleware model

      ### <code>Query</code>Load a Cedar entity, then authorize the result.
### <code>QueryResource</code>Authorize a known resource around a non-entity result.
### <code>PageQuery</code>Fill a page with authorized rows without leaking denied ones.

      ### <code>Command</code>Authorize caller input and resulting state.
### <code>LoadCommand</code>Load trusted state inside the transaction.
### <code>LoadCommandActions</code>Derive transition-specific action requirements from loaded state.

    This removed wrappers and specification ceremony. Transactions, authorization, events, audit, paging, and failure behavior did not change.
    [Adjacent note: Go 1.27 Generic Methods and the Mixology Pipeline](/notes/go-1-27-generic-methods-and-the-mixology-pipeline.md)

    ## Compiler, generator, analyzer, test
    <table class="matrix"><thead><tr><th>Rule</th><th>Best carrier</th><th>Example</th></tr></thead><tbody>
      <tr><td>Coarse package privacy</td><td>Go compiler</td><td><code>internal</code> blocks callers outside the owning tree</td></tr>
      <tr><td>Fine package allowlist</td><td><code>arch-lint</code></td><td>only facades, queries, handlers, and internals may consume domain internals</td></tr>
      <tr><td>Repetitive wiring</td><td>Generator</td><td>Event and Cedar registration</td></tr>
      <tr><td>Repository topology</td><td><code>arch-lint</code></td><td>Surfaces stay bespoke; handlers cannot import commands</td></tr>
      <tr><td>Composition completeness</td><td>Architecture test</td><td>Every domain is initialized by <code>app.New</code></td></tr>
      <tr><td>Business behavior</td><td>Integration test</td><td>Retirement rolls back as one operation</td></tr>
    </tbody></table>

    ## Capture ownership instead of naming every module

      ### Capture the imported target<code class="language-yaml"># imported target
forbid:
  - app/domains/{module}/internal/**

# permitted importers reuse {module}
except:
  - app/domains/{module}
  - app/domains/{module}/queries/**
  - app/domains/{module}/handlers/**
  - app/domains/{module}/internal/**</code></pre>
      ∧
      ### Importer must share ownership<p>The forbidden import captures <code>{module}</code>. Importer exceptions reuse that value, so Drinks cannot claim Ingredients’ private implementation.
One rule covers every current and future domain.

    ## Future adapters inherit the rule
    **capture**<code>{module}</code> + <code>{surface}</code>→**forbid**concrete surface imports→**except**same module + surface→**fixture**CLI, TUI, GUI, and Web
    ### Allowed fixture<code>drinks/surfaces/web/valid</code> imports its own <code>drinks/surfaces/web</code> implementation.
### Rejected fixture<code>drinks/surfaces/web/invalid-gui</code> imports the GUI surface and domain-internal storage.

    The same adversarial fixture separately rejects cross-domain surfaces, mismatched toolkits, and <code>main</code> imports across the current adapters. It proves the configuration, not merely a clean tree.
    [Adjacent project: arch-lint](/projects/arch-lint.md) · <code>architecture/arch_lint_test.go</code>

    ## Spend complexity when the pressure appears

      **Folders**make ownership legible**Public contracts**separate questions from decisions**Events**reverse reactive dependencies**Two phases**preserve pre-mutation facts**Projection**share action meaning**SQLite**enable concurrent local clients**Rules**freeze lessons into checks

    The sequence matters. Each mechanism pays rent by solving a problem the working application has already made concrete.

    Chapter two<h1>Turn calls into boundaries</h1>
    Ingredient retirement changes four domains without giving Ingredients four collaborators.
02

    ## The tempting implementation
    <code class="language-go">func (m *Ingredients) Retire(ctx Context, id ID) error {
    m.inventory.Remove(ctx, id)
    m.drinks.ReplaceOrReview(ctx, id)
    m.orders.BlockSnapshots(ctx, id)
    m.menus.Recalculate(ctx, id)
    return m.ingredients.Retire(ctx, id)
}</code></pre>
    <b>×</b>Ingredients decides what retirement means everywhere.<b>×</b>The source domain imports every consumer.<b>×</b>Adding a reaction edits the initiating command.<b>×</b>The “simple” path becomes the system map.

    ## Separate questions from decisions
    ### Public query<p>“Is this ingredient referenced?”
Safe when the caller owns the decision that follows.
vs### Public event“This ingredient was retired with this explicit replacement intent.”
Each consumer owns its reaction.

    **Queries move information.** Events move facts. Neither exposes another domain’s command implementation.

    ## One fact, bounded fan-out
    **Ingredients**IngredientDeleted⇢**Drinks**rewrite future recipes or require review**Inventory**remove unusable stock**Orders**block affected snapshots, never rewrite history**Menus**recompute availability, preserve curation
    command mutation + four leaf reactions + touched entities + successful audit = one SQLite transaction

    ## The event dispatcher is generated glue
    **AddEvent**owned fact→**command returns**still in UoW→**Handling**all snapshots→**Handle**all reactions→**audit + commit**atomic result
    <code class="language-go">func (h *IngredientDeleted) Handling(
    ctx *middleware.HandlerContext,
    event ingredientsevents.IngredientDeleted,
) error // snapshot pre-mutation state

func (h *IngredientDeleted) Handle(
    ctx *middleware.HandlerContext,
    event ingredientsevents.IngredientDeleted,
) error // apply the owned reaction</code></pre>
    <code>HandlerContext</code> has transaction, principal, and <code>TouchEntity</code>. It deliberately has no <code>AddEvent</code>.

    ## Package rules preserve the dependency direction
    <b>×</b><code>commands-emit-own-domain-events</code><b>×</b><code>handlers-no-commands</code><b>×</b><code>handlers-no-modules</code><b>×</b><code>queries-no-commands</code>
    The event changes the dependency direction. The analyzer keeps it changed.

  Chapter three<h1>Preserve truth through degradation</h1><p class="lede">A system can remain operational without pretending its state is healthy.
03

    ## Retirement is a business decision
    <table class="matrix"><thead><tr><th>Reference</th><th>No replacement</th><th>Permanent replacement</th></tr></thead><tbody><tr><td>Required recipe component</td><td class="maybe">keep visible, review required</td><td class="yes">rewrite compatible future recipe</td></tr><tr><td>Optional component</td><td class="yes">remove from future recipe</td><td class="yes">rewrite when compatible</td></tr><tr><td>Accepted order snapshot</td><td class="no">block, preserve snapshot</td><td class="no">block, preserve snapshot</td></tr><tr><td>Published menu item</td><td class="maybe" colspan="2">preserve curation and recalculate current availability</td></tr></tbody></table>

    ## Three substitutions, three meanings
    ### Recipe substituteA modeled alternative inside the drink. It is not permission to rewrite the canonical recipe.
### Operational substitutionA temporary way to fulfill a drink. It affects readiness and availability.
### Permanent replacementExplicit retirement intent carried by the source event, including conversion.

    <code>IngredientDeleted{Replacement, ReplacementRatio}</code> carries explicit permanent intent.

    Similarity is not intent. Consumers must not infer permanent replacement from whatever substitute happens to be available.

    ## Rewrite plans. Preserve records.
    ### Future intentDraft recipes and menus may be rewritten, reviewed, or prevented from publication.
Plans can absorb new truth.
∥### Historical truthAccepted order snapshots keep the ingredient the customer actually ordered.
History can be blocked, never laundered.

    ## Degradation is not promotion
    published→degraded but honest│draft⤫known-bad publish
    ### Existing published menuMay remain published while item availability reflects new operational truth.
### Draft promotionReadiness blockers prevent publishing state already known to be unsuitable.

    ## Readiness belongs to Menus
    **Load menu**authorized state→**Evaluate**recipes + stock→**Report**blockers + warnings→**Publish**re-check in command
    ### BlockersInvalid canonical state, unavailable items, or temporary substitution.
### WarningsOperational concerns such as low stock that deserve visibility but not a false invariant.

  Chapter four<h1>Grow a reciprocal workflow</h1>planned workshop<br>Add Procurement only when the new business loop teaches something the current seven contexts cannot.
04

    ## The next build: stock creates demand
    **Inventory**stock becomes low⇢**Procurement**record demand→**Explicit operation**draft purchase order→**Supplier**ships goods⇢**Inventory**records receipt
    This chapter is a workshop plan, not current shipped behavior. The deck keeps that status explicit.

    ## Establish ownership before packages
    ### Inventory ownsOn-hand amount, reservation, thresholds, and stock facts.
### Procurement ownsSuppliers, offerings, purchase orders, receiving workflow, and commercial intent.
### Later: Analytics observesQueryable facts beside the completed slice. It does not become a dependency of the write path.

    ## Build the slice in visible increments
    **Suppliers**identity and offerings**Purchase orders**stateful lifecycle**Low-stock facts**draft demand, idempotently**Receipt facts**inventory reacts**Consistency view**show what converged**Workflow limit**find hidden coordination**Outbox**only if commit boundary moves

    ## When a handler becomes a workflow
    ### Leaf reactionOne fact, bounded local mutation, same transaction, no new event.
Keep it in a handler.
→### Process managerWaits over time, coordinates retries or compensations, tracks intermediate state, spans commits.
Name the workflow.

    Add an outbox when delivery must survive a transaction boundary. Do not use it to decorate a transaction that is already atomic.

  Chapter five<h1>Build a TUI toolkit without hiding the app</h1>Borrow MVVM’s presentation seam and Elm’s explicit loop, then let Go set the shape.
05

    ## Two lineages, one adaptation
    ### MVVM contributesScreen-owned presentation state, commands, standard view shapes, and testable view models.
+### The Elm Architecture contributes<code>Model</code>, typed messages, explicit <code>Update</code>, rendered <code>View</code>, and effects as commands.

    Interfaces replace base classes. Messages replace binding notifications. Constructors replace runtime discovery.

    ## The shell owns application concerns
    ### Domain surface- drink workflows- menu publication- order lifecycle- domain action keys### Root application shell- current route and back stack- cached view models- global title, status, help- terminal size and global keys- explicit domain construction### TUI toolkit- list/detail- forms and dialogs- spinners and layout- test drivers

    ## A deliberately small contract
    <code class="language-go">type ViewModel interface {
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
    The toolkit knows Bubble Tea. It does not know Drinks, Menus, Cedar actors, or the application composition root.

    ## Typed messages keep ownership visible
    **Interaction**shell routes input→**Update**domain screen→**Cmd**application call→**typed Msg**result returns
    ### Reusable mechanics<p>Generic list items retain their typed domain values while satisfying Bubbles interfaces.
### Domain choicesPublish, complete, cancel, adjust, and retire remain bindings owned by their domain adapters.

    ## Tests follow the ownership
    pure presentation model testscomponent update and rendering testsdomain surface testsreal Bubble Tea program driverroot navigation and input ownershipcross-surface persisted behavior

  Chapter six<h1>Grow a retained-mode GUI in slices</h1>Fyne changes the interaction model, so the adapter should change too.
06

    ## Start from the application seam
    **<code>main/gui</code>**database, actor, logs, application, session, native lifecycle**domain GUI surfaces**presenters and views shaped for each bounded context**<code>pkg/toolkits/gui</code>**shell, forms, tables, semantic controls, dialogs, executors**Fyne runtime**retained widgets, callbacks, windows, platform event loop

    ## Adapt MVVM to retained widgets
    ### Presentation model- plain state- validation- latest-request ownership- no native widgets### Presenter- loads through application- publishes deterministic state- owns submission and errors- uses injected dialogs### View- Fyne controls- focus and selection- pointer bindings- native rendering

    ## Reviewable slices kept the change surface small
    **Shell**routes + lifecycle**Models**state + errors**Toolkits**standard mechanics**Domains**workspace by workspace**Parity**paging + workflows**Lifecycle**drain accepted work**Evidence**process + visual checks

    ## The integration gaps were architectural clues
    ### DashboardMoved business-shaped aggregation into <code>app</code>.
### TagsNeeded one atomic application mutation.
### PagingHad to remain explicit and domain-backed.
### ShutdownRequired admission, drain, then store close.

    A third interface is useful precisely because it refuses to fit abstractions built around the first two.

  Chapter seven<h1>Use the third surface as an architecture test</h1>Difference creates pressure. Pressure reveals misplaced ownership.
07

    ## Parity is a union, not a porting checklist
    ### What every surface must preserveApplication capabilities, authorization, invariants, error meaning, atomicity, and persisted results.
∪### What each runtime teachesCLI composability, TUI keyboard flow, GUI retained state, async lifecycle, dialogs, and focus.

    ## Hidden ownership fails under a different runtime
    <table class="matrix"><thead><tr><th>Pressure</th><th>Revealed mistake</th><th>Durable correction</th></tr></thead><tbody><tr><td>Persistent dashboard</td><td>views assembled business aggregates</td><td>shared application read model</td></tr><tr><td>Tag editing</td><td>two commands could partially commit</td><td>atomic <code>RunTaggedMutation</code></td></tr><tr><td>GUI action state</td><td>views duplicated policy-shaped logic</td><td>domain action projectors</td></tr><tr><td>Native shutdown</td><td>store could close under accepted work</td><td>managed executor and gated dispatcher</td></tr></tbody></table>

    ## Cross-surface evidence crosses a boundary
    **CLI process**mutate→**SQLite**commit→**data_version**invalidate→**GUI / TUI**re-query
    Asserting that two presenters format similar fixtures is not cross-surface proof. Observe the same persisted application state through both adapters.

    ## A repeatable audit
    1### Choose differenceAdd a runtime with a different interaction model.
2### Define parityList durable behavior, not screen shapes.
3### Route findingsName the owning boundary and add an executable rule.
4### Repair inwardImprove shared seams, then update every surface.

  Chapter eight<h1>Share behavior, keep views bespoke</h1>Consistency lives in contracts and outcomes, not identical presentation internals.
08

    ## Each runtime has a different unit of interaction
    ### CLIInvocation, flags, stdin, stdout, exit status. State ends when the process ends.
### TUIMessages, commands, focus, terminal cells, key chords, and a continuous update loop.
### GUIRetained controls, pointer and keyboard events, background work, dispatch, and native lifecycle.

    ## The least common denominator is not neutral
    A universal view model either leaks one runtime into the others, or erases the affordances that made each runtime useful.
    ### Shared contracts- public models- queries and events- action meaning- typed errors- observable outcomes### Application boundary- the narrow waist- durable semantics- authorization- transaction ownership- atomic composition### Bespoke- focus and selection- widget or terminal state- async request state- navigation mechanics- rendering

    ## Reuse mechanics within a surface
    **CLI toolkit**JSON input and output, reflection-based tables**TUI toolkit**view contracts, list/detail, forms, dialogs, layout**GUI toolkit**shell, tables, semantic controls, executors, dispatchers**Domain surfaces**compose only the matching toolkit with domain workflows

    ## Cross-cutting does not mean ownerless
    **surface**desired tags→**RunTaggedMutation**validate + compose→**domain mutation**owned behavior+**Tags.Replace**owned association
    domain result + complete tag set = one transaction
    ### Application seamParticipates in a caller transaction or opens one shared unit of work.
### Narrow contract<code>TaggableEntity</code> exposes only <code>EntityUID</code> and <code>SetTags</code>.
### Bespoke interactionEach surface keeps parsing, confirmation, form state, and feedback native.

    Invalid tags never start the mutation. A replacement failure rolls the domain change back with it.
    [Adjacent project commentary: atomic tagged mutations](/projects/go-modular-monolith.md)

    ## Triangulation finds the durable seam
    ### If all three need itIt may belong in the application: dashboard aggregation, atomic tagged mutation, action projection.
△### If only one runtime needs itIt probably belongs in that toolkit or surface: cursor history, dialog ownership, terminal layout.

    Share meaning. Specialize interaction. Test equality at the application boundary.

  Chapter nine<h1>Test native desktop behavior headlessly</h1>Confidence comes from a ladder of distinct evidence, not one giant simulated UI test.
09

    ## The evidence ladder
    pure state + presenter with fake executor and dispatcherreal Fyne controls in the in-memory driverdialogs, composed shell, and close orderingfresh-process and cross-surface behaviorrace detector and target compilationpixels and manual accessibility evidence

    ## Inject execution and publication separately
    **Presenter**requests work→**Executor**runs off UI thread→**Dispatcher**returns to UI thread→**View**renders state
    ### Deterministic testImmediate executor and dispatcher expose state transitions without timing guesses.
### Production runtimeManaged executor and Fyne dispatcher preserve thread and shutdown ownership.

    ## Semantic controls carry behavior
    ### PointerButton activation reaches the guarded command.
### KeyboardShortcuts invoke the same enabled control, not a parallel code path.
### TestThe control exposes state and behavior without pixel coordinates.

    A disabled button, its shortcut, and its command must agree. Semantic controls make that one assertion.

    ## Pixels are different evidence
    <table class="matrix"><thead><tr><th>Question</th><th>Evidence</th></tr></thead><tbody><tr><td>Did the presenter compute the right state?</td><td>pure model and presenter tests</td></tr><tr><td>Did the widget wire that state correctly?</td><td>virtual window and semantic control tests</td></tr><tr><td>Does the composed process close safely?</td><td>lifecycle and fresh-process tests</td></tr><tr><td>Does it look right?</td><td>targeted screenshots and human review</td></tr><tr><td>Does assistive technology work?</td><td>manual platform protocol, not inferred from pixels</td></tr></tbody></table>

  Chapter ten<h1>Authorization is part of navigation</h1>A policy decision changes what can be discovered, counted, selected, and attempted.
10

    ## One decision appears at four scales
    ### WorkspaceCan the actor discover this area?
### AggregateCan a count reveal hidden records?
### RowWhich results survive authorization?
### ActionWhat may happen to this resource now?

    A route is a promise of an authorized read path, not a hard-coded item in a global menu.

    ## Lists filter; failures still fail
    **DAO**stable cursor stream→**hydrate**complete domain model→**Cedar**authorize each row→**page**fill with visible rows
    ### Permission denialOmit the row and continue until the page is full or input ends.
### Evaluation failureReturn the error. Infrastructure trouble is not “no results.”

    ## Denied is different from unavailable
    <table class="matrix"><thead><tr><th>State</th><th>Presentation</th><th>Meaning</th></tr></thead><tbody><tr><td>Denied</td><td class="no">omit action</td><td>The actor lacks permission.</td></tr><tr><td>Authorized + blocked</td><td class="maybe">visible, disabled, explained</td><td>A domain prerequisite is unmet.</td></tr><tr><td>Authorized + ready</td><td class="yes">visible, enabled</td><td>The projected state permits an attempt.</td></tr></tbody></table>
    The command re-authorizes and re-checks current state inside the transaction, then commits mutation, events, and audit atomically.

    ## Counts are queries too
    A dashboard that hides rows but shows the total still leaks the hidden rows.
    ### Wrong<code>SELECT count(*)</code>, then authorize the widget.
The number already escaped.
→### CorrectCompute the count after row-level authorization, or expose unavailable when the aggregate cannot be authorized.
No hidden existence leak.

    authorized and empty = 0 · denied = omitted · operational failure = unavailable

  Chapter eleven<h1>Give people and programs one filter language</h1>Typed expressions remain the contract. SQLite is an execution detail that may optimize only what stays exact.
11

    ## Borrow a compiler, own the contract
    **text**user expression→**parse**AST→**type check**domain environment→**plan**pushdown + residual→**evaluate**exact semantics
    The public language stays above persistence. A domain exposes fields and types, not JSON paths or SQL fragments.

    ## Push down only what remains true
    <table class="matrix"><thead><tr><th>Expression shape</th><th>SQLite candidate plan</th><th>Exact evaluation</th></tr></thead><tbody><tr><td>persisted equality / range</td><td class="yes">push down</td><td>complete compiled expression</td></tr><tr><td>set membership</td><td class="yes">push down</td><td>complete compiled expression</td></tr><tr><td>safe conjunction</td><td class="yes">push safe terms</td><td>complete compiled expression</td></tr><tr><td>unsafe disjunction</td><td class="no">do not partially narrow</td><td>complete compiled expression</td></tr><tr><td>derived or hydrated field</td><td class="no">cannot push</td><td>hydrate, then evaluate all</td></tr></tbody></table>

    ## Partial <code>AND</code> can be safe. Partial <code>OR</code> cannot.
    ### <code>A AND B</code>If SQLite safely selects every possible <code>A</code>, residual <code>B</code> can narrow the candidates.
No true result is lost.
≠### <code>A OR B</code>Selecting only pushable <code>A</code> would discard rows that satisfy residual <code>B</code>.
Semantics change.

    ## Hydrate before exact evaluation
    **SQL**candidate rows→**domain DAO**hydrate related state→**typed filter**exact predicate→**authorization**visible page
    Concrete DAOs remain concrete because only the owning domain knows how a stored row becomes a complete model.

  Chapter twelve<h1>Project actions, not widgets</h1>Share durable action meaning across interfaces without sharing runtime state.
12

    ## Give each state one meaning
    ### HiddenAuthorization denied. Do not advertise an operation the actor cannot perform.
### DisabledAuthorized, but a durable domain prerequisite is unmet. Keep the reason.
### EnabledAuthorized and currently eligible. The command still remains authoritative.

    ## Declare permission at the right scope
    <code class="language-go">declaration := actions.Group{
    Permission: actions.Require(canEdit),
    Controls: []actions.Control{
        {ID: "name"},
        {ID: "publish",
         Permission: actions.Require(canPublish),
         Conditions: []actions.Condition{saved, publishable}},
    },
}</code></pre>
    A group permission is an inherited default, not a permanent decision. Distinct operations override it explicitly.
    <p class="source">Permission runs before conditions, so denial never leaks disabled reasons.

    ## Project once, adapt natively
    **Domain projector**authorization + durable prerequisites⇢**TUI**bindings and help**GUI**buttons, menus, shortcuts**Future web**controls and explanations**Evaluation failure**operational error, never action state

    ## Projection guides. Commands enforce.
    load→authorize + project→state changes→command re-checks
    A polished control state is not a lock. Current authorization, revision, and invariants are checked inside the write transaction.

  Chapter thirteen<h1>Replace persistence without replacing the app</h1>The bstore-to-SQLite migration tested whether the store was truly a boundary.
13

    ## Preserve the contract, replace the engine
    ### Application keepsTyped queries, transactions, errors, revisions, domain-owned DAOs, middleware ordering, and observable behavior.
⇄### Store changesSQLite records, migrations, JSON-field plans, WAL, busy handling, immediate writes, and connection-local invalidation.

    ## SQLite without SQL in every domain
    **Domain model**owns meaning, validation, and hydrated relationships**Private row**declares ID, revision, JSON data, uniqueness, and expression indexes**Typed store query**equality, ranges, membership, ordering, cursor, pushdown**SQLite**generic record table plus domain-declared indexes and migrations

    ## Several processes, one local file
    ### WALReaders continue while another connection commits.
### 10 s busy timeoutWriters wait for the single write slot.
### Immediate writesAvoid deferred read-to-write upgrade races.
### Local filesystemOne machine, never a shared network filesystem.

    Concurrency is explicit, not magical. SQLite serializes writes, and application transactions stay short.

    ## Stale writes fail at the boundary
    **read**revision 7→**another process**updates to 8→**UPDATE**WHERE revision = 7→**typed conflict**no overwrite
    <code class="language-sql">UPDATE records
SET data = ?, revision = revision + 1
WHERE model = ? AND id = ? AND revision = ?;</code></pre>

    ## Invalidation means “query again”
    **pinned connection**PRAGMA data_version→**lossy signal**coalesced edge→**persistent client**refresh request→**application query**auth + hydrate
    The monitor carries no record payload and is not a durable event stream. Multiple commits may collapse into one signal.
    <p class="source">Rolled-back writes do not signal. Reconnect emits one invalidation because commits may have been missed.

    ## Treat the file format honestly
    A bstore database is not a SQLite database.
    ### Disposable dataReseed into a fresh SQLite file.
### Valuable dataExport with the previous version, import into a fresh database, verify, and keep the backup.

  Build path<h1>Walk the pressure, not the package tree</h1>Each chapter starts with a decision the business forces, then follows the mechanism that makes it durable.
→

    ## The recording arc
    **Premise**ownership + executable rules**Pressure**retirement + degradation**Coordination**transactional fan-out**Interfaces**TUI + GUI + parity**Policy**navigation + actions**Queries**filters + authorization**Persistence**SQLite + concurrency

    ## Keep one code trace in frame
    <code class="language-text">main/<surface>
  → app/domains/<domain>/surfaces/<surface>
  → app/domains/<domain>/module.go
  → queries/ or internal/commands/
  → middleware pipeline
  → dispatcher + audit
  → store transaction</code></pre>
    Return to this trace whenever a mechanism feels abstract. The architecture is a path a real operation takes.

    The destination
    <h1>One application.<br>Many honest boundaries.</h1>
    <p class="lede">The monolith is the deployment choice. Modularity is the behavior we keep proving.

    github.com/TheFellow/go-modular-monolith · thefellow.github.io/series/mixology/
