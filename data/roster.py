"""Loader for the versioned roster artifact.

`roster-v1.json` is the single source for every unit stat, technology payload,
track step and balance constant in WARWEAVE. It is hand-authored from
`docs/spec/v0.4.md` and it outlives the throwaway runner (#26).

This module is the *Python* reader. The Go runner reads the same file with
`encoding/json`; neither side owns the values.

`unit_dict()` adapts a stat block into the short-key shape `matchup-math/mm.py`
expects, so the 1-D control arm and the 2-D runner cannot drift apart.
"""
import hashlib
import json
import os

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'roster-v1.json')

with open(PATH, 'rb') as _f:
    _RAW = _f.read()

DATA = json.loads(_RAW.decode('utf-8'))

#: SHA-256 of the artifact as loaded. Every recorded measurement names this
#: alongside `rosterVersion`, so a forgotten version bump is still detectable.
CONTENT_SHA256 = hashlib.sha256(_RAW).hexdigest()

VERSION = DATA['rosterVersion']
UNITS = DATA['unitTypes']
TECHNOLOGIES = DATA['technologies']
TRACKS = DATA['tracks']
CONSTANTS = DATA['constants']

TRACK_STEP_COSTS = tuple(CONSTANTS['economy']['prices']['trackStepCosts'])


def frontage(unit):
    """(front rank - 1) * spacing + 2 * collision radius. §13.

    The formula is a rule and lives in code; only its inputs are data.
    """
    f = unit['formation']
    return (f['frontRank'] - 1) * f['spacingMetres'] + 2 * f['collisionRadiusMetres']


def unit_dict(name):
    """A `mm.U`-shaped dict for one unit type — the control arm's short keys."""
    u = UNITS[name]
    f, a, m = u['formation'], u['attack'], u['movement']
    d = dict(
        cost=u['cost'],
        n=f['models'],
        hp=u['hpPerModel'],
        ar=u['armour'],
        dmg=a['damage'],
        cd=a['cooldownSeconds'],
        rng=a.get('rangeMetres', a.get('reachMetres')),
        typ='magic' if a['damageType'] == 'magic' else 'phys',
        spd=m['speedMetresPerSecond'],
        rad=f['collisionRadiusMetres'],
        front=f['frontRank'],
        ranks=f['ranks'],
        sp=f['spacingMetres'],
        heavy='Heavy' in a['tags'],
        branch=u['branch'],
        large='Large' in u['tags'],
        tier=u['affinityTier'],
        role=u['role'] or 'none',
        rung=u['rung'] or 'none',
    )
    if 'Charging' in u['tags']:
        d['charging'] = True
    if u['regenerationPerSecond']:
        d['regen'] = u['regenerationPerSecond']
    return d


def roster():
    """Every unit type, in file order, in `mm.U` shape."""
    return {name: unit_dict(name) for name in UNITS}


def track_cost(step):
    return sum(TRACK_STEP_COSTS[:step])


# The paper calculator names each track payload with a short key of its own.
# Those keys are the calculator's, not canon, so the translation lives here
# rather than in the artifact: (JSON primitive, param) -> mm short key.
_MM_TRACK_KEYS = {
    'Bodkin':         [('ArmorPenetration', 'add', 'pen')],
    'Volley':         [('AreaZone', 'splashRadiusMetres', 'volley_r')],
    'Rally':          [('Aura', 'bonus', 'aura_ehp'), ('Aura', 'defensive', 'aura_brace')],
    'Oath':           [('Aura', 'offensive', 'aura_dmg')],
    'ChainLightning': [('AreaZone', 'splashRadiusMetres', 'aoe_r')],
    'Skyfall':        [('DamageModifier', 'offensive', 'skyfall')],
    'DeepFreeze':     [('Freeze', 'frozenSeconds', 'fz')],
    'FrostArmor':     [('Shield', 'amount', 'shield')],
    'Stonehide':      [('ArmorModifier', 'add', 'ar_add')],
    'Bulwark':        [('FormationSpacing', 'spacingMetres', 'sp'),
                       ('DamageModifier', 'defensive', 'front_phys_res')],
    'Singling':       [('DamageModifier', 'offensive', 'scarce')],
    'Talons':         [('ArmorBypass', 'bypass', 'bypass')],
}


def mm_tracks():
    """Track payloads in `matchup-math/roster19.py`'s override-dict shape:
    {unitType: {trackName: [step1_overrides, step2, step3]}}."""
    out = {}
    for name, t in TRACKS.items():
        steps = []
        for s in t['steps']:
            over = {}
            for eff in s['effects']:
                params = dict(eff.get('params', {}))
                params.update(eff.get('grants', {}).get('params', {}))
                for prim, param, key in _MM_TRACK_KEYS[name]:
                    if eff['primitive'] == prim and param in params:
                        over[key] = params[param]
                if eff['primitive'] == 'RemoveAttackTag' and eff['params']['tag'] == 'Heavy':
                    over['heavy'] = False
            steps.append(over)
        out.setdefault(t['unitType'], {})[name] = steps
    return out


def unexercised_payloads():
    """Every technology and track step that carries no paper evidence (§34.3)."""
    out = []
    for name, t in TECHNOLOGIES.items():
        if t['evidence'] == 'unexercised':
            out.append(name)
    for name, t in TRACKS.items():
        for s in t['steps']:
            if s['evidence'] == 'unexercised':
                out.append('%s %d' % (name, s['step']))
    return out


def authored_at_write_up():
    """The six ⚠ technologies of §18.1 / §34.4."""
    return [n for n, t in TECHNOLOGIES.items() if t['authoredAtWriteUp']]
