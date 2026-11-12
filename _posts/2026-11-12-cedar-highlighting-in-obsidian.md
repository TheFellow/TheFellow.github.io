---
title: "Cedar Highlighting in Obsidian"
date: 2026-11-12 10:00:00 -0800
last_modified_at: 2026-11-12 10:00:00 -0800
permalink: /notes/cedar-highlighting-in-obsidian/
excerpt: "How obsidian-cedar highlights Cedar policies and schemas in Obsidian notes by running the official VS Code extension's TextMate grammars, unmodified, in both of Obsidian's highlighters."
icon: "note"
accent: "#845ef7"
tags: ["Cedar", "TypeScript", "Obsidian", "Developer tools"]
---

Obsidian has no highlighting for Cedar, so a `cedar` fenced code block renders as plain text. [obsidian-cedar](https://github.com/TheFellow/obsidian-cedar) is a small Obsidian plugin that highlights `cedar` policy blocks and `cedarschema` blocks in the human-readable schema format, in Live Preview, Source mode, and Reading view, using the theme's own code colours. The current release is 0.1.2, and it runs on desktop and mobile.

## Reuse the upstream grammars

The [Cedar extension for VS Code](https://github.com/cedar-policy/vscode-cedar) already defines Cedar highlighting as TextMate grammars, and [jetbrains-cedar]({{ '/notes/porting-vscode-cedar-to-jetbrains/' | relative_url }}) runs those same grammars verbatim. The Obsidian plugin bundles them unmodified too, so a policy is tokenized the same way in all three editors, and an upstream grammar change is a file copy.

TextMate grammars are written against Oniguruma regular expressions. Instead of shipping Oniguruma as WebAssembly, the plugin loads the grammars into [`@shikijs/vscode-textmate`](https://github.com/shikijs/vscode-textmate) with Shiki's JavaScript regex engine, which translates the patterns to native JavaScript regular expressions. The whole tokenizer is about 80 lines of TypeScript and needs no network access or native code.

## Feed one tokenizer to two highlighters

Obsidian highlights code in two unrelated ways. The editor resolves a fence's language to a CodeMirror 5-style stream mode in `window.CodeMirror.modes`, while Reading view, embeds, hover previews, and PDF export all go through Prism. The plugin plugs the same tokenizer into both.

For the editor, a TextMate rule stack maps directly onto a stream mode's state. The first token request on a line tokenizes the rest of that line, and later requests are served from the result. The mode detects a new line by its text and position rather than CodeMirror's `sol()`, because inside a blockquote or list the Markdown mode consumes the `> ` or indent prefix before it delegates to the code block's mode.

Prism grammars are lists of regular expressions, so rewriting Cedar for Prism would have meant a second, divergent grammar. Instead the plugin registers empty Prism languages named `cedar` and `cedarschema`, then replaces their token streams in an `after-tokenize` hook:

```typescript
for (const t of tokenizer.block(lang, env.code)) {
	if (t.start > pos) out.push(env.code.slice(pos, t.start));
	const text = env.code.slice(t.start, t.end);
	out.push(t.cls ? new prism.Token(t.cls.prism, text, `cedar-${t.cls.name}`) : text);
	pos = t.end;
}
```

## Map scopes to theme colours

A TextMate grammar produces scopes like `variable.language.cedar` or `entity.name.type.cedar`, not colours. `scopes.ts` mirrors jetbrains-cedar's `CedarColors.forScope`, checking the most specific scope first, and gives each class a CodeMirror token type and a Prism token type that resolve to the same `--code-*` theme variable. Live Preview and Reading view therefore agree with each other and follow whatever theme is installed. Every token also carries a `cedar-<kind>` class, so a CSS snippet such as `.cedar-variable { font-weight: bold; }` can restyle `principal`, `action`, `resource`, and `context` without touching the plugin.

## Handle notes that were already open

Notes open when the plugin loads have already chosen CodeMirror's plain-text mode for their unknown code blocks, and that choice lives in the editor's saved parse state. Obsidian re-highlights once after loading its own bundled modes, which usually happens before community plugins load. When the layout is ready, and again on unload, the plugin re-renders every open note that contains a Cedar fence, so highlighting appears without reopening anything and disappears cleanly when the plugin is disabled.

The tests exercise the tokenizer against upstream's `testdata/` fixtures, drive the stream mode with CodeMirror's `StringStream` the way Obsidian's Markdown mode does, including repeated identical lines inside a blockquote, and check that the Prism hook renders and unregisters cleanly. Linting uses Obsidian's official ESLint rules, the same rules the community directory's automated review runs.

The result is Cedar in Obsidian notes that looks like Cedar in VS Code and JetBrains IDEs, because it comes from the same grammars, with one small tokenizer adapted to each of Obsidian's highlighters.

## Where to look

- [obsidian-cedar](https://github.com/TheFellow/obsidian-cedar) for the plugin, install instructions, and releases.
- [`src/editor-mode.ts`](https://github.com/TheFellow/obsidian-cedar/blob/main/src/editor-mode.ts) and [`src/reading-view.ts`](https://github.com/TheFellow/obsidian-cedar/blob/main/src/reading-view.ts) for the two adapters over the shared tokenizer.
- [jetbrains-cedar]({{ '/projects/jetbrains-cedar/' | relative_url }}) for the JetBrains plugin that runs the same grammars.
