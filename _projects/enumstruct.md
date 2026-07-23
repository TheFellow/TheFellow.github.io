---
title: "enumstruct"
excerpt: "A Go analyzer that makes pointer-union switches exhaustive, catching missing cases as generated models evolve."
language: "Go"
license: "MIT"
repository_url: "https://github.com/TheFellow/enumstruct"
order: 45
featured: true
icon: "exhaustive"
accent: "#ffd43b"
topics: ["Static analysis", "Exhaustiveness", "GraphQL"]
---

<div class="project-meta"><span>Go</span><span>Static analysis</span><span>GraphQL</span><span>MIT</span></div>

[View the repository](https://github.com/TheFellow/enumstruct){: .btn .btn--primary }

enumstruct closes a type-safety gap that appears when a “one of these” value is represented as a struct whose fields are all pointers. GraphQL generators commonly use this shape for union-like inputs. When a generator adds a field, an existing nil-check switch still compiles—even if it silently forgets the new variant.

The analyzer makes that switch exhaustive. Types can opt in through a source annotation or configuration, which also covers generated and imported models. It recognizes real-world nil-check forms, reports duplicate cases, and uses Go analysis facts to carry declarations across package boundaries rather than matching fields by name.

### Why it is worth exploring

- It turns a limitation of generated models into a build-time guarantee without replacing those models.
- Strict and lenient modes make the meaning of a `default` case explicit instead of guessing intent.
- The analyzer is deliberately narrow, making its AST and `go/types` reasoning approachable for readers learning Go static analysis.

Start with `pkg/enumstruct/analyzer.go`, then use the focused cases under `pkg/enumstruct/testdata/src` to see how missing, duplicate, cross-package, suppressed, and alternate nil-check forms are handled.

