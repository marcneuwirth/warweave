# ADR-0028 — The technology layer is cap relief, and is measured at twelve squads

**Status:** accepted · **Ticket:** [#11](https://github.com/marcneuwirth/warweave/issues/11) · **Spec:** §4.4, §17.1

## Context

Technologies are flat-priced, **cost no squad slot**, and apply to every squad of a unit type. Their value is therefore proportional to squads fielded — and the whole pool had been judged in **single-squad equal-gold fights**, precisely the regime the matchup tables proved *inverts* at the cap.

The clean case is the model-count technology, called "the most expensive relative purchase in the game" at +200 gold on a 100-gold squad. At twelve squads:

| Militia ×12 | Models | Total HP | Gold |
| --- | --- | --- | --- |
| Plain | 96 | 9,600 | 1,200 |
| + Conscription | 132 | **11,220** | 1,400 |

8.1 HP/gold against the unit's own 8.00 — and under the ownership cap the thirteenth squad **cannot be bought**, so this is the only way a maxed army grows.

## Decision

> **The technology layer is cap relief: worthless while gold binds, correct the moment slots bind. Every technology verdict is derived at twelve squads against a full archetype field, not at single-squad equal gold.**

Technology attaches to the **unit type**, not the squad instance — confirmed, ruling out per-squad purchase. Value scaling with squad count is intended.

## Consequences

- **Three prior findings were overturned by re-measurement alone**, with no number changing: a technology that "flipped nothing" flips six matchups at the cap; a technology that was a hard on/off switch at one squad flips nothing at twelve, because a full field carries enough output to outrun +45 armour; and a "wrong-signed" shield turns out to be the only effect that makes a whole branch win anything.
- The layer is also the natural sink for the dead gold the economy flagged at R10–R11.
- **A regime finding, not a pool defect:** the same number can be decisive at one squad and inert at twelve. That is why every balance target in the spec now states its regime in the same sentence as its number ([ADR-0037](0037-regime-split-and-sweep.md)).
- Because it partially buys back the currency the cap rations, the model-count technology's magnitude **and its cap-bypass property** were routed to repricing together — a technology that partially disables the cap cannot be priced without saying so.
