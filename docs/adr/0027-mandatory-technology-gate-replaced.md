# ADR-0027 — "No technology is effectively mandatory" is replaced by a two-part conditional test

**Status:** accepted · **Ticket:** [#11](https://github.com/marcneuwirth/warweave/issues/11) · **Spec:** §27.2

## Context

The expansion gate read *"no technology is effectively mandatory"*. Read literally, it **condemns the best-shaped technology in the pool** — an armour-penetration effect worthless against six unarmoured unit types and decisive against armour, with the round loop's previous-army inspection making the condition knowable in advance. That is exactly what a good technology looks like.

Meanwhile a unit type holding **two sub-5% halves** — a choice with no content at all — is far worse, and the gate cannot see it.

## Decision

> **(a)** No technology is chosen more than ~70% of the time **across the matchup distribution**, and
> **(b)** every unit type's pair contains at least one matchup in which each side is the correct pick.
>
> **Mandatory-against-a-condition is the design target. Unconditionally mandatory and unconditionally inert are the two failures.**

## Why the container is kept

The one-technology-per-unit-type rule survives unchanged. **The choice binds through permanence, not budget** — the whole pool caps at ~2,050 gold against R8's 3,500, so gold never rations it. The alternatives all cost more than they buy:

- **1-of-3** multiplies the design surface while a majority of the pool does not work.
- **Making technologies cost a squad slot** re-prices the frozen economy identities.
- **Refundability** dissolves the commitment that is doing the work.

**The defect was never the container.** Eight of the eighteen were authored as **flat stat tweaks** (−25% cooldown / −15% damage; +60% spacing / −20% AoE), and a flat tweak cannot produce a decision in *any* container.

## Consequences

- Every technology in the shipped pool is a **conditional fork** — worth zero or negative in the other half's domain.
- The same principle sizes tier-3 upgrade tracks: one effect at three magnitudes crossing flip only at step 3, so partial investment is sub-flip rather than inert ([ADR-0045](0045-forked-tracks.md)).
- The gate needs **pick-rate distribution across the matchup distribution**, which a single equal-spend snapshot cannot produce — routed into the sweep ([ADR-0037](0037-regime-split-and-sweep.md)).
- One measured reversal recorded here: a shield technology read as "measurably worse than nothing" at single-squad scale, which was an artifact — the shield extended an attrition fight one caster was already losing. At six casters it is the only effect in the game that makes a pure Magic army win anything.
