# ADR-0001 — The damage kernel has three buckets: offence pools, delivery multiplies per hit, defence chains

**Status:** accepted · **Ticket:** [#2](https://github.com/marcneuwirth/warweave/issues/2) · **Spec:** §22.1, §22.6

## Context

`initial-spec.md` §22 gave an armour curve and nothing else. It did not say where percentage modifiers land relative to armour, and with a dozen effects in circulation (+45% Hooked Spears, +32% Pack Hunter, −20% Phalanx, −50% Brace) the answer changes stacked outcomes by large factors. No time-to-kill in the game was computable.

## Decision

```
1. rawDamage      = baseDamage × (1 + Σ offensive modifiers)          # additive pool
2. hitDamage      = rawDamage × Π delivery scalars                    # per target hit
3. effectiveArmor = max(0, armor × (1 − bypass) − armorPenetration)
   armorMult      = 100 / (100 + effectiveArmor)
4. finalDamage    = max(1, floor(hitDamage × armorMult × Π (1 − defensive modifiers)))
```

One `floor`, at the end. Overkill does not carry; targeting is squad-level with per-model resolution and cooldowns staggered on acquisition.

## Why each bucket has the arithmetic it has

**Offence pools additively.** Diminishing returns per added source is the only brake on effect-stacking available to a spec with no simulation. Worked on a four-source stack: pooled gives raw 96.0, chained gives 112.1 — a 17% divergence concentrated on exactly the deepest-invested builds.

**Defence chains multiplicatively.** Two reductions co-occur on the game's most iconic defensive play. The decisive argument is the asymptote: an additive pool of −20%, −50% and one further −30% reaches exactly 0.0 — literal immunity from three unremarkable numbers. A chain can never reach zero and needs no clamp. Armour's `100/(100+x)` is already an asymptotic multiplicative reducer, so it is simply the chain's first term.

**Delivery is its own bucket.** Splash falloff is a property of *which target was hit*, varying within one attack, so it cannot sit in a pool computed once. Pooling is not merely different, it is incoherent: at +100% offensive buffs a pooled −50% falloff pays a splash target 1.5× base, more than half of the primary's 2.0×.

Brace splits across two buckets (+50% offensive contact, −50% defensive charge), which is a useful check that the split is real rather than cosmetic.

## Consequences

- Every effect in the spec must declare its bucket; §22.1 tabulates them.
- **Paper math can no longer divide squad HP by DPS** — no-carry plus per-model reach makes every TTK a per-model resolution. That cost was paid by writing a deterministic calculator (`docs/analysis/matchup-math/`).
- No-carry makes model count a real defensive stat and forces anti-swarm to come from splash, which is where the roster already puts it.
- Squad volleys were rejected outright: under them a squad behind a screen would pay full damage from its back rank, and the entire positioning game stops functioning. **Per-model reach *is* the positioning game.**
