# ADR-0019 — The objective is reached by an order, not by positioning — and that does not violate the targeting principle

**Status:** accepted · **Ticket:** [#17](https://github.com/marcneuwirth/warweave/issues/17) · **Spec:** §23.3, §23.6, §24.1

## Context

The control objective ([ADR-0009](0009-control-objective-scope-exception.md)) was specified with **no order that could reach it**. Stance offered `Hold` (stay put) and `Advance` (close to weapon range on the nearest enemy) — and `Advance` actively fights a raid, since a raiding squad would stop the moment anything came into range, which is the whole enemy army standing between it and the point.

§24 also says the player should primarily influence targeting through positioning, which reads as an argument against any direct order.

## Decision

**Stance becomes a trit: `Hold`, `Advance` or `Raid`.** `Raid` moves the squad toward the **enemy control point**. `Advance`'s heading is confirmed unchanged — toward the nearest enemy squad, always. **Defence stays orderless**: a player's own point is inside their own deployment band, so garrisoning is `Hold` plus a placement.

## Why this does not violate the targeting principle

§24 constrains **targeting**, and `Raid` does not touch target selection. It is a **movement** order, and movement in v0.4 is *already* directly commanded — deployment is free continuous placement and Stance is an explicit per-squad order. What §24 forbids is the player hand-picking what dies.

So `Raid` is a **commitment decision, not a command interface**: the player chooses whether to spend a squad on the objective, never what it shoots, and the destination is fixed by the rules rather than chosen.

## Alternatives rejected

- **An orthogonal per-squad target order** (a waypoint, or an objective flag separate from stance) buys flexibility the game has no use for — there is exactly one destination worth ordering, so an enum beats coordinates, and a player-chosen waypoint *is* the direct-command system §24 is written against.
- **Redefining `Advance`'s axis** toward the enemy control point was the most attractive option, because it makes raiding a pure consequence of deployment — the positional expression §24 asks for. It fails on a concrete case: a melee squad on an open flank still acquires the nearest enemy squad and moves to fight it. Making it actually raid requires movement to stop following target acquisition, which either sends advancing melee squads walking past enemies to be shot in the back, or invents an "engagement corridor" threshold — a larger invention than a third stance value.
- **A fourth `Garrison` stance** (deploy forward, retreat to the point later) was rejected: it lets one squad hold the line *and* defend the point, dissolving the commitment cost the objective exists to charge.

## Consequences

- **Attack is a command; defence is a position.** The round's decision is two-sided and asymmetric in kind.
- **Nothing turns around mid-battle.** An ungarrisoned point is banked uncontested and there is no reactive answer: the player either predicted the raid in the planning phase or did not.
- Availability is unrestricted — no squad cap on raiding, no unit-type gate. Three economic brakes already exist (the 70/30 split, the 400g threshold with per-model decay, push-through attrition), and a squad-count cap would be a number with no argument behind it.
