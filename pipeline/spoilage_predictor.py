"""Assess sensor readings against simulator environmental baselines."""

from iot_simulator.config import (
    NORMAL_HUMIDITY_RANGE,
    NORMAL_TEMPERATURE_RANGE,
    NORMAL_VIBRATION_RANGE,
)
from pipeline.data_validator import validate_sensor_reading


def assess_spoilage_risk(reading):
    """Return a baseline assessment for a sensor reading.

    The configured ranges are simulator environmental baselines, not
    food-specific spoilage thresholds or a scientifically validated prediction.
    """
    validation_result = validate_sensor_reading(reading)
    container_id = reading.get("container_id") if isinstance(reading, dict) else None

    if not validation_result["is_valid"]:
        return {
            "container_id": container_id,
            "status": "INVALID",
            "deviation_count": 0,
            "reasons": validation_result["errors"],
        }

    baselines = (
        ("temperature", NORMAL_TEMPERATURE_RANGE),
        ("humidity", NORMAL_HUMIDITY_RANGE),
        ("vibration", NORMAL_VIBRATION_RANGE),
    )
    reasons = []
    for parameter, (minimum, maximum) in baselines:
        value = reading[parameter]
        if not minimum <= value <= maximum:
            reasons.append(
                f"{parameter} {value} is outside simulator baseline range "
                f"[{minimum}, {maximum}]."
            )

    return {
        "container_id": container_id,
        "timestamp": reading["timestamp"],
        "status": "WARNING" if reasons else "NORMAL",
        "deviation_count": len(reasons),
        "reasons": reasons,
    }
