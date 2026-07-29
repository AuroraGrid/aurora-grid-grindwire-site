import sqlite3
import tempfile
import unittest
from pathlib import Path

from aurora_grid_core import AuroraGrid, Forecast, route, validate_probability


class AuroraGridCoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Path(self.tmp.name) / "test.db"
        self.grid = AuroraGrid(self.db)

    def tearDown(self):
        self.grid.close()
        self.tmp.cleanup()

    def forecast(self, probability=60, gate="GATE-G3"):
        return Forecast(
            question="Will the pathway activate?",
            probability=probability,
            horizon="2026-12-31",
            resolution_criteria="A controlling primary record confirms activation.",
            gate=gate,
            binding_constraint="Authorization is absent.",
            trigger="Authorization is published.",
            falsifier="The institution formally rejects the pathway.",
            action="MONITOR",
        )

    def test_probability_increment_validation(self):
        self.assertEqual(validate_probability(65), 65)
        with self.assertRaises(ValueError):
            validate_probability(63)

    def test_register_revision_and_chain(self):
        forecast_id = self.grid.register_forecast(self.forecast())
        self.grid.revise_forecast(
            forecast_id,
            70,
            "GATE-G4",
            "Official preparatory action was published.",
            ["SRC-T1:official-record"],
        )
        state = self.grid.current_state(forecast_id)
        self.assertEqual(state["original_probability"], 60)
        self.assertEqual(state["probability"], 70)
        self.assertEqual(state["revision_count"], 1)
        self.assertTrue(self.grid.verify_chain()["valid"])

    def test_multi_gate_jump_requires_multiple_evidence_items(self):
        forecast_id = self.grid.register_forecast(self.forecast(gate="GATE-G1"))
        with self.assertRaises(ValueError):
            self.grid.revise_forecast(
                forecast_id,
                80,
                "GATE-G4",
                "Rapid transition claimed.",
                ["SRC-T1:single-record"],
            )

    def test_append_only_trigger(self):
        forecast_id = self.grid.register_forecast(self.forecast())
        with self.assertRaises(sqlite3.IntegrityError):
            self.grid.conn.execute(
                "UPDATE forecasts SET probability = 95 WHERE id = ?",
                (forecast_id,),
            )

    def test_resolution_and_brier_score(self):
        forecast_id = self.grid.register_forecast(self.forecast(probability=60))
        self.grid.revise_forecast(
            forecast_id,
            70,
            "GATE-G4",
            "New evidence increased activation probability.",
            ["SRC-T1:record"],
        )
        self.grid.resolve_forecast(
            forecast_id,
            "RES-HIT",
            "SRC-T1:controlling-resolution-record",
        )
        score = self.grid.score()
        self.assertEqual(score["n"], 1)
        self.assertEqual(score["initial_brier"], 0.16)
        self.assertEqual(score["final_brier"], 0.09)

    def test_router(self):
        result = route("verify whether this source is authentic")
        self.assertIn("Q03 Verification", result["modes"])
        self.assertEqual(result["governor"], "AAIK")


if __name__ == "__main__":
    unittest.main()
