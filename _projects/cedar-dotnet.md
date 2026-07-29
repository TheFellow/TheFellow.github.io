---
title: "cedar-dotnet"
date: 2026-07-23 12:03:42 -0700
last_modified_at: 2026-07-24 15:15:38 -0700
excerpt: "A C# implementation of the Cedar policy language and authorization model."
language: "C#"
license: "Apache-2.0"
repository_url: "https://github.com/TheFellow/cedar-dotnet"
last_updated: 2026-06-01
order: 20
icon: "shield"
accent: "#b197fc"
topics: ["Authorization", "Language tooling"]
---

<div class="project-meta"><span>C#</span><span>Authorization</span><span>Cedar</span><span>Apache-2.0</span><span>Updated {{ page.last_updated | date: "%B %-d, %Y" }}</span></div>

[View the repository](https://github.com/TheFellow/cedar-dotnet){: .btn .btn--primary }

cedar-dotnet is a full semantic port of Cedar's policy language and authorization model into the .NET ecosystem. Applications can parse policies, construct them through an AST, load entity graphs, and evaluate authorization requests entirely in C#.

Keeping policy separate from application code gives the project much of its practical value. Permissions become independently readable and auditable data while the application supplies principals, actions, resources, and context. The AST-building API also gives strongly typed code a route to generate policies without assembling policy text by hand.

### Why it is worth exploring

- It shows how to port behavior across language ecosystems while preserving the source model's semantics.
- The parser, AST, evaluator, entity graph, and diagnostics form a substantial language-tooling case study.
- It offers .NET applications an authorization approach that keeps policy decisions out of business-logic conditionals.

The quickest path through the code is the README authorization example, followed by the policy parser and authorization engine under `src`.
