# ADR-0015 — Branch technology investment is capped per unit type *(forward invariant)*

**Status:** accepted, dormant · **Ticket:** [#7](https://github.com/marcneuwirth/warweave/issues/7) · **Spec:** §32.1

## Context

The economy work ruled that `branchInvestment` counts every branch technology ever bought. That is sound at 2 choices / 1 active, since technologies never refund and buying-then-abandoning is strictly worse than holding.

**It breaks at 4 choices / 2 active**, which is the stated expansion shape: buy all four technologies for a unit type, two active, all four counting 250 each — **1,000 gold of affinity per unit type, zero squad slots, two purchases with no gameplay effect.** That is the affinity-churn exploit returning through a door v0.4 cannot see.

## Decision

> **Branch technology investment is capped at one technology's worth (250) per unit type**, however many are owned.

## Why not the obvious alternative

Counting only *active* technologies reintroduces the non-monotonicity the economy work rejected, since swapping actives would be free and affinity would move without spending. The cap keeps affinity **monotonic and purchase-time-checkable**, and survives any future pool shape.

## Status in v0.4

**Dormant.** [ADR-0050](0050-units-only-affinity.md) later ruled that **only unit purchases generate affinity at all**, which removes the mechanism this cap was written to bound. The invariant is retained rather than deleted because it goes live the moment any non-unit purchase counts toward investment again — which the expansion may well want.

Recorded now because it is cheap to close here and expensive to rediscover later.
