# `data/` — the roster artifact

Resolves [#26](https://github.com/marcneuwirth/warweave/issues/26); cut to **v2** by
[#47](https://github.com/marcneuwirth/warweave/issues/47).

**[`roster-v2.json`](roster-v2.json) is the single source for every unit stat, technology
payload, track step and balance constant in WARWEAVE.** It is hand-authored from
[`docs/spec/v0.4.md`](../docs/spec/v0.4.md) and it is **designed to outlive the throwaway
runner**: when a real engine is chosen it inherits this file unchanged.

| File | What it is |
| --- | --- |
| `roster-v2.json` | the artifact. Frozen, versioned, never generated at run time |
| `roster-v1.json` | superseded, retained for provenance. **Nothing reads it** — `roster.py` is the only loader and it points at v2 |
| `roster.py` | the Python reader, and the adapter into `matchup-math`'s short keys |
| `conformance_test.py` | proves the port is value-identical to what the paper calculator held |

The Go runner reads `roster-v2.json` with `encoding/json`. No third file, no second copy.

---

## 1. Why JSON

The format has to be read by **Go** (the runner) and by **Python** (`matchup-math/`, the
1-D control arm), and it has to survive both.

| | Go stdlib | Python stdlib | Nesting | Comments |
| --- | --- | --- | --- | --- |
| **JSON** | ✅ `encoding/json` | ✅ `json` | ✅ | ✗ |
| TOML | ✗ third-party | ✅ `tomllib` (3.11+, read-only) | awkward for arrays of tables | ✅ |
| YAML | ✗ | ✗ | ✅ | ✅ |
| CSV | ✅ | ✅ | ✗ | ✗ |

CSV is what the deployment-archetype artifact uses and is right there — 1,056 flat
coordinate rows. It cannot express a track step's effect payload, so it is out here.

TOML's one advantage is comments, and that advantage is a trap: **provenance must not be a
comment.** The ⚠ flags of §18.1 and §34.4 are the most important thing in this file, and a
comment is invisible to every consumer. They are fields instead — at which point TOML costs
the Go side a dependency and buys nothing.

**JSON, hand-authored, no comments, provenance as data.**

## 2. Where the data/rules line falls

> **Data is a value a balance pass would change. A rule is the function that consumes it.**

In: unit stat blocks, the price list and income curve, the elemental constants of §11, the
damage-kernel constants of §22, the combat magnitudes of §23 (flanking, Charging, Brace),
the affinity ladder, every technology and track-step payload, the §27.3 magnitude ladder.

Out, living in code: the damage pipeline's order of operations, the frontage formula, the
AoE catch formula `πr²/sp²`, targeting and stickiness logic, stance semantics, the armour
curve's *shape*.

Payloads are encoded as **§25 effect primitives plus parameters** — `{primitive, params,
predicate}`. Effects that no primitive expresses (Brace, culling, Frostcaller's negative
targeting, Pounce's leap, Firestorm's every-fourth-cast) carry a **named behaviour key**
whose numbers are data and whose logic is code. The file does not pretend the kernel is
data-driven; it pretends nothing.

**Deliberately absent, and whose they are:**

- ~~**Match and objective constants**~~ — **landed at v2** as `constants.match`, per
  [#36](https://github.com/marcneuwirth/warweave/issues/36). It carries §5's round stake,
  battle-damage terms, battle-end and pursuit windows and the control point, **plus** two
  values #36 ruled rather than quoted: the full-HP-reset rule and the 20-round `overrun`
  ceiling. Both are values a balance pass would change, which is this section's own test.
- **Field and deployment coordinates** are the other versioned artifact,
  [`docs/analysis/deployment-archetypes-v1.csv`](../docs/analysis/deployment-archetypes-v1.csv).
- **§29's fifteen reference builds** are `data/builds.json` — located by
  [#47](https://github.com/marcneuwirth/warweave/issues/47), authored by
  [#49](https://github.com/marcneuwirth/warweave/issues/49). Deliberately **unversioned in
  the filename**, carrying an internal `layoutVersion`, because they are governed by the
  `layout` number: [#33](https://github.com/marcneuwirth/warweave/issues/33) §7
  version-locks the layout rule, the builds and the conformance table under one number,
  since the table is a pure function of the other two. They are *also* roster-coupled — all
  fifteen are 11–12 squads against a gold budget — and that coupling is caught by a
  **legality conformance test** rather than a version, which is why there is no fifth
  version number.
- **Doctrine payloads** (§9) are P3 content and stay out. **Hybrid-unlock payloads** (§10)
  came *in* at v2 — see §7 below.

## 3. Provenance — where the ⚠ flags live

Two orthogonal fields, because §34 records two different facts and conflating them loses one:

| Field | Meaning |
| --- | --- |
| `evidence: "measured"` | the payload was implemented in the paper calculator and live in the run that produced the archetype field |
| `evidence: "unexercised"` | authored in the spec, but inert or absent in that run — its magnitude follows the §27.3 ladder by construction, not by measurement (§34.3) |
| `authoredAtWriteUp: true` | the ⚠ flag of §18.1 / §34.4 — written during the spec write-up with no ticket behind it and no paper evidence at all |

Six technologies carry the ⚠: **Lance Charge, Barding** (Knights), **Warding Chant,
Thornmail** (Lifewarden), **Quarry Stones, Thick Hide** (Troll). §34.4 calls them the
weakest content in the spec and the first thing the runner should re-derive; carrying the
flag as a field is what lets the runner sort by it.

Thirty-four payloads are `unexercised`. That number is a finding in itself, and
`roster.unexercised_payloads()` prints it. The three hybrid unlocks authored at v2 carry
the same two fields and are `unexercised` / `authoredAtWriteUp: false`.

## 4. Authored from the spec, not generated from `roster19.py`

`roster19.py`'s `U19` dict was a **subset** — no turn rate, no projectile speed, no
technologies, no elemental constants — and it carried paper-calculator artifacts (the
`BYPASS` table, the `phys`/`magic` short names). Generating from it would have laundered
the spec through the calculator's abbreviations, which is the exact direction §33.9 warns
against.

So the spec is the source and this is the port. `roster19.py`'s `U19` and `TRACKS`
literals are **deleted**, replaced by `rosterdata.roster()` and `rosterdata.mm_tracks()`.
There is now one copy of every number.

`conformance_test.py` is what makes that safe:

```
python3 data/conformance_test.py
```

It asserts the loaded values equal, field by field, what `roster19.py` held before the
port; that every track step's payload survives the primitive encoding; that prices, counts
and the two-technologies-per-tier-0/2-unit structure match what §17 states; and that the
frontage formula reproduces every frontage the spec prints. **Running `roster19.py all`
before and after the port produces byte-identical output.**

## 5. Versioning

Versioned exactly like the deployment archetype set, and for the same reason: **a stat
change invalidates prior measurements.**

- The filename carries the version (`roster-v2.json`) and so does `rosterVersion` inside it.
- **Any change to a value the kernel reads bumps the version.** Editing a `note`, a
  `specSection` or a citation does not.
- Every recorded measurement names **`roster vN` alongside `archetypes vN`**. Neither
  number alone identifies a result.
- The runner also logs the file's **SHA-256** (`roster.CONTENT_SHA256`) into every result
  record, so a version bump somebody forgot is still detectable after the fact.
- **`schemaVersion` is a second, independent number.** It moves when the *shape* changes,
  not the values, and [#27](https://github.com/marcneuwirth/warweave/issues/27) makes a
  mismatch a hard load failure. v2 moved both: the values gained `constants.match` and the
  three hybrid payloads, and the shape gained the steps reshape below.

**No measurement was ever recorded against v1** — no kernel exists yet, so the bump
invalidates nothing. That will not be true of the next one.

## 6. Spec discrepancies, recorded not fixed

Three, each carried as a field under `specDiscrepancies` and none repaired — the runner
grades v0.4 as written, and a spec change is a finding to report, not an edit to make.

### `troll-frontage`

§16 prints the Troll's frontage as **8.4m**. §13's own formula
`(frontRank − 1) × spacing + 2 × radius` gives **5.4m** on the Troll's stat line — 8.4m is
exactly a *three*-model Troll, stale from before ADR-0046 made it a two-model squad. The
frozen archetype table already lays Trolls out on 5.4m, so the prose is the outlier.

This file records the **inputs** and no derived frontage.

### `control-point-separation`

Found at v2. §5.5 places the two control points at **(30, 12)** and **(30, 68)** and calls
them **"44m apart"**. They are **56m** apart. The coordinates are self-consistent — each
sits at the centre of its own 24m-deep band on the 80m field — so only the stated
separation is wrong.

44m is a real distance in this spec, just a different one: the **band front edge** (y = 24)
to the **enemy** point (y = 68). That is the figure §5.4 uses (*"the enemy must march 44m
to dig them out"*) and §23.6 uses (*"raiders cross ~44m eating fire they never answer"*) —
both about travel from the line, not the gap between points. §5.5 borrowed the traverse and
labelled it a separation.

Decision-relevant rather than cosmetic: a kernel placing the points 44m apart would put
them inside the bands' own gap and shorten every pursuit walk in §5.4. Both numbers are
carried — `separationMetres` **56.0**, derived from the coordinates, and
`raidTraverseMetres` **44.0**.

### `primitive-set-not-closed`

Found at v2. §25 says its primitive set is closed but for *"two extensions and one
carve-out, each recorded rather than waved through"*. The roster uses **eight** primitives
§25 does not name: five were already in v1 (`FormationSpacing`, `GrantAttackTag`,
`RemoveAttackTag`, `Regeneration`, `EffectiveHealthModifier` — found by
[#44](https://github.com/marcneuwirth/warweave/issues/44)) and v2 adds `RefreshStatus`.
§25's set is not closed over its own roster. `conformance_test.py` asserts the exact
extension list, so a ninth cannot arrive unnoticed.

## 7. What changed at v2

Cut by [#47](https://github.com/marcneuwirth/warweave/issues/47). Four changes, and a
**value-drift check proves the first is pure**: normalising v1's technologies into the new
shape and deep-comparing the two files reports changes in exactly the intended places and
nowhere else. `roster19.py all` is **byte-identical** before and after
(`6a325b84be3e…`), which is the same net #26's port used.

### The 16 technologies became one-step tracks

```
before   {unitType, cost, specSection, evidence, authoredAtWriteUp, effects}
after    {unitType, specSection, steps: [{step: 1, cost, evidence, effects}], authoredAtWriteUp}
```

Technologies and tracks now have an **identical value shape**, so a reader never branches
on which of the two it holds — `roster.steps(entry)` works on both, and `roster.upgrades()`
walks them together. A technology is simply a track that has not been given a step 2 yet,
and **giving it one is now a data edit rather than a schema change**. Done now because
nothing reads the roster yet, and the invalidation never gets cheaper.

They stay **two top-level keys** rather than merging under a `kind` discriminator. The
split is not cosmetic: §34.4's six ⚠ technologies and §34.3's seven unproven track payloads
are two sets [#38](https://github.com/marcneuwirth/warweave/issues/38)'s handoff inherits
separately, so merging would make every such read filter to recover a split the data
already had for free.

### The three §10 hybrid unlocks gained payloads

They stay **flat `effects`, not `steps`** — the honest discriminator is *purchased* (steps)
versus *gated* (flat). §10 says hybrids "activate automatically… never purchased", so they
have no cost, and §6.3's ladder gates at 0/2/4/5 with hybrids at 3+3: there is no affinity
3.5, so a step 2 is **unreachable by construction**. A `steps` array there would encode an
extensibility the ladder cannot express.

| Unlock | Encoding |
| --- | --- |
| **Enchanted Arms** | `DamageModifier{offensive: 0.15}` on Military-branch squads, predicate *target has Burning, Chilled or Frozen* |
| **Beastmastery** | `DamageModifier{offensive: 0.15}` on Beast-branch squads, predicate *target within 6m of an allied Military model* |
| **Primal Magic** | `RefreshStatus{statuses: [Burning, Chilled], seconds: 0.5, clampPerSecondPer: "target"}` on Beast-branch squads |

Each entry's `note` carries the reading it was authored under, in
[#30](https://github.com/marcneuwirth/warweave/issues/30)'s shape, so a failing test is
adjudicated against the reading before the kernel is blamed. The load-bearing ones: the
6m is measured **model to model** (a squad centre covers barely half of a 10.8m Spear Guard
line); Primal Magic's clamp is **global per target** (both per-attacker readings hold a
status indefinitely and contradict §10.3's own "it always runs out"); and a refresh is a
**deadline extension, never an application**, because application is what §11.2 turns into
Frozen and §10.3 forbids Beast attacks from creating it.

`RefreshStatus` is a new §25 primitive, and the honest answer to §25's challenge — *can
this be expressed through existing primitives?* — is **no**. `ApplyStatus` is excluded by
the line above, so reusing it would mean a mode flag that switches off the primitive's
defining behaviour. Recorded as `specDiscrepancies["primitive-set-not-closed"]`: §25 claims
two extensions, the roster now has **eight**.

### `constants.match` landed, and `notCarriedHere` shrank

See §2. `notCarriedHere.p3Payloads` is **amended, not deleted** — deleting it would erase
the record that hybrid payloads were once out of scope and why.
