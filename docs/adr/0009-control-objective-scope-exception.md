# ADR-0009 — A battlefield objective is admitted despite `Terrain: None`

**Status:** accepted · **Ticket:** [#6](https://github.com/marcneuwirth/warweave/issues/6) · **Spec:** §5.5, §26

## Context

The scope table says `Terrain: None` and the deferred-systems list defers terrain to the alpha. The hardening map rules deferred systems out of scope as design work, with one stated escape hatch: *a ticket may move an excluded system back in, but the change must be argued and recorded as an ADR.* This is that argument.

## Decision

Each player has one **control point** at the centre of their own deployment band — `(30, 12)` and `(30, 68)`, 44m apart. No collision; it obstructs nothing and is a **scoring volume only**. A player banks control of the *enemy's* point by holding ≥400 gold of squad value within 8m for a continuous 3 seconds, exceeding the enemy's value inside that radius.

## Why the exception is narrow

**It is not terrain in the deferred sense.** No cover, no elevation, no pathing cost, no collision. Nothing about it changes how movement or line of sight work.

**It is load-bearing rather than decorative.** The ramp that fixes match length destroys the decisiveness signal, and this is what replaces it. Without it, [ADR-0007](0007-round-number-stake.md) makes Command damage a pure function of the clock.

## Why these numbers

- **Each player's point sits in their own territory, mid-band.** A single contested centre point pulls both armies into one scrum and flattens positional variety. Front-edge depth is ground you already occupy, so defence is free; back-edge depth puts a garrison out of the battle entirely. Mid-band puts defenders 12m behind their own line — far enough that garrisoning costs something, close enough to fall back into the fight. Attack-theirs/defend-yours also gives *time* a job: crossing the field costs seconds, so speed converts into Command.
- **400 gold stops cheap fast raiding.** Without it a lone 200g fast squad banks ~85% of a battle unopposed — a quarter of the round's stake for 200 gold and no fight, which is a dominant purchase.
- **3s dwell** stops a squad passing through en route to the fight from banking by accident, which would be unreadable.
- **8m radius** is sized to hold a qualifying force — a 16m diameter accommodates a 10m frontage plus a following rank.

## Consequences

- **The precedent does not reopen terrain.** It licenses scoring volumes with no physical presence, and nothing else.
- Round 1 is effectively uncapturable (400g is the entire starting army). Intended; round 1's stake is 7.
- Known decay: 400g is ~14% of a round-10 army, so raids get relatively cheaper late. If simulation shows late raids becoming free, switch to a fraction of deployed value rather than re-tuning the flat number.
- The objective was specified before any order existed that could reach it — see [ADR-0019](0019-raid-is-an-order-not-a-position.md).
