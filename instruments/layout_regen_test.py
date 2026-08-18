"""`layout v2` regenerates byte-identically.

Contract: `instruments/deployment-layout-v2.md`. Reserved as a CI slot by
[#41](https://github.com/marcneuwirth/warweave/issues/41) (determinism-v1 §3.3,
F-1) and written here by #49.

#33 demoted `deployment-archetypes-v2.csv` from *what the runner reads* to
*what proves the runner's generator is the same generator*. That is only true
if something regenerates and diffs it, and nothing did — `cmd_freeze` was not
even in the CLI dispatch, so the one command a reader would try exited 0 in
silence.

Its subject today is the **Python witness against the committed table**, which
catches a hand-edit to either and pins the amendments #49 made. When `runner/`
lands, the Go generator becomes a second subject checked against the same file;
this check does not change when it does.

Run:  python3 instruments/layout_regen_test.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'docs', 'analysis', 'matchup-math'))

import proto_archetypes as layout  # noqa: E402

failures = []


def fail(msg):
    failures.append(msg)


# --- the table regenerates byte-identically ---------------------------------
want = open(layout.CSV).read()
got = '\n'.join(layout.table()) + '\n'

if got != want:
    wl, gl = want.splitlines(), got.splitlines()
    if len(wl) != len(gl):
        fail('row count: committed %d, regenerated %d' % (len(wl) - 1, len(gl) - 1))
    diffs = [(i, w, g) for i, (w, g) in enumerate(zip(wl, gl), 1) if w != g]
    fail('%d row(s) differ; first at line %d:\n    committed   %s\n    regenerated %s'
         % (len(diffs), diffs[0][0], diffs[0][1], diffs[0][2]) if diffs
         else 'contents differ')

# --- the shape §33's artifact table states ----------------------------------
rows = [ln.split(',') for ln in want.splitlines()[1:]]
if len(rows) != 1056:
    fail('§33 states 1,056 rows; found %d' % len(rows))
if sorted({r[0] for r in rows}) != sorted(layout.ARCHETYPES):
    fail('archetype column does not match the six')
if sorted({r[1] for r in rows}) != sorted(layout.FIELD):
    fail('build column does not match the fifteen in data/builds.json')
if {r[6] for r in rows} - {'Hold', 'Advance', 'Raid'}:
    fail('unknown stance in the table')

# --- every coordinate is inside the band, footprints included ---------------
# The depth-aware clamp is an *invariant* of the rule, so it is asserted on the
# artifact rather than trusted from the generator that wrote it.
for r in rows:
    n, x, y = r[3], float(r[4]), float(r[5])
    w, d = layout.frontage(n), layout.depth(n)
    if x - w / 2 < -1e-6 or x + w / 2 > layout.W + 1e-6:
        fail('%s/%s slot %s: %s off-field in x' % (r[0], r[1], r[2], n))
    if y - d / 2 < -1e-6 or y + d / 2 > layout.BAND + 1e-6:
        fail('%s/%s slot %s: %s out of band in y' % (r[0], r[1], r[2], n))

# --- no cell of the fifteen is deploymentInfeasible -------------------------
# §1.5's "all 90 cells are legal" is a property of the fifteen, not of the rule
# (#33 F-6), so it is checked rather than assumed.
for army, arch, why in layout.infeasible_cells():
    fail('deploymentInfeasible %s/%s: %s' % (army, arch, '; '.join(why)))

if failures:
    print('\nFAIL — %d problem(s):' % len(failures))
    for f in failures:
        print('  ' + f)
    sys.exit(1)
print('PASS — layout v%d: %d rows regenerate byte-identically, 90/90 cells legal.'
      % (layout.LAYOUT_VERSION, len(rows)))
