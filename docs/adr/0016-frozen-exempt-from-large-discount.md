# ADR-0016 — Frozen is exempt from the Large HardControl discount

**Status:** accepted · **Ticket:** [#9](https://github.com/marcneuwirth/warweave/issues/9) · **Spec:** §11.3, §12

## Context

§12 gives Large targets 50% HardControl duration. Frozen was the **only live referent** of that clause in v0.4 — and Frozen on a Large target is exactly the case the Magic branch exists to set up for a Heavy physical squad.

Worked out, the system was worse than the ticket suspected:

| Target | Frozen | Uptime at one caster | Ceiling | Heavy hits per freeze |
| --- | --- | --- | --- | --- |
| Small | 0.75s | 20.8% | 37.5% | 3.0 |
| Large, **before** | 0.375s | **10.4%** | 23.1% | 1.5 |
| Large, **after** | 0.75s | **20.8%** | 37.5% | 3.0 |

**10.4% on the one target a per-model freeze is worth gold on.**

## Decision

**Frozen no longer receives the Large 50% discount.** §12's clause stays on the books for Root and Stun and is therefore **inert in v0.4**.

## Why

The 1.25s Hard-Control Immunity is a sufficient brake on its own: it caps chain-locking at `0.75 / (0.75 + 1.25)` = **37.5%** regardless of how many casters are fielded. The Large discount was a **second brake on an already-braked mechanic**, and it blunted precisely the combination the roster is built around — the anti-Large physical technology got the *shortest* window to exploit its own payoff.

## Consequences

- Large targets lose a defensive property. Routed to repricing and accepted there.
- The clause is retained rather than deleted because Root and Stun return in the alpha; it is marked inert so the next reader does not mistake it for live.
- In the post-rotation roster **only one unit type is Large at all**, which makes this clause thinner still — recorded as an open weakness in the spec's §34.
