---
title: "Porting Cedar from Go to .NET: Semantics Before Syntax"
date: 2026-07-23 12:00:00 -0700
permalink: /notes/porting-cedar-semantics-from-go-to-dotnet/
excerpt: "How contributing to cedar-go informs cedar-dotnet—and why a trustworthy language port follows behavior instead of copying source syntax."
tags: ["Cedar", "Authorization", "Go", ".NET"]
---

I contribute to [cedar-go](https://github.com/cedar-policy/cedar-go), but I do not control it. It is the Cedar project's official Go implementation, maintained in the `cedar-policy` organization. [cedar-dotnet](https://github.com/TheFellow/cedar-dotnet) is different: it is my C# implementation, semantically ported from cedar-go and shaped for the .NET ecosystem.

That distinction is useful. cedar-go is not a project to claim as my own; it is an upstream implementation I learn from and contribute to. cedar-dotnet is where I am responsible for translating those semantics into a coherent C# library.

## A semantic dependency, not a runtime dependency

cedar-dotnet does not wrap a Go binary or call cedar-go at runtime. The projects share the Cedar model—policies, entities, schemas, requests, authorization decisions, and serialization contracts—but each implementation owns its language-facing API.

A direct transliteration would preserve the wrong things. Go package boundaries, error-return conventions, and type patterns are not automatically good C# APIs. The port instead uses C# records, interfaces, collections, exceptions, and builders where they make the model clearer, while preserving the behavior that applications and policy authors depend on.

The useful question is not “does this C# file resemble the Go file?” It is “given the same Cedar input, do both implementations reach the same result?”

## Contributions reveal where compatibility actually lives

Working in cedar-go is a reminder that compatibility often lives in details that look small in isolation. Two examples from my contributions are:

- adding binary marshal and unmarshal support for `EntityUID`, including round-trip and interface-level tests; and
- hardening IP parsing so invalid IPv6 zone identifiers and zone-like suffixes are rejected consistently.

Neither feature changes the headline description of an authorization engine. Both matter at a boundary where another system expects a stable answer. Serialization, parsing, escaping, numeric limits, extension types, and error behavior are exactly where “mostly compatible” implementations diverge.

That experience changes how I approach cedar-dotnet. Edge cases are not cleanup work after the port; they are part of the language contract.

## Conformance is the shared language

Source code is a useful reference, but tests are a better agreement. At the time of writing, cedar-dotnet runs 124,000 cases from the official Cedar conformance corpus alongside more than 2,400 project tests. The corpus is also exercised by cedar-go and the Rust reference implementation.

This gives the port an external definition of success. Parser choices, AST shapes, and public APIs can remain idiomatic to C#, while authorization and validation behavior are checked against the same scenarios as the other implementations.

It also makes upstream work more actionable. A semantic change in cedar-go should lead to a focused question: which behavior changed, which corpus or unit cases demonstrate it, and what is the most natural way to express that behavior in C#?

## Keeping pace without copying blindly

cedar-dotnet tracks cedar-go through a daily semantic-porting pipeline. The pipeline analyzes upstream commits, identifies behaviorally relevant changes, and ports them while respecting C# idioms. It is described as a DOT workflow and executed with [F#kYeah](https://github.com/TheFellow/fkyeah), the pipeline engine that is also featured on this site.

Automation helps with attention, not judgment. An upstream commit can mix refactoring, tests, API changes, and new semantics. The important work is separating those concerns and deciding what the .NET implementation should adopt, adapt, or ignore.

That is the larger lesson I take from working across both projects: a high-quality port is neither a fork nor a rewrite performed once. It is a maintained relationship between implementations, grounded in shared behavior and expressed through different language ecosystems.

## Where to look

- [cedar-go](https://github.com/cedar-policy/cedar-go) for the official Go implementation and upstream development.
- [cedar-dotnet](https://github.com/TheFellow/cedar-dotnet) for the C# API, conformance suite, and semantic-porting workflow.
- [`cedar-dotnet/semport`](https://github.com/TheFellow/cedar-dotnet/tree/main/semport) for the pipeline that follows upstream changes.
