---
title: "Notes"
date: 2026-07-23 12:03:42 -0700
last_modified_at: 2026-08-06 18:00:00 -0700
permalink: /notes/
layout: single
author_profile: true
classes: wide
---

Shorter technical observations, implementation details, and working ideas drawn from the projects and guide series.

{% if site.posts.size > 0 %}
<div class="feature-tiles">
  {% for post in site.posts %}
    {% assign tile_position = forloop.index0 | modulo: 5 %}
    <a class="feature-tile{% if tile_position == 0 %} feature-tile--featured{% endif %}" href="{{ post.url | relative_url }}" style="--feature-accent: {{ post.accent | default: '#f783ac' }};">
      <header class="feature-tile__header">
        <span class="feature-tile__icon">{% include feature-icon.html name=post.icon %}</span>
        <span>
          <span class="feature-tile__eyebrow">{{ post.date | date: "%B %-d, %Y" }}</span>
          <span class="feature-tile__title">{{ post.title }}</span>
        </span>
      </header>
      <span class="feature-tile__description">{{ post.excerpt | strip_html | truncate: 190 }}</span>
      {% if post.tags.size > 0 %}
      <span class="feature-tile__topics">
        {% for tag in post.tags %}<span>{{ tag }}</span>{% endfor %}
      </span>
      {% endif %}
      <span class="feature-tile__cta">Read note <span class="feature-tile__arrow" aria-hidden="true">→</span></span>
    </a>
  {% endfor %}
</div>
{% else %}
<div class="feature-tiles">
  <section class="feature-tile feature-tile--featured feature-tile--static" style="--feature-accent: #f783ac;">
    <header class="feature-tile__header">
      <span class="feature-tile__icon">{% include feature-icon.html name="note" %}</span>
      <span>
        <span class="feature-tile__eyebrow">Notebook opening soon</span>
        <span class="feature-tile__title">The first notes are taking shape</span>
      </span>
    </header>
    <span class="feature-tile__description">This space is ready for shorter pieces that do not need a full tutorial: design decisions, experiments, implementation details, and lessons learned while the projects evolve.</span>
    <span class="feature-tile__topics"><span>Architecture</span><span>Developer tools</span><span>AI workflows</span></span>
  </section>
</div>
{% endif %}
