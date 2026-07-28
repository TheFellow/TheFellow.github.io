---
title: "Guides"
permalink: /guides/
layout: single
author_profile: true
classes: wide
---

Long-form tutorials connect design principles to running code. Each series is structured so written chapters can stand on their own and later pair with video walkthroughs.

<div class="feature-tiles">
  {% assign sorted_guides = site.guides | sort: "order" %}
  {% for guide in sorted_guides %}
    <a class="feature-tile feature-tile--featured" href="{{ guide.url | relative_url }}" style="--feature-accent: {{ guide.accent }};">
      <header class="feature-tile__header">
        <span class="feature-tile__icon">{% include feature-icon.html name=guide.icon %}</span>
        <span>
          <span class="feature-tile__eyebrow">{{ guide.status }}</span>
          <span class="feature-tile__title">{{ guide.title }}</span>
        </span>
      </header>
      <span class="feature-tile__description">{{ guide.excerpt }}</span>
      <span class="feature-tile__topics">
        {% for topic in guide.topics %}<span>{{ topic }}</span>{% endfor %}
      </span>
      <span class="feature-tile__cta">Open guide <span class="feature-tile__arrow" aria-hidden="true">→</span></span>
    </a>
  {% endfor %}
</div>
