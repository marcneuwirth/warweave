# ADR-0045 — Tier-3 unit types carry two forked 3-step upgrade tracks instead of technologies

**Status:** accepted · **Ticket:** [#19](https://github.com/marcneuwirth/warweave/issues/19) · **Spec:** §17.2

## Context

The tier-3 row ([ADR-0044](0044-tier-3-row-at-affinity-4.md)) adds six unit types. Giving each of them two technologies in the existing shape would add twelve entries to a pool the audit had just found **majority-inert**, on the unit types players reach *last*.

The audit's diagnosis was specific: eight of eighteen were authored as **flat stat tweaks**, and a flat tweak cannot produce a decision in any container.

## Decision

> **Two forked 3-step upgrade tracks per tier-3 unit type.** A player picks one at step 1 and climbs it; the fork is locked thereafter and no step refunds. Steps cost **150 / 200 / 250**.
>
> Each track is **one named effect at three magnitudes**, crossing the ~+40% flip threshold **only at step 3**.

Technologies stay on tiers 0 and 2 at the existing shape (two authored, at most one owned), holding that pool at **16**.

## Why this shape

**Partial investment is sub-flip rather than inert** — which is precisely the failure mode the audit diagnosed. A player who climbs two steps has bought something real and has not bought the flip. That is a gradient, and a gradient is what a flat tweak could never provide.

**The fork carries the specialization decision**, so §17's *"one meaningful specialization decision per unit type"* **generalises** rather than acquiring an exception for tier 3.

**Tracks cost no squad slot but are the largest single gold commitment in the game** — a tier-3 unit plus a full track is roughly 3.2 slots forgone at the slot ceiling ([ADR-0049](0049-repricing-against-the-slot-ceiling.md)). That is the price of owning a counter.

## Consequences

- Step 3 of one track per branch carries that branch's **counter** ([ADR-0046](0046-counters-key-on-properties.md)), which is why counters are *earned by commitment* and why **a wide build owns none**.
- **Open, and honestly so:** whether tier-3 unit types eventually want technologies *as well* as tracks is not answerable on paper. The tracks carry the fork; whether a deep build wants a second, orthogonal decision on its showpiece units is a play question.
- **Recorded weakness:** several track payloads were authored but **not modelled** in the paper calculator that produced the field, so their magnitudes follow the ladder by construction rather than by measurement. The spec's §34 names them.
