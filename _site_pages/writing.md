---
title: "Writing"
date: 2026-09-12
last_modified_at: 2026-09-12
permalink: /writing/
layout: single
author_profile: true
classes: wide
excerpt: "Articles, notes, and series on software architecture, developer tools, and experiments, newest first."
---

Articles, notes, and series from the projects and experiments behind this site, ordered by publication date, newest first.

<div class="feature-tiles">
  {% assign writing_index = 0 %}
  {% assign writing_days = site.guides | concat: site.posts | concat: site.reading_series | group_by_exp: "entry", "entry.date | date: '%Y-%m-%d'" | sort: "name" | reverse %}
  {% for day in writing_days %}
  {% assign writing = day.items | sort_natural: "title" %}
  {% for entry in writing %}
    {% case entry.collection %}
      {% when "posts" %}
        {% assign kind = "Note" %}
      {% when "reading_series" %}
        {% assign kind = "Series" %}
      {% else %}
        {% assign kind = "Article" %}
    {% endcase %}
    {% assign tile_position = writing_index | modulo: 5 %}
    <a class="feature-tile{% if tile_position == 0 %} feature-tile--featured{% endif %}" href="{{ entry.url | relative_url }}" style="--feature-accent: {{ entry.accent | default: '#ffa94d' }};">
      <header class="feature-tile__header">
        <span class="feature-tile__icon">{% include feature-icon.html name=entry.icon %}</span>
        <span>
          <span class="feature-tile__eyebrow">{{ kind }} · <time datetime="{{ entry.date | date_to_xmlschema }}">{{ entry.date | date: "%B %-d, %Y" }}</time></span>
          <span class="feature-tile__title">{{ entry.title | escape }}</span>
        </span>
      </header>
      <span class="feature-tile__description">{{ entry.excerpt | strip_html | truncate: 240 | escape }}</span>
      {% assign topics = entry.topics | default: entry.tags %}
      {% if topics.size > 0 %}
      <span class="feature-tile__topics">
        {% for topic in topics %}<span>{{ topic | escape }}</span>{% endfor %}
      </span>
      {% endif %}
      <span class="feature-tile__cta">{% if kind == "Series" %}Open series{% else %}Read {{ kind | downcase }}{% endif %} <span class="feature-tile__arrow" aria-hidden="true">→</span></span>
    </a>
    {% assign writing_index = writing_index | plus: 1 %}
  {% endfor %}
  {% endfor %}
</div>
