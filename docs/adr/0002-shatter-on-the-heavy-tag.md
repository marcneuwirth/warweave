# ADR-0002 — Shatter triggers on the `Heavy` attack tag, does not consume Frozen, and pays +25%

**Status:** accepted · **Ticket:** [#2](https://github.com/marcneuwirth/warweave/issues/2) · **Spec:** §11.5

## Context

`v0.4-draft.md` §11 gated Shatter on "a physical attack with at least **70 raw damage**". Sorting every physical stack in the roster against a Frozen target put three of them within 1.9 points of the line, on both sides:

| raw | stack | vs the 70 gate |
| --- | --- | --- |
| 69.6 | Spear Guard + Hooked Spears, vs Large | misses by 0.4 |
| 70.2 | Longbowmen + Bodkin | clears by 0.2 |
| 71.5 | a Common stack | clears by 1.5 |

That is not a threshold, it is a rounding error. Any one-point rebalance — which repricing would certainly perform — silently flips a control mechanic.

## Decision

Shatter triggers on the **`Heavy` attack tag**, **does not consume Frozen**, and grants **+25%** in the offensive pool. The `Heavy` roster is editorial: Troll, Longbowmen, and Spear Guard *with Hooked Spears*. Bodkin at step 3 trades `Heavy` away.

## Why

- **A tag is immune to damage retuning.** Moving the gate to 65 was banked as a fallback and rejected: it fixes the margin without removing the coupling.
- **Non-consuming deletes an anti-synergy.** Under consume-rules the Heavy hit *ended the freeze early* — the physical half of the combo cut short the window the Magic half paid for. It also removes a circularity: with a tag trigger, Shatter's own bonus needs no exclusion term.
- **+25% rather than +40% because non-consuming roughly doubles the hits.** Expected in-window Heavy hits = `models × window / cooldown`; for multi-model Heavy squads that goes 0.85 → 1.56 (1.8×), while single-model Heavy is unchanged. Holding +40% would silently double the Magic→Military payoff.
- The tag also preserves the *investment-unlock* story that the scalar gate delivered only by coincidence — a Common attack in Heavy damage range is deliberately excluded.

## Consequences

- Multi-model Heavy squads hold at parity-plus; single-model Heavy weakens by ~37% per freeze. Accepted.
- `Heavy` joins a taxonomy the spec must keep consistent, which is why the glossary makes attack tags a namespace rather than an ad-hoc label.
- +25% becomes the house magnitude for *"a window was created and cashed"*, later reused by flanking (ADR-0032).
