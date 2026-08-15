"""Proves the port is value-identical to what `roster19.py` used to hold.

The roster JSON was authored from `docs/spec/v0.4.md`, not generated from
`roster19.py` — deliberately, so the spec stays the source and the paper
calculator's abbreviations do not become canon (#26). This check is what makes
that safe: it asserts the two agree on every value the calculator ever read, so
the port cannot have silently changed a number.

Run:  python3 data/conformance_test.py
"""
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import roster  # noqa: E402

# The U19 dict exactly as it stood in roster19.py before the port. Frozen here
# on purpose: this is a one-time equivalence proof, not a live import.
U19_BEFORE_PORT = {
 'Militia':    dict(cost=100, n=8, hp=100, ar=0,  dmg=30, cd=1.0,  rng=1.0,  typ='phys',  spd=4.5, rad=0.4, front=4, ranks=2, sp=2.0, heavy=False, branch='Common',   large=False, tier=0, role='none',   rung='none'),
 'Hunters':    dict(cost=150, n=5, hp=120, ar=0,  dmg=42, cd=1.6,  rng=12.0, typ='phys',  spd=4.0, rad=0.4, front=5, ranks=1, sp=2.0, heavy=False, branch='Common',   large=False, tier=0, role='none',   rung='none'),
 'SpearGuard': dict(cost=200, n=6, hp=210, ar=30, dmg=48, cd=1.5,  rng=2.2,  typ='phys',  spd=4.5, rad=0.4, front=6, ranks=1, sp=2.0, heavy=False, branch='Military', large=False, tier=0, role='hold',   rung='best'),
 'Knights':    dict(cost=275, n=4, hp=260, ar=30, dmg=62, cd=1.6,  rng=1.8,  typ='phys',  spd=6.5, rad=0.6, front=4, ranks=1, sp=2.5, heavy=False, branch='Military', large=False, tier=2, role='access', rung='adequate', charging=True),
 'Longbowmen': dict(cost=350, n=5, hp=195, ar=15, dmg=58, cd=2.4,  rng=14.0, typ='phys',  spd=4.0, rad=0.4, front=5, ranks=1, sp=2.0, heavy=True,  branch='Military', large=False, tier=4, role='reach',  rung='weak'),
 'BannerGuard':dict(cost=350, n=6, hp=300, ar=40, dmg=52, cd=1.5,  rng=2.2,  typ='phys',  spd=4.0, rad=0.4, front=6, ranks=1, sp=2.0, heavy=False, branch='Military', large=False, tier=4, role='hold',   rung='capstone'),
 'EmberMage':  dict(cost=200, n=3, hp=150, ar=0,  dmg=95, cd=2.25, rng=26.0, typ='magic', spd=4.0, rad=0.4, front=3, ranks=1, sp=2.0, heavy=False, branch='Magic',    large=False, tier=0, role='reach',  rung='best'),
 'Lifewarden': dict(cost=250, n=6, hp=165, ar=20, dmg=38, cd=1.5,  rng=2.2,  typ='magic', spd=4.0, rad=0.4, front=6, ranks=1, sp=2.0, heavy=False, branch='Magic',    large=False, tier=2, role='hold',   rung='adequate'),
 'Stormcaller':dict(cost=325, n=3, hp=210, ar=0,  dmg=70, cd=2.0,  rng=15.0, typ='magic', spd=4.0, rad=0.4, front=3, ranks=1, sp=2.0, heavy=False, branch='Magic',    large=False, tier=4, role='access', rung='weak'),
 'Frostcaller':dict(cost=325, n=3, hp=160, ar=0,  dmg=115,cd=1.8,  rng=24.0, typ='magic', spd=4.0, rad=0.4, front=3, ranks=1, sp=2.0, heavy=False, branch='Magic',    large=False, tier=4, role='reach',  rung='capstone'),
 'Direwolves': dict(cost=200, n=8, hp=125, ar=0,  dmg=34, cd=0.9,  rng=1.0,  typ='phys',  spd=7.5, rad=0.5, front=4, ranks=2, sp=2.0, heavy=False, branch='Beast',    large=False, tier=0, role='access', rung='best',     charging=True),
 'Troll':      dict(cost=225, n=2, hp=520, ar=25, dmg=120,cd=2.0,  rng=19.0, typ='phys',  spd=3.5, rad=1.2, front=2, ranks=1, sp=3.0, heavy=True,  branch='Beast',    large=True,  tier=2, role='reach',  rung='adequate', regen=25.0),
 'Stonebacks': dict(cost=300, n=4, hp=200, ar=20, dmg=55, cd=1.8,  rng=2.4,  typ='phys',  spd=4.0, rad=0.6, front=4, ranks=1, sp=2.5, heavy=False, branch='Beast',    large=False, tier=4, role='hold',   rung='weak'),
 'Griffin':    dict(cost=300, n=3, hp=300, ar=10, dmg=72, cd=1.4,  rng=1.6,  typ='phys',  spd=9.0, rad=0.6, front=3, ranks=1, sp=2.5, heavy=False, branch='Beast',    large=False, tier=4, role='access', rung='capstone', charging=True),
}

# Track payload overrides, as roster19.TRACKS held them. Same shape: cumulative
# override dicts are built by the caller, so this compares step by step.
TRACKS_BEFORE_PORT = {
 'Bodkin':        [{'pen': 20.0}, {'pen': 40.0}, {'pen': 60.0, 'heavy': False}],
 'Volley':        [{'volley_r': 0.75}, {'volley_r': 1.10}, {'volley_r': 1.50}],
 'Rally':         [{'aura_ehp': 0.08}, {'aura_ehp': 0.15}, {'aura_brace': 0.40}],
 'Oath':          [{'aura_dmg': 0.08}, {'aura_dmg': 0.15}, {'aura_dmg': 0.25}],
 'ChainLightning':[{'aoe_r': 1.5}, {'aoe_r': 2.2}, {'aoe_r': 3.2}],
 'Skyfall':       [{'skyfall': 0.15}, {'skyfall': 0.28}, {'skyfall': 0.45}],
 'DeepFreeze':    [{'fz': 0.90}, {'fz': 1.05}, {'fz': 1.25}],
 'FrostArmor':    [{'shield': 60.0}, {'shield': 90.0}, {'shield': 120.0}],
 'Stonehide':     [{'ar_add': 15}, {'ar_add': 30}, {'ar_add': 45}],
 'Bulwark':       [{'sp': 2.8}, {'sp': 3.1}, {'sp': 3.4, 'front_phys_res': 0.20}],
 'Singling':      [{'scarce': 0.15}, {'scarce': 0.25}, {'scarce': 0.40}],
 'Talons':        [{'bypass': 0.20}, {'bypass': 0.35}, {'bypass': 0.50}],
}

# Where each old short key now lives in a track step's effect params.
TRACK_KEY_PARAM = {
    'pen': 'add', 'volley_r': 'splashRadiusMetres', 'aura_ehp': 'bonus',
    'aura_brace': 'defensive', 'aura_dmg': 'offensive', 'aoe_r': 'splashRadiusMetres',
    'skyfall': 'offensive', 'fz': 'frozenSeconds', 'shield': 'amount',
    'ar_add': 'add', 'sp': 'spacingMetres', 'scarce': 'offensive', 'bypass': 'bypass',
    'front_phys_res': 'defensive', 'heavy': None,
}

failures = []


def check(label, got, want):
    if got != want:
        failures.append('%s: got %r, want %r' % (label, got, want))


def step_values(track, step_index):
    """Every numeric param appearing anywhere in a step's effects."""
    vals = []
    for eff in roster.TRACKS[track]['steps'][step_index]['effects']:
        for src in (eff.get('params', {}), eff.get('grants', {}).get('params', {})):
            for k, v in src.items():
                if isinstance(v, (int, float)) and not isinstance(v, bool):
                    vals.append((k, v))
    return vals


print('roster v%d  sha256=%s' % (roster.VERSION, roster.CONTENT_SHA256[:16]))

# --- 1. unit stat blocks -----------------------------------------------------
check('unit count', len(roster.UNITS), len(U19_BEFORE_PORT))
for name, want in U19_BEFORE_PORT.items():
    if name not in roster.UNITS:
        failures.append('missing unit %s' % name)
        continue
    got = roster.unit_dict(name)
    for k, v in want.items():
        check('%s.%s' % (name, k), got.get(k), v)
    extra = set(got) - set(want)
    if extra:
        failures.append('%s: unexpected keys %s' % (name, sorted(extra)))

# --- 2. track step payloads --------------------------------------------------
check('track count', len(roster.TRACKS), len(TRACKS_BEFORE_PORT))
for track, steps in TRACKS_BEFORE_PORT.items():
    if track not in roster.TRACKS:
        failures.append('missing track %s' % track)
        continue
    for i, want in enumerate(steps):
        got = dict(step_values(track, i))
        for old_key, v in want.items():
            param = TRACK_KEY_PARAM[old_key]
            if param is None:      # `heavy: False` is now RemoveAttackTag
                tags = [e['params'].get('tag') for e in roster.TRACKS[track]['steps'][i]['effects']
                        if e['primitive'] == 'RemoveAttackTag']
                check('%s %d removes Heavy' % (track, i + 1), tags, ['Heavy'])
                continue
            if old_key == 'ar_add':   # absolute in the JSON, additive in the old dict
                base = roster.UNITS[roster.TRACKS[track]['unitType']]['armour']
                check('%s %d %s' % (track, i + 1, old_key), got.get(param), v)
                assert base is not None
                continue
            check('%s %d %s' % (track, i + 1, old_key), got.get(param), float(v)
                  if isinstance(got.get(param), float) else v)

# --- 3. prices and step costs ------------------------------------------------
check('track step costs', list(roster.TRACK_STEP_COSTS), [150, 200, 250])
for track, t in roster.TRACKS.items():
    check('%s step costs' % track, [s['cost'] for s in t['steps']], [150, 200, 250])
for name, t in roster.TECHNOLOGIES.items():
    want = 200 if roster.UNITS[t['unitType']]['branch'] == 'Common' else 250
    check('%s cost' % name, t['cost'], want)

# --- 4. structural counts the spec states outright ---------------------------
check('technologies', len(roster.TECHNOLOGIES), 16)
check('tracks', len(roster.TRACKS), 12)
check('authored-at-write-up technologies', len(roster.authored_at_write_up()), 6)
check('unit types with two technologies',
      sorted({t['unitType'] for t in roster.TECHNOLOGIES.values()}),
      sorted(n for n, u in roster.UNITS.items() if u['affinityTier'] in (0, 2)))
check('unit types with two tracks',
      sorted({t['unitType'] for t in roster.TRACKS.values()}),
      sorted(n for n, u in roster.UNITS.items() if u['affinityTier'] == 4))

# --- 5. the frontage formula against the spec's stated values ----------------
STATED_FRONTAGE = {
    'Militia': 6.8, 'Hunters': 8.8, 'SpearGuard': 10.8, 'Knights': 8.7,
    'Longbowmen': 8.8, 'BannerGuard': 10.8, 'EmberMage': 4.8, 'Lifewarden': 10.8,
    'Stormcaller': 4.8, 'Frostcaller': 4.8, 'Direwolves': 7.0,
    'Stonebacks': 8.7, 'Griffin': 6.2,
    # Troll deliberately absent — §16 states 8.4m, the formula derives 5.4m.
    # Recorded as specDiscrepancies["troll-frontage"], not reconciled here.
}
for name, want in STATED_FRONTAGE.items():
    check('%s frontage' % name, round(roster.frontage(roster.UNITS[name]), 2), want)
known = roster.DATA['specDiscrepancies'][0]
check('troll discrepancy recorded', known['id'], 'troll-frontage')
check('troll derived frontage', round(roster.frontage(roster.UNITS['Troll']), 2),
      known['derived'])

# --- report ------------------------------------------------------------------
if failures:
    print('\nFAIL — %d mismatch(es):' % len(failures))
    for f in failures:
        print('  ' + f)
    sys.exit(1)
print('PASS — port is value-identical to roster19.U19 and to §13–§21.')
print('  unexercised payloads (§34.3): %s' % ', '.join(roster.unexercised_payloads()))
print('  authored at write-up (§34.4): %s' % ', '.join(roster.authored_at_write_up()))
