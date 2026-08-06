---
title: "Series"
date: 2026-08-06 08:00:00 -0700
last_modified_at: 2026-08-06 12:00:00 -0700
permalink: /series/
layout: single
author_profile: true
classes: wide
excerpt: "Ordered reading paths that connect related articles and notes."
---

Series collect related writing into an intentional reading order. Each article or note still stands on its own, while the series page shows how the ideas developed across a project.

<div class="feature-tiles">
  {% assign sorted_series = site.reading_series | sort: "order" %}
  {% for series in sorted_series %}
    <a class="feature-tile{% if forloop.first %} feature-tile--featured{% endif %}" href="{{ series.url | relative_url }}" style="--feature-accent: {{ series.accent }};">
      <header class="feature-tile__header">
        <span class="feature-tile__icon">{% include feature-icon.html name=series.icon %}</span>
        <span>
          <span class="feature-tile__eyebrow">{{ series.entries_label }}</span>
          <span class="feature-tile__title">{{ series.title }}</span>
        </span>
      </header>
      <span class="feature-tile__description">{{ series.excerpt }}</span>
      <span class="feature-tile__topics">
        {% for topic in series.topics %}<span>{{ topic }}</span>{% endfor %}
      </span>
      <span class="feature-tile__cta">Open series <span class="feature-tile__arrow" aria-hidden="true">→</span></span>
    </a>
  {% endfor %}
</div>
