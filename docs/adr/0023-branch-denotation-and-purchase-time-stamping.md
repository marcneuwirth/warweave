# ADR-0023 — A branch name denotes the `branch` property, never a damage type — and investment is stamped at purchase

**Status:** accepted · **Ticket:** [#16](https://github.com/marcneuwirth/warweave/issues/16) · **Spec:** §6.2, §22.5

## Context

"Military attacks deal +15% against Burning, Chilled or Frozen enemies" has two readings: **Military-branch unit types**, or **all physical attacks**. The spec had no rule for which *units* count as Military, because affinity is defined as investment rather than as unit membership. The same ambiguity recurs on every rule that names a branch, on both the attacker and the target side.

This decision carries two rulings together — what a branch word means, and what it must never retroactively mean. They are one decision seen from two sides, and splitting them would let a future reader adopt the first without the second, which is precisely how the affinity pump returns.

## Decision

> **Wherever a rule names a branch, it denotes the `branch` property of the unit type of the model in question — attacker, ally or target alike. Common unit types match none of the three tracks. A branch name never denotes damage type, and damage type never implies a branch.**

**Common becomes the fourth value of a total, single-valued `branch` property**, superseding the earlier glossary ruling that Common is "not a branch".

**Forward invariant:** `branchInvestment` is **stamped at purchase** — gold is credited to the branch the unit type held when it was spent, and nothing later moves it. Reclassification is a set-valued **counts-as membership**, evaluated live for rules reads only, never a branch swap.

## Why the branch reading

- The damage-type reading fires on **nine of eleven attack profiles**, including both unit types of the branch the hybrid does *not* involve. A Military+Magic hybrid buffing Beast attacks is incoherent on its face.
- It lands a 1,200-gold two-branch reward on the 100-gold Common swarm, *better per gold* than on the units the hybrid is named for, when the affinity rules are explicit that Common generates no investment.
- It is not cosmetic against the predicted convergent build: a 5/3/3 player's Magic setup would silently buff their own Common screen.

**Common as a fourth value** rather than a null: a null forces a null case into every rule that reads branch, forever, and Common is already a real category doing real work with its own technology list. The gain is that "generates no branch investment" becomes a stated rule rather than an artefact of a null.

## Why purchase-time stamping, now

The obvious next design move is a technology making Common units *count as* Military. If branch is simply mutable and investment is derived from branch, then: buy six Common squads over R1–R4 (600g, generating nothing), buy the reclassification technology in R5, and 600 gold of past spending relocates — **+3 affinity for the price of one technology**, on the cheapest gold in the game. Declaring branch immutable and forbidding the move was rejected in favour of keeping the design available under a safe shape.

## Consequences

- The rule reaches doctrines, hybrid unlocks and target-side technology predicates alike. **The spec spells out "Military-branch" / "Beast-branch" explicitly** rather than relying on the reader having internalised the rule — the rule is the law, the explicit wording is what stops it being re-litigated.
- **Common is excluded from the rewards, not the systems**: a Common technology can create Burning that a hybrid then cashes on somebody else. Accepted as a good shape.
- Two defects exposed and *not* fixed here, because fixing them is rebalancing rather than denotation: the Military/Beast hybrid was triggerable by exactly one unit type, and the Military doctrine silently requires two Military-branch squads. Both were routed to the doctrine weighing ([ADR-0025](0025-beastmastery-gets-a-zone.md), [ADR-0026](0026-deep-wide-is-temporal.md)).
