# ADR-0036 — The 60m field width is load-bearing on the wall-versus-concentrate trade

**Status:** accepted, with a correction · **Ticket:** [#12](https://github.com/marcneuwirth/warweave/issues/12), corrected by [#18](https://github.com/marcneuwirth/warweave/issues/18) · **Spec:** §23.6

## Context

The battlefield is 60m × 80m and nothing in the spec argued for either number. Measured against authored frontages, the width turns out to be doing two jobs.

## Decision

**60m is kept, and the frontage arithmetic becomes §23's stated reason for it.**

**A 12-squad army cannot deploy in one rank.** Even the narrowest-frontage army needs more than 60m for twelve squads. **Depth is therefore forced**, so frontline/backline structure is structural rather than optional and **screening is always available to every composition**. This is the strongest single argument that the no-terrain bet is survivable.

**The width creates a real trade.** *Wall* — spread a holding army across the front to deny the flank and the raid lane, at the cost of depth, reserve, and squads spread thin. *Concentrate* — mass twelve squads on a 30m front, take local superiority at the point of contact, and roll the line up from inside. Lateral distance is what makes concentration work: a reach squad 30m across the field cannot support the breach.

Widening to ~80m makes walling impossible and flanking **free** rather than earned; narrowing to ~40m kills flanking and raiding both.

## The correction

This decision was originally argued on the claim that **six holding squads span exactly 60m**, and concluded that one archetype could wall the field edge to edge — denying both the flank axis and the raid lane — and that its measured dominance was therefore *understated*.

**That arithmetic was centre-to-centre.** Distances are measured **surface-to-surface** and footprints may not overlap, so the true squad pitch is **10.8m** and six squads need **64.8m** on a 60m field. Five wall 54m and leave a **6m seam** — and it is **passable model by model** under individual collision. The correction was computed before the roster rotation and concluded the seam admits no squad at all; on the shipped roster the 3-model caster squads are 4.8m wide and pass it intact, which strengthens the finding rather than weakening it.

> **The full-width wall does not exist.** A holding army can make walling expensive; it cannot deny the lane.

The conclusion did not follow from the footprint rule it was built on. **The width stays load-bearing — on the seam rather than on a perfect wall**, and whether the dominant archetype's strength is still understated becomes a sweep question rather than a paper one.

## Consequences

- The `line` / `screened` archetype pair is the instrument for that sweep question.
- Recorded as the clearest instance in the effort of a conclusion surviving its own premise being corrected: the trade is real, the absolute claim was not.
