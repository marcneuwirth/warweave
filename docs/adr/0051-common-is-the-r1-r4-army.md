# ADR-0051 — Common is the R1–R4 army, and its equal-gold dominance is not repriced

**Status:** accepted · **Ticket:** [#19](https://github.com/marcneuwirth/warweave/issues/19) · **Spec:** §1.1, §13

## Context

The rule that a Common unit type never matches a branch on that branch's signature axis ([ADR-0005](0005-common-never-matches-a-branch-signature.md)) says what Common is **not**, and the role scheme sharpens that to *Common owns no role*. Neither says what Common **is**.

Meanwhile the headline matchup finding was that the cheap Common swarm is **undefeated at equal gold, 8 of 8** — beating both of its designated counters — and **second-worst at twelve squads**, 2–7.

## Decision

> **Common is the R1–R4 army.** It wins at the early-round budget, when gold binds and twelve slots are unreachable, and loses at the squad cap, when slots bind.

**The swarm is not repriced.** Its equal-gold dominance is the **specification** of a Common unit type, not a bug in it.

## Why

The inversion *is* the design. Two repricings were tried and **neither moved any row but the swarm's own**, and the reason is now clear: the unit measures a budget that **stops binding** around R4. Repricing it changes what happens in a regime that lasts four rounds and nothing about the regime that decides matches.

The invariant holds at **army level**, and the per-unit form is deliberately weaker: at the early budget the swarm loses to a reach gateway and the ranged Common unit loses to two branch units. **Reach beating a melee swarm at equal gold is correct behaviour, not a violation** — the invariant is about what a Common *army* can achieve, not about winning every duel.

At the cap it holds cleanly: a Common-heavy army loses to all three pure branch armies and finishes near the bottom of the field.

## Consequences

- Common gets a **positive definition** rather than a list of exclusions, which is what makes it authorable: a Common unit type is priced for the opening rounds and expected to be outgrown.
- It closes the question of whether the swarm's dominance is a defect. **It is the same fact as the two-regime inversion**, seen from the roster side rather than the measurement side — and the measurement side already requires every band to state its regime ([ADR-0037](0037-regime-split-and-sweep.md)).
- The player-facing corollary is the one thing the spec must say out loud: **which budget is currently binding changes what is worth buying**, and the slot ceiling is the number that makes it sayable ([ADR-0049](0049-repricing-against-the-slot-ceiling.md)).
