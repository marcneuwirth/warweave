# ADR-0032 — Flanking is a geometric test, and combined arms falls out of the turn rate rather than a rule

**Status:** accepted · **Ticket:** [#12](https://github.com/marcneuwirth/warweave/issues/12) · **Spec:** §23.1, §23.2

## Context

§23 bet that nine listed systems give the bare field enough spatial depth. Audited against the settled mechanics, **four were never player decisions** (facing is auto-set, formation width and spacing are authored per unit type, collision is physics) and **one was structurally impossible** (flanking: at 120°/s an attacker orbiting at 5m sweeps only ~74°/s, and widening the orbit makes it angularly *slower*).

**Nine reduce to three, two of which are the same lever** — where you put squads in a 24m band. That is too thin to carry a gate requiring three matchups flippable by positioning.

## Decision

> **Flanking** — an attack landing from **outside the target squad's ±90° frontal arc**, measured at the moment of the hit. Flanked models take **+25% damage from all sources**, melee and ranged alike. The arc test is made **per attacking model** against squad-level facing.

No pin condition, no `Engaged` check, no target-commitment check: a pure geometric test against state the spec already defines.

## Why

**The geometric reading needs no protection clause because the turn rate already is one.** No single squad can sustain a flank on anything, so a flank **structurally requires two squads on different bearings** — whichever one you turn to face, the other is behind you. Combined arms falls out of the geometry rather than out of a rule. The earlier work *claimed* this was the intent but shipped no mechanism that read the arc; this is the mechanism, and it costs one predicate.

*(This inverts the original rationale for 120°/s without changing the number: it was chosen to make solo flanking impossible, and that is now exactly what makes flanking a combined-arms play.)*

Two other readings were rejected. A **melee-pinned** reading (flankable only while `Engaged`) gives a textbook backline dive nothing — the branch built to get behind things would be the branch flanking cannot reward. A **target-committed** reading generalises correctly but fails on its own terms: a squad that never rotates is flanked permanently and for free.

**Per model, not per squad.** A 10m-frontage squad straddling the boundary would flip its entire bonus on one model's position — an authored step function, and the spec already has one cliff it is trying to detect. Per-model is inherently graduated: a squad wrapping a formation flanks with some models and not others. It costs nothing new, since the kernel already resolves damage per model with staggered timers.

**+25%, and not armour bypass.** +25% is deliberately **below** the ~+40% flip threshold: flanking should flip a matchup *with* the squad doing the pinning, never alone. It is also the house magnitude for "a window was created and cashed", shared with Shatter. Armour bypass was thematically exact and fails on arithmetic — worth 20–30% against three unit types and **zero against the six unarmoured ones**, a counter to three units wearing a universal rule's clothes.

**Ranged flanking is in**, one rule with no damage-type exception. It is what finally gives *ranged access* — on the positioning list since v0.4 and doing nothing — a live positional payoff.

**Technology-only was rejected outright**: passing the positional-depth gate by a 200-gold purchase means the depth is bought rather than being in the battlefield.

## Consequences

- The four real levers become **placement, stance, flanking, and the raid lane**, and §23's source list is re-authored to say so.
- The rule is inert without a rotation trigger — see [ADR-0033](0033-rear-arc-breaks-stickiness.md).
- Flanking is `DamageModifier` on a positional predicate, so §25 needs no new primitive; what is new is the **state** the kernel must expose, which is why it lands in P0 rather than late.
