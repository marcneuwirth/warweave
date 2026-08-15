# ADR-0017 — Each branch cashes its own control: magic damage gains +25% against Frozen

**Status:** accepted · **Ticket:** [#9](https://github.com/marcneuwirth/warweave/issues/9) · **Spec:** §11.1, §11.5, §15

## Context

Auditing every interaction the three elemental states have with the rest of the game produced this table:

| Interaction | Owner |
| --- | --- |
| Chilled + Chilled → Frozen | Magic |
| Frozen + `Heavy` → Shatter | **Military / Beast** |
| Any status + Military attack → Enchanted Arms | Mil 3 + Magic 3 |
| Burning/Chilled + Beast attack → refresh | Magic 3 + Beast 3 |
| **Burning + Chilled** | **nothing** |

Two findings. **No Magic attack carries `Heavy`**, so a pure Magic player physically could not cash the Frozen window they had paid for. And **the branch named *Combine* was the one branch whose own two unit types did not combine with each other** — every listed combination is Magic combining with somebody else.

Separately, **Burning had no damage number at all**, so its entire anti-regeneration claim was uncheckable.

## Decision

1. **Magic damage deals +25% against a Frozen target**, in the offensive pool, requiring no tag. Frostcaller freezes; Ember Mage cashes.
2. **Burning deals 10 magic damage per second**, flat and source-independent, **outside** the applying attack's offensive pool.
3. **The base fireball gains a 50% splash falloff** — the primary target takes full damage, every other model within radius takes half.

## Why these numbers

**+25%** mirrors Shatter's magnitude without its tag requirement, giving the two branches symmetric ways to cash the same window. Honest weakness: at ~20.8% uptime on one model this is only about +5% to a caster's DPS. Real identity, thin numbers — which is what the Magic doctrine then amplifies.

**10/s** is budgeted so a full 4-second burn deals 40 raw — enough that Burning *finishes what a fireball started*. Flat and source-independent because only one Burning exists per model and refreshing would otherwise raise the question of whose value survives; outside the offensive pool because a damage-boosting technology would otherwise silently scale the DoT. A 19/s tick budgeted to equal the regeneration it strips was rejected: a 200-gold caster should not solo-counter a branch's tier-2 gateway.

**The falloff was forced by the burn tick.** Setting Burning's damage made the fireball a squad wipe: 4 models caught, each left on 5 HP, all four dead 0.5s later to the burn — an 8-model squad gone in two casts. The spacing value was chosen explicitly for "meaningful anti-swarm, not a squad wipe", and the swarm has no counterplay because formation is authored per unit type. The falloff takes the wipe from 2 casts to ~4, and gives the roster's other AoE effects something real to trade against.

Two alternatives were rejected: a **Brittle** status (bonus damage while carrying both Burning and Chilled) is too narrow, since a fireball burns several models while a frostbolt chills one, so the overlap is a single model; and a **consuming** cash-in was rejected for the same reason Shatter was made non-consuming — it would fight the Chill→Frozen chain.

## Consequences

- The Magic 2 gate now buys a **complete loop** rather than half of one — the map's standing question of whether two Magic unit types can demonstrate *Combine* is answered yes.
- The falloff makes splash a third member of the delivery bucket, and gives the "reduce splash radius, raise single-target damage" technology a real trade.
- Repricing inherits four movements at once: Large targets lose Frozen resistance, casters lose splash reach, gain a DoT, and gain the +25%.
