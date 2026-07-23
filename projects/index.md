---
title: "Projects"
permalink: /projects/
layout: single
author_profile: true
classes: wide
---

These are the projects currently pinned on [my GitHub profile](https://github.com/TheFellow). Each page adds context beyond the repository README: the problem I was exploring, the ideas worth carrying forward, and a practical route into the code.

<div class="project-tiles">
  {% assign sorted_projects = site.projects | sort: "order" %}
  {% for project in sorted_projects %}
    <a class="project-tile{% if project.featured %} project-tile--featured{% endif %}" href="{{ project.url | relative_url }}" style="--project-accent: {{ project.accent }};">
      <header class="project-tile__header">
        <span class="project-tile__icon">{% include project-icon.html name=project.icon %}</span>
        <span>
          <span class="project-tile__language">{{ project.language }}</span>
          <span class="project-tile__title">{{ project.title }}</span>
        </span>
      </header>
      <span class="project-tile__description">{{ project.excerpt }}</span>
      <span class="project-tile__topics">
        {% for topic in project.topics %}<span>{{ topic }}</span>{% endfor %}
      </span>
      <span class="project-tile__cta">Explore project <span class="project-tile__arrow" aria-hidden="true">→</span></span>
    </a>
  {% endfor %}
</div>
