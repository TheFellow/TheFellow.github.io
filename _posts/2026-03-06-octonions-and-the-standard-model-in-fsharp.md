---
title: "Octonions and the Standard Model in F#"
date: 2026-03-06 18:10:26 -0800
permalink: /notes/octonions-and-the-standard-model-in-fsharp/
excerpt: "An executable tour from non-associative octonion multiplication to a Furey-inspired eight-state particle pattern."
tags: ["F#", "Octonions", "Mathematical Physics"]
math: true
---

There is a familiar progression through the normed division algebras:

$$
\mathbb{R} \subset \mathbb{C} \subset \mathbb{H} \subset \mathbb{O}.
$$

Each step doubles the dimension and gives up a familiar law. The complex numbers cannot be ordered like the reals, quaternion multiplication is not commutative, and octonion multiplication is not associative. Hurwitz's theorem says the chain ends here: these are the only finite-dimensional normed division algebras over $\mathbb{R}$.

The [complete F# gist](https://gist.github.com/TheFellow/55fd4f0d58275d8b21b8cc070da71633) turns that last loss into something executable. It starts with the octonion multiplication table, then follows a small part of Cohl Furey's algebraic approach toward the $1+3+3+1$ pattern of one Standard Model generation.

## Build the multiplication table

An octonion has one real component and seven imaginary components. The gist stores those eight coefficients in an array and derives multiplication from seven oriented triples in the Fano plane:

```fsharp
let private fano =
    [| (1,2,3); (1,4,5); (1,7,6); (2,4,6);
       (2,5,7); (3,4,7); (3,6,5) |]
```

For an oriented triple $(i,j,k)$, the rule is

$$
e_i e_j=e_k, \qquad e_j e_i=-e_k,
$$

with cyclic permutations preserving the sign. Together with $e_i^2=-1$, those few rules fill the complete basis multiplication table.

Once multiplication is code, the unusual laws become tests rather than slogans. The script prints $e_1e_2$ beside $e_2e_1$, compares $(e_1e_2)e_4$ with $e_1(e_2e_4)$, and computes their associator

$$
[a,b,c] = (ab)c-a(bc).
$$

It then checks the weaker structure octonions retain: alternativity, the Moufang identities, and multiplicativity of the norm,

$$
\lVert ab\rVert=\lVert a\rVert\,\lVert b\rVert.
$$

F# makes grouping unusually easy to see. The `*.` operator associates left and the `^*` operator associates right, so these two expressions use the same multiplication function but construct different syntax trees:

```fsharp
e1 *. e2 *. e4   // (e1 e2) e4
e1 ^* e2 ^* e4   // e1 (e2 e4)
```

For octonions, that is an observable distinction.

## Add complex coefficients

The next layer is the complexified octonions, $\mathbb{C}\otimes\mathbb{O}$. The implementation represents an element as $a+ib$, where $a,b\in\mathbb{O}$. The external complex unit commutes with the octonion units, while octonion multiplication keeps its non-associative behavior:

$$
(a+ib)(c+id)=(ac-bd)+i(ad+bc).
$$

From there the script introduces the idempotent

$$
\omega=\frac{1}{2}(1+ie_7), \qquad \omega^2=\omega,
$$

and three pairs of ladder operators $\alpha_k,\alpha_k^\dagger$. The annihilation operators kill the vacuum, $\alpha_k\omega=0$, while their conjugates act as creation operators. Applying zero, one, two, or three creation operators produces

$$
\binom{3}{0}+\binom{3}{1}+\binom{3}{2}+\binom{3}{3}
=1+3+3+1=8
$$

states.

Because multiplication is non-associative, “apply one operator after another” must mean composed left multiplication:

$$
L_a\!\left(L_b(x)\right)=a(bx) \ne (ab)x=L_{ab}(x)
$$

in general. The parentheses are part of the model.

## Read charge from the number operator

The final step applies the number operator assembled from the ladder operators,

$$
N(x)=-\sum_{k=1}^{3}\alpha_k^\dagger\!\left(\alpha_k(x)\right).
$$

Its eigenvalues on the eight states are $0,1,2,3$, with multiplicities $1,3,3,1$. With $Q=N/3$, the resulting spectrum is

$$
\begin{array}{c|c|c}
\text{multiplicity} & Q & \text{particle label} \\
\hline
1 & 0 & \nu \\
3 & \tfrac{1}{3} & \bar d_r,\bar d_g,\bar d_b \\
3 & \tfrac{2}{3} & u_r,u_g,u_b \\
1 & 1 & e^+
\end{array}
$$

The satisfying part of the experiment is that those multiplicities and charges are computed from the algebra rather than stored in a lookup table. The program also checks the fermionic anti-commutation relations on a sample state, connecting the ladder-operator notation back to executable operations.

This script is a guided computational model, not a derivation of the full Standard Model. It does not construct all particles, interactions, gauge structure, or physical predictions. Its narrower value is to make a surprising mathematical proposal inspectable: the non-associativity of the octonions is not an obstacle to work around, but the feature that makes ordered operator composition meaningful.
