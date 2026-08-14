# WARWEAVE

A competitive 1v1 fantasy army auto-battler. Players build persistent armies across 8–12 rounds, deepening one or more of three branches — Military, Magic, Beast — and win by reducing the opponent's Command to 0.

This is the project's glossary and nothing else. Design detail lives in the spec; recorded decisions live in `docs/adr/`.

## Language

**The word `unit` is banned.** It has meant a roster entry, a single body, and a purchased group in different sections of the same document. Use **Unit type**, **Model**, or **Squad**.

### Army and roster

**Model**:
One individual body on the battlefield. Carries HP, armour, size, collision radius, position and its own attack cooldown, and is the atomic thing that dies. Facing is *not* a model property — it is squad-level.
_Avoid_: unit, entity, creature

**Squad**:
One purchased group of models, positioned and targeted as a single object of command. What the squad cap counts.
_Avoid_: unit, stack, group

**Unit type**:
A roster entry such as Militia or Troll — what a stat block describes and what a technology attaches to. Always written in full, never shortened.
_Avoid_: unit, class, troop

**Army**:
A player's complete set of owned squads, persistent across rounds.
_Avoid_: warhost (flavour copy only, never rules text), warband, force

**Squad cost**:
The gold purchase price of one squad of a unit type. Excludes technology cost.
_Avoid_: unitCost, unit value

**Squad cap**:
The maximum number of squads a player may own — 12. Technologies do not consume slots.

**Common**:
The fourth value of the **branch** property — Militia, Hunters and Outriders, available to every player from round 1. It is a branch value but not a specialization track: no gateway, no doctrine, no affinity, and it accumulates no branch investment. It matches no rule that names Military, Magic or Beast, so Common unit types receive no doctrine and no hybrid unlock. They are not excluded from the *systems* those effects read — Pitch & Torch lets Militia apply Burning — only from the rewards.

### Branch and progression

**Branch**:
A single-valued property of a **unit type**, total across the roster, with exactly four values: Military (*Coordinate*), Magic (*Combine*), Beast (*Overwhelm*) and **Common**. The first three are specialization tracks — each owns a unit-type pool, its technologies, gateway unit types at affinity 0 and 2, and a doctrine at 5. Common is a branch value that is not a track.
_Avoid_: faction, tree, affinity (when naming the branch itself); "the three branches" when the property is meant (there are three *tracks* and four *values*)

**Branch denotation**:
The rule governing what a branch name means in rules text. **Wherever a rule names a branch, it denotes the `branch` property of the unit type of the model in question — attacker, ally or target alike.** Common unit types match none of the three tracks. A branch name never denotes damage type, and damage type never implies a branch: "Military attacks" means attacks by Military-branch unit types, not physical attacks. The rule is global — it governs doctrines, hybrid unlocks, technologies, and both attacker-side and target-side predicates.

**Affinity**:
The integer level from 0 to 5 that a player holds **in a branch**, derived as `floor(branchInvestment / 200)`. Never standalone — always branch-then-level, as in "Military 3".
_Avoid_: affinity points, "the three affinities" (there are three *branches*)

**Branch investment**:
Cumulative gold committed to a branch: squads of its unit types, plus technologies belonging to those unit types. It only ever accumulates, and continues past the affinity 5 cap. **Stamped at purchase** — gold is credited to the branch the unit type held at the moment it was spent, and nothing later moves it. Investment is an accounting fact about a transaction, never a live re-read of the branch property.
_Avoid_: affinity investment (affinity is derived, never purchased)

**Counts-as membership** *(forward invariant — no member in v0.4)*:
A set-valued membership letting a unit type match a branch it does not belong to, for **rules reads only**. It adds a membership rather than overwriting `branch`, is evaluated live at the moment a rule reads it, and **never touches branch investment**. This is the only sanctioned shape for an effect such as "Common units count as Military": as a branch swap it would relocate past spending and become an affinity pump.

**Technology**:
A purchased permanent upgrade attached to a unit type, applying to every squad of that type. At most one per unit type, and never refunded.
_Avoid_: upgrade, perk, research

**Doctrine**:
The automatic permanent effect a branch grants at affinity 5. Exactly three exist. Never purchased and never chosen.
_Avoid_: ultimate, capstone

**Hybrid unlock**:
The automatic permanent effect granted when two branches both reach affinity 3. Exactly three exist, each keyed to a pair of branches rather than to either branch alone. Never purchased.
_Avoid_: hybrid tech, combo unlock

**Deep build / Hybrid build / Pure build / Common-heavy build**:
Informal descriptors for discussing strategy — respectively, carrying a branch to 5, reaching 3 in two branches, investing in at most one branch, and spending mostly on Common. Deliberately overlapping and non-exhaustive; never predicates the rules evaluate.

### The match

**Match**:
One complete contest between two players, ending when a player reaches 0 Command. Targeted at 8–12 rounds.

**Round**:
One iteration of the loop — income, inspection, purchase, repositioning, lock, simultaneous reveal, battle, Command damage. What the match is counted in and what Command damage is assessed per.

**Battle**:
The automatic combat phase inside a round. A battle produces a round winner; it does not itself deal Command damage. It ends when a player has no surviving models, or at 90 simulated seconds, whichever comes first — subject to the pursuit phase.
_Avoid_: fight, combat round

**Pursuit phase**:
The bounded window following a wipe, ending at wipe + 20s or at 90s, during which surviving squads with nothing left to fight move to the enemy control point. It is what lets a decisive battle win earn a *slice* of the objective axis rather than none of it or all of it. The 20s is a dial: a longer window pays the victor more and dilutes the loser's earlier banking more.

**Control point**:
The scoring volume at the centre of each player's own deployment band. No collision, obstructs nothing. A player banks control of the *enemy's* point by holding, continuously, more squad value within 8m than the enemy holds there — where a squad contributes `squadCost × (models within 8m ÷ its full model count)`, so contribution decays with casualties and with formation sprawl. Because contesting requires value *inside* the radius, **a point cannot be denied from outside it**.
_Avoid_: objective (ambiguous — the mechanic is the point), capture point

**controlShare**:
Banked seconds ÷ total battle duration, including the pursuit phase. Accrues continuously while the battle is live rather than being read as an end-of-battle snapshot, so an army that dominates the point early keeps the credit even if it is later destroyed. This is what decouples control from the battle result.

**Planning phase**:
Everything in a round before simultaneous reveal. Private to each player.

**Lock**:
The act that ends a player's planning phase, fixing their purchases and positions for the round.

**Locked army**:
A player's army configuration as of their lock in a given round. Load-bearing: a player may inspect only the opponent's *previous* locked army, which is what prevents live counter-positioning.

**Command**:
The 100-point total that serves as a player's life. A player loses the match at 0.

**Round damage**:
The Command each player loses in a round, drawn from a conserved **round stake** that ramps with the round number and splits across two decoupled axes — 70% battle, 30% control objective. Both players may take damage in the same round, since objective damage flows independently of who won the battle.
_Avoid_: "the loser's damage" (retired with #6 — damage is exchanged, not one-way)

**Income**:
Gold granted at the start of each round from round 2 onward. Unused gold carries forward.

### Combat

**Tag**:
A boolean classifier from an open, extensible set. A thing may carry any number of tags or none, in one of two namespaces: **attack tag** and **status tag**.

**Attack tag**:
A tag classifying an attack. `Heavy` is the only member in v0.4.

**Status tag**:
A tag classifying a status. `HardControl` is the only member in v0.4, covering Root, Stun and Frozen.

**Heavy**:
The attack tag marking an attack as heavy enough to Shatter a Frozen target. Editorially assigned per attack, not derived from a damage threshold.

**Size**:
A single-valued property of a **model**, derived physically as **Large** when its collision radius is ≥ 0.8m and **Small** otherwise. `Huge` is reserved for later rosters and unused in v0.4. Because it is a model property, size is evaluated per target model rather than per squad. In v0.4 the Large models are Troll and Outriders.

**Collision radius**:
The radius of the circle a model occupies and obstructs movement with. All distances in v0.4 are measured **surface-to-surface** — between collision circles, not between centres — so reach means the same thing regardless of target size.

**Damage type**:
A single-valued property of an attack: **physical** or **magic**. Magic sees half of a target's armour; physical sees all of it.

**Branch, size and damage type are properties, not tags** — a thing has exactly one of each, where tags are set-valued and open.

**Offensive modifier**:
A damage modifier that pools **additively** onto base damage before anything else, so each added source gives less than the last.

**Delivery scalar**:
A damage multiplier that is a property of *which target was hit* rather than of the attack, applied per target hit. Splash falloff is the archetype.

**Defensive modifier**:
A damage reduction on the target's side, chained **multiplicatively** with the armour curve, so no stack of reductions can reach immunity.

**Bypass**:
The fraction of a target's armour an attack simply does not see, applied before armour penetration. Magic damage bypasses 0.5.

**Armour penetration**:
A flat subtraction from the armour an attack faces, applied after bypass.

**Attacking models**:
The models in a squad that currently have a valid target within their own reach — the count that effective squad DPS is actually computed from, which for a deep formation is fewer than the squad's model count.
_Avoid_: engagedModels (retired — it collided with `Engaged` below)

**Engaged**:
The state of a model that has been hit by a squad's **melee** attack within the last 2.0 seconds — always engaged *by* a named squad. Directional and defender-side: being engaged says nothing about whether you are attacking back.

**Predation**:
The movement behaviour granting +10% movement speed while moving toward a wounded or isolated enemy model. Innate to Direwolves, granted branch-wide by the Beast doctrine. Strictly a movement effect — it has nothing to do with target selection.

**Target preference**:
A unit-type-specific bias in target *selection* that overrides plain distance-and-stickiness. Three exist: Direwolves' **backline preference**, Hooked Spear Guard's Large preference, and Bodkin Longbowmen's armoured preference.

**Wounded**:
Below 50% HP.

**Isolated**:
Having no allied model within 3.5m.

### Elemental and control

**Burning**:
An elemental status dealing periodic magic damage and cutting regeneration by 75%. Refreshes on reapplication and never stacks its damage.

**Chilled**:
An elemental status reducing movement speed. A second application while it is active causes Frozen.

**Frozen**:
An elemental status preventing movement and pausing the attack timer, tagged `HardControl`. Large models receive half its duration.

**Shatter**:
The bonus damage a `Heavy` attack deals to a Frozen target. It does not consume Frozen.

**Hard-Control Immunity**:
The window following any `HardControl` status during which the model cannot receive another. Replaces bespoke per-ability immunity rules.

**Brace / Braced**:
The state a stationary Spear Guard squad enters, trading incoming charge damage for a bonus first contact attack and ending the attacker's charge. Ends when the squad moves.

### Positioning

**Facing**:
The direction a **squad** is turned — the direction of its current move order, or toward its current squad target when stationary or engaged. Squad-level and authoritative: models may face wherever for presentation, and no rule reads model facing.

**Frontal arc**:
The ±90° wedge around a squad's facing. Attacks from inside it are frontal; everything else strikes the rear hemisphere.

**Flanking**:
Attacking a squad from outside its frontal arc. A combined-arms play by construction — turn rates are set high enough that no squad can out-orbit another alone.

**Formation**:
The arrangement of a squad's models relative to one another, authored per unit type rather than derived from model count, because formation shape carries role identity.

**Frontage**:
How broad a formation is across its facing — the width it presents to an enemy line.
_Avoid_: formation width

**Formation spacing**:
The centre-to-centre distance between a formation's models, trading area-damage exposure against frontage and flanking exposure.

**Charging**:
The state a **Large** model enters when it has closed on its target far and long enough unobstructed, granting a bonus contact attack. Ends on impact and cannot be re-entered immediately.

**Stance**:
The one-of-three order — **Hold**, **Advance** or **Raid** — every squad carries, set by the player during the reposition step. Hold squads stay on their deployed position; Advance squads close to weapon range on the nearest enemy squad and stop; Raid squads move to the enemy control point. A movement order, never a targeting one — which is why it does not violate §24.
_Avoid_: "the stance bit" (retired — Stance has three values, not two)

**Raid**:
The stance ordering a squad to the **enemy control point**. Its destination is fixed by the rules rather than chosen by the player, making it a commitment decision rather than a command interface. Offence-only: defending a control point is Hold plus a deployment position, since a player's own point lies inside their own deployment band.

**Push through**:
The travel behaviour of a Raid squad: it does not acquire targets and does not stop for them, attacking only enemy models physically obstructing its path and resuming when the path clears. On arrival it reverts to Hold. Consequently **Exposed is blind to a raid** — screening a raid is collisional, not perceptual, so a screen must stand *on* the lane rather than near it.

**Break**:
The conversion of a **Hold** squad to Advance, permanent for the battle, triggered when it takes damage while no model in it is `Engaged` and it has no valid target within its own weapon range. A squad within 8m of either control point does not break. Exists so that out-ranging a screen is a trade rather than a free delete.
_Avoid_: rout, morale (nothing here models morale — Discipline/Terror is deferred)

**Screening**:
Interposing a squad so that it, rather than what stands behind it, is what the enemy reaches. With no terrain in v0.4, enemy models are the only possible obstruction, so screening and path accessibility are the same fact — both are read off **Exposed**.
_Avoid_: target access (retired — use Exposed)

**Backline**:
A **unit class**, not a map region: unit types whose primary weapon range is long enough to fight from behind a line. What backline preference hunts.

**Exposed**:
The property of a target squad with no enemy melee-capable squad near the straight line from attacker to target. The single check behind both screening and "reasonably accessible path".
