# ADR-0043 — Each branch owns one role at best and one at adequate, in a rotation

**Status:** accepted · **Tickets:** [#14](https://github.com/marcneuwirth/warweave/issues/14), [#19](https://github.com/marcneuwirth/warweave/issues/19) · **Spec:** §1.1

## Context

The v0.4 archetype field is a **total order**: 120 pairings, **2 upsets**, one branch 15–0 at the top and another 0–15 at the bottom. "Counter now" presupposes that some army beats the army beating you; on this field no such army exists, so **the central strategic product test collapses before affinity timing is even relevant.**

Twelve repricings — every obvious lever handed over by the matchup tables — left a Military archetype on top in **every** row and Magic at the bottom in every row. **Continuous stats compose into something close to a scalar: they reorder a ladder, they cannot bend it into a cycle.** The one demonstrated two-way flip in v0.4 has a different shape — a *conditional* keyed on a property the opponent's build actually has.

The defect is in the branch charter. It granted *"combined arms"* and *"range control"* to one branch as **traits**, and the roster took it literally: that branch fielded a line **and** artillery while the other two fielded half-armies (**role asymmetry**), and it owned **both** best positions — the best front rank and the best far rank (**role monopoly**).

**Neither half of the fix works alone.** Property-keyed conditionals at flip magnitude, verified firing at scale, loosened the ladder from 2 to 7–9 upsets and **did not move the top**. Role symmetry alone revived a dead branch and **did not move the top**. Together, with the monopoly broken, the top finally moves.

## Decision

**Each branch owns exactly one role at *best* and one at *adequate*, assigned as a rotation — each branch's adequate role is the role of the branch it beats:**

| Branch | best | adequate | hole | beaten by |
| --- | --- | --- | --- | --- |
| Military | hold | **access** | reach | Magic |
| Magic | reach | **hold** | access | Beast |
| Beast | access | **reach** | hold | Military |

**Common owns no role at all.**

**Combined arms is what hybridisation buys**, not a branch trait. "Range control" leaves the charter.

## Why the rotation, and not the first assignment

The core-bet work's own table gave Military hold/reach and Magic reach/hold — a **closed pair**, each one's adequate being exactly the other's best, with hold owned three times and access once. A Military/Magic hybrid buys two bests with both adequates redundant, which is exactly the hybrid that topped that probe. **The 11–0 was not a tuning artifact; it is what the role table says should win.**

Under the rotation every role is owned once at best and once at adequate, no two branches are mutual, every pair leaves a real hole, and **the cycle's direction is derived from which hole each branch has** rather than authored on top of it. The opposite rotation was rejected: its whole appeal is that it changes nothing about the branch that went 15–0 while owning both best positions.

**Roles set the cycle's direction; conditionals give each edge its magnitude.** That is why the two layers are one decision rather than two.

## Consequences

- **Recorded cost:** the two units of the showcase combination the original spec was built around move to opposite sides of the affinity ladder, removing that combination from the 3/3 hybrid space entirely. It survives only in a 4/4 build.
- **A model-count finding falls out and is load-bearing:** Magic's collapse was never damage or armour — full armour bypass changed *nothing* and doubling caster DPS changed nothing, while making the casters multi-model squads took a pure Magic army from 0–15 to 8–7. Magic was priced as though gold were binding, when the cap makes slots binding from R4.
- **One unit type is deleted** — the Common cavalry chassis, which under the role scheme would have to own a role, which Common may not. Its chassis is promoted into Military, where owning a role is permitted, and its technology slot leaves with it.
- **Two failing unit types are rescued by role rather than by price** ([ADR-0046](0046-counters-key-on-properties.md)), discharging the marginal-inclusion obligation to zero failures.
- **The rotation's symmetry claim is not confirmed**, and the reason is recorded in the spec's §34: one of the three roles it balances across is worth ~0 on a one-dimensional instrument, so hybrid symmetry is **unobservable** rather than falsified.
