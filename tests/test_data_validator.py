"""Tests for IoT sensor reading validation."""

import unittest

from pipeline.data_validator import validate_sensor_reading


class ValidateSensorReadingTests(unittest.TestCase):
    def setUp(self):
        self.valid_reading = {
            "container_id": "CONTAINER-001",
            "timestamp": "2026-11-23T21:32:27.431",
            "temperature": 4.82,
            "humidity": 72.16,
            "vibration": 0.21,
        }

    def test_valid_reading(self):
        result = validate_sensor_reading(self.valid_reading)

        self.assertTrue(result["is_valid"])
        self.assertEqual(result["errors"], [])

    def test_missing_fields(self):
        result = validate_sensor_reading({"container_id": "CONTAINER-001"})

        self.assertFalse(result["is_valid"])
        self.assertTrue(
            any("timestamp is required" in error for error in result["errors"])
        )
        self.assertTrue(
            any("temperature is required" in error for error in result["errors"])
        )
        self.assertTrue(
            any("humidity is required" in error for error in result["errors"])
        )
        self.assertTrue(
            any("vibration is required" in error for error in result["errors"])
        )

    def test_invalid_numeric_values(self):
        reading = self.valid_reading.copy()
        reading.update(temperature="warm", humidity="humid", vibration=True)

        result = validate_sensor_reading(reading)

        self.assertFalse(result["is_valid"])
        self.assertTrue(
            any("temperature must be numeric" in error for error in result["errors"])
        )
        self.assertTrue(
            any("humidity must be numeric" in error for error in result["errors"])
        )
        self.assertTrue(
            any("vibration must be numeric" in error for error in result["errors"])
        )

    def test_out_of_range_sensor_values(self):
        reading = self.valid_reading.copy()
        reading.update(temperature=101, humidity=-1, vibration=-0.1)

        result = validate_sensor_reading(reading)

        self.assertFalse(result["is_valid"])
        self.assertTrue(
            any("temperature must be between" in error for error in result["errors"])
        )
        self.assertTrue(
            any("humidity must be between" in error for error in result["errors"])
        )
        self.assertTrue(
            any(
                "vibration must be non-negative" in error
                for error in result["errors"]
            )
        )

    def test_empty_fields_and_invalid_timestamp(self):
        reading = self.valid_reading.copy()
        reading.update(container_id=" ", timestamp="2026-11-23")

        result = validate_sensor_reading(reading)

        self.assertFalse(result["is_valid"])
        self.assertTrue(
            any("container_id must not be empty" in error for error in result["errors"])
        )
        self.assertTrue(
            any("timestamp must be a valid ISO 8601" in error for error in result["errors"])
        )

    def test_boolean_sensor_values_are_rejected(self):
        for field in ("temperature", "humidity", "vibration"):
            for value in (True, False):
                with self.subTest(field=field, value=value):
                    reading = self.valid_reading.copy()
                    reading[field] = value

                    result = validate_sensor_reading(reading)

                    self.assertFalse(result["is_valid"])
                    self.assertTrue(
                        any(
                            f"{field} must be numeric" in error
                            for error in result["errors"]
                        )
                    )

    def test_non_finite_sensor_values_are_rejected(self):
        for field in ("temperature", "humidity", "vibration"):
            for value in (float("nan"), float("inf"), float("-inf")):
                with self.subTest(field=field, value=value):
                    reading = self.valid_reading.copy()
                    reading[field] = value

                    result = validate_sensor_reading(reading)

                    self.assertFalse(result["is_valid"])
                    self.assertTrue(
                        any(
                            f"{field} must be a finite number" in error
                            for error in result["errors"]
                        )
                    )

    def test_non_dictionary_input_is_rejected(self):
        for reading in ("not a reading", []):
            with self.subTest(reading=reading):
                result = validate_sensor_reading(reading)

                self.assertFalse(result["is_valid"])
                self.assertEqual(
                    result["errors"], ["Reading must be a dictionary."]
                )


if __name__ == "__main__":
    unittest.main()
