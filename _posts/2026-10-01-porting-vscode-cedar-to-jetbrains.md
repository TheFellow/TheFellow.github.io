---
title: "Porting the Cedar VS Code Extension to JetBrains IDEs"
date: 2026-10-01 11:30:00 -0700
last_modified_at: 2026-10-01 11:30:00 -0700
permalink: /notes/porting-vscode-cedar-to-jetbrains/
excerpt: "How jetbrains-cedar brings the official Cedar VS Code extension to IntelliJ-based IDEs by running the Cedar SDK as WebAssembly and porting the extension near line for line."
icon: "shield"
accent: "#845ef7"
tags: ["Cedar", "Kotlin", "Semantic porting", "Developer tools"]
---

The official [Cedar extension for Visual Studio Code](https://github.com/cedar-policy/vscode-cedar) gives policy authors highlighting, validation, formatting, and navigation. [jetbrains-cedar](https://github.com/TheFellow/jetbrains-cedar) is my semantic port of that extension to IntelliJ-based IDEs: GoLand, IntelliJ IDEA, PyCharm, WebStorm, and the rest of the family. It tracks vscode-cedar 0.10.6 with Cedar SDK 4.13.0, and the current release is 0.10.6.1.

The plugin covers the same ground as the extension. Policies, schemas, and entities files get highlighting and validate as you edit, including validation of policies and entities against a detected schema. Formatting, completion, signature help, hover, quick fixes, **Go to Declaration**, the Structure view, and folding all work. Schemas translate between the Cedar and JSON formats, policies export to JSON, and `cedar` fenced code blocks in Markdown are highlighted.

## Run the same Cedar SDK

Most of the extension's behavior comes from the Cedar SDK itself. vscode-cedar compiles a small Rust crate to WebAssembly and calls it from TypeScript for validation, formatting, and schema translation. Reimplementing those in Kotlin would create a second Cedar implementation for an editor plugin, which is the wrong place for one.

The plugin instead runs the same Rust code as WebAssembly inside the JVM on [Chicory](https://chicory.dev), a pure-Java WebAssembly runtime. The modules under `cedar-wasm/src/` are upstream's modules, kept close enough that SDK upgrades port mechanically. The one structural change is the boundary: upstream exposes each function through wasm-bindgen, while the JVM bridge has a single export that takes a JSON request such as `{"fn": "...", "args": [...]}` and returns the upstream result struct serialized as JSON.

That keeps the plugin free of native binaries and gives it the same diagnostics and formatting output as the VS Code extension and the `cedar` CLI.

## Port the extension near line for line

When I ported [Cedar's Go implementation to .NET]({{ '/notes/porting-cedar-semantics-from-go-to-dotnet/' | relative_url }}), a direct transliteration would have preserved the wrong things; the C# API needed to be idiomatic. The extension is a different case. Its TypeScript modules are editor logic: scanning documents, building completions, mapping SDK errors to ranges. Keeping the Kotlin structurally close to them makes every later upstream commit easier to port and review.

To make that possible, the plugin includes a small re-creation of the VS Code API types the extension uses: `Position`, `Range`, `TextDocument`, `Diagnostic`, `CompletionItem`, and a few others. Each upstream `src/*.ts` file has a matching Kotlin file in `core/`, with the same function names, comments, TODOs, and order. Here is upstream's policy formatter:

```typescript
export const formatCedarDoc = (
  cedarDoc: vscode.TextDocument
): string | null => {
  let formattedPolicy = null;
  const { skipFormatting } = scanLeadingComments(cedarDoc);

  if (!skipFormatting) {
    const editorConfig = vscode.workspace.getConfiguration('editor', {
      languageId: 'cedar',
    });
    const tabSize = editorConfig.get<number>('tabSize', 2);
    const wordWrapColumn = editorConfig.get<number>('wordWrapColumn', 80);

    const formatResult: cedar.FormatPoliciesResult = cedar.formatPolicies(
      cedarDoc.getText(),
      wordWrapColumn,
      tabSize
    );
    if (formatResult.success) {
      formattedPolicy = formatResult.policy as string;
    }
    formatResult.free();
  }

  return formattedPolicy;
};
```

And the port:

```kotlin
fun formatCedarDoc(
    cedarDoc: TextDocument,
    tabSize: Int = 4,
    wordWrapColumn: Int = 80,
): String? {
    var formattedPolicy: String? = null
    val (_, skipFormatting) = scanLeadingComments(cedarDoc)

    if (!skipFormatting) {
        val formatResult = Cedar.formatPolicies(
            cedarDoc.getText(),
            wordWrapColumn,
            tabSize,
        )
        if (formatResult.success) {
            formattedPolicy = formatResult.policy
        }
    }

    return formattedPolicy
}
```

The editor configuration lookup becomes parameters supplied by the IntelliJ Cedar code style, and the manual `free()` disappears because results arrive as JSON. Everything else lines up, so a reviewer can read the two side by side.

The IntelliJ integration lives in a separate `ide/` layer. It adapts IntelliJ documents and projects to the shim types and wires the ported functions into the platform's own extension points: an annotator and the Problems tool window for diagnostics, a formatting service, completion and parameter-info contributors, a structure view, and actions under **Tools \| Cedar**. The `core/` files stay IDE-independent and unit-testable.

Two smaller pieces preserve upstream behavior that is easy to lose in translation. A TextMate grammar interpreter runs upstream's `syntaxes/*.tmLanguage.json` files verbatim, so highlighting comes from the same grammars and upstream's grammar tests port directly. A `Js.kt` helper file replicates the JavaScript semantics the TypeScript relies on, such as `indexOf` with a start position, `substring` clamping, falsy `0` and `""`, and regex `match` and `matchAll`.

## Compare against upstream directly

Parity claims need evidence. Beyond unit and IntelliJ platform tests, the repository has a differential harness for the parser and schema-diagram generator. It runs upstream's own `parser.ts` and `generate.ts` under Node, with stub `vscode` and `vscode-cedar-wasm` modules and the exact `jsonc-parser` version upstream locks, then runs the Kotlin port over the same `testdata/` and fixtures and compares every entry point's output field by field.

The port also has to respect IntelliJ's threading model, which VS Code does not impose. Document and PSI reads happen in read actions, writes happen in write commands on the event dispatch thread, and Cedar SDK calls stay off that thread. Several later commits went into this, moving Cedar SDK calls and problem reporting off the EDT so editing stays responsive.

A few differences are deliberate and documented. Validation runs continuously through the IntelliJ daemon instead of on open and save, the JSON preview opens as a read-only editor tab, and **Activate Cedar Extension** remains as a no-op because the plugin is always active.

## Keep pace with upstream

The initial port covers all 29 reachable upstream commits through vscode-cedar 0.10.6, recorded as baseline events in an append-only `semport/ledger.tsv`. New upstream commits are discovered and processed one at a time, oldest first, using the same ledger model as my other [semantic ports]({{ '/notes/autonomous-semantic-porting-with-fkyeah/' | relative_url }}): each commit ends as implemented, acknowledged with a written skip rationale, or wedged with its work preserved in a Git stash.

Two drivers share that ledger and its gates. A `/semport` skill in Claude Code runs separate analysis, implementation, and independent review agents. [`semport.dot`](https://github.com/TheFellow/jetbrains-cedar/blob/main/semport/semport.dot) encodes the same workflow as an Attractor graph for [F#kYeah]({{ '/projects/fkyeah/' | relative_url }}). Both run the same validation contract: `cargo test` for the SDK bridge, the Gradle test suite, `buildPlugin`, and plugin structure verification.

[`semport/MAPPING.md`](https://github.com/TheFellow/jetbrains-cedar/blob/main/semport/MAPPING.md) maps every upstream file to its port, which also documents where typical changes land. A Cedar SDK bump goes to `cedar-wasm/Cargo.toml`, a grammar change is copied verbatim, and a change to `src/*.ts` goes to the mapped Kotlin file. Plugin versions follow upstream, with a fourth component for plugin-only releases like 0.10.6.1, and a tagged release builds, verifies, and publishes the plugin to the JetBrains Marketplace.

The result is Cedar editing in JetBrains IDEs that behaves like the VS Code extension because it runs the same SDK and the same editor logic, with a ledger and a set of checks that make keeping it that way routine.

## Where to look

- [jetbrains-cedar](https://github.com/TheFellow/jetbrains-cedar) for the plugin, install instructions, and releases.
- [`jetbrains-cedar/semport`](https://github.com/TheFellow/jetbrains-cedar/tree/main/semport) for the ledger, mapping, differential harness, and porting workflow.
- [vscode-cedar](https://github.com/cedar-policy/vscode-cedar) for the upstream extension that defines the behavior.
