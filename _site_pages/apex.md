---
layout: single
title: "Apex"
date: 2026-08-23 17:00:00 -0700
last_modified_at: 2026-08-23 17:00:00 -0700
permalink: /apex/
author_profile: false
classes: wide
excerpt: "A working recreation of the Windows 3.1 unit converter my dad built and released as shareware in the 1990s."
project_listing: true
order: 0
language: "TypeScript"
last_updated: 2026-08-23
accent: "#ffd43b"
topics: ["Windows 3.1", "Pixel art", "Family history"]
---

<div class="apex-page-copy" markdown="1">

My dad built Apex in the 1990s and released it as Windows 3.1 shareware. It put everyday conversions into one compact window, with a category rail, two editable values, and the vivid 256-color icons he drew in CorelDRAW.

This is my working recreation of that application. Choose a category, select two units, and type into either field. Apex immediately recomputes the other value, just as the original did.

</div>

<div id="apex-app" aria-busy="true">
  <noscript>Apex needs JavaScript enabled to run the converter.</noscript>
</div>

<script src="{{ '/assets/apex/dist/apex.js' | relative_url }}" defer></script>

<div class="apex-page-copy" markdown="1">

## A small piece of family software history

The interface follows the original single-window design: conversion categories on the left, the selected pair of units on the right, and direct entry in either direction. I rebuilt the calculations as a data-driven TypeScript application and recreated each category icon as indexed 256-color pixel art.

Apex is a gift for my dad and an homage to the care he put into a useful little program. Decades later, the lightning bolt still belongs in that blue title bar.

</div>
