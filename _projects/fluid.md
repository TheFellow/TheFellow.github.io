---
title: "fluid"
date: 2026-07-23 12:03:42 -0700
last_modified_at: 2026-08-06 17:50:00 -0700
excerpt: "An interactive 2D fluid simulator and visualization playground written in Go."
language: "Go"
repository_url: "https://github.com/TheFellow/fluid"
last_updated: 2026-02-17
order: 50
icon: "fluid"
accent: "#74c0fc"
topics: ["Simulation", "Visualization"]
---

<div class="project-meta"><span>Go</span><span>Simulation</span><span>Visualization</span><span>Updated {{ page.last_updated | date: "%B %-d, %Y" }}</span></div>

[View the repository](https://github.com/TheFellow/fluid){: .btn .btn--primary }

fluid is an interactive Eulerian fluid simulation built on a staggered grid. It combines semi-Lagrangian advection with optional BFECC correction and exposes the solver through visual modes for smoke, pressure, velocity magnitude, and vorticity.

<figure class="article-figure article-figure--compact">
  <img src="{{ '/assets/images/projects/fluid/staggered-grid.png' | relative_url }}" alt="A staggered fluid grid with pressure values at cell centers, horizontal velocity on vertical faces, and vertical velocity on horizontal faces.">
  <figcaption>Pressure lives at cell centers while velocity components live on the faces they cross, making each cell's net flow and the pressure correction natural to compute.</figcaption>
</figure>

Live controls turn the numerical method into an effective learning tool. Walls, forces, sources, sinks, particles, border conditions, and presets can all be changed while the simulation runs. Toggling BFECC or vorticity confinement exposes tradeoffs such as numerical diffusion directly in the simulation.

<div class="fluid-gallery">
  <figure class="article-figure">
    <img src="{{ '/assets/images/projects/fluid/karman-smoke.png' | relative_url }}" alt="Smoke visualization of a developed Karman vortex street flowing around a circular obstacle.">
    <figcaption>Smoke</figcaption>
  </figure>
  <figure class="article-figure">
    <img src="{{ '/assets/images/projects/fluid/karman-velocity.png' | relative_url }}" alt="Velocity-magnitude visualization of the same Karman wake with green velocity arrows overlaid.">
    <figcaption>Velocity magnitude and direction</figcaption>
  </figure>
  <figure class="article-figure">
    <img src="{{ '/assets/images/projects/fluid/karman-vorticity.png' | relative_url }}" alt="Signed vorticity visualization of the same Karman wake, with alternating red and blue rotation behind the obstacle.">
    <figcaption>Signed vorticity</figcaption>
  </figure>
</div>

The three views show the same paused state. Smoke makes transport visible, velocity arrows expose the vector field carrying it, and signed vorticity separates clockwise from counterclockwise rotation in the wake.

### Why it is worth exploring

- It connects numerical techniques to immediate visual feedback.
- Multiple presets, including jet flow, a lid-driven cavity, and a Kármán vortex street, exercise the same solver under different conditions.
- The controls make it a useful test bench for comparing stability, sharpness, and performance choices.

Begin with the grid and simulation-step code, then trace how the visualization modes turn solver fields into something inspectable.
