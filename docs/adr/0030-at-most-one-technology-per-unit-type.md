# ADR-0030 — "At most one technology per unit type", and no replacement is invented to fill an empty slot

**Status:** accepted · **Ticket:** [#11](https://github.com/marcneuwirth/warweave/issues/11) · **Spec:** §17.1

## Context

One technology in the pool **never fired**: it rewarded attacking a target facing more than 90° away, at a moment when nothing in the game pinned facing and the turn rate made solo flanking impossible at any orbit radius. It was a 200-gold Common technology that did nothing on its own, competing against an unconditional alternative.

Rewriting it means inventing a facing-pin subsystem, which the primitive-set rule says to challenge.

## Decision

The technology is **deleted**, and §17 relaxes from *"exactly 2 available, maximum 1 equipped"* to:

> **At most one technology per unit type.** A unit type may hold one; **no replacement is invented merely to fill a slot.**

## Why not backfill

A technology authored to fill a hole is a technology with no design pressure behind it, and the audit had just found that a majority of the pool was already inert. Adding a nineteenth to make a table look tidy is the same mistake at a smaller scale. The expansion's 4-choice/2-active pool is where the pool properly refills.

## Consequences

- One unit type sat at a single technology, recorded as fog rather than patched — and the question was closed when that unit type was **deleted entirely** ([ADR-0046](0046-counters-key-on-properties.md)): the slot left with the unit.
- **The stated reason for the deletion later became false.** Flanking was subsequently built as a universal geometric rule with a rotation trigger ([ADR-0032](0032-flanking-is-geometric.md), [ADR-0033](0033-rear-arc-breaks-stickiness.md)), so a facing-keyed technology is now expressible. The deletion stands on the *no-backfill* policy rather than on impossibility — and the note is recorded here so a future reader does not cite a defunct reason.
- The relaxed wording is what makes tier-3 unit types coherent too: they hold **tracks instead of technologies**, and "at most one" tolerates that asymmetry where "exactly two" would not.
