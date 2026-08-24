---
layout: single
title: "Apex"
date: 2026-08-23 17:00:00 -0700
last_modified_at: 2026-08-24 12:00:00 -0700
permalink: /apex/
author_profile: false
classes: wide
excerpt: "A working recreation of the Windows 3.1 unit converter my dad built and released as shareware in the 1990s."
project_listing: true
order: 0
language: "TypeScript"
last_updated: 2026-08-24
accent: "#ffd43b"
topics: ["Windows 3.1", "Pixel art", "Family history"]
---

<div class="apex-page-copy" markdown="1">

My dad built Apex in the 1990s and released it as Windows 3.1 shareware. It put everyday conversions into one compact window, with a category rail, two editable values, and vivid 256-color icons drawn in CorelDRAW.

Choose a category, select two units, and type into either field. Apex immediately recomputes the other value.

</div>

<div id="apex-app" aria-busy="true">
  <noscript>Apex needs JavaScript enabled to run the converter.</noscript>
</div>

<script src="{{ '/assets/apex/dist/apex.js' | relative_url }}" defer></script>

<div class="apex-page-copy" markdown="1">

## About the recreation

The interface follows the original single-window design, with conversion categories on the left and direct entry in either direction on the right. The calculations are data-driven TypeScript, and each category has recreated indexed 256-color pixel art.

The lightning bolt still belongs in that blue title bar.

</div>
