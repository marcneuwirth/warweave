# ADR-0022 — A battle ends on a wipe or at 90s with a bounded 20s pursuit; and `Hold` breaks under fire it cannot answer

**Status:** accepted · **Ticket:** [#17](https://github.com/marcneuwirth/warweave/issues/17) · **Spec:** §5.4, §23.3

## Context

Two rules the spec never wrote down, both forced open by the objective.

**1. What ends a battle.** §5 defined only the 90s timeout. It never stated that destroying the enemy army ends the battle — which did not matter until post-wipe time became scoreable.

**2. What `Hold` does under fire it cannot answer.** *"Hold squads remain on their deployed position"*, read literally, means a screen at 32m from a reach squad stands still and dies without ever swinging. **Out-ranging a screen is therefore free** — a zero-risk delete.

## Decision

> A battle ends when a player has **no surviving models**, or at **90 simulated seconds**, whichever comes first. On a wipe, a **pursuit phase** runs: surviving squads with nothing left to fight move to the enemy control point under `Raid` travel rules and bank what they can. The battle ends at **wipe + 20s**, or at 90s. `controlShare`'s denominator is the full duration including pursuit.

> A `Hold` squad **breaks** — converting to `Advance` for the remainder of the battle — when it takes damage while **no model in it is `Engaged`** *and* **it has no valid target within its own weapon range**. A squad within 8m of **either** control point does not break.

## Why the pursuit window is bounded

A wipe at 30s pays the victor ≈20% of the control axis: *you earned the field, and you had time to walk onto their point before the round closed.* Not nothing, not a sweep.

Running to 90s uncapped hands the victor 50%+ on top of full battle damage — the end-of-battle snapshot that continuous banking exists to prevent, arriving through the back door — plus up to 70s of dead clock. Ending the battle on the survivor's *arrival* is theatre with no payoff.

**The cost, stated plainly:** the loser's earlier raid is diluted, since `controlShare` divides by total duration. The dilution is smaller than it looks, because a wipe means *all* of a player's models are dead, raiders included — pursuit only ever dilutes banking that had already stopped. **20s is the only arbitrary constant here and it is a dial**, and it is given an instrument in [ADR-0040](0040-objective-three-numbers.md).

## Why `Hold` breaks, with those exact conditions

- **`Engaged` is reused, not reinvented** — a squad already in a fight does not abandon it.
- **"No valid target in range" extends past melee** — a squad out-ranged by anything, melee or not, also breaks. Same logic: it cannot answer.
- **Breaking is permanent for the battle**, or it oscillates: charge, reach range, stop, get out-ranged, charge again.
- **A broken squad converts to `Advance`; it does not chase its attacker.** Chasing would let the enemy dictate the player's target selection, which is a genuine §24 violation unlike `Raid`.
- **The control-point exemption is principled, not a patch.** The break rule's premise is *taking damage you cannot answer while accomplishing nothing*, and a squad banking or contesting control is accomplishing something. Without it, one cheap ranged squad parked outside the radius peels raiders off the point — or a garrison off its own — without ever contesting it, and the objective becomes free to deny. **A point cannot be denied from outside its radius.**

**Literal Hold** was rejected despite being defensible (out-ranging is legitimate counterplay) because it makes free deletion the dominant line. **Unconditional breaking** was rejected because a screen that abandons its charge the instant anyone shoots is not a commitment.

## Consequences

- **What this buys:** out-ranging a screen becomes a trade, and the degenerate case becomes a real combined-arms play — *shoot the screen to peel it, dive the exposed backline*. Two squads and a plan.
- **A raid outlives the line.** If the main army collapses but raiders are alive on the enemy point, there is no wipe — the enemy must march 44m to dig them out while the raiders bank.
- `Hold` constrains **position, not action**: a Hold squad still rotates to face its target and still attacks anything in reach.
- Match-length bounds re-verified with pursuit: a pure-battle stomp moves from R10 to R9, still inside 8–12.
