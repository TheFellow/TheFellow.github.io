---
title: "From Groups to ECDSA: Teaching Elliptic-Curve Cryptography from First Principles"
date: 2026-07-24 00:15:00 -0700
permalink: /notes/teaching-elliptic-curve-cryptography/
excerpt: "How I structured a StrongDM presentation to build ECDSA from groups, finite fields, and elliptic-curve point arithmetic."
tags: ["Cryptography", "ECDSA", "Mathematics", "Teaching"]
---

Cryptography talks often start at one of two unhelpful altitudes. They either stay at the API level, where signing and verification remain black boxes, or begin with enough notation to lose anyone who has not recently studied abstract algebra.

For an internal presentation at StrongDM, I wanted a route between those extremes. The goal was not to teach people to implement cryptography. It was to make the structure underneath ECDSA understandable: what the objects are, which operations are allowed, where the asymmetry comes from, and why a verifier can check a signature without learning the private key.

The slides built that argument one layer at a time.

## Start with an operation, not a curve

Elliptic-curve cryptography depends on groups, but opening a talk with the formal definition of a group makes the subject feel more remote than it is. I started with familiar operations and then named the properties we needed.

A group is a set with an operation that has four useful guarantees:

1. combining two members produces another member of the set;
2. the order of evaluation does not change the result;
3. an identity leaves a value unchanged; and
4. every value has an inverse that returns it to the identity.

The integers under addition already provide most of the intuition. Zero is the identity, the inverse of `5` is `-5`, and repeated addition gives scalar multiplication. The vocabulary is abstract, but the behavior is ordinary.

That framing mattered for the rest of the presentation. Once the audience understood that a group is a collection of values with predictable rules for combining them, elliptic-curve points could become another example rather than a leap into unfamiliar mathematics.

## Move arithmetic into a finite field

Cryptographic curves do not use the smooth, continuous number line shown in the familiar curve diagrams. Their coordinates live in a finite field.

For a prime `p`, arithmetic in the field `F_p` wraps modulo `p`. Addition, subtraction, and multiplication stay inside a finite set of values. Division is multiplication by a modular inverse. Every nonzero value has such an inverse because `p` is prime.

This is the point where modular arithmetic stops being a programming trick and becomes part of the design. The field gives us a finite space with enough algebraic structure to define point addition consistently.

A small example is easier to reason about than a production curve. Consider:

```text
y² = x³ + 2x + 2  (mod 17)
```

Only coordinate pairs from `0` through `16` are candidates. The equation selects a finite collection of points, including `(5, 1)`. There is no continuous arc between those points, but the same algebraic addition rules still apply.

<figure class="ecc-figure ecc-figure--square">
  <img src="{{ '/assets/images/notes/ecc/finite-field-curve.png' | relative_url }}" alt="The eighteen affine points satisfying y squared equals x cubed plus 2x plus 2 modulo 17, with the point G at 5 comma 1 highlighted.">
  <figcaption>The toy curve has eighteen affine points. Including the point at infinity gives a group of order nineteen.</figcaption>
</figure>

## Turn curve points into a group

Over the real numbers, the point-addition construction is visual. Draw a line through two points on the curve. It intersects the curve at a third point. Reflect that point across the horizontal axis, and the result is the sum.

The special cases complete the operation:

- a tangent line handles adding a point to itself;
- a vertical line sends a point and its inverse to the point at infinity; and
- the point at infinity acts as the identity.

<figure class="ecc-figure">
  <img src="{{ '/assets/images/notes/ecc/curve-addition.png' | relative_url }}" alt="A line through points P and Q intersects a real elliptic curve at negative P plus Q, which is reflected across the horizontal axis to obtain P plus Q.">
  <figcaption>Point addition is easiest to introduce geometrically: intersect, then reflect.</figcaption>
</figure>

Over a finite field, the picture becomes a set of dots, so the geometry is no longer something we literally draw between coordinates. The formulas survive. Slope, intersection, and reflection are computed with field arithmetic, including modular inverses.

This was the central transition in the slides. The points are not merely coordinates satisfying an equation. Together with point addition, they form a group. That gives us an identity, inverses, addition, and repeated addition, which is exactly the machinery public-key cryptography needs.

## Scalar multiplication creates the useful asymmetry

Choose a public base point `G` with a large prime order `n`. A private key is an integer `d`, and the corresponding public key is:

```text
Q = dG
```

Here `dG` means adding `G` to itself `d` times, although real implementations use much faster algorithms. Computing `Q` from `d` and `G` is efficient. Recovering `d` from `G` and `Q` is the elliptic-curve discrete logarithm problem.

That difference is the security boundary. The public key is a point everyone may know. The private key is the scalar that produced it. Properly selected curves and key sizes make recovering that scalar computationally infeasible with known classical methods.

By this stage, the audience had already seen every ingredient in the equation. The public-key construction did not require a new kind of object, only a new use for repeated group addition.

## ECDSA is arranged so verification reconstructs the same point

ECDSA adds a message hash and a fresh per-signature scalar. Let `z` be an integer derived from the message digest, and let `k` be a secret nonce selected for this signature.

Signing follows this outline:

1. Compute the point `R = kG`.
2. Let `r` be the x-coordinate of `R`, reduced modulo `n`.
3. Compute `s = k⁻¹(z + rd) mod n`.
4. Publish `(r, s)` as the signature.

Verification first computes `w = s⁻¹ mod n`, then:

```text
u₁ = zw mod n
u₂ = rw mod n
X  = u₁G + u₂Q
```

The signature is valid when the x-coordinate of `X`, reduced modulo `n`, equals `r`.

The formulas can look arbitrary until the substitutions are written out. Since `Q = dG`:

```text
X = zs⁻¹G + rs⁻¹dG
  = (z + rd)s⁻¹G
  = kG
```

The verifier reconstructs the same point the signer used without knowing either `d` or `k`. That cancellation was the destination of the presentation. Everything before it existed so that these few lines could be read as group arithmetic rather than magic.

<figure class="ecc-figure">
  <img src="{{ '/assets/images/notes/ecc/ecdsa-verification.png' | relative_url }}" alt="A flow diagram showing a private scalar producing a public point, signing producing r and s, and verification reconstructing the nonce point kG.">
  <figcaption>The public key and signature give the verifier enough information to reconstruct the nonce point, but not the private scalar.</figcaption>
</figure>

## The nonce is part of the secret

The private key is not the only value that must remain protected. The nonce `k` must be secret, unpredictable, and never reused with the same private key.

If two messages are signed with the same `k`, their signatures share enough algebraic structure to recover the nonce and then the private key. Biased or partially exposed nonces can also be dangerous. This is why production ECDSA implementations deserve the same scrutiny around randomness and side channels as they receive around curve selection.

It is also a useful engineering lesson. A value described as temporary may still carry the full security weight of a long-lived credential. Lifetime and sensitivity are different properties.

## What I wanted the slides to demonstrate

The talk was about more than one signature algorithm. It was an exercise in making a stack of abstractions earn its keep.

Each layer answered one question and introduced the vocabulary needed for the next:

- groups explained the required behavior of an operation;
- finite fields supplied a closed arithmetic system;
- elliptic curves supplied a useful group of points;
- scalar multiplication produced a public value from a private scalar; and
- ECDSA combined those pieces so a signature could be verified publicly.

Skipping a layer makes the final formula shorter to present but harder to understand. Spending time on every theorem has the opposite problem. The useful path is to preserve the dependency chain while choosing the smallest example that makes each dependency concrete.

That is the same approach I use when explaining software architecture. Start with the behavior a design needs, introduce the mechanism that provides it, and keep the connections visible. Good abstractions should compress an idea after it is understood, not hide the idea before it has been examined.

## The practical boundary

Understanding ECDSA is valuable. Implementing it for production is a separate matter.

Real cryptographic libraries must address constant-time operations, secure nonce generation, validation of points and parameters, serialization rules, malformed input, and many other details that a conceptual walkthrough intentionally omits. Application code should use maintained, reviewed implementations rather than translating the equations above.

For the complete specifications and a production API example, see:

- [NIST FIPS 186-5, Digital Signature Standard](https://csrc.nist.gov/pubs/fips/186-5/final)
- [SEC 1: Elliptic Curve Cryptography](https://www.secg.org/sec1-v2.pdf)
- [Go's `crypto/ecdsa` package](https://pkg.go.dev/crypto/ecdsa)
