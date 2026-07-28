<!-- Generated from https://thefellow.github.io/projects/cedar-dotnet/ by scripts/generate_llm_content.py; do not edit. -->

# cedar-dotnet

Source: [https://thefellow.github.io/projects/cedar-dotnet/](https://thefellow.github.io/projects/cedar-dotnet/)

## Pyramid summary

- **~2 words:** Cedar for .NET
- **~8 words:** A semantic Cedar implementation with idiomatic C# APIs and conformance tests.
- **Expanded:** A C# implementation of the Cedar policy language and authorization model.

## Full content

[View the repository](https://github.com/TheFellow/cedar-dotnet)

cedar-dotnet is a full semantic port of Cedar's policy language and authorization model into the .NET ecosystem. Applications can parse policies, construct them through an AST, load entity graphs, and evaluate authorization requests entirely in C#.

Keeping policy separate from application code gives the project much of its practical value. Permissions become independently readable and auditable data while the application supplies principals, actions, resources, and context. The AST-building API also gives strongly typed code a route to generate policies without assembling policy text by hand.

### Why it is worth exploring

- It shows how to port behavior across language ecosystems while preserving the source model's semantics.
- The parser, AST, evaluator, entity graph, and diagnostics form a substantial language-tooling case study.
- It offers .NET applications an authorization approach that keeps policy decisions out of business-logic conditionals.

The quickest path through the code is the README authorization example, followed by the policy parser and authorization engine under `src`.
