---
title: "ValueTypes"
excerpt: "A small C# library for expressing structural equality in domain-driven value objects."
language: "C#"
license: "MIT"
repository_url: "https://github.com/TheFellow/ValueTypes"
---

<div class="project-meta"><span>C#</span><span>Domain-driven design</span><span>MIT</span></div>

[View the repository](https://github.com/TheFellow/ValueTypes){: .btn .btn--primary }

ValueTypes tackles a deceptively important modeling problem: two domain values should be equal because their meaningful components are equal, not because they happen to be the same object. The library makes that intent explicit without forcing every type to repeat equality and hashing boilerplate.

The most interesting part is the vocabulary it develops for different kinds of composition. `Yield` captures ordered components, `Group` captures components whose order should not matter, and sequence helpers let nested values retain the right equality semantics. A line segment, a roll call, and a wallet do not mean “same” in quite the same way; the API makes those differences visible in the model.

### Why it is worth exploring

- It is a compact example of turning a domain concept into a reusable type-level abstraction.
- Its examples show why collection ordering is part of semantics, not merely an implementation detail.
- The small surface area makes it approachable for readers learning value objects or structural equality.

Start with the repository's `Value` and `ValueBase` types, then follow the tests for `Yield`, `Group`, `AsValues`, and `AsGroup`.

