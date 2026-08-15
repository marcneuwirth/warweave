# ADR-0004 — Magic halves armour before the curve, and bypass applies before penetration

**Status:** accepted · **Ticket:** [#2](https://github.com/marcneuwirth/warweave/issues/2) · **Spec:** §22.3

## Context

`initial-spec.md` §22 said "magic ignores 50% of physical armor" without saying whether that halves the *armour value* before the curve or the *resulting reduction* after it. The two differ.

## Decision

**Halve the armour**: `armorMult = 100 / (100 + armor × 0.5)`. **Bypass is applied before penetration**: `effectiveArmor = max(0, armor × (1 − bypass) − armorPenetration)`.

## Why

The two readings sit within a point of each other across most of the roster and separate only at the top of the armour range — 7% on a heavily armoured target, which is precisely the target Magic exists to threaten. Halving armour wins on three counts:

- it is the faithful reading of "ignores 50% of *armour*";
- it keeps **one curve and one pre-curve armour value**, so bypass and penetration compose without inventing an ordering rule;
- "magic sees half your armour" is a sentence a player can hold in their head, which matters for the explicability gate.

Bypass-before-penetration reads sequentially — what the attack *sees*, then what it *drills through* — and keeps flat penetration worth a constant amount regardless of damage type, which is what makes penetration tunable.

## Consequences

- No v0.4 attack carries both bypass and penetration, so the ordering is forward-compatibility only.
- **Revisit if a magic-penetration effect is ever introduced**: bypass-first allows the two to compound toward total armour negation.
