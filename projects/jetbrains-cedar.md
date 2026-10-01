<!-- Generated from https://thefellow.github.io/projects/jetbrains-cedar/ by scripts/generate_llm_content.py; do not edit. -->

# jetbrains-cedar

Source: [https://thefellow.github.io/projects/jetbrains-cedar/](https://thefellow.github.io/projects/jetbrains-cedar/)

## Pyramid summary

- **~2 words:** Cedar IDE plugin
- **~8 words:** Cedar editing for JetBrains IDEs, ported from vscode-cedar.
- **Expanded:** Cedar policy language support for JetBrains IDEs, ported from the official VS Code extension.

## Full content

[View the repository](https://github.com/TheFellow/jetbrains-cedar)

jetbrains-cedar brings the official [Cedar extension for Visual Studio Code](https://github.com/cedar-policy/vscode-cedar) to GoLand, IntelliJ IDEA, PyCharm, WebStorm, and other IntelliJ-based IDEs. Cedar policies, schemas, and entities files get highlighting, validation as you edit, formatting, completion, hover, quick fixes, navigation, and the extension's export and translation commands.

The Cedar SDK runs inside the IDE as WebAssembly on Chicory, a pure-Java runtime, so validation and formatting match the VS Code extension and the `cedar` CLI without native binaries. The extension's TypeScript modules are ported near line for line against a small re-creation of the VS Code API, and a separate layer wires them into IntelliJ's annotators, formatter, completion, and structure view.

### Why it is worth exploring

- It shows a semantic port where staying structurally close to upstream is the point, because it keeps later upstream commits easy to port and review.
- Running upstream's Rust crate as WebAssembly in the JVM reuses the SDK instead of reimplementing it.
- A ledger, a file-by-file mapping, and a differential harness against upstream's own TypeScript keep the plugin in step with vscode-cedar.

The [porting note](/notes/porting-vscode-cedar-to-jetbrains.md) walks through the design. In the repository, start with the README, then `semport/MAPPING.md` to see how each upstream file maps to its Kotlin counterpart.
