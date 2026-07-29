from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import sys
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

WORKFLOW = [
    "ROUTER", "SCOUT", "SOURCEGRID", "K-ALIGN", "IPR",
    "BLACKGLASS-I", "CRF", "COMMAND", "BLACKGLASS-II", "RECORD LOCK",
]
ACTIONS = {"MONITOR", "WAIT", "INVESTIGATE", "PREPARE", "HEDGE", "TRADE", "PUBLISH", "ESCALATE", "REJECT"}
GATES = {f"GATE-G{i}" for i in range(6)}
RESOLUTIONS = {"RES-OPEN", "RES-HIT", "RES-PARTIAL", "RES-MISS", "RES-VOID"}


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
    framework_version: str = "2.0"

    def validate(self) -> None:
        validate_probability(self.probability)
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
            (lock_id, created_at, record_type, record_id, payload_text, payload_hash, previous_hash, record_hash),
        )
        return {**material, "record_hash": record_hash}

    def register_forecast(self, forecast: Forecast) -> str:
        forecast.validate()
        forecast_id = str(uuid.uuid4())
        created_at = utc_now()
        payload = asdict(forecast)
        self.conn.execute(
            "INSERT INTO forecasts (id, created_at, payload, probability, gate, action) VALUES (?, ?, ?, ?, ?, ?)",
            (forecast_id, created_at, canonical_json(payload), forecast.probability, forecast.gate, forecast.action),
        )
        self._lock("forecast", forecast_id, {"id": forecast_id, "created_at": created_at, **payload})
        self.conn.commit()
        return forecast_id

    def revise_forecast(self, forecast_id: str, probability: int, gate: str, reason: str, evidence: list[str]) -> str:
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
            (revision_id, forecast_id, created_at, current["probability"], probability, current["gate"], gate, reason, canonical_json(evidence)),
        )
        self._lock("revision", revision_id, payload)
        self.conn.commit()
        return revision_id

    def resolve_forecast(self, forecast_id: str, outcome: str, resolution_source: str, notes: str = "") -> str:
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
        resolution = self.conn.execute("SELECT outcome FROM resolutions WHERE forecast_id = ?", (forecast_id,)).fetchone()
        count = self.conn.execute("SELECT COUNT(*) AS n FROM revisions WHERE forecast_id = ?", (forecast_id,)).fetchone()["n"]
        payload = json.loads(base["payload"])
        return {
            "id": forecast_id,
            "question": payload["question"],
            "original_probability": base["probability"],
            "probability": latest["new_probability"] if latest else base["probability"],
            "original_gate": base["gate"],
            "gate": latest["new_gate"] if latest else base["gate"],
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
                "id": row["id"], "created_at": row["created_at"], "record_type": row["record_type"],
                "record_id": row["record_id"], "payload_hash": row["payload_hash"], "previous_hash": row["previous_hash"],
            }
            if sha256_text(canonical_json(material)) != row["record_hash"]:
                errors.append(f"sequence {row['sequence']}: record hash mismatch")
            expected_previous = row["record_hash"]
        return {"valid": not errors, "entries": len(rows), "errors": errors}

    def score(self) -> dict[str, Any]:
        rows = self.conn.execute(
            """SELECT f.id, f.probability AS initial_probability,
            COALESCE((SELECT new_probability FROM revisions r WHERE r.forecast_id=f.id ORDER BY created_at DESC, rowid DESC LIMIT 1), f.probability) AS final_probability,
            x.outcome FROM forecasts f JOIN resolutions x ON x.forecast_id=f.id
            WHERE x.outcome IN ('RES-HIT','RES-MISS')"""
        ).fetchall()
        if not rows:
            return {"n": 0, "initial_brier": None, "final_brier": None}
        def outcome_value(outcome: str) -> float:
            return 1.0 if outcome == "RES-HIT" else 0.0
        initial = sum(((r["initial_probability"] / 100) - outcome_value(r["outcome"])) ** 2 for r in rows) / len(rows)
        final = sum(((r["final_probability"] / 100) - outcome_value(r["outcome"])) ** 2 for r in rows) / len(rows)
        return {"n": len(rows), "initial_brier": round(initial, 6), "final_brier": round(final, 6)}


def route(task: str, consequence: str = "medium", evidence_stability: str = "mixed") -> dict[str, Any]:
    task = task.lower().strip()
    consequence = consequence.lower().strip()
    modes = ["Q02 Fast Signal Check"]
    if any(word in task for word in ("verify", "true", "fake", "source")):
        modes = ["Q03 Verification", "Q04 Source Audit"]
    elif any(word in task for word in ("forecast", "probability", "predict")):
        modes = ["Q08 Constraint Forecast", "Q09 Red-Team"]
    elif any(word in task for word in ("publish", "report", "research")):
        modes = ["Q16 Publishable Research", "Q17 Record Lock"]
    if consequence == "high" or evidence_stability == "unstable":
        modes = ["Q01 Full Pipeline", "Q09 Red-Team", "Q17 Record Lock"]
    return {"modes": modes, "workflow": WORKFLOW, "governor": "AAIK"}


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
    grid.revise_forecast(forecast_id, 70, "GATE-G4", "New official preparatory action", ["SRC-T1:demo-record"])
    state = grid.current_state(forecast_id)
    return {"forecast": state, "chain": grid.verify_chain()}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="AURORA GRID v2 core ledger")
    parser.add_argument("command", choices=["init", "demo", "verify", "route", "score"])
    parser.add_argument("--db", default="aurora.db")
    parser.add_argument("--task", default="verify a consequential claim")
    args = parser.parse_args(argv)
    grid = AuroraGrid(args.db)
    try:
        if args.command == "init":
            result = {"initialized": args.db, "workflow": WORKFLOW}
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
