---
title: "Projects"
permalink: /projects/
layout: single
author_profile: true
classes: wide
---

These are the projects currently pinned on [my GitHub profile](https://github.com/TheFellow). Each page adds context beyond the repository README: the problem I was exploring, the ideas worth carrying forward, and a practical route into the code.

<div class="feature-tiles">
  {% assign sorted_projects = site.projects | sort: "order" %}
  {% for project in sorted_projects %}
    <a class="feature-tile{% if project.featured %} feature-tile--featured{% endif %}" href="{{ project.url | relative_url }}" style="--feature-accent: {{ project.accent }};">
      <header class="feature-tile__header">
        <span class="feature-tile__icon">{% include feature-icon.html name=project.icon %}</span>
        <span>
          <span class="feature-tile__eyebrow">{{ project.language }}</span>
          <span class="feature-tile__title">{{ project.title }}</span>
        </span>
      </header>
      <span class="feature-tile__description">{{ project.excerpt }}</span>
      <span class="feature-tile__topics">
        {% for topic in project.topics %}<span>{{ topic }}</span>{% endfor %}
      </span>
      <span class="feature-tile__cta">Explore project <span class="feature-tile__arrow" aria-hidden="true">→</span></span>
    </a>
  {% endfor %}
</div>
