# ADR-0018 — Arcane Resonance is retired and replaced with a status spread

**Status:** accepted · **Ticket:** [#9](https://github.com/marcneuwirth/warweave/issues/9) · **Spec:** §9.3

## Context

The Magic doctrine granted "+25% duration on the **first** elemental status applied to each enemy". The ticket asked which reading of "first" was intended — first-*ever* per enemy, or first-*currently-active*.

**The question is moot: the doctrine is inert under both readings, for the same reason under each.** Duration is never the binding constraint. Every applier's cadence is shorter than the status it applies — a 1.8s frostbolt inside a 3s Chill, a 2.25s fireball inside a 4s Burning — so statuses self-refresh long before they expire, and +25% duration extends a resource already in surplus. Effect on Frozen uptime under either reading: **zero**.

## Decision

The reading question is **closed without an answer**. The doctrine is replaced, keeping the name:

> **Arcane Resonance (Magic 5).** An elemental status applied by your squads also applies to the nearest **other** enemy model within 2.5m of the target. The spread does not itself spread.

## Why replacement rather than retuning

Under exclusive doctrines ([ADR-0013](0013-doctrines-are-exclusive.md)) **an inert doctrine is worse than a weak one** — nobody would ever select it, so Magic 5 would buy literally nothing while Magic 2 buys a complete loop and a Magic/Beast hybrid buys the branch's ceiling.

The replacement doubles the branch's **footprint** rather than its damage, which is the doctrine layer's stated design constraint, and it **cannot be inert** because it scales with everything the branch does: Frozen output roughly doubles, Burning footprint roughly doubles.

Two alternatives were rejected. Cutting Hard-Control Immunity from 1.25s to 0.75s attacks the number that actually caps the branch, but **repeats this doctrine's own failure mode**: at one caster the *cadence* binds, not the immunity, so a player reaching Magic 5 with a single caster would see no change at all. Straight numeric amplification is exactly the "directly multiplying spell damage" the doctrine was written to avoid, and gives Magic 5 no new play.

## Consequences

- **A general lesson, recorded because it will recur:** a duration-extension effect is inert whenever the applying unit's cadence is shorter than the status duration — which it almost always is. Duration is a bad currency for an effect to be paid in.
- **Known blind spot, predicted rather than hidden:** the replacement does nothing against a single-model target, because there is no *other* model to spread to. That includes the showcase matchup the original spec was built around, which is carried as a named predicted outcome ([ADR-0041](0041-viability-band-and-crossover.md), spec §33.8).
