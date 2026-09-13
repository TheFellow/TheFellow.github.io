---
title: "Autonomous Semantic Porting with F#kYeah"
date: 2026-09-12 18:14:35 -0700
last_modified_at: 2026-09-12 18:14:35 -0700
permalink: /notes/autonomous-semantic-porting-with-fkyeah/
excerpt: "How I use F#kYeah across projects to analyze, implement, validate, and review semantic ports without a human in the execution loop."
icon: "route"
accent: "#f783ac"
tags: ["F#", "AI workflows", "Semantic porting", "Automation"]
---

I have used [F#kYeah]({{ '/projects/fkyeah/' | relative_url }}) across projects to run semantic ports autonomously, with no human in the execution loop. The workflow reads upstream changes, decides which behavior belongs in the target implementation, writes code, runs validation, and reviews the result. I define the contract and the workflow; the pipeline carries individual changes through it.

F#kYeah is my F# implementation of the [StrongDM Attractor specifications](https://github.com/strongdm/attractor). It executes workflows described as directed graphs in DOT. Semantic porting has become one of the most useful applications of that engine because it gives the automation a concrete source of change and a behavior to preserve.

## Keep an upstream behavioral contract

A [semport](https://factory.strongdm.ai/techniques/semport) carries intent and behavior between implementations. That can be an initial port or an ongoing relationship with an upstream project. The ongoing case is where I keep using F#kYeah: upstream continues to evolve, and the target needs to absorb relevant changes in its own language and architecture.

[cedar-dotnet](https://github.com/TheFellow/cedar-dotnet) follows Cedar's Go implementation. [Expr.NET](https://github.com/TheFellow/expr-dotnet) follows the Go Expr language. Both need to preserve observable semantics while exposing idiomatic C# APIs. A parser fix, diagnostic change, or newly handled edge case can matter even when the corresponding Go code has no direct C# equivalent.

Each upstream commit becomes a bounded question: what changed, does it affect this implementation, and which tests demonstrate the required behavior? Recording the answer in a ledger gives the next run a precise place to continue.

## Put the process in the graph

The DOT file describes stages and the conditions that connect them. Coding-agent stages inspect repositories and edit files. Tool stages run commands and expose their outcomes to routing. Review stages examine the implementation against the upstream source and tests. Failure and revision paths are part of the same graph.

The following is a simplified view of the Expr.NET workflow. Each repair path is bounded in the actual pipeline:

<figure class="article-figure">
  <img src="{{ '/assets/images/notes/fkyeah/semport-flow.svg' | relative_url }}" alt="F#kYeah semport flow: select an upstream commit, analyze it, then implement or review a proposed skip. Ports pass validation and agent review before being committed. Failed checks enter bounded repair paths; unresolved attempts preserve work and record failure evidence. Each recorded outcome leads to the next commit.">
  <figcaption>Agents interpret the change; commands measure the result. The graph connects them, including skip review and recovery paths. <a href="{{ '/assets/images/notes/fkyeah/semport-flow.svg' | relative_url }}">View the full-size diagram.</a></figcaption>
</figure>

This makes the maintenance process inspectable alongside the code. I can read the graph to see what happens after a failed build, where a proposed skip is challenged, and which checks precede a commit. Changes to that process can be versioned and reviewed like other repository changes.

## Make review and validation executable

In the [Expr.NET pipeline](https://github.com/TheFellow/expr-dotnet/blob/main/semport/semport.dot), a tool stage runs the repository's validation script. That script covers restore, formatting, a Release build, tests, and package creation. Separate agent stages review semantic faithfulness and proposed skips. The graph routes from those results without waiting for me to approve each step.

The ledger distinguishes implemented changes, acknowledged changes that need no port, and wedged attempts. An implemented entry follows validation and review. An acknowledgment requires evidence for the skip. A wedged attempt preserves the failed work in a recoverable Git stash and records what prevented completion. Those states give later runs and later investigation something concrete to work from.

Repository policy also belongs in the workflow. The [Cedar pipeline](https://github.com/TheFellow/cedar-dotnet/blob/main/semport/semport.dot) includes pushing completed changes. Expr.NET creates local commits and leaves publication to its surrounding repository workflow. F#kYeah executes the stages each project defines.

## Leave enough evidence to continue

Long-running maintenance needs durable progress. F#kYeah writes checkpoints and per-stage artifacts, including prompts, responses, status, and tool output. An interrupted run can resume from a checkpoint; a completed run leaves evidence of the decisions and commands that produced its changes.

The graph and ledger answer different questions. The graph describes the process. The ledger records which upstream changes have been handled. Stage artifacts explain what happened during a particular attempt. Together they make repeated autonomous runs practical to inspect and maintain.

That is why F#kYeah has kept finding a place in my projects. I can express the porting contract, validation commands, review criteria, and recovery paths once, then let the workflow carry upstream changes through them without my participation in each iteration.

The [F#kYeah repository](https://github.com/TheFellow/fkyeah) contains the engine and example graphs. The [Cedar porting note]({{ '/notes/porting-cedar-semantics-from-go-to-dotnet/' | relative_url }}) goes further into the conformance work that gives one of these workflows its behavioral contract.
