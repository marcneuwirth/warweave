# ADR-0020 — A raid pushes through rather than fighting or evading, and attacks what physically blocks it

**Status:** accepted · **Ticket:** [#17](https://github.com/marcneuwirth/warweave/issues/17) · **Spec:** §23.6, §25

## Context

Once `Raid` exists ([ADR-0019](0019-raid-is-an-order-not-a-position.md)), what a raiding squad does when intercepted decides whether the objective is reachable at all.

## Decision

> A `Raid` squad **does not acquire targets and does not stop for them**. It attacks only enemy models physically obstructing its path — within its own reach and in the way — and resumes the moment the path clears. On arrival at the point it reverts to **`Hold`** and behaves normally.

A raid is therefore a two-phase order with one bit of state, and **there is no return trip** — a squad committed to a raid is committed for the round.

## Why

**Fighting normally en route** degenerates `Raid` into `Advance` with a different heading: raiders stop at the enemy line, fight, and the point is never touched.

**Evasion** was rejected on cost: movement is straight-line-toward-target with collision, and steering and avoidance is a genuinely new subsystem for one mechanic.

**The "attacks what blocks it" clause is load-bearing, not a detail.** With no terrain, enemy models are the only obstruction in v0.4. A raider that could not attack would be body-blocked permanently by one cheap squad parked on the lane, and the objective would be uncapturable for a second time — and screening would go from "a real decision" to an auto-win button.

**Reverting to Hold on arrival** rather than staying in raid behaviour: a squad that will not acquire targets sits next to a defending ranged squad being shot and never shoots back — unreadable, and it makes the point trivially defensible by anything ranged.

**The destination is the point itself**, not the nearest spot within 8m of it. Under the latter a wide squad stops at the radius edge with half its models outside, and a partial-contribution rule is immediately owed. Walking to the point and packing around it under collision makes the 8m radius a pure **scoring** test that movement never reasons about.

## Consequences

- **Interception bleeds a raid; it does not cancel it.** Raiders cross ~44m eating fire they never answer — a ranged squad shooting them from outside their path gets a free ride. That is the price of the order, it is readable on the field, and it is what makes the 400g threshold bite.
- **Screening a raid is collisional, not perceptual.** Raiders select no targets, so the `Exposed` check is blind to them and a screen must stand *on* the lane rather than near it. Reusing the 4m `Exposed` corridor was rejected: a 4m corridor across 44m of travel is nearly impossible to keep clear, so every raid would convert to an `Advance` at first contact — the degenerate case arriving through a different door.
- **An honest "no" to the primitive-set challenge.** There is no movement-destination primitive, and "suppress acquisition, attack only obstructions" is not a target-priority modifier. The cost is **one new movement mode, not a subsystem** — it reuses machinery `Advance` already required, substituting a constant coordinate with no pathfinding.
