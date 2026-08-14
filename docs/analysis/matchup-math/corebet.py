"""Core-bet stress test (#14).

#8 measured the roster. This asks a different question: does the archetype field
have any non-transitive structure at all? "Counter now" presupposes that some
army beats the army beating you, so if the field is a total order the central
strategic product test (§31) fails regardless of how anything is priced.

Four experiments, in the order they were run:

  1. baseline      -- reproduce #8's 12-squad round robin, post-#10 targeting
  2. reprice       -- twelve continuous-stat levers, looking for a cycle
  3. counters      -- property-keyed conditionals at flip magnitude
  4. roles         -- role symmetry, then role monopoly, then the sweep

Run:  python3 corebet.py [baseline|reprice|counters|roles|sweep|all]
"""
import sys, copy, itertools

import mm
import sim2
from sim2 import Cont, run
from tech11 import FIELD, pick_target_v10

sim2.pick_target = pick_target_v10          # #10's Direwolves rewrite is canon
BASE = copy.deepcopy(mm.U)
ORIG_APPLY = sim2.apply_attack
ORIG_SPLASH = sim2.splash_models

# Two hardened rules are hooks rather than stats, so they are patched in:
#   brace  -- Military's line takes less from a Charging attacker (§14, widened)
#   fbrad  -- the Ember Mage fireball radius, whose catch is spacing-derived (#11)
CFG = {'brace': 0.0, 'fbrad': 2.5}


def _apply(c, i, tc, j, Y, am):
    if CFG['brace'] > 0 and tc.u.get('braces') and c.u.get('charging'):
        old = tc.u.get('front_phys_res', 0.0)
        tc.u['front_phys_res'] = CFG['brace']
        ORIG_APPLY(c, i, tc, j, Y, am)
        tc.u['front_phys_res'] = old
    else:
        ORIG_APPLY(c, i, tc, j, Y, am)


sim2.apply_attack = _apply
sim2.splash_models = lambda t, r: ORIG_SPLASH(t, CFG['fbrad'] if r == 2.5 else r)

CATS = ['PureMilitary', 'SpearGuard12', 'Direwolves12', 'MilitiaLongbow', 'MilSGLB',
        'SGLBFrost', 'Hunters12', 'Militia12', 'BeastTroll', 'PureMagic', 'CommonHeavy',
        'MilBeast', 'Mil533', 'PureBeast', 'MagicBeast', 'MagicScreen']


def build(spec):
    return [Cont(n, k) for n, k in spec]


def reset(patch=None, brace=0.0, fbrad=2.5):
    for k, v in BASE.items():
        mm.U[k] = dict(v)
    for name in [n for n in mm.U if n not in BASE]:
        del mm.U[name]
    for u, ov in (patch or {}).items():
        mm.U.setdefault(u, {}).update(ov)
    CFG['brace'], CFG['fbrad'] = brace, fbrad


def roundrobin(field, cats):
    """W-L for every archetype, plus the pairings that violate the ranking.

    `upsets` is the measurement that matters: a field with no upsets is a total
    order, and a total order has no counterplay to sell.
    """
    rec = {n: [0, 0, 0] for n in cats}
    res = {}
    for a, b in itertools.combinations(cats, 2):
        r = run(build(field[a]), build(field[b]))
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


def report(tag, field=None, cats=None, patch=None, brace=0.0, fbrad=2.5, verbose=False):
    reset(patch, brace, fbrad)
    field = field or FIELD
    cats = cats or CATS
    order, upsets, _ = roundrobin(field, cats)
    n = len(cats) * (len(cats) - 1) // 2
    print(f"--- {tag}   upsets={len(upsets)}/{n}")
    if verbose:
        for name, (w, l, d) in order:
            gold = sum(mm.U[u]['cost'] * k for u, k in field[name])
            print(f"      {name:16s} {gold:5d}g  {w}-{l}" + (f"-{d}d" if d else ""))
    else:
        print("      " + " | ".join(f"{nm}:{w}-{l}" for nm, (w, l, _) in order))
    return order, upsets


# ---------------------------------------------------------------------------
# 1. baseline
# ---------------------------------------------------------------------------
def exp_baseline():
    print("\n### 1. Baseline — #8's field at the squad cap\n")
    report("baseline", verbose=True)


# ---------------------------------------------------------------------------
# 2. can any continuous-stat lever bend the ladder into a loop?
# ---------------------------------------------------------------------------
REPRICINGS = [
    ("Militia hp 100->75",            {'Militia': {'hp': 75}}),
    ("Militia cost 100->150",         {'Militia': {'cost': 150}}),
    ("Troll 105/2.0s -> 65/1.2s",     {'Troll': {'cd': 1.2, 'dmg': 65}}),
    ("Ember 95->130, Frost 45->75",   {'EmberMage': {'dmg': 130}, 'Frostcaller': {'dmg': 75}}),
    ("Ember n1->2 (hp 360->180)",     {'EmberMage': {'n': 2, 'hp': 180, 'front': 2}}),
    ("Longbowmen 25m->18m",           {'Longbowmen': {'rng': 18.0}}),
    ("Longbowmen 25m->16m",           {'Longbowmen': {'rng': 16.0}}),
    ("SpearGuard hp 210->160",        {'SpearGuard': {'hp': 160}}),
]


def exp_reprice():
    print("\n### 2. Repricing — twelve levers, no cycle\n")
    for tag, patch in REPRICINGS:
        report(tag, patch=patch)


# ---------------------------------------------------------------------------
# 3. property-keyed conditional counters at flip magnitude
# ---------------------------------------------------------------------------
CASTERS = {'EmberMage': {'n': 3, 'hp': 150, 'front': 3},
           'Frostcaller': {'n': 3, 'hp': 160, 'front': 3}}
# Military holds the only tight formation; everyone else loosens, so AoE catch
# (pi*r^2/sp^2, #11) becomes a property-keyed counter rather than a flat tax.
LOOSE = {'Direwolves': {'sp': 3.0, 'charging': True},
         'Troll': {'sp': 3.0, 'charging': True, 'spd': 5.5},
         'Militia': {'sp': 2.5}, 'Hunters': {'sp': 2.5}, 'Outriders': {'sp': 3.0}}
BRACES = {'SpearGuard': {'braces': True}, 'Longbowmen': {'braces': True}}


def exp_counters():
    print("\n### 3. Conditional counters — loosens the ladder, never moves the top\n")
    report("casters n3 only", patch=CASTERS)
    report("+ Military-only tight spacing", patch={**CASTERS, **LOOSE})
    report("+ Brace 40% vs Charging, fireball 3.5m",
           patch={**CASTERS, **LOOSE, **BRACES}, brace=0.40, fbrad=3.5)
    report("+ Brace 60% vs Charging, fireball 4.5m",
           patch={**CASTERS, **LOOSE, **BRACES}, brace=0.60, fbrad=4.5)


# ---------------------------------------------------------------------------
# 4. role symmetry, then role monopoly
# ---------------------------------------------------------------------------
# §1 grants "combined arms" to Military alone, and the roster takes it literally:
# Military fields a line and artillery, Magic is all backline, Beast all melee.
# ROLES gives Magic a holding unit and Beast a reach unit; MONOPOLY additionally
# moves the longest range off Military and onto Magic.
WARDENS = dict(cost=200, n=6, hp=185, ar=15, dmg=40, cd=1.5, rng=2.2, typ='magic',
               spd=4.0, rad=0.4, front=6, ranks=1, sp=2.0, heavy=False,
               branch='Magic', large=False)

ROLES = {**CASTERS, **LOOSE, **BRACES,
         'Wardens': WARDENS,
         'Troll': {**LOOSE['Troll'], 'rng': 13.0, 'dmg': 90, 'cd': 2.4, 'spd': 4.5}}

MONOPOLY = {**ROLES,
            'Longbowmen': {'rng': 18.0, 'braces': True},
            'EmberMage': {**CASTERS['EmberMage'], 'rng': 25.0},
            'Frostcaller': {**CASTERS['Frostcaller'], 'rng': 26.0},
            'Troll': {**LOOSE['Troll'], 'spd': 4.5}}

ROLE_FIELD = {
    'PureMilitary':   [('SpearGuard', 6), ('Longbowmen', 6)],
    'PureMagic':      [('Wardens', 6), ('EmberMage', 3), ('Frostcaller', 3)],
    'PureBeast':      [('Direwolves', 8), ('Troll', 4)],
    'MilMagic':       [('SpearGuard', 4), ('Longbowmen', 2), ('EmberMage', 3), ('Frostcaller', 3)],
    'MilBeast':       [('SpearGuard', 4), ('Longbowmen', 4), ('Direwolves', 4)],
    'MagicBeast':     [('Wardens', 3), ('EmberMage', 3), ('Frostcaller', 2), ('Direwolves', 4)],
    'CommonHeavy':    [('Militia', 6), ('Hunters', 4), ('Outriders', 2)],
    'SpearGuard12':   [('SpearGuard', 12)],
    'Direwolves12':   [('Direwolves', 12)],
    'Militia12':      [('Militia', 12)],
    'MilitiaLongbow': [('Militia', 6), ('Longbowmen', 6)],
    'Mil533':         [('SpearGuard', 3), ('Longbowmen', 3), ('Frostcaller', 3), ('Direwolves', 3)],
}


def exp_roles():
    print("\n### 4. Roles — symmetry revives Magic, monopoly moves the top\n")
    report("role symmetry only (Military keeps 25m)",
           field=ROLE_FIELD, cats=list(ROLE_FIELD), patch=ROLES, brace=0.60, fbrad=2.5,
           verbose=True)
    report("+ monopoly broken (Magic takes longest range)",
           field=ROLE_FIELD, cats=list(ROLE_FIELD), patch=MONOPOLY, brace=0.60, fbrad=2.5,
           verbose=True)


# ---------------------------------------------------------------------------
# 5. does the third edge ever close?
# ---------------------------------------------------------------------------
TRI = {'Mil': [('SpearGuard', 6), ('Longbowmen', 6)],
       'Mag': [('Wardens', 6), ('EmberMage', 3), ('Frostcaller', 3)],
       'Bst': [('Direwolves', 8), ('Troll', 4)]}


def exp_sweep():
    """Beast's edge over Magic is target access, which is 2-D. The calculator
    resolves a single 1-D gap, so no setting of speed, splash or Brace can
    express it -- the edge is not paper-gradeable, and goes to the runner."""
    print("\n### 5. Sweep — the Beast>Magic edge never closes\n")
    print(f"{'fbrad':>6}{'wolfspd':>9}{'brace':>7}   Mag-v-Mil  Bst-v-Mag  Mil-v-Bst  CYCLE?")
    for fbrad in (2.0, 2.5, 3.0, 3.5):
        for spd in (7.5, 8.5, 9.5):
            for brace in (0.30, 0.60):
                reset(MONOPOLY, brace, fbrad)
                mm.U['Direwolves']['spd'] = spd

                def duel(a, b):
                    r = run(build(TRI[a]), build(TRI[b]))
                    return a if r['win'] == 'A' else (b if r['win'] == 'B' else 'tie')

                x, y, z = duel('Mag', 'Mil'), duel('Bst', 'Mag'), duel('Mil', 'Bst')
                cycle = (x, y, z) == ('Mag', 'Bst', 'Mil')
                print(f"{fbrad:6.1f}{spd:9.1f}{brace:7.2f}   {x:9s}  {y:9s}  {z:9s}  "
                      + ("*** YES" if cycle else ""))


EXPERIMENTS = {'baseline': exp_baseline, 'reprice': exp_reprice, 'counters': exp_counters,
               'roles': exp_roles, 'sweep': exp_sweep}

if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'all'
    for name, fn in EXPERIMENTS.items():
        if which in ('all', name):
            fn()
