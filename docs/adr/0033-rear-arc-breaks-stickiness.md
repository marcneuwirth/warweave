# ADR-0033 — Rear-arc damage breaks target stickiness once, re-acquiring the nearest squad, with a 4s lockout

**Status:** accepted · **Ticket:** [#12](https://github.com/marcneuwirth/warweave/issues/12) · **Spec:** §23.2, §24.1

## Context

Flanking ([ADR-0032](0032-flanking-is-geometric.md)) is inert without an answer to *what makes a squad turn*. Facing follows the current target and targeting is sticky, so **a squad fighting A never rotates while A lives, and a flanker behind it flanks forever at no cost**. That is a worse outcome than no flanking at all.

## Decision

> Rear-arc damage **breaks stickiness once**. The squad re-acquires the **nearest enemy squad** — which may or may not be the attacker — and then **cannot re-acquire again for 4 seconds**.

## Why each clause

- **Breaking on rear-arc damage** is what creates the trade. You get hit from behind, you wheel to answer (1.5s of not attacking at 120°/s), and the squad that was pinning you frontally is now in *your* rear arc. Being caught on two bearings is a real punish with a real counterplay: don't be pincered, or screen the second bearing.
- **Nearest, not the attacker.** This is the `Hold`-breaking precedent applied unchanged — chasing the specific attacker would let the enemy dictate the player's target selection. It also closes a concrete abuse: a cheap ranged squad plinking from 20m is never nearest, so it can never steal a squad's facing, while a pack in contact behind you **is** nearest, so it does. The rule fires exactly where the pincer is real.
- **The 4s lockout** prevents a spin lock. Without it, two cheap squads on opposite bearings paralyse anything — face A, B flanks, turn to B, A flanks, wheel forever, deal nothing. With it, wheeling costs 1.5s of a 4s commitment and the flank you conceded is *supposed* to hurt.

## The line this crosses, and why it survives

`Hold` breaking refused to let the enemy dictate **where a squad walks**, because that surrenders position irreversibly. This lets them dictate **which way it looks** — and the exposure is symmetric, since turning to answer B is exactly what hands A the flank. **Nobody gets a free ride**, which is the property the earlier refusal was protecting.

## Consequences

- **Target stickiness is no longer unconditional**, so §24 has to say so, and the kernel must expose facing geometry to the damage pipeline. Both land in P0.
- Together with `Hold` breaking, the player's formation can now be moved by the opponent in two ways. The failure mode — that this reads as *the opponent yanking your formation around* rather than as clever combined arms — is an explicability risk, and it is exactly what the positioning matchups are specified to test.
