# AURORA GRID OS Core v2.2.0

This directory contains the runnable standard-library implementation of the AURORA GRID OS v2.2.0 public configuration.

## Version contract

- Current runtime version: `2.2.0`
- New forecast default: `framework_version="2.2.0"`
- Historical compatibility: v2.0 and v2.1.1 records remain accepted and are not silently rewritten
- Canonical specification: [`../docs/AURORA_GRID_V2_CANONICAL.md`](../docs/AURORA_GRID_V2_CANONICAL.md)
- Machine-readable release manifest: [`../release/aurora-grid-v2.2.0.json`](../release/aurora-grid-v2.2.0.json)

## Capabilities

- SQLite forecast, revision, resolution and RECORD LOCK ledger
- append-only RECORD LOCK chain using canonical JSON and SHA-256
- database triggers preventing mutation of locked records
- forecast registration and revision history
- initial and final Brier score calculation
- minimum-sufficient Quick Mode router
- AAIK `OFF`, `NORMAL` and `SPIKE` operating states with enforceable governor logic
- **Cognitive control plane (Luna, Terra, Sol)** with executable boundaries
- AAIK SPIKE probability haircuts, pure T4/T5 rejection, and action downsizing
- canonical gate labels embedded in runtime output
- machine-readable version and taxonomy manifest
- deterministic configuration and ledger tests

## Canonical workflow

`ROUTER -> SCOUT -> SOURCEGRID -> K-ALIGN -> IPR -> BLACKGLASS-I -> CRF -> COMMAND -> BLACKGLASS-II -> RECORD LOCK`

AAIK operates across the workflow. Luna, Terra and Sol are the cognitive control plane and now have executable methods.

## Cognitive Control Plane (v2.2.0)

- **Luna** — expands alternative frames, scenarios and second-order effects
- **Terra** — verifies evidence tiers, flags gaps, detects pure T4/T5 foundations
- **Sol** — synthesizes judgment, applies AAIK haircuts, preserves unresolved uncertainty

## Locked gate taxonomy

- `GATE-G0` Blocked
- `GATE-G1` Latent
- `GATE-G2` Forming
- `GATE-G3` Credible Pathway
- `GATE-G4` Trigger-Ready
- `GATE-G5` Activated

## Run

```bash
cd core
python aurora_grid_core.py version
python aurora_grid_core.py init --db aurora.db
python aurora_grid_core.py demo --db aurora.db
python aurora_grid_core.py verify --db aurora.db
python aurora_grid_core.py route --task "forecast a high-consequence event"
python aurora_grid_core.py cognitive --task "Will the pathway activate?" --probability 70 --aaik SPIKE
python -m unittest -v test_core.py
```

The implementation uses only the Python standard library.

## Deterministic validation

The test suite verifies:

- probability increment validation;
- v2.2.0 forecast defaults;
- append-only mutation prevention;
- revision and resolution behavior;
- multi-gate evidence controls;
- hash-chain integrity;
- Brier scoring;
- Quick Mode routing;
- automatic AAIK `SPIKE` routing;
- all 17 Quick Mode identifiers;
- locked G2–G4 gate labels;
- Luna expansion;
- Terra pure-T4/T5 detection;
- Sol haircut and action downsizing under SPIKE;
- full cognitive_pass pipeline.

## Validation boundary

A working implementation does not establish empirical superiority. Institution-grade validation still requires prospective forecasts, independent resolution, external operators and benchmark comparison.
