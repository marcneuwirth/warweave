# ADR-0011 — The squad cap is on ownership, not deployment: own 12 = field 12

**Status:** accepted · **Ticket:** [#4](https://github.com/marcneuwirth/warweave/issues/4) · **Spec:** §4.4

## Context

The scope table said "12 **deployed** squads" and §4 said a player "may **own/deploy** a maximum of 12". Those are different rules, and the difference decides whether a bench exists.

## Decision

**Own 12 = field 12.** One number, no bench.

## Why

A bench is a **commitment solvent**. With simultaneous reveal against the opponent's *previous* locked army, a player owning 20 and fielding 12 counter-swaps every round at zero cost — countering **and** staying deep. The deep-versus-wide tension and the central product test ("counter now, deepen, or weave") both require that countering costs something.

This is not marginal: by round 12 there is enough gold to bank 8–10 unfielded squads.

## Consequences

- The cap becomes a genuine second resource, and it binds at different rounds for different archetypes — R4 for the cheapest builds, R8–R10 for the most expensive. **The cap disciplines cheap builds; gold disciplines expensive ones.**
- It makes selling necessary rather than optional ([ADR-0010](0010-selling-reinstated.md)): under an ownership cap with no selling, a round-1 mistake is entombed for the whole match.
- 12 is kept. Raising to 15 pushes binding to R5–R10 and the cap stops being a resource for expensive builds at all; lowering to 10 binds mid-match for everyone but thins formations on a 60m field and costs the positional layer its texture.
- It makes the technology layer **cap relief** ([ADR-0028](0028-technology-layer-is-cap-relief.md)), because technologies add power without consuming a slot.
