---
title: "Building Weave"
date: 2026-08-06 22:55:00 -0700
last_modified_at: 2026-08-08 14:20:00 -0700
excerpt: "An ordered path through Weave's move from an exhaustive semantic graph to a compact, fresh navigation index built for practical source discovery."
order: 5
entries_label: "15 articles"
icon: "route"
accent: "#4dabf7"
topics: ["Go", "Code intelligence", "Developer tools"]
project_url: "/projects/weave/"
repository_url: "https://github.com/TheFellow/weave"
---

Weave began by retaining a broad compiler and content graph. Repository and agent measurements showed that this made both the database and discovery responses much larger than the source evidence they were meant to reveal. The current implementation produces a compact navigation profile, returns a few semantic anchors and ripgrep hits, and opens current source only after a caller selects a useful anchor.

This series preserves the engineering path that exposed that correction. Earlier articles describe the broad graph at the point it was built; each affected article now identifies what the navigation profile retained, replaced, or removed. Format 4 first narrowed persistence, and format 5 moved that boundary into fact production and the adapter contract. The stable ideas are freshness at read time, language-native adapters, explicit evidence, bounded queries, disposable local state, and measured agent outcomes. Exhaustive occurrences, statement-level call and reference storage, large multi-focus dossiers, and body-token postings are no longer the product direction.

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
