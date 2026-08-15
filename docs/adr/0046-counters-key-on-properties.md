# ADR-0046 — Counters key on functional properties, never on `branch`, and live at step 3 of a tier-3 track

**Status:** accepted · **Tickets:** [#14](https://github.com/marcneuwirth/warweave/issues/14), [#19](https://github.com/marcneuwirth/warweave/issues/19) · **Spec:** §17.3, §23.4

## Context

A cycle needs **conditionals** — continuous stats can reorder a ladder but never bend it into a loop ([ADR-0043](0043-rotation-a.md)). The question is what a conditional is allowed to read.

Branch-keyed counters are expressible under the denotation rule ([ADR-0023](0023-branch-denotation-and-purchase-time-stamping.md)) and were **rejected anyway**: a player cannot see why the number moved. `branch` is a label in a UI; a property is visible on the field. This matters more since explicability was split into prediction accuracy and **attribution agreement scored against the battle log** ([ADR-0042](0042-no-threshold-without-n.md)) — a counter nobody can attribute fails a gate.

## Decision

**Each branch exposes exactly one property it cannot avoid exposing, because the property falls out of how the branch wins:**

| Branch | Property | Why unavoidable | Counter |
| --- | --- | --- | --- |
| Military | formation coherence | holding a line *is* standing shoulder to shoulder | AoE catch `πr²/sp²` |
| Beast | closing speed (`Charging`) | access means crossing the gap | −40% damage from Charging attackers |
| Magic | model scarcity | reach-best is bought with range and output, not bodies | +40% against squads of ≤3 models |

All three are `DamageModifier` on a predicate, so the primitive set is untouched. **All three live at step 3 of a tier-3 upgrade track**, one per branch.

## Consequences

**Charging widens from Large models to access-role chassis.** The state was originally gated on size, which made the counter that reads it a curiosity aimed at one unit type. Keying it on the chassis that *crosses the gap* is what makes Brace and its capstone escalation the genuine **Military-beats-Beast** edge.

**Counters are earned by commitment, and a wide build has no counter at all.** A 3/3 hybrid covers every role and flips nothing; a deep build owns one flip and one hole. **That is the deep-versus-wide bet in its sharpest form — variance against coverage** — and it is the axis the earlier temporal framing ([ADR-0026](0026-deep-wide-is-temporal.md)) could not reach.

**Two failing unit types are rescued by role rather than by price.** The dead frontline monster was *a unit with no role*, not bad numbers; as its branch's reach it has a reason to exist. The dead caster is half of its branch's best-in-game reach. **F4 and F5 fold into the role assignment**, which is why no repricing of either was performed.

**The model-scarcity counter keys on model count, so it also fires into single-model and small squads of any branch**, including mirrors. That is the point of keying on a property: the counter is not a branch-hate button.

**One property is not gradeable on paper.** *Access* is two-dimensional and the calculator resolves a single one-dimensional gap. The model-scarcity conditional makes Beast's **edge** measurable; nothing makes Beast's **role** measurable. Every Beast row in the paper field is a floor, not a measurement — which is why the corresponding edge ships as a named prediction rather than a grading.
