# `layout v2` — the deployment layout rule

Resolves [#49](https://github.com/marcneuwirth/warweave/issues/49). Implements the rulings
of [#33](https://github.com/marcneuwirth/warweave/issues/33). Supersedes §1 of
[`docs/analysis/deployment-archetypes.md`](../docs/analysis/deployment-archetypes.md),
which authored the set for [#18](https://github.com/marcneuwirth/warweave/issues/18).

**This document is the canonical definition of the rule.** Two witnesses implement it, and
where either disagrees with this document, this document is right and the witness is a bug:

| Witness | What it is |
| --- | --- |
| [`docs/analysis/matchup-math/proto_archetypes.py`](../docs/analysis/matchup-math/proto_archetypes.py) | The Python generator. Independently authored, and scheduled for deletion with the rest of the throwaway |
| [`docs/analysis/deployment-archetypes-v2.csv`](../docs/analysis/deployment-archetypes-v2.csv) | The conformance table: 1,056 rows the Go generator must reproduce byte for byte |

The reason the rule is written down rather than promoted from either implementation is
[#30](https://github.com/marcneuwirth/warweave/issues/30)'s precedent. #30 did not ship
`golden-v1.json` alone; it shipped `golden-v1.md` **with the arithmetic shown**, so a
failing test is adjudicated against a *stated reading* before anyone opens the kernel.
Deployment has the same structure and the same silences: overflow ranks appended at 5m, a
comparator that broke ties on descending frontage, `forward` packing at 3.5m — none of which
anyone decided. They were incidental properties of prototype Python, and promoting that file
would have made the accidents the spec by default. Its own docstring said `PROTOTYPE --
throwaway`.

The rule survives the redo. **The Go implementation does not**, so nothing here may be
recorded only as code.

---

## 1. What `layout v2` versions

**One artifact, one number** (#33 §7), replacing §33's *"Deployment archetype set v1"* row.
Three components travel together:

| Component | Where |
| --- | --- |
| The rule | this document |
| The fifteen builds | [`data/builds.json`](../data/builds.json) |
| The conformance table | [`docs/analysis/deployment-archetypes-v2.csv`](../docs/analysis/deployment-archetypes-v2.csv) |

They carry one version number because **the table is a pure function of the other two**: a
rule change or a build-set change each invalidate it, and neither can be adopted without
regenerating it. Two numbers would encode three states, one of which — rule v3 + builds v2 +
a table matching neither — is always a bug. The roster keeps its own number for the opposite
reason: the rule *reads* the roster and does not define it.

Accepted cost: a sixteenth build bumps the same number as a layout-rule fix, so `layout v2`
does not say *which* changed without opening the artifact. §33's change semantics are
deliberately cache-invalidation-shaped, and coarse invalidation is the safe direction.

`manifest.json` carries `layoutVersion`. It is one of the four version slots fixed by
[#39](https://github.com/marcneuwirth/warweave/issues/39); this document does not add a
fifth.

### What changed from v1

| | Change | Cells moved |
| --- | --- | --- |
| **The comparator became total** (§4) | third sort key on unit-type name | **12 of 90** — `MilDeepRally` and `MilMagic`, in all six archetypes |
| **The band clamp became an invariant** (§6) | every squad's `y` in `[depth/2, 24 − depth/2]` | **0 of 90** |
| **The fifteen moved into `data/`** (§7) | out of `FIELD` in the 1-D witness | none — value-identical |

Measured, not asserted: the two amendments were applied in isolation against the v1 table,
and v1 → v2 differs in **exactly those twelve cells and nowhere else**.

---

## 2. The field

60m × 80m (§23). Each player deploys inside the nearest **24m** (§23.1).

| | Value |
| --- | --- |
| Field | `x ∈ [0, 60]`, `y ∈ [0, 80]` |
| Own band | `y ∈ [0, 24]`; baseline `y = 0`, front edge `y = 24` |
| Enemy band | `y ∈ [56, 80]`; enemy front edge `y = 56` |
| Gap between front edges | **32m** |
| Own control point | `(30, 12)` |
| Enemy control point | `(30, 68)` |

**The rule emits own-band coordinates only.** The opposing side is the **point reflection
about the field centre `(30, 40)`**:

> `(x, y) ↦ (60 − x, 80 − y)`

Reflection rather than a `y`-translation, because
[#28](https://github.com/marcneuwirth/warweave/issues/28) made *an army against its own
point reflection must draw, with a reflection-invariant result hash* a committed P0
acceptance test. A translated mirror would place both armies' left flanks on the same side
of the field and the test would be measuring something else. It is also what
[#39](https://github.com/marcneuwirth/warweave/issues/39)'s mirrored rollout replicates
mean by *mirrored*.

**Placement is continuous** — no grid snap. Coordinates are a squad's **centre**.

### Footprint

```
frontage = (frontRank − 1) × spacing + 2 × collisionRadius
depth    = (ranks − 1)     × spacing + 2 × collisionRadius
```

Surface-to-surface per §13, which is what makes six Spear Guard **64.8m** rather than 60m
(§1.6 of the #18 write-up: the full-width wall does not exist, and five Spear Guard leave a
6m seam). Both are **rules over data**, per #26's line — only the inputs (`frontRank`, `ranks`,
`spacing`, `collisionRadius`) are in `roster-v2.json`. `frontage` has a canonical Python
implementation in [`data/roster.py`](../data/roster.py), checked against the spec's stated
values by `conformance_test.py` §5; `depth` is the same formula on the other axis and has no
reader outside the layout rule.

**Footprints may not overlap** (§23.1). This binds a player's own squads and is a
*deployment* constraint: [#45](https://github.com/marcneuwirth/warweave/issues/45) ruled
that after deployment enemy models block and **friendly models are permeable**. So
non-overlap is checked here, once, and never again during the battle.

---

## 3. Building an army's list

An army is a **multiset** of unit types — one entry per squad, never an ordered list.
#33 §4 rejected making purchase order part of an army's identity: it makes two identical
armies bought in different orders into rows that never aggregate, and it breaks §33.3's
substitution rule (*"the substitute stands exactly where the replaced squad stood"*) the
moment a swap changes sort position.

For the fifteen, the list is `data/builds.json`'s squads expanded by `count`, in file order.
For a policy army it is whatever the policy owns. **After §4 the two are treated
identically**, because the comparator no longer reads input order.

---

## 4. `by_role` — the front-to-back order

Every archetype begins by sorting the army's squads:

```
key(unitType) = ( roleOrder[role], −frontage, unitTypeName )

roleOrder = { hold: 0, none: 1, access: 2, reach: 3 }
```

Ascending. Hold leads, Common follows, access next, reach trails; within a role the widest
squad leads; ties break on the unit type's name, ascending by Unicode code point.

**The third key is load-bearing, and it is the v2 change** (#33 F-2). Without it the
comparator is **not a total order**, and there are three real collision groups in the v0.4
roster:

| Group | Ties on |
| --- | --- |
| `SpearGuard`, `BannerGuard`, `Lifewarden` | hold, 10.8m |
| `EmberMage`, `Frostcaller` | reach, 4.8m |
| every repeated unit type | itself |

A stable sort resolves those by **input order**. For the fifteen that is file order — frozen,
harmless. For a policy army it is **purchase order**: where your Spear Guard stand would
depend on which round you bought them. That is an undeclared input, and a silent violation of
[#25](https://github.com/marcneuwirth/warweave/issues/25)'s rule that every comparator ends
in an ID.

The bump was taken at this moment rather than later because the invalidation cost is
near-zero now and never gets cheaper: **no coordinate-based measurement exists yet.** The 1-D
arm has no geometry and §33.8's predictions are paper.

**The rest of the rule inherits totality from here.** `stances()`'s raider pick (§9) breaks
ties by list index — placement order — and is total only because this comparator is. So is
every rank-fill decision in §5.

---

## 5. `row` and `rows` — filling ranks

### `row(names, y, x0, x1)` — one rank, evenly gapped

Given a lane `[x0, x1]` of width `L = x1 − x0` and squads whose frontages sum to `S`:

```
g = (L − S) / (n + 1)                     the gap, n = number of squads
if g < 0: g = 0
x = x0 + g                                the left edge of the first squad
for each squad, in order:
    centre = x + frontage/2
    x += frontage + g
```

`n + 1` gaps rather than `n − 1`, so the rank carries a margin of `g` at each end and is
**centred in its lane** as a consequence rather than by a second calculation. A rank whose
squads do not fit (`g < 0`) packs flush from `x0` and runs off the right of the lane; §5's
fill rule is what stops that arising.

### `rows(names, ys, x0, x1, step)` — front to back

Ranks are consumed from `ys` in order. Each rank greedily takes squads off the front of the
list while they fit the lane:

```
span = 0
while the next squad has frontage f and span + f ≤ L:
    take it; span += f + 1.0
```

The `+ 1.0` is a **notional 1m separation** reserved between squads during the fit test only;
the actual gap is `row`'s `g`, which is ≥ 1.0 exactly when the rank is not full. It is
charged for the last squad taken as well, which makes the fill conservative by one metre —
recorded because it is arbitrary, not because it is right.

If not even one squad fits (a squad wider than the lane), **that squad is placed alone and
overflows the lane.** This is a `deploymentInfeasible` outcome (§6), not a clamp: no unit
type in the v0.4 roster is wider than any archetype's narrowest lane (`column` at 24m against
Spear Guard's 10.8m), so it is unreachable today and is specified so a future roster cannot
reach it silently.

### Overflow ranks

**This is the path a novel army hits hardest, and it was an unrecorded incidental of
prototype Python.** Twelve squads never fit in one rank on a 60m field, so every archetype
needs an unbounded rank supply.

> When `ys` is exhausted and squads remain, one further rank is appended at
> `previousRank − step`, repeatedly, until the army is placed.

`previousRank` is the **planned** `y` of the rank before it, taken *before* §6's clamp. An
overflow rank must keep descending even where the clamp held the previous rank's squads
inside the band; reading back a clamped coordinate could stall the descent and stack two
ranks on the same line.

`step` is per archetype (§8). Running out of band is not a stopping condition — it is a
`deploymentInfeasible` outcome.

Exercised by the conformance table on **12 of the 90 cells** — nine `refused` and three
`screened`. `line`, `wings`, `column` and `forward` never reach it with the fifteen.

---

## 6. The depth-aware band clamp

> **Invariant.** Every squad's centre `y` satisfies `depth/2 ≤ y ≤ 24 − depth/2`.

Applied to each squad as its coordinate is emitted, using **that squad's own depth**. It is a
stated invariant of the rule in the shape of
[#28](https://github.com/marcneuwirth/warweave/issues/28)'s load-time
`maxSpeedSum × tickSeconds < minMeleeReach` — a property the rule guarantees, not a repair
applied afterwards.

It closes a gap §1.5 of the #18 write-up half-closed (#33 F-3). That section derived *"rank
pitch is bounded below by footprint depth"* for `forward`'s 3.5m, but never applied the same
treatment to **the rear rank's offset from the baseline**. `screened` and `refused` park
their rear rank at `y = 1.0`, and a Troll there is 2.4m deep and lands at `y = −0.2`, off the
field.

Measured, at both ends:

| | Result |
| --- | --- |
| Cells of the frozen 90 it moves | **0** |
| Cells of the frozen 90 where it even fires | **0** |
| Random-army sweep, 6,000 armies × 6 archetypes | **15 of 36,000 infeasible without it; 0 with it** (#33 measured 18 at its own seed) |

The sweep draws 1–12 squads uniformly from all fourteen unit types. Every failure was the
same shape — an out-of-band rear rank — and every one is a Troll, the only unit whose depth
exceeds 2m.

**The clamp is therefore the one path in this rule that the conformance table does not
cover**, by construction: it never fires on the fifteen. That is why #33 also put a
`deploymentHash` on every battle row (§10) — the table can prove a port reproduces 90 cells
and still miss a divergence here entirely.

---

## 7. `deploymentInfeasible` — a declared cell outcome

§1.5 of the #18 write-up claimed *"all 90 archetype × build cells are legal."* That is a
property **of the fifteen, not of the rule** (#33 F-6). It was established by forcing
legality over a frozen build set, and §6 shows the rule admits illegal output outside it.
Under runtime generation, legality is a per-cell outcome.

> A cell is **`deploymentInfeasible`** when any squad's footprint leaves the field or the
> own band, or when two squads' footprints overlap. The harness records the outcome for that
> `(army, archetype)` and continues.

Rejected alternatives, both from #33 §5:

- **Silently clamping whatever comes out.** `screened` means *reach withdrawn behind the
  wall*; a clamp that shoves a Troll forward yields a cell still labelled `screened` that is
  not one. The layout artefact becomes invisible, which is the exact failure §1.1 exists to
  prevent. §6's clamp is different in kind: it is a *stated invariant applied before* the
  legality question, in one axis, and it was measured not to move an authored cell.
- **Hard-failing the pass**, as [#27](https://github.com/marcneuwirth/warweave/issues/27)
  treats `schemaVersion`. At the measured rate across thousands of policy armies, Instrument
  A would abort routinely on a cosmetic rear-rank case.

**Accepted cost, and the constraint it puts on the log.** A dropped cell means §33.1's 6×6
mean is taken over **35 cells, not 36**, for that army. #34 already ruled *every collapse is
an instrument's decision, made at read time*, so it is non-negotiable that
**`deploymentInfeasible` reaches the promoted aggregate as a count** — an instrument that
cannot see the absence would quietly average a different basis.

### The build set's own legality

`data/builds.json` is version-locked to `layout`, but every build is **priced and gated by
the roster**, so a reprice can make one illegal without touching this rule. That second
coupling gets a check rather than a fifth version number (#47):
[`data/conformance_test.py`](../data/conformance_test.py) §9 asserts the §4.4 squad cap, the
§6 affinity prerequisite of every unit fielded, that each track belongs to the unit that
climbs it, and the **round each build first becomes affordable** against §4.2's cumulative
income — so a reprice that moves a build across one of §33.6's R3 / R5 / R8 snapshots is
loud.

---

## 8. The six archetypes

All six sort with §4 first. Coordinates below are the **named ranks**; overflow ranks follow
§5 at the archetype's `step`.

### `line` — the naive wall

Reach is split to **both flanks and stands in the contact rank**. With the sorted list
`ns`, let `back` be its reach squads and `body` the rest; the rank order is
`back[:⌊|back|/2]] + body + back[⌊|back|/2⌋:]`.

| | |
| --- | --- |
| Ranks | `22, 17, 12` |
| Lane | full width, `[0, 60]` |
| `step` | 5.0 |

This is the designated **poor-positioning row** for §27.1's *"hard counter with poor
positioning should fall below 60%"* clause — poor for a stated reason (reach is in the
contact rank), not by decree. A cell lookup on `line` is what makes that clause computable.

### `screened` — the same wall, reach withdrawn

| | |
| --- | --- |
| Screen ranks | `22, 17`, lane `[0, 60]` |
| Reach ranks | `6, 1`, lane `[10, 50]` |
| `step` | 5.0 |

`screen` is every **non-reach** squad; `back` is every reach squad.

**A build with no non-reach squad still gets screened**: its frontmost `⌊|back|/2⌋` reach
squads take the screen slots and the remainder go behind. This is what makes the set legal
for *every* build rather than only for builds that own a screening unit — #18's open
question.

`line` and `screened` are **the same wall differing only in where reach stands**, and the
pair is the instrument for §33's P1: screening was shown to *matter*, but *placing* a screen
is unmeasured. Cutting the set to five means cutting the pair.

### `refused` — refused flank

The sorted list splits at `⌈n/2⌉`: `strong` is the front half, `weak` the back half.

| | |
| --- | --- |
| `strong` ranks | `22, 16`, lane `[30, 60]` |
| `weak` ranks | `12, 6`, lane `[0, 30]` |
| `step` | 5.0 |

### `wings` — split wings, empty centre

The sorted list deals alternately: `left = ns[0::2]`, `right = ns[1::2]`.

| | |
| --- | --- |
| Ranks, both wings | `22, 17, 12, 7, 2` |
| Left lane | `[0, 24]` |
| Right lane | `[36, 60]` |
| `step` | 3.0 |

### `column` — deep column

| | |
| --- | --- |
| Ranks | `22, 19, 16, 13, 10, 7, 4, 1` |
| Lane | `[18, 42]` — a **24m centre lane** |
| `step` | 3.0 |

24m is derived, not chosen: at 16–22m the twelve-squad builds run out of band depth
(`MilDeepRally`, `MilMagic`, `MilBeast` bind first).

### `forward` — forward-concentrated

| | |
| --- | --- |
| Ranks | `22.5, 19, 15.5, 12, 8.5, 5, 1.5` |
| Lane | `[15, 45]` — 30m centre |
| `step` | 3.5 |

**3.5m is a floor set by the roster, not by taste**: Direwolves are two ranks at 2.0m
spacing plus radii = 2.8m deep, and concentration cannot pack tighter than the deepest
squad it concentrates.

---

## 9. Stance

**An archetype is a complete deployment**, so every squad carries a stance and the sweep has
no free variable (§1.4 of the #18 write-up). Six coordinate sets with a free stance would
have left the sweep undetermined, since Hold-vs-Advance decides whether the armies close at
all.

| Archetype | Base stance |
| --- | --- |
| `column`, `wings`, `forward` | all **Advance** |
| `refused` | **Advance** where `x ≥ 30`, else **Hold** |
| `line`, `screened` | **Advance** for role `access`, else **Hold** |

### The raider

**Raid appears in exactly two archetypes** — `refused` and `wings` — so raid-vs-no-raid is a
comparison the sweep can read rather than a global setting.

> Candidates are the squads with role `access`; if the build has none, every **non-reach**
> squad. The raider is `min(candidates, key=(y, −speed))` — the rearmost, breaking ties on
> the fastest. A build with neither fields no raider, which is itself a measurable property
> of the build.
>
> The Raid stance **overwrites** whatever the table above assigned.

`min` breaks its own remaining ties by **list index**, which is placement order. That is a
real dependency and it is recorded rather than removed: placement order is total only
because §4's comparator is. `y` here is the **clamped** coordinate — the raider is picked
from where squads actually stand.

Across the conformance table: **30 Raid, 315 Hold, 711 Advance** of 1,056 slots.

---

## 10. What the runner does with this

**Deployments are reconstructed, never stored** (#33 §3).
[#34](https://github.com/marcneuwirth/warweave/issues/34) fixed the run directory as exactly
`manifest.json` + `battles.jsonl` + `matches.jsonl` and ruled *replay is never evidence*.
Storing coordinates adds a fourth file to a closed container and duplicates heavily — the
same army recurs across thousands of battles. Because the rule is now a durable written
spec, `(composition, archetype) → coordinates` is a pure, cheap, kernel-free function
computable from artifacts that survive the redo. That is not the replay #34 banned, which
required re-running a dead binary.

Per battle row, per side:

| Field | Value |
| --- | --- |
| `armyA` / `armyB` | composition as a **sorted multiset** of unit types |
| `buildRefA` / `buildRefB` | **nullable** — one of the fifteen, or `null` |
| `deploymentHashA` / `deploymentHashB` | FNV-1a over the coordinate table, **including stance** |

`ownArchetype` / `oppArchetype` / `roundIndex` are #34's, unchanged.

The hash is not belt-and-braces. §6 established that the conformance table cannot cover the
clamp at all, and §5 that four of six archetypes never reach an overflow rank with the
fifteen. A future implementation could diverge on exactly those and still reproduce all 90
cells perfectly. FNV-1a costs ~16 bytes a battle and converts a silent divergence into a loud
one. Stance is included because §1.4 makes stance part of a deployment.

Coordinates themselves are written into the **promoted aggregate** only for battles a finding
actually cites — exactly when someone would want to eyeball a layout artefact — rather than
for all 24,300 up front.

### Substitution never invokes this rule

§33.3's marginal-inclusion gate is a **coordinate-level edit**, and §1.7 of the #18 write-up
stands unchanged: the substitute stands exactly where the replaced squad stood in all six
archetypes, neighbours shift along the rank by half the frontage difference, and the rank
and role position never change.

Now that the runner *can* generate, the temptation is to feed a swap back through the rule.
§4 supplies the argument §33.3 did not have: substitution draws from unit types the build's
affinity already grants, and §4's two collision groups **are** the plausible swap pairs —
`Lifewarden ↔ SpearGuard ↔ BannerGuard`, `EmberMage ↔ Frostcaller`. Under regeneration those
swaps change nothing but the name tiebreak, reordering the rank and moving squads that had
nothing to do with the substitution. The gate would read a layout shuffle as a unit's
marginal contribution — a confound manufactured entirely by our own tiebreak.

---

## 11. How this is checked

| Check | Runs |
| --- | --- |
| [`instruments/layout_regen_test.py`](layout_regen_test.py) | regenerates the 1,056 rows and diffs them byte for byte; asserts §33's stated shape, §6's invariant on every committed coordinate, and 90/90 legality |
| [`data/conformance_test.py`](../data/conformance_test.py) §9 | the build set is value-identical to the pre-port `FIELD`, and legal against the roster (§7) |
| `python3 docs/analysis/matchup-math/proto_archetypes.py freeze` | rewrites the table; **refuses to write** an infeasible one |

Both tests run in CI, per determinism-v1 §1: *a check is a runnable thing in the repo; CI is
only the place that runs it where nobody can skip it.*

When `runner/` lands, the Go generator becomes a second subject of the same regeneration
check. Nothing in this document changes when it does.

---

## 12. Findings

**F-1 — three of the fifteen builds are not affordable until R9, one round past §33.6's last
snapshot.** `MilDeepRally` (3,700g), `BeastDeepSing` (3,575g) and `MilDeepBodkin` (3,550g)
sit above §4.2's R8 cumulative of 3,500. The whole set is R4–R9: nothing is fieldable at R3
or R5 at all, the cheapest being `CommonHeavy` at R4. This is consistent rather than broken —
§29 derives its round-indexed builds by rolling the policy forward, so R3 and R5 field
*partial* armies and the fifteen are terminal states — but it means **the frozen fifteen
cannot be the R3 or R5 column of §29's matrix**, and three of them cannot be the R8 column
either. Anything that reads the fifteen as "the builds §29 grades at R3/R5/R8" is wrong.
Now asserted per build by `conformance_test.py` §9.

**F-2 — the three "wide" builds are 5+5, not 3+3.** `roster19.py` documented them as
*"wide (3+3): tiers 0/2 of two branches"*, and #19's Q14 rests on *"tier-3 gates at Affinity
4, so a 3+3 hybrid never fields one."* Measured against §6.3, `MilMagic` invests 1,550
Military and 1,100 Magic — **Affinity 5 in both**, because affinity caps at 5 from 1,000 and
these are twelve-squad armies. Same for `MilBeast` and `MagicBeast`. The builds field tiers
0/2 by *authorial choice*, not because the ladder stops them: all three could field tier-3
units and a doctrine in either branch. Q14's argument is sound about a genuine 3+3 army and
does not describe these three. It sharpens #47's finding 4, which noted the six `*Deep`, the
three `Pure` and the two 12-stacks sit at Affinity 5 gating nothing — the *wide* builds do
too, and for them it is the more surprising half.

**F-3 — the conformance table covers more of the rule than #33 assumed, and less of the one
path that matters.** #33 §3 named three paths the fifteen never touch — the overflow rank,
the name tiebreak, `forward`'s 3.5m floor — as the argument for `deploymentHash`. Measured:
the overflow rank fires on **12 of 90** cells (nine `refused`, three `screened`), the name
tiebreak on **12 of 90**, and `forward` uses 3–6 ranks on every build, so its floor is
exercised throughout. The genuinely uncovered path is the one #33 introduced in the same
ticket: **the band clamp fires on 0 of 90**. The conclusion is unchanged and the argument is
stronger — the hash guards a path that is now provably untestable by the table — but the
three examples #33 gave for it were the wrong three.

**F-4 — `rows()`'s fit test charges a 1m separation for the last squad in a rank as well**,
so a rank is declared full one metre before it is. Unrecorded, arbitrary, and it changes
which squads land on which rank near the boundary. Preserved rather than fixed: correcting
it would move cells for no stated benefit, and #33 already ruled the v2 bump is paid for by
the comparator. Recorded in §5 so it is a decision rather than an accident.

**F-5 — `proto_archetypes.py freeze` exited 0 having done nothing**, because `cmd_freeze`
was never in the `__main__` dispatch — determinism-v1's F-1, routed here. Both halves fixed:
`freeze` is dispatched, and an unrecognised subcommand now exits **2** with a message on
stderr. It also now refuses to write an infeasible table rather than reporting a violation
count nobody reads.

**F-6 — the 1,050g figure in `roster19.py`'s deep-build comment is wrong.** A track climbed
to step 3 costs 150 + 200 + 250 = **600g**. Corrected in place; it is a comment in the
witness, and no measurement read it.

---

## 13. What this leaves open

- **Which archetype a rollout battle deploys** —
  [#50](https://github.com/marcneuwirth/warweave/issues/50). #39 has since ruled the rollout
  deploys **one archetype, mirrored, replicated across the six diagonal cells**, which this
  document's §2 mirror mapping serves directly.
- **The Go generator**, and the second subject of §11's regeneration check. Out of #49's
  scope by its own terms.
- **Footprint overlap at twelve wide squads on a 60m band** is sample-clean, not proven:
  36,000 random cells found none, but the sweep draws uniformly from fourteen unit types and
  does not deliberately construct the worst case. §7's declared outcome is what carries the
  residual risk.
