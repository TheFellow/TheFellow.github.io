<!-- Generated from https://thefellow.github.io/notes/porting-cedar-semantics-from-go-to-dotnet/ by scripts/generate_llm_content.rb; do not edit. -->

# Porting Cedar from Go to .NET: Semantics Before Syntax

Source: [https://thefellow.github.io/notes/porting-cedar-semantics-from-go-to-dotnet/](https://thefellow.github.io/notes/porting-cedar-semantics-from-go-to-dotnet/)

## Pyramid summary

- **~2 words:** Semantic porting
- **~8 words:** How conformance tests preserve Cedar behavior while C# APIs remain idiomatic.
- **Expanded:** How cedar-dotnet establishes correct Cedar behavior through conformance tests, then uses benchmarks to make it fast.

## Full content

I contribute to [cedar-go](https://github.com/cedar-policy/cedar-go), the Cedar project's official Go implementation. [cedar-dotnet](https://github.com/TheFellow/cedar-dotnet) is my C# implementation, shaped for the .NET ecosystem while preserving the same semantics.

## A semantic dependency

cedar-dotnet doesn't wrap a Go binary or call cedar-go at runtime. The projects share the Cedar model, including policies, entities, schemas, requests, authorization decisions, and serialization contracts, but each implementation owns its language-facing API.

A direct transliteration would preserve the wrong things. Go package boundaries, error-return conventions, and type patterns are not automatically good C# APIs. The port instead uses C# records, interfaces, collections, exceptions, and builders where they make the model clearer, while preserving the behavior that applications and policy authors depend on.

The useful question is not “does this C# file resemble the Go file?” It is “given the same Cedar input, do both implementations reach the same result?”

## Correctness first, then performance

The first obligation is behavioral correctness. Recent work has included accepting annotations without values, handling cyclic entity-type parent declarations, supporting shorthand common-type names in schema JSON, rejecting IPv6 zone identifiers, and correctly classifying IPv4-mapped IPv6 addresses. These cases may look small in isolation, but each closes a gap where valid input could fail or invalid input could slip through.

Only after that behavior is pinned down by tests does optimization make sense. Benchmarks can then identify expensive paths without making performance a matter of guesswork. One recent pass cached compiled policy evaluators, removed allocations from common evaluator results, replaced LINQ in hot paths, and used stack allocation while hashing. Depending on the scenario, those changes made authorization up to 12 times faster and reduced allocations by as much as 98 percent, with the full test suite still passing.

That ordering matters: tests establish what the implementation must do, and benchmarks show where it can do the same work more efficiently. Performance work is valuable only while the behavioral contract remains intact.

## Conformance is the shared language

Source code is a useful reference, but tests are a better agreement. At the time of writing, cedar-dotnet runs 124,000 cases from the official Cedar conformance corpus alongside 2,462 project tests: 126,462 tests in total. The corpus is also exercised by cedar-go and the Rust reference implementation.

This gives the port an external definition of success. Parser choices, AST shapes, and public APIs can remain idiomatic to C#, while authorization and validation behavior are checked against the same scenarios as the other implementations.

It also makes upstream work more actionable. A semantic change in cedar-go should lead to a focused question: which behavior changed, which corpus or unit cases demonstrate it, and what is the most natural way to express that behavior in C#?

## Keeping pace without copying blindly

cedar-dotnet tracks cedar-go through a daily semantic-porting pipeline. The pipeline analyzes upstream commits, identifies behaviorally relevant changes, and ports them while respecting C# idioms. It is described as a DOT workflow and executed with [F#kYeah](https://github.com/TheFellow/fkyeah), the pipeline engine that is also featured on this site.

Automation helps with attention, not judgment. An upstream commit can mix refactoring, tests, API changes, and new semantics. The important work is separating those concerns and deciding what the .NET implementation should adopt, adapt, or ignore.

The result should feel native to .NET without drifting from Cedar's contract: shared behavior first, deliberate API and performance work on top.

## Where to look

- [cedar-go](https://github.com/cedar-policy/cedar-go) for the official Go implementation and upstream development.
- [cedar-dotnet](https://github.com/TheFellow/cedar-dotnet) for the C# API, conformance suite, and semantic-porting workflow.
- [`cedar-dotnet/semport`](https://github.com/TheFellow/cedar-dotnet/tree/main/semport) for the pipeline that follows upstream changes.
