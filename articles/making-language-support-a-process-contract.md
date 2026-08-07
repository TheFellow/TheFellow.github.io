<!-- Generated from https://thefellow.github.io/articles/making-language-support-a-process-contract/ by scripts/generate_llm_content.py; do not edit. -->

# Making Language Support a Process Contract

Source: [https://thefellow.github.io/articles/making-language-support-a-process-contract/](https://thefellow.github.io/articles/making-language-support-a-process-contract/)

## Pyramid summary

- **~2 words:** Compiler plugins
- **~8 words:** A bounded process contract keeps language runtimes isolated and evidence complete.
- **Expanded:** How Weave keeps compiler runtimes outside its Go process while the core owns capability negotiation, bounds, validation, freshness, and atomic publication.

## Full content

**Part 2 of [Building Weave](/series/weave.md).**

A semantic index can gain a second language by adding another parser to its core. That approach looks direct until the language's real semantics live behind Roslyn, FSharp.Compiler.Service, CPython, a JVM compiler, or a build system with its own runtime and dependency graph. Reimplementing those semantics in Go would trade compiler truth for one convenient address space. Loading every compiler into that address space would trade isolation for dependency and crash coupling.

[Weave](https://github.com/TheFellow/weave) treats its Go executable like a compiler driver instead. A language adapter is a subordinate process that describes its capabilities, accepts one bounded indexing request, returns complete semantic units, and exits. The wire contract is the extension point; the adapter does not import a Weave Go package, and the core does not load the adapter's runtime.

```sh
weave adapters doctor
weave index --adapter ./my-compiler-adapter --timeout 2m
```

The same [experimental protocol](https://github.com/TheFellow/weave/blob/main/protocol/adapter/v0/README.md) is implemented by the .NET adapter in C# and the Python adapter in Python. That makes language neutrality observable rather than architectural intent.

<figure class="article-figure">
  <img src="/assets/images/articles/weave/adapter-contract.svg" alt="The Weave core first asks an isolated adapter process to describe its capabilities. It then sends a bounded request containing repository context, permissions, and limits. The adapter uses its native compiler runtime and streams complete unit frames. The core stages and validates the full response before publishing semantic units to the graph.">
  <figcaption>The process boundary keeps compiler runtimes isolated. The core retains control of trust, bounds, graph validity, and publication.</figcaption>
</figure>

## Put ownership on the correct side

The process split is useful because each side has a different kind of authority.

| Weave core owns | Adapter owns |
| --- | --- |
| Executable selection and literal arguments | Compiler and build-system APIs |
| Capability and protocol negotiation | Compilation-unit boundaries |
| Repository context and explicit permissions | Semantic facts and fingerprints |
| Deadlines, cancellation, and byte/fact bounds | Toolchain diagnostics |
| Frame order and graph validation | Declared refresh capability |
| Storage, freshness, and atomic publication | No direct database access |

The core cannot decide how F# compilation order affects invalidation without reproducing F# project semantics. The adapter cannot decide when its facts become visible without bypassing the graph's ownership and freshness rules. Keeping those responsibilities separate lets each side enforce the facts it actually knows.

This is why the adapter is a process rather than a Go plugin or shared library. A compiler crash does not corrupt the Go address space. Roslyn, MSBuild, FSharp.Compiler.Service, and CPython can carry the dependency versions their ecosystems require. Another adapter can be written in Rust, Java, Kotlin, TypeScript, or any runtime that can exchange the same bytes.

## Negotiate capabilities before work

Every adapter supports a side-effect-free description command:

```text
<adapter> describe --protocol weave.adapter/v0
```

It writes one strict JSON document and exits. The document names supported protocols, provider identity, languages, operations, refresh modes, fact encoding, position encodings, required executables, and whether indexing may invoke a build tool.

```json
{
  "protocols": ["weave.adapter/v0"],
  "provider": {"name": "weave-python", "version": "..."},
  "languages": ["python"],
  "operations": ["index"],
  "refresh_modes": ["full"],
  "fact_encoding": "weave.facts/v0",
  "position_encodings": ["utf8-byte"],
  "requires": {
    "executables": ["python>=3.9", "git"],
    "may_run_build_tool": false
  }
}
```

Provider identity establishes provenance and inventory ownership; it does not select special behavior in the parser. The core checks capabilities instead. The current `full` refresh mode promises a complete provider-owned inventory on every run. A future `changed-units` mode will need a stronger incremental contract rather than being inferred from a provider name.

Capability discovery also participates in freshness for runtime-backed automatic adapters. `weave-python` includes its implementation, interpreter version, and code digest in the reported provider version. Installing a different Python patch release therefore invalidates the cached inventory even when the repository has not changed.

## Make trust an input, not an assumption

The index request is one JSON document written to stdin. It includes an absolute repository root, stable repository identity, build variant, changed-path hints, a small allowlisted environment, host-selected limits, and explicit permissions:

```json
{
  "permissions": {
    "network": false,
    "restore": false,
    "build_tool": false,
    "run_generators": false
  },
  "limits": {
    "max_frame_bytes": 1048576,
    "max_total_bytes": 33554432,
    "max_frames": 100000,
    "max_facts": 1000000
  }
}
```

A false permission is a prohibition. The core launches argument arrays without a shell, gives the adapter the repository as its working directory, and supplies only selected environment values. The adapter still has to enforce the permissions that apply to its runtime.

The contrast between the first two adapters is useful. Roslyn and FSharp.Compiler.Service require MSBuild project evaluation, so automatic .NET discovery grants build-tool permission while still denying network access, restore, and generators. The Python adapter needs no build permission. It inventories regular Git-visible `.py` files, reads them through CPython's standard library, and never imports repository modules or executes project tooling.

An explicit adapter run can widen those permissions deliberately:

```sh
weave index \
  --adapter ./my-adapter \
  --adapter-arg ./config.json \
  --allow-build-tool \
  --timeout 4m
```

The permission flags describe authority. They do not cause Weave to run a restore, generator, or network operation itself.

## Stream a complete inventory

The adapter's `index` operation reserves stdout for newline-delimited protocol frames. Human diagnostics go to bounded stderr. Every stdout line repeats the protocol and request ID, names a frame kind, and carries its payload.

```text
run.begin
  unit.begin
    facts
    facts
    diagnostic
  unit.end
  unit.begin
    facts
  unit.end
run.end
```

`run.begin` repeats the negotiated provider and fact encoding. Each `unit.begin` declares one atomically replaceable semantic unit. `facts` frames carry documents, symbols, occurrences, and edges in bounded batches. `unit.end` supplies exact counts, and `run.end` supplies the complete duplicate-free unit inventory.

This lifecycle gives the core more than a collection of objects. It gives it a proof of completeness that can be checked mechanically. A unit that began must end. Counts must match. Every fact must name the unit and provider that owns it. The terminal inventory must name exactly the units that completed.

Diagnostics remain part of that structure. An adapter can attach an informational, warning, or error message to a run or unit without putting log text in the fact stream. A process failure and a repository semantic diagnostic are therefore different outcomes.

## Reject incomplete truth before publication

Weave stages and validates the response before it publishes any of it. The host rejects:

- an unsupported protocol, fact encoding, position encoding, operation, or refresh mode;
- unknown fields or frame kinds;
- wrong request IDs or lifecycle order;
- duplicate IDs, unit ownership conflicts, invalid UTF-8, ranges, edges, or evidence;
- count and terminal-inventory mismatches;
- frame, byte, fact, process, or deadline limits;
- missing terminal frames, cancellation, or a nonzero exit.

Previously published facts remain untouched when any of those checks fail. The adapter cannot leave half of a C# solution or Python package looking current merely because it produced several valid frames before the failure.

After a complete response passes protocol and graph validation, a known automatic provider hands its units to the same [freshness lifecycle](/articles/keeping-a-semantic-index-fresh-without-a-daemon.md) as native Go and structured workspace facts. Provider ownership prevents one adapter from deleting another adapter's units. The graph update finishes before the freshness manifest is published, so process completeness and repository freshness form one observable contract.

An explicit `--adapter` run uses the same validation and atomic unit publication, but remains a snapshot import. It does not publish an automatic producer manifest for a process the core does not yet know how to reproduce.

## Preserve evidence across languages

A shared wire shape does not make every language equally static. It gives each adapter one vocabulary for saying how it knows a fact.

The .NET adapter uses Roslyn and MSBuild for exact C# declarations, references, and calls, plus compiler-evaluated project relationships. FSharp.Compiler.Service supplies typed F# definitions and references, while F# call edges remain absent until the compiler-backed implementation can support them. Omitting an edge is more accurate than filling the shape with a guess.

Rust and C++ take a second route through the same contract. `weave-rust` supervises `rust-analyzer scip`, while `weave-cpp` supervises `scip-clang` and passes its output through Weave's bounded SCIP normalizer. Rust-analyzer currently distinguishes resolved definitions and references but not calls, so an occurrence that looks like a call remains a reference. C++ facts are exact for one selected compilation database and Clang version; the adapter refuses zero or multiple discovered databases rather than blending incompatible build variants.

Python makes the distinction sharper. CPython's `symtable` can establish that a name is a local, global, free, or nonlocal lexical binding slot. It cannot establish which object that slot will hold when a call executes. The adapter therefore emits:

| Python fact | Evidence |
| --- | --- |
| Compiler-accepted declarations and lexical references | `exact` |
| Import and dependency statements | `declared` |
| A call spelled through a resolved lexical slot | `syntactic` |
| Dynamic attributes, decorators' effects, and runtime-generated symbols | omitted |

`exact` is scoped to the claim. An exact Python fact says the recorded interpreter made that lexical decision, not that Python's runtime dispatch has become static.

## Let a new language improve the common graph

Python also exposed an assumption that the original graph could not keep. A single Python lexical slot may be assigned, imported, or defined several times. Modeling every statement as a different symbol would lose the compiler's binding decision; storing only one definition would lose real source locations.

Weave now treats `Symbol.Definition` as the canonical display anchor and retains every binding site as a `definition` occurrence. The `definition` query prefers those complete occurrences, with the singular anchor as a fallback for older providers. A capability discovered through the Python adapter improved the language-neutral query model rather than becoming a Python-only output special case.

C++ exposed a different interchange assumption. SCIP permits a producer to repeat the same global `SymbolInformation` in every document that uses it. Weave's C++ import path now retains every occurrence while selecting one canonical symbol fact deterministically, preferring a definition and then stable path and unit order. Equivalent repetitions collapse; conflicting semantic descriptions reject the complete index.

`scip-clang` can also omit a symbol's presentation name or kind even when its canonical SCIP descriptor contains both. The normalizer derives only that presentation from the parsed descriptor instead of leaking a long encoded identity into query output or inventing a semantic relationship. A language adapter should be allowed to expose pressure in the shared representation, then fix that representation at the narrowest truthful boundary.

That is the architectural test an external adapter should create. It may extend the fact vocabulary or reveal a missing invariant, but the resulting semantics belong in the shared graph and protocol. Presentation code should not inspect `provider == "weave-python"` to decide what a definition means.

## Make automatic authority an explicit choice

The core includes conservative automatic profiles for its known adapters. A third-party language can join the same freshness path without adding its executable name or file extensions to Go. The user selects a strict [`weave.adapters/v1` registry](https://github.com/TheFellow/weave/blob/main/internal/adapter/registry.go) with `WEAVE_ADAPTER_CONFIG`; each registration declares a provider name, a literal argv array, Git-visible input extensions and filenames, explicit permissions, and an optional timeout.

The registry is never discovered inside the repository or inferred by scanning `PATH` for a naming convention. Weave resolves the selected file to an absolute path; selecting it is the trust decision. Bare command names receive normal platform executable lookup only after that decision, arguments never pass through a shell, and permissions remain denied unless the registration grants them. The normalized registration and registry path participate in provider identity, so changing execution policy invalidates the appropriate inventory.

That configuration also fails closed. Unknown fields, duplicate or reserved provider names, unsafe inputs, an unavailable command, a capability-name mismatch, or an invalid selected file prevent automatic freshness from claiming a current graph. `weave adapters doctor` makes the same configuration and protocol checks visible before a query needs them.

An arbitrary executable can already be run with `weave index --adapter PATH`. That explicit command validates and atomically publishes its inventory, but it does not yet teach future queries how to rediscover and rerun the executable. Its facts are an imported snapshot until the user runs it again. Automatic discovery of arbitrary PATH entries would need an installation registry and trust policy, not a broader filename convention.

This distinction keeps the extension point open without silently executing a newly installed program inside every repository. The protocol is public; automatic authority remains a user-controlled policy.

## Build against the bytes

The checked-in [`protocol/adapter/v0`](https://github.com/TheFellow/weave/tree/main/protocol/adapter/v0) directory contains a capability document, index request, valid response stream, and deliberately truncated stream. Go contract tests decode those files through the same strict implementation used for real adapters.

An adapter author can work from that small surface:

1. Implement `describe --protocol weave.adapter/v0` and match the capability fixture.
2. Implement `index --protocol weave.adapter/v0`, reading one request through EOF.
3. Emit ordered unit frames and an exact terminal inventory on stdout.
4. Send bounded operator context to stderr.
5. Run the executable explicitly and inspect the normalized result.

```sh
weave index --adapter ./my-adapter --json
weave verify --json
weave export --json
```

No Go helper library is required for conformance. A generated binding or ecosystem SDK may reduce boilerplate later, but the bytes and behavior remain authoritative.

Version zero is intentionally experimental. Its newline JSON framing lets the fact model and failure contract evolve before compatibility is promised. A stable version one is planned around a checked-in protobuf schema with optional generated bindings. A persistent worker mode may eventually reduce compiler startup time, but one-shot execution remains the compatibility floor and correctness cannot depend on a resident process.

That leaves Weave with a narrow center. The core knows how to supervise evidence, validate it, keep it fresh, and query it. Each adapter knows how its language establishes that evidence. Adding a compiler no longer requires pretending every runtime belongs inside one program.
