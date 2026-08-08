---
title: "Making Language Support a Process Contract"
date: 2026-08-07 01:02:00 -0700
last_modified_at: 2026-08-08 13:10:00 -0700
excerpt: "How Weave keeps compiler runtimes outside its Go process while the core owns capability negotiation, bounds, validation, freshness, and atomic publication."
permalink: /articles/making-language-support-a-process-contract/
series: weave
series_order: 2
order: 6
featured: true
status: "Weave, part 2"
icon: "terminal"
accent: "#b197fc"
topics: ["Compiler adapters", "Process isolation", "Protocols"]
---

{% include series-notice.html %}

A semantic index can gain a second language by adding another parser to its core. That approach looks direct until the language's real semantics live behind Roslyn, FSharp.Compiler.Service, CPython, a JVM compiler, or a build system with its own runtime and dependency graph. Reimplementing those semantics in Go would trade compiler truth for one convenient address space. Loading every compiler into that address space would trade isolation for dependency and crash coupling.

[Weave](https://github.com/TheFellow/weave) treats its Go executable like a compiler driver instead. A language adapter is a subordinate process that describes its capabilities, accepts one bounded indexing request, returns complete semantic units, and exits. The wire contract is the extension point; the adapter does not import a Weave Go package, and the core does not load the adapter's runtime.

```sh
weave adapters doctor
weave index --adapter ./my-compiler-adapter --timeout 2m
```

The same [experimental protocol](https://github.com/TheFellow/weave/blob/main/protocol/adapter/v0/README.md) is implemented directly in C#, Python, and Rust, while small Go bridges supervise compiler-native SCIP producers and Universal Ctags. Language neutrality is observable in running processes rather than left as architectural intent.

<figure class="article-figure">
  <img src="{{ '/assets/images/articles/weave/adapter-contract.svg' | relative_url }}" alt="The Weave core first asks an isolated adapter process to describe its capabilities. It then sends a bounded request containing repository context, permissions, and limits. The adapter uses its native compiler runtime and streams complete unit frames. The core stages and validates the full response before publishing semantic units to the graph.">
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
  },
  "claims": {
    "inputs": {
      "extensions": [".py", ".pyi"],
      "filenames": ["pyproject.toml"]
    },
    "evidence": ["declared", "exact", "syntactic"]
  }
}
```

Provider identity establishes provenance and inventory ownership; it does not select special behavior in the parser. The core checks capabilities instead. Input and evidence claims make applicability routable before execution rather than hiding extension policy behind an executable name. The current `full` refresh mode promises a complete provider-owned inventory on every run. A future `changed-units` mode will need a stronger incremental contract rather than being inferred from a provider name.

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

That authority now travels through one bounded child environment for adapter doctoring, explicit indexing, and automatic freshness. The allowlist carries the selected platform path and home, .NET host and package roots, Java home, Cargo and Rust locations, SCIP executable overrides, and temporary-system paths required by the compiler runtimes. It does not inherit the entire parent environment. One adapter therefore observes the same toolchain inputs regardless of which supported entry point launched it, without receiving unrelated credentials as an accidental convenience.

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

That protocol inventory is richer than the current managed database. Format 4 validates complete adapter output, then retains declaration anchors and high-value navigation relationships while dropping occurrences, statement-level calls and references, fields, constants, and locals. The adapter remains responsible for semantic truth; the storage projection remains responsible for what is practical to keep.

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

After a complete response passes protocol and graph validation, a known automatic provider hands its units to the same [freshness lifecycle](/articles/keeping-a-semantic-index-fresh-without-a-daemon/) as native Go and structured workspace facts. Provider ownership prevents one adapter from deleting another adapter's units. The graph update finishes before the freshness manifest is published, so process completeness and repository freshness form one observable contract.

An explicit `--adapter` run uses the same validation and atomic unit publication, but remains a snapshot import. It does not publish an automatic producer manifest for a process the core does not yet know how to reproduce.

## Preserve evidence across languages

A shared wire shape does not make every language equally static. It gives each adapter one vocabulary for saying how it knows a fact.

The .NET adapter uses Roslyn and MSBuild for exact C# declarations, references, and calls, plus compiler-evaluated project relationships. FSharp.Compiler.Service supplies typed F# definitions and references. Those richer facts remain useful during normalization, but the format-4 worktree index persists declaration anchors and project, import, implementation, and other navigation relationships rather than statement-level events. Omitting unsupported evidence is still more accurate than filling the provider stream with a guess.

Rust and C++ take a second route through the same contract. `weave-rust` supervises `rust-analyzer scip`, while `weave-cpp` supervises `scip-clang` and passes its output through Weave's bounded SCIP normalizer. Rust-analyzer currently distinguishes resolved definitions and references but not calls, so an occurrence that looks like a call remains a reference. C++ facts are exact for one selected compilation database and Clang version; the adapter refuses zero or multiple discovered databases rather than blending incompatible build variants.

Repository-scale Rust validation made the root and ownership rules concrete. The adapter discovers the nearest nested Cargo manifest or `rust-project.json`, runs rust-analyzer at that build root, and rebases its SCIP documents to repository-relative paths. rust-analyzer may repeat one equivalent global symbol record across library, binary, and test documents. The adapter assigns that record to the lexically first document while retaining every occurrence and relationship; conflicting descriptions still reject the run. Per-document line indexes and memoized symbol validation bound coordinate normalization without weakening the imported evidence.

TypeScript, JavaScript, Java, and Kotlin reuse that SCIP boundary with different trust profiles. `weave-typescript` requires an existing root compiler configuration and never invokes a package manager, infers a configuration, or writes into the checkout. `weave-jvm` delegates to `scip-java`, which can run Gradle, Maven, or Bazel and execute build extensions. JVM indexing therefore remains an explicit run with all four grants unless a user-controlled registry deliberately records those powers and a conservative input inventory. Both adapters translate their producers' legacy UTF-16 ranges to Weave's byte coordinates instead of guessing from source encoding metadata.

Python makes the distinction sharper. CPython's `symtable` can establish that a name is a local, global, free, or nonlocal lexical binding slot. It cannot establish which object that slot will hold when a call executes. The adapter therefore emits:

| Python fact | Evidence |
| --- | --- |
| Compiler-accepted declarations and lexical references | `exact` |
| Import and dependency statements | `declared` |
| A call spelled through a resolved lexical slot | `syntactic` |
| Dynamic attributes, decorators' effects, and runtime-generated symbols | omitted |

`exact` is scoped to the claim. An exact Python fact says the recorded interpreter made that lexical decision, not that Python's runtime dispatch has become static.

The Universal Ctags adapter makes the lower boundary equally explicit. It emits documents, symbols, and definition occurrences as `syntactic` evidence for a broad collection of languages and formats. References, calls, inheritance, and other relationships are absent. It is an explicit enrichment provider, not an automatic replacement for a compiler-backed adapter.

## Let a new language improve the common graph

Python also exposed an assumption that the original graph could not keep. A single Python lexical slot may be assigned, imported, or defined several times. Modeling every statement as a different symbol would lose the compiler's binding decision; storing only one definition would lose real source locations.

Weave treats `Symbol.Definition` as the canonical retained declaration anchor. Providers may emit repeated binding occurrences, but format 4 omits occurrence rows and `definition` points to the retained anchor. The Python experiment still improved the language-neutral fact model; the practical projection now makes the narrower query contract explicit.

C++ exposed a different interchange assumption. SCIP permits a producer to repeat the same global `SymbolInformation` in every document that uses it. Weave's C++ import path now retains every occurrence while selecting one canonical symbol fact deterministically, preferring a definition and then stable path and unit order. Equivalent repetitions collapse; conflicting semantic descriptions reject the complete index.

`scip-clang` can also omit a symbol's presentation name or kind even when its canonical SCIP descriptor contains both. The normalizer derives only that presentation from the parsed descriptor instead of leaking a long encoded identity into query output or inventing a semantic relationship. A language adapter should be allowed to expose pressure in the shared representation, then fix that representation at the narrowest truthful boundary.

That is the architectural test an external adapter should create. It may extend the fact vocabulary or reveal a missing invariant, but the resulting semantics belong in the shared graph and protocol. Presentation code should not inspect `provider == "weave-python"` to decide what a definition means.

## Keep enrichment additive

Every completed run may replace only facts owned by its provider. The host now rejects a document, symbol, occurrence, or edge whose provider differs from the enclosing unit and run. A broad syntactic adapter therefore cannot relabel compiler facts, and a compiler upgrade cannot delete document relationships owned by the workspace provider.

Owning an edge does not imply owning either endpoint. A precise compiler relationship, a syntactic outline, a generated-schema bridge, and a declared human relationship can connect the same graph without one provider calling another or writing storage directly. The core unions those observations while retaining provider and evidence. Any future reconciliation must add its own evidenced relationship rather than silently merging identities or promoting a heuristic to compiler truth.

## Make automatic authority an explicit choice

The core includes conservative automatic profiles for known adapters whose query-time permissions are bounded. TypeScript activates only for a root `tsconfig.json` or `jsconfig.json` and fingerprints every Git-visible input rather than guessing through a monorepo. A third-party language or a more powerful JVM build can join the same freshness path without adding its executable name or file extensions to Go.

There are three explicit routes. `weave adapters install` copies a user-selected local executable into private platform state and pins both its artifact bytes and normalized capability document. Known companion environment variables preserve deliberate executable overrides with fixed compatibility claims. `WEAVE_ADAPTER_CONFIG` selects a strict [`weave.adapters/v1` registry](https://github.com/TheFellow/weave/blob/main/internal/adapter/registry.go) whose entries declare a literal argv array, capability digest, input and evidence claims, permissions, and timeout. Same-name precedence is registry, environment, then managed state; overlapping claims across different providers fail instead of becoming an ordering rule.

None of these routes is discovered inside the repository or inferred by scanning `PATH`. Arguments never pass through a shell, and permissions remain denied unless the installation or registration grants them. Concrete Git-visible paths expose precise ownership conflicts before execution. A broad syntactic fallback receives an exact `input_paths` allowlist containing only paths not claimed by the built-in Go provider or a precise external adapter; the host rejects fallback documents outside it. The artifact and capability pins participate in freshness, so changing executable bytes, provider identity, public claims, or execution policy prevents the previous inventory from being called current.

That policy also stays inspectable. `weave adapters list` reads metadata without executing adapters. `weave adapters doctor` verifies integrity and performs bounded capability negotiation without indexing. An arbitrary `weave index --adapter PATH` remains a deliberate snapshot import, while `weave adapters install PATH` is the separate action that grants reproducible automatic authority.

[The managed lifecycle](/articles/managing-compiler-adapters-without-inventing-a-package-registry/) keeps the extension point open without silently executing a newly available program in every repository. The protocol is public; automatic authority remains a user-controlled policy.

## Pressure-test the complete process

Protocol fixtures prove framing, bounds, and atomic publication. They do not prove that a real repository places its solution at the checkout root, avoids SDK-generated documents outside that root, lists every buildable project in one solution, or emits each global SCIP symbol once.

The [cross-repository indexing soak](/articles/turning-cross-repository-soaks-into-indexing-contracts/) therefore exercises the complete process across Go, C#, F#, Rust, and structured content. Each isolated clone is prepared before timing; the candidate then indexes offline, answers current queries, verifies, exports, and proves the original source status unchanged. Failures corrected nearest-root discovery, project de-duplication, F# restore policy, generated-document handling, Rust symbol ownership, environment consistency, and memory accounting before the full twelve-repository matrix passed.

That matrix is not a claim that every language or repository is covered. It is retained evidence that the protocol, compiler adapters, graph publication, and storage verifier compose under pinned real inputs. A future optimization must preserve those complete results rather than merely making an adapter process exit faster.

## Package the bridge without hiding the runtime

The process boundary also makes distribution honest. The release configuration can ship the pure-Go C++, TypeScript, JVM, and Universal Ctags bridges together for macOS, Linux, and Windows on amd64 and arm64. Those small executables still report their external requirements: `scip-clang`, Node plus `scip-typescript`, Java plus `scip-java`, or Universal Ctags remain explicit installations.

The other runtimes keep their native delivery shapes. .NET uses self-contained companion archives, Python uses a wheel, and Rust waits for a reproducible native target matrix. A bundle name is convenience, not evidence that the language toolchain is embedded or trusted. `describe` stays side-effect free when the producer is absent, and `weave adapters doctor` reports the missing requirement.

Release construction is another validated boundary. GoReleaser derives binary and archive timestamps from the commit, emits an SPDX JSON SBOM beside every core and bridge archive, and hashes the archives, SBOMs, .NET companions, and Python wheel into one SHA-256 inventory. A repository-owned verifier reads GoReleaser's artifact manifest, inspects archives without extracting them, rejects unsafe or unexpected paths and modes, checks the complete six-platform matrix and SPDX document shape, and recomputes every listed digest.

A tag starts with a private draft release. The workflow validates the exact local artifacts, uses GitHub's keyless provenance to attest every checksum-listed subject, and only then makes the draft public. These early binaries remain explicitly unsigned at the operating-system layer. Provenance does not substitute for Apple notarization or Windows code signing, and package-manager distribution can wait until those platform commitments are deliberate.

## Cache dependencies without caching authority

An open process boundary creates a wide validation matrix. Every bridge has its own runtime, producer, operating-system coverage, and real indexing smoke test. Weave keeps path filters around those workflows so an unrelated change does not start them, then gives each workflow and pull request or ref its own concurrency group. A newer commit cancels only the obsolete run for that boundary. Another pull request remains independent.

The caches follow the same ownership rule as the graph. Go modules, Python packages, npm packages, NuGet packages, Gradle dependencies, and Cargo dependencies are replaceable inputs. They can be restored from ecosystem-aware caches without becoming declarations about what Weave supports. The .NET workflows commit `packages*.lock.json`, place NuGet packages inside the workspace, restore the solution, fixtures, package build, and release build in locked mode, then build without restoring again. A test module initializer registers MSBuild before FSharp.Compiler.Service or compiler test code can be loaded by the JIT, keeping that cached restore compatible with deterministic compiler startup.

The larger SCIP producers get a narrower cache. `scip-clang` and `scip-java` are already selected by checksum-pinned installer scripts, so their cache keys include the runner operating system, architecture, and installer-script digest. A hit avoids another download; a changed pin selects different bytes. Rust pins its cache action and lets pull requests restore while only `main` saves. `cargo package` writes into a runner-temporary target directory so its packaging output cannot enter the shared workspace cache. Gradle uses its open-source basic cache provider with the same write boundary. Neither path caches failed work or treats Weave's own workspace output as a reusable authority.

The core semantic workflow may restore `.git/weave` by a content-derived key, but that index remains disposable. `weave ci index` still brings it current and `weave ci check` still verifies the graph and architecture policy. SARIF and the deterministic JSON export are written under the runner's temporary directory and uploaded from there, so validation outputs cannot become new worktree inputs or perturb a later Git observation. Credentials, mutable managed-adapter state, and checked-in declarations stay outside these caches. Runner conservation changes validation latency, not the evidence being validated.

## Build against the bytes

The checked-in [`protocol/adapter/v0`](https://github.com/TheFellow/weave/tree/main/protocol/adapter/v0) directory contains a capability document, index request, valid response stream, deliberately truncated stream, and a language-neutral conformance corpus. Go contract tests decode the base files through the same strict implementation used for real adapters, while `weave adapters conformance` exercises an opaque executable against a genuine caller-supplied fixture.

An adapter author can work from that small surface:

1. Implement `describe --protocol weave.adapter/v0` and match the capability fixture.
2. Implement `index --protocol weave.adapter/v0`, reading one request through EOF.
3. Emit ordered unit frames and an exact terminal inventory on stdout.
4. Send bounded operator context to stderr.
5. Run the executable explicitly, then run the black-box conformance suite.

```sh
weave index --adapter ./my-adapter --json
weave adapters conformance ./my-adapter --fixture ./my-fixture --json
weave verify --json
weave export --json
```

The conformance runner checks describe negotiation, malformed and wrong-protocol rejection, a real fixture index, deterministic replay, host bounds, and process failure behavior. No Go helper library is required. A generated binding or ecosystem SDK may reduce boilerplate later, but the bytes and behavior remain authoritative.

Version zero is intentionally experimental. Its newline JSON framing lets the fact model and failure contract evolve before compatibility is promised. A stable version one will still require explicit compatibility rules and a durable wire specification, but it already has language-neutral fixtures and a reusable executable conformance suite. It is not required to use protobuf merely because the process model resembles `protoc`. A persistent worker mode may eventually reduce compiler startup time, but one-shot execution remains the compatibility floor and correctness cannot depend on a resident process.

That leaves Weave with a narrow center. The core knows how to supervise evidence, validate it, keep it fresh, and query it. Each adapter knows how its language establishes that evidence. Adding a compiler no longer requires pretending every runtime belongs inside one program.
