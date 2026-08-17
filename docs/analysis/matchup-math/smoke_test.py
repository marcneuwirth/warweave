"""Proves the 1-D control arm still runs.

`#27` demoted `matchup-math/` from oracle to **control arm** and made its
runnability "a *tested* property, not a hope" — but nothing tested it. This does.

The arm is a **witness**: its value is that it was authored independently of the
2-D kernel, so it is never refactored to match and never ported. What it needs
instead is proof that it still executes, on a stdlib-only Python, years from now.

Each module is run as a subprocess with no arguments. For the four with a
`__main__` that is a full run; for the three without, it is an import check. A
non-zero exit fails the suite.

Deliberately no assertions on output. Pinning numbers here would make this a
second oracle, and `#33.9` disqualified the arm as one.

Run:  python3 docs/analysis/matchup-math/smoke_test.py
"""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))

# Ordered cheapest-first so a broken import fails fast, before the slow ones.
MODULES = [
    'mm.py',
    'canon.py',
    'sim2.py',
    'roster19.py',
    'proto_archetypes.py',
    'tech11.py',
    'corebet.py',
]

# See `instruments/determinism-v1.md` §3.2: if the total passes this, the check
# moves from every-push to the promotion gate rather than getting a path filter.
BUDGET_SECONDS = 15 * 60


def main():
    failures = []
    total = 0.0
    for name in MODULES:
        started = time.monotonic()
        proc = subprocess.run(
            [sys.executable, name],
            cwd=HERE,
            capture_output=True,
            text=True,
        )
        elapsed = time.monotonic() - started
        total += elapsed
        status = 'ok  ' if proc.returncode == 0 else 'FAIL'
        print(f'  {status} {name:<22} {elapsed:6.1f}s')
        if proc.returncode != 0:
            failures.append((name, proc.returncode, proc.stderr.strip()[-2000:]))

    print(f'  ---- {len(MODULES)} modules, {total:.1f}s total')

    for name, code, stderr in failures:
        print(f'\n{name} exited {code}:\n{stderr}', file=sys.stderr)

    if failures:
        print(f'FAIL — {len(failures)} control-arm module(s) no longer run.', file=sys.stderr)
        return 1

    if total > BUDGET_SECONDS:
        print(
            f'FAIL — {total:.0f}s exceeds the {BUDGET_SECONDS}s budget stated in '
            f'instruments/determinism-v1.md §3.2. Move this check to the promotion '
            f'gate; do not give it a path filter.',
            file=sys.stderr,
        )
        return 1

    print('PASS — the 1-D control arm still runs.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
