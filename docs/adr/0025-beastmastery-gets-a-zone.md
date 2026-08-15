# ADR-0025 — Beastmastery keys on a zone, not on a melee state

**Status:** accepted · **Ticket:** [#10](https://github.com/marcneuwirth/warweave/issues/10) · **Spec:** §10.2

## Context

Beastmastery originally read: *"Beast units deal +15% damage against enemies currently engaged in melee by a Military squad."* Under the branch denotation rule ([ADR-0023](0023-branch-denotation-and-purchase-time-stamping.md)) and the operational definition of `Engaged` (hit by a squad's **melee** attack within 2.0s), that had **exactly one trigger in the game** — the Military line — because the branch's other unit type at the time was a long-ranged squad with no melee profile at all.

Worse, it was anti-synergistic. The Military line's identity is standing still; the Beast pack's identity is selecting *past* the line. **The Beast half was built to attack the models the Military half cannot be engaging.**

## Decision

> **Beastmastery (Mil 3 + Beast 3).** Beast-branch attacks deal **+15%** damage against enemies within **6m** of an allied Military-branch squad.

6m reuses the Military doctrine's existing coherence radius rather than inventing a second number.

## Why a positional predicate specifically

The structural problem is sharper than a wording fix can reach: **Military's identity is the line and Beast's is explicitly the backline** — the culling rewrite ([ADR-0024](0024-apex-instinct-rebuilt-and-culling.md)) makes access units track the *lowest-total-HP* squad by rule. The two branches are **designed to want different targets**, so any repair phrased as "both hit the same thing" fights both units' own rules. A zone is projected by **position** rather than by target agreement, which is the only shape that survives that.

Alternatives rejected:

- *"Engaged **or attacked** by a Military squad within 2s"* would let a ranged Military squad designate and the pack follow — but the player cannot order targeting, and the culling rule makes convergence *less* likely, not more.
- *"While an allied Military squad is Engaged"* is reliable, but it is a flat buff in a costume: no play, no positioning decision.
- *Dropping the branch word* ("engaged by any allied squad") makes a 100-gold Common screen the enabler, which the denotation ruling explicitly rejected.

## Consequences

- Longbowmen and every other Military-branch squad now count, and Brace stops being a liability to its own hybrid.
- **This is where deep-versus-wide becomes mechanical.** Beast 5 sends the pack past the line and collapses Beastmastery's uptime; Mil 3 + Beast 3 wants the pack fighting alongside it. **The two Beast payoffs pull against each other by design**, expressed as geometry rather than as a rule — which is a positioning tension, where player influence is supposed to live.
