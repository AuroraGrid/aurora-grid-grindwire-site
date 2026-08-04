# Changelog

All material public changes to AURORA GRID OS are recorded here. Internal doctrine changes that have not completed the release process must be labeled `UNRELEASED` and must not be presented publicly as the active version.

## [2.1.1] — 2026-08-04

### Release purpose

Corrected a configuration-management failure in which the active doctrine had advanced beyond the public specification and executable runtime version.

### Synchronized

- public canonical specification now identifies AURORA GRID OS v2.1.1;
- runtime default for new forecast records changed from `2.0` to `2.1.1`;
- v2.0 retained as an accepted historical record version;
- all 17 Quick Modes registered in code and documentation;
- output modifiers separated from Quick Modes;
- gate labels locked to Blocked, Latent, Forming, Credible Pathway, Trigger-Ready and Activated;
- confidence labels locked to Directional, High Confidence and Verified;
- AAIK states locked to `OFF`, `NORMAL` and `SPIKE`;
- high-consequence or unstable-evidence routing standardized to Full Pipeline, Red-Team and Record Lock under `SPIKE`;
- runtime outputs now identify framework version and canonical gate label;
- machine-readable release manifest added;
- README, core documentation and implementation-status record synchronized.

### Validation

- Python compilation passed;
- eight deterministic unit tests passed locally;
- append-only ledger controls passed;
- hash-chain verification passed;
- Brier scoring tests passed;
- v2.1.1 manifest and taxonomy tests passed;
- AAIK `SPIKE` routing test passed.

### Compatibility

Existing v2.0 records remain valid historical records. They are not silently migrated or rewritten. New records default to v2.1.1.

### Configuration-management control

Future releases require one version identifier across the canonical specification, runtime, tests, manifest, changelog, public references, merged commit and publication state. A doctrine update is not a public release until those surfaces are synchronized and verified.

### Validation boundary

This release synchronizes architecture and executable configuration. It does not establish institution-grade empirical superiority. Independent prospective benchmarking, external operators and sufficient independently resolved forecasts remain required.

## [2.0] — 2026-07-29

### Added

- canonical system boundary;
- canonical workflow;
- runnable Python and SQLite core;
- append-only RECORD LOCK chain;
- revision and resolution ledger;
- Brier scoring;
- minimum-sufficient router;
- deterministic tests and CI.

### Known issue corrected by 2.1.1

The public release did not keep pace with later doctrine and taxonomy changes. The runtime and public specification therefore remained labeled v2.0 after the operating doctrine had advanced.
