# `determinism v1` — the discipline, and how it is enforced

Resolves [#41](https://github.com/marcneuwirth/warweave/issues/41). Implements the rules
decided in [#25](https://github.com/marcneuwirth/warweave/issues/25).

[#25](https://github.com/marcneuwirth/warweave/issues/25) decided *what* determinism means
for this kernel. It named the enforcement in one clause — *"the `map` type, `hash/maphash`
and global `math/rand` banned by a CI lint rule"* — against a repo that has never run CI.
This document is that clause made real, and it lives in `instruments/` rather than
`runner/` for the reason [#27](https://github.com/marcneuwirth/warweave/issues/27) gives:
**`rm -rf runner/` must delete the mechanism and leave the contract.**

It is not a fifth `manifest.versions` entry. A version earns a manifest slot by
re-denominating results orthogonally
([#31](https://github.com/marcneuwirth/warweave/issues/31),
[#39](https://github.com/marcneuwirth/warweave/issues/39)); this contract denominates
nothing. A breach does not change a number, it withdraws trust in every number. It is cited
instead from the **acceptance block** of §5 — a record of what was checked, not a
denominator.

---

## 1. The rule that generates the rest

> **A check is a runnable thing in the repo. CI is only the place that runs it where nobody
> can skip it.**

Everything below follows from that, and it has one hard consequence: **no check may exist
only inside `.github/workflows/ci.yml`.** Every step in the workflow is a one-line
invocation of something an agent can run locally with no arguments. A check that can only be
executed by pushing is a check that nobody runs while they are writing the code that breaks
it.

This is what rules out the alternatives the ticket named:

| Candidate | Why not |
| --- | --- |
| **Pre-commit hook** | `.git/hooks/` is not cloned. A fresh clone, a worktree, a cloud agent, a new session — none inherit it. Enforcement that is absent exactly for the newcomer. Not the primary mechanism; permitted as a local convenience that only invokes the same commands. |
| **Reviewer discipline** | The ticket's own premise. These breaches produce *plausible numbers that differ run to run*. There is nothing to see. |
| **A `go vet` custom analyzer** | Needs `golang.org/x/tools`, a separate binary and a separate invocation, to express three syntactic rules over one package. `go/ast` and `go/parser` are stdlib and run under the `go test ./...` CI already invokes. |
| **`golangci-lint` with `depguard`** | A versioned third-party toolchain added to the one directory whose defining property is that it gets deleted. |

**Ruled: plain tests in the repo, run by a GitHub Actions workflow, with `main` protected so
they cannot be merged around.**

---

## 2. The contract the kernel must satisfy

[#25](https://github.com/marcneuwirth/warweave/issues/25)'s rules, restated as the
checkable list, with the three amendments §6 argues for marked **⊕**.

1. **No unordered iteration.** The `map` type does not appear in kernel source. Identity is
   `ModelID = (side, squadIndex, modelIndex)` over flat tombstoned slices.
2. **No ambient nondeterminism.** No `hash/maphash`, no global `math/rand`, no RNG of any
   kind in the kernel — the v0.4 battle is a pure function of its initial state. The
   per-match PCG lives in the harness.
3. **No transcendentals.** No `math.Sin`, `Cos`, `Atan2`, `Pow`. §23.2's arc test is a
   dot-product sign; the turn clamp is a cross-product sign.
4. **Total orders.** Every comparator ends in a `ModelID`. No epsilons — they are not
   transitive.
5. **⊕ No clock, no concurrency, no environment.** The kernel is single-goroutine; a kernel
   that reads `time`, spawns a goroutine or touches `os` is nondeterministic in ways
   [#25](https://github.com/marcneuwirth/warweave/issues/25)'s three-item ban list does not
   name.
6. **⊕ The ban is on the closed import set, not on three names.** A syntactic ban is
   defeated by a transitive import: a helper package that ranges a map, imported by the
   kernel, breaks rule 1 while the kernel's own source stays clean.
7. **⊕ The toolchain is part of the identity.**
   [#25](https://github.com/marcneuwirth/warweave/issues/25) promises *same binary + same
   arch* and leaves unnamed the compiler that produced the binary. The Go version is
   recorded in every manifest and pinned in CI.

---

## 3. The guards

### 3.1 Go — `runner/kernel/determinism_test.go`

Two checks, both stdlib, both under `go test ./...`. **They die with `runner/`, which is
correct — their subject dies with it. §2 is what makes them re-derivable.**

**`TestKernelPurity`** parses every file under `runner/kernel/...` with `go/parser` and
fails on: a `map` type expression, and a selector into `math` outside a declared allowlist
(rule 3). It reports `file:line` and the offending expression.

**`TestKernelImportsAreClosed`** shells `go list -deps ./runner/kernel/...` and asserts the
transitive dependency set is a **subset of a literal allowlist declared at the top of the
test**. This is the primary guard, and it subsumes rules 2 and 5: `math/rand`,
`math/rand/v2`, `hash/maphash`, `time`, `os`, `sync` and `runtime` cannot be reached at any
depth because *nothing* not on the list can. Widening the kernel's reach is therefore a
visible diff to the guard, never a new import line.

**Exemptions.** Rule 1 is deliberately blunt: a map used only for keyed lookup is
deterministic, and a smarter analyzer that could tell the difference would be a second
implementation of the very reasoning we are trying not to trust. So the escape hatch is a
directive comment —

```go
//determinism:allow-map — keyed lookup only, never ranged; loader-time, not tick-time
```

— and `TestKernelPurity` asserts the **total exemption count equals a constant declared at
the top of the test file**. Adding an exemption is then an edit to a number in the guard,
visible in the diff, rather than a comment somebody sprinkles. The test prints every
exemption and its reason in verbose mode, so a promoted run's log carries the list.

### 3.2 Python — three checks at the repo root, stdlib only

**No `pytest`, no `requirements.txt`, no venv.** Every check is `python3 <file>` and the
exit code is the verdict. This is not minimalism for its own sake: the control arm has to
still run in five years, on a machine nobody has configured, for a reader who is checking
whether we cheated. A dependency file is a thing that can rot; stdlib is not.

| Check | What it defends |
| --- | --- |
| `python3 data/conformance_test.py` | [#26](https://github.com/marcneuwirth/warweave/issues/26)'s port. Passes today: `roster v1 sha256=943607c470af7e4f`. |
| `python3 docs/analysis/matchup-math/smoke_test.py` | [#27](https://github.com/marcneuwirth/warweave/issues/27)'s *"runnability is a tested property, not a hope"* — executes all seven control-arm modules as subprocesses and asserts exit 0. |
| `python3 instruments/promoted_manifest_test.py` | §5. Validates every committed manifest under `docs/analysis/runs/`. |

**Measured cost of the smoke check** on an M-series laptop, all seven modules:
`corebet.py` 79s, `tech11.py` 36s, `roster19.py` 12s, the other four under a second —
**127s**. Measured again on `ubuntu-latest`: **228s** (139s / 67s / 21s), a flat 1.8×.
Accepted, because it runs in a parallel job and the workflow's wall clock is its slowest
job, not the sum. **Stated
trigger, enforced by the check itself:** if the total exceeds **15 minutes** the check
fails and tells you to move it to the promotion gate of §5 — the point being that it may
not be quietly given a path filter instead.

### 3.3 The check that is specified here and lands elsewhere

**`layout v2` regeneration.** [#33](https://github.com/marcneuwirth/warweave/issues/33)
promoted `deployment-archetypes-v1.csv` from *what the runner reads* to *what proves the
runner's generator is the same generator* — which is only true if something regenerates and
diffs it. Nothing does.

Verified while resolving this ticket: **the committed CSV does reproduce byte-identically
today** (1,056 rows, 0 violations) when `proto_archetypes.cmd_freeze` is called. That is a
baseline, not a property — [#33](https://github.com/marcneuwirth/warweave/issues/33) already
found `by_role` is not a total order, so today's byte-identity is the luck of one dict
insertion order.

The check itself belongs to [#49](https://github.com/marcneuwirth/warweave/issues/49), not
here, because #49 both fixes that defect and ports the rule to Go — so the check's real
subject is *Go generator vs committed CSV*, and a Python-vs-CSV version written now is a
guard on a generator already scheduled for deletion. Its CI slot is reserved in
`ci.yml`. See F-1.

---

## 4. Trigger tiering

> **A check runs on every push if it is cheaper than the human's patience. A check runs at
> promotion if its subject *is* the promoted number.**

**Tier 1 — every push, every branch, no path filters.** The Go guards and `go test ./...`
(including [#30](https://github.com/marcneuwirth/warweave/issues/30)'s twelve golden
oracles) on **both arches of F-2's matrix**, plus the three Python checks. Parallel jobs;
target wall clock under 10 minutes.

**No path filters, deliberately.** A skipped required check reports differently from a
passed one but reads the same at a glance, and that is
[#34](https://github.com/marcneuwirth/warweave/issues/34)'s absent-versus-measured-zero
confusion arriving in the CI surface.

**Tier 2 — the promotion gate, §5.** The acceptance tests that cost real battles:
[#25](https://github.com/marcneuwirth/warweave/issues/25)'s width change (`NumCPU` 1 vs 16)
and the full golden-trace corpus,
[#28](https://github.com/marcneuwirth/warweave/issues/28)'s mirror-draw reflection test,
[#36](https://github.com/marcneuwirth/warweave/issues/36)'s order-swap fence test, and
[#39](https://github.com/marcneuwirth/warweave/issues/39)'s two-seed test — which alone is
a whole graded pass run twice, ~15M battles. These can never run in CI.

A **sampled** golden-trace subset (single-digit traces, one pass each) rides in tier 1; the
corpus rides in tier 2.

---

## 5. The acceptance block — enforcing what CI cannot run

Tier 2 is unrunnable by CI, so **CI does not check that it ran. It checks the paperwork, and
the paperwork is committed.**

`docs/analysis/runs/` is committed evidence
([#27](https://github.com/marcneuwirth/warweave/issues/27): *a falsification test whose
evidence was discarded is just an assertion*). So a promoted run's `manifest.json` carries
an `acceptance` block, and a **tier-1 test validates it on every push** — cheap, and it is
the only mechanism that survives the fact that the real test costs 15M battles.

```json
"acceptance": {
  "contract": "determinism v1",
  "goVersion": "go1.24.2",
  "goarch": "arm64",
  "checks": {
    "widthChange":  {"result": "pass"},
    "goldenTrace":  {"result": "pass"},
    "twoSeed":      {"result": "pass"},
    "mirrorDraw":   {"result": "pass"},
    "orderSwap":    {"result": "notApplicable", "reason": "single-side pass, no fence to test"}
  }
}
```

Four rules, each closing a way to lie by omission:

1. **Every key in the contract's check set must be present.** A missing key is a hard fail,
   never an assumed pass — [#34](https://github.com/marcneuwirth/warweave/issues/34)'s rule
   applied to paperwork.
2. **`result` is a closed enum: `pass`, `fail`, `notApplicable`.** There is no `skipped`.
3. **`notApplicable` requires a non-empty `reason`.** Skipping a check is permitted; skipping
   it *quietly* is not. The cost of an exemption is a written sentence in committed evidence.
4. **The harness is the sole writer** ([#34](https://github.com/marcneuwirth/warweave/issues/34)),
   and serialises a typed result returned by the check function. There is no code path that
   writes the string `"pass"`.

`manifest.versions` stays at four — roster, layout, policy, populations. `acceptance` is a
different block with a different meaning: what was *checked*, not what the numbers are
*denominated by*.

---

## 6. Findings

**F-1 — `proto_archetypes.py freeze` exits 0 having done nothing.** `cmd_freeze` is defined
at line 313 but **is not in the `__main__` dispatch**, which handles only `render`, `legal`,
`span` and `all`. An unknown subcommand falls through every branch and the script exits
successfully in silence. So the versioned artifact
`docs/analysis/deployment-archetypes-v1.csv` has **no runnable regeneration path**, and the
one command a reader would try to reproduce it reports success. This was hit accidentally
while resolving this ticket, which is the point: it is exactly the silent-pass failure mode
[#41](https://github.com/marcneuwirth/warweave/issues/41) exists to abolish, sitting in the
half of the repo that *survives* `rm -rf runner/`. Two fixes, both routed to
[#49](https://github.com/marcneuwirth/warweave/issues/49): dispatch `freeze`, and **make an
unrecognised subcommand exit non-zero** in every control-arm CLI.

**F-2 — the trig ban does not buy cross-arch identity, because FMA does not need
transcendentals.** [#25](https://github.com/marcneuwirth/warweave/issues/25) banned
`Sin`/`Cos`/`Atan2`/`Pow` to take *"the cheap half of portability free"*. But the Go
specification permits an implementation to fuse `x*y + z` into a single FMA — and Go's
compiler does this on **arm64** and not on **amd64**. §23.2's arc test is a dot product,
`a.X*b.X + a.Y*b.Y`; the turn clamp is a cross product. **The two load-bearing geometric
predicates in the kernel are the exact expression shape that fuses.** So the same source,
built with the same Go version, can produce different signs on the two architectures — and
the dev machine here is arm64 while `ubuntu-latest` is amd64.

Response is a ladder whose first rung is decided and lands with the Go job (F-5): **the Go
job is a two-arch matrix** — `ubuntu-latest` (amd64) and `macos-latest` (arm64) — which
makes the divergence *measured* rather than assumed. The second arch is therefore not
redundancy; it is a free continuous instrument on the portability
[#25](https://github.com/marcneuwirth/warweave/issues/25) chose to give away, and a
divergence there is a finding to record, not a red build to route around. If it does
diverge, rung 2 is to route every dot and cross product through a helper using **explicit
`float64(...)` conversions**, which the Go spec says round to the target type and therefore
forbid fusion; rung 3 is to **arch-tag the golden-trace corpus** and accept the split. The
later rungs are named, not pre-chosen: nothing about them can be decided before the first
trace exists.

**F-3 — the Go toolchain version was never part of the determinism identity.** *Same binary
+ same arch* leaves the compiler unnamed, but a golden-trace corpus is only valid for the
toolchain that produced it, and a Go minor upgrade changing a floating-point code path would
present as a red CI indistinguishable from a real regression. Ruled: the version is pinned
in `go.mod`'s `toolchain` directive, pinned in `ci.yml` from that file
(`go-version-file`, never `stable`), and **recorded in the acceptance block of every
promoted run** alongside `goarch`.

**F-4 — the guards cannot be enforced by a file in this repo.** A workflow that runs but is
not a **required status check** on `main` is reviewer discipline with extra steps, and branch
protection is repository settings, not a committed file. The one step of this ticket that no
agent can take: mark the tier-1 jobs required on `main`. Recorded rather than done.

**F-5 — the Go job is deliberately not written yet.** There is no `runner/`, so a Go job
authored today would be a green check over an empty directory — the same silent pass as F-1,
installed on purpose. §3.1 specifies it; it is authored in the same commit as
`runner/go.mod`, when it can first fail.
