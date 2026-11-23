"""Generate stateful simulated sensor readings."""

import random
from datetime import datetime

from .config import (
    ABNORMAL_HUMIDITY_RANGE,
    ABNORMAL_READING_PROBABILITY,
    ABNORMAL_TEMPERATURE_RANGE,
    ABNORMAL_VIBRATION_RANGE,
    MAX_HUMIDITY_CHANGE,
    MAX_TEMPERATURE_CHANGE,
    MAX_VIBRATION_CHANGE,
    NORMAL_HUMIDITY_RANGE,
    NORMAL_TEMPERATURE_RANGE,
    NORMAL_VIBRATION_RANGE,
)


def create_sensor_state() -> dict:
    """Create the initial normal sensor values for one container."""
    return {
        "temperature": round(random.uniform(*NORMAL_TEMPERATURE_RANGE), 2),
        "humidity": round(random.uniform(*NORMAL_HUMIDITY_RANGE), 2),
        "vibration": round(random.uniform(*NORMAL_VIBRATION_RANGE), 2),
    }


def _next_normal_value(current_value: float, normal_range: tuple, max_change: float) -> float:
    """Move a sensor value slightly while keeping it in its normal range."""
    lower_bound, upper_bound = normal_range
    next_value = current_value + random.uniform(-max_change, max_change)
    next_value = round(max(lower_bound, min(next_value, upper_bound)), 2)

    if next_value == round(current_value, 2) and max_change > 0:
        if current_value + 0.01 <= upper_bound:
            next_value = round(current_value + 0.01, 2)
        else:
            next_value = round(current_value - 0.01, 2)

    return next_value


def generate_reading(container_id: str, sensor_state: dict) -> dict:
    """Generate one reading and update the container's normal sensor state."""
    next_state = {
        "temperature": _next_normal_value(
            sensor_state["temperature"],
            NORMAL_TEMPERATURE_RANGE,
            MAX_TEMPERATURE_CHANGE,
        ),
        "humidity": _next_normal_value(
            sensor_state["humidity"],
            NORMAL_HUMIDITY_RANGE,
            MAX_HUMIDITY_CHANGE,
        ),
        "vibration": _next_normal_value(
            sensor_state["vibration"],
            NORMAL_VIBRATION_RANGE,
            MAX_VIBRATION_CHANGE,
        ),
    }
    sensor_state.update(next_state)

    reading = {
        "container_id": container_id,
        "timestamp": datetime.now().isoformat(timespec="milliseconds"),
        **next_state,
    }

    # Keep anomalies out of the normal state so the next reading resumes its trend.
    if random.random() < ABNORMAL_READING_PROBABILITY:
        abnormal_ranges = {
            "temperature": ABNORMAL_TEMPERATURE_RANGE,
            "humidity": ABNORMAL_HUMIDITY_RANGE,
            "vibration": ABNORMAL_VIBRATION_RANGE,
        }
        sensor_name = random.choice(tuple(abnormal_ranges))
        reading[sensor_name] = round(random.uniform(*abnormal_ranges[sensor_name]), 2)

    return reading
