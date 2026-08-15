# ADR-0039 — The central product test splits into availability and exercise, and needs a versioned purchase policy

**Status:** accepted · **Ticket:** [#13](https://github.com/marcneuwirth/warweave/issues/13) · **Spec:** §33.4

## Context

The spec names *"the game creates repeated moments where a player must choose between counter now, deepen, or weave"* as **the central strategic product test for WARWEAVE** — and gave it **no instrument of any kind**.

It also conflates two things that fail independently: whether the choice is **available**, and whether players **exercise** it. A live-but-invisible choice fails the product test exactly as hard as one that was never live.

## Decision

**Instrument A — choice liveness (runner).** Each planning phase, evaluate the best line under each heading — *counter* (spend against the opponent's last locked army), *deepen* (into the highest-invested branch), *weave* (into a branch below affinity 3) — by rolling the match to its end and reading the Command differential.

> A round is **live** when two or more headings finish within **ε**.
>
> **Gate:** the median match carries **≥3 live rounds**, not clustered, and **each heading appears in the top two in at least one round**.

The last clause is what catches *"weave is never correct"*.

**Instrument B — choice exercise (playtest).** Classify each round's actual spend by heading; measure heading distribution per round and heading-switch count per match. The dominant-line failure reads off directly: weave-rate collapsing after round 4, counter-rate near zero, switch count zero.

## The cost, named rather than hidden

Rollouts need a **fixed purchase policy for both sides, and its blind spots become measured product facts** — the same hazard as a positioning AI, handled the same way: it becomes a **second load-bearing versioned artifact, the reference purchase policy**, named explicitly rather than left implicit inside the runner where nobody versions it.

Subsequently authored as **greedy marginal value with no authored preferences** over a **two-round gold horizon**, with the category constraint acting as a legality filter and nothing more. Two derivations fell out of authoring it:

- **A single-purchase greedy policy can never buy a gateway** — a gateway confers no combat power, so its marginal win rate is zero or negative and no tier-2 or tier-3 build would ever be generated. The unit of decision must be a **round plan**, and the horizon is derived from the longest enabler-to-payoff distance in the price list.
- **The same policy can honestly play both sides only if the two sides are not doing the same thing.** Each side is locked to a heading and all nine pairings are rolled, so a heading's score is a **row of a payoff matrix** rather than a scalar. Unconstrained self-play would run the gate that catches "weave is never correct" in the exact configuration where both players weave together and it looks fine.

**ε = 2 Command points, flat** — ~10% of a mid-match round stake. Flat rather than proportional, because a proportional ε tightens as the match runs and would bias "≥3 live rounds, not clustered" toward early rounds by construction. **ε is unprincipled and is stated as a dial**; no derivation is available, and pretending otherwise is the failure this work exists to stop.
