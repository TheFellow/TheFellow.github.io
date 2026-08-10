---
title: "Building Mixology"
date: 2026-07-23 12:03:42 -0700
last_modified_at: 2026-08-09 19:30:00 -0700
excerpt: "An ordered path through the architecture, domain modeling, authorization, and three user interfaces of the go-modular-monolith reference application."
order: 10
entries_label: "12 articles and notes"
icon: "modules"
accent: "#63e6be"
topics: ["Go", "Modular architecture", "Application design"]
project_url: "/projects/go-modular-monolith/"
repository_url: "https://github.com/TheFellow/go-modular-monolith"
---

Mixology is a Go reference application that makes modular boundaries and cross-cutting concerns executable. This series follows the application from its architectural premise through transactional domain collaboration, presentation boundaries, native desktop testing, authorization, and shared action meaning.

The completed [.NET semantic port](/projects/modular-monolith/) preserves that observable behavior while rebuilding the application with .NET 10, EF Core, Terminal.Gui, and Avalonia. It provides a parallel implementation for separating the architecture's durable ideas from the Go-specific mechanisms described throughout this series.

[Explore the project](/projects/go-modular-monolith/){: .btn .btn--primary }
[View the repository](https://github.com/TheFellow/go-modular-monolith){: .btn }
[Explore the .NET port](/projects/modular-monolith/){: .btn }

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
