# `data/` — the roster artifact

Resolves [#26](https://github.com/marcneuwirth/warweave/issues/26).

**[`roster-v1.json`](roster-v1.json) is the single source for every unit stat, technology
payload, track step and balance constant in WARWEAVE.** It is hand-authored from
[`docs/spec/v0.4.md`](../docs/spec/v0.4.md) and it is **designed to outlive the throwaway
runner**: when a real engine is chosen it inherits this file unchanged.

| File | What it is |
| --- | --- |
| `roster-v1.json` | the artifact. Frozen, versioned, never generated at run time |
| `roster.py` | the Python reader, and the adapter into `matchup-math`'s short keys |
| `conformance_test.py` | proves the port is value-identical to what the paper calculator held |

The Go runner reads `roster-v1.json` with `encoding/json`. No third file, no second copy.

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

- **Match and objective constants** (§5 — round stake, battle damage, objective damage,
  battle end, pursuit, the control point) belong to
  [#36](https://github.com/marcneuwirth/warweave/issues/36). A `match` block is the
  intended home once that ticket fixes them.
- **Field and deployment coordinates** are the other versioned artifact,
  [`docs/analysis/deployment-archetypes-v1.csv`](../docs/analysis/deployment-archetypes-v1.csv).
- **Doctrine and hybrid-unlock payloads** (§9, §10) are P3 content, out of scope for this
  map. The affinity ladder names them and authors nothing.

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
`roster.unexercised_payloads()` prints it.

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

- The filename carries the version (`roster-v1.json`) and so does `rosterVersion` inside it.
- **Any change to a value the kernel reads bumps the version.** Editing a `note`, a
  `specSection` or a citation does not.
- Every recorded measurement names **`roster vN` alongside `archetypes vN`**. Neither
  number alone identifies a result.
- The runner also logs the file's **SHA-256** (`roster.CONTENT_SHA256`) into every result
  record, so a version bump somebody forgot is still detectable after the fact.

## 6. One spec discrepancy, recorded not fixed

§16 prints the Troll's frontage as **8.4m**. §13's own formula
`(frontRank − 1) × spacing + 2 × radius` gives **5.4m** on the Troll's stat line — 8.4m is
exactly a *three*-model Troll, stale from before ADR-0046 made it a two-model squad. The
frozen archetype table already lays Trolls out on 5.4m, so the prose is the outlier.

This file records the **inputs** and no derived frontage, and carries the mismatch under
`specDiscrepancies`. **No spec edit was made** — the runner grades v0.4 as written, and a
spec change is a finding to report, not an edit to make.
