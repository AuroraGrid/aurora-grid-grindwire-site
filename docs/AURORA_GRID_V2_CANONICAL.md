# AURORA GRID v2.0 — Canonical Operating Architecture

**Status:** Active canonical specification  
**Effective date:** 2026-07-29  
**System owner:** Hasan Raza Kazmi  
**Supersedes:** Public descriptions that treated AURORA GRID as both the complete system and a stage inside its own pipeline.

## System boundary

**AURORA GRID** is the complete decision-intelligence operating system.

- **Luna** expands hypotheses, weak signals, alternative frames, scenarios, and second-order effects.
- **Terra** verifies evidence, provenance, baselines, chronology, mechanisms, and constraints.
- **Sol** synthesizes judgments, probabilities, priorities, and actions while preserving unresolved uncertainty.
- **AAIK** operates across the full system as the evidence, instability, and exposure governor.
- **RECORD LOCK** is the append-only audit, revision, and outcome layer.

## Canonical chain

`ROUTER -> SCOUT -> SOURCEGRID -> K-ALIGN -> IPR -> BLACKGLASS-I -> CRF -> COMMAND -> BLACKGLASS-II -> RECORD LOCK`

### ROUTER
Selects the minimum sufficient workflow based on task type, consequence of error, evidence stability, decision urgency, and publication requirements.

### SCOUT
Defines the baseline, material change, weak signals, collection gaps, decision question, and stop condition.

### SOURCEGRID
Maps source provenance, authenticity, independence, incentives, freshness, contradictions, and common-origin repetition.

### K-ALIGN
Decomposes material statements into claim-level objects and separates claim type, support status, verification status, evidence, assumptions, contradictions, and confidence ceilings.

### IPR
Tests whether a development is structural, temporary, cyclical, local, symbolic, or primarily narrative.

### BLACKGLASS-I
Independently attacks the thesis before forecast finalization. It must be capable of revising or rejecting the original thesis.

### CRF
Builds the forecast from reference class, constraints, dependency graph, gate state, trigger, probability, range, falsifier, and revision conditions.

### COMMAND
Converts the analysis into an action using probability, consequence, reversibility, urgency, cost of delay, information value, authority, and exposure.

### BLACKGLASS-II
Attacks the proposed action rather than only the analytical thesis. It tests sizing, timing, reversibility, operational failure, and safer alternatives.

### RECORD LOCK
Preserves the original judgment, evidence snapshot, assumptions, probability, gate, action, revisions, resolution evidence, and error classification without silent overwriting.

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

- `CONF-G1` — directional
- `CONF-G2` — high confidence
- `CONF-G3` — reserved for resolved outcomes or directly verified factual judgments

An unresolved future outcome cannot be called verified.

### Outcome resolution

- `RES-OPEN`
- `RES-HIT`
- `RES-PARTIAL`
- `RES-MISS`
- `RES-VOID`

### Gate state

- `GATE-G0` — blocked
- `GATE-G1` — latent
- `GATE-G2` — emerging
- `GATE-G3` — viable pathway
- `GATE-G4` — near-trigger
- `GATE-G5` — activated

Gate movement requires timestamped evidence addressing explicit transition conditions. G5 means the pathway is underway, not that completion is guaranteed.

## Source discipline

The source hierarchy remains:

- `SRC-T1` primary records or raw data
- `SRC-T2` official institutions and formal records
- `SRC-T3` strong original reporting
- `SRC-T4` expert or secondary analysis
- `SRC-T5` social, rumor, opaque, or contamination-prone material

Source tier does not equal truth. Each material source must also be evaluated for proximity, authenticity, independence, incentive risk, and freshness.

## Multi-agent rule

Agent count is not a confidence multiplier. Consensus is weighted by evidence quality, independence, mechanism quality, constraint validity, historical calibration, and unique contribution. Agents sharing the same prompt, thesis, or source packet are not independent confirmations.

## Decision states

`MONITOR`, `WAIT`, `INVESTIGATE`, `PREPARE`, `HEDGE`, `TRADE`, `PUBLISH`, `ESCALATE`, `REJECT`

Every material decision must state its owner, authority, exposure, deadline, expiration, stop condition, reversal condition, and reason for acting now.

## Calibration requirements

Scored forecasts require pre-resolution wording, timestamp, probability, range, horizon, resolution criteria, resolution source, reference class, gate, constraint, trigger, falsifier, action state, and framework version.

The calibration record must include hits, partials, misses, voids, false alarms, overconfidence, underconfidence, correct outcomes reached through poor reasoning, and sound reasoning defeated by irreducible uncertainty.

## Public-description rule

Public repositories must no longer display this deprecated chain as canonical:

`SCOUT -> SOURCEGRID -> K-ALIGN -> IPR -> BLACKGLASS -> CRF -> COMMAND -> AURORA GRID -> RECORD LOCK`

Legacy case studies may retain the historical chain when clearly labeled as the version used at the time.

## Current validation boundary

The architecture is specified and partially implemented. Independent prospective benchmarking, external operator testing, and sufficient resolved forecasts remain necessary before claiming institution-grade empirical validation.
