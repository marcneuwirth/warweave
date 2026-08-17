"""Validates the acceptance block of every promoted run.

See `instruments/determinism-v1.md` §5. The determinism acceptance tests — the
width change, the golden-trace corpus, the two-seed pass — cost real battles and
can never run in CI. So CI does not check that they ran; it checks the
**paperwork**, and the paperwork is committed evidence under
`docs/analysis/runs/`.

The four rules, each closing a way to lie by omission:

  1. every check in the contract's set must be present — a missing key is a hard
     fail, never an assumed pass (`#34`'s absent-vs-measured-zero rule, applied
     to paperwork);
  2. `result` is a closed enum — there is no `skipped`;
  3. `notApplicable` requires a non-empty `reason`, so an exemption costs a
     written sentence in committed evidence;
  4. the toolchain identity (`goVersion`, `goarch`) is recorded, because a
     golden-trace corpus is only valid for the build that produced it (F-3).

This test passes vacuously until the first run is promoted. That is correct and
not a silent pass: it reports the number of runs it found, so zero is visible.

Run:  python3 instruments/promoted_manifest_test.py
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, 'docs', 'analysis', 'runs')

CONTRACT = 'determinism v1'

# `#25` width change, `#25` golden-trace corpus, `#39` two-seed, `#28` mirror
# draw, `#36` order swap. Extending the contract means editing this set *and*
# bumping the contract version — every already-promoted run then names the older
# contract, which is exactly the record we want.
REQUIRED_CHECKS = {
    'widthChange',
    'goldenTrace',
    'twoSeed',
    'mirrorDraw',
    'orderSwap',
}

RESULTS = {'pass', 'fail', 'notApplicable'}


def validate(path, manifest):
    """Return a list of human-readable problems with one promoted manifest."""
    problems = []

    acceptance = manifest.get('acceptance')
    if not isinstance(acceptance, dict):
        return ['no `acceptance` block — a promoted run must record what was checked']

    contract = acceptance.get('contract')
    if contract != CONTRACT:
        problems.append(
            f'acceptance.contract is {contract!r}, expected {CONTRACT!r}'
        )

    for field in ('goVersion', 'goarch'):
        if not acceptance.get(field):
            problems.append(
                f'acceptance.{field} missing — the toolchain is part of the '
                f'determinism identity (determinism-v1 F-3)'
            )

    checks = acceptance.get('checks')
    if not isinstance(checks, dict):
        return problems + ['acceptance.checks missing or not an object']

    for name in sorted(REQUIRED_CHECKS - set(checks)):
        problems.append(f'check {name!r} absent — absent is not a pass')

    for name in sorted(set(checks) - REQUIRED_CHECKS):
        problems.append(
            f'check {name!r} is not in contract {CONTRACT!r} — extend the '
            f'contract and bump its version, do not add keys ad hoc'
        )

    for name in sorted(set(checks) & REQUIRED_CHECKS):
        entry = checks[name]
        if not isinstance(entry, dict):
            problems.append(f'check {name!r} is not an object')
            continue
        result = entry.get('result')
        if result not in RESULTS:
            problems.append(
                f'check {name!r} result is {result!r}, not one of '
                f'{sorted(RESULTS)} — there is no "skipped"'
            )
        elif result == 'fail':
            problems.append(f'check {name!r} FAILED — this run must not be promoted')
        elif result == 'notApplicable' and not str(entry.get('reason', '')).strip():
            problems.append(
                f'check {name!r} is notApplicable with no reason — skipping is '
                f'allowed, skipping quietly is not'
            )

    return problems


def main():
    if not os.path.isdir(RUNS):
        print(f'  0 promoted runs — {os.path.relpath(RUNS, ROOT)} does not exist yet.')
        print('PASS — vacuously; no run has been promoted.')
        return 0

    manifests = sorted(
        os.path.join(dirpath, 'manifest.json')
        for dirpath, _, files in os.walk(RUNS)
        if 'manifest.json' in files
    )

    if not manifests:
        print(f'  0 promoted runs under {os.path.relpath(RUNS, ROOT)}.')
        print('PASS — vacuously; no run has been promoted.')
        return 0

    failed = 0
    for path in manifests:
        rel = os.path.relpath(path, ROOT)
        try:
            with open(path) as f:
                manifest = json.load(f)
        except (OSError, ValueError) as exc:
            print(f'  FAIL {rel}: unreadable — {exc}')
            failed += 1
            continue

        problems = validate(path, manifest)
        if problems:
            failed += 1
            print(f'  FAIL {rel}')
            for problem in problems:
                print(f'         · {problem}')
        else:
            print(f'  ok   {rel}')

    print(f'  ---- {len(manifests)} promoted run(s), {failed} invalid')
    if failed:
        print(
            'FAIL — a promoted run is committed evidence. Its acceptance block '
            'is the only enforcement the expensive determinism tests have.',
            file=sys.stderr,
        )
        return 1

    print(f'PASS — every promoted run records its {CONTRACT} acceptance.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
