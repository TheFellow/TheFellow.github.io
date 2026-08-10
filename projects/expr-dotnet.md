<!-- Generated from https://thefellow.github.io/projects/expr-dotnet/ by scripts/generate_llm_content.py; do not edit. -->

# Expr for .NET

Source: [https://thefellow.github.io/projects/expr-dotnet/](https://thefellow.github.io/projects/expr-dotnet/)

## Pyramid summary

- **~2 words:** Typed expressions
- **~8 words:** A safe .NET expression language with inspectable compilation and bounded execution.
- **Expanded:** A safe, statically checked expression language for .NET, with a public AST, an optimizing bytecode compiler, and bounded execution.

## Full content

[Install from NuGet](https://www.nuget.org/packages/Expr)
[View the repository](https://github.com/TheFellow/expr-dotnet)
[Read the security model](https://github.com/TheFellow/expr-dotnet/blob/main/docs/security-model.md)

I wanted a way for a .NET application to accept useful logic without accepting arbitrary C#. A pricing rule, feature condition, authorization predicate, or filter should be able to mention the values the application deliberately exposes, use a compact collection-oriented language, and fail early when its names or types are wrong. It should not acquire the rest of the process as an accidental API.

[Expr](https://expr-lang.org/) already has the language I wanted. It combines familiar operators with predicates such as `all`, `filter`, `map`, and `reduce`, then compiles the result to bytecode for a small virtual machine. Expr for .NET is my semantic port of that language. Version 0.1.0 is now available as the dependency-free [`Expr` package on NuGet](https://www.nuget.org/packages/Expr), targeting .NET 10 and C# 14.

The port retains Expr's observable language behavior while giving the .NET side its own deliberate shape. Environment schemas are typed, compiled expressions are immutable and reusable, every evaluation gets isolated runtime state, and the syntax tree is a public API rather than a compiler detail. Explicit schemas also keep the complete path available to trimmed and Native AOT applications.

```text
customer == 'Ada' &&
all(prices, # > 0.0) &&
sum(prices) >= 100.0
```

That expression is small, but the path from untrusted text to a trustworthy answer crosses most of the interesting parts of language implementation: lexing, parsing, static checking, tree rewriting, optimization, bytecode generation, resource accounting, and host integration.

## Start with a host contract

Install the package with the ordinary .NET CLI:

```sh
dotnet add package Expr
```

For a one-off expression that needs no application values, `Evaluate` is enough:

```csharp
using Expr;

object? result = ExprEngine.Evaluate("all([2, 3, 5], # > 0)");
// true
```

The more interesting case is a rule evaluated repeatedly against application data. I define the visible environment once, require a Boolean result, compile once, then reuse the immutable compilation:

```csharp
using System.Collections.Generic;
using Expr;
using Expr.Configuration;
using Expr.Runtime;
using Expr.Types;

var schema = new ExprEnvironmentSchemaBuilder<OrderContext>()
    .Member("customer", static value => value.Customer, ExprTypes.String)
    .ArrayMember("prices", static value => value.Prices, ExprTypes.Float)
    .Build();

ExprConfiguration configuration = ExprConfiguration.Default
    .WithEnvironment(schema)
    .WithExpectedType(ExprTypes.Boolean);

CompiledExpression rule = ExprEngine.Compile(
    "customer == 'Ada' && sum(prices) >= 100.0",
    configuration);

bool accepted = (bool)rule.Run(
    new OrderContext("Ada", [45.0, 60.0]))!;

public sealed record OrderContext(
    string Customer,
    IReadOnlyList<double> Prices);
```

The schema is both an integration API and a security boundary. The expression can see `customer` and `prices` under their Expr names, and the checker knows their types before any order exists. A misspelled `customers`, an invalid comparison, or a rule that returns a string fails during `Compile`.

For conventional applications, `ExprEnvironmentSchema.Reflect<T>()` can build and cache a schema from public CLR members. The explicit builder is the stronger boundary when the exposed names should differ from the object model, and it is the path for trimming and Native AOT because it needs no runtime discovery.

Application functions cross the same boundary. An `ExprFunction` declares one or more Expr-visible signatures separately from the delegate that implements them. The checker can therefore reject a bad call before the delegate runs. Registering a function grants expression authors access to host code, so that registration remains an application decision rather than something expressions can discover.

## Follow the compiler pipeline

<figure class="article-figure">
  <img src="/assets/images/projects/expr-dotnet/compiler-pipeline.png" alt="Expr source passes through a lexer and parser into a public immutable syntax tree, then through static checking and semantic patchers, optimizer rewrites, bytecode compilation, and an isolated bounded virtual machine evaluation.">
  <figcaption>Compilation turns source into a checked, inspectable, immutable program. Evaluations share that program while keeping stacks, counters, variables, and temporary values isolated.</figcaption>
</figure>

The high-level API is a composition of public stages:

```text
source -> lexer -> parser -> public AST -> binder and type checker
       -> semantic patchers -> optimizer -> bytecode compiler -> VM
```

The lexer retains source positions and produces the tokens needed for Expr's operators, literals, collection syntax, predicates, pipes, slices, optional access, and `let` bindings. The parser then builds immutable node records with source locations. Invalid syntax stops here with a diagnostic anchored to the original text.

The checker resolves identifiers against the environment and function tables, annotates nodes with Expr types, verifies overloads and operators, and enforces the expected result type. Semantic patchers handle host-directed transformations such as operator overloads, context injection, value providers, and time-zone behavior without mixing those decisions into parsing.

Optimization is tree rewriting over that checked model. Constant expressions can collapse at compile time. Membership in a constant collection can become a faster lookup. Predicate shapes such as filtered counts can be fused so the VM does not have to materialize an intermediate collection. Optimizations are optional, and the conformance suite checks that enabling them does not change the result.

The compiler finally emits an immutable stack-machine program. Instructions retain source associations for diagnostics, while constants, variable slots, and function bindings are fixed into the program. `CompiledExpression` exposes the checked `SyntaxTree`, `SemanticModel`, and `Program`, so the convenient API does not hide the work it performed.

## Keep the syntax tree public

Embedded languages often expose only `Compile` and `Run`. That is enough until an application needs to explain a rule, migrate a name, restrict a construct, translate part of a predicate into a query, or build editor tooling. Re-parsing source with an unrelated grammar is a poor foundation for those jobs.

Expr for .NET treats its immutable AST as a product surface. It can be walked, printed canonically, visited, and replaced without opening the checker or VM internals:

```csharp
using Expr;
using Expr.Syntax;

SyntaxTree tree = ExprEngine.Parse("price * quantity");

SyntaxNode rewritten = new RenamePrice().Visit(tree.Root);
Console.WriteLine(SyntaxPrinter.Print(rewritten));
// unitPrice * quantity

sealed class RenamePrice : SyntaxRewriter
{
    protected override SyntaxNode VisitNode(SyntaxNode node) =>
        node is IdentifierNode { Name: "price" } identifier
            ? identifier with { Name = "unitPrice" }
            : node;
}
```

Because the nodes are sealed records with strongly typed children, consumers can use C# pattern matching and non-mutating `with` expressions. A rule management UI can retain source positions for diagnostics, an analyzer can reject project-specific constructs, and a data adapter can conservatively translate the subset it understands. Those tools operate on the same tree the compiler checks.

## Make execution bounded and reusable

Expr programs do not contain general loops or recursion, but a terminating expression can still be expensive. A large range, nested predicates, growing strings, JSON conversion, or a hostile regular expression all consume finite but potentially unreasonable resources. Cancellation alone is not a deterministic limit, especially when many short instructions perform a large amount of work before a caller observes elapsed time.

Each evaluation therefore carries independent limits:

```csharp
using System;
using Expr.Execution;

object? value = rule.Run(
    environment,
    new ExprEvaluationOptions
    {
        WorkBudget = 100_000,
        MemoryBudget = 1_000_000,
        MaximumCollectionLength = 10_000,
        MaximumStackDepth = 1_024,
        RegularExpressionTimeout = TimeSpan.FromMilliseconds(100),
    },
    cancellationToken);
```

The VM charges instruction work and expression-created memory, checks collection and stack growth, uses non-backtracking regular expressions with explicit time and pattern limits, and observes cancellation at bounded dispatch and host-call points. Parser source length, node count, and checker depth have their own compile-time controls.

The compiled program itself contains no per-run stack or counters. It is safe to reuse concurrently because each call creates isolated execution state. The environment values and custom host functions remain the application's responsibility, which makes the ownership line explicit: Expr bounds and isolates the interpreter, while the host controls what crossing into application code means.

The reflection boundary follows the same rule. Unschematized values typed as `any` cannot be used to wander through arbitrary CLR members, obtain `Type` objects, call constructors, or invoke members the host did not expose. There is no untrusted bytecode deserialization path. Expression text enters through the parser, and compiled programs are trusted only when produced by the compatible library pipeline.

## Port semantics, not Go implementation details

The original Expr implementation is written in Go. A useful .NET port cannot simply rename Go structs and reproduce their package layout. Go interfaces, reflection, integer behavior, time values, regular expressions, Unicode tables, and collection types do not have one-to-one CLR equivalents.

I use the upstream implementation and tests as the semantic oracle, then choose idiomatic .NET representations at the host boundary. Expr integers use `long`; time values use `DateTimeOffset`; durations use `TimeSpan`; arrays and maps accept ordinary read-only .NET collection shapes; context-aware host functions receive a `CancellationToken`. Where the platforms cannot agree exactly, the difference is narrow, documented, and tested.

The release gate makes that discipline inspectable. Its traceability inventory accounts for 585 upstream tests, 59 benchmarks, 42 examples, and one fuzz entry point at the pinned revision. Each of those 687 symbols has an explicit disposition linking it to differential corpus cases, focused .NET evidence, a benchmark, a reviewed platform mapping, or embedded Go support code. An explicit gap blocks release.

The larger generated corpus runs 43,689 upstream expressions and 673 CrowdSec expressions through the public .NET pipeline. That does not replace focused tests. It catches broad semantic drift, while focused cases explain the boundary and preserve useful failures.

## Measure the whole lifecycle

Expression engines have at least two performance stories. Compilation covers parsing, checking, optimization, and bytecode generation. Evaluation covers the hot VM path after that work has been cached. Mixing the two makes a reusable compiled expression look much more expensive than its steady-state behavior.

The benchmark suite measures syntax operations, full compilation, scalar policy evaluation, CLR and map access, regular expressions, and collection predicates separately. An initial short-run baseline on an Intel Core i5 Mac measured a complete small policy compilation at 14.770 microseconds. After removing detailed-result allocations from ordinary `Run` calls and making diagnostic containers lazy, the focused scalar policy workload used 536 bytes per evaluation, down from 920 bytes in the earlier baseline. Its 801.7 nanosecond mean was encouraging, although the short runs were too variable to treat that timing difference as established.

That is the kind of performance work I want in this project: preserve the machine description and revision, distinguish allocation evidence from noisy latency, and trace a result back to an architectural choice. Compile-time optimization has a cost, so callers should cache compiled expressions. Evaluation allocation still has room to improve, especially for collection predicates, but pooling cannot be allowed to leak values or counters between tenants.

## Use the parts you need

The shortest route into the package depends on the integration:

- Use `ExprEngine.Evaluate` for a one-off expression with no reusable setup.
- Use an `ExprEnvironmentSchema`, an expected result type, and `Compile` for application rules evaluated more than once.
- Register `ExprFunction` values when the language needs a deliberately exposed application operation.
- Use `Parse`, `SyntaxWalker`, `SyntaxRewriter`, and `SyntaxPrinter` when rules need analysis, migration, formatting, or translation.
- Set explicit evaluation budgets at every untrusted boundary, even when application-level cancellation and timeouts also exist.
- Use explicit environment schemas for trimming and Native AOT. A working sample in the repository publishes and runs the complete path without reflection-based discovery.

Version 0.1.0 is the first public release, and the API remains pre-1.0 while it gets real use. The core shape is already the one I wanted: expression authors get a compact, capable language; applications get a typed and inspectable contract; and evaluation remains a small, bounded machine rather than a doorway into arbitrary C#.
