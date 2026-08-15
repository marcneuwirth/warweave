# ADR-0047 — Each role has one stated quantity, and adjacent rungs differ by 25–40%

**Status:** accepted · **Ticket:** [#19](https://github.com/marcneuwirth/warweave/issues/19) · **Spec:** §1.1, §23.5

## Context

A gate without a quantity is unevaluable in principle ([ADR-0037](0037-regime-split-and-sweep.md)). "Military is best at holding" is exactly such a gate unless *holding* is a number.

## Decision

| Role | Quantity |
| --- | --- |
| **hold** | eHP × frontage |
| **reach** | range × applied DPS |
| **access** | speed × screen bypass — **not paper-gradeable**; reported, not graded |

> **Adjacent rungs differ by 25–40% on their role's quantity.**

All nine rungs in the shipped roster land in band.

## Why that band

**≥25%** because that is the smallest magnitude established as reading like a difference at all. **<40%** because a rung gap at flip magnitude would make **owning a role itself a counter** — and then the α unit could not narrow its branch's hole without closing it, which would dissolve the cycle the holes are made of.

## The derivation that fell out

**Holding is denying passage, so frontage is load-bearing — from which it follows that a single-model squad cannot be a holding unit at any HP total.**

That is why one branch's line is a four-model herd rather than a lone monster, and why the reach unit that used to be a single 1,250-HP body became a two-model squad. It **independently reproduces the model-count finding** from the core-bet work, arriving from a completely different direction: there, a one-model caster squad could not survive a slot cap; here, a one-model squad cannot hold at any HP total. The two together are why no unit type in the shipped roster is a single model.

This is the second arithmetic fact that turns out to be *behind a branch identity* rather than incidental to it — the first being that a rank fights only when `reach ≥ spacing`, which is why the Military gateway is hold-best. **Both are stated in the spec together, as arithmetic rather than as authored bonuses.**

## Consequences

- Adding a unit type to the roster is now a constrained act: it joins a branch at a rung of an existing role, at 25–40% from its neighbour on that role's quantity. Recorded as a forward invariant binding the expansion.
- **Access is reported but not graded**, because its quantity is two-dimensional and the paper instrument is not. Stating the quantity anyway is deliberate: the gate exists and is waiting for an instrument, rather than being silently dropped.
