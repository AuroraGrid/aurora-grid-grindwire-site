# AURORA GRID Core

This directory is the runnable implementation of the AURORA GRID v2 operating architecture.

## Capabilities

- SQLite evidence, forecast, decision, revision and resolution ledger
- append-only RECORD LOCK chain using canonical JSON and SHA-256
- database triggers preventing mutation of locked records
- forecast registration and revision history
- Brier score calculation
- minimum-sufficient mode router
- command-line interface
- deterministic tests

## Canonical workflow

`ROUTER -> SCOUT -> SOURCEGRID -> K-ALIGN -> IPR -> BLACKGLASS-I -> CRF -> COMMAND -> BLACKGLASS-II -> RECORD LOCK`

AAIK operates across the workflow. Luna, Terra and Sol are the cognitive control plane.

## Run

```bash
cd core
python aurora_grid_core.py init --db aurora.db
python aurora_grid_core.py demo --db aurora.db
python aurora_grid_core.py verify --db aurora.db
python -m unittest -v test_core.py
```

The implementation uses only the Python standard library.

## Validation boundary

A working implementation does not establish empirical superiority. Institution-grade validation still requires prospective forecasts, independent resolution, external operators and benchmark comparison.
