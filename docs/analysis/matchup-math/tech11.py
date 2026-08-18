"""Tech audit re-derivation at the squad cap (#11).

sim2.py measured technologies in single-squad equal-gold fights. #4 fixed the
cap at own-12 = field-12, and #8 (F9) showed the value ordering inverts across
it. Technologies cost no slot, so they are cap relief: this re-runs every
technology inside 12-squad armies against the §3.2/§3.3 field.

Also carries #10's Direwolves targeting rewrite (cull lowest-current-HP in
reach, else track lowest-total-HP squad), which postdates sim2.py and is what
Pack Hunter's trigger now depends on.
"""
import math, itertools, sys
from mm import U
import sim2
from sim2 import Cont, Side, run

# ---- #10: Direwolves targeting rewrite (squad-level: lowest total HP) -------
def pick_target_v10(side, attacker):
    live = [c for c in side.c if c.alive() > 0]
    if not live:
        return None
    if attacker.name == 'Direwolves':
        return min(live, key=lambda c: c.tot())
    return live[0]

# ---- the §3.2 / §3.3 field, all at 12 squads -------------------------------
FIELD = {
    'PureMilitary':   [('SpearGuard', 6), ('Longbowmen', 6)],
    'SpearGuard12':   [('SpearGuard', 12)],
    'Direwolves12':   [('Direwolves', 12)],
    'MilitiaLongbow': [('Militia', 6), ('Longbowmen', 6)],
    'MilSGLB':        [('Militia', 4), ('SpearGuard', 4), ('Longbowmen', 4)],
    'SGLBFrost':      [('SpearGuard', 4), ('Longbowmen', 4), ('Frostcaller', 4)],
    'Hunters12':      [('Hunters', 12)],
    'Militia12':      [('Militia', 12)],
    'BeastTroll':     [('Direwolves', 6), ('Troll', 6)],
    'PureMagic':      [('EmberMage', 6), ('Frostcaller', 6)],
    'CommonHeavy':    [('Militia', 6), ('Hunters', 4), ('Outriders', 2)],
    'MilBeast':       [('SpearGuard', 4), ('Longbowmen', 4), ('Direwolves', 4)],
    'Mil533':         [('SpearGuard', 3), ('Longbowmen', 3), ('Frostcaller', 3), ('Direwolves', 3)],
    'PureBeast':      [('Direwolves', 8), ('Troll', 4)],
    'MagicBeast':     [('Direwolves', 6), ('EmberMage', 3), ('Frostcaller', 3)],
    'MagicScreen':    [('Militia', 6), ('EmberMage', 3), ('Frostcaller', 3)],
    'Outriders12':    [('Outriders', 12)],
    'Troll12':        [('Troll', 12)],
}

TECHS = {
    'Militia':     ['Conscription', 'PitchTorch'],
    'Hunters':     ['LooseFormation', 'RapidFire'],
    'Outriders':   ['JavelinVolley', 'FlankingManeuver'],
    'SpearGuard':  ['Phalanx', 'HookedSpears'],
    'Longbowmen':  ['BodkinArrows', 'VolleyFire'],
    'EmberMage':   ['Firestorm', 'FocusedFlame'],
    'Frostcaller': ['DeepFreeze', 'FrostArmor'],
    'Direwolves':  ['PackHunter', 'Pounce'],
    'Troll':       ['Stonehide', 'BoulderThrow'],
}


def build(spec, tech_for=None, tech=None):
    return [Cont(n, k, tech if (tech_for == n) else None) for n, k in spec]


def score(spec, tech_for=None, tech=None, opponents=None):
    """W-L of this army against the field (excluding mirrors)."""
    w = l = d = 0
    detail = []
    for oname in (opponents or FIELD):
        if FIELD[oname] == spec:
            continue
        r = run(build(spec, tech_for, tech), build(FIELD[oname]))
        if r['win'] == 'A':
            w += 1
        elif r['win'] == 'B':
            l += 1
        else:
            d += 1
        detail.append((oname, r['win'], r['t'], r['a_hp']))
    return w, l, d, detail


# armies used to evaluate each unit's technologies: one where the unit is the
# whole army, one where it is a component of a strong build.
HOSTS = {
    'Militia':     ['Militia12', 'MilitiaLongbow'],
    'Hunters':     ['Hunters12', 'CommonHeavy'],
    'Outriders':   ['Outriders12', 'CommonHeavy'],
    'SpearGuard':  ['SpearGuard12', 'PureMilitary'],
    'Longbowmen':  ['PureMilitary', 'MilitiaLongbow'],
    'EmberMage':   ['PureMagic', 'MagicScreen'],
    'Frostcaller': ['PureMagic', 'SGLBFrost'],
    'Direwolves':  ['Direwolves12', 'MilBeast'],
    'Troll':       ['BeastTroll', 'PureBeast'],
}


def main():
    """An unrecognised argument exits non-zero (determinism-v1 F-1, #49)."""
    unknown = [a for a in sys.argv[1:] if a != '--v10']
    if unknown:
        print('unknown argument %r; this script takes --v10 or nothing'
              % unknown[0], file=sys.stderr)
        return 2
    if '--v10' in sys.argv:
        sim2.pick_target = pick_target_v10
        print("### Direwolves targeting: #10 rewrite (lowest-total-HP squad)\n")
    else:
        print("### Direwolves targeting: pre-#10 (backline preference)\n")

    for unit, techs in TECHS.items():
        print(f"\n===== {unit} " + "=" * 50)
        for host in HOSTS[unit]:
            spec = FIELD[host]
            base = score(spec)
            print(f"  host {host:16s} baseline {base[0]}-{base[1]}"
                  + (f"-{base[2]}d" if base[2] else ""))
            for t in techs:
                s = score(spec, unit, t)
                flips = [(o, wv) for (o, wv, _, _), (o2, wv2, _, _)
                         in zip(s[3], base[3]) if wv != wv2]
                mark = "  <== FLIPS: " + ", ".join(f"{o}->{wv}" for o, wv in flips) if flips else ""
                print(f"      {t:16s} {s[0]}-{s[1]}"
                      + (f"-{s[2]}d" if s[2] else "") + mark)
    return 0


if __name__ == '__main__':
    sys.exit(main())
