# ADR-0026 — Deep and wide are separated on the time axis; hybrids keep stacking while doctrines do not

**Status:** accepted, later extended by [ADR-0043](0043-rotation-a.md) · **Ticket:** [#10](https://github.com/marcneuwirth/warweave/issues/10) · **Spec:** §8

## Context

The six payoffs — three doctrines, three hybrid unlocks — are not comparable in power: the spread is roughly **60×**. But the diagnosis is not mispricing.

Calibrated against measured flips (+39% flips a matchup, +11% never decides anything, <5% is inert), **four of the six sit below the level that never decides anything**: the Military doctrine at +8.4% eHP is beneath a 250-gold technology, one hybrid at +1.5%, and two at zero. Meanwhile the composition choice they are supposed to modulate swings a matchup record from 9–0 to 0–9. **The riders are one to two orders of magnitude beneath the noise.**

**The ticket's own framing was also wrong, and the reframe is the finding.** Nobody pays 1,000 gold for a doctrine — they pay 1,000 gold for squads they wanted anyway, and the doctrine arrives as a rider on spending already justified. **The marginal gold cost of deep-versus-wide is zero**, so the only like-for-like comparison is one doctrine against one hybrid.

## Decision

**Two of the six were *broken* rather than small and were repaired** ([ADR-0024](0024-apex-instinct-rebuilt-and-culling.md), [ADR-0025](0025-beastmastery-gets-a-zone.md)). The rest stay small **on purpose**, and §8 is rewritten to say so:

> The tension between deep and wide is **temporal, not magnitudinal.** **Deep pays first** — Affinity 5 by round 3 — but doctrines are exclusive, so a player holds exactly one, ever. **Wide pays more, later** — hybrid unlocks stack, so 3/3/3 holds all three by roughly R7–8, for less gold than 5/5/5 costs. A deep build must convert its rounds 3–6 tempo before a wide build's stacking overtakes it.
>
> In the prototype the riders are deliberately small. The strategic weight of a branch choice is carried by **which unit types it lets you field**.

**Hybrid exclusivity — the symmetric completion of the doctrine ruling — was rejected.** A doctrine is a branch capstone, so "you get one" reads naturally; a hybrid represents two branches *combining*, and if a player genuinely holds 3/3/3 then all three combinations genuinely exist in their army. Exclusivity there is a rules imposition rather than a fiction the design supports, and it would deepen the dead-gold tail.

**The two small effects stay as written.** Raising them to flip magnitude injects ~1,000 gold of free power on guesswork, ahead of the repricing that owns it. The "unpriced tax" on the Military doctrine — granting nothing to a player screening with Common squads — is ruled **not a defect**: coherent formations is the doctrine's stated intent.

## Consequences

- **Stated honestly:** at v0.4 magnitudes the tempo race is real in shape and small in size. It is underwritten by a rising affinity ceiling and by higher-tier unit types arriving with it, not by current numbers.
- **Nothing in the acceptance gates could falsify a temporal claim** — a single equal-spend snapshot reads one moment. That gap is closed by round-indexing the category matrix ([ADR-0041](0041-viability-band-and-crossover.md)).
- Later **extended, not replaced**: the role scheme restates deep-versus-wide as *composition* — variance against coverage, since counters live only at tier 3 — which is the axis this decision could not reach.
- Recorded finding: the matchup tables modelled **no doctrine and no hybrid at all**. That *confirms* rather than rescues the convergent build's poor showing — it holds four effects to a pure build's one, and at these magnitudes that closes well under 10% of the gap.
