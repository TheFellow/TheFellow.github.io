---
title: "jetbrains-cedar"
date: 2026-10-01 11:30:00 -0700
last_modified_at: 2026-10-01 11:30:00 -0700
excerpt: "Cedar policy language support for JetBrains IDEs, ported from the official VS Code extension."
language: "Kotlin"
license: "Apache-2.0"
repository_url: "https://github.com/TheFellow/jetbrains-cedar"
last_updated: 2026-09-28
order: 22
icon: "shield"
accent: "#9775fa"
topics: ["Authorization", "Developer tools"]
---

<div class="project-meta"><span>Kotlin</span><span>Cedar</span><span>IntelliJ Platform</span><span>Apache-2.0</span><span>Updated {{ page.last_updated | date: "%B %-d, %Y" }}</span></div>

[View the repository](https://github.com/TheFellow/jetbrains-cedar){: .btn .btn--primary }

jetbrains-cedar brings the official [Cedar extension for Visual Studio Code](https://github.com/cedar-policy/vscode-cedar) to GoLand, IntelliJ IDEA, PyCharm, WebStorm, and other IntelliJ-based IDEs. Cedar policies, schemas, and entities files get highlighting, validation as you edit, formatting, completion, hover, quick fixes, navigation, and the extension's export and translation commands.

The Cedar SDK runs inside the IDE as WebAssembly on Chicory, a pure-Java runtime, so validation and formatting match the VS Code extension and the `cedar` CLI without native binaries. The extension's TypeScript modules are ported near line for line against a small re-creation of the VS Code API, and a separate layer wires them into IntelliJ's annotators, formatter, completion, and structure view.

### Why it is worth exploring

- It shows a semantic port where staying structurally close to upstream is the point, because it keeps later upstream commits easy to port and review.
- Running upstream's Rust crate as WebAssembly in the JVM reuses the SDK instead of reimplementing it.
- A ledger, a file-by-file mapping, and a differential harness against upstream's own TypeScript keep the plugin in step with vscode-cedar.

The [porting note]({{ '/notes/porting-vscode-cedar-to-jetbrains/' | relative_url }}) walks through the design. In the repository, start with the README, then `semport/MAPPING.md` to see how each upstream file maps to its Kotlin counterpart.
