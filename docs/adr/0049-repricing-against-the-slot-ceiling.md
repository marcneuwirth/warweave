# ADR-0049 — Tier-3 units and upgrade tracks are priced against the 292-gold slot ceiling

**Status:** accepted · **Ticket:** [#19](https://github.com/marcneuwirth/warweave/issues/19) · **Spec:** §4.2, §17.2

## Context

A quantified defect, found while building the archetype field:

> **R8's 3,500 gold across a 12-squad cap is 292 gold per affordable slot.**

As first authored, tier-3 unit types cost 350–450 and a full upgrade track cost 1,050 — **3.6 squad slots forgone for one conditional.** Deep builds fielded **8 squads against wide's 12** and finished **last in the field** (0–14 and 1–13).

## Decision

**Every purchase above the slot ceiling is bought in *slots forgone*, not in gold, and is priced accordingly.**

| Layer | Repriced to |
| --- | --- |
| Tier-2 unit types | 225 / 250 / 275 by branch |
| Tier-3 unit types | 300 / 325 / 350 by branch |
| Track steps | 150 / 200 / 250 (600 for a full track) |

Deep builds move from the bottom of the field to competitive.

**The ceiling itself is stated in the spec** rather than left derivable, because it is a rule a player can be told outright.

## Why this is not a tuning pass

**It is the same diagnosis as the Magic collapse, applied to the whole deep archetype.** Magic was priced as though gold were the binding budget, when the squad cap makes *slots* binding from R4; the deep archetype was priced the same way. In both cases the number that looked wrong (caster damage; tier-3 price) was not the number that was wrong — **the budget being priced against was wrong.**

Once slots are the currency, "expensive" has a unit: a 900-gold unit-plus-track is **~3.2 slots**, and it has to beat three squads to be worth buying.

## Consequences

- **Gateways are untouched** ([ADR-0048](0048-branch-price-axis.md)) — the repricing lives entirely in the tunable half of the price list, so no economy identity moves.
- The ceiling generalises: it is the test any future price is checked against, and it is what makes the technology layer's slot-free pricing legible as **cap relief** rather than as a discount.
- The ceiling moves with the income curve and the cap, so it is stated as a derivation (`R8 income ÷ squad cap`) rather than as the constant 292.
