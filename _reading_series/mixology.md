---
title: "Building Mixology"
date: 2026-07-23 12:03:42 -0700
last_modified_at: 2026-09-06
excerpt: "An ordered path through the architecture, domain modeling, persistence, authorization, and three user interfaces of the go-modular-monolith reference application."
order: 10
entries_label: "13 articles and notes"
icon: "modules"
accent: "#63e6be"
topics: ["Go", "Modular architecture", "Application design"]
project_url: "/projects/go-modular-monolith/"
repository_url: "https://github.com/TheFellow/go-modular-monolith"
---

Mixology is a Go reference application that makes modular boundaries and cross-cutting concerns executable. This series follows the application from its architectural premise through transactional domain collaboration, presentation boundaries, native desktop testing, authorization, shared action meaning, and the migration from bstore to SQLite.

The [.NET semantic port](/projects/modular-monolith/) explores the same architecture using .NET 10, EF Core, Terminal.Gui, and .NET MAUI; its own parity ledger defines the ported baseline. It provides a parallel implementation for separating the architecture's durable ideas from the Go-specific mechanisms described throughout this series.

The [onboarding deck](/talks/building-mixology/) follows the current Go implementation, including Cedar's input/result authorization, prepared transactional reactions, accepted-order amendments, retained stock lifecycle, correlated audit evidence, and all three presentation toolkits. The articles include development journals and migration histories; their historical checkpoints remain identified as such.

[Explore the project](/projects/go-modular-monolith/){: .btn .btn--primary }
[View the repository](https://github.com/TheFellow/go-modular-monolith){: .btn }
[Explore the .NET port](/projects/modular-monolith/){: .btn }
[Present the slide deck](/talks/building-mixology/){: .btn }

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
