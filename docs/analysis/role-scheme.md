# The role-symmetric roster (#19)

Evidence for [#19](https://github.com/marcneuwirth/warweave/issues/19). Arithmetic in
[`matchup-math/roster19.py`](matchup-math/roster19.py); run `python3 roster19.py all`.

#14 ruled that v0.4's archetype field is a total order, that no continuous-stat lever
bends it into a cycle, and that the fix is structural — roles set the cycle's direction,
property-keyed conditionals give each edge its magnitude. It deliberately authored
neither. This document authors both and reports what the arithmetic then shows.

---

## 1. The rotation

#14 assigned each branch one role at *best* and one at *adequate*:

| Branch | best | adequate |
| --- | --- | --- |
| Military | hold | reach |
| Magic | reach | hold |
| Beast | access | hold |

Hold appears three times, reach twice, access once — and Military↔Magic is a **closed
pair**, each one's *adequate* being exactly the other's *best*. A Mil/Magic hybrid buys
hold-best and reach-best with both adequates redundant, which is precisely the
`MilMagic` 11–0 that topped #14's structural probe. The 11–0 was not a tuning artifact;
it is what the role table says should win.

**Ruling — rotation A.** Each branch's *adequate* is the role of the branch it beats:

| Branch | best | adequate | hole | beaten by |
| --- | --- | --- | --- | --- |
| Military | hold | access | **reach** | Magic |
| Magic | reach | hold | **access** | Beast |
| Beast | access | reach | **hold** | Military |

Every role is owned once at best and once at adequate; no two branches are mutual; every
pair leaves a real hole. The cycle's direction is no longer authored — it is **derived
from which hole each branch has**, which is the property #14's table lacked.

The opposite rotation (Military hold/reach, Magic reach/access, Beast access/hold) was
rejected: its whole appeal is that it changes nothing about Military, and Military is the
branch that went 15–0 while owning both best positions.

**Cost, recorded rather than discovered later:** Longbowmen drop from Affinity 2 to
Affinity 4 and become deliberately *weak* reach, and Frostcaller rises from 2 to 4. That
removes **Frostcaller + Longbowmen** — §9's showcase combo, which #10 concluded "the spec
is built around" — from the 3/3 hybrid space entirely, since #7 ruled secondary branches
stop at 3. It survives only in a 4/4 build.

---

## 2. The roster: 14 units

#14's "8 units" does not survive its own rulings — 9 today, minus Outriders is 8, **plus**
the new Magic holding unit is 9. The count was written before the new unit was added back.
The grilling session widened it further: a **tier-3 row at Affinity 4, two units per
branch**, filling the empty rung in §7's ladder (which currently buys units at 0 and 2 and
nothing at 3, 4 or 5 except a doctrine).

Affinity **4**, not the alpha table's 3: #7 puts the hybrid unlock at 3+3 and secondary
branches stop at 3, so a tier-3 row at 3 would hand **every 3/3 hybrid four capstones** and
inverts the deep/wide structure. At 4, a 3+3 hybrid gets none, a 4/4 build gets all four
but forfeits Affinity 5's doctrine, and a deep 5 build gets two plus the doctrine.

| Affinity | Military — hold-best | Magic — reach-best | Beast — access-best |
| --- | --- | --- | --- |
| 0 | **Spear Guard** · hold, best | **Ember Mage** · reach, best | **Direwolves** · access, best |
| 2 | **Knights** · access, adequate | **Lifewarden** · hold, adequate | **Troll** · reach, adequate |
| 4 α | **Longbowmen** · reach, weak | **Stormcaller** · access, weak | **Stonebacks** · hold, weak |
| 4 β | **Banner Guard** · hold, capstone | **Frostcaller** · reach, capstone | **Griffin** · access, capstone |

Common stays at two — **Militia** and **Hunters** — and generates no affinity, so it has no
tier-3.

Three map questions close here. The fog's *"is the new Magic holding unit genuinely new or
a §26 deferred unit arriving early"* → it is the **Lifewarden**, arriving early. #11's
neutered **Boulder Throw** becomes the Troll's baseline, because the Troll is now Beast's
reach rather than a confused brawler. And **Outriders stay deleted** — Knights are their
chassis, promoted into Military, where owning a role is permitted.

### The α / β fork

α **narrows the branch's hole** so it is not free-hit; β **escalates the role the branch
already wins with**. α is authored so that **weak-tier loses to adequate-tier of the same
role, always** — its job is to stop the branch being free-hit, never to contest the role.
The hole narrows; it never closes, because the hole is what the cycle is made of.

---

## 3. The guard rail: 25–40% per rung

#13 ruled a gate without a quantity is unevaluable in principle, so each role gets one:

| Role | Quantity |
| --- | --- |
| hold | eHP × frontage |
| reach | range × applied DPS |
| access | speed × screen-bypass — **not paper-gradeable** (#14); reported, not graded |

**Each rung differs from the next by 25–40%.** ≥25% because #12 established that as the
smallest magnitude that reads as a difference; <40% because a rung gap at #10's flip
magnitude would make *owning a role* itself a counter, and then α could not narrow a hole
without closing it.

```
HOLD    (eHP x frontage)                REACH   (range x dps)
  best     SpearGuard   17690             best     EmberMage    3293
  adequate Lifewarden   12830  -27.5%     adequate Troll        2280  -30.8%
  weak     Stonebacks    8352  -34.9%     weak     Longbowmen   1692  -25.8%

ACCESS  (speed x bypass)
  best     Direwolves      4.5
  adequate Knights         3.3  -27.8%
  weak     Stormcaller     2.2  -32.3%
```

All nine rungs land in band. One derivation fell out of the hold quantity and is worth
stating: **holding requires frontage, so a single-model squad cannot be a holding unit at
any HP total.** That is why Beast's hold-weak unit is a 4-model herd rather than a lone
monster, and it is also why the Troll had to become a 2-model squad to serve reach — which
independently reproduces #14's finding that Magic's collapse was model count.

---

## 4. The three counters

#14 ruled counters key on functional properties, never `branch`. Each branch needs one
*unavoidable* property — unavoidable because it falls out of how the branch wins.

| Branch | Exposed property | Why unavoidable | Counter |
| --- | --- | --- | --- |
| Military | formation coherence | holding a line *is* standing shoulder to shoulder | AoE catch `πr²/sp²` (#11) |
| Beast | closing speed (`Charging`) | access means crossing the gap | Brace vs `Charging`, −40% |
| Magic | model scarcity | reach-best is bought with range and output, not bodies | +40% vs squads of ≤3 models |

All three are `DamageModifier` on a predicate, so §25 is untouched, as #14 required.

They live at **step 3 of a tier-3 track**, so they are *earned by commitment* rather than
granted to everyone. The consequence is structural: **a wide build has no counter at all.**
A 3/3 hybrid covers every role and flips nothing; a deep build owns one flip and one hole.
That is §8's deep-vs-wide bet expressed as variance against coverage — the sharpest form it
has taken — and §5 below reports whether it survives contact with the arithmetic.

### Upgrade tracks

Two forked 3-step tracks per tier-3 unit, twelve in all; pick one at step 1 and climb it,
locked thereafter (§17 already forbids refunds). Each track is **one named effect at three
magnitudes**, crossing #10's ~+40% flip threshold only at step 3 — so partial investment is
**sub-flip** rather than inert, which is the failure mode #11 diagnosed in eight of the
existing eighteen technologies. Technologies stay on tiers 0/2 at §17's existing shape
(2 authored, buy 1), holding that pool at **16**.

---

## 5. What the arithmetic shows

Fifteen archetypes, each built to **≤3,500g (R8 cumulative income) and ≤12 squads**,
whichever binds first. #8 and #14 built at 12 squads regardless of gold; once tier-3 units
and tracks exist, that is no longer a comparable field.

### 5.1 The slot economics — a new, quantified defect

R8 income of 3,500g across a 12-squad cap gives **292g per affordable slot**. As first
authored, tier-3 units cost 350–450 and a full track cost 1,050g — **3.6 squad slots
forgone for one conditional.** Deep builds fielded 8 squads against wide's 12 and finished
**last in the field** (`MilDeepBodkin` 1–13, `BeastDeepSing` 0–14).

This is the mirror of #14's Magic diagnosis, applied to the whole deep archetype: it was
priced as though gold were binding, and #4 made slots binding from R4.

Repriced against the 292g/slot ceiling — tier-2 to **225 / 250 / 275**, tier-3 to
**300 / 325 / 350**, track steps to **150 / 200 / 250** (600 total) — deep moves from the
bottom of the field to competitive (`MagDeepChain` 13–1, `MilDeepRally` 9–5). The branch
price axis survives in relative terms, with **gateways fixed at 200g on every branch**
because #4's *400 = two gateways = Affinity 2* and #7's *5 × gateway = Affinity 5* both
rest on it.

### 5.2 The field

```
MilMagic        2650g  14-0        MilDeepBodkin   3550g   6-8
MagDeepChain    3450g  13-1        MagicBeast      2550g   6-8
PureMagic       2700g  12-2        PureMilitary    2700g   6-8
MagDeepFrost    3500g  10-4        PureBeast       2525g   6-8
SpearGuard12    2400g  10-4        Direwolves12    2400g   6-8
MilDeepRally    3700g   9-5        CommonHeavy     1400g   3-11
                                   BeastDeepStone  3475g   2-12
upsets = 6/105                     BeastDeepSing   3575g   1-13
                                   MilBeast        2600g   1-13
```

**Upsets rise from #14's 2/120 to 6/105** — the field has non-transitive structure for the
first time — but it is still much closer to a ladder than to a cycle.

### 5.3 The intended cycle: two of three

| Edge | Result |
| --- | --- |
| Magic > Military (reach into Military's hole) | **YES** — 11.2s, Magic at 54% |
| Military > Beast (hold into Beast's hole) | **YES** — 13.2s, Military at 88% |
| Beast > Magic (access into Magic's hole) | **no** — Beast wiped, Magic at 55% |

### 5.4 The Mil/Magic hybrid survives the rotation — and the reason matters

#19's stated first problem was #14's 11–0 Mil/Magic hybrid. Under rotation A it is
**14–0**, and it is the *cheapest* build in the top half at 2,650g.

Rotation A's central claim was that in a rotation, **every hybrid pair is symmetric** —
each covers all three roles with two bests and one adequate. The field falsifies the
claim's *observability*, not obviously the claim: `MilMagic` is 14–0, `MagicBeast` 6–8 and
`MilBeast` 1–13, when the structure says all three should be alike.

The simple explanation — that range is dominant in a 1-D closing model — was **tested and
rejected**: the correlation between an army's gold-weighted mean range and its win rate is
only **r = 0.43**, and `SpearGuard12` wins 71% at a mean range of 2.2m.

What remains is narrower and sharper: **access is worth approximately zero on this
instrument, so gold spent on Beast is gold spent on nothing.** `MilBeast` gives up five
Spear Guard squads to buy 1,050g of Beast units that the calculator values at nil; it
finishes below `SpearGuard12`, which is the same army with the Beast half deleted. Hybrid
symmetry cannot be *measured* here, because one of the three roles it balances across is
invisible to the measurement.

This refines #14 rather than overturning it. #14 said Beast's edge is not paper-gradeable
because access is 2-D. The sharper statement is that **the model-scarcity conditional makes
Beast's *edge* 1-D gradeable, but nothing makes Beast's *role* gradeable** — every Beast
row is a floor, not a measurement, because Beast pays gold for a capability the calculator
refunds at zero.

### 5.5 §29's seven categories

Scored as #13 redefined it — a two-sided 35–65% band, each category represented by its
best-performing build:

| Category | Representative | Rate | |
| --- | --- | --- | --- |
| Military/Magic | MilMagic | 100% | **top failure** |
| Pure Magic | MagDeepChain | 83% | **top failure** |
| Pure Military | SpearGuard12 | 67% | **top failure** |
| Pure Beast | PureBeast | 50% | OK |
| Magic/Beast | MagicBeast | 33% | **bottom failure** |
| Common-heavy | CommonHeavy | 17% | **bottom failure** |
| Military/Beast | MilBeast | 0% | **bottom failure** |

**Six of seven fail.** Every category containing Beast is a bottom failure and no category
without Magic or Spear Guard is a top failure — which is §5.4 restated at category scale.

§29 is therefore **still not repaired**. #14 made it repairable; #19 has repaired the
*structure* it needs and cannot demonstrate the repair on this instrument.

---

## 6. The Common invariant

#14 ruled Common must own no role. That says what Common is not. The definition adopted
here says what it is:

> **Common is the R1–R4 army.** It wins at the early-round budget, when gold binds and
> twelve slots are unreachable, and loses at the squad cap, when slots bind.

At the cap it holds cleanly: `CommonHeavy` loses to all three pure branch armies, and
finishes 3–11 overall. At the R2 budget (700g) Militia wins five of six unit matchups and
Hunters four of six; **Militia loses to the Ember Mage and Hunters lose to Spear Guard and
the Troll.** The per-unit form of the invariant is therefore too strong — reach beating a
melee swarm at equal gold is correct behaviour, not a violation — and it holds in its
army-level form only.

**F1 is not repriced.** Militia being undefeated at equal gold is the *specification* of a
Common unit, not a bug in it; #8's own inversion (8–0 at equal gold, 2–7 at twelve squads)
is the invariant working. #14 already found neither repricing moved any row but Militia's
own, and the reason is that Militia measures a budget that stops binding.

---

## 7. Verdict

The roster is authored, internally consistent, and passes every guard rail it was authored
against: nine rungs in band, the Common invariant holding at army level, the economy
identities intact, §25 untouched, the technology pool held at 16.

**The central claim is not confirmed.** Rotation A produces two of three edges, six upsets
in 105, and a hybrid at 14–0 that is the very build #19 was spawned to answer. Whether that
is rotation A failing or the instrument failing is **not decidable on paper**, because the
difference between the two hypotheses is the value of target access, and that is precisely
what #14 proved the calculator cannot price.

The honest handoff is a falsifiable prediction rather than a grading:

> **If target access is worth anything on a 2-D field, `MilMagic`'s 14–0 collapses and the
> Beast-containing categories rise into #13's band. If the runner reproduces 14–0 with
> access modelled, rotation A is falsified**, and the reserve levers are Q2's rotation B, a
> fourth role, or #12's player-set facing.

This is the second time the map has hit the same wall, and it is now the binding constraint
on the whole effort: **paper math grades roles and magnitudes; it cannot grade access.**
