<!-- Generated from https://thefellow.github.io/projects/the-line/ by scripts/generate_llm_content.py; do not edit. -->

# the-line

Source: [https://thefellow.github.io/projects/the-line/](https://thefellow.github.io/projects/the-line/)

## Pyramid summary

- **~2 words:** Racing playground
- **~8 words:** Editable roads and car setups make racing physics visible.
- **Expanded:** A racing-line playground in Go for reshaping corners, experimenting with car setup, and watching the physics change a lap.

## Full content

[View the repository](https://github.com/TheFellow/the-line)
[Read the build note](/notes/building-a-racing-line-playground.md)

The Line is a physics playground in the same spirit as [fluid](/projects/fluid.md): change something, watch the result, and use the picture to ask a better question. Here the questions are about corners. What happens if the exit opens up? Does more power help on this stretch? How much braking grip remains while the car is turning?

<figure class="article-figure">
  <img src="/assets/images/projects/the-line/club-loop.gif" alt="A GT car and its reference ghost circulating around Club Loop, with their speed traces below." width="960" height="600">
  <figcaption>Club Loop, one of twelve fictional tracks. The ghost shows a reference run while the chart compares speeds at matching positions along the road.</figcaption>
</figure>

A native Ebitengine viewer exposes editable track geometry, banking, elevation, surfaces, kerbs, and car setup. Smooth candidate lines are evaluated against tyre-force limits, then checked on a finer road mesh. The model includes power, drag, axle drive split, and optional brake bias, downforce, longitudinal load transfer, and tyre load sensitivity.

### Things to try

- Pin a reference, change grip or power, and compare the speed traces and elapsed-time delta.
- Drag a corner wider or change its banking, then watch the line and braking points move.
- Author a line with lateral handles and compare your idea with the searched result.
- Switch between plan, elevated, and perspective views, or export a PNG, GIF, or CSV from the CLI.

The cars use illustrative quasi-static force limits, which makes the relationship between geometry, grip, and time easy to inspect. The [build note](/notes/building-a-racing-line-playground.md) follows that model through braking, axle balance, periodic laps, and the profiling work that made repeated experiments faster.

Start with the repository's [quick start](https://github.com/TheFellow/the-line#readme), launch the viewer, and reshape the default esses.
