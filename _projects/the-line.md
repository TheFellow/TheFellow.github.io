---
title: "the-line"
date: 2026-09-10 12:00:00 -0700
last_modified_at: 2026-09-10 12:00:00 -0700
excerpt: "A racing-line playground in Go for reshaping corners, experimenting with car setup, and watching the physics change a lap."
language: "Go"
repository_url: "https://github.com/TheFellow/the-line"
last_updated: 2026-09-10
order: 51
icon: "racing"
accent: "#ffb454"
topics: ["Simulation", "Vehicle dynamics", "Visualization"]
---

<div class="project-meta"><span>Go</span><span>Simulation</span><span>Vehicle dynamics</span><span>Updated {{ page.last_updated | date: "%B %-d, %Y" }}</span></div>

[View the repository](https://github.com/TheFellow/the-line){: .btn .btn--primary }
[Read the build note](/notes/building-a-racing-line-playground/){: .btn }

The Line is a physics playground in the same spirit as [fluid](/projects/fluid/): change something, watch the result, and use the picture to ask a better question. Here the questions are about corners. What happens if the exit opens up? Does more power help on this stretch? How much braking grip remains while the car is turning?

<figure class="article-figure">
  <img src="{{ '/assets/images/projects/the-line/club-loop.gif' | relative_url }}" alt="A GT car and its reference ghost circulating around Club Loop, with their speed traces below." width="960" height="600">
  <figcaption>Club Loop, one of twelve fictional tracks. The ghost shows a reference run while the chart compares speeds at matching positions along the road.</figcaption>
</figure>

A native Ebitengine viewer exposes editable track geometry, banking, elevation, surfaces, kerbs, and car setup. Smooth candidate lines are evaluated against tyre-force limits, then checked on a finer road mesh. The model includes power, drag, axle drive split, and optional brake bias, downforce, longitudinal load transfer, and tyre load sensitivity.

### Things to try

- Pin a reference, change grip or power, and compare the speed traces and elapsed-time delta.
- Drag a corner wider or change its banking, then watch the line and braking points move.
- Author a line with lateral handles and compare your idea with the searched result.
- Switch between plan, elevated, and perspective views, or export a PNG, GIF, or CSV from the CLI.

The cars use illustrative quasi-static force limits, which makes the relationship between geometry, grip, and time easy to inspect. The [build note](/notes/building-a-racing-line-playground/) follows that model through braking, axle balance, periodic laps, and the profiling work that made repeated experiments faster.

Start with the repository's [quick start](https://github.com/TheFellow/the-line#readme), launch the viewer, and reshape the default esses.
