---
title: "fluid"
date: 2026-07-23 12:03:42 -0700
last_modified_at: 2026-07-24 15:15:38 -0700
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

Live controls turn the numerical method into an effective learning tool. Walls, forces, sources, sinks, particles, border conditions, and presets can all be changed while the simulation runs. Toggling BFECC or vorticity confinement exposes tradeoffs such as numerical diffusion directly in the simulation.

### Why it is worth exploring

- It connects numerical techniques to immediate visual feedback.
- Multiple presets, including jet flow, a lid-driven cavity, and a Kármán vortex street, exercise the same solver under different conditions.
- The controls make it a useful test bench for comparing stability, sharpness, and performance choices.

Begin with the grid and simulation-step code, then trace how the visualization modes turn solver fields into something inspectable.
