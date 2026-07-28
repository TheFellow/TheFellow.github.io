---
title: "Type-Safe Linear Algebra in F#"
date: 2026-07-28 12:00:00 -0700
permalink: /notes/type-safe-linear-algebra-in-fsharp/
excerpt: "Using phantom dimensions and F# operators to make invalid matrix arithmetic fail at compile time."
tags: ["F#", "Linear Algebra", "Type Systems"]
math: true
---

Matrix multiplication has a small but important precondition. If $A \in \mathbb{R}^{m \times n}$ and $B \in \mathbb{R}^{p \times q}$, then the product $AB$ exists only when $n=p$, in which case

$$
AB \in \mathbb{R}^{m \times q}.
$$

Most compact matrix types store those dimensions only in their data, so an invalid multiplication remains possible until a runtime check rejects it.

The [complete F# gist](https://gist.github.com/TheFellow/4cb72a3dbce7ad0c4033054ecf38c496) is an experiment in moving that check into the type system. It is deliberately small—just enough matrix arithmetic to show where types can carry the proof.

## Dimensions that occupy no space

The example begins with four marker types, `D1` through `D4`, and a matrix whose row and column dimensions are type parameters:

```fsharp
type Matrix<'rows, 'cols> = { Data: float[,] }
type Vec<'n> = Matrix<'n, D1>
```

These are phantom dimensions. A value of `D2` is never stored in a matrix, and the runtime representation is still a two-dimensional array. The markers exist only while the compiler checks the program.

That makes the signature of multiplication do the interesting work:

```fsharp
let mul (a: Matrix<'r,'k>)
        (b: Matrix<'k,'c>) : Matrix<'r,'c>
```

The shared `'k` says that the inner dimensions must be the same. At the type level, the function encodes

$$
\mathbb{R}^{r \times k} \times \mathbb{R}^{k \times c}
\longrightarrow \mathbb{R}^{r \times c}.
$$

Multiplying a `Matrix<D2,D3>` by a `Matrix<D3,D4>` produces a `Matrix<D2,D4>`. Trying to multiply it by a `Matrix<D4,D2>` does not reach the loop that computes the result; the program does not type-check.

Transpose, addition, and vectors extend the same idea. Transpose witnesses $\mathbb{R}^{r \times c} \to \mathbb{R}^{c \times r}$. Addition requires both operands to inhabit the same $\mathbb{R}^{r \times c}$. A column vector is simply a matrix with `D1` as its column dimension, so matrix-vector multiplication needs no separate rule.

## Let the expression preserve the proof

Custom operators make the examples read like their algebra. `*.` delegates to matrix multiplication, while `+.` delegates to addition:

```fsharp
let left = a *. b *. c
let av : Vec<D2> = a *. v
```

F# infers every intermediate dimension. In the first expression, `a *. b` must produce something that can be multiplied by `c`. In the second, the declared result type records the linear map

$$
A : \mathbb{R}^{3} \longrightarrow \mathbb{R}^{2}.
$$

The gist also uses the language's operator naming rules to make associativity visible. An operator beginning with `*` associates to the left, while one beginning with `^` associates to the right. Matrix multiplication is associative,

$$
(AB)C = A(BC),
$$

so both parses produce the same answer when their dimensions fit. The transpose example similarly checks the contravariant reversal

$$
(AB)^{\mathsf T}=B^{\mathsf T}A^{\mathsf T}.
$$

The cross-product example at the end uses the same two operator spellings to show why grouping still matters for a non-associative operation: in general,

$$
(\mathbf u \times \mathbf v) \times \mathbf w
\ne
\mathbf u \times (\mathbf v \times \mathbf w).
$$

Changing the operator changes the parse, and therefore the result.

## What this buys

This is not a full linear-algebra library. The constructors do not verify that the runtime array shape agrees with the phantom markers, and a production design would need to protect that boundary. The useful part is the shape of the API: validate once when constructing a value, then let function signatures preserve dimensional correctness through the rest of the computation.

The larger lesson is that a type parameter does not need runtime data to be useful. It can carry a fact from one operation to the next, turning a comment such as “these dimensions must agree” into a constraint the compiler enforces.
