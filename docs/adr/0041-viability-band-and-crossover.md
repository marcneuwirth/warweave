# ADR-0041 — Category viability is a two-sided 35/65 band on a round-indexed matrix

**Status:** accepted · **Ticket:** [#13](https://github.com/marcneuwirth/warweave/issues/13) · **Spec:** §29

## Context

The full-build section required that "at least one representative build from every category should be capable of winning competitive matches" — a **one-sided** gate. But the actual finding from the matchup work is a **top** failure: one category beating every other category outright, which **nothing in the spec prohibits**.

Separately, once deep-versus-wide was relocated onto the **time axis** ([ADR-0026](0026-deep-wide-is-temporal.md)), a single equal-spend snapshot became structurally incapable of observing the claim. It reads one moment.

## Decision

> A category is **viable** if its win rate over the sweep is **≥ 35%**, and **no category exceeds 65%**.

> The 7 × 7 category matrix is **round-indexed at R3 / R5 / R8**: deep categories lead at R3; wide categories close or reverse by R8. **Identical ordering at all three snapshots means the tension is not present**, whatever the final numbers look like.

> **Representative builds are derived, not authored** — rolled forward from the reference purchase policy under each category constraint.

## Why

**Two-sided** because both violations are present on today's numbers — one category below the floor and another above the ceiling — and only one of them was previously nameable as a failure.

**Round-indexed** because it is the **first instrument on the map that separates *mispriced* from *not yet load-bearing***, which the doctrine weighing asked for and could not settle on paper. Flat ordering means mispriced; a crossover that exists but is small means the "underwritten by a later ceiling rise" defence holds. R3/R5/R8 are dials, argued from the first doctrine landing at R3 and the convergent build at ~R7.

**Derived builds** hold the versioned-artifact count at two and buy consistency: the builds graded here are the builds the liveness instrument reasons about, rather than two authored sets that can silently disagree.

## Consequences

- The same round indexing serves the round-dependent positioning decision, which is scored at the same snapshots — no third artifact and no fourth sweep. **If the optimal choice is identical at all three, the claim that a round-dependent positioning decision exists is withdrawn** rather than asserted.
- The predicted convergent build is run as a named benchmark column alongside the seven categories.
- On the roster as shipped this gate is **predicted to fail six of seven categories**, which is carried openly in the predicted-outcome column rather than being smoothed over ([ADR-0042](0042-no-threshold-without-n.md)).
