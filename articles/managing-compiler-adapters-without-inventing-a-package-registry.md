<!-- Generated from https://thefellow.github.io/articles/managing-compiler-adapters-without-inventing-a-package-registry/ by scripts/generate_llm_content.py; do not edit. -->

# Managing Compiler Adapters Without Inventing a Package Registry

Source: [https://thefellow.github.io/articles/managing-compiler-adapters-without-inventing-a-package-registry/](https://thefellow.github.io/articles/managing-compiler-adapters-without-inventing-a-package-registry/)

## Pyramid summary

- **~2 words:** Managed local adapters
- **~8 words:** Pinned artifacts, capability claims, deterministic routing, and black-box conformance make local adapters safely automatic.
- **Expanded:** How Weave turns an explicitly selected local adapter executable into pinned, routable automatic language support with no remote registry, ambient discovery, or hidden trust expansion.

## Full content

**Part 10 of [Building Weave](/series/weave.md).**

The [adapter process contract](/articles/making-language-support-a-process-contract.md) makes language support open without pulling every compiler runtime into Weave's Go process. An executable can describe itself, accept one bounded indexing request, emit a complete inventory, and exit. That is enough for an explicit run. It is not yet enough to let every future query execute the adapter automatically.

Automatic execution needs durable answers to harder questions. Which local artifact did the user trust? What repository inputs may it claim? What evidence can it produce? Did its bytes or public contract change? What happens when two adapters both claim the same file? A filename convention or a scan of `PATH` cannot answer any of them safely.

[Weave](https://github.com/TheFellow/weave) adds a deliberately local adapter lifecycle instead. The user selects one existing executable. Weave copies it into private platform state, records normalized capabilities and two content digests, and routes Git-visible inputs only through non-overlapping claims. A metadata-only list, bounded doctor, and language-neutral conformance runner make each layer observable. There is no download command, remote catalog, archive extraction, package-manager invocation, or repository-local executable discovery hiding inside the convenience.

<figure class="article-figure">
  <img src="/assets/images/articles/weave/managed-adapter-lifecycle.svg" alt="An explicitly selected regular local adapter executable is copied into Weave's private platform state and asked for its side-effect-free capability document. Weave normalizes input and evidence claims, then atomically records artifact and capability SHA-256 digests in a locked manifest. For automatic indexing, registry, environment, and managed policy merge with fixed precedence, conflicting claims fail closed, concrete Git-visible paths route to one precise or fallback owner, and both artifact and capability identity are checked before the existing bounded index protocol runs. Separate list, doctor, and conformance commands expose metadata, integrity and negotiation, and black-box fixture behavior without creating a remote package registry.">
  <figcaption>Installation records a local trust decision. Routing and integrity checks preserve it every time the adapter becomes automatic.</figcaption>
</figure>

## Separate an open protocol from automatic authority

The subprocess ABI remains the public extension point. Any runtime can implement `weave.adapter/v0`, and an explicit `weave index --adapter` invocation can validate and publish its output without a Go SDK. That operation is intentionally one-shot: choosing an executable for one command does not grant it authority over every matching repository opened later.

The managed lifecycle turns a second, explicit action into that durable policy:

```sh
weave adapters install ./weave-example
weave adapters list
weave adapters doctor
weave adapters update example-provider ./weave-example-next
weave adapters remove example-provider
```

Install accepts a local regular non-symlink, relocatable single-file executable. It does not resolve a package name or fetch bytes. Weave stages a private executable copy, runs the side-effect-free `describe` negotiation against that candidate, and takes the provider name from the returned contract rather than the source filename. Optional literal arguments, indexing permissions, and a timeout become part of the managed installation.

This is closer to linking a known local toolchain than installing from an app store. A language ecosystem can still use `go install`, Cargo, `dotnet publish`, or its own release process to produce a relocatable artifact. A launcher that depends on an existing Python or other managed environment remains an explicit environment selection instead of being copied away from its runtime. Weave starts where executable authority already exists and refuses to pretend it has a remote publisher, update channel, signature policy, or sandbox that it has not actually built.

## Let adapters declare routable claims

Provider names establish provenance. They should not be a hidden table of file extensions in the core. The capability document therefore gains normalized claims alongside its languages, operations, encodings, and runtime requirements:

```json
{
  "claims": {
    "inputs": {
      "extensions": [".fixture"],
      "project_markers": ["fixture.project"]
    },
    "evidence": ["exact"]
  }
}
```

Inputs may name extensions, exact filenames, and project-marker basenames. Markers activate an adapter for a repository; extensions and filenames identify the concrete Git-visible paths it may own. Evidence claims use the graph's existing vocabulary, including `exact`, `declared`, `generated`, `inferred`, `syntactic`, and `ambiguous`. A broad enrichment adapter can identify itself as a fallback so a precise compiler-backed owner wins when both apply. An adapter whose compiler can consume arbitrary repository files may separately request all-file invalidation without claiming ownership of every path.

Weave lowercases, sorts, deduplicates, bounds, and validates the claims before using them. The same normalization feeds their digest. Reordering equivalent arrays cannot create false drift, while adding an extension, evidence class, executable requirement, language, provider version, or other public capability changes the pinned contract.

The important design move is that discovery remains declarative. Weave can decide whether an adapter applies before executing it. It never has to launch every command on `PATH` and ask each one whether it feels relevant to the current checkout.

## Pin the artifact and the contract separately

One digest answers whether the managed executable bytes changed. Another answers whether its normalized `describe` document changed. They protect different promises.

The artifact SHA-256 detects replacement, corruption, or an unexpected edit to the private executable. The capability SHA-256 binds automatic routing to the provider identity and claims the user installed. A tool whose bytes legitimately change during an upgrade will receive a new artifact digest. A tool that starts claiming more inputs or powers receives a new capability digest even if the host would otherwise be able to run it.

The manifest stores both digests, the complete normalized capabilities, literal arguments, permissions, timeout, and a relative private artifact path. It is strict, bounded, sorted, and held under a small bbolt writer lock. Publication uses a synced temporary file and atomic rename, with a previous-file recovery step for an interrupted Windows-style replacement. Install and update finish the candidate negotiation before replacing the manifest; remove publishes the smaller manifest before deleting the no-longer-referenced artifact.

At startup, Weave reads that metadata and verifies the artifact without executing it. Automatic refresh verifies the bytes again immediately before use, performs a bounded `describe`, and compares the provider and capability digest. Artifact damage, provider drift, claim drift, or malformed state becomes a freshness configuration error. The previous graph cannot be called current by silently running a different authority.

## Route ownership before launching a compiler

Managed installations, explicit companion environment paths, and the selected `WEAVE_ADAPTER_CONFIG` registry share one registration model. Same-name precedence is deliberate and fixed: registry over environment over managed state. An environment override retains bounded compatibility claims for its known companion and checks them against negotiation on every refresh. None of the three sources can use ordering to hide overlap between different providers.

An external registry entry is not allowed to make an unpinned command automatic. Its first `weave adapters doctor --json` probe reports the observed capability digest while preserving the integrity error. The user must copy that exact digest into the selected registration before freshness can execute it. Inspection helps construct policy; it does not silently approve the observed executable.

Weave rejects two precise adapters that claim the same extension or filename. At repository time it resolves those claims against the concrete Git-visible inventory and names the exact path when a dynamic conflict remains. Multiple fallback owners for the same path also fail instead of running both and hoping their facts reconcile later.

Every precise adapter receives its routed paths. A fallback receives only the paths left unclaimed by the built-in Go provider and precise external adapters. The host includes that exact `input_paths` allowlist in the index request. Ctags restricts its private snapshot to the allowlist, and protocol validation rejects any fallback document emitted outside it. A full-refresh fallback can therefore return a complete inventory for its assigned slice of a polyglot repository without duplicating compiler-owned files.

Project markers answer activation, not ownership. A `Cargo.toml`, solution file, or compiler configuration can make an adapter eligible without becoming a file that two semantic providers must both own. The routed paths then drive the same input fingerprints, bounded adapter request, staged validation, and atomic graph publication already used by known bridges.

This removes another ambient behavior: an executable merely appearing on `PATH` no longer makes it an automatic repository provider. Legacy environment variables remain explicit choices, and managed or configured adapters carry the claims necessary for deterministic routing.

## Make inspection cheaper than execution

An adapter manager should not require running every compiler to answer a list command. `weave adapters list` therefore reads metadata without negotiating or indexing. It can be used in scripts and diagnostics without starting build tools.

`weave adapters doctor` is the deliberate active probe. It verifies artifact integrity, evaluates current-worktree activation and claim conflicts, runs bounded capability negotiation, compares the pinned provider and capability digest, and resolves named external requirements. Doctor does not issue an index request, build a project, restore dependencies, install another tool, or grant network access. Its scope is the contract that automatic routing would rely on later.

Updates are equally explicit. The user names an installed provider and supplies a replacement local executable. Weave stages and describes the replacement, requires the provider name to remain the requested one, and atomically advances both pins. Existing literal arguments, permissions, and timeout remain in force unless replacement flags are supplied explicitly. A mutable handshake can reveal drift; it cannot silently bless it.

## Test the bytes, not a favored implementation language

The protocol can be language-neutral only if its compatibility test is language-neutral too. Weave ships a checked-in conformance corpus with a tiny genuine repository, malformed inputs, expected case names, and a reference Python executable that imports no Weave implementation package.

```sh
weave adapters conformance ./my-adapter \
  --fixture ./my-genuine-fixture \
  --json
```

The runner treats the candidate as opaque. It checks capability negotiation, wrong-protocol rejection, malformed-request rejection, one genuine fixture index, deterministic replay of normalized units, stderr separation, permissions, bounded host output, and process failure semantics. A third-party adapter can bring the smallest repository that exercises its real compiler while reusing the same executable boundary and machine-readable report.

That distinction matters more than publishing a convenience SDK. Shared helper code can accidentally make a Go implementation and its Go tests agree about the same bug. A black-box runner asks whether the executable accepts and emits the documented bytes, exits correctly, remains deterministic, and obeys host bounds.

The result is an ecosystem boundary with no invented ecosystem service. Weave can trust, route, diagnose, update, remove, and test a local adapter while keeping acquisition and publishing outside the promise. If a real remote catalog, signing policy, or runtime sandbox arrives later, it can extend this foundation. It does not need to be simulated today by scanning names and calling that discovery.
