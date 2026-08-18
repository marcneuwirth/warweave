# WARWEAVE

A competitive 1v1 fantasy army auto-battler. Players build persistent armies across 8–12 rounds, deepening one or more of three branches — Military, Magic, Beast — and win by reducing the opponent's Command to 0.

This is the project's glossary and nothing else. Design detail lives in [`docs/spec/v0.4.md`](docs/spec/v0.4.md); recorded decisions live in [`docs/adr/`](docs/adr/).

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
The gold purchase price of one squad of a unit type. Excludes technology and track cost.
_Avoid_: unitCost, unit value

**Squad cap**:
The maximum number of squads a player may own — 12. **Owned equals fielded; there is no bench.** Technologies and track steps do not consume slots.

**Slot ceiling**:
R8's cumulative income divided by the squad cap — **292 gold per affordable slot**. A purchase priced above it is bought in *slots forgone* rather than in gold. The price list is authored against it.

**Common**:
The fourth value of the **branch** property — **Militia and Hunters**, available to every player from round 1. A branch value but not a specialization track: no gateway, no doctrine, no affinity, no branch investment, and **no role**. It matches no rule that names Military, Magic or Beast, so Common unit types receive no doctrine and no hybrid unlock. They are not excluded from the *systems* those effects read — Pitch & Torch lets Militia apply Burning — only from the rewards. **Common is the R1–R4 army**: it wins when gold binds and loses when slots bind.

### Role and rung

**Role**:
What a unit type is *for*. Exactly three exist, each graded on a stated quantity: **hold** (eHP × frontage), **reach** (range × applied DPS), **access** (speed × screen bypass). Every branch owns one role at *best* and one at *adequate*, and has a **hole** where the third would be.
_Avoid_: archetype (that word is a deployment shape), class

**Hole**:
The role a branch does not own. It is what a hybrid partner fills, and it is what the branch's counter is aimed at — so the direction of the counter cycle is *derived* from the holes rather than authored on top of them.

**Rotation**:
The assignment of adequate roles such that each branch's adequate role is the role of the branch it beats. Military hold/access, Magic reach/hold, Beast access/reach. Its consequence is that no two branches are mutual and every hybrid pair is structurally symmetric.

**Rung**:
A unit type's standing in its role — **best**, **adequate**, **weak** or **capstone**. Adjacent rungs differ by **25–40%** on that role's quantity: ≥25% because that is the smallest magnitude that reads as a difference, <40% because a rung gap at flip magnitude would make *owning a role* itself a counter.

**Tier**:
The affinity gate a unit type sits behind — **0** (gateway), **2**, or **4** (tier-3). Tier-3 has two unit types per branch: **α**, which narrows the branch's hole, and **β**, which escalates the role it already wins with.

**Counter**:
A conditional damage effect keyed on a **functional property** the opponent's build cannot avoid exposing — formation coherence, closing speed, model scarcity — never on `branch`. Three exist, each at step 3 of one tier-3 upgrade track, each at flip magnitude. A wide build owns none.

### Branch and progression

**Branch**:
A single-valued property of a **unit type**, total across the roster, with exactly four values: Military (*Coordinate*), Magic (*Combine*), Beast (*Overwhelm*) and **Common**. The first three are specialization tracks — each owns a unit-type pool, its technologies, unit types at affinity 0, 2 and 4, and a doctrine at 5. Common is a branch value that is not a track.
_Avoid_: faction, tree, affinity (when naming the branch itself); "the three branches" when the property is meant (there are three *tracks* and four *values*)

**Branch denotation**:
The rule governing what a branch name means in rules text. **Wherever a rule names a branch, it denotes the `branch` property of the unit type of the model in question — attacker, ally or target alike.** Common unit types match none of the three tracks. A branch name never denotes damage type, and damage type never implies a branch: "Military attacks" means attacks by Military-branch unit types, not physical attacks. The rule is global — doctrines, hybrid unlocks, technologies, and both attacker-side and target-side predicates.

**Affinity**:
The integer level from 0 to 5 that a player holds **in a branch**, derived as `floor(branchInvestment / 200)`. Never standalone — always branch-then-level, as in "Military 3".
_Avoid_: affinity points, "the three affinities" (there are three *branches*)

**Branch investment**:
Cumulative gold committed to a branch through **squad purchases only** — technologies and track steps generate none. Removed in full at the purchase price when a squad is sold, so affinity always describes the army currently owned. **Stamped at purchase**: gold is credited to the branch the unit type held at the moment it was spent, and nothing later moves it. Investment is an accounting fact about a transaction, never a live re-read of the branch property.
_Avoid_: affinity investment (affinity is derived, never purchased)

**Gateway**:
A branch's affinity-0 unit type. Every gateway costs **200 gold** against a 200 divisor, which is what makes *400 = two gateways = Affinity 2* and *5 × gateway = Affinity 5* hold identically on all three branches. Load-bearing: repricing a gateway breaks both identities.

**Counts-as membership** *(forward invariant — no member in v0.4)*:
A set-valued membership letting a unit type match a branch it does not belong to, for **rules reads only**. It adds a membership rather than overwriting `branch`, is evaluated live at the moment a rule reads it, and **never touches branch investment**. This is the only sanctioned shape for an effect such as "Common units count as Military": as a branch swap it would relocate past spending and become an affinity pump.

**Technology**:
A purchased permanent upgrade attached to a **tier-0 or tier-2** unit type, applying to every squad of that type. Two authored per unit type, **at most one owned**, never refunded, no squad slot. Sixteen in v0.4.
_Avoid_: upgrade, perk, research

**Upgrade track**:
A tier-3 unit type's specialization: **one named effect at three magnitudes**, crossing flip magnitude only at step 3, so partial investment is sub-flip rather than inert. Two authored per tier-3 unit type; a player picks one at step 1 and the fork is locked thereafter. Steps cost 150 / 200 / 250 and never refund.

**Doctrine**:
The permanent effect a branch grants at affinity 5. Exactly three exist, never purchased — but **at most one is active at a time**, so reaching affinity 5 in a second branch grants nothing by itself.
_Avoid_: ultimate, capstone (capstone is a *rung*)

**Active doctrine**:
The single doctrine currently in effect. Distinct from being at affinity 5, which may be true of up to three branches at once.

**Doctrine re-choice**:
The priced, rate-limited act of moving the active doctrine to another branch already at affinity 5 — **500 gold** (one round's plateau income), immediate, with a **3-round lockout**. The lockout is structural; the fee is a dial.

**Hybrid unlock**:
The automatic permanent effect granted when two branches both reach affinity 3. Exactly three exist, each keyed to a pair of branches rather than to either branch alone. Never purchased, and they **stack**.
_Avoid_: hybrid tech, combo unlock

**Deep build / Hybrid build / Pure build / Common-heavy build**:
Informal descriptors for discussing strategy — respectively, carrying a branch to 5, reaching 3 in two branches, investing in at most one branch, and spending mostly on Common. Deliberately overlapping and non-exhaustive; never predicates the rules evaluate.

**Convergent build**:
Informal descriptor for **5/3/3** — one doctrine plus all three hybrid unlocks, the predicted gold- and slot-optimal end state. Named so that it can be tested as a benchmark rather than assumed.

### The match

**Match**:
One complete contest between two players, ending when a player reaches 0 Command. Targeted at 8–12 rounds.

**Round**:
One iteration of the loop — income, inspection, purchase, repositioning and stance, lock, simultaneous reveal, battle, Command damage. What the match is counted in and what Command damage is assessed per.

**Battle**:
The automatic combat phase inside a round. A battle produces a round winner; it does not itself deal Command damage. It ends when a player has no surviving models, or at 90 simulated seconds, whichever comes first — subject to the pursuit phase.
_Avoid_: fight, combat round

**Pursuit phase**:
The bounded window following a wipe, ending at wipe + 20s or at 90s, during which surviving squads with nothing left to fight move to the enemy control point. It is what lets a decisive battle win earn a *slice* of the objective axis rather than none of it or all of it. The 20s is a dial: a longer window pays the victor more and dilutes the loser's earlier banking more.

**Control point**:
The scoring volume at the centre of each player's own deployment band. No collision, obstructs nothing. A player banks control of the *enemy's* point by holding, continuously, more squad value within 8m than the enemy holds there — where a squad contributes `squad cost × (models within 8m ÷ its full model count)`, so contribution decays with casualties and with formation sprawl. Because contesting requires value *inside* the radius, **a point cannot be denied from outside it**.
_Avoid_: objective (ambiguous — the mechanic is the point), capture point

**controlShare**:
Banked seconds ÷ total battle duration, including the pursuit phase. Accrues continuously while the battle is live rather than being read as an end-of-battle snapshot, so an army that dominates the point early keeps the credit even if it is later destroyed. This is what decouples control from the battle result.

**Planning phase**:
Everything in a round before simultaneous reveal. Private to each player.

**Lock**:
The act that ends a player's planning phase, fixing their purchases, positions and stances for the round.

**Locked army**:
A player's army configuration as of their lock in a given round. Load-bearing: a player may inspect only the opponent's *previous* locked army, which is what prevents live counter-positioning.

**Command**:
The 100-point total that serves as a player's life. A player loses the match at 0.

**Round stake**:
The Command placed on the table each round, `S(round) = 5 + 2 × round`, split **70% battle / 30% control objective**. Conserved when the point is contested — which is what bounds match length to 8–12 regardless of how the two axes fall.

**Round damage**:
The Command each player loses in a round, drawn from the round stake. Both players may take damage in the same round, since objective damage flows independently of who won the battle.
_Avoid_: "the loser's damage" (retired — damage is exchanged, not one-way)

**winnerIntegrity**:
The round winner's surviving fraction of its own deployed value, scaling battle damage over a compressed [0.75, 1.00]. Read on the *winner* because in an elimination the loser has zero remaining, so any ratio between armies is inert.

**Income**:
Gold granted at the start of each round from round 2 onward, `min(300 + 50 × (round − 2), 550)`. Unused gold carries forward.

### Combat

**Tag**:
A boolean classifier from an open, extensible set. A thing may carry any number of tags or none, in one of two namespaces: **attack tag** and **status tag**.

**Attack tag**:
A tag classifying an attack. `Heavy` is the only member in v0.4.

**Status tag**:
A tag classifying a status. `HardControl` is the only member in v0.4, covering Root, Stun and Frozen.

**Heavy**:
The attack tag marking an attack as heavy enough to Shatter a Frozen target. Editorially assigned per attack, never derived from a damage threshold — so retuning a damage number can never silently move a control mechanic.

**Size**:
A single-valued property of a **model**, derived physically as **Large** when its collision radius is ≥ 0.8m and **Small** otherwise. `Huge` is reserved for later rosters and unused. Because it is a model property, size is evaluated per target model rather than per squad. **In v0.4 the Troll is the only Large unit type.**

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

**Overkill**:
Damage in excess of a model's remaining HP. **It does not carry** to the next model, which is what makes model count a real defensive stat and forces anti-swarm to come from splash.

**AoE catch**:
The number of models an area effect hits, derived geometrically as `≈ πr² / spacing²` rather than counted off a list. Single-model squads catch nothing. This is what makes formation spacing a defensive stat and formation coherence a counterable property.

**Engaged**:
The state of a model that has been hit by a squad's **melee** attack within the last 2.0 seconds — always engaged *by* a named squad. Directional and defender-side: being engaged says nothing about whether you are attacking back.

**Predation**:
The movement behaviour granting +10% movement speed while moving toward a wounded or isolated enemy model. Innate to Direwolves, granted branch-wide by the Beast doctrine. Strictly a movement effect — it has nothing to do with target selection.

**Target preference**:
A bias in target *selection* that overrides plain distance-and-stickiness. Three exist, plus one negative clause. **Access-role unit types cull** — each model attacks the lowest-current-HP enemy model within its own reach, and with nothing in reach the squad tracks the enemy squad with the lowest *total* HP, which makes **backline preference derived from the stat blocks rather than authored**. Two are technology-granted (Large preference, armoured preference). The negative clause: Frostcaller does not select a model that is currently Frozen.

**Wounded**:
Below 50% HP.

**Isolated**:
Having no allied model within 3.5m. At default spacing this describes exactly two states: lone survivors, and single-model squads.

### Elemental and control

**Burning**:
An elemental status lasting 4 seconds, dealing **10 magic damage per second** — flat and source-independent, outside the applying attack's offensive pool — and cutting regeneration by 75%. Refreshes on reapplication and never stacks its damage.

**Chilled**:
An elemental status lasting 3 seconds and reducing movement speed by 20%. A second application while it is active causes Frozen — so **a freeze normally costs two chills**, and Primal Magic is the one exception.

**Frozen**:
An elemental status preventing movement and pausing the attack timer, tagged `HardControl`. Lasts 0.75s and is followed by Hard-Control Immunity. **Exempt from the Large 50% discount** — the immunity window is a sufficient brake on its own — and **does not consume Chilled**, which is what lets Beast attacks hold a chill through a freeze.

**Shatter**:
The **+25%** bonus a `Heavy` attack deals to a Frozen target. It does not consume Frozen, so the physical half of the combo no longer cuts short the window the Magic half paid for.

**Deep chill**:
The **+25%** bonus **magic** damage deals to a Frozen target, requiring no tag. It exists because no Magic attack is `Heavy`, so without it the branch could not cash the window it created.

**Hard-Control Immunity**:
The 1.25-second window following any `HardControl` status during which the model cannot receive another. Replaces bespoke per-ability immunity rules, and caps Frozen uptime on one target at 37.5% however many casters are fielded.

**Brace / Braced**:
The state a stationary Spear Guard squad enters, halving an incoming **Charging** attacker's charge damage, gaining a bonus first contact attack, and ending the attacker's Charging state. Ends when the squad moves.

### Positioning

**Facing**:
The direction a **squad** is turned — the direction of its current move order, or toward its current squad target when stationary or engaged. Squad-level and authoritative: models may face wherever for presentation, and no rule reads model facing.

**Frontal arc**:
The ±90° wedge around a squad's facing. Attacks from inside it are frontal.

**Rear arc**:
Everything outside the frontal arc. Attacks landing here flank.

**Flanking**:
Attacking a squad from outside its frontal arc, for **+25% from all sources**, melee and ranged alike. Tested **per attacking model** against squad-level facing, so a squad wrapping a formation flanks with some models and not others rather than flipping the whole bonus at a boundary. A combined-arms play by construction — turn rates are set high enough that no squad can out-orbit another alone, so a flank structurally requires two squads on different bearings.

**Re-acquisition lockout**:
The 4 seconds during which a squad that has just re-acquired cannot re-acquire again. Rear-arc damage breaks target stickiness **once**, sending the squad to the *nearest* enemy squad rather than to its attacker; the lockout is what stops two cheap squads spin-locking anything forever.

**Formation**:
The arrangement of a squad's models relative to one another, authored per unit type rather than derived from model count, because formation shape carries role identity.

**Frontage**:
How broad a formation is across its facing, `(front rank − 1) × spacing + 2 × collision radius`. Load-bearing twice over: it is half of the hold quantity, and it is what a squad sprawls outside a control point's radius with.
_Avoid_: formation width

**Formation spacing**:
The centre-to-centre distance between a formation's models, trading area-damage exposure against frontage and flanking exposure.

**Charging**:
The state a model whose unit type carries the **Charging chassis** enters when it has closed on its target far and long enough unobstructed, granting a bonus contact attack. Ends on impact and cannot be re-entered for 6s. Carried by access-role chassis rather than by Large models, which is what makes closing speed the property the Beast counter keys on.

**Stance**:
The one-of-three order — **Hold**, **Advance** or **Raid** — every squad carries, set by the player during the reposition step. Hold squads stay on their deployed position; Advance squads close to weapon range on the nearest enemy squad and stop; Raid squads move to the enemy control point. A movement order, never a targeting one.
_Avoid_: "the stance bit" (retired — Stance has three values, not two)

**Raid**:
The stance ordering a squad to the **enemy control point**. Its destination is fixed by the rules rather than chosen by the player, making it a commitment decision rather than a command interface. Offence-only: defending a control point is Hold plus a deployment position, since a player's own point lies inside their own deployment band. **Attack is a command; defence is a position.**

**Push through**:
The travel behaviour of a Raid squad: it does not acquire targets and does not stop for them, attacking only enemy models physically obstructing its path and resuming when the path clears. On arrival it reverts to Hold. Consequently **Exposed is blind to a raid** — screening a raid is collisional, not perceptual, so a screen must stand *on* the lane rather than near it.

**Break**:
The conversion of a **Hold** squad to Advance, permanent for the battle, triggered when it takes damage while no model in it is `Engaged` and it has no valid target within its own weapon range. A squad within 8m of either control point does not break. Exists so that out-ranging a screen is a trade rather than a free delete.
_Avoid_: rout, morale (nothing here models morale — Discipline/Terror is deferred)

**Screening**:
Interposing a squad so that it, rather than what stands behind it, is what the enemy reaches. With no terrain in v0.4, enemy models are the only possible obstruction, so screening and path accessibility are the same fact — both are read off **Exposed**.
_Avoid_: target access (retired — use Exposed)

**Backline**:
A **unit class**, not a map region: unit types whose primary weapon range is long enough to fight from behind a line.

**Exposed**:
The property of a target squad with no enemy melee-capable squad near the straight line from attacker to target. The single check behind both screening and "reasonably accessible path". Blind to raids by construction.

**Wall / Concentrate**:
The two ways to spend the field's 60m width. **Walling** spreads a holding army across the front to deny the flank and the raid lane, at the cost of depth and reserve — and it is never complete, because non-overlapping footprints leave a seam passable model by model. **Concentrating** masses squads on a narrow front for local superiority at the point of contact, conceding the flank to win the collision.

### Measurement

**Deployment archetype**:
One of six named layouts — `line`, `screened`, `refused`, `wings`, `column`, `forward` — each fixing an exact coordinate and stance per squad. The versioned thing is the **rule** (`layout v2`, `instruments/deployment-layout-v2.md`), not the coordinates: the runner generates a deployment for any army, and the frozen 1,056-row table is the conformance check that a second implementation is the same generator. A cell the rule cannot place legally is `deploymentInfeasible` and drops out of that army's 6 × 6 mean rather than failing the pass. Run as a 6 × 6 cross product, they are the sampling population that turns a deterministic battle into a **win rate**. `line` and `screened` are the same wall differing only in where reach stands, and are the instrument for measuring whether *placing* a screen matters. `line` is the designated **poor positioning** row.

**Reference purchase policy**:
The versioned decision procedure that generates representative builds and scores the three headings — greedy marginal value with no authored preferences, over a two-round gold horizon. Category constraints are a legality filter on its action set and nothing more, so the constraint never does the policy's work for it.

**Dominant core / Guessing margin**:
The two halves of positioning skill. The **core** is correct against the opponent's revealed *composition*, whatever their placement — screen the backline, don't leave two bearings open, match frontage. The **margin** is correct only against their specific *placement*. Only the core counts as evidence for a positioning gate; the margin is intended texture.

**Engagement scale**:
2–4 squads a side, equal gold — the scale at which positioning gates are read. At unit scale three of the four levers cannot produce a flip at all; at twelve squads a flip cannot be attributed.

**Marginal inclusion**:
The test for whether a unit type is competitively useful: there is at least one army and one opponent archetype where **replacing it with the best legal substitute at equal spend turns a win into a loss**. Load-bearing in a winning army — strictly stronger than appearing in one, strictly weaker than dominating a matchup.

**Heading**:
One of the three lines a planning phase can take — **counter**, **deepen**, **weave**. A round is **live** when the best two headings finish within ε of each other; the recurrence of live rounds is the central strategic product test.
