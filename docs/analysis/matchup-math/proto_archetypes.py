"""WITNESS -- not the canonical rule. Deployment layout generator (#18, #49).

The canonical definition of the layout rule is the written spec
`instruments/deployment-layout-v2.md` (#33 s2). This file is one of its two
witnesses; `../deployment-archetypes-v2.csv` is the other. Where this file and
the spec disagree, the spec is right and this file is a bug.

It reads its inputs -- the roster and the fifteen builds -- from `data/`, so it
cannot drift from what the Go runner reads.

Run:  python3 proto_archetypes.py [render|legal|span|freeze|all]

Field (s23): 60m x 80m, own band y in [0, 24], front edge y = 24, enemy front
edge y = 56, gap 32m. Own control point (30, 12). The opposing side is the
point reflection about (30, 40): (x, y) -> (60 - x, 80 - y).
Frontage = (front - 1) * sp + 2 * rad, surface to surface per s13 -- so six
Spear Guard span 64.8m and not the 60m #12 assumed.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', '..', '..', 'data'))
import builds as buildsdata

from roster19 import U19

# The build set is a versioned artifact in `data/` (#33 F-4, #47), not a dict
# inside this witness. `FIELD` is re-exported unchanged so `roster19.py` and
# this file cannot disagree about which fifteen builds exist.
FIELD = buildsdata.field()
LAYOUT_VERSION = buildsdata.LAYOUT_VERSION

W, BAND = 60.0, 24.0          # field width, own band depth
FRONT, BACK = 24.0, 0.0       # y of band front edge / baseline
CP = (30.0, 12.0)             # own control point (#6)


def frontage(u):
    d = U19[u]
    return (d['front'] - 1) * d['sp'] + 2 * d['rad']


def depth(u):
    d = U19[u]
    return (d['ranks'] - 1) * d['sp'] + 2 * d['rad']


def squads(name):
    """Flatten an army spec into a list of unit-type names, one per squad."""
    out = []
    for s in FIELD[name]:
        out += [s[0]] * s[1]
    return out


ROLE_ORDER = {'hold': 0, 'none': 1, 'access': 2, 'reach': 3}


def by_role(names):
    """Front-to-back ordering. Hold leads, reach trails, access flanks.

    The third key is load-bearing, not cosmetic (#33 F-2). Without it the
    comparator ties for {SpearGuard, BannerGuard, Lifewarden} at hold/10.8m,
    for {EmberMage, Frostcaller} at reach/4.8m, and for every repeated unit
    type -- and Python's stable sort would then resolve those by input order,
    which under runtime generation is *purchase order*. Where your Spear Guard
    stand would depend on which round you bought them.
    """
    return sorted(names, key=lambda n: (ROLE_ORDER[U19[n]['role']],
                                        -frontage(n), n))


def clamp_y(n, y):
    """The depth-aware band clamp (#33 F-3), a stated invariant of the rule.

    Every squad's centre sits in `[depth/2, 24 - depth/2]`, so its footprint is
    inside the band. s1.5 derived exactly this bound for rank *pitch* and never
    applied it to the rear rank's offset from the baseline: `screened` and
    `refused` park their rear rank at y = 1.0, and a Troll there (2.4m deep)
    lands at y = -0.2, off the field. #33 measured 18 infeasible cells in a
    36,000-cell random-army sweep; #49 re-ran it at its own seed and got 15,
    all the same shape, all eliminated by this clamp.

    Measured before adoption: it changes 0 of the 90 frozen cells, and fires on
    none of them -- so this is the one path the conformance table cannot cover.
    """
    d = depth(n)
    return min(max(y, d / 2), BAND - d / 2)


# ---------------------------------------------------------------------------
# Layout helpers -- each returns [(unit, x_centre, y_centre)]
# ---------------------------------------------------------------------------
def row(names, y, x0=0.0, x1=W, gap=None):
    """Lay names left-to-right across [x0, x1], centred, evenly gapped."""
    if not names:
        return []
    span = sum(frontage(n) for n in names)
    slack = (x1 - x0) - span
    g = slack / (len(names) + 1) if gap is None else gap
    if g < 0:
        g = 0.0
    x = x0 + max(g, (x1 - x0 - span - g * (len(names) - 1)) / 2)
    out = []
    for n in names:
        out.append((n, x + frontage(n) / 2, clamp_y(n, y)))
        x += frontage(n) + g
    return out


def rows(names, ys, x0=0.0, x1=W, step=5.0):
    """Fill ranks front-to-back; each rank takes as many as fit in [x0, x1].

    #12: twelve squads never fit in one rank on a 60m field, so every
    archetype needs an unbounded rank supply. Extra ranks are appended
    behind `ys` at `step` metres until the army is placed or the band runs
    out -- running out of band is a real illegality and is reported.
    """
    out, i, ys, last = [], 0, list(ys), None
    while i < len(names):
        if not ys:
            ys = [last - step if last is not None else 0.0]
        y = ys.pop(0)
        last = y                          # the *planned* rank, pre-clamp: an
                                          # overflow rank must keep descending
                                          # even where the clamp held a squad
        take, span = [], 0.0
        while i < len(names) and span + frontage(names[i]) <= (x1 - x0):
            span += frontage(names[i]) + 1.0
            take.append(names[i]); i += 1
        if not take:                      # squad wider than the lane
            take, i = [names[i]], i + 1
        out += row(take, y, x0, x1)
    return out


# ---------------------------------------------------------------------------
# The six candidate archetypes
# ---------------------------------------------------------------------------
def a_line(ns):
    """LINE -- the naive wall: one rank at the front edge with reach standing
    *in* it, on the flanks. The designated poor-positioning row (#27), and the
    unscreened half of the screening pair (#12 P1)."""
    ns = by_role(ns)
    body = [n for n in ns if U19[n]['role'] != 'reach']
    back = [n for n in ns if U19[n]['role'] == 'reach']
    half = len(back) // 2
    order = back[:half] + body + back[half:]      # reach pushed to both flanks
    return rows(order, [22.0, 17.0, 12.0])


def a_refused(ns):
    """REFUSED FLANK -- right half at the edge, left half echeloned back."""
    ns = by_role(ns)
    half = (len(ns) + 1) // 2
    strong, weak = ns[:half], ns[half:]
    return (rows(strong, [22.0, 16.0], 30.0, W)
            + rows(weak, [12.0, 6.0], 0.0, 30.0))


def a_wings(ns):
    """SPLIT WINGS -- two blocks on the flanks, centre empty."""
    ns = by_role(ns)
    left, right = ns[0::2], ns[1::2]
    return (rows(left, [22.0, 17.0, 12.0, 7.0, 2.0], 0.0, 24.0, step=3.0)
            + rows(right, [22.0, 17.0, 12.0, 7.0, 2.0], 36.0, W, step=3.0))


def a_column(ns):
    """DEEP COLUMN -- narrow centre spearhead, stacked in depth."""
    ns = by_role(ns)
    return rows(ns, [22.0, 19.0, 16.0, 13.0, 10.0, 7.0, 4.0, 1.0], 18.0, 42.0,
                step=3.0)


def a_screened(ns):
    """SCREENED BACKLINE -- reach deep, every non-reach squad in front of it."""
    ns = by_role(ns)
    back = [n for n in ns if U19[n]['role'] == 'reach']
    screen = [n for n in ns if U19[n]['role'] != 'reach']
    if not screen:
        # A build with no non-reach squad still has to be screened, so its
        # frontmost reach squads take the screen slots. This is what makes the
        # set legal for every build (#18) rather than only for builds that
        # happen to own a screening unit.
        screen, back = back[:len(back) // 2], back[len(back) // 2:]
    return rows(screen, [22.0, 17.0]) + rows(back, [6.0, 1.0], 10.0, 50.0)


def a_forward(ns):
    """FORWARD-CONCENTRATED -- everything jammed at the front edge, massed
    on the centre. Candidate for the designated *poor positioning* row."""
    ns = by_role(ns)
    return rows(ns, [22.5, 19.0, 15.5, 12.0, 8.5, 5.0, 1.5], 15.0, 45.0,
                step=3.5)


ARCHETYPES = {
    'line': a_line,
    'refused': a_refused,
    'wings': a_wings,
    'column': a_column,
    'screened': a_screened,
    'forward': a_forward,
}


# ---------------------------------------------------------------------------
# Stance (#3 s2.4 Hold/Advance, #17 Raid)
# ---------------------------------------------------------------------------
# An archetype is a *complete* deployment, so every squad carries a stance and
# the sweep has no free variable. Raid appears in exactly two archetypes, so
# raid-vs-no-raid is a comparison the sweep can read rather than a setting.
RAIDING = ('refused', 'wings')


def stances(arch, place):
    """Assign a stance to each placed squad. Returns a list parallel to place."""
    out = []
    for n, x, y in place:
        role = U19[n]['role']
        if arch in ('column', 'wings', 'forward'):
            s = 'Advance'
        elif arch == 'refused':
            s = 'Advance' if x >= 30.0 else 'Hold'
        else:                                  # line, screened
            s = 'Advance' if role == 'access' else 'Hold'
        out.append(s)
    if arch in RAIDING:
        # The rearmost access squad raids; failing that, the fastest non-reach
        # squad does. A build with neither fields no raider, which is itself a
        # measurable property of the build.
        cand = [i for i, (n, _, _) in enumerate(place)
                if U19[n]['role'] == 'access']
        if not cand:
            cand = [i for i, (n, _, _) in enumerate(place)
                    if U19[n]['role'] != 'reach']
        if cand:
            out[min(cand, key=lambda i: (place[i][2], -U19[place[i][0]]['spd']))] \
                = 'Raid'
    return out


# ---------------------------------------------------------------------------
# Legality
# ---------------------------------------------------------------------------
def violations(place):
    """In-band and non-overlap checks (#3 s1.7). Returns list of strings.

    A non-empty return is the `deploymentInfeasible` cell outcome (#33 s5):
    the harness records it for that (army, archetype) and continues, so the
    6x6 mean for that army is taken over 35 cells rather than 36 and the
    instrument sees the absence explicitly. Silently clamping whatever comes
    out was rejected -- a clamp that shoves a Troll forward yields a cell
    still labelled `screened` that is not one.
    """
    bad = []
    boxes = []
    for n, x, y in place:
        w, d = frontage(n), depth(n)
        x0, x1 = x - w / 2, x + w / 2
        y0, y1 = y - d / 2, y + d / 2
        if x0 < -1e-6 or x1 > W + 1e-6:
            bad.append(f'{n} off-field x [{x0:.1f},{x1:.1f}]')
        if y0 < BACK - 1e-6 or y1 > FRONT + 1e-6:
            bad.append(f'{n} out of band y [{y0:.1f},{y1:.1f}]')
        boxes.append((n, x0, x1, y0, y1))
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, b = boxes[i], boxes[j]
            if a[1] < b[2] - 1e-6 and b[1] < a[2] - 1e-6 \
               and a[3] < b[4] - 1e-6 and b[3] < a[4] - 1e-6:
                bad.append(f'{a[0]}/{b[0]} footprints overlap')
    return bad


# ---------------------------------------------------------------------------
# Span metrics -- what each archetype is supposed to make measurable
# ---------------------------------------------------------------------------
def metrics(place):
    if not place:
        return {}
    xs = [x for _, x, _ in place]
    ys = [y for _, _, y in place]
    ymax = max(ys)
    covered = sum(frontage(n) for n, _, y in place if y > ymax - 1.0)
    return dict(
        width=max(x + frontage(n) / 2 for n, x, _ in place)
              - min(x - frontage(n) / 2 for n, x, _ in place),
        wall=min(100.0, 100.0 * covered / W),        # % of 60m walled
        depth=max(ys) - min(ys),
        cx=sum(xs) / len(xs),
        reach_y=min([y for n, _, y in place if U19[n]['role'] == 'reach'] or [0]),
    )


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------
GLYPH = {'hold': '#', 'reach': '^', 'access': '>', 'none': '.'}
COLS, ROWS = 60, 13           # 1m per col, ~2m per row


def render(place, title):
    grid = [[' '] * COLS for _ in range(ROWS)]
    for n, x, y in place:
        w = frontage(n)
        r = ROWS - 1 - int(round(y / BAND * (ROWS - 1)))
        r = max(0, min(ROWS - 1, r))
        for c in range(int(round(x - w / 2)), int(round(x + w / 2)) + 1):
            if 0 <= c < COLS:
                grid[r][c] = GLYPH[U19[n]['role']]
    cpr = ROWS - 1 - int(round(CP[1] / BAND * (ROWS - 1)))
    if grid[cpr][30] == ' ':
        grid[cpr][30] = 'o'
    print(f'  {title}')
    print('   +' + '-' * COLS + '+   <- front edge y=24 (32m gap to enemy)')
    for i, r in enumerate(grid):
        print('   |' + ''.join(r) + '|')
    print('   +' + '-' * COLS + '+   <- own baseline y=0')
    m = metrics(place)
    print(f'   width {m["width"]:.0f}m  wall {m["wall"]:.0f}%  depth {m["depth"]:.0f}m'
          f'  reach-y {m["reach_y"]:.0f}m')
    v = violations(place)
    print('   ILLEGAL: ' + '; '.join(v) if v else '   legal')
    print()


def cmd_render(army='PureMilitary'):
    ns = squads(army)
    print(f'\n=== {army}: {len(ns)} squads  ({"  ".join(sorted(set(ns)))})')
    print('    # hold   ^ reach   > access   . Common   o control point\n')
    for name, fn in ARCHETYPES.items():
        render(fn(ns), name.upper())


def cmd_legal():
    print(f'\nlegality: {len(ARCHETYPES)} archetypes x {len(FIELD)} builds\n')
    print(f'{"build":16} ' + ' '.join(f'{a:>9}' for a in ARCHETYPES))
    fails = 0
    for army in FIELD:
        cells = []
        for a, fn in ARCHETYPES.items():
            v = violations(fn(squads(army)))
            fails += bool(v)
            cells.append('ok' if not v else f'{len(v)}BAD')
        print(f'{army:16} ' + ' '.join(f'{c:>9}' for c in cells))
    print(f'\n{fails} illegal cells of {len(ARCHETYPES) * len(FIELD)}')


def cmd_span():
    """Does the set separate the builds it is meant to separate?"""
    print('\nspan -- per-archetype metrics, averaged over the 15 builds\n')
    print(f'{"archetype":12} {"width":>7} {"wall%":>7} {"depth":>7} {"reach-y":>8}')
    for a, fn in ARCHETYPES.items():
        ms = [metrics(fn(squads(x))) for x in FIELD]
        print(f'{a:12} ' + ' '.join(
            f'{sum(m[k] for m in ms) / len(ms):7.1f}'
            for k in ('width', 'wall', 'depth')) +
            f' {sum(m["reach_y"] for m in ms) / len(ms):8.1f}')
    print('\nfull-width wall (#12: six Spear Guard span exactly 60m):')
    for army in ('SpearGuard12', 'PureMilitary', 'MilMagic'):
        m = metrics(a_line(squads(army)))
        print(f'  {army:14} line wall = {m["wall"]:.0f}% of 60m')


CSV = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    '..', 'deployment-archetypes-v2.csv'))


def table():
    """The conformance table, as a list of CSV lines including the header.

    #33 s1 demoted this from *what the runner reads* to *what proves the
    runner's generator is the same generator*: the Go generator regenerates
    all 1,056 rows from the same two `data/` files and must match byte for
    byte. `%.2f` is what makes byte-identity achievable.

    It is a conformance table and not the artifact, so it cannot cover every
    path a novel army takes. Measured (layout-v2 F-3): the overflow rank fires
    on 12 of 90 cells and the name tiebreak on 12, but the band clamp fires on
    none. That last one is why #33 put a `deploymentHash` on every battle row.
    """
    lines = ['archetype,build,slot,unit,x,y,stance']
    for army in FIELD:
        for a, fn in ARCHETYPES.items():
            place = fn(squads(army))
            for i, ((n, x, y), s) in enumerate(zip(place, stances(a, place)), 1):
                lines.append(f'{a},{army},{i},{n},{x:.2f},{y:.2f},{s}')
    return lines


def infeasible_cells():
    """Every (build, archetype) the rule cannot place legally."""
    out = []
    for army in FIELD:
        for a, fn in ARCHETYPES.items():
            v = violations(fn(squads(army)))
            if v:
                out.append((army, a, v))
    return out


def cmd_freeze(path=CSV):
    """Write the conformance table.

    Refuses to write an infeasible table: s1.5's "all 90 cells are legal" is a
    property of the fifteen rather than of the rule (#33 F-6), so it is checked
    here rather than assumed.
    """
    bad = infeasible_cells()
    if bad:
        for army, a, v in bad:
            print(f'  deploymentInfeasible {army}/{a}: {"; ".join(v)}')
        print(f'REFUSING to write {path}: {len(bad)} infeasible cell(s)')
        return 1
    lines = table()
    with open(path, 'w') as f:
        f.write('\n'.join(lines) + '\n')
    print(f'wrote {path}: {len(lines) - 1} rows, layout v{LAYOUT_VERSION}, '
          f'0 infeasible cells')
    raiders = sum(1 for ln in lines if ln.endswith(',Raid'))
    holds = sum(1 for ln in lines if ln.endswith(',Hold'))
    print(f'  Raid {raiders}  Hold {holds}  Advance {len(lines) - 1 - raiders - holds}')
    return 0


COMMANDS = ('render', 'legal', 'span', 'freeze', 'all')


def main(argv):
    """An unrecognised subcommand exits non-zero (determinism-v1 F-1).

    `freeze` was defined but never dispatched, so the one command a reader
    would try to reproduce the versioned artifact fell through every branch
    and the script exited 0 in silence -- the exact silent pass #41 exists to
    abolish, in the half of the repo that survives `rm -rf runner/`.
    """
    cmd = argv[1] if len(argv) > 1 else 'all'
    if cmd not in COMMANDS:
        print(f'unknown subcommand {cmd!r}; expected one of '
              f'{", ".join(COMMANDS)}', file=sys.stderr)
        return 2
    if cmd in ('render', 'all'):
        cmd_render(argv[2] if len(argv) > 2 else 'PureMilitary')
    if cmd in ('legal', 'all'):
        cmd_legal()
    if cmd in ('span', 'all'):
        cmd_span()
    if cmd == 'freeze':
        return cmd_freeze()
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
