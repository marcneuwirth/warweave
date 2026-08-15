# ADR-0021 — Contribution to the control threshold is per-model prorated

**Status:** accepted · **Ticket:** [#17](https://github.com/marcneuwirth/warweave/issues/17) · **Spec:** §5.5

## Context

The control point requires ≥400 gold of squad value within 8m. Once movement stops reasoning about the radius ([ADR-0020](0020-raid-pushes-through.md)), "did the raid work" is unanswerable without saying how a squad's value is counted.

## Decision

> `contribution = squad cost × (models within 8m ÷ the unit type's full model count)`

## Why not squad-level all-or-nothing

All-or-nothing needs a reference point, and squad-to-squad distance is defined as *nearest-model to nearest-model* — under which a 10m-frontage squad banks its full cost by dipping **one model** inside the radius. Avoiding that requires inventing a "squad centre" term for this rule alone.

Three properties are worth more than the simpler alternative:

- **No cliff.** Contribution is continuous in position, so there is no gameable boundary and no new geometry term.
- **Casualties count.** A squad down to its last model contributes a fraction of its cost, which makes the 400g threshold a **live** condition rather than a purchase-time one: contesting a raid works by killing raiders. All-or-nothing would make grinding two raiding squads down to one model each accomplish exactly nothing until the final model died.
- **Frontage acquires an objective cost.** Wide formations sprawl outside the radius — a free interaction with formation spacing rather than a special case.

This is not a new kind of computation: models are already the atomic spatial entity, and an existing doctrine already runs a per-model radius check.

## Consequences

- **The cheapest qualifying raid is two 200g fast squads at exactly 400g — and it drops below threshold on the first casualty.** A raid that survives contact is **three squads**, which becomes a named predicted outcome for the runner.
- It **taxes multi-model squads and exempts single-model ones**, which sharpens rather than blunts the case for a single big body as an objective holder. Routed to repricing, and one reason a single-model squad is not a good shape for the roster generally ([ADR-0047](0047-rung-band-and-role-quantities.md)).
- Refines rather than contradicts the objective's original sizing, whose 8m argument was already per-model reasoning.
