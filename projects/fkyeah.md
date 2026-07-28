<!-- Generated from https://thefellow.github.io/projects/fkyeah/ by scripts/generate_llm_content.rb; do not edit. -->

# F#kYeah

Source: [https://thefellow.github.io/projects/fkyeah/](https://thefellow.github.io/projects/fkyeah/)

## Pyramid summary

- **~2 words:** Agent pipelines
- **~8 words:** An F# engine executing inspectable, resumable AI workflows from DOT graphs.
- **Expanded:** An F# pipeline engine for multi-stage AI workflows described as executable graphs.

## Full content

[View the repository](https://github.com/TheFellow/fkyeah)

F#kYeah implements the StrongDM Attractor specifications as a DOT-driven pipeline runner. A graph describes stages, transitions, conditions, retries, human gates, and tool execution; the engine runs that graph against multiple LLM providers and checkpoints progress so interrupted workflows can resume.

DOT is a strong fit because it keeps control flow declarative and inspectable. A workflow can be rendered as a diagram, validated before execution, and versioned as text. F# adds a second layer of clarity: discriminated unions and pattern matching are natural tools for representing stage types and execution outcomes that should be handled exhaustively.

### Why it is worth exploring

- It models agent workflows as inspectable programs with explicit control flow.
- Simulation, validation, checkpoints, and conformance tests make workflow behavior testable without spending model tokens on every iteration.
- The unified model client separates pipeline semantics from any single provider.

Start with a small graph under `examples`, use the schema command to understand its attributes, and then follow graph parsing into the execution engine.
