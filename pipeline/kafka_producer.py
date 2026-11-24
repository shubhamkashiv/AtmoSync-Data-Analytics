"""Send simulated sensor readings to the local Kafka broker."""

import json
import sys
import time

from kafka import KafkaProducer
from kafka.errors import KafkaError

from iot_simulator.config import (
    CONTAINER_IDS,
    GENERATION_INTERVAL_SECONDS,
    READINGS_PER_CONTAINER,
)
from iot_simulator.sensor_simulator import create_sensor_state, generate_reading


BROKER = "127.0.0.1:9092"
TOPIC = "atmosync.sensor-readings"


def main() -> int:
    sensor_states = {
        container_id: create_sensor_state() for container_id in CONTAINER_IDS
    }

    try:
        producer = KafkaProducer(
            bootstrap_servers=BROKER,
            key_serializer=lambda key: key.encode("utf-8"),
            value_serializer=lambda reading: json.dumps(reading).encode("utf-8"),
        )
    except KafkaError as error:
        print(f"Could not connect to Kafka at {BROKER}: {error}", file=sys.stderr)
        return 1

    close_failed = False
    try:
        for reading_number in range(READINGS_PER_CONTAINER):
            for container_id in CONTAINER_IDS:
                reading = generate_reading(
                    container_id,
                    sensor_states[container_id],
                )
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

    return 1 if close_failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
