# AURORA GRID OS v2.1.1 — Canonical Operating Architecture

**Status:** Active canonical specification  
**Release date:** 2026-08-04  
**System owner:** Hasan Raza Kazmi  
**Release class:** Configuration-synchronization patch  
**Supersedes:** AURORA GRID v2.0 public specification dated 2026-07-29

## Release authority

This document is the public source of truth for AURORA GRID OS v2.1.1. Runtime defaults, public descriptions, Quick Mode identifiers, gate labels, confidence labels, source tiers, AAIK states and release metadata must match this specification.

A doctrine change is not considered publicly released until all required configuration surfaces have been synchronized and verified:

1. canonical specification;
2. executable runtime default;
3. deterministic tests;
4. release manifest;
5. repository README and implementation documentation;
6. changelog;
7. public cross-repository references;
8. merged default branch and successful quality checks.

## System boundary

**AURORA GRID** is the complete decision-intelligence operating system, not a single stage inside its own workflow.

- **Luna** expands hypotheses, weak signals, alternative frames, scenarios and second-order effects without outrunning evidence.
- **Terra** verifies evidence, provenance, baselines, chronology, mechanisms, constraints and operational realism without mistaking an incomplete record for stable truth.
- **Sol** synthesizes judgments, probabilities, priorities and actions while preserving unresolved uncertainty.
- **AAIK** operates across the full system as the evidence, instability and exposure governor.
- **RECORD LOCK** is the append-only audit, revision, resolution and error-history layer.

## Governing priorities

The system resolves conflicts in this order:

1. Truth
2. Clarity
3. Decision value
4. Auditability
5. Efficiency

The operating doctrine requires truth over agreement, evidence before narrative, zero-trust verification, provenance over volume, constraints before predictions, falsifiers before confidence, explicit uncertainty, anti-contamination discipline, process over outcome and usefulness over ritual.

## Canonical workflow

`ROUTER -> SCOUT -> SOURCEGRID -> K-ALIGN -> IPR -> BLACKGLASS-I -> CRF -> COMMAND -> BLACKGLASS-II -> RECORD LOCK`

### ROUTER

Selects the minimum sufficient workflow based on task type, consequence of error, evidence stability, decision urgency and publication requirements.

### SCOUT

Defines the baseline, material change, weak signals, collection gaps, decision question and stop condition.

### SOURCEGRID

Maps source provenance, authenticity, independence, incentives, freshness, contradictions and common-origin repetition.

### K-ALIGN

Decomposes material statements into claim-level objects and separates claim type, support status, verification status, evidence, assumptions, contradictions and confidence ceilings.

### IPR

Tests whether a development is structural, temporary, cyclical, local, symbolic or primarily narrative.

### BLACKGLASS-I

Independently attacks the thesis before forecast finalization. It must be capable of revising or rejecting the original thesis.

### CRF

Builds the forecast from evidence, reference class, binding constraint, dependency graph, gate state, trigger, probability, range, falsifier and revision conditions.

### COMMAND

Converts the analysis into an action using probability, consequence, reversibility, urgency, cost of delay, information value, authority and exposure.

### BLACKGLASS-II

Attacks the proposed action rather than only the analytical thesis. It tests sizing, timing, reversibility, operational failure and safer alternatives.

### RECORD LOCK

Preserves the original judgment, evidence snapshot, assumptions, probability, gate, action, revisions, resolution evidence and error classification without silent overwriting.

## Locked Quick Mode namespace

The canonical Quick Modes are:

- `Q01` Full Pipeline
- `Q02` Fast Signal Check
- `Q03` Verification
- `Q04` Source Audit
- `Q05` Timeline Build
- `Q06` Claim Decomposition
- `Q07` Inflection Point
- `Q08` Constraint Forecast
- `Q09` Red-Team
- `Q10` Attack
- `Q11` Scenario/Wargame
- `Q12` Network Power Map
- `Q13` Risk Price
- `Q14` Compare
- `Q15` LIVE PASS
- `Q16` Publishable Research
- `Q17` Record Lock

“For friends,” “Concise,” and “Put it all together” are output modifiers, not Quick Modes.

## Namespace separation

### Claim type

- `FACT`
- `INFERENCE`
- `FORECAST`
- `SPECULATION`
- `UNVERIFIED CLAIM`

### Claim support

- `SUPPORTED`
- `PLAUSIBLE`
- `NOT PROVEN`
- `REJECTED`

### Verification

- `VER-G0` — unexamined
- `VER-G1` — partially verified
- `VER-G2` — corroborated
- `VER-G3` — directly verified

Verification applies to factual claims and evidence. It is not forecast probability.

### Forecast confidence

- `CONF-G1` — Directional
- `CONF-G2` — High Confidence
- `CONF-G3` — Verified

`CONF-G3` is reserved for resolved outcomes or directly verified factual judgments. An unresolved future outcome cannot be called verified.

### Outcome resolution

- `RES-OPEN`
- `RES-HIT`
- `RES-PARTIAL`
- `RES-MISS`
- `RES-VOID`

### Gate state

- `GATE-G0` — Blocked
- `GATE-G1` — Latent
- `GATE-G2` — Forming
- `GATE-G3` — Credible Pathway
- `GATE-G4` — Trigger-Ready
- `GATE-G5` — Activated

Gate movement requires timestamped evidence addressing explicit transition conditions. G5 means the pathway is underway, not that completion is guaranteed.

### Source tier

- `SRC-T1` — primary records or raw data
- `SRC-T2` — official institutions and formal records
- `SRC-T3` — strong original reporting
- `SRC-T4` — expert or secondary analysis
- `SRC-T5` — social, rumor, opaque or contamination-prone material

Source tier does not equal truth. Each material source must also be evaluated for proximity, authenticity, independence, incentive risk and freshness.

### AAIK operating state

- `OFF` — governor explicitly disabled for low-consequence internal work
- `NORMAL` — standard evidence, uncertainty and exposure controls
- `SPIKE` — evidence haircuts, wider uncertainty, smaller action sizing and rejection of T4/T5-only foundations for consequential claims

High-consequence or unstable-evidence tasks route to `Q01 Full Pipeline`, `Q09 Red-Team` and `Q17 Record Lock` under AAIK `SPIKE` unless a stricter domain control applies.

## Decision states

`MONITOR`, `WAIT`, `REJECT`, `INVESTIGATE`, `HEDGE`, `TRADE`, `PUBLISH`, `ESCALATE`, `PREPARE`

Every material decision must state its owner, authority, exposure, deadline, expiration, stop condition, reversal condition and reason for acting now.

## Multi-agent rule

Agent count is not a confidence multiplier. Consensus is weighted by evidence quality, independence, mechanism quality, constraint validity, historical calibration and unique contribution. Agents sharing the same prompt, thesis or source packet are not independent confirmations.

## Anti-contamination controls

The system actively tests for rumor stacking, circular sourcing, source laundering, authority mirage, hidden assumption chains, narrative lock-in, selection bias, hindsight bias, false precision and confidence theater.

## Calibration requirements

Scored forecasts require pre-resolution wording, timestamp, probability, range, horizon, resolution criteria, resolution source, reference class, gate, constraint, trigger, falsifier, action state and framework version.

The calibration record must include hits, partials, misses, voids, false alarms, overconfidence, underconfidence, correct outcomes reached through poor reasoning and sound reasoning defeated by irreducible uncertainty.

## Runtime compatibility

- New forecast records default to `framework_version: 2.1.1`.
- Existing records created under v2.0 remain valid historical records and are not silently rewritten.
- The runtime accepts v2.0 and v2.1.1 record versions for continuity.
- Current-state output exposes the originating framework version and canonical gate label.
- The `version` command emits the machine-readable release manifest.

## Public-description rule

Public repositories must not display either of these deprecated descriptions as current:

`SCOUT -> SOURCEGRID -> K-ALIGN -> IPR -> BLACKGLASS -> CRF -> COMMAND -> AURORA GRID -> RECORD LOCK`

or gate labels using `emerging`, `viable pathway` or `near-trigger` for G2–G4.

Legacy case studies may retain historical terms only when clearly labeled with the version used at the time.

## Configuration-management control

A future doctrine update must use a release branch and include:

- one authoritative version identifier;
- a documented change set;
- synchronized code and documentation;
- deterministic taxonomy tests;
- backward-compatibility decision;
- public-reference search;
- pull-request review record;
- merged commit SHA;
- release tag or immutable commit reference;
- deployment or publication verification.

A version is not “publicly synchronized” until these controls are complete. Internal doctrine may be newer than the public release only when explicitly labeled `UNRELEASED` and kept out of public-current claims.

## Current validation boundary

The architecture is specified and partially implemented. Independent prospective benchmarking, external operator testing and a sufficiently large independently resolved forecast set remain necessary before claiming institution-grade empirical validation or demonstrated superiority over established baselines.
