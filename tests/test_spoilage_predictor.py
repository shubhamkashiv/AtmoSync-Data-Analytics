"""Tests for environmental baseline assessment."""

import unittest

from iot_simulator.config import (
    NORMAL_HUMIDITY_RANGE,
    NORMAL_TEMPERATURE_RANGE,
    NORMAL_VIBRATION_RANGE,
)
from pipeline.spoilage_predictor import assess_spoilage_risk


class AssessSpoilageRiskTests(unittest.TestCase):
    def setUp(self):
        self.valid_reading = {
            "container_id": "CONTAINER-001",
            "timestamp": "2026-11-23T21:32:27.431",
            "temperature": 4.82,
            "humidity": 72.16,
            "vibration": 0.21,
        }

    def test_all_parameters_within_baselines_are_normal(self):
        result = assess_spoilage_risk(self.valid_reading)

        self.assertEqual(result["status"], "NORMAL")
        self.assertEqual(result["deviation_count"], 0)
        self.assertEqual(result["reasons"], [])
        self.assertEqual(result["container_id"], self.valid_reading["container_id"])
        self.assertEqual(result["timestamp"], self.valid_reading["timestamp"])

    def test_temperature_outside_baseline_is_warning(self):
        reading = self.valid_reading.copy()
        reading["temperature"] = NORMAL_TEMPERATURE_RANGE[1] + 1

        result = assess_spoilage_risk(reading)

        self.assertEqual(result["status"], "WARNING")
        self.assertEqual(result["deviation_count"], 1)
        self.assertIn("temperature", result["reasons"][0])

    def test_humidity_outside_baseline_is_warning(self):
        reading = self.valid_reading.copy()
        reading["humidity"] = NORMAL_HUMIDITY_RANGE[0] - 1

        result = assess_spoilage_risk(reading)

        self.assertEqual(result["status"], "WARNING")
        self.assertEqual(result["deviation_count"], 1)
        self.assertIn("humidity", result["reasons"][0])

    def test_vibration_outside_baseline_is_warning(self):
        reading = self.valid_reading.copy()
        reading["vibration"] = NORMAL_VIBRATION_RANGE[1] + 0.1

        result = assess_spoilage_risk(reading)

        self.assertEqual(result["status"], "WARNING")
        self.assertEqual(result["deviation_count"], 1)
        self.assertIn("vibration", result["reasons"][0])

    def test_multiple_deviations_are_counted(self):
        reading = self.valid_reading.copy()
        reading.update(
            temperature=NORMAL_TEMPERATURE_RANGE[1] + 1,
            humidity=NORMAL_HUMIDITY_RANGE[0] - 1,
            vibration=NORMAL_VIBRATION_RANGE[1] + 0.1,
        )

        result = assess_spoilage_risk(reading)

        self.assertEqual(result["status"], "WARNING")
        self.assertEqual(result["deviation_count"], 3)
        self.assertEqual(len(result["reasons"]), 3)

    def test_invalid_input_returns_validation_errors(self):
        result = assess_spoilage_risk({"container_id": "CONTAINER-001"})

        self.assertEqual(result["status"], "INVALID")
        self.assertEqual(result["container_id"], "CONTAINER-001")
        self.assertEqual(result["deviation_count"], 0)
        self.assertNotIn("timestamp", result)
        self.assertIn("timestamp is required.", result["reasons"])


if __name__ == "__main__":
    unittest.main()
