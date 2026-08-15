# ADR-0013 — Doctrines are exclusive: one active at a time

**Status:** accepted · **Ticket:** [#7](https://github.com/marcneuwirth/warweave/issues/7) · **Spec:** §9

## Context

Charting affinity reachability against the income curve found that affinity is far cheaper than the deep-versus-wide section assumes, and that its scarcity collapses mid-match.

Branch technologies consume **no squad slot**, so Affinity 5 costs three squad slots, not five. **Affinity 5/5/5 costs 3,450 gold and 9 slots against R8's cumulative income of 3,500.** Under the spec as written, an omni build holds **all three doctrines and all three hybrid unlocks by round 8**, with three slots and 2,200 gold still spare. The deep-versus-wide tension is live for rounds 3–7 and then dissolves entirely.

## Decision

**At most one doctrine is active at a time**, chosen on first reaching Affinity 5 in any branch. Hybrid unlocks remain automatic and stackable.

## Why exclusivity rather than the alternatives

- **Raising the divisor** (200 → 300) breaks the *400 = two gateways = Affinity 2* identity and re-prices every affinity band.
- **Raising the cap** above 5 only moves the convergence round.
- **Affinity as a share of total spend** is the theoretically clean fix but makes affinity non-monotonic — buying a Common squad could cost you a doctrine — which the economy work explicitly ruled out.
- **Exclusivity costs one sentence**, leaves the affinity formula untouched, and restores a commitment decision that persists to round 12: *you can own three branches, but you only ever are one.*

## Consequences

- **Secondary branches gain a natural stopping point.** Once your doctrine is chosen, level 5 in another branch buys nothing by itself. Before exclusivity every branch wanted 5.
- **Sunk cost becomes the late-game scarcity.** A player may sit at 5/5/5 holding one doctrine, with 2,000 gold buying only the *right to consider* another. Affinity stays a live constraint to round 12 because the **doctrine slot** is scarce even once affinity is not.
- **The predicted convergent build becomes 5/3/3** — one doctrine plus all three hybrids — which is named as a benchmark rather than assumed away.
- An **inert doctrine is now worse than a weak one**, because nobody would ever choose it. That is what forced the Magic doctrine's replacement ([ADR-0018](0018-arcane-resonance-replaced.md)).
- Binding on the expansion: more unit types per branch and apex pricing bring the convergence round *forward*, so this matters more later, not less.
