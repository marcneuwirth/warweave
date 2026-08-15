# ADR-0034 — The positioning gate counts the dominant core only, at engagement scale, with stance included

**Status:** accepted · **Ticket:** [#12](https://github.com/marcneuwirth/warweave/issues/12) · **Spec:** §31 gate 4, §33.2

## Context

The gate read *"at least three near-even matchups can be flipped through positioning alone."* Three separate things in that sentence are unfalsifiable.

## Decision

> The gate is: **at least three of the four canonical positioning matchups flip through deployment and stance, without changing army composition, counting the dominant core only, measured at engagement scale (2–4 squads a side).**

## The three repairs

**1. Stance counts, and the gate must say so.** Stance is an order set in the planning phase, not a coordinate. Counting it silently while the gate says "positioning alone" is exactly the quiet reinterpretation the measurement work exists to eliminate. The boundary that carries the gate's real intent is **composition versus execution** — *can you beat a better army by playing the field better, without buying different units?* Stance is on the execution side.

**2. Only the dominant core counts.** Armies are persistent and income is ~550/round against 100–350g squads, so an army changes by **one to three squads** between rounds — and you just fought it. **Composition is a near-certain read; placement is a fresh guess every round.**

- The **dominant core** is correct against their *composition*, whatever their placement: screen the backline, don't leave two bearings open, match frontage. Readable, teachable, right every time.
- The **guessing margin** is correct only against their *placement*: which flank to weight, whether to raid, which lane.

> A flip counts only if the positioning choice **would hold against any competent placement**, not one specific one.

"Positioning alone" as written is satisfiable by **guessing right** — a coin flip that flips a matchup half the time technically flips it, and the gate would pass on mind-game variance while telling you nothing about whether the field has depth. The guessing margin stays as intended texture; it simply stops being *evidence*.

**3. The gate is measured at engagement scale.** The four levers have different minimum sizes:

| Lever | Minimum squads |
| --- | --- |
| Screening / backline protection | 2 defending |
| Stance | 1 |
| **Flanking** | **2 attacking** — one to pin, one on a second bearing |
| **Raid** | **3 attacking** — per-model decay puts a surviving raid at ~600g |

At unit-versus-unit scale **flanking and raiding cannot produce a flip at all** and the bet reduces to screening alone; at twelve squads a flip cannot be *attributed*, which fails the core-only standard on its own terms. 2–4 squads a side is not an invention — it is the scale a third of the canonical matchup list already uses, and the scale at which a player actually experiences a positioning decision.

## Consequences

- Four canonical positioning matchups (P1–P4) are specified, **one per lever**, so the gate tests breadth rather than one mechanism four times.
- **None can be settled on paper** — two-dimensional manoeuvre is precisely what the paper calculator cannot see — so they are specified with predicted flips for P1/P2 verification.
- Whether the margin dominates the core becomes a telemetry question, and is one of the five falsifiers ([ADR-0035](0035-terrain-answers-one-failure.md)).
- **A correction is issued to the one confirmed positioning result:** it compared two *different armies* (a squad swapped, not moved), which is a composition change under this ADR's own boundary. It establishes that **having** a screen matters; it does not establish that **placing** one does. That is P1, and it is unmeasured.
