<!-- Generated from https://thefellow.github.io/articles/weave-language-adapters/ by scripts/generate_llm_content.py; do not edit. -->

# Language Adapters Share One Navigation Contract

Source: [https://thefellow.github.io/articles/weave-language-adapters/](https://thefellow.github.io/articles/weave-language-adapters/)

## Pyramid summary

- **~2 words:** Language adapters
- **~8 words:** Bounded processes emit one validated navigation profile.
- **Expanded:** Compiler-backed adapters project bounded facts into the same format-5 profile.

## Full content

**Part 3 of [Building Weave](/series/weave.md).**

Weave treats language support as a process contract. An adapter reads a bounded request and emits validated `navigation-v1` facts over framed standard input and output.

![Language tools converging on one adapter contract](/assets/images/articles/weave/adapter-contract.svg)

The boundary lets a language tool use its own compiler without moving that compiler into Weave. Weave validates framing, limits, identities, paths, source ranges, edge kinds, and the advertised capability digest before publication.

The adapter registry records explicit commands and input routing. Managed adapters add pinned artifacts and lifecycle commands, but do not invent a package registry. Cross-repository soak fixtures check the contract against real repository shapes before support is advertised.

The built-in Go provider and external adapters therefore produce the same small navigation model. Query behavior does not depend on which compiler produced the facts.

[Continue to progressive discovery](/articles/weave-progressive-discovery.md)
