<!-- Generated from https://thefellow.github.io/projects/fluid/ by scripts/generate_llm_content.py; do not edit. -->

# fluid

Source: [https://thefellow.github.io/projects/fluid/](https://thefellow.github.io/projects/fluid/)

## Pyramid summary

- **~2 words:** Fluid simulation
- **~8 words:** An interactive Go playground for exploring two-dimensional Eulerian fluid dynamics.
- **Expanded:** An interactive 2D fluid simulator and visualization playground written in Go.

## Full content

[View the repository](https://github.com/TheFellow/fluid)

fluid is an interactive Eulerian fluid simulation built on a staggered grid. It combines semi-Lagrangian advection with optional BFECC correction and exposes the solver through visual modes for smoke, pressure, velocity magnitude, and vorticity.

Live controls turn the numerical method into an effective learning tool. Walls, forces, sources, sinks, particles, border conditions, and presets can all be changed while the simulation runs. Toggling BFECC or vorticity confinement exposes tradeoffs such as numerical diffusion directly in the simulation.

### Why it is worth exploring

- It connects numerical techniques to immediate visual feedback.
- Multiple presets, including jet flow, a lid-driven cavity, and a Kármán vortex street, exercise the same solver under different conditions.
- The controls make it a useful test bench for comparing stability, sharpness, and performance choices.

Begin with the grid and simulation-step code, then trace how the visualization modes turn solver fields into something inspectable.
