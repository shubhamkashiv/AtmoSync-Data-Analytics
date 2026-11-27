"""Send simulated sensor readings to the local Kafka broker."""

import sys
import time

from kafka import KafkaProducer
from kafka.errors import KafkaError
from kafka.serializer import DefaultSerializer, JsonSerializer

from iot_simulator.config import (
    CONTAINER_IDS,
    GENERATION_INTERVAL_SECONDS,
    READINGS_PER_CONTAINER,
)
from iot_simulator.sensor_simulator import create_sensor_state, generate_reading
from pipeline.data_validator import validate_sensor_reading


BROKER = "127.0.0.1:9092"
TOPIC = "atmosync.sensor-readings"


def _print_reading_summary(
    total_generated: int,
    valid_sent: int,
    invalid_rejected: int,
) -> None:
    print(
        "Reading summary: "
        f"total generated={total_generated}, "
        f"valid sent={valid_sent}, "
        f"invalid rejected={invalid_rejected}"
    )


def main() -> int:
    sensor_states = {
        container_id: create_sensor_state() for container_id in CONTAINER_IDS
    }
    total_generated = 0
    valid_sent = 0
    invalid_rejected = 0

    try:
        producer = KafkaProducer(
            bootstrap_servers=BROKER,
            key_serializer=DefaultSerializer(),
            value_serializer=JsonSerializer(),
        )
    except KafkaError as error:
        print(f"Could not connect to Kafka at {BROKER}: {error}", file=sys.stderr)
        _print_reading_summary(total_generated, valid_sent, invalid_rejected)
        return 1

    close_failed = False
    try:
        for reading_number in range(READINGS_PER_CONTAINER):
            for container_id in CONTAINER_IDS:
                reading = generate_reading(
                    container_id,
                    sensor_states[container_id],
                )
                total_generated += 1
                validation_result = validate_sensor_reading(reading)
                if not validation_result["is_valid"]:
                    invalid_rejected += 1
                    errors = "; ".join(validation_result["errors"])
                    print(
                        f"Rejected reading for {container_id}; "
                        f"validation errors: {errors}"
                    )
                    continue

                try:
                    metadata = producer.send(
                        TOPIC,
                        key=container_id,
                        value=reading,
                    ).get(timeout=10)
                except KafkaError as error:
                    print(
                        f"Could not send reading for {container_id}: {error}",
                        file=sys.stderr,
                    )
                    return 1

                valid_sent += 1
                print(
                    f"Sent reading for {container_id} to "
                    f"{metadata.topic} (partition {metadata.partition})"
                )

            if reading_number < READINGS_PER_CONTAINER - 1:
                time.sleep(GENERATION_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\nProducer stopped.")
    finally:
        try:
            producer.close(timeout=10)
        except KafkaError as error:
            print(f"Error closing Kafka producer: {error}", file=sys.stderr)
            close_failed = True
        _print_reading_summary(total_generated, valid_sent, invalid_rejected)

    return 1 if close_failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
