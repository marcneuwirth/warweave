# ADR-0029 — AoE catch is derived from formation spacing geometry, and "a 3m area" is a diameter

**Status:** accepted · **Ticket:** [#11](https://github.com/marcneuwirth/warweave/issues/11) · **Spec:** §22.4, §19.3

## Context

The calculator applied splash as *"the next k living models in the target contingent"* — a **list operation with no spacing check** — plus a flat AoE-resistance constant that appears nowhere in the spec. That is why an arrow volley appeared to help against twelve separate single-model squads, which is geometrically impossible.

## Decision

> **AoE catch is derived from formation spacing geometry.** Models on a lattice of pitch `sp` within radius `r` number approximately `πr² / sp²`. Single-model squads catch nothing; separate squads are never adjacent.
>
> **"Attacks target a 3m area" denotes a diameter — r = 1.5m.**

The redundant flat "−20% AoE damage received" clause on the spacing technology is **retired**: the spacing increase already *is* the resistance, and stating both pays twice for one idea.

## Why the diameter reading

At radius 3.0m an arrow volley would catch 7 of 8 models — **strictly more than a dedicated fireball at 2.5m**, which inverts the roster's implied ordering of focused splash < fireball < area doctrine. The diameter reading preserves that ordering. At default spacing the fireball still catches 4, so the elemental numbers set elsewhere are undisturbed; only spacing-modified targets move.

## Consequences

**One ruling repaired four technologies:**

- The volley technology was the real gate failure, not the penetration one: before the ruling it improved 6 of 7 sampled matchups and flipped a whole archetype; after it, it flips nothing and carries a genuine liability against single-model armies.
- The spacing technology went from **flatly inert to a real conditional without a single number changing** — it was inert because of how splash was modelled.
- The tight-formation technology's *stated* drawback finally exists.
- The spacing-insensitive area doctrine becomes the one AoE that a loosened formation cannot answer — a counter-relationship falling out of geometry rather than being authored.

**Two structural consequences beyond the pool:**

- **Formation spacing becomes a real defensive stat**, and therefore a property that can be countered — which is what later makes *formation coherence* the property Military cannot avoid exposing ([ADR-0046](0046-counters-key-on-properties.md)).
- `ModelCount` is added to the primitive set for the one technology that adds models, rather than the technology being rewritten to fit the list. It is the pool's strongest card and it buys back exactly the currency the squad cap rations, so legitimising it explicitly is better than leaving it as an unchallenged violation.
