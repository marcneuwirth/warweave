# ADR-0006 — Charging is an emergent state, not a unit stat; and Stance exists because armies would otherwise never move

**Status:** accepted · **Ticket:** [#3](https://github.com/marcneuwirth/warweave/issues/3) · **Spec:** §23.3, §23.4, §14 Brace

## Context

Filling the numeric gap surfaced **two structural defects**, each of which made a shipped rule inert.

**1. Brace could never fire.** Brace triggers on "a frontal **charging** Large unit", reduces "**charge damage**", and ends the "**charge state**". None of those three terms had any referent in the spec — there was no charge mechanic, no charge damage stat, no charge state. Worse, the expansion plan deferred a charge unit until *"after Spear Brace is proven"*: the spec expected v0.4 to prove an ability it shipped no trigger for.

**2. Neither army would ever move.** The gap between deployment bands is **32m** and the longest range in the game is shorter than that. At deployment, nothing can reach anything. If squads advance only on acquiring a target within a finite acquisition range, **both armies stand still until the 90s timeout** — a draw, both players damaged, every round of every match.

## Decision

**Charging is an emergent state derived from movement history**, not an authored unit stat:

> A model whose unit type carries the Charging chassis enters Charging when it has moved toward its current target for ≥1.5s covering ≥6m unobstructed and is within 4m of contact. Its contact attack deals +50%, after which Charging ends. It cannot re-enter for 6s.

**Acquisition range is unlimited** (the whole battlefield), which forces squads to close from t = 0.

**Stance exists**: every squad carries `Hold` or `Advance` (later a third value, `Raid` — [ADR-0019](0019-raid-is-an-order-not-a-position.md)), set during the existing reposition step.

## Why

Charging as an emergent state is buildable from `OnEngage` + `DamageModifier` + a status, with no new subsystem — which is what the primitive-set challenge asks for. Deriving it from movement rather than authoring a `chargeDamage` stat also means Brace has something to read that is true of any attacker that behaved like a charger.

Unlimited acquisition fixes the static-armies defect, and immediately re-broke Brace for a second reason: if every squad advances until it reaches weapon range, a Spear Guard squad is *moving* when a charge arrives, and Brace requires standing still. **Stance is what fixes that**, and it lands several other systems properly at the same time — screening becomes a commitment rather than an emergent accident, a reach squad's range becomes a genuine hold-or-advance choice, and the anvil-and-hammer pattern becomes something a player can actually order.

Authored-per-unit stance was rejected: it makes a hold-branch mirror match Hold-vs-Hold, producing a string of timeout draws, so the branch written as hold-oriented could not be hold-oriented.

## Consequences

- Stance is a **new decision layer** the spec did not have, and the positioning bet had to validate it rather than assume it.
- Charging was later widened from Large models to **access-role chassis** ([ADR-0046](0046-counters-key-on-properties.md)), which is what turns Brace into Military's answer to Beast rather than a Troll-only curiosity.
- The 120°/s turn rate derived alongside this makes solo flanking impossible; that rationale was later *inverted* without changing the number ([ADR-0032](0032-flanking-is-geometric.md)).
