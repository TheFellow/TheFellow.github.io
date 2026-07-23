---
title: "fluid"
excerpt: "An interactive 2D fluid simulator and visualization playground written in Go."
language: "Go"
repository_url: "https://github.com/TheFellow/fluid"
---

<div class="project-meta"><span>Go</span><span>Simulation</span><span>Visualization</span></div>

[View the repository](https://github.com/TheFellow/fluid){: .btn .btn--primary }

fluid is an interactive Eulerian fluid simulation built on a staggered grid. It combines semi-Lagrangian advection with optional BFECC correction and exposes the solver through visual modes for smoke, pressure, velocity magnitude, and vorticity.

The interactivity is what turns the numerical method into an effective learning tool. Walls, forces, sources, sinks, particles, border conditions, and presets can all be changed while the simulation runs. Toggling BFECC or vorticity confinement makes tradeoffs such as numerical diffusion visible rather than leaving them buried in an equation or benchmark.

### Why it is worth exploring

- It connects numerical techniques to immediate visual feedback.
- Multiple presets—jet flow, a lid-driven cavity, and a Kármán vortex street—exercise the same solver under different conditions.
- The controls make it a useful test bench for comparing stability, sharpness, and performance choices.

Begin with the grid and simulation-step code, then trace how the visualization modes turn solver fields into something inspectable.

