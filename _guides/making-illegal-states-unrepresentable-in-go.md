---
title: "Making Illegal States Unrepresentable in Go"
date: 2026-03-06
last_modified_at: 2026-08-28 00:40:42 -0700
excerpt: "What F#'s algebraic types teach about modeling identifiers, validated values, closed variants, and typed workflows in Go, including how generic methods make Result pipelines practical."
permalink: /articles/making-illegal-states-unrepresentable-in-go/
redirect_from: /guides/making-illegal-states-unrepresentable-in-go/
order: 45
featured: true
status: "Domain modeling guide"
icon: "exhaustive"
accent: "#f06595"
topics: ["Algebraic types", "Go domain modeling", "Generic methods"]
---

A type can do more than hold data. It can record which states the domain permits, carry evidence that validation happened, and make the compiler reject operations performed out of order.

F# makes these techniques unusually direct. Its records, discriminated unions, private union cases, and exhaustive pattern matching let a model describe both the shape of valid data and the alternatives that may occur. Go has no native discriminated unions, but defined types, package boundaries, sealed interfaces, constructors, and static analysis recover much of the same design value.

I will build one order-processing model in both languages. The comparison is useful because F# exposes the underlying algebra clearly, while Go shows which parts of that algebra survive in an ordinary imperative codebase.

## Read the F# signatures first

F# function signatures read from left to right. The rightmost type is the result:

```fsharp
// Go: func(int, string) int
// F#: int -> string -> int
```

Every F# function formally takes one argument. A declaration that appears to take several arguments is a sequence of functions:

```fsharp
let add x y = x + y       // int -> int -> int
let add3 = add 3          // int -> int
add3 5                    // 8
```

That representation makes partial application and composition ordinary operations. The pipeline operator passes a value into the next function, and the composition operator connects compatible functions:

```fsharp
let normalize = String.trim >> String.toLower

"  Hello  "
|> normalize
|> Email.create
```

The compiler infers the intermediate types. If one function produces a value the next function cannot accept, the code does not compile. These signatures become especially useful when the types describe domain stages instead of primitives.

## Product types and sum types

<figure class="article-figure">
  <img src="{{ '/assets/images/articles/illegal-states/state-space.png' | relative_url }}" alt="Four combinations created by independent lifecycle options include two invalid states. Replacing them with Draft and Published cases leaves only meaningful states and attaches publication time to Published.">
  <figcaption>Independent options multiply combinations. Named cases reduce the model to states the domain actually permits.</figcaption>
</figure>

A record is a product type. A value contains one value for every field:

```fsharp
type User = {
    Name      : string
    Email     : string
    CreatedAt : DateTime
}
```

A discriminated union is a sum type. A value is exactly one of its named cases, and each case may carry different data:

```fsharp
type PaymentMethod =
    | Cash
    | PayPal     of accountEmail: string
    | CreditCard of cardNumber: string * expiry: DateTime
```

The names come from cardinality. If `Theme` has two possible values and `Color` has three, a record containing both has $2 \times 3 = 6$ possible values. A union containing either one has $2 + 3 = 5$ possible values.

That arithmetic is a practical modeling tool. Every unnecessary Boolean or optional field multiplies the number of states the rest of the program must understand. A sum type can instead enumerate the cases the domain actually permits.

## Put lifecycle data on the state that owns it

Consider an order moving through this lifecycle:

```text
Unvalidated -> Validated -> Priced -> Placed -> Shipped -> Delivered
                                      |
                                      +-> Cancelled
```

A string status and a collection of conditionally populated fields allow combinations that make no sense:

```go
type Order struct {
	ID             string
	CustomerID     string
	Email          string
	Status         string
	Price          decimal.Decimal
	TrackingNumber string
	DeliveredAt    time.Time
	CancelReason   string
}
```

Nothing in this type answers whether `"shipping"` is a valid status, whether a shipped order must have a tracking number, or whether a delivered order may also have a cancellation reason. The type system is storing the data without modeling its constraints.

In F#, each state can carry only the data that belongs to it:

```fsharp
type OrderStatus =
    | Unvalidated
    | Validated
    | Priced    of price: decimal
    | Placed    of placedAt: DateTime
    | Shipped   of trackingNumber: TrackingNumber
    | Delivered of deliveredAt: DateTime
    | Cancelled of reason: string
```

There is no tracking-number field to inspect on `Unvalidated`. There is no cancellation reason waiting at its zero value on `Delivered`. Code must first establish which case it has, then it receives the data carried by that case.

## Give primitives domain meaning

An order identifier and a customer identifier may share a storage representation without being interchangeable concepts.

F# uses single-case discriminated unions to keep those concepts distinct:

```fsharp
type OrderId    = OrderId of string
type CustomerId = CustomerId of string

let processOrder (orderId: OrderId) (customerId: CustomerId) = ...

processOrder customerId orderId // does not compile
```

Unwrapping is explicit pattern matching:

```fsharp
let (OrderId rawOrderId) = orderId
```

Go defined types provide the same protection when values are assigned or passed:

```go
type OrderID string
type CustomerID string

func processOrder(orderID OrderID, customerID CustomerID) {}

processOrder(customerID, orderID) // does not compile
```

Go permits an explicit conversion such as `OrderID(raw)`, so a defined string type does not prove that parsing or validation occurred. It still prevents accidental interchange, documents intent in signatures, and gives domain behavior a natural method set.

## Use a smart constructor when a value carries proof

Sometimes a new type should mean more than “this string is used in a particular place.” An email address should mean that the program accepted the value according to its email rules.

F# can hide a union case inside its module and expose a fallible constructor:

```fsharp
module Email =
    type Address = private Address of string

    let create (raw: string) : Result<Address, string> =
        let value = raw.Trim().ToLowerInvariant()
        if value.Contains("@") && value.Length >= 5 then
            Ok (Address value)
        else
            Error $"'{raw}' is not a valid email address"

    let value (Address value) = value
```

Outside the module, `Email.Address "bad"` does not compile because the case is private. Callers receive either `Ok address` or `Error message`. Obtaining the address requires choosing how to handle both cases, and an incomplete match produces a compiler warning that a project can promote to an error. The whole result can still be deliberately discarded; the important property is that its value and failure cannot separate accidentally.

Go can enforce the same constructor path at a package boundary by using an unexported field:

```go
package email

type Address struct {
	value string
}

func New(raw string) (Address, error) {
	value := strings.ToLower(strings.TrimSpace(raw))
	if !strings.Contains(value, "@") || len(value) < 5 {
		return Address{}, fmt.Errorf("%q is not a valid email address", raw)
	}
	return Address{value: value}, nil
}

func (a Address) String() string { return a.value }
```

From another package, neither of these bypasses compiles:

```go
bad1 := email.Address{value: "bad"} // value is unexported
bad2 := email.Address("bad")        // no conversion from string to struct
```

Code in `package email` can still construct the struct directly, and `email.Address{}` remains a legal zero value everywhere. A method such as `Valid`, validation during decoding, or an API that keeps the zero value out of stored domain objects must account for that difference. The package boundary controls construction, but Go does not make every zero value meaningful automatically.

## Replace combinations of options with named cases

Suppose a contact must have at least an email address or a phone number. Two optional fields encode four combinations even though only three are valid:

```fsharp
type Contact = {
    Email : Email.Address option
    Phone : PhoneNumber option
}
```

The absent-and-absent combination remains representable. A union describes the three allowed cases directly:

```fsharp
type ContactInfo =
    | EmailOnly     of Email.Address
    | PhoneOnly     of PhoneNumber
    | EmailAndPhone of Email.Address * PhoneNumber

type Contact = {
    Name : string
    Info : ContactInfo
}
```

Go can represent a closed set of variants with a sealed interface. The unexported method prevents packages outside `contact` from adding implementations:

```go
package contact

//sumtype:decl
type Info interface {
	contactInfo()
}

type EmailOnly struct {
	Address email.Address
}

type PhoneOnly struct {
	Number phone.Number
}

type EmailAndPhone struct {
	Address email.Address
	Number  phone.Number
}

func (EmailOnly) contactInfo()     {}
func (PhoneOnly) contactInfo()     {}
func (EmailAndPhone) contactInfo() {}
```

This closes the set of non-nil implementations, but Go interfaces can be `nil`. A `Contact` with an exported `Info` field would therefore still have an invalid zero value. A constructor can enforce the invariant at the package boundary:

```go
type Contact struct {
	name string
	info Info
}

func New(name string, info Info) (Contact, error) {
	if strings.TrimSpace(name) == "" {
		return Contact{}, errors.New("contact name is required")
	}
	if info == nil {
		return Contact{}, errors.New("contact information is required")
	}
	return Contact{name: name, info: info}, nil
}
```

The model still eliminates the fourth non-nil variant. The constructor handles the language-level `nil` and zero-value escape hatches explicitly.

## Make variant handling exhaustive

The benefit of a closed set appears when code consumes it. F# pattern matching names each case and binds the data that case carries:

```fsharp
let notify info =
    match info with
    | EmailOnly email          -> sendEmail email
    | PhoneOnly phone          -> sendSMS phone
    | EmailAndPhone (email, _) -> sendEmail email
```

If a new `PostalOnly` case is added, the compiler reports every incomplete match. Teams commonly treat that warning as an error, turning a domain change into a concrete list of decisions that must be made before the build passes.

Go type switches do not provide that check by themselves:

```go
func notify(info contact.Info) {
	switch value := info.(type) {
	case contact.EmailOnly:
		sendEmail(value.Address)
	case contact.PhoneOnly:
		sendSMS(value.Number)
	case contact.EmailAndPhone:
		sendEmail(value.Address)
	}
}
```

The [`go-check-sumtype`](https://github.com/alecthomas/go-check-sumtype) analyzer recognizes the `//sumtype:decl` marker and reports a missing case. The [`exhaustive`](https://github.com/nishanths/exhaustive) analyzer performs the corresponding check for switches over enum-like defined types. Running either analyzer in the repository's required lint or build checks changes an omitted case from a review concern into a failed check.

The three parts work together:

1. An unexported method closes the set of implementations.
2. `//sumtype:decl` records that exhaustive handling is intended.
3. Static analysis rejects type switches that omit a known variant.

Without the sealed interface, another package could add cases the analyzer cannot know about. Without the analyzer, Go accepts a partial switch. The model and its enforcement are one design.

## Model workflows as transformations

State-specific types are useful even when a domain has a linear path rather than alternatives. The order workflow can say what each step requires and what evidence it produces:

```fsharp
type ValidateOrder =
    UnvalidatedOrder -> Result<ValidatedOrder, OrderError>

type PriceOrder =
    ValidatedOrder -> PricedOrder

type PlaceOrder =
    PricedOrder -> Result<OrderPlaced, OrderError>
```

The same boundaries are ordinary Go function signatures:

```go
func validateOrder(UnvalidatedOrder) (ValidatedOrder, error)
func priceOrder(ValidatedOrder) PricedOrder
func placeOrder(PricedOrder) (OrderPlaced, error)
```

Passing an `UnvalidatedOrder` directly to `placeOrder` does not compile. The transformation is worthwhile when the output carries proof the input did not:

```go
type UnvalidatedOrder struct {
	CustomerID string
	Email      string
}

type ValidatedOrder struct {
	CustomerID CustomerID
	Email      email.Address
}

func validateOrder(input UnvalidatedOrder) (ValidatedOrder, error) {
	customerID, err := parseCustomerID(input.CustomerID)
	if err != nil {
		return ValidatedOrder{}, err
	}

	address, err := email.New(input.Email)
	if err != nil {
		return ValidatedOrder{}, err
	}

	return ValidatedOrder{
		CustomerID: customerID,
		Email:      address,
	}, nil
}
```

The raw strings enter at the boundary. The validated stage contains domain types. Later functions cannot accidentally consume the raw representation because their signatures do not accept it.

The [`exhaustruct`](https://github.com/GaijinEntertainment/go-exhaustruct) analyzer can additionally require every field in selected struct literals to be initialized. When a field is added to `ValidatedOrder`, required lint checks then identify each transition that needs to supply it. This is not a compiler feature, but it can be a useful repository rule for domain-state construction.

## Compose results inside typed workflows

F# uses `Result.map` to transform a successful value and `Result.bind` to run the next fallible step. Either operation propagates an existing error without calling its function:

```fsharp
let placeOrderWorkflow =
    validateOrder
    >> Result.map priceOrder
    >> Result.bind placeOrder
```

Before Go 1.27, a method on `Result[T]` could not introduce the next contained type `U`. Type-changing `Map` and `Bind` operations therefore had to be package functions, which made a pipeline nested or required intermediate wrappers:

```go
result := Bind(Map(validateOrder(input), priceOrder), placeOrder)
```

Go 1.27 allows a concrete method to declare its own type parameters. `T` belongs to the receiver, while `U` belongs to one method invocation and is inferred from the function argument:

```go
type Result[T any] struct {
	value T
	err   error
	ok    bool
}

func Ok[T any](value T) Result[T]       { return Result[T]{value: value, ok: true} }
func Err[T any](err error) Result[T]    { return Result[T]{err: err} }

func (r Result[T]) Map[U any](f func(T) U) Result[U] {
	if !r.ok {
		return Err[U](r.err)
	}
	return Ok(f(r.value))
}

func (r Result[T]) Bind[U any](f func(T) Result[U]) Result[U] {
	if !r.ok {
		return Err[U](r.err)
	}
	return f(r.value)
}
```

The workflow can now read from left to right. The function signatures determine the operation: pricing is an infallible transformation, so it uses `Map`; placement can fail, so it uses `Bind`.

```go
func validateOrder(UnvalidatedOrder) Result[ValidatedOrder]
func priceOrder(ValidatedOrder) PricedOrder
func placeOrder(PricedOrder) Result[OrderPlaced]

result := validateOrder(input).
	Map(priceOrder).
	Bind(placeOrder)
```

Generic methods remove the main ergonomic objection to using `Result` inside a multi-stage domain workflow. They do not require the rest of a Go program to adopt a new error convention. Small adapters preserve native pairs at repository, transport, SDK, and public API boundaries:

```go
func FromPair[T any](value T, err error) Result[T] { /* ... */ }
func (r Result[T]) Pair() (T, error)               { /* ... */ }

func placeOrderWorkflow(input UnvalidatedOrder) (OrderPlaced, error) {
	return validateOrder(input).
		Map(priceOrder).
		Bind(placeOrder).
		Pair()
}
```

`(T, error)` remains the convention understood by Go's ecosystem. `Result` is useful where several typed transformations benefit from keeping success and failure coupled, while `FromPair` and `Pair` keep that choice inside the workflow that benefits from it.

## Know where each guarantee lives

F# and Go can express many of the same domain decisions, but they enforce them at different layers.

| Concern               | F#                                    | Go                                            |
| --------------------- | ------------------------------------- | --------------------------------------------- |
| Immutable values      | Language default                      | API design and convention                     |
| Hidden construction   | Private union case                    | Package and unexported fields                 |
| Closed variants       | Discriminated union                   | Sealed interface pattern                      |
| Exhaustive handling   | Compiler warning, optionally an error | Static analyzer in required checks            |
| Distinct primitives   | Single-case union                     | Defined type                                  |
| Fallible construction | `Result`                              | `(T, error)`                                  |
| Fallible composition  | `Result.map` and `Result.bind`        | Go 1.27 generic `Map` and `Bind` methods      |
| Missing values        | `option`                              | Pointers, `nil`, or an explicit optional type |
| Zero-value validity   | Constructed union cases               | Must be designed or checked explicitly        |

This difference affects how strongly a model can support its claims. In F#, a private union case plus immutable data can make construction through the smart constructor the only path. In Go, package-local code and zero values remain part of the design. Constructors, unexported representation, validation at serialization boundaries, and required analyzers narrow those gaps without pretending they disappeared. Generic methods improve how typed workflows compose, but they do not change where these broader guarantees live.

## Start with the state space

I now begin a domain type by listing the valid states and transitions before choosing structs or interfaces.

- If two primitives mean different things, I define different types.
- If a value is evidence that validation succeeded, I hide its representation and expose a fallible constructor.
- If alternatives carry different data, I model named variants instead of a tag plus conditional fields.
- If a workflow changes what is known, I give the stages different types.
- If a Go invariant can escape through `nil` or a zero value, I make that boundary explicit.
- If correctness depends on exhaustive handling, I put the analyzer in required repository checks.

The goal is not to reproduce F# syntax in Go. It is to make domain decisions visible in function signatures and data shapes, then place enforcement at the strongest boundary the language and toolchain provide. The compiler should reject as many incorrect programs as the model can describe, and the remaining checks should be deliberate rather than hidden in comments.

## Further reading

- Scott Wlaschin's [Domain Modeling Made Functional](https://pragprog.com/titles/swdddf/domain-modeling-made-functional/) develops this approach in F#.
- Wlaschin's free [Designing with Types](https://fsharpforfunandprofit.com/series/designing-with-types/) series introduces the core techniques.
- The [Go 1.27 release notes](https://go.dev/doc/go1.27) describe generic methods and their limits.
- My [type-safe linear algebra in F#](/notes/type-safe-linear-algebra-in-fsharp/) note shows the same idea applied to matrix dimensions.
- My [enumstruct project](/projects/enumstruct/) explores exhaustive pointer-union handling in Go.
