# ADR-0008 — Command flows through two decoupled axes, and the round stake is conserved

**Status:** accepted · **Ticket:** [#6](https://github.com/marcneuwirth/warweave/issues/6) · **Spec:** §5.1, §5.3, §5.5

## Context

Making the stake an explicit function of the round number ([ADR-0007](0007-round-number-stake.md)) fixes match length and removes the decisiveness signal in the same move. Something has to carry that signal.

## Decision

The round stake splits **70% battle / 30% control objective**. Objective damage is dealt by **each player independently**, regardless of who won the battle:

> `objectiveDamage = 0.3 × S(round) × controlShare`

`controlShare` is **banked continuously while the battle is live**, never read as an end-of-battle snapshot.

## Why

**Conservation is what bounds match length.** Exactly `S(round)` leaves the table each round no matter how the two axes fall, so the worst case for length is perfect parity — every battle even, the point split 50/50 — which still reaches 0 on round 12. The bound is a property of the structure, not of tuning.

**Continuous banking is what keeps the axes decoupled.** A snapshot would hand the point to whoever won the fight — they have surviving squads and an empty field — collapsing the two axes back into one. Banking mid-battle means an army that dominates the point early keeps the credit even if it is subsequently destroyed.

**A battlefield objective carries the decisiveness signal better than the retired term ever did:** it is visible on the field, readable in the UI, and a *decision* rather than a derived statistic.

## Consequences

- Round loop step 8 changes from "the losing player takes Command damage" to "both players exchange Command damage".
- **Conservation is slightly overstated and this is recorded rather than repaired:** when *neither* player banks, 30% of the stake is simply never dealt. The bound survives — the never-banks stomp row lands at round 10, still inside range.
- Match length is therefore **structurally blind to the objective axis**: the total never moves, only the split. That blindness is why the objective needs its own three-number gate ([ADR-0040](0040-objective-three-numbers.md)).
