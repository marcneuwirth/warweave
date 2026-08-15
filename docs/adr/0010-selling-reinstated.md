# ADR-0010 — Selling is reinstated at 50% with a cap of 2 sales per round

**Status:** accepted · **Ticket:** [#4](https://github.com/marcneuwirth/warweave/issues/4) · **Spec:** §4.3

## Context

`v0.4-draft.md` §4 stated "**No selling in v0.4**", deferring it because it "interacts directly with affinity investment and creates progression exploits if affinity survives a sale", and arguing that "the larger army cap gives players enough room to make tactical corrections without requiring liquidation".

The first reason is real. The second is false under an ownership cap ([ADR-0011](0011-cap-is-on-ownership.md)): without selling, four cheap squads bought in round 1 permanently consume a third of the army, and a swarm build capped at R4 has 4,250 gold of future income and nothing to buy with it. That is not commitment, it is build death eight rounds early.

## Decision

| Rule | Value |
| --- | --- |
| Refund | **50% of squad cost**, uniform |
| Technology / track refund | **never** |
| Sales per round | **2 maximum** |
| Sell-and-rebuy in one planning phase | permitted |
| Before lock | 100% refund — an undo affordance, not a game decision |

The exploit the original deferral feared is closed directly by [ADR-0012](0012-affinity-tracks-currently-owned.md) instead of by removing the mechanic.

## Why 50%, and why a velocity cap

Swapping a 200-gold squad costs `200 × (1 − R)`:

| Refund | Swap cost | Full liquidation | Reads as |
| --- | --- | --- | --- |
| 25% | 150 | +660 | correction punitive; entombment returns |
| **50%** | **100** | +1,320 | about half a round's income |
| 75% | 50 | +1,980 | counter-swapping near-free — the bench problem returns |

**The refund rate alone cannot separate *correction* from *rewrite*.** At 50% with no cap, a round-10 player holding idle gold liquidates for ~1,320 and rebuys eight squads in a single planning phase, erasing ten rounds of commitment exactly when it should bind hardest. A **velocity cap** is the only lever that permits the first and denies the second: two per round is real flex, and a full 12-squad rewrite takes six rounds.

## Consequences

- The economy is self-consistent at the plateau: a churn upgrade costs ~250, so 550/round funds ~2.2 upgrades against a 2-sale brake. **The rule binds just before the wallet does**, which is the correct order — the brake is the designed constraint and gold is the backstop.
- The prototype exclusion list drops selling.
- The rate and the cap are unvalidated and should be **tuned together**, since the brake is what separates correction from rewrite.
- The velocity-cap precedent is reused for doctrine re-choice ([ADR-0014](0014-doctrine-rechoice-is-rate-limited.md)).
