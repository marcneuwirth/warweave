# Architecture Decision Records

Decisions taken while hardening the v0.4 design spec ([map #1](https://github.com/marcneuwirth/warweave/issues/1)). Each records what was decided, what was rejected, and why — so a future reader can tell a decision from drift.

The spec they produce is [`docs/spec/v0.4.md`](../spec/v0.4.md); the vocabulary they use is [`CONTEXT.md`](../../CONTEXT.md); the arithmetic behind them is in [`docs/analysis/`](../analysis/).

## The damage kernel

| # | Decision |
| --- | --- |
| [0001](0001-three-bucket-damage-kernel.md) | Three buckets: offence pools, delivery multiplies per hit, defence chains |
| [0002](0002-shatter-on-the-heavy-tag.md) | Shatter triggers on the `Heavy` tag, does not consume Frozen, pays +25% |
| [0003](0003-decisiveness-measures.md) | HP-weighted margin, squad-count-weighted surviving value *(partly superseded)* |
| [0004](0004-magic-halves-armour.md) | Magic halves armour before the curve; bypass before penetration |

## Mechanics and geometry

| # | Decision |
| --- | --- |
| [0005](0005-common-never-matches-a-branch-signature.md) | A Common unit type never matches a branch on that branch's signature axis |
| [0006](0006-charging-is-emergent-and-stance-exists.md) | Charging is an emergent state; Stance exists because armies would never move |

## Command, match length and the objective

| # | Decision |
| --- | --- |
| [0007](0007-round-number-stake.md) | Match length is governed by a round-number stake, not by army value |
| [0008](0008-two-decoupled-axes.md) | Command flows through two decoupled axes; the stake is conserved |
| [0009](0009-control-objective-scope-exception.md) | A battlefield objective is admitted despite `Terrain: None` |
| [0019](0019-raid-is-an-order-not-a-position.md) | The objective is reached by an order, not by positioning |
| [0020](0020-raid-pushes-through.md) | A raid pushes through, and attacks what physically blocks it |
| [0021](0021-control-contribution-is-per-model-prorated.md) | Contribution to the control threshold is per-model prorated |
| [0022](0022-battle-end-pursuit-and-hold-breaking.md) | Battle end, the 20s pursuit phase, and `Hold` breaking |

## Economy and progression

| # | Decision |
| --- | --- |
| [0010](0010-selling-reinstated.md) | Selling reinstated at 50% with a 2-per-round cap |
| [0011](0011-cap-is-on-ownership.md) | The squad cap is on ownership: own 12 = field 12 |
| [0012](0012-affinity-tracks-currently-owned.md) | Affinity tracks currently-owned squads; the full price leaves on a sale |
| [0013](0013-doctrines-are-exclusive.md) | Doctrines are exclusive — one active at a time |
| [0014](0014-doctrine-rechoice-is-rate-limited.md) | Doctrine re-choice is rate-limited, not merely priced |
| [0015](0015-per-unit-type-technology-investment-cap.md) | Technology investment capped per unit type *(dormant forward invariant)* |
| [0048](0048-branch-price-axis.md) | A branch price axis at tiers 2 and 3; gateways stay at 200 gold |
| [0049](0049-repricing-against-the-slot-ceiling.md) | Tier-3 units and tracks priced against the 292-gold slot ceiling |
| [0050](0050-units-only-affinity.md) | Only unit purchases generate affinity |

## Elemental system and effects

| # | Decision |
| --- | --- |
| [0016](0016-frozen-exempt-from-large-discount.md) | Frozen is exempt from the Large HardControl discount |
| [0017](0017-each-branch-cashes-its-own-control.md) | Each branch cashes its own control; Burning gets a damage number |
| [0018](0018-arcane-resonance-replaced.md) | Arcane Resonance retired and replaced with a status spread |

## Doctrines, hybrids and denotation

| # | Decision |
| --- | --- |
| [0023](0023-branch-denotation-and-purchase-time-stamping.md) | A branch name denotes the `branch` property; investment is stamped at purchase |
| [0024](0024-apex-instinct-rebuilt-and-culling.md) | Apex Instinct rebuilt; access-role targeting becomes a culling rule |
| [0025](0025-beastmastery-gets-a-zone.md) | Beastmastery keys on a zone, not a melee state |
| [0026](0026-deep-wide-is-temporal.md) | Deep and wide are separated on the time axis; hybrids keep stacking |

## Technologies and tracks

| # | Decision |
| --- | --- |
| [0027](0027-mandatory-technology-gate-replaced.md) | The mandatory-technology gate is replaced by a two-part conditional test |
| [0028](0028-technology-layer-is-cap-relief.md) | The technology layer is cap relief, measured at twelve squads |
| [0029](0029-aoe-catch-is-geometric.md) | AoE catch is geometric; "a 3m area" is a diameter |
| [0030](0030-at-most-one-technology-per-unit-type.md) | "At most one per unit type"; no replacement invented to fill a slot |
| [0031](0031-model-count-primitive.md) | The primitive set gains a model-count operation |
| [0045](0045-forked-tracks.md) | Tier-3 unit types carry two forked 3-step tracks instead of technologies |

## Positioning

| # | Decision |
| --- | --- |
| [0032](0032-flanking-is-geometric.md) | Flanking is a geometric test; combined arms falls out of the turn rate |
| [0033](0033-rear-arc-breaks-stickiness.md) | Rear-arc damage breaks stickiness once, with a 4s lockout |
| [0034](0034-positioning-gate-core-only.md) | The positioning gate counts the dominant core, at engagement scale |
| [0035](0035-terrain-answers-one-failure.md) | Terrain is the remedy for a dominant deployment, not for shortfall in general |
| [0036](0036-sixty-metre-width-is-load-bearing.md) | The 60m width is load-bearing on wall-versus-concentrate |

## Measurement

| # | Decision |
| --- | --- |
| [0037](0037-regime-split-and-sweep.md) | Win rate is a fraction over a versioned archetype sweep; bands state their regime |
| [0038](0038-marginal-inclusion.md) | "Competitively useful" means marginal inclusion |
| [0039](0039-availability-vs-exercise.md) | The product test splits into availability and exercise |
| [0040](0040-objective-three-numbers.md) | The objective axis gets three numbers |
| [0041](0041-viability-band-and-crossover.md) | Category viability is a two-sided band on a round-indexed matrix |
| [0042](0042-no-threshold-without-n.md) | Explicability splits; "enjoyable" is deleted; no threshold without an N |

## The roster and the core bet

| # | Decision |
| --- | --- |
| [0043](0043-rotation-a.md) | Each branch owns one role at best and one at adequate, in a rotation |
| [0044](0044-tier-3-row-at-affinity-4.md) | A tier-3 row of two unit types per branch, gated at Affinity 4 |
| [0046](0046-counters-key-on-properties.md) | Counters key on functional properties, at step 3 of a tier-3 track |
| [0047](0047-rung-band-and-role-quantities.md) | Each role has one quantity; adjacent rungs differ by 25–40% |
| [0051](0051-common-is-the-r1-r4-army.md) | Common is the R1–R4 army, and is not repriced |
