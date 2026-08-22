"""Minimal counterfactual helper for AURORA GRID OS v2.2.0.

Generates structured "what if X had been different" probes that can be fed
into BLACKGLASS-I / Scenario work. Deterministic and standard-library only.
"""

from __future__ import annotations

from typing import Any


def generate_counterfactuals(
    thesis: str,
    key_assumptions: list[str] | None = None,
    binding_constraint: str | None = None,
) -> dict[str, Any]:
    """Return a structured set of counterfactual probes.

    Does not claim the counterfactuals are true. It only surfaces the
    alternative worlds that should be attacked or tested.
    """
    assumptions = key_assumptions or ["primary evidence holds", "binding constraint remains active"]
    probes = []

    for i, assumption in enumerate(assumptions, start=1):
        probes.append({
            "id": f"CF-{i:02d}",
            "type": "assumption_negation",
            "prompt": f"What if the following assumption is false: {assumption}?",
            "original_assumption": assumption,
        })

    if binding_constraint:
        probes.append({
            "id": f"CF-{len(probes)+1:02d}",
            "type": "constraint_removal",
            "prompt": f"What if the binding constraint is removed or overcome: {binding_constraint}?",
            "original_constraint": binding_constraint,
        })

    probes.append({
        "id": f"CF-{len(probes)+1:02d}",
        "type": "opposite_outcome",
        "prompt": f"What if the opposite of the thesis occurs: NOT ({thesis})?",
        "original_thesis": thesis,
    })

    probes.append({
        "id": f"CF-{len(probes)+1:02d}",
        "type": "timing_shift",
        "prompt": "What if the critical timing is delayed by one full decision cycle?",
    })

    return {
        "framework_version": "2.2.0",
        "role": "Counterfactual",
        "thesis": thesis,
        "probes": probes,
        "usage": "Feed selected probes into BLACKGLASS-I, Q09 Red-Team, or Q11 Scenario/Wargame. Do not treat probes as evidence.",
        "boundary": "Counterfactuals expand the attack surface; they do not raise confidence by themselves.",
    }
