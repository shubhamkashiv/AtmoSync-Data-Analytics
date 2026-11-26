"""Validation helpers for IoT sensor readings."""

import math
from datetime import datetime


REQUIRED_FIELDS = (
    "container_id",
    "timestamp",
    "temperature",
    "humidity",
    "vibration",
)


def validate_sensor_reading(reading):
    """Validate a sensor reading and return its validity and any errors."""
    errors = []

    if not isinstance(reading, dict):
        return {
            "is_valid": False,
            "errors": ["Reading must be a dictionary."],
        }

    for field in REQUIRED_FIELDS:
        if field not in reading:
            errors.append(f"{field} is required.")
        elif reading[field] is None or (
            isinstance(reading[field], str) and not reading[field].strip()
        ):
            errors.append(f"{field} must not be empty.")

    container_id = reading.get("container_id")
    if container_id is not None and not isinstance(container_id, str):
        errors.append("container_id must be a non-empty string.")

    timestamp = reading.get("timestamp")
    if timestamp is not None and not (
        isinstance(timestamp, str) and not timestamp.strip()
    ):
        if not isinstance(timestamp, str):
            errors.append("timestamp must be a valid ISO 8601 datetime string.")
        else:
            try:
                if "T" not in timestamp.upper() and " " not in timestamp:
                    raise ValueError
                datetime.fromisoformat(timestamp)
            except ValueError:
                errors.append(
                    "timestamp must be a valid ISO 8601 datetime string."
                )

    limits = {
        "temperature": (-50, 100, "\u00b0C"),
        "humidity": (0, 100, "%"),
        "vibration": (0, None, ""),
    }
    for field, (minimum, maximum, unit) in limits.items():
        value = reading.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            continue
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            errors.append(f"{field} must be numeric.")
            continue
        if isinstance(value, float) and not math.isfinite(value):
            errors.append(f"{field} must be a finite number.")
            continue
        if value < minimum or (maximum is not None and value > maximum):
            if maximum is None:
                errors.append(f"{field} must be non-negative.")
            else:
                errors.append(
                    f"{field} must be between {minimum} and {maximum}{unit}."
                )

    return {"is_valid": not errors, "errors": errors}
