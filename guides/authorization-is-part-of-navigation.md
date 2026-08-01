<!-- Generated from https://thefellow.github.io/guides/authorization-is-part-of-navigation/ by scripts/generate_llm_content.py; do not edit. -->

# Authorization Is Part of Navigation

Source: [https://thefellow.github.io/guides/authorization-is-part-of-navigation/](https://thefellow.github.io/guides/authorization-is-part-of-navigation/)

## Pyramid summary

- **~2 words:** Authorized navigation
- **~8 words:** How Cedar shapes routes, aggregates, rows, and available actions.
- **Expanded:** How Mixology carries Cedar authorization through workspace discovery, dashboard summaries, row filtering, and action availability without turning the interface into a second policy engine.

## Full content

Authorization becomes visible long before someone presses Save. It determines which workspaces exist in navigation, which summary cards appear on a dashboard, which rows enter a list, and which actions make sense for the selected entity. Treating only the final command as protected leaves the application technically resistant to mutation while its interface still discloses names, counts, relationships, and capabilities.

The Fyne surface added to [Mixology](https://github.com/TheFellow/go-modular-monolith) forced this issue into the open. A persistent desktop shell advertises the shape of the application continuously. Its dashboard summarizes several domains at once. Its tables expose row actions. The GUI could not rely on a permission error at the end of a workflow and still present a coherent experience.

The resulting rule is simple: policy remains in Cedar and the application boundary, while each presentation surface composes only the experience the active principal is allowed to use.

## One decision appears at several scales

A useful way to reason about authorization in an application surface is to follow it from the outside inward:

```mermaid
flowchart TD
    P[Authenticated principal] --> W[Workspace visibility]
    W --> D[Dashboard cards and aggregates]
    W --> L[Authorized list query]
    L --> R[Visible rows]
    R --> A[Actions for selected resource]
    A --> M[Authorized application mutation]
    M --> T[Transaction, audit, and events]
```

Each layer answers a different question.

- Workspace visibility asks whether the principal has a meaningful read path into a domain.
- Dashboard composition asks whether even the existence or count of that domain may be disclosed.
- A list query decides which resources the principal can observe.
- Action availability evaluates a concrete resource, including its attributes and relationships.
- The operation authorizes again inside the application pipeline before changing state.

These are not duplicate implementations of policy. They are multiple consumers of the same policy at points where the interface needs to make a decision. The final operation remains authoritative because interface state can be stale, bypassed, or raced.

## Build navigation from authorized read paths

Mixology's desktop composition begins with all known workspaces, then establishes visibility for the active session. Drinks, Ingredients, Inventory, Menus, and Orders probe the public `Count` query using an empty list request. Those calls pass through the same authorized query path used by the workspace itself. Audit and Tags do not have an equivalent count operation, so the composition root asks Cedar about representative workspace resources using their public list or summary actions.

The distinction between denial and failure matters. A Cedar permission error removes the workspace. A database or operational error leaves it visible so that the surface can present the real problem. Hiding every failed probe would misreport an outage as a policy decision and make a broken domain silently disappear.

After the probes, the shell is constructed from the filtered route collection. A restricted route is therefore absent from the navigation rail, application menu, keyboard shortcut registration, route lookup, and lazy view construction. It is not merely a hidden button pointing at an otherwise reachable screen.

```go
if err := check.read(); err == nil || !apperrors.IsPermission(err) {
    visible[check.id] = true
}
```

This is composition, not enforcement. The public query still authorizes its work, and an attempted mutation still authorizes at the application boundary. Composition makes the shell truthful about the capabilities it can offer.

## Aggregates can leak what rows conceal

A dashboard count is data. If a sommelier is allowed to see only wine drinks and drinks tagged for that audience, an unfiltered total still reveals that other drinks exist. Low-stock totals, pending-order counts, recent audit activity, and published-menu counts can reveal business state even when no row is named.

Mixology handles this at two levels. First, the desktop dashboard receives the same workspace visibility map as the shell and omits cards for unauthorized workspaces. A principal who cannot read Audit or summarize Tags does not receive a teaser card for either feature. Second, dashboard values are loaded through the application session rather than by reading DAOs from the GUI. The application owns how counts and recent activity are derived, so the presentation cannot accidentally bypass row policy for convenience.

Unknown data also deserves an explicit representation. A failed or partial dashboard load should not substitute zero, because zero is a factual claim. Mixology uses unknown dashboard values and presents the error beside any data that could be loaded. That separates three states which have different security and operational meaning: authorized and empty, unauthorized and omitted, or unavailable and unknown.

When adding an aggregate, I now ask the same questions I ask for a list:

1. Which principal and action authorize this observation?
2. Does the aggregate include only resources that principal may observe?
3. Can the label, zero state, or error reveal a restricted domain?
4. Does a partial failure remain distinguishable from a legitimate count?

## Let authorized queries filter rows

Route access does not imply access to every entity in a workspace. The sommelier example makes that concrete: the Drinks workspace remains useful, but Cedar filters its result to wines and explicitly tagged drinks. The surface calls the public list operation and renders the returned page. It does not fetch every row and reproduce Cedar conditions in GUI code.

Filtering below the surface has several benefits. Pagination counts the records the caller can actually traverse. Selectors used by recipes, menus, and order placement do not fill with inaccessible entities. CLI, TUI, and GUI observe the same resource boundary. Policy changes remain policy changes instead of requiring coordinated edits to three presentations.

This also prevents a common side channel. Client-side filtering may hide row text after IDs, totals, page counts, or loading behavior have already disclosed the hidden records. Returning an authorized result set from the application boundary gives the surface less sensitive material to mishandle.

## Availability belongs to the selected resource

Mutation permissions are often more specific than roles. A pending order can be completed while a completed order cannot. A draft menu can accept drinks and be published, while a published menu can be returned to draft. Cedar can also consider tags and resource relationships. The interface therefore needs action availability for the actual selected row, not a single `isManager` flag computed at login.

Mixology presenters expose capability state such as `CanCreate`, `CanUpdate`, `CanDelete`, `CanTag`, `CanPublish`, `CanDraft`, `CanComplete`, and `CanCancel`. They derive those values by authorizing the appropriate Cedar action against the selected resource's entity. Views translate the result into native presentation behavior: create controls disappear when creation is unavailable, row menus contain only relevant actions, and detail action bars change with selection and lifecycle state.

Inventory demonstrates why row-level capability data is useful. Each row carries whether Adjust, Set, and Tag are authorized for that resource. Orders similarly derives Complete, Cancel, and Tag availability per item. The table can present an honest action menu without waiting for a denied click, but the presenter still refuses to start a workflow when its capability is false.

Capability state has a lifetime. Selection changes clear the previous permissions. Refreshing a row recomputes them. Starting asynchronous work captures the target so a later selection cannot inherit the result. A stale `CanDelete` from the previous drink is both a usability bug and a dangerous statement about authority.

## Denial is still an ordinary application result

Preflight authorization improves composition, but it never replaces authorization at execution. State may change after a button appears. Another operation may change a resource attribute used by Cedar. A caller may invoke the public module without any interface at all.

Every mutation therefore enters the normal application pipeline and can return a typed permission error. GUI presenters treat that error as recoverable presentation state. They retain correctable input, leave persisted state unchanged, and show the denial consistently with other typed application errors. Tests exercise this path even for controls that should normally be unavailable, proving that the boundary holds when presentation assumptions are bypassed.

```mermaid
sequenceDiagram
    participant V as View
    participant P as Presenter
    participant C as Cedar-backed operation
    V->>P: invoke visible action
    P->>C: fresh session context + captured resource
    C-->>P: success or typed permission error
    P-->>V: publish current state, retain input on denial
```

This is the useful separation of responsibilities. Cedar decides. The application enforces and returns typed results. The presenter asks enough questions to compose a truthful interaction. The view renders that interaction using its runtime's native controls.

## Test the absence as well as the success

Authorization tests should observe the complete presentation boundary. Mixology's composed desktop tests start sessions for restricted personas and assert the route IDs offered by the real shell. They verify that hidden routes cannot be navigated to, that dashboard cards follow the same visibility set, and that visible workspaces still expose only authorized rows and actions. Presenter tests compare an owner with a read-only actor and inspect capability state for concrete resources. Mutation tests force permission failures and prove that no state changed.

The useful assertions include negative space:

- The route, menu item, shortcut, and dashboard card are all absent.
- Restricted rows do not affect visible totals or selectors.
- Row and detail actions disappear when their Cedar action is denied.
- Changing selection cannot retain an earlier resource's capabilities.
- A direct or stale invocation is denied by the application operation.
- The denial does not discard form input or partially mutate persisted state.

This ladder catches different failures. A policy unit test can prove a Cedar rule, but not that a dashboard leaks a count. A view test can prove a button is hidden, but not that the operation rejects a bypass. Both are required because authorization shapes both information and behavior.

## Authorization is a composition input

The desktop work changed how I describe authorization in a modular application. It is not only middleware around commands, and it is not a collection of role checks scattered through widgets. It is an input to application composition.

Routes come from authorized read paths. Dashboard summaries follow the same information boundary as their workspaces. Lists return only observable resources. Presenters derive actions from Cedar-backed decisions about concrete entities. Operations authorize again when work executes. Keeping those layers aligned gives each surface an interface that is useful, truthful, and resistant to bypass without asking the interface to become the policy engine.
