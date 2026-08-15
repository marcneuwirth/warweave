> # ⚠ SUPERSEDED
>
> **This document is no longer the source of truth.** It is the pre-hardening draft, retained unchanged because the ADRs cite its section numbers and rulings.
>
> The current specification is **[`docs/spec/v0.4.md`](docs/spec/v0.4.md)**. Vocabulary is in [`CONTEXT.md`](CONTEXT.md); the decisions that changed this document into that one are in [`docs/adr/`](docs/adr/).
>
> Much of what follows was found to be wrong during hardening — the Command formula cannot produce its own target match length, two signature abilities could never fire, the elemental loop could not be cashed by its own branch, and the roster produced a total-ordered archetype field. Read it as history, never as rules.

---

I’d make v0.4 a **narrower, fun-complete prototype** rather than expanding the current implementation scope. It keeps the shared roster, affinity identity, positioning emphasis, and deterministic simulation from v0.3, but moves the full match loop and hybridization ahead of the 18-unit/72-tech expansion.  

# WARWEAVE — Prototype Design Specification v0.4

**Purpose:** Prove the core strategic game before expanding the roster.

v0.4 narrows the first playable from 18 units and 72 technologies to **9 units and 18 technologies**, while moving the economy, affinity system, hybridization, and complete match loop earlier in development.

The prototype should answer one question:

> Does building a warhost through Military, Magic, and Beast specialization create interesting decisions about commitment, counterplay, positioning, and hybridization?

If the answer is yes, the remaining nine units become expansion of a proven game rather than prerequisites for discovering whether the game works.

---

# 1. Core Game

WARWEAVE is a competitive 1v1 fantasy army auto-battler.

Players build persistent armies over multiple rounds. Before each battle they purchase units and technologies, position their squads, and deepen one or more of three affinities:

**Military — Coordinate**
Formation, screening, range control, armor, combined arms, and positional discipline.

**Magic — Combine**
Elemental states, battlefield control, AoE, and interactions between effects.

**Beast — Overwhelm**
Mobility, predation, regeneration, target access, and physical disruption.

There are no factions. Every player begins with access to the same roster.

Build identity emerges from investment.

---

# 2. v0.4 Prototype Scope

| Area                 | v0.4 Target                              |
| -------------------- | ---------------------------------------- |
| Players              | 1v1                                      |
| Base roster          | 9 units                                  |
| Common units         | 3                                        |
| Military units       | 2                                        |
| Magic units          | 2                                        |
| Beast units          | 2                                        |
| Technologies         | 2 per unit, 18 total                     |
| Equipped techs       | Maximum 1 per unit type                  |
| Hybrid systems       | 3                                        |
| Deep specialization  | 1 doctrine per branch                    |
| Squad cap            | 12 deployed squads per player            |
| Maps                 | 1 symmetric open battlefield             |
| Terrain              | None                                     |
| Match length         | Target 8–12 rounds                       |
| Battle duration      | Target 25–60 seconds                     |
| Simulation           | Deterministic fixed-tick Simulation.Core |
| Multiplayer          | Local first                              |
| Metagame progression | None                                     |

The prototype intentionally excludes:

* Flying
* Siege
* Healing
* Healing Exhaustion
* Discipline/Terror
* Wet/Shocked/Conduct/Steam
* Apex units
* Terrain
* Selling
* Hybrid transformation technologies

These systems remain candidates for the 18-unit alpha.

---

# 3. Match Structure

## 3.1 Round loop

Each round:

1. Players receive income.
2. Players inspect the opponent's **previous locked army**.
3. Players privately purchase units and technologies.
4. Players privately reposition their army.
5. Players lock their plans.
6. Both new configurations are revealed simultaneously.
7. Combat resolves automatically.
8. The losing player takes Command damage.
9. Persistent purchased armies return for the next planning phase.

This prevents last-second counter-positioning against live opponent movement.

Players are predicting the opponent rather than racing the planning timer.

---

# 4. Economy

## Starting resources

**Starting gold: 400**

Round 1 begins with this amount. No additional round-one income is awarded.

## Income

Before rounds 2+:

`income = min(300 + 50 × (round - 2), 550)`

Therefore:

| Round |            Income |
| ----- | ----------------: |
| 1     | Starting 400 only |
| 2     |               300 |
| 3     |               350 |
| 4     |               400 |
| 5     |               450 |
| 6     |               500 |
| 7+    |               550 |

Unused gold carries forward.

## Selling

**No selling in v0.4.**

Selling is deliberately deferred because it interacts directly with affinity investment and creates progression exploits if affinity survives a sale.

The larger army cap gives players enough room to make tactical corrections without requiring liquidation.

## Squad cap

Each player may own/deploy a maximum of **12 squads**.

Technologies do not consume squad slots.

This creates a second strategic resource beyond gold and prevents unlimited cheap-body spam.

---

# 5. Command & Victory

Each player begins with:

**100 Command**

A player loses at 0 Command.

After a round loss:

`roundDamage = clamp(6 + floor(survivingEnemyUnitValue / 200), 6, 16)`

Only surviving squad purchase value counts. Technology cost does not.

This preserves the idea that decisive victories matter while reducing extreme snowball finishes.

## Battle timeout

Maximum battle duration:

**90 simulated seconds**

At timeout, calculate:

`remainingValue = Σ(unitCost × squadRemainingHPPercent)`

The player with greater remaining value wins the round.

If remaining values differ by less than 5%, the round is a draw and both players lose **4 Command**.

This guarantees that defensive stalemates still advance the match.

---

# 6. Affinity

Affinity is no longer generated from arbitrary purchase-price bands.

Instead, each branch tracks **gold committed to that branch**.

`Affinity = floor(branchInvestment / 200)`

Prototype affinity is capped at **5**.

Branch investment includes:

* Branch units
* Technologies belonging to branch units

Common units and Common technologies generate no affinity.

Because selling does not exist in v0.4, branch investment cannot be cycled or manipulated.

---

# 7. Affinity Unlocks

Each branch has one gateway unit available immediately.

| Affinity | Military       | Magic            | Beast         |
| -------- | -------------- | ---------------- | ------------- |
| 0        | Spear Guard    | Ember Mage       | Direwolves    |
| 2        | Longbowmen     | Frostcaller      | Troll         |
| 3+3      | Hybrid unlock  | Hybrid unlock    | Hybrid unlock |
| 5        | Grand Strategy | Arcane Resonance | Apex Instinct |

This removes the affinity-0 progression deadlock and makes the first branch choice immediate.

A player can therefore start a match with any mixture of:

* Common units
* Spear Guard
* Ember Mage
* Direwolves

Their purchases then determine future options.

---

# 8. Deep vs. Wide Strategy

The affinity system should generate a meaningful tension:

**Deep build**

Reach Affinity 5 quickly and receive a branch doctrine.

Advantages:

* Earlier specialization payoff
* More concentrated synergy
* Stronger execution of one strategic identity

Disadvantages:

* Narrower counter coverage
* Delayed access to hybrid effects

**Hybrid build**

Reach 3 affinity in two branches.

Advantages:

* Cross-branch interactions
* Better counter coverage
* New composition possibilities

Disadvantages:

* Delays Affinity 5 doctrine
* Splits gold between branches

Neither approach should be inherently stronger.

---

# 9. Deep Doctrines

## Military 5 — Grand Strategy

Military squads within 6m of another Military squad gain:

**+10 Armor**

The bonus encourages coherent formations without making Military generically stronger in every situation.

Breaking the formation removes the benefit.

## Magic 5 — Arcane Resonance

The first elemental status applied to each enemy lasts:

**+25% duration**

This strengthens elemental setup without directly multiplying spell damage.

## Beast 5 — Apex Instinct

All Beast units gain Predation behavior.

When moving toward a wounded or isolated target:

**+10% movement speed**

A target is wounded below 50% HP.

A target is isolated when no allied model is within 3.5m.

---

# 10. Hybrid Unlocks

Hybrid effects activate automatically when both required affinities reach 3.

They do not require an additional purchase.

## Military 3 + Magic 3 — Enchanted Arms

Military attacks deal:

**+15% damage against Burning, Chilled, or Frozen enemies.**

This makes Magic setup valuable to physical formations without turning all Military attacks into elemental attacks.

---

## Military 3 + Beast 3 — Beastmastery

Beast units deal:

**+15% damage against enemies currently engaged in melee by a Military squad.**

Military creates the battle line.

Beasts exploit it.

---

## Magic 3 + Beast 3 — Primal Magic

A Beast attack against a Burning or Chilled enemy refreshes that status by **0.5 seconds**.

Maximum once per second per target.

Beast attacks cannot create Frozen directly.

This allows Beasts to extend magical setup without producing uncontrolled CC chains.

---

# 11. Elemental System

v0.4 uses only three elemental states.

## Burning

Duration: **4 seconds**

Effects:

* Periodic magic damage
* Regeneration reduced by 75%

Repeated application refreshes duration.

Burning does not stack damage.

## Chilled

Duration:

**3 seconds**

Effect:

**-20% movement speed**

Repeated application within the active duration can trigger Frozen.

## Frozen

Applying a second Chill while Chilled causes Frozen.

Duration:

**0.75 seconds**

Effects:

* Cannot move
* Attack timer pauses

After Frozen ends, the target receives:

**1.25 seconds Hard-Control Immunity**

Large units receive only 50% of the normal Frozen duration.

## Shatter

A physical attack with at least **70 raw damage** against a Frozen target:

* Removes Frozen
* Deals +40% damage

This creates natural interaction between Magic control and heavy physical attacks.

---

# 12. Universal Hard-Control Rule

Root, Stun, and Frozen are tagged **HardControl**.

After HardControl ends:

**Hard-Control Immunity: 1.25 seconds**

Large targets receive 50% HardControl duration.

Huge targets, when introduced later, can receive an even larger resistance.

This replaces bespoke CC immunity rules on individual abilities.

---

# 13. Prototype Roster

## Common

### Militia

Cost: **100**
Models: **8**
HP/model: **100**
Armor: **0**
Attack: **30 physical**
Cooldown: **1.0s**
Range: **Melee**

Role:

Cheap bodies, screening, model-count advantage.

### Hunters

Cost: **150**
Models: **5**
HP/model: **120**
Armor: **5**
Attack: **42 physical**
Cooldown: **1.6s**
Range: **16m**

Role:

Flexible ranged damage.

### Outriders

Cost: **200**
Models: **3**
HP/model: **260**
Armor: **20**
Attack: **55 physical**
Cooldown: **2.0s**
Opening range: **9m**

Role:

Mobile harassment and flank pressure.

Outriders begin with ranged javelins and switch to melee inside 3m.

---

# 14. Military

## Spear Guard

Cost: **200**
Models: **6**
HP/model: **210**
Armor: **30**
Attack: **48 physical**
Cooldown: **1.5s**
Range: **2.2m**

Role:

Defensive frontline and anti-large formation.

### Brace

After remaining stationary for 1 second, Spear Guard becomes Braced.

Against a frontal charging Large unit:

* Incoming charge damage -50%
* Spear Guard's first contact attack gains +50% damage
* The target's charge state ends

Brace ends when the squad moves.

## Longbowmen

Affinity requirement:

**Military 2**

Cost: **250**
Models: **5**
HP/model: **135**
Armor: **5**
Attack: **78 physical**
Cooldown: **2.4s**
Range: **25m**

Role:

Long-range focus fire and armor counter.

---

# 15. Magic

## Ember Mage

Cost: **200**
Models: **1**
HP: **360**
Armor: **0**
Attack: **95 magic**
Cooldown: **2.25s**
Range: **17m**

Base fireball:

* 2.5m splash
* Applies Burning

Role:

Anti-swarm and regeneration counter.

## Frostcaller

Affinity requirement:

**Magic 2**

Cost: **225**
Models: **1**
HP: **390**
Armor: **0**
Attack: **45 magic**
Cooldown: **1.8s**
Range: **18m**

Every attack applies Chill.

Role:

Movement control and setup for physical damage.

---

# 16. Beast

## Direwolves

Cost: **200**
Models: **8**
HP/model: **125**
Armor: **0**
Attack: **34 physical**
Cooldown: **0.9s**
Range: **Melee**

Predation enabled.

Direwolves prefer exposed ranged and caster targets when the path is reasonably accessible.

Role:

Backline hunting and high-speed disruption.

## Troll

Affinity requirement:

**Beast 2**

Cost: **300**
Models: **1**
HP: **1,250**
Armor: **25**
Attack: **105 physical**
Cooldown: **2.0s**
Range: **2.4m**

Role:

Regenerating frontline bruiser.

### Regeneration

While recently damaged:

**25 HP/second**

After 2 seconds without taking damage:

**60 HP/second**

Burning suppresses regeneration by 75%.

All designer-facing regeneration values are authored per second. Simulation.Core converts them to deterministic per-tick values.

---

# 17. Technology System

Each unit type has exactly:

**2 available technologies**

A player may purchase:

**Maximum 1 technology per unit type**

Technology is global for every squad of that unit type.

This produces one meaningful specialization decision per unit without creating the 72-tech balance explosion yet.

Common technology cost:

**200 gold**

Branch unit technology cost:

**250 gold**

Technologies cannot be refunded.

---

# 18. Common Technologies

## Militia

### Conscription

+3 models.

Each model:

-15% HP
-10% attack damage

Purpose:

Increase screening and body count without providing a nearly free 50% DPS increase.

### Pitch & Torch

+30% damage against Beast units.

Attacks against Large Beast units apply Burning for 2 seconds.

---

## Hunters

### Loose Formation

Formation spacing +60%.

AoE damage received -20%.

The larger formation footprint makes the squad easier to flank.

### Rapid Fire

Attack cooldown -25%.

Raw damage -15%.

Creates sustained pressure at the cost of per-hit effectiveness.

---

## Outriders

### Javelin Volley

Opening javelin:

+60% damage
+5m range

One empowered javelin per model.

### Flanking Maneuver

+30% damage when attacking a target facing more than 90° away from the attacker.

---

# 19. Military Technologies

## Spear Guard

### Phalanx

Frontal physical damage received -20%.

Formation spacing -20%.

Turn speed -20%.

### Hooked Spears

+45% damage against Large targets.

-10% damage against Small targets.

---

## Longbowmen

### Bodkin Arrows

Armor penetration +60.

Raw damage -10%.

### Volley Fire

Attacks target a 3m area.

Nearby models receive splash damage with 50% falloff.

Attack cooldown +20%.

---

# 20. Magic Technologies

## Ember Mage

### Firestorm

Every fourth cast targets a 5m area.

Models hit receive 70% of normal fireball damage.

### Focused Flame

Splash radius -50%.

Damage against Large targets +80%.

This converts Ember Mage from swarm control into monster killing.

---

## Frostcaller

### Deep Freeze

Frozen duration +0.5 seconds.

Hard-Control Immunity after Frozen increases to 1.75 seconds.

This creates a stronger but less chainable control window.

### Frost Armor

Every 4 seconds, shield the nearest allied unit for:

**120 damage**

Shield duration:

**4 seconds**

Prefer Large allies.

---

# 21. Beast Technologies

## Direwolves

### Pack Hunter

Each additional wolf attacking the same target gives:

**+8% damage**

Maximum bonus:

**+32%**

### Pounce

On first engagement:

Leap up to 4m through unit collision.

First hit:

**+25% damage**

---

## Troll

### Stonehide

+45 Armor.

Movement speed -10%.

### Boulder Throw

If the current target is more than 5m away, throw a projectile:

Damage: **90 physical**
Range: **13m**
Cooldown: **4 seconds**

Troll remains primarily a melee unit.

---

# 22. Armor

Physical damage uses:

`effectiveArmor = max(0, armor - armorPenetration)`

`damageMultiplier = 100 / (100 + effectiveArmor)`

`finalDamage = max(1, floor(rawDamage × damageMultiplier))`

Magic damage does **not** completely bypass armor.

Default rule:

**Magic ignores 50% of physical armor.**

Specific future spells or technologies may receive full armor bypass.

This preserves Magic as relatively effective against armored formations without making the entire Magic branch a universal Military counter.

---

# 23. Positioning

The prototype battlefield remains:

**60m × 80m**

Each player deploys inside the nearest 24m.

There is no terrain.

Strategic positioning comes from:

* Screening
* Formation width
* Facing
* Ranged access
* Flanking
* Formation spacing
* Backline protection
* Unit collision
* Target access

Terrain should only be added if these systems fail to provide sufficient spatial depth.

---

# 24. Targeting

Default targeting remains deterministic and distance-based with target stickiness.

Units should not continuously choose tactically perfect targets.

The player should primarily influence targeting through positioning.

Special targeting behavior should be limited to:

**Direwolves:** backline preference
**Hooked Spear Guard:** Large-target preference
**Longbowmen with Bodkin:** armored-target preference

Technologies should rarely rewrite AI behavior.

---

# 25. Effect Primitives

Prototype technologies and abilities should be constructed from a limited reusable set.

Supported primitives:

* DamageModifier
* ArmorModifier
* ArmorPenetration
* AttackRateModifier
* MoveSpeedModifier
* RangeModifier
* TargetTagBonus
* ApplyStatus
* RemoveStatus
* Shield
* Aura
* AreaZone
* Knockback
* Root
* Stun
* Freeze
* TargetPriorityModifier
* EveryNthAttack
* HealthThresholdTrigger
* OnDeath
* OnEngage
* CooldownAbility

Any technology requiring a new simulation subsystem should be challenged before implementation.

The default answer should be:

**Can this behavior be expressed through existing primitives instead?**

---

# 26. Systems Explicitly Deferred

The following concepts remain part of the broader WARWEAVE design but should not block the first fun-complete prototype:

### Banner Guard

Tests leadership, Discipline, and formation auras later.

### Knights

Tests charge/trample interactions after Spear Brace is proven.

### Stormcaller

Introduces Shocked and chain interactions after the basic elemental system is readable.

### Lifewarden

Introduces healing and Exhaustion after baseline time-to-kill is stable.

### Trebuchet

Introduces siege and minimum-range artillery.

### Griffin

Introduces flying and Grounded windows.

### Hydra

Introduces Huge multi-target monsters.

### Archmage

Introduces battlefield-scale spells.

### Dragon

Tests the apex unit fantasy only after anti-apex counterplay is established.

---

# 27. Balance Targets

Equal-gold neutral matchup:

**40–60%**

Soft counter:

**60–70%**

Hard counter:

**70–80%**

Hard counter with poor positioning:

Should be capable of falling below **60%**

No single technology should be chosen more than approximately:

**70% of the time**

unless intentionally functioning as part of the unit's baseline identity.

At least **7 of 9 units** should appear competitively useful before roster expansion begins.

---

# 28. Required Canonical Matchups

The automated suite should include at minimum:

Militia vs Direwolves
Militia vs Ember Mage
Hunters vs Direwolves
Spear Guard vs Direwolves
Spear Guard vs Troll
Longbowmen vs Troll
Ember Mage vs Militia
Ember Mage vs Troll
Frostcaller + Longbowmen vs Troll
Outriders vs protected ranged line
Direwolves vs protected ranged line

Each test should run across multiple formations.

The goal is not to create 50/50 matchups.

The goal is to detect:

* Dominant strategies
* Dead units
* Mandatory technologies
* Position-insensitive counters
* Excessive snowball effects
* Unexpected interaction discontinuities

---

# 29. Full-Build Tests

The balance runner must additionally compare equal-total-spend armies representing:

* Common-heavy
* Pure Military
* Pure Magic
* Pure Beast
* Military/Magic
* Military/Beast
* Magic/Beast

At least one representative build from every category should be capable of winning competitive matches.

A hybrid build should not automatically beat a pure build merely because it has access to more systems.

---

# 30. Prototype Development Order

## P0 — Deterministic Combat Kernel

Implement only:

Militia
Direwolves

Required systems:

* Fixed tick
* Movement
* Collision
* Target acquisition
* Attacks
* Death
* Squad membership
* Deterministic ordering
* State hashing

100 repeated identical simulations must produce identical results.

---

## P1 — Nine-Unit Combat Sandbox

Add:

Hunters
Outriders
Spear Guard
Longbowmen
Ember Mage
Frostcaller
Troll

Implement:

* Armor
* Projectiles
* AoE
* Size
* Brace
* Burning
* Chill/Freeze
* Shatter
* Predation
* Regeneration
* Shields
* Basic formations

Do **not** add the shop yet.

The nine units should already produce understandable counter relationships.

---

## P2 — Complete Match

Add:

* Gold
* Income
* Persistent army
* 12-squad cap
* Private planning
* Simultaneous reveal
* Affinity
* Unlocks
* Command
* Victory condition
* Timeout resolution

At this milestone, WARWEAVE becomes a game rather than a combat sandbox.

---

## P3 — Technologies & The Weave

Add:

* 18 technologies
* One-tech-per-unit rule
* Three hybrid unlocks
* Three deep doctrines
* Opponent inspection
* Affinity UI
* Tech UI
* Range/facing/formation previews

This milestone should test the game's primary differentiator.

---

## P4 — External Prototype Playtest

Do not implement the remaining nine units first.

Run external playtests.

Collect:

* Unit purchase rate
* Technology choice rate
* Affinity progression
* Pure vs hybrid win rate
* Average match length
* Round damage distribution
* Composition diversity
* Position changes between rounds
* Counter-purchase frequency
* Battle timeout rate

Also collect qualitative feedback:

* Could players predict why battles resolved the way they did?
* Did repositioning feel meaningful?
* Were opponent counters readable?
* Did affinity create interesting commitment?
* Did hybrid unlocks feel exciting?
* Did players feel able to recover from an early disadvantage?
* Did players want to try a different build next match?

---

# 31. Expansion Gate

Do not proceed to the 18-unit alpha until the prototype demonstrates all of the following:

A complete match is enjoyable without apex units.

Military, Magic, and Beast each have viable pure builds.

All three two-branch hybrid strategies have demonstrated viable builds.

At least 7 of 9 units have competitive uses.

No technology is effectively mandatory.

At least three near-even matchups can be flipped through positioning alone.

Players can explain why they won or lost most battles.

Average matches fall reasonably close to the 8–12 round target.

Timeouts are uncommon.

The deterministic simulation remains reproducible.

The game creates repeated moments where a player must choose between:

**Counter now, deepen my current strategy, or begin weaving into another branch.**

That decision is the central strategic product test for WARWEAVE.

---

# 32. Path From v0.4 to the 18-Unit Alpha

Once v0.4 succeeds, add units in pairs based on the system they validate.

**Banner Guard + Knights**
Complete Military identity through leadership and charge mechanics.

**Stormcaller + Lifewarden**
Expand Magic into chain effects and support.

**Griffin + Hydra**
Expand Beast into flight and Huge monsters.

Then add the apex layer:

**Trebuchet**
Military battlefield-scale threat.

**Archmage**
Magic battlefield-scale threat.

**Dragon**
Beast battlefield-scale threat.

Only after those systems work should the technology pool expand from:

**2 choices / 1 active**

to:

**4 choices / 2 active**

This makes the 72-technology version the result of validated strategic depth rather than the prerequisite for finding it.

