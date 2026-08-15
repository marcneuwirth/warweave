# `instruments/golden-v1` — the golden oracle set

Resolves [#30](https://github.com/marcneuwirth/warweave/issues/30). Map: [#23](https://github.com/marcneuwirth/warweave/issues/23).

**Twelve scenarios, each with an expected value computed by hand from
[`docs/spec/v0.4.md`](../docs/spec/v0.4.md), with the arithmetic shown.** This is the kernel's
acceptance suite. It is deliberately **not** the paper calculator: §33.9 records that
`matchup-math/` has already measured in the wrong regime once, so it is a *control arm*, never an
oracle ([#27](https://github.com/marcneuwirth/warweave/issues/27)).

**This file outlives `runner/`.** The Go that checks these numbers is throwaway; the numbers and
the readings behind them are not. Every expected value here is also carried machine-readable in
[`golden-v1.json`](golden-v1.json), which is what the Go test actually consumes — the prose here
is the *derivation*, so a disagreement is adjudicable rather than a staring contest.

**Versioning.** `goldenVersion: 1`, against `spec v0.4 (hardened)` and `roster v1`. Every recorded
result names it alongside `roster vN` and `archetypes vN`.

---

## How to read a test

Each test states the **scenario** (precise enough to set up), the **arithmetic**, the **expected
value**, and — where the spec did not decide — the **reading** taken, marked ⚖. Every ⚖ is also
listed in [Findings](#findings), because a reading is a place the redo can diverge.

Conventions carried in from earlier decisions:

- **20Hz, `tick = 0.05s`**, authored durations exact on the grid ([#24](https://github.com/marcneuwirth/warweave/issues/24)).
- **Ten-phase tick, move before attack, damage applied at the end of the attack phase, absolute
  deadline ticks, Burning per *second* and regeneration per *tick*** ([#28](https://github.com/marcneuwirth/warweave/issues/28)).
- **No RNG in the kernel**; comparators end in `ModelID = (side, squadIndex, modelIndex)` ([#25](https://github.com/marcneuwirth/warweave/issues/25)).
- **All distances surface-to-surface** between collision circles (§22.6).
- The pipeline is §22.1, with **one `floor`, at the end**, and `max(1, ·)`.

---

## G-1 — the three-bucket pipeline, end to end

### G-1a · fireball into Militia, flanking live, no armour

One Ember Mage model (95 magic, fireball r = 2.5m, 50% falloff, applies Burning) fires from
**outside** the Militia squad's ±90° frontal arc into an 8-model Militia squad (100 HP, armour 0,
4 wide × 2 ranks, 2.0m spacing) at full strength. Impact point is the target model's centre.

```
1. rawDamage      = 95 × (1 + 0.25)            = 118.75      # flanking, offensive pool
2. hitDamage      = 118.75 × 1.0               = 118.75      # primary: no delivery scalar
                    118.75 × 0.5               =  59.375     # splash: falloff is delivery
3. effectiveArmor = max(0, 0 × (1 − 0.5) − 0)  =   0
   armorMult      = 100 / (100 + 0)            =   1.0
4. finalDamage    = max(1, floor(118.75 × 1.0 × 1.0)) = 118  # primary
                    max(1, floor( 59.375 × 1.0 × 1.0)) =  59  # each splash target
```

Catch: `π × 2.5² / 2.0² = 4.9087 → 4` models, clamped to 8 living. **1 primary at 118, 3 splash at 59.**

| Expected | Value |
| --- | --- |
| Primary damage | **118** |
| Splash damage, per target | **59** |
| Models hit | **4** |
| Kills on impact | **1** (no overkill carry — see G-7) |
| Survivor HP | **41** × 3 |
| Burning, per second | `max(1, floor(10 × 1.0))` = **10**, four events, **40** total |
| Survivor HP after the full burn | **1** × 3 |

The last row is the sharpest cell in the suite: a fireball plus a full burn leaves three Militia
models alive on **exactly 1 HP**. Any error anywhere in the pipeline moves it.

⚖ **Burning is applied to every model the attack damages**, primary and splash alike (§15 says the
fireball "applies Burning" and never names a subset). ⚖ **A Burning event is not an attack**: it
takes no flanking, no arc test and no offensive pool (§11.1 — "flat and source-independent,
sitting outside the applying attack's offensive pool"), but it *is* magic damage and so pays
`bypass = 0.5` and the armour curve.

### G-1b · the same fireball into Spear Guard, armour live, no flanking

Target: 6-model Spear Guard (210 HP, armour 30, 6 × 1, 2.0m spacing).

```
1. rawDamage      = 95                                    = 95
2. hitDamage      = 95 × 1.0 / 95 × 0.5                   = 95 / 47.5
3. effectiveArmor = max(0, 30 × (1 − 0.5) − 0)            = 15
   armorMult      = 100 / 115                             = 0.8695652
4. primary        = floor(95   × 0.8695652)               = floor(82.6087) = 82
   splash         = floor(47.5 × 0.8695652)               = floor(41.3043) = 41
```

| Expected | Value |
| --- | --- |
| Primary / splash | **82** / **41** |
| Models hit | **4** (formula), clamped to 6 living — ⚖ see F-2 |
| Burning, per second | `floor(10 × 0.8695652)` = **8**, **32** over four seconds |
| Kills | **0** |

**Bucket order is exercised**: pooling the falloff instead of keeping it a delivery scalar would
pay the splash targets `95 × 0.5 × 0.8695652` computed off a *pooled* `(1 − 0.5)` — the incoherence
ADR-0001 names — and halving the armour *reduction* instead of the armour would pay 84 / 42.

---

## G-2 — the armour curve, and magic's halving

`armorMult = 100 / (100 + effectiveArmor)`; magic sets `bypass = 0.5`, applied **before**
penetration (§22.2, §22.3, ADR-0004). Every armour value on the v0.4 roster, plus §22.2's
"invested at 65" which no v0.4 unit type carries:

| Armour | Unit types | Physical | Magic (**halve the armour** — the spec's reading) | Rejected reading (halve the *reduction*) | Δ |
| --- | --- | --- | --- | --- | --- |
| 0 | Militia, Hunters, Ember Mage, Stormcaller, Frostcaller, Direwolves | 1.0000000 | 1.0000000 | 1.0000000 | 0.0000000 |
| 10 | Griffin | 0.9090909 | 0.9523810 | 0.9545455 | 0.0021645 |
| 15 | Longbowmen | 0.8695652 | 0.9302326 | 0.9347826 | 0.0045501 |
| 20 | Lifewarden, Stonebacks | 0.8333333 | 0.9090909 | 0.9166667 | 0.0075758 |
| 25 | Troll | 0.8000000 | 0.8888889 | 0.9000000 | 0.0111111 |
| 30 | Spear Guard, Knights | 0.7692308 | 0.8695652 | 0.8846154 | 0.0150502 |
| 40 | Banner Guard | 0.7142857 | 0.8333333 | 0.8571429 | 0.0238095 |
| 65 | *(none in v0.4)* | 0.6060606 | 0.7547170 | 0.8030303 | 0.0483133 |

**The discriminating test.** One Ember Mage attack (95 magic, no modifiers) into one Banner Guard
model: `floor(95 × 0.8333333)` = **79**. The rejected reading gives `floor(95 × 0.8571429)` = **81**.
A kernel that returns 81 has implemented ADR-0004 backwards, and this is the cheapest place in the
suite to catch it.

---

## G-3 — geometric AoE catch

`catch ≈ π r² / sp²` (§22.4, ADR-0029), with **"a 3m area" read as a diameter**. Every cell,
computed:

| Radius | sp 1.6 (Phalanx) | sp 2.0 (default) | sp 2.5 (Knights, Stonebacks, Griffin) | sp 3.0 (Troll) | sp 3.2 (Loose Formation) |
| --- | --- | --- | --- | --- | --- |
| Volley 3 · r 1.50 | 2.7612 → **2** | 1.7671 → **1** | 1.1310 → **1** | 0.7854 → **0** | 0.6903 → **0** |
| Chain Lightning 3 · r 3.20 | 12.5664 → **12** | 8.0425 → **8** | 5.1472 → **5** | 3.5744 → **3** | 3.1416 → **3** |
| Fireball · r 2.50 | 7.6699 → **7** | 4.9087 → **4** | 3.1416 → **3** | 2.1817 → **2** | 1.9175 → **1** |
| Focused Flame · r 1.25 | 1.9175 → **1** | 1.2272 → **1** | 0.7854 → **0** | 0.5454 → **0** | 0.4794 → **0** |
| Firestorm · r 5.00 | 30.6796 → **30** | 19.6350 → **19** | 12.5664 → **12** | 8.7266 → **8** | 7.6699 → **7** |

⚖ **The count includes the primary target**, so splash targets = `catch − 1`. ADR-0029's own
argument reads "an arrow volley would catch **7 of 8** models" at r = 3.0 (`π × 9 / 4 = 7.07`),
which is a count *of the squad*, not of bystanders. §22.4's "single-model squads catch nothing"
then means the same thing under either reading and does not discriminate.

⚖ **Clamp to living models in the target squad**, after the floor.

Against **§22.4's published table for an 8-model squad**, this reproduces every cell except three,
and the three are the table's own inconsistencies (F-1):

- **Chain Lightning at sp 2.0 → 12** in the spec, uncapped, into a squad that has 8 models.
- **Firestorm → 7 across the whole row**, which is the sp = 3.2 value copied across four columns;
  clamped, every cell should read 8.
- The **herd column (labelled "2.5–3.0")** switches between its two values row by row: Volley and
  Fireball match sp 3.0, Chain Lightning matches sp 2.5.

The **P1 test asserts the formula, not the table.**

---

## G-4 — the flanking arc, at 89° and 91°

§23.2: an attack from **outside the target squad's ±90° frontal arc**, measured at the moment of
the hit, per **attacking model**, deals **+25%** into the offensive pool. Post-rotation facing
([#28](https://github.com/marcneuwirth/warweave/issues/28)).

Target squad at the origin facing `f = (0, 1)`. Attacker model at 5m and angle θ off `f`:

| θ | Attacker position | `dot(f, d)` | Flanking? |
| --- | --- | --- | --- |
| 89° | (4.999238, 0.087262) | **+0.087262** | no |
| 90° | (5.000000, 0.000000) | **0.000000** | **no** — ⚖ boundary belongs to the front |
| 91° | (4.999238, −0.087262) | **−0.087262** | **yes** |

⚖ **The test is `dot(f, d) < 0`, strictly, on the *unnormalised* offset** — the sign is
scale-invariant, so no normalisation, no `Atan2`, no trig anywhere, which is exactly the ban
[#25](https://github.com/marcneuwirth/warweave/issues/25) placed on the kernel.

⚖ **`d` runs from the target squad's centre to the attacking model.** Facing is a squad property
(§23.1 — auto-set, never player-set), so the arc it defines is the squad's; a per-target-model
origin would let one attack flank one model of a squad and not the model beside it, an effect the
spec never mentions.

**Damage, both sides of the line.** One Militia model (30 physical) into a Spear Guard model
(armour 30):

```
no flank:  floor(30   × 0.7692308) = floor(23.0769) = 23
flanking:  floor(37.5 × 0.7692308) = floor(28.8462) = 28
```

---

## G-5 — Frozen against a cooldown, and the immunity brake

### G-5a · 0.75s Frozen against a 1.5s cooldown

Frozen = **15 ticks**, immunity = **25 ticks**, a 1.5s cooldown = **30 ticks** — all exact on the
20Hz grid. §11.3: cannot move, **attack timer pauses**.

| Tick | t | Event |
| --- | --- | --- |
| 0 | 0.00s | model acquires and **fires** (⚖ fire-on-acquisition); next-attack deadline = tick 30 |
| 10 | 0.50s | Frozen applied; 20 ticks of cooldown remain |
| 10–24 | 0.50–1.25s | Frozen — 15 ticks, timer suspended |
| 25 | 1.25s | thaws; timer resumes with 20 ticks; Hard-Control Immunity begins |
| 45 | 2.25s | **fires** — the shot is late by exactly 0.75s, not 0.70s or 0.80s |
| 25–49 | 1.25–2.50s | immune; the earliest a second Frozen can land is **tick 50** |

⚖ **The paused timer stores *remaining ticks*, not a shifted deadline.** Equivalent in v0.4
(nothing removes Frozen early), and the two diverge the moment anything does.

⚖ **Frozen pauses the attack timer only.** Other status durations — Burning, Chilled — keep
running underneath it; §11.4 says exactly that of Chilled and gives no reason to treat Burning
differently.

### G-5b · one Frostcaller on one target reproduces §11.6's 20.8%

Frostcaller: 115 magic, **1.8s** cadence (= 36 ticks), applies Chill on every attack, **does not
select a model that is currently Frozen**. Chilled = 3.0s; a second application while active
causes Frozen. Measured from impact (flight handled in G-6):

| t | Event |
| --- | --- |
| 0.00s | Chilled applied, runs to 3.00s |
| 1.80s | second Chilled while active → **Frozen 1.80–2.55s**; immunity 2.55–3.80s |
| 3.60s | target is not Frozen, so it *is* selected; Chill applied; Frozen suppressed by immunity |
| 5.40s | Chilled from 3.60s still active (1.8 < 3.0) → **Frozen 5.40–6.15s** |

**Steady cycle = 3.6s = 72 ticks, of which 15 are Frozen → 15/72 = 20.833%.** §11.6 says
**20.8%**. This is the single best end-to-end check in the suite: it exercises tick quantisation,
two status durations, the immunity brake and a negative targeting clause at once, against a number
the spec printed.

The theoretical ceiling is `0.75 / (0.75 + 1.25)` = **37.5%** (§11.3) — a P1 invariant no
configuration may exceed.

---

## G-6 — Shatter on the tag, deep chill, and the additive pool

§11.5: **Shatter** — a `Heavy` attack into a Frozen target, **+25%**, **does not consume Frozen**.
**Deep chill** — **magic** damage into a Frozen target, +25%, no tag needed. Both sit in the
offensive pool (§22.1). `Heavy` in v0.4: Troll (thrown and melee), Longbowmen, Hooked Spear Guard
(P3). Nothing else, and **no Magic attack carries `Heavy`**.

| # | Attack | Target | Arithmetic | Expected |
| --- | --- | --- | --- | --- |
| G-6a | Troll, 120 physical `Heavy` | Frozen Banner Guard model (armour 40) | `120 × 1.25 = 150`; `floor(150 × 0.7142857)` | **107**, Frozen **still applied** |
| G-6b | Ember Mage, 95 magic | Frozen Spear Guard model (armour 30) | deep chill: `95 × 1.25 = 118.75`; `floor(118.75 × 0.8695652)` | **103** |
| G-6c | Militia, 30 physical, no tag | Frozen Spear Guard model | no bonus — Shatter is tag-gated, not damage-gated (ADR-0002) | **23** |
| G-6d | Longbowmen, 58 physical `Heavy` | Frozen **and** flanked Spear Guard model | `58 × (1 + 0.25 + 0.25) = 87.0`; `floor(87 × 0.7692308)` | **66** |

**G-6d is the pool test.** Multiplying the two +25% sources instead of pooling them gives
`58 × 1.5625 = 90.625 → floor(69.71)` = **69**. A kernel returning 69 has built the offensive
bucket as a chain, which is precisely the divergence ADR-0001 accepted a pool to avoid.

G-6a is the non-consumption test: assert the target is **still Frozen** on the tick after the hit,
and that its remaining Frozen ticks are unchanged.

---

## G-7 — no overkill carry

§22.6: **damage dies with the model.** Two forms, because the waste has two different shapes.

### G-7a · the spec's own example

"A 5-model volley of 78-damage arrows into 100 HP models kills 2, not 3." Resolved sequentially in
`ModelID` order within one attack phase, each attacker taking the lowest-HP model in reach:

| Attack | Target | Result |
| --- | --- | --- |
| 1 | M1 | 100 → 22 |
| 2 | M1 (lowest HP) | dead — **56 wasted** |
| 3 | M2 | 100 → 22 |
| 4 | M2 | dead — **56 wasted** |
| 5 | M3 | 100 → 22 |

**Kills = 2.** Total damage dealt 390; a carrying kernel kills `floor(390/100)` = **3**. ⚖ The
example only reaches 2 under a **culling** preference (§24.2) and sequential resolution — and the
squads that fire arrows (Hunters, Longbowmen) are *not* access-role and do not cull (F-8).

### G-7b · the same rule inside G-1a, geometry-free

G-1a deals `118 + 3 × 59` = **295** into 100 HP models and kills **1**. A carrying kernel kills
**2**. This form needs no targeting assumption at all, which makes it the one to assert in P0.

---

## G-8 — frontage

`frontage = (front rank − 1) × spacing + 2 × collision radius`, surface-to-surface (§13). All
fourteen unit types:

| Unit type | Front × spacing × radius | Computed | Spec prints |
| --- | --- | --- | --- |
| Militia | 4 · 2.0 · 0.4 | **6.8** | 6.8 ✓ |
| Hunters | 5 · 2.0 · 0.4 | **8.8** | 8.8 ✓ |
| Spear Guard | 6 · 2.0 · 0.4 | **10.8** | 10.8 ✓ |
| Knights | 4 · 2.5 · 0.6 | **8.7** | 8.7 ✓ |
| Longbowmen | 5 · 2.0 · 0.4 | **8.8** | 8.8 ✓ |
| Banner Guard | 6 · 2.0 · 0.4 | **10.8** | 10.8 ✓ |
| Ember Mage | 3 · 2.0 · 0.4 | **4.8** | 4.8 ✓ |
| Lifewarden | 6 · 2.0 · 0.4 | **10.8** | 10.8 ✓ |
| Stormcaller | 3 · 2.0 · 0.4 | **4.8** | 4.8 ✓ |
| Frostcaller | 3 · 2.0 · 0.4 | **4.8** | 4.8 ✓ |
| Direwolves | 4 · 2.0 · 0.5 | **7.0** | 7.0 ✓ |
| **Troll** | 2 · 3.0 · 1.2 | **5.4** | **8.4 ✗** |
| Stonebacks | 4 · 2.5 · 0.6 | **8.7** | 8.7 ✓ |
| Griffin | 3 · 2.5 · 0.6 | **6.2** | 6.2 ✓ |

Thirteen of fourteen agree. The Troll cell is the stale three-model figure already recorded by
[#26](https://github.com/marcneuwirth/warweave/issues/26) — **the runner computes 5.4 from the
formula and does not edit the spec.**

### The 10.8m pitch and the 6m seam (§23.6)

```
six Spear Guard, centre-to-centre : 6 × (6 − 1) × 2.0        = 60.0m
six Spear Guard, surface-to-surface: 6 × 10.8               = 64.8m   ✓ §23.6
five Spear Guard                   : 5 × 10.8               = 54.0m
seam                               : 60.0 − 54.0            =  6.0m   ✓ §23.6
```

Both §23.6 figures check. Its *claim about the seam* does not: "too narrow for any line, access or
Common formation (all ≥ 6.8m)" — **Griffin is 6.2m** and is the access capstone (F-10). The
conclusion survives, because 6.2 > 6.0. But with the Troll's frontage corrected to **5.4m**, a
Troll squad passes the seam **intact**, joining the three 4.8m caster squads the spec's own ⚠ note
already admits. **The wall denies even less than the correction said it denied.**

---

## G-9 — projectile flight, quantised

Projectiles advance **before** launch resolution, so flight is never a tick short
([#28](https://github.com/marcneuwirth/warweave/issues/28)); homing, cannot miss, **fizzle** if the
target dies in flight (§22.7). `flightTicks = ceil(range / (speed × 0.05))`.

| Weapon | Range | Speed | m/tick | Flight ticks | Quantised | §22.7 prints |
| --- | --- | --- | --- | --- | --- | --- |
| Arrow — Hunters | 12m | 60 | 3.00 | **4** | 0.20s | 0.20s ✓ |
| Arrow — Longbowmen | 14m | 60 | 3.00 | **5** | 0.25s | 0.23s |
| Frostbolt | 24m | 35 | 1.75 | **14** | 0.70s | 0.69s |
| Storm bolt | 15m | 35 | 1.75 | **9** | 0.45s | 0.43s |
| Fireball | 26m | 30 | 1.50 | **18** | 0.90s | 0.87s |
| Thrown stone | 19m | 25 | 1.25 | **16** | 0.80s | 0.76s |

Every quantised flight is **longer** than the spec's, by at most 0.04s — under one tick, and
always in the same direction, which is the ceiling rule doing what it was chosen to do. §22.7's
"small travel-time correction on the opening exchange only" holds.

---

## G-10 — `controlShare` across a battle with pursuit

§5.5: bank while, **continuously for 3 seconds**, ≥ **400 gold** of squad value sits within **8m**
of the enemy point, exceeding the enemy's value inside that radius. Contribution is
**per-model prorated**: `squad cost × (models within 8m ÷ full model count)`.

Scenario: three Direwolves squads (200g, 8 models each) raid an uncontested enemy point. The
defender's army wipes the attacker's line at **t = 60.0s**; pursuit runs 20s; the battle ends at
**t = 80.0s** (< 90s).

| t | Event | Contribution | Banking |
| --- | --- | --- | --- |
| 30.0s | all three squads, all 24 models, inside 8m | `3 × 200 × 8/8` = **600** | dwell starts |
| 33.0s | 3s dwell complete | 600 | **banking begins** |
| 50.0s | squad A down to 4 models | `200×4/8 + 200 + 200` = **500** | continues |
| 70.0s | squad C wiped, squad B at 3 models | `200×4/8 + 200×3/8 + 0` = **175** | **stops** |

```
bankedSeconds = 70.0 − 33.0                       = 37.0s   (740 ticks)
duration      = 80.0s  — wipe + 20s pursuit       = 80.0s   (1600 ticks)
controlShare  = 37.0 / 80.0                       = 0.4625
objectiveDamage at round 5 (S = 15) = 0.3 × 15 × 0.4625 = 2.08125
```

⚖ **A lapse costs a fresh 3s dwell** — §5.5 says banking "stops the instant the condition lapses"
and never describes resumption, and a free resume would make the dwell purchasable once per battle.

⚖ **The 8m radius is measured centre-of-model to the point.** §22.6's surface-to-surface rule is
about collision circles; the point explicitly has none ("no collision … a scoring volume only").

⚖ **"Exceeding" is strict** — a tie inside the radius banks for neither player.

⚖ **Banked time accumulates in ticks**; `controlShare` is a ratio of tick counts, so it never
depends on when a sample was taken.

---

## G-11 — `winnerIntegrity` and battle damage

§5.2, included because P2 cannot score a round without it and it costs one line to check.

Winner deployed three squads — Militia 100g, Spear Guard 200g, Ember Mage 200g, **500g deployed**:

| Squad | Start HP | Current HP | `squadRemainingHPPercent` |
| --- | --- | --- | --- |
| Militia | 8 × 100 = 800 | 300 | 0.3750000 |
| Spear Guard | 6 × 210 = 1260 | 1260 | 1.0000000 |
| Ember Mage | 3 × 150 = 450 | 150 | 0.3333333 |

```
Σ(cost × pct) = 100 × 0.375 + 200 × 1.0 + 200 × 0.3333333 = 304.16667
winnerIntegrity = 304.16667 / 500                          = 0.6083333
battleDamage(round 5, S = 15) = 0.7 × 15 × (0.75 + 0.25 × 0.6083333)
                              = 10.5 × 0.9020833          = 9.471875
```

A draw at the same round pays `0.35 × 15` = **5.25** to both.

⚖ **Command is `float64` and is never rounded.** The spec's own match-length table (§5.3) only
lands inside 8–12 rounds with fractional damage, and rounding to integers at 20Hz would compound.

---

## G-12 — `reach ≥ spacing`, and what a second rank fields

§23.5 claims a **silent 2× DPS swing**: Militia and Direwolves field "4 of 8 models against a line
and 8 of 8 against a single model". Under a **rigid** formation, the first half checks and the
second does not:

```
Militia rank-1 model in contact with an enemy model (both r = 0.4):
  centre-to-centre = 0.4 + 0.4 = 0.8m,  surface = 0.0m
Militia rank-2 model sits one spacing interval back:
  centre-to-centre = 0.8 + 2.0 = 2.8m,  surface = 2.8 − 0.8 = 2.0m
  reach 1.0m  <  2.0m   →  rank 2 cannot attack.  4 of 8  ✓
```

Against a **single Large model** (Troll, r = 1.2), rigid formation gives the *same* answer:

```
rank-1 in contact: centre-to-centre = 1.2 + 0.4 = 1.6m
rank-2:            centre-to-centre = 3.6m,  surface = 3.6 − 1.6 = 2.0m
  reach 1.0m  <  2.0m   →  still 4 of 8, not 8 of 8
```

**"8 of 8 against a single model" is only reachable if models leave formation and envelop** — and
the spec never says whether a squad holds its formation in contact (F-11). The kernel cannot
compute `attackingModels` — §22.6 calls it "a first-class derived quantity" — without an answer,
so this test is **authored but not yet gradeable**, and the question is now
[#45](https://github.com/marcneuwirth/warweave/issues/45).

The Spear Guard half of §23.5 does not survive either: it is a **6 × 1** squad and has no rank 2,
so "fields all six" is a property of its formation, not of `reach ≥ spacing`. Its 2.2m reach is
still doing real work — it strikes 1.2m before Militia or Direwolves can answer — but that is the
*reach* argument, not the rank argument.

---

## Findings

Each is a place the spec did not decide, or decided something its own arithmetic contradicts.
**None is fixed here** — the runner grades v0.4 as written (map scope). They are inputs to
[#38](https://github.com/marcneuwirth/warweave/issues/38)'s report.

| # | Finding | Where | Consequence |
| --- | --- | --- | --- |
| F-1 | §22.4's published table is internally inconsistent: Chain Lightning is uncapped at 12 into an 8-model squad, Firestorm's row is the sp 3.2 value copied across all four columns, and the "2.5–3.0" column silently switches between 2.5 and 3.0 row by row | §22.4 | the P1 test asserts **the formula**, not the table |
| F-2 | The lattice formula over-counts every **single-rank** squad, and 10 of 14 unit types are `n × 1`. A fireball on a 6 × 1 line at 2.0m spacing catches 3 by geometry (`1 + 2⌊r/sp⌋`) and 4 by formula | §22.4 | **grading Magic's anti-swarm on a geometrically impossible count** — ticketed as [#45](https://github.com/marcneuwirth/warweave/issues/45) |
| F-3 | Whether the catch **includes the primary target** is never stated; ADR-0029's "7 of 8" implies it does | §22.4 | ⚖ ruled included; splash targets = `catch − 1` |
| F-4 | Whom an AoE applies its status to is unstated | §15, §11.1 | ⚖ ruled: every model the attack damages |
| F-5 | The flanking arc's **target-side origin** and its **boundary at exactly 90°** are both unstated | §23.2 | ⚖ ruled: squad centre; `dot < 0` strictly |
| F-6 | Whether a model **fires on acquisition** or pays a cooldown first is unstated | §22.6 | ⚖ ruled fire-first — §22.7's "opening exchange" correction presumes a t = 0 shot |
| F-7 | "Cooldowns stagger on acquisition" delivers **zero stagger** when a whole squad acquires on one tick — the common case, since both armies close together | §22.6 | the anti-lumping claim is only partly delivered; ranged squads still volley in lockstep |
| F-8 | §22.6's 5 × 78 example needs **culling** and sequential resolution to reach "kills 2", and neither arrow squad culls. For projectiles the waste is **fizzle**-waste, not overkill-waste: five arrows launched on one tick at one model kill it once and fizzle four times | §22.6, §22.7, §24.2 | overkill waste is *understated* for ranged squads |
| F-9 | §16 prints the Troll's frontage as 8.4m; the formula gives **5.4m** | §16 | already recorded by [#26](https://github.com/marcneuwirth/warweave/issues/26); restated because F-10 depends on it |
| F-10 | §23.6's "all ≥ 6.8m" is false — **Griffin is 6.2m** — and with F-9's correction the **Troll (5.4m) passes the 6m seam intact**, a second unit type the ⚠ note does not list | §23.6 | the wall denies even less than the correction said; strengthens ADR-0036 rather than weakening it |
| F-11 | The spec never says whether a squad **holds formation in contact**, and §23.5's headline 2× DPS claim is unreachable if it does | §23.5, §22.6 | blocks `attackingModels`; ticketed as [#45](https://github.com/marcneuwirth/warweave/issues/45) |
| F-12 | Whether Command is integral is unstated | §5 | ⚖ ruled `float64`, never rounded |
| F-13 | Control-point **dwell resumption** after a lapse, and whether 8m is surface- or centre-measured, are both unstated | §5.5 | ⚖ ruled: fresh 3s dwell; centre-to-point |
| F-14 | ADR-0004's "the two readings sit within a point across most of the roster" holds to armour 25; at 30 the gap is **1.5pp** and at 40 it is **2.4pp** — about 2 damage on a 95 hit | ADR-0004 | accurate in direction, optimistic in magnitude at the top of the range |
| F-15 | §22.7's flight times are 0.01–0.04s shorter than 20Hz can express | §22.7, [#24](https://github.com/marcneuwirth/warweave/issues/24) | under one tick, always in the same direction — recorded, not repaired |

---

## What P0 and P1 must assert

| Phase | Tests |
| --- | --- |
| **P0** — kernel | G-1a, G-1b, G-2, G-4, G-6, G-7b, G-8, G-9 |
| **P1** — sandbox | G-3, G-5a, G-5b, G-7a, G-12 *(pending [#45](https://github.com/marcneuwirth/warweave/issues/45))* |
| **P2** — match | G-10, G-11 |

Two of these are **invariants** rather than point checks, and should run on every recorded pass,
not only in the test binary: Frozen uptime on any one model never exceeds **37.5%** (§11.3), and
`maxSpeedSum × tickSeconds < minMeleeReach` holds at load ([#28](https://github.com/marcneuwirth/warweave/issues/28)).
