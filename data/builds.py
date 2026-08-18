"""Loader for the build set the deployment layout rule is frozen against.

`builds.json` is version-locked to **layout**, not to the roster (#47): #33 §7
makes the conformance table a pure function of *(rule, builds)*, so the rule,
the fifteen and the table carry one number. The file is a sibling of
`roster-v2.json` rather than part of it for that reason — the roster is a game
rule a balance pass edits, the build set is an *instrument's* input.

It has a second coupling the version number does **not** carry: every build is
priced and gated by the roster, so a reprice can make one illegal without
touching `layout`. That coupling is enforced by a check instead of a number —
`conformance_test.py` §9. See `instruments/deployment-layout-v2.md` §7.

This module is the Python reader. The Go runner reads the same file with
`encoding/json`; neither side owns the values.
"""
import hashlib
import json
import os

import roster

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'builds.json')

with open(PATH, 'rb') as _f:
    _RAW = _f.read()

DATA = json.loads(_RAW.decode('utf-8'))

#: SHA-256 of the artifact as loaded, alongside `LAYOUT_VERSION` in every
#: recorded measurement — a forgotten version bump is still detectable (#26).
CONTENT_SHA256 = hashlib.sha256(_RAW).hexdigest()

SCHEMA_VERSION = DATA['schemaVersion']
LAYOUT_VERSION = DATA['layoutVersion']
BUILDS = DATA['builds']
CATEGORIES = DATA['categories']

#: §4.2's cumulative income, R1..R12. Index 0 is round 1.
CUMULATIVE_INCOME = (400, 700, 1050, 1450, 1900, 2400, 2950, 3500,
                     4050, 4600, 5150, 5700)

#: §4.4.
SQUAD_CAP = 12


def squads(name):
    """Flatten a build into one unit-type name per squad, in file order."""
    out = []
    for s in BUILDS[name]['squads']:
        out += [s['unitType']] * s['count']
    return out


def squad_count(name):
    return sum(s['count'] for s in BUILDS[name]['squads'])


def gold(name):
    """Total spend: squads at list price, plus every track step climbed.

    §17.2 makes a track cumulative — reaching step 3 pays steps 1–3 — so the
    cost is `sum(trackStepCosts[:step])`, not the step's own price.
    """
    total = 0
    for s in BUILDS[name]['squads']:
        total += roster.UNITS[s['unitType']]['cost'] * s['count']
        if 'track' in s:
            total += roster.track_cost(s['trackStep'])
    return total


def branch_investment(name):
    """§6.1 gold per branch. Only a track's *first* step counts (#19 Q11)."""
    inv = {}
    for s in BUILDS[name]['squads']:
        u = roster.UNITS[s['unitType']]
        if u['branch'] == 'Common':
            continue
        inv[u['branch']] = (inv.get(u['branch'], 0)
                            + u['cost'] * s['count']
                            + (roster.TRACK_STEP_COSTS[0] if 'track' in s else 0))
    return inv


def affinity(name):
    """§6.3 affinity per branch this build reaches."""
    return {b: roster.affinity(v) for b, v in branch_investment(name).items()}


def earliest_round(name):
    """First round of §4.2's cumulative income that affords the build.

    `None` if no round through R12 does. Derived, never stored: storing it
    would put a roster-dependent number in a file the roster does not version.
    """
    g = gold(name)
    for i, c in enumerate(CUMULATIVE_INCOME, 1):
        if g <= c:
            return i
    return None


def mm_spec(name):
    """The build in `matchup-math/roster19.py`'s `FIELD` tuple shape.

    The calculator's shape is the calculator's, not canon, so the translation
    lives here — same treatment `roster.mm_tracks()` gives the track payloads.
    """
    out = []
    for s in BUILDS[name]['squads']:
        t = (s['unitType'], s['count'])
        if 'track' in s:
            t += (s['track'], s['trackStep'])
        out.append(t)
    return out


def field():
    """Every build in `FIELD` shape, in file order."""
    return {name: mm_spec(name) for name in BUILDS}
