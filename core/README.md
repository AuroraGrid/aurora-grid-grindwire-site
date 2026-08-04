# AURORA GRID OS Core v2.1.1

This directory contains the runnable standard-library implementation of the AURORA GRID OS v2.1.1 public configuration.

## Version contract

- Current runtime version: `2.1.1`
- New forecast default: `framework_version="2.1.1"`
- Historical compatibility: v2.0 records remain accepted and are not silently rewritten
- Canonical specification: [`../docs/AURORA_GRID_V2_CANONICAL.md`](../docs/AURORA_GRID_V2_CANONICAL.md)
- Machine-readable release manifest: [`../release/aurora-grid-v2.1.1.json`](../release/aurora-grid-v2.1.1.json)

## Capabilities

- SQLite forecast, revision, resolution and RECORD LOCK ledger
- append-only RECORD LOCK chain using canonical JSON and SHA-256
- database triggers preventing mutation of locked records
- forecast registration and revision history
- initial and final Brier score calculation
- minimum-sufficient Quick Mode router
- AAIK `OFF`, `NORMAL` and `SPIKE` operating states
- canonical gate labels embedded in runtime output
- machine-readable version and taxonomy manifest
- deterministic configuration and ledger tests

## Canonical workflow

`ROUTER -> SCOUT -> SOURCEGRID -> K-ALIGN -> IPR -> BLACKGLASS-I -> CRF -> COMMAND -> BLACKGLASS-II -> RECORD LOCK`

AAIK operates across the workflow. Luna, Terra and Sol are the cognitive control plane.

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
python -m unittest -v test_core.py
```

The implementation uses only the Python standard library.

## Deterministic validation

The test suite verifies:

- probability increment validation;
- v2.1.1 forecast defaults;
- append-only mutation prevention;
- revision and resolution behavior;
- multi-gate evidence controls;
- hash-chain integrity;
- Brier scoring;
- Quick Mode routing;
- automatic AAIK `SPIKE` routing;
- all 17 Quick Mode identifiers;
- locked G2–G4 gate labels.

## Validation boundary

A working implementation does not establish empirical superiority. Institution-grade validation still requires prospective forecasts, independent resolution, external operators and benchmark comparison.
