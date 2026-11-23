"""Generate simulated refrigerated-container readings and save them as CSV."""

import csv
import json
import os
import time

from .config import (
    CONTAINER_IDS,
    GENERATION_INTERVAL_SECONDS,
    OUTPUT_FILENAME,
    READINGS_PER_CONTAINER,
)
from .sensor_simulator import create_sensor_state, generate_reading


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIRECTORY = os.path.join(PROJECT_ROOT, "datasets", "processed")
OUTPUT_PATH = os.path.join(OUTPUT_DIRECTORY, OUTPUT_FILENAME)
CSV_FIELDS = ["container_id", "timestamp", "temperature", "humidity", "vibration"]


def generate_data() -> None:
    """Generate readings for all containers, print them, and save a CSV."""
    sensor_states = {
        container_id: create_sensor_state() for container_id in CONTAINER_IDS
    }

    try:
        os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)
        with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDS)
            writer.writeheader()

            for reading_number in range(READINGS_PER_CONTAINER):
                for container_id in CONTAINER_IDS:
                    reading = generate_reading(
                        container_id,
                        sensor_states[container_id],
                    )
                    print(json.dumps(reading, indent=2))
                    writer.writerow(reading)

                if reading_number < READINGS_PER_CONTAINER - 1:
                    time.sleep(GENERATION_INTERVAL_SECONDS)
    except OSError as error:
        raise OSError(f"Could not write simulated data to {OUTPUT_PATH}: {error}") from error

    print(f"\nSaved simulated readings to: {OUTPUT_PATH}")


if __name__ == "__main__":
    generate_data()
