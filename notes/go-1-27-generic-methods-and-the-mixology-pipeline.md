<!-- Generated from https://thefellow.github.io/notes/go-1-27-generic-methods-and-the-mixology-pipeline/ by scripts/generate_llm_content.py; do not edit. -->

# Go 1.27 Generic Methods and the Mixology Pipeline

Source: [https://thefellow.github.io/notes/go-1-27-generic-methods-and-the-mixology-pipeline/](https://thefellow.github.io/notes/go-1-27-generic-methods-and-the-mixology-pipeline/)

## Pyramid summary

- **~2 words:** Generic pipeline
- **~8 words:** Go 1.27 generic methods simplify Mixology's typed middleware calls.
- **Expanded:** How generic methods let Mixology put typed middleware operations on the pipeline they configure.

## Full content

[Mixology](https://github.com/TheFellow/go-modular-monolith) now requires Go 1.27. The practical reason for the migration is small but pervasive: generic methods let the middleware API express operations on the `Pipeline` value that actually owns them.

Before Go 1.27, the typed entry points had to be package-level generic functions. A command also used a specification value to carry the operation's load and handle stages:

```go
return middleware.RunCommand(m.pipeline, ctx, middleware.CommandSpec[Input, Output]{
	Action: authz.ActionCreate,
	Load:   func(*middleware.Context) (Input, error) { return input, nil },
	Handle: m.commands.Create,
})
```

With generic methods, the common case reads as an operation performed by the configured pipeline:

```go
return m.pipeline.Command(ctx, authz.ActionCreate, input, m.commands.Create)
```

The same change applies across queries, authorized pages, and commands that load trusted state inside the transaction. `Pipeline.Query`, `Pipeline.QueryResource`, `Pipeline.PageQuery`, `Pipeline.Command`, `Pipeline.LoadCommand`, and `Pipeline.LoadCommandActions` name those cases directly, while Go infers their request and result types from the arguments.

This is an ergonomics improvement, not a different middleware model. Commands still authorize the input and result, run inside the unit of work, dispatch transactional events, and record audit activity. Page queries still omit denied rows without shortening a visible page. The API now makes the pipeline the obvious starting point and removes wrappers that existed largely because the language could not attach fresh type parameters to its methods.

The result is less ceremony at every domain facade and a smaller gap between reading an operation and understanding which pipeline executes it. The [migration commit](https://github.com/TheFellow/go-modular-monolith/commit/507572d8d66109636d2e8aaba99e32c1748aa9d9) shows the change across the complete application, and the [middleware guide](https://github.com/TheFellow/go-modular-monolith/blob/main/pkg/middleware/README.md#typed-pipeline-operations) documents the resulting API.
