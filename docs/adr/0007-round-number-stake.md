# ADR-0007 — Match length is governed by a round-number stake, not by army value

**Status:** accepted · **Ticket:** [#6](https://github.com/marcneuwirth/warweave/issues/6) · **Spec:** §5.1, §5.2

## Context

`initial-spec.md` §5 dealt `clamp(6 + floor(survivingEnemyUnitValue / 200), 6, 16)` and targeted 8–12 rounds. It cannot produce that range, and the reason is structural rather than a mistuned constant.

- **The floor is 9 rounds.** A perfect stomp — winning decisively from round 1 — deals 87 Command through round 8 and only crosses 100 on round 9. An 8-round match is arithmetically unreachable.
- **A competitive match runs 13–18 rounds.** At a 50/50 record the loser takes damage on half the rounds, so 100 Command needs ~9 losses ≈ 17–18 rounds. **The better the match, the further outside the target it falls.**
- **The formula was a round-number ramp in disguise.** Army value tracks cumulative income and then saturates at the squad cap, so the term is ~90% a proxy for *what round it is* and ~10% a signal of decisiveness. The clamp floor confirms it from the other end: in rounds 1–3 a one-squad win and a total wipe pay 7 versus 9.

Let **N** be total rounds and **L** rounds lost by the loser. A stomp has L≈N, an even match L≈N/2, and both must land in 8–12 and sum to 100. The even-match loser must take **~60% more per loss** than the stomp loser — and *no property of army quality distinguishes the two cases*. Only **which rounds were lost** does.

## Decision

> `S(round) = 5 + 2 × round` — a conserved stake, split **70% battle / 30% control objective**.
>
> `battleDamage = 0.7 × S × (0.75 + 0.25 × winnerIntegrity)`; draws cost both players `0.35 × S`.

`survivingEnemyUnitValue`, the `/200` divisor, the `clamp(…, 6, 16)` and the flat 4-Command draw cost are **retired**.

## Why these shapes

**Round number must climb steeply**, which kills the entire "make the value term steeper" family of fixes: scaling harder off surviving value compresses stomps and even matches together, so the ratio that is wrong now stays wrong.

**`winnerIntegrity` reads the winner, not a ratio.** Battles resolve by elimination, so the loser has zero remaining and any ratio-based margin reads ~100% in nearly every round — the same defect as the old clamp in a new costume.

**The multiplier is compressed to [0.75, 1.00].** Margin scaling pushes *against* the reconciliation: a dominant player wins with high integrity, an evenly-matched player wins pyrrhic, so margin pays stomps more. At full range even matches land at ~14 rounds regardless of ramp shape, and forcing them back to 12 drives the ramp's intercept negative. The 1.33× spread looks weaker than the old 6→16 clamp, but **that 2.67× spread was fake** — it tracked the clock.

**The flat draw cost had to go regardless**: a constant 4 against a stake ramping 7→29 makes late-round stalling progressively cheaper.

## Consequences

- Verified across the record spectrum: total domination R8, 60/40 R10, 50/50 R12, lose-every-battle-hold-the-point R10. The whole spectrum is inside 8–12 and **the more competitive match runs longer**.
- Command damage becomes a pure function of the clock, which strips out the decisiveness signal entirely — [ADR-0008](0008-two-decoupled-axes.md) and [ADR-0009](0009-control-objective-scope-exception.md) are what replace it.
- Battle duration is untouched, so the movement-speed table derived from the closing-time budget does **not** need regenerating.
- On stalling: mutual draw damage hurts the **trailing** player, so the abuse case is a *leader* turtling for draws. The objective is the designed counterplay.
