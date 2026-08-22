from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import sys
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CURRENT_FRAMEWORK_VERSION = "2.2.0"
SUPPORTED_FRAMEWORK_VERSIONS = {"2.0", "2.1.1", CURRENT_FRAMEWORK_VERSION}

WORKFLOW = [
    "ROUTER",
    "SCOUT",
    "SOURCEGRID",
    "K-ALIGN",
    "IPR",
    "BLACKGLASS-I",
    "CRF",
    "COMMAND",
    "BLACKGLASS-II",
    "RECORD LOCK",
]

QUICK_MODES = {
    "Q01": "Full Pipeline",
    "Q02": "Fast Signal Check",
    "Q03": "Verification",
    "Q04": "Source Audit",
    "Q05": "Timeline Build",
    "Q06": "Claim Decomposition",
    "Q07": "Inflection Point",
    "Q08": "Constraint Forecast",
    "Q09": "Red-Team",
    "Q10": "Attack",
    "Q11": "Scenario/Wargame",
    "Q12": "Network Power Map",
    "Q13": "Risk Price",
    "Q14": "Compare",
    "Q15": "LIVE PASS",
    "Q16": "Publishable Research",
    "Q17": "Record Lock",
}

GATE_LABELS = {
    "GATE-G0": "Blocked",
    "GATE-G1": "Latent",
    "GATE-G2": "Forming",
    "GATE-G3": "Credible Pathway",
    "GATE-G4": "Trigger-Ready",
    "GATE-G5": "Activated",
}
GATES = set(GATE_LABELS)

ACTIONS = {
    "MONITOR",
    "WAIT",
    "REJECT",
    "INVESTIGATE",
    "HEDGE",
    "TRADE",
    "PUBLISH",
    "ESCALATE",
    "PREPARE",
}
AAIK_STATES = {"OFF", "NORMAL", "SPIKE"}
RESOLUTIONS = {"RES-OPEN", "RES-HIT", "RES-PARTIAL", "RES-MISS", "RES-VOID"}

SOURCE_TIERS = {
    "SRC-T1": "primary records or raw data",
    "SRC-T2": "official institutions and formal records",
    "SRC-T3": "strong original reporting",
    "SRC-T4": "expert or secondary analysis",
    "SRC-T5": "social, rumor, opaque or contamination-prone material",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def validate_probability(value: int) -> int:
    if not isinstance(value, int) or value < 0 or value > 100:
        raise ValueError("probability must be an integer from 0 to 100")
    if value % 5 != 0:
        raise ValueError("probability must use 5-point increments")
    return value


def validate_framework_version(value: str) -> str:
    if value not in SUPPORTED_FRAMEWORK_VERSIONS:
        raise ValueError(
            f"unsupported framework version: {value}; "
            f"supported versions: {sorted(SUPPORTED_FRAMEWORK_VERSIONS)}"
        )
    return value


def manifest() -> dict[str, Any]:
    return {
        "framework": "AURORA GRID OS",
        "framework_version": CURRENT_FRAMEWORK_VERSION,
        "workflow": WORKFLOW,
        "quick_modes": QUICK_MODES,
        "gate_labels": GATE_LABELS,
        "aaik_states": sorted(AAIK_STATES),
        "actions": sorted(ACTIONS),
        "resolutions": sorted(RESOLUTIONS),
        "cognitive_control_plane": ["Luna", "Terra", "Sol"],
        "source_tiers": SOURCE_TIERS,
    }


# ---------------------------------------------------------------------------
# Cognitive Control Plane (v2.2.0)
# ---------------------------------------------------------------------------

class Luna:
    """Expands hypotheses, alternative frames, scenarios and second-order effects."""

    @staticmethod
    def expand(task: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        task_l = task.lower().strip()
        frames = [
            "baseline continuation",
            "accelerated pathway",
            "blocked or reversed pathway",
        ]
        if any(w in task_l for w in ("war", "conflict", "attack", "military")):
            frames.extend(["escalation cascade", "de-escalation window", "proxy displacement"])
        if any(w in task_l for w in ("market", "price", "trade", "oil", "rate")):
            frames.extend(["supply shock", "demand collapse", "policy intervention"])
        second_order = [
            "information cascade / narrative lock-in",
            "authority reaction lag",
            "hidden constraint activation",
        ]
        return {
            "role": "Luna",
            "task": task,
            "alternative_frames": frames,
            "second_order_effects": second_order,
            "weak_signals_to_watch": ["source independence shift", "timing compression", "new primary record"],
            "boundary": "does not outrun evidence",
        }


class Terra:
    """Verifies evidence, provenance, baselines and operational realism."""

    @staticmethod
    def verify(evidence: list[str]) -> dict[str, Any]:
        if not evidence:
            return {
                "role": "Terra",
                "status": "INCOMPLETE",
                "tiers_present": [],
                "gaps": ["no evidence supplied"],
                "pure_t4_t5": False,
                "boundary": "incomplete record is not stable truth",
            }
        tiers = set()
        for item in evidence:
            item_u = item.upper()
            for t in ("SRC-T1", "SRC-T2", "SRC-T3", "SRC-T4", "SRC-T5"):
                if t in item_u:
                    tiers.add(t)
        pure_t4_t5 = bool(tiers) and tiers.issubset({"SRC-T4", "SRC-T5"})
        gaps = []
        if "SRC-T1" not in tiers and "SRC-T2" not in tiers:
            gaps.append("no primary or official record")
        if pure_t4_t5:
            gaps.append("foundation is exclusively T4/T5")
        return {
            "role": "Terra",
            "status": "GAPPED" if gaps else "ADEQUATE",
            "tiers_present": sorted(tiers),
            "gaps": gaps,
            "pure_t4_t5": pure_t4_t5,
            "boundary": "incomplete record is not stable truth",
        }


class Sol:
    """Synthesizes judgments, probabilities, priorities and actions."""

    @staticmethod
    def synthesize(
        luna: dict[str, Any],
        terra: dict[str, Any],
        probability: int,
        action: str = "MONITOR",
        aaik_state: str = "NORMAL",
    ) -> dict[str, Any]:
        validate_probability(probability)
        adjusted = probability
        notes = []
        if aaik_state == "SPIKE":
            if terra.get("pure_t4_t5"):
                notes.append("AAIK SPIKE: pure T4/T5 foundation rejected for consequential claim")
                adjusted = min(adjusted, 30)
            else:
                adjusted = max(5, min(95, adjusted - 10))
                notes.append("AAIK SPIKE: probability haircut applied (-10)")
            if action in {"TRADE", "PUBLISH", "ESCALATE"}:
                action = "HEDGE"
                notes.append("AAIK SPIKE: action downsized to HEDGE")
        return {
            "role": "Sol",
            "probability": adjusted,
            "original_probability": probability,
            "action": action,
            "aaik_state": aaik_state,
            "luna_frames": luna.get("alternative_frames", []),
            "terra_status": terra.get("status"),
            "terra_gaps": terra.get("gaps", []),
            "notes": notes,
            "boundary": "preserves unresolved uncertainty",
        }


def cognitive_pass(
    task: str,
    evidence: list[str] | None = None,
    probability: int = 50,
    action: str = "MONITOR",
    aaik_state: str = "NORMAL",
) -> dict[str, Any]:
    """Run the full cognitive control plane in order: Luna → Terra → Sol."""
    luna_out = Luna.expand(task)
    terra_out = Terra.verify(evidence or [])
    sol_out = Sol.synthesize(luna_out, terra_out, probability, action, aaik_state)
    return {
        "framework_version": CURRENT_FRAMEWORK_VERSION,
        "luna": luna_out,
        "terra": terra_out,
        "sol": sol_out,
    }


# ---------------------------------------------------------------------------
# AAIK Governor helpers (v2.2.0)
# ---------------------------------------------------------------------------

def aaik_apply(
    probability: int,
    evidence: list[str],
    action: str = "MONITOR",
    aaik_state: str = "NORMAL",
) -> dict[str, Any]:
    """Apply AAIK evidence haircuts and exposure controls."""
    terra = Terra.verify(evidence)
    return Sol.synthesize(
        Luna.expand("aaik application"),
        terra,
        probability,
        action,
        aaik_state,
    )


@dataclass(frozen=True)
class Forecast:
    question: str
    probability: int
    horizon: str
    resolution_criteria: str
    gate: str
    binding_constraint: str
    trigger: str
    falsifier: str
    action: str = "MONITOR"
    framework_version: str = CURRENT_FRAMEWORK_VERSION

    def validate(self) -> None:
        validate_probability(self.probability)
        validate_framework_version(self.framework_version)
        if self.gate not in GATES:
            raise ValueError(f"invalid gate: {self.gate}")
        if self.action not in ACTIONS:
            raise ValueError(f"invalid action: {self.action}")
        for field, value in asdict(self).items():
            if field != "probability" and not str(value).strip():
                raise ValueError(f"{field} is required")


SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS forecasts (
    id TEXT PRIMARY KEY,
    created_at TEXT NOT NULL,
    payload TEXT NOT NULL,
    probability INTEGER NOT NULL CHECK(probability BETWEEN 0 AND 100),
    gate TEXT NOT NULL,
    action TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'RES-OPEN'
);
CREATE TABLE IF NOT EXISTS revisions (
    id TEXT PRIMARY KEY,
    forecast_id TEXT NOT NULL REFERENCES forecasts(id),
    created_at TEXT NOT NULL,
    old_probability INTEGER NOT NULL,
    new_probability INTEGER NOT NULL,
    old_gate TEXT NOT NULL,
    new_gate TEXT NOT NULL,
    reason TEXT NOT NULL,
    evidence TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS resolutions (
    id TEXT PRIMARY KEY,
    forecast_id TEXT NOT NULL UNIQUE REFERENCES forecasts(id),
    created_at TEXT NOT NULL,
    outcome TEXT NOT NULL,
    resolution_source TEXT NOT NULL,
    notes TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS record_locks (
    sequence INTEGER PRIMARY KEY AUTOINCREMENT,
    id TEXT UNIQUE NOT NULL,
    created_at TEXT NOT NULL,
    record_type TEXT NOT NULL,
    record_id TEXT NOT NULL,
    payload TEXT NOT NULL,
    payload_hash TEXT NOT NULL,
    previous_hash TEXT NOT NULL,
    record_hash TEXT NOT NULL
);
CREATE TRIGGER IF NOT EXISTS forecasts_no_update BEFORE UPDATE ON forecasts
BEGIN SELECT RAISE(ABORT, 'forecasts are append-only; use revisions or resolutions'); END;
CREATE TRIGGER IF NOT EXISTS forecasts_no_delete BEFORE DELETE ON forecasts
BEGIN SELECT RAISE(ABORT, 'forecasts are append-only'); END;
CREATE TRIGGER IF NOT EXISTS revisions_no_update BEFORE UPDATE ON revisions
BEGIN SELECT RAISE(ABORT, 'revisions are append-only'); END;
CREATE TRIGGER IF NOT EXISTS revisions_no_delete BEFORE DELETE ON revisions
BEGIN SELECT RAISE(ABORT, 'revisions are append-only'); END;
CREATE TRIGGER IF NOT EXISTS resolutions_no_update BEFORE UPDATE ON resolutions
BEGIN SELECT RAISE(ABORT, 'resolutions are append-only'); END;
CREATE TRIGGER IF NOT EXISTS resolutions_no_delete BEFORE DELETE ON resolutions
BEGIN SELECT RAISE(ABORT, 'resolutions are append-only'); END;
CREATE TRIGGER IF NOT EXISTS locks_no_update BEFORE UPDATE ON record_locks
BEGIN SELECT RAISE(ABORT, 'record locks are append-only'); END;
CREATE TRIGGER IF NOT EXISTS locks_no_delete BEFORE DELETE ON record_locks
BEGIN SELECT RAISE(ABORT, 'record locks are append-only'); END;
"""


class AuroraGrid:
    def __init__(self, db_path: str | Path = "aurora.db") -> None:
        self.db_path = str(db_path)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)

    def close(self) -> None:
        self.conn.close()

    def _lock(self, record_type: str, record_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        payload_text = canonical_json(payload)
        payload_hash = sha256_text(payload_text)
        previous = self.conn.execute(
            "SELECT record_hash FROM record_locks ORDER BY sequence DESC LIMIT 1"
        ).fetchone()
        previous_hash = previous["record_hash"] if previous else "GENESIS"
        created_at = utc_now()
        lock_id = str(uuid.uuid4())
        material = {
            "id": lock_id,
            "created_at": created_at,
            "record_type": record_type,
            "record_id": record_id,
            "payload_hash": payload_hash,
            "previous_hash": previous_hash,
        }
        record_hash = sha256_text(canonical_json(material))
        self.conn.execute(
            """INSERT INTO record_locks
            (id, created_at, record_type, record_id, payload, payload_hash, previous_hash, record_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                lock_id,
                created_at,
                record_type,
                record_id,
                payload_text,
                payload_hash,
                previous_hash,
                record_hash,
            ),
        )
        return {**material, "record_hash": record_hash}

    def register_forecast(self, forecast: Forecast) -> str:
        forecast.validate()
        forecast_id = str(uuid.uuid4())
        created_at = utc_now()
        payload = asdict(forecast)
        self.conn.execute(
            "INSERT INTO forecasts (id, created_at, payload, probability, gate, action) VALUES (?, ?, ?, ?, ?, ?)",
            (
                forecast_id,
                created_at,
                canonical_json(payload),
                forecast.probability,
                forecast.gate,
                forecast.action,
            ),
        )
        self._lock("forecast", forecast_id, {"id": forecast_id, "created_at": created_at, **payload})
        self.conn.commit()
        return forecast_id

    def revise_forecast(
        self,
        forecast_id: str,
        probability: int,
        gate: str,
        reason: str,
        evidence: list[str],
    ) -> str:
        validate_probability(probability)
        if gate not in GATES:
            raise ValueError(f"invalid gate: {gate}")
        if not reason.strip() or not evidence:
            raise ValueError("revision reason and evidence are required")
        current = self.current_state(forecast_id)
        if current["status"] != "RES-OPEN":
            raise ValueError("resolved forecasts cannot be revised")
        old_index = int(current["gate"].split("G")[-1])
        new_index = int(gate.split("G")[-1])
        if abs(new_index - old_index) > 1 and len(evidence) < 2:
            raise ValueError("multi-gate jumps require at least two evidence references")
        revision_id = str(uuid.uuid4())
        created_at = utc_now()
        payload = {
            "id": revision_id,
            "forecast_id": forecast_id,
            "created_at": created_at,
            "old_probability": current["probability"],
            "new_probability": probability,
            "old_gate": current["gate"],
            "new_gate": gate,
            "reason": reason,
            "evidence": evidence,
        }
        self.conn.execute(
            """INSERT INTO revisions
            (id, forecast_id, created_at, old_probability, new_probability, old_gate, new_gate, reason, evidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                revision_id,
                forecast_id,
                created_at,
                current["probability"],
                probability,
                current["gate"],
                gate,
                reason,
                canonical_json(evidence),
            ),
        )
        self._lock("revision", revision_id, payload)
        self.conn.commit()
        return revision_id

    def resolve_forecast(
        self,
        forecast_id: str,
        outcome: str,
        resolution_source: str,
        notes: str = "",
    ) -> str:
        if outcome not in RESOLUTIONS - {"RES-OPEN"}:
            raise ValueError(f"invalid final outcome: {outcome}")
        self.current_state(forecast_id)
        resolution_id = str(uuid.uuid4())
        created_at = utc_now()
        payload = {
            "id": resolution_id,
            "forecast_id": forecast_id,
            "created_at": created_at,
            "outcome": outcome,
            "resolution_source": resolution_source,
            "notes": notes,
        }
        self.conn.execute(
            "INSERT INTO resolutions (id, forecast_id, created_at, outcome, resolution_source, notes) VALUES (?, ?, ?, ?, ?, ?)",
            (resolution_id, forecast_id, created_at, outcome, resolution_source, notes),
        )
        self._lock("resolution", resolution_id, payload)
        self.conn.commit()
        return resolution_id

    def current_state(self, forecast_id: str) -> dict[str, Any]:
        base = self.conn.execute("SELECT * FROM forecasts WHERE id = ?", (forecast_id,)).fetchone()
        if not base:
            raise KeyError(f"forecast not found: {forecast_id}")
        latest = self.conn.execute(
            "SELECT * FROM revisions WHERE forecast_id = ? ORDER BY created_at DESC, rowid DESC LIMIT 1",
            (forecast_id,),
        ).fetchone()
        resolution = self.conn.execute(
            "SELECT outcome FROM resolutions WHERE forecast_id = ?", (forecast_id,)
        ).fetchone()
        count = self.conn.execute(
            "SELECT COUNT(*) AS n FROM revisions WHERE forecast_id = ?", (forecast_id,)
        ).fetchone()["n"]
        payload = json.loads(base["payload"])
        return {
            "id": forecast_id,
            "question": payload["question"],
            "framework_version": payload.get("framework_version", "2.0"),
            "original_probability": base["probability"],
            "probability": latest["new_probability"] if latest else base["probability"],
            "original_gate": base["gate"],
            "gate": latest["new_gate"] if latest else base["gate"],
            "gate_label": GATE_LABELS[latest["new_gate"] if latest else base["gate"]],
            "action": base["action"],
            "status": resolution["outcome"] if resolution else "RES-OPEN",
            "revision_count": count,
        }

    def verify_chain(self) -> dict[str, Any]:
        rows = self.conn.execute("SELECT * FROM record_locks ORDER BY sequence").fetchall()
        expected_previous = "GENESIS"
        errors: list[str] = []
        for row in rows:
            payload_hash = sha256_text(row["payload"])
            if payload_hash != row["payload_hash"]:
                errors.append(f"sequence {row['sequence']}: payload hash mismatch")
            if row["previous_hash"] != expected_previous:
                errors.append(f"sequence {row['sequence']}: previous hash mismatch")
            material = {
                "id": row["id"],
                "created_at": row["created_at"],
                "record_type": row["record_type"],
                "record_id": row["record_id"],
                "payload_hash": row["payload_hash"],
                "previous_hash": row["previous_hash"],
            }
            if sha256_text(canonical_json(material)) != row["record_hash"]:
                errors.append(f"sequence {row['sequence']}: record hash mismatch")
            expected_previous = row["record_hash"]
        return {
            "framework_version": CURRENT_FRAMEWORK_VERSION,
            "valid": not errors,
            "entries": len(rows),
            "errors": errors,
        }

    def score(self) -> dict[str, Any]:
        rows = self.conn.execute(
            """SELECT f.id, f.probability AS initial_probability,
            COALESCE((SELECT new_probability FROM revisions r WHERE r.forecast_id=f.id ORDER BY created_at DESC, rowid DESC LIMIT 1), f.probability) AS final_probability,
            x.outcome FROM forecasts f JOIN resolutions x ON x.forecast_id=f.id
            WHERE x.outcome IN ('RES-HIT','RES-MISS')"""
        ).fetchall()
        if not rows:
            return {
                "framework_version": CURRENT_FRAMEWORK_VERSION,
                "n": 0,
                "initial_brier": None,
                "final_brier": None,
            }

        def outcome_value(outcome: str) -> float:
            return 1.0 if outcome == "RES-HIT" else 0.0

        initial = sum(
            ((row["initial_probability"] / 100) - outcome_value(row["outcome"])) ** 2
            for row in rows
        ) / len(rows)
        final = sum(
            ((row["final_probability"] / 100) - outcome_value(row["outcome"])) ** 2
            for row in rows
        ) / len(rows)
        return {
            "framework_version": CURRENT_FRAMEWORK_VERSION,
            "n": len(rows),
            "initial_brier": round(initial, 6),
            "final_brier": round(final, 6),
        }


def mode(code: str) -> str:
    return f"{code} {QUICK_MODES[code]}"


def route(
    task: str,
    consequence: str = "medium",
    evidence_stability: str = "mixed",
    aaik_state: str | None = None,
) -> dict[str, Any]:
    task_normalized = task.lower().strip()
    consequence_normalized = consequence.lower().strip()
    stability_normalized = evidence_stability.lower().strip()

    if aaik_state is None:
        resolved_aaik_state = (
            "SPIKE"
            if consequence_normalized == "high" or stability_normalized == "unstable"
            else "NORMAL"
        )
    else:
        resolved_aaik_state = aaik_state.upper().strip()
        if resolved_aaik_state not in AAIK_STATES:
            raise ValueError(f"invalid AAIK state: {aaik_state}")

    modes = [mode("Q02")]
    if any(word in task_normalized for word in ("verify", "true", "fake", "authentic")):
        modes = [mode("Q03"), mode("Q04")]
    elif any(word in task_normalized for word in ("source audit", "provenance", "source chain")):
        modes = [mode("Q04")]
    elif any(word in task_normalized for word in ("timeline", "chronology")):
        modes = [mode("Q05")]
    elif any(word in task_normalized for word in ("decompose", "claim decomposition")):
        modes = [mode("Q06")]
    elif any(word in task_normalized for word in ("inflection", "structural change")):
        modes = [mode("Q07"), mode("Q09")]
    elif any(word in task_normalized for word in ("forecast", "probability", "predict")):
        modes = [mode("Q08"), mode("Q09")]
    elif any(word in task_normalized for word in ("attack", "break this")):
        modes = [mode("Q10")]
    elif any(word in task_normalized for word in ("scenario", "wargame")):
        modes = [mode("Q11")]
    elif any(word in task_normalized for word in ("network power", "power map", "influence map")):
        modes = [mode("Q12")]
    elif any(word in task_normalized for word in ("risk price", "price the risk", "trade")):
        modes = [mode("Q13")]
    elif any(word in task_normalized for word in ("compare", " versus ", " vs ")):
        modes = [mode("Q14")]
    elif any(word in task_normalized for word in ("live pass", "update live", "monitor live")):
        modes = [mode("Q15")]
    elif any(word in task_normalized for word in ("publish", "report", "research")):
        modes = [mode("Q16"), mode("Q17")]
    elif any(word in task_normalized for word in ("record lock", "lock the record")):
        modes = [mode("Q17")]

    if resolved_aaik_state == "SPIKE":
        modes = [mode("Q01"), mode("Q09"), mode("Q17")]

    return {
        "framework_version": CURRENT_FRAMEWORK_VERSION,
        "modes": modes,
        "workflow": WORKFLOW,
        "governor": "AAIK",
        "aaik_state": resolved_aaik_state,
        "cognitive_control_plane": ["Luna", "Terra", "Sol"],
    }


def demo(grid: AuroraGrid) -> dict[str, Any]:
    forecast = Forecast(
        question="Will the monitored pathway activate before the stated horizon?",
        probability=60,
        horizon="2026-12-31",
        resolution_criteria="Controlling primary record confirms activation before the horizon.",
        gate="GATE-G3",
        binding_constraint="Required institutional authorization has not yet been issued.",
        trigger="Official authorization is published.",
        falsifier="Authorizing institution formally rejects the pathway.",
        action="MONITOR",
    )
    forecast_id = grid.register_forecast(forecast)
    grid.revise_forecast(
        forecast_id,
        70,
        "GATE-G4",
        "New official preparatory action",
        ["SRC-T1:demo-record"],
    )
    state = grid.current_state(forecast_id)
    return {
        "framework_version": CURRENT_FRAMEWORK_VERSION,
        "forecast": state,
        "chain": grid.verify_chain(),
        "cognitive": cognitive_pass(
            "Will the monitored pathway activate before the stated horizon?",
            evidence=["SRC-T1:demo-record"],
            probability=70,
            aaik_state="NORMAL",
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="AURORA GRID OS v2.2.0 core ledger")
    parser.add_argument(
        "command",
        choices=["init", "demo", "verify", "route", "score", "version", "cognitive"],
    )
    parser.add_argument("--db", default="aurora.db")
    parser.add_argument("--task", default="verify a consequential claim")
    parser.add_argument("--probability", type=int, default=50)
    parser.add_argument("--aaik", default="NORMAL")
    args = parser.parse_args(argv)

    if args.command == "version":
        print(json.dumps(manifest(), indent=2, sort_keys=True))
        return 0

    if args.command == "cognitive":
        result = cognitive_pass(
            args.task,
            evidence=[],
            probability=args.probability,
            aaik_state=args.aaik,
        )
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0

    grid = AuroraGrid(args.db)
    try:
        if args.command == "init":
            result = {"initialized": args.db, **manifest()}
        elif args.command == "demo":
            result = demo(grid)
        elif args.command == "verify":
            result = grid.verify_chain()
        elif args.command == "route":
            result = route(args.task)
        else:
            result = grid.score()
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    finally:
        grid.close()


if __name__ == "__main__":
    sys.exit(main())
