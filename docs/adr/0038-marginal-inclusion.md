# ADR-0038 — "Competitively useful" means marginal inclusion, and "7 of 9" is replaced

**Status:** accepted · **Ticket:** [#13](https://github.com/marcneuwirth/warweave/issues/13) · **Spec:** §27.2, §33.3

## Context

The expansion gate required *"at least 7 of 9 units competitively useful"* and never defined the term. All three readings the ticket offered fail:

- ***Appears in a winning build*** passes a unit type that appears in armies **and makes them strictly worse** (7–2 at 2,400g → 1–8 at 3,000g). A passenger satisfies it.
- ***Appears in >X% of builds*** measures popularity, which is downstream of whoever authored the build set — circular.
- ***Best answer to a matchup*** demands a monopoly and kills legitimate second-best picks.

"7 of 9" also **tightens when the roster shrinks**: cut a failing unit type and the gate becomes 7 of 8, which is backwards when deletion is a legitimate remedy.

## Decision

> A unit type is **competitively useful** if there exists at least one army in the tested build set and at least one opponent archetype where **replacing it with the best legal substitute at equal spend turns a win into a loss**.

Substitution: same squad-slot count, filled from unit types the build's affinity already grants, gold difference banked rather than respent, at **fixed coordinates** — the substitute stands exactly where the replaced squad stood in all six archetypes. Measured in the **army regime**.

> **Every unit type in the shipped roster passes. At most two may fail, and each failure is resolved by deletion or by an explicit v0.4-provisional flag naming what would have to change.**

## Why

Marginal inclusion is **load-bearing in at least one winning army** — strictly stronger than appearing in one, strictly weaker than dominating a matchup. It is the only reading of the three that a passenger fails.

Fixing deployment during substitution also makes the gate **sharper**, not just cheaper: it isolates the unit type's contribution from a re-optimised layout, which is what the gate claims to measure.

## Consequences

- **The gate failed at the moment it was written**, and that is the finding: three unit types were candidates against a two-failure allowance. It therefore handed the core-bet work an **obligation** rather than a judgement call — at least one must be repriced into usefulness or deleted.
- That obligation was discharged by **deleting one unit type and rescuing two by role rather than by price** ([ADR-0046](0046-counters-key-on-properties.md)), taking failures to zero rather than flagging them.
- The allowance is stated as an absolute count precisely so that shrinking the roster cannot silently tighten the gate.
