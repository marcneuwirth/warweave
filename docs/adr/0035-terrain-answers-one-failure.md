# ADR-0035 — Terrain is the remedy for a dominant deployment, not for spatial shortfall in general

**Status:** accepted · **Ticket:** [#12](https://github.com/marcneuwirth/warweave/issues/12) · **Spec:** §23.7, §33.2

## Context

§23 closed with *"Terrain should only be added if these systems fail to provide sufficient spatial depth."* That makes terrain the universal fallback for an unenumerated failure. Enumerating the failures shows it answers one of five.

## Decision

Five failure modes, each with its own detection method **and its own remedy**:

| | Failure mode | Detected by | Remedy |
| --- | --- | --- | --- |
| **F-1** | Fewer than 3 of P1–P4 flip under core-only positioning | the gate itself | add a lever — **not** terrain |
| **F-2** | All flips trace to **one** lever | attribution across P1–P4 | as F-1 |
| **F-3** | A **dominant deployment** exists — one placement correct against every composition | round-robin placement sweep | **terrain** |
| **F-4** | Outcome is a **step function** in placement distance | sweep a screen 0→8m off the lane in 1m steps | widen the `Exposed` corridor |
| **F-5** | The **guessing margin dominates the core** | P4's three-way comparison, plus the sweep's variance ratio | reduce placement freedom, or reveal placement in the lock |

> §23's closing line names **F-3 as terrain's trigger specifically**.

## Why

**Terrain's actual job is to make *places differ*, so that no placement is universally correct** — which is F-3 and nothing else. Answering a targeting-corridor cliff (F-4) or a one-lever shortfall (F-1/F-2) with a map feature is reaching for the largest available tool to fix something it does not touch.

**F-4 is not hypothetical.** The 4m `Exposed` corridor was flagged as a known cliff when it was authored — a screen at 4.1m does nothing, one at 3.9m fully redirects — and the matchup tables independently observed the symptom as an ungraduated reversal. Two separate pieces of work have seen the same edge from different directions. Binary positioning is arguably *worse* than shallow positioning: you either got it right or you did not, with no gradient for skill to express itself along.

**The reserve lever for F-1 and F-2 is player-set facing.** It was rejected explicitly during the mechanics work, to protect flanking's impossibility — *"pre-set facing would let a player hand-defend a rear arc against a flank that has not happened, reopening that door."* Flanking is now a **designed mechanic** rather than a door held shut, so that rejection is **stale**. It is not adopted here; it is recorded as the first thing to try, ahead of terrain.

## Consequences

- The per-model arc test in [ADR-0032](0032-flanking-is-geometric.md) is written the way it is specifically to avoid authoring a **second** cliff of the F-4 kind.
- Terrain's narrow admission for the control point ([ADR-0009](0009-control-objective-scope-exception.md)) remains the only exception, and this ADR does not widen it.
