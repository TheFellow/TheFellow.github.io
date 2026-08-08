---
title: "Building Weave"
date: 2026-08-06 22:55:00 -0700
last_modified_at: 2026-08-08 04:04:08 -0700
excerpt: "An ordered path through Weave's fresh compiler-backed graph, exact storage, managed adapters, agent measurement, resident query sessions, and cross-repository validation."
order: 5
entries_label: "15 articles"
icon: "route"
accent: "#4dabf7"
topics: ["Go", "Code intelligence", "Developer tools"]
project_url: "/projects/weave/"
repository_url: "https://github.com/TheFellow/weave"
---

Weave turns language-native compiler facts and live Git state into a local semantic graph for people and coding agents. This series follows the tool from its query-driven freshness contract through cross-language bridges, graph inspection, current source context, exact machine-wide aggregation, compact private storage, Git-aware semantic comparison, optional watch-mode warming, revision-guarded contextual authoring, managed adapter trust and conformance, source-only declarations, paired agent-research measurement, body-concept discovery, a resident query session that keeps the graph hot without installing a daemon, and a strict cross-repository soak that makes real compiler and repository behavior part of the indexing contract.

[Explore the project](/projects/weave/){: .btn .btn--primary }
[View the repository](https://github.com/TheFellow/weave){: .btn }

{% assign series_entries = site.guides | concat: site.posts | where: "series", page.slug | sort: "series_order" %}

<div class="series-list">
{% for entry in series_entries %}
  <article class="series-entry">
    <span class="series-entry__number">{{ entry.series_order }}</span>
    <div>
      <p class="series-entry__kind">{% if entry.collection == "posts" %}Note{% else %}Article{% endif %}</p>
      <h2><a href="{{ entry.url | relative_url }}">{{ entry.title }}</a></h2>
      <p>{{ entry.excerpt }}</p>
    </div>
  </article>
{% endfor %}
</div>
