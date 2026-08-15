# ADR-0044 — A tier-3 row of two unit types per branch, gated at Affinity 4

**Status:** accepted · **Ticket:** [#19](https://github.com/marcneuwirth/warweave/issues/19) · **Spec:** §7, §13–§16

## Context

The core-bet work said the roster would be "8 units", which does not survive its own rulings — nine today, minus the deleted Common cavalry is eight, **plus** the new Magic holding unit is nine. The count was written before the new unit was added back.

Separately, the affinity ladder buys unit types at 0 and 2 and **nothing at 3, 4 or 5 except a doctrine** — a long empty stretch on the ladder the whole deep-versus-wide bet runs along.

## Decision

**A tier-3 row: two unit types per branch, gated at Affinity 4.** The roster is **14 unit types** — Common 2, and four per branch.

| Affinity | Military | Magic | Beast |
| --- | --- | --- | --- |
| 0 | hold, **best** | reach, **best** | access, **best** |
| 2 | access, adequate | hold, adequate | reach, adequate |
| 4 **α** | reach, **weak** | access, **weak** | hold, **weak** |
| 4 **β** | hold, **capstone** | reach, **capstone** | access, **capstone** |

## Why Affinity 4, not 3

At 3, **every 3+3 hybrid would field four capstones** and the deep/wide structure inverts — wide would buy strictly more unit access than deep. At 4:

- a 3+3 hybrid gets **none**;
- a 4/4 build gets **all four** but forfeits Affinity 5's doctrine;
- a deep 5 build gets **two plus the doctrine**.

That is a real ladder with a real decision at each rung, and it fills the empty stretch without touching the affinity formula.

## The α / β fork

**α narrows the branch's hole; β escalates the role it already wins with.**

α is authored so that **weak-tier always loses to adequate-tier of the same role.** Its job is to stop the branch being free-hit, never to contest the role. **The hole narrows; it never closes, because the hole is what the cycle is made of.**

## Consequences

- Three open map questions close here: the new Magic holding unit is a deferred unit type arriving early; the Beast reach unit's optional thrown attack becomes its baseline; and the deleted cavalry stays deleted, its chassis promoted into Military.
- **Five deferred unit types arrive early, and the systems they were deferred to test do not arrive with them** — no flying, no healing, no chain effects, no Discipline, no trample. The spec states this explicitly so that the deferred-systems list is not quietly emptied by the roster.
- Tier-3 unit types carry **upgrade tracks instead of technologies** ([ADR-0045](0045-forked-tracks.md)), which holds the technology pool at 16.
