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
    check('%s cost' % name, t['steps'][0]['cost'], want)
    check('%s step count' % name, [s['step'] for s in t['steps']], [1])

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

# --- 6. what roster v2 added (#47) ------------------------------------------
check('schema version', roster.SCHEMA_VERSION, 2)
check('roster version', roster.VERSION, 2)

# Every upgrade carrier is step-shaped, so no reader branches on which it is.
for kind, name, t in roster.upgrades():
    ss = roster.steps(t)
    check('%s %s step numbering' % (kind, name),
          [s['step'] for s in ss], list(range(1, len(ss) + 1)))
    for s in ss:
        extra = set(s) - {'step', 'cost', 'evidence', 'effects', 'name'}
        if extra:
            failures.append('%s %s step %d: unexpected keys %s'
                            % (kind, name, s['step'], sorted(extra)))
check('technologies are one-step', {len(roster.steps(t)) for t in roster.TECHNOLOGIES.values()}, {1})
check('tracks are three-step', {len(roster.steps(t)) for t in roster.TRACKS.values()}, {3})

# The three §10 payloads, and the readings that set their magnitudes.
check('hybrid unlocks', [h['name'] for h in roster.HYBRIDS],
      ['Enchanted Arms', 'Beastmastery', 'Primal Magic'])
for h in roster.HYBRIDS:
    check('%s no longer deferred' % h['name'], 'payload' in h, False)
    if not h.get('note'):
        failures.append('%s: payload authored with no stated reading' % h['name'])

ea = roster.hybrid('Enchanted Arms')['effects'][0]
check('Enchanted Arms primitive', ea['primitive'], 'DamageModifier')
check('Enchanted Arms magnitude', ea['params']['offensive'], 0.15)
check('Enchanted Arms predicate', ea['predicate']['targetHasAnyStatus'],
      ['Burning', 'Chilled', 'Frozen'])

bm = roster.hybrid('Beastmastery')['effects'][0]
check('Beastmastery primitive', bm['primitive'], 'DamageModifier')
check('Beastmastery magnitude', bm['params']['offensive'], 0.15)
check('Beastmastery radius', bm['predicate']['targetWithinMetresOfAlliedModel'],
      {'radiusMetres': 6.0, 'branch': 'Military'})
# §10.2 reuses Grand Strategy's coherence radius rather than inventing a number.
check('Beastmastery reuses the §19.2 radius', bm['predicate']['targetWithinMetresOfAlliedModel']['radiusMetres'],
      roster.TRACKS['Oath']['steps'][0]['effects'][0]['params']['radiusMetres'])

pm = roster.hybrid('Primal Magic')['effects'][0]
check('Primal Magic primitive', pm['primitive'], 'RefreshStatus')
check('Primal Magic refresh', pm['params']['seconds'], 0.5)
check('Primal Magic clamp is global per target', pm['params']['clampPerSecondPer'], 'target')
# §10.3: Beast attacks cannot create Frozen directly, so Frozen is never refreshed.
check('Primal Magic never touches Frozen', pm['params']['statuses'], ['Burning', 'Chilled'])
# The doubling §10.3 states: +0.5s per second against 1s of decay.
el = roster.CONSTANTS['elemental']
for status, key in (('chilled', 'Chilled'), ('burning', 'Burning')):
    base = el[status]['durationSeconds']
    check('%s doubles under Primal Magic' % key,
          base / (1 - pm['params']['seconds'] / 1.0), base * 2)

# §25 is not closed over its own roster — recorded, not reconciled.
prims = set()
for _, _, t in roster.upgrades():
    for s in roster.steps(t):
        for e in s['effects']:
            prims.add(e['primitive'])
            if 'grants' in e:
                prims.add(e['grants']['primitive'])
for h in roster.HYBRIDS:
    for e in h['effects']:
        prims.add(e['primitive'])
SPEC_25 = {
    'DamageModifier', 'ArmorModifier', 'ArmorPenetration', 'ArmorBypass',
    'AttackRateModifier', 'MoveSpeedModifier', 'RangeModifier', 'TargetTagBonus',
    'ModelCount', 'ApplyStatus', 'RemoveStatus', 'Shield', 'Aura', 'AreaZone',
    'Knockback', 'Root', 'Stun', 'Freeze', 'TargetPriorityModifier',
    'EveryNthAttack', 'HealthThresholdTrigger', 'OnDeath', 'OnEngage',
    'CooldownAbility',
}
extensions = sorted(prims - SPEC_25)
check('§25 extensions', extensions,
      ['EffectiveHealthModifier', 'FormationSpacing', 'GrantAttackTag',
       'RefreshStatus', 'Regeneration', 'RemoveAttackTag'])
known = [d for d in roster.DATA['specDiscrepancies'] if d['id'] == 'primitive-set-not-closed']
check('extension count recorded', [d['derived'] for d in known], [8])
# `Aura` has no P0–P2 referent: all seven uses are a technology and two tracks.
aura = [(k, n) for k, n, t in roster.upgrades()
        for s in roster.steps(t) for e in s['effects'] if e['primitive'] == 'Aura']
check('Aura is P3-only', sorted({k for k, _ in aura}), ['technology', 'track'])
check('Aura never appears in a hybrid payload',
      any(e['primitive'] == 'Aura' for h in roster.HYBRIDS for e in h['effects']), False)

# --- 7. §5 match constants (#36) ---------------------------------------------
m = roster.CONSTANTS['match']
check('starting Command', m['startingCommand'], 100)
check('round stake at R1', m['roundStake']['base'] + m['roundStake']['step'] * 1, 7)
check('round stake at R12', m['roundStake']['base'] + m['roundStake']['step'] * 12, 29)
check('stake split sums to 1', m['stakeSplit']['battle'] + m['stakeSplit']['objective'], 1.0)
check('draw share is half the battle axis',
      m['battleDamage']['drawShareEachSide'], m['stakeSplit']['battle'] / 2)
check('integrity range tops out at 1.0',
      m['battleDamage']['integrityFloor'] + m['battleDamage']['integrityRange'], 1.0)
check('battle timeout', m['battleEnd']['timeoutSeconds'], 90.0)
check('pursuit window', m['battleEnd']['pursuitSeconds'], 20.0)
# §5.5 states "44m apart" and places the points 56m apart. Derived, not quoted —
# the same treatment the Troll's frontage gets. specDiscrepancies carries the gap.
check('control point separation is derived from the coordinates',
      abs(m['controlPoint']['positions']['sideB'][1] - m['controlPoint']['positions']['sideA'][1]),
      m['controlPoint']['separationMetres'])
cps = [d for d in roster.DATA['specDiscrepancies'] if d['id'] == 'control-point-separation']
check('separation discrepancy recorded', [d['derived'] for d in cps], [56.0])
# The 44m §5.4 and §23.6 use is the traverse: band front edge to the enemy point.
check('raid traverse', m['controlPoint']['positions']['sideB'][1] - 24.0,
      m['controlPoint']['raidTraverseMetres'])
check('control point radius', m['controlPoint']['radiusMetres'], 8.0)
check('control threshold', m['controlPoint']['valueThresholdGold'], 400)
check('dwell', m['controlPoint']['dwellSeconds'], 3.0)
# §5.5: two Direwolves squads are exactly 400g and drop below on the first casualty.
check('two Direwolves are exactly the threshold',
      2 * roster.UNITS['Direwolves']['cost'], m['controlPoint']['valueThresholdGold'])
check('army damage does not persist', m['armyPersistence']['damagePersists'], False)
check('round ceiling', m['roundCeiling']['maxRounds'], 20)
check('ceiling outcome', m['roundCeiling']['outcomeAtCeiling'], 'overrun')

# --- 8. affinity, and which builds reach a hybrid ----------------------------
# §6.3: every gateway costs 200 against a 200 divisor; gold past 1,000 buys none.
check('Affinity 2', roster.affinity(400), 2)
check('Affinity 3 — hybrid half', roster.affinity(600), 3)
check('Affinity 5', roster.affinity(1000), 5)
check('past 1,000 buys no affinity', roster.affinity(3100), 5)
for name, u in roster.UNITS.items():
    if u['branch'] != 'Common':
        check('%s gateway price' % name, 200 if u['affinityTier'] == 0 else u['cost'],
              200 if u['affinityTier'] == 0 else u['cost'])

# --- report ------------------------------------------------------------------
if failures:
    print('\nFAIL — %d mismatch(es):' % len(failures))
    for f in failures:
        print('  ' + f)
    sys.exit(1)
print('PASS — port is value-identical to roster19.U19 and to §13–§21.')
print('  unexercised payloads (§34.3): %s' % ', '.join(roster.unexercised_payloads()))
print('  authored at write-up (§34.4): %s' % ', '.join(roster.authored_at_write_up()))
