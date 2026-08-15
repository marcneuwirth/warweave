# ADR-0024 — Apex Instinct is rebuilt, and access-role targeting becomes a culling rule

**Status:** accepted · **Ticket:** [#10](https://github.com/marcneuwirth/warweave/issues/10) · **Spec:** §9.4, §24.2

## Context

Splitting the word *Predation* into a movement effect and a separate target preference exposed that the Beast doctrine — "all Beast units gain Predation" — grants the branch's own gateway **nothing**, because Direwolves already had it. Its entire payload landed on one melee model already in contact. The double meaning had been hiding a doctrine measuring ~0.

Calibrated against measured flips, the decisiveness line sits at **+25–40%**, with ~10% explicitly the level that never decides anything. The doctrine was at zero.

## Decision

**One decision, two sections.**

> **Apex Instinct (Beast 5).** All Beast-branch unit types hunt as Direwolves do (below). A Beast model that kills an enemy model gains **−15% attack cooldown for 3 seconds**, per model, non-stacking.

> **Access-role targeting.** Each model attacks the enemy **model within its own reach** with the **lowest current HP**. With no target in reach, the squad moves toward the enemy **squad** with the lowest **total** HP.

## Why

**Breadth was never the problem — payload was.** Every doctrine has two halves: payload (what is granted) and breadth (who gets it). Breadth is roster-scaling headroom and should be left to grow into the alpha. Payload is not, and **6 × 0 is still 0**.

The rebuild makes **the branch's signature behaviour universal** — the gateway *is* the apex predator, and at affinity 5 the whole branch hunts that way — so it is a breadth doctrine by construction with a payload that is a real behaviour. The tempo clause is phrased in the spec's existing idiom (a cooldown modifier, not "attack speed") and sizes to roughly +8–13% squad DPS against multi-model squads, ~+4% against a heavy line, ~0 against a single large target: **Beast gets faster the more bodies it faces and nothing against one big thing** — *Overwhelm* stated mechanically.

**Backline preference becomes derived rather than authored.** Squad total HP is a static property of the unit type, so the tracking clause gives a fixed ordering — casters first, the heaviest line last, the cheap swarm mid-table so a pack still runs past a screen. The authored special case falls out of the stat blocks, and the confirmed screening result is **preserved by arithmetic** rather than by a rule.

The *model*-level reading of the tracking clause was rejected: lowest HP-per-model is the cheap swarm, so packs would charge the screen and the one design bet the paper math confirmed would break.

**Culling is correct despite raising overkill waste.** A bite into a nearly-dead model wastes most of itself. But with no overkill carry, killing the nearly-dead model is the cheapest possible **removal of an enemy attacker** — a model at 5 HP deals full DPS until it dies. Focused, a model dies every few seconds; spread, nobody dies for three volleys. The two metrics point opposite ways and the one pointing the pack's way is the one that wins fights.

Two doctrine candidates were rejected: giving Predation teeth (bonus damage against wounded targets) pays you for hitting models already dying, straight into no-overkill-carry; and a squad-concentration bonus **already exists** as a Direwolves technology, so proposing it as the doctrine would duplicate the technology whose name fits concentration.

## Consequences

- **This changes a stated principle, not just a list.** §24's "units should not continuously choose tactically perfect targets" had to be **rewritten**: the in-range cull *is* continuous re-evaluation. It is defensible because it is **local** to one model's own reach, deterministic, and grants no omniscience — and because the tracking clause is a static ordering the player answers by positioning.
- Under the role scheme this generalises from Direwolves to **every access-role unit type**, which is what *access* means.
- It also makes the Direwolves concentration technology live for the first time, since a culling squad concentrates by construction.
