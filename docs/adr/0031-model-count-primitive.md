# ADR-0031 — The primitive set is extended with a model-count operation

**Status:** accepted · **Ticket:** [#11](https://github.com/marcneuwirth/warweave/issues/11) · **Spec:** §18, §25

## Context

§25 lists the reusable primitives every technology and ability should be built from, and instructs that anything requiring a new simulation subsystem be challenged. **One technology in the pool has no primitive at all**: the one that adds models to a squad. The list has `DamageModifier`, `ArmorModifier`, `Shield`, `Aura` — and no model-count operation.

It is also the pool's strongest card. It converts 200 gold into +36 models on a capped swarm army, **buying back exactly the currency the squad cap exists to ration**, on the unit type that is already dominant at equal gold.

## Decision

**The technology is kept, and `ModelCount` is added to §25's primitive set** to legitimise it — rather than the technology being rewritten to fit the existing list.

Its magnitude **and its cap-bypass property** are routed to repricing together, with the explicit note that it partially buys back slot currency.

## Why keep it

The effect is doing real design work: it is the clearest instance of the technology layer as **cap relief** ([ADR-0028](0028-technology-layer-is-cap-relief.md)), worthless while gold binds and correct the moment slots bind, and it is the only way a maxed cheap army can grow at all. Rewriting it into a stat modifier would delete the one technology that makes the cap legible.

Adding the primitive is honest bookkeeping: the challenge test asks *can this be expressed through existing primitives?*, and the answer here is genuinely **no**, so the set grows by one entry rather than the answer being fudged.

## Consequences

- Any future effect that changes squad size has a sanctioned shape.
- Repricing cannot reason about the squad cap without knowing that one technology partially disables it — which is why the two were handed over as a single item rather than as a number.
- This is the second honest "no" to the primitive-set challenge, alongside the `Raid` movement mode ([ADR-0020](0020-raid-pushes-through.md)). Both are recorded as carve-outs rather than waved through.
