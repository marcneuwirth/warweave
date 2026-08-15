# The two measurement artifacts (#18)

Resolves [#18](https://github.com/marcneuwirth/warweave/issues/18). Generator in
[`matchup-math/proto_archetypes.py`](matchup-math/proto_archetypes.py); the frozen table
is [`deployment-archetypes-v1.csv`](deployment-archetypes-v1.csv).

[#13](https://github.com/marcneuwirth/warweave/issues/13) declared two versioned artifacts
and fixed their shape, count and change-invalidation semantics, but not their contents.
Every balance number in WARWEAVE is measured relative to them. This document authors both.

---

## 1. The deployment archetype set

### 1.1 What the artifact is

**A coordinate table, not a rule.** Six archetypes × fifteen builds × up to twelve squads —
**1,056 rows**, each carrying an exact `x`, `y` and stance. The versioned artifact is the
table; nothing is computed at run time.

The role-keyed layout rule in `proto_archetypes.py` is a **generator, run once**. It exists
because 1,056 rows are not authorable by hand, and it is retained so the table can be
regenerated when the roster changes — but it is not the artifact, and the runner never
executes it. A generator bug and a balance fact are distinguishable precisely because the
output is frozen and inspectable.

The build set is therefore **part of the artifact**. A sixteenth build requires a version
bump, not a run.

### 1.2 The field

60m × 80m (§23). Each player deploys inside the nearest **24m** (#3 §1.7): own band
`y ∈ [0, 24]`, front edge `y = 24`, a **32m** gap to the enemy front edge. Own control
point at `(30, 12)` (#6). Placement is continuous, no grid snap; squad footprints may not
overlap.

**Frontage** = `(front − 1) × spacing + 2 × radius`, measured surface-to-surface per #3
§1.4. Spear Guard is 6 × 2.0m + 0.8m = **10.8m**.

### 1.3 The six

| Archetype | Shape | Stance |
| --- | --- | --- |
| **line** | One rank at `y = 22`, reach standing **in** the rank on both flanks | Hold; access Advance |
| **screened** | Same wall, reach withdrawn to `y = 6`/`y = 1` behind it | Hold; access Advance |
| **refused** | Right half at the edge, left half echeloned back to `y = 6` | Right Advance, left Hold, one **Raid** |
| **wings** | Two 24m blocks on the flanks, centre empty | Advance, one **Raid** |
| **column** | 24m centre lane, stacked eight ranks deep | Advance |
| **forward** | 30m centre lane jammed at the front edge, 3.5m rank pitch | Advance |

`line` and `screened` are **the same wall differing only in where reach stands**. That is
deliberate: #12 established that screening reverses both fast-attacker matchups but that
*placing* a screen is unmeasured, F16 being composition-confounded (#8 §5 swaps a squad
rather than moving one). The pair isolates screening as a single variable, so #12's P1
becomes a cell comparison rather than an experiment someone has to design.

`line` is the designated **poor positioning** row for §27's *"hard counter with poor
positioning should fall below 60%"* clause. It is poor for a stated reason — reach is in
the contact rank — rather than by decree.

### 1.4 Stance is part of a deployment

An archetype fixes stance per squad. #3 added Hold/Advance and #17 added `Raid`; a layout
without them is not a determined battle, since Hold-vs-Advance decides whether the armies
close at all. Six coordinate sets with a free stance variable would have left the sweep
undetermined.

**Raid appears in exactly two archetypes** (`refused`, `wings`) — the rearmost access
squad, or the fastest non-reach squad if the build owns no access unit. Raid-vs-no-raid is
therefore a comparison the sweep can read, not a global setting. Of 1,056 slots: 30 Raid,
315 Hold, 711 Advance.

### 1.5 Legality

**All 90 archetype × build cells are legal** — in band, on field, no overlapping
footprints. Three constraints were derived rather than picked while forcing this:

- **A deep column needs a 24m centre lane.** At 16–22m the twelve-squad builds run out of
  band depth (`MilDeepRally`, `MilMagic`, `MilBeast` bind first).
- **Rank pitch is bounded below by footprint depth.** `forward` cannot pack tighter than
  **3.5m** between ranks, because Direwolves are two ranks at 2.0m spacing plus radii =
  2.8m deep. Concentration has a floor set by the roster, not by taste.
- **A build with no non-reach squad still gets screened** — its frontmost reach squads take
  the screen slots. This is what makes the set legal for *every* build rather than only for
  builds that happen to own a screening unit, which was #18's open question.

### 1.6 Finding: the full-width wall does not exist

#12 made 60m load-bearing on the claim that **six Spear Guard span exactly 60m**, and
concluded that pure Military alone can wall the field, denying both the flank and the raid
lane — and therefore that **#8's 9–0 understates F2**.

That arithmetic is centre-to-centre. #3 §1.4 measures **surface-to-surface**, and #3 §1.7
forbids overlapping footprints, so the true squad pitch is **10.8m** and six Spear Guard
need **64.8m** on a 60m field. Five wall 54m and leave a **6m seam**.

The seam is not passable by a squad — the narrowest non-single-model formation is
Direwolves at 6.8m — but models carry individual collision (#3 §2.0), so it is passable
model by model. `SpearGuard12` and `PureMilitary` reach **90%** wall coverage; `MilMagic`
reaches **80%**.

**#12's conclusion does not follow from its own footprint rule.** Pure Military cannot deny
the raid lane by walling; it can only make walling expensive. Whether F2 is still
understated is now a sweep question rather than a paper one, and the `line`/`screened` pair
is the instrument for it.

### 1.7 Substitution

#13's marginal-inclusion gate replaces a unit "with the best legal substitute at equal
spend", which manufactures a build with no authored coordinates.

> **Substitution is a squad-for-squad swap at fixed coordinates.** The substitute stands
> exactly where the replaced squad stood, in all six archetypes. Where its frontage differs,
> neighbours shift along the rank by half the difference; the rank and the role position
> never change.

No coordinates are ever authored for a substituted build. The gate also gets sharper:
holding deployment fixed isolates the unit's contribution from a re-optimised layout, which
is what the gate claims to measure.

### 1.8 Six is the count

Six was #13's dial, chosen by argument. It survives, but for a reason #13 did not have: the
set now contains a **matched pair** (`line`/`screened`) that exists to isolate one variable.
Cutting to five means cutting the pair, and the pair is the only instrument for #12's P1.
The other four span width (`line`), asymmetry (`refused`), split (`wings`), depth
(`column`) and mass (`forward`) — with `wings` and `refused` also carrying the objective
axis.

---

## 2. The reference purchase policy

### 2.1 The procedure

Greedy marginal value against a fixed opponent panel. Each planning phase:

```
A  = every legal action: buy | sell (#4: 2/round at 50%) |
     doctrine choice or re-choice (#7: 500g, 3-round lockout)
plan = a multiset of actions affordable within the horizon
score(plan) = winrate(army + plan, panel) − winrate(army, panel)
              measured over the 6×6 archetype sweep
while max score > 0 and gold remains:
    apply argmax, recompute
```

The policy holds **no authored preferences**. Its blind spots are the *kernel's* rather
than an author's, which is the only honest answer to #13's warning that a policy's blind
spots become measured product facts. A hand-written build order would have had the author
doing all the work the category constraint was supposed to do — the same failure for which
#13 rejected a sane-only deployment sweep.

**The category constraint is a legality filter on `A`, and nothing more.** It restricts
which unit types may be bought; it never ranks them. This is what stops the constraint from
generating §29's representative builds by itself.

### 2.2 The horizon is two rounds, and it is derived

A single-purchase greedy policy is **structurally unable to buy a gateway**. A gateway
confers no combat power, so its marginal win rate is zero or negative — the policy would
never reach Affinity 2, and would generate no tier-2 or tier-3 build at all. Every §29
category above Common-heavy would be unreachable.

The unit of decision is therefore a **round plan**, scored over a **two-round gold horizon**.
Two rounds is not picked:

> The longest enabler-to-payoff distance in the price list is **Affinity 4 plus a tier-3
> unit** — four gateways at 200g (#19: gateways stay 200g on every branch) plus a 300–350g
> unit = **1,100–1,150g**. At #4's 550 plateau income that is **exactly two rounds**.

Any shorter horizon cannot see the deepest purchase the roster offers; any longer one is
buying lookahead the price list does not require.

### 2.3 What the policy does not observe

The policy is 1-ply against the opponent, so it cannot see #10's deep-vs-wide **timing**
claim — deep collecting at R3, wide's stacked hybrids landing by R7–8.

It does not need to. #13 already round-indexes the §29 category matrix at **R3/R5/R8**,
which is the instrument that separates *mispriced* from *not yet load-bearing*. The timing
axis is measured there; the policy is not asked to observe it.

### 2.4 Playing both sides

The same policy plays both sides of the choice-liveness rollout, **but each side is locked
to a heading** and all nine pairings are rolled:

|  | opp: counter | deepen | weave |
| --- | --- | --- | --- |
| **counter** | · | · | · |
| **deepen** | · | · | · |
| **weave** | · | · | · |

A heading's score is a **row of a payoff matrix**, not a scalar. This answers #18's
question directly: the same policy *can* honestly play both sides, provided the two sides
are not doing the same thing. Unconstrained self-play would have run the gate that catches
*"weave is never correct"* in the exact configuration where both players weave together and
it looks fine.

A round is **live** when the top two **row-maxima** fall within ε.

### 2.5 ε = 2 Command points, flat

Of the 100-point pool (§5), and roughly **10% of a mid-match round stake** — #6's
`S(r) = 5 + 2r` puts round 8 at 21. Small enough that a genuinely dominant heading never
ties; large enough that the gate is not measuring kernel rounding.

Flat rather than proportional, so it means the same thing at round 2 and round 11. A
proportional ε tightens as the match goes on, which would bias #13's *"≥3 live rounds, not
clustered"* clause toward early rounds by construction.

ε remains a **dial**, per #13's precedent of naming unprincipled constants rather than
inventing derivations for them. Unlike the two-round horizon above, no derivation is
available.

---

## 3. What this changes elsewhere

- **#12's §23 rewrite needs a correction.** The full-width wall is not expressible; the
  60m width stays load-bearing, but on a 6m seam rather than a perfect wall (§1.6).
- **#13's artifact count holds at two**, and both are now authored rather than named.
- **The archetype set is versioned with the roster.** #19's roster change would invalidate
  the table; the generator exists so that regeneration is mechanical.
