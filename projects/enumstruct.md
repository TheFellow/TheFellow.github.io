<!-- Generated from https://thefellow.github.io/projects/enumstruct/ by scripts/generate_llm_content.py; do not edit. -->

# enumstruct

Source: [https://thefellow.github.io/projects/enumstruct/](https://thefellow.github.io/projects/enumstruct/)

## Pyramid summary

- **~2 words:** Exhaustive unions
- **~8 words:** A Go analyzer that detects missing pointer-union cases as models evolve.
- **Expanded:** A Go analyzer that makes pointer-union switches exhaustive, catching missing cases as generated models evolve.

## Full content

[View the repository](https://github.com/TheFellow/enumstruct)

enumstruct closes a type-safety gap that appears when a “one of these” value is represented as a struct whose fields are all pointers. GraphQL generators commonly use this shape for union-like inputs. When a generator adds a field, an existing nil-check switch still compiles, even if it silently forgets the new variant.

The analyzer makes that switch exhaustive. Types can opt in through a source annotation or configuration, which also covers generated and imported models. It recognizes real-world nil-check forms, reports duplicate cases, and uses Go analysis facts so declarations retain their identity across package boundaries.

### Why it is worth exploring

- It turns a limitation of generated models into a build-time guarantee without replacing those models.
- Strict and lenient modes make the meaning of a `default` case explicit instead of guessing intent.
- The analyzer is deliberately narrow, making its AST and `go/types` reasoning approachable for readers learning Go static analysis.

Start with `pkg/enumstruct/analyzer.go`, then use the focused cases under `pkg/enumstruct/testdata/src` to see how missing, duplicate, cross-package, suppressed, and alternate nil-check forms are handled.
