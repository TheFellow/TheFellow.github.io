<!-- Generated from https://thefellow.github.io/notes/type-safe-linear-algebra-in-fsharp/ by scripts/generate_llm_content.py; do not edit. -->

# Type-Safe Linear Algebra in F#

Source: [https://thefellow.github.io/notes/type-safe-linear-algebra-in-fsharp/](https://thefellow.github.io/notes/type-safe-linear-algebra-in-fsharp/)

## Pyramid summary

- **~2 words:** Typed dimensions
- **~8 words:** Phantom dimensions make invalid matrix arithmetic fail at compile time.
- **Expanded:** Using phantom dimensions and F# operators to make invalid matrix arithmetic fail at compile time.

## Full content

Matrix multiplication has a small but important precondition: the left matrix's column count must equal the right matrix's row count. Most compact matrix types store those dimensions only in their data, so an invalid multiplication remains possible until a runtime check rejects it.

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

The shared `'k` says that the inner dimensions must be the same. Multiplying a `Matrix<D2,D3>` by a `Matrix<D3,D4>` produces a `Matrix<D2,D4>`. Trying to multiply it by a `Matrix<D4,D2>` does not reach the loop that computes the result; the program does not type-check.

Transpose, addition, and vectors extend the same idea. Transpose swaps the two type parameters. Addition requires both operands to have the same pair. A column vector is simply a matrix with `D1` as its column dimension, so matrix-vector multiplication needs no separate rule.

## Let the expression preserve the proof

Custom operators make the examples read like their algebra. `*.` delegates to matrix multiplication, while `+.` delegates to addition:

```fsharp
let left = a *. b *. c
let av : Vec<D2> = a *. v
```

F# infers every intermediate dimension. In the first expression, `a *. b` must produce something that can be multiplied by `c`. In the second, the declared result type records that a 2-by-3 matrix maps a three-dimensional vector to a two-dimensional one.

The gist also uses the language's operator naming rules to make associativity visible. An operator beginning with `*` associates to the left, while one beginning with `^` associates to the right. Matrix multiplication is associative, so `(A B) C` and `A (B C)` produce the same answer when both are defined. The cross-product example at the end uses the same two spellings to show why grouping still matters for a non-associative operation: changing the operator changes the parse, and therefore the result.

## What this buys

This is not a full linear-algebra library. The constructors do not verify that the runtime array shape agrees with the phantom markers, and a production design would need to protect that boundary. The useful part is the shape of the API: validate once when constructing a value, then let function signatures preserve dimensional correctness through the rest of the computation.

The larger lesson is that a type parameter does not need runtime data to be useful. It can carry a fact from one operation to the next, turning a comment such as “these dimensions must agree” into a constraint the compiler enforces.
