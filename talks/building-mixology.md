<!-- Generated from https://thefellow.github.io/talks/building-mixology/ by scripts/generate_llm_content.py; do not edit. -->

# Building Mixology: The Slide Deck

Source: [https://thefellow.github.io/talks/building-mixology/](https://thefellow.github.io/talks/building-mixology/)

## Pyramid summary

- **~2 words:** Mixology deck
- **~8 words:** A visual walkthrough of Mixology's executable modular architecture.
- **Expanded:** A visual walkthrough of the foundational domain, module, middleware, event, audit, tagging, filtering, persistence, and presentation choices behind go-modular-monolith.

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

    <i></i> caller → public query owner<i class="event"></i> event owner ⇢ reacting owner

    ## The current trace

      **main/<surface>**process composition→
      **surfaces/<surface>**domain presentation→
      **module.go**public facade→
      **queries / internal**behavior + storage

      ### CLIOne command, one fresh operation context.
### Bubble Tea TUIPersistent session, message-driven presentation.
### Fyne GUIRetained native widgets and managed lifecycle.

    All three enter the same application behavior and local SQLite database. Views are adapters, not alternate applications.

    Foundation 1.1<h1>Shape modules around business ownership</h1>
    A modular monolith begins with decisions, language, and collaboration contracts, not a folder template.
1.1

    ## A boundary should resist the shortest path

      **Public facade**<code>app/domains/drinks</code> composes and exposes supported behavior.
      **Public contracts**<code>models</code>, <code>queries</code>, and <code>events</code> are deliberate collaboration seams.
      **Event handlers**<code>handlers</code> consume public facts and mutate only their owning domain.
      **Private work**<code>internal/commands</code> and <code>internal/dao</code> remain implementation details.

    If a neighboring domain can import the command that “just does the thing,” ownership is only a suggestion.

    ## Start with seven different kinds of ownership
    <table class="matrix"><thead><tr><th>Profile</th><th>Contexts</th><th>Why it exists</th></tr></thead><tbody><tr><td>Operational</td><td>Ingredients, Drinks, Inventory, Menus, Orders</td><td>business state, commands, queries, events, persistence, policy</td></tr><tr><td>Activity</td><td>Audit</td><td>append-only evidence written by the operation pipeline</td></tr><tr><td>Cross-cutting domain</td><td>Tagging</td><td>owned associations over registered operational targets</td></tr></tbody></table>
    Consistency does not require identical package trees. Audit and Tagging use smaller profiles because their responsibilities differ.

    ## A module has a public edge and a private center
    **<code>module.go</code>**application-facing facade chooses a typed operation path**<code>models / queries / events</code>**deliberate vocabulary for callers and neighboring domains**<code>handlers</code>**consume public peer facts and mutate only owned state**<code>internal/commands + internal/dao</code>**business decisions and persistence stay private
    Queries answer another domain's question. Events announce a fact. Neither exposes the command that owns the decision.

    ## Composition is ordinary, visible Go
    **Foundation**Audit + Tagging schemas**Ports**tag repository + empty registry**Evidence**separate audit writer**Pipeline**dispatcher + writer callback**Operational modules**rows + tag targets**Public facades**Tagging + Audit
    ### No import side effectsPrivate SQLite rows register during construction. Invalid or missing registration fails at startup or in architecture tests.
### No second manifest<code>TestEveryDomainIsComposed</code> treats domain directories as the source of truth and verifies <code>app.New</code>.

    The private Audit writer exists before the public Audit facade, breaking the construction cycle between pipeline activity and authorized audit reads.

    ## Application state is not request state
    ### <code>App</code>Store and public modules whose private composition retains the configured pipeline. No actor identity.
+### <code>Session</code>Binds a persistent TUI or GUI to an authenticated base context, then creates a fresh operation context every time.

    **base context**actor + logger + metrics→**<code>Session.Context()</code>**fresh mutable state→**operation**events + activity + attributes→**discard**nothing leaks forward
    The CLI starts fresh per invocation. Persistent clients reuse authentication, never accumulated operation state.

  Foundation 1.2<h1>Let types carry cheap invariants</h1>Use the compiler for distinctions it can defend, and domain behavior for transitions it cannot.
1.2

    ## Let types carry the distinctions they can

      ### Generated entity IDs<code>DrinkID</code> and <code>IngredientID</code> share the same generated Cedar method shape without becoming interchangeable parameters.

      ### Closed amount variantsAn unexported <code>isAmount</code> method limits <code>Amount</code> to volume and discrete quantities owned by the kernel.

      ### Validated valuesCurrency, price, quantity, and tag parsers turn accepted external text into domain-shaped values.

    Go still permits zero values and package-local construction. Constructors, decoding validation, and boundary checks carry the guarantees the type system cannot.
    [Adjacent article: Making Illegal States Unrepresentable in Go](/articles/making-illegal-states-unrepresentable-in-go.md)

    ## Identity should reveal the entity
    ### Raw string<code class="language-go">func Load(id string)

Load(orderID) // compiles</code></pre><p class="muted">Meaning survives only in names and review.
→### Generated ID<code class="language-go">func Load(id DrinkID)

Load(orderID) // compiler error</code></pre><p class="accent">Parsing, prefixes, Cedar identity, and JSON behavior stay consistent.

    Six entity ID types share generated mechanics without becoming interchangeable values.

    ## Model absence, variants, and concurrency explicitly
    ### Closed variants<code>Amount</code> accepts only kernel-owned volume or discrete quantity implementations.
### Intentional absence<code>optional.Value[T]</code> distinguishes absent from present, including a deliberately present zero value.
### Opaque revisionMutable public models round-trip the store token. Surfaces never compare or increment it.

    Make invalid combinations expensive to express, then validate every decoding boundary.

    ## Capability types remove forbidden moves
    ### <code>middleware.Context</code>Transaction, principal, activity, <code>AddEvent</code>, and <code>TouchEntity</code>.
Commands may originate owned facts.
⊃### <code>HandlerContext</code>Transaction, principal, and <code>TouchEntity</code>. No event accumulator.
Reactions cannot cascade.

    The most reliable prohibition is an API that cannot express the forbidden operation.

  Foundation 1.3<h1>Make errors part of the application protocol</h1>Domains choose meaning once. Every present and future edge chooses only how to render it.
1.3

    ## Failure kind is not presentation
    **Domain / store**typed failure→**<code>pkg/errors</code>**semantic kind→**CLI / TUI / GUI**native feedback→**HTTP / gRPC**future mapping
    Lower layers never choose exit codes, colors, dialogs, HTTP status, or gRPC codes.

    ## Six meanings cover the application boundary
    <table class="matrix"><thead><tr><th>Kind</th><th>Meaning</th><th>Typical response</th></tr></thead><tbody><tr><td>Invalid</td><td>the request is malformed</td><td>fix input</td></tr><tr><td>NotFound</td><td>the resource does not exist</td><td>choose another</td></tr><tr><td>Permission</td><td>the actor is not allowed</td><td>hide or deny</td></tr><tr><td>Conflict</td><td>state collides or revision is stale</td><td>reload or rename</td></tr><tr><td>FailedPrecondition</td><td>valid request, invalid current state</td><td>resolve prerequisite</td></tr><tr><td>Internal</td><td>invariant or dependency failed</td><td>safe message + diagnostics</td></tr></tbody></table>

    ## Diagnostics and safe text are different data
    ### For operators<code class="language-go">errors.Internalf(
  "load inventory: %w", err,
)</code></pre><p><code>Error()</code> retains the cause for logs and wrapping.
∥### For people<code class="language-go">err.WithUserMessage(
  "Inventory is temporarily unavailable",
)</code></pre><p>Internal detail is generic unless explicitly made safe.

    Unknown errors do not inherit this safety guarantee. Classify unexpected failures before a presentation boundary.

    ## Generate the repetitive family, enforce one vocabulary
    ### GeneratedTyped constructors, classifiers, metadata, and matching test assertions.
### Wrapped<code>%w</code>, <code>Is</code>, and <code>As</code> preserve semantic inspection through context.
### Enforced<code>arch-lint</code> rejects direct standard-library <code>errors</code> imports outside <code>pkg/errors</code>.

    One immutable kind survives every layer without turning the core into a transport library.

  Foundation 1.4<h1>Give every operation one trustworthy path</h1>Commands and queries should state intent while the pipeline owns the guarantees around them.
1.4

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

    ## The chain runs inward, then proves the result outward
    ### EnterSerialize, enrich logs, start metrics and activity, open the unit of work, load trusted state, authorize, handle.
↩### UnwindAuthorize result, dispatch facts, record successful activity, commit, observe final duration and error.

    Declaration order and completion order differ. Moving one middleware can move work outside the transaction or hide an unwind failure from telemetry.

    ## The unit of work is the consistency membrane
    domain mutation + prepared event reactions + touched entities + successful audit
    ### SuccessEvery write and the durable activity record commit together.
One business operation.
or### Any failureResult authorization, handler, audit, or storage error rolls the complete write graph back.
No partial truth.

    A caller-supplied transaction retains commit and rollback ownership. Ordinary domain calls use the middleware-managed SQLite transaction.

    ## Load trusted state inside the transaction
    **ID + intent**small request→**<code>LoadCommand</code>**current persisted value→**authorize**before + after→**commit**revision still current
    ### Why not trust a UI model?It may be stale, incomplete, or shaped for display rather than authority.
### Why authorize twice?A policy may allow editing a draft without allowing the transition to produce a published resource.

  Foundation 1.5<h1>Make the architecture executable</h1>The compiler provides privacy. Generators, analyzers, and adversarial tests defend the dependency graph.
1.5

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

  Foundation 1.6<h1>Make authorization part of the domain</h1>Policy belongs beside the resource language, and enforcement belongs on every trustworthy operation path.
1.6

    ## Each domain owns its policy vocabulary
    **Domain model**complete business state→**Generated authz model**Cedar shape→**Principal + action**operation intent→**Cedar evaluator**permit or deny
    The shared evaluator knows Cedar. Ingredients, Menus, and Orders decide what their resources and actions mean.

    ## One decision appears at four scales
    ### WorkspaceCan this actor discover and enter the domain?
### CollectionWhich rows and counts may become visible?
### EntityMay this exact resource be read or selected?
### ActionMay this exact resource transition now?

    Navigation, summaries, lists, and mutations are all application reads. None gets a policy exemption for being convenient UI.

    ## Fill the visible page, not the storage page
    **stable candidates**filter + hydrate→**authorize each**deny disappears→**continue scanning**until N visible→**look ahead**safe cursor
    ### Permission denialExpected list behavior. Omit the entity and keep scanning.
### Evaluation or storage failureNot a denial. Fail the query instead of returning a believable partial result.

    ## Counts can leak what lists conceal
    ### Unsafe<code>SELECT COUNT(*)</code> reports hidden entities even when the list omits them.
→### Current contractCount the same authorized page stream the actor is allowed to observe.

    Authorization changes information architecture, not just button state.

    ## Projection guides. Commands enforce.
    ### Presentation projectionCombines permission with durable prerequisites so a view can hide denied actions and explain unavailable ones.
≠### Authoritative commandReloads current state, repeats authorization, and checks invariants inside the write transaction.

    A stale screen may offer an action that just became invalid. That is a normal race, not authority granted by the UI.

  Foundation 1.7<h1>Observe the operation, not random functions</h1>Logs diagnose one execution. Metrics describe the population. Neither replaces durable business activity.
1.7

    ## Three lenses answer three questions
    ### Structured logsWhat happened during this execution, with actor, action, resource, duration, and diagnostic error?
### Bounded metricsHow often, how slowly, and how unsuccessfully do operation classes behave?
### Audit activityWho attempted which business action, against what, and what else changed?

    One middleware boundary provides consistent meaning without scattering instrumentation through domain code.

    ## Context accumulates useful log meaning
    **Entrypoint**logger + actor→**Pipeline**Cedar action→**Command**primary resource→**Unwind**duration + final error
    ### Deliberate levelsPermission denial is informational; query failures warn; command failures error.
### Fresh scopeEnriched attributes live only for one operation and cannot bleed into the next session call.

    ## Metric labels must stay boring
    ### Current instrumentsCommand/query totals use action + result. Error counters and durations use action. Store read/write durations have no labels.
Small, stable cardinality.
≠### Never labelsEntity IDs, user filter text, error messages, tag values, or arbitrary resource names.
Unbounded and operationally expensive.

    Authorization and event metric names are reserved but not currently emitted. The deck distinguishes available vocabulary from actual instrumentation.

    ## Libraries expose a contract; executables own lifecycle
    **Domain + store**record through a tiny <code>Metrics</code> interface**<code>pkg/telemetry</code>**no-op, memory, OTEL, and Prometheus-backed implementations**<code>main/<surface></code>**address, HTTP server, startup, and shutdown**Runtime constraint**concurrent local surfaces need distinct metrics ports

  Foundation 1.8<h1>Treat auditing as a domain</h1>An audit trail is durable business evidence with transaction semantics, policy, filtering, and its own read model.
1.8

    ## An activity is more than a log line
    ### Who + whatPrincipal, Cedar action, and primary resource identify the attempted operation.
### When + outcomeStart, completion, success, and diagnostic error preserve what happened.
### Blast radiusDeduplicated touched entity IDs reveal every indirect resource changed by handlers.

    Audit is append-only evidence. It is not diagnostic logging and it is not a replayable domain event stream.

    ## Success and failure take different transaction paths
    ### Successful commandmutation + handlers + success auditIf recording fails, the business operation rolls back.
∥### Failed managed commandrollback firstThen persist the failed attempt in a separate managed write.

    <code>recordSuccessfulActivity</code> runs inside the unit of work. <code>TrackActivity</code> records a managed failure only after rollback. Caller-owned transactions keep failure activity under the caller's decision.

    ## Touches turn fan-out into explainable history
    **Ingredients**retire catalog item→**Drinks**touch recipes→**Inventory**touch stock→**Menus + Orders**touch dependents
    One originating activity can answer “what changed because of this decision?” without pretending every reaction was a separate user command.

    ## Failure to record has an explicit policy
    <table class="matrix"><thead><tr><th>Situation</th><th>Audit behavior</th><th>Returned result</th></tr></thead><tbody><tr><td>successful command, success audit fails</td><td>inside UoW</td><td>internal error; command rolls back</td></tr><tr><td>failed command, failure audit succeeds</td><td>after managed rollback</td><td>original command error</td></tr><tr><td>failed command, failure audit also fails</td><td>recording failure is logged</td><td>original command error remains authoritative</td></tr></tbody></table>

    ## The read side is still an application boundary
    **Audit module**list, count, entity history, and actor activity**Query contract**action, principal, entity, time window, typed expression, cursor**Pipeline**Cedar authorization and permission-safe paging**Surfaces**CLI, TUI, and GUI adapt the same append-only evidence
    The system that records activity automatically does not grant everyone permission to inspect it.

    Foundation 2.1<h1>Turn calls into bounded event fan-out</h1>
    Ingredient retirement changes four domains without giving Ingredients four collaborators.
2.1

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

    ## Prepare every reader before mutating anything
    **fresh handlers**one event-local receiver each→**optional <code>Handling</code>**all snapshots finish┃**every <code>Handle</code>**apply owned reactions→**commit**one outcome
    <code>Handling</code> is a generator-recognized method convention, not a shared Go interface. Correctness never depends on generated handler order.

    ## No cascades is defended twice
    ### Capability boundary<p><code>HandlerContext</code> omits <code>AddEvent</code>, so ordinary handlers cannot enqueue another fact.
+### Runtime boundary<code>DispatchEvents</code> clones the original event slice before delivery, so accidental later additions are not dispatched.

    Every event has a bounded, reviewable leaf fan-out. Multi-step time-spanning work deserves an explicit workflow.

    ## Package rules preserve the dependency direction
    <b>×</b><code>commands-emit-own-domain-events</code><b>×</b><code>handlers-no-commands</code><b>×</b><code>handlers-no-modules</code><b>×</b><code>queries-no-commands</code>
    The event changes the dependency direction. The analyzer keeps it changed.

  Foundation 2.2<h1>Give cross-cutting tags an owner</h1>Shared vocabulary does not require ownerless persistence, global meaning, or private-domain reach-through.
2.2

    ## Tagging is a bounded context
    ### Kernel value<code>tag.Tag</code> owns canonical key/value parsing, validation, ordering, and formatting.
→### Tagging domainOwns polymorphic associations, authorized mutations, discovery, summary, and target registration.

    A tag may influence filtering, presentation, or Cedar ABAC. Its business meaning remains with the policy and domain that interpret it.

    ## The registry reverses the dependency
    **Tagging**target registry⇄**Operational domain provides**load complete Cedar state**Operational domain provides**bulk active-target check**Operational domain provides**get, tag, and untag action IDs**Tagging provides**one narrow association repository port
    Tagging never imports Ingredients, Drinks, Inventory, Menus, or Orders models and private DAOs.

    ## Hydration stays with the entity owner
    **Domain DAO**load owned rows→**tag repository**batch associations→**Domain model**complete tags→**Cedar + filter**evaluate full state
    The association store is shared infrastructure. The complete Ingredient or Drink is still assembled by its owner before authorization and exact filtering.

    ## Replace is one intent with dynamic authority
    <table class="matrix"><thead><tr><th>Difference</th><th>Required action</th><th>Recorded activity</th></tr></thead><tbody><tr><td>add or change values</td><td>tag</td><td rowspan="3">one stable tag operation</td></tr><tr><td>remove keys</td><td>untag</td></tr><tr><td>mixed replacement</td><td>tag + untag</td></tr></tbody></table>
    <code>LoadCommandActions</code> derives the complete Cedar action set from current tags and the desired complete set.

    ## Compose domain change and tag change atomically
    non-nil tag intent: <code>RunTaggedMutation</code> owns or joins one shared transaction
    **validate tags**before write→**domain command**normal pipeline+**<code>Tags.Replace</code>**normal pipeline→**commit**both or neither
    ### <code>nil</code> desired setPreserve existing tags and run only the domain mutation.
### Non-nil empty setExplicitly clear every tag as part of the same application operation.

    The domain command and <code>Tags.Replace</code> remain two normal pipeline commands with two audit activities, committed atomically together.

    ## Discovery is its own authorized workflow
    ### ShowFind active entity references for an exact tag or every value of a key.
### SummaryAggregate canonical tags across active registered entity types.
### PolicyTagging-owned Cedar actions govern discovery; referenced entity authorization is not silently replayed.

    Inactive targets are excluded from discovery through each owner's registered bulk check. Stale association rows are not silently deleted.

  Foundation 2.3<h1>Give people and programs one filter language</h1>Own exact expression semantics above storage, authorization, and every presentation surface.
2.3

    ## The schema is a public domain contract
    **typed filter view**stable field names→**Expr parser + checker**accepted syntax→**owned tree**stable semantics→**surface help**fields + examples
    The filter view need not mirror a SQLite row or returned model. It can expose nested and hydrated values without leaking persistence.

    ## Borrow a compiler, keep ownership
    ### <code>Source</code>The trimmed expression a person supplied.
### <code>String</code>Canonical syntax for display and reparsing.
### <code>Tree</code>Mixology's stable node model for integrations and SQL planning.

    Expr optimization is deliberately disabled. Expr parses, checks, and executes; Mixology owns the restricted language and pushdown plan.

    ## One expression, two execution stages
    **checked expression**exact contract→**safe SQL pushdown**candidate reduction→**hydrate**tags + derived values→**<code>Match</code>**authoritative result
    <code>ApplySQLPushdowns</code> returns candidates, never proof. Every operational DAO evaluates the complete hydrated view afterward.

    ## Push down only what the full expression requires
    ### Conjunction<code>A && tags.contains("x")</code>
Persisted <code>A</code> is required even when tags need memory evaluation.
Push down A safely.
≠### Disjunction<code>A || tags.contains("x")</code>
A row failing <code>A</code> may still match after tag hydration.
Do not push down A alone.

    ## Common constraints survive alternatives
    <code class="language-text">(category == "spirit" && tags contains "featured")
||
(category == "spirit" && name.contains("gin"))</code></pre>
    **both branches require**<code>category == "spirit"</code>→**SQL candidate set**spirits only→**exact Match**full OR expression
    Optimization is a theorem about preserved truth, not a list of AST nodes the translator happens to understand.

    ## Filtering and authorization compose in order
    **parse once**typed invalid on error→**filter + hydrate**domain semantics→**authorize each**elide denies→**page**fill visible count
    Audit can use direct <code>ApplySQL</code> because its filter view comes from one row. Operational domains use staged hydration.
    <p class="source">[Adjacent article: Typed Filtering over SQLite](/articles/typed-filtering-over-sqlite.md)

  Foundation 2.4<h1>Make persistence a replaceable boundary</h1>The bstore-to-SQLite migration proved which contracts belonged to the application and which belonged to an engine.
2.4

    ## Preserve the contract, replace the engine
    <table class="matrix"><thead><tr><th>Preserved</th><th>Rebuilt</th></tr></thead><tbody><tr><td>domain ownership and public module contracts</td><td>DAO implementations, rows, and hydration adapters</td></tr><tr><td>models, commands, queries, policies, events</td><td>schema registration and row conversion</td></tr><tr><td>transaction participation</td><td>query builder and cursor predicates</td></tr><tr><td>typed errors and filter semantics</td><td>SQLite mapping and safe pushdowns</td></tr><tr><td>surface-observable behavior</td><td>change monitoring and concurrency coordination</td></tr></tbody></table>

    ## SQLite stays below domain persistence
    **Domain DAO**owned queries, row conversion, hydration**Typed store API**<code>Register</code>, <code>Get</code>, <code>Insert</code>, <code>Update</code>, <code>Query</code>**Unit of work**shared transaction carried by operation context**modernc SQLite**WAL, constraints, revisions, migration ledger, data version

    ## Several processes can share one local truth
    **CLI**short write→**SQLite WAL**one writer, many readers←**TUI**persistent reader↔**GUI**persistent reader
    ### Process coordinationBusy timeout and immediate transactions make writer contention explicit.
### Application coordinationKeep commands short; never hold a transaction while waiting for user input.

    ## Revisions turn stale writes into typed conflicts
    read rev 7→other client writes rev 8→update WHERE rev = 7⤫Conflict
    Public mutable models carry an opaque revision. The store performs the atomic comparison and increment.

    ## Invalidation carries no domain truth
    **SQLite <code>data_version</code>**external commit observed→**<code>Signals</code>**coalesced edge+**<code>Epoch</code>**level guard→**ordinary query**reload authorized state
    The epoch closes lost-wakeup gaps around coalesced signals. Neither carries records or bypasses application policy, filters, and request-order guards.

    ## Treat the file format honestly
    ### Migration ledgerOrdered migrations advance deliberately; a database from a newer schema is rejected.
### RegistrationExplicit model schemas fail early; imports do not mutate global persistence state.
### ErrorsConstraints and stale revisions become application kinds, not leaked driver strings.

    [Adjacent article: Migrating Mixology from bstore to SQLite](/articles/migrating-mixology-from-bstore-to-sqlite.md)

  Domain workshop 3.1<h1>Preserve truth through degradation</h1>A system can remain operational without pretending its state is healthy.
3.1

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

  Domain workshop 3.2<h1>Grow a reciprocal workflow</h1>planned workshop<br>Add Procurement only when the new business loop teaches something the current seven contexts cannot.
3.2

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

  Surfaces 4.1<h1>Build a reusable MVVM toolkit for the terminal</h1>Bubble Tea supplies the runtime. Mixology owns the view-model contract.
4.1

    ## Adapt the pattern to the runtime
    ### Reusable MVVM seamA screen owns presentation state and commands behind a testable view-model contract.
+### Bubble Tea runtimeMessages drive explicit updates, commands carry effects, and a string view renders each frame.

    The framework is an implementation detail of the toolkit, not the architecture of every screen.

    ## The shell owns application concerns
    ### Domain surface- typed presentation state- queries and commands- domain workflows- action projection### Root application shell- route and back stack- cached view models- title, status, help- global keys and sizing- deferred invalidation### TUI toolkit- view-model contract- list/detail and viewports- forms and dialogs- layout, keys, styles

    ## Only the root is a <code>tea.Model</code>
    ### Bubble Tea contract<code class="language-go">Update(tea.Msg) (
    tea.Model, tea.Cmd,
)</code></pre><p>The executable shell satisfies this runtime boundary.
≠### Mixology contract<code class="language-go">Update(tea.Msg) (
    ViewModel, tea.Cmd,
)</code></pre><p>Every domain screen stays inside the richer repository-owned abstraction.

    Returning <code>ViewModel</code> preserves help and interaction contracts after every update. Domain screens neither embed nor pretend to be <code>tea.Model</code>.

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

    ## The toolkit is a kit, not a base screen
    ### Browse<p><code>ListDetail</code>, typed <code>ListItem[T]</code>, summaries, loading, filtering, paging, and selection.
### Compose<code>DetailViewport</code>, <code>FormViewport</code>, layout arithmetic, reusable components.
### InteractForms, dialogs, keys, styles, help bindings, and explicit input ownership.
### RefreshDomain-payload-free invalidation starts an ordinary query; request tokens reject stale results.

    <code>pkg/testutil/tuitest</code> is the deterministic program driver. It tests the toolkit and completed application without becoming part of either.

    ## Typed messages keep ownership visible
    **<code>tea.Msg</code>**input arrives→**Root shell**consults <code>Interaction</code>→**ViewModel**updates state→**<code>tea.Cmd</code>**returns typed result
    ### Reusable mechanicsGeneric list items retain their typed domain values while satisfying Bubbles interfaces.
### Domain choicesPublish, complete, cancel, adjust, and retire remain bindings owned by their domain adapters.

    External change? Inactive screens become stale. Active input finishes first, then a domain-payload-free invalidation starts the screen's normal tokenized query.

    ## Tests follow the ownership
    pure presentation model testscomponent update and rendering testsdomain surface testsreal Bubble Tea program driverroot navigation and input ownershipcross-surface persisted behavior

  Surfaces 4.2<h1>Adapt the MVVM toolkit to retained widgets</h1>Fyne changes the interaction model, so the reusable mechanics change with it.
4.2

    ## Start from the application seam
    **<code>main/gui</code>**database, actor, logs, application, session, native lifecycle**domain GUI surfaces**presenters and views shaped for each bounded context**<code>pkg/toolkits/gui</code>**shell, forms, tables, semantic controls, dialogs, executors**Fyne runtime**retained widgets, callbacks, windows, platform event loop

    ## Make state publication the binding seam
    ### State- plain typed snapshot- items and selection- mode, form, errors- busy and action state### Presenter- calls the application- owns latest loads- admits one submission- publishes clones via <code>OnChange</code>### View- subscribes to state- updates Fyne controls- binds pointer and keys- owns widget-local state
    Synchronous UI actions can publish directly. Async completions and external invalidation cross the injected <code>Dispatcher</code> before touching presenter or widget state.

    ## The GUI toolkit owns retained-mode mechanics
    **Shell + Route**cache and activate views→**Standard pages**layout and hierarchy→**Semantic controls**stable test identities→**Domain view**renders state
    ### Navigation<code>UnsavedChanges</code> guards route changes. <code>Commander</code> gives menus, shortcuts, and controls the same intents.
### PresentationList, form, filter, paging, table, tag, validation, dialog, and error mechanics stay domain-free.
### TestingSemantic controls preserve visible guards so tests trigger the same behavior as a person.

    ## Async work has two boundaries
    **Presenter**requests work→**Executor**runs application call→**Dispatcher**publishes on UI thread→**View**updates widgets
    ### <code>LatestRequest[T]</code>Cancels superseded loads and rejects stale queued publications.
### <code>Submission</code>Admits one mutation, then releases on dispatched completion before presenting its result.
### <code>GatedDispatcher</code>Drops widget publications after desktop shutdown closes the publication gate.

    ## Reviewable slices kept the change surface small
    **Shell**routes + lifecycle**Models**state + errors**Toolkits**standard mechanics**Domains**workspace by workspace**Parity**paging + workflows**Lifecycle**drain accepted work**Evidence**process + visual checks

    ## The integration gaps were architectural clues
    ### DashboardMoved business-shaped aggregation into <code>app</code>.
### TagsNeeded one atomic application mutation.
### PagingHad to remain explicit and domain-backed.
### ShutdownRequired admission, drain, then store close.

    A third interface is useful precisely because it refuses to fit abstractions built around the first two.

  Surfaces 4.3<h1>Use the third surface as an architecture test</h1>Difference creates pressure. Pressure reveals misplaced ownership.
4.3

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

  Surfaces 4.4<h1>Share behavior, keep views bespoke</h1>Consistency lives in contracts and outcomes, not identical presentation internals.
4.4

    ## Each runtime has a different unit of interaction
    ### CLIInvocation, flags, stdin, stdout, exit status. State ends when the process ends.
### TUIMessages, commands, focus, terminal cells, key chords, and a continuous update loop.
### GUIRetained controls, pointer and keyboard events, background work, dispatch, and native lifecycle.

    ## The least common denominator is not neutral
    A universal view model either leaks one runtime into the others, or erases the affordances that made each runtime useful.
    ### Shared contracts- public models- queries and events- action meaning- typed errors- observable outcomes### Application boundary- the narrow waist- durable semantics- authorization- transaction ownership- atomic composition### Bespoke- focus and selection- widget or terminal state- async request state- navigation mechanics- rendering

    ## Reuse mechanics within a surface
    **CLI toolkit**JSON input and output, reflection-based tables**TUI toolkit**view contracts, list/detail, forms, dialogs, layout**GUI toolkit**shell, tables, semantic controls, executors, dispatchers**Domain surfaces**compose only the matching toolkit with domain workflows

    ## Reusable does not mean symmetrical
    <table class="matrix"><thead><tr><th>Toolkit</th><th>Reusable shape</th><th>Why it differs</th></tr></thead><tbody><tr><td>CLI</td><td>encoders, decoders, tables</td><td>one invocation, then exit</td></tr><tr><td>TUI</td><td>autonomous forms, dialogs, and view models</td><td>messages repeatedly advance explicit state</td></tr><tr><td>GUI</td><td>shell, page objects, controls, async coordinators</td><td>widgets persist and callbacks publish state</td></tr></tbody></table>
    Package shape follows the runtime’s interaction model. Shared application meaning sits below all three.

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

  Surfaces 4.5<h1>Test native desktop behavior headlessly</h1>Confidence comes from a ladder of distinct evidence, not one giant simulated UI test.
4.5

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

  Surfaces 4.6<h1>Project actions, not widgets</h1>Share durable action meaning across interfaces without sharing runtime state.
4.6

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

  Build path<h1>Walk the pressure, not the package tree</h1>Each chapter starts with a decision the business forces, then follows the mechanism that makes it durable.
→

    ## The recording arc
    **Ownership**contexts + module contracts**Protocol**types + errors + policy**Execution**pipeline + transactions**Evidence**logs + metrics + audit**Coordination**events + tags + filters**Pressure**degradation + workflows**Surfaces**CLI + TUI + GUI

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
