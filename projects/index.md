---
title: Projects
nav:
  order: 2
  tooltip: Software, datasets, and more
---

# {% include icon.html icon="fa-solid fa-diagram-project" %}Projects

Our group develops computational tools, educational programs, and collaborative
research initiatives to advance quantum information theory and real-time quantum
field evolution. All projects support open science and reproducible research in
theoretical physics and quantum computing.

{% include tags.html tags="software, education, research-program, collaboration" %}

{% include search-info.html %}

{% include section.html %}

## Featured

{% include list.html component="card" data="projects" filter="group == 'featured'" %}

{% include section.html %}

## More

{% include list.html component="card" data="projects" filter="!group" style="small" %}
