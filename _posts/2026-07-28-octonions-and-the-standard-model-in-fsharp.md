---
title: "Octonions and the Standard Model in F#"
date: 2026-07-28 12:01:00 -0700
permalink: /notes/octonions-and-the-standard-model-in-fsharp/
excerpt: "An executable tour from non-associative octonion multiplication to a Furey-inspired eight-state particle pattern."
tags: ["F#", "Octonions", "Mathematical Physics"]
---

There is a familiar progression through the normed division algebras. The real numbers give way to complex numbers, then quaternions, then octonions. Each step doubles the dimension and gives up a familiar law: complex numbers cannot be ordered like the reals, quaternion multiplication is not commutative, and octonion multiplication is not associative.

The [complete F# gist](https://gist.github.com/TheFellow/55fd4f0d58275d8b21b8cc070da71633) turns that last loss into something executable. It starts with the octonion multiplication table, then follows a small part of Cohl Furey's algebraic approach toward the `1 + 3 + 3 + 1` pattern of one Standard Model generation.

## Build the multiplication table

An octonion has one real component and seven imaginary components. The gist stores those eight coefficients in an array and derives multiplication from seven oriented triples in the Fano plane:

```fsharp
let private fano =
    [| (1,2,3); (1,4,5); (1,7,6); (2,4,6);
       (2,5,7); (3,4,7); (3,6,5) |]
```

For a triple `(i,j,k)`, the orientation gives `e_i e_j = e_k`; reversing the order changes the sign. Together with `e_i² = -1`, those few rules fill the complete basis multiplication table.

Once multiplication is code, the unusual laws become tests rather than slogans. The script prints `e₁e₂` beside `e₂e₁`, compares `(e₁e₂)e₄` with `e₁(e₂e₄)`, and computes their associator. It then checks the weaker structure octonions retain: alternativity, the Moufang identities, and multiplicativity of the norm.

F# makes grouping unusually easy to see. The `*.` operator associates left and the `^*` operator associates right, so these two expressions use the same multiplication function but construct different syntax trees:

```fsharp
e1 *. e2 *. e4   // (e1 e2) e4
e1 ^* e2 ^* e4   // e1 (e2 e4)
```

For octonions, that is an observable distinction.

## Add complex coefficients

The next layer is the complexified octonions, `ℂ⊗𝕆`. The implementation represents an element as a real octonion plus an imaginary octonion. The external complex unit commutes with the octonion units, while octonion multiplication keeps its non-associative behavior.

From there the script introduces the idempotent

```text
ω = ½(1 + ie₇)
```

and three pairs of ladder operators. The annihilation operators kill `ω`; their conjugates act as creation operators. Applying zero, one, two, or three creation operators produces eight states:

```text
1 + 3 + 3 + 1
```

Because multiplication is non-associative, “apply one operator after another” must mean composed left multiplication: `a · (b · x)`. Replacing that chain with `(ab) · x` would silently change the construction. The parentheses are part of the model.

## Read charge from the number operator

The final step applies a number operator assembled from the ladder operators. Its eigenvalues on the eight states are `0`, `1`, `2`, and `3`, with multiplicities `1`, `3`, `3`, and `1`. Dividing by three gives the charge pattern used to label the states as a neutrino, three anti-down colors, three up colors, and a positron.

The satisfying part of the experiment is that those multiplicities and charges are computed from the algebra rather than stored in a lookup table. The program also checks the fermionic anti-commutation relations on a sample state, connecting the ladder-operator notation back to executable operations.

This script is a guided computational model, not a derivation of the full Standard Model. It does not construct all particles, interactions, gauge structure, or physical predictions. Its narrower value is to make a surprising mathematical proposal inspectable: the non-associativity of the octonions is not an obstacle to work around, but the feature that makes ordered operator composition meaningful.

