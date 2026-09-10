---
title: "the-line"
date: 2026-09-10 12:00:00 -0700
last_modified_at: 2026-09-10 15:05:53 -0700
excerpt: "A racing-line playground in Go for reshaping corners, experimenting with car setup, and exploring two-car overtaking and defence."
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
  <img src="{{ '/assets/images/projects/the-line/club-loop.gif' | relative_url }}" alt="Qualifying with a reference ghost on Club Loop, followed by two-car over-under and pass/repass experiments." width="960" height="600">
  <figcaption>Qualifying on Club Loop, then two-car racecraft in plan and elevated views, with shared-time speed and position-gap charts.</figcaption>
</figure>

A native Ebitengine viewer exposes editable track geometry, banking, elevation, surfaces, kerbs, and car setup. Smooth candidate lines are evaluated against tyre-force limits, then checked on a finer road mesh. The model includes power, drag, axle drive split, and optional brake bias, downforce, longitudinal load transfer, and tyre load sensitivity.

Racecraft adds two solid cars sharing an open corner sequence. Authored tactical intentions explore an over-under, pass/repass, inside defence, and an esses duel. The planner evaluates a finite set of placements and accepts only pairs with continuously certified body clearance. Changing the starting gap or entry caps can change the result: increasing the default over-under gap from 6 m to 11 m prevents its completed pass before the finish.

### Things to try

- Pin a reference, change grip or power, and compare the speed traces and elapsed-time delta.
- Drag a corner wider or change its banking, then watch the line and braking points move.
- Author a line with lateral handles and compare your idea with the searched result.
- Press **R** for racecraft, adjust the starting conditions, and scrub both cars on a shared timeline to inspect an overtaking attempt.
- Save a complete race experiment, including its road, vehicle, and inputs, then return to the retained qualifying study.
- Switch between plan, elevated, and perspective views, or export a PNG, GIF, or CSV from the CLI.

The cars use illustrative quasi-static force limits, which makes the relationship between geometry, grip, and time easy to inspect. The [build note](/notes/building-a-racing-line-playground/) follows that model through braking, axle balance, periodic laps, performance profiling, and the tactical planning and clearance checks behind racecraft.

Start with the repository's [quick start](https://github.com/TheFellow/the-line#readme), launch the viewer, and reshape the default esses.
