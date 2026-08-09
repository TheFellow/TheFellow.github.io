---
title: "Building Weave"
date: 2026-08-06 22:55:00 -0700
last_modified_at: 2026-08-09 10:00:00 -0700
excerpt: "How Weave builds a compact, fresh navigation index for practical source discovery."
order: 5
entries_label: "15 articles"
icon: "route"
accent: "#4dabf7"
topics: ["Go", "Code intelligence", "Developer tools"]
project_url: "/projects/weave/"
repository_url: "https://github.com/TheFellow/weave"
---

Weave format 5 is a compact navigation index. Providers emit declaration and document anchors plus high-value relationships, discovery combines those anchors with bounded source search, and context opens authoritative source only after selection. The series covers freshness, adapters, storage, content, federation, and agent-facing queries within that practical contract.

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
