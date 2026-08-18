"""Role-symmetric roster (#19).

#14 ruled the archetype field is a total order and that the fix is structural:
roles set the cycle's direction, property-keyed conditionals give each edge its
magnitude. It deliberately did not author either. This does.

The grilling session settled eight things, all of which are inputs here:

  Q6   rotation A -- each branch's *adequate* role is the role of the branch it
                     beats, so every branch has a hole and the hole names its
                     counter:  Magic > Military (reach)
                               Military > Beast (hold)
                               Beast > Magic  (access)
  Q3/4 a tier-3 row at Affinity 4, two units per branch, 14 units total
  Q5/9 two forked 3-step upgrade tracks per tier-3 unit, single effect at three
       magnitudes, crossing #10's ~+40% flip threshold only at step 3
  Q7   three counters, keyed on functional properties, living at step 3:
         formation coherence -> AoE catch (pi*r^2/sp^2), Magic's edge
         closing speed       -> Brace vs Charging,       Military's edge
         model scarcity      -> +40% vs squads of <=3,   Beast's edge
  Q10  role rungs differ by 25-40% on their role's quantity
  Q12  branch price axis at tier-2/tier-3 only (gateways stay 200g)
  Q13  Common is the R1-R4 army: wins at the early-round budget, loses at cap
  Q14  tier-3 gates at Affinity 4, so a 3+3 hybrid never fields one

Run:  python3 roster19.py [rungs|common|field|cats|all]
"""
import sys, os, copy, itertools, math

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', '..', '..', 'data'))
import builds as buildsdata
import roster as rosterdata

import mm
import sim2
from sim2 import Cont, run

BASE_APPLY = sim2.apply_attack
BASE_SPLASH = sim2.splash_models

# ---------------------------------------------------------------------------
# The roster
# ---------------------------------------------------------------------------
# role      : which of hold / reach / access this unit serves
# rung      : best | adequate | weak | capstone | none (Common owns no role)
# tier      : affinity gate (0, 2, 4)
# charging  : enters the Charging state to reach contact -- Military's counter
#             keys on this, so it is a property of *access*, not of Beast
# The stat blocks are no longer authored here. They live in the versioned
# artifact `data/roster-v1.json`, hand-authored from the spec, which the Go
# runner reads with `encoding/json` and this control arm reads through
# `data/roster.py` (#26). Written once, so the two arms cannot diverge.
U19 = rosterdata.roster()

# ---------------------------------------------------------------------------
# Tier-3 upgrade tracks -- two per unit, three steps, pick one and climb it
# ---------------------------------------------------------------------------
# Step 3 of one track per branch carries that branch's counter (Q9).
# Costs 150 / 200 / 250; only the first step counts toward branchInvestment (Q11).
# Both now come from `data/roster-v1.json`, same as the stat blocks.
STEP_COST = rosterdata.TRACK_STEP_COSTS

TRACKS = rosterdata.mm_tracks()


def track_over(unit, track, step):
    """Cumulative override dict for climbing `track` on `unit` to `step` (1-3)."""
    over = {}
    for s in TRACKS[unit][track][:step]:
        over.update(s)
    if 'ar_add' in over:
        over['ar'] = U19[unit]['ar'] + over.pop('ar_add')
    return over


def track_cost(step):
    return sum(STEP_COST[:step])


# ---------------------------------------------------------------------------
# The three counters (Q7) -- all DamageModifier on a predicate, so §25 stands
# ---------------------------------------------------------------------------
def _apply(c, i, tc, j, Y, am):
    u, tgt = c.u, tc.u
    bonus = 0.0
    restore = {}

    # Beast's edge: model scarcity. Keys on the target squad's model count,
    # never on `branch` -- so it also fires into the Troll and into Magic mirrors.
    if u.get('scarce') and tgt['n'] <= 3:
        bonus += u['scarce']

    # Military's edge: Brace against Charging. Keys on the attacker's state.
    if u.get('charging'):
        brace = max((d.u.get('aura_brace', 0.0) for d in Y.c if d.alive() > 0), default=0.0)
        if brace:
            restore['front_phys_res'] = tgt.get('front_phys_res', 0.0)
            tgt['front_phys_res'] = brace

    if bonus:
        restore.setdefault('dmg', u['dmg'])
        u['dmg'] = u['dmg'] * (1.0 + bonus)

    BASE_APPLY(c, i, tc, j, Y, am)

    for k, v in restore.items():
        (u if k == 'dmg' else tgt)[k] = v

    # Magic's edge: formation coherence. Catch is pi*r^2/sp^2, so it lands on
    # tight formations and thins out against loose ones -- #11's ruling.
    r = u.get('aoe_r')
    if r and tgt['n'] > 1:
        raw = u['dmg'] * (1.0 + bonus) * 0.5
        for k2 in [k for k, h in enumerate(tc.models) if h > 0 and k != j][:BASE_SPLASH(tgt, r)]:
            tc.models[k2] -= mm.final_dmg(raw, tgt, u['typ'])


sim2.apply_attack = _apply


def pick_target(side, attacker):
    """#10's culling rewrite, generalised: access-role units track the squad with
    the lowest total HP. #10 authored it for Direwolves as a special case; under
    the role scheme it is what *access* means, so it follows the role."""
    live = [c for c in side.c if c.alive() > 0]
    if not live:
        return None
    if attacker.u.get('role') == 'access':
        return min(live, key=lambda c: c.tot())
    return live[0]


sim2.pick_target = pick_target


def install():
    mm.U.clear()
    mm.U.update(copy.deepcopy(U19))


def C(name, k=1, track=None, step=0):
    over = track_over(name, track, step) if track and step else None
    c = Cont(name, k, None, over)
    if track and step:
        c.cost += track_cost(step)
        c.gold = c.cost
    return c


# ---------------------------------------------------------------------------
# 1. role rungs -- the Q10 guard rail, 25-40% per rung
# ---------------------------------------------------------------------------
def hold_q(u):
    """eHP x frontage. Holding is denying passage, so frontage is load-bearing:
    this is what rules out a single-model holding unit."""
    return u['n'] * u['hp'] / mm.armor_mult(u['ar'], 'phys') * mm.frontage(u)


def reach_q(u):
    """range x applied dps -- damage delivered across #3's 32m closing window."""
    return u['rng'] * u['n'] * u['dmg'] / u['cd']


BYPASS = {'Direwolves': 0.60, 'Knights': 0.50, 'Stormcaller': 0.55, 'Griffin': 0.90}


def access_q(u, name):
    """speed x screen-bypass. Not paper-gradeable (#14) -- reported, not graded."""
    return u['spd'] * BYPASS.get(name, 0.30)


QUANT = {'hold': lambda n, u: hold_q(u), 'reach': lambda n, u: reach_q(u),
         'access': lambda n, u: access_q(u, n)}
ORDER = ['capstone', 'best', 'adequate', 'weak']


def exp_rungs():
    print("\n### 1. Role rungs — the 25–40% guard rail\n")
    for role in ('hold', 'reach', 'access'):
        members = [(n, u) for n, u in U19.items() if u['role'] == role]
        members.sort(key=lambda kv: ORDER.index(kv[1]['rung']))
        print(f"  {role.upper()}   (quantity: "
              f"{'eHP x frontage' if role=='hold' else 'range x dps' if role=='reach' else 'speed x bypass'})")
        prev = None
        for n, u in members:
            q = QUANT[role](n, u)
            delta = f"{(q/prev-1)*100:+6.1f}%" if prev else "      —"
            ok = ""
            if prev and u['rung'] != 'best':
                drop = 1 - q / prev
                ok = "  OK" if 0.25 <= drop <= 0.40 else "  ** OUT OF BAND **"
            print(f"    {u['rung']:9s} {n:12s} {u['branch']:9s} {q:10.0f} {delta}{ok}")
            if u['rung'] != 'capstone':
                prev = q
        print()


# ---------------------------------------------------------------------------
# 2. the Common invariant (Q13) -- army-level, per #8's two-regime finding
# ---------------------------------------------------------------------------
EARLY = 700     # R2 cumulative income (#4)


def squads_for(name, budget):
    return max(1, int(budget // U19[name]['cost']))


def exp_common():
    print("\n### 2. Common invariant — the R1–R4 army\n")
    print(f"  (a) at the early budget ({EARLY}g, R2) Common should WIN")
    for opp in ('SpearGuard', 'EmberMage', 'Direwolves', 'Knights', 'Lifewarden', 'Troll'):
        for cm in ('Militia', 'Hunters'):
            r = run([C(cm, squads_for(cm, EARLY))], [C(opp, squads_for(opp, EARLY))])
            w = 'WIN ' if r['win'] == 'A' else ('LOSS' if r['win'] == 'B' else 'draw')
            flag = '' if w == 'WIN ' else '   <-- violates'
            print(f"      {cm:8s} x{squads_for(cm,EARLY)} vs {opp:12s} x{squads_for(opp,EARLY)}  {w}{flag}")
    print(f"\n  (b) at the squad cap (12 squads) Common should LOSE")
    for opp in ('PureMilitary', 'PureMagic', 'PureBeast'):
        r = run(build(FIELD['CommonHeavy']), build(FIELD[opp]))
        w = 'LOSS' if r['win'] == 'B' else ('WIN' if r['win'] == 'A' else 'draw')
        flag = '' if w == 'LOSS' else '   <-- violates'
        print(f"      CommonHeavy vs {opp:14s} {w}{flag}")


# ---------------------------------------------------------------------------
# 3. the archetype field
# ---------------------------------------------------------------------------
# Deep builds (Affinity 5) field tier-3 units and one fully-climbed track, so
# they own one counter and one hole. Wide builds (3+3) field tiers 0/2 of two
# branches: they cover every role and flip nothing. Q9's open question is
# whether coverage beats variance.
# The fifteen are no longer authored here. They are a versioned artifact,
# `data/builds.json`, hand-authored from the spec and read by both arms (#49).
# They lived inside this file until #33's F-4: §33 calls the build set part of
# the measurement artifact, but it was only expressible inside the 1-D witness
# that §33.9 disqualifies as an oracle. `conformance_test.py` §9 proves the
# port did not move a value.
FIELD = buildsdata.field()

CATS = list(FIELD)


def build(spec):
    return [C(*s) for s in spec]


def gold_of(spec):
    return sum(C(*s).cost for s in spec)


def roundrobin(cats):
    rec = {n: [0, 0, 0] for n in cats}
    res = {}
    for a, b in itertools.combinations(cats, 2):
        r = run(build(FIELD[a]), build(FIELD[b]))
        res[(a, b)] = r['win']
        if r['win'] == 'A':
            rec[a][0] += 1; rec[b][1] += 1
        elif r['win'] == 'B':
            rec[b][0] += 1; rec[a][1] += 1
        else:
            rec[a][2] += 1; rec[b][2] += 1
    order = sorted(rec.items(), key=lambda kv: -kv[1][0])
    rank = {n: i for i, (n, _) in enumerate(order)}
    upsets = [(a, b) for (a, b), w in res.items()
              if (w == 'A' and rank[a] > rank[b]) or (w == 'B' and rank[b] > rank[a])]
    return order, upsets, res


def exp_field():
    print("\n### 3. The archetype field\n")
    order, upsets, res = roundrobin(CATS)
    n = len(CATS) * (len(CATS) - 1) // 2
    for name, (w, l, d) in order:
        print(f"    {name:14s} {gold_of(FIELD[name]):5d}g  {w:2d}-{l:<2d}" + (f" {d}d" if d else ""))
    print(f"\n    upsets = {len(upsets)}/{n}")
    for a, b in upsets:
        print(f"      {a} vs {b} -> {'A' if res[(a,b)]=='A' else 'B'} wins")
    return order, upsets, res


def exp_cycle(res=None):
    """Do the three intended edges resolve in the intended direction?"""
    print("\n### 4. The intended cycle\n")
    pairs = [('MagDeepChain', 'MilDeepRally', 'Magic > Military  (reach into Military\'s hole)'),
             ('MilDeepRally', 'BeastDeepSing', 'Military > Beast  (hold into Beast\'s hole)'),
             ('BeastDeepSing', 'MagDeepChain', 'Beast > Magic     (access into Magic\'s hole)')]
    for a, b, label in pairs:
        r = run(build(FIELD[a]), build(FIELD[b]))
        got = 'YES' if r['win'] == 'A' else ('no' if r['win'] == 'B' else 'draw')
        print(f"    {label:52s} {got:5s}  t={r['t']:5.1f}s  {a}@{r['a_hp']}%  {b}@{r['b_hp']}%")


# ---------------------------------------------------------------------------
# 5. §29's seven categories
# ---------------------------------------------------------------------------
CATEGORY = {
    'Common-heavy':   ['CommonHeavy'],
    'Pure Military':  ['PureMilitary', 'MilDeepRally', 'MilDeepBodkin', 'SpearGuard12'],
    'Pure Magic':     ['PureMagic', 'MagDeepChain', 'MagDeepFrost'],
    'Pure Beast':     ['PureBeast', 'BeastDeepSing', 'BeastDeepStone', 'Direwolves12'],
    'Military/Magic': ['MilMagic'],
    'Military/Beast': ['MilBeast'],
    'Magic/Beast':    ['MagicBeast'],
}


def exp_cats():
    """§29: every category must field at least one build capable of winning.

    #13 replaced the pass/fail with a two-sided 35-65% band, two-sided because
    #8's violation was a *top* failure that nothing in the spec prohibited.
    Each category is represented by its best-performing build (#13 derives these
    from the purchase policy; that artifact is #18's, so best-of stands in).
    """
    print("\n### 5. §29 — the seven categories\n")
    order, _, _ = roundrobin(CATS)
    rec = dict(order)
    best = {c: max(bs, key=lambda b: rec[b][0]) for c, bs in CATEGORY.items()}
    names = list(CATEGORY)
    wins = {c: 0 for c in names}
    played = {c: 0 for c in names}
    for a, b in itertools.combinations(names, 2):
        r = run(build(FIELD[best[a]]), build(FIELD[best[b]]))
        played[a] += 1; played[b] += 1
        if r['win'] == 'A': wins[a] += 1
        elif r['win'] == 'B': wins[b] += 1
    print(f"    {'category':16s} {'representative':16s} {'W-L':>6s}  {'rate':>6s}  band")
    for c in sorted(names, key=lambda c: -wins[c]):
        rate = wins[c] / played[c]
        band = 'OK' if 0.35 <= rate <= 0.65 else ('** TOP FAILURE **' if rate > 0.65 else '** BOTTOM FAILURE **')
        print(f"    {c:16s} {best[c]:16s} {wins[c]}-{played[c]-wins[c]:<4d} {rate:5.0%}  {band}")


COMMANDS = ('rungs', 'common', 'field', 'cycle', 'cats', 'all')


def main(argv=None):
    """An unrecognised subcommand exits non-zero (determinism-v1 F-1, #49)."""
    argv = sys.argv if argv is None else argv
    what = argv[1] if len(argv) > 1 else 'all'
    if what not in COMMANDS:
        print('unknown subcommand %r; expected one of %s'
              % (what, ', '.join(COMMANDS)), file=sys.stderr)
        return 2
    install()
    if what in ('rungs', 'all'):  exp_rungs()
    if what in ('common', 'all'): exp_common()
    if what in ('field', 'all'):  exp_field()
    if what in ('cycle', 'all'):  exp_cycle()
    if what in ('cats', 'all'):   exp_cats()
    return 0


if __name__ == '__main__':
    sys.exit(main())
