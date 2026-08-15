# ADR-0014 — Doctrine re-choice is rate-limited, not merely priced

**Status:** accepted · **Ticket:** [#7](https://github.com/marcneuwirth/warweave/issues/7) · **Spec:** §9.1

## Context

With doctrines exclusive ([ADR-0013](0013-doctrines-are-exclusive.md)), a player whose build grows into a different branch needs a way to move the doctrine — without that becoming a re-roll every round.

## Decision

| Rule | Value |
| --- | --- |
| Target branch must already be at | Affinity 5 |
| Cost | **500 gold** — one round's plateau income |
| Activation | **immediate** |
| Lockout before re-choosing again | **3 rounds** |

## Why a velocity cap rather than a fee alone

Direct precedent: the sales refund rate alone could not separate *correction* from *rewrite*, and the answer was a velocity cap ([ADR-0010](0010-selling-reinstated.md)). Identical shape here — a fee alone cannot separate "my build grew into a different doctrine" from "I re-roll every round".

The two levers have different natures and that is why the split is made explicitly:

- **The 3-round lockout is structural** — three rounds is three rounds whether the most expensive unit costs 300 or 800.
- **The fee is a dial** — soft in v0.4's dead-gold tail, sharp in an alpha where apex pricing keeps gold live to R12.

**The fee is expressed as a relationship, not a value** — *one round's plateau income*, rounded to 500 for legibility — so it self-scales as the roster grows rather than becoming a stale number a future price list has quietly made trivial. It is also, incidentally, a new gold sink.

## Why immediate activation

An earlier draft delayed activation by one round, to stop a player counter-picking after inspecting the opponent. **That justification is void**: reveal is simultaneous and against the opponent's *previous* locked army, so neither player is responding to anything and both may switch.

What survives is a narrower argument — **persistence asymmetry**. Everything else about an army moves slowly and legibly (12 owned squads, 2 sales a round, technologies that never refund), which is what makes a stale snapshot a good predictor. A free-to-flip doctrine would be the one fast-moving hidden variable in an otherwise slow, legible game. **The lockout, not a delay, is what prevents that.**

## Consequences

- Puts a *deepen* decision at roughly R5, R8 and R11, which is part of why the affinity ladder itself did not need stretching ([ADR-0051](0051-common-is-the-r1-r4-army.md) discussion, [#14](https://github.com/marcneuwirth/warweave/issues/14) ruling 6).
- The fee and lockout are unvalidated and should be tuned together.
- **A doctrine nobody chooses, or a fee that priced re-choice out of existence, would be invisible to every other gate** — hence doctrine distribution and re-choice usage are non-optional playtest metrics ([ADR-0042](0042-no-threshold-without-n.md)).
