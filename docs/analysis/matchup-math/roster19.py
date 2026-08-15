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
import sys, copy, itertools, math

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
U19 = {
 # ---- Common: no role, no affinity, gold-efficient and slot-inefficient -----
 'Militia':    dict(cost=100, n=8, hp=100, ar=0,  dmg=30, cd=1.0,  rng=1.0,  typ='phys',  spd=4.5, rad=0.4, front=4, ranks=2, sp=2.0, heavy=False, branch='Common',   large=False, tier=0, role='none',   rung='none'),
 'Hunters':    dict(cost=150, n=5, hp=120, ar=0,  dmg=42, cd=1.6,  rng=12.0,  typ='phys',  spd=4.0, rad=0.4, front=5, ranks=1, sp=2.0, heavy=False, branch='Common',   large=False, tier=0, role='none',   rung='none'),

 # ---- Military: hold-best / access-adequate / reach is the hole -------------
 'SpearGuard': dict(cost=200, n=6, hp=210, ar=30, dmg=48, cd=1.5,  rng=2.2,  typ='phys',  spd=4.5, rad=0.4, front=6, ranks=1, sp=2.0, heavy=False, branch='Military', large=False, tier=0, role='hold',   rung='best'),
 'Knights':    dict(cost=275, n=4, hp=260, ar=30, dmg=62, cd=1.6,  rng=1.8,  typ='phys',  spd=6.5, rad=0.6, front=4, ranks=1, sp=2.5, heavy=False, branch='Military', large=False, tier=2, role='access', rung='adequate', charging=True),
 'Longbowmen': dict(cost=350, n=5, hp=195, ar=15, dmg=58, cd=2.4,  rng=14.0, typ='phys',  spd=4.0, rad=0.4, front=5, ranks=1, sp=2.0, heavy=True,  branch='Military', large=False, tier=4, role='reach',  rung='weak'),
 'BannerGuard':dict(cost=350, n=6, hp=300, ar=40, dmg=52, cd=1.5,  rng=2.2,  typ='phys',  spd=4.0, rad=0.4, front=6, ranks=1, sp=2.0, heavy=False, branch='Military', large=False, tier=4, role='hold',   rung='capstone'),

 # ---- Magic: reach-best / hold-adequate / access is the hole ----------------
 'EmberMage':  dict(cost=200, n=3, hp=150, ar=0,  dmg=95, cd=2.25, rng=26.0, typ='magic', spd=4.0, rad=0.4, front=3, ranks=1, sp=2.0, heavy=False, branch='Magic',    large=False, tier=0, role='reach',  rung='best'),
 'Lifewarden': dict(cost=250, n=6, hp=165, ar=20, dmg=38, cd=1.5,  rng=2.2,  typ='magic', spd=4.0, rad=0.4, front=6, ranks=1, sp=2.0, heavy=False, branch='Magic',    large=False, tier=2, role='hold',   rung='adequate'),
 'Stormcaller':dict(cost=325, n=3, hp=210, ar=0,  dmg=70, cd=2.0,  rng=15.0, typ='magic', spd=4.0, rad=0.4, front=3, ranks=1, sp=2.0, heavy=False, branch='Magic',    large=False, tier=4, role='access', rung='weak'),
 'Frostcaller':dict(cost=325, n=3, hp=160, ar=0,  dmg=115, cd=1.8,  rng=24.0, typ='magic', spd=4.0, rad=0.4, front=3, ranks=1, sp=2.0, heavy=False, branch='Magic',    large=False, tier=4, role='reach',  rung='capstone'),

 # ---- Beast: access-best / reach-adequate / hold is the hole ---------------
 'Direwolves': dict(cost=200, n=8, hp=125, ar=0,  dmg=34, cd=0.9,  rng=1.0,  typ='phys',  spd=7.5, rad=0.5, front=4, ranks=2, sp=2.0, heavy=False, branch='Beast',    large=False, tier=0, role='access', rung='best',     charging=True),
 'Troll':      dict(cost=225, n=2, hp=520, ar=25, dmg=120,cd=2.0,  rng=19.0, typ='phys',  spd=3.5, rad=1.2, front=2, ranks=1, sp=3.0, heavy=True,  branch='Beast',    large=True,  tier=2, role='reach',  rung='adequate', regen=25.0),
 'Stonebacks': dict(cost=300, n=4, hp=200, ar=20, dmg=55, cd=1.8,  rng=2.4,  typ='phys',  spd=4.0, rad=0.6, front=4, ranks=1, sp=2.5, heavy=False, branch='Beast',    large=False, tier=4, role='hold',   rung='weak'),
 'Griffin':    dict(cost=300, n=3, hp=300, ar=10, dmg=72, cd=1.4,  rng=1.6,  typ='phys',  spd=9.0, rad=0.6, front=3, ranks=1, sp=2.5, heavy=False, branch='Beast',    large=False, tier=4, role='access', rung='capstone', charging=True),
}

# ---------------------------------------------------------------------------
# Tier-3 upgrade tracks -- two per unit, three steps, pick one and climb it
# ---------------------------------------------------------------------------
# Step 3 of one track per branch carries that branch's counter (Q9).
# Costs 150 / 200 / 250; only the first step counts toward branchInvestment (Q11).
STEP_COST = (150, 200, 250)

TRACKS = {
 'Longbowmen':  {'Bodkin':   [{'pen': 20.0}, {'pen': 40.0}, {'pen': 60.0, 'heavy': False}],
                 'Volley':   [{'volley_r': 0.75}, {'volley_r': 1.10}, {'volley_r': 1.50}]},
 'BannerGuard': {'Rally':    [{'aura_ehp': 0.08}, {'aura_ehp': 0.15}, {'aura_brace': 0.40}],   # <- Military's counter
                 'Oath':     [{'aura_dmg': 0.08}, {'aura_dmg': 0.15}, {'aura_dmg': 0.25}]},
 'Stormcaller': {'ChainLightning': [{'aoe_r': 1.5}, {'aoe_r': 2.2}, {'aoe_r': 3.2}],           # <- Magic's counter
                 'Skyfall':  [{'skyfall': 0.15}, {'skyfall': 0.28}, {'skyfall': 0.45}]},
 'Frostcaller': {'DeepFreeze': [{'fz': 0.90}, {'fz': 1.05}, {'fz': 1.25}],
                 'FrostArmor': [{'shield': 60.0}, {'shield': 90.0}, {'shield': 120.0}]},
 'Stonebacks':  {'Stonehide': [{'ar_add': 15}, {'ar_add': 30}, {'ar_add': 45}],
                 'Bulwark':  [{'sp': 2.8}, {'sp': 3.1}, {'sp': 3.4, 'front_phys_res': 0.20}]},
 'Griffin':     {'Singling': [{'scarce': 0.15}, {'scarce': 0.25}, {'scarce': 0.40}],           # <- Beast's counter
                 'Talons':   [{'bypass': 0.20}, {'bypass': 0.35}, {'bypass': 0.50}]},
}


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
FIELD = {
    # --- deep (Affinity 5): tier-3 units + one track climbed to step 3 -------
    # Deep owns a counter and a hole, and pays 1,050g of track that buys no slot.
    'MilDeepRally':  [('SpearGuard', 4), ('Knights', 2), ('BannerGuard', 5, 'Rally', 3)],
    'MilDeepBodkin': [('SpearGuard', 5), ('Knights', 2), ('Longbowmen', 4, 'Bodkin', 3)],
    'MagDeepChain':  [('EmberMage', 4), ('Lifewarden', 3), ('Stormcaller', 4, 'ChainLightning', 3)],
    'MagDeepFrost':  [('EmberMage', 3), ('Lifewarden', 4), ('Frostcaller', 4, 'DeepFreeze', 3)],
    'BeastDeepSing': [('Direwolves', 4), ('Troll', 3), ('Griffin', 5, 'Singling', 3)],
    'BeastDeepStone':[('Direwolves', 5), ('Troll', 3), ('Stonebacks', 4, 'Stonehide', 3)],
    # --- wide (3+3): tiers 0/2 of two branches. Covers every role, flips none.
    'MilMagic':      [('SpearGuard', 5), ('Knights', 2), ('EmberMage', 3), ('Lifewarden', 2)],
    'MilBeast':      [('SpearGuard', 5), ('Knights', 2), ('Direwolves', 3), ('Troll', 2)],
    'MagicBeast':    [('EmberMage', 4), ('Lifewarden', 2), ('Direwolves', 4), ('Troll', 2)],
    # --- pure (Affinity 5, tier-3 skipped): fills all twelve slots -----------
    'PureMilitary':  [('SpearGuard', 8), ('Knights', 4)],
    'PureMagic':     [('EmberMage', 6), ('Lifewarden', 6)],
    'PureBeast':     [('Direwolves', 7), ('Troll', 5)],
    # --- controls ------------------------------------------------------------
    'SpearGuard12':  [('SpearGuard', 12)],
    'Direwolves12':  [('Direwolves', 12)],
    'CommonHeavy':   [('Militia', 8), ('Hunters', 4)],
}
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


def main():
    install()
    what = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if what in ('rungs', 'all'):  exp_rungs()
    if what in ('common', 'all'): exp_common()
    if what in ('field', 'all'):  exp_field()
    if what in ('cycle', 'all'):  exp_cycle()
    if what in ('cats', 'all'):   exp_cats()


if __name__ == '__main__':
    main()
