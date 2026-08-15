# ADR-0012 — Affinity tracks currently-owned squads; the full purchase price leaves on a sale

**Status:** accepted · **Ticket:** [#4](https://github.com/marcneuwirth/warweave/issues/4) · **Spec:** §6.1, §6.2

## Context

Reinstating selling ([ADR-0010](0010-selling-reinstated.md)) reopens exactly the exploit the original deferral named. What happens to `branchInvestment` when a squad is sold decides whether the affinity system survives.

## Decision

```
branchInvestment = Σ purchase price of CURRENTLY OWNED squads of that branch's unit types
Affinity         = floor(branchInvestment / 200), capped at 5
```

Selling removes the **full purchase price**, not the refunded half.

**Purchase gates check at purchase time; doctrines and hybrid unlocks check continuously.**

## The three readings

- **Investment survives the sale.** Buy a 200g gateway → +200 investment; sell → +100 gold, investment unchanged. Each cycle buys 200 of permanent affinity for 100 net gold and **zero squad slots**. Affinity 5 costs 500 instead of 1,000 and every player churns to 3/3/3 collecting every hybrid. **This ends the affinity system.**
- **Only the refunded amount leaves.** No discount versus holding, so not strictly an exploit — but it accrues affinity while owning **no squads of that branch** and burning no slots. A pure-Common army buys a hybrid unlock for 1,200 gold, and affinity stops describing the army, which is the one thing it exists to do.
- **Full removal** is the only reading where affinity means *what I currently have committed*, and the only one that is **refund-rate independent** — the 50% can be retuned by simulation without reopening this.

## Consequences

- The gate/bonus split has a real consequence a player can feel: buy two gateways (Beast 2), buy the tier-2 unit, sell the gateways — you keep the unit and fall to Beast 1, losing every continuous effect. The tier-2 unit effectively cost 500 gold and two rounds. A real price, not a loophole.
- The original sentence "because selling does not exist in v0.4, branch investment cannot be cycled or manipulated" is void.
- Later strengthened: **only unit purchases generate affinity at all** ([ADR-0050](0050-units-only-affinity.md)), which removes the technology half of the pump rather than capping it.
