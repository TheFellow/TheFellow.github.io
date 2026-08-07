---
title: "Articles"
date: 2026-07-23 12:03:42 -0700
last_modified_at: 2026-08-06 23:45:00 -0700
permalink: /articles/
redirect_from: /guides/
layout: single
author_profile: true
classes: wide
---

Long-form tutorials, essays, case studies, and development journals connect design principles to running code. Related articles are collected into [ordered series](/series/) without requiring each article to use the same format.

<div class="feature-tiles">
  {% assign sorted_guides = site.guides | sort: "order" %}
  {% for article in sorted_guides %}
    {% assign tile_position = forloop.index0 | modulo: 5 %}
    <a class="feature-tile{% if tile_position == 0 %} feature-tile--featured{% endif %}" href="{{ article.url | relative_url }}" style="--feature-accent: {{ article.accent }};">
      <header class="feature-tile__header">
        <span class="feature-tile__icon">{% include feature-icon.html name=article.icon %}</span>
        <span>
          <span class="feature-tile__eyebrow">{{ article.status }}</span>
          <span class="feature-tile__title">{{ article.title }}</span>
        </span>
      </header>
      <span class="feature-tile__description">{{ article.excerpt }}</span>
      <span class="feature-tile__topics">
        {% for topic in article.topics %}<span>{{ topic }}</span>{% endfor %}
      </span>
      <span class="feature-tile__cta">Open article <span class="feature-tile__arrow" aria-hidden="true">→</span></span>
    </a>
  {% endfor %}
</div>
