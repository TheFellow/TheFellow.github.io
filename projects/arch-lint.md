<!-- Generated from https://thefellow.github.io/projects/arch-lint/ by scripts/generate_llm_content.py; do not edit. -->

# arch-lint

Source: [https://thefellow.github.io/projects/arch-lint/](https://thefellow.github.io/projects/arch-lint/)

## Pyramid summary

- **~2 words:** Enforced boundaries
- **~8 words:** A Go analyzer that makes architectural dependency rules build-time checks.
- **Expanded:** A Go analyzer that turns architectural dependency rules into build-time checks.

## Full content

[View the repository](https://github.com/TheFellow/arch-lint)

Architecture diagrams and conventions are useful, but they drift when nothing checks them. arch-lint makes package-boundary rules executable: a YAML specification selects packages, forbids dependency patterns, and records narrowly scoped exceptions or exemptions.

Glob captures move arch-lint beyond a simple deny list. A rule can capture the module owning an imported `internal` package, then exempt only the facade, queries, handlers, and implementation packages belonging to that same module. Another capture can keep every concrete presentation surface private to its domain and surface kind without naming CLI, TUI, or GUI individually. The same analyzer can run as a command, through Go's `analysis` framework, or as a golangci-lint module plugin, so the constraint can live in both local feedback and CI.

### Why it is worth exploring

- It demonstrates architecture as an automatically tested property of a repository.
- Its pattern language balances broad rules with explicit, reviewable exceptions.
- It is used by the Mixology modular-monolith sample, showing the rules at work in a real codebase.

Read the configuration schema and matcher first, then see `.arch-lint.yaml` in [go-modular-monolith](https://github.com/TheFellow/go-modular-monolith) for a real rule set.
