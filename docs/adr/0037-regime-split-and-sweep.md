# ADR-0037 — Win rate is a fraction over a versioned deployment archetype sweep, and every band states its regime

**Status:** accepted · **Ticket:** [#13](https://github.com/marcneuwirth/warweave/issues/13) · **Spec:** §27, §33.1

## Context

Two structural defects, either of which alone makes the balance targets unevaluable.

**1. Every §27 number is a percentage with no population.** The engine is deterministic by construction — P0 requires 100 identical simulations to produce identical results — so a fixed matchup at fixed deployments does not yield a 62% win rate, it yields **a winner**. A percentage exists only over a declared sampling distribution, and none is declared anywhere in the spec. **No runner, however good, can evaluate the band.**

**2. The bands span two regimes that invert.** The band language is unit-versus-unit counter talk, but "7 of 9 units competitively useful" and the whole full-build section are army statements — and a unit type measured 8–0 at equal gold measures 2–7 at twelve squads. **The same numbers satisfy the band in one regime and violate it in the other**, so any verdict is arguable either way.

## Decision

> **Win rate = the fraction of sampled deployment pairs won, over a hand-authored, versioned set of six named deployment archetypes per side, run as a symmetric 6 × 6 cross product.** A matchup is a matrix, not a scalar.

> **Every band states its regime in the same sentence as its number** — duel regime or army regime.

## Why this population and not another

- **Sane-only was rejected.** It requires a deployment policy — a positioning AI whose every blind spot silently becomes a measured *balance* fact — and it makes the spec's own *"hard counter with poor positioning should fall below 60%"* clause uncomputable, because it never samples poor positioning.
- **The full space was rejected.** It is not an enumerable object on a 60 × 80m field with twelve squads, and diluting with nonsense drags every matchup toward 50%: a genuine 80% hard counter would measure in the sixties and **the band would pass for the wrong reason**.

## Four gates from one sweep

- §27's bands read the matrix **mean**.
- "Flippable by positioning" reads whether any **cell crosses 50%** while the mean sits near even.
- The mispositioning clause becomes a **cell lookup** — "poor positioning" is a named archetype, not a mood.
- **F-5** reads a **variance decomposition**: main-effect variance (your own archetype choice) ÷ interaction variance (the specific pairing). If interaction dominates, positioning is a coin flip wearing a skill costume. No extra runs.

## Consequences

- **Cost, on the record:** the archetype set becomes **load-bearing spec**. Every balance number in the game is measured relative to it, so changing it invalidates prior measurements the way a schema migration invalidates a cache. It is versioned; the count of six is a dial.
- The set was subsequently authored as a **1,056-row coordinate table** with the build set as part of the artifact.
- The ~70% technology pick-rate target only becomes measurable here, since it requires a distribution to be a rate over.
