# ADR-0003 — `squadRemainingHPPercent` is HP-weighted; surviving-value is squad-count-weighted

**Status:** accepted, and partly superseded by [ADR-0007](0007-round-number-stake.md) · **Ticket:** [#2](https://github.com/marcneuwirth/warweave/issues/2) · **Spec:** §5.2

## Context

`v0.4-draft.md` §5 used `survivingEnemyUnitValue` for Command damage and `squadRemainingHPPercent` for timeout resolution, and defined neither.

## Decision

The two terms are **deliberately different measures**.

- **`squadRemainingHPPercent`** = Σ current HP of living models ÷ Σ starting HP of all models. Shields are absorption, not HP, and are excluded.
- **`survivingEnemyUnitValue`** = Σ squad cost over every squad with at least one living model — squad-attrition, not HP-attrition.

## Why, and the contested half

Model-count was rejected for the first measure outright: a Troll on 100 of 1,250 HP reads 8% by HP and **100%** by model count, which breaks worst on exactly the single-model squads the timeout rule most needs to evaluate.

The second is contested and both sides belong on the record. **The agent recommended HP-weighting** for gradient preservation — squads are rarely wiped outright, so a squad-count measure compresses the decisiveness signal badly. **It was overridden in favour of board legibility**: a player can look across the board mid-round and predict the Command swing without doing HP arithmetic, which an HP-weighted measure never allows.

## Consequences

- The compression the agent warned about turned out to be decisive, but for a reason neither party anticipated: [ADR-0007](0007-round-number-stake.md) found `survivingEnemyUnitValue` is ~90% a proxy for the round number, and **retired it entirely**. The contested choice was resolved by deleting the term.
- `squadRemainingHPPercent` survives and becomes the single margin measure in the game, feeding `winnerIntegrity`.
- Recorded rider: regeneration walks an undisturbed squad back toward 100% during a lull — regeneration's identity working as designed, but a thumb on the timeout scale.
