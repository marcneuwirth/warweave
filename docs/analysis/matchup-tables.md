# Canonical matchup tables — WARWEAVE v0.4

Evidence base for [Compute the canonical matchup tables](https://github.com/marcneuwirth/warweave/issues/8).
Paper math only, per the map's validation method. **No decisions are made here** — every defect
below is flagged and routed, not resolved.

Computed against the hardened kernel, not `initial-spec.md` as written:

- [Fix the combat math kernel](https://github.com/marcneuwirth/warweave/issues/2) — three-bucket
  pipeline, magic halves armour before the curve, **no overkill carry**, squad-level targeting with
  per-model resolution, Shatter on `Heavy` at +25%, Hunters and Longbowmen at **0 armour**.
- [Fill the numeric mechanics gap](https://github.com/marcneuwirth/warweave/issues/3) — speeds,
  spacings, footprints, surface-to-surface distances, 32m opening gap, Stance.
- [Audit the elemental loop](https://github.com/marcneuwirth/warweave/issues/9) — Burning at 10/s,
  fireball 50% splash falloff, magic +25% vs Frozen, Frozen exempt from the Large discount.

---

## 0. Method, and what it cannot see

Every figure comes from a 0.02s-tick deterministic resolution of a one-dimensional engagement:
both sides start **32m** apart, the shorter-ranged side Advances and the longer-ranged side Holds,
projectile travel is folded into the closing distance, damage is applied per model with **no
overkill carry**, and melee attackers are capped by contact geometry (below). Cooldowns are
staggered per model per the kernel.

Three modelling rules do real work and should be read as claims, not plumbing:

**Contact geometry — rank 2 can attack only if `reach ≥ spacing`.** Surface-to-surface, a rank-2
model sits exactly one spacing interval behind contact. At 2.0m spacing:

| Squad | Formation | Reach | Models that can attack a line |
| --- | --- | --- | --- |
| Militia | 4×2 | 1.0m | **4 of 8** |
| Direwolves | 4×2 | 1.0m | **4 of 8** |
| Spear Guard | 6×1 | 2.2m | 6 of 6 |
| Outriders | 3×1 | 1.2m | 3 of 3 |
| Troll | single | 2.4m | 1 of 1 |

**Against a single-model target, everyone attacks.** The ring at `r_target + r_attacker + reach`
has room for 17–24 attackers, well past any squad size — so envelopment is unconstrained and the
rank-2 penalty vanishes. Militia and Direwolves therefore double their effective DPS the moment the
target is a Troll or a caster rather than a line.

**Equal-gold matchups are gold-independent.** `TTK(A→B) = (cost_A / cost_B) × (eHP_B / DPS_A)`, and
the budget cancels. Every "equal gold" figure below therefore holds at any budget; 1,200g is used
only to keep model counts whole.

The arithmetic is in [`matchup-math/`](./matchup-math/) — `mm.py` (kernel, contact geometry,
per-gold tables), `sim2.py` (engagement resolution, technologies, elemental states), `canon.py`
(the §28 suite). It is a calculator for the paper math, not a balance runner: no AI, no
two-dimensional movement, no rounds, no Command. The map's method stands.

**What this cannot see.** No two-dimensional manoeuvre, so flanking, wrap-around and `Exposed`
corridor geometry are absent; screening is modelled as a binary target-redirect, not a lane. No
Command, no rounds, no reinforcement. Frost Armor, Firestorm and Boulder Throw are approximated
(noted where they appear). Everything here is a **defensible starting value awaiting simulation**.

---

## 1. Per-gold and per-slot reference tables

### 1.1 Damage per gold

Squad DPS after armour, divided by cost. Ranged squads fire every model; melee figures are raw
(before the contact cap in §0).

| Unit | Cost | vs 0 armour | vs 20 | vs 25 (Troll) | vs 30 (Spear Guard) | vs 70 (Stonehide) |
| --- | --- | --- | --- | --- | --- | --- |
| **Militia** | 100 | **2.400** | **2.000** | **1.920** | **1.840** | **1.360** |
| **Direwolves** | 200 | 1.511 | 1.244 | 1.200 | 1.156 | 0.889 |
| Spear Guard | 200 | 0.960 | 0.800 | 0.760 | 0.720 | 0.560 |
| Hunters | 150 | 0.875 | 0.729 | 0.688 | 0.667 | 0.500 |
| Longbowmen | 250 | 0.650 | 0.542 | 0.517 | 0.500 | 0.375 |
| Outriders | 200 | 0.412 | 0.338 | 0.330 | 0.315 | 0.240 |
| Ember Mage | 200 | 0.211 | 0.191 | 0.187 | 0.182 | 0.156 |
| Troll | 300 | 0.175 | 0.145 | 0.140 | 0.133 | 0.102 |
| Frostcaller | 225 | 0.111 | 0.099 | 0.099 | 0.096 | 0.081 |

### 1.2 Effective HP per gold

| Unit | Raw squad HP | eHP vs physical | per gold | eHP vs magic | per gold |
| --- | --- | --- | --- | --- | --- |
| **Spear Guard** | 1,260 | 1,638 | **8.19** | 1,449 | 7.25 |
| **Militia** | 800 | 800 | **8.00** | 800 | **8.00** |
| Troll | 1,250 | 1,562 | 5.21 | 1,406 | 4.69 |
| Direwolves | 1,000 | 1,000 | 5.00 | 1,000 | 5.00 |
| Outriders | 780 | 936 | 4.68 | 858 | 4.29 |
| Hunters | 600 | 600 | 4.00 | 600 | 4.00 |
| Longbowmen | 675 | 675 | 2.70 | 675 | 2.70 |
| Ember Mage | 360 | 360 | 1.80 | 360 | 1.80 |
| Frostcaller | 390 | 390 | 1.73 | 390 | 1.73 |

**Militia is first or second on both axes simultaneously.** No other unit is top-three on both.
This is the arithmetic behind §3.1.

### 1.3 Per slot — the other budget

[The economy ticket](https://github.com/marcneuwirth/warweave/issues/4) fixed the cap at **own 12 =
field 12**, so a squad slot is a second currency and the two rankings are almost inverted.

| Unit | Cost | DPS / slot | eHP / slot | DPS / gold | 12-squad army cost |
| --- | --- | --- | --- | --- | --- |
| Direwolves | 200 | **302.2** | 1,000 | 1.511 | 2,400 |
| Militia | 100 | 240.0 | 800 | **2.400** | **1,200** |
| Spear Guard | 200 | 192.0 | **1,638** | 0.960 | 2,400 |
| Longbowmen | 250 | 162.5 | 675 | 0.650 | 3,000 |
| Hunters | 150 | 131.2 | 600 | 0.875 | 1,800 |
| Outriders | 200 | 82.5 | 936 | 0.412 | 2,400 |
| Troll | 300 | 52.5 | 1,562 | 0.175 | **3,600** |
| Ember Mage | 200 | 42.2 | 360 | 0.211 | 2,400 |
| Frostcaller | 225 | 25.0 | 390 | 0.111 | 2,700 |

A full Militia army costs **1,200 gold against R8's 3,500 cumulative income**. That gap is the
whole story of §3.1 — and the reason the dominance has a hard expiry date.

### 1.4 Overkill efficiency — the invisible tax

Fraction of dealt damage that lands on living HP, given `ceil(HP / hit)` and no carry.

| Attacker ↓ / Target → | Militia | Hunters | Outriders | Spear Guard | Longbowmen | Ember | Frost | Direwolves | Troll |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Militia | 83% | 100% | 95% | 91% | 90% | 100% | 100% | 83% | 98% |
| Hunters | 79% | 95% | 93% | 94% | 80% | 95% | 93% | 99% | 100% |
| Outriders | 91% | 73% | 96% | 100% | 82% | 94% | 89% | 76% | 98% |
| Spear Guard | 69% | 83% | 93% | 97% | 94% | 94% | 90% | 87% | 100% |
| **Longbowmen** | **64%** | 77% | 100% | 88% | 87% | 92% | 100% | 80% | 96% |
| Ember Mage | 53%¹ | 63% | 76% | 85% | 71% | 95% | 82% | 66% | 99% |
| Frostcaller | 74% | 89% | 93% | 90% | 100% | 100% | 96% | 93% | 98% |
| Direwolves | 98% | 88% | 93% | 90% | 99% | 96% | 96% | 92% | 99% |
| **Troll** | 95% | **57%** | 100% | 88% | **64%** | 86% | 93% | **60%** | 99% |

¹ Ember Mage's splash recovers most of this in practice; the primary-target figure is shown.

**This is the largest hidden variable in the game.** The Troll wastes 40–43% of its damage against
Hunters, Longbowmen and Direwolves; Longbowmen waste 36% against Militia. Nothing in a stat block
shows it, and it moves matchups by more than most technologies do. Routed to
[the balance-target ticket](https://github.com/marcneuwirth/warweave/issues/13) as a §31
explicability risk.

---

## 2. Equal-gold matrix — every unit against every other unit

Budget-independent (§0). **W** = row wins, **L** = row loses; `time / row's surviving squad HP %`.

| ↓ vs → | Militia | Hunters | Outriders | Spear&nbsp;Gd | Longbow | Ember | Frost | Direwolves | Troll |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Militia** | — | W 10.1s / 56% | W 10.9 / 83 | W 14.3 / 61 | W 9.3 / 65 | W 7.9 / 69 | W 7.5 / 96 | W 7.5 / 65 | W 9.2 / 96 |
| **Hunters** | L | — | W 8.6 / 85 | L 25.7 | W 13.4 / 25 | W 6.5 / 72 | W 5.8 / 96 | W 9.4 / 50 | W 10.7 / 98 |
| **Outriders** | L | L | — | L 12.8 | L 8.6 | W 14.1 / 8 | W 8.1 / 89 | L 10.8 | W 22.6 / 70 |
| **Spear Guard** | L 14.3 | W 25.7 / 8 | W 12.8 / 75 | — | W 12.4 / 44 | W 9.4 / 61 | W 8.6 / 92 | W 11.7 / 57 | W 12.4 / 92 |
| **Longbowmen** | L | L | W 8.6 / 76 | L 12.4 | — | W 4.5 / 100 | W 4.1 / 100 | L 7.7 | W 9.9 / 97 |
| **Ember Mage** | L | L | L | L | L | — | W 11.5 / 72 | L | L 25.3 |
| **Frostcaller** | L | L | L | L | L | L | — | L | L |
| **Direwolves** | L 7.5 | L 9.7 | W 10.8 / 69 | L 11.9 | W 7.7 / 45 | W 5.7 / 69 | W 5.3 / 93 | — | W 7.7 / 94 |
| **Troll** | L | L | L 22.6 | L | L | W 25.3 / 43 | W 17.3 / 85 | L | — |

Win counts out of eight: **Militia 8**, Spear Guard 7, Hunters 6, Direwolves 5, Longbowmen 4,
Outriders 3, Troll 2, Ember Mage 1, **Frostcaller 0**.

---

## 3. Dominant strategies

### 3.1 Militia is undefeated at equal gold — and its counters fail too

Militia wins **8 of 8** equal-gold unit matchups. It also beats every archetype, including the two
things the spec designates as anti-swarm:

| Militia ×12 (1,200g) vs, at equal gold | Result |
| --- | --- |
| Direwolves ×6 | **W** 7.5s, 65% left |
| Spear Guard ×6 | **W** 14.3s, 61% |
| Longbowmen ×4.8 | **W** 9.3s, 65% |
| Troll ×4 | **W** 9.2s, **96%** |
| Ember Mage ×6 | **W** 7.9s, 69% |
| Ember Mage ×5 + Firestorm (1,250g) | **W** 7.6s, 73% |
| Ember Mage ×4 + Longbowmen ×1.6 + Volley Fire (1,450g) | **W** 8.5s, 62% |
| Spear Guard ×3 + Longbowmen ×2.4 | **W** 11.9s, 61% |

Three compounding causes, all introduced by the hardening rather than present in v0.4 as written:

1. **Cheapest DPS and near-cheapest eHP at once** (§1.1, §1.2). Militia is the only unit top-two on
   both axes.
2. **No overkill carry** makes 100 HP/model the best defensive stat in the game against exactly the
   units built to punish it — Longbowmen 64%, Ember Mage 53%, Spear Guard 69%.
3. **The fireball's new 50% falloff** ([the elemental
   ticket](https://github.com/marcneuwirth/warweave/issues/9)) halved the AoE answer at the same
   moment the burn tick made it necessary. Ember Mage now loses to an equal-gold Militia force in
   both §28 listings of that fight (matchups 2 and 7b), and Firestorm does not change it.

Each fix was individually correct; the interaction is what compounds. **Not resolved here.**

### 3.2 But Militia collapses at the squad cap — and pure Military is undefeated there

Militia's dominance is purely gold-bound. At the cap it can only spend 1,200 gold, and the ordering
inverts. Twelve-squad armies, round robin:

| Army | Gold | W–L |
| --- | --- | --- |
| **Spear Guard ×6 + Longbowmen ×6** | 2,700 | **9–0** |
| Spear Guard ×12 | 2,400 | 8–1 |
| Direwolves ×12 | 2,400 | 7–2 |
| Militia ×6 + Longbowmen ×6 | 2,100 | 6–3 |
| Militia ×4 + Spear Guard ×4 + Longbowmen ×4 | 2,200 | 5–4 |
| Spear Guard ×4 + Longbowmen ×4 + Frostcaller ×4 | 2,700 | 4–5 |
| Hunters ×12 | 1,800 | 3–6 |
| **Militia ×12** | **1,200** | **2–7** |
| Direwolves ×6 + Troll ×6 | 3,000 | 1–8 |
| **Ember Mage ×6 + Frostcaller ×6** | 2,550 | **0–9** |

**Two regimes, and the crossover is exactly the round [the economy
ticket](https://github.com/marcneuwirth/warweave/issues/4) identified as cap-binding** (R4 for
swarm builds). Before it, gold is scarce and Militia is strictly dominant; after it, slots are
scarce and Militia is second-worst. This is an *interaction discontinuity*, not a curve — see §6.1.

### 3.3 Pure Military beats every §29 category

The full-build round robin §29 asks for, all at 12 squads:

| Archetype | Composition | Gold | W–L |
| --- | --- | --- | --- |
| **Pure Military** | Spear Guard ×6, Longbowmen ×6 | 2,700 | **9–0** |
| Military / Beast | SG ×4, LB ×4, Direwolves ×4 | 2,600 | 8–1 |
| Beast without Troll | Direwolves ×12 | 2,400 | 7–2 |
| Military / Magic | SG ×4, LB ×4, Ember ×2, Frost ×2 | 2,650 | 6–3 |
| **Mil 5 / Mag 3 / Beast 3** (#7's prediction) | SG ×3, LB ×3, Frost ×3, Wolves ×3 | 2,625 | 5–4 |
| Common-heavy | Militia ×6, Hunters ×4, Outriders ×2 | 1,600 | 4–5 |
| Pure Beast | Direwolves ×8, Troll ×4 | 2,800 | 2–7 |
| Magic / Beast | Wolves ×6, Ember ×3, Frost ×3 | 2,475 | 2–6 |
| Magic + Militia screen | Militia ×6, Ember ×3, Frost ×3 | 1,875 | 1–7 |
| **Pure Magic** | Ember ×6, Frostcaller ×6 | 2,550 | **0–9** |

**§29 is violated on two counts.** Pure Military beats every other category, and Pure Magic wins
nothing — §29 requires at least one winning build from every category, and forbids a build
dominating merely by system access.

**This also falsifies [the affinity-curve ticket's](https://github.com/marcneuwirth/warweave/issues/7)
prediction.** 5/3/3 was named as the convergent build every archetype must beat; it goes 5–4 and
loses to pure Military, Military/Beast and Beast. On current numbers there is nothing to converge
on but Military. Routed to [Stress-test the core
bet](https://github.com/marcneuwirth/warweave/issues/14).

---

## 4. The eleven §28 canonical matchups

At natural squad scale. Gold is asymmetric by design here — these test whether the *intended*
counter functions, not whether it is fairly priced.

| # | Matchup | Winner | Time | Survivor's HP |
| --- | --- | --- | --- | --- |
| 1 | Militia (100g) vs Direwolves (200g) | Direwolves | 8.1s | 50% |
| 1b | Militia ×2 (200g) vs Direwolves | **Militia** | 7.4s | 62% |
| 2 | Militia vs Ember Mage (200g) | Ember Mage | 10.1s | 33% |
| 3 | Hunters (150g) vs Direwolves | Direwolves | 8.5s | 38% |
| 3b | Hunters ×2 (300g) vs Direwolves | **Hunters** | 5.6s | 92% |
| 4 | Spear Guard vs Direwolves (200g each) | **Spear Guard** | 10.8s | 54% |
| 5 | Spear Guard (200g) vs Troll (300g) | **Spear Guard** | 18.0s | 67% |
| 5b | Spear Guard + Hooked Spears (450g) vs Troll | Spear Guard | 13.3s | 77% |
| 6 | Longbowmen (250g) vs Troll (300g) | **Longbowmen** | 14.7s | 60% |
| 6b | Longbowmen vs Troll + Stonehide (550g) | **Troll** | 27.4s | 21% |
| 6c | Longbowmen + Bodkin (500g) vs Troll + Stonehide | **Longbowmen** | 14.6s | 64% |
| 7 | Ember Mage (200g) vs Militia (100g) | Ember Mage | 10.1s | 33% |
| 7b | Ember Mage vs Militia ×2 (200g) | **Militia** | 7.9s | 51% |
| 8 | Ember Mage (200g) vs Troll (300g) | **Troll** | 14.4s | 63% |
| 8b | Ember Mage + Focused Flame (450g) vs Troll | **Troll** | 14.4s | 36% |
| 9 | Frostcaller + Longbowmen (475g) vs Troll | Longbowmen line | 11.6s | 80% |
| 9b | + Deep Freeze (725g) vs Troll | Longbowmen line | 10.6s | 80% |
| 9c | Longbowmen alone (250g) vs Troll — *control* | Longbowmen | 14.7s | 60% |
| 10 | Outriders ×2 (400g) vs protected line (450g) | **Line** | 11.7s | 74% |
| 10b | Outriders ×2 + Javelin Volley (600g) vs line | **Line** | 11.7s | 70% |
| 11 | Direwolves ×2 (400g) vs protected line (450g) | **Line** | 9.1s | 66% |
| 11b | Direwolves ×2 vs **unprotected** Longbowmen ×2 (500g) | **Direwolves** | 16.0s | 2% |

"Protected ranged line" = Spear Guard (200g) screening Longbowmen (250g).

**Four of the eleven behave as the spec intends.** Spear Guard beats both Direwolves and the Troll
on reach alone, exactly as [the mechanics ticket](https://github.com/marcneuwirth/warweave/issues/3)
predicted from 2.2m surface-to-surface. Longbowmen focus-fire the Troll down. Bodkin Arrows answers
Stonehide. Screening works — see §5.

**Three do not**, and each is flagged below: Ember Mage's anti-swarm role (#7b), the Troll's price
(#5, #6, and §4.2), and the Frostcaller + Longbowmen combo (#9).

### 4.1 Matchup 9 — the combo the spec is built around pays 3.1 seconds

| Configuration | Cost | Kills the Troll in |
| --- | --- | --- |
| Longbowmen alone | 250g | 14.7s |
| Frostcaller + Longbowmen | 475g | 11.6s |
| Frostcaller + Deep Freeze + Longbowmen | 725g | 10.6s |

§15 gives Frostcaller the role "setup for physical damage", and the elemental audit rebuilt Frozen
specifically so this combo could function. Adding a 225g Frostcaller to a 250g Longbowmen squad —
a **90% cost increase** — buys **21% faster**. Deep Freeze adds 250g more for another 8.6%.

The arithmetic is straightforward and was foreseen: 20.8% uptime × +25% Shatter on the fraction of
volleys landing in-window is a small number, and the Troll is a single model, so a per-model freeze
also denies only one attacker. The elemental audit called this out as "real identity, thin numbers".
**These are the numbers.** Routed to [Weigh deep doctrines against hybrid
unlocks](https://github.com/marcneuwirth/warweave/issues/10) and #13.

### 4.2 Matchup 5 and 6 — the Troll is not a frontline

The 300-gold Beast 2 gateway unit loses at equal gold to six of eight units, loses at *below* equal
gold to Spear Guard (200g, 67% left) and Longbowmen (250g, 60% left), and **makes a Beast army worse
by joining it**: Direwolves ×12 goes 7–2 for 2,400g, while Direwolves ×6 + Troll ×6 goes 1–8 for
3,000g. Twelve Militia beat four Trolls at equal gold with **96%** of their HP intact.

Causes: 52.5 DPS/slot (second-worst in the game), 2.0s cooldown into a no-carry kernel (40–43%
overkill waste against every multi-model squad), and regeneration that is irrelevant while it is
being focused. Its 1,562 eHP is real but 5.21 eHP/gold is below Spear Guard's 8.19.

---

## 5. Position-insensitive counters — the positioning bet holds

The one clean result. A 200g Spear Guard screen in front of a 250g Longbowmen squad **completely
reverses** both fast-attacker matchups:

| Attacker (400g) | vs unprotected Longbowmen ×2 (500g) | vs Spear Guard + Longbowmen (450g) |
| --- | --- | --- |
| Direwolves ×2 | **wins**, 2% HP left | **loses**, line keeps 66% |
| Direwolves ×2 + Pack Hunter (650g) | — | loses, line keeps 46% |
| Outriders ×2 | — | loses, line keeps 74% |

The `Exposed` gate from the mechanics ticket is doing exactly what it was written to do: the screen
redirects the wolves into their worst matchup rather than merely absorbing them. **No
position-insensitive counter was found** — every fast attacker's win is conditional on the defender
failing to screen.

Two riders for [Test the positioning bet](https://github.com/marcneuwirth/warweave/issues/12):
the reversal is total rather than graduated (2% survival becomes 0% survival, no middle), which
matches the known 4m-corridor cliff; and this model treats screening as a binary redirect, so the
*sharpness* is assumed rather than measured. The finding is that screening matters, not that its
current shape is right.

---

## 6. Interaction discontinuities

### 6.1 The squad cap inverts the entire value ordering

Militia goes from **8–0** at equal gold to **2–7** at equal slots; Longbowmen from 3–5 to a
component of the undefeated build. Nothing in §4 or §13 tells a player that a unit's value depends
on which budget is currently binding, and the switch happens in a single round when the twelfth
squad is bought. Routed to #13 and #14.

### 6.2 Rank 2 never fights

Militia and Direwolves field **4 of 8** models in a frontal line engagement and **8 of 8** against
a single-model target — a silent 2× DPS swing driven by `reach < spacing`, visible nowhere in the
stat block. It is the single largest reason Spear Guard (6×1, 2.2m reach, all six attacking) beats
both of them. Whether that is intended depth or an invisible trap is a §31 explicability question
for #13.

### 6.3 Stonehide is a hard on/off switch

Longbowmen beat a plain Troll (14.7s, 60% left) and **lose** to a Stonehide Troll (27.4s, wiped).
Bodkin Arrows flips it straight back (14.6s, 64% left) — better than against the *unarmoured* Troll,
because +60 penetration against 70 armour outruns the -10% damage. A 250g tech that decides a
matchup in both directions with nothing in between. Routed to [the tech
audit](https://github.com/marcneuwirth/warweave/issues/11).

---

## 7. Technology audit input

Deltas measured as the same matchup with the technology on and off. **This is evidence for
[the tech audit](https://github.com/marcneuwirth/warweave/issues/11), not a verdict.**

> **Superseded by #11.** Everything in this section was measured in single-squad equal-gold fights.
> Technologies cost no squad slot, so the layer is *cap relief* and these are the wrong regime —
> the same inversion §6.1 describes for units. #11 re-derived all eighteen inside 12-squad armies
> ([`matchup-math/tech11.py`](./matchup-math/tech11.py)) and overturned **F12** (Stonehide flips
> nothing at the cap) and **F15** (Frost Armor is positive at six casters; "measurably worse" was a
> single-caster artifact). #11 also ruled that **AoE catch derives from formation spacing geometry**
> rather than the list-based splash used here, which moved Volley Fire, Loose Formation and Phalanx.
> `sim2.py` carries that ruling; the figures below predate it.

### Mandatory (flips a result)

| Tech | Evidence |
| --- | --- |
| **Bodkin Arrows** | Longbowmen vs Stonehide Troll: loss (wiped, 27.4s) → win (64% left, 14.6s). Does nothing against the six 0-armour units. |
| **Volley Fire** | Longbowmen vs Militia ×2: loss (wiped) → win (60% left). The only counter Longbowmen have to their own 64% overkill efficiency. |
| **Hooked Spears** | Spear Guard vs Troll: 18.0s → 13.3s (26% faster); vs Outriders 12.2s → 10.5s. The `Heavy` tag it grants is a second, unpriced payoff. |

### Inert or near-inert (< 5% measured delta)

| Tech | Evidence |
| --- | --- |
| **Flanking Maneuver** | **Never fires.** Confirms the mechanics ticket's structural finding — solo flanking is impossible at 120°/s, and nothing else pins a target's facing. A 200g tech with no trigger. |
| **Firestorm** | Ember Mage vs Militia ×2 and ×4: identical result with and without, at +250g. Every fourth cast at 5m/70% does not change who dies first. |
| **Pounce** | Direwolves vs Longbowmen: identical. One +25% hit per wolf, once, is inside the noise. |
| **Rapid Fire** | Hunters ×2 vs Direwolves: 5.6s → 5.7s. -25% cooldown and -15% damage very nearly cancel. |
| **Loose Formation** | Hunters ×2 vs Ember Mage: 5.2s either way. The -20% AoE is real but the matchup does not last long enough to bank it. |
| **Pitch & Torch** | vs Direwolves (Small, no Burning) −0.2s; vs Troll −0.3s. Much weaker than the elemental audit feared — its regen suppression matters only in fights the Troll survives, and it does not. |
| **Focused Flame** | Ember Mage still loses to the Troll (14.4s either way); it dies with 36% of the Troll gone instead of 63%. Improves the loss, does not flip it. |
| **Frost Armor** | Frostcaller + Spear Guard vs Troll: 25.2s → 28.6s at +250g — measurably **worse**, because the shield extends a fight the line was winning on attrition. Approximated (nearest damaged ally, Large preferred); treat as directional. |

### Conditional

| Tech | Evidence |
| --- | --- |
| **Conscription** | Militia vs Direwolves: extends the loss from 8.1s to 11.5s and takes the wolves from 50% to 17%. Real, but at +200g on a 100g squad it is the most expensive relative purchase in the game. |
| **Javelin Volley** | The only thing that makes Outriders win anything: vs Hunters, loss → win (29% left). Does not help against a screened line (10 vs 10b: no change). |
| **Phalanx** | Spear Guard vs Direwolves: 54% → 65% survival. Consistent, modest, never decisive. |
| **Stonehide** | Flips Longbowmen (§6.3) and improves the Troll's loss to Spear Guard (12.8s → 15.8s) without flipping it. |
| **Pack Hunter** | Direwolves ×2 vs a screened line: still a loss, line 66% → 46%. Helps a fight wolves should not be taking. |
| **Deep Freeze** | §4.1 — 8.6% faster for 250g. |
| **Boulder Throw** | Modelled as a 13m stand-off (the Troll Holds rather than closing). vs Militia ×3 it still loses at 96% enemy HP; vs Spear Guard ×1.5 it loses. In a melee engagement it never fires at all, since the Troll's target is inside 5m. |

**Ten of eighteen technologies are inert or near-inert on these numbers**, and three are mandatory
in specific matchups. §17's "one meaningful specialization decision per unit" does not currently
hold for Outriders (one dead, one mandatory), Ember Mage (both weak), Hunters (both near-inert) or
Direwolves (both near-inert).

---

## 8. Findings register

Nothing below is resolved here. Each is stated with its evidence and its destination.

| # | Finding | Type | Route to |
| --- | --- | --- | --- |
| F1 | Militia is undefeated at equal gold (8–0), including against both designated AoE counters | Dominant strategy | [#14](https://github.com/marcneuwirth/warweave/issues/14), [#13](https://github.com/marcneuwirth/warweave/issues/13) |
| F2 | Pure Military goes 9–0 across all §29 categories | Dominant strategy | [#14](https://github.com/marcneuwirth/warweave/issues/14) |
| F3 | Pure Magic goes 0–9; Magic with a screen goes 1–7. §29 violated | Dead branch | [#10](https://github.com/marcneuwirth/warweave/issues/10), [#14](https://github.com/marcneuwirth/warweave/issues/14) |
| F4 | The Troll makes a Beast army strictly worse (7–2 → 1–8 for +600g) | Dead unit | [#14](https://github.com/marcneuwirth/warweave/issues/14) |
| F5 | Frostcaller wins 0 of 8 equal-gold matchups; 25 DPS/slot is 40% of the next-worst | Dead unit | [#10](https://github.com/marcneuwirth/warweave/issues/10) |
| F6 | Outriders win 2 of 8, both against casters | Dead unit | [#11](https://github.com/marcneuwirth/warweave/issues/11) |
| F7 | Frostcaller + Longbowmen vs Troll: +90% cost buys 21% faster | Underpowered combo | [#10](https://github.com/marcneuwirth/warweave/issues/10) |
| F8 | Ember Mage loses to Militia at equal gold in both directions — anti-swarm role fails | Role failure | [#14](https://github.com/marcneuwirth/warweave/issues/14) |
| F9 | The squad cap inverts the value ordering discontinuously | Discontinuity | [#13](https://github.com/marcneuwirth/warweave/issues/13) |
| F10 | Overkill waste of 36–43% is invisible in every stat block | Discontinuity / explicability | [#13](https://github.com/marcneuwirth/warweave/issues/13) |
| F11 | Rank 2 never attacks a line — a silent 2× DPS swing on Militia and Direwolves | Discontinuity / explicability | [#13](https://github.com/marcneuwirth/warweave/issues/13), [#12](https://github.com/marcneuwirth/warweave/issues/12) |
| F12 | ~~Stonehide / Bodkin is a hard on-off switch in both directions~~ **Overturned by #11** — single-squad only; Stonehide flips nothing at the cap | Mandatory tech | [#11](https://github.com/marcneuwirth/warweave/issues/11) |
| F13 | Volley Fire and Hooked Spears flip results; ten of eighteen techs are near-inert | Mandatory / dead tech | [#11](https://github.com/marcneuwirth/warweave/issues/11) |
| F14 | Flanking Maneuver never fires — no trigger exists. **#11: deleted** | Dead tech | [#11](https://github.com/marcneuwirth/warweave/issues/11) |
| F15 | ~~Frost Armor measurably worsens the fight it is bought for~~ **Overturned by #11** — positive at six casters; takes pure Magic 0–17 → 2–15 | Dead tech | [#11](https://github.com/marcneuwirth/warweave/issues/11) |
| F16 | Screening fully reverses both fast-attacker matchups — no position-insensitive counter found | Bet confirmed | [#12](https://github.com/marcneuwirth/warweave/issues/12) |
| F17 | #7's predicted convergent 5/3/3 build goes 5–4 and loses to pure Military | Prediction falsified | [#14](https://github.com/marcneuwirth/warweave/issues/14) |

### Repricing levers this ticket deliberately did not pull

The kernel ticket handed over "the local-armour-tuning lever" and the affinity-curve ticket listed
five gold identities that repricing must not break (400 = two gateways = Affinity 2; the 200-gold
affinity band; 550 ≈ 2.2 churn upgrades; 5 × gateway = Affinity 5; the doctrine re-choice fee =
one round's plateau income). None was touched. The obvious candidates — Militia's cost or
HP/model, the Troll's cost or cooldown, Frostcaller's damage — are all
[#14](https://github.com/marcneuwirth/warweave/issues/14)'s to weigh, because F1, F2 and F3 are
symptoms of the same question about whether the core bet survives.
