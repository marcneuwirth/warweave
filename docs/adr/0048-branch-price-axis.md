# ADR-0048 — There is a branch price axis at tiers 2 and 3, and gateways stay at 200 gold on every branch

**Status:** accepted · **Ticket:** [#19](https://github.com/marcneuwirth/warweave/issues/19) · **Spec:** §4.1, §6.4, §13–§16

## Context

Three branches with symmetric role structures still need to feel different to buy into. The obvious lever is price. The obvious hazard is that **five economy identities are pinned to exact numbers**, and four of the five rest on the gateway price.

## Decision

**Gateways are fixed at 200 gold on every branch.** The branch price axis lives entirely at **tier 2 and tier 3**: the hold-best branch's units are the most expensive, the access-best branch's the cheapest, with reach in between.

## Why gateways cannot move

Every gateway costs 200 against a 200 divisor, which is what makes both of these hold *identically on all three branches*:

- **400 starting gold = two gateways = Affinity 2**
- **5 × gateway = Affinity 5**

Move any gateway off 200 and both identities break on that branch, the round-1 decision stops being symmetric across the three branches, and the affinity band has to be re-derived. The economy work made the first identity load-bearing and the affinity-curve work extended it up the whole ladder; **repricing a gateway is the one move the price list forbids.**

The remaining identities — the 200-gold affinity band, the plateau-income-to-sales-cap relationship, and the doctrine re-choice fee as one round's plateau income — are likewise stated as invariants in the spec rather than left to drift. The case for stating them became decisive when stretching the affinity ladder was **rejected precisely because it detonates four of them**.

## Consequences

- The price axis survives **in relative terms** — a branch still costs more or less to field — while the ladder's arithmetic stays branch-independent.
- The price list is now explicitly split into a **load-bearing half** (gateways, the divisor, the plateau) and a **tunable half** (tier 2, tier 3, track steps). Repricing work knows which is which.
- Tier-2 and tier-3 prices were then set against the slot ceiling rather than against each other ([ADR-0049](0049-repricing-against-the-slot-ceiling.md)).
