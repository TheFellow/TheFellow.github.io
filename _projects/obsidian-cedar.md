---
title: "Obsidian Cedar plugin"
date: 2026-11-12 10:00:00 -0800
last_modified_at: 2026-11-12 10:00:00 -0800
excerpt: "Cedar policy and schema highlighting for Obsidian notes, using the official VS Code extension's grammars."
language: "TypeScript"
license: "Apache-2.0"
repository_url: "https://github.com/TheFellow/obsidian-cedar"
last_updated: 2026-11-11
order: 23
icon: "note"
accent: "#845ef7"
topics: ["Authorization", "Developer tools"]
---

<div class="project-meta"><span>TypeScript</span><span>Cedar</span><span>Obsidian</span><span>Apache-2.0</span><span>Updated {{ page.last_updated | date: "%B %-d, %Y" }}</span></div>

[View the repository](https://github.com/TheFellow/obsidian-cedar){: .btn .btn--primary }
[Install from Obsidian](https://community.obsidian.md/plugins/cedar){: .btn }

The Obsidian Cedar plugin highlights `cedar` policy and `cedarschema` fenced code blocks in Obsidian notes, in Live Preview, Source mode, and Reading view. Colors come from the active theme, and a `cedar-<kind>` class on every token lets a CSS snippet restyle any part of the language.

<figure class="article-figure">
  <img src="{{ '/assets/images/projects/obsidian-cedar/cedar-note.png' | relative_url }}" alt="An Obsidian note in the default dark theme with a highlighted Cedar policy and a highlighted Cedar schema. Keywords, entity types, strings, slots, operators, and comments each take a distinct theme code color, and an invalid string escape has a dashed red underline." width="1400" height="1367">
  <figcaption>A Cedar policy and the TinyTodo schema highlighted in Reading view.</figcaption>
</figure>

The highlighting comes from the TextMate grammars in the official [Cedar extension for VS Code](https://github.com/cedar-policy/vscode-cedar), bundled unmodified and run by a pure-JavaScript TextMate engine. One tokenizer feeds both of Obsidian's highlighters: a CodeMirror stream mode for the editor and a Prism hook for Reading view, embeds, hover previews, and PDF export.

### Why it is worth exploring

- It reuses the same grammars as VS Code and [jetbrains-cedar]({{ '/projects/jetbrains-cedar/' | relative_url }}), so Cedar is tokenized identically in all three editors.
- It adapts a line-at-a-time TextMate tokenizer to two very different highlighting APIs without writing a second grammar.
- Its scope-to-color mapping mirrors jetbrains-cedar's, so the plugins stay consistent as the grammars change.

The [build note]({{ '/notes/cedar-highlighting-in-obsidian/' | relative_url }}) walks through the design. In the repository, start with the README, then `src/editor-mode.ts` and `src/reading-view.ts` for the two adapters.
