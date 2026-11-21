---
title: "F# for Go Devs: The Slide Deck"
date: 2026-11-21
last_modified_at: 2026-11-21
permalink: /talks/fsharp-for-go-devs/
excerpt: "A talk for Go developers that teaches F#'s algebraic types, then carries closed variants, smart constructors, exhaustive matching, and typed workflows back into Go."
layout: deck
deck_markdown: true
deck_center: true
deck_theme: black
deck_css: /assets/css/fsharp-deck.css
deck_back_url: /articles/making-illegal-states-unrepresentable-in-go/
deck_back_label: Article
deck_back_aria: Return to the Making Illegal States Unrepresentable in Go article
author_profile: false
search: false
---

<section data-markdown data-separator="^---$" data-separator-vertical="^--$">
<script type="text/template">
{% raw %}
<!-- .slide: class="centered" -->
# Make Illegal States Unrepresentable

### F#'s algebraic type system as a tool
(and how to steal the ideas in Go)

---

## Reading F# function signatures

F# and Go signatures read the same direction — left to right.

```fsharp
// Go:   func(int, string) int
// F#:   int -> string -> int    ← rightmost is the return type
```

There's **no syntactic distinction between inputs and output**: `->` all the way.

Data flows left to right. One special return type to know: `unit` — the type of a function that does something without returning a meaningful value. Go's "no return type"; F# makes it explicit.

---

## One argument. Always.

Last expression is the return value — no `return` keyword. Every function takes exactly one argument; multi-arg is syntactic sugar. (`fun` = anonymous function, same as Go's inline `func` literal)

```fsharp
let add x y = x + y   // : int -> int -> int
// desugars to:
let add = fun x -> (fun y -> x + y)
```

The practical payoff is **partial application** — fix some arguments, get a new function back. This is a real closure at runtime:

```fsharp
let add3 = add 3      // add3 : int -> int  — closure capturing 3
add3 5                // 8
```

Go has the same thing, just less idiomatic:
```go
x := 3
add3 := func(y int) int { return add(x, y) }  // closes over x
```

---

## Turtles all the way down.

Even operators are just curried functions:
```fsharp
(+)  : int -> int -> int
3 + 5                 // 8  — infix sugar for (+) 3 5
let add3 = (+) 3      // add3 : int -> int

(|>)  : 'a -> ('a -> 'b) -> 'b
5 |> add3             // 8  — same as add3 5
"  Hello  " |> String.trim |> String.toLower  // "hello"

(>>)  : ('a -> 'b) -> ('b -> 'c) -> ('a -> 'c)
let normalize = String.trim >> String.toLower  // : string -> string
normalize "  Hello  "  // "hello"
```


---

## One more thing: type inference

The compiler figures out types from usage — and it's surprisingly powerful.
Annotations are optional, and we use them at boundaries to document intent.

```fsharp
let greet name = $"Hello, {name}"            // inferred: string -> string
let greet (name: string) : string = ...      // same, annotated
```

**`|>` in practice** — the inferred types flow through the pipeline automatically:
```fsharp
let rawInput : string = "  hello@example.com  "

rawInput
|> String.trim           // : string
|> String.toLower        // : string
|> Email.create          // : Result<Email.Address, ValidationError>
```

F# infers the type at each step. If `String.trim` returns something `String.toLower` can't accept, it's a compile error.

No implicit conversions — F# won't silently coerce an `int` to a `float`. That strictness is what makes inference possible: the compiler reasons precisely because values never quietly change type.

---

<!-- .slide: class="centered" -->
# Part I
## F#
A domain model

---

## Product Types: Tuples & Records

**Tuples** — anonymous, lightweight, no field names:
```fsharp
(42, "hello")   // : int * string
```

**Records** — named fields, the primary product type for domain modeling:
```fsharp
type User = {
    Name      : string
    Email     : string
    CreatedAt : DateTime
}
```

Named fields, `name : type` order — same as Go. Every field is **immutable after construction**. Once you have a `User`, no one can mutate its fields.

---

## Sum Types: Discriminated Unions

A type that is **exactly one** of several named variants. Each variant can carry different data.

```fsharp
type PaymentMethod =
    | Cash
    | PayPal     of accountEmail: string
    | CreditCard of cardNumber: string * expiry: DateTime
```

- `Cash` carries no data
- `PayPal` carries an account email
- `CreditCard` carries a tuple — `string * DateTime` — a number and expiry together

Accessing `cardNumber` on a `Cash` payment is a **compile time error**.


---

## The "algebra" in algebraic type system

**Product types**: The cardinality of the values for the type is the *product* of the cardinality of each field's possible values.
```fsharp
// Theme has 2 values (Light|Dark). Color has 3 (R|G|B).
// ThemedColor has 2 × 3 = 6 possible values.
type ThemedColor = {
	Theme : Theme
	Color : Color
}
```

**Sum types**: The cardinality of the values for the type is the *sum* of the cardinality of each variant's possible values.
```fsharp
// ThemeOrColor has 2 + 3 = 5 possible values.
type ThemeOrColor =
    | ThemeCase of Theme
    | ColorCase of Color
```

The vocabulary is precise — "product" and "sum" aren't metaphors, they're the actual math.

---

## Our domain: an order-processing system

We'll use one example throughout: An order moving through its lifecycle.

```
Unvalidated → Validated → Priced → Placed → Shipped → Delivered
                                           ↘ Cancelled
```

Goal: Model this using the algebraic type system F# gives us

---

## The order lifecycle as a discriminated union

```fsharp
type OrderStatus =
    | Unvalidated
    | Validated
    | Priced    of price: decimal
    | Shipped   of trackingNumber: TrackingNumber
    | Delivered of deliveredAt: DateTime
    | Cancelled of reason: string
```

Each state carries exactly the data that makes sense for it.

A `Shipped` order has a tracking number. A `Cancelled` order has a reason. An `Unvalidated` order has neither, and cannot be confused with either.

---

## Giving primitives meaning

Single-case discriminated unions — a DU with exactly one variant:

```fsharp
type OrderId    = OrderId    of string  // type OrderId = | OrderId of string
type CustomerId = CustomerId of int     // type CustomerId = | CustomerId of int
```

Create one and F# tracks the type with the underlying primitive value as a unit:

```fsharp
let orderId = OrderId "ord-123"
// val orderId: OrderId = OrderId "ord-123"
```

`orderId` is an `OrderId`. Not a `string`. You cannot pass it where a `string` is expected.

> In Go `type OrderId string` is similar: a distinct type, not an alias.

---

## Unwrapping with pattern matching

To get the `string` back out, you pattern match, or destructure the value:

```fsharp
let (OrderId s) = orderId
// val s: string = "ord-123"
```

`(OrderId s)` on the left of a `let` is a **pattern** — the same mechanism as `match`. It destructs the single-case DU and binds the inner value to `s`. The same syntax works across all F# types:

```fsharp
let (a, b)          = (42, "hello")        // tuple
let { Name = n }    = user                 // record
let (OrderId s)     = orderId              // single-case DU
```

This is intentional friction. Every place you cross back to a raw `string` is explicit in the code. And mixing types up is a compile error:

```fsharp
let processOrder (id: OrderId) (cid: CustomerId) = ...

processOrder customerId orderId   // ← type mismatch. won't compile.
```

---

## Smart constructors — why F# cares

We want `Email.Address` to mean "this is a valid email." How can F# enforce that?

**1. Immutability by default**
Once an `Email.Address` is constructed, it cannot be mutated. A valid value stays valid for its entire lifetime.

**2. Private constructors via modules**
The constructor can be marked `private` to its module. No external code can call it directly — not even with a cast.

**3. `Result<T, E>` keeps success and failure together**
A fallible constructor returns `Result<Email.Address, string>`. To obtain the address, the caller must pattern-match on both `Ok` and `Error` — the success value cannot be extracted while silently dropping its failure.

---

## Smart constructors — the full F# pattern

```fsharp
module Email =
    // 'private' hides the constructor outside this module
    type Address = private Address of string

    let create (s: string) : Result<Address, string> =
        if s.Contains("@") && s.Length >= 3
        then Ok (Address s)
        else Error $"'{s}' is not a valid email"

    let value (Address s) = s   // the only way to unwrap
```

```fsharp
// Outside the module — compile ERROR, constructor is private:
let bad = Email.Address "not-valid"

// The only valid path:
match Email.create rawInput with
| Ok email  -> sendWelcome email   // email: Email.Address — provably valid
| Error msg -> handleError msg     // can't skip this branch

// When you need the raw string back — call value explicitly:
let raw = Email.value email        // raw: string = "someone@example.com"
```

---

## Making illegal states unrepresentable

A contact must have **at least one of**: email or phone.

```fsharp
// This allows neither — an illegal domain state that compiles fine
type Contact = { Email: string option; Phone: string option }
```

Model the actual constraint instead:

```fsharp
type ContactInfo =
    | EmailOnly     of Email.Address
    | PhoneOnly     of PhoneNumber
    | EmailAndPhone of Email.Address * PhoneNumber

type Contact = {
    Name : string
    Info : ContactInfo   // always exactly one of the three. always.
}
```

There is **no representation** for "no contact info." You cannot construct one. The type prevents it at definition time, not runtime.

---

## Exhaustive matching — the payoff

In F#, `if` is an expression — it returns a value, and the compiler requires both branches. This is the same instinct applied to sum types: you must handle every variant.

```fsharp
// if returns a value — both branches must exist and return the same type:
let label = if order.IsRush then "URGENT" else "standard"
//                                        ↑ omit this → compile error
```

```fsharp
let notifyContact contact =
    match contact.Info with
    | EmailOnly email           -> sendEmail email
    | PhoneOnly phone           -> sendSms phone
    | EmailAndPhone (email, _)  -> sendEmail email
    // Forgot a case? Compiler error. Every time.
```

Add a new variant to `ContactInfo` and **every match expression across the entire codebase** that touches it becomes a compiler error. The compiler tells you everywhere you need to update.

This is the real payoff. The type and the exhaustiveness check together mean you can refactor with confidence.

---

## Workflows as types

```fsharp
// Function signatures are types — they document the contract
type ValidateOrder = UnvalidatedOrder -> Result<ValidatedOrder, OrderError>
type PriceOrder    = ValidatedOrder   -> PricedOrder
type PlaceOrder    = PricedOrder      -> Result<OrderPlaced, OrderError>
```

Read these three lines. You know what each step needs, what it produces, and what can go wrong — **before reading a line of implementation**.

```fsharp
// Compose them into a pipeline:
let placeOrderWorkflow =
    validateOrder
    >> Result.map priceOrder
    >> Result.bind placeOrder
```

Each step is a function. Errors short-circuit. The types guarantee the steps connect correctly.

---

## The full F# picture

```fsharp
type OrderId        = OrderId        of string
type CustomerId     = CustomerId     of int
type TrackingNumber = TrackingNumber of string

module Email =
    type Address = private Address of string
    let create (s: string) : Result<Address, string> = ...

type OrderStatus =
    | Unvalidated
    | Validated
    | Priced    of price: decimal
    | Shipped   of trackingNumber: TrackingNumber
    | Delivered of deliveredAt: DateTime
    | Cancelled of reason: string

type Order = {
    Id       : OrderId
    Customer : CustomerId
    Email    : Email.Address   // if you have one, it's valid
    Status   : OrderStatus     // one case, always the right one
}
```

Keep this in mind.

---

## The code we actually write

```go
type Order struct {
    ID          string
    CustomerID  string
    Email       string
    Status      string
    TrackingNum string
}
```

Now that you've seen what's possible, what's wrong here?

---

## Primitive Obsession

Everything is possible. Nothing is guaranteed.
- Is `Email` validated? By whom? When?
- Is `TrackingNum` set? Only when shipped? What if `Status` is `"pending"`?
- What are the valid values of `Status`? The compiler doesn't know.
- Can you pass an `ID` where a `CustomerID` is expected? Yes. Silently.

> **The type system is not modeling your domain. It's just holding your data.**

---

<!-- .slide: class="centered" -->
# Part II
## Go — taking what matters

---

## What we already have

Before translating anything: we already run the linters that close the most important gap.

**`exhaustive`** — build fails if a `switch` over a const enumerated type misses a case, or a `map` literal does not include a key

**`go-check-sumtype`** — build fails if a type switch over a sealed `//sumtype:decl` interface misses a case

These two linters exist because the Go community independently arrived at the same conclusion F# encoded into its type system: **exhaustive handling of closed variant sets is too important to leave to code review.**

We already have the enforcement. The patterns below are what make it meaningful.

---

## New Types in Go

```go
type OrderId        string
type CustomerId     int
type TrackingNumber string
```

```go
func processOrder(id OrderId, cid CustomerId) { ... }

processOrder(order.CustomerID, order.ID)
// ← compile error: CustomerId is not OrderId
```

Go's type definitions are **real distinct types**. Assignment and passing are type-checked. This works today, for free.

Two differences:

- **Wrapper boundaries:** `Account(someInt64)` converts trivially; F# makes crossing the boundary deliberately explicit.
- **Immutability:** Go passes values by value, and receiver choice makes method mutation visible, but a type cannot enforce immutability of composite or referenced state. F# defaults to immutable bindings and records.

---

## Sum types in Go — the sealed interface pattern

```go
//sumtype:decl
type OrderStatus interface{ orderStatus() }

type Unvalidated struct{}
type Validated   struct{}
type Priced      struct{ Price          decimal.Decimal }
type Shipped     struct{ TrackingNumber string          }
type Delivered   struct{ DeliveredAt    time.Time       }
type Cancelled   struct{ Reason         string          }

func (Unvalidated) orderStatus() {}
func (Validated)   orderStatus() {}
func (Priced)      orderStatus() {}
func (Shipped)     orderStatus() {}
func (Delivered)   orderStatus() {}
func (Cancelled)   orderStatus() {}
```

Three pieces working as a unit. The unexported method seals the interface; external packages can't satisfy it. `//sumtype:decl` declares a sealed sum type. `go-check-sumtype` enforces it at build time.

---

## Smart constructors in Go — as close as it gets

```go
package email

type Address struct {
    v string  // unexported — nothing outside this package can set it directly
}

func New(s string) (Address, error) {
    if !strings.Contains(s, "@") || len(s) < 3 {
        return Address{}, fmt.Errorf("%q is not a valid email address", s)
    }
    return Address{v: s}, nil
}

func (a Address) String() string { return a.v }
```

```go
// From any other package — both are compile errors:
bad  := email.Address{v: "bad"}   // unexported field
bad2 := email.Address("bad")      // no defined conversion from string to struct

// The only valid path:
addr, err := email.New(rawInput)
```

Package-internal code can still access `v` directly — that's the remaining gap. Outside the package, the constructor is the only path.

---

## Making illegal states unrepresentable in Go

```go
//sumtype:decl
type ContactInfo interface{ contactInfo() }

type EmailOnly     struct { Address email.Address }
type PhoneOnly     struct { Number  phone.Number  }
type EmailAndPhone struct {
    Address email.Address
    Number  phone.Number
}

func (EmailOnly)     contactInfo() {}
func (PhoneOnly)     contactInfo() {}
func (EmailAndPhone) contactInfo() {}

type Contact struct {
    Name string
    Info ContactInfo   // always exactly one of the three cases. always.
}
```

No `Contact` without contact info. Add a variant: every type switch that misses it is a build failure.

---

## Exhaustive matching — side by side

```fsharp
// F# — forgot a case? Compiler error.
match contact.Info with
| EmailOnly email           -> sendEmail email
| PhoneOnly phone           -> sendSms phone
| EmailAndPhone (email, _)  -> sendEmail email
```

```go
// Go — forgot a case? Build error.
switch info := contact.Info.(type) {
case EmailOnly:     sendEmail(info.Address)
case PhoneOnly:     sendSMS(info.Number)
case EmailAndPhone: sendEmail(info.Address)
}
```

Same guarantee. Different delivery mechanism. We have it.

---

## The pipeline — what the types enforce

The enforcement is in the **distinct types at each stage**:

```go
func validateOrder(o UnvalidatedOrder) (ValidatedOrder, error) { ... }
func priceOrder(o ValidatedOrder) PricedOrder                  { ... }
func placeOrder(o PricedOrder) (*OrderPlaced, error)           { ... }
```

```go
placeOrder(unvalidatedOrder)  // ← compile error: UnvalidatedOrder is not PricedOrder
```

```go
func PlaceOrderWorkflow(input UnvalidatedOrder) (*OrderPlaced, error) {
    validated, err := validateOrder(input)
    if err != nil { return nil, err }

    priced := priceOrder(validated)
    return placeOrder(priced)
}
```

Each boundary allocates a new struct — justified when the step does real work. That constraint is the point.

---

## The transforming step — making the boundary worth it

The output type should carry **proof** the input type doesn't:

```go
type UnvalidatedOrder struct {
    CustomerID string         // raw — could be anything
    Email      string
}

type ValidatedOrder struct {
    CustomerID ids.Customer   // parsed, typed — not a string
    Email      email.Address  // proven valid — not a string
}
```

```go
func validateOrder(o UnvalidatedOrder) (ValidatedOrder, error) {
    custID, err := ids.ParseCustomer(o.CustomerID)
    if err != nil { return ValidatedOrder{}, err }
    addr, err := email.New(o.Email)
    if err != nil { return ValidatedOrder{}, err }
    return ValidatedOrder{        // exhaustruct: missing field → compile error
        CustomerID: custID,
        Email:      addr,
    }, nil
}
```

`exhaustruct` requires every field to be explicitly provided. Add a field to `ValidatedOrder` and every construction site is a build error until you handle it.

---

<!-- .slide: data-visibility="hidden" -->
## Go 1.27 makes Result chainable

Generic methods can introduce the next contained type `U`. Before Go 1.27, type-changing `Map` and `Bind` had to be package functions.

```go
func validateOrder(o UnvalidatedOrder) Result[ValidatedOrder]
func priceOrder(o ValidatedOrder)      PricedOrder
func placeOrder(o PricedOrder)         Result[OrderPlaced]

result := validateOrder(input).
    Map(priceOrder).
    Bind(placeOrder)
```

`Map` transforms a successful value; `Bind` chains another fallible step. This is compact because every stage is unary and context-free.

---

<!-- .slide: data-visibility="hidden" -->

## `(T, error)` remains the default

Real workflows commonly take a context and call repositories or services:

```go
validated, err := validateOrder(ctx, repo, input)
if err != nil { return OrderPlaced{}, err }
priced, err := priceOrder(ctx, pricing, validated)
if err != nil { return OrderPlaced{}, err }
return placeOrder(ctx, repo, priced)
```

Adapting those signatures to `Map` and `Bind` requires closures or another effect abstraction. Start with ordinary pairs; a package-local `Result[T]` earns its place only when several context-free transformations already fit and the chain is visibly clearer.

---

## The honest reckoning

| | F# | Go |
|-|----|----|
| Immutability | Compiler | Convention |
| Private constructors | Module | Package (unexported field) |
| Exhaustive matching | Compiler | `exhaustive` + `go-check-sumtype` ✓ |
| Newtypes | DU, forced unwrap | Type def, trivial cast |
| Error handling | `Result` keeps cases together | `(T, error)` by default; local `Result[T]` when earned |
| Railway composition | `Result.map` / `bind` + `>>` | Generic `Map` / `Bind` when signatures align |
| Null safety | `option`; no null | `nil` everywhere; `pkg/optional` ✓ |

Go uses **linters and convention** where F# uses the **compiler**.

---

## Bonus: F# oddities

**Units of measure** — the compiler tracks physical units through arithmetic:

```fsharp
[<Measure>] type kg
[<Measure>] type lb

let mass = 68.0<kg>
let goal = 150.0<lb>

mass + goal   // COMPILE ERROR: kg ≠ lb
```

> _This is why the Mars Polar Lander burned up in 1999. (F# didn't exist yet. The lesson does.)_

---

## Bonus: Custom operators

Almost any symbol combination is a valid operator name:

```fsharp
// The >> from slide 4? Defined exactly like this:
let (>>) f g x = g (f x)

// Unicode is legal:
let π   = System.Math.PI
let (∘) f g x = f (g x)      // the actual mathematical symbol

// Domain operators:
let (<+>) (Money a) (Money b) = Money (a + b)
total <+> tax <+> shipping
```

Fixity is determined by the first character: infix is the default; No postfix. Prefix operators must start with `~` (the `~` is dropped at the call site):

```fsharp
let (~%%) x = x * x
%% 5   // 25
```

Associativity is fixed by the first character: left-associative unless it starts with `^` or `**`.

The backward pipe `<|` is left-associative, so `f <| g <| 3` is a type error: it parses as `(f <| g) <| 3`.


---

## Further reading

- **"Domain Modeling Made Functional"** — Scott Wlaschin (the source of all of this)
- **fsharpforfunandprofit.com** — Wlaschin's blog; "Designing with Types" series is free
- **"Domain-Driven Design"** — Eric Evans (the original DDD book)
- Go: `github.com/nishanths/exhaustive` - exhaustive switch linter (we use this)
- Go: `github.com/alecthomas/go-check-sumtype` - exhaustive type switches over sealed interfaces (we use this)
- Go: `github.com/GaijinEntertainment/go-exhaustruct`  - exhaustive struct declarations
- F# demo: [Type-Safe Linear Algebra](https://gist.github.com/TheFellow/4cb72a3dbce7ad0c4033054ecf38c496) — phantom types, custom operators, associativity
- F# demo: [Octonions and the Standard Model](https://gist.github.com/TheFellow/55fd4f0d58275d8b21b8cc070da71633) — Cohl Furey's algebraic approach to particle physics

---

<!-- .slide: class="centered" -->
# Questions?

_Companion article:_ [Making Illegal States Unrepresentable in Go](/articles/making-illegal-states-unrepresentable-in-go/)
{% endraw %}
</script>
</section>
