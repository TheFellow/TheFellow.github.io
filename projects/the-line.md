<!-- Generated from https://thefellow.github.io/projects/the-line/ by scripts/generate_llm_content.py; do not edit. -->

# the-line

Source: [https://thefellow.github.io/projects/the-line/](https://thefellow.github.io/projects/the-line/)

## Pyramid summary

- **~2 words:** Racing playground
- **~8 words:** Editable roads, car setups, and two-car racecraft experiments.
- **Expanded:** A racing-line playground in Go for reshaping corners, experimenting with car setup, and exploring two-car overtaking and defence.

## Full content

[View the repository](https://github.com/TheFellow/the-line)
[Read the build note](/notes/building-a-racing-line-playground.md)

The Line is a physics playground in the same spirit as [fluid](/projects/fluid.md): change something, watch the result, and use the picture to ask a better question. Here the questions are about corners. What happens if the exit opens up? Does more power help on this stretch? How much braking grip remains while the car is turning?

<figure class="article-figure">
  <img src="/assets/images/projects/the-line/club-loop.gif" alt="Qualifying with a reference ghost on Club Loop, followed by two-car over-under and pass/repass experiments." width="960" height="600">
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

The cars use illustrative quasi-static force limits, which makes the relationship between geometry, grip, and time easy to inspect. The [build note](/notes/building-a-racing-line-playground.md) follows that model through braking, axle balance, periodic laps, performance profiling, and the tactical planning and clearance checks behind racecraft.

Start with the repository's [quick start](https://github.com/TheFellow/the-line#readme), launch the viewer, and reshape the default esses.
