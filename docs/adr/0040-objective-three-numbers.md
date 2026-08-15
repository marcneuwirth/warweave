# ADR-0040 — The objective axis gets three numbers, and uncontested holds are undecidable by counts

**Status:** accepted · **Ticket:** [#13](https://github.com/marcneuwirth/warweave/issues/13) · **Spec:** §33.5

## Context

The objective introduced two dials with no falsification criterion — the **20s pursuit window** and the **per-model prorating** of the 400g threshold — and **the existing gates are structurally blind to both.** Match length cannot see the objective at all: the round stake is conserved and merely *split*, so the total never moves and only the split does. The gate would not notice if the objective became a mandatory 600-gold tax every round, nor if both players rationally ignored it.

## Decision

Three numbers, each attached to the decision it can falsify:

1. **Decoupling rate** — the fraction of rounds where the battle winner and the control winner differ. Band **20–50%**, and it is falsifiable at **both** ends: near 0% the objective is battle damage with extra steps and the 30% axis should be **deleted** rather than tuned; near 100% the battle result has stopped mattering.
2. **Wipe control share** — the fraction of the control axis earned by a player who wipes the enemy. **This is the pursuit window's gate**, and it finally connects an arbitrary constant to a measurement: 20s was sized to pay a decisive win ~20% of the axis, so the gate is that a wipe lands near that, and the 20s moves if it does not.
3. **Minimum banking commitment** — the distribution of squad value committed by raids that successfully bank. **This is the prorating gate**: the prediction that a real raid costs three squads is either true in the runner or it is not. Successful banks at one squad mean prorating is too weak; three squads reliably failing means the objective is uncapturable again in a new form.

## Uncontested holds

**No count disambiguates them.** Nobody contesting the point reads identically to both players *correctly* pricing the 30% axis as not worth 400 gold. One is broken and one is working, and the observation is the same.

The clause therefore hangs explicitly on **Instrument A** ([ADR-0039](0039-availability-vs-exercise.md)) — *is raiding in the top two headings?* — rather than on a fourth count. A measurement that cannot separate the two cases is not made trustworthy by being precise.

## Consequences

- Decoupling rate is the headline number, and the only one whose failure calls for **deleting** a mechanic rather than tuning it. That is deliberate: the axis was added to decouple control from the battle, so the gate measures the thing it was built to do.
- Every dial in the objective now has an instrument. The 20s and the 400g threshold stop being unfalsifiable choices and become measured ones.
