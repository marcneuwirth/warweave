# ADR-0042 — Explicability splits in two, "enjoyable" is deleted, and no threshold ships without a stated N

**Status:** accepted · **Ticket:** [#13](https://github.com/marcneuwirth/warweave/issues/13) · **Spec:** §31, §33.7, §33.8

## Context

Three of the human-facing gates cannot be evaluated as written, in three different ways.

## Decision

**1. "Players can explain why they won or lost" splits in two.** It is two claims in one sentence, failing independently and needing different remedies:

- **Prediction accuracy** (forward) — the player calls the round winner before reveal; measure the hit rate on non-close rounds. At chance, the counter-play loop is dead. *This is simultaneously the instrument for "does one round of inspection lag make counters guesses?" — one instrument, two questions.*
- **Attribution agreement** (backward) — the player names the decisive factor, **scored against the battle log** rather than accepted at face value, since "why did you win" invites rationalisation. Failing this means the simulation is a black box, which is a different defect with a different remedy.

**2. "A complete match is enjoyable without apex units" is deleted.** It cannot be falsified and every operationalisation smuggles in a proxy anyway. It is replaced by behavioural proxies the playtest list half-collects already: **voluntary rematch rate** and **build-change rate between consecutive matches** — the latter doing double duty as the exercise measure.

**3. No threshold without a stated N.** "Most battles", "uncommon" and "reasonably close" state no population, and a threshold without one is unfalsifiable regardless of how precisely it is worded, because any result is dismissible as too few matches.

> The measurement appendix requires a minimum match count per playtest gate. **A gate evaluated below its N is *unevaluated* — not passed and not failed.**

The per-gate N is deferred to the build effort, which alone knows its playtest capacity, and is flagged in the spec as awaiting it.

**4. The acceptance criteria carry a predicted-outcome column** — for each gate, what the paper math expects the first runner pass to show, and which ticket predicted it.

## Why the predicted-outcome column

Two reasons, and the second is the larger one.

A gate whose expected value is unstated can be **quietly declared passed by a friendly measurement**. And stating the predictions makes the acceptance section a **falsification test of the entire hardening effort**: if the runner disagrees with the paper predictions, the paper math was wrong — which is the single most valuable signal the build effort can send back. It is dated *"predicted at v0.4 write-up"* because the roster moved after several predictions were made.

## Consequences

- Net effect on the gate list: **one deleted, one relocated** (determinism → P0 engineering acceptance, since it is not a balance property), **six redefined, two added**.
- Two playtest metrics are non-optional and would otherwise never have been collected: **doctrine choice distribution** and **doctrine re-choice usage**. Once only one doctrine can be held, a doctrine nobody chooses passes every other gate, and a re-choice fee that priced re-choice out of existence would be invisible.
- **Only the 8–12 round bound and the economy identities are paper-gradeable.** Everything else reads off the sweep, which is a runner. What the hardening produced is **predictions, not gradings**.
